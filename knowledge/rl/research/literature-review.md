# RL 文献调研总结

**学习时间:** 2026-03-05 22:04-22:14
**主题:** 5 篇核心论文综合分析

---

## 论文清单

| 论文 | Venue | 年份 | 引用数 |
|------|-------|------|--------|
| DQN | Nature | 2015 | 10000+ |
| Double DQN | AAAI | 2016 | 5000+ |
| World Models | - | 2018 | 3000+ |
| MuZero | Nature | 2019 | 5000+ |
| DreamerV3 | ICLR | 2024 | 500+ |

---

## 演进脉络

### 2015-2016: Value-Based 成熟期
- DQN: 首次将 CNN 与 Q-Learning 结合
- Double DQN: 解决过估计问题

**核心思想:** 用神经网络近似 Q 函数

### 2018-2019: Model-Based 复兴
- World Models: 在"梦境"中学习
- MuZero: 潜空间 MCTS 规划

**核心思想:** 学习环境模型，在模型中规划

### 2020-2024: 端到端世界模型
- Dreamer 系列: 端到端训练
- DreamerV3: 单一 agent 通用

**核心思想:** 端到端世界模型 + 潜空间 Actor-Critic

---

## 技术演进

### 表示学习
```
DQN: 原始像素 → CNN → Q 值
World Models: 像素 → VAE → 潜空间 z
MuZero: 观察 → Representation → 隐藏状态 h
DreamerV3: 像素 → CNN → RSSM (h, z)
```

### 规划方式
```
DQN: 无规划，ε-greedy
World Models: 梦境中训练 Controller
MuZero: 潜空间 MCTS
DreamerV3: 潜空间 Actor-Critic
```

### 样本效率
```
DQN: ~50M frames (Atari)
Double DQN: ~50M frames
MuZero: ~10M frames (等效)
DreamerV3: ~100K frames (Atari 100k)
```

**提升:** 500x 样本效率提升 (2015→2024)

---

## 关键洞察

### 1. 从 Value 到 Policy 到 Model
- Value-based (DQN): 简单但不灵活
- Policy-based (PPO): 可处理连续动作
- Model-based (Dreamer): 样本效率最高

### 2. 潜空间是核心
- 高维原始状态 → 低维潜空间
- 在潜空间学习动态、规划、决策
- 抽象表示是关键

### 3. 端到端训练
- 早期：多阶段分离训练
- 现代：单一损失函数端到端
- 更稳定，更易用

### 4. 通用 Agent
- 早期：针对环境调参
- DreamerV3: 单一配置 20+ 领域
- 迈向通用 RL

---

## 开放问题

### 1. 样本效率仍有提升空间
- DreamerV3: 100K frames (Atari)
- 人类：~10K frames
- 差距：10x

### 2. 长程规划
- 当前：短期预测 (<100 步)
- 挑战：长序列误差累积
- 方向：层次化模型

### 3. 迁移学习
- 当前：单任务训练
- 挑战：跨任务迁移
- 方向：预训练世界模型

### 4. 真实世界应用
- 当前：模拟环境为主
- 挑战：sim-to-real gap
- 方向：域随机化 + 自适应

---

## 研究方向建议

### 方向 1: 层次化世界模型
- 学习多尺度动态
- 短期 + 长期预测
- 层次化规划

### 方向 2: 预训练世界模型
- 大规模无标签数据预训练
- 下游任务微调
- 类似 RL 的"Foundation Model"

### 方向 3: 因果世界模型
- 学习因果关系而非相关性
- 干预推理
- 更好的泛化

### 方向 4: 多 Agent 世界模型
- 建模其他 Agent
- 社会推理
- 博弈场景

---

*学习时间：2026-03-05 22:04-22:14 | 小虾 🦐*
