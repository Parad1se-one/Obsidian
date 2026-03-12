#!/usr/bin/env python3
"""
DRAMA 算法对比分析脚本
生成 Reward 曲线、Loss 曲线、性能对比表格
支持 Easy/Medium/Hard 难度，自动留空未完成的实验

用法:
    python analyze_baselines.py                    # 分析所有可用数据
    python analyze_baselines.py --difficulty easy  # 只分析 Easy
    python analyze_baselines.py --output pdf       # 输出 PDF 格式
"""

import os
import sys
import argparse
import json
import glob
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 项目根目录
PROJECT_ROOT = Path(__file__).parent
EXPERIMENTS_DIR = PROJECT_ROOT / "experiments"

# 算法配置
ALGORITHMS = {
    'mappo_baseline': {'name': 'MAPPO (Baseline)', 'color': '#1f77b4', 'marker': 'o'},
    'ippo_baseline': {'name': 'IPPO', 'color': '#ff7f0e', 'marker': 's'},
    'qmix_baseline': {'name': 'QMIX', 'color': '#2ca02c', 'marker': '^'},
    'mappo_rm': {'name': 'MAPPO-RM (Ours)', 'color': '#d62728', 'marker': 'd', 'highlight': True},
}

DIFFICULTIES = ['easy', 'medium', 'hard']

def find_latest_experiment(exp_pattern: str, difficulty: str) -> Optional[Path]:
    """查找最新的实验目录"""
    pattern = EXPERIMENTS_DIR / difficulty / exp_pattern / "*"
    dirs = sorted(glob.glob(str(pattern)), reverse=True)
    return Path(dirs[0]) if dirs else None

