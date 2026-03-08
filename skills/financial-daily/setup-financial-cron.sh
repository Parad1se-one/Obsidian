#!/bin/bash
# setup-financial-cron.sh - 配置财经日报 Cron 定时任务
# 工作日 07:30 自动推送

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_SCRIPT="$SCRIPT_DIR/financial-daily-cron.sh"
CRON_LOG="/home/openclaw/.openclaw/workspace/logs/financial-daily-cron.log"

echo "🦐 财经日报 Cron 配置工具"
echo "=========================================="

# 确保脚本可执行
chmod +x "$CRON_SCRIPT"
echo "✅ 脚本权限已设置：$CRON_SCRIPT"

# 获取当前 cron 列表
CURRENT_CRON=$(crontab -l 2>/dev/null || echo "")

# 检查是否已存在财经日报 cron
if echo "$CURRENT_CRON" | grep -q "financial-daily-cron.sh"; then
    echo "⚠️  财经日报 Cron 已存在"
    echo ""
    echo "当前配置:"
    echo "$CURRENT_CRON" | grep "financial-daily-cron.sh"
    echo ""
    read -p "是否重新配置？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "✅ 保持现有配置"
        exit 0
    fi
    
    # 删除旧配置
    echo "$CURRENT_CRON" | grep -v "financial-daily-cron.sh" | crontab -
    echo "🗑️  已删除旧配置"
fi

# 添加新 cron (工作日 07:30)
# 格式：分 时 日 月 周 命令
# 0 7 * * 1-5 = 周一至周五 07:30

NEW_CRON="0 7 * * 1-5 $CRON_SCRIPT >> $CRON_LOG 2>&1"

# 添加到 crontab
if [ -n "$CURRENT_CRON" ]; then
    (echo "$CURRENT_CRON"; echo "$NEW_CRON") | crontab -
else
    echo "$NEW_CRON" | crontab -
fi

echo ""
echo "✅ Cron 配置成功!"
echo ""
echo "📅 定时任务：工作日 (周一至周五) 07:30"
echo "📝 日志位置：$CRON_LOG"
echo ""
echo "当前 Cron 列表:"
crontab -l | grep -E "(financial|^[^#])" || echo "(无其他任务)"
echo ""
echo "=========================================="
echo "💡 手动测试：$CRON_SCRIPT"
echo "🔧 编辑 Cron: crontab -e"
echo "📋 查看日志：tail -f $CRON_LOG"
echo "=========================================="
