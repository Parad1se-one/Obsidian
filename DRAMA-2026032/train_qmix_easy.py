#!/usr/bin/env python3
"""
QMIX 训练脚本 - Easy 难度
训练 QMIX (Value-based Multi-Agent RL) 在 Easy 难度环境

QMIX vs MAPPO:
- QMIX: Value-based, 学习 Q 函数，单调混合
- MAPPO: Policy-based, 直接学习策略

用法:
    python train_qmix_easy.py              # 默认训练
    python train_qmix_easy.py --episodes 1000  # 指定训练轮数
    python train_qmix_easy.py --seed 123   # 指定随机种子
"""

import os
import sys
import argparse
import json
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import torch
import numpy as np
import random
from tqdm import tqdm

# Import DRAMA components
from configs.difficulty_loader import load_config
from envs.grid_env import GridAreaEnv
from marl.algos.qmix import qmix as qmix_train
from reward_machines.reward_machine_enhanced import EnhancedRewardMachine

# Default SEED
DEFAULT_SEED = 42

def set_seed(seed):
    """设置随机种子"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def create_experiment_dir(exp_name, difficulty):
    """创建实验结果目录"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    exp_dir = Path(__file__).parent / "experiments" / difficulty / exp_name / timestamp
    exp_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建子目录
    (exp_dir / "checkpoints").mkdir(exist_ok=True)
    (exp_dir / "logs").mkdir(exist_ok=True)
    (exp_dir / "results").mkdir(exist_ok=True)
    
    return exp_dir

def save_experiment_config(exp_dir, config, meta, args):
    """保存实验配置"""
    config_dict = {
        "experiment": {
            "name": args.exp_name,
            "timestamp": datetime.now().isoformat(),
            "difficulty": meta["level"],
            "seed": args.seed
        },
        "environment": {
            "grid_size": f"{config['grid_width']}x{config['grid_height']}",
            "total_grids": meta["total_grids"],
            "num_robots": config["num_robots"],
            "obstacles": len(config["obstacles"]["static"]),
            "description": meta["description"]
        },
        "algorithm": {
            "name": "QMIX",
            "episodes": args.episodes,
            "buffer_size": args.buffer_size,
            "batch_size": args.batch_size,
            "learning_rate": args.lr,
            "gamma": args.gamma,
            "target_update": args.target_update
        },
        "hardware": {
            "cuda": torch.cuda.is_available(),
            "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "pytorch_version": torch.__version__
        }
    }
    
    config_file = exp_dir / "config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config_dict, f, indent=2, ensure_ascii=False)
    
    return config_dict

def save_training_results(exp_dir, training_stats):
    """保存训练结果"""
    results_file = exp_dir / "results" / "training_stats.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(training_stats, f, indent=2, ensure_ascii=False)

def train():
    parser = argparse.ArgumentParser(description='QMIX Training - Easy Difficulty')
    parser.add_argument('--episodes', type=int, default=500, help='Number of training episodes')
    parser.add_argument('--rollout-len', type=int, default=200, help='Rollout length per episode')
    parser.add_argument('--buffer-size', type=int, default=5000, help='Replay buffer size')
    parser.add_argument('--batch-size', type=int, default=64, help='Training batch size')
    parser.add_argument('--lr', type=float, default=1e-4, help='Learning rate')
    parser.add_argument('--gamma', type=float, default=0.99, help='Discount factor')
    parser.add_argument('--epsilon-start', type=float, default=1.0, help='Initial epsilon for exploration')
    parser.add_argument('--epsilon-end', type=float, default=0.05, help='Final epsilon')
    parser.add_argument('--epsilon-decay', type=float, default=50000, help='Epsilon decay steps')
    parser.add_argument('--target-update', type=int, default=200, help='Target network update frequency')
    parser.add_argument('--seed', type=int, default=DEFAULT_SEED, help='Random seed')
    parser.add_argument('--exp-name', type=str, default='qmix_easy_baseline', help='Experiment name')
    parser.add_argument('--save-interval', type=int, default=50, help='Save checkpoint interval')
    
    args = parser.parse_args()
    set_seed(args.seed)
    
    # Load Easy difficulty config
    print("="*70)
    print("  QMIX 训练 - Easy 难度 (Baseline)")
    print("="*70)
    
    config, meta = load_config('easy')
    print(f"\n📦 加载 Easy 难度配置...")
    print(f"   施工单元：{meta['total_grids']} 个")
    print(f"   网格大小：{config['grid_width']}x{config['grid_height']}")
    print(f"   机器人数量：{config['num_robots']}")
    print(f"   障碍物：{len(config['obstacles']['static'])} 个")
    
    # Create experiment directory
    exp_dir = create_experiment_dir(args.exp_name, 'easy')
    print(f"\n💾 实验目录：{exp_dir}")
    
    # Save config
    save_experiment_config(exp_dir, config, meta, args)
    
    
    # Initialize environment
    print(f"\n🎮 初始化环境...")
    env = GridAreaEnv(config=config)
    rm = EnhancedRewardMachine(config["task_dependencies"], num_agents=config["num_robots"])
    
    initial_cells = config.get('floors', {}).get('to_distribute', [])
    print(f"   初始状态：{len(initial_cells)} 个待施工单元")
    print(f"   动作空间：6 (UP/DOWN/LEFT/RIGHT/WORK/HOVER)")
    
    # Set CUDA
    if torch.cuda.is_available():
        print(f"\n🚀 使用 CUDA: {torch.cuda.get_device_name(0)}")
    else:
        print(f"\n⚠️  未使用 CUDA (CPU 训练)")
    
    print(f"\n🚀 开始 QMIX 训练...")
    print(f"   Episodes: {args.episodes}")
    print(f"   Batch Size: {args.batch_size}")
    print(f"   Buffer Size: {args.buffer_size}")
    print(f"   Learning Rate: {args.lr}")
    print("-"*70)
    
    # Call QMIX training function
    qmix_train(
        env, rm,
        episodes=args.episodes,
        batch_size=args.batch_size,
        buffer_capacity=args.buffer_size,
        eps_start=args.epsilon_start,
        eps_end=args.epsilon_end,
        eps_decay=args.epsilon_decay,
        lr=args.lr,
        gamma=args.gamma,
        exp_name=args.exp_name,
        save_interval=args.save_interval
    )

if __name__ == "__main__":
    train()
