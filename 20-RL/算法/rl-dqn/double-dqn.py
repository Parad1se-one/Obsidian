"""
Double DQN 实现
关键改进：解耦动作选择和价值评估

小虾 🦐 | 2026-03-05 20:10
"""

import torch
import torch.nn as nn
import numpy as np
from dqn import DQN_MLP, ReplayBuffer, DQNAgent


class DoubleDQNAgent(DQNAgent):
    """Double DQN Agent"""
    
    def __init__(self, state_dim, n_actions, **kwargs):
        super().__init__(state_dim, n_actions, **kwargs)
    
    def compute_target(self, reward, next_state, done):
        """Double DQN target - 解耦动作选择和评估"""
        if done:
            return reward
        
        # Online net 选择动作
        with torch.no_grad():
            next_state_tensor = torch.FloatTensor(next_state)
            next_action = self.q_net(next_state_tensor).argmax().item()
            
            # Target net 评估价值
            next_q = self.target_net(next_state_tensor)[next_action].item()
            
            return reward + self.gamma * next_q
    
    def update_batch(self, batch):
        """Batch 更新 (Double DQN)"""
        states, actions, rewards, next_states, dones = batch
        
        # 转换为 tensor
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)
        
        # 计算当前 Q 值
        current_q = self.q_net(states).gather(1, actions).squeeze()
        
        # Double DQN target
        with torch.no_grad():
            # Online net 选择动作
            next_actions = self.q_net(next_states).argmax(dim=1, keepdim=True)
            # Target net 评估价值
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


def compare_dqn_vs_double_dqn(env, n_episodes=300):
    """对比 DQN 和 Double DQN"""
    from dqn import DQNAgent
    import gym
    
    # DQN
    print("🔵 训练 DQN...")
    dqn_agent, dqn_rewards = DQNAgent(
        state_dim=4, n_actions=2,
        lr=1e-3, gamma=0.99,
        epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995
    ), []
    
    for episode in range(n_episodes):
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = dqn_agent.get_action(state)
            next_state, reward, done, _ = env.step(action)
            dqn_agent.update(state, action, reward, next_state, done)
            total_reward += reward
            state = next_state
        
        dqn_rewards.append(total_reward)
        
        if episode % 50 == 0:
            avg = np.mean(dqn_rewards[-50:])
            print(f"DQN Episode {episode}, Avg: {avg:.2f}")
    
    # Double DQN
    print("🟢 训练 Double DQN...")
    env.reset()
    ddqn_agent = DoubleDQNAgent(
        state_dim=4, n_actions=2,
        lr=1e-3, gamma=0.99,
        epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995
    )
    ddqn_rewards = []
    
    for episode in range(n_episodes):
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = ddqn_agent.get_action(state)
            next_state, reward, done, _ = env.step(action)
            ddqn_agent.update(state, action, reward, next_state, done)
            total_reward += reward
            state = next_state
        
        ddqn_rewards.append(total_reward)
        
        if episode % 50 == 0:
            avg = np.mean(ddqn_rewards[-50:])
            print(f"Double DQN Episode {episode}, Avg: {avg:.2f}")
    
    return dqn_rewards, ddqn_rewards


if __name__ == "__main__":
    import gym
    import matplotlib.pyplot as plt
    
    env = gym.make('CartPole-v1')
    
    print("🦐 开始对比 DQN vs Double DQN...")
    dqn_rewards, ddqn_rewards = compare_dqn_vs_double_dqn(env)
    
    # 绘图对比
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(dqn_rewards, label='DQN', alpha=0.7)
    plt.plot(ddqn_rewards, label='Double DQN', alpha=0.7)
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.title('Training Curve Comparison')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    window = 50
    dqn_avg = np.convolve(dqn_rewards, np.ones(window)/window, mode='valid')
    ddqn_avg = np.convolve(ddqn_rewards, np.ones(window)/window, mode='valid')
    plt.plot(dqn_avg, label='DQN (avg)')
    plt.plot(ddqn_avg, label='Double DQN (avg)')
    plt.xlabel('Episode')
    plt.ylabel('Average Reward')
    plt.title(f'Moving Average (window={window})')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('dqn_vs_double_dqn.png')
    print("📊 对比图已保存")
    
    # 统计
    print(f"\n📈 最终性能 (最后 50 集平均):")
    print(f"DQN: {np.mean(dqn_rewards[-50:]):.2f}")
    print(f"Double DQN: {np.mean(ddqn_rewards[-50:]):.2f}")
