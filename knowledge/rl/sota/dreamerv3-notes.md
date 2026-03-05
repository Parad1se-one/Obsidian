# DreamerV3 论文笔记

**学习时间:** 2026-03-05 21:44-21:54
**主题:** DreamerV3 (ICLR 2024)

---

## 基本信息
- **标题:** Mastering Diverse Domains through World Models
- **作者:** Hafner et al. (DeepMind)
- **Venue:** ICLR 2024
- **链接:** https://arxiv.org/abs/2301.04104

---

## 核心贡献

**单一 agent 在 20+ 不同领域达到 SOTA**

| 领域 | 环境数 | 结果 |
|------|--------|------|
| Atari | 50+ | SOTA |
| DeepMind Control | 30+ | SOTA |
| Minecraft | - | 复杂任务 |
| 机器人控制 | - | 真实世界 |

---

## 关键创新

### 1. 端到端世界模型
- 直接从像素学习潜空间动态
- 无需三阶段分离训练
- 更稳定，更易用

### 2. Actor-Critic 在潜空间
- 在世界模型生成的 trajectories 上训练
- 无需真实环境交互
- 样本效率极高

### 3. 归一化技巧
- 输入归一化
- 奖励缩放
- 潜空间标准化

---

## 模型架构

### World Model

```
输入：图像 (64x64x3)
  ↓
CNN Encoder
  ↓
潜状态 z_t
  ↓
RSSM (Recurrent State Space Model)
  ↓
预测：z_{t+1}, reward, done
  ↓
CNN Decoder → 重建图像
```

### RSSM 组件

- **Deterministic state:** h_t (RNN hidden)
- **Stochastic state:** z_t (latent)
- **Transition:** p(z_t | h_t, z_{t-1})

---

### Actor-Critic

```
输入：潜状态 [h_t, z_t]
  ↓
MLP Actor → 动作分布
  ↓
MLP Critic → 值估计
```

---

## 训练流程

### 1. 收集数据
- 用当前 policy 与环境交互
- 存储 (s, a, r, s') 轨迹

### 2. 训练 World Model
- 重建损失：图像重建
- 动态损失：预测准确
- KL 正则：潜空间正则化

### 3. 训练 Actor-Critic
- 在世界模型中"想象"trajectories
- 计算 returns
- 更新 policy 和 value

---

## 与 DreamerV2 对比

| 特性 | V2 | V3 |
|------|----|----|
| 归一化 | 部分 | 全面 |
| 网络大小 | 小 | 大 |
| 训练稳定 | 好 | 更好 |
| 通用性 | 好 | 极好 |

---

## 关键代码结构

```python
class DreamerV3:
    def __init__(self):
        self.world_model = WorldModel()
        self.actor = Actor()
        self.critic = Critic()
    
    def train_step(self, batch):
        # 1. 训练 World Model
        model_loss = self.train_world_model(batch)
        
        # 2. 在潜空间想象
        imagined_traj = self.world_model.imagine()
        
        # 3. 训练 Actor
        actor_loss = self.train_actor(imagined_traj)
        
        # 4. 训练 Critic
        critic_loss = self.train_critic(imagined_traj)
        
        return model_loss, actor_loss, critic_loss
```

---

## 实验结果

### Atari 100k (100k 步)
- 50+ 游戏
- 中位人类归一化分数：>1.0
- 超越所有 baseline

### DeepMind Control
- 30+ 连续控制任务
- 样本效率提升 2-10x

### Minecraft
- 完成复杂任务链
- 钻石采集等

---

## 启发

1. **端到端训练** - 简化流程，提高稳定性
2. **潜空间规划** - 通用且高效
3. **单一 agent** - 无需针对环境调参

---

*学习时间：2026-03-05 21:44-21:54 | 小虾 🦐*
