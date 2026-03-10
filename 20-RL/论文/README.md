# 学术论文调研报告合集

**生成时间**: 2026-03-05  
**整理者**: Claw (OpenClaw Assistant)

---

## 📁 文件夹结构

```
survey/
├── README.md                          # 本说明文件
├── 01_RL_Survey/                      # 强化学习综述 (2025-2026)
├── 02_RLVR_Survey/                    # RLVR 综述 (2025-2026)
├── 03_World_Models/                   # World Models 综述 (2025-2026)
├── 04_Computer_Vision/                # 计算机视觉论文速递
├── 05_Other_Reports/                  # 其他研究报告
├── 06_Memory_Logs/                    # 每日记忆日志
└── paper-deep-reading/                # 学术论文精读（8 模块框架）
```

---

## 📄 文件清单

### 01_RL_Survey - 强化学习综述
| 文件 | 说明 |
|------|------|
| `rl_survey_2025_2026_final.md` | 主综述文档，118+ 篇论文，45 分钟完成 |
| `rl_survey_references_2025_2026.md` | 完整参考文献列表 |

**覆盖 Venue**: ICML 2025, NeurIPS 2025, ICLR 2026, CoRL 2025, AAAI 2026, IJCAI 2025, JMLR, TMLR, AAMAS 2025

### 02_RLVR_Survey - RLVR 综述
| 文件 | 说明 |
|------|------|
| `rlvr_survey_2025_2026_final.md` | 主综述文档，120+ 篇论文，~25,000 字 |
| `rlvr_survey_references_2025_2026.md` | 完整参考文献列表 |

**核心主题**: DeepSeek-R1, GRPO, 过程奖励 vs 结果奖励，数学推理，代码生成，多模态 RLVR，具身智能，科学发现，多智能体 RLVR

**关键发现**:
- 单样本 RLVR 有效性：1 样本从 36.0% → 73.6% (MATH500)
- 长上下文突破：LongRLVR 在 RULER-QA 上 73.17% → 88.90%

**覆盖 Venue**: ICML 2025, NeurIPS 2025, ICLR 2026, AAAI 2026, CoRL 2025, AAMAS 2025, CVPR 2025, ICCV 2025, ICRA 2025, IROS 2025, Nature, Nature Machine Intelligence, JMLR, TMLR

### 03_World_Models - World Models 综述
| 文件 | 说明 |
|------|------|
| `world_model_survey_2025_2026_final.md` | 主综述文档 |
| `world_model_references_2025_2026.md` | 完整参考文献列表 |

**覆盖方向**: Embodied AI, Video Generation, Planning/Reasoning, Causal, VLA, JEPA/SSL, Autonomous Driving, 3D/4D, Game Playing, Physics Simulation, Human Motion, Multi-Agent, Safety/Alignment

### 04_Computer_Vision - 计算机视觉
| 文件 | 说明 |
|------|------|
| `cv_sota_papers_2026_03.md` | CV SOTA 论文速递 (2026-03) |
| `semantic_segmentation_models.md` | 语义分割模型综述 |
| `computer_vision_models.md` | 计算机视觉模型综述 |

### 05_Other_Reports - 其他报告
| 文件 | 说明 |
|------|------|
| `discorl_nature_2025_review.md` | DiscoRL Nature 2025 综述 |
| `llm_rl_README.md` | LLM+RL 整合研究说明 |
| `limix_survey.md` | Limix 调研报告 |
| `大模型 + 运筹优化前沿研究报告.md` | 大模型与运筹优化交叉领域报告 |

### 06_Memory_Logs - 记忆日志
每日工作日志和学习笔记，包含：
- 每日调研进展
- 重要发现记录
- 配置变更记录

### paper-deep-reading - 学术论文精读
按照"跨学科教授与顶级期刊审稿人"框架完成的深度阅读报告。

**精读框架**: 8 模块结构化分析（Executive Overview → Method → Results → Limitations → Future Directions）

**目标读者**: 博士阶段研究人员

**输出内容**:
- 核心问题与贡献评估
- 方法可落地复述（含伪代码、复杂度）
- 结果效应大小与鲁棒性分析
- 批判性审视（有效性威胁、伦理风险）
- 复现建议与优先级

**使用技能**: `skills/paper-deep-reader/`

---

## 📊 统计信息

| 调研主题 | 论文数量 | 完成时间 | 字数 |
|----------|----------|----------|------|
| RL Survey | 118+ | 45 分钟 | ~20,000 |
| RLVR Survey | 120+ | 45 分钟 | ~25,000 |
| World Models | 进行中 | - | - |
| CV Papers | 20+ | - | - |

---

## 🔧 使用说明

1. 解压 zip 文件到本地
2. 使用 Markdown 阅读器（如 Obsidian、Typora、VS Code）打开文件
3. 建议将 `survey_package` 文件夹导入 Obsidian 知识库

---

## 📝 备注

- 所有论文均来自正式发表的会议/期刊（排除 arXiv preprints）
- 时间范围：2025 年 9 月 - 2026 年 3 月
- 如需更新或补充，请联系 Claw 助手
