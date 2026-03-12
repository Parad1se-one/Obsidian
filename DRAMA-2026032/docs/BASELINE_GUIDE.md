# DRAMA Baseline 实验指南

> 📊 完整的算法对比实验配置和分析流程

---

## 🎯 实验目标

在 **Easy 难度**下对比以下算法的性能：

| 算法 | 类型 | 特点 | 状态 |
|------|------|------|------|
| **MAPPO (Baseline)** | Policy-based | 集中式 critic，无 RM | ✅ 训练中 |
| **IPPO** | Policy-based | 独立学习，无 RM | ⏳ 待运行 |
| **QMIX** | Value-based | 单调值分解 | ⏳ 待运行 |
| **MAPPO-RM (Ours)** | Policy-based + RM | Reward Machine 增强 | ✅ 已有 |

---

## 📁 文件结构

```
DRAMA/
├── train_mappo_easy_baseline_v2.py    # MAPPO Baseline (无 RM)
├── train_ippo_easy.py                  # IPPO (待完善)
├── train_qmix_easy.py                  # QMIX (待完善)
├── train_mappo_easy_rm.py              # MAPPO-RM (已有)
├── analyze_baselines.py                # 对比分析脚本
├── run_all_baselines_easy.sh           # 一键运行脚本
└── analysis_results/                   # 分析结果输出目录
    └── YYYYMMDD_HHMMSS/
        ├── reward_comparison_easy.png
        ├── success_rate_comparison_easy.png
        ├── comparison_table.md
        └── README.md
```

---

## 🚀 快速开始

### 方式 1: 单个运行

```bash
cd /home/openclaw/.openclaw/DRAMA/DRAMA

# 1. MAPPO Baseline (500 episodes)
python3 train_mappo_easy_baseline_v2.py --episodes 500 --seed 42 --exp_name mappo_easy_baseline

# 2. MAPPO-RM (已有)
python3 train_mappo_easy_rm.py --episodes 500 --seed 42 --exp_name mappo_easy_rm_full

# 3. IPPO (待完善)
python3 train_ippo_easy.py --episodes 500 --seed 42 --exp_name ippo_easy_baseline

# 4. QMIX (待完善)
python3 train_qmix_easy.py --episodes 500 --seed 42 --exp_name qmix_easy_baseline
```

### 方式 2: 一键运行

```bash
# 顺序运行 (推荐)
./run_all_baselines_easy.sh 500 42

# 并行运行 (需要更多 GPU/CPU 资源)
./run_all_baselines_easy.sh 500 42 true
```

---

## 📊 分析对比

训练完成后运行：

```bash
python3 analyze_baselines.py
```

### 输出内容

1. **Reward 对比图**: `reward_comparison_easy.png`
   - 横轴：Episodes
   - 纵轴：Episode Reward (滑动平均平滑)
   - 对比所有算法的学习曲线

2. **成功率对比图**: `success_rate_comparison_easy.png`
   - 横轴：Episodes
   - 纵轴：累积成功率 (%)
   - 展示任务完成能力

3. **性能对比表格**: `comparison_table.md`
   ```markdown
   ## Easy 难度 (6x6 网格，2 个施工单元)
   
   | 算法 | 最佳奖励 | 成功率 | 训练时间 |
   |------|----------|--------|----------|
   | MAPPO (Baseline) | xxx.xx | xx.x% | xx.xm |
   | IPPO | xxx.xx | xx.x% | xx.xm |
   | QMIX | xxx.xx | xx.x% | xx.xm |
   | MAPPO-RM (Ours) ⭐ | xxx.xx | xx.x% | xx.xm |
   ```

4. **Medium/Hard 难度**: 自动留空待填充

---

## 📈 当前进度

### Easy 难度

| 算法 | 状态 | 进度 | 预计完成 |
|------|------|------|----------|
| MAPPO Baseline | 🟢 训练中 | ~3% (15/500) | ~15 分钟 |
| IPPO | ⏸️ 待启动 | - | - |
| QMIX | ⏸️ 待启动 | - | - |
| MAPPO-RM | ✅ 已完成 | 100% (500/500) | - |

### Medium 难度

| 算法 | 状态 | 进度 | 备注 |
|------|------|------|------|
| MAPPO-RM (Optimized v2) | 🟢 训练中 | ~39% (193/500) | 修复任务依赖 |

### Hard 难度

| 算法 | 状态 | 备注 |
|------|------|------|
| 所有算法 | ⏸️ 待规划 | 需先定义 Hard 配置 |

---

## 🔧 配置说明

### Easy 难度
- **网格**: 6x6
- **施工单元**: 2 个
- **机器人**: 4 个
- **障碍物**: 0 个
- **初始待施工**: 25 个单元格

### Medium 难度
- **网格**: 6x6
- **施工单元**: 10 个
- **机器人**: 4 个
- **障碍物**: 1 个 @ (3,3)
- **任务依赖**: 并行 → 振动 → 找平 → 覆盖

### Hard 难度 (待定义)
- **网格**: 8x8 (建议)
- **施工单元**: 20 个 (建议)
- **机器人**: 4-6 个
- **障碍物**: 3 个 (建议)
- **更复杂的任务依赖**

---

## 📝 待办事项

### 短期 (今天)
- [ ] 完成 MAPPO Baseline 训练 (15 分钟)
- [ ] 完善 IPPO 训练脚本
- [ ] 完善 QMIX 训练脚本
- [ ] 运行所有 Easy baseline
- [ ] 生成对比图表

### 中期 (本周)
- [ ] 完成 Medium RM 训练 (优化版 v2)
- [ ] 启动 Medium Baseline 训练
- [ ] 定义 Hard 难度配置
- [ ] 启动 Hard RM 训练

### 长期
- [ ] 多随机种子实验 (seed=123, 456, 789)
- [ ] 消融实验 (RM 各组件贡献)
- [ ] 超参数敏感性分析
- [ ] 论文撰写

---

## 🎨 图表定制

### 修改颜色/样式

编辑 `analyze_baselines.py`:

```python
ALGORITHMS = {
    'mappo_baseline': {'name': 'MAPPO (Baseline)', 'color': '#1f77b4', 'marker': 'o'},
    'ippo_baseline': {'name': 'IPPO', 'color': '#ff7f0e', 'marker': 's'},
    'qmix_baseline': {'name': 'QMIX', 'color': '#2ca02c', 'marker': '^'},
    'mappo_rm': {'name': 'MAPPO-RM (Ours)', 'color': '#d62728', 'marker': 'd', 'highlight': True},
}
```

### 修改平滑窗口

```python
rewards = smooth_curve(data['rewards'], window=20)  # 改为 10 或 50
```

---

## 📚 参考

- **MAPPO 论文**: [Multi-Agent PPO](https://arxiv.org/abs/2103.01955)
- **IPPO 论文**: [Independent PPO](https://arxiv.org/abs/2011.09533)
- **QMIX 论文**: [QMIX: Monotonic Value Function Factorisation](https://arxiv.org/abs/1803.11485)
- **Reward Machine 论文**: [Using Reward Machines for High-Level Task Specification](https://proceedings.mlr.press/v80/icarte18a.html)

---

*最后更新：2026-03-09 22:45*  
*维护者：小虾 🦐*
