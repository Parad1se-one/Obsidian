# 强化学习每日论文总结 - 2026 年 3 月 4 日

## 📌 核心亮点

### 1. LongRLVR: 长上下文强化学习 (ICLR 2026)
- **论文**: longrlvr: long-context reinforcement learning
- **机构**: 发表于 ICLR 2026
- **核心贡献**: 
  - 解决了在长上下文训练中使用简单 RLVR（仅结果奖励）时模型上下文回忆分数快速停滞的问题
  - 提出了专门的数据集生成方法，包含 (X, Q, G, y) 元组，其中 G 是回答问题所需的关键证据块
  - 在所有基准测试和模型上相比 naive RLVR 取得显著提升
  - 对于 Qwen2.5-14B-1M 模型，在 LongBench v2 上表现优异

### 2. ReGFT: 参考引导微调解决奖励稀疏问题
- **论文**: Learn Hard Problems During RL with Reference Guided Fine-tuning
- **机构**: ByteDance Seed, UC Berkeley, Carnegie Mellon University
- **核心贡献**:
  - 解决了数学推理 RL 中的奖励稀疏问题：对于难题，LLM 无法采样到任何正确轨迹
  - 在 RL 之前，将模型自己的推理与训练数据中的专家解决方案交错，合成难题的轨迹
  - 提高模型的初始能力，使后续 RL 阶段的奖励驱动学习更有效
  - 实验显示，使用 ReGFT 初始化的模型在所有基准测试中持续优于原始检查点

### 3. 多智能体强化学习新进展 (ICLR 2026)
- **论文**: Robust Multi-Agent Reinforcement Learning with Diverse Adversarial Agent Generation
- **核心贡献**:
  - 提出了鲁棒 MARL 训练框架，联合训练合作智能体与多样化对抗策略生成器
  - **DAAG**: 多样化对抗智能体生成器，通过信息论目标优化，产生行为多样化且具有挑战性的对抗智能体
  - **CAPE**: 基于对比学习的智能体策略编码器，持续学习对抗智能体策略的信息表示
  - 提高多智能体协调的泛化能力和鲁棒性

### 4. MARTI-MARS²: 多智能体自搜索扩展
- **论文**: MARTI-MARS²: Scaling Multi-Agent Self-Search via Reinforcement Learning
- **核心贡献**:
  - 提出了多智能体强化训练和推理框架，集成自搜索扩展
  - 通过强化学习扩展多智能体自搜索能力

### 5. Flow-Factory: 扩散模型的统一 RL 框架
- **论文**: Flow-Factory: A Unified Framework for Reinforcement Learning in Flow-Matching Models
- **核心贡献**:
  - 强化学习已成为对齐扩散和流匹配模型与人类偏好的有前景的范式
  - 提供了统一的强化学习框架用于流匹配模型

### 6. Experiential Reinforcement Learning (ERL): 经验强化学习
- **机构**: 南加州大学和宾夕法尼亚大学
- **核心贡献**:
  - 提出新的训练范式，将"经验学习"引入强化学习过程
  - 模型不仅通过试错优化行为，还能反思并将经验内化为策略
  - 通过反思机制分析失败并纠正策略，使行为改进在后续任务中持续积累
  - 相比传统 RL 的重复试错探索，ERL 形成更稳定的学习过程

### 7. 鲁棒价值分解的多智能体 RL
- **论文**: Agent Reinforcement Learning via Robust Value Factorization
- **核心贡献**:
  - 提出了鲁棒 QTRAN 算法，使用ρ-污染不确定性集
  - 增强了多智能体系统在不确定性环境下的鲁棒性

## 🔬 研究趋势分析

### 趋势 1: RL + LLM 推理能力增强
- DeepSeek-R1 系列继续影响研究方向
- 多个工作聚焦于使用 RL 提升 LLM 的数学推理和长上下文理解能力
- 奖励建模和稀疏奖励问题成为关键研究点

### 趋势 2: 多智能体系统的鲁棒性
- ICLR 2026 有多篇论文关注 MARL 的鲁棒性和泛化能力
- 对抗训练和对比学习成为提升鲁棒性的重要技术
- 多智能体与生成式 AI 的融合成为新兴方向

### 趋势 3: 经验学习与反思机制
- ERL 代表了从纯试错向经验内化的范式转变
- 反思机制使模型能够从失败中学习并积累策略改进
- 这可能成为未来 RL 训练的标准组件

### 趋势 4: 扩散模型与 RL 的结合
- Flow-Factory 等工作显示 RL 在扩散模型对齐中的应用
- 这是一个快速发展的交叉领域

## 📅 即将关注的会议
- **ICLR 2026**: 多篇 RL 相关论文已被接收，包括长上下文 RL、多智能体 RL 等方向
- **AAAI 2026**: 接收了 RL 与 LLM 推理相关的工作

## 🔗 重要资源
- arXiv 最新论文: https://arxiv.org/list/cs.AI/recent
- ICLR 2026: https://iclr.cc/
- alphaXiv 论文探索: https://alphaxiv.org/

---
*生成时间: 2026-03-04 09:00 (Asia/Shanghai)*
*数据来源: Tavily Search*
