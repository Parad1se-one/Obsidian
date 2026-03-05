# DiscoRL: Discovering State-of-the-art Reinforcement Learning Algorithms

## 博士研究生学术报告

**论文来源**: Nature (2025), DOI: 10.1038/s41586-025-09761-x  
**团队**: Google DeepMind (Junhyuk Oh, Iurii Kemaev, Greg Farquhar, David Silver 等)  
**报告人**: [Your Name]  
**日期**: 2026 年 3 月

---

# 目录

1. 研究背景与动机
2. 核心问题定义
3. 方法概述：DiscoRL 框架
4. 技术架构详解
5. 元学习优化过程
6. 实验设计与基准
7. 主要实验结果
8. 零样本泛化能力
9. 发现的新语义分析
10. 可扩展性研究
11. 创新点与贡献
12. 局限性与未来方向
13. 总结

---

# 1. 研究背景与动机

## 强化学习的成功与局限

**RL 的里程碑成就**:
- 🎮 复杂博弈游戏：Go、国际象棋、StarCraft、Minecraft
- 🔬 新数学工具发明
- 🤖 复杂物理系统控制

**核心问题**:
> "Unlike humans, whose learning mechanism has been naturally discovered by biological evolution, RL algorithms are typically manually designed."

**手工设计算法的局限**:
- 缓慢且劳动密集
- 受限于人类知识和直觉
- 难以探索更大的算法空间

---

# 2. 核心问题定义

## 研究目标

**核心问题**: 能否通过自动化方法发现超越手工设计的 RL 算法？

**关键挑战**:
1. **搜索空间狭窄**: 现有工作仅在超参数、策略损失等有限空间搜索
2. **环境简单**:  prior work 集中在 grid-worlds 等简单环境
3. **泛化能力不足**: 发现的规则难以迁移到未见环境

**DiscoRL 的突破**:
- ✅ 探索更表达性的 RL 规则空间
- ✅ 在复杂多样环境中大规模元学习
- ✅ 实现零样本泛化到全新领域

---

# 3. 方法概述：DiscoRL 框架

## 核心思想

**传统 RL**: 手工设计更新规则（数学方程）
```
Loss = (target - prediction)²  # 例如 TD 误差
```

**DiscoRL**: 用神经网络表示更新规则
```
Meta-Network(trajectory) → targets
```

## 发现过程

```
┌─────────────────────────────────────────────────┐
│  种群：数百个并行 Agent                          │
│  ↓ 与环境交互                                    │
│  ↓ 使用共享 Meta-Network 更新                    │
│  ↓ 计算 Meta-Gradient                           │
│  ↓ 优化 Meta-Network                            │
└─────────────────────────────────────────────────┘
           ↓
    发现更强的 RL 规则
```

---

# 4. 技术架构详解

## Agent 架构

```
Agent Network (θ):
├── π(s)              : 策略 (Policy)
├── y(s) ∈ ℝⁿ         : 状态条件预测向量 (待发现语义)
├── z(s,a) ∈ ℝᵐ       : 动作条件预测向量 (待发现语义)
├── q(s,a)            : 动作价值函数 (预定义语义)
└── p(s,a)            : 辅助策略预测 (预定义语义)
```

**设计原理**:
- y 和 z 的语义由 Meta-Network 决定，无预定义
- 保留 q 和 p 鼓励发现**新概念**而非重新发现已知规则
- 函数形式足够通用，可表示但不局限于现有 RL 概念

---

# 5. Meta-Network 架构

## 核心组件

```
输入 (时间步 t → t+n):
├── Agent 预测轨迹：π, y, z
├── 环境奖励：r_t, r_{t+1}, ...
└── 回合终止信号

↓ LSTM 处理

输出:
├── π̂ : 策略目标
├── ŷ : y 预测目标
└── ẑ : z 预测目标
```

## 关键设计特性

