#!/usr/bin/env python3
"""
Medium 难度 - 全算法对比分析脚本
在所有训练完成后运行，生成对比图和统计报告
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ==================== 配置 ====================

BASE_DIR = Path("/home/openclaw/.openclaw/DRAMA/DRAMA")
EXP_DIR = BASE_DIR / "experiments" / "medium"
RESULTS_DIR = BASE_DIR / "results" / "medium"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# 实验名称前缀
EXP_PREFIX = "medium_comparison_20260310"

# 算法列表
ALGORITHMS = {
    "ippo": {"name": "IPPO", "color": "blue", "marker": "o"},
    "ippo_rm": {"name": "IPPO-RM (Ours)", "color": "red", "marker": "s"},
    "mappo": {"name": "MAPPO", "color": "magenta", "marker": "x"},
    "mappo_rm": {"name": "MAPPO-RM", "color": "green", "marker": "^"},
    "dqn": {"name": "DQN", "color": "cyan", "marker": "d"},
}

# ==================== 数据加载 ====================

def load_experiment_data(algo_key):
    """加载单个算法的训练数据"""
    # 查找实验目录
    exp_dirs = list(EXP_DIR.glob(f"{EXP_PREFIX}_{algo_key}*"))
    if not exp_dirs:
        print(f"⚠️  未找到实验目录：{EXP_PREFIX}_{algo_key}*")
        return None
    
    # 取最新的实验目录
    exp_dir = sorted(exp_dirs)[-1]
    stats_file = exp_dir / "results" / "training_stats.csv"
    
    if not stats_file.exists():
        print(f"⚠️  未找到统计数据：{stats_file}")
        return None
    
    # 读取 CSV
    df = pd.read_csv(stats_file)
    
    # 计算统计信息
    rewards = df["reward"].values
    episodes = df["episode"].values
    
    return {
        "episodes": episodes.tolist(),
        "rewards": rewards.tolist(),
        "mean_reward": float(np.mean(rewards)),
        "max_reward": float(np.max(rewards)),
        "min_reward": float(np.min(rewards)),
        "std_reward": float(np.std(rewards)),
        "final_reward": float(rewards[-1]) if len(rewards) > 0 else 0,
        "success_rate": float(df["success"].mean()) if "success" in df.columns else 0.0,
    }

# ==================== 主分析函数 ====================

def analyze_and_plot():
    """加载所有数据并生成对比图"""
    
    print("=" * 70)
    print("  Medium 难度 - 全算法对比分析")
    print("=" * 70)
    print()
    
    # 加载所有算法数据
    all_data = {}
    for algo_key, algo_info in ALGORITHMS.items():
        print(f"📊 加载 {algo_info['name']} 数据...")
        data = load_experiment_data(algo_key)
        if data:
            all_data[algo_key] = data
            print(f"   ✅ {len(data['episodes'])} 集，平均奖励：{data['mean_reward']:.2f}")
        else:
            print(f"   ❌ 数据不完整")
    
    if not all_data:
        print("\n❌ 没有完整的数据，无法生成对比图")
        return
    
    # ==================== 生成对比图 ====================
    
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    
    # 图 1: 训练曲线对比
    ax1 = axes[0, 0]
    for algo_key, data in all_data.items():
        algo_info = ALGORITHMS[algo_key]
        episodes = data["episodes"]
        rewards = data["rewards"]
        
        # 平滑曲线
        if len(rewards) > 5:
            rewards_smooth = pd.Series(rewards).rolling(window=5, min_periods=1).mean()
        else:
            rewards_smooth = rewards
        
        ax1.plot(episodes, rewards_smooth, 
                color=algo_info["color"], 
                linewidth=2, 
                label=algo_info["name"],
                marker=algo_info["marker"],
                markersize=3,
                alpha=0.7)
    
    ax1.set_xlabel("Episodes", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Average Reward", fontsize=12, fontweight='bold')
    ax1.set_title("Training Curves Comparison (Medium Difficulty)", fontsize=14, fontweight='bold')
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # 图 2: 最终奖励对比 (柱状图)
    ax2 = axes[0, 1]
    algo_names = [ALGORITHMS[k]["name"] for k in all_data.keys()]
    final_rewards = [all_data[k]["final_reward"] for k in all_data.keys()]
    colors = [ALGORITHMS[k]["color"] for k in all_data.keys()]
    
    bars = ax2.bar(algo_names, final_rewards, color=colors, alpha=0.7)
    ax2.set_ylabel("Final Reward", fontsize=12, fontweight='bold')
    ax2.set_title("Final Reward Comparison", fontsize=14, fontweight='bold')
    ax2.tick_params(axis='x', rotation=15)
    
    # 在柱子上标注数值
    for bar, val in zip(bars, final_rewards):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                f"{val:.1f}", ha='center', va='bottom', fontsize=9)
    
    # 图 3: 平均奖励对比 (带误差棒)
    ax3 = axes[1, 0]
    mean_rewards = [all_data[k]["mean_reward"] for k in all_data.keys()]
    std_rewards = [all_data[k]["std_reward"] for k in all_data.keys()]
    
    bars = ax3.bar(algo_names, mean_rewards, yerr=std_rewards, capsize=5,
                   color=colors, alpha=0.7, error_kw={'elinewidth': 2})
    ax3.set_ylabel("Mean Reward ± Std", fontsize=12, fontweight='bold')
    ax3.set_title("Average Reward with Standard Deviation", fontsize=14, fontweight='bold')
    ax3.tick_params(axis='x', rotation=15)
    
    # 在柱子上标注数值
    for bar, mean_val, std_val in zip(bars, mean_rewards, std_rewards):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                f"{mean_val:.1f}±{std_val:.1f}", ha='center', va='bottom', fontsize=8)
    
    # 图 4: 统计表格
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    table_data = []
    for algo_key in all_data.keys():
        data = all_data[algo_key]
        table_data.append([
            ALGORITHMS[algo_key]["name"],
            f"{data['mean_reward']:.2f}",
            f"{data['max_reward']:.2f}",
            f"{data['min_reward']:.2f}",
            f"{data['std_reward']:.2f}",
            f"{data['final_reward']:.2f}",
            f"{data['success_rate']*100:.1f}%"
        ])
    
    table = ax4.table(
        cellText=table_data,
        colLabels=["Algorithm", "Mean", "Max", "Min", "Std", "Final", "Success Rate"],
        loc='center',
        cellLoc='center',
        colColours=[f"{c}20" for c in colors] + ["lightgray"] * 6
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.8)
    ax4.set_title("Statistical Summary", fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    # 保存图表
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    png_path = RESULTS_DIR / f"medium_comparison_{timestamp}.png"
    pdf_path = RESULTS_DIR / f"medium_comparison_{timestamp}.pdf"
    
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    
    print(f"\n✅ 图表已保存:")
    print(f"   PNG: {png_path}")
    print(f"   PDF: {pdf_path}")
    
    # ==================== 生成文本报告 ====================
    
    report_path = RESULTS_DIR / f"medium_analysis_report_{timestamp}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Medium 难度 - 全算法对比分析报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        f.write("## 实验配置\n\n")
        f.write(f"- **难度**: Medium\n")
        f.write(f"- **网格大小**: 6x6\n")
        f.write(f"- **智能体数量**: 4\n")
        f.write(f"- **训练集数**: 500\n")
        f.write(f"- **随机种子**: 42\n\n")
        
        f.write("## 统计结果\n\n")
        f.write("| 算法 | 平均奖励 | 最高奖励 | 最低奖励 | 标准差 | 最终奖励 | 成功率 |\n")
        f.write("|------|----------|----------|----------|--------|----------|--------|\n")
        
        for algo_key in all_data.keys():
            data = all_data[algo_key]
            f.write(f"| {ALGORITHMS[algo_key]['name']} | ")
            f.write(f"{data['mean_reward']:.2f} | ")
            f.write(f"{data['max_reward']:.2f} | ")
            f.write(f"{data['min_reward']:.2f} | ")
            f.write(f"{data['std_reward']:.2f} | ")
            f.write(f"{data['final_reward']:.2f} | ")
            f.write(f"{data['success_rate']*100:.1f}% |\n")
        
        f.write("\n## 关键洞察\n\n")
        
        # 找出最佳算法
        best_algo = max(all_data.keys(), key=lambda k: all_data[k]['mean_reward'])
        best_data = all_data[best_algo]
        
        f.write(f"1. **最佳算法**: {ALGORITHMS[best_algo]['name']}\n")
        f.write(f"   - 平均奖励：{best_data['mean_reward']:.2f}\n")
        f.write(f"   - 最终奖励：{best_data['final_reward']:.2f}\n\n")
        
        # 计算改进百分比
        f.write("2. **性能对比**:\n")
        for algo_key in all_data.keys():
            if algo_key != best_algo:
                data = all_data[algo_key]
                improvement = ((best_data['mean_reward'] / data['mean_reward']) - 1) * 100 if data['mean_reward'] != 0 else 0
                f.write(f"   - {ALGORITHMS[best_algo]['name']} vs {ALGORITHMS[algo_key]['name']}: ")
                f.write(f"+{improvement:.2f}%\n")
        
        f.write("\n## 图表文件\n\n")
        f.write(f"- PNG: `{png_path.name}`\n")
        f.write(f"- PDF: `{pdf_path.name}`\n")
    
    print(f"\n✅ 报告已保存：{report_path}")
    
    # ==================== 打印总结 ====================
    
    print("\n" + "=" * 70)
    print("  分析完成!")
    print("=" * 70)
    print(f"\n🏆 最佳算法：{ALGORITHMS[best_algo]['name']}")
    print(f"   平均奖励：{best_data['mean_reward']:.2f}")
    print(f"   最终奖励：{best_data['final_reward']:.2f}")

if __name__ == "__main__":
    analyze_and_plot()
