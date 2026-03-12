import os
import torch
import torch.nn as nn
import torch.nn.utils as nn_utils
from marl.agents import DQNAgent
from torch.utils.tensorboard import SummaryWriter
from marl.buffer import ReplayBuffer
from utils.utils import *
from datetime import datetime
from tqdm import tqdm

def dqn_vdn(env, rm, episodes=1000, batch_size=64, buffer_capacity=50000,
                  lr=1e-4, gamma=0.99, log_dir="runs", exp_name="vdn",
                  save_interval=100, warmup_steps=5000, grad_clip=10.0):
    """VDN训练"""
    os.makedirs("checkpoints/vdn", exist_ok=True)
    writer = SummaryWriter(
        log_dir=os.path.join(log_dir, f"{exp_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    )

    num_agents = len(env.robots)
    obs_list0 = build_obs_list_from_env(env)
    obs_dim = len(obs_list0[0])
    action_n = len(ACTION_STR)

    agents = [DQNAgent(obs_dim, action_n, lr=lr) for _ in range(num_agents)]
    buffer = ReplayBuffer(capacity=buffer_capacity)

    eps_start, eps_end, eps_decay = 1.0, 0.05, 5e4
    global_step, update_count = 0, 0

    for ep in tqdm(range(episodes), desc="Training"):
        env.reset()
        rm.reset()
        obs_list = build_obs_list_from_env(env)
        done = False
        ep_reward, steps = 0.0, 0

        while not done:
            eps = max(eps_end, eps_start - (global_step / eps_decay) * (eps_start - eps_end))
            actions_int = [agents[i].act(obs_list[i], eps) for i in range(num_agents)]
            env_actions = [map_action_int_to_env_action(i, a, env) for i, a in enumerate(actions_int)]
            rewards, infos = env.step(env_actions)
            next_obs_list = build_obs_list_from_env(env)

            events = [info.get("status", None) for info in infos]
            rm_rewards, _ = rm.step(events)
            total_rewards = [
                (rewards[i] if i < len(rewards) else 0.0) + (rm_rewards[i] if i < len(rm_rewards) else 0.0)
                for i in range(num_agents)
            ]

            buffer.push(obs_list, actions_int, total_rewards, next_obs_list, False)
            obs_list = next_obs_list
            ep_reward += sum(total_rewards)
            steps += 1
            global_step += 1

            # --- train update ---
            if len(buffer) >= batch_size and global_step > warmup_steps:
                batch = buffer.sample(batch_size)
                obs_batch, next_obs_batch, actions_batch, rewards_batch, done_batch = buffer.sample_torch(batch_size, device)
                
                joint_next_max = torch.zeros(len(batch), device=device)
                for i in range(num_agents):
                    q_next = agents[i].target(next_obs_batch[i])
                    max_q_next, _ = torch.max(q_next, dim=1)
                    joint_next_max += max_q_next

                r_global = rewards_batch.sum(dim=1)
                td_target = r_global + (1 - done_batch) * gamma * joint_next_max

                total_loss = 0.0
                for i in range(num_agents):
                    q_vals = agents[i].net(obs_batch[i])
                    acts_i = actions_batch[:, i].unsqueeze(1)
                    q_taken = q_vals.gather(1, acts_i).squeeze(1)
                    loss = nn.MSELoss()(q_taken, td_target.detach())
                    agents[i].opt.zero_grad()
                    loss.backward()
                    # --- 梯度裁剪 ---
                    nn_utils.clip_grad_norm_(agents[i].net.parameters(), grad_clip)
                    agents[i].opt.step()
                    total_loss += loss.item()

                update_count += 1
                writer.add_scalar("loss", total_loss / num_agents, update_count)
                writer.add_scalar("epsilon", eps, global_step)

                if global_step % 1000 == 0:
                    for ag in agents:
                        ag.update_target()

            

            st = env._get_state()
            if len(st.get("walls_to_build", [])) == 0:
                done = True

        writer.add_scalar("episode_reward", ep_reward, ep + 1)

        if (ep + 1) % save_interval == 0:
            for i, ag in enumerate(agents):
                torch.save(ag.net.state_dict(), f"checkpoints/vdn/agent{i}_{datetime.now().strftime('%Y%m%d-%H%M%S')}_ep{ep+1}.pth")
            print(f"[Checkpoint] Saved at episode {ep+1}", flush=True)

        if (ep + 1) % 10 == 0:
            print(f"\nEp {ep+1}/{episodes} reward={ep_reward:.2f} steps={steps}", flush=True)

    # 保存最终模型
    for i, ag in enumerate(agents):
        torch.save(ag.net.state_dict(), f"checkpoints/vdn/agent{i}_{datetime.now().strftime('%Y%m%d-%H%M%S')}_final.pth")
    writer.close()
    return agents