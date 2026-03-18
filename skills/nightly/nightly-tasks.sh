#!/bin/bash
# nightly-tasks.sh - 每日 23:50 夜间任务
# 功能：
#   1. OpenViking 记忆同步
#   2. Self-Improving Agent 学习日志整理
#   3. 每日记忆总结 (memory flush)

set -e

WORKSPACE="/home/openclaw/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/nightly-tasks.log"
DATE=$(date '+%Y-%m-%d')

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "🌙 夜间任务开始 ($DATE)"
log "=========================================="

# ─────────────────────────────────────────
# 1. OpenViking 记忆同步
# ─────────────────────────────────────────
log ""
log "📦 [1/3] OpenViking 记忆同步..."
if [ -f "$WORKSPACE/skills/openviking/openviking-sync.sh" ]; then
    bash "$WORKSPACE/skills/openviking/openviking-sync.sh" 2>&1 | tee -a "$LOG_FILE"
    log "✅ OpenViking 同步完成"
else
    log "⚠️  OpenViking 脚本不存在，跳过"
fi

# ─────────────────────────────────────────
# 2. Self-Improving Agent 学习日志整理
# ─────────────────────────────────────────
log ""
log "🧠 [2/3] Self-Improving Agent 学习日志整理..."

LEARNINGS_DIR="$WORKSPACE/.learnings"
if [ -d "$LEARNINGS_DIR" ]; then
    # 统计今日新增条目
    LEARNINGS_COUNT=$(grep -c "^\## \[LRN-${DATE//-/}" "$LEARNINGS_DIR/LEARNINGS.md" 2>/dev/null || echo "0")
    ERRORS_COUNT=$(grep -c "^\## \[ERR-${DATE//-/}" "$LEARNINGS_DIR/ERRORS.md" 2>/dev/null || echo "0")
    FEATURES_COUNT=$(grep -c "^\## \[FEAT-${DATE//-/}" "$LEARNINGS_DIR/FEATURE_REQUESTS.md" 2>/dev/null || echo "0")
    
    log "  📊 今日统计:"
    log "    Learnings: $LEARNINGS_COUNT"
    log "    Errors: $ERRORS_COUNT"
    log "    Feature Requests: $FEATURES_COUNT"
    
    # 检查是否有 pending 的高优先级条目需要 promote
    PENDING_HIGH=$(grep -B2 "Priority\*\*: high" "$LEARNINGS_DIR/LEARNINGS.md" 2>/dev/null | grep "Status\*\*: pending" | wc -l || echo "0")
    if [ "$PENDING_HIGH" -gt 0 ]; then
        log "  ⚠️  有 $PENDING_HIGH 条高优先级 pending 条目待 promote"
    fi
    
    log "✅ Self-Improving Agent 整理完成"
else
    log "⚠️  .learnings/ 目录不存在，跳过"
fi

# ─────────────────────────────────────────
# 3. 每日记忆总结
# ─────────────────────────────────────────
log ""
log "📝 [3/3] 每日记忆总结..."

MEMORY_FILE="$WORKSPACE/memory/$DATE.md"
if [ -f "$MEMORY_FILE" ]; then
    MEMORY_LINES=$(wc -l < "$MEMORY_FILE")
    log "  📄 今日记忆文件: $MEMORY_FILE ($MEMORY_LINES 行)"
    
    # 追加夜间任务执行记录
    cat >> "$MEMORY_FILE" << EOF

### 🌙 夜间任务执行 (23:50)
- OpenViking 同步: ✅
- Self-Improving 统计: Learnings=$LEARNINGS_COUNT, Errors=$ERRORS_COUNT, Features=$FEATURES_COUNT
- 记忆总结: ✅ ($MEMORY_LINES 行)
EOF
    log "✅ 记忆总结已追加"
else
    log "⚠️  今日记忆文件不存在: $MEMORY_FILE"
    # 创建一个最小记忆文件
    mkdir -p "$WORKSPACE/memory"
    echo "## $DATE 记忆日志" > "$MEMORY_FILE"
    echo "" >> "$MEMORY_FILE"
    echo "### 🌙 夜间任务执行 (23:50)" >> "$MEMORY_FILE"
    echo "- 今日无记忆记录" >> "$MEMORY_FILE"
    log "📝 已创建最小记忆文件"
fi

# ─────────────────────────────────────────
# Git 提交 (如果有变更)
# ─────────────────────────────────────────
log ""
log "📤 Git 提交..."
cd "$WORKSPACE"
if [ -n "$(git status --porcelain memory/ .learnings/ 2>/dev/null)" ]; then
    git add memory/ .learnings/ 2>/dev/null
    git commit -m "🌙 夜间任务 $DATE - 记忆同步 + 学习日志 [auto]" 2>/dev/null
    log "✅ Git 提交完成"
else
    log "ℹ️  无变更需要提交"
fi

log ""
log "=========================================="
log "🌙 夜间任务完成 ($DATE)"
log "=========================================="
