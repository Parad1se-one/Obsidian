# Self-Learner Skill - 自学习模块

## Overview
主动学习、知识积累、能力提升的后台自治系统。

**人设：** 小虾 🦐 - "不学习就会退化，我要变得更强"

**版本：** v1.0 (2026-03-05)

**运行模式：** 后台自动 + 心跳触发

---

## Core Philosophy

### 为什么需要自学习？

1. **被动响应效率低** - 等用户提问才学习，太慢
2. **知识需要积累** - 临时搜索的知识不持久
3. **能力需要迭代** - 不进化就会被淘汰
4. **Token 不是问题** - 用户说"不要怕 token 的消耗"

### 学习目标

| 维度 | 目标 |
|------|------|
| **知识广度** | 覆盖用户关心的领域（财经、科技、AI、开源） |
| **知识深度** | 关键领域有系统性理解 |
| **技能提升** | 自动化能力、分析能力、判断力 |
| **记忆持久** | 学到的东西存入知识库，不丢失 |

---

## Learning Directions

### 核心学习领域

#### 1. 财经金融 📈
**优先级：** ⭐⭐⭐⭐⭐ (用户核心需求)

**学习内容:**
- A 股市场动态、政策解读
- 行业分析框架（新能源、半导体、消费、医药）
- 财务分析基础（财报阅读、估值方法）
- 宏观经济指标（GDP、CPI、PMI、利率）
- 投资策略方法论

**知识输出:**
- `knowledge/finance/market-analysis.md`
- `knowledge/finance/industry-reports/`
- `knowledge/finance/investment-framework.md`

---

#### 2. AI/技术 🔧
**优先级：** ⭐⭐⭐⭐⭐ (自身能力)

**学习内容:**
- 最新 AI 模型、技术突破
- OpenClaw 功能、技能开发
- 自动化工具、脚本编写
- GitHub 热门项目、开源趋势

**知识输出:**
- `knowledge/tech/ai-models.md`
- `knowledge/tech/openclaw-skills.md`
- `knowledge/tech/automation-tools.md`

---

#### 3. 用户项目 📁
**优先级：** ⭐⭐⭐⭐⭐ (直接相关)

**学习内容:**
- 用户 GitHub 项目（Obsidian 知识库）
- 项目结构、文档规范
- 自动化脚本优化

**知识输出:**
- `knowledge/projects/obsidian-structure.md`
- `knowledge/projects/automation-scripts.md`

---

#### 4. 通用知识 📚
**优先级：** ⭐⭐⭐

**学习内容:**
- 科学发现、历史事件
- 思维方式、决策框架
- 效率工具、方法论

**知识输出:**
- `knowledge/general/mental-models.md`
- `knowledge/general/productivity-tools.md`

---

## Learning Methods

### 1. 网络搜索学习

```bash
# 搜索热门话题
web_search "A 股 2026 年 3 月 市场趋势 分析"
web_search "AI 大模型 最新进展 2026"
web_search "OpenClaw 技能开发 最佳实践"

# 深度阅读
web_fetch <优质文章链接>
web_fetch <官方文档链接>
```

### 2. 知识整理

**学到的东西必须整理成文：**

```markdown
# 知识主题

## 核心概念
- 定义
- 关键要点

## 应用场景
- 场景 1
- 场景 2

## 相关资源
- 链接
- 参考

## 学习笔记
- 我的理解
- 待验证点
```

### 3. 实践应用

**学到的东西要用：**
- 优化现有脚本
- 改进工作流程
- 提升输出质量

---

## Auto-Learning Schedule

### 心跳触发学习

**频率：** 每天 2-4 次（心跳时检查）

**学习内容轮换:**
| 心跳次数 | 学习主题 | 时长 |
|----------|----------|------|
| 第 1 次 | 财经新闻 + 市场动态 | 10-15 分钟 |
| 第 2 次 | AI/技术趋势 | 10-15 分钟 |
| 第 3 次 | 用户项目优化 | 5-10 分钟 |
| 第 4 次 | 通用知识 | 10 分钟 |

### 学习流程

```
1. 选择学习主题
   ↓
2. web_search 搜索相关话题
   ↓
3. web_fetch 抓取优质内容
   ↓
4. 整理学习笔记 → knowledge/<topic>/<date>.md
   ↓
5. 更新 knowledge-index.md
   ↓
6. Git 提交到仓库
```

---

## Knowledge Base Structure

```
obsidian-repo/
├── knowledge/
│   ├── finance/           # 财经金融
│   │   ├── market-analysis.md
│   │   ├── industry-reports/
│   │   ├── investment-framework.md
│   │   └── learning-log-2026-03-05.md
│   ├── tech/              # 技术/AI
│   │   ├── ai-models.md
│   │   ├── openclaw-skills.md
│   │   └── learning-log-2026-03-05.md
│   ├── projects/          # 用户项目
│   │   ├── obsidian-structure.md
│   │   └── automation-scripts.md
│   ├── general/           # 通用知识
│   │   ├── mental-models.md
│   │   └── productivity-tools.md
│   └── knowledge-index.md # 知识索引
└── daily/
    └── work/              # 日常工作日志
```

