#!/bin/bash
# financial-daily-cron.sh - 工作日财经日报自动推送（Cron 版）
# 用法：Cron 定时调用（工作日 07:30）
#       手动测试：./financial-daily-cron.sh --force
# 功能：生成日报 → 质量检查 → 推送飞书

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/openclaw/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/financial-daily-cron.log"
DATE="$(date +%Y-%m-%d)"
OUTPUT_FILE="$WORKSPACE/obsidian-repo/10-Daily/财经日报/财经日报-${DATE}.md"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查是否为工作日 (1-5)，--force 参数可跳过此检查
FORCE=false
if [ "$1" = "--force" ]; then
    FORCE=true
    log "🔧 强制模式：跳过工作日检查"
fi

DAY_OF_WEEK=$(date +%u)
if [ "$DAY_OF_WEEK" -gt 5 ] && [ "$FORCE" = false ]; then
    log "⏭️  周末/节假日，跳过财经日报 (使用 --force 强制运行)"
    exit 0
fi

log "=========================================="
log "🦐 财经日报自动推送 | $DATE | 周${DAY_OF_WEEK}"
log "=========================================="

# 1. 生成财经日报
log "📊 步骤 1/4: 生成财经日报..."
cd "$WORKSPACE" && ./skills/financial-daily/financial-daily.sh "$DATE" 2>&1 | tee -a "$LOG_FILE"

if [ ! -f "$OUTPUT_FILE" ]; then
    log "❌ 财经日报生成失败：文件不存在"
    exit 1
fi
log "✅ 财经日报生成完成：$OUTPUT_FILE"

# 2. 质量检查
log "📋 步骤 2/4: 质量检查..."
QUALITY_OUTPUT=$(cd "$WORKSPACE" && ./skills/quality-checker/quality-checker.sh "$OUTPUT_FILE" "financial" 2>&1)
echo "$QUALITY_OUTPUT" | tee -a "$LOG_FILE"

# 提取质量分数 (支持多种格式)
QUALITY_SCORE=$(echo "$QUALITY_OUTPUT" | grep -oP '(综合得分：|总分：|得分：)\s*\K\d+' | head -1 || echo "0")
if [ -z "$QUALITY_SCORE" ] || [ "$QUALITY_SCORE" = "0" ]; then
    # 尝试另一种格式：**综合得分：90/100**
    QUALITY_SCORE=$(echo "$QUALITY_OUTPUT" | grep -oP '\*\*综合得分：\K\d+' || echo "0")
fi
log "📊 质量评分：$QUALITY_SCORE / 100"

if [ "$QUALITY_SCORE" -lt 80 ]; then
    log "⚠️  质量评分 < 80，重新生成..."
    cd "$WORKSPACE" && ./skills/financial-daily/financial-daily.sh "$DATE" 2>&1 | tee -a "$LOG_FILE"
    
    # 二次检查
    QUALITY_OUTPUT=$(cd "$WORKSPACE" && ./skills/quality-checker/quality-checker.sh "$OUTPUT_FILE" "financial" 2>&1)
    QUALITY_SCORE=$(echo "$QUALITY_OUTPUT" | grep -oP '总分：\K\d+' || echo "0")
    log "📊 二次评分：$QUALITY_SCORE / 100"
    
    if [ "$QUALITY_SCORE" -lt 80 ]; then
        log "❌ 二次检查仍 < 80 分，推送失败"
        exit 1
    fi
fi
log "✅ 质量检查通过"

# 3. Git 提交并推送
log "📤 步骤 3/4: Git 提交并推送..."
cd "$WORKSPACE/obsidian-repo"

# 添加今日日报文件 (使用相对路径)
RELATIVE_FILE="daily/financial-news/${DATE}.md"
git add "$RELATIVE_FILE" 2>&1 | tee -a "$LOG_FILE"

# 提交
git commit -m "📈 财经日报 $DATE [auto]" 2>&1 | tee -a "$LOG_FILE"

# 推送
git push 2>&1 | tee -a "$LOG_FILE"

PUSH_RESULT=${PIPESTATUS[2]}
if [ "$PUSH_RESULT" -eq 0 ]; then
    log "✅ Git 推送成功"
else
    log "⚠️  Git 推送失败 (exit code: $PUSH_RESULT)，继续尝试飞书推送"
fi

# 4. 推送飞书
log "📤 步骤 4/4: 推送飞书..."

# 提取日报摘要（前 50 行）
SUMMARY=$(head -50 "$OUTPUT_FILE" | tail -40)

# 构造飞书消息
MESSAGE="📈 **财经日报 | $DATE**

**质量评分:** $QUALITY_SCORE/100

**市场概览:**
$(grep -A5 '## 🌍 市场概览' "$OUTPUT_FILE" | tail -4 | sed 's/^/  /')

**热门板块:**
$(grep -A8 '## 🔥 热门板块' "$OUTPUT_FILE" | tail -6 | sed 's/^/  /')

**资金流向:**
$(grep -A5 '## 💰 资金流向' "$OUTPUT_FILE" | tail -3 | sed 's/^/  /')

---
_完整报告已保存至 Obsidian_"

# 使用 message 工具推送 (feishu 不需要显式指定 target，自动使用当前会话)
cd "$WORKSPACE" && openclaw message send \
    --channel feishu \
    --target "ou_519fce3fc3512f400ecc41a440758fc1" \
    --message "$MESSAGE" 2>&1 | tee -a "$LOG_FILE"

RESULT=${PIPESTATUS[0]}
if [ "$RESULT" -eq 0 ]; then
    log "✅ 飞书推送成功"
else
    log "❌ 飞书推送失败 (exit code: $RESULT)"
    exit 1
fi

log "=========================================="
log "✅ 财经日报生成 + Git 推送 + 飞书通知 完成"
log "=========================================="
