import os
import math
import torch
import numpy as np
from marl.agents import MAPPOActor, MAPPOCritic
from torch.distributions import Categorical
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter
from utils.utils import *
from datetime import datetime
from tqdm import tqdm

def mappo(env, rm,
            episodes=500,
            rollout_len=200,
            ppo_epochs=8,
            mini_batch_size=64,
            clip_eps=0.2,
            lr=3e-4,
            gamma=0.99,
            lam=0.95,
            grad_clip=0.5,
            advantage_norm=True,
            value_noise_std=1.0,
            log_dir="runs",
            exp_name="mappo",
            save_interval=200):
    
    os.makedirs("checkpoints/mappo", exist_ok=True)
    runs_save_path = os.path.join(log_dir, "mappo", f"{exp_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    writer = SummaryWriter(log_dir=runs_save_path)

    # reset env & RM
    env.reset()
    rm.reset()
    num_agents = len(env.robots)

    # ---- dims ----
    obs0 = build_obs_list_from_env(env)
    obs_dim = len(obs0[0])
    state0 = build_state(env)
    state_dim = len(state0)
    action_n = 6

    # create nets
    actors = [MAPPOActor(obs_dim, action_n).to(device) for _ in range(num_agents)]
    critic = MAPPOCritic(state_dim).to(device)

    # optimizers
    actor_params = []
    for a in actors:
        actor_params += list(a.parameters())
    actor_optim = optim.Adam(actor_params, lr=lr)
    critic_optim = optim.Adam(critic.parameters(), lr=lr)

    total_steps = 0

    for ep in tqdm(range(episodes), desc="Training MAPPO"):
        # rollout storage
        rollout = {
            "obs": [],        # list of length T, each is list of per-agent obs numpy arrays
            "states": [],     # list length T, each global state numpy array
            "actions": [],    # list length T, each list of n ints
            "logprobs": [],   # list length T, each list of n floats
            "values": [],     # list length T, scalar float V(s)
            "rewards": [],    # list length T, list of per-agent rewards (length n)
            "dones": []       # list length T, 0/1
        }

        env.reset()
        rm.reset()
        done = False
        ep_reward = 0.0
        steps = 0

        for t in range(rollout_len):
            # get current observations/state
            obs_list = build_obs_list_from_env(env)
            state = build_state(env)

            # tensors
            obs_tensor_list = [torch.tensor(o, dtype=torch.float32, device=device).unsqueeze(0)     # per-agent: (1, obs_dim)
                                for o in obs_list]
            state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)     # (1, state_dim)

            # critic value
            with torch.no_grad():
                value = critic(state_tensor).squeeze().detach()  # scalar tensor

            # sample actions & logprobs per agent
            actions = []
            logps = []
            for i in range(num_agents):
                probs = actors[i](obs_tensor_list[i])   # (1, action_n)
                dist = Categorical(probs)
                a = dist.sample()
                actions.append(int(a.item()))
                logps.append(float(dist.log_prob(a).item()))

            # step env with integer actions
            rewards_env, infos = env.step(actions)
            events = [info.get("status", None) for info in infos]
            rm_rewards, _ = rm.step(events)

            # per-agent reward list
            per_agent_rewards = [(rewards_env[i] if i < len(rewards_env) else 0.0) + (rm_rewards[i] if i < len(rm_rewards) else 0.0)
                                 for i in range(num_agents)]
            
            # store
            rollout["obs"].append(obs_list)
            rollout["states"].append(state)
            rollout["actions"].append(actions)
            rollout["logprobs"].append(logps)
            rollout["values"].append(float(value.item()))
            rollout["rewards"].append(per_agent_rewards)   # list length n
            rollout["dones"].append(0.0)

            ep_reward += sum(per_agent_rewards)
            steps += 1
            total_steps += 1

            # termination check (use same conditions as env._get_state fields)
            st = env._get_state()
            finish_cond = (
                len(st.get("walls_to_distribute", [])) == 0 and
                len(st.get("walls_to_vibrate", [])) == 0 and
                len(st.get("floors_to_distribute", [])) == 0 and
                len(st.get("floors_to_vibrate", [])) == 0 and
                len(st.get("floors_to_level", [])) == 0 and
                len(st.get("floors_to_cover", [])) == 0
            )
            if finish_cond:
                # mark last step done, give bonus to all agents as per design
                rollout["rewards"][-1] = [r + 100.0/num_agents for r in rollout["rewards"][-1]]
                rollout["dones"][-1] = 1.0
                done = True

            if done:
                break

        # convert to tensors
        T = len(rollout["rewards"])
        rewards_agent = torch.tensor(rollout["rewards"], dtype=torch.float32, device=device)  # (T, N)
        dones = torch.tensor(rollout["dones"], dtype=torch.float32, device=device)            # (T,)
        values = torch.tensor(rollout["values"], dtype=torch.float32, device=device)          # (T,)
        if value_noise_std > 0:
                noise = torch.randn_like(values) * value_noise_std
                values = values + noise
        # compute next_value from last state (or zero if terminal)
        if rollout["dones"][-1] == 1.0:
            next_value = torch.tensor(0.0, dtype=torch.float32, device=device)
        else:
            last_state = torch.tensor(rollout["states"][-1], dtype=torch.float32, device=device).unsqueeze(0)
            with torch.no_grad():
                next_value = critic(last_state).squeeze().detach()

        # compute per-agent GAE
        advantages, returns = compute_gae(rewards_agent, values, next_value, dones, gamma=gamma, lam=lam)
        # advantages: (T, N), returns: (T, N)

        # normalize advantages across all agents/time if desired
        if advantage_norm:
            adv_mean = advantages.mean()
            adv_std = advantages.std(unbiased=False) + 1e-8
            advantages = (advantages - adv_mean) / adv_std

        # prepare tensors for PPO update
        old_logprobs = torch.tensor(rollout["logprobs"], dtype=torch.float32, device=device)  # (T, N)
        actions_tensor = torch.tensor(rollout["actions"], dtype=torch.long, device=device)     # (T, N)
        states_tensor = torch.tensor(np.array(rollout["states"], dtype=np.float32), dtype=torch.float32, device=device)  # (T, state_dim)

        # PPO update
        last_actor_loss = 0.0
        last_critic_loss = 0.0
        for _ in range(ppo_epochs):
            idxs = np.arange(T)
            np.random.shuffle(idxs)
            for start in range(0, T, mini_batch_size):
                mb_idx = idxs[start:start+mini_batch_size]
                if len(mb_idx) == 0:
                    continue

                mb_states = states_tensor[mb_idx]                       # (mb, state_dim)
                mb_returns_per_agent = returns[mb_idx]                 # (mb, N)
                mb_adv_per_agent = advantages[mb_idx]                  # (mb, N)
                mb_actions = actions_tensor[mb_idx]                    # (mb, N)
                mb_old_logp = old_logprobs[mb_idx]                     # (mb, N)

                # Critic update: use mean of per-agent returns as target for V(s)
                critic_target = mb_returns_per_agent.reshape(-1)       # (mb*N,)
                mb_states_expand = mb_states.repeat_interleave(num_agents, dim=0)  # (mb*N, state_dim)

                values_pred = critic(mb_states_expand).squeeze()        # (mb*N,)                     # (mb,)
                critic_loss = F.mse_loss(values_pred, critic_target.detach())
                critic_optim.zero_grad()
                critic_loss.backward()
                torch.nn.utils.clip_grad_norm_(critic.parameters(), grad_clip)
                critic_optim.step()
                last_critic_loss = float(critic_loss.item())

                # Actor update: each agent uses its own advantage
                actor_loss_total = 0.0
                for i in range(num_agents):
                    # build obs batch for agent i
                    obs_i = np.array([rollout["obs"][t][i] for t in mb_idx], dtype=np.float32)
                    obs_i = torch.tensor(obs_i, dtype=torch.float32, device=device)  # (mb, obs_dim)
                    probs = actors[i](obs_i)  # (mb, action_n)
                    dist = Categorical(probs)
                    logp_now = dist.log_prob(mb_actions[:, i])  # (mb,)

                    old_lp = mb_old_logp[:, i]
                    ratio = torch.exp(logp_now - old_lp)
                    adv_i = mb_adv_per_agent[:, i]  # (mb,)

                    obj1 = ratio * adv_i
                    obj2 = torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * adv_i
                    actor_loss = -torch.min(obj1, obj2).mean()
                    actor_loss_total += actor_loss

                actor_optim.zero_grad()
                actor_loss_total.backward()
                torch.nn.utils.clip_grad_norm_(actor_params, grad_clip)
                actor_optim.step()
                last_actor_loss = float(actor_loss_total.item())

        # logging
        writer.add_scalar("train/episode_reward", ep_reward, ep+1)
        writer.add_scalar("train/episode_length", steps, ep+1)
        writer.add_scalar("train/actor_loss", last_actor_loss, ep+1)
        writer.add_scalar("train/critic_loss", last_critic_loss, ep+1)
        writer.add_scalar("train/value_mean", values.mean().item(), ep+1)
        writer.add_scalar("train/adv_mean", advantages.mean().item(), ep+1)

        if (ep+1) % 10 == 0:
            print(f"\nEp {ep+1}/{episodes} reward={ep_reward:.2f} steps={steps} (T={T})", flush=True)

        if (ep+1) % save_interval == 0:
            ckpt = {
                "actors": [a.state_dict() for a in actors],
                "critic": critic.state_dict(),
                "episode": ep+1
            }
            torch.save(ckpt, f"checkpoints/mappo/mappo_ep{ep+1}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.pth")

    hparams = {
        "episodes": episodes,
        "rollout_len": rollout_len,
        "ppo_epochs": ppo_epochs,
        "mini_batch_size": mini_batch_size,
        "clip_eps": clip_eps,
        "lr": lr,
        "gamma": gamma,
        "lam": lam,
        "grad_clip": grad_clip,
        "advantage_norm": advantage_norm
    }
    writer.add_hparams(hparams)
    writer.close()
    return actors, critic


