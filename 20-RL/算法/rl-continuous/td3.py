"""
TD3 实现 - Twin Delayed DDPG
改进 DDPG 的三个关键技术

小虾 🦐 | 2026-03-05 20:54
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from ddpg import Actor, ReplayBuffer

# ==================== Twin Critic ====================

class TwinCritic(nn.Module):
    """双 Critic 网络 - 解决过估计"""
    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super(TwinCritic, self).__init__()
        
        # Critic 1
        self.q1_fc1 = nn.Linear(state_dim + action_dim, hidden_dim)
        self.q1_fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.q1_fc3 = nn.Linear(hidden_dim, 1)
        
        # Critic 2
        self.q2_fc1 = nn.Linear(state_dim + action_dim, hidden_dim)
        self.q2_fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.q2_fc3 = nn.Linear(hidden_dim, 1)
    
    def forward(self, state, action):
        x = torch.cat([state, action], dim=1)
        
        q1 = F.relu(self.q1_fc1(x))
        q1 = F.relu(self.q1_fc2(q1))
        q1 = self.q1_fc3(q1)
        
        q2 = F.relu(self.q2_fc1(x))
        q2 = F.relu(self.q2_fc2(q2))
        q2 = self.q2_fc3(q2)
        
        return q1, q2
    
    def q1(self, state, action):
        x = torch.cat([state, action], dim=1)
        x = F.relu(self.q1_fc1(x))
        x = F.relu(self.q1_fc2(x))
        return self.q1_fc3(x)


# ==================== TD3 Agent ====================

class TD3Agent:
    """TD3 Agent - Twin Delayed DDPG"""
    def __init__(self, state_dim, action_dim, max_action=1.0,
                 lr_actor=1e-4, lr_critic=1e-3, gamma=0.99, tau=0.005,
                 buffer_capacity=100000, batch_size=256,
                 explore_noise=0.1, target_noise=0.2, noise_clip=0.5,
                 policy_delay=2):
        self.gamma = gamma
        self.tau = tau
        self.batch_size = batch_size
        self.explore_noise = explore_noise
        self.target_noise = target_noise
        self.noise_clip = noise_clip
        self.policy_delay = policy_delay
        self.total_steps = 0
        
        # Actor
        self.actor = Actor(state_dim, action_dim, max_action)
        self.actor_target = Actor(state_dim, action_dim, max_action)
        self.actor_target.load_state_dict(self.actor.state_dict())
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=lr_actor)
        
        # Twin Critic
        self.critic = TwinCritic(state_dim, action_dim)
        self.critic_target = TwinCritic(state_dim, action_dim)
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
            action += torch.randn_like(action) * self.explore_noise
        
        return action.numpy()[0]
    
    def update(self):
        """TD3 更新 - 三个关键技术"""
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
        
        # ==================== Critic 更新 ====================
        with torch.no_grad():
            # 目标动作 + 噪声平滑 (Target Smoothing)
            next_actions = self.actor_target(next_states)
            noise = torch.randn_like(next_actions) * self.target_noise
            noise = noise.clamp(-self.noise_clip, self.noise_clip)
            next_actions = (next_actions + noise).clamp(-1, 1)
            
            # 双 Critic 取最小值 (Twin Critic)
            q1_next, q2_next = self.critic_target(next_states, next_actions)
            next_q = torch.min(q1_next, q2_next)
            
            targets = rewards + self.gamma * next_q * (1 - dones)
        
        # 更新 Critic
        q1, q2 = self.critic(states, actions)
        critic_loss = F.mse_loss(q1, targets) + F.mse_loss(q2, targets)
        
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()
        
        # ==================== Actor 更新 (Delayed) ====================
        if self.total_steps % self.policy_delay == 0:
            actor_actions = self.actor(states)
            actor_q = self.critic.q1(states, actor_actions)
            actor_loss = -actor_q.mean()
            
            self.actor_optimizer.zero_grad()
            actor_loss.backward()
            self.actor_optimizer.step()
            
            # 软更新 target networks
            for target_param, param in zip(self.actor_target.parameters(), self.actor.parameters()):
                target_param.data.copy_(self.tau * param.data + (1 - self.tau) * target_param.data)
            
            for target_param, param in zip(self.critic_target.parameters(), self.critic.parameters()):
                target_param.data.copy_(self.tau * param.data + (1 - self.tau) * target_param.data)
        
        self.total_steps += 1
    
    def store_transition(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)


def train_td3(env_name='Pendulum-v1', n_episodes=100):
    """训练循环"""
    env = gym.make(env_name)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]
    max_action = float(env.action_space.high[0])
    
    agent = TD3Agent(state_dim, action_dim, max_action)
    rewards_per_episode = []
    
    print(f"🦐 开始训练 TD3 ({env_name})...")
    
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
            last_10 = rewards_per_episode[-10:] if len(rewards_per_episode) >= 10 else rewards_per_episode
            avg = np.mean(last_10)
            print(f"Episode {episode}, Avg Reward: {avg:.2f}")
    
    env.close()
    return agent, rewards_per_episode


if __name__ == "__main__":
    import gym
    # 训练
    agent, rewards = train_td3('Pendulum-v1', n_episodes=100)
    
    # 保存
    torch.save(agent.actor.state_dict(), 'td3_pendulum.pth')
    print("💾 模型已保存")
