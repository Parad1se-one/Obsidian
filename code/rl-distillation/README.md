# DisCoRL 知识蒸馏项目

**基于 DisCoRL 论文的策略蒸馏实现**

---

## 📚 项目概述

本项目实现论文 **DisCoRL: Continual Reinforcement Learning via Policy Distillation** (arXiv:1907.05855) 的核心算法，并扩展用于知识蒸馏到特定 RL 问题。

**核心思想:** 用大模型 (教师) 蒸馏到小模型 (学生)，实现模型压缩和多任务学习。

---

## 📁 目录结构

```
code/rl-distillation/
├── discorl.py              # DisCoRL 核心实现
├── requirements.txt        # Python 依赖
├── README.md              # 本文件
└── experiments/           # 实验脚本 (待创建)
    ├── cartpole_distill.py
    └── pendulum_distill.py
```

---

## 🚀 快速开始

### 安装依赖

```bash
cd code/rl-distillation
pip install -r requirements.txt
```

### 运行示例

```bash
python discorl.py
```

输出示例:
```
DisCoRL 初始化完成!
状态维度：4
动作维度：4
任务数量：3
隐空间维度：32
设备：cpu

开始训练教师策略...
  Task 0: 最终损失 = 0.1234
  Task 1: 最终损失 = 0.1456
  Task 2: 最终损失 = 0.1389

蒸馏到学生策略...
最终蒸馏损失：0.0892

测试模型...
已知任务 (task=0): action=2
推断任务：task=1, action=3

✅ DisCoRL 实现完成!
```

---

## 🏗️ 架构说明

### 核心组件

| 组件 | 作用 |
|------|------|
| `StateEncoder` | 状态编码器 - 学习低维状态表示 z |
| `TaskInference` | 任务推断 - 基于 z 自动识别任务 |
| `TeacherPolicies` | 教师策略集合 - 每个任务一个 |
| `StudentPolicy` | 学生策略 - 通过蒸馏学习 |
| `DisCoRL` | 主框架 - 协调所有组件 |

### 训练流程

```
1. 训练状态编码器
   ↓
2. 顺序训练每个任务的教师策略
   ↓
3. 收集教师策略的轨迹
   ↓
4. 蒸馏到学生策略 (KL 散度最小化)
   ↓
5. 训练任务推断网络
```

---

## 📊 蒸馏场景

### 场景 1: DQN 压缩 (推荐入门)

```python
# 教师：大 DQN
teacher_config = {
    'layers': [512, 512, 256],
    'action_dim': 2  # CartPole: left/right
}

# 学生：小 DQN
student_config = {
    'layers': [64, 64],
    'action_dim': 2
}

# 目标：压缩 10x, 性能保持 90%+
```

### 场景 2: SAC 策略蒸馏 (连续控制)

```python
# 教师：大 SAC (Pendulum)
teacher_config = {
    'layers': [400, 300],
    'action_dim': 1  # torque
}

# 学生：小 SAC
student_config = {
    'layers': [128, 128],
    'action_dim': 1
}
```

### 场景 3: 多任务蒸馏

```python
# 多个任务特定教师
teachers = [policy_cartpole, policy_pendulum, ...]

# 单一通用学生
student = universal_policy(task_embedding)
```

---

## 🎯 评估指标

| 指标 | 计算方法 | 目标 |
|------|----------|------|
| 模型大小压缩 | teacher_size / student_size | 5-10x |
| 推理速度提升 | teacher_time / student_time | 3-5x |
| 性能保持 | student_reward / teacher_reward | ≥90% |
| 训练时间减少 | student_train_time / teacher_train_time | ≥50% |

---

## 📝 下一步

### 待创建文件

1. `experiments/cartpole_distill.py` - CartPole 蒸馏实验
2. `experiments/pendulum_distill.py` - Pendulum 蒸馏实验
3. `utils/visualization.py` - 结果可视化
4. `configs/` - 实验配置文件

### 待办事项

- [ ] 安装 PyTorch 依赖
- [ ] 运行 CartPole 实验
- [ ] 记录压缩率 vs 性能曲线
- [ ] 与端到端训练对比
- [ ] 撰写技术报告

---

## 📄 论文参考

**DisCoRL: Continual Reinforcement Learning via Policy Distillation**

- **arXiv:** 1907.05855
- **PDF:** https://arxiv.org/pdf/1907.05855.pdf
- **笔记:** ../../knowledge/rl/papers/discorl-2019-notes.md

---

## 🦐 小虾注释

**当前状态:** 核心实现完成，待安装依赖并运行实验

**推荐起点:** CartPole-v1 环境 - 简单、快速、易验证

**关键问题:** 用户想蒸馏到哪个"特定问题"? 需要进一步讨论。

---

**最后更新:** 2026-03-05 23:59
**实现者:** 小虾 🦐
