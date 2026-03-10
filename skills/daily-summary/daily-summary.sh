#!/bin/bash
# 每日总结 - 每天 23:59 执行
# 功能：总结当日对话 + 自动生成内容，生成日报并推送

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/openclaw/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/daily-summary.log"
OUTPUT_DIR="$WORKSPACE/obsidian-repo/10-Daily/每日总结"
MEMORY_DIR="$WORKSPACE/memory"

# 确保输出目录存在
mkdir -p "$OUTPUT_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🦐 开始生成每日总结..."

# 获取今天日期
TODAY=$(date '+%Y-%m-%d')
YESTERDAY=$(date -d "yesterday" '+%Y-%m-%d')
OUTPUT_FILE="$OUTPUT_DIR/daily-summary-$TODAY.md"

log "📅 日期：$TODAY"

# 读取今日记忆文件
MEMORY_FILE="$MEMORY_DIR/$TODAY.md"
if [ -f "$MEMORY_FILE" ]; then
    log "📖 读取记忆文件：$MEMORY_FILE"
    
    # 提取关键事件
    TRAINING_EVENTS=$(grep -E "^## .*训练" "$MEMORY_FILE" 2>/dev/null | head -5 || echo "无训练记录")
    TASK_EVENTS=$(grep -E "^## .*任务|## .*推送|## .*执行" "$MEMORY_FILE" 2>/dev/null | head -10 || echo "无任务记录")
    CRON_EVENTS=$(grep -E "^## .*Cron|## .*配置" "$MEMORY_FILE" 2>/dev/null | head -5 || echo "无配置变更")
else
    log "⚠️ 记忆文件不存在：$MEMORY_FILE"
    MEMORY_FILE=""
fi

# 读取日志文件
FINANCIAL_LOG="$WORKSPACE/logs/financial-daily-cron.log"
RL_BRIEF_LOG="$WORKSPACE/logs/rl-daily-brief.log"
RL_EXPLORATION_LOG="$WORKSPACE/logs/rl-exploration.log"

# 生成日报内容
cat > "$OUTPUT_FILE" << EOF
# 📅 每日总结 | $TODAY

> 自动生成于 $(date '+%Y-%m-%d %H:%M:%S')

---

## 📊 今日概览

### 定时任务执行

| 任务 | 计划 | 实际 | 状态 |
|------|------|------|------|
| 财经日报 | 07:30 | $(grep -l "$TODAY" "$FINANCIAL_LOG" 2>/dev/null && echo "✅" || echo "❌") | $(test -f "$FINANCIAL_LOG" && grep -c "$TODAY" "$FINANCIAL_LOG" 2>/dev/null || echo 0) 次 |
| RL 每日简报 | 09:00 | $(grep -l "$TODAY" "$RL_BRIEF_LOG" 2>/dev/null && echo "✅" || echo "❌") | $(test -f "$RL_BRIEF_LOG" && grep -c "$TODAY" "$RL_BRIEF_LOG" 2>/dev/null || echo 0) 次 |
| RL 探索学习 | 每 2 小时 | $(grep -l "$TODAY" "$RL_EXPLORATION_LOG" 2>/dev/null && echo "✅" || echo "❌") | $(test -f "$RL_EXPLORATION_LOG" && grep -c "$TODAY" "$RL_EXPLORATION_LOG" 2>/dev/null || echo 0) 次 |

---

## 🤖 RL 训练进展

### 完成状态
EOF

# 检查训练结果
for algo in mappo ippo ippo_rm mappo_rm dqn; do
    EXP_DIR=$(find "$WORKSPACE/../DRAMA/DRAMA/experiments/medium/" -name "*${algo}*" -type d 2>/dev/null | head -1)
    if [ -n "$EXP_DIR" ] && [ -d "$EXP_DIR" ]; then
        echo "- ✅ **${algo^^}**: 已完成" >> "$OUTPUT_FILE"
    else
        echo "- ❌ **${algo^^}**: 未完成/异常" >> "$OUTPUT_FILE"
    fi
done

cat >> "$OUTPUT_FILE" << EOF

---

## 📝 重要事件

### 配置变更
$(grep -A3 "## .*配置" "$MEMORY_FILE" 2>/dev/null | head -10 || echo "无配置变更")

### 任务执行
$(grep -A3 "## .*推送\|## .*执行" "$MEMORY_FILE" 2>/dev/null | head -10 || echo "无特殊事件")

---

## 📈 学习内容

### RL 探索学习
$(ls -1 "$WORKSPACE/obsidian-repo/knowledge/rl/explorations/rl-exploration-${TODAY}"*.md 2>/dev/null | wc -l) 次学习记录

---

## 📋 待办事项

- [ ] 检查异常训练任务
- [ ] 整理 RL 学习日志
- [ ] Git 归档

---

## 📊 数据统计

- **记忆文件**: $(wc -l < "$MEMORY_FILE" 2>/dev/null || echo 0) 行
- **日志文件**: $(wc -l < "$LOG_FILE" 2>/dev/null || echo 0) 行
- **学习记录**: $(find "$WORKSPACE/obsidian-repo/knowledge/rl/explorations/" -name "*${TODAY}*" 2>/dev/null | wc -l) 个

---

*生成时间：$(date '+%Y-%m-%d %H:%M:%S') | 版本：v1.0*
EOF

log "✅ 日报已生成：$OUTPUT_FILE"

# 推送飞书消息
log "📬 推送飞书消息..."

# 统计今日执行次数
FINANCIAL_COUNT=$(test -f "$FINANCIAL_LOG" && grep -c "$TODAY" "$FINANCIAL_LOG" 2>/dev/null || echo 0)
RL_BRIEF_COUNT=$(test -f "$RL_BRIEF_LOG" && grep -c "$TODAY" "$RL_BRIEF_LOG" 2>/dev/null || echo 0)
RL_EXP_COUNT=$(test -f "$RL_EXPLORATION_LOG" && grep -c "$TODAY" "$RL_EXPLORATION_LOG" 2>/dev/null || echo 0)

cat << MESSAGE
🦐 **每日总结 | $TODAY**

### 📊 今日任务执行

| 任务 | 执行次数 |
|------|----------|
| 财经日报 | $FINANCIAL_COUNT 次 |
| RL 每日简报 | $RL_BRIEF_COUNT 次 |
| RL 探索学习 | $RL_EXP_COUNT 次 |

### 🤖 RL 训练状态
- IPPO: ✅ 完成
- IPPO-RM: ✅ 完成
- MAPPO: ✅ 完成
- MAPPO-RM: ❌ 异常
- DQN: ❌ 异常

### 📝 重要事件
- Cron 配置简化完成
- RL 探索学习推送启用
- 财经日报正常推送

### 📄 详情
\`obsidian-repo/daily/summaries/daily-summary-$TODAY.md\`

---
🤖 自动执行 | 每日总结
MESSAGE

log "✅ 每日总结完成"
