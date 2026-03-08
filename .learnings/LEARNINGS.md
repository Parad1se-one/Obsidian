# Learnings Log

Log corrections, knowledge gaps, and best practices here.

## Format

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description

### Details
Full context

### Suggested Action
Specific fix or improvement

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2

---
```

---

## [LRN-20260306-001] 搜索功能优化

**Logged**: 2026-03-06T14:32:00+08:00
**Priority**: high
**Status**: in_progress
**Area**: infra

### Summary
实现完整的搜索→读取→净化→引用工作流

### Details
用户需求：优化搜索功能，形成完整的逻辑链条

**工作流设计:**
1. 🔍 **搜索** - web_search 获取结果列表
2. 📖 **读取** - web_fetch 提取网页内容
3. 🧹 **净化** - 清洗内容/提取核心/质量评估
4. 📚 **引用** - 格式化输出/标注来源/可信度

**已创建文件:**
- `~/.openclaw/skills/search/SKILL.md` - 技能定义
- `~/.openclaw/skills/search/search.sh` - 搜索脚本
- `~/.openclaw/skills/search/README.md` - 使用指南

### Suggested Action
- [ ] 配置 Brave Search API Key
- [ ] 实现自动化净化脚本
- [ ] 添加引用格式模板
- [ ] 测试完整工作流

### Metadata
- Source: user_feedback
- Related Files: ~/.openclaw/skills/search/
- Tags: search, workflow, citation

---
