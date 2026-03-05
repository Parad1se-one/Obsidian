"""
SAC 实现 - Soft Actor-Critic
最大熵强化学习

小虾 🦐 | 2026-03-05 21:10
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from ddpg import ReplayBuffer
from math import log, pi

# ==================== 网络架构 ====================

class GaussianPolicy(nn.Module):
    """随机策略 - 输出高斯分布"""
    def __init__(self, state_dim, action_dim, max_action, hidden_dim=256):
        super(GaussianPolicy, self).__init__()
        
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        
        self.mu_head = nn.Linear(hidden_dim, action_dim)
        self.log_sigma_head = nn.Linear(hidden_dim, action_dim)
        
        self.max_action = max_action
    
    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        
        mu = self.mu_head(x)
        log_sigma = self.log_sigma_head(x)
        log_sigma = torch.clamp(log_sigma, -20, 2)
        
        return mu, log_sigma
    
    def sample(self, state, deterministic=False):
        """采样动作"""
        mu, log_sigma = self.forward(state)
        
        if deterministic:
            return mu.tanh()
        
        sigma = torch.exp(log_sigma)
        dist = torch.distributions.Normal(mu, sigma)
        
        # Reparameterization trick
        x_t = dist.rsample()
        action = torch.tanh(x_t)
        
        # 计算 log 概率 (包含 tanh 变换)
        log_prob = dist.log_prob(x_t)
        log_prob -= torch.log(1 - action.pow(2) + 1e-6)
        log_prob = log_prob.sum(dim=1, keepdim=True)
        
        return action * self.max_action, log_prob


class SoftQNetwork(nn.Module):
    """Soft Q Network"""
    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super(SoftQNetwork, self).__init__()
        
        self.fc1 = nn.Linear(state_dim + action_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, 1)
    
    def forward(self, state, action):
        x = torch.cat([state, action], dim=1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


# ==================== SAC Agent ====================

class SACAgent:
    """SAC Agent"""
    def __init__(self, state_dim, action_dim, max_action=1.0,
                 lr_actor=3e-4, lr_critic=3e-4, lr_alpha=3e-4,
                 gamma=0.99, tau=0.005, target_entropy=None,
                 buffer_capacity=100000, batch_size=256):
        self.gamma = gamma
        self.tau = tau
        self.batch_size = batch_size
        
        # 自动熵温度系数
        if target_entropy is None:
            self.target_entropy = -action_dim
        else:
            self.target_entropy = target_entropy
        
        self.log_alpha = torch.tensor(np.log(0.2), requires_grad=True)
        self.alpha_optimizer = optim.Adam([self.log_alpha], lr=lr_alpha)
        
        # Actor
        self.actor = GaussianPolicy(state_dim, action_dim, max_action)
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=lr_actor)
        
        # Twin Critic
        self.critic1 = SoftQNetwork(state_dim, action_dim)
        self.critic2 = SoftQNetwork(state_dim, action_dim)
        self.critic1_target = SoftQNetwork(state_dim, action_dim)
        self.critic2_target = SoftQNetwork(state_dim, action_dim)
        
        self.critic1_target.load_state_dict(self.critic1.state_dict())
        self.critic2_target.load_state_dict(self.critic2.state_dict())
        
        self.critic1_optimizer = optim.Adam(self.critic1.parameters(), lr=lr_critic)
        self.critic2_optimizer = optim.Adam(self.critic2.parameters(), lr=lr_critic)
        
        # 回放缓冲区
        self.memory = ReplayBuffer(capacity=buffer_capacity)
    
    def select_action(self, state, evaluate=False):
        """选择动作"""
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        
        with torch.no_grad():
            action, _ = self.actor.sample(state_tensor, deterministic=evaluate)
        
        return action.numpy()[0]
    
    def update(self):
        """SAC 更新"""
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
        
        alpha = self.log_alpha.exp()
        
        # ==================== Critic 更新 ====================
        with torch.no_grad():
            next_actions, next_log_probs = self.actor.sample(next_states)
            q1_next, q2_next = self.critic1_target(next_states, next_actions), \
                               self.critic2_target(next_states, next_actions)
            next_q = torch.min(q1_next, q2_next) - alpha * next_log_probs
            targets = rewards + self.gamma * next_q * (1 - dones)
        
        q1, q2 = self.critic1(states, actions), self.critic2(states, actions)
        critic1_loss = F.mse_loss(q1, targets)
        critic2_loss = F.mse_loss(q2, targets)
        
        self.critic1_optimizer.zero_grad()
        critic1_loss.backward()
        self.critic1_optimizer.step()
        
        self.critic2_optimizer.zero_grad()
        critic2_loss.backward()
        self.critic2_optimizer.step()
        
        # ==================== Actor 更新 ====================
        actor_actions, actor_log_probs = self.actor.sample(states)
        q1_actor, q2_actor = self.critic1(states, actor_actions), \
                             self.critic2(states, actor_actions)
        q_actor = torch.min(q1_actor, q2_actor)
        
        actor_loss = (alpha * actor_log_probs - q_actor).mean()
        
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()
        
        # ==================== Alpha 更新 ====================
        with torch.no_grad():
            _, log_probs = self.actor.sample(states)
        
        alpha_loss = -(self.log_alpha * (log_probs + self.target_entropy).detach()).mean()
        
        self.alpha_optimizer.zero_grad()
        alpha_loss.backward()
        self.alpha_optimizer.step()
        
        # ==================== Target 网络软更新 ====================
        for target_param, param in zip(self.critic1_target.parameters(), self.critic1.parameters()):
            target_param.data.copy_(self.tau * param.data + (1 - self.tau) * target_param.data)
        
        for target_param, param in zip(self.critic2_target.parameters(), self.critic2.parameters()):
            target_param.data.copy_(self.tau * param.data + (1 - self.tau) * target_param.data)
    
    def store_transition(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)


def train_sac(env, n_episodes=100):
    """训练循环"""
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]
    max_action = float(env.action_space.high[0])
    
    agent = SACAgent(state_dim, action_dim, max_action)
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
    agent, rewards = train_sac(env, n_episodes=100)
    print("✅ SAC 训练完成")
