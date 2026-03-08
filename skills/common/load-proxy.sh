#!/bin/bash
# load-proxy.sh - 智能代理加载脚本
# 用法：source "$(dirname "$0")/load-proxy.sh"

# 检查 mihomo-agent 容器是否运行
if sudo docker ps --format '{{.Names}}' 2>/dev/null | grep -q mihomo-agent; then
    # 启用代理
    export http_proxy=http://127.0.0.1:7890
    export https_proxy=http://127.0.0.1:7890
    export ALL_PROXY=socks5://127.0.0.1:7890
    
    # 排除列表 (直连)
    # - 飞书/字节系 (IM/API)
    # - 国内服务 (阿里云、腾讯云等)
    # - 本地网络
    # - GitHub SSH (不受 http_proxy 影响)
    export NO_PROXY="localhost,127.0.0.1,\
*.feishu.cn,*.feishucn.com,*.bytedance.com,\
*.cn,*.aliyuncs.com,*.tencent.com,\
192.168.*,10.*,172.*"
    
    echo "✅ 代理已启用 (mihomo-agent) | 飞书/国内服务走直连" >&2
else
    # 容器未运行，清除代理配置
    unset http_proxy https_proxy ALL_PROXY
    echo "⚠️ 代理容器未运行，使用直连" >&2
fi
