import os
import math
import torch
import numpy as np
from marl.agents import RecurrentMAPPOActor, MAPPOCritic
from torch.distributions import Categorical
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter
from utils.utils import *
from datetime import datetime
from tqdm import tqdm

def r_ippo(env, rm,
         episodes=500,
         rollout_len=2000,
         ppo_epochs=4,
         mini_batch_size=2048,
         chunk_len=10,
         clip_eps=0.2,
         lr=3e-4,
         gamma=0.99,
         lam=0.95,
         grad_clip=0.5,
         advantage_norm=True,
         value_noise_std=2.0,
         hidden_dim=64,
         log_dir="runs",
         exp_name="r_ippo",
         save_interval=200):
    
    os.makedirs("checkpoints/r_ippo", exist_ok=True)
    runs_save_path = os.path.join(log_dir, "r_ippo", f"{exp_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    writer = SummaryWriter(log_dir=runs_save_path)

    env.reset()
    rm.reset()
    num_agents = len(env.robots)


    obs0 = build_obs_list_for_agents(env)
    obs_dim = len(obs0[0])
    action_n = 6
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # --- Change 1: 使用 Recurrent Actor ---
    # 只有 Actor 使用 GRU，Critic 依然保持全连接
    actors = [RecurrentMAPPOActor(obs_dim, action_n, hidden_dim=hidden_dim).to(device) for _ in range(num_agents)]
    critics = [MAPPOCritic(obs_dim).to(device) for _ in range(num_agents)] 
    
    actor_optims = [optim.Adam(a.parameters(), lr=lr) for a in actors]
    critic_optims = [optim.Adam(c.parameters(), lr=lr) for c in critics]

    warmup_steps = np.zeros(num_agents)

    for ep in tqdm(range(episodes), desc="Training Recurrent IPPO"):
        # 初始化 rollout buffer
        rollout = [{
            "obs": [],
            "actions": [],
            "logprobs": [],
            "values": [],
            "rewards": [],
            "dones": [],
            "hidden_states": [] # 新增：存储每一步的 hidden state (用于 chunk 初始状态)
        } for _ in range(num_agents)]

        env.reset()
        rm.reset()
        done = False
        ep_reward = 0.0
        steps = 0
        final_reward = np.zeros(num_agents, dtype=np.int32)

        # --- Change 2: 初始化 Hidden States ---
        # shape: (1, num_agents, hidden_dim) - 假设 GRU 只有 1 层
        actor_hidden = torch.randn(1, num_agents, hidden_dim).to(device)

        for t in range(rollout_len):
            obs_list = build_obs_list_for_agents(env)
            actions = np.zeros(num_agents, dtype=np.int32) + 5
            logps = []
            values = []
            per_agent_rewards = []
            
            # 暂存当前 step 各个智能体的 hidden state 用于存入 buffer (copy 以防后续修改)
            step_hiddens = actor_hidden.detach().cpu().numpy() # (1, num_agents, hidden)

            # 每个智能体独立决策
            for i in range(num_agents):
                # Obs: (1, 1, obs_dim) -> Batch=1, Seq=1
                obs_tensor = torch.tensor(obs_list[i], dtype=torch.float32, device=device).unsqueeze(0).unsqueeze(0)
                
                # 取出当前智能体的 hidden state: (1, 1, hidden_dim)
                h_in = actor_hidden[:, i:i+1, :].contiguous()

                with torch.no_grad():
                    # Critic (Feed Forward): input (1, obs_dim)
                    value = critics[i](obs_tensor.squeeze(1)).squeeze().detach()
                    if value_noise_std > 0:
                        noise = torch.randn_like(value) * value_noise_std
                        value += noise
                    
                    # Actor (Recurrent): returns logits and new_hidden
                    probs_logits, h_out = actors[i](obs_tensor, h_in)
                    dist = Categorical(logits=probs_logits) # 注意这里是 logits
                    a = dist.sample()
                    
                    actions[i] = int(a.item())
                    logps.append(float(dist.log_prob(a).item()))
                    values.append(float(value.item()))
                    
                    # 更新当前智能体的 hidden state
                    actor_hidden[:, i, :] = h_out.squeeze(1)

            # Environment Step
            rewards_env, infos = env.step(actions)
            events = [info.get("status", None) for info in infos]
            rm_rewards, _, _ = rm.step(events)
            
            # Calculate Rewards
            for i in range(num_agents):
                r = (rewards_env[i] if i < len(rewards_env) else 0.0) + \
                    (rm_rewards[i] if i < len(rm_rewards) else 0.0)
                per_agent_rewards.append(r)

            # Check Done (Logic unchanged)
            st = env._get_state()
            finish_cond = [
                (len(st.get("walls_to_distribute", [])) == 0 and len(st.get("floors_to_distribute", [])) == 0),
                (len(st.get("walls_to_vibrate", [])) == 0 and len(st.get("floors_to_vibrate", [])) == 0 and len(st.get("walls_to_distribute", [])) == 0 and len(st.get("floors_to_distribute", [])) == 0),
                (len(st.get("floors_to_level", [])) == 0 and len(st.get("walls_to_vibrate", [])) == 0 and len(st.get("floors_to_vibrate", [])) == 0 and len(st.get("walls_to_distribute", [])) == 0 and len(st.get("floors_to_distribute", [])) == 0),
                (len(st.get("floors_to_cover", [])) == 0 and len(st.get("floors_to_level", [])) == 0 and len(st.get("walls_to_vibrate", [])) == 0 and len(st.get("floors_to_vibrate", [])) == 0 and len(st.get("walls_to_distribute", [])) == 0 and len(st.get("floors_to_distribute", [])) == 0),
            ]
            
            for idx in range(len(finish_cond)):
                if finish_cond[idx] and final_reward[idx] == 0:
                    per_agent_rewards[idx] += 2000000.0 / steps  # 提前完成奖励越高
                    final_reward[idx] = 1
            done = all(finish_cond)

            # 存储数据
            for i in range(num_agents):
                rollout[i]["obs"].append(obs_list[i])
                rollout[i]["actions"].append(actions[i])
                rollout[i]["logprobs"].append(logps[i])
                rollout[i]["values"].append(values[i])
                rollout[i]["rewards"].append(per_agent_rewards[i])
                rollout[i]["dones"].append(1.0 if done else 0.0)
                # 存储执行该动作之前的 hidden state
                rollout[i]["hidden_states"].append(step_hiddens[:, i, :]) 

            ep_reward += sum(per_agent_rewards)
            steps += 1

            if done:
                break
        
        # --- Training Loop ---
        for i in range(num_agents):
            # 整理数据为 Tensor
            obs_arr = torch.tensor(np.array(rollout[i]["obs"]), dtype=torch.float32, device=device)
            actions_arr = torch.tensor(rollout[i]["actions"], dtype=torch.long, device=device)
            logprobs_arr = torch.tensor(rollout[i]["logprobs"], dtype=torch.float32, device=device)
            values_arr = torch.tensor(rollout[i]["values"], dtype=torch.float32, device=device)
            rewards_arr = torch.tensor(rollout[i]["rewards"], dtype=torch.float32, device=device)
            dones_arr = torch.tensor(rollout[i]["dones"], dtype=torch.float32, device=device) # (T,) 1 for done
            hidden_arr = torch.tensor(np.array(rollout[i]["hidden_states"]), dtype=torch.float32, device=device).squeeze(1) # (T, 1, H) -> (T, 1, H) -> 实际上我们需要 (T, H) 方便处理，但 GRU 需要 (1, B, H)

            # GAE 计算
            if rollout[i]["dones"][-1] == 1.0:
                next_value = torch.tensor(0.0, dtype=torch.float32, device=device)
            else:
                next_obs = torch.tensor(rollout[i]["obs"][-1], dtype=torch.float32, device=device).unsqueeze(0)
                with torch.no_grad():
                    next_value = critics[i](next_obs).squeeze().detach()
            
            advantages, returns = compute_gae(
                rewards_arr.unsqueeze(1), values_arr, next_value, dones_arr, gamma=gamma, lam=lam
            )
            advantages = advantages.squeeze(1)
            returns = returns.squeeze(1)
            
            if advantage_norm:
                adv_mean = advantages.mean()
                adv_std = advantages.std(unbiased=False) + 1e-8
                advantages = (advantages - adv_mean) / adv_std

            # --- Change 3: 序列分块 (Chunking) ---
            # 我们需要丢弃最后不足 chunk_len 的数据，或者 padding。这里选择丢弃以保持简单。
            T_total = len(rewards_arr)
            num_chunks = T_total // chunk_len
            cutoff = num_chunks * chunk_len
            
            # Reshape into (Num_Chunks, Chunk_Len, ...)
            # Obs: (Batch, Seq, Dim)
            b_obs = obs_arr[:cutoff].view(num_chunks, chunk_len, -1)
            b_actions = actions_arr[:cutoff].view(num_chunks, chunk_len)
            b_logprobs = logprobs_arr[:cutoff].view(num_chunks, chunk_len)
            b_advantages = advantages[:cutoff].view(num_chunks, chunk_len)
            b_returns = returns[:cutoff].view(num_chunks, chunk_len)
            b_dones = dones_arr[:cutoff].view(num_chunks, chunk_len)
            
            # Hidden States: 我们只需要每个 chunk 开始时的 hidden state
            # hidden_arr shape: (T, 1, H) -> (Num_Chunks, Chunk_Len, 1, H)
            # 取出每个 chunk 第 0 个时间步的 hidden: (Num_Chunks, 1, H)
            # GRU init hidden 需要 permute 为 (1, Num_Chunks, H)
            b_hiddens = hidden_arr[:cutoff].view(num_chunks, chunk_len, 1, hidden_dim)[:, 0, :, :]
            b_hiddens = b_hiddens.permute(1, 0, 2).contiguous() # (1, Num_Chunks, H)

            # 生成索引并打乱 (针对 Chunks)
            chunk_idxs = np.arange(num_chunks)
            
            for _ in range(ppo_epochs):
                np.random.shuffle(chunk_idxs)
                
                for start in range(0, num_chunks, mini_batch_size):
                    mb_idx = chunk_idxs[start:start+mini_batch_size]
                    if len(mb_idx) == 0: continue

                    # 获取 Mini-batch 数据
                    # obs: (B, Seq, Dim)
                    mb_obs = b_obs[mb_idx] 
                    mb_actions = b_actions[mb_idx]
                    mb_old_logp = b_logprobs[mb_idx]
                    mb_adv = b_advantages[mb_idx]
                    mb_ret = b_returns[mb_idx]
                    mb_dones = b_dones[mb_idx] # (B, Seq)
                    
                    # Hidden: (1, B, H)
                    mb_init_hidden = b_hiddens[:, mb_idx, :] 
                    
                    # --- Actor Update (Recurrent) ---
                    # 生成 mask: 1.0 if not done, 0.0 if done
                    # 注意：dones_arr 存的是 "Done=1", 我们通常需要 "Mask=1-Done"
                    # 且如果 t 时刻 done，t+1 时刻 hidden 应清零。
                    mb_masks = 1.0 - mb_dones.unsqueeze(-1) # (B, Seq, 1)

                    # Forward pass with TBPTT logic inside
                    # 这里的 mb_init_hidden 是该 chunk 起始时刻的 hidden，是从 rollout 中记录下来的，
                    # 相当于截断了反向传播（因为我们不会 backprop 到上一个 chunk）
                    probs_logits, _ = actors[i](mb_obs, mb_init_hidden, masks=mb_masks)
                    
                    dist = Categorical(logits=probs_logits)
                    logp_now = dist.log_prob(mb_actions) # (B, Seq)
                    entropy = dist.entropy().mean()
                    
                    ratio = torch.exp(logp_now - mb_old_logp)
                    obj1 = ratio * mb_adv
                    obj2 = torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * mb_adv
                    
                    # Loss 需要在维度上取平均
                    actor_loss = -torch.min(obj1, obj2).mean() - 0.01 * entropy

                    actor_optims[i].zero_grad()
                    actor_loss.backward()
                    torch.nn.utils.clip_grad_norm_(actors[i].parameters(), grad_clip)
                    actor_optims[i].step()

                    # --- Critic Update (Feed Forward) ---
                    # Critic 不使用 RNN，直接展平 (Batch * Seq, Dim) 进行处理
                    flat_obs = mb_obs.view(-1, obs_dim)
                    flat_ret = mb_ret.view(-1)
                    
                    values_pred = critics[i](flat_obs).squeeze()
                    critic_loss = F.mse_loss(values_pred, flat_ret)
                    
                    critic_optims[i].zero_grad()
                    critic_loss.backward()
                    torch.nn.utils.clip_grad_norm_(critics[i].parameters(), grad_clip)
                    critic_optims[i].step()

            writer.add_scalar(f"agent{i}/actor_loss", actor_loss.item(), ep+1)
            writer.add_scalar(f"agent{i}/critic_loss", critic_loss.item(), ep+1)
            writer.add_scalar(f"agent{i}/average_return", b_returns.mean().item(), ep+1)

        writer.add_scalar("train/episode_reward", ep_reward, ep+1)
        writer.add_scalar("train/episode_length", steps, ep+1)
        
        if (ep+1) % 10 == 0:
            print(f"\nEp {ep+1}/{episodes} reward={ep_reward:.2f} steps={steps}", flush=True)

        if (ep+1) % save_interval == 0:
            ckpt = {
                "actors": [a.state_dict() for a in actors],
                "critics": [c.state_dict() for c in critics],
                "episode": ep+1
            }
            torch.save(ckpt, f"checkpoints/r_ippo/r_ippo_ep{ep+1}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.pth")
            
    writer.close()
    return actors, critics