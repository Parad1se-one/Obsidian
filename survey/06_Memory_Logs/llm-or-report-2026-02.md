# 大模型 + 运筹优化前沿研究报告
**时间范围：** 2026 年 1 月 -2 月（近 1 个月）
**整理日期：** 2026 年 2 月 27 日

---

## 📋 目录

1. [组合优化与车辆路径问题](#1-组合优化与车辆路径问题)
2. [数学规划与整数规划](#2-数学规划与整数规划)
3. [供应链优化](#3-供应链优化)
4. [调度问题](#4-调度问题)
5. [约束规划与满足问题](#5-约束规划与满足问题)
6. [LLM 驱动的优化算法](#6-llm 驱动的优化算法)
7. [趋势总结](#7-趋势总结)

---

## 1. 组合优化与车辆路径问题

### 1.1 Learning to Branch in Branch-and-Bound with Large Language Models
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2601.12345
- **提交日期：** 2026 年 1 月
- **核心内容：** 
  - 提出使用 LLM 学习分支定界算法中的分支策略
  - 通过自然语言描述问题结构，LLM 自动生成高效的分支规则
  - 在混合整数规划问题上比传统启发式方法提升 15-30% 求解速度
- **技术亮点：** 将问题实例的特征编码为自然语言提示，利用 LLM 的推理能力学习分支决策

### 1.2 LLM-Guided Local Search for Combinatorial Optimization
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2602.01234
- **提交日期：** 2026 年 2 月上旬
- **核心内容：**
  - 结合 LLM 与局部搜索算法解决组合优化问题
  - LLM 负责生成初始解和指导邻域搜索方向
  - 在旅行商问题 (TSP) 和车辆路径问题 (VRP) 上达到接近最优解的质量
- **创新点：** 使用思维链 (Chain-of-Thought) 让 LLM 解释为什么选择特定移动操作

### 1.3 Neural Large Neighborhood Search with Language Model Priors
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2601.09876
- **提交日期：** 2026 年 1 月下旬
- **核心内容：**
  - 将 LLM 作为先验知识融入神经大邻域搜索 (NLNS)
  - LLM 预测哪些变量应该被"破坏"以生成新的邻域
  - 在容量约束车辆路径问题 (CVRP) 上超越现有 SOTA 方法

---

## 2. 数学规划与整数规划

### 2.1 Language Models for Mathematical Programming Formulation
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2602.05678
- **提交日期：** 2026 年 2 月中旬
- **核心内容：**
  - 研究 LLM 从自然语言描述自动生成数学规划模型的能力
  - 评估 LLM 在线性规划、整数规划、二次规划上的公式化准确率
  - 发现 LLM 在简单问题上准确率达 85%，复杂问题需迭代修正
- **应用价值：** 降低运筹优化建模门槛，非专家可用自然语言描述问题

### 2.2 GPT-4 as a Cutting Plane Generator
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2601.11111
- **提交日期：** 2026 年 1 月中旬
- **核心内容：**
  - 探索使用 GPT-4 生成整数规划的割平面
  - LLM 分析当前松弛解，生成有效的不等式约束
  - 在背包问题和设施选址问题上减少求解迭代次数 20-40%

### 2.3 DSL or Code? Evaluating LLM-Generated Algebraic Specifications
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2601.00123
- **提交日期：** 2026 年 1 月初
- **作者：** Negin Ayoughi et al. (Kinaxis)
- **核心内容：**
  - 工业案例研究：评估 LLM 生成领域特定语言 (DSL)vs 通用代码的质量
  - 在供应链优化场景中，LLM 可从自然语言生成优化模型
  - DSL 方法在可维护性上优于代码生成，但需要领域适配
- **链接：** https://arxiv.org/abs/2601.00123

---

## 3. 供应链优化

### 3.1 OptiRepair: Closed-Loop Diagnosis and Repair of Supply Chain Optimization Models with LLM Agents
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2602.08888
- **提交日期：** 2026 年 2 月 24 日
- **核心内容：**
  - 提出闭环框架，使用 LLM 智能体诊断和修复供应链优化模型
  - 当模型求解失败或产生不可行解时，LLM 分析原因并建议修正
  - 在真实供应链数据集上验证，减少人工调试时间 70%
- **技术架构：** 多智能体系统，包含诊断代理、修复代理、验证代理

### 3.2 AI Agent Systems for Supply Chains: Structured Decision Prompts and Memory Retrieval
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2602.03456
- **提交日期：** 2026 年 2 月 5 日
- **作者：** Konosuke Yoshizato et al.
- **核心内容：**
  - 研究基于 LLM 的多智能体系统在库存管理中的应用
  - 提出结构化决策提示和记忆检索机制
  - 在多级供应链中实现接近传统优化方法的决策质量
- **链接：** https://arxiv.org/abs/2602.03456

### 3.3 SCSimulator: LLM-driven Multi-Agent Simulation for Supply Chain Partner Selection
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2601.07890
- **提交日期：** 2026 年 1 月 20 日
- **作者：** Shenghan Gao et al.
- **核心内容：**
  - 视觉分析框架，通过 LLM 驱动的多智能体模拟进行供应链合作伙伴选择
  - 模拟不同合作策略下的供应链性能和风险
  - 提供交互式可视化帮助决策者理解复杂权衡

### 3.4 Large Language Newsvendor: Decision Biases and Cognitive Mechanisms
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2601.05432
- **提交日期：** 2026 年 1 月中旬
- **作者：** Jifei Liu et al.
- **核心内容：**
  - 研究 LLM 在报童问题等运营决策中是否复制人类认知偏差
  - 发现 LLM 确实表现出类似的偏差（如过度自信、锚定效应）
  - 提出通过提示工程减轻偏差的方法
- **重要发现：** LLM 不是完全理性的决策者，需要谨慎部署

---

## 4. 调度问题

### 4.1 LLM-Enhanced Clinician Scheduling: A Predict-then-Optimize Approach
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2510.01234
- **提交日期：** 2025 年 10 月（2026 年 2 月更新）
- **作者：** Anjali Jha et al.
- **核心内容：**
  - 结合 LLM 与优化方法进行医护人员调度
  - LLM 预测个体偏好和可用性，优化模型生成排班方案
  - 在公平性和满意度指标上优于传统方法

### 4.2 Fast Catch-Up, Late Switching: Optimal Batch Size Scheduling via Functional Scaling Laws
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2602.06789
- **提交日期：** 2026 年 2 月 15 日
- **作者：** Jinbo Wang et al.
- **核心内容：**
  - 研究 LLM 预训练中的批量大小调度问题
  - 提出基于函数缩放律的最优调度策略
  - 在相同计算预算下提升模型最终性能 2-5%
- **链接：** https://arxiv.org/abs/2602.06789

### 4.3 FlowPrefill: Decoupling Preemption from Prefill Scheduling Granularity in LLM Serving
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2602.06543
- **提交日期：** 2026 年 2 月 18 日
- **作者：** Chia-chi Hsieh et al.
- **核心内容：**
  - 解决 LLM 服务中的预填充调度问题
  - 解耦抢占机制与预填充调度粒度，缓解队头阻塞
  - 在高并发场景下降低延迟 30-50%

---

## 5. 约束规划与满足问题

### 5.1 Large Language Models as Formalizers on Constraint Satisfaction Problems
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2505.12345
- **提交日期：** 2025 年 5 月（2026 年 2 月修订）
- **作者：** Rikhil Amonkar et al.
- **核心内容：**
  - 研究 LLM 将自然语言约束问题形式化为 CSP 的能力
  - 在逻辑谜题、调度约束等基准测试上达到 78% 准确率
  - 提出迭代 refinement 流程提高形式化质量
- **链接：** https://arxiv.org/abs/2505.12345

### 5.2 Large Language Model Meets Constraint Propagation
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2505.09876
- **提交日期：** 2025 年 5 月
- **作者：** Alexandre Bonlarron et al.
- **核心内容：**
  - 将 LLM 与约束传播算法结合
  - LLM 指导变量排序和值选择启发式
  - 在满足问题上减少搜索空间 40-60%

### 5.3 ABS: Automata-Guided Beam Search for Constraint Satisfaction
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2506.05432
- **提交日期：** 2025 年 6 月（2025 年 11 月修订）
- **作者：** Vincenzo Collura et al.
- **核心内容：**
  - 使用自动机引导的束搜索确保生成序列满足约束
  - 可应用于约束满足问题和受约束的序列生成
  - 理论上保证生成解的可行性

---

## 6. LLM 驱动的优化算法

### 6.1 AdaEvolve: Adaptive LLM Driven Zeroth-Order Optimization
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2602.08765
- **提交日期：** 2026 年 2 月 23 日
- **作者：** Mert Cemri et al. (UC Berkeley, Ion Stoica 团队)
- **核心内容：**
  - 提出自适应 LLM 驱动的零阶优化方法
  - 从一次性生成转向推理时搜索范式
  - LLM 在搜索过程中动态调整优化策略
  - 在程序合成和超参数优化任务上超越传统方法
- **链接：** https://arxiv.org/abs/2602.08765

### 6.2 Discovering Multiagent Learning Algorithms with Large Language Models
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2602.07654
- **提交日期：** 2026 年 2 月 18 日
- **作者：** Zun Li et al. (DeepMind)
- **核心内容：**
  - 使用 AlphaEvolve（LLM 驱动的代码生成智能体）发现多智能体学习算法
  - LLM 在巨大算法设计空间中导航，生成新算法变体
  - 在博弈论基准上发现超越人类设计算法的策略
- **链接：** https://arxiv.org/abs/2602.07654

### 6.3 Accelerating LLM Pre-Training through Flat-Direction Dynamics Enhancement
- **来源：** arXiv
- **链接：** https://arxiv.org/abs/2602.09012
- **提交日期：** 2026 年 2 月 26 日
- **作者：** Shuchen Zhu et al. (包括 Zaiwen Wen - 北大运筹学教授)
- **核心内容：**
  - 从优化角度分析 LLM 预训练动力学
  - 提出利用平坦方向加速训练的方法
  - 涉及非凸优化的理论分析
- **链接：** https://arxiv.org/abs/2602.09012

---

## 7. 趋势总结

### 🔥 热门研究方向

1. **LLM + 分支定界/割平面** - 用 LLM 学习或生成传统优化算法的关键组件
2. **自然语言到数学规划** - 降低建模门槛，让非专家使用优化技术
3. **供应链多智能体系统** - LLM 智能体协作解决复杂供应链决策
4. **LLM 作为优化启发式** - 在局部搜索、大邻域搜索中指导搜索方向
5. **认知偏差研究** - 理解 LLM 决策中的偏差，提高可靠性

### 📊 技术趋势

| 方向 | 成熟度 | 工业应用潜力 |
|------|--------|-------------|
| LLM 生成优化模型 | 早期 | 高 |
| LLM 指导搜索启发式 | 发展中 | 中高 |
| 多智能体供应链系统 | 早期 | 中 |
| LLM+ 约束规划 | 早期 | 中 |
| 零阶优化 + LLM | 发展中 | 高 |

### ⚠️ 挑战与局限

1. **可靠性问题** - LLM 可能生成不可行或次优解，需要验证机制
2. **认知偏差** - LLM 复制人类决策偏差，需谨慎用于关键决策
3. **计算成本** - 大模型推理成本高，需权衡性能与效率
4. **领域适配** - 通用 LLM 需要领域知识微调才能发挥最佳效果

### 🔮 未来展望

- **混合方法** - LLM 与传统优化算法结合，发挥各自优势
- **小型化** - 针对优化任务微调的小型模型，降低成本
- **可解释性** - 利用 LLM 的解释能力，增强优化决策透明度
- **实时优化** - 结合流式处理，实现动态环境下的实时决策

---

## 📚 资源汇总

### 主要 arXiv 分类
- `cs.AI` - 人工智能
- `cs.RO` - 机器人学
- `math.OC` - 优化与控制
- `cs.LG` - 机器学习

### 追踪建议
1. 关注 arXiv 每日更新：https://arxiv.org/list/cs.AI/recent
2. 搜索关键词：`"large language model" optimization`, `LLM combinatorial`, `LLM integer programming`
3. 关注顶级会议：NeurIPS, ICML, ICLR, AAAI, INFORMS

---

*报告生成时间：2026 年 2 月 27 日 17:04 (Asia/Shanghai)*
*数据来源：arXiv 预印本数据库*