def mappo_with_stats(env, rm,
            episodes=500,
            rollout_len=200,
            ppo_epochs=8,
            mini_batch_size=64,
            clip_eps=0.2,
            lr=3e-4,
            gamma=0.99,
            lam=0.95,
            grad_clip=0.5,
            advantage_norm=True,
            value_noise_std=1.0,
            log_dir="runs",
            exp_name="mappo",
            save_interval=200,
            save_path=None,
            stats_callback=None):
    """
    MAPPO 训练函数 - 带统计回调版本
    
    Args:
        stats_callback: 回调函数，每轮训练后调用，接收统计字典参数
                       格式：{"episode": int, "reward": float, "success": bool, "steps": int, ...}
    """
    
    if save_path is None:
        os.makedirs("checkpoints/mappo", exist_ok=True)
    else:
        os.makedirs(save_path, exist_ok=True)
    
    runs_save_path = os.path.join(log_dir, "mappo", f"{exp_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    writer = SummaryWriter(log_dir=runs_save_path)

    # reset env & RM
    env.reset()
    rm.reset()
    num_agents = len(env.robots)

    # ---- dims ----
    obs0 = build_obs_list_from_env(env)
    obs_dim = len(obs0[0])
    state0 = build_state(env)
    state_dim = len(state0)
    action_n = 6

    # create nets
    actors = [MAPPOActor(obs_dim, action_n).to(device) for _ in range(num_agents)]
    critic = MAPPOCritic(state_dim).to(device)

    # optimizers
    actor_params = []
    for a in actors:
        actor_params += list(a.parameters())
    actor_optim = optim.Adam(actor_params, lr=lr)
    critic_optim = optim.Adam(critic.parameters(), lr=lr)

    total_steps = 0
    best_reward = -float('inf')
    
    # 训练统计
    training_stats = []
    success_count = 0
    convergence_episode = None

    for ep in tqdm(range(episodes), desc="Training MAPPO"):
        # rollout storage
        rollout = {
            "obs": [],        # list of length T, each is list of per-agent obs numpy arrays
            "states": [],     # list length T, each global state numpy array
            "actions": [],    # list length T, each list of n ints
            "logprobs": [],   # list length T, each list of n floats
            "values": [],     # list length T, scalar float V(s)
            "rewards": [],    # list length T, list of per-agent rewards (length n)
            "dones": []       # list length T, 0/1
        }

        env.reset()
        rm.reset()
        done = False
        ep_reward = 0.0
        steps = 0

        for t in range(rollout_len):
            # get current observations/state
            obs_list = build_obs_list_from_env(env)
            state = build_state(env)

            # tensors
            obs_tensor_list = [torch.tensor(o, dtype=torch.float32, device=device).unsqueeze(0)     # per-agent: (1, obs_dim)
                                for o in obs_list]
            state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)     # (1, state_dim)

            # critic value
            with torch.no_grad():
                value = critic(state_tensor).squeeze().detach()  # scalar tensor

            # sample actions & logprobs per agent
            actions = []
            logps = []
            for i in range(num_agents):
                probs = actors[i](obs_tensor_list[i])   # (1, action_n)
                dist = Categorical(probs)
                a = dist.sample()
                actions.append(int(a.item()))
                logps.append(float(dist.log_prob(a).item()))

            # step environment
            rewards_env, infos = env.step(actions)
            next_obs_list = build_obs_list_from_env(env)
            next_state = build_state(env)

            # reward machine
            events = [info.get("status", None) for info in infos]
            rm_rewards, _ = rm.step(events)

            # total rewards
            total_rewards = [
                rewards_env[i] + (rm_rewards[i] if i < len(rm_rewards) else 0.0)
                for i in range(num_agents)
            ]
            global_reward = sum(total_rewards)

            # check if done
            st = env._get_state()
            if len(st.get("walls_to_distribute", [])) == 0 and len(st.get("walls_to_vibrate", [])) == 0 and \
               len(st.get("floors_to_distribute", [])) == 0 and len(st.get("floors_to_vibrate", [])) == 0 and \
               len(st.get("floors_to_level", [])) == 0 and len(st.get("floors_to_cover", [])) == 0:
                done = True
                global_reward += 100.0  # success bonus

            # store
            rollout["obs"].append(obs_list)
            rollout["states"].append(state)
            rollout["actions"].append(actions)
            rollout["logprobs"].append(logps)
            rollout["values"].append(value)
            rollout["rewards"].append(total_rewards)
            rollout["dones"].append(1 if done else 0)

            ep_reward += global_reward
            steps += 1
            total_steps += 1

            if done:
                break

        # PPO update
        returns = compute_returns(rollout["rewards"], rollout["dones"], gamma)
        values = rollout["values"]
        advantages = compute_gae(values, returns, rollout["dones"], gamma, lam)

        # flatten data for training
        all_obs = []
        all_states = []
        all_actions = []
        all_old_logp = []
        all_returns = []
        all_adv = []

        for t in range(len(rollout["obs"])):
            for i in range(num_agents):
                all_obs.append(rollout["obs"][t][i])
                all_states.append(rollout["states"][t])
                all_actions.append(rollout["actions"][t][i])
                all_old_logp.append(rollout["logprobs"][t][i])
                all_returns.append(returns[t])
                all_adv.append(advantages[t])

        all_obs = np.array(all_obs, dtype=np.float32)
        all_states = np.array(all_states, dtype=np.float32)
        all_actions = np.array(all_actions, dtype=np.int64)
        all_old_logp = np.array(all_old_logp, dtype=np.float32)
        all_returns = np.array(all_returns, dtype=np.float32)
        all_adv = np.array(all_adv, dtype=np.float32)

        # normalize advantages
        if advantage_norm:
            all_adv = (all_adv - all_adv.mean()) / (all_adv.std() + 1e-8)

        # PPO epochs
        dataset_size = len(all_obs)
        indices = np.arange(dataset_size)
        last_actor_loss = 0.0
        last_critic_loss = 0.0

        for _ in range(ppo_epochs):
            np.random.shuffle(indices)
            for start in range(0, dataset_size, mini_batch_size):
                end = start + mini_batch_size
                mb_idx = indices[start:end]

                # critic update
                states_mb = torch.tensor(all_states[mb_idx], dtype=torch.float32, device=device)
                returns_mb = torch.tensor(all_returns[mb_idx], dtype=torch.float32, device=device).unsqueeze(1)

                values_mb = critic(states_mb)
                critic_loss = F.mse_loss(values_mb, returns_mb)

                critic_optim.zero_grad()
                critic_loss.backward()
                torch.nn.utils.clip_grad_norm_(critic.parameters(), grad_clip)
                critic_optim.step()
                last_critic_loss = float(critic_loss.item())

                # Actor update
                actor_loss_total = 0.0
                for i in range(num_agents):
                    mb_start = i * len(rollout["obs"])
                    mb_end = mb_start + len(rollout["obs"])
                    mb_idx_i = indices[start:end]
                    # filter indices for agent i
                    mb_idx_i = [idx for idx in mb_idx_i if mb_start <= idx < mb_end]
                    if len(mb_idx_i) == 0:
                        continue
                    # adjust indices
                    mb_idx_i = [idx - mb_start for idx in mb_idx_i]

                    obs_i = torch.tensor(all_obs[mb_start + np.array(mb_idx_i)], dtype=torch.float32, device=device)
                    actions_i = torch.tensor(all_actions[mb_start + np.array(mb_idx_i)], dtype=torch.int64, device=device)
                    old_lp_i = torch.tensor(all_old_logp[mb_start + np.array(mb_idx_i)], dtype=torch.float32, device=device)
                    adv_i = torch.tensor(all_adv[mb_start + np.array(mb_idx_i)], dtype=torch.float32, device=device)

                    probs = actors[i](obs_i)
                    dist = Categorical(probs)
                    logp_now = dist.log_prob(actions_i)

                    ratio = torch.exp(logp_now - old_lp_i)
                    obj1 = ratio * adv_i
                    obj2 = torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * adv_i
                    actor_loss = -torch.min(obj1, obj2).mean()
                    actor_loss_total += actor_loss

                if actor_loss_total > 0:
                    actor_optim.zero_grad()
                    actor_loss_total.backward()
                    torch.nn.utils.clip_grad_norm_(actor_params, grad_clip)
                    actor_optim.step()
                    last_actor_loss = float(actor_loss_total.item())

        # logging
        writer.add_scalar("train/episode_reward", ep_reward, ep+1)
        writer.add_scalar("train/episode_length", steps, ep+1)
        writer.add_scalar("train/actor_loss", last_actor_loss, ep+1)
        writer.add_scalar("train/critic_loss", last_critic_loss, ep+1)

        # 检查成功
        success = (ep_reward > 50)  # 简单阈值判断成功
        if success:
            success_count += 1
            if convergence_episode is None:
                convergence_episode = ep + 1
        
        if ep_reward > best_reward:
            best_reward = ep_reward

        # 回调统计
        if stats_callback is not None:
            stat = {
                "episode": ep + 1,
                "reward": float(ep_reward),
                "success": success,
                "steps": steps,
                "avg_value": float(np.mean(values)) if len(values) > 0 else 0,
                "entropy": float(np.mean([np.random.entropy() for _ in range(num_agents)])),  # placeholder
                "actor_loss": last_actor_loss,
                "critic_loss": last_critic_loss
            }
            stats_callback(stat)
            training_stats.append(stat)

        if (ep+1) % 10 == 0:
            print(f"\nEp {ep+1}/{episodes} reward={ep_reward:.2f} steps={steps} (T={T})", flush=True)

        # save checkpoint
        if (ep+1) % save_interval == 0:
            ckpt = {
                "actors": [a.state_dict() for a in actors],
                "critic": critic.state_dict(),
                "episode": ep+1,
                "best_reward": best_reward
            }
            if save_path is None:
                torch.save(ckpt, f"checkpoints/mappo/mappo_ep{ep+1}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.pth")
            else:
                torch.save(ckpt, f"{save_path}/mappo_ep{ep+1}.pth")

    # final save
    final_ckpt = {
        "actors": [a.state_dict() for a in actors],
        "critic": critic.state_dict(),
        "episode": episodes,
        "best_reward": best_reward,
        "training_stats": training_stats
    }
    if save_path is None:
        torch.save(final_ckpt, f"checkpoints/mappo/mappo_final_{datetime.now().strftime('%Y%m%d-%H%M%S')}.pth")
    else:
        torch.save(final_ckpt, f"{save_path}/mappo_final.pth")

    writer.add_hparams({
        "episodes": episodes,
        "rollout_len": rollout_len,
        "ppo_epochs": ppo_epochs,
        "mini_batch_size": mini_batch_size,
        "clip_eps": clip_eps,
        "lr": lr,
        "gamma": gamma,
        "lam": lam,
        "grad_clip": grad_clip
    }, {
        "best_reward": best_reward,
        "success_rate": success_count / episodes,
        "convergence_episode": convergence_episode or episodes
    })
    writer.close()

    final_stats = {
        "final_reward": float(ep_reward),
        "best_reward": float(best_reward),
        "success_rate": success_count / episodes,
        "convergence_episode": convergence_episode,
        "total_steps": total_steps
    }
    
    return final_stats


