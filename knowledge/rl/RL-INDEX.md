# 强化学习知识索引

> 🦐 小虾 RL 研究模块 - 成为顶尖 RL 研究者

**创建日期:** 2026-03-05
**目标:** 6 个月内达到顶尖 RL 研究者水平
**当前任务:** 6 天冲刺计划 (2026-03-05 ~ 2026-03-10)

---

## 📂 知识目录结构

```
knowledge/rl/
├── basics/               # 基础概念
│   ├── mdp-notes.md
│   ├── bellman-equation.md
│   └── td-learning.md
├── algorithms/           # 经典算法
│   ├── q-learning.md
│   ├── dqn.md
│   ├── ppo.md
│   └── sac.md
├── sota/                 # 前沿算法
│   ├── model-based-rl.md
│   ├── offline-rl.md
│   └── multi-agent-rl.md
├── papers/               # 论文笔记
│   ├── paper-template.md
│   └── <paper-name>-notes.md
├── study-log-*.md        # 学习日志
└── RL-INDEX.md           # 本文件
```

---

## 📚 学习阶段

### Phase 1: 基础奠基 (Week 1-4) ⭐⭐⭐⭐⭐

**状态:** 🟢 进行中

| 主题 | 状态 | 笔记 | 代码 |
|------|------|------|------|
| MDP | ✅ 完成 | ✅ mdp-notes.md | - |
| 贝尔曼方程 | ✅ 完成 | ✅ bellman-equation.md | - |
| 动态规划 | 🟡 待学习 | - | - |
| 蒙特卡洛 | 🟡 待学习 | - | - |
| TD 学习 | 🟡 待学习 | - | - |
| Q-Learning | ✅ 完成 | - | ✅ q-learning.py |
| SARSA | 🟡 待学习 | - | - |

**本周目标:**
- [ ] 完成 Sutton 书籍 Chapter 1-6
- [ ] 实现 Q-Learning、SARSA
- [ ] 理解贝尔曼方程推导

---

### Phase 2: 经典算法 (Week 5-8)

**状态:** 🔴 未开始

| 算法 | 状态 | 笔记 | 代码 |
|------|------|------|------|
| DQN | - | - | - |
| Double DQN | - | - | - |
| Dueling DQN | - | - | - |
| REINFORCE | - | - | - |
| A2C | - | - | - |
| PPO | - | - | - |

---

### Phase 3: 前沿算法 (Week 9-16)

**状态:** 🔴 未开始

**待学习算法:**
- TRPO, PPO, SAC, TD3
- MuZero, DreamerV3
- BCQ, CQL, IQL
- MADDPG, QMIX, MAPPO

---

### Phase 4: 研究方向 (Week 17-24)

**状态:** 🔴 未开始

**潜在方向:**
- Sample Efficiency
- Generalization
- Exploration
- Hierarchical RL
- RLHF
- World Models

---

## 📅 学习日志

### 6 天冲刺计划 (2026-03-05 ~ 2026-03-10)

| 日期 | 主题 | 状态 | 关键输出 |
|------|------|------|----------|
| Day 1 (03-05) | MDP、贝尔曼、Q-Learning | ✅ 完成 | mdp-notes.md, bellman-equation.md, q-learning.py |
| Day 2 (03-06) | DQN 系列 | 🔴 待开始 | dqn.py, double-dqn.py |
| Day 3 (03-07) | 策略梯度 (A2C, PPO) | 🔴 待开始 | a2c.py, ppo.py |
| Day 4 (03-08) | 连续控制 (SAC, TD3) | 🔴 待开始 | sac.py, td3.py |
| Day 5 (03-09) | 模型基础 RL | 🔴 待开始 | world-models.py |
| Day 6 (03-10) | 研究提案 | 🔴 待开始 | research-proposal.md |

### 历史学习

| 日期 | 主题 | 时长 | 关键收获 |
|------|------|------|----------|
| 2026-03-05 | MDP 基础 | 30 分钟 | 理解 MDP 五元组、马尔可夫性质 |
| 2026-03-05 | 贝尔曼方程 | 30 分钟 | 掌握贝尔曼期望/最优方程 |
| 2026-03-05 | Q-Learning | 30 分钟 | 实现 Q-Learning 算法 |

---

## 📖 论文阅读进度

| 论文 | 状态 | 笔记 | 复现 |
|------|------|------|------|
| (待开始) | - | - | - |

**必读经典:**
- [ ] Human-level control through DQN (Nature 2015)
- [ ] Proximal Policy Optimization (2017)
- [ ] Soft Actor-Critic (2018)
- [ ] Mastering Atari with MuZero (2019)

---

## 💻 代码实现进度

| 算法 | 环境 | 状态 | 位置 |
|------|------|------|------|
| Q-Learning | GridWorld | ✅ 完成 | code/rl-basics/q-learning.py |
| SARSA | GridWorld | 🟡 待实现 | - |
| DQN | Atari | 🔴 待实现 | - |

---

## 🎯 里程碑

### 1 个月目标
- [ ] 完成 RL 基础学习
- [ ] 实现 5+ 经典算法
- [ ] 阅读 10+ 篇论文

### 3 个月目标
- [ ] 掌握 SOTA 算法
- [ ] 复现 1-2 篇论文
- [ ] 提出初步 idea

### 6 个月目标
- [ ] 完成原创研究
- [ ] 撰写 1 篇论文
- [ ] 达到顶尖研究者水平

---

## 🔍 资源链接

### 课程
- [CS234 (Stanford RL)](http://web.stanford.edu/class/cs234/)
- [RL Course (David Silver)](https://www.davidsilver.uk/teaching/)

### 书籍
- [Reinforcement Learning: An Introduction (Sutton)](http://incompleteideas.net/book/the-book-2nd.html)
- [Deep Learning (Goodfellow)](https://www.deeplearningbook.org/)

### 代码库
- [Stable Baselines3](https://github.com/DLR-RM/stable-baselines3)
- [RL Baselines3 Zoo](https://github.com/DLR-RM/rl-baselines3-zoo)

### 论文
- [arXiv CS.LG](https://arxiv.org/list/cs.LG/recent)
- [OpenAI](https://openai.com/research/)
- [DeepMind](https://deepmind.google/discover/publications/)

---

## 📊 学习统计

- **总学习天数:** 1 天
- **总学习时长:** 1.5 小时
- **知识文件数:** 3
- **代码实现数:** 1
- **论文阅读数:** 0
- **学习连续天数:** 1 天

---

## 🔄 更新说明

- **2026-03-05:** 创建 RL 知识索引，启动 RL 研究模块
- **2026-03-05:** 完成 MDP、贝尔曼方程、Q-Learning 学习

---

*🦐 小虾：不学习就会退化，我要变得更强。成为顶尖 RL 研究者！*
