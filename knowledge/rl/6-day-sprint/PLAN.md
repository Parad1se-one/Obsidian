# RL 6 天冲刺计划

> 🦐 小虾：6 天完成前 3 个月计划！疯狂但必须完成！

**原始计划:** 3 个月 (12 周)
**新计划:** 6 天 (每天 ≈ 2 周内容)

---

## 📅 每日计划

### Day 1 (2026-03-05) - RL 基础 ✅

**目标:** 掌握 MDP、贝尔曼方程、基础算法

| 时段 | 内容 | 输出 |
|------|------|------|
| 上午 | MDP 基础 | mdp-notes.md |
| 下午 | 贝尔曼方程 | bellman-equation.md |
| 晚间 | Q-Learning 实现 | q-learning.py |

**状态:** ✅ 完成 (19:28)

---

### Day 2 (2026-03-06) - 深度 Q 学习

**目标:** 掌握 DQN 系列算法

| 时段 | 内容 | 输出 |
|------|------|------|
| 上午 | DQN 论文阅读 | dqn-paper-notes.md |
| 下午 | DQN 实现 | dqn.py (Atari) |
| 晚间 | Double/Dueling DQN | double-dueling-dqn.py |

**必读论文:**
- Mnih et al. "Human-level control through DQN" Nature 2015
- Van Hasselt et al. "Deep Reinforcement Learning with Double Q-learning" AAAI 2016
- Wang et al. "Dueling Network Architectures for DRL" ICML 2016

**代码任务:**
- [ ] 实现 DQN (PyTorch)
- [ ] 经验回放缓冲区
- [ ] 目标网络
- [ ] 在 Atari Pong 上训练

---

### Day 3 (2026-03-07) - 策略梯度方法

**目标:** 掌握 Policy Gradient、A2C、PPO

| 时段 | 内容 | 输出 |
|------|------|------|
| 上午 | REINFORCE、Actor-Critic | policy-gradient-notes.md |
| 下午 | A2C 实现 | a2c.py |
| 晚间 | PPO 实现 | ppo.py |

**必读论文:**
- Sutton et al. "Policy Gradient Methods for Reinforcement Learning" 2000
- Mnih et al. "Asynchronous Methods for DRL" ICML 2016 (A3C)
- Schulman et al. "Proximal Policy Optimization Algorithms" 2017

**代码任务:**
- [ ] 实现 REINFORCE
- [ ] 实现 A2C
- [ ] 实现 PPO (clipped surrogate objective)
- [ ] 在 CartPole、LunarLander 上测试

---

### Day 4 (2026-03-08) - 连续控制与 SOTA

**目标:** 掌握 SAC、TD3 等连续控制算法

| 时段 | 内容 | 输出 |
|------|------|------|
| 上午 | DDPG、TD3 | ddpg-td3-notes.md |
| 下午 | SAC 实现 | sac.py |
| 晚间 | 算法对比实验 | algorithm-comparison.md |

**必读论文:**
- Lillicrap et al. "Continuous Control with DDPG" ICLR 2016
- Fujimoto et al. "TD3: Addressing Function Approximation Error" ICML 2018
- Haarnoja et al. "Soft Actor-Critic" ICML 2018

**代码任务:**
- [ ] 实现 DDPG
- [ ] 实现 TD3
- [ ] 实现 SAC
- [ ] 在 MuJoCo (Pendulum, HalfCheetah) 上测试

---

### Day 5 (2026-03-09) - 模型基础 RL 与前沿

**目标:** 掌握 MuZero、Dreamer 等 SOTA

| 时段 | 内容 | 输出 |
|------|------|------|
| 上午 | MuZero 论文阅读 | muzero-notes.md |
| 下午 | DreamerV3 论文阅读 | dreamer-notes.md |
| 晚间 | World Models 实现 | world-models.py |

**必读论文:**
- Schrittwieser et al. "Mastering Atari with MuZero" Nature 2019
- Hafner et al. "Dream to Control" ICLR 2020
- Hafner et al. "Mastering Diverse Domains through World Models" 2023 (DreamerV3)

**代码任务:**
- [ ] 实现简单 World Model
- [ ] 潜空间预测
- [ ] 基于模型的规划

---

### Day 6 (2026-03-10) - 研究提案与实验设计

**目标:** 提出原创 idea，设计实验

| 时段 | 内容 | 输出 |
|------|------|------|
| 上午 | 文献调研、识别空白 | research-gap-analysis.md |
| 下午 | Idea 提案 | research-proposal.md |
| 晚间 | 实验设计、开始初步实验 | experiment-design.md |

**研究方向候选:**
1. **Sample Efficiency** - 结合模型和无模型方法
2. **Generalization** - 数据增强 + 域随机化
3. **Exploration** - 内在动机 + 好奇心
4. **RLHF** - 从人类偏好学习
5. **Hierarchical RL** - 目标条件策略

**输出:**
- [ ] 研究提案文档
- [ ] 实验设计
- [ ] 初步代码框架
- [ ] 论文草稿大纲

---

## 📊 每日时间分配

```
08:00-12:00  理论学习 + 论文阅读 (4h)
14:00-18:00  代码实现 (4h)
20:00-23:00  实验运行 + 文档整理 (3h)
────────────────────────────
总计：11 小时/天
```

---

## 📁 GitHub 文档结构

```
obsidian-repo/
├── knowledge/rl/
│   ├── 6-day-sprint/
│   │   ├── day1-basics.md
│   │   ├── day2-dqn.md
│   │   ├── day3-policy.md
│   │   ├── day4-continuous.md
│   │   ├── day5-model-based.md
│   │   └── day6-research.md
│   ├── basics/
│   ├── algorithms/
│   └── papers/
├── code/
│   ├── rl-basics/
│   ├── rl-dqn/
│   ├── rl-policy/
│   └── rl-sota/
└── research/
    ├── proposals/
    └── experiments/
```

---

## ✅ 每日提交要求

**每天必须完成:**
1. 学习日志 `knowledge/rl/6-day-sprint/dayX-*.md`
2. 代码实现 `code/rl-*/`
3. Git 提交并 push
4. 更新 RL-INDEX.md 进度

**提交信息格式:**
```
🤖 RL 6-Day Sprint: Day X - <主题>
- 学习内容：...
- 代码实现：...
- 论文阅读：...
```

---

## 🎯 成功标准

### Day 1 ✅
- [x] MDP 笔记
- [x] 贝尔曼方程笔记
- [x] Q-Learning 实现

### Day 2
- [ ] DQN 论文笔记
- [ ] DQN 实现 (能玩 Atari)
- [ ] Double/Dueling DQN 实现

### Day 3
- [ ] 策略梯度笔记
- [ ] A2C 实现
- [ ] PPO 实现 (能解决连续控制)

### Day 4
- [ ] DDPG/TD3笔记
- [ ] SAC 实现
- [ ] 算法对比实验

### Day 5
- [ ] MuZero 笔记
- [ ] DreamerV3 笔记
- [ ] World Model 实现

### Day 6
- [ ] 研究提案
- [ ] 实验设计
- [ ] 论文草稿大纲

---

## 🦐 承诺

**6 天后，我将:**
- 掌握 RL 主流算法
- 有 10+ 个算法实现
- 阅读 20+ 篇核心论文
- 提出 1-2 个原创 idea
- 设计完整实验方案

**开始时间:** 2026-03-05 19:30
**结束时间:** 2026-03-10 23:00

**没有退路，只能前进！** 🦐
