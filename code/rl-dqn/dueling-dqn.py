"""
Dueling DQN 实现
核心思想：分离状态值函数 V(s) 和优势函数 A(s,a)

小虾 🦐 | 2026-03-05 20:20
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from dqn import ReplayBuffer, DQNAgent


class DuelingDQN(nn.Module):
    """Dueling DQN 网络"""
    def __init__(self, state_dim, n_actions):
        super(DuelingDQN, self).__init__()
        
        # 共享特征提取层
        self.fc1 = nn.Linear(state_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        
        # 值函数流 V(s)
        self.value_fc = nn.Linear(128, 64)
        self.value = nn.Linear(64, 1)
        
        # 优势函数流 A(s,a)
        self.advantage_fc = nn.Linear(128, 64)
        self.advantage = nn.Linear(64, n_actions)
        
        self.relu = nn.ReLU()
    
    def forward(self, x):
        # 共享特征
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        
        # 值函数
        v = self.relu(self.value_fc(x))
        v = self.value(v)  # [batch, 1]
        
        # 优势函数
        a = self.relu(self.advantage_fc(x))
        a = self.advantage(a)  # [batch, n_actions]
        
        # 聚合：Q(s,a) = V(s) + (A(s,a) - mean(A(s,:)))
        # 减去均值确保可识别性
        q = v + (a - a.mean(dim=1, keepdim=True))
        
        return q


class DuelingDQNAgent(DQNAgent):
    """Dueling DQN Agent"""
    
    def __init__(self, state_dim, n_actions, **kwargs):
        # 跳过父类初始化，自己创建网络
        self.state_dim = state_dim
        self.n_actions = n_actions
        self.gamma = kwargs.get('gamma', 0.99)
        self.epsilon = kwargs.get('epsilon', 1.0)
        self.epsilon_min = kwargs.get('epsilon_min', 0.01)
        self.epsilon_decay = kwargs.get('epsilon_decay', 0.995)
        self.batch_size = kwargs.get('batch_size', 64)
        self.target_update_freq = kwargs.get('target_update_freq', 100)
        
        # Dueling 网络
        self.q_net = DuelingDQN(state_dim, n_actions)
        self.target_net = DuelingDQN(state_dim, n_actions)
        self.target_net.load_state_dict(self.q_net.state_dict())
        
        # 优化器
        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=kwargs.get('lr', 1e-3))
        self.criterion = nn.MSELoss()
        
        # 回放缓冲区
        self.memory = ReplayBuffer(capacity=kwargs.get('buffer_capacity', 10000))
        
        self.steps = 0
    
    def get_action(self, state):
        """ε-greedy 策略"""
        import random
        if random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        else:
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state).unsqueeze(0)
                q_values = self.q_net(state_tensor)
                return q_values.argmax().item()
    
    def update(self, state, action, reward, next_state, done):
        """单步更新"""
        import random
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
        
        # Double DQN target (结合 Dueling)
        with torch.no_grad():
            next_actions = self.q_net(next_states).argmax(dim=1, keepdim=True)
            next_q_values = self.target_net(next_states).gather(1, next_actions).squeeze()
            targets = rewards + self.gamma * next_q_values * (1 - dones)
        
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


def analyze_dueling_architecture():
    """分析 Dueling 架构的值和优势"""
    import gym
    
    env = gym.make('CartPole-v1')
    agent = DuelingDQNAgent(state_dim=4, n_actions=2)
    
    # 随机状态
    state = env.reset()
    state_tensor = torch.FloatTensor(state).unsqueeze(0)
    
    with torch.no_grad():
        q_values = agent.q_net(state_tensor)
        print(f"Q 值：{q_values}")
        print(f"最优动作：{q_values.argmax().item()}")


if __name__ == "__main__":
    import gym
    import matplotlib.pyplot as plt
    
    print("🦐 训练 Dueling DQN...")
    
    env = gym.make('CartPole-v1')
    agent = DuelingDQNAgent(
        state_dim=4, n_actions=2,
        lr=1e-3, gamma=0.99,
        epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995,
        batch_size=64, target_update_freq=100,
        buffer_capacity=10000
    )
    
    rewards_per_episode = []
    
    for episode in range(500):
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
        
        if episode % 50 == 0:
            avg_reward = np.mean(rewards_per_episode[-50:])
            print(f"Episode {episode}, Avg Reward: {avg_reward:.2f}, Epsilon: {agent.epsilon:.3f}")
    
    # 保存
    agent.save('dueling_dqn_cartpole.pth')
    print("✅ 训练完成，模型已保存")
    
    # 绘图
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(rewards_per_episode)
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.title('Dueling DQN Training Curve')
    
    plt.subplot(1, 2, 2)
    window = 50
    avg = np.convolve(rewards_per_episode, np.ones(window)/window, mode='valid')
    plt.plot(avg)
    plt.xlabel('Episode')
    plt.ylabel('Average Reward')
    plt.title(f'Moving Average (window={window})')
    
    plt.tight_layout()
    plt.savefig('dueling_dqn_training.png')
    print("📊 训练曲线已保存")
