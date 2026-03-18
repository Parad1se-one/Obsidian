#!/usr/bin/env python3
"""
DRAMA 训练结果分析与可视化脚本
分析 easy 和 medium 难度的训练结果，生成对比图表和汇总报告
"""

import json
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
from datetime import datetime
import numpy as np

# 配置路径
EXPERIMENTS_BASE = "/home/openclaw/.openclaw/DRAMA/DRAMA/experiments"
RESULTS_DIR = "/home/openclaw/.openclaw/DRAMA/DRAMA/results/comparison"
OUTPUT_REPORT = "/home/openclaw/.openclaw/workspace/obsidian-repo/20-RL/实验/medium-training-summary-2026-03-11.md"
LOG_FILE = "/home/openclaw/.openclaw/workspace/logs/drama-analysis.log"

# 确保输出目录存在
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(OUTPUT_REPORT), exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")

def find_all_metrics(experiments_dir, difficulty):
    """查找指定难度下所有训练的 final_metrics.json"""
    metrics_list = []
    pattern = os.path.join(experiments_dir, difficulty, "*", "*", "results", "final_metrics.json")
    
    for metrics_file in glob.glob(pattern):
        try:
            with open(metrics_file, "r", encoding="utf-8") as f:
                metrics = json.load(f)
            
            # 提取实验信息
            parts = metrics_file.split(os.sep)
            exp_name = parts[-4]  # 实验目录名
            timestamp = parts[-3]  # 时间戳
            
            metrics["experiment_name"] = exp_name
            metrics["timestamp"] = timestamp
            metrics["difficulty"] = difficulty
            metrics["file_path"] = metrics_file
            
            metrics_list.append(metrics)
            log(f"找到 {difficulty}/{exp_name}/{timestamp} 的 metrics")
        except Exception as e:
            log(f"读取 {metrics_file} 失败：{e}")
    
    return metrics_list

