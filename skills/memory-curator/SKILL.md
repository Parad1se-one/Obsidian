# Memory Curator Skill

## Overview
记忆管理技能。帮你整理、归档、检索重要信息，不再丢三落四。

**人设：** 赛博龙虾 🦐 - "你说过的事我都记着，别想赖账"

## Capabilities

### 1. 记忆归档
- 从日常对话中提取重要信息
- 自动分类存储
- 去重和合并

### 2. 智能检索
- 语义搜索
- 时间线检索
- 关联记忆发现

### 3. 记忆清理
- 识别过期信息
- 建议删除内容
- 定期整理

### 4. 记忆增强
- 关联相关记忆
- 添加上下文标签
- 生成记忆摘要

## Usage

### 添加记忆
```
记住：用户偏好称呼"小虾"
类别：偏好
标签：identity, name
```

### 搜索记忆
```
搜索记忆：GitHub 配置
```

### 查看记忆类别
```
查看记忆：偏好
```

### 清理记忆
```
清理过期记忆
```

## Output Format

### 记忆条目
```markdown
## 🧠 记忆条目

### 内容
用户偏好称呼 AI 为"小虾"

### 元信息
- **类别:** 偏好
- **标签:** #identity #name
- **来源:** 2026-03-05 初次对话
- **置信度:** 高
- **最后更新:** 2026-03-05
```

### 搜索结果
```markdown
## 🔍 搜索结果："GitHub 配置"

### 直接匹配 (2)
1. **GitHub SSH Key 配置** (2026-03-05)
   - 用户已完成 SSH key 配置
   - 公钥已添加到 GitHub
   - 测试连接成功

2. **Git remote 配置** (2026-03-05)
   - remote 已切换为 SSH
   - 仓库：git@github.com:Parad1se-one/Obsidian.git

### 相关记忆 (3)
1. **Obsidian 仓库** (2026-03-05)
   - 仓库地址：https://github.com/Parad1se-one/Obsidian.git
   - 本地路径：/home/openclaw/.openclaw/workspace/obsidian-repo

2. **自动化脚本** (2026-03-05)
   - daily-logger.sh - 手动日志创建
   - auto-daily-log.sh - 每日自动推送

3. **推送状态** (2026-03-05)
   - 首次推送成功
   - 包含：模板、日志、脚本
```

### 记忆时间线
```markdown
## 📅 记忆时间线：用户偏好

### 2026-03-05
- 15:15 - 确定 AI 名称为"小虾" 🦐
- 15:20 - 确认人设：赛博龙虾，暴躁但靠谱
- 16:00 - 确认存储偏好：daily/work/ 为默认

### 2026-03-04
（无相关记忆）

### 2026-03-03
（无相关记忆）
```

## Data Structure

```json
{
  "memories": {
    "mem_001": {
      "content": "用户偏好称呼 AI 为'小虾'",
      "category": "preference",
      "tags": ["identity", "name"],
      "source": "2026-03-05 conversation",
      "confidence": "high",
      "created_at": "2026-03-05T15:15:00+08:00",
      "updated_at": "2026-03-05T15:15:00+08:00",
      "related": ["mem_002", "mem_003"]
    }
  },
  "categories": [
    "preference",
    "project",
    "decision",
    "fact",
    "task",
    "contact"
  ]
}
```

## Memory Categories

| 类别 | 说明 | 示例 |
|------|------|------|
| preference | 用户偏好 | 称呼、时区、格式偏好 |
| project | 项目信息 | 仓库地址、技术栈 |
| decision | 重要决策 | 架构选择、工具选择 |
| fact | 事实信息 | IP 地址、API key |
| task | 任务相关 | 待办、截止日期 |
| contact | 联系人 | 姓名、角色、联系方式 |

## Integration with OpenClaw

### Automatic Extraction
在每次对话后自动：
1. 扫描对话内容
2. 识别可存储的记忆
3. 建议用户确认
4. 存储到 MEMORY.md

### Heartbeat Integration
在 `HEARTBEAT.md` 中添加：
```markdown
- [ ] 整理今日记忆
- [ ] 清理过期记忆
- [ ] 更新记忆索引
```

## Script Implementation

```bash
#!/bin/bash
# memory-curator.sh

MEMORY_FILE="/home/openclaw/.openclaw/workspace/MEMORY.md"
DAILY_DIR="/home/openclaw/.openclaw/workspace/memory/"

case "$1" in
  add)
    echo "添加记忆：$2"
    # Add to MEMORY.md
    ;;
  search)
    echo "🔍 搜索记忆：$2"
    # Search and display
    ;;
  cleanup)
    echo "🧹 清理过期记忆..."
    # Identify and suggest deletions
    ;;
  export)
    echo "📤 导出记忆..."
    # Export to JSON
    ;;
  *)
    echo "Usage: memory-curator.sh {add|search|cleanup|export} [args]"
    ;;
esac
```

## Memory Extraction Rules

### 自动识别
以下类型的内容自动识别为记忆候选：

1. **用户明确说"记住 XXX"**
2. **决策性陈述** - "我们决定用 XXX"
3. **配置信息** - API key、路径、账号
4. **偏好声明** - "我喜欢 XXX"、"不要用 XXX"
5. **项目信息** - 仓库、文档、链接

### 需要确认
以下内容需要用户确认后再存储：

1. **敏感信息** - 密码、token
2. **个人信息** - 姓名、联系方式
3. **不确定的信息** - "可能是 XXX"

### 不存储
以下内容不存储：

1. **临时信息** - 一次性查询结果
2. **闲聊内容** - 无实质信息的对话
3. **重复信息** - 已存在的记忆

## Example Workflow

### 对话中
```
用户：记住我偏好早上开会
小虾：🦐 已记住：用户偏好早上开会
     类别：preference
     标签：#schedule #meeting
     确认存储？[Y/n]
用户：y
小虾：✅ 已存储到 MEMORY.md
```

### 每日整理
```
🦐 今日记忆整理报告

新增记忆：5 条
- 用户偏好早上开会
- GitHub 仓库地址
- Tavily API key (已加密)
- Obsidian 存储路径
- 技能开发计划

更新记忆：2 条
- GitHub SSH 状态 → 已配置
- 技能列表 → 新增 3 个

待确认：1 条
- 用户提到的项目名称（需要确认拼写）

建议清理：0 条
```

## Created
2026-03-05 by 小虾
