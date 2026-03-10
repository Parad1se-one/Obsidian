#!/bin/bash
# RL 探索学习 - 每 2 小时执行
# 功能：自动探索 RL 领域知识点，记录学习日志

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/openclaw/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/rl-exploration.log"
OUTPUT_DIR="$WORKSPACE/obsidian-repo/20-RL"

# 确保输出目录存在
mkdir -p "$OUTPUT_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🦐 开始 RL 探索学习..."

# 检查是否在执行窗口内 (09:00-21:00)
HOUR=$(date +%H)
if [ "$HOUR" -lt 9 ] || [ "$HOUR" -gt 21 ]; then
    log "⏰ 非学习时间 (09:00-21:00)，跳过"
    exit 0
fi

# 生成学习日志
DATE=$(date '+%Y-%m-%d')
HOUR=$(date +%H)
LOG_FILE_NAME="rl-exploration-${DATE}-${HOUR}h.md"
LOG_PATH="$OUTPUT_DIR/探索记录/$LOG_FILE_NAME"

mkdir -p "$OUTPUT_DIR/探索记录"

cat > "$LOG_PATH" << EOF
# 🔍 RL 探索学习 | $DATE ${HOUR}:00

> 自动探索记录

---

## 📖 学习主题

### 核心概念
- 待更新

### 关键算法
- 待更新

---

## 💡 学习收获

1. 
2. 
3. 

---

## ❓ 待探索问题

- [ ] 
- [ ] 

---

## 📚 参考资料

- 

---

*生成时间：$(date '+%Y-%m-%d %H:%M:%S')*
EOF

log "✅ 学习日志已生成：$LOG_PATH"

# 推送飞书通知
log "📬 推送学习通知..."
NEXT_HOUR=$((HOUR + 2))
if [ "$NEXT_HOUR" -gt 21 ]; then
    NEXT_SHOW="明天 09:00"
else
    NEXT_SHOW="${NEXT_HOUR}:00"
fi

cat << MESSAGE
🦐 **RL 探索学习 | 已完成**

⏰ 时间：$DATE ${HOUR}:00
📝 日志：\`obsidian-repo/knowledge/rl/explorations/$LOG_FILE_NAME\`

💡 学习时段：09:00-21:00
📊 下次学习：$NEXT_SHOW

---
🤖 自动执行 | RL 研究助手
MESSAGE

log "✅ RL 探索学习完成"
