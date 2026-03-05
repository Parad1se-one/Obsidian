# Double DQN 论文笔记 - AAAI 2016

## 基本信息
- **标题:** Deep Reinforcement Learning with Double Q-learning
- **作者:** Hado van Hasselt et al. (DeepMind)
- **Venue:** AAAI 2016
- **链接:** https://arxiv.org/abs/1509.06461

## 一句话总结
解决 DQN 的过估计问题，通过使用两个 Q 网络解耦动作选择和评估。

## 核心问题：过估计 (Overestimation)

### 问题来源
标准 Q-Learning 更新：
$$Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$$

**问题:** $\max$ 操作倾向于选择高估的值

### 为什么过估计有害？
- 导致次优策略
- 训练不稳定
- 在某些环境中性能显著下降

## 方法：Double Q-Learning

### 核心思想
**解耦动作选择和价值评估:**
- 用 Q_A 选择动作：$a^* = \arg\max_a Q_A(s',a)$
- 用 Q_B 评估价值：$Q_B(s', a^*)$

### Double DQN 更新
$$Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma Q'(s', \arg\max_{a'} Q(s',a'; \theta)) - Q(s,a)]$$

**关键:** 用 online network 选择动作，用 target network 评估

### 与 DQN 对比

| 方法 | Target 计算 |
|------|------------|
| DQN | $r + \gamma \max_{a'} Q'(s',a')$ |
| Double DQN | $r + \gamma Q'(s', \arg\max_{a'} Q(s',a'))$ |

## 实验

### 环境
- Atari 2600 (57 个游戏)
- 相同超参数对比

### 主要结果

| 指标 | DQN | Double DQN | 提升 |
|------|-----|------------|------|
| 平均人类归一化 | 1022% | 1378% | +35% |
| 中位数人类归一化 | 530% | 656% | +24% |

### 过估计分析

**DQN:**
- 平均过估计：约 50%
- 某些游戏高达 200%

**Double DQN:**
- 平均过估计：约 10%
- 显著降低

### 学习曲线对比
- Space Invaders: Double DQN 最终性能 +50%
- Seaquest: 收敛更快，最终性能 +30%

## 代码实现

```python
# DQN target
def dqn_target(reward, next_state, done, target_net):
    if done:
        return reward
    return reward + gamma * torch.max(target_net(next_state))

# Double DQN target
def double_dqn_target(reward, next_state, done, online_net, target_net):
    if done:
        return reward
    # Online net 选择动作
    next_action = online_net(next_state).argmax(dim=1, keepdim=True)
    # Target net 评估价值
    next_q = target_net(next_state).gather(1, next_action)
    return reward + gamma * next_q
```

## 批判性思考

### 优点
- ✅ 简单有效，只需改一行代码
- ✅ 显著降低过估计
- ✅ 性能稳定提升
- ✅ 无需额外超参数

### 局限性
- ❌ 仍然使用 target network
- ❌ 没有解决样本效率问题

### 与 Prioritized ER 结合
- Double DQN + PER = 更强
- 两者正交，可以叠加

## 启发

**解耦思想可以应用到其他地方:**
- 策略选择 vs 策略评估
- 探索 vs 利用
- 模型学习 vs 规划

---
*阅读时间：2026-03-05 19:50-20:00 | 小虾 🦐*
