#!/usr/bin/env python3
"""
MAPPO 训练脚本 - Easy 难度 (增强版 Reward Machine)

使用增强的 Reward Machine 进行奖励 shaping，支持:
- 任务完成奖励
- 协作奖励
- 进度奖励
- 效率奖励

用法:
    python train_mappo_easy_rm.py              # 默认训练
    python train_mappo_easy_rm.py --episodes 500  # 指定训练轮数
    python train_mappo_easy_rm.py --seed 123   # 指定随机种子
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
from reward_machines.reward_machine_enhanced import EnhancedRewardMachine, REWARD_MACHINE_STATES

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
    (exp_dir / "diagrams").mkdir(exist_ok=True)
    
    return exp_dir

def save_experiment_config(exp_dir, config, meta, args):
    """保存实验配置"""
    config_dict = {
        "experiment": {
            "name": args.exp_name,
            "timestamp": datetime.now().isoformat(),
            "difficulty": meta["level"],
            "seed": args.seed,
            "reward_machine": "enhanced"
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
        "reward_machine": {
            "type": "EnhancedRewardMachine",
            "task_complete_base": 5.0,
            "all_complete_bonus": 50.0,
            "collab_bonus": 2.0,
            "progress_reward": 1.0,
            "efficiency_bonus": 0.1,
            "collision_penalty": -0.5,
            "idle_penalty": -0.1,
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

def save_rm_diagram(exp_dir):
    """保存 Reward Machine 结构图 (JSON 格式)"""
    diagram_file = exp_dir / "diagrams" / "reward_machine_structure.json"
    with open(diagram_file, 'w', encoding='utf-8') as f:
        json.dump(REWARD_MACHINE_STATES, f, indent=2, ensure_ascii=False)
    
    # 同时保存为文本格式
    txt_file = exp_dir / "diagrams" / "reward_machine_structure.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("  DRAMA Reward Machine 结构设计\n")
        f.write("="*70 + "\n\n")
        
        f.write("状态机结构:\n")
        f.write("-"*50 + "\n")
        for node in REWARD_MACHINE_STATES["nodes"]:
            f.write(f"  {node['id']}: {node['label']} - {node['description']}\n")
        f.write("\n")
        
        f.write("状态转移:\n")
        f.write("-"*50 + "\n")
        for trans in REWARD_MACHINE_STATES["transitions"]:
            f.write(f"  {trans['from']} → {trans['to']}: {trans['condition']}\n")
        f.write("\n")
        
        f.write("奖励组件:\n")
        f.write("-"*50 + "\n")
        for key, value in REWARD_MACHINE_STATES["rewards"].items():
            f.write(f"  {key}: {value}\n")
    
    return diagram_file

def save_training_results(exp_dir, training_stats):
    """保存训练结果"""
    results_file = exp_dir / "results" / "training_stats.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(training_stats, f, indent=2, ensure_ascii=False)
    
    # CSV 格式
    csv_file = exp_dir / "results" / "training_stats.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("episode,reward,success,steps,avg_value,entropy,rm_stage,completed_ratio\n")
        for stat in training_stats:
            f.write(f"{stat['episode']},{stat['reward']:.2f},{stat['success']},{stat['steps']},{stat['avg_value']:.4f},{stat['entropy']:.4f},{stat.get('rm_stage','N/A')},{stat.get('completed_ratio',0):.2f}\n")

def save_final_metrics(exp_dir, metrics):
    """保存最终评估指标"""
    metrics_file = exp_dir / "results" / "final_metrics.json"
    with open(metrics_file, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

def train_mappo_easy_rm(args):
    """训练 MAPPO - Easy 难度 (增强 Reward Machine)"""
    
    print("\n" + "="*70)
    print("  MAPPO 训练 - Easy 难度 (增强 Reward Machine)")
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
    
    # 保存配置和 RM 图
    save_experiment_config(exp_dir, config, meta, args)
    save_rm_diagram(exp_dir)
    print(f"   📊 Reward Machine 结构图已保存")
    
    # 初始化环境
    print(f"\n🎮 初始化环境...")
    env = GridAreaEnv(config)
    rm = EnhancedRewardMachine(config["task_dependencies"], num_agents=config["num_robots"])
    
    env.reset()
    print(f"   初始状态：{len(env.floors_to_distribute)} 个待施工单元")
    print(f"   动作空间：6 (UP/DOWN/LEFT/RIGHT/WORK/HOVER)")
    
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
    convergence_episode = None
    
    start_time = time.time()
    
    # 导入训练函数
    from marl.algos.mappo_easy_rm import mappo_train_easy_rm
    
    try:
        final_stats = mappo_train_easy_rm(
            env, rm,
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
            "best_reward": best_reward if best_reward != -float('inf') else None,
            "convergence_episode": convergence_episode,
        }
        
        save_final_metrics(exp_dir, final_metrics)
        save_training_results(exp_dir, training_stats)
        
        print("\n" + "="*70)
        print("  训练完成!")
        print("="*70)
        print(f"\n📊 训练统计:")
        print(f"   总耗时：{training_time/60:.1f} 分钟")
        print(f"   总轮数：{args.episodes}")
        print(f"   最佳奖励：{final_stats.get('best_reward', 'N/A')}")
        print(f"   成功率：{final_stats.get('success_rate', 0)*100:.1f}%")
        print(f"   收敛轮数：{final_stats.get('convergence_episode', 'N/A')}")
        
        print(f"\n💾 结果已保存:")
        print(f"   配置：{exp_dir}/config.json")
        print(f"   训练统计：{exp_dir}/results/training_stats.json")
        print(f"   最终指标：{exp_dir}/results/final_metrics.json")
        print(f"   模型检查点：{exp_dir}/checkpoints/")
        print(f"   TensorBoard 日志：{exp_dir}/logs/")
        print(f"   RM 结构图：{exp_dir}/diagrams/")
        
        print("\n" + "="*70)
        
    except Exception as e:
        import traceback
        print(f"\n❌ 训练出错：{e}")
        traceback.print_exc()
    
    print("\n✅ 训练完成!")
    print("\n📊 查看结果:")
    print(f"   配置：cat {exp_dir}/config.json")
    print(f"   统计：cat {exp_dir}/results/training_stats.json")
    print(f"\n📈 TensorBoard 可视化:")
    print(f"   tensorboard --logdir {exp_dir}/logs/")

def main():
    parser = argparse.ArgumentParser(description="MAPPO 训练 - Easy 难度 (增强 Reward Machine)")
    
    # 训练参数
    parser.add_argument("--episodes", type=int, default=500, help="训练轮数 (default: 500)")
    parser.add_argument("--rollout-len", type=int, default=200, help="Rollout 长度 (default: 200)")
    parser.add_argument("--ppo-epochs", type=int, default=8, help="PPO 更新轮数 (default: 8)")
    parser.add_argument("--mini-batch-size", type=int, default=64, help="小批量大小 (default: 64)")
    parser.add_argument("--clip-eps", type=float, default=0.2, help="PPO clip 参数 (default: 0.2)")
    parser.add_argument("--lr", type=float, default=3e-4, help="学习率 (default: 3e-4)")
    parser.add_argument("--gamma", type=float, default=0.99, help="折扣因子 (default: 0.99)")
    parser.add_argument("--lam", type=float, default=0.95, help="GAE lambda (default: 0.95)")
    parser.add_argument("--grad-clip", type=float, default=0.5, help="梯度裁剪 (default: 0.5)")
    
    # 实验参数
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="随机种子 (default: 42)")
    parser.add_argument("--exp-name", type=str, default="mappo_easy_rm", help="实验名称")
    parser.add_argument("--save-interval", type=int, default=100, help="模型保存间隔")
    
    args = parser.parse_args()
    
    train_mappo_easy_rm(args)

if __name__ == "__main__":
    main()
