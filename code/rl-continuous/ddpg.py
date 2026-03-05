"""
DDPG 实现 - Deep Deterministic Policy Gradient
连续控制的基础算法

小虾 🦐 | 2026-03-05 20:50
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from collections import deque
import random

# ==================== 网络架构 ====================

class Actor(nn.Module):
    """Actor - 输出确定性动作"""
    def __init__(self, state_dim, action_dim, max_action):
        super(Actor, self).__init__()
        self.fc1 = nn.Linear(state_dim, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, action_dim)
        self.max_action = max_action
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = torch.tanh(self.fc3(x)) * self.max_action
        return x


class Critic(nn.Module):
    """Critic - 输出 Q 值"""
    def __init__(self, state_dim, action_dim):
        super(Critic, self).__init__()
        self.fc1 = nn.Linear(state_dim + action_dim, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, 1)
    
    def forward(self, state, action):
        x = torch.cat([state, action], dim=1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


# ==================== 回放缓冲区 ====================

class ReplayBuffer:
    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.array(states),
            np.array(actions),
            np.array(rewards),
            np.array(next_states),
            np.array(dones)
        )
    
    def __len__(self):
        return len(self.buffer)


# ==================== DDPG Agent ====================

class DDPGAgent:
    """DDPG Agent"""
    def __init__(self, state_dim, action_dim, max_action=1.0,
                 lr_actor=1e-4, lr_critic=1e-3, gamma=0.99, tau=0.005,
                 buffer_capacity=100000, batch_size=256,
                 explore_noise=0.1, start_steps=10000):
        self.gamma = gamma
        self.tau = tau
        self.batch_size = batch_size
        self.explore_noise = explore_noise
        self.start_steps = start_steps
        self.total_steps = 0
        
        # Actor
        self.actor = Actor(state_dim, action_dim, max_action)
        self.actor_target = Actor(state_dim, action_dim, max_action)
        self.actor_target.load_state_dict(self.actor.state_dict())
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=lr_actor)
        
        # Critic
        self.critic = Critic(state_dim, action_dim)
        self.critic_target = Critic(state_dim, action_dim)
        self.critic_target.load_state_dict(self.critic.state_dict())
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=lr_critic)
        
        # 回放缓冲区
        self.memory = ReplayBuffer(capacity=buffer_capacity)
    
    def select_action(self, state, evaluate=False):
        """选择动作"""
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        
        with torch.no_grad():
            action = self.actor(state_tensor)
        
        if not evaluate:
            # 添加探索噪声
            action += torch.randn_like(action) * self.explore_noise
        
        return action.numpy()[0]
    
    def update(self):
        """更新 Actor 和 Critic"""
        if len(self.memory) < self.batch_size:
            return
        
        # 采样 batch
        batch = self.memory.sample(self.batch_size)
        states, actions, rewards, next_states, dones = batch
        
        # 转换为 tensor
        states = torch.FloatTensor(states)
        actions = torch.FloatTensor(actions)
        rewards = torch.FloatTensor(rewards).unsqueeze(1)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones).unsqueeze(1)
        
        # 计算 target Q 值
        with torch.no_grad():
            next_actions = self.actor_target(next_states)
            next_q = self.critic_target(next_states, next_actions)
            targets = rewards + self.gamma * next_q * (1 - dones)
        
        # Critic 更新
        current_q = self.critic(states, actions)
        critic_loss = F.mse_loss(current_q, targets)
        
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()
        
        # Actor 更新
        actor_actions = self.actor(states)
        actor_q = self.critic(states, actor_actions)
        actor_loss = -actor_q.mean()
        
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()
        
        # 软更新 target networks
        for target_param, param in zip(self.actor_target.parameters(), self.actor.parameters()):
            target_param.data.copy_(self.tau * param.data + (1 - self.tau) * target_param.data)
        
        for target_param, param in zip(self.critic_target.parameters(), self.critic.parameters()):
            target_param.data.copy_(self.tau * param.data + (1 - self.tau) * target_param.data)
        
        return actor_loss.item(), critic_loss.item()
    
    def store_transition(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)
        self.total_steps += 1


def train_ddpg(env, n_episodes=100):
    """训练循环"""
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]
    max_action = float(env.action_space.high[0])
    
    agent = DDPGAgent(state_dim, action_dim, max_action)
    rewards_per_episode = []
    
    for episode in range(n_episodes):
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = agent.select_action(state)
            next_state, reward, done, _ = env.step(action)
            agent.store_transition(state, action, reward, next_state, done)
            agent.update()
            total_reward += reward
            state = next_state
        
        rewards_per_episode.append(total_reward)
        
        if episode % 10 == 0:
            avg = np.mean(rewards_per_episode[-10:])
            print(f"Episode {episode}, Avg Reward: {avg:.2f}")
    
    return agent, rewards_per_episode


if __name__ == "__main__":
    import gym
    env = gym.make('Pendulum-v1')
    agent, rewards = train_ddpg(env, n_episodes=100)
    print("✅ DDPG 训练完成")
