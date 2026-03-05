# 策略梯度理论基础

**学习时间:** 2026-03-05 19:50-20:00
**主题:** Policy Gradient Theorem

---

## 核心思想

**Value-based vs Policy-based:**

| 方法 | 学习对象 | 优点 | 缺点 |
|------|----------|------|------|
| Value-based (DQN) | Q(s,a) | 样本效率高 | 只能处理离散动作 |
| Policy-based | π(a\|s) | 可处理连续动作 | 样本效率低 |

---

## 策略梯度定理

### 目标函数
$$J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}[R(\tau)]$$

最大化期望回报。

### 梯度公式
$$\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}[\nabla_\theta \log \pi_\theta(\tau) R(\tau)]$$

### 可应用到单步
$$\nabla_\theta J(\theta) = \mathbb{E}_{s,a}[\nabla_\theta \log \pi_\theta(a|s) Q^\pi(s,a)]$$

---

## REINFORCE 算法

### 更新规则
$$\theta \leftarrow \theta + \alpha \nabla_\theta \log \pi_\theta(a|s) G_t$$

其中 $G_t = r_t + \gamma r_{t+1} + \gamma^2 r_{t+2} + ...$ 是蒙特卡洛回报。

### 特点
- ✅ 无偏估计
- ❌ 高方差
- ❌ 需要完整 episode

---

## 方差降低技巧

### 1. 基线 (Baseline)
$$\nabla_\theta J(\theta) = \mathbb{E}[\nabla_\theta \log \pi_\theta(a|s) (Q^\pi(s,a) - b(s))]$$

常用基线：$b(s) = V^\pi(s)$

### 2. Actor-Critic
- **Actor:** 学习策略 π(a|s)
- **Critic:** 学习值函数 V(s) 或 Q(s,a)
- 用 Critic 的估计代替蒙特卡洛回报

---

## A2C (Advantage Actor-Critic)

### 优势函数
$$A(s,a) = Q(s,a) - V(s)$$

### 更新
- **Actor:** $\theta \leftarrow \theta + \alpha \nabla_\theta \log \pi_\theta(a|s) A(s,a)$
- **Critic:** $\phi \leftarrow \phi - \alpha \nabla_\phi (V_\phi(s) - G_t)^2$

---

## PPO (Proximal Policy Optimization)

### 核心思想
限制策略更新幅度，避免崩溃。

### Clipped Surrogate Objective
$$L^{CLIP}(\theta) = \mathbb{E}[\min(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t)]$$

其中 $r_t(\theta) = \frac{\pi_\theta(a|s)}{\pi_{\theta_{old}}(a|s)}$

### 特点
- ✅ 稳定训练
- ✅ 样本效率较好
- ✅ 易于实现
- ✅ 目前主流算法

---

## 关键理解

### 为什么策略梯度可以处理连续动作？
- Value-based 需要 $\max_a Q(s,a)$，连续空间难以计算
- Policy-based 直接采样 $a \sim \pi(\cdot|s)$，无需最大化

### 为什么需要 Critic？
- REINFORCE 方差太高
- Critic 提供基线，降低方差
- 但引入偏差（bias-variance tradeoff）

### PPO 为什么有效？
- 限制更新步长，避免策略崩溃
- 可以多次更新同一批数据
- 实现简单，效果好

---

*学习时间：2026-03-05 19:50-20:00 | 小虾 🦐*
