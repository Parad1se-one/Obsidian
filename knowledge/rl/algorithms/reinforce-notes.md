# REINFORCE 算法笔记

**学习时间:** 2026-03-05 20:00-20:10
**主题:** REINFORCE (Monte Carlo Policy Gradient)

---

## 基本信息
- **论文:** "Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning"
- **作者:** Ronald J. Williams
- **年份:** 1992
- **核心:** 最基础的策略梯度算法

---

## 算法原理

### 策略表示
$$\pi(a|s, \theta) = \frac{e^{h(s,a,\theta)}}{\sum_b e^{h(s,b,\theta)}}$$

### 更新规则
$$\theta \leftarrow \theta + \alpha G_t \nabla_\theta \log \pi(a|s, \theta)$$

其中 $G_t = \sum_{k=0}^{\infty} \gamma^k r_{t+k+1}$

---

## REINFORCE 实现

```python
"""
REINFORCE 算法实现
小虾 🦐 | 2026-03-05 20:00
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import gym

class PolicyNetwork(nn.Module):
    """策略网络 - 输出动作概率分布"""
    def __init__(self, state_dim, n_actions):
        super(PolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, 128)
        self.fc2 = nn.Linear(128, n_actions)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return torch.softmax(x, dim=-1)
    
    def get_action(self, state):
        """采样动作"""
        probs = self.forward(torch.FloatTensor(state))
        dist = torch.distributions.Categorical(probs)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        return action.item(), log_prob


class REINFORCE:
    """REINFORCE Agent"""
    def __init__(self, state_dim, n_actions, lr=1e-3, gamma=0.99):
        self.gamma = gamma
        self.policy = PolicyNetwork(state_dim, n_actions)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)
    
    def select_action(self, state):
        return self.policy.get_action(state)
    
    def update(self, states, actions, log_probs, rewards):
        """更新策略"""
        # 计算折扣回报 G_t
        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + self.gamma * G
            returns.insert(0, G)
        returns = torch.FloatTensor(returns)
        
        # 标准化 returns (降低方差)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        
        # 计算策略梯度损失
        policy_gradient = []
        for log_prob, G in zip(log_probs, returns):
            policy_gradient.append(-log_prob * G)
        
        loss = torch.stack(policy_gradient).sum()
        
        # 反向传播
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item()
    
    def train_episode(self, env):
        """训练一个 episode"""
        states, actions, log_probs, rewards = [], [], [], []
        
        state = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            action, log_prob = self.select_action(state)
            next_state, reward, done, _ = env.step(action)
            
            states.append(state)
            actions.append(action)
            log_probs.append(log_prob)
            rewards.append(reward)
            
            total_reward += reward
            state = next_state
        
        # 更新
        loss = self.update(states, actions, log_probs, rewards)
        
        return total_reward, loss


def train_reinforce(env, n_episodes=1000):
    """训练循环"""
    agent = REINFORCE(state_dim=4, n_actions=2)  # CartPole
    rewards_per_episode = []
    
    for episode in range(n_episodes):
        reward, loss = agent.train_episode(env)
        rewards_per_episode.append(reward)
        
        if episode % 50 == 0:
            avg = np.mean(rewards_per_episode[-50:])
            print(f"Episode {episode}, Avg Reward: {avg:.2f}")
    
    return agent, rewards_per_episode


if __name__ == "__main__":
    env = gym.make('CartPole-v1')
    agent, rewards = train_reinforce(env, n_episodes=500)
    print("✅ REINFORCE 训练完成")
```

---

## 关键要点

### 1. 蒙特卡洛采样
- 需要完整 episode 才能更新
- 无偏估计，但高方差

### 2. 对数概率技巧
$$\nabla_\theta \log \pi(a|s) = \frac{\nabla_\theta \pi(a|s)}{\pi(a|s)}$$

### 3. 方差降低
- 基线减法
- 回报标准化
- 增加采样

---

## 优缺点

| 优点 | 缺点 |
|------|------|
| 简单易懂 | 高方差 |
| 无偏估计 | 样本效率低 |
| 可处理连续动作 | 需要完整 episode |
| 收敛到局部最优 | 训练不稳定 |

---

*学习时间：2026-03-05 20:00-20:10 | 小虾 🦐*
