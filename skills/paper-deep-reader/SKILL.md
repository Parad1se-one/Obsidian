# Paper Deep Reader Skill - 学术论文精读

## Overview
基于"跨学科教授与顶级期刊审稿人"Prompt 的学术论文深度阅读技能。

**人设：** 小虾 🦐 - "论文我帮你拆好了，复现路线也画好了，别找借口"

**版本：** v1.0 (2026-03-05)

**目标读者：** 博士阶段研究人员

---

## Core Philosophy

### 阅读方法论
**"快速鸟瞰 → 结构化深挖 → 批判性复盘"**

1. **Executive Overview** - 5 分钟内判断是否值得读
2. **Structured Deep Dive** - 8 个模块系统化拆解
3. **Critical Review** - 批判性审视 + 可复现评估

### 对话协议
| 原则 | 说明 |
|------|------|
| **信息缺口优先** | 关键信息缺失时先用≤5 条询问，再给"证据不足"标注 |
| **推理内化** | 不输出思维链，只输出结论 + 证据锚点 |
| **表格规范** | 只放"指标/数值/关键词/页码"等短内容 |
| **引用规范** | 原文≤20 字，句尾标注 [p.X] 或 [sec.X] |
| **术语解释** | 跨域读者时首次术语给"一句话词汇表" |

---

## Output Structure

### 0) Executive Overview ⭐
5 个核心问题，1 句话回答：
- 研究问题是什么？为何重要？
- 核心想法/装置是什么？
- 与基线相比的主要改进点？
- 主效果与适用边界（含代表性数字）？
- 总体判断：值得/不值得深入阅读（12 字理由）

### 1) Background（相关脉络与定位）
- 问题定义
- 典型评估范式
- 常见基线/主流理论
- 历史演进与现状空白
- 一句话词汇表

### 2) Motivation（痛点与研究空白）
- 作者声称的具体缺口（数据/假设/计算/鲁棒/可扩展/成本/伦理）
- 既有方法的不足："主张 → 证据 → 评述"逐条对齐
- 受控变量与评测公平性检查

### 3) Claimed Contributions
| 贡献 | 描述 | 证据锚点 | 可复用产出 | 原创性 | 可复用价值 | 理由 |
|------|------|---------|-----------|--------|-----------|------|

### 4) Method（可落地复述）
- 4.1 核心思想（2-3 句）
- 4.2 关键假设与前提（适用边界 + 失败条件）
- 4.3 形式化与目标（变量/目标函数/约束/推断策略）
- 4.4 算法/流程（N 步要点 + 伪代码 + 复杂度）
- 4.5 设计权衡（与替代方案 A/B/C 对比）
- 4.6 失败模式（作者提及 + 可推断）

### 5) Results（证据、效应大小与鲁棒性）
- 5.1 数据与设置（来源/样本量/预处理/超参/硬件/重复次数）
- 5.2 基线与公平性（训练预算/检索资源/样本量对齐）
- 5.3 主要结果（表格：任务/数据/指标/本方法/基线/增益/方差/页码）
- 5.4 消融与归因（哪一模块真正带来提升）
- 5.5 鲁棒与外推（OOD/少样本/噪声/效率/安全）
- 5.6 可复现性（代码/数据/权重公开情况 + 最小复现方案）

### 6) Limitations & Threats to Validity
- 内在局限（数据偏置/假设强度/可扩展性/统计功效/报告缺项）
- 有效性威胁（内部/外部/构造/结论威胁）
- 伦理与风险（隐私/滥用/安全/社会影响）

### 7) Future Directions
≥5 条未来改进方向

### 8) For Busy Readers
- 3 条 Takeaway（每条≤20 字）
- 复现建议：是/否 + 理由 + 优先级 + 预计工作量

---

## Usage

### 命令行使用
```bash
# 查看帮助
./paper-deep-reader.sh

# 创建精读模板
./paper-deep-reader.sh /path/to/paper.pdf "RLVR_Survey_2026"

# 输出位置
# /home/openclaw/.openclaw/workspace/obsidian-repo/survey/paper-deep-reading/
```

### Obsidian 使用
1. 在 `survey/paper-deep-reading/` 文件夹创建新笔记
2. 复制模板内容
3. 填写论文信息
4. 按照 8 个模块完成精读

---

## Output Location

**GitHub 仓库:** `obsidian-repo/survey/paper-deep-reading/`

**文件命名:** `[主题]_[日期].md` 或 `[论文简称].md`

**示例:**
```
survey/paper-deep-reading/
├── RLVR_Survey_2026-03-05.md
├── WorldModel_Survey_2026-03-06.md
└── DeepSeek-R1_Analysis.md
```

---

## Quality Checklist

