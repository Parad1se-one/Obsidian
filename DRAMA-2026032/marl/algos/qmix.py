import os
import torch
import math
import torch.nn as nn
import numpy as np
from marl.agents import QMIXAgent
from marl.mixer import Mixer
from torch.utils.tensorboard import SummaryWriter
from marl.buffer import ReplayBuffer
from utils.utils import *
from datetime import datetime
from tqdm import tqdm

def qmix(env, rm, episodes=1000, batch_size=64, buffer_capacity=5000,
               eps_start=0.5, eps_end=0.05, eps_decay=5e-4,
               lr=5e-4, gamma=0.99, log_dir="runs", exp_name="qmix", save_interval=100):
    os.makedirs("checkpoints/qmix", exist_ok=True)
    runs_save_path = os.path.join(log_dir, "qmix", f"{exp_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    writer = SummaryWriter(log_dir=runs_save_path)

    env.reset(); rm.reset()
    num_agents = len(env.robots)

    # build dims
    ## build dims for agents
    obs_list0 = build_obs_list_for_agents(env)
    obs_dim = len(obs_list0[0])

    ## build dims of environment state
    state0 = build_state(env)
    state_dim = len(state0)
    action_n = 6

    # create agents and mixer
    agents = [QMIXAgent(obs_dim, action_n, lr=lr) for _ in range(num_agents)]
    mixer = Mixer(n_agents=num_agents, state_dim=state_dim).to(device)
    target_mixer = Mixer(n_agents=num_agents, state_dim=state_dim).to(device)
    target_mixer.load_state_dict(mixer.state_dict())

    # optimizer: agent nets + mixer params
    params = []
    for ag in agents:
        params += list(ag.net.parameters())
    params += list(mixer.parameters())
    optimizer = torch.optim.Adam(params, lr=lr)

    buffer = ReplayBuffer(capacity=buffer_capacity)

    global_step = 0
    update_count = 0

    for ep in tqdm(range(episodes),desc="Training QMIX"):
        env.reset(); rm.reset()

        obs_list = build_obs_list_for_agents(env)
        state = build_state(env)
        done = False
        ep_reward = 0.0
        steps = 0

        for t in range(4000):
            eps = max(eps_end, eps_start - (global_step / eps_decay) * (eps_start - eps_end))
            # select actions
            actions_int = [agents[i].act(obs_list[i], eps) for i in range(num_agents)]
            rewards_env, infos = env.step(actions_int)
            next_obs_list = build_obs_list_for_agents(env)
            next_state = build_state(env)

            events = [info.get("status", None) for info in infos]
            rm_rewards, _, _ = rm.step(events)
            total_rewards = [(rewards_env[i] if i < len(rewards_env) else 0.0) + (rm_rewards[i] if i < len(rm_rewards) else 0.0) for i in range(num_agents)]

            # Store state in buffer for efficient retrieval during training
            buffer.push(obs_list, actions_int, total_rewards, next_obs_list, False, state=state, next_state=next_state)
            obs_list = next_obs_list
            state = next_state
            ep_reward += sum(total_rewards) * math.pow(gamma, t)
            steps += 1
            global_step += 1

            # training
            if len(buffer) >= batch_size:
                B = batch_size
                # build tensors: per-agent obs/next_obs + state (from buffer, no reconstruction!)
                obs_batch, next_obs_batch, actions_batch, rewards_batch, done_batch, state_batch, next_state_batch = buffer.sample_torch(batch_size, device, return_state=True)

                # compute individual Q-values for current obs, gather taken actions
                q_taken_list = []
                for i in range(num_agents):
                    q_vals = agents[i].net(obs_batch[i])  # (B, action_n)
                    q_taken = q_vals.gather(1, actions_batch[:, i].unsqueeze(1)).squeeze(1)  # (B,)
                    q_taken_list.append(q_taken)
                # stack -> (B, n_agents)
                q_taken_stack = torch.stack(q_taken_list, dim=1)

                # compute current joint Q via mixer (state_batch from buffer - OPTIMIZED!)
                q_tot = mixer(q_taken_stack, state_batch)  # (B,)

                # target: compute max next joint q
                # compute next-agent max q via target networks
                q_next_max_list = []
                for i in range(num_agents):
                    q_next = agents[i].target_q_values(next_obs_batch[i])  # (B, action_n)
                    max_q_next, _ = torch.max(q_next, dim=1)  # (B,)
                    q_next_max_list.append(max_q_next)
                q_next_max_stack = torch.stack(q_next_max_list, dim=1)  # (B, n)
                # next_state_batch from buffer - OPTIMIZED!

                with torch.no_grad():
                    q_tot_next = target_mixer(q_next_max_stack, next_state_batch)  # (B,)

                r_global = rewards_batch.sum(dim=1)  # (B,)
                td_target = r_global + (1 - done_batch) * gamma * q_tot_next  # (B,)

                # loss = MSE(q_tot, td_target)
                loss = nn.MSELoss()(q_tot, td_target.detach())

                optimizer.zero_grad()
                loss.backward()
                # gradient clipping optional
                torch.nn.utils.clip_grad_norm_(list(optimizer.param_groups[0]['params']), 10)
                optimizer.step()

                update_count += 1
                writer.add_scalar("train/loss", loss.item(), update_count)
                writer.add_scalar("train/epsilon", eps, global_step)

                # soft update targets periodically
                if global_step % 1000 == 0:
                    for ag in agents:
                        ag.update_target()
                    target_mixer.load_state_dict(mixer.state_dict())

            st = env._get_state()
            if len(st.get("walls_to_distribute", [])) == 0 and len(st.get("floors_to_distribute", [])) == 0 and \
               len(st.get("floors_to_vibrate", [])) == 0 and len(st.get("floors_to_level", [])) == 0 and \
               len(st.get("floors_to_cover", [])) == 0 and len(st.get("walls_to_vibrate", [])) == 0:
                done = True
                ep_reward += 100.0  # bonus for finishing task
                break


        writer.add_scalar("episode_reward", ep_reward, ep + 1)
        writer.add_scalar("episode_steps", steps, ep + 1)

        if (ep + 1) % save_interval == 0:
            # save full checkpoint (agents + mixer)
            checkpoint = {"num_agents": num_agents, "obs_dim": obs_dim, "state_dim": state_batch.shape[1], "action_n": action_n}
            for i, ag in enumerate(agents):
                checkpoint[f"agent_{i}"] = ag.net.state_dict()
            checkpoint["mixer"] = mixer.state_dict()
            torch.save(checkpoint, f"checkpoints/qmix/qmix_{datetime.now().strftime('%Y%m%d-%H%M%S')}_ep{ep+1}.pth")
            print(f"[Checkpoint] Saved QMIX at episode {ep+1}", flush=True)

        if (ep + 1) % 10 == 0:
            print(f"\nEp {ep+1}/{episodes} reward={ep_reward:.2f} steps={steps}, done={done}", flush=True)
            infos = np.savetxt(runs_save_path + f"/infos_seq_ep{ep+1}.csv",
                np.array([list(info.values()) for info in infos]), fmt="%s", delimiter=",")
            
            print(f"\nActions sequence saved to actions_seq_ep{ep+1}", flush=True)



    # final save
    checkpoint = {"num_agents": num_agents, "obs_dim": obs_dim, "state_dim": state_batch.shape[1], "action_n": action_n}
    for i, ag in enumerate(agents):
        checkpoint[f"agent_{i}"] = ag.net.state_dict()
    checkpoint["mixer"] = mixer.state_dict()
    torch.save(checkpoint, f"checkpoints/qmix/qmix_{datetime.now().strftime('%Y%m%d-%H%M%S')}_final.pth")
    writer.close()
    return agents, mixer