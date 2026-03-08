#!/bin/bash
# setup-whoogle-cron.sh - 配置 Whoogle 自动维护 Cron 任务

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAINTENANCE_SCRIPT="$SCRIPT_DIR/whoogle-maintenance.sh"
LOG_FILE="/home/openclaw/.openclaw/workspace/logs/whoogle-maintenance.log"

chmod +x "$MAINTENANCE_SCRIPT"

CURRENT_CRON=$(crontab -l 2>/dev/null || echo "")

if echo "$CURRENT_CRON" | grep -q "whoogle-maintenance.sh"; then
    echo "⚠️  Cron 已配置"
    crontab -l | grep whoogle
    exit 0
fi

CRON_CHECK="*/30 * * * * $MAINTENANCE_SCRIPT check >> $LOG_FILE 2>&1"

if [ -n "$CURRENT_CRON" ]; then
    (echo "$CURRENT_CRON"; echo "$CRON_CHECK") | crontab -
else
    echo "$CRON_CHECK" | crontab -
fi

echo "✅ Cron 配置完成：每 30 分钟自动检查"
crontab -l | grep whoogle
