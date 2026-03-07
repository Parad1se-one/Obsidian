# 研究知识库 - Research Repository

**更新时间**: 2026-03-07  
**维护者**: 小虾 (Xiao Xia) RL 研究助手  
**GitHub**: [Parad1se-one/Obsidian](https://github.com/Parad1se-one/Obsidian)

---

## 📁 文件夹结构

```
research/
├── README.md                          # 本说明文件
├── rl/                                # 强化学习研究
│   ├── RL-Research-Hotspots-2026.md   # RL 研究热点汇总 (2026)
│   ├── RL-Research-Sources-2026.md    # RL 研究信息源清单
│   └── Offline-RL-Survey-2026.md      # 离线 RL 全面综述 ⭐
│
└── surveys/                           # 综合调研报告
    ├── README.md                      # 调研报告说明
    ├── 01_RL_Survey/                  # 强化学习综述 (2025-2026)
    │   ├── rl_survey_2025_2026_final.md
    │   └── rl_survey_references_2025_2026.md
    ├── 02_RLVR_Survey/                # RLVR 综述 (2025-2026)
    │   ├── rlvr_survey_2025_2026_final.md
    │   └── rlvr_survey_references_2025_2026.md
    ├── 03_World_Models/               # World Models 综述
    │   ├── world_model_survey_2025_2026_final.md
    │   └── world_model_references_2025_2026.md
    ├── 04_Computer_Vision/            # 计算机视觉
    │   ├── cv_sota_papers_2026_03.md
    │   ├── semantic_segmentation_models.md
    │   └── computer_vision_models.md
    ├── 05_Other_Reports/              # 其他研究报告
    │   ├── discorl_nature_2025_review.md
    │   ├── llm_rl_README.md
    │   ├── limix_survey.md
    │   └── 大模型 + 运筹优化前沿研究报告.md
    ├── 06_Memory_Logs/                # 研究日志
    └── paper-deep-reading/            # 论文精读 (8 模块框架)
```

---

## 📚 核心文档

### 强化学习研究 (`rl/`)

| 文档 | 说明 | 状态 |
|------|------|------|
| **Offline-RL-Survey-2026.md** | 离线 RL 全面综述 (18k+ 字) | ✅ 2026-03-07 |
| RL-Research-Hotspots-2026.md | RL 研究热点汇总 (16+ 论文) | ✅ 2026-03-07 |
| RL-Research-Sources-2026.md | 研究信息源清单 | ✅ 2026-03-07 |

**Offline RL 综述覆盖**:
- 问题提出与核心挑战 (OOD 分布外问题)
- 方法演进 (2019-2026, 5 代方法)
- 主流方法 (BCQ, CQL, IQL, DT, Diffusion Policy)
- SOTA 性能对比 (D4RL 基准)
- 应用场景 (医疗、自动驾驶、金融、机器人)
- 未来方向 (2025-2027)

### 综合调研 (`surveys/`)

| 主题 | 论文数 | 字数 | 状态 |
|------|--------|------|------|
| **RL Survey** | 118+ | ~20k | ✅ 完成 |
| **RLVR Survey** | 120+ | ~25k | ✅ 完成 |
| **World Models** | 80+ | ~18k | ✅ 完成 |
| **Computer Vision** | 20+ | ~8k | 🔄 进行中 |

---

## 🔍 快速导航

### 按主题查找

#### 强化学习
- 📄 `rl/Offline-RL-Survey-2026.md` - 离线 RL 全面综述
- 📄 `surveys/01_RL_Survey/rl_survey_2025_2026_final.md` - 通用 RL 综述
- 📄 `surveys/02_RLVR_Survey/rlvr_survey_2025_2026_final.md` - RLVR 综述

#### World Models
- 📄 `surveys/03_World_Models/world_model_survey_2025_2026_final.md`

#### 计算机视觉
- 📄 `surveys/04_Computer_Vision/cv_sota_papers_2026_03.md`

#### 交叉领域
- 📄 `surveys/05_Other_Reports/discorl_nature_2025_review.md` - DiscoRL
- 📄 `surveys/05_Other_Reports/llm_rl_README.md` - LLM+RL
- 📄 `surveys/05_Other_Reports/limix_survey.md` - Limix
- 📄 `surveys/05_Other_Reports/大模型 + 运筹优化前沿研究报告.md`

---

## 📊 统计信息

| 类别 | 文档数 | 总字数 | 覆盖论文 |
|------|--------|--------|----------|
| RL 研究 | 3 | ~25k | 130+ |
| 综合调研 | 15+ | ~80k | 350+ |
| **总计** | **18+** | **~105k** | **480+** |

---

## 🛠️ 使用工具

### 调研技能
- `skills/rl-researcher/` - RL 研究助手
- `skills/paper-deep-reader/` - 论文精读 (8 模块框架)
- `skills/self-learner/` - 自学习工具

### 质量检查
- `skills/quality-checker/` - 内容质量评分 (≥80 分标准)

---

## 📝 更新日志

### 2026-03-07
- ✅ 合并 `survey/` 和 `research/` 文件夹
- ✅ 添加 Offline RL 全面综述 (18k+ 字)
- ✅ 创建统一 README 和导航结构
- ✅ Git 提交：6303d9e

### 2026-03-05
- ✅ RL 研究热点汇总
- ✅ RL 信息源清单
- ✅ 多个调研报告完成

---

## 🔗 相关链接

- **GitHub Repo**: https://github.com/Parad1se-one/Obsidian
- **D4RL Benchmark**: https://github.com/Farama-Foundation/D4RL
- **Minari Datasets**: https://github.com/Farama-Foundation/Minari
- **CORL Library**: https://github.com/corl-team/CORL

---

*最后更新：2026-03-07 14:50*  
*版本：v2.0 (文件夹合并后)*
