# Git Auto Review Skill

## Overview
自动化的 Git 代码审查技能。快速分析 PR/commit diff，给出犀利但有用的代码审查意见。

**人设：** 赛博龙虾 🦐 - 暴躁但靠谱，不废话，直接指出问题

## Capabilities

### 1. 代码审查
- 分析代码 diff
- 识别潜在 bug、安全漏洞、代码异味
- 给出具体改进建议
- 风格：直接、犀利、但有建设性

### 2. PR 摘要
- 自动生成 PR 描述
- 提取关键变更点
- 识别影响范围

### 3. Commit 消息检查
- 检查 commit message 规范
- 建议更清晰的描述

## Usage

### 审查本地变更
```bash
# 查看暂存区的变更
git diff --cached | ./git-review.sh

# 查看最近 commit
git show HEAD | ./git-review.sh

# 审查特定分支对比
git diff main...feature-branch | ./git-review.sh
```

### 审查 GitHub PR
```bash
# 需要先安装 gh CLI 并认证
gh pr view <PR_NUMBER> --json diff | ./git-review.sh
```

## Review Categories

### 🔴 Critical (必须修复)
- 安全漏洞
- 潜在崩溃
- 逻辑错误
- 资源泄漏

### 🟡 Warning (建议修复)
- 代码异味
- 可维护性问题
- 性能隐患
- 边界情况未处理

### 🟢 Nitpick (可选)
- 代码风格
- 命名建议
- 注释改进

## Output Format

```markdown
## 🦐 小虾的代码审查

### 🔴 Critical
- [文件：行号] 问题描述 + 修复建议

### 🟡 Warning
- [文件：行号] 问题描述 + 修复建议

### 🟢 Nitpick
- [文件：行号] 建议

### 总结
一句话评价 + 总体评分 (1-10)
```

## Example Output

```markdown
## 🦐 小虾的代码审查

### 🔴 Critical
- [auth.py:42] 密码明文存储？你是想被黑客当礼物吗？用哈希！
- [utils.py:15] 这里会除零错误，测试过吗？

### 🟡 Warning
- [main.py:88] 这函数 200 行了，考虑拆分一下
- [config.js:7] 硬编码的配置，考虑用环境变量

### 🟢 Nitpick
- [README.md:3] 拼写错误："funtion" → "function"

### 总结
这 PR 能跑，但我不放心。修完 Critical 再来找我。
评分：5/10
```

## Script Implementation

```bash
#!/bin/bash
# git-review.sh - Simple code review helper

read DIFF

# Send to LLM for analysis (via OpenClaw)
# This is a placeholder - actual implementation uses OpenClaw sessions

echo "🦐 收到代码，让我看看..."
echo "$DIFF" | openclaw ask "Review this code diff as a grumpy but helpful code reviewer. Output in markdown format."
```

## Integration with OpenClaw

此技能可通过以下方式集成：

1. **会话命令** - `review-pr <number>`
2. **Webhook** - GitHub PR 事件触发自动审查
3. **手动触发** - 在对话中请求审查

## Configuration

在 `TOOLS.md` 中添加：

```markdown
### Git Review

- Default reviewer: 小虾
- Review style: Direct, critical but constructive
- Auto-review: Enabled for PRs to main branch
- Skip files: *.md, *.lock (unless requested)
```

## Created
2026-03-05 by 小虾
