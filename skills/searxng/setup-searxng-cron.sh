#!/bin/bash
# setup-searxng-cron.sh - 配置 SearXNG 自动维护 Cron 任务

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAINTENANCE_SCRIPT="$SCRIPT_DIR/searxng-maintenance.sh"
LOG_FILE="/home/openclaw/.openclaw/workspace/logs/searxng-maintenance.log"

echo "🦐 SearXNG 自动维护配置工具"
echo "=========================================="

# 确保脚本可执行
chmod +x "$MAINTENANCE_SCRIPT"
echo "✅ 脚本权限已设置"

# 获取当前 cron 列表
CURRENT_CRON=$(crontab -l 2>/dev/null || echo "")

# 检查是否已存在 SearXNG cron
if echo "$CURRENT_CRON" | grep -q "searxng-maintenance.sh"; then
    echo "⚠️  SearXNG 自动维护 Cron 已存在"
    echo ""
    echo "当前配置:"
    echo "$CURRENT_CRON" | grep "searxng-maintenance.sh"
    echo ""
    read -p "是否重新配置？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "✅ 保持现有配置"
        exit 0
    fi
    
    # 删除旧配置
    echo "$CURRENT_CRON" | grep -v "searxng-maintenance.sh" | crontab -
    echo "🗑️  已删除旧配置"
fi

# 添加 Cron 任务
# 1. 每 30 分钟检查一次健康状态
# 2. 每周日 03:00 更新镜像
# 3. 每天 04:00 清理缓存

CRON_CHECK="*/30 * * * * $MAINTENANCE_SCRIPT check >> $LOG_FILE 2>&1"
CRON_UPDATE="0 3 * * 0 $MAINTENANCE_SCRIPT update >> $LOG_FILE 2>&1"
CRON_CLEANUP="0 4 * * * $MAINTENANCE_SCRIPT cleanup >> $LOG_FILE 2>&1"

# 添加到 crontab
if [ -n "$CURRENT_CRON" ]; then
    (echo "$CURRENT_CRON"; echo "$CRON_CHECK"; echo "$CRON_UPDATE"; echo "$CRON_CLEANUP") | crontab -
else
    (echo "$CRON_CHECK"; echo "$CRON_UPDATE"; echo "$CRON_CLEANUP") | crontab -
fi

echo ""
echo "✅ Cron 配置成功!"
echo ""
echo "📅 定时任务:"
echo "   - 每 30 分钟：健康检查 + 自动修复"
echo "   - 每周日 03:00：更新镜像"
echo "   - 每天 04:00：清理缓存"
echo ""
echo "📝 日志位置：$LOG_FILE"
echo ""
echo "当前 Cron 列表:"
crontab -l | grep searxng || echo "(无)"
echo ""
echo "=========================================="
echo "💡 手动测试：$MAINTENANCE_SCRIPT status"
echo "🔧 编辑 Cron: crontab -e"
echo "📋 查看日志：tail -f $LOG_FILE"
echo "=========================================="
