# DRAMA Medium 难度训练总结报告

**生成时间**: 2026-03-11 07:44:17  
**分析范围**: Easy vs Medium 难度对比  
**日志文件**: `/home/openclaw/.openclaw/workspace/logs/drama-analysis.log`

---

## 📊 总体统计

| 指标 | 数值 |
|------|------|
| 总实验数 | 7 |
| Easy 难度实验 | 5 |
| Medium 难度实验 | 2 |
| 平均训练时长 | 3462.69 秒 |
| 平均训练轮次 | 365 episodes |

---

## 📈 训练结果对比

### Easy 难度实验

| 实验名称 | 时间戳 | 训练时长 (s) | Episodes | 最终奖励 | 成功率 |
|----------|--------|--------------|----------|----------|--------|
| mappo_easy_baseline | 20260309_223531 | 1038.3 | 500 | -154.00 | 0.0% |
| mappo_easy_rm_full | 20260309_174442 | 1237.0 | 500 | nan | 0.0% |
| mappo_easy_baseline_test | 20260309_223508 | 12.5 | 5 | -170.72 | 0.0% |
| mappo_easy_quick | 20260309_172037 | 109.3 | 50 | -213.98 | 0.0% |
| mappo_easy_easy_rm_full | 20260309_182954 | 1255.0 | 500 | nan | 0.0% |

### Medium 难度实验

| 实验名称 | 时间戳 | 训练时长 (s) | Episodes | 最终奖励 | 成功率 |
|----------|--------|--------------|----------|----------|--------|
| mappo_medium_rm_full | 20260309_195249 | 1246.1 | 500 | nan | 0.0% |
| medium_comparison_20260310_mappo | 20260310_105148 | 19340.7 | 500 | -154.00 | 0.0% |

---

## 📉 可视化对比

### 跨难度奖励对比

![难度对比](/home/openclaw/.openclaw/DRAMA/DRAMA/results/comparison/difficulty_comparison_reward.png)

### 训练时长对比

![训练时长](/home/openclaw/.openclaw/DRAMA/DRAMA/results/comparison/training_time_comparison.png)

### 学习曲线对比

![学习曲线](/home/openclaw/.openclaw/DRAMA/DRAMA/results/comparison/learning_curves_comparison.png)

### 成功率对比

![成功率](/home/openclaw/.openclaw/DRAMA/DRAMA/results/comparison/success_rate_comparison.png)

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

## 🔄 补跑任务

根据分析结果，启动以下补跑训练：

### 补跑 1: MAPPO-RM Medium
- **状态**: 已启动
- **脚本**: `train_mappo_medium_rm.py`
- **目标**: 500 episodes
- **说明**: 重新训练 MAPPO with Reward Machine (Medium 难度)

### 补跑 2: DQN Medium
- **状态**: 已启动
- **脚本**: `train_dqn_medium.py`
- **目标**: 500 episodes
- **说明**: 重新训练 DQN baseline (Medium 难度)

**训练日志**: `/home/openclaw/.openclaw/workspace/logs/drama-analysis.log`

---

## 📁 输出文件

- 对比图表：`/home/openclaw/.openclaw/DRAMA/DRAMA/results/comparison/`
- 本报告中提到的图表已保存到上述目录

---

*报告由 DRAMA 分析脚本自动生成*
*最后更新*: 2026-03-11 07:45