# def mappo(env, rm, episodes=1000, rollout_len=2048, ppo_epochs=32, mini_batch_size=64, clip_eps=0.2,
#                lr=5e-4, gamma=0.99, lam=0.95, log_dir="runs", exp_name="mappo", save_interval=100):

#     os.makedirs("checkpoints/mappo", exist_ok=True)
#     runs_save_path = os.path.join(log_dir, "mappo", f"{exp_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}")
#     writer = SummaryWriter(log_dir=runs_save_path)

#     env.reset()
#     rm.reset()
#     num_agents = len(env.robots)

#     # ---- dims ----
#     obs_list0 = build_obs_list_from_env(env)
#     obs_dim = len(obs_list0[0])
#     state_dim = len(build_state(env))
#     action_n = 6

#     # ---- networks ----
#     actors = [MAPPOActor(obs_dim, action_n).to(device) for _ in range(num_agents)]
#     critic = MAPPOCritic(state_dim).to(device)

#     # Optimizers
#     actor_optim = optim.Adam([p for a in actors for p in a.parameters()], lr=lr)
#     critic_optim = optim.Adam(critic.parameters(), lr=lr)

#     global_step = 0

#     for ep in tqdm(range(episodes), desc="Training MAPPO"):
#         env.reset(); rm.reset()
#         done = False
#         ep_reward = 0
#         steps = 0

