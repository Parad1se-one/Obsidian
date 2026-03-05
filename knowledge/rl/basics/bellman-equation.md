# 贝尔曼方程 (Bellman Equation)

## 核心思想

值函数可以递归地表示为即时奖励和未来值的期望。

## 贝尔曼期望方程

### 状态值函数
$$V^\pi(s) = \mathbb{E}_\pi[R_{t+1} + \gamma V^\pi(S_{t+1}) | S_t = s]$$

展开形式:
$$V^\pi(s) = \sum_a \pi(a|s) \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^\pi(s')]$$

### 动作值函数
$$Q^\pi(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma \sum_{a'} \pi(a'|s') Q^\pi(s',a')]$$

## 贝尔曼最优方程

### 最优状态值函数
$$V^*(s) = \max_a \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^*(s')]$$

### 最优动作值函数
$$Q^*(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma \max_{a'} Q^*(s',a')]$$

## 求解方法

### 值迭代 (Value Iteration)
```python
def value_iteration(mdp, gamma=0.99, theta=1e-6):
    V = np.zeros(len(mdp.states))
    while True:
        delta = 0
        for s in mdp.states:
            v = V[s]
            V[s] = max(a, sum(p * (r + gamma * V[s_]) 
                              for p, s_, r, _ in mdp.P[s][a]))
            delta = max(delta, abs(v - V[s]))
        if delta < theta:
            break
    return V
```

### 策略迭代 (Policy Iteration)
1. 策略评估：计算 V^π
2. 策略改进：π' = greedy(π)
3. 重复直到收敛

## 直观理解

贝尔曼方程的核心是**自洽性**：一个状态的值等于即时奖励加上下一个状态的折扣值。

---
*最后更新：2026-03-05*
