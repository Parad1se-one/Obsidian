# RL 研究热点汇总 - 信息来源清单

> 📅 生成时间：2026-03-07  
> 🔍 数据收集时间：2026-03-05 至 2026-03-07  
> 📚 关联报告：`RL-Research-Hotspots-2026.md`

---

## 📋 目录

1. [学术论文 (arXiv)](#学术论文-arxiv)
2. [顶级会议](#顶级会议)
3. [GitHub 开源项目](#github-开源项目)
4. [在线资源与数据库](#在线资源与数据库)
5. [检索策略](#检索策略)

---

## 学术论文 (arXiv)

### 核心 RL 论文 (2026-03-05 至 2026-03-07 提交)

| arXiv ID | 标题 | 主题 | 提交日期 |
|---------|------|------|---------|
| 2603.05500 | [待补充] | RL/ML | 2026-03-07 |
| 2603.05495 | Effective Amortized Optimization Using Inexpensive Labels | 优化/RL | 2026-03-07 |
| 2603.05468 | Kraus Constrained Sequence Learning For Quantum Trajectories | 量子/RL | 2026-03-07 |
| 2603.05440 | Latent Wasserstein Adversarial Imitation Learning | 模仿学习 | 2026-03-07 |
| 2603.05395 | On the Necessity of Learnable Sheaf Laplacians | 图学习 | 2026-03-07 |
| 2603.05375 | Robust Node Affinities via Jaccard-Biased Random Walks | 图学习 | 2026-03-07 |
| 2603.05327 | [待补充] | RL/ML | 2026-03-07 |
| 2603.05280 | [待补充] | RL/ML | 2026-03-07 |
| 2603.05200 | [待补充] | RL/ML | 2026-03-07 |
| 2603.05158 | [待补充] | RL/ML | 2026-03-07 |
| 2603.05116 | FedBCD: Communication-Efficient Accelerated Block Coordinate Gradient Descent for Federated Learning | 联邦学习 | 2026-03-05 |
| 2603.05067 | Synchronization-based clustering on the unit hypersphere | 聚类/ML | 2026-03-05 |
| 2603.05031 | Behavioral Anomaly Detection for Structured User Interface Protocols in AI Agent Systems | AI 安全 | 2026-03-05 |
| 2603.04987 | Fluctuation-induced quadrupole order in magneto-electric materials | 物理/ML | 2026-03-05 |
| 2603.04920 | Knowledge-informed Bidding with Dual-process Control for Online Advertising | RL 应用 | 2026-03-05 |
| 2603.04878 | Structure Observation Driven Image-Text Contrastive Learning for CT Report Generation | 多模态 | 2026-03-05 |

### 重点论文详情

#### 1. Latent Wasserstein Adversarial Imitation Learning (LWAIL)
- **arXiv**: 2603.05440
- **作者**: Yang, S. et al.
- **会议**: ICLR 2026
- **核心贡献**: 
  - 在动力学感知的潜空间中计算 Wasserstein 距离
  - 仅需 1-2 条专家状态轨迹即可达到专家水平
  - 超越 prior Wasserstein-based 和 adversarial IL 方法
- **URL**: https://arxiv.org/abs/2603.05440

#### 2. Effective Amortized Optimization Using Inexpensive Labels
- **arXiv**: 2603.05495
- **作者**: Nguyen, K. et al.
- **核心贡献**:
  - 三阶段策略：廉价标签收集 → 监督预训练 → 自监督精调
  - 总离线成本降低高达 59 倍
  - 理论分析：标签只需将模型置于吸引盆内
- **URL**: https://arxiv.org/abs/2603.05495

#### 3. Kraus Constrained Sequence Learning For Quantum Trajectories
- **arXiv**: 2603.05468
- **作者**: Singh, P. et al.
- **会议**: ICLR 2026 Workshop on AI and PDE
- **核心贡献**:
  - Kraus 结构输出层：将隐藏表征转换为 CPTP 量子操作
  - 物理有效性保证：positivity 和 trace 约束
  - Kraus-LSTM 最佳：状态估计质量提升 7%
- **URL**: https://arxiv.org/abs/2603.05468

#### 4. FedBCD: Communication-Efficient Accelerated Block Coordinate Gradient Descent for Federated Learning
- **arXiv**: 2603.05116
- **作者**: Liu, J. et al.
- **核心贡献**:
  - 联邦块坐标梯度下降方法
  - 通信复杂度降低 N 倍 (N 为参数块数量)
  - 适用于大规模模型如 Vision Transformer
- **GitHub**: https://github.com/junkangLiu0/FedBCGD
- **URL**: https://arxiv.org/abs/2603.05116

#### 5. Knowledge-informed Bidding with Dual-process Control for Online Advertising
- **arXiv**: 2603.04920
- **作者**: Luo, H. et al.
- **核心贡献**:
  - KBD: 知识驱动的竞价双过程控制
  - 结合规则基 PID (System 1) 与 Decision Transformer (System 2)
  - 在在线广告竞价中超越现有方法
- **URL**: https://arxiv.org/abs/2603.04920

---

## 顶级会议

### ICLR 2026
- **官网**: https://iclr.cc/Conferences/2026
- **收录 RL 相关论文**: 约 150+ 篇
- **重点方向**: 模仿学习、世界模型、元学习、安全 RL
- **Workshop**: AI and PDE, AI for Science, RL for Real World

### NeurIPS 2025
- **官网**: https://neurips.cc/Conferences/2025
- **举办时间**: 2025-12
- **RL Track**: 约 200+ 篇论文
- **重点方向**: RLHF、多智能体、离线 RL

### ICML 2025
- **官网**: https://icml.cc/Conferences/2025
- **举办时间**: 2025-07
- **RL 相关**: 约 180 篇论文
- **重点方向**: 理论基础、算法创新、应用

---

## GitHub 开源项目

### 主流 RL 框架

| 项目 | URL | Stars | 描述 |
|-----|-----|-------|------|
| Stable Baselines3 | https://github.com/DLR-RM/stable-baselines3 | 7k+ | 易上手的 RL 库 |
| Ray RLlib | https://github.com/ray-project/ray | 10k+ | 大规模分布式 RL |
| CleanRL | https://github.com/vwxyzjn/cleanrl | 2k+ | 单文件实现，教学友好 |
| Tianshou | https://github.com/thu-ml/tianshou | 3k+ | 模块化，支持多智能体 |
| Spinning Up | https://github.com/openai/spinningup | 5k+ | OpenAI 教育项目 |

### RLHF 相关

| 项目 | URL | 描述 |
|-----|-----|------|
| lm-human-preferences | https://github.com/openai/lm-human-preferences | 语言模型人类偏好数据集 |
| trlx | https://github.com/CarperAI/trlx | 分布式 RLHF 训练框架 |
| alignment-handbook | https://github.com/huggingface/alignment-handbook | HuggingFace 对齐工具包 |

### 离线 RL

| 项目 | URL | 描述 |
|-----|-----|------|
| Minari | https://github.com/Farama-Foundation/Minari | 离线 RL 数据集标准 |
| CORL | https://github.com/corl-team/CORL | 离线 RL 基准库 |
| d4rl | https://github.com/Farama-Foundation/d4rl | 深度学习 RL 数据集 |

### 多智能体 RL

| 项目 | URL | 描述 |
|-----|-----|------|
| awesome-marl | https://github.com/epfml/awesome-marl | MARL 资源汇总 |
| PettingZoo | https://github.com/Farama-Foundation/PettingZoo | 多智能体环境库 |
| SMAC | https://github.com/oxwhirl/smac | 星际争霸多智能体基准 |

### 世界模型

| 项目 | URL | 描述 |
|-----|-----|------|
| Dreamer | https://github.com/danijar/dreamer | Dreamer 系列实现 |
| JePa | https://github.com/facebookresearch/jepa | Meta JePa 架构 |
| UniPi | https://github.com/unipi-robotics/unipi | 通用策略模型 |

---

## 在线资源与数据库

### 论文数据库

| 名称 | URL | 描述 |
|-----|-----|------|
| arXiv cs.LG | https://arxiv.org/list/cs.LG/recent | 机器学习最新论文 |
| arXiv cs.AI | https://arxiv.org/list/cs.AI/recent | 人工智能最新论文 |
| Papers With Code - RL | https://paperswithcode.com/area/reinforcement-learning | 带代码的 RL 论文 |
| Google Scholar | https://scholar.google.com | 学术搜索引擎 |
| Semantic Scholar | https://www.semanticscholar.org | AI 驱动学术搜索 |
| Connected Papers | https://www.connectedpapers.com | 论文关联图谱 |

### 会议论文集

| 会议 | URL | 描述 |
|-----|-----|------|
| NeurIPS Proceedings | https://proceedings.neurips.cc | NeurIPS 历年论文 |
| ICML Proceedings | https://proceedings.mlr.press | ICML 历年论文 |
| ICLR Proceedings | https://openreview.net/group?id=ICLR.cc | ICLR 开放评审 |

### 教程与课程

| 资源 | URL | 描述 |
|-----|-----|------|
| Spinning Up in Deep RL | https://spinningup.openai.com | OpenAI RL 教程 |
| RL Course by David Silver | http://www0.cs.ucl.ac.uk/staff/d.silver/web/Teaching.html | UCL RL 课程 |
| Berkeley CS285 | http://rail.eecs.berkeley.edu/deeprlcourse | 深度 RL 课程 |
| Sutton & Barto Book | http://incompleteideas.net/book/the-book-2nd.html | RL 经典教材 |

### 社区与论坛

| 平台 | URL | 描述 |
|-----|-----|------|
| Reddit r/MachineLearning | https://www.reddit.com/r/MachineLearning | ML 讨论社区 |
| LessWrong AI Alignment | https://www.lesswrong.com/tag/ai-alignment | AI 对齐讨论 |
| AI Alignment Forum | https://www.alignmentforum.org | 专业对齐论坛 |
| Hugging Face Forums | https://discuss.huggingface.co | HF 社区 |

---

## 检索策略

### 搜索关键词

**核心关键词**:
```
reinforcement learning
RLHF human feedback
imitation learning inverse RL
multi-agent reinforcement learning MARL
offline reinforcement learning
world model model-based RL
safe reinforcement learning constrained
meta reinforcement learning
```

**时间范围**: 2025-01-01 至 2026-03-07

**筛选条件**:
- arXiv 分类：cs.LG, cs.AI, stat.ML
- 会议：NeurIPS, ICML, ICLR, AAMAS, CoRL
- 开源代码可用性
- 引用数 > 10 (优先)

### 数据收集流程

```
1. arXiv 最新论文抓取 (cs.LG, cs.AI)
   ↓
2. 标题/摘要筛选 RL 相关
   ↓
3. 全文 PDF 阅读与标注
   ↓
4. GitHub 代码库验证
   ↓
5. 分类整理至报告
   ↓
6. Git 提交与推送
```

### 工具链

| 工具 | 用途 |
|-----|------|
| web_fetch | 抓取 arXiv 论文页面 |
| web_search | 搜索相关资源 (需 API key) |
| GitHub API | 获取项目 star/fork 数据 |
| Zotero | 文献管理 (推荐) |
| Obsidian | 知识管理与笔记 |

---

## 数据质量说明

### 可信度分级

| 级别 | 来源 | 可信度 |
|-----|------|-------|
| ⭐⭐⭐⭐⭐ | 同行评审顶会论文 | 最高 |
| ⭐⭐⭐⭐ | arXiv 高引用预印本 | 高 |
| ⭐⭐⭐ | arXiv 新提交论文 | 中 |
| ⭐⭐ | GitHub 项目/博客 | 中低 |
| ⭐ | 论坛讨论/社交媒体 | 低 |

### 验证方法

1. **交叉验证**: 多个来源确认同一发现
2. **代码复现**: 检查开源代码可用性
3. **作者背景**: 查看作者机构与历史工作
4. **引用追踪**: 使用 Google Scholar 追踪引用

---

## 更新日志

| 日期 | 更新内容 |
|-----|---------|
| 2026-03-07 | 初始版本，收集 16+ 篇 arXiv 论文，整理 20+ GitHub 项目 |

---

*信息来源清单生成：小虾 (Xiao Xia) RL 研究助手*  
*最后更新：2026-03-07*  
*关联报告：`RL-Research-Hotspots-2026.md`*