#         rollout_data = {
#             "obs": [],
#             "actions": [],
#             "logprobs": [],
#             "values": [],
#             "rewards": [],
#             "dones": [],
#             "states": [],
#         }

#         # =============================
#         #   Rollout phase
#         # =============================
#         for t in range(rollout_len):
#             obs_list = build_obs_list_from_env(env)
#             state = build_state(env)
#             obs_tensor_list = [torch.tensor(o, dtype=torch.float32, device=device).unsqueeze(0)
#                                for o in obs_list]
#             state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)

#             # get value from critic
#             value = critic(state_tensor).squeeze(0)

#             # select actions for each agent
#             actions = []
#             logprobs = []
#             for i in range(num_agents):
#                 probs = actors[i](obs_tensor_list[i])
#                 dist = Categorical(probs)
#                 act = dist.sample()
#                 actions.append(act.item())
#                 logprobs.append(dist.log_prob(act))

#             # env step
#             rewards_env, infos = env.step(actions)
#             next_obs_list = build_obs_list_from_env(env)
#             next_state = build_state(env)

#             # reward machine
#             events = [info.get("status", None) for info in infos]
#             rm_rewards, _ = rm.step(events)

#             total_rewards = [
#                 rewards_env[i] + (rm_rewards[i] if i < len(rm_rewards) else 0.0)
#                 for i in range(num_agents)
#             ]
#             global_reward = sum(total_rewards) * math.pow(gamma, t)

