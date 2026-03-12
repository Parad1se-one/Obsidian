# DRAMA 代码架构详解

> 🏗️ 核心模块设计与数据流

---

## 📦 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                      Training Scripts                        │
│  train_mappo_easy_rm.py | train_mappo_baseline_v2.py | ...  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       MARL Library                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   trainer.py │  │   buffer.py  │  │   mixer.py   │      │
│  │  (训练循环)  │  │ (经验回放池) │  │ (值分解网络) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                              │                               │
│  ┌──────────────────────────────────────────────────┐       │
│  │                    algos/                        │       │
│  │  mappo.py | ippo.py | qmix.py | dqn_vdn.py | ... │       │
│  └──────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Environment (envs/)                       │
│                     grid_env.py                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  State: robots, floors, obstacles, task_progress    │    │
│  │  Actions: UP/DOWN/LEFT/RIGHT/PERFORM/STAY           │    │
│  │  Rewards: task + collaboration + progress + efficiency│   │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Configs (configs/)                         │
│  env_config.py | difficulty_loader.py | algo_config.py      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 核心模块详解

### 1. 训练脚本层 (`*.py`)

**职责**: 实验配置、训练启动、日志记录

#### 关键文件
- `train_mappo_easy_rm.py` - MAPPO + Reward Machine
- `train_mappo_easy_baseline_v2.py` - MAPPO Baseline (无 RM)
- `train_qmix_easy.py` - QMIX 算法
- `evaluate.py` - 模型评估

#### 典型流程
```python
# 1. 加载配置
config = load_config('easy')

# 2. 初始化环境
env = GridAreaEnv(config)

# 3. 初始化算法
agent = MAPPO(config)

# 4. 训练循环
for episode in range(num_episodes):
    obs = env.reset()
    for step in range(max_steps):
        actions = agent.select_action(obs)
        next_obs, rewards, dones, info = env.step(actions)
        buffer.store(obs, actions, rewards, next_obs, dones)
        agent.update(buffer)
        obs = next_obs
```

---

### 2. MARL 核心库 (`marl/`)

#### 2.1 `agents.py` - 神经网络模型

**核心类**:
- `RecurrentMAPPOActor` - 带 GRU 的 Actor 网络
- `MAPPOActor` - 标准 Actor 网络
- `MAPPOCritic` - Critic 网络
- `QTRANAgent` - QTRAN 网络

**网络结构**:
```
Actor:
  obs_dim → Linear(64) → ReLU → GRU → Linear → action_dim

Critic:
  state_dim → Linear(256) → ReLU → Linear(256) → ReLU → Linear → 1
```

#### 2.2 `trainer.py` - 训练循环

**职责**:
- 数据收集 (rollout)
- 批量采样 (batch sampling)
- 损失计算 (loss computation)
- 反向传播 (backpropagation)

**关键方法**:
```python
class Trainer:
    def collect_rollouts():      # 收集轨迹
    def update_policy():         # 更新策略
    def compute_advantage():     # 计算 GAE 优势
    def save_checkpoint():       # 保存模型
```

#### 2.3 `buffer.py` - 经验回放池

**存储内容**:
- observations, actions, rewards
- next_observations, dones, masks
- hidden_states (for RNN)

**操作**:
```python
buffer = ReplayBuffer(capacity=50000)
buffer.store(obs, action, reward, next_obs, done)
batch = buffer.sample(batch_size=64)
```

#### 2.4 `mixer.py` - 值分解网络

**支持算法**:
- VDN: 简单求和
- QMIX: 单调混合网络

**QMIX 结构**:
```
Q_total = Mixer(Q1, Q2, ..., Qn, state)
∂Q_total/∂Q_i ≥ 0  (单调性约束)
```

---

### 3. 算法实现 (`marl/algos/`)

#### 3.1 MAPPO (`mappo.py`)

**核心思想**: 集中式训练，分布式执行

```python
class MAPPO:
    def __init__(self):
        self.actor = Actor(obs_dim, action_dim)
        self.critic = Critic(state_dim)
    
    def update(self, batch):
        # 计算优势函数 (GAE)
        advantages = self.compute_gae(batch)
        
        # PPO-Clip 损失
        ratio = new_prob / old_prob
        surr1 = ratio * advantages
        surr2 = clip(ratio, 1-ε, 1+ε) * advantages
        policy_loss = -min(surr1, surr2).mean()
        
        # Critic 损失
        value_loss = (returns - values).pow(2).mean()
```

