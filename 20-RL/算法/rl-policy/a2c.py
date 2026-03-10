"""
A2C 实现 - Advantage Actor-Critic
结合策略梯度和值函数基线

小虾 🦐 | 2026-03-05 20:14
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import gym

# ==================== Actor-Critic 网络 ====================

class ActorCritic(nn.Module):
    """Actor-Critic 网络 - 共享特征"""
    def __init__(self, state_dim, n_actions, hidden_dim=128):
        super(ActorCritic, self).__init__()
        
        # 共享特征层
        self.shared = nn.Linear(state_dim, hidden_dim)
        
        # Actor - 输出动作概率
        self.actor = nn.Linear(hidden_dim, n_actions)
        
        # Critic - 输出状态值
        self.critic = nn.Linear(hidden_dim, 1)
        
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.shared(x))
        
        # 策略
        policy = F.softmax(self.actor(x), dim=-1)
        
        # 值函数
        value = self.critic(x)
        
        return policy, value
    
    def get_action(self, state):
        """采样动作"""
        state_tensor = torch.FloatTensor(state)
        policy, value = self.forward(state_tensor)
        
        dist = torch.distributions.Categorical(policy)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        
        return action.item(), log_prob, value


# ==================== A2C Agent ====================

class A2CAgent:
    """A2C Agent"""
    def __init__(self, state_dim, n_actions, lr=1e-3, gamma=0.99, 
                 value_coef=0.5, entropy_coef=0.01):
        self.gamma = gamma
        self.value_coef = value_coef  # Critic 损失权重
        self.entropy_coef = entropy_coef  # 熵正则化
        
        self.model = ActorCritic(state_dim, n_actions)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
    
    def select_action(self, state):
        action, log_prob, value = self.model.get_action(state)
        return action, log_prob, value
    
    def compute_advantage(self, rewards, values, dones):
        """计算优势函数 (TD 误差)"""
        advantages = []
        deltas = []
        
        # 计算 TD 误差
        for t in range(len(rewards)):
            if t == len(rewards) - 1:
                next_value = 0
            else:
                next_value = values[t + 1]
            
            delta = rewards[t] + self.gamma * next_value * (1 - dones[t]) - values[t]
            deltas.append(delta)
        
        # 计算优势 (累积 TD 误差)
        advantage = 0
        for delta in reversed(deltas):
            advantage = delta + self.gamma * advantage
            advantages.insert(0, advantage)
        
        advantages = torch.FloatTensor(advantages)
        
        # 标准化
        if len(advantages) > 1:
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        return advantages
    
    def update(self, states, actions, log_probs, rewards, values, dones):
        """更新 Actor 和 Critic"""
        # 转换为 tensor
        states = torch.FloatTensor(np.array(states))
        actions = torch.LongTensor(actions)
        log_probs = torch.stack(log_probs)
        rewards = torch.FloatTensor(rewards)
        values = torch.stack(values).squeeze()
        dones = torch.FloatTensor(dones)
        
        # 计算优势
        advantages = self.compute_advantage(rewards, values, dones)
        
        # 计算目标值 (用于 Critic)
        targets = advantages + values
        
        # 重新获取策略 (用于计算新 log_prob)
        new_policies, new_values = self.model(states)
        new_dist = torch.distributions.Categorical(new_policies)
        new_log_probs = new_dist.log_prob(actions)
        
        # Actor 损失 - 策略梯度
        actor_loss = -(new_log_probs * advantages.detach()).mean()
        
        # Critic 损失 - 值函数 MSE
        critic_loss = F.mse_loss(new_values.squeeze(), targets.detach())
        
        # 熵正则化 - 鼓励探索
        entropy = new_dist.entropy().mean()
        
        # 总损失
        loss = actor_loss + self.value_coef * critic_loss - self.entropy_coef * entropy
        
        # 反向传播
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item(), actor_loss.item(), critic_loss.item()
    
    def train_n_steps(self, env, n_steps=5):
        """训练 n 步"""
        states, actions, log_probs, rewards, values, dones = [], [], [], [], [], []
        
        state = env.reset()
        done = False
        total_reward = 0
        
        for _ in range(n_steps):
            action, log_prob, value = self.select_action(state)
            next_state, reward, done, _ = env.step(action)
            
            states.append(state)
            actions.append(action)
            log_probs.append(log_prob)
            rewards.append(reward)
            values.append(value)
            dones.append(done)
            
            total_reward += reward
            state = next_state
            
            if done:
                break
        
        if len(states) > 0:
            loss, actor_loss, critic_loss = self.update(
                states, actions, log_probs, rewards, values, dones
            )
            return total_reward, loss, actor_loss, critic_loss
        
        return total_reward, 0, 0, 0


def train_a2c(env_name='CartPole-v1', n_episodes=1000, n_steps=5):
    """训练循环"""
    env = gym.make(env_name)
    state_dim = env.observation_space.shape[0]
    n_actions = env.action_space.n
    
    agent = A2CAgent(state_dim, n_actions)
    rewards_per_episode = []
    
    print(f"🦐 开始训练 A2C ({env_name})...")
    
    for episode in range(n_episodes):
        reward, loss, actor_loss, critic_loss = agent.train_n_steps(env, n_steps)
        rewards_per_episode.append(reward)
        
        if episode % 50 == 0:
            last_50 = rewards_per_episode[-50:] if len(rewards_per_episode) >= 50 else rewards_per_episode
            avg = np.mean(last_50)
            print(f"Episode {episode}, Avg Reward: {avg:.2f}, "
                  f"Loss: {loss:.4f}, Actor: {actor_loss:.4f}, Critic: {critic_loss:.4f}")
        
        # 提前结束
        if len(rewards_per_episode) >= 100:
            last_100 = np.mean(rewards_per_episode[-100:])
            if last_100 >= 450:
                print(f"✅ 训练完成！Episode {episode}, Avg Reward: {last_100:.2f}")
                break
    
    env.close()
    return agent, rewards_per_episode


if __name__ == "__main__":
    # 训练
    agent, rewards = train_a2c('CartPole-v1', n_episodes=500)
    
    # 保存
    torch.save(agent.model.state_dict(), 'a2c_cartpole.pth')
    print("💾 模型已保存")
    
    # 测试
    print("\n🎮 测试训练好的模型...")
    env = gym.make('CartPole-v1')
    state = env.reset()
    total_reward = 0
    done = False
    
    while not done:
        action, _, _ = agent.select_action(state)
        env.render()
        state, reward, done, _ = env.step(action)
        total_reward += reward
    
    print(f"测试奖励：{total_reward}")
    env.close()