#             st = env._get_state()
#             if len(st.get("walls_to_distribute", [])) == 0 and len(st.get("walls_to_vibrate", [])) == 0 and  \
#                len(st.get("floors_to_distribute", [])) == 0 and len(st.get("floors_to_vibrate", [])) == 0 and  \
#                len(st.get("floors_to_level", [])) == 0 and len(st.get("floors_to_cover", [])) == 0 :
#                 done = True
#                 global_reward += 100.0  # bonus for finishing task


#             # store batch
#             rollout_data["obs"].append(obs_list)
#             rollout_data["states"].append(state)
#             rollout_data["actions"].append(actions)
#             rollout_data["logprobs"].append([lp.item() for lp in logprobs])
#             rollout_data["values"].append(value.item())
#             rollout_data["rewards"].append(global_reward)
#             rollout_data["dones"].append(done)

#             ep_reward += global_reward

#             obs_list = next_obs_list
#             state = next_state
            
#             steps += 1
#             global_step += 1

#             if done:
#                 break

#         # ==========================================
#         #   Compute GAE for this rollout
#         # ==========================================
#         rewards = torch.tensor(rollout_data["rewards"], dtype=torch.float32, device=device)
#         dones = torch.tensor(rollout_data["dones"], dtype=torch.float32, device=device)
#         values = torch.tensor(rollout_data["values"], dtype=torch.float32, device=device)

