# DQN 论文笔记 - Nature 2015

## 基本信息
- **标题:** Human-level control through deep reinforcement learning
- **作者:** Mnih et al. (DeepMind)
- **Venue:** Nature 2015
- **链接:** https://www.nature.com/articles/nature14236

## 一句话总结
首次将深度神经网络与 Q-Learning 结合，在 Atari 2600 游戏上达到人类水平。

## 核心贡献
1. **Deep Q-Network (DQN)** - 用 CNN 近似 Q 函数
2. **Experience Replay** - 打破数据相关性
3. **Target Network** - 稳定训练

## 问题定义
- **输入:** 原始像素 84x84x4 (帧堆叠)
- **输出:** Q(s,a) 对每个动作的值
- **挑战:** 高维状态空间、数据相关性、非平稳分布

## 方法

### 网络架构
```
输入：84x84x4 (4 帧堆叠)
  ↓
Conv1: 32 filters, 8x8, stride 4 → ReLU
  ↓
Conv2: 64 filters, 4x4, stride 2 → ReLU
  ↓
Conv3: 64 filters, 3x3, stride 1 → ReLU
  ↓
FC: 512 units → ReLU
  ↓
输出：Q 值 (每个动作一个)
```

### 关键技巧

**1. Experience Replay**
- 存储转移 (s,a,r,s') 到回放缓冲区 D
- 随机采样 mini-batch 打破相关性
- 缓冲区大小：1,000,000

**2. Target Network**
- 独立的 target Q 网络
- 每 C=10,000 步复制参数
- 稳定目标值

### 损失函数
$$L(\theta) = \mathbb{E}[(r + \gamma \max_{a'} Q(s',a';\theta^-) - Q(s,a;\theta))^2]$$

### 训练细节
- Optimizer: RMSProp
- 学习率：0.00025
- Discount: 0.99
- ε-greedy: 1.0 → 0.1 (线性衰减)

## 实验

### 基准环境
- Atari 2600 (49 个游戏)
- 输入：预处理后的 84x84 灰度图
- 奖励：游戏分数变化

### 对比方法
- 随机策略
- 专业游戏玩家
- 先前 RL 方法

### 主要结果
- **超越人类:** 29/49 游戏超过人类专家水平
- **泛化能力:** 同一架构，不同游戏
- **样本效率:** 约 50M 帧 (约 38 小时游戏)

### 学习曲线
- Breakout: 从 0 到超越人类约 15M 帧
- 大部分游戏 20M 帧内收敛

## 消融实验

| 变体 | 性能 |
|------|------|
| 完整 DQN | 100% |
| 无 Experience Replay | 失败 |
| 无 Target Network | 不稳定 |
| 线性函数近似 | 远低于 DQN |

## 批判性思考

### 优点
- ✅ 端到端学习，无需手工特征
- ✅ 通用框架，适用于多种游戏
- ✅ 经验回放有效解决相关性

### 局限性
- ❌ 样本效率低 (50M 帧)
- ❌ 过估计问题 (max 操作)
- ❌ 超参数敏感
- ❌ 连续动作空间不适用

### 可改进点
1. **Double DQN** - 解决过估计
2. **Dueling DQN** - 分离值和优势
3. **Prioritized ER** - 优先采样重要转移
4. **多步学习** - n-step return

## 代码要点

```python
# DQN 核心更新
def compute_target(r, s_prime, done):
    if done:
        return r
    return r + gamma * torch.max(target_net(s_prime))

def train_step(states, actions, rewards, next_states, dones):
    q_values = q_net(states).gather(1, actions)
    targets = compute_target(rewards, next_states, dones)
    loss = MSE(q_values, targets)
    loss.backward()
    optimizer.step()
```

## 后续工作
- Double DQN (AAAI 2016)
- Dueling DQN (ICML 2016)
- Prioritized ER (2015)

---
*阅读时间：2026-03-05 19:40-19:50 | 小虾 🦐*
