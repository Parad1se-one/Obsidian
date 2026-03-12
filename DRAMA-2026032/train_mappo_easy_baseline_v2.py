#!/usr/bin/env python3
"""
MAPPO 训练脚本 - Easy 难度
训练 Multi-Agent PPO 在 Easy 难度环境 (2 个施工单元)

用法:
    python train_mappo_easy.py              # 默认训练
    python train_mappo_easy.py --episodes 1000  # 指定训练轮数
    python train_mappo_easy.py --seed 123   # 指定随机种子
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

# Import DRAMA components
from configs.difficulty_loader import load_config
from envs.grid_env import GridAreaEnv
from marl.algos.mappo import mappo

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
            "name": "MAPPO",
            "episodes": args.episodes,
            "rollout_len": args.rollout_len,
            "ppo_epochs": args.ppo_epochs,
            "mini_batch_size": args.mini_batch_size,
            "clip_eps": args.clip_eps,
            "learning_rate": args.lr,
            "gamma": args.gamma,
            "lam": args.lam,
            "grad_clip": args.grad_clip
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
    
    # 同时保存为 CSV 格式方便分析
    csv_file = exp_dir / "results" / "training_stats.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("episode,reward,success,steps,avg_value,entropy\n")
        for stat in training_stats:
            f.write(f"{stat['episode']},{stat['reward']:.2f},{stat['success']},{stat['steps']},{stat['avg_value']:.4f},{stat['entropy']:.4f}\n")

def save_final_metrics(exp_dir, metrics):
    """保存最终评估指标"""
    metrics_file = exp_dir / "results" / "final_metrics.json"
    with open(metrics_file, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

def train_mappo_easy(args):
    """训练 MAPPO - Easy 难度"""
    
    print("\n" + "="*70)
    print("  MAPPO 训练 - Easy 难度")
    print("="*70)
    
    # 设置随机种子
    set_seed(args.seed)
    
    # 加载难度配置
    print(f"\n📦 加载 Easy 难度配置...")
    config, meta = load_config('easy')
    print(f"   施工单元：{meta['total_grids']} 个")
    print(f"   网格大小：{config['grid_width']}x{config['grid_height']}")
    print(f"   机器人数量：{config['num_robots']}")
    
    # 创建实验目录
    exp_dir = create_experiment_dir(args.exp_name, 'easy')
    print(f"\n💾 实验目录：{exp_dir}")
    
    # 保存配置
    save_experiment_config(exp_dir, config, meta, args)
    
    # 初始化环境
    print(f"\n🎮 初始化环境...")
    env = GridAreaEnv(config)
    
    # 打印环境信息
    env.reset()
    print(f"   初始状态：{len(env.floors_to_distribute)} 个待施工单元")
    print(f"   动作空间：6 (UP/DOWN/LEFT/RIGHT/WORK/HOVER)")
    print(f"   ⚠️  Baseline 版本：无 Reward Machine")
    
    # 设置 CUDA
    if torch.cuda.is_available():
        print(f"\n🚀 使用 CUDA: {torch.cuda.get_device_name(0)}")
    else:
        print(f"\n⚠️  未使用 CUDA (CPU 训练)")
    
    print(f"\n🚀 开始训练...")
    print(f"   Episodes: {args.episodes}")
    print(f"   Rollout Length: {args.rollout_len}")
    print(f"   PPO Epochs: {args.ppo_epochs}")
    print(f"   Learning Rate: {args.lr}")
    print("-"*70)
    
    # 训练统计
    training_stats = []
    best_reward = -float('inf')
    success_count = 0
    
    start_time = time.time()
    
    # 调用 MAPPO 训练 (Easy 难度专用版本)
    from marl.algos.mappo_easy import mappo_train_easy
    
    try:
        # Baseline: 不传入 rm (使用环境原始奖励)
        final_stats = mappo_train_easy(
            env, None,
            episodes=args.episodes,
            rollout_len=args.rollout_len,
            ppo_epochs=args.ppo_epochs,
            mini_batch_size=args.mini_batch_size,
            clip_eps=args.clip_eps,
            lr=args.lr,
            gamma=args.gamma,
            lam=args.lam,
            grad_clip=args.grad_clip,
            advantage_norm=True,
            log_dir=str(exp_dir / "logs"),
            exp_name=args.exp_name,
            save_interval=args.save_interval,
            save_path=str(exp_dir / "checkpoints"),
            stats_callback=lambda stat: training_stats.append(stat)
        )
        
        # 计算最终指标
        training_time = time.time() - start_time
        final_metrics = {
            "total_training_time": training_time,
            "total_episodes": args.episodes,
            "success_rate": success_count / args.episodes if args.episodes > 0 else 0,
            "best_reward": best_reward,
            "final_reward": final_stats.get("final_reward", 0) if final_stats else 0,
            "convergence_episode": final_stats.get("convergence_episode", None) if final_stats else None
        }
        
        # 保存结果
        save_training_results(exp_dir, training_stats)
        save_final_metrics(exp_dir, final_metrics)
        
        print("\n" + "="*70)
        print("  训练完成!")
        print("="*70)
        print(f"\n📊 训练统计:")
        print(f"   总耗时：{training_time/60:.1f} 分钟")
        print(f"   总轮数：{args.episodes}")
        print(f"   最佳奖励：{best_reward:.2f}")
        print(f"   成功率：{final_metrics['success_rate']*100:.1f}%")
        
        print(f"\n💾 结果已保存:")
        print(f"   配置：{exp_dir / 'config.json'}")
        print(f"   训练统计：{exp_dir / 'results' / 'training_stats.json'}")
        print(f"   最终指标：{exp_dir / 'results' / 'final_metrics.json'}")
        print(f"   模型检查点：{exp_dir / 'checkpoints'}/")
        print(f"   TensorBoard 日志：{exp_dir / 'logs'}/")
        
    except Exception as e:
        print(f"\n❌ 训练出错：{e}")
        import traceback
        traceback.print_exc()
        return None
    
    print("\n" + "="*70 + "\n")
    
    return exp_dir

def main():
    parser = argparse.ArgumentParser(description="MAPPO 训练 - Easy 难度")
    
    # 训练参数
    parser.add_argument("--episodes", type=int, default=500, help="训练轮数")
    parser.add_argument("--rollout_len", type=int, default=200, help="rollout 长度")
    parser.add_argument("--ppo_epochs", type=int, default=8, help="PPO epochs")
    parser.add_argument("--mini_batch_size", type=int, default=64, help="Mini batch size")
    parser.add_argument("--clip_eps", type=float, default=0.2, help="PPO clip epsilon")
    parser.add_argument("--lr", type=float, default=3e-4, help="学习率")
    parser.add_argument("--gamma", type=float, default=0.99, help="折扣因子")
    parser.add_argument("--lam", type=float, default=0.95, help="GAE lambda")
    parser.add_argument("--grad_clip", type=float, default=0.5, help="梯度裁剪")
    
    # 实验参数
    parser.add_argument("--exp_name", type=str, default="mappo_easy", help="实验名称")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="随机种子")
    parser.add_argument("--save_interval", type=int, default=100, help="模型保存间隔")
    
    args = parser.parse_args()
    
    train_mappo_easy(args)

if __name__ == "__main__":
    main()