#         # last next_value
#         next_state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
#         next_value = critic(next_state_tensor).detach().squeeze(0)
#         next_values = torch.cat([values[1:], next_value], dim=0)

#         advantages, returns = compute_gae(rewards, values, next_values, dones, gamma, lam)

#         # ==========================================
#         #   PPO Update (multiple epochs)
#         # ==========================================
#         T = len(rewards)
#         old_logprobs = torch.tensor(rollout_data["logprobs"], dtype=torch.float32, device=device)
#         actions = torch.tensor(rollout_data["actions"], dtype=torch.long, device=device)

#         for _ in range(ppo_epochs):
#             idxs = np.arange(T)
#             np.random.shuffle(idxs)

#             for start in range(0, T, mini_batch_size):
#                 end = start + mini_batch_size
#                 mb = idxs[start:end]

#                 mb_adv = advantages[mb]
#                 mb_ret = returns[mb]
#                 mb_states = torch.tensor(np.array(rollout_data["states"]), dtype=torch.float32, device=device)[mb]
#                 mb_obs = rollout_data["obs"][0]  # list of per-agent obs, index with mb inside loop

#                 # Critic loss
#                 values_pred = critic(mb_states).squeeze(-1)
#                 critic_loss = F.mse_loss(values_pred, mb_ret)

#                 critic_optim.zero_grad()
#                 critic_loss.backward()
#                 critic_optim.step()

#                 # Actor update (for each agent)
#                 actor_loss_total = 0

#                 for i in range(num_agents):
#                     # collect obs for this agent at mb indices
#                     obs_i = [rollout_data["obs"][t][i] for t in mb]
#                     obs_i = torch.tensor(np.array(obs_i), dtype=torch.float32, device=device)

#                     probs = actors[i](obs_i)
#                     dist = Categorical(probs)
#                     logprobs_now = dist.log_prob(actions[mb, i])

#                     ratio = torch.exp(logprobs_now - old_logprobs[mb, i])
#                     obj1 = ratio * mb_adv
#                     obj2 = torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * mb_adv
#                     actor_loss = -torch.min(obj1, obj2).mean()

#                     actor_loss_total += actor_loss

#                 actor_optim.zero_grad()
#                 actor_loss_total.backward()
#                 actor_optim.step()

#         writer.add_scalar("value", values.mean().item(), ep + 1)
#         writer.add_scalar("episode_reward", ep_reward, ep + 1)
#         writer.add_scalar("episode_length", steps, ep + 1)
#         writer.add_scalar("loss/actor_loss", actor_loss, ep + 1)
#         writer.add_scalar("loss/critic_loss", critic_loss, ep + 1)

#         if (ep + 1) % 10 == 0:
#             print(f"\nEp {ep+1}/{episodes}, reward={ep_reward:.2f}, steps={steps}, done={done}", flush=True)
#             actions_arr = np.array(rollout_data["actions"])  # shape: [steps, num_agents]
#             actions_arr = np.savetxt(runs_save_path + f"/actions_seq_ep{ep+1}.csv",
#                 actions_arr, fmt="%d", delimiter=",")
#             # infos = np.savetxt(runs_save_path + f"/infos_seq_ep{ep+1}.csv",
#             #     np.array([list(info.values()) for info in infos]), fmt="%s", delimiter=",")
            
#             print(f"\nActions sequence saved to actions_seq_ep{ep+1}", flush=True)

#         if (ep + 1) % save_interval == 0:
#             ckpt = {
#                 "actors": [a.state_dict() for a in actors],
#                 "critic": critic.state_dict(),
#                 "num_agents": num_agents,
#                 "obs_dim": obs_dim,
#                 "state_dim": state_dim,
#                 "action_n": action_n,
#                 "steps": steps
#             }
#             torch.save(ckpt, f"checkpoints/mappo/mappo_{datetime.now().strftime('%Y%m%d-%H%M%S')}_ep{ep+1}.pth")

#     writer.close()
#     return actors, critic

# def train_mappo_fixed(
#     env,
#     rm,
#     episodes=1000,
#     rollout_len=1024,
#     ppo_epochs=8,
#     mini_batch_size=64,
#     clip_eps=0.2,
#     lr=3e-4,
#     gamma=0.99,
#     lam=0.95,
#     grad_clip=0.5,
#     warmup_steps=1000,
#     advantage_norm=True,
#     log_dir="runs",
#     exp_name="mappo_fixed",
#     save_interval=100
# ):
#     """
#     完整修正版 MAPPO 训练函数（适配整型动作 env.step(actions)）。
#     依赖：MAPPOActor, MAPPOCritic, build_obs_list_from_env, build_state, compute_gae, device
#     """

#     import os
#     import numpy as np
#     import torch
#     import torch.nn.functional as F
#     import torch.optim as optim
#     from torch.distributions import Categorical
#     from torch.utils.tensorboard import SummaryWriter
#     from datetime import datetime
#     from tqdm import tqdm

#     os.makedirs("checkpoints/mappo", exist_ok=True)
#     runs_save_path = os.path.join(log_dir, "mappo", f"{exp_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}")
#     writer = SummaryWriter(log_dir=runs_save_path)