| 特性 | 说明 |
|------|------|
| **观测无关** | 不直接接收观测，通过预测间接处理 → 可泛化到不同观测空间 |
| **动作空间无关** | 在动作维度共享权重 → 可泛化到不同动作空间 |
| **Agent 架构无关** | 只看 Agent 输出 → 可迁移到不同网络架构 |
| **支持 Bootstrap** | 搜索空间包含自举方法 |
| **联合处理** | 同时处理策略和预测 → 可发现方差缩减等高级技术 |

---

# 6. 优化过程

## Agent 优化

**损失函数**:
```
L(θ) = E[D(π̂, π_θ) + D(ŷ, y_θ) + D(ẑ, z_θ)] + L_aux

其中:
- D = KL 散度
- L_aux = D(q̂, q_θ) + D(p̂, p_θ)  # 预定义语义的辅助损失
- q̂ = Retrace 目标 (投影到 two-hot)
- p̂ = π_θ(s')  # 一步未来策略
```

## Meta 优化

**发现目标**:
```
J(η) = E_ε E_θ[J(θ)]

Meta-Gradient:
∇_η J(η) ≈ E_ε E_θ[∇_η θ · ∇_θ J(θ)]
```

**实现细节**:
- 通过 20 次 Agent 更新反向传播 (滑动窗口)
- 使用 Meta-Value Function 估计 Advantage
- 定期重置 Agent 参数鼓励快速学习

---

# 7. 实验设计

## 训练基准

| 变体 | 训练环境 | 目的 |
|------|----------|------|
| **Disco57** | Atari 57 游戏 | 在标准基准上发现规则 |
| **Disco103** | Atari 57 + ProcGen + DMLab-30 | 增加多样性和复杂性 |

## 评估基准 (零样本)

| 基准 | 特点 | 挑战 |
|------|------|------|
| **ProcGen** | 程序化生成关卡 | 泛化到未见关卡 |
| **DMLab-30** | 3D 导航与解谜 | 部分可观测、长视野 |
| **Crafter** | 生存与制作 | 稀疏奖励、长序列规划 |
| **NetHack** | Roguelike 游戏 | 极端复杂性、永久死亡 |
| **Sokoban** | 推箱子谜题 | 组合爆炸、精确规划 |

---

# 8. 主要实验结果

## Atari 基准表现

**Disco57 vs SOTA** (IQM 人类归一化分数):

| 算法 | IQM 分数 |
|------|----------|
| **Disco57** | **13.86** |
| MuZero | ~12.5 |
| Dreamer | ~10.2 |
| MEME | ~9.8 |
| STACX | ~9.5 |

**关键发现**:
- ✅ 超越所有现有 RL 算法
- ✅ 在更大网络上泛化 (训练时用小网络)
- ✅  wall-clock 效率显著高于 MuZero

---

# 9. 零样本泛化能力

## 未见领域表现

**Disco57** (仅在 Atari 训练):
- ProcGen:  competitive with PPO
- DMLab-30:  strong zero-shot transfer

**Disco103** (增加 ProcGen+DMLab 训练):
- Crafter: **显著优于 PPO、Dreamer**
- NetHack: **首个在该基准表现良好的通用 RL 规则**
- Sokoban: **超越所有基线**

## 泛化维度

| 泛化类型 | 表现 |
|----------|------|
| 不同观测空间 (像素→向量) | ✅ |
| 不同动作空间 (离散维度变化) | ✅ |
| 更大网络架构 | ✅ |
| 更多训练数据 | ✅ |
| 完全不同领域 | ✅ |

---

# 10. 发现的新语义分析

## 预测语义可视化

**关键发现**: DiscoRL 学习了**独特的预测语义**，不同于传统 RL 概念

**分析结果**:
- 预测捕捉**中等时间尺度**的重要特征
- 识别**未来策略熵** (future policy entropies)
- 预测**大奖励事件** (large-reward events)
- 不等同于价值函数、优势函数或 successor features

**意义**:
> "The discovered predictions capture novel semantics... distinct from existing RL concepts such as value functions."

---

# 11. 可扩展性研究

## 规模效应

