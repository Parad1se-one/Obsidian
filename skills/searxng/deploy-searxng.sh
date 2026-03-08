#!/bin/bash
# deploy-searxng.sh - 部署 SearXNG 元搜索引擎
# 用法：./deploy-searxng.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/openclaw/.openclaw/workspace"
DOCKER_DIR="$WORKSPACE/.docker/searxng"
LOG_FILE="$WORKSPACE/logs/searxng-deploy.log"

mkdir -p "$DOCKER_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "🔍 SearXNG 部署脚本"
log "=========================================="

# 1. 检查 mihomo 容器
log "📋 检查 mihomo 容器状态..."
if ! sudo docker ps --format '{{.Names}}' | grep -q mihomo-agent; then
    log "❌ mihomo-agent 容器未运行，请先启动代理容器"
    exit 1
fi
log "✅ mihomo-agent 运行中"

# 2. 创建 SearXNG 配置
log "📝 创建 SearXNG 配置文件..."

mkdir -p "$DOCKER_DIR/searxng"

cat > "$DOCKER_DIR/searxng/settings.yml" << 'SEARXNG_CONFIG'
# SearXNG 配置
use_default_settings: true

general:
  debug: false
  instance_name: "SearXNG"
  donation_url: false
  contact_url: false
  enable_metrics: false

search:
  safe_search: 0
  autocomplete: "google"
  default_lang: "zh-CN"
  formats:
    - html
    - json

server:
  secret_key: "searxng-secret-key-change-me"
  limiter: false
  image_proxy: true
  http_protocol_version: "1.1"

engines:
  # 搜索引擎
  - name: google
    engine: google
    shortcut: g
    disabled: false
    
  - name: bing
    engine: bing
    shortcut: b
    disabled: false
    
  - name: duckduckgo
    engine: duckduckgo
    shortcut: ddg
    disabled: false
    
  # 学术搜索
  - name: google scholar
    engine: google_scholar
    shortcut: gs
    disabled: false
    
  - name: arxiv
    engine: arxiv
    shortcut: arx
    disabled: false
    
  # 代码
  - name: github
    engine: github
    shortcut: gh
    disabled: false
    
  # 新闻
  - name: google news
    engine: google_news
    shortcut: gn
    disabled: false
    
  # 禁用有问题的引擎
  - name: wikimedia
    engine: wikimedia
    shortcut: wm
    disabled: false

outgoing:
  request_timeout: 5.0
  max_request_timeout: 15.0
  useragent_suffix: ""
  
ui:
  default_theme: simple
  query_in_title: true
  infinite_scroll: true
  center_alignment: true
  
plugins:
  - plugin: self_info
    enabled: true
SEARXNG_CONFIG

log "✅ 配置文件创建完成"

# 3. 创建 Docker 卷
log "📦 创建 Docker 卷..."
sudo docker volume create searxng-data 2>/dev/null || true
log "✅ Docker 卷创建完成"

# 4. 启动容器
log "🚀 启动 SearXNG 容器..."

# 先停止旧容器 (如果存在)
sudo docker stop searxng 2>/dev/null || true
sudo docker rm searxng 2>/dev/null || true

# 启动新容器
sudo docker run -d \
  --name searxng \
  --network container:mihomo-agent \
  -e SEARXNG_BASE_URL=http://127.0.0.1:8080 \
  -e SEARXNG_SECRET=searxng-secret-key-change-me \
  -v "$DOCKER_DIR/searxng/settings.yml:/etc/searxng/settings.yml:ro" \
  -v searxng-data:/var/lib/searxng \
  --restart unless-stopped \
  searxng/searxng:latest

# 5. 等待容器启动
log "⏳ 等待容器启动..."
sleep 10

# 6. 检查状态
if sudo docker ps --format '{{.Names}}' | grep -q searxng; then
    log "✅ SearXNG 部署成功!"
    log ""
    log "📍 访问地址:"
    log "   Web UI: http://127.0.0.1:8080"
    log "   API:    http://127.0.0.1:8080/search?q=xxx&format=json"
    log ""
    log "📋 管理命令:"
    log "   查看日志：docker logs searxng"
    log "   重启：docker compose restart"
    log "   停止：docker compose down"
else
    log "❌ SearXNG 启动失败，请检查日志"
    sudo docker logs searxng 2>&1 | tail -20
    exit 1
fi

log "=========================================="
log "✅ SearXNG 部署完成"
log "=========================================="