#     env.reset()
#     rm.reset()
#     num_agents = len(env.robots)

#     # dims
#     obs_list0 = build_obs_list_from_env(env)
#     obs_dim = len(obs_list0[0])
#     state_dim = len(build_state(env))
#     action_n = 6  # 0..5

#     # networks
#     actors = [MAPPOActor(obs_dim, action_n).to(device) for _ in range(num_agents)]
#     critic = MAPPOCritic(state_dim).to(device)

#     # optimizers (separate for actor params vs critic)
#     actor_params = []
#     for a in actors:
#         actor_params += list(a.parameters())
#     actor_optim = optim.Adam(actor_params, lr=lr)
#     critic_optim = optim.Adam(critic.parameters(), lr=lr)

#     global_step = 0
#     total_steps = episodes * rollout_len

#     for ep in tqdm(range(episodes), desc="Training MAPPO"):
#         env.reset(); rm.reset()
#         done = False
#         ep_reward = 0.0
#         steps = 0

#         # rollout storage (lists)
#         rollout = {
#             "obs": [],        # list length T, each element: list of per-agent obs arrays
#             "states": [],     # list length T, each element: global state vector
#             "actions": [],    # list length T, each element: list of ints per agent
#             "logprobs": [],   # list length T, each element: list of logprob floats per agent
#             "values": [],     # list length T, each element: scalar value (critic)
#             "rewards": [],    # list length T, scalar global reward
#             "dones": []       # list length T, 0.0/1.0
#         }

#         # rollout phase
#         for t in range(rollout_len):
#             # get current observations/state
#             obs_list = build_obs_list_from_env(env)    # list of per-agent obs arrays
#             state = build_state(env)                   # global state vector

#             # convert to tensors
#             obs_tensor_list = [torch.tensor(o, dtype=torch.float32, device=device).unsqueeze(0)
#                                for o in obs_list]    # per-agent: (1, obs_dim)
#             state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)  # (1, state_dim)

#             # critic value
#             with torch.no_grad():
#                 value_t = critic(state_tensor).squeeze()   # scalar tensor

#             # sample actions from actors (Categorical on softmax probs)
#             actions = []
#             logps = []
#             for i in range(num_agents):
#                 probs = actors[i](obs_tensor_list[i])   # (1, action_n) - should be probs
#                 dist = Categorical(probs)
#                 a = dist.sample()
#                 actions.append(int(a.item()))
#                 logps.append(float(dist.log_prob(a).item()))

#             # step env directly with integer actions
#             # env.step expects list of ints of length num_agents
#             rewards_env, infos = env.step(actions)
#             next_obs_list = build_obs_list_from_env(env)
#             next_state = build_state(env)

#             # reward machine integration
#             events = [info.get("status", None) for info in infos]
#             rm_rewards, _ = rm.step(events)

#             # compute per-agent rewards and aggregate global reward (sum)
#             per_agent_rewards = [(rewards_env[i] if i < len(rewards_env) else 0.0) + (rm_rewards[i] if i < len(rm_rewards) else 0.0)
#                                  for i in range(num_agents)]
#             global_reward = float(sum(per_agent_rewards))  # scalar

#             # done condition (use env state)
#             st = env._get_state()
#             finish_cond = (
#                 len(st.get("walls_to_distribute", [])) == 0 and
#                 len(st.get("walls_to_vibrate", [])) == 0 and
#                 len(st.get("floors_to_distribute", [])) == 0 and
#                 len(st.get("floors_to_vibrate", [])) == 0 and
#                 len(st.get("floors_to_level", [])) == 0 and
#                 len(st.get("floors_to_cover", [])) == 0
#             )
#             if finish_cond:
#                 done = True
#                 global_reward += 100.0  # finishing bonus

#             # store
#             rollout["obs"].append(obs_list)      # each obs_list: list of per-agent arrays
#             rollout["states"].append(state)
#             rollout["actions"].append(actions)
#             rollout["logprobs"].append(logps)
#             rollout["values"].append(float(value_t.item()))
#             rollout["rewards"].append(global_reward)
#             rollout["dones"].append(1.0 if done else 0.0)

#             ep_reward += global_reward
#             steps += 1
#             global_step += 1

#             # advance
#             if done:
#                 break

#         # compute GAE / returns
#         T = len(rollout["rewards"])
#         rewards_t = torch.tensor(rollout["rewards"], dtype=torch.float32, device=device)   # (T,)
#         dones_t = torch.tensor(rollout["dones"], dtype=torch.float32, device=device)       # (T,)
#         values_t = torch.tensor(rollout["values"], dtype=torch.float32, device=device)     # (T,)

#         # next_value for last state
#         last_state = rollout["states"][-1]
#         last_state_tensor = torch.tensor(last_state, dtype=torch.float32, device=device).unsqueeze(0)
#         with torch.no_grad():
#             next_value = critic(last_state_tensor).squeeze()   # scalar tensor

#         # build next_values aligned with values_t: next_values[t] = values[t+1], last element = next_value
#         next_values = torch.cat([values_t[1:], next_value.unsqueeze(0)], dim=0)    # (T,)

