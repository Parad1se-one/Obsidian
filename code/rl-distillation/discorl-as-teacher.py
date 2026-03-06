"""
DisCoRL as Teacher: 知识蒸馏实验

Teacher: 完整的 DisCoRL 框架 (多任务 continual RL + 策略蒸馏)
Student: 简化的单一策略网络

实验流程:
1. 训练 DisCoRL Teacher (3 个连续任务)
2. 收集 Teacher 的动作分布
3. 蒸馏到 Student 网络
4. 对比性能

作者：小虾 🦐
日期：2026-03-06
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import gymnasium as gym
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
from dataclasses import dataclass
import time


# ============================================================
# 实验配置
# ============================================================

@dataclass
class Config:
    # 环境
    env_name: str = "CartPole-v1"
    num_tasks: int = 3  # 3 个连续任务
    
    # 任务定义 (通过修改物理参数创建不同任务)
    task_configs: Dict = None
    
    # 网络架构
    z_dim: int = 64  # 状态表示维度
    teacher_hidden: int = 256
    student_hidden: int = 128
    
    # 训练参数
    teacher_epochs: int = 200  # 每个任务训练轮数
    distill_epochs: int = 100
    batch_size: int = 64
    lr: float = 3e-4
    
    # 蒸馏参数
    temperature: float = 2.0
    alpha: float = 0.7  # soft target 权重
    
    # 评估
    eval_episodes: int = 50
    
    def __post_init__(self):
        if self.task_configs is None:
            # 定义 3 个不同难度的 CartPole 任务
            self.task_configs = {
                0: {"name": "Easy", "gravity": 9.8, "pole_length": 0.5},
                1: {"name": "Normal", "gravity": 9.8, "pole_length": 0.5},  # 标准
                2: {"name": "Hard", "gravity": 15.0, "pole_length": 0.3},  # 更难
            }


# ============================================================
# 1. DisCoRL Teacher 组件
# ============================================================

class StateEncoder(nn.Module):
    """状态编码器 - 学习任务的低维表示"""
    
    def __init__(self, state_dim: int, z_dim: int = 64):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, z_dim)
        )
    
    def forward(self, x):
        return self.network(x)


class TeacherPolicy(nn.Module):
    """单个任务的教师策略"""
    
    def __init__(self, z_dim: int, action_dim: int = 2):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(z_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )
    
    def forward(self, z):
        return self.network(z)
    
    def get_probs(self, z, temperature=1.0):
        logits = self.forward(z)
        return F.softmax(logits / temperature, dim=-1)


class DisCoRLTeacher:
    """
    DisCoRL Teacher - 多任务 continual RL
    """
    
    def __init__(self, state_dim: int, action_dim: int, num_tasks: int, config: Config):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.num_tasks = num_tasks
        self.config = config
        self.device = torch.device('cpu')
        
        # 状态编码器 (共享)
        self.encoder = StateEncoder(state_dim, config.z_dim).to(self.device)
        
        # 每个任务一个教师策略
        self.teachers = nn.ModuleList([
            TeacherPolicy(config.z_dim, action_dim)
            for _ in range(num_tasks)
        ])
        
        self.encoder_opt = torch.optim.Adam(self.encoder.parameters(), lr=config.lr)
        self.teacher_opts = [
            torch.optim.Adam(t.parameters(), lr=config.lr)
            for t in self.teachers
        ]
        
        # 训练数据缓冲区
        self.buffers: List[List[Tuple]] = [[] for _ in range(num_tasks)]
    
    def encode(self, state: np.ndarray) -> torch.Tensor:
        """编码状态"""
        with torch.no_grad():
            s = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            return self.encoder(s)
    
    def train_task(self, task_id: int, env: gym.Env, num_epochs: int):
        """训练单个任务的教师策略"""
        print(f"  训练任务 {task_id} ({self.config.task_configs[task_id]['name']})...")
        
        # 收集训练数据
        states, actions = [], []
        for _ in range(num_epochs):
            state, _ = env.reset()
            done = False
            while not done:
                z = self.encode(state)
                probs = self.teachers[task_id].get_probs(z)
                action = torch.multinomial(probs, 1).item()
                
                next_state, reward, terminated, truncated, _ = env.step(action)
                done = terminated or truncated
                
                states.append((z.clone().detach(), state.copy()))
                actions.append(action)
                state = next_state
        
        # 行为克隆训练
        states_tensor = torch.cat([s[0] for s in states], dim=0)
        actions_tensor = torch.LongTensor(actions)
        
        for epoch in range(50):
            self.teacher_opts[task_id].zero_grad()
            logits = self.teachers[task_id](states_tensor)
            loss = F.cross_entropy(logits, actions_tensor)
            loss.backward()
            self.teacher_opts[task_id].step()
        
        # 评估
        avg_reward = self.evaluate_task(task_id, env, episodes=20)
        print(f"    ✓ 任务 {task_id} 完成 - 平均奖励：{avg_reward:.1f}")
        return avg_reward
    
    def evaluate_task(self, task_id: int, env: gym.Env, episodes: int = 20) -> float:
        """评估单个任务的性能"""
        rewards = []
        for _ in range(episodes):
            state, _ = env.reset()
            total_reward = 0
            done = False
            while not done:
                z = self.encode(state)
                probs = self.teachers[task_id].get_probs(z)
                action = torch.argmax(probs).item()
                state, reward, terminated, truncated, _ = env.step(action)
                total_reward += reward
                done = terminated or truncated
            rewards.append(total_reward)
        return np.mean(rewards)
    
    def collect_distillation_data(self, envs: List[gym.Env], samples_per_task: int = 500):
        """收集蒸馏数据"""
        print("收集蒸馏数据...")
        distill_data = []
        
        for task_id, env in enumerate(envs):
            for _ in range(samples_per_task):
                state, _ = env.reset()
                done = False
                steps = 0
                while not done and steps < 100:
                    z = self.encode(state)
                    teacher_probs = self.teachers[task_id].get_probs(z, temperature=self.config.temperature)
                    
                    distill_data.append({
                        'state': state.copy(),
                        'z': z.clone().detach(),
                        'task_id': task_id,
                        'teacher_probs': teacher_probs.clone().detach()
                    })
                    
                    action = torch.argmax(teacher_probs).item()
                    state, _, terminated, truncated, _ = env.step(action)
                    done = terminated or truncated
                    steps += 1
        
        print(f"  ✓ 收集 {len(distill_data)} 个样本")
        return distill_data


# ============================================================
# 2. Student Network
# ============================================================

class StudentNetwork(nn.Module):
    """
    学生网络 - 简化架构
    直接从状态到动作，通过蒸馏学习 Teacher 知识
    """
    
    def __init__(self, state_dim: int, action_dim: int = 2, hidden_dim: int = 128):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )
    
    def forward(self, x):
        return self.network(x)
    
    def get_probs(self, x, temperature=1.0):
        logits = self.forward(x)
        return F.softmax(logits / temperature, dim=-1)


class StudentTrainer:
    """学生网络蒸馏训练器"""
    
    def __init__(self, state_dim: int, action_dim: int, config: Config):
        self.config = config
        self.device = torch.device('cpu')
        
        self.student = StudentNetwork(state_dim, action_dim, config.student_hidden).to(self.device)
        self.optimizer = torch.optim.Adam(self.student.parameters(), lr=config.lr)
    
    def distill(self, data: List[Dict], num_epochs: int):
        """知识蒸馏"""
        print(f"开始蒸馏 (T={self.config.temperature}, α={self.config.alpha})...")
        
        losses = []
        for epoch in range(num_epochs):
            epoch_loss = 0
            np.random.shuffle(data)
            
            for i in range(0, len(data), self.config.batch_size):
                batch = data[i:i+self.config.batch_size]
                
                states = torch.FloatTensor(np.array([d['state'] for d in batch])).to(self.device)
                teacher_probs = torch.cat([d['teacher_probs'] for d in batch], dim=0).to(self.device)
                
                self.optimizer.zero_grad()
                
                student_logits = self.student(states)
                student_log_probs = F.log_softmax(student_logits / self.config.temperature, dim=-1)
                
                # KL 散度损失
                kl_loss = F.kl_div(student_log_probs, teacher_probs, reduction='batchmean')
                loss = kl_loss * (self.config.temperature ** 2)
                
                loss.backward()
                self.optimizer.step()
                
                epoch_loss += loss.item()
            
            avg_loss = epoch_loss / (len(data) // self.config.batch_size)
            losses.append(avg_loss)
            
            if (epoch + 1) % 20 == 0:
                print(f"  Epoch {epoch+1}/{num_epochs} - Loss: {avg_loss:.4f}")
        
        print(f"  ✓ 蒸馏完成")
        return losses
    
    def evaluate(self, env: gym.Env, episodes: int = 50) -> float:
        """评估学生性能"""
        rewards = []
        for _ in range(episodes):
            state, _ = env.reset()
            total_reward = 0
            done = False
            while not done:
                s = torch.FloatTensor(state).unsqueeze(0).to(self.device)
                probs = self.student.get_probs(s)
                action = torch.argmax(probs).item()
                state, reward, terminated, truncated, _ = env.step(action)
                total_reward += reward
                done = terminated or truncated
            rewards.append(total_reward)
        return np.mean(rewards)


# ============================================================
# 3. 主实验
# ============================================================

def modify_env(env: gym.Env, task_config: Dict):
    """修改环境参数以创建不同任务"""
    # CartPole 任务修改
    if hasattr(env.unwrapped, 'gravity'):
        env.unwrapped.gravity = task_config.get('gravity', 9.8)
    if hasattr(env.unwrapped, 'pole_length'):
        env.unwrapped.pole_length = task_config.get('pole_length', 0.5)
    return env


def run_experiment():
    """运行完整实验"""
    print("=" * 60)
    print("🔬 DisCoRL as Teacher - 知识蒸馏实验")
    print("=" * 60)
    
    config = Config()
    
    # 创建环境
    print("\n📦 创建环境...")
    base_env = gym.make(config.env_name)
    state_dim = base_env.observation_space.shape[0]
    action_dim = base_env.action_space.n
    print(f"  环境：{config.env_name}")
    print(f"  状态维度：{state_dim}, 动作维度：{action_dim}")
    print(f"  任务数量：{config.num_tasks}")
    
    # 初始化 Teacher
    print("\n🎓 初始化 DisCoRL Teacher...")
    teacher = DisCoRLTeacher(state_dim, action_dim, config.num_tasks, config)
    
    # 训练每个任务的教师
    print("\n📚 训练教师策略 (Continual RL)...")
    teacher_rewards = []
    for task_id in range(config.num_tasks):
        env = gym.make(config.env_name)
        modify_env(env, config.task_configs[task_id])
        reward = teacher.train_task(task_id, env, config.teacher_epochs)
        teacher_rewards.append(reward)
        env.close()
    
    # 收集蒸馏数据
    print("\n📊 收集蒸馏数据...")
    envs = []
    for task_id in range(config.num_tasks):
        env = gym.make(config.env_name)
        modify_env(env, config.task_configs[task_id])
        envs.append(env)
    
    distill_data = teacher.collect_distillation_data(envs, samples_per_task=300)
    
    # 评估 Teacher
    print("\n📈 评估 Teacher 性能...")
    teacher_eval_rewards = []
    for task_id in range(config.num_tasks):
        env = gym.make(config.env_name)
        modify_env(env, config.task_configs[task_id])
        reward = teacher.evaluate_task(task_id, env, episodes=config.eval_episodes)
        teacher_eval_rewards.append(reward)
        print(f"  任务 {task_id} ({config.task_configs[task_id]['name']}): {reward:.1f}")
        env.close()
    
    # 初始化并训练 Student
    print("\n🎓 初始化 Student...")
    student_trainer = StudentTrainer(state_dim, action_dim, config)
    
    print("\n🔄 知识蒸馏...")
    distill_losses = student_trainer.distill(distill_data, config.distill_epochs)
    
    # 评估 Student
    print("\n📈 评估 Student 性能...")
    student_eval_rewards = []
    for task_id in range(config.num_tasks):
        env = gym.make(config.env_name)
        modify_env(env, config.task_configs[task_id])
        reward = student_trainer.evaluate(env, episodes=config.eval_episodes)
        student_eval_rewards.append(reward)
        print(f"  任务 {task_id} ({config.task_configs[task_id]['name']}): {reward:.1f}")
        env.close()
    
    # 计算性能保持率
    print("\n" + "=" * 60)
    print("📊 实验结果")
    print("=" * 60)
    
    for task_id in range(config.num_tasks):
        t_reward = teacher_eval_rewards[task_id]
        s_reward = student_eval_rewards[task_id]
        retention = (s_reward / t_reward * 100) if t_reward > 0 else 0
        print(f"任务 {task_id} ({config.task_configs[task_id]['name']}):")
        print(f"  Teacher: {t_reward:.1f}")
        print(f"  Student: {s_reward:.1f}")
        print(f"  性能保持率：{retention:.1f}%")
    
    avg_teacher = np.mean(teacher_eval_rewards)
    avg_student = np.mean(student_eval_rewards)
    avg_retention = (avg_student / avg_teacher * 100) if avg_teacher > 0 else 0
    
    print(f"\n平均性能:")
    print(f"  Teacher: {avg_teacher:.1f}")
    print(f"  Student: {avg_student:.1f}")
    print(f"  平均保持率：{avg_retention:.1f}%")
    
    # 模型大小对比
    teacher_params = sum(p.numel() for p in teacher.encoder.parameters())
    teacher_params += sum(p.numel() for t in teacher.teachers for p in t.parameters())
    student_params = sum(p.numel() for p in student_trainer.student.parameters())
    
    print(f"\n模型大小:")
    print(f"  Teacher (Encoder + {config.num_tasks} Policies): {teacher_params:,} 参数")
    print(f"  Student: {student_params:,} 参数")
    print(f"  压缩比：{teacher_params / student_params:.1f}x")
    
    # 可视化
    print("\n📈 生成可视化...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. 蒸馏损失曲线
    axes[0, 0].plot(distill_losses)
    axes[0, 0].set_title('Distillation Loss')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('KL Loss')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Teacher vs Student 性能对比
    tasks = [f"T{i}\n({config.task_configs[i]['name']})" for i in range(config.num_tasks)]
    x = np.arange(len(tasks))
    width = 0.35
    axes[0, 1].bar(x - width/2, teacher_eval_rewards, width, label='Teacher', color='steelblue')
    axes[0, 1].bar(x + width/2, student_eval_rewards, width, label='Student', color='coral')
    axes[0, 1].set_title('Teacher vs Student Performance')
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(tasks)
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # 3. 性能保持率
    retentions = [(s/t*100) if t > 0 else 0 for s, t in zip(student_eval_rewards, teacher_eval_rewards)]
    axes[1, 0].bar(tasks, retentions, color='seagreen')
    axes[1, 0].set_title('Performance Retention Rate (%)')
    axes[1, 0].axhline(y=100, color='r', linestyle='--', alpha=0.5, label='100%')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # 4. 训练总结
    axes[1, 1].axis('off')
    summary = f"""
    ════════════════════════════════════════
    📊 实验总结
    ════════════════════════════════════════
    
    Teacher (DisCoRL):
      - 平均奖励：{avg_teacher:.1f}
      - 参数量：{teacher_params:,}
    
    Student:
      - 平均奖励：{avg_student:.1f}
      - 参数量：{student_params:,}
    
    性能保持率：{avg_retention:.1f}%
    模型压缩比：{teacher_params / student_params:.1f}x
    
    蒸馏配置:
      - 温度 T: {config.temperature}
      - Soft 权重 α: {config.alpha}
      - 蒸馏轮数：{config.distill_epochs}
    ════════════════════════════════════════
    """
    axes[1, 1].text(0.1, 0.5, summary, fontsize=10, family='monospace',
                   verticalalignment='center', transform=axes[1, 1].transAxes)
    
    plt.tight_layout()
    plt.savefig('/home/openclaw/.openclaw/workspace/research/experiments/discorl-teacher-results.png', dpi=150)
    print(f"  ✓ 可视化已保存")
    
    # 关闭环境
    for env in envs:
        env.close()
    base_env.close()
    
    print("\n✅ 实验完成!")
    
    return {
        'teacher_rewards': teacher_eval_rewards,
        'student_rewards': student_eval_rewards,
        'retention_rate': avg_retention,
        'compression_ratio': teacher_params / student_params,
        'distill_losses': distill_losses
    }


if __name__ == "__main__":
    results = run_experiment()
