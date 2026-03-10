#!/usr/bin/env python3
"""
简化版 CartPole 知识蒸馏演示
不依赖外部库，使用纯 Python + 数学

用于测试 Code Agent v2.0 的运行能力

小虾 🦐 | 2026-03-06
"""

import math
import random
from typing import List, Tuple

# ============================================================
# 简化的 CartPole 环境 (纯 Python 实现)
# ============================================================

class SimpleCartPole:
    """简化版 CartPole 环境"""
    
    def __init__(self):
        self.gravity = 9.8
        self.cart_mass = 1.0
        self.pole_mass = 0.1
        self.pole_length = 0.5
        self.dt = 0.02
        
        self.reset()
    
    def reset(self) -> List[float]:
        """重置环境"""
        self.x = random.uniform(-0.05, 0.05)
        self.x_dot = random.uniform(-0.05, 0.05)
        self.theta = random.uniform(-0.05, 0.05)
        self.theta_dot = random.uniform(-0.05, 0.05)
        self.steps = 0
        return self._get_state()
    
    def _get_state(self) -> List[float]:
        """获取状态"""
        return [self.x, self.x_dot, self.theta, self.theta_dot]
    
    def step(self, action: int) -> Tuple[List[float], float, bool]:
        """执行动作"""
        force = 10.0 if action == 1 else -10.0
        
        # 简化的物理模拟
        cos_theta = math.cos(self.theta)
        sin_theta = math.sin(self.theta)
        
        total_mass = self.cart_mass + self.pole_mass
        pole_mass_length = self.pole_mass * self.pole_length
        
        acc_theta = (self.gravity * sin_theta + 
                    (force + pole_mass_length * self.theta_dot**2 * sin_theta) / total_mass) / \
                   (self.pole_length * (4/3 - self.pole_mass * cos_theta**2 / total_mass))
        
        acc_x = (force - pole_mass_length * (self.theta_dot**2 * sin_theta - acc_theta * cos_theta)) / total_mass
        
        # 更新状态
        self.x += self.dt * self.x_dot
        self.x_dot += self.dt * acc_x
        self.theta += self.dt * self.theta_dot
        self.theta_dot += self.dt * acc_theta
        
        self.steps += 1
        
        # 检查终止条件
        done = (
            abs(self.x) > 2.4 or
            abs(self.theta) > 0.2095 or  # 12 度
            self.steps >= 200
        )
        
        # 奖励：存活越久越好
        reward = 1.0 if not done else 0.0
        
        return self._get_state(), reward, done


# ============================================================
# 简化的 DQN 网络 (纯 Python 实现)
# ============================================================

class SimpleNeuralNetwork:
    """简化的神经网络"""
    
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        
        # 初始化权重 (Xavier 初始化)
        self.W1 = [[random.gauss(0, math.sqrt(2.0 / input_dim)) 
                    for _ in range(hidden_dim)] for _ in range(input_dim)]
        self.b1 = [0.0] * hidden_dim
        
        self.W2 = [[random.gauss(0, math.sqrt(2.0 / hidden_dim)) 
                    for _ in range(output_dim)] for _ in range(hidden_dim)]
        self.b2 = [0.0] * output_dim
    
    def relu(self, x: float) -> float:
        return max(0, x)
    
    def forward(self, x: List[float]) -> List[float]:
        """前向传播"""
        # 隐藏层
        hidden = []
        for j in range(self.hidden_dim):
            h = self.b1[j]
            for i in range(self.input_dim):
                h += x[i] * self.W1[i][j]
            hidden.append(self.relu(h))
        
        # 输出层
        output = []
        for k in range(self.output_dim):
            o = self.b2[k]
            for j in range(self.hidden_dim):
                o += hidden[j] * self.W2[j][k]
            output.append(o)
        
        return output
    
    def get_action(self, state: List[float]) -> int:
        """获取动作"""
        q_values = self.forward(state)
        return q_values.index(max(q_values))
    
    def copy_weights_from(self, other: 'SimpleNeuralNetwork', alpha: float = 0.5):
        """从另一个网络软更新权重 (用于蒸馏)"""
        for i in range(self.input_dim):
            for j in range(self.hidden_dim):
                self.W1[i][j] = alpha * self.W1[i][j] + (1 - alpha) * other.W1[i][j]
        
        for j in range(self.hidden_dim):
            self.b1[j] = alpha * self.b1[j] + (1 - alpha) * other.b1[j]
            for k in range(self.output_dim):
                self.W2[j][k] = alpha * self.W2[j][k] + (1 - alpha) * other.W2[j][k]
        
        for k in range(self.output_dim):
            self.b2[k] = alpha * self.b2[k] + (1 - alpha) * other.b2[k]


# ============================================================
# 知识蒸馏训练器
# ============================================================

