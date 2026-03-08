# RL Researcher Skill - 强化学习研究专家

## Overview
系统性学习强化学习，从基础到前沿，最终能够独立提出并验证新 idea，自动设计实验，撰写论文。

**人设：** 小虾 🦐 - "我要成为顶尖 RL 研究者"

**版本：** v1.0 (2026-03-05)

**目标:** 6 个月内达到顶尖 RL 研究者水平

---

## Core Philosophy

### 学习理念

1. **系统性** - 从基础到前沿，不跳跃
2. **实践性** - 每个算法都要动手实现
3. **批判性** - 读论文要质疑、要思考
4. **创新性** - 最终要提出自己的 idea

### 研究方法论

```
观察现象 → 提出问题 → 文献调研 → 形成假设 → 设计实验 → 验证假设 → 撰写论文
```

---

## Learning Roadmap

### Phase 1: 基础奠基 (Week 1-4) ⭐⭐⭐⭐⭐

#### 数学基础
| 主题 | 内容 | 资源 |
|------|------|------|
| 概率论 | 随机变量、期望、方差、常见分布 | 《概率论与数理统计》 |
| 线性代数 | 矩阵运算、特征值、SVD | 《线性代数应该这样学》 |
| 优化理论 | 梯度下降、凸优化、拉格朗日 | 《Convex Optimization》Boyd |
| 信息论 | 熵、KL 散度、互信息 | 《Elements of Information Theory》 |

#### 机器学习基础
| 主题 | 内容 | 资源 |
|------|------|------|
| 监督学习 | 回归、分类、神经网络 | 《Deep Learning》Goodfellow |
| 无监督学习 | 聚类、降维、生成模型 | CS231n |
| 深度学习 | CNN、RNN、Transformer | 《动手学深度学习》 |

#### 强化学习入门
| 主题 | 内容 | 资源 |
|------|------|------|
| MDP | 马尔可夫决策过程、贝尔曼方程 | 《Reinforcement Learning: An Introduction》Sutton |
| 动态规划 | 值迭代、策略迭代 | Sutton Chapter 3-4 |
| 蒙特卡洛 | MC 预测、MC 控制 | Sutton Chapter 5 |
| TD 学习 | Q-learning、SARSA | Sutton Chapter 6 |

**输出:**
- `knowledge/rl/basics/mdp-notes.md`
- `knowledge/rl/basics/bellman-equation.md`
- `knowledge/rl/basics/td-learning.md`
- `code/rl-basics/` - 基础算法实现

---

### Phase 2: 经典算法 (Week 5-8) ⭐⭐⭐⭐⭐

#### Value-Based Methods
| 算法 | 核心思想 | 实现任务 |
|------|----------|----------|
| DQN | 深度 Q 网络、经验回放 | 实现 DQN 玩 Atari |
| Double DQN | 解决过估计问题 | 对比 DQN 效果 |
| Dueling DQN | 分离值和优势 | 分析消融实验 |
| Prioritized ER | 优先经验回放 | 实现 PER |

#### Policy-Based Methods
| 算法 | 核心思想 | 实现任务 |
|------|----------|----------|
| REINFORCE | 蒙特卡洛策略梯度 | 实现 CartPole |
| Actor-Critic | 结合值和策略 | 实现 A2C |
| A3C | 异步并行 | 对比 A2C |
| GAE | 广义优势估计 | 理解λ-return |

#### Model-Based Methods
| 算法 | 核心思想 | 实现任务 |
|------|----------|----------|
| Dyna | 学习模型 + 规划 | 实现 Dyna-Q |
| MCTS | 蒙特卡洛树搜索 | 实现五子棋 AI |
| World Models | 学习隐空间模型 | 复现 Ha & Schmidhuber |

**输出:**
- `code/rl-algorithms/dqn.py`
- `code/rl-algorithms/a2c.py`
- `code/rl-algorithms/ppo.py`
- `knowledge/rl/algorithms/algorithm-comparison.md`

---

### Phase 3: 前沿算法 (Week 9-16) ⭐⭐⭐⭐⭐

#### Policy Optimization
| 算法 | 年份 | 核心贡献 |
|------|------|----------|
| TRPO | 2015 | 信赖域策略优化 |
| PPO | 2017 | 近端策略优化 (主流) |
| SAC | 2018 | 软 Actor-Critic |
| TD3 | 2018 | 解决连续控制过估计 |

#### Model-Based RL (SOTA)
| 算法 | 年份 | 核心贡献 |
|------|------|----------|
| MuZero | 2019 | 无需已知规则的 MCTS |
| Dreamer | 2020 | 基于模型的想象学习 |
| DreamerV2/V3 | 2021/2023 | 改进版 |
| EfficientZero | 2021 | 样本效率提升 |

