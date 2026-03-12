# DRAMA - Reward Machine-Enhanced MARL for Collaborative Construction

> **版本**: 2026-03-12 核心代码整理版  
> **原始项目**: `/home/openclaw/DRAMA/DRAMA/`  
> **整理目的**: 提取核心代码和文档，便于论文实验和代码复用

---

## 🎯 项目简介

DRAMA 是一个**Reward Machine 增强的多智能体强化学习框架**，专为协作式建筑施工任务设计。

### 核心贡献

1. **Reward Machine (RM) 集成**: 将高层任务规范（DAG 依赖）集成到 MARL 训练中
2. **任务依赖感知奖励**: 基于施工阶段的任务分解和进度追踪
3. **多阶段奖励设计**: 任务完成 + 协作奖励 + 进度奖励 + 效率奖励
4. **系统性实验验证**: 在 DRAMA 环境中验证 MAPPO-RM 的有效性

### 支持的算法

| 算法 | 类型 | 文件 | 说明 |
|------|------|------|------|
| **MAPPO** | Policy-based | `marl/algos/mappo.py` | 多智能体 PPO（集中式 critic） |
| **IPPO** | Policy-based | `marl/algos/ippo.py` | 独立 PPO（去中心化学习） |
| **QMIX** | Value-based | `marl/algos/qmix.py` | 单调值分解 |
| **VDN/DQN** | Value-based | `marl/algos/dqn_vdn.py` | 值分解网络 |
| **R-IPPO** | Policy-based + RM | `marl/algos/r_ippo.py` | IPPO + Reward Machine |

---

## 📁 项目结构

```
DRAMA-2026032/
├── README.md                          # 本文件
├── requirements.txt                   # Python 依赖
│
├── train_mappo_easy_rm.py            # MAPPO + RM (核心算法)
├── train_mappo_easy_baseline_v2.py   # MAPPO Baseline (无 RM)
├── train_dqn_easy.py                 # DQN/VDN 训练
├── train_qmix_easy.py                # QMIX 训练
├── evaluate.py                       # 模型评估
├── plot_results.py                   # 结果可视化
├── analyze_baselines.py              # Baseline 对比分析
│
├── marl/                             # MARL 核心库
│   ├── agents.py                     # 神经网络模型 (Actor/Critic)
│   ├── trainer.py                    # 训练循环逻辑
│   ├── buffer.py                     # 经验回放缓冲区
│   ├── mixer.py                      # QMIX/VDN 混合网络
│   └── algos/
│       ├── mappo.py                  # MAPPO 算法实现
│       ├── ippo.py                   # IPPO 算法实现
│       ├── qmix.py                   # QMIX 算法实现
│       ├── dqn_vdn.py                # DQN/VDN 算法实现
│       └── r_ippo.py                 # R-IPPO 算法实现
│
├── envs/
│   └── grid_env.py                   # DRAMA 环境 (网格化施工场景)
│
├── configs/                          # 配置文件
│   ├── env_config.py                 # 环境配置 (Easy/Medium/Hard)
│   └── algo_config.py                # 算法超参数配置
│
├── utils/                            # 工具函数
│   └── *.py                          # 日志、可视化等工具
│
├── scripts/                          # 辅助脚本
│   └── *.py                          # 数据处理、分析脚本
│
└── docs/                             # 文档
    ├── PAPER_EXPERIMENT_DESIGN.md    # 论文实验设计方案
    ├── BASELINE_GUIDE.md             # Baseline 实验指南
    └── EXPERIMENT_PROGRESS.md        # 实验进度追踪
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /home/openclaw/.openclaw/workspace/DRAMA-2026032
pip install -r requirements.txt
```

### 2. 训练 MAPPO-RM (核心算法)

```bash
python train_mappo_easy_rm.py \
    --episodes 500 \
    --seed 42 \
    --exp_name mappo_rm_easy
```

### 3. 训练 Baseline (无 RM)

```bash
python train_mappo_easy_baseline_v2.py \
    --episodes 500 \
    --seed 42 \
    --exp_name mappo_baseline_easy
```

### 4. 查看训练结果

```bash
tensorboard --logdir runs/
```

### 5. 对比分析

```bash
python analyze_baselines.py
```

---

## 🎮 环境配置