#         # advantages and returns (assume compute_gae returns (advantages, returns))
#         advantages, returns = compute_gae(rewards_t, values_t, next_values, dones_t, gamma, lam)
#         # flatten and to device
#         advantages = advantages.detach()
#         returns = returns.detach()

#         # optional normalization
#         if advantage_norm:
#             adv_mean = advantages.mean()
#             adv_std = advantages.std(unbiased=False) + 1e-8
#             advantages = (advantages - adv_mean) / adv_std

#         # prepare tensors for PPO update
#         old_logprobs = torch.tensor(rollout["logprobs"], dtype=torch.float32, device=device)  # (T, num_agents)
#         actions_tensor = torch.tensor(rollout["actions"], dtype=torch.long, device=device)     # (T, num_agents)
#         states_tensor = torch.tensor(np.array(rollout["states"], dtype=np.float32), dtype=torch.float32, device=device)  # (T, state_dim)

#         # learning rate warmup handling (simple linear schedule applied to optim param_groups)
#         def apply_warmup(step):
#             if warmup_steps <= 0:
#                 return
#             factor = min(1.0, step / max(1, warmup_steps))
#             for g in actor_optim.param_groups:
#                 g['lr'] = lr * factor
#             for g in critic_optim.param_groups:
#                 g['lr'] = lr * factor

#         # PPO update epochs (on-policy)
#         last_actor_loss = 0.0
#         last_critic_loss = 0.0
#         for _ in range(ppo_epochs):
#             idxs = np.arange(T)
#             np.random.shuffle(idxs)
#             for start in range(0, T, mini_batch_size):
#                 mb_idx = idxs[start:start + mini_batch_size]
#                 if len(mb_idx) == 0:
#                     continue

#                 mb_adv = advantages[mb_idx]    # (mb,)
#                 mb_ret = returns[mb_idx]       # (mb,)
#                 mb_states = states_tensor[mb_idx]  # (mb, state_dim)

#                 # critic update
#                 values_pred = critic(mb_states).squeeze(-1)    # (mb,)
#                 critic_loss = F.mse_loss(values_pred, mb_ret)
#                 critic_optim.zero_grad()
#                 critic_loss.backward()
#                 torch.nn.utils.clip_grad_norm_(critic.parameters(), grad_clip)
#                 critic_optim.step()
#                 last_critic_loss = float(critic_loss.item())

#                 # actor update aggregated over agents
#                 actor_loss_total = 0.0
#                 for agent_i in range(num_agents):
#                     # build obs batch for agent_i
#                     obs_i = np.array([rollout["obs"][t][agent_i] for t in mb_idx], dtype=np.float32)  # (mb, obs_dim)
#                     obs_i = torch.tensor(obs_i, dtype=torch.float32, device=device)

#                     probs = actors[agent_i](obs_i)   # (mb, action_n)
#                     dist = Categorical(probs)
#                     logp_now = dist.log_prob(actions_tensor[mb_idx, agent_i])   # (mb,)
#                     old_lp = old_logprobs[mb_idx, agent_i]                       # (mb,)

#                     ratio = torch.exp(logp_now - old_lp)
#                     obj1 = ratio * mb_adv
#                     obj2 = torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * mb_adv
#                     actor_loss = -torch.min(obj1, obj2).mean()
#                     actor_loss_total += actor_loss

#                 actor_optim.zero_grad()
#                 actor_loss_total.backward()
#                 torch.nn.utils.clip_grad_norm_(actor_params, grad_clip)
#                 actor_optim.step()
#                 last_actor_loss = float(actor_loss_total.item())

#                 # apply warmup step scaling to lr (based on global_step)
#                 apply_warmup(global_step)

#         # logging
#         writer.add_scalar("train/value_mean", values_t.mean().item(), ep + 1)
#         writer.add_scalar("train/adv_mean", advantages.mean().item(), ep + 1)
#         writer.add_scalar("train/episode_reward", ep_reward, ep + 1)
#         writer.add_scalar("train/episode_length", steps, ep + 1)
#         writer.add_scalar("train/actor_loss", last_actor_loss, ep + 1)
#         writer.add_scalar("train/critic_loss", last_critic_loss, ep + 1)

#         # periodic saving & action trace
#         if (ep + 1) % 10 == 0:
#             print(f"\nEp {ep+1}/{episodes}, reward={ep_reward:.2f}, steps={steps}, done={done}", flush=True)
#             actions_arr = np.array(rollout["actions"], dtype=np.int32)  # (T, num_agents)
#             np.savetxt(os.path.join(runs_save_path, f"actions_seq_ep{ep+1}.csv"), actions_arr, fmt="%d", delimiter=",")

#         if (ep + 1) % save_interval == 0:
#             ckpt = {
#                 "actors": [a.state_dict() for a in actors],
#                 "critic": critic.state_dict(),
#                 "num_agents": num_agents,
#                 "obs_dim": obs_dim,
#                 "state_dim": state_dim,
#                 "action_n": action_n,
#                 "ep": ep+1
#             }
#             torch.save(ckpt, f"checkpoints/mappo/mappo_{datetime.now().strftime('%Y%m%d-%H%M%S')}_ep{ep+1}.pth")

#     writer.close()
#     return actors, critic
