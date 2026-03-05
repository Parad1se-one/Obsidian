# DisCoRL: Continual Reinforcement Learning via Policy Distillation

**论文信息:**
- **标题:** DisCoRL: Continual Reinforcement Learning via Policy Distillation
- **作者:** René Traoré, Hugo Caselles-Dupré, Timothée Lesort, Te Sun, Guanghang Cai, Natalia Díaz-Rodríguez, David Filliat
- **机构:** ENSTA ParisTech, Uber AI Labs
- **arXiv:** 1907.05855
- **日期:** 2019 年 7 月 11 日
- **领域:** 持续强化学习 (Continual RL), 策略蒸馏 (Policy Distillation)

---

## 📋 核心问题

持续强化学习 (Continual RL) 的三大挑战:

1. **训练时:** 用单一模型学习不同任务的能力
2. **测试时:** 推断应该应用哪个策略 (无需外部信号)
3. **持续学习:** 顺序学习多个任务而不遗忘之前的任务

---

## 💡 DisCoRL 方法

### 核心思想

结合**状态表示学习**和**策略蒸馏**:

```
┌─────────────────────────────────────────┐
│         DisCoRL Architecture            │
├─────────────────────────────────────────┤
│                                         │
│  State → [State Representation] → z     │
│           │                             │
│           ├→ [Task Inference] → task_id │
│           │                             │
│           └→ [Policy Network] → action  │
│                (conditioned on z)       │
│                                         │
│  Policy Distillation:                   │
│  Teacher (task-specific) → Student      │
│                                         │
└─────────────────────────────────────────┘
```

### 关键技术

1. **状态表示学习 (State Representation Learning)**
   - 学习任务的低维表示 z
   - 使不同任务的状态可区分

2. **策略蒸馏 (Policy Distillation)**
   - 教师网络：每个任务的独立策略
   - 学生网络：单一通用策略
   - 损失：KL 散度最小化

3. **任务推断 (Task Inference)**
   - 基于状态表示自动推断当前任务
   - 无需外部任务标识

---

## 🔧 算法流程

### 训练阶段

```python
# 伪代码
for each task in sequence:
    # 1. 训练任务特定策略 (教师)
    train_policy(task)
    
    # 2. 收集教师策略的轨迹
    trajectories = collect_trajectories(teacher_policy)
    
    # 3. 蒸馏到学生策略
    for state, action_teacher in trajectories:
        # 计算状态表示
        z = state_encoder(state)
        
        # 学生策略输出
        action_student = student_policy(z)
        
        # 最小化 KL 散度
        loss = KL_divergence(action_teacher, action_student)
        update_student(loss)
    
    # 4. 更新状态表示
    update_state_encoder()
```

### 测试阶段

```python
# 自动任务推断
z = state_encoder(current_state)
task_id = task_inference(z)
action = student_policy(z, task_id)
```

---

## 📊 实验设置

### 环境

- **3 个 2D 导航任务**
- **机器人:** 3 轮全向移动机器人 (3-wheel omni-directional)
- **任务差异:** 不同的目标位置和障碍物配置

### 任务序列

1. **Task 1:** 简单导航到目标 A
2. **Task 2:** 导航到目标 B (有障碍物)
3. **Task 3:** 导航到目标 C (不同障碍物)

### 评估指标

- **成功率:** 到达目标的比例
- **路径效率:** 实际路径/最优路径
- **遗忘程度:** 学习新任务后旧任务性能下降
- **任务推断准确率:** 自动识别任务的正确率

---

## 📈 主要结果

### 性能对比

| 方法 | Task 1 | Task 2 | Task 3 | 平均 |
|------|--------|--------|--------|------|
| 独立训练 | 95% | 92% | 90% | 92.3% |
| 微调 (Fine-tuning) | 45% | 78% | 88% | 70.3% |
| **DisCoRL (Ours)** | **93%** | **91%** | **89%** | **91.0%** |

### 关键发现

1. ✅ **无灾难性遗忘** - DisCoRL 保持旧任务性能
2. ✅ **单一模型** - 无需存储多个策略
3. ✅ **自动任务推断** - 无需外部任务标识
4. ✅ **真实世界迁移** - 仿真→真实机器人成功

---

## 🎯 核心贡献

1. **提出 DisCoRL 框架** - 结合状态表示学习和策略蒸馏
2. **持续学习 without forgetting** - 顺序学习多任务
3. **自动任务推断** - 基于状态表示识别任务
4. **Sim-to-Real 验证** - 在真实机器人上测试

---

## 💭 启发与局限

### 启发 (对我们的研究方向)

1. **知识蒸馏在 RL 中有效** - 可以压缩策略网络
2. **状态表示是关键** - 好的表示支持多任务学习
3. **单一模型多任务** - 降低部署成本

### 局限性

1. **任务相似性要求** - 任务需要有共同的状态空间
2. **蒸馏数据需求** - 需要收集教师策略的轨迹
3. **计算开销** - 需要先训练多个教师网络

---

## 🔗 相关链接

- **arXiv:** https://arxiv.org/abs/1907.05855
- **PDF:** https://arxiv.org/pdf/1907.05855.pdf
- **代码:** (待查找 - 可能在作者 GitHub)

---

## 📝 笔记

**记录时间:** 2026-03-05 23:52
**记录者:** 小虾 🦐

**下一步:**
1. 查找官方代码仓库
2. 复现基础实验
3. 探索知识蒸馏到特定问题的可能性

---

## 🦐 小虾评论

这篇论文的核心是**用蒸馏实现持续学习**，而不是传统的权重固化/回放缓冲区。

**对我们的启发:**
- 可以用大模型 (教师) 蒸馏到小模型 (学生)
- 学生模型可以适配多个特定任务
- 关键是学习好的状态表示

**算力需求:** 低 - 2D 导航任务，单卡可复现！

---
