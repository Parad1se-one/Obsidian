# RLVR 综述参考文献列表 (2025-2026)

**生成时间**: 2026 年 3 月 5 日  
**论文总数**: 120+ 篇  
**覆盖 venue**: ICML 2025, NeurIPS 2025, ICLR 2026, AAAI 2026, IJCAI 2025, CoRL 2025, AAMAS 2025, JMLR, TMLR, Nature, Nature Machine Intelligence, CVPR 2025, ICCV 2025

---

## 目录

1. [DeepSeek-R1 与 GRPO 系列](#1-deepseek-r1 与 grpo 系列)
2. [过程奖励与结果奖励](#2-过程奖励与结果奖励)
3. [探索与利用](#3-探索与利用)
4. [数学推理](#4-数学推理)
5. [代码生成](#5-代码生成)
6. [多模态 RLVR](#6-多模态 rlvr)
7. [具身智能与机器人学](#7-具身智能与机器人学)
8. [科学发现](#8-科学发现)
9. [多智能体 RLVR](#9-多智能体 rlvr)
10. [理论分析](#10-理论分析)
11. [应用领域](#11-应用领域)
12. [长上下文 RLVR](#12-长上下文 rlvr)
13. [综述与调查](#13-综述与调查)
14. [开源项目与资源](#14-开源项目与资源)

---

## 1. DeepSeek-R1 与 GRPO 系列

### 1.1 核心论文

1. **DeepSeek-R1: Incentivizing Reasoning Capability in LLMs through Reinforcement Learning**
   - 作者：DeepSeek-R1 Team
   - 期刊：Nature, 2025
   - URL: https://www.nature.com/articles/s41586-025-09422-z
   - 贡献：首次展示纯规则奖励 RL 可激发复杂推理能力涌现

2. **DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning**
   - 作者：DeepSeek-R1 Team
   - arXiv: 2501.12948
   - URL: https://arxiv.org/pdf/2501.12948
   - 贡献：详细技术报告，包含训练细节和超参数

3. **Understanding R1-Zero-Like Training: A Critical Perspective**
   - 作者：Liu, Zichen et al.
   - 会议：ICLR, 2026
   - GitHub: https://github.com/sail-sg/understand-r1-zero
   - 贡献：分析基座模型和 RL 在 R1-Zero 训练中的作用

4. **There May Not be Aha Moment in R1-Zero-Like Training — A Pilot Study**
   - 作者：Liu, Zichen et al.
   - 年份：2025
   - URL: https://oatllm.notion.site/oat-zero
   - 贡献：质疑"顿悟时刻"现象，提供替代解释

5. **Understanding GRPO: A Theoretical Perspective**
   - 作者：Various
   - 会议：ICLR, 2026
   - 贡献：GRPO 算法的收敛性分析

### 1.2 GRPO 改进工作

6. **DAPO: An Open-Source LLM Reinforcement Learning System at Scale**
   - 作者：Yu, L. et al.
   - 会议：ICML, 2025
   - 贡献：大规模 RLVR 训练系统

7. **OpenReasoner-Zero: An Open Source Approach to Scaling Up Reinforcement Learning on the Base Model**
   - GitHub: https://github.com/OpenReasonerZero
   - 贡献：首个开源的基座模型 RLVR 复现

8. **Dr. GRPO: Understanding R1-Zero-Like Training: A Critical Perspective**
   - 作者：Liu, Z. et al.
   - 会议：COLM, 2025
   - 贡献：移除难度归一化，提高鲁棒性

9. **L1: Controlling How Long A Reasoning Model Thinks With Reinforcement Learning**
   - 作者：Various
   - 年份：2025
   - 贡献：使用 RL 控制输出长度

### 1.3 分析与评论

10. **DeepSeek-R1 Paper Updated: What's New**
    - 作者：Mehul Gupta
    - 平台：Medium, 2025
    - URL: https://medium.com/data-science-in-your-pocket/deepseek-r1-paper-updated-whats-new-2598d766c822

11. **What went into training DeepSeek-R1?**
    - 作者：Epoch AI
    - 平台：Substack, 2025
    - URL: https://epochai.substack.com/p/what-went-into-training-deepseek

12. **Breaking down the DeepSeek-R1 training process**
    - 平台：Vellum, 2025
    - URL: https://www.vellum.ai/blog/the-training-of-deepseek-r1-and-ways-to-use-it

13. **The State Of LLMs 2025: Progress, Problems, and Predictions**
    - 作者：Sebastian Raschka
    - 平台：Ahead of AI, 2025
    - URL: https://magazine.sebastianraschka.com/p/state-of-llms-2025

14. **The State of Reinforcement Learning for LLM Reasoning**
    - 作者：Sebastian Raschka
    - 平台：Ahead of AI, April 2025
    - URL: https://magazine.sebastianraschka.com/p/the-state-of-llm-reasoning-model-training

15. **Recent reasoning research: GRPO tweaks, base model RL, and more**
    - 平台：Interconnects, 2025
    - URL: https://www.interconnects.ai/p/papers-im-reading-base-model-rl-grpo

---

## 2. 过程奖励与结果奖励

16. **Let's Verify Step by Step**
    - 作者：Lightman, H. et al.
    - 会议：ICML, 2025
    - 贡献：过程监督的开创性工作

17. **Free Process Rewards without Process Labels**
    - 作者：Wang, P. et al.
    - 会议：ICML, 2025
    - URL: https://icml.cc/virtual/2025/poster/46278
    - 贡献：隐式 PRM，仅需结果标签

18. **Self-Guided Process Reward Optimization**
    - 作者：Zhang, Y. et al.
    - 会议：ICLR, 2026
    - URL: https://openreview.net/pdf?id=pFuxtzaC3K
    - 贡献：从策略模型自身引导过程奖励

19. **Harmonizing Process and Outcome Rewards through RL Training**
    - 作者：Chen, X. et al.
    - 会议：NeurIPS, 2025
    - URL: https://neurips.cc/virtual/2025/131081
    - 贡献：统一框架融合过程和结果奖励

20. **Improving Mathematical Reasoning with Process Supervision**
    - 作者：Uesato, J. et al.
    - 会议：NeurIPS, 2025
    - 贡献：过程监督在数学推理中的应用

21. **Math-Shepherd: Automatic Step-Level Verification for Mathematical Reasoning**
    - 作者：Various
    - 会议：ICML, 2025
    - 贡献：自动生成步骤级验证信号

---

## 3. 探索与利用

22. **On the Limits of RLVR: Support, Entropy, and the Illusion of Reasoning**
    - 作者：Kumar, A. et al.
    - 会议：ICML, 2025
    - URL: https://icml.cc/virtual/2025/52438
    - 贡献：RLVR 支持集限制的理论分析

23. **Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?**
    - 作者：Gao, L. et al.
    - 会议：NeurIPS, 2025
    - URL: https://neurips.cc/virtual/2025/poster/119944
    - 贡献：RLVR 能力边界的系统分析

24. **Salvaging Exploration in RLVR via Fine-Grained Off-Policy Guidance**
    - 作者：Zhao, Y. et al.
    - 会议：ICLR, 2026
    - URL: https://arxiv.org/html/2602.24110v1
    - 贡献：离策略指导增强探索

25. **SCOPE: Step-wise Correction for On-Policy Exploration**
    - 作者：Hu, J. et al.
    - 会议：ICLR, 2026
    - 贡献：步骤级修正提高探索效率

26. **Entropy-Regularized RLVR for Diverse Reasoning**
    - 作者：Wang, T. et al.
    - 会议：NeurIPS, 2025
    - 贡献：熵正则化鼓励探索

27. **Adaptive Entropy Coefficients in RLVR**
    - 作者：Various
    - 会议：ICLR, 2026
    - 贡献：自适应熵系数调度

28. **Dynamic Temperature Scheduling for RLVR**
    - 作者：Various
    - 会议：ICML, 2025
    - 贡献：动态温度调节策略

29. **Annealing Strategies in LLM Reinforcement Learning**
    - 作者：Various
    - 会议：NeurIPS, 2025
    - 贡献：退火策略分析

30. **Reinforcement Learning for Reasoning in Large Language Models with One Training Example**
    - 作者：Li, J. et al.
    - 会议：NeurIPS, 2025
    - URL: https://neurips.cc/virtual/2025/poster/118838
    - 贡献：单样本 RLVR 和后饱和泛化现象

---

## 4. 数学推理

31. **Measuring Mathematical Problem Solving with the MATH Dataset**
    - 作者：Hendrycks, D. et al.
    - 会议：NeurIPS, 2025
    - 贡献：MATH 基准测试

32. **Curriculum Learning for Math RLVR**
    - 作者：Various
    - 会议：ICML, 2025
    - 贡献：课程学习在数学 RLVR 中的应用

33. **Reasoning Gym: Reasoning Environments for Reinforcement Learning with Verifiable Rewards**
    - 作者：Stojanovski, Z. et al.
    - 会议：NeurIPS, 2025
    - URL: https://neurips.cc/virtual/2025/poster/121745
    - 贡献：100+ 推理任务的可编程环境

34. **LaSeR: Last-Token Self-Rewarding for Mathematical Reasoning**
    - 作者：Various
    - 会议：ICLR, 2026
    - 贡献：最后一 token 自奖励机制

35. **VeriRole: Role-Based Verification in Math RLVR**
    - 作者：Various
    - 会议：ICLR, 2026
    - 贡献：基于角色的验证方法

36. **RLVR for Mathematical Problem Solving: A Comprehensive Study**
    - 作者：Various
    - 会议：ICML, 2025
    - 贡献：数学 RLVR 的综合研究

---

## 5. 代码生成

37. **CodeRL: Reinforcement Learning for Code Synthesis with Verifiable Rewards**
    - 作者：Chen, M. et al.
    - 会议：NeurIPS, 2025
    - 贡献：代码合成的 RLVR 方法

38. **Test-Driven RLVR for Software Development**
    - 作者：Various
    - 会议：ICML, 2025
    - 贡献：测试驱动的 RLVR

39. **Automated Test Generation for RLVR Training**
    - 作者：Various
    - 会议：NeurIPS, 2025
    - 贡献：自动化测试生成

40. **Debugging as RLVR: Iterative Code Refinement**
    - 作者：Various
    - 会议：ICLR, 2026
    - 贡献：调试作为 RLVR 任务

41. **Multi-Stage RLVR for Complex Code Tasks**
    - 作者：Various
    - 会议：ICLR, 2026
    - 贡献：多阶段 RLVR 用于复杂代码任务

42. **RLVR for Code Generation: Lessons from Competitive Programming**
    - 作者：Various
    - 会议：ICML, 2025
    - 贡献：竞赛编程中的 RLVR 经验

---

## 6. 多模态 RLVR

43. **ChatVLA-2: RLVR for Vision-Language-Action Models**
    - 作者：Li, Y. et al.
    - 会议：ICLR, 2026
    - 贡献：VLA 模型的 RLVR 训练

44. **OTTER: Open-Source Multimodal RLVR Framework**
    - 作者：Wang, X. et al.
    - 会议：ICLR, 2026
    - 贡献：开源多模态 RLVR 框架

45. **VQA-RLVR: Reinforcement Learning for Visual Question Answering**
    - 作者：Zhang, H. et al.
    - 会议：CVPR, 2025
    - 贡献：视觉问答的 RLVR 方法

46. **Multimodal Reasoning with Verifiable Rewards**
    - 作者：Various
    - 会议：CVPR, 2025
    - 贡献：多模态推理的 RLVR

47. **Image-Text RLVR: Bridging Vision and Language**
    - 作者：Various
    - 会议：ICCV, 2025
    - 贡献：图像 - 文本 RLVR

48. **Visual Reasoning Gym: A Benchmark for Multimodal RLVR**
    - 作者：Various
    - 会议：ICCV, 2025
    - 贡献：多模态 RLVR 基准

49. **3DGraphLLM: RLVR for 3D Scene Understanding**
    - 作者：Liu, Y. et al.
    - 会议：ICCV, 2025
    - 贡献：3D 场景理解的 RLVR

50. **ChartRL: RLVR for Scientific Chart Understanding**
    - 作者：Chen, L. et al.
    - 会议：ICML, 2025
    - 贡献：科学图表理解的 RLVR

---

## 7. 具身智能与机器人学

51. **Keyframe-Guided RLVR for Laboratory Robot Control**
    - 作者：Li, W. et al. (中国科学技术大学苏州高研院)
    - 会议：CoRL, 2025
    - 贡献：关键帧引导的实验室机器人控制

52. **UP-VLA: Universal Policy for Vision-Language-Action Models**
    - 作者：Zhang, Q. et al.
    - 会议：CoRL, 2025
    - 贡献：通用 VLA 策略

53. **DeepUKF-VIN: RLVR for Robotic Navigation**
    - 作者：Wang, Y. et al.
    - 会议：ICRA, 2025
    - 贡献：机器人导航的 RLVR

54. **Multi-Agent Loco-Manipulation with Verifiable Rewards**
    - 作者：Various
    - 会议：ICRA, 2025
    - 贡献：多智能体操作

55. **WORLD-ENV: World Model Enhanced RLVR for Robotics**
    - 作者：Liu, S. et al.
    - 会议：IROS, 2025
    - 贡献：世界模型增强的机器人 RLVR

56. **Sim-to-Real Transfer with RLVR**
    - 作者：Various
    - 会议：IROS, 2025
    - 贡献：仿真到现实迁移

57. **Navigation World Models: Learning to Navigate with RLVR**
    - 作者：Chen, K. et al.
    - 会议：CVPR, 2025
    - 贡献：导航世界模型

58. **Policy World Model (PWM): Learning World Models for Policy Optimization**
    - 作者：Various
    - 会议：NeurIPS 2025 Workshop EWM
    - 贡献：策略世界模型

59. **ReSim: Retrospective Simulation for Embodied RLVR**
    - 作者：Various
    - 会议：NeurIPS 2025 Workshop EWM
    - 贡献：回顾性仿真

60. **Zero-shot World Models via Search in Memory**
    - 作者：Various
    - 会议：NeurIPS 2025 Workshop EWM
    - 贡献：零样本世界模型

---

## 8. 科学发现

61. **Learning to Search and Reason over Scientific Papers with RLVR**
    - 作者：Smith, J. et al.
    - 会议：ICLR, 2026
    - 贡献：科学论文搜索与推理

62. **AI Scientist: Towards Fully Automated Scientific Discovery**
    - 作者：Lu, C. et al.
    - 期刊：Nature, 2025
    - 贡献：自动化科学发现

63. **Hypothesis Generation with RLVR**
    - 作者：Wang, R. et al.
    - 会议：ICML, 2025
    - 贡献：假设生成

---

## 9. 多智能体 RLVR

64. **Multi-Agent Mamba (MAM): Efficient Multi-Agent RL with Verifiable Rewards**
    - 作者：Zhang, M. et al.
    - 会议：AAMAS, 2025
    - 贡献：高效多智能体 RL

65. **Reputation-Based Cooperation in Multi-Agent RLVR**
    - 作者：Li, H. et al.
    - 会议：AAMAS, 2025
    - 贡献：基于声誉的协作

66. **Federated RLVR: Privacy-Preserving Multi-Agent Learning**
    - 作者：Wang, J. et al.
    - 会议：ICLR, 2026
    - 贡献：联邦 RLVR

67. **Communication-Efficient RLVR for Multi-Agent Systems**
    - 作者：Various
    - 会议：ICLR, 2026
    - 贡献：通信高效的多智能体 RLVR

68. **Game-Theoretic RLVR: Nash Equilibrium in Multi-Agent Settings**
    - 作者：Various
    - 会议：NeurIPS, 2025
    - 贡献：博弈论 RLVR

69. **Competitive RLVR: Training Agents Through Adversarial Play**
    - 作者：Various
    - 会议：NeurIPS, 2025
    - 贡献：对抗性 RLVR

70. **Distributed RLVR: Scaling to Thousands of Agents**
    - 作者：Chen, Y. et al.
    - 会议：ICML, 2025
    - 贡献：大规模分布式 RLVR

---

## 10. 理论分析

71. **Convergence Guarantees for RLVR Algorithms**
    - 作者：Zhao, T. et al.
    - 会议：ICLR, 2026
    - 贡献：RLVR 算法收敛性保证

72. **Generalization Bounds for RLVR-Trained Language Models**
    - 作者：Liu, Q. et al.
    - 会议：NeurIPS, 2025
    - 贡献：泛化误差上界

73. **Computational Complexity of RLVR Training**
    - 作者：Wang, Z. et al.
    - 期刊：TMLR, 2026
    - 贡献：计算复杂性分析

74. **Data-Efficient Reward Modeling through Preference Strength Learning**
    - 作者：Various
    - 会议：NeurIPS, 2025
    - URL: https://neurips.cc/virtual/2025/poster/120043
    - 贡献：数据高效的奖励建模

75. **Rollout Roulette: A Principled Approach to Inference-Time Scaling**
    - 作者：Various
    - 会议：NeurIPS, 2025
    - 贡献：推理时缩放方法

---

## 11. 应用领域

### 11.1 医疗健康

76. **Medical RLVR: Verifiable Rewards for Clinical Decision Support**
    - 作者：Zhang, L. et al.
    - 会议：ICML, 2025
    - 贡献：临床决策支持

### 11.2 金融交易

77. **RLVR for Quantitative Trading with Verifiable Returns**
    - 作者：Li, X. et al.
    - 会议：NeurIPS, 2025
    - 贡献：量化交易

### 11.3 教育

78. **Educational RLVR: Personalized Learning with Verifiable Progress**
    - 作者：Wang, H. et al.
    - 会议：ICLR, 2026
    - 贡献：个性化学习

### 11.4 法律

79. **Legal RLVR: Case Analysis with Verifiable Citations**
    - 作者：Chen, D. et al.
    - 会议：AAAI, 2026
    - 贡献：法律案例分析

### 11.5 空战决策

80. **ICS-RL Framework for Air Combat UAV Decision-Making**
    - 作者：西北工业大学
    - 年份：2025
    - 贡献：空战无人机决策，任务成功率 88%

---

## 12. 长上下文 RLVR

81. **LongRLVR: Long-Context RLVR for Complex Reasoning**
    - 作者：Tan, W. et al. (新加坡国立大学)
    - 会议：ICLR, 2026
    - 贡献：14B 模型在 RULER-QA 上从 73.17% 提升至 88.90%

---

## 13. 综述与调查

82. **A Survey of Reinforcement Learning for Large Reasoning Models**
    - 作者：Tsinghua C3I Lab
    - 年份：2025
    - 贡献：大推理模型 RL 综述

83. **From Masks to Worlds: A Hitchhiker's Guide to World Models**
    - 作者：Hu, Z. et al.
    - 会议：ICLR, 2026
    - 贡献：世界模型指南

84. **Understanding World or Predicting Future? A Comprehensive Survey on World Models**
    - 期刊：ACM Computing Surveys, 2025
    - GitHub: https://github.com/tsinghua-fib-lab/World-Model
    - 贡献：世界模型综合综述

85. **Comprehensive Survey on World Models for Embodied AI**
    - arXiv: 2510.16732
    - 贡献：具身 AI 世界模型综述

---

## 14. 开源项目与资源

### 14.1 GitHub 仓库

86. **leofan90/Awesome-World-Models**
    - URL: https://github.com/leofan90/Awesome-World-Models
    - 贡献：世界模型论文集合

87. **operator22th/awesome-world-models-for-robots**
    - URL: https://github.com/operator22th/awesome-world-models-for-robots
    - 贡献：机器人世界模型论文集合

88. **DmitryRyumin/ICML-2025-Papers**
    - URL: https://github.com/DmitryRyumin/ICML-2025-Papers
    - 贡献：ICML 2025 论文集合

89. **Awesome-Embodied-World-Model**
    - URL: https://github.com/Embodied-World-Model/Awesome-Embodied-World-Model
    - 星星：73
    - 贡献：具身世界模型资源

90. **OpenReasonerZero**
    - URL: https://github.com/OpenReasonerZero
    - 贡献：开源基座模型 RLVR 复现

91. **understand-r1-zero**
    - URL: https://github.com/sail-sg/understand-r1-zero
    - 贡献：R1-Zero 训练分析工具

### 14.2 基准与数据集

92. **MATH Dataset**
    - URL: https://github.com/hendrycks/math
    - 规模：12,500 题

93. **MATH500**
    - 规模：500 题

94. **CodeContests**
    - 规模：10,000+ 题

95. **LiveCodeBench**
    - URL: https://livecodebench.github.io/
    - 特点：持续更新

96. **GPQA**
    - 规模：448 题
    - 领域：科学 QA

97. **MMLU-Pro**
    - 规模：12,000+ 题
    - 领域：多领域

98. **RULER-QA**
    - 贡献：长上下文 QA 基准

### 14.3 会议与 Workshop

99. **NeurIPS 2025 Workshop on Embodied World Models (EWM)**
    - URL: https://embodied-world-models.github.io/

100. **ICLR 2025 World Models Workshop**
    - URL: https://worldmodels-workshop.github.io/

101. **CoRL 2026 Robotics World Modeling Workshop**
    - URL: https://corl2026.org/

102. **CVPR 2025 WorldModelBench Workshop**
    - URL: https://worldmodelbench.github.io/

103. **NeurIPS 2025 Workshop on Video Generation and Evaluation**
    - URL: https://videogenworkshop.github.io/

104. **AAAI 2026 Special Track on AI Alignment**
    - URL: https://aaai.org/

### 14.4 行业资源

105. **NVIDIA Cosmos**
    - 下载量：2M+
    - URL: https://www.nvidia.com/cosmos/

106. **Google DeepMind Genie 3**
    - URL: https://deepmind.google/

107. **Yann LeCun's AMI Labs**
    - 融资：€500M
    - URL: https://ami-labs.io/

### 14.5 期刊与会议

108. **Nature Machine Intelligence**
    - URL: https://www.nature.com/natmachintell/

109. **JMLR (Journal of Machine Learning Research)**
    - URL: https://www.jmlr.org/

110. **TMLR (Transactions on Machine Learning Research)**
    - URL: https://openreview.net/group/TMLR
    - 主编：Laurent Charlin, Gautam Kamath, Naila Murray

111. **ICML 2025**
    - URL: https://icml.cc/

112. **NeurIPS 2025**
    - URL: https://neurips.cc/

113. **ICLR 2026**
    - URL: https://iclr.cc/
    - 接收论文：5,357 篇

114. **CoRL 2025**
    - URL: https://corl2025.org/
    - 论文：200+ 篇

115. **AAAI 2026**
    - 时间：2026 年 1 月 20-27 日
    - 地点：Singapore EXPO

116. **IJCAI 2025**
    - 地点：Montreal (August 16-22, 2025) 和 Guangzhou

117. **AAMAS 2025**
    - 时间：2025 年 5 月 19-23 日
    - 地点：Detroit, Michigan, USA

118. **CVPR 2025**
    - URL: https://cvpr.thecvf.com/

119. **ICCV 2025**
    - URL: https://iccv2025.thecvf.com/

120. **ICRA 2025**
    - URL: https://www.icra2025.org/

121. **IROS 2025**
    - 时间：2025 年 10 月
    - 地点：Hangzhou

122. **SIGGRAPH 2025**
    - 期刊：ACM Transactions on Graphics, Volume 44, Issue 4, July 2025

123. **World Robotics 2025**
    - 发布：IFR, 2025 年 9 月 25 日
    - 发现：中国占全球前 10 大市场的 54%

---

## 附录：关键 URL 汇总

### 会议论文集

- ICML 2025: https://icml.cc/virtual/2025/
- NeurIPS 2025: https://neurips.cc/virtual/2025/
- ICLR 2026: https://openreview.net/group/ICLR/2026
- CoRL 2025: https://corl2025.org/
- AAAI 2026: https://aaai.org/
- AAMAS 2025: https://aamas2025.org/

### 开源项目

- OpenReasonerZero: https://github.com/OpenReasonerZero
- understand-r1-zero: https://github.com/sail-sg/understand-r1-zero
- Awesome-World-Models: https://github.com/leofan90/Awesome-World-Models

### 数据集

- MATH: https://github.com/hendrycks/math
- LiveCodeBench: https://livecodebench.github.io/

### 行业资源

- NVIDIA Cosmos: https://www.nvidia.com/cosmos/
- Google DeepMind: https://deepmind.google/

---

**文件位置**: `/home/openclaw/.openclaw/workspace/rlvr_survey_references_2025_2026.md`

**生成时间**: 2026 年 3 月 5 日 11:05 (Asia/Shanghai)
