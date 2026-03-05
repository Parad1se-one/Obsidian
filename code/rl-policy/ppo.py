"""
PPO 实现 - Proximal Policy Optimization
当前主流的策略梯度算法

小虾 🦐 | 2026-03-05 20:24
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import gym

# ==================== Actor-Critic 网络 ====================

class ActorCritic(nn.Module):
    """Actor-Critic 网络 (PPO)"""
    def __init__(self, state_dim, n_actions, hidden_dim=128):
        super(ActorCritic, self).__init__()
        
        self.shared = nn.Linear(state_dim, hidden_dim)
        self.actor = nn.Linear(hidden_dim, n_actions)
        self.critic = nn.Linear(hidden_dim, 1)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.shared(x))
        policy = F.softmax(self.actor(x), dim=-1)
        value = self.critic(x)
        return policy, value
    
    def get_action(self, state):
        state_tensor = torch.FloatTensor(state)
        policy, value = self.forward(state_tensor)
        
        dist = torch.distributions.Categorical(policy)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        
        return action.item(), log_prob, value
    
    def evaluate(self, states, actions):
        """评估动作 (用于 PPO 更新)"""
        states_tensor = torch.FloatTensor(states)
        actions_tensor = torch.LongTensor(actions)
        
        policy, value = self.forward(states_tensor)
        dist = torch.distributions.Categorical(policy)
        
        log_probs = dist.log_prob(actions_tensor)
        entropy = dist.entropy().mean()
        
        return log_probs, value, entropy


# ==================== PPO Agent ====================

class PPOAgent:
    """PPO Agent"""
    def __init__(self, state_dim, n_actions, lr=3e-4, gamma=0.99, 
                 epsilon=0.2, k_epochs=4, value_coef=0.5, entropy_coef=0.01):
        self.gamma = gamma
        self.epsilon = epsilon  # clip 范围
        self.k_epochs = k_epochs  # 每次更新次数
        self.value_coef = value_coef
        self.entropy_coef = entropy_coef
        
        self.model = ActorCritic(state_dim, n_actions)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
    
    def select_action(self, state):
        return self.model.get_action(state)
    
    def compute_advantage(self, rewards, values, dones):
        """GAE 优势估计"""
        advantages = []
        deltas = []
        
        for t in range(len(rewards)):
            if t == len(rewards) - 1:
                next_value = 0
            else:
                next_value = values[t + 1]
            
            delta = rewards[t] + self.gamma * next_value * (1 - dones[t]) - values[t]
            deltas.append(delta)
        
        advantage = 0
        for delta in reversed(deltas):
            advantage = delta + self.gamma * advantage
            advantages.insert(0, advantage)
        
        advantages = torch.FloatTensor(advantages)
        if len(advantages) > 1:
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        return advantages
    
    def update(self, states, actions, old_log_probs, rewards, values, dones):
        """PPO 更新 - 多次 epoch"""
        # 转换为 tensor
        states = torch.FloatTensor(np.array(states))
        actions = torch.LongTensor(actions)
        old_log_probs = torch.stack(old_log_probs)
        rewards = torch.FloatTensor(rewards)
        values = torch.stack(values).squeeze()
        dones = torch.FloatTensor(dones)
        
        # 计算优势
        advantages = self.compute_advantage(rewards, values, dones)
        targets = advantages + values
        
        # 多次更新
        for _ in range(self.k_epochs):
            # 评估当前策略
            log_probs, cur_values, entropy = self.model.evaluate(states, actions)
            
            # 计算比率
            ratio = torch.exp(log_probs - old_log_probs.detach())
            
            # Clipped surrogate objective
            surr1 = ratio * advantages.detach()
            surr2 = torch.clamp(ratio, 1 - self.epsilon, 1 + self.epsilon) * advantages.detach()
            actor_loss = -torch.min(surr1, surr2).mean()
            
            # Critic 损失
            critic_loss = F.mse_loss(cur_values.squeeze(), targets.detach())
            
            # 总损失
            loss = actor_loss + self.value_coef * critic_loss - self.entropy_coef * entropy
            
            # 反向传播
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        
        return loss.item(), actor_loss.item(), critic_loss.item()
    
    def train_batch(self, env, batch_size=2048):
        """训练一个 batch"""
        states, actions, log_probs, rewards, values, dones = [], [], [], [], [], []
        
        state = env.reset()
        done = False
        total_reward = 0
        
        while len(states) < batch_size:
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
                state = env.reset()
        
        loss, actor_loss, critic_loss = self.update(
            states, actions, log_probs, rewards, values, dones
        )
        
        return total_reward, loss, actor_loss, critic_loss


def train_ppo(env_name='CartPole-v1', n_iterations=500, batch_size=2048):
    """训练循环"""
    env = gym.make(env_name)
    state_dim = env.observation_space.shape[0]
    n_actions = env.action_space.n
    
    agent = PPOAgent(state_dim, n_actions)
    rewards_per_iteration = []
    
    print(f"🦐 开始训练 PPO ({env_name})...")
    
    for iteration in range(n_iterations):
        reward, loss, actor_loss, critic_loss = agent.train_batch(env, batch_size)
        rewards_per_iteration.append(reward)
        
        if iteration % 10 == 0:
            last_10 = rewards_per_iteration[-10:] if len(rewards_per_iteration) >= 10 else rewards_per_iteration
            avg = np.mean(last_10)
            print(f"Iteration {iteration}, Avg Reward: {avg:.2f}, "
                  f"Loss: {loss:.4f}, Actor: {actor_loss:.4f}, Critic: {critic_loss:.4f}")
        
        # 提前结束
        if len(rewards_per_iteration) >= 50:
            last_50 = np.mean(rewards_per_iteration[-50:])
            if last_50 >= 450:
                print(f"✅ 训练完成！Iteration {iteration}, Avg Reward: {last_50:.2f}")
                break
    
    env.close()
    return agent, rewards_per_iteration


if __name__ == "__main__":
    # 训练
    agent, rewards = train_ppo('CartPole-v1', n_iterations=100)
    
    # 保存
    torch.save(agent.model.state_dict(), 'ppo_cartpole.pth')
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
