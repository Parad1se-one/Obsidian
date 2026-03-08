#!/bin/bash
# searxng-maintenance.sh - SearXNG 自动维护脚本
# 用法：./searxng-maintenance.sh [check|restart|update|status]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/openclaw/.openclaw/workspace"
DOCKER_DIR="$WORKSPACE/.docker/searxng"
LOG_FILE="$WORKSPACE/logs/searxng-maintenance.log"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查 SearXNG 健康状态
check_health() {
    log "🔍 检查 SearXNG 健康状态..."
    
    # 检查容器是否运行
    if ! sudo docker ps --format '{{.Names}}' | grep -q searxng; then
        log "❌ 容器未运行"
        return 1
    fi
    log "✅ 容器运行中"
    
    # 检查健康检查状态
    HEALTH=$(sudo docker inspect --format='{{.State.Health.Status}}' searxng 2>/dev/null || echo "unknown")
    log "📊 健康状态：$HEALTH"
    
    # 检查 API 可访问性
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/healthz 2>/dev/null || echo "000")
    if [ "$RESPONSE" = "200" ]; then
        log "✅ API 可访问 (HTTP $RESPONSE)"
        return 0
    else
        log "❌ API 不可访问 (HTTP $RESPONSE)"
        return 1
    fi
}

# 自动重启
auto_restart() {
    log "🔄 尝试重启 SearXNG..."
    
    if sudo docker ps --format '{{.Names}}' | grep -q searxng; then
        sudo docker restart searxng
    else
        # 重新创建容器
        sudo docker run -d \
          --name searxng \
          --network container:mihomo-agent \
          -e SEARXNG_BASE_URL=http://127.0.0.1:8080 \
          -e SEARXNG_SECRET=searxng-secret-key-change-me \
          -v "$DOCKER_DIR/searxng/settings.yml:/etc/searxng/settings.yml:ro" \
          -v searxng-data:/var/lib/searxng \
          --restart unless-stopped \
          searxng/searxng:latest
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

# 更新镜像
update_image() {
    log "📦 更新 SearXNG 镜像..."
    
    sudo docker pull searxng/searxng:latest
    
    log "✅ 镜像更新完成，重启容器..."
    auto_restart
}

# 清理缓存
cleanup_cache() {
    log "🧹 清理 SearXNG 缓存..."
    
    # 清理 Docker 卷中的缓存数据
    sudo docker exec searxng rm -rf /var/lib/searxng/cache/* 2>/dev/null || true
    
    log "✅ 缓存清理完成"
}

# 显示状态
show_status() {
    echo "=========================================="
    echo "🔍 SearXNG 状态"
    echo "=========================================="
    
    # 容器状态
    echo ""
    echo "📦 容器信息:"
    sudo docker ps --filter "name=searxng" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    # 健康状态
    echo ""
    echo "💚 健康检查:"
    sudo docker inspect --format='{{.State.Health.Status}}' searxng 2>/dev/null || echo "未知"
    
    # 资源使用
    echo ""
    echo "📊 资源使用:"
    sudo docker stats searxng --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
    
    # API 测试
    echo ""
    echo "🌐 API 测试:"
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/healthz 2>/dev/null || echo "000")
    echo "   Healthz: HTTP $RESPONSE"
    
    echo ""
    echo "=========================================="
}

# 主逻辑
case "${1:-check}" in
    check)
        if check_health; then
            log "✅ SearXNG 运行正常"
            exit 0
        else
            log "⚠️  SearXNG 异常，尝试自动修复..."
            if auto_restart; then
                log "✅ 自动修复成功"
                exit 0
            else
                log "❌ 自动修复失败，需要人工干预"
                exit 1
            fi
        fi
        ;;
    
    restart)
        auto_restart
        ;;
    
    update)
        update_image
        ;;
    
    cleanup)
        cleanup_cache
        ;;
    
    status)
        show_status
        ;;
    
    *)
        echo "用法：$0 [check|restart|update|cleanup|status]"
        echo ""
        echo "命令说明:"
        echo "  check    - 健康检查 (默认)"
        echo "  restart  - 重启容器"
        echo "  update   - 更新镜像"
        echo "  cleanup  - 清理缓存"
        echo "  status   - 显示状态"
        exit 1
        ;;
esac
