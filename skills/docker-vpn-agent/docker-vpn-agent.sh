#!/bin/bash
# docker-vpn-agent.sh - Docker 容器运行 mihomo + Subagent
# 网络隔离：容器内运行 VPN，宿主机网络不受影响

set -e

CONTAINER_NAME="mihomo-agent"
IMAGE_NAME="mihomo:latest"
WORKSPACE="/home/openclaw/.openclaw/workspace"
MIHOMO_CONFIG="/home/openclaw/.openclaw/workspace/.docker/mihomo/config.yaml"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# 检查 Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    log "Docker 版本：$(docker --version)"
}

# 创建配置目录
setup_dirs() {
    log "创建配置目录..."
    mkdir -p "$(dirname "$MIHOMO_CONFIG")"
    mkdir -p "$WORKSPACE/.docker/mihomo/data"
}

# 拉取 mihomo 镜像
pull_image() {
    log "拉取 mihomo 镜像..."
    # 使用国内镜像源
    if sudo docker pull docker.1panel.live/metacubex/mihomo:latest 2>/dev/null; then
        log "✅ 镜像拉取成功：docker.1panel.live/metacubex/mihomo"
        return 0
    elif sudo docker pull ghcr.io/metacubex/mihomo:latest 2>/dev/null; then
        log "✅ 镜像拉取成功：ghcr.io/metacubex/mihomo"
        return 0
    else
        warn "所有镜像源拉取失败"
        return 1
    fi
}

# 生成 mihomo 配置模板
generate_config() {
    cat > "$MIHOMO_CONFIG" << 'EOF'
# Mihomo 配置模板
# 请在此文件中配置你的订阅或节点

# 订阅配置 (二选一)
# 方式 1: 直接填写订阅 URL (不推荐，日志会暴露)
# external-controller: 0.0.0.0:9090
# profile:
#   store-selected: true
#   store-fake-ip: true

# 方式 2: 手动配置节点 (推荐)
proxies:
  # 示例节点，请替换为你的实际节点
  # - name: "Example Node"
  #   type: vmess
  #   server: example.com
  #   port: 443
  #   uuid: your-uuid
  #   alterId: 0
  #   cipher: auto
  #   tls: true

proxy-groups:
  - name: "PROXY"
    type: select
    proxies:
      - DIRECT
      # - 你的节点名称

rules:
  - DOMAIN-SUFFIX,google.com,PROXY
  - DOMAIN-SUFFIX,github.com,PROXY
  - DOMAIN,api.openai.com,PROXY
  - GEOIP,CN,DIRECT
  - MATCH,DIRECT

# 其他配置
external-controller: 0.0.0.0:9090
allow-lan: false
mode: rule
log-level: info
ipv6: false
EOF
    log "配置模板已生成：$MIHOMO_CONFIG"
    warn "请编辑 $MIHOMO_CONFIG 填入你的节点配置"
}

# 启动容器
start_container() {
    log "启动 mihomo 容器..."
    
    sudo docker run -d \
        --name "$CONTAINER_NAME" \
        --restart unless-stopped \
        --cap-add=NET_ADMIN \
        --network=bridge \
        -v "$MIHOMO_CONFIG:/root/.config/mihomo/config.yaml:ro" \
        -v "$WORKSPACE/.docker/mihomo/data:/root/.config/mihomo/data" \
        -p 9090:9090 \
        -p 7890:7890 \
        -e TZ="Asia/Shanghai" \
        docker.1panel.live/metacubex/mihomo:latest 2>/dev/null || \
    {
        error "镜像启动失败，请检查 Docker 和镜像"
        exit 1
    }
    
    log "容器已启动：$CONTAINER_NAME"
}

# 检查容器状态
check_status() {
    log "检查容器状态..."
    sudo docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    # 检查 mihomo API
    sleep 3
    if curl -s http://localhost:9090/proxies > /dev/null 2>&1; then
        log "✅ mihomo API 正常"
    else
        warn "⚠️ mihomo API 未响应，请检查配置"
    fi
}

# 在容器内运行命令
run_in_container() {
    local cmd="$1"
    log "在容器内执行：$cmd"
    sudo docker exec "$CONTAINER_NAME" sh -c "$cmd"
}

# 通过代理运行命令 (宿主机)
run_with_proxy() {
    local cmd="$1"
    log "通过代理执行：$cmd"
    
    export http_proxy="http://127.0.0.1:7890"
    export https_proxy="http://127.0.0.1:7890"
    export ALL_PROXY="http://127.0.0.1:7890"
    
    eval "$cmd"
    
    unset http_proxy https_proxy ALL_PROXY
}

# 停止容器
stop_container() {
    log "停止容器..."
    sudo docker stop "$CONTAINER_NAME" 2>/dev/null || true
    sudo docker rm "$CONTAINER_NAME" 2>/dev/null || true
    log "容器已停止"
}

# 显示帮助
show_help() {
    cat << EOF
🦐 Docker + Mihomo VPN 隔离方案

用法：$0 <command> [options]

命令:
  setup       初始化和启动容器
  start       启动容器
  stop        停止并删除容器
  status      查看状态
  exec <cmd>  在容器内执行命令
  proxy <cmd> 通过代理执行命令 (宿主机)
  config      编辑配置文件
  logs        查看日志
  help        显示帮助

示例:
  $0 setup              # 首次初始化
  $0 status             # 查看状态
  $0 exec "curl ip.sb"  # 在容器内测试 IP
  $0 proxy "curl ip.sb" # 通过代理测试 IP
  $0 config             # 编辑 mihomo 配置

EOF
}

# 主逻辑
main() {
    case "${1:-help}" in
        setup)
            check_docker
            setup_dirs
            pull_image
            generate_config
            start_container
            check_status
            ;;
        start)
            sudo docker start "$CONTAINER_NAME" 2>/dev/null || start_container
            ;;
        stop)
            stop_container
            ;;
        status)
            check_status
            ;;
        exec)
            shift
            run_in_container "$*"
            ;;
        proxy)
            shift
            run_with_proxy "$*"
            ;;
        config)
            ${EDITOR:-nano} "$MIHOMO_CONFIG"
            sudo docker restart "$CONTAINER_NAME" 2>/dev/null
            ;;
        logs)
            sudo docker logs -f "$CONTAINER_NAME"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "未知命令：$1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
