"""
REINFORCE 算法实现
Monte Carlo Policy Gradient

小虾 🦐 | 2026-03-05 20:04
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import gym

# ==================== 策略网络 ====================

class PolicyNetwork(nn.Module):
    """策略网络 - 输出动作概率分布"""
    def __init__(self, state_dim, n_actions, hidden_dim=128):
        super(PolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, n_actions)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return torch.softmax(x, dim=-1)
    
    def get_action(self, state):
        """采样动作"""
        with torch.no_grad():
            probs = self.forward(torch.FloatTensor(state))
            dist = torch.distributions.Categorical(probs)
            action = dist.sample()
            log_prob = dist.log_prob(action)
        return action.item(), log_prob


# ==================== REINFORCE Agent ====================

class REINFORCE:
    """REINFORCE Agent"""
    def __init__(self, state_dim, n_actions, lr=1e-3, gamma=0.99):
        self.gamma = gamma
        self.policy = PolicyNetwork(state_dim, n_actions)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)
    
    def select_action(self, state):
        return self.policy.get_action(state)
    
    def update(self, states, actions, log_probs, rewards):
        """更新策略 - 使用完整 episode 的回报"""
        # 计算折扣回报 G_t
        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + self.gamma * G
            returns.insert(0, G)
        returns = torch.FloatTensor(returns)
        
        # 标准化 returns (降低方差)
        if len(returns) > 1:
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


def train_reinforce(env_name='CartPole-v1', n_episodes=1000):
    """训练循环"""
    env = gym.make(env_name)
    state_dim = env.observation_space.shape[0]
    n_actions = env.action_space.n
    
    agent = REINFORCE(state_dim, n_actions)
    rewards_per_episode = []
    
    print(f"🦐 开始训练 REINFORCE ({env_name})...")
    
    for episode in range(n_episodes):
        reward, loss = agent.train_episode(env)
        rewards_per_episode.append(reward)
        
        if episode % 50 == 0:
            last_50 = rewards_per_episode[-50:] if len(rewards_per_episode) >= 50 else rewards_per_episode
            avg = np.mean(last_50)
            print(f"Episode {episode}, Avg Reward (last 50): {avg:.2f}, Loss: {loss:.4f}")
        
        # 提前结束条件
        if len(rewards_per_episode) >= 100:
            last_100 = np.mean(rewards_per_episode[-100:])
            if last_100 >= 450:  # CartPole 满分 500
                print(f"✅ 训练完成！Episode {episode}, Avg Reward: {last_100:.2f}")
                break
    
    env.close()
    return agent, rewards_per_episode


if __name__ == "__main__":
    # 训练
    agent, rewards = train_reinforce('CartPole-v1', n_episodes=500)
    
    # 保存
    torch.save(agent.policy.state_dict(), 'reinforce_cartpole.pth')
    print("💾 模型已保存")
    
    # 测试
    print("\n🎮 测试训练好的模型...")
    env = gym.make('CartPole-v1')
    state = env.reset()
    total_reward = 0
    done = False
    
    while not done:
        action, _ = agent.select_action(state)
        env.render()
        state, reward, done, _ = env.step(action)
        total_reward += reward
    
    print(f"测试奖励：{total_reward}")
    env.close()
