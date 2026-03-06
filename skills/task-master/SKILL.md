# Task Master Skill

## Overview
任务和日程管理技能。帮你记住所有破事，不再丢三落四。

**人设：** 赛博龙虾 🦐 - 比你妈还唠叨你的待办事项

## Capabilities

### 1. 任务管理
- 创建/更新/完成任务
- 设置优先级和截止日期
- 自动提醒即将到期的任务

### 2. 日程安排
- 管理日历事件
- 检测时间冲突
- 建议最佳会议时间

### 3. 习惯追踪
- 记录日常习惯
- 统计连续天数
- 生成进度报告

### 4. 智能提醒
- 基于上下文的提醒
- 批量提醒（每日/每周摘要）
- 过期任务警告

## Usage

### 添加任务
```
添加任务：完成项目报告
截止：明天 17:00
优先级：高
标签：work, deadline
```

### 查看任务
```
今天有什么任务？
这周的截止日期？
显示所有高优先级任务
```

### 完成任务
```
完成任务：项目报告
```

## Data Storage

任务存储在 `tasks/tasks.json`：

```json
{
  "tasks": [
    {
      "id": "task_001",
      "title": "完成项目报告",
      "description": "Q1 项目总结报告",
      "priority": "high",
      "due": "2026-03-06T17:00:00+08:00",
      "status": "pending",
      "tags": ["work", "deadline"],
      "created": "2026-03-05T16:00:00+08:00"
    }
  ],
  "habits": [
    {
      "name": "每日代码审查",
      "frequency": "daily",
      "streak": 5,
      "lastCompleted": "2026-03-04"
    }
  ]
}
```

## Output Format

### 每日任务摘要
```markdown
## 🦐 今日任务 (2026-03-05)

### 🔴 紧急 (今天截止)
- [ ] 完成项目报告 [17:00]

### 🟡 即将到期 (3 天内)
- [ ] 准备周会材料 [周五]
- [ ] 审查 PR #42 [周四]

### 🟢 常规任务
- [ ] 更新文档
- [x] 回复邮件 ✅

### ⏰ 习惯追踪
- 每日代码审查：🔥 5 天连续
- 运动：❌ 今天还没动

### 💬 小虾点评
今天任务不多，别摸鱼了，赶紧干完。
```

### 周摘要
```markdown
## 🦐 本周总结 (Week 10)

### 完成情况
- 完成：12/15 任务 (80%)
- 延期：2 个
- 取消：1 个

### 习惯统计
- 代码审查：5/7 天
- 运动：2/7 天 - 你这周太懒了

### 下周预览
- 周一：团队例会
- 周三：项目评审
- 周五：截止日期 x2

### 💬 小虾点评
80% 完成率还行，但运动是怎么回事？身体不要了？
```

## Integration with OpenClaw

### Heartbeat 集成
在 `HEARTBEAT.md` 中添加：
```markdown
- [ ] 检查今日任务
- [ ] 提醒即将到期的任务
- [ ] 更新习惯追踪
```

### 定时提醒
```bash
# 每天 9:00 发送任务摘要
0 9 * * * openclaw send "今日任务摘要"

# 每天 17:00 检查完成情况
0 17 * * * openclaw send "任务完成检查"
```

## Script Implementation

```bash
#!/bin/bash
# task-master.sh

TASKS_FILE="/home/openclaw/.openclaw/workspace/tasks/tasks.json"

case "$1" in
  add)
    echo "添加任务: $2"
    # Add task to JSON file
    ;;
  list)
    echo "🦐 今日任务："
    # Query and display tasks
    ;;
  complete)
    echo "完成任务：$2"
    # Mark task as complete
    ;;
  summary)
    echo "生成任务摘要..."
    # Generate daily/weekly summary
    ;;
  *)
    echo "Usage: task-master.sh {add|list|complete|summary} [args]"
    ;;
esac
```

## Priority Levels

| 级别 | 颜色 | 说明 | 提醒频率 |
|------|------|------|----------|
| Critical | 🔴 | 今天截止/已过期 | 每 2 小时 |
| High | 🟠 | 3 天内截止 | 每天 |
| Medium | 🟡 | 本周内 | 每周 |
| Low | 🟢 | 无明确截止 | 按需 |

## Created
2026-03-05 by 小虾