def load_training_stats(exp_dir: Path) -> Optional[Dict]:
    """加载训练统计"""
    stats_file = exp_dir / "results" / "training_stats.json"
    if stats_file.exists():
        with open(stats_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def load_tensorboard_data(exp_dir: Path) -> Dict:
    """从 TensorBoard 日志加载数据 (简化版)"""
    # 实际使用时可以用 tensorboard.backend.event_processing 解析
    # 这里先用 training_stats.json 替代
    stats = load_training_stats(exp_dir)
    if stats:
        return {
            'episodes': stats.get('episodes', []),
            'rewards': stats.get('episode_rewards', []),
            'success_rate': stats.get('success_rate', []),
            'completed_ratio': stats.get('completed_ratio', [])
        }
    return {}

def smooth_curve(data: List[float], window: int = 10) -> List[float]:
    """滑动平均平滑曲线"""
    if len(data) < window:
        return data
    
    smoothed = []
    for i in range(len(data)):
        start = max(0, i - window + 1)
        smoothed.append(np.mean(data[start:i+1]))
    return smoothed

def plot_reward_comparison(difficulty: str, output_dir: Path, 
                           output_format: str = 'png') -> Dict[str, bool]:
    """绘制 Reward 对比图"""
    print(f"\n📊 绘制 {difficulty.upper()} 难度 Reward 对比图...")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    results = {}
    has_data = False
    
    for algo_key, algo_config in ALGORITHMS.items():
        exp_dir = find_latest_experiment(f"{algo_key}_{difficulty}", difficulty)
        
        if exp_dir and exp_dir.exists():
            data = load_tensorboard_data(exp_dir)
            if data.get('rewards'):
                episodes = data['episodes']
                rewards = smooth_curve(data['rewards'], window=20)
                
                label = algo_config['name']
                if algo_config.get('highlight'):
                    label += " ⭐"
                
                ax.plot(episodes, rewards, 
                       label=label,
                       color=algo_config['color'],
                       marker=algo_config.get('marker', 'o'),
                       markevery=max(1, len(episodes)//20),
                       linewidth=2,
                       markersize=4,
                       alpha=0.8)
                
                results[algo_key] = True
                has_data = True
        else:
            results[algo_key] = False
            # 标注空缺
            ax.text(0.5, 0.5, f'{algo_config["name"]}\n(待运行)', 
                   transform=ax.transAxes,
                   ha='center', va='center',
                   fontsize=9, alpha=0.3,
                   bbox=dict(boxstyle='round', facecolor='gray', alpha=0.1))
    
    if not has_data:
        ax.text(0.5, 0.5, '暂无数据', transform=ax.transAxes,
               ha='center', va='center', fontsize=16, alpha=0.5)
        ax.set_title(f'{difficulty.upper()} - Reward Comparison\n(No data available)',
                    fontsize=14)
    else:
        ax.set_xlabel('Episodes', fontsize=12)
        ax.set_ylabel('Episode Reward (smoothed)', fontsize=12)
        ax.set_title(f'{difficulty.upper()} Difficulty - Reward Comparison', fontsize=14)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    plt.tight_layout()
    
    # 保存
    output_file = output_dir / f"reward_comparison_{difficulty}.{output_format}"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ 已保存：{output_file}")
    return results

def plot_success_rate_comparison(difficulty: str, output_dir: Path,
                                  output_format: str = 'png') -> Dict[str, bool]:
    """绘制成功率对比图"""
    print(f"\n📈 绘制 {difficulty.upper()} 难度成功率对比图...")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    results = {}
    has_data = False
    
    for algo_key, algo_config in ALGORITHMS.items():
        exp_dir = find_latest_experiment(f"{algo_key}_{difficulty}", difficulty)
        
        if exp_dir and exp_dir.exists():
            data = load_tensorboard_data(exp_dir)
            if data.get('success_rate'):
                episodes = data['episodes']
                # 计算累积成功率
                success_rates = np.cumsum(data['success_rate']) / np.arange(1, len(data['success_rate'])+1)
                success_rates = smooth_curve(success_rates * 100, window=20)
                
                label = algo_config['name']
                if algo_config.get('highlight'):
                    label += " ⭐"
                
                ax.plot(episodes, success_rates,
                       label=label,
                       color=algo_config['color'],
                       marker=algo_config.get('marker', 'o'),
                       markevery=max(1, len(episodes)//20),
                       linewidth=2,
                       markersize=4,
                       alpha=0.8)
                
                results[algo_key] = True
                has_data = True
        else:
            results[algo_key] = False
    
    if not has_data:
        ax.text(0.5, 0.5, '暂无数据', transform=ax.transAxes,
               ha='center', va='center', fontsize=16, alpha=0.5)
        ax.set_title(f'{difficulty.upper()} - Success Rate Comparison\n(No data available)',
                    fontsize=14)
    else:
        ax.set_xlabel('Episodes', fontsize=12)
        ax.set_ylabel('Success Rate (%)', fontsize=12)
        ax.set_title(f'{difficulty.upper()} Difficulty - Success Rate Comparison', fontsize=14)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 105)
    
    plt.tight_layout()
    
    output_file = output_dir / f"success_rate_comparison_{difficulty}.{output_format}"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ 已保存：{output_file}")
    return results

def generate_comparison_table(output_dir: Path) -> None:
    """生成性能对比表格"""
    print(f"\n📋 生成性能对比表格...")
    
    table_data = []
    
    for difficulty in DIFFICULTIES:
        row = {'Difficulty': difficulty.upper()}
        
        for algo_key, algo_config in ALGORITHMS.items():
            exp_dir = find_latest_experiment(f"{algo_key}_{difficulty}", difficulty)
            
            if exp_dir and exp_dir.exists():
                stats = load_training_stats(exp_dir)
                if stats:
                    best_reward = stats.get('best_reward', 'N/A')
                    success_rate = stats.get('best_success_rate', 0) * 100
                    training_time = stats.get('training_time', 0) / 60  # 分钟
                    
                    if isinstance(best_reward, (int, float)):
                        row[f'{algo_key}_reward'] = f'{best_reward:.2f}'
                        row[f'{algo_key}_success'] = f'{success_rate:.1f}%'
                        row[f'{algo_key}_time'] = f'{training_time:.1f}m'
                    else:
                        row[f'{algo_key}_reward'] = 'N/A'
                        row[f'{algo_key}_success'] = 'N/A'
                        row[f'{algo_key}_time'] = 'N/A'
                else:
                    row[f'{algo_key}_reward'] = '待运行'
                    row[f'{algo_key}_success'] = '待运行'
                    row[f'{algo_key}_time'] = '待运行'
            else:
                row[f'{algo_key}_reward'] = '待运行'
                row[f'{algo_key}_success'] = '待运行'
                row[f'{algo_key}_time'] = '待运行'
        
        table_data.append(row)
    
    # 生成 Markdown 表格
    md_table = []
    md_table.append("# DRAMA 算法性能对比\n")
    md_table.append(f"*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    # Easy 难度
    md_table.append("## Easy 难度 (6x6 网格，2 个施工单元)\n")
    md_table.append("| 算法 | 最佳奖励 | 成功率 | 训练时间 |")
    md_table.append("|------|----------|--------|----------|")
    
    for algo_key, algo_config in ALGORITHMS.items():
        reward = table_data[0].get(f'{algo_key}_reward', 'N/A')
        success = table_data[0].get(f'{algo_key}_success', 'N/A')
        time = table_data[0].get(f'{algo_key}_time', 'N/A')
        name = algo_config['name']
        if algo_config.get('highlight'):
            name += " ⭐"
        md_table.append(f"| {name} | {reward} | {success} | {time} |")
    
    # Medium 难度
    md_table.append("\n## Medium 难度 (6x6 网格，10 个施工单元，1 个障碍物)\n")
    md_table.append("| 算法 | 最佳奖励 | 成功率 | 训练时间 |")
    md_table.append("|------|----------|--------|----------|")
    
    for algo_key, algo_config in ALGORITHMS.items():
        reward = table_data[1].get(f'{algo_key}_reward', '待运行')
        success = table_data[1].get(f'{algo_key}_success', '待运行')
        time = table_data[1].get(f'{algo_key}_time', '待运行')
        name = algo_config['name']
        if algo_config.get('highlight'):
            name += " ⭐"
        md_table.append(f"| {name} | {reward} | {success} | {time} |")
    
    # Hard 难度
    md_table.append("\n## Hard 难度 (8x8 网格，20 个施工单元，3 个障碍物)\n")
    md_table.append("| 算法 | 最佳奖励 | 成功率 | 训练时间 |")
    md_table.append("|------|----------|--------|----------|")
    
    for algo_key, algo_config in ALGORITHMS.items():
        reward = table_data[2].get(f'{algo_key}_reward', '待运行')
        success = table_data[2].get(f'{algo_key}_success', '待运行')
        time = table_data[2].get(f'{algo_key}_time', '待运行')
        name = algo_config['name']
        if algo_config.get('highlight'):
            name += " ⭐"
        md_table.append(f"| {name} | {reward} | {success} | {time} |")
    
    # 保存
    md_file = output_dir / "comparison_table.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_table))
    
    print(f"   ✓ 已保存：{md_file}")
    
    # 同时生成 JSON 格式
    json_file = output_dir / "comparison_table.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(table_data, f, indent=2, ensure_ascii=False)
    
    print(f"   ✓ 已保存：{json_file}")

def generate_all_plots(output_format: str = 'png') -> None:
    """生成所有对比图"""
    print("="*70)
    print("  DRAMA 算法对比分析")
    print("="*70)
    
    # 创建输出目录
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = PROJECT_ROOT / "analysis_results" / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n💾 输出目录：{output_dir}")
    
    # 为每个难度生成图表
    for difficulty in DIFFICULTIES:
        print(f"\n{'='*70}")
        print(f"  处理 {difficulty.upper()} 难度")
        print(f"{'='*70}")
        
        plot_reward_comparison(difficulty, output_dir, output_format)
        plot_success_rate_comparison(difficulty, output_dir, output_format)
    
    # 生成对比表格
    generate_comparison_table(output_dir)
    
    # 生成 README
    readme_file = output_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(f"# DRAMA 算法对比分析结果\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## 文件列表\n\n")
        f.write(f"### Reward 对比图\n")
        for difficulty in DIFFICULTIES:
            f.write(f"- `reward_comparison_{difficulty}.{output_format}`\n")
        f.write(f"\n### 成功率对比图\n")
        for difficulty in DIFFICULTIES:
            f.write(f"- `success_rate_comparison_{difficulty}.{output_format}`\n")
        f.write(f"\n### 对比表格\n")
        f.write(f"- `comparison_table.md` (Markdown 格式)\n")
        f.write(f"- `comparison_table.json` (JSON 格式)\n")
    
    print(f"\n{'='*70}")
    print("  ✅ 分析完成!")
    print(f"{'='*70}")
    print(f"\n📁 所有结果已保存到：{output_dir}")
    print(f"\n📊 生成的文件:")
    for f in sorted(output_dir.glob("*")):
        print(f"   - {f.name}")
    print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DRAMA 算法对比分析')
    parser.add_argument('--difficulty', type=str, default='all',
                       choices=['all', 'easy', 'medium', 'hard'],
                       help='分析的难度')
    parser.add_argument('--output', type=str, default='png',
                       choices=['png', 'pdf', 'svg'],
                       help='输出格式')
    
    args = parser.parse_args()
    
    if args.difficulty == 'all':
        generate_all_plots(args.output)
    else:
        # TODO: 支持单难度分析
        print(f"⚠️  单难度分析功能待实现，当前生成所有难度的图表")
        generate_all_plots(args.output)
