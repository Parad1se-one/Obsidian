#!/usr/bin/env python3
"""
DQN Baseline 训练脚本 - Easy 难度
独立 DQN (每个智能体一个 Q 网络，无协作)
"""

import os
import sys
import torch
import torch.nn as nn
import torch.nn.utils as nn_utils
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime
from tqdm import tqdm
import numpy as np
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from envs.grid_env import GridAreaEnv
from marl.buffer import ReplayBuffer
from utils.utils import build_obs_list_for_agents, map_action_int_to_env_action, ACTION_STR

# ===================== 配置 =====================

EPISODES = 500
BATCH_SIZE = 64
BUFFER_CAPACITY = 50000
LR = 1e-4
GAMMA = 0.99
WARMUP_STEPS = 5000
GRAD_CLIP = 10.0
SAVE_INTERVAL = 100
SEED = 42
EXP_NAME = "dqn_easy_baseline"

# ε-greedy 参数
EPS_START = 1.0
EPS_END = 0.05
EPS_DECAY = 5e4

# ===================== DQN 网络 =====================

class DQNNetwork(nn.Module):
    def __init__(self, obs_dim, action_n):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_n)
        )
    
    def forward(self, x):
        return self.net(x)

class DQNAgent:
    def __init__(self, obs_dim, action_n, lr=1e-4):
        self.device = torch.device("cpu")
        self.net = DQNNetwork(obs_dim, action_n).to(self.device)
        self.target = DQNNetwork(obs_dim, action_n).to(self.device)
        self.target.load_state_dict(self.net.state_dict())
        self.opt = torch.optim.Adam(self.net.parameters(), lr=lr)
        self.action_n = action_n
    
    def act(self, obs, eps):
        if np.random.rand() < eps:
            return np.random.randint(self.action_n)
        with torch.no_grad():
            obs_t = torch.tensor(obs, dtype=torch.float32).unsqueeze(0).to(self.device)
            q_vals = self.net(obs_t)
            return q_vals.argmax().item()
    
    def update_target(self):
        self.target.load_state_dict(self.net.state_dict())

# ===================== 训练函数 =====================

