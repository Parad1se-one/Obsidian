#!/bin/bash
# whoogle-maintenance.sh - Whoogle 自动维护脚本
# 用法：./whoogle-maintenance.sh [check|restart|status]

set -e

WORKSPACE="/home/openclaw/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/whoogle-maintenance.log"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_health() {
    log "🔍 检查 Whoogle 健康状态..."
    
    if ! sudo docker ps --format '{{.Names}}' | grep -q whoogle; then
        log "❌ 容器未运行"
        return 1
    fi
    log "✅ 容器运行中"
    
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/ 2>/dev/null || echo "000")
    if [ "$RESPONSE" = "200" ]; then
        log "✅ Web UI 可访问 (HTTP $RESPONSE)"
        return 0
    else
        log "❌ Web UI 不可访问 (HTTP $RESPONSE)"
        return 1
    fi
}

auto_restart() {
    log "🔄 重启 Whoogle..."
    
    if sudo docker ps --format '{{.Names}}' | grep -q whoogle; then
        sudo docker restart whoogle
    else
        sudo docker run -d --name whoogle --network host \
          -e whoogle_port=5000 \
          -e http_proxy=http://127.0.0.1:7890 \
          -e https_proxy=http://127.0.0.1:7890 \
          --restart unless-stopped \
          benbusby/whoogle-search:latest
    fi
    
    sleep 10
    
    if check_health; then
        log "✅ 重启成功"
        return 0
    else
        log "❌ 重启失败"
        return 1
    fi
}

show_status() {
    echo "=========================================="
    echo "🔍 Whoogle 状态"
    echo "=========================================="
    
    sudo docker ps --filter "name=whoogle" --format "table {{.Names}}\t{{.Status}}"
    
    echo ""
    echo "🌐 API 测试:"
    curl -s -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1:5000/ 2>/dev/null || echo "不可访问"
    
    echo ""
    echo "=========================================="
}

case "${1:-check}" in
    check)
        if check_health; then
            log "✅ Whoogle 运行正常"
            exit 0
        else
            log "⚠️  Whoogle 异常，尝试自动修复..."
            auto_restart && exit 0 || exit 1
        fi
        ;;
    restart)
        auto_restart
        ;;
    status)
        show_status
        ;;
    *)
        echo "用法：$0 [check|restart|status]"
        exit 1
        ;;
esac
