"""
DQN 实现 - Deep Q-Network
环境：Atari Pong / CartPole
框架：PyTorch

小虾 🦐 | 2026-03-05 20:00
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

# ==================== 网络架构 ====================

class DQN(nn.Module):
    """DQN 网络 - CNN 架构 (Atari)"""
    def __init__(self, n_actions):
        super(DQN, self).__init__()
        self.conv1 = nn.Conv2d(4, 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
        
        # 计算 FC 输入维度
        self.fc_input_dim = self._get_conv_output_dim()
        
        self.fc1 = nn.Linear(self.fc_input_dim, 512)
        self.fc2 = nn.Linear(512, n_actions)
        
        self.relu = nn.ReLU()
    
    def _get_conv_output_dim(self):
        """计算卷积后维度"""
        with torch.no_grad():
            x = torch.zeros(1, 4, 84, 84)
            x = self.relu(self.conv1(x))
            x = self.relu(self.conv2(x))
            x = self.relu(self.conv3(x))
            return x.view(1, -1).size(1)
    
    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.relu(self.conv3(x))
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        return self.fc2(x)


class DQN_MLP(nn.Module):
    """DQN 网络 - MLP 架构 (CartPole 等)"""
    def __init__(self, state_dim, n_actions):
        super(DQN_MLP, self).__init__()
        self.fc1 = nn.Linear(state_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, n_actions)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc3(x)


# ==================== 经验回放缓冲区 ====================

class ReplayBuffer:
    """经验回放缓冲区"""
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        """存储转移"""
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        """随机采样 batch"""
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


# ==================== DQN Agent ====================

class DQNAgent:
    """DQN Agent"""
    def __init__(self, state_dim, n_actions, lr=1e-3, gamma=0.99, 
                 epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995,
                 buffer_capacity=10000, batch_size=64,
                 target_update_freq=100):
        self.state_dim = state_dim
        self.n_actions = n_actions
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.target_update_freq = target_update_freq
        
        # 网络
        self.q_net = DQN_MLP(state_dim, n_actions)
        self.target_net = DQN_MLP(state_dim, n_actions)
        self.target_net.load_state_dict(self.q_net.state_dict())
        
        # 优化器
        self.optimizer = optim.Adam(self.q_net.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        
        # 回放缓冲区
        self.memory = ReplayBuffer(capacity=buffer_capacity)
        
        self.steps = 0
    
    def get_action(self, state):
        """ε-greedy 策略"""
        if random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        else:
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state).unsqueeze(0)
                q_values = self.q_net(state_tensor)
                return q_values.argmax().item()
    
    def compute_target(self, reward, next_state, done):
        """计算 target Q 值 (DQN)"""
        if done:
            return reward
        with torch.no_grad():
            next_q = self.target_net(torch.FloatTensor(next_state)).max().item()
            return reward + self.gamma * next_q
    
    def update(self, state, action, reward, next_state, done):
        """单步更新"""
        # 存储转移
        self.memory.push(state, action, reward, next_state, done)
        
        # 采样 batch
        if len(self.memory) < self.batch_size:
            return
        
        batch = self.memory.sample(self.batch_size)
        states, actions, rewards, next_states, dones = batch
        
        # 转换为 tensor
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)
        
        # 计算当前 Q 值
        current_q = self.q_net(states).gather(1, actions).squeeze()
        
        # 计算 target Q 值
        with torch.no_grad():
            next_q = self.target_net(next_states).max(dim=1)[0]
            targets = rewards + self.gamma * next_q * (1 - dones)
        
        # 计算损失
        loss = self.criterion(current_q, targets)
        
        # 反向传播
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # 更新 target network
        self.steps += 1
        if self.steps % self.target_update_freq == 0:
            self.target_net.load_state_dict(self.q_net.state_dict())
        
        # ε 衰减
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        return loss.item()
    
    def save(self, path):
        """保存模型"""
        torch.save({
            'q_net': self.q_net.state_dict(),
            'target_net': self.target_net.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'steps': self.steps
        }, path)
    
    def load(self, path):
        """加载模型"""
        checkpoint = torch.load(path)
        self.q_net.load_state_dict(checkpoint['q_net'])
        self.target_net.load_state_dict(checkpoint['target_net'])
        self.optimizer.load_state_dict(checkpoint['optimizer'])
        self.epsilon = checkpoint['epsilon']
        self.steps = checkpoint['steps']


# ==================== 训练循环 ====================

def train_dqn(env, n_episodes=500):
    """训练 DQN"""
    agent = DQNAgent(
        state_dim=4,  # CartPole
        n_actions=2,
        lr=1e-3,
        gamma=0.99,
        epsilon=1.0,
        epsilon_min=0.01,
        epsilon_decay=0.995,
        buffer_capacity=10000,
        batch_size=64,
        target_update_freq=100
    )
    
    rewards_per_episode = []
    
    for episode in range(n_episodes):
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = agent.get_action(state)
            next_state, reward, done, _ = env.step(action)
            loss = agent.update(state, action, reward, next_state, done)
            total_reward += reward
            state = next_state
        
        rewards_per_episode.append(total_reward)
        
        # 打印进度
        if episode % 50 == 0:
            avg_reward = np.mean(rewards_per_episode[-50:])
            print(f"Episode {episode}, Avg Reward: {avg_reward:.2f}, Epsilon: {agent.epsilon:.3f}")
    
    return agent, rewards_per_episode


if __name__ == "__main__":
    import gym
    
    # 创建环境
    env = gym.make('CartPole-v1')
    
    # 训练
    print("🦐 开始训练 DQN...")
    agent, rewards = train_dqn(env, n_episodes=500)
    
    # 保存
    agent.save('dqn_cartpole.pth')
    print("✅ 训练完成，模型已保存")
    
    # 绘图
    import matplotlib.pyplot as plt
    plt.plot(rewards)
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.title('DQN Training - CartPole')
    plt.savefig('dqn_training_curve.png')
    print("📊 训练曲线已保存")