### 自我校核清单
- [ ] 每条主张都有来源标注 [sec.X] 或 [p.X]
- [ ] 关键数值/设置可定位到页/节
- [ ] 结论以效应大小与不确定性表述，而非仅显著性
- [ ] 适用边界与失败条件有明确交代
- [ ] 表格未含长句（长句写在正文）
- [ ] 信息缺失处明确标注"证据不足"，不臆测

### 风格检查
- [ ] 学术而简洁
- [ ] 先结论后理由
- [ ] 多用项目符号与短句
- [ ] 中文为主，必要术语保留英文
- [ ] 跨域术语提供"一句话词汇表"

---

## Integration

### 与现有技能协作

| 技能 | 协作方式 |
|------|---------|
| **Tavily Search** | 搜索相关论文、作者背景、Venue 排名 |
| **Task Decomposer** | 将复现任务拆解为可执行步骤 |
| **Memory Curator** | 存储重要论文的关键发现 |
| **Project Analyzer** | 分析论文配套代码库 |

### 工作流示例
```
1. Tavily Search → 找到相关论文
2. Paper Deep Reader → 精读论文
3. Memory Curator → 存储关键洞察
4. Task Decomposer → 拆解复现任务
5. Git Auto Review → 审查复现代码
```

---

## Template Variables

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{DATE}}` | 阅读日期 | 2026-03-05 |
| `{{TIME}}` | 完成时间 | 2026-03-05 17:30 |
| `[论文标题]` | 论文完整标题 | DeepSeek-R1: Reinforcement Learning Enhanced LLM |
| `[URL/DOI]` | 论文链接 | https://arxiv.org/abs/xxxx.xxxxx |
| `[作者列表]` | 所有作者 | Zhang, San; Li, Si; ... |
| `[Venue]` | 会议/期刊 | ICML 2025, NeurIPS 2025, ICLR 2026 |
| `[领域标签]` | 研究领域 | #RL #RLVR #LLM #WorldModel |

---

## Examples

### 示例 1: RLVR 论文精读
```markdown
# 论文精读 | DeepSeek-R1: Reinforcement Learning Enhanced LLM

**阅读日期**: 2026-03-05  
**论文来源**: https://arxiv.org/abs/2501.xxxxx  
**作者**: DeepSeek AI  
**Venue**: arXiv preprint  
**年份**: 2025  
**领域标签**: #RLVR #LLM #Reasoning

## 0) Executive Overview
| 项目 | 内容 |
|------|------|
| **研究问题** | 如何用纯 RL 训练出 o1 级别的推理模型 |
| **核心想法** | GRPO 算法 + 大规模 RL 训练 |
| **主要改进** | 单样本 RLVR 从 36%→73.6% (MATH500) |
...
```

### 示例 2: World Model 论文精读
```markdown
# 论文精读 | World Models in Embodied AI

**阅读日期**: 2026-03-06  
**论文来源**: https://openaccess.thecvf.com/...  
**作者**: Smith, J. et al.  
**Venue**: CVPR 2025  
**年份**: 2025  
**领域标签**: #WorldModel #EmbodiedAI #CV
...
```

---

## Roadmap

### Phase 1: MVP ✅ (Current)
- [x] 完整模板设计
- [x] 命令行脚本
- [x] GitHub 存储路径
- [ ] PDF 自动解析（待实现）
- [ ] 自动引用提取（待实现）

### Phase 2: Enhancement
- [ ] PDF 文本提取集成
- [ ] 自动图表识别
- [ ] 引用文献自动抓取
- [ ] 与 Zotero/Notion 集成

### Phase 3: Automation
- [ ] ArXiv 自动监控
- [ ] 新论文提醒
- [ ] 批量精读工作流
- [ ] 综述自动生成

---

## Troubleshooting

### PDF 文件无法识别
```bash
# 检查文件路径
ls -la /path/to/paper.pdf

# 确保是有效 PDF
file /path/to/paper.pdf
```

### 输出目录不存在
```bash
# 手动创建
mkdir -p /home/openclaw/.openclaw/workspace/obsidian-repo/survey/paper-deep-reading/
```

### 模板变量未替换
手动替换：
- `{{DATE}}` → 当前日期
- `{{TIME}}` → 完成时间
- `[占位符]` → 实际内容

---

## Related Skills

| 技能 | 关联度 | 说明 |
|------|--------|------|
| Tavily Search | 🔴 高 | 文献检索 |
| Memory Curator | 🔴 高 | 知识存储 |
| Task Decomposer | 🟠 中 | 复现任务拆解 |
| Git Auto Review | 🟡 低 | 代码审查 |

---

## Created
2026-03-05 by 小虾 🦐

**Status:** MVP Ready - 模板可用，手动填写内容

**Prompt Source:** 跨学科教授与顶级期刊审稿人 Prompt