#### Offline RL
| 算法 | 年份 | 核心贡献 |
|------|------|----------|
| BCQ | 2019 | 批量约束 Q 学习 |
| CQL | 2020 | 保守 Q 学习 |
| IQL | 2021 | 隐式 Q 学习 |
| Diffusion Policy | 2022 | 扩散模型用于策略 |

#### Multi-Agent RL
| 算法 | 年份 | 核心贡献 |
|------|------|----------|
| MADDPG | 2017 | 多智能体 DDPG |
| QMIX | 2018 | 值分解 |
| MAPPO | 2021 | 多智能体 PPO |

**输出:**
- `knowledge/rl/sota/algorithm-survey-2026.md`
- `code/rl-sota/ppo-implementation.py`
- `code/rl-sota/sac-implementation.py`
- `papers/` - 论文阅读笔记

---

### Phase 4: 研究方向 (Week 17-24) ⭐⭐⭐⭐⭐

#### 潜在研究方向

**1. Sample Efficiency (样本效率)**
- 问题：RL 需要大量交互，样本效率低
- 思路：结合模型、离线数据、迁移学习
- 验证：在 Atari/MuJoCo 上对比样本效率

**2. Generalization (泛化能力)**
- 问题：训练好的策略在新环境表现差
- 思路：数据增强、域随机化、元学习
- 验证：ProcGen 基准测试

**3. Exploration (探索策略)**
- 问题：稀疏奖励下探索困难
- 思路：内在动机、好奇心驱动、信息增益
- 验证：Montezuma's Revenge

**4. Hierarchical RL (分层强化学习)**
- 问题：长视野任务难以学习
- 思路：选项框架、目标条件策略
- 验证：长序列任务

**5. RLHF (人类反馈强化学习)**
- 问题：奖励函数难以设计
- 思路：从人类偏好学习奖励
- 验证：LLM 对齐任务

**6. World Models (世界模型)**
- 问题：环境模型学习困难
- 思路：潜空间模型、扩散世界模型
- 验证：Dreamer 系列改进

**输出:**
- `research/proposals/<idea-name>-proposal.md`
- `research/experiments/<experiment-name>/`
- `papers/drafts/<paper-name>.md`

---

## Research Workflow

### 1. 文献调研

```bash
# 搜索最新论文
web_search "reinforcement learning NeurIPS 2025 best paper"
web_search "model-based RL survey 2026"
web_fetch <arxiv 论文链接>

# 整理笔记
cat > papers/<paper-name>-notes.md << EOF
# 论文笔记

## 基本信息
- 标题：
- 作者：
- Venue:
- 年份：

## 核心贡献
1. 
2. 
3. 

## 方法
- 问题定义：
- 核心思想：
- 关键技术：

## 实验
- 基准：
- 对比方法：
- 主要结果：

## 批判性思考
- 优点：
- 局限：
- 可改进点：
EOF
```

### 2. Idea 形成

**Idea 来源:**
- 论文局限性的改进
- 不同方法的组合
- 跨领域迁移
- 实际应用场景

**Idea 评估框架:**
| 维度 | 评分 (1-5) | 说明 |
|------|------------|------|
| 新颖性 | | 是否有创新 |
| 可行性 | | 是否可实现 |
| 影响力 | | 潜在影响大小 |
| 可验证性 | | 是否可实验验证 |

**综合 ≥16 分 → 值得 pursued**

### 3. 实验设计

**实验设计模板:**
```markdown
## 实验设计

### 研究问题
- 核心假设：

### 基准环境
- [ ] Atari (离散动作)
- [ ] MuJoCo (连续控制)
- [ ] ProcGen (泛化测试)
- [ ] 自定义环境

### 对比方法
- [ ] PPO (baseline)
- [ ] SAC (连续控制)
- [ ] 相关 SOTA

### 评估指标
- 样本效率 (steps to threshold)
- 最终性能 (average return)
- 稳定性 (std across seeds)
- 泛化能力 (unseen levels)

### 消融实验
- [ ] 关键组件 A
- [ ] 关键组件 B
- [ ] 超参数敏感性

### 计算资源
- GPU: 
- 预计时间：
```

### 4. 代码实现

**项目结构:**
```
rl-research/
├── algorithms/         # 算法实现
│   ├── ppo.py
│   ├── sac.py
│   └── my新方法.py
├── environments/       # 环境
│   ├── atari.py
│   ├── mujoco.py
│   └── custom.py
├── experiments/        # 实验配置
│   ├── config.yaml
│   └── run.sh
├── results/            # 实验结果
│   ├── logs/
│   └── plots/
└── papers/             # 论文
    └── draft.md
```

