#!/bin/bash
# setup-cron.sh - 设置财经日报定时任务
# 每天早上 7:30 执行（工作日）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FINANCIAL_SCRIPT="$SCRIPT_DIR/financial-daily.sh"
LOG_FILE="/home/openclaw/.openclaw/workspace/logs/financial-daily.log"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

echo "🦐 设置财经日报定时任务..."
echo ""
echo "📍 脚本位置：$FINANCIAL_SCRIPT"
echo "📝 日志位置：$LOG_FILE"
echo "⏰ 执行时间：每周一至周五 07:30 (Asia/Shanghai)"
echo ""

# 检查脚本是否存在
if [ ! -f "$FINANCIAL_SCRIPT" ]; then
    echo "❌ 错误：脚本不存在 $FINANCIAL_SCRIPT"
    exit 1
fi

# 检查 crontab 是否已存在
EXISTING=$(crontab -l 2>/dev/null | grep "financial-daily" || true)

if [ -n "$EXISTING" ]; then
    echo "⚠️  警告：已存在财经日报定时任务"
    echo ""
    echo "现有任务:"
    echo "$EXISTING"
    echo ""
    read -p "是否覆盖？[y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 已取消"
        exit 0
    fi
    
    # 删除旧任务
    crontab -l 2>/dev/null | grep -v "financial-daily" | crontab -
    echo "✅ 已删除旧任务"
fi

# 添加新任务
# 注意：cron 时区可能是 UTC，需要根据服务器时区调整
# Asia/Shanghai = UTC+8，所以 7:30 CST = 23:30 UTC (前一天)
CRON_ENTRY="30 23 * * 1-5 cd $SCRIPT_DIR && ./financial-daily.sh >> $LOG_FILE 2>&1"

(crontab -l 2>/dev/null | grep -v "financial-daily"; echo "$CRON_ENTRY") | crontab -

echo ""
echo "✅ 定时任务设置完成！"
echo ""
echo "📋 当前 crontab:"
crontab -l | grep "financial-daily"
echo ""
echo "💡 提示:"
echo "   - 查看日志：tail -f $LOG_FILE"
echo "   - 手动测试：$FINANCIAL_SCRIPT"
echo "   - 编辑任务：crontab -e"
echo "   - 删除任务：crontab -l | grep -v financial-daily | crontab -"
