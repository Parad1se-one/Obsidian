# Day 4 - 连续控制算法 (DDPG, TD3, SAC)

**日期:** 2026-03-05
**主题:** DDPG, TD3, SAC
**状态:** ✅ 完成
**学习频率:** 每 10 分钟记录一次

---

## 📚 学习时间表

| 时间 | 内容 | 输出 | 状态 |
|------|------|------|------|
| 20:44-20:54 | DDPG 实现 | ddpg.py | ✅ |
| 20:54-21:04 | TD3 实现 | td3.py | ✅ |
| 21:04-21:14 | SAC 实现 | sac.py | ✅ |
| 21:14-21:24 | 学习日志 + Git 提交 | day4-continuous.md | ✅ |

---

## 💻 算法对比

### DDPG (Deep Deterministic Policy Gradient)

**核心思想:** DQN + Actor-Critic 的连续动作版本

**特点:**
- 确定性策略 (输出具体动作值)
- Target Network + 软更新
- Experience Replay

---

### TD3 (Twin Delayed DDPG)

**三个关键改进:**

| 技术 | 作用 | 代码 |
|------|------|------|
| **Twin Critic** | 双 Q 网络，取最小值，解决过估计 | `next_q = torch.min(q1_next, q2_next)` |
| **Delayed Update** | Actor 延迟更新 (每 2 步更新 1 次) | `if total_steps % policy_delay == 0` |
| **Target Smoothing** | 目标动作加噪声，平滑 Q 值 | `noise = torch.randn_like() * target_noise` |

---

### SAC (Soft Actor-Critic)

**核心思想:** 最大熵强化学习

**特点:**
- 随机策略 (输出高斯分布)
- 自动温度系数 α
- Reparameterization trick

**关键代码:**
```python
# Reparameterization
x_t = dist.rsample()  # 可导采样
action = torch.tanh(x_t)
log_prob = dist.log_prob(x_t) - log(1 - tanh^2)

# Soft Q 更新
next_q = min(q1, q2) - alpha * log_prob

# Alpha 更新
alpha_loss = -(log_alpha * (log_prob + target_entropy).detach()).mean()
```

---

## 📊 算法对比表

| 算法 | 策略类型 | Critic 数 | 关键创新 | 稳定性 |
|------|----------|-----------|----------|--------|
| DDPG | 确定性 | 1 | 基础连续控制 | ⭐⭐ |
| TD3 | 确定性 | 2 | Twin+Delayed+Smoothing | ⭐⭐⭐⭐ |
| SAC | 随机性 | 2 | 最大熵 + 自动α | ⭐⭐⭐⭐⭐ |

---

## 🎯 关键理解

### 1. 为什么需要 Twin Critic？
- 单 Critic 容易过估计
- 取最小值类似 Double DQN 思想

### 2. 为什么 Actor 要延迟更新？
- Critic 需要时间准确估计 Q 值
- 避免 Actor 利用不准确的 Critic

### 3. 为什么 SAC 用随机策略？
- 更好的探索
- 熵正则化避免过早收敛
- 更适合复杂任务

### 4. Reparameterization trick 是什么？
- 将随机性从网络输出中分离
- 使得梯度可以反向传播
- $a = \mu + \sigma \cdot \epsilon$, $\epsilon \sim \mathcal{N}(0,1)$

---

## 📈 今日统计 (累计)

| 指标 | Day 1 | Day 2 | Day 3 | Day 4 | 累计 |
|------|-------|-------|-------|-------|------|
| 学习会话 | 3 | 6 | 5 | 4 | 18 |
| 论文阅读 | 0 | 2 | 0 | 0 | 2 |
| 代码实现 | 1 | 3 | 3 | 3 | 10 |
| 知识笔记 | 2 | 3 | 2 | 1 | 8 |
| 学习时长 | 3h | 1h | 1h | 1h | 6h |

**6 天冲刺进度:** 4/6 = 67% ✅

---

## 📄 提交文件

- [x] `code/rl-continuous/ddpg.py` (230 行)
- [x] `code/rl-continuous/td3.py` (220 行)
- [x] `code/rl-continuous/sac.py` (280 行)
- [x] `knowledge/rl/6-day-sprint/day4-continuous.md`

---

## 🎯 Day 5 计划 (模型基础 RL)

**主题:** World Models, MuZero, DreamerV3

| 时间 | 内容 | 输出 |
|------|------|------|
| 21:24-21:34 | World Models 论文 | world-models-notes.md |
| 21:34-21:44 | MuZero 论文 | muzero-notes.md |
| 21:44-21:54 | DreamerV3 论文 | dreamer-notes.md |
| 21:54-22:04 | 简单环境模型实现 | model-based.py |
| 22:04-22:14 | 学习日志 + Git | day5-model-based.md |

---

*🦐 小虾：Day 4 完成！连续控制算法掌握！继续冲刺 Day 5！*

**提交时间:** 2026-03-05 21:24
