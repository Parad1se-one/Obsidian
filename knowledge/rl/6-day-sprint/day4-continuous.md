# Day 4 - 连续控制算法 (DDPG, TD3, SAC)

**日期:** 2026-03-05
**主题:** DDPG, TD3, SAC
**状态:** ✅ 完成
**学习频率:** 每 10 分钟记录一次

---

## 📚 学习时间表

| 时间 | 内容 | 输出 | 状态 |
|------|------|------|------|
| 20:50-21:00 | DDPG 实现 | ddpg.py | ✅ |
| 21:00-21:10 | TD3 实现 | td3.py | ✅ |
| 21:10-21:20 | SAC 实现 | sac.py | ✅ |
| 21:20-21:30 | 学习日志 + Git 提交 | day4-continuous.md | ✅ |

---

## 💻 算法对比

### DDPG (Deep Deterministic Policy Gradient)

**核心思想:** DQN + Actor-Critic 的连续动作版本

**特点:**
- 确定性策略 (输出具体动作值)
- Target Network + 软更新
- Experience Replay

**更新:**
```python
# Critic: Q(s,a) → r + γQ'(s', π'(s'))
# Actor: max_a Q(s,a) ≈ Q(s, π(s))
```

---

### TD3 (Twin Delayed DDPG)

**三个关键改进:**

| 技术 | 作用 |
|------|------|
| **Twin Critic** | 双 Q 网络，取最小值，解决过估计 |
| **Delayed Update** | Actor 延迟更新 (每 2 步更新 1 次) |
| **Target Smoothing** | 目标动作加噪声，平滑 Q 值 |

**代码关键:**
```python
# Twin Critic
q1_next, q2_next = critic_target(next_states, next_actions)
next_q = torch.min(q1_next, q2_next)  # 取最小值

# Target Smoothing
noise = torch.randn_like(next_actions) * target_noise
noise = noise.clamp(-noise_clip, noise_clip)
next_actions = (next_actions + noise).clamp(-1, 1)

# Delayed Update
if total_steps % policy_delay == 0:
    update_actor()
```

---

### SAC (Soft Actor-Critic)

**核心思想:** 最大熵强化学习

**目标函数:**
$$J(\theta) = \mathbb{E}[\sum \gamma^t (r_t + \alpha \mathcal{H}(\pi(\cdot|s_t)))]$$

**特点:**
- 随机策略 (输出高斯分布)
- 自动温度系数 α
- Reparameterization trick

**代码关键:**
```python
# Reparameterization
x_t = dist.rsample()  # 可导采样
action = torch.tanh(x_t)
log_prob = dist.log_prob(x_t) - log(1 - tanh^2)

# Soft Q 更新
next_q = min(q1, q2) - alpha * log_prob
targets = r + γ * next_q

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
| 代码实现 | 1 | 3 | 2 | 3 | 9 |
| 知识笔记 | 2 | 3 | 2 | 1 | 8 |
| 学习时长 | 3h | 1h | 1h | 1h | 6h |

**6 天冲刺进度:** 4/6 = 67% ✅

---

## 📄 提交文件

- [x] `code/rl-continuous/ddpg.py`
- [x] `code/rl-continuous/td3.py`
- [x] `code/rl-continuous/sac.py`
- [x] `knowledge/rl/6-day-sprint/day4-continuous.md`

---

## 🎯 Day 5 计划 (模型基础 RL)

**主题:** MuZero, DreamerV3, World Models

| 时间 | 内容 | 输出 |
|------|------|------|
| 21:30-21:40 | World Models 论文 + 实现 | world-models.py |
| 21:40-21:50 | MuZero 论文笔记 | muzero-notes.md |
| 21:50-22:00 | DreamerV3 论文笔记 | dreamer-notes.md |
| 22:00-22:10 | 简单环境模型实现 | model-based.py |
| 22:10-22:20 | 学习日志 + Git | day5-model-based.md |

---

*🦐 小虾：Day 4 完成！连续控制算法掌握！继续冲刺 Day 5！*

**提交时间:** 2026-03-05 21:30