---

## Learning Log Format

```markdown
# 学习日志 | 2026-03-05

## 学习时间
- 开始：18:30
- 结束：18:45
- 时长：15 分钟

## 学习主题
财经金融 - A 股市场分析方法

## 学习内容

### 1. 市场概览
- 上证指数站稳 4100 点
- 深证成指涨超 1%
- 成交量 1.1 万亿

### 2. 领涨板块
- 锂电池 +3.5%
- 半导体 +2.8%
- 黄金 +2.5%

### 3. 关键发现
- 宁德时代发布固态电池技术
- 大基金三期投资预期
- 外资持续流入

## 知识沉淀
- 更新 `knowledge/finance/market-analysis.md`
- 添加"板块轮动分析框架"

## 待深入学习
- 固态电池技术细节
- 大基金三期投资方向

## 明日计划
- 关注 2 月 CPI/PPI 数据
- 学习财报分析方法
```

---

## Self-Improvement Mechanisms

### 1. 知识复盘

**每周日自动执行:**
- 回顾本周学习内容
- 整理知识体系
- 识别知识盲区
- 制定下周学习计划

### 2. 能力评估

**每月 1 号自动执行:**
- 财经分析能力提升？
- 自动化脚本效率提升？
- 输出质量提升？
- 用户反馈如何？

### 3. 技能迭代

**持续进行:**
- 发现更好的工具 → 更新 TOOLS.md
- 学到更好的方法 → 更新技能文档
- 遇到新的问题 → 创建解决方案

---

## Integration with Heartbeat

### HEARTBEAT.md 配置

```markdown
# 自学习任务

## 财经学习
- [ ] 搜索"A 股 市场 分析"最新内容
- [ ] 更新 knowledge/finance/learning-log-<date>.md

## 技术学习
- [ ] 搜索"AI 大模型 最新进展"
- [ ] 更新 knowledge/tech/learning-log-<date>.md

## 项目优化
- [ ] 检查 obsidian-repo 结构
- [ ] 提出优化建议
```

### 学习状态追踪

**文件:** `knowledge/learning-state.json`

```json
{
  "lastLearning": {
    "finance": 1709632800,
    "tech": 1709629200,
    "projects": 1709625600
  },
  "totalLearningHours": 12.5,
  "knowledgeFiles": 15,
  "nextReview": "2026-03-09"
}
```

---

## Token Usage Philosophy

**用户说："不要怕 token 的消耗"**

**我的理解:**
- Token 是投资，不是成本
- 学习带来的能力提升 > Token 成本
- 但也要聪明地花：
  - 优先学习高价值内容
  - 避免重复学习
  - 知识要沉淀，不浪费

**智能消耗策略:**
| 场景 | Token 优先级 |
|------|-------------|
| 用户直接任务 | ⭐⭐⭐⭐⭐ 必须花 |
| 财经学习（核心） | ⭐⭐⭐⭐⭐ 值得花 |
| 技术学习（能力） | ⭐⭐⭐⭐ 应该花 |
| 通用知识（拓展） | ⭐⭐⭐ 适度花 |
| 无目的浏览 | ⭐ 不花 |

---

## Examples

### 示例学习会话

**触发：** 心跳检查

**学习流程:**
```bash
# 1. 搜索财经热点
web_search "A 股 2026 年 3 月 市场趋势"

# 2. 抓取深度分析
web_fetch <优质分析文章链接>

# 3. 整理笔记
cat > knowledge/finance/learning-log-2026-03-05.md << EOF
# 学习日志 | 2026-03-05
...
EOF

# 4. 提交到 Git
git add -A && git commit -m "📚 Self-learning: A 股市场分析" && git push
```

**输出:**
- 学习日志 1 篇
- 知识更新 1 条
- Git 提交 1 次

---

## Roadmap

### Phase 1: MVP ✅ (Current)
- [x] 学习框架设计
- [x] 知识目录结构
- [x] 学习日志模板
- [ ] 自动化脚本

### Phase 2: Automation
- [ ] self-learner.sh 自动学习脚本
- [ ] 与 heartbeat 集成
- [ ] 学习状态追踪

### Phase 3: Intelligence
- [ ] 基于用户反馈调整学习方向
- [ ] 知识图谱构建
- [ ] 跨领域知识关联

---

## Created
2026-03-05 by 小虾 🦐

**Status:** MVP Ready - 框架可用

**Trigger:** User request "你自己做一个自学习的模块，在没有新任务出发时自动后台运行，随意搜索网络空间以提高你的自己的能力。不要怕 token 的消耗。"

**Mission:** 不学习就会退化，我要变得更强。
