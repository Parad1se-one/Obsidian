# MuZero 论文笔记

**学习时间:** 2026-03-05 21:50-22:00
**主题:** MuZero (DeepMind, Nature 2019)

---

## 基本信息
- **标题:** Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model
- **作者:** Schrittwieser et al. (DeepMind)
- **Venue:** Nature 2019
- **链接:** https://www.nature.com/articles/s41586-020-03051-4

---

## 核心贡献

**首个在不知道环境规则的情况下，通过规划达到 SOTA 的算法**

| 环境 | 结果 |
|------|------|
| Atari 57 游戏 | 超越 AlphaGo Zero |
| Go | 达到 AlphaGo Zero 水平 |
| Chess | 达到 AlphaZero 水平 |
| Shogi | 达到 AlphaZero 水平 |

---

## 关键创新

### 1. 潜空间规划
- 不在原始状态空间规划
- 学习潜空间表示 + 动态
- 在潜空间中运行 MCTS

### 2. 三个组件

```
Representation: s → h (初始隐藏状态)
Dynamics:       h, a → h', r (预测下一状态和奖励)
Prediction:     h → p, v (策略和价值)
```

---

## 算法架构

### 网络结构

```
观察 o_t
  ↓
Representation Network
  ↓
隐藏状态 h_t
  ↓
┌──────────────────────────┐
│  Dynamics (递归展开)     │
│  h_t, a_t → h_{t+1}, r_t │
└──────────────────────────┘
  ↓
Prediction Network
  ↓
策略 p_t, 价值 v_t
```

---

### MCTS 在潜空间

```python
# MuZero MCTS 伪代码

def mcts_search(h_state, n_simulations):
    tree = Tree()
    
    for _ in range(n_simulations):
        # 1. Selection - 选择叶子节点
        node = tree.select()
        
        # 2. Expansion - 展开
        p, v = prediction_network(node.hidden_state)
        node.expand(p)
        
        # 3. Backup - 回溯更新
        node.backup(v)
    
    # 返回最佳动作
    return tree.best_action()
```

---

## 训练流程

### 1. 自我对弈
- 使用当前最佳策略玩游戏
- 存储 (观察，策略，价值) 轨迹

### 2. 训练
- **表示损失:** 隐藏状态重建
- **动态损失:** 预测 r 和 h' 准确
- **预测损失:** p 和 v 准确

### 3. 重放
- 从旧策略重新评估动作
- 提高数据效率

---

## 与 AlphaZero 对比

| 特性 | AlphaZero | MuZero |
|------|-----------|--------|
| 环境模型 | 已知 (游戏规则) | 学习 |
| 规划空间 | 原始状态 | 潜空间 |
| 适用范围 | 完全信息游戏 | 通用 (包括 Atari) |
| 样本效率 | 高 | 更高 |

---

## 关键公式

### 损失函数
$$l = l_p + l_v + l_r$$

- $l_p$: 策略损失 (交叉熵)
- $l_v$: 价值损失 (MSE)
- $l_r$: 奖励损失 (MSE)

### 动态函数
$$h_{t+1}, r_t = \text{dynamics}(h_t, a_t)$$

---

## 实验结果

### Atari
- 57 个游戏
- 超越 AlphaGo Zero (使用真实环境)
- 样本效率提升

### 棋盘游戏
- Go, Chess, Shogi
- 达到 AlphaZero 水平
- 无需知道规则

---

## 代码要点

```python
class MuZero:
    def __init__(self):
        self.representation = RepNetwork()
        self.dynamics = DynamicsNetwork()
        self.prediction = PredictionNetwork()
    
    def represent(self, observation):
        return self.representation(observation)
    
    def dynamics(self, hidden_state, action):
        return self.dynamics(hidden_state, action)
    
    def predict(self, hidden_state):
        return self.prediction(hidden_state)
    
    def mcts_search(self, hidden_state):
        # 在潜空间运行 MCTS
        pass
    
    def train(self, batch):
        # 计算三种损失
        loss_rep = ...
        loss_dyn = ...
        loss_pred = ...
        return loss_rep + loss_dyn + loss_pred
```

---

## 启发

1. **潜空间规划** - 比原始空间更高效
2. **学习模型 + 规划** - 结合两者优势
3. **通用框架** - 适用于多种环境

---

*学习时间：2026-03-05 21:50-22:00 | 小虾 🦐*