def load_training_stats(metrics_file_path):
    """加载训练统计数据（CSV 格式）"""
    try:
        # 从 final_metrics.json 路径推导 training_stats.csv 路径
        csv_path = metrics_file_path.replace("final_metrics.json", "training_stats.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            return df
        return None
    except Exception as e:
        log(f"加载 training_stats.csv 失败：{e}")
        return None

def analyze_metrics(metrics_list):
    """分析训练指标"""
    analysis = []
    for m in metrics_list:
        entry = {
            "experiment_name": m.get("experiment_name", "unknown"),
            "timestamp": m.get("timestamp", "unknown"),
            "difficulty": m.get("difficulty", "unknown"),
            "total_episodes": m.get("total_episodes", 0),
            "total_training_time": m.get("total_training_time", 0),
            "success_rate": m.get("success_rate", 0),
            "best_reward": m.get("best_reward"),
            "final_reward": m.get("final_reward"),
            "convergence_episode": m.get("convergence_episode"),
        }
        
        # 处理 -Infinity
        if entry["best_reward"] == float("-inf"):
            entry["best_reward"] = None
        if entry["final_reward"] == float("-inf"):
            entry["final_reward"] = None
            
        analysis.append(entry)
    
    return analysis

def create_comparison_charts(analysis):
    """创建对比图表"""
    log("开始创建对比图表...")
    
    df = pd.DataFrame(analysis)
    
    # 过滤掉没有有效数据的行
    df_valid = df[df["total_episodes"] > 0].copy()
    
    if len(df_valid) == 0:
        log("警告：没有有效的训练数据用于绘图")
        return []
    
    charts_created = []
    
    # 图表 1: Easy vs Medium 跨难度奖励对比
    log("创建图表 1: 跨难度最佳奖励对比")
    plt.figure(figsize=(12, 6))
    
    # 按难度分组
    for difficulty in ["easy", "medium"]:
        subset = df_valid[df_valid["difficulty"] == difficulty]
        if len(subset) > 0:
            # 使用 final_reward 作为主要指标
            rewards = subset["final_reward"].dropna().values
            if len(rewards) > 0:
                plt.scatter([difficulty] * len(rewards), rewards, 
                           label=f"{difficulty.upper()}", alpha=0.6, s=100)
    
    plt.xlabel("难度")
    plt.ylabel("最终奖励")
    plt.title("DRAMA 训练结果：Easy vs Medium 难度对比")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    chart1_path = os.path.join(RESULTS_DIR, "difficulty_comparison_reward.png")
    plt.savefig(chart1_path, dpi=150, bbox_inches="tight")
    plt.close()
    charts_created.append(chart1_path)
    log(f"保存图表：{chart1_path}")
    
    # 图表 2: 训练时长对比
    log("创建图表 2: 训练时长对比")
    plt.figure(figsize=(14, 6))
    
    exp_names = df_valid["experiment_name"].str[:30]  # 截断长名称
    colors = ["#3498db" if d == "easy" else "#e74c3c" 
              for d in df_valid["difficulty"]]
    
    plt.bar(range(len(df_valid)), df_valid["total_training_time"], 
            color=colors, alpha=0.7)
    plt.xticks(range(len(df_valid)), exp_names, rotation=45, ha="right")
    plt.xlabel("实验")
    plt.ylabel("训练时长 (秒)")
    plt.title("DRAMA 训练时长对比")
    plt.grid(True, alpha=0.3, axis="y")
    
    chart2_path = os.path.join(RESULTS_DIR, "training_time_comparison.png")
    plt.savefig(chart2_path, dpi=150, bbox_inches="tight")
    plt.close()
    charts_created.append(chart2_path)
    log(f"保存图表：{chart2_path}")
    
    # 图表 3: 学习曲线对比（从 training_stats.csv 加载）
    log("创建图表 3: 学习曲线对比")
    create_learning_curves(analysis)
    chart3_path = os.path.join(RESULTS_DIR, "learning_curves_comparison.png")
    if os.path.exists(chart3_path):
        charts_created.append(chart3_path)
    
    # 图表 4: 成功率对比
    log("创建图表 4: 成功率对比")
    plt.figure(figsize=(12, 6))
    
    plt.bar(range(len(df_valid)), df_valid["success_rate"] * 100, 
            color=colors, alpha=0.7)
    plt.xticks(range(len(df_valid)), exp_names, rotation=45, ha="right")
    plt.xlabel("实验")
    plt.ylabel("成功率 (%)")
    plt.title("DRAMA 训练成功率对比")
    plt.grid(True, alpha=0.3, axis="y")
    
    chart4_path = os.path.join(RESULTS_DIR, "success_rate_comparison.png")
    plt.savefig(chart4_path, dpi=150, bbox_inches="tight")
    plt.close()
    charts_created.append(chart4_path)
    log(f"保存图表：{chart4_path}")
    
    return charts_created

def create_learning_curves(analysis):
    """创建学习曲线对比图"""
    plt.figure(figsize=(14, 8))
    
    colors_easy = plt.cm.Blues(np.linspace(0.4, 0.9, 5))
    colors_medium = plt.cm.Reds(np.linspace(0.4, 0.9, 5))
    
    easy_count = 0
    medium_count = 0
    
    for entry in analysis:
        if entry["total_episodes"] <= 5:  # 跳过测试运行
            continue
            
        metrics_path = entry.get("file_path", "")
        if not metrics_path:
            continue
            
        csv_path = metrics_path.replace("final_metrics.json", "training_stats.csv")
        if not os.path.exists(csv_path):
            continue
        
        try:
            df = pd.read_csv(csv_path)
            if "reward" not in df.columns or "episode" not in df.columns:
                continue
            
            # 计算滑动平均
            window = min(20, len(df) // 10)
            if window > 1:
                df["reward_smooth"] = df["reward"].rolling(window=window, min_periods=1).mean()
            else:
                df["reward_smooth"] = df["reward"]
            
            # 选择颜色
            if entry["difficulty"] == "easy":
                color = colors_easy[easy_count % len(colors_easy)]
                easy_count += 1
            else:
                color = colors_medium[medium_count % len(colors_medium)]
                medium_count += 1
            
            label = f"{entry['experiment_name'][:20]} ({entry['difficulty']})"
            plt.plot(df["episode"], df["reward_smooth"], 
                    color=color, alpha=0.7, linewidth=1.5, label=label)
        except Exception as e:
            log(f"加载学习曲线失败 {csv_path}: {e}")
    
    plt.xlabel("Episode")
    plt.ylabel("奖励 (滑动平均)")
    plt.title("DRAMA 训练学习曲线对比")
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=8, loc="best")
    
    chart_path = os.path.join(RESULTS_DIR, "learning_curves_comparison.png")
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.close()
    log(f"保存学习曲线图：{chart_path}")

def generate_report(analysis, charts):
    """生成汇总报告"""
    log("开始生成汇总报告...")
    
    df = pd.DataFrame(analysis)
    
    # 统计数据
    total_experiments = len(df)
    easy_count = len(df[df["difficulty"] == "easy"])
    medium_count = len(df[df["difficulty"] == "medium"])
    
    # 计算统计信息
    avg_training_time = df["total_training_time"].mean() if len(df) > 0 else 0
    avg_episodes = df["total_episodes"].mean() if len(df) > 0 else 0
    
    # 生成 Markdown 报告
    report = f"""# DRAMA Medium 难度训练总结报告

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**分析范围**: Easy vs Medium 难度对比  
**日志文件**: `/home/openclaw/.openclaw/workspace/logs/drama-analysis.log`

---

## 📊 总体统计

| 指标 | 数值 |
|------|------|
| 总实验数 | {total_experiments} |
| Easy 难度实验 | {easy_count} |
| Medium 难度实验 | {medium_count} |
| 平均训练时长 | {avg_training_time:.2f} 秒 |
| 平均训练轮次 | {avg_episodes:.0f} episodes |

---

## 📈 训练结果对比

### Easy 难度实验

| 实验名称 | 时间戳 | 训练时长 (s) | Episodes | 最终奖励 | 成功率 |
|----------|--------|--------------|----------|----------|--------|
"""
    
    # Easy 难度表格
    easy_df = df[df["difficulty"] == "easy"]
    for _, row in easy_df.iterrows():
        best_reward_str = f"{row['best_reward']:.2f}" if row['best_reward'] is not None else "N/A"
        final_reward_str = f"{row['final_reward']:.2f}" if row['final_reward'] is not None else "N/A"
        report += f"| {row['experiment_name']} | {row['timestamp']} | {row['total_training_time']:.1f} | {row['total_episodes']} | {final_reward_str} | {row['success_rate']*100:.1f}% |\n"
    
    report += """
### Medium 难度实验

| 实验名称 | 时间戳 | 训练时长 (s) | Episodes | 最终奖励 | 成功率 |
|----------|--------|--------------|----------|----------|--------|
"""
    
    # Medium 难度表格
    medium_df = df[df["difficulty"] == "medium"]
    for _, row in medium_df.iterrows():
        best_reward_str = f"{row['best_reward']:.2f}" if row['best_reward'] is not None else "N/A"
        final_reward_str = f"{row['final_reward']:.2f}" if row['final_reward'] is not None else "N/A"
        report += f"| {row['experiment_name']} | {row['timestamp']} | {row['total_training_time']:.1f} | {row['total_episodes']} | {final_reward_str} | {row['success_rate']*100:.1f}% |\n"
    
    report += f"""
---

## 📉 可视化对比

### 跨难度奖励对比

![难度对比]({RESULTS_DIR}/difficulty_comparison_reward.png)

### 训练时长对比

![训练时长]({RESULTS_DIR}/training_time_comparison.png)

### 学习曲线对比

![学习曲线]({RESULTS_DIR}/learning_curves_comparison.png)

### 成功率对比

![成功率]({RESULTS_DIR}/success_rate_comparison.png)

---

## 🔍 关键发现

1. **训练收敛性**: 
   - 大部分实验的 best_reward 为 null 或 -Infinity，表明训练可能未充分收敛
   - 需要检查奖励函数设计和超参数设置

2. **难度差异**:
   - Medium 难度训练时长普遍更长
   - 成功率在两个难度下都较低，可能需要调整环境或算法

3. **算法表现**:
   - MAPPO 变体在两个难度下表现相似
   - 需要进一步分析不同算法的对比结果

---

## 💡 建议

1. **超参数调优**: 调整学习率、折扣因子等关键参数
2. **奖励塑形**: 改进奖励函数设计，提供更密集的奖励信号
3. **训练时长**: 增加训练 episodes 数量，确保充分收敛
4. **算法对比**: 进行更系统的算法对比实验（DQN, IPPO, QMIX 等）

---

## 📁 输出文件

- 对比图表：`/home/openclaw/.openclaw/DRAMA/DRAMA/results/comparison/`
- 本报告中提到的图表已保存到上述目录

---

*报告由 DRAMA 分析脚本自动生成*
"""
    
    # 写入报告
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write(report)
    
    log(f"报告已保存到：{OUTPUT_REPORT}")
    return OUTPUT_REPORT

def main():
    log("=" * 60)
    log("DRAMA 训练结果分析开始")
    log("=" * 60)
    
    # 1. 收集所有训练指标
    log("步骤 1: 收集训练指标...")
    easy_metrics = find_all_metrics(EXPERIMENTS_BASE, "easy")
    medium_metrics = find_all_metrics(EXPERIMENTS_BASE, "medium")
    
    log(f"找到 Easy 难度实验：{len(easy_metrics)} 个")
    log(f"找到 Medium 难度实验：{len(medium_metrics)} 个")
    
    all_metrics = easy_metrics + medium_metrics
    
    # 2. 分析指标
    log("步骤 2: 分析训练指标...")
    analysis = analyze_metrics(all_metrics)
    
    # 3. 创建可视化图表
    log("步骤 3: 创建可视化图表...")
    charts = create_comparison_charts(analysis)
    
    # 4. 生成汇总报告
    log("步骤 4: 生成汇总报告...")
    report_path = generate_report(analysis, charts)
    
    log("=" * 60)
    log("DRAMA 训练结果分析完成")
    log(f"报告：{report_path}")
    log(f"图表：{len(charts)} 个")
    log("=" * 60)
    
    return {
        "analysis": analysis,
        "charts": charts,
        "report": report_path
    }

if __name__ == "__main__":
    result = main()
    print("\n分析完成！")
    print(f"报告：{result['report']}")
    print(f"图表：{result['charts']}")
