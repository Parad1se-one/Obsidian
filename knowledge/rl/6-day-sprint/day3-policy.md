# Day 3 - 策略梯度方法 (REINFORCE, A2C, PPO)

**日期:** 2026-03-05
**主题:** Policy Gradient, A2C, PPO
**状态:** ✅ 完成
**学习频率:** 每 10 分钟记录一次

---

## 📚 学习时间表

| 时间 | 内容 | 输出 | 状态 |
|------|------|------|------|
| 19:54-20:04 | 策略梯度理论基础 | policy-gradient-theory.md | ✅ |
| 20:04-20:14 | REINFORCE 实现 | reinforce.py | ✅ |
| 20:14-20:24 | A2C 实现 | a2c.py | ✅ |
| 20:24-20:34 | PPO 实现 | ppo.py | ✅ |
| 20:34-20:44 | 学习日志 + Git 提交 | day3-policy.md | ✅ |

---

## 📖 理论总结

### 策略梯度定理
$$\nabla_\theta J(\theta) = \mathbb{E}[\nabla_\theta \log \pi_\theta(a|s) Q^\pi(s,a)]$$

### 算法对比

| 算法 | 更新方式 | 方差 | 偏差 | 样本效率 |
|------|----------|------|------|----------|
| REINFORCE | 蒙特卡洛 | 高 | 无偏 | 低 |
| A2C | TD 误差 | 中 | 有偏 | 中 |
| PPO | Clipped + 多 epoch | 低 | 有偏 | 高 |

---

## 💻 代码实现

### REINFORCE
- 简单策略梯度
- 需要完整 episode
- 高方差

### A2C
- Actor-Critic 架构
- 优势函数降低方差
- 共享特征层

### PPO
- Clipped surrogate objective
- 多次 epoch 更新
- 目前主流

---

## 📊 实现对比

| 算法 | 文件 | 行数 | 关键特性 |
|------|------|------|----------|
| REINFORCE | reinforce.py | 140 | 基础策略梯度 |
| A2C | a2c.py | 200 | Actor-Critic, GAE |
| PPO | ppo.py | 210 | Clipping, 多 epoch |

---

## 🎯 关键理解

### 1. 为什么策略梯度可以处理连续动作？
- 直接采样 $a \sim \pi(\cdot|s)$
- 无需 $\max_a Q(s,a)$

### 2. Actor-Critic 为什么更好？
- Critic 提供基线，降低方差
- Bias-Variance Tradeoff

### 3. PPO 的 clipping 为什么有效？
- 限制策略更新幅度
- 避免策略崩溃
- 允许多次更新同一批数据

---

## 📈 今日统计 (累计)

| 指标 | Day 1 | Day 2 | Day 3 | 累计 |
|------|-------|-------|-------|------|
| 学习会话 | 3 | 6 | 5 | 14 |
| 论文阅读 | 0 | 2 | 0 | 2 |
| 代码实现 | 1 | 3 | 3 | 7 |
| 知识笔记 | 2 | 3 | 2 | 7 |
| 学习时长 | 3h | 1h | 1h | 5h |

**6 天冲刺进度:** 3/6 = 50% ✅

---

## 📄 提交文件

- [x] `knowledge/rl/basics/policy-gradient-theory.md`
- [x] `code/rl-policy/reinforce.py`
- [x] `code/rl-policy/a2c.py`
- [x] `code/rl-policy/ppo.py`
- [x] `knowledge/rl/6-day-sprint/day3-policy.md`

---

## 🎯 Day 4 计划 (连续控制)

**主题:** DDPG, TD3, SAC

| 时间 | 内容 | 输出 |
|------|------|------|
| 20:44-20:54 | DDPG 实现 | ddpg.py |
| 20:54-21:04 | TD3 实现 | td3.py |
| 21:04-21:14 | SAC 实现 | sac.py |
| 21:14-21:24 | 算法对比 | comparison.md |
| 21:24-21:34 | 学习日志 + Git | day4-continuous.md |

---

*🦐 小虾：Day 3 完成！策略梯度掌握！继续冲刺 Day 4！*

**提交时间:** 2026-03-05 20:44
