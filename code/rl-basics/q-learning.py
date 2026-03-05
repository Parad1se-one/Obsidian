"""
Q-Learning 算法实现
环境：GridWorld
"""

import numpy as np
import random

class QLearning:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = alpha  # 学习率
        self.gamma = gamma  # 折扣因子
        self.epsilon = epsilon  # 探索率
        self.q_table = np.zeros((n_states, n_actions))
    
    def get_action(self, state):
        """ε-greedy 策略"""
        if random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        else:
            return np.argmax(self.q_table[state])
    
    def update(self, state, action, reward, next_state, done):
        """Q-Learning 更新"""
        if done:
            target = reward
        else:
            target = reward + self.gamma * np.max(self.q_table[next_state])
        
        td_error = target - self.q_table[state, action]
        self.q_table[state, action] += self.alpha * td_error
    
    def train(self, env, n_episodes=1000):
        """训练循环"""
        rewards_per_episode = []
        
        for episode in range(n_episodes):
            state = env.reset()
            total_reward = 0
            done = False
            
            while not done:
                action = self.get_action(state)
                next_state, reward, done = env.step(action)
                self.update(state, action, reward, next_state, done)
                total_reward += reward
                state = next_state
            
            rewards_per_episode.append(total_reward)
            
            if episode % 100 == 0:
                avg_reward = np.mean(rewards_per_episode[-100:])
                print(f"Episode {episode}, Avg Reward: {avg_reward:.2f}")
        
        return rewards_per_episode

# 简单 GridWorld 环境
class GridWorld:
    def __init__(self, size=5):
        self.size = size
        self.goal = size - 1
        self.reset()
    
    def reset(self):
        self.state = 0
        return self.state
    
    def step(self, action):
        # 0: 左，1: 右
        if action == 1:  # 右
            self.state = min(self.state + 1, self.goal)
        
        reward = -1
        done = (self.state == self.goal)
        if done:
            reward = 100
        
        return self.state, reward, done

if __name__ == "__main__":
    env = GridWorld(size=10)
    agent = QLearning(n_states=env.size, n_actions=2)
    rewards = agent.train(env, n_episodes=500)
    print(f"Final Q-table: \n{agent.q_table}")
