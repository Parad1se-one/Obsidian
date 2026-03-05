"""
DisCoRL: Continual Reinforcement Learning via Policy Distillation
PyTorch Implementation

基于 arXiv:1907.05855 实现
实现者：小虾 🦐
日期：2026-03-05
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, List, Tuple, Optional


# ============================================================
# 1. 状态表示网络 (State Representation Network)
# ============================================================

class StateEncoder(nn.Module):
    """
    状态编码器 - 学习任务的低维表示
    
    输入：原始状态 (如图像或向量)
    输出：低维状态表示 z
    """
    
    def __init__(self, state_dim: int, z_dim: int = 64, hidden_dim: int = 256):
        super(StateEncoder, self).__init__()
        
        self.encoder = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, z_dim)
        )
        
        self.z_dim = z_dim
    
    def forward(self, state: torch.Tensor) -> torch.Tensor:
        """编码状态为低维表示"""
        return self.encoder(state)
    
    def get_z_dim(self) -> int:
        return self.z_dim


# ============================================================
# 2. 任务推断网络 (Task Inference Network)
# ============================================================

class TaskInference(nn.Module):
    """
    任务推断网络 - 基于状态表示推断当前任务
    
    输入：状态表示 z
    输出：任务概率分布
    """
    
    def __init__(self, z_dim: int, num_tasks: int, hidden_dim: int = 128):
        super(TaskInference, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(z_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, num_tasks)
        )
        
        self.num_tasks = num_tasks
    
    def forward(self, z: torch.Tensor) -> torch.Tensor:
        """推断任务概率"""
        return F.softmax(self.network(z), dim=-1)
    
    def predict(self, z: torch.Tensor) -> int:
        """预测最可能的任务 ID"""
        with torch.no_grad():
            probs = self.forward(z)
            return torch.argmax(probs, dim=-1).item()


# ============================================================
# 3. 策略网络 (Policy Network)
# ============================================================

class PolicyNetwork(nn.Module):
    """
    策略网络 - 输出动作分布
    
    支持两种模式:
    1. 任务特定策略 (教师)
    2. 通用策略 (学生，条件于任务 ID)
    """
    
    def __init__(self, 
                 z_dim: int, 
                 action_dim: int, 
                 num_tasks: int = 1,
                 hidden_dim: int = 256,
                 is_teacher: bool = False):
        super(PolicyNetwork, self).__init__()
        
        self.is_teacher = is_teacher
        self.num_tasks = num_tasks
        
        # 如果是学生网络，需要任务嵌入
        if not is_teacher and num_tasks > 1:
            self.task_embedding = nn.Embedding(num_tasks, z_dim)
            input_dim = z_dim * 2  # z + task embedding
        else:
            self.task_embedding = None
            input_dim = z_dim
        
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, action_dim)
        )
        
        self.action_dim = action_dim
    
    def forward(self, 
                z: torch.Tensor, 
                task_id: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        输出动作 logits
        
        Args:
            z: 状态表示 [batch, z_dim]
            task_id: 任务 ID [batch] (学生网络需要)
        """
        if self.task_embedding is not None and task_id is not None:
            task_emb = self.task_embedding(task_id)
            z = torch.cat([z, task_emb], dim=-1)
        
        return self.network(z)
    
    def get_action_probs(self, 
                         z: torch.Tensor, 
                         task_id: Optional[torch.Tensor] = None,
                         temperature: float = 1.0) -> torch.Tensor:
        """输出动作概率分布"""
        logits = self.forward(z, task_id)
        return F.softmax(logits / temperature, dim=-1)


# ============================================================
# 4. 教师策略集合 (Teacher Policies)
# ============================================================

class TeacherPolicies:
    """
    管理多个教师策略 (每个任务一个)
    """
    
    def __init__(self, 
                 z_dim: int, 
                 action_dim: int, 
                 num_tasks: int,
                 device: str = 'cpu'):
        
        self.teachers = nn.ModuleList([
            PolicyNetwork(z_dim, action_dim, num_tasks=1, is_teacher=True)
            for _ in range(num_tasks)
        ])
        
        self.num_tasks = num_tasks
        self.device = device
    
    def get_teacher_action(self, 
                           z: torch.Tensor, 
                           task_id: int) -> torch.Tensor:
        """获取指定任务教师策略的动作概率"""
        teacher = self.teachers[task_id]
        return teacher.get_action_probs(z)
    
    def train_teacher(self, 
                      task_id: int, 
                      states: torch.Tensor, 
                      actions: torch.Tensor,
                      optimizer: torch.optim.Optimizer) -> float:
        """
        训练单个教师策略 (使用行为克隆)
        
        Args:
            task_id: 任务 ID
            states: 状态表示 [batch, z_dim]
            actions: 专家动作 [batch]
            optimizer: 优化器
        
        Returns:
            损失值
        """
        teacher = self.teachers[task_id]
        optimizer.zero_grad()
        
        logits = teacher(states)
        loss = F.cross_entropy(logits, actions)
        
        loss.backward()
        optimizer.step()
        
        return loss.item()