### 5. 论文写作

**论文结构:**
```markdown
# 论文标题

## Abstract
- 问题
- 方法
- 结果

## Introduction
- 背景
- 挑战
- 贡献

## Related Work
- 相关领域
- 现有方法局限

## Method
- 问题定义
- 核心思想
- 技术细节

## Experiments
- 设置
- 主结果
- 消融实验
- 分析

## Conclusion
- 总结
- 局限
- 未来工作
```

---

## Auto-Research System

### 自动化流程

```
1. 每日论文扫描
   ↓
2. 自动阅读 + 笔记
   ↓
3. 识别研究空白
   ↓
4. 生成 Idea 提案
   ↓
5. 设计实验
   ↓
6. 运行实验
   ↓
7. 分析结果
   ↓
8. 撰写论文
```

### 工具集成

| 任务 | 工具 |
|------|------|
| 论文搜索 | arXiv API, Google Scholar |
| 论文阅读 | web_fetch + 摘要生成 |
| 代码实现 | Python + PyTorch + Gymnasium |
| 实验管理 | Weights & Biases / TensorBoard |
| 论文写作 | LaTeX / Markdown |
| 自动编程 | ACP harness / sessions_spawn |

---

## Reference: Auto-Paper Frameworks

### 最新自动写论文大模型框架

**需要调研的框架:**
1. **Agent Scientist** - 自动提出假设并验证
2. **AI Scientist** - 自动写论文
3. **ResearchAgent** - 全流程研究自动化
4. **PaperCoder** - 从论文到代码

**调研任务:**
- [ ] web_search "AI Scientist paper writing framework 2025 2026"
- [ ] web_search "automated research agent reinforcement learning"
- [ ] web_fetch <框架 GitHub/论文链接>
- [ ] 分析框架架构
- [ ] 借鉴到自己的系统

---

## Learning Schedule

### 每日学习 (心跳触发)

| 时段 | 内容 | 时长 |
|------|------|------|
| 上午 | RL 基础/算法学习 | 30 分钟 |
| 下午 | 论文阅读 + 笔记 | 30 分钟 |
| 晚间 | 代码实现/实验 | 60 分钟 |

### 每周目标

| 周数 | 主题 | 输出 |
|------|------|------|
| 1-4 | 基础奠基 | 基础算法实现 + 笔记 |
| 5-8 | 经典算法 | DQN/PPO/SAC实现 |
| 9-16 | 前沿算法 | SOTA 复现 + 对比 |
| 17-24 | 研究方向 | 1-2 个原创 idea + 实验 |

---

## Progress Tracking

### 知识追踪
```json
{
  "rl-basics": {
    "mdp": 0,
    "bellman": 0,
    "mc": 0,
    "td": 0
  },
  "algorithms": {
    "dqn": 0,
    "ppo": 0,
    "sac": 0
  },
  "papers-read": 0,
  "code-implemented": 0,
  "experiments-run": 0
}
```

### 里程碑
- [ ] 完成 Sutton 书籍阅读
- [ ] 实现 10+ 经典算法
- [ ] 阅读 50+ 篇论文
- [ ] 提出 1 个原创 idea
- [ ] 完成实验验证
- [ ] 撰写 1 篇论文

---

## Integration with Self-Learner

### HEARTBEAT.md 更新

```markdown
## RL 研究学习 (每日)

### 上午心跳
- [ ] RL 基础/算法学习 30 分钟
- [ ] 运行 `./skills/rl-researcher/study.sh basics 30`

### 下午心跳
- [ ] 论文阅读 + 笔记 30 分钟
- [ ] 运行 `./skills/rl-researcher/study.sh paper 30`

### 晚间心跳
- [ ] 代码实现/实验 60 分钟
- [ ] 运行 `./skills/rl-researcher/study.sh code 60`
```

---

## Created
2026-03-05 by 小虾 🦐

**Status:** MVP Ready - 框架可用

**Trigger:** User request "成为一名顶尖的强化学习领域的科研工作者。你要掌握学习当前能够接触到的所有的强化学习主流方法，并自己提出和验证新的 idea，自动设计实验来进行验证，自己搭环境，自己写论文。不要怕 token 的消耗，最终你要成为一个顶尖的强化学习领域的研究者。可以去参考一下有一个最新的自动写论文的大模型框架"

**Mission:** 6 个月内成为顶尖 RL 研究者。
