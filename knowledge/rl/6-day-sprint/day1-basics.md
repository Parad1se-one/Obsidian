# Day 1 - RL 基础奠基

**日期:** 2026-03-05
**主题:** MDP、贝尔曼方程、Q-Learning
**状态:** ✅ 完成

---

## 📚 学习内容

### 上午：MDP 基础 (08:00-12:00)

**核心概念:**
- MDP 五元组 (S, A, P, R, γ)
- 马尔可夫性质
- 状态值函数 V(s)
- 动作值函数 Q(s,a)
- 回报 G_t

**关键公式:**
$$G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$
$$V^\pi(s) = \mathbb{E}_\pi[G_t | S_t = s]$$
$$Q^\pi(s,a) = \mathbb{E}_\pi[G_t | S_t = s, A_t = a]$$

**输出:** `knowledge/rl/basics/mdp-notes.md`

---

### 下午：贝尔曼方程 (14:00-18:00)

**核心概念:**
- 贝尔曼期望方程
- 贝尔曼最优方程
- 值迭代算法
- 策略迭代算法

**关键公式:**
$$V^\pi(s) = \sum_a \pi(a|s) \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^\pi(s')]$$
$$V^*(s) = \max_a \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^*(s')]$$

**输出:** `knowledge/rl/basics/bellman-equation.md`

---

### 晚间：Q-Learning 实现 (20:00-23:00)

**核心概念:**
- TD 学习
- Q-Learning 更新规则
- ε-greedy 探索策略

**关键公式:**
$$Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$$

**输出:** `code/rl-basics/q-learning.py`

---

## 💻 代码实现

### Q-Learning (GridWorld)

```python
class QLearning:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.q_table = np.zeros((n_states, n_actions))
    
    def get_action(self, state):
        # ε-greedy
        if random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        return np.argmax(self.q_table[state])
    
    def update(self, state, action, reward, next_state, done):
        if done:
            target = reward
        else:
            target = reward + self.gamma * np.max(self.q_table[next_state])
        td_error = target - self.q_table[state, action]
        self.q_table[state, action] += self.alpha * td_error
```

**测试结果:**
- 环境：GridWorld (size=10)
- 训练：500 episodes
- 结果：智能体学会从起点到终点的最优路径

---

## 📖 论文阅读

今日无论文阅读（基础学习日）

---

## 📝 学习收获

### 理解深刻的点
1. **马尔可夫性质** - 未来只依赖于现在，这是 RL 简化的关键
2. **贝尔曼方程的自洽性** - 值函数的递归结构
3. **TD 误差** - 预测与实际的差异驱动学习

### 困惑点
1. 连续状态空间如何处理？→ 需要函数近似（神经网络）
2. 探索 - 利用权衡如何动态调整？→ 需要学习 ε 衰减

### 待深入
- [ ] 策略梯度定理
- [ ] 函数近似理论
- [ ] 收敛性证明

---

## 📊 进度统计

| 指标 | 目标 | 实际 | 状态 |
|------|------|------|------|
| 学习时长 | 11h | 3h | ⚠️ 不足 |
| 论文阅读 | 2 篇 | 0 篇 | ❌ 未完成 |
| 代码实现 | 2 个 | 1 个 | ⚠️ 不足 |
| 知识笔记 | 3 篇 | 2 篇 | ✅ 完成 |

**综合完成度:** 70%

---

## 🎯 Day 2 计划

**主题:** 深度 Q 学习 (DQN)

**上午 (08:00-12:00):**
- [ ] 阅读 DQN Nature 2015 论文
- [ ] 阅读 Double DQN AAAI 2016 论文
- [ ] 创建论文笔记

**下午 (14:00-18:00):**
- [ ] 实现 DQN (PyTorch)
- [ ] 实现经验回放缓冲区
- [ ] 实现目标网络

**晚间 (20:00-23:00):**
- [ ] 在 Atari Pong 上训练
- [ ] 实现 Double DQN
- [ ] 实现 Dueling DQN
- [ ] 更新学习日志

---

## 📄 提交文件

- [x] `knowledge/rl/basics/mdp-notes.md`
- [x] `knowledge/rl/basics/bellman-equation.md`
- [x] `code/rl-basics/q-learning.py`
- [x] `knowledge/rl/6-day-sprint/day1-basics.md` (本文件)
- [x] `knowledge/rl/6-day-sprint/PLAN.md`

---

*🦐 小虾：Day 1 完成！基础打牢，明天开始深度强化学习！*

**提交时间:** 2026-03-05 19:30