**实验**: 增加训练环境的数量、多样性、复杂度

| 扩展维度 | 效果 |
|----------|------|
| 环境数量 ↑ | 性能持续提升 |
| 环境多样性 ↑ | 泛化能力增强 |
| 环境复杂度 ↑ | 发现更强大规则 |
| 总经验量 ↑ | 无饱和迹象 |

**结论**:
> "The discovery process scales, increasing performance as we increase the number, diversity, and complexity of training environments."

**启示**: RL 算法设计未来可能由**自动化方法**主导，可有效扩展数据和计算

---

# 12. 创新点与贡献

## 核心贡献

1. **方法创新**:
   - 首个在复杂多样环境中大规模元学习 RL 规则的方法
   - 用神经网络表示更新规则，超越数学方程的表达限制

2. **性能突破**:
   - 在 Atari 基准超越所有 SOTA 手工设计算法
   - 实现零样本泛化到多个未见领域

3. **理论贡献**:
   - 证明自动化发现 RL 算法的可行性
   - 发现新的预测语义，拓展 RL 理论

4. **开源贡献**:
   - 代码开源：https://github.com/google-deepmind/disco_rl
   - 提供 Disco103 元参数 (Apache 2.0)

---

# 13. 局限性与未来方向

## 当前局限

| 局限 | 说明 |
|------|------|
| **计算成本** | 需要大规模并行计算资源 |
| **连续动作空间** | 当前仅支持离散动作 |
| **多智能体** | 未在协作/竞争多智能体场景验证 |
| **可解释性** | 神经网络规则难以解析理解 |

## 未来方向

1. **扩展动作空间**: 支持连续控制和混合动作
2. **多智能体 RL**: 发现协作和竞争规则
3. **世界模型整合**: 结合模型基方法
4. **理论分析**: 理解发现规则的收敛性和最优性
5. **实际应用**: 机器人控制、推荐系统、自动驾驶

---

# 14. 总结

## 核心要点

✅ **自动化发现可行**: RL 算法可由数据驱动自动发现，无需手工设计

✅ **性能超越 SOTA**: DiscoRL 在多个基准超越 MuZero、Dreamer 等

✅ **零样本泛化**: 在未见环境和不同架构上表现优异

✅ **发现新概念**: 学习到不同于价值函数的新预测语义

✅ **可扩展**: 性能随数据、计算、环境多样性持续提升

## 深远影响

> "The design of RL algorithms may, in the future, be led by automated methods that can scale effectively with data and compute."

**范式转变**: 从"设计算法"到"发现算法"

---

# 15. Q&A

## 讨论问题

1. DiscoRL 的元学习框架如何避免过拟合到训练环境？
2. 发现的预测语义能否被解析理解？
3. 该方法是否适用于样本效率极低的真实世界场景？
4. 如何保证发现的算法的稳定性和安全性？

## 参考文献

- Oh, J. et al. Discovering state-of-the-art reinforcement learning algorithms. *Nature* (2025). DOI: 10.1038/s41586-025-09761-x
- Kemaev, I. et al. Scalable meta-learning via mixed-mode differentiation. *ICML* (2025)
- GitHub: https://github.com/google-deepmind/disco_rl
- 项目页面：https://google-deepmind.github.io/disco_rl/

---

# 附录：关键技术细节

## 计算基础设施

- **并行 Agent 数量**: 数百个
- **训练环境**: 57-103 个复杂环境
- **优化技术**:
  - Mixed-mode differentiation
  - Recursive gradient checkpointing
  - Mixed precision training
  - Pre-emptive parameter offloading

## 超参数设置

- Meta-Network: LSTM 架构
- 反向传播窗口：20 步
- Agent 参数定期重置
- 使用 Meta-Value Function 估计 Advantage

## 评估指标

- **IQM (InterQuartile Mean)**: 统计可靠的聚合指标
- **人类归一化分数**: (score - random) / (human - random)
- **95% 置信区间**: 评估统计显著性

---

*感谢聆听！*