# ============================================================
# 5. 学生策略 (Student Policy with Distillation)
# ============================================================

class StudentPolicy:
    """
    学生策略 - 通过蒸馏学习多个教师策略
    """
    
    def __init__(self, 
                 z_dim: int, 
                 action_dim: int, 
                 num_tasks: int,
                 device: str = 'cpu'):
        
        self.student = PolicyNetwork(
            z_dim, action_dim, num_tasks=num_tasks, is_teacher=False
        )
        
        self.num_tasks = num_tasks
        self.device = device
        self.optimizer = torch.optim.Adam(self.student.parameters(), lr=3e-4)
    
    def distill(self, 
                z: torch.Tensor,
                task_id: int,
                teacher_probs: torch.Tensor,
                temperature: float = 1.0) -> float:
        """
        策略蒸馏 - 最小化学生与教师的 KL 散度
        
        Args:
            z: 状态表示 [batch, z_dim]
            task_id: 任务 ID
            teacher_probs: 教师动作概率 [batch, action_dim]
            temperature: 蒸馏温度
        
        Returns:
            蒸馏损失
        """
        self.optimizer.zero_grad()
        
        task_ids = torch.full((z.shape[0],), task_id, 
                             dtype=torch.long, device=self.device)
        
        student_logits = self.student(z, task_ids)
        student_probs = F.softmax(student_logits / temperature, dim=-1)
        
        # KL 散度损失
        kl_loss = F.kl_div(
            F.log_softmax(student_logits / temperature, dim=-1),
            teacher_probs,
            reduction='batchmean'
        )
        
        # 温度缩放
        loss = kl_loss * (temperature ** 2)
        
        loss.backward()
        self.optimizer.step()
        
        return loss.item()
    
    def get_action(self, 
                   z: torch.Tensor, 
                   task_id: int, 
                   deterministic: bool = True) -> int:
        """
        获取动作
        
        Args:
            z: 状态表示
            task_id: 任务 ID
            deterministic: 是否确定性选择
        
        Returns:
            动作 ID
        """
        with torch.no_grad():
            task_ids = torch.tensor([task_id], dtype=torch.long, device=self.device)
            probs = self.student.get_action_probs(z, task_ids)
            
            if deterministic:
                return torch.argmax(probs, dim=-1).item()
            else:
                return torch.multinomial(probs, 1).item()


# ============================================================
# 6. DisCoRL 主框架
# ============================================================

