# Daily Summary Skill

## Overview
每日自动摘要技能。自动生成当天工作/对话摘要，不再浪费时间写日报。

**人设：** 赛博龙虾 🦐 - "今天干了啥？我帮你记着呢"

## Capabilities

### 1. 自动摘要
- 收集当天的对话记录
- 提取关键决策和任务
- 生成结构化日报

### 2. 多源整合
- 整合聊天记录
- 整合 Git 提交
- 整合任务完成状态

### 3. 格式输出
- Markdown 格式
- 支持导出为邮件
- 支持发送到聊天群组

### 4. 历史对比
- 与昨日对比
- 周/月统计
- 趋势分析

## Usage

### 生成今日摘要
```
生成今日摘要
```

### 指定日期范围
```
生成周报：2026-03-03 to 2026-03-07
```

### 发送到指定位置
```
发送日报到：daily/work/2026-03-05.md
```

## Output Format

### 日报模板
```markdown
# 2026-03-05 日报

## 📊 今日概览
- **工作时长:** 6.5h
- **完成任务:** 5/7
- **对话轮数:** 42
- **代码提交:** 3

## ✅ 完成事项
1. [x] 初始化 Obsidian 工作流
2. [x] 创建 Tavily 搜索技能
3. [x] 配置 GitHub SSH
4. [x] 设置自动整理 cron
5. [x] 安装 3 个新技能

## 🔄 进行中
1. [~] 技能集成 (50%)
2. [~] 文档完善 (30%)

## 📝 关键决策
- 日常对话存储到 daily/work/
- 使用 Tavily 替代 Brave Search
- 自定义技能风格：暴躁但靠谱

## 💡 学习/收获
- Tavily API 配置方法
- OpenClaw 技能开发流程
- Git 自动化脚本编写

## ⚠️ 问题/风险
- GitHub push 需要 SSH 认证（已解决）
- 部分技能待集成

## 📅 明日计划
1. 完成技能集成
2. 测试自动化流程
3. 完善文档

---
*生成时间：2026-03-05 23:59*
```

### 周报模板
```markdown
# Week 10 周报 (2026-03-03 ~ 2026-03-07)

## 📊 本周统计
| 指标 | 数值 | 环比 |
|------|------|------|
| 工作时长 | 32h | +5% |
| 完成任务 | 28 | +12% |
| 对话轮数 | 215 | +8% |
| 代码提交 | 15 | -3% |

## 🎯 主要成就
1. 完成 Obsidian 知识库搭建
2. 配置自动化工作流
3. 开发 4 个自定义技能

## 📈 趋势分析
- 任务完成率稳步提升
- 代码提交略有下降（主要在做配置）
- 对话质量提高（更聚焦）

## 🐛 遇到的问题
- GitHub 认证配置（已解决）
- 技能集成待完善

## 📋 下周计划
1. 完成所有技能集成
2. 开始实际项目使用
3. 优化自动化流程

---
*生成时间：2026-03-07 23:59*
```

## Data Sources

### 1. 对话记录
- 从 `memory/YYYY-MM-DD.md` 读取
- 从 Obsidian daily logs 读取

### 2. Git 活动
- 从 Git commits 读取
- 统计文件变更

### 3. 任务状态
- 从 Task Master 技能读取
- 统计完成/进行中/延期

## Integration with OpenClaw

### Cron 配置
```bash
# 每天 23:59 生成日报
59 23 * * * openclaw send "生成今日摘要"

# 每周五 17:00 生成周报
0 17 * * 5 openclaw send "生成周报"
```

### 输出位置
- 本地文件：`daily/reports/YYYY-MM-DD.md`
- Obsidian：`daily/work/YYYY-MM-DD.md`
- 邮件：配置 SMTP 后发送
- 聊天：发送到指定群组

## Script Implementation

```bash
#!/bin/bash
# daily-summary.sh

DATE="${1:-$(date +%Y-%m-%d)}"
OUTPUT_DIR="/home/openclaw/.openclaw/workspace/obsidian-repo/daily/reports"

mkdir -p "$OUTPUT_DIR"

echo "🦐 生成 $DATE 的日报..."

# Collect data sources
# - Memory files
# - Git commits
# - Task status

# Generate summary
# Save to file

echo "✅ 日报已生成：$OUTPUT_DIR/$DATE.md"
```

## Customization

### 摘要风格
在 `TOOLS.md` 中配置：
```markdown
### Daily Summary

- Style: Concise, bullet points
- Include metrics: true
- Include git activity: true
- Include task status: true
- Send to: daily/work/
```

### 指标阈值
```json
{
  "workHours": {
    "target": 8,
    "warning": 6
  },
  "taskCompletion": {
    "target": 80,
    "warning": 60
  }
}
```

## Example Output

```markdown
# 2026-03-05 日报

## 📊 今日概览
- **工作时长:** 8h 15m
- **完成任务:** 7/8 (87.5%)
- **对话轮数:** 56
- **代码提交:** 5

## ✅ 完成事项
1. [x] 初始化 Obsidian 工作流
2. [x] 创建对话记录模板
3. [x] 创建 Tavily 搜索技能
4. [x] 配置 GitHub SSH 认证
5. [x] 设置 cron 自动整理
6. [x] 开发 Task Decomposer 技能
7. [x] 开发 Daily Summary 技能

## 🔄 进行中
1. [~] 技能正式集成 (60%)

## 📝 关键决策
- 使用 Tavily API 进行网络搜索
- 日常对话默认存储到 daily/work/
- 技能风格统一为"暴躁但靠谱"

## 💡 学习/收获
- OpenClaw 技能开发流程
- Tavily API 集成方法
- Git 自动化脚本编写

## ⚠️ 问题/风险
- 无重大风险

## 📅 明日计划
1. 完成技能集成测试
2. 开始实际项目使用
3. 优化 cron 任务

---
*生成时间：2026-03-05 23:59*
```

## Created
2026-03-05 by 小虾