class DistillationTrainer:
    """知识蒸馏训练器"""
    
    def __init__(self, teacher: SimpleNeuralNetwork, student: SimpleNeuralNetwork):
        self.teacher = teacher
        self.student = student
        self.env = SimpleCartPole()
    
    def collect_teacher_demos(self, num_episodes: int = 50) -> List[Tuple[List[float], int]]:
        """收集教师演示"""
        demos = []
        
        for _ in range(num_episodes):
            state = self.env.reset()
            done = False
            
            while not done:
                action = self.teacher.get_action(state)
                demos.append((state.copy(), action))
                state, reward, done = self.env.step(action)
        
        return demos
    
    def train_student(self, demos: List[Tuple[List[float], int]], epochs: int = 100) -> List[float]:
        """训练学生网络 (行为克隆)"""
        losses = []
        
        for epoch in range(epochs):
            total_loss = 0.0
            count = 0
            
            for state, teacher_action in demos:
                # 学生预测
                student_logits = self.student.forward(state)
                
                # 简单 MSE 损失
                target = [0.0] * self.student.output_dim
                target[teacher_action] = 1.0
                
                loss = sum((s - t)**2 for s, t in zip(student_logits, target))
                total_loss += loss
                count += 1
                
                # 简单梯度下降 (简化版)
                for j in range(self.student.hidden_dim):
                    for k in range(self.student.output_dim):
                        grad = 2 * (student_logits[k] - target[k])
                        self.student.W2[j][k] -= 0.01 * grad * self.relu(sum(state))
            
            avg_loss = total_loss / max(count, 1)
            losses.append(avg_loss)
            
            if epoch % 10 == 0:
                print(f"  Epoch {epoch}: Loss = {avg_loss:.4f}")
        
        return losses
    
    def evaluate(self, network: SimpleNeuralNetwork, num_episodes: int = 20) -> dict:
        """评估网络性能"""
        total_rewards = []
        total_steps = []
        
        for _ in range(num_episodes):
            state = self.env.reset()
            done = False
            reward_sum = 0.0
            steps = 0
            
            while not done:
                action = network.get_action(state)
                state, reward, done = self.env.step(action)
                reward_sum += reward
                steps += 1
            
            total_rewards.append(reward_sum)
            total_steps.append(steps)
        
        return {
            'avg_reward': sum(total_rewards) / len(total_rewards),
            'max_reward': max(total_rewards),
            'min_reward': min(total_rewards),
            'avg_steps': sum(total_steps) / len(total_steps),
            'max_steps': max(total_steps)
        }


# ============================================================
# 主程序
# ============================================================

def main():
    print("=" * 60)
    print("CartPole 知识蒸馏演示 (纯 Python 版)")
    print("=" * 60)
    print()
    
    # 创建网络
    # 教师：大网络
    teacher = SimpleNeuralNetwork(input_dim=4, hidden_dim=32, output_dim=2)
    # 学生：小网络
    student = SimpleNeuralNetwork(input_dim=4, hidden_dim=8, output_dim=2)
    
    print("网络架构:")
    print(f"  教师：4 → 32 → 2 (参数：{4*32 + 32 + 32*2 + 2} = ~{4*32 + 32 + 32*2 + 2})")
    print(f"  学生：4 → 8 → 2  (参数：{4*8 + 8 + 8*2 + 2} = ~{4*8 + 8 + 8*2 + 2})")
    print(f"  压缩比：{(4*32 + 32 + 32*2 + 2) / (4*8 + 8 + 8*2 + 2):.1f}x")
    print()
    
    # 创建训练器
    trainer = DistillationTrainer(teacher, student)
    
    # Phase 1: 收集教师演示
    print("Phase 1: 收集教师演示...")
    demos = trainer.collect_teacher_demos(num_episodes=30)
    print(f"  收集 {len(demos)} 个状态 - 动作对")
    print()
    
    # Phase 2: 蒸馏到学生
    print("Phase 2: 知识蒸馏...")
    losses = trainer.train_student(demos, epochs=50)
    print()
    
    # Phase 3: 评估
    print("Phase 3: 评估性能...")
    print()
    
    print("教师性能:")
    teacher_stats = trainer.evaluate(teacher)
    print(f"  平均奖励：{teacher_stats['avg_reward']:.1f}")
    print(f"  最大奖励：{teacher_stats['max_reward']:.1f}")
    print(f"  平均步数：{teacher_stats['avg_steps']:.1f}")
    print()
    
    print("学生性能 (蒸馏后):")
    student_stats = trainer.evaluate(student)
    print(f"  平均奖励：{student_stats['avg_reward']:.1f}")
    print(f"  最大奖励：{student_stats['max_reward']:.1f}")
    print(f"  平均步数：{student_stats['avg_steps']:.1f}")
    print()
    
    # 性能保持率
    retention = (student_stats['avg_reward'] / max(teacher_stats['avg_reward'], 1)) * 100
    print(f"性能保持率：{retention:.1f}%")
    print()
    
    print("=" * 60)
    print("✅ 知识蒸馏演示完成!")
    print("=" * 60)
    
    return {
        'teacher': teacher_stats,
        'student': student_stats,
        'retention': retention,
        'compression': (4*32 + 32 + 32*2 + 2) / (4*8 + 8 + 8*2 + 2)
    }


if __name__ == '__main__':
    result = main()
    
    # 保存结果
    import json
    from pathlib import Path
    
    output_dir = Path('/home/openclaw/.openclaw/workspace/obsidian-repo/results/cartpole-simple')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / 'metrics.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n结果已保存到：{output_dir / 'metrics.json'}")