def train_dqn_easy(episodes=EPISODES, seed=SEED, exp_name=EXP_NAME):
    # 设置随机种子
    torch.manual_seed(seed)
    np.random.seed(seed)
    
    # 创建实验目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    exp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                          "experiments", "easy", f"{exp_name}", timestamp)
    os.makedirs(exp_dir, exist_ok=True)
    
    # 保存配置
    config = {
        "algorithm": {"name": "DQN", "episodes": episodes, "seed": seed},
        "environment": {"difficulty": "easy", "grid_size": "6x6", "num_agents": 4},
        "experiment": {"timestamp": timestamp, "dir": exp_dir}
    }
    with open(os.path.join(exp_dir, "config.json"), "w") as f:
        json.dump(config, f, indent=2)
    
    # 创建日志
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                          "runs", f"{exp_name}_{timestamp}")
    os.makedirs(log_dir, exist_ok=True)
    writer = SummaryWriter(log_dir)
    
    # 初始化环境
    print("=" * 70)
    print("  DQN 训练 - Easy 难度 (Baseline)")
    print("=" * 70)
    print("\n📦 加载 Easy 难度配置...")
    print("   网格大小：6x6")
    print("   机器人数量：4")
    print("   动作空间：6 (UP/DOWN/LEFT/RIGHT/WORK/HOVER)")
    
    env = GridAreaEnv()
    env.reset()
    
    num_agents = len(env.robots)
    obs_list0 = build_obs_list_for_agents(env)
    obs_dim = len(obs_list0[0])
    action_n = len(ACTION_STR)
    
    print(f"\n🎮 初始化环境...")
    print(f"   观察维度：{obs_dim}")
    print(f"   智能体数量：{num_agents}")
    print(f"   动作数量：{action_n}")
    
    # 初始化 DQN agents
    agents = [DQNAgent(obs_dim, action_n, lr=LR) for _ in range(num_agents)]
    buffer = ReplayBuffer(capacity=BUFFER_CAPACITY)
    
    device = torch.device("cpu")
    print(f"\n⚠️  未使用 CUDA (CPU 训练)")
    
    print(f"\n🚀 开始 DQN 训练...")
    print(f"   Episodes: {episodes}")
    print(f"   Batch Size: {BATCH_SIZE}")
    print(f"   Buffer Size: {BUFFER_CAPACITY}")
    print(f"   Learning Rate: {LR}")
    print("-" * 70)
    
    global_step = 0
    update_count = 0
    
    training_stats = []
    
    for ep in tqdm(range(episodes), desc="Training DQN"):
        env.reset()
        obs_list = build_obs_list_for_agents(env)
        done = False
        ep_reward = 0.0
        steps = 0
        
        while not done:
            eps = max(EPS_END, EPS_START - (global_step / EPS_DECAY) * (EPS_START - EPS_END))
            
            # 选择动作
            actions_int = [agents[i].act(obs_list[i], eps) for i in range(num_agents)]
            
            # 执行动作
            env_actions = [map_action_int_to_env_action(i, a, env) for i, a in enumerate(actions_int)]
            rewards, infos = env.step(env_actions)
            next_obs_list = build_obs_list_for_agents(env)
            
            # 计算奖励 (无 RM，仅环境奖励)
            total_rewards = list(rewards)
            
            # 存储到 buffer
            buffer.push(obs_list, actions_int, total_rewards, next_obs_list, False)
            
            obs_list = next_obs_list
            ep_reward += sum(total_rewards)
            steps += 1
            global_step += 1
            
            # 训练更新
            if len(buffer) >= BATCH_SIZE and global_step > WARMUP_STEPS:
                batch = buffer.sample(BATCH_SIZE)
                B = len(batch)
                
                # 采样 batch
                obs_batch = []
                next_obs_batch = []
                for i in range(num_agents):
                    obs_i = np.array([b.obs[i] for b in batch], dtype=np.float32)
                    next_obs_i = np.array([b.next_obs[i] for b in batch], dtype=np.float32)
                    obs_batch.append(torch.tensor(obs_i, dtype=torch.float32, device=device))
                    next_obs_batch.append(torch.tensor(next_obs_i, dtype=torch.float32, device=device))
                
                actions_batch = torch.tensor([b.actions for b in batch], dtype=torch.long, device=device)
                rewards_batch = torch.tensor([b.rewards for b in batch], dtype=torch.float32, device=device)
                done_batch = torch.tensor([float(b.done) for b in batch], dtype=torch.float32, device=device)
                
                # 计算 target (独立 DQN，无协作)
                td_targets = []
                for i in range(num_agents):
                    with torch.no_grad():
                        q_next = agents[i].target(next_obs_batch[i])
                        max_q_next, _ = torch.max(q_next, dim=1)
                    
                    r_i = rewards_batch[:, i]
                    td_target = r_i + (1 - done_batch) * GAMMA * max_q_next
                    td_targets.append(td_target)
                
                # 更新每个 agent
                total_loss = 0.0
                for i in range(num_agents):
                    q_vals = agents[i].net(obs_batch[i])
                    acts_i = actions_batch[:, i].unsqueeze(1)
                    q_taken = q_vals.gather(1, acts_i).squeeze(1)
                    
                    loss = nn.MSELoss()(q_taken, td_targets[i].detach())
                    agents[i].opt.zero_grad()
                    loss.backward()
                    nn_utils.clip_grad_norm_(agents[i].net.parameters(), GRAD_CLIP)
                    agents[i].opt.step()
                    total_loss += loss.item()
                
                update_count += 1
                writer.add_scalar("loss", total_loss / num_agents, update_count)
                writer.add_scalar("epsilon", eps, global_step)
                
                if global_step % 1000 == 0:
                    for ag in agents:
                        ag.update_target()
            
            # 检查终止条件
            st = env._get_state()
            if (len(st.get("walls_to_distribute", [])) == 0 and 
                len(st.get("floors_to_distribute", [])) == 0 and
                len(st.get("floors_to_vibrate", [])) == 0 and
                len(st.get("floors_to_level", [])) == 0 and
                len(st.get("floors_to_cover", [])) == 0):
                done = True
                ep_reward += 100.0  # 完成任务奖励
                break
        
        # 记录 episode 统计
        writer.add_scalar("episode_reward", ep_reward, ep + 1)
        writer.add_scalar("episode_steps", steps, ep + 1)
        
        training_stats.append({
            "episode": ep + 1,
            "reward": ep_reward,
            "steps": steps,
            "success": ep_reward > 0
        })
        
        if (ep + 1) % 10 == 0:
            tqdm.write(f"Ep {ep+1:3d}: reward={ep_reward:7.2f}, steps={steps:3d}")
        
        if (ep + 1) % SAVE_INTERVAL == 0:
            checkpoint = {
                "num_agents": num_agents,
                "obs_dim": obs_dim,
                "action_n": action_n
            }
            for i, ag in enumerate(agents):
                checkpoint[f"agent_{i}"] = ag.net.state_dict()
            
            ckpt_path = os.path.join(exp_dir, "checkpoints", f"dqn_ep{ep+1}.pth")
            os.makedirs(os.path.dirname(ckpt_path), exist_ok=True)
            torch.save(checkpoint, ckpt_path)
            print(f"[Checkpoint] Saved DQN at episode {ep+1}")
    
    # 保存训练统计
    stats_path = os.path.join(exp_dir, "results", "training_stats.csv")
    os.makedirs(os.path.dirname(stats_path), exist_ok=True)
    with open(stats_path, "w") as f:
        f.write("episode,reward,steps,success\n")
        for stat in training_stats:
            f.write(f"{stat['episode']},{stat['reward']:.2f},{stat['steps']},{stat['success']}\n")
    
    # 保存最终指标
    rewards = [s["reward"] for s in training_stats]
    final_metrics = {
        "episodes": episodes,
        "mean_reward": float(np.mean(rewards)),
        "max_reward": float(np.max(rewards)),
        "min_reward": float(np.min(rewards)),
        "std_reward": float(np.std(rewards)),
        "final_reward": float(rewards[-1])
    }
    
    metrics_path = os.path.join(exp_dir, "results", "final_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(final_metrics, f, indent=2)
    
    writer.close()
    
    print("\n" + "=" * 70)
    print("  训练完成!")
    print("=" * 70)
    print(f"\n📊 最终统计:")
    print(f"   平均奖励：{final_metrics['mean_reward']:.2f}")
    print(f"   最高奖励：{final_metrics['max_reward']:.2f}")
    print(f"   最低奖励：{final_metrics['min_reward']:.2f}")
    print(f"   标准差：{final_metrics['std_reward']:.2f}")
    print(f"\n💾 实验目录：{exp_dir}")
    print("=" * 70)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DQN Easy Baseline Training")
    parser.add_argument("--episodes", type=int, default=EPISODES, help="训练集数")
    parser.add_argument("--seed", type=int, default=SEED, help="随机种子")
    parser.add_argument("--exp-name", type=str, default=EXP_NAME, help="实验名称")
    args = parser.parse_args()
    
    train_dqn_easy(episodes=args.episodes, seed=args.seed, exp_name=args.exp_name)