### Easy 难度
- **网格**: 6×6
- **施工单元**: 2 个
- **机器人**: 4 个
- **障碍物**: 0 个
- **任务阶段**: distribute → vibrate → level → cover

### Medium 难度
- **网格**: 6×6
- **施工单元**: 10 个
- **机器人**: 4 个
- **障碍物**: 1 个 @ (3,3)
- **任务依赖**: 更复杂的 DAG 结构

### Hard 难度 (待实现)
- **网格**: 8×8
- **施工单元**: 20 个
- **机器人**: 4-6 个
- **障碍物**: 3 个

---

## 📊 核心算法详解

### Reward Machine 设计

```python
# 任务阶段定义
TASK_STAGES = {
    0: "distribute_floor",   # 布料
    1: "vibrate_floor",      # 振捣
    2: "level_floor",        # 整平
    3: "cover_surface",      # 覆膜
    4: "completed"           # 完成
}

# 奖励组成
reward = (
    task_completion_reward * 10.0 +    # 任务完成奖励
    collaboration_reward * 5.0 +        # 协作奖励
    progress_reward * 2.0 +             # 进度奖励
    efficiency_reward * 1.0             # 效率奖励
)
```

### MAPPO 网络结构

```python
# Actor 网络
RecurrentMAPPOActor:
    obs_dim → Linear(64) → ReLU → GRU → Linear → action_dim

# Critic 网络
MAPPOCritic:
    state_dim → Linear(256) → ReLU → Linear(256) → ReLU → Linear → 1
```

---

## 📈 实验结果 (截至 2026-03-12)

### Easy 难度对比

| 算法 | Best Reward | Success Rate | Training Time |
|------|-------------|--------------|---------------|
| MAPPO Baseline | ~1200 | ~85% | ~15 min |
| IPPO | 待运行 | 待运行 | - |
| QMIX | 待运行 | 待运行 | - |
| **MAPPO-RM (Ours)** | **~1450** | **~95%** | **~15 min** |

### Medium 难度

| 算法 | Best Reward | Success Rate | 状态 |
|------|-------------|--------------|------|
| MAPPO-RM (Optimized v2) | 运行中 | 运行中 | 🟢 训练中 |

---

## 🔬 论文章节对应

### Section 3: Method
- **Reward Machine 设计**: `envs/grid_env.py` (任务依赖逻辑)
- **MARL 集成**: `marl/algos/mappo.py` (核心算法)
- **网络结构**: `marl/agents.py` (Actor/Critic)

### Section 4: Experimental Setup
- **环境配置**: `configs/env_config.py`
- **超参数**: `configs/algo_config.py`
- **训练脚本**: `train_*.py`

### Section 5: Results & Analysis
- **结果可视化**: `plot_results.py`
- **对比分析**: `analyze_baselines.py`
- **实验进度**: `docs/EXPERIMENT_PROGRESS.md`

---

## 📝 待办事项

### 短期 (本周)
- [ ] 完成所有 Easy 难度 Baseline 实验
- [ ] 完成 Medium 难度 MAPPO-RM 训练
- [ ] 运行消融实验 (4 组)
- [ ] 生成论文图表 (Figures 1-6)

### 中期 (下周)
- [ ] 多随机种子验证 (seed=123, 456)
- [ ] 敏感性分析 (学习率、rollout 长度等)
- [ ] Hard 难度实验
- [ ] 撰写完整论文初稿

### 长期
- [ ] 投稿 AAMAS 2026 / ICML 2026
- [ ] 代码开源 (GitHub)
- [ ] 补充更多消融实验

---

## 📚 相关论文

1. **MAPPO**: [Multi-Agent PPO](https://arxiv.org/abs/2103.01955)
2. **IPPO**: [Independent PPO](https://arxiv.org/abs/2011.09533)
3. **QMIX**: [Monotonic Value Function Factorisation](https://arxiv.org/abs/1803.11485)
4. **Reward Machine**: [Using Reward Machines for High-Level Task Specification](https://proceedings.mlr.press/v80/icarte18a.html)

---

## 👥 维护者

- **原始作者**: DRAMA Team 🎭
- **整理**: 小虾 🦐 (2026-03-12)
- **联系**: Linyi Wang

---

## 📄 许可证

本项目代码仅供学术研究使用。

---

*最后更新：2026-03-12 | 版本：v1.0*
