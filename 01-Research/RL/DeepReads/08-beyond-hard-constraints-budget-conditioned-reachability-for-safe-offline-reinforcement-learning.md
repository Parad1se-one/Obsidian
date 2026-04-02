# DeepRead | Beyond Hard Constraints: Budget-Conditioned Reachability For Safe Offline Reinforcement Learning

> 自动精读生成时间：2026-04-02 08:00 UTC+08:00

## 论文信息
- 标题：Beyond Hard Constraints: Budget-Conditioned Reachability For Safe Offline Reinforcement Learning
- 作者：Janaka Chathuranga Brahmanage, Akshat Kumar
- 发布时间：2026-03-08
- 更新时间：2026-03-31 21:32
- arXiv：http://arxiv.org/abs/2603.22292v2
- PDF：http://arxiv.org/pdf/2603.22292v2
- 分类：cs.LG, cs.AI, cs.RO
- 来源可信度（粗判）：中

## 入选原因
- 命中主题词：reinforcement learning
- 命中主题词：offline reinforcement learning
- 命中主题词：model-based
- 命中主题词：safety
- arXiv 分类匹配 RL/ML/机器人/多智能体
- 最近 14 天内更新

## 原始摘要
Sequential decision making using Markov Decision Process underpins many realworld applications. Both model-based and model free methods have achieved strong results in these settings. However, real-world tasks must balance reward maximization with safety constraints, often conflicting objectives, that can lead to unstable min/max, adversarial optimization. A promising alternative is safety reachability analysis, which precomputes a forward-invariant safe state, action set, ensuring that an agent starting inside this set remains safe indefinitely. Yet, most reachability based methods address only hard safety constraints, and little work extends reachability to cumulative cost constraints. To address this, first, we define a safetyconditioned reachability set that decouples reward maximization from cumulative safety cost constraints. Second, we show how this set enforces safety constraints without unstable min/max or Lagrangian optimization, yielding a novel offline safe RL algorithm that learns a safe policy from a fixed dataset without environment interaction. Finally, experiments on

## 一句话总结
这篇论文试图解决什么问题、核心抓手是什么、为什么值得继续看，还需要结合全文进一步验证。

## 重点精读框架
### 1. 研究问题
- 它针对的具体任务/痛点是什么？
- 为什么现有方法不够好？

### 2. 方法核心
- 状态、动作、奖励、训练信号分别是什么？
- 新方法和 PPO / SAC / Offline RL / World Model / MARL 这些经典线有什么关系？
- 真正新的部分到底在哪？是目标函数、训练流程、架构、数据构造，还是评估协议？

### 3. 实验设计
- 用了哪些 benchmark？
- baseline 是否公平？
- ablation 是否足够？
- 指标是不是只挑了对自己有利的？

### 4. 批判性判断
- 论文最可能被高估的点是什么？
- 哪些结果可能依赖算力、数据规模、prompt、筛选策略？
- 如果要复现，最大的坑在哪？

### 5. 对我们有什么价值
- 对 RL / RLVR / World Model / Agent / Robotics 哪条线最有启发？
- 值不值得纳入后续日报？
- 值不值得做二次深读或实验复现？

## 小虾初判
- 精读优先级：高 / 中 / 低（待阅读全文后确认）
- 推荐动作：继续全文精读 / 只保留摘要信息 / 纳入后续专题追踪

## 关联记录
- Papers 卡片：待补充
- 当日摘要引用：待补充