class DisCoRL:
    """
    DisCoRL 完整框架
    
    流程:
    1. 训练状态编码器
    2. 顺序训练每个任务的教师策略
    3. 蒸馏教师到学生
    4. 学习任务推断
    """
    
    def __init__(self, 
                 state_dim: int,
                 action_dim: int,
                 num_tasks: int,
                 z_dim: int = 64,
                 device: str = 'cpu'):
        
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.num_tasks = num_tasks
        self.device = device
        
        # 组件
        self.state_encoder = StateEncoder(state_dim, z_dim).to(device)
        self.task_inference = TaskInference(z_dim, num_tasks).to(device)
        self.teachers = TeacherPolicies(z_dim, action_dim, num_tasks, device)
        self.student = StudentPolicy(z_dim, action_dim, num_tasks, device)
        
        # 优化器
        self.encoder_optimizer = torch.optim.Adam(
            self.state_encoder.parameters(), lr=3e-4
        )
        self.task_optimizer = torch.optim.Adam(
            self.task_inference.parameters(), lr=3e-4
        )
    
    def encode_state(self, state: np.ndarray) -> torch.Tensor:
        """编码原始状态为 z"""
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            z = self.state_encoder(state_tensor)
        return z
    
    def train_teacher_for_task(self, 
                               task_id: int,
                               trajectories: List[Tuple[np.ndarray, int]],
                               num_epochs: int = 100) -> List[float]:
        """
        训练指定任务的教师策略
        
        Args:
            task_id: 任务 ID
            trajectories: (state, action) 轨迹列表
            num_epochs: 训练轮数
        
        Returns:
            损失历史
        """
        losses = []
        
        # 编码所有状态
        states = []
        actions = []
        for state, action in trajectories:
            z = self.encode_state(state)
            states.append(z)
            actions.append(action)
        
        states = torch.cat(states, dim=0)
        actions = torch.LongTensor(actions).to(self.device)
        
        # 训练教师
        teacher_optimizer = torch.optim.Adam(
            self.teachers.teachers[task_id].parameters(), lr=3e-4
        )
        
        for epoch in range(num_epochs):
            loss = self.teachers.train_teacher(
                task_id, states, actions, teacher_optimizer
            )
            losses.append(loss)
        
        return losses
    
    def distill_all_teachers(self,
                             replay_buffer: List[Tuple[np.ndarray, int, int]],
                             num_epochs: int = 100) -> List[float]:
        """
        蒸馏所有教师策略到学生
        
        Args:
            replay_buffer: (state, task_id, action) 列表
            num_epochs: 训练轮数
        
        Returns:
            损失历史
        """
        losses = []
        
        for epoch in range(num_epochs):
            epoch_loss = 0.0
            num_samples = 0
            
            for state, task_id, _ in replay_buffer:
                z = self.encode_state(state)
                
                # 获取教师动作概率
                with torch.no_grad():
                    teacher_probs = self.teachers.get_teacher_action(z, task_id)
                
                # 蒸馏
                loss = self.student.distill(z, task_id, teacher_probs)
                epoch_loss += loss
                num_samples += 1
            
            avg_loss = epoch_loss / max(num_samples, 1)
            losses.append(avg_loss)
        
        return losses
    
    def infer_task(self, state: np.ndarray) -> int:
        """推断当前状态属于哪个任务"""
        z = self.encode_state(state)
        return self.task_inference.predict(z)
    
    def get_action(self, 
                   state: np.ndarray, 
                   task_id: Optional[int] = None) -> int:
        """
        获取动作
        
        如果 task_id 为 None，自动推断任务
        """
        z = self.encode_state(state)
        
        if task_id is None:
            task_id = self.infer_task(state)
        
        return self.student.get_action(z, task_id)
    
    def save(self, path: str):
        """保存模型"""
        torch.save({
            'state_encoder': self.state_encoder.state_dict(),
            'task_inference': self.task_inference.state_dict(),
            'teachers': [t.state_dict() for t in self.teachers.teachers],
            'student': self.student.student.state_dict(),
        }, path)
    
    def load(self, path: str):
        """加载模型"""
        checkpoint = torch.load(path, map_location=self.device)
        self.state_encoder.load_state_dict(checkpoint['state_encoder'])
        self.task_inference.load_state_dict(checkpoint['task_inference'])
        for i, sd in enumerate(checkpoint['teachers']):
            self.teachers.teachers[i].load_state_dict(sd)
        self.student.student.load_state_dict(checkpoint['student'])


# ============================================================
# 7. 使用示例
# ============================================================

if __name__ == "__main__":
    # 示例：3 个任务的 2D 导航
    STATE_DIM = 4  # (x, y, vx, vy)
    ACTION_DIM = 4  # 上、下、左、右
    NUM_TASKS = 3
    Z_DIM = 32
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # 初始化 DisCoRL
    discorl = DisCoRL(STATE_DIM, ACTION_DIM, NUM_TASKS, Z_DIM, device)
    
    print(f"DisCoRL 初始化完成!")
    print(f"状态维度：{STATE_DIM}")
    print(f"动作维度：{ACTION_DIM}")
    print(f"任务数量：{NUM_TASKS}")
    print(f"隐空间维度：{Z_DIM}")
    print(f"设备：{device}")
    
    # 模拟训练数据
    print("\n开始训练教师策略...")
    for task_id in range(NUM_TASKS):
        # 生成模拟轨迹
        trajectories = []
        for _ in range(100):
            state = np.random.randn(STATE_DIM)
            action = np.random.randint(ACTION_DIM)
            trajectories.append((state, action))
        
        # 训练教师
        losses = discorl.train_teacher_for_task(task_id, trajectories, num_epochs=50)
        print(f"  Task {task_id}: 最终损失 = {losses[-1]:.4f}")
    
    # 创建蒸馏回放缓冲区
    replay_buffer = []
    for task_id in range(NUM_TASKS):
        for _ in range(50):
            state = np.random.randn(STATE_DIM)
            action = np.random.randint(ACTION_DIM)
            replay_buffer.append((state, task_id, action))
    
    # 蒸馏到学生
    print("\n蒸馏到学生策略...")
    distill_losses = discorl.distill_all_teachers(replay_buffer, num_epochs=50)
    print(f"最终蒸馏损失：{distill_losses[-1]:.4f}")
    
    # 测试
    print("\n测试模型...")
    test_state = np.random.randn(STATE_DIM)
    
    # 已知任务 ID
    action_known = discorl.get_action(test_state, task_id=0)
    print(f"已知任务 (task=0): action={action_known}")
    
    # 自动推断任务
    inferred_task = discorl.infer_task(test_state)
    action_inferred = discorl.get_action(test_state, task_id=None)
    print(f"推断任务：task={inferred_task}, action={action_inferred}")
    
    print("\n✅ DisCoRL 实现完成!")
