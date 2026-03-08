#!/bin/bash
# setup-heartbeat-cron.sh - 设置 Heartbeat 自动执行定时任务
# 每小时检查一次，自动执行到期任务

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HEARTBEAT_SCRIPT="$SCRIPT_DIR/heartbeat-exec.sh"
LOG_FILE="/home/openclaw/.openclaw/workspace/logs/heartbeat-cron.log"

echo "🦐 设置 Heartbeat 自动执行定时任务..."
echo ""
echo "📍 脚本位置：$HEARTBEAT_SCRIPT"
echo "⏰ 执行频率：每小时检查一次"
echo ""

# 检查脚本是否存在
if [ ! -f "$HEARTBEAT_SCRIPT" ]; then
    echo "❌ 错误：脚本不存在 $HEARTBEAT_SCRIPT"
    exit 1
fi

# 删除旧的 heartbeat 任务
crontab -l 2>/dev/null | grep -v "heartbeat-exec" | crontab - 2>/dev/null || true

# 添加新任务 - 每小时执行一次
CRON_ENTRY="0 * * * * cd $SCRIPT_DIR && ./heartbeat-exec.sh >> $LOG_FILE 2>&1"

(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✅ Heartbeat 定时任务设置完成！"
echo ""
echo "📋 当前 crontab:"
crontab -l | grep -E "(heartbeat|financial)" || echo "(无相关任务)"
echo ""
echo "📅 自动执行任务:"
echo "   - 工作日 07:30 → 财经日报"
echo "   - 每日 09:00 → RL 学习 (basics/algorithms)"
echo "   - 每日 14:00 → RL 论文阅读"
echo "   - 每日 20:00 → RL 代码实现"
echo "   - 周日 10:00 → 知识维护提醒"
echo ""
echo "💡 提示:"
echo "   - 查看日志：tail -f $LOG_FILE"
echo "   - 手动测试：$HEARTBEAT_SCRIPT"
echo "   - 编辑任务：crontab -e"