#### 3.2 IPPO (`ippo.py`)

**特点**: 独立学习，无集中式 Critic

```python
# 每个智能体独立更新
for agent in agents:
    agent.update(local_obs, local_action, reward)
```

#### 3.3 QMIX (`qmix.py`)

**核心**: 单调值分解

```python
# 混合网络
Q_total = self.hypernet(Q_individuals, state)

# 单调性约束
self.hypernet.weights = abs(self.hypernet.weights)
```

---

### 4. 环境层 (`envs/grid_env.py`)

#### 4.1 状态表示

```python
class GridAreaEnv:
    # 静态元素
    - passable_map: 可通行性地图
    - obstacles: 障碍物位置
    
    # 动态元素
    - robots: 机器人位置和状态
    - floors_to_*: 各阶段任务地图
    - task_progress: 任务进度追踪
```

#### 4.2 动作空间

```python
ACTION_STR = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT",
    4: "PERFORM",  # 执行施工动作
    5: "STAY"
}
```

#### 4.3 Reward Machine 设计

**任务阶段 DAG**:
```
distribute_wall → vibrate_wall
       ↓
distribute_floor → vibrate_floor → level_floor → cover_surface
```

**奖励组成**:
```python
reward = (
    task_completion * 10.0 +    # 任务完成
    collaboration * 5.0 +       # 协作奖励
    progress * 2.0 +            # 进度奖励
    efficiency * 1.0            # 效率奖励
)
```

**RM 状态转换**:
```python
def rm_transition(state, event):
    if state == "distribute" and event == "all_distributed":
        return "vibrate"
    elif state == "vibrate" and event == "all_vibrated":
        return "level"
    # ...
```

---

### 5. 配置层 (`configs/`)

#### 5.1 环境配置

```python
# env_config.py
env_config = {
    "grid_width": 6,
    "grid_height": 6,
    "robots": {...},
    "floors": {...},
    "task_dependencies": {...}
}
```

#### 5.2 难度配置

```python
# difficulty/easy_config.py
easy_config = {
    "grid_size": (6, 6),
    "construction_units": 2,
    "obstacles": 0,
    "complexity": "low"
}
```

---

## 🔄 数据流详解

### 训练流程

```
1. 环境初始化
   env = GridAreaEnv(config)
   
2. 重置环境
   obs = env.reset()
   # → 返回：(num_agents, obs_dim)
   
3. 选择动作
   actions = agent.select_action(obs)
   # → 返回：(num_agents,)
   
4. 执行动作
   next_obs, rewards, dones, info = env.step(actions)
   # → rewards: (num_agents,)
   # → info: {'task_progress': ..., 'rm_state': ...}
   
5. 存储经验
   buffer.store(obs, actions, rewards, next_obs, dones)
   
6. 更新策略
   for _ in range(update_epochs):
       batch = buffer.sample(batch_size)
       agent.update(batch)
```

### Reward Machine 集成

```
每个 timestep:
  1. 环境返回原始奖励 r_env
  2. RM 根据当前状态和事件计算 r_rm
  3. 总奖励 r = r_env + λ * r_rm
  4. RM 状态转换: state' = δ(state, event)
  5. 智能体观察到 r 和 state'
```

---

## 📊 关键设计模式

### 1. 集中式 Critic

```python
# Actor: 局部观测
action_prob = actor(local_obs)

# Critic: 全局状态
value = critic(global_state)
```

### 2. Recurrent Policy

```python
# GRU 处理序列数据
logits, h_new = gru(obs_sequence, h_prev, masks)
```

### 3. Parameter Sharing

```python
# 所有智能体共享同一个 Actor 网络
# 通过 agent_id 区分
```

---

## 🎯 扩展指南

### 添加新算法

1. 在 `marl/algos/` 创建 `new_algo.py`
2. 实现 `select_action()` 和 `update()` 方法
3. 在训练脚本中导入并使用

### 修改环境

1. 编辑 `envs/grid_env.py`
2. 修改 `step()` 中的奖励逻辑
3. 更新 `configs/env_config.py`

### 添加新难度

1. 在 `configs/difficulty/` 创建 `new_config.py`
2. 定义网格大小、任务复杂度等
3. 在 `difficulty_loader.py` 中注册

---

*最后更新：2026-03-12 | 维护者：小虾 🦐*
