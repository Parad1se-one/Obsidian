# Docker + Mihomo VPN 隔离方案

> ⚠️ **安全警告**: 不要在任何公开场合分享你的订阅链接！

---

## 📦 架构概览

```
┌─────────────────────────────────────────────────────────┐
│                    宿主机 (Host)                         │
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │   Main Agent    │    │   Docker Container          │ │
│  │  (正常网络)      │    │  ┌───────────────────────┐  │ │
│  │                 │    │  │   Mihomo (VPN)        │  │ │
│  │                 │    │  │   - 独立网络栈        │  │ │
│  │                 │    │  │   - 代理端口 7890     │  │ │
│  │                 │    │  │   - API 端口 9090     │  │ │
│  │                 │    │  └───────────────────────┘  │ │
│  │                 │    │         ↑                   │ │
│  │                 │    │    容器内进程                │ │
│  └─────────────────┘    └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**关键点:**
- ✅ 宿主机网络配置**不受影响**
- ✅ 容器内独立运行 mihomo
- ✅ 通过代理端口 (7890) 访问 VPN

---

## 🚀 快速开始

### 1. 初始化

```bash
cd /home/openclaw/.openclaw/workspace
chmod +x skills/docker-vpn-agent/docker-vpn-agent.sh
./skills/docker-vpn-agent/docker-vpn-agent.sh setup
```

### 2. 配置 Mihomo

编辑配置文件：
```bash
./skills/docker-vpn-agent/docker-vpn-agent.sh config
```

**配置位置:** `.docker/mihomo/config.yaml`

**两种配置方式:**

#### 方式 A: 手动配置节点 (推荐)
```yaml
proxies:
  - name: "My Node"
    type: vmess
    server: example.com
    port: 443
    uuid: your-uuid
    alterId: 0
    cipher: auto
    tls: true

proxy-groups:
  - name: "PROXY"
    type: select
    proxies:
      - "My Node"

rules:
  - MATCH,PROXY
```

#### 方式 B: 使用订阅 (注意安全)
```yaml
# 不要直接写在 config.yaml 里！
# 使用订阅转换工具转换为本地点配置
```

### 3. 启动服务

```bash
./skills/docker-vpn-agent/docker-vpn-agent.sh start
./skills/docker-vpn-agent/docker-vpn-agent.sh status
```

### 4. 测试连接

```bash
# 在容器内测试 (走 VPN)
./skills/docker-vpn-agent/docker-vpn-agent.sh exec "curl ip.sb"

# 在宿主机通过代理测试
./skills/docker-vpn-agent/docker-vpn-agent.sh proxy "curl ip.sb"

# 直接测试 (不走 VPN，对比用)
curl ip.sb
```

---

## 📋 常用命令

| 命令 | 说明 |
|------|------|
| `./docker-vpn-agent.sh setup` | 首次初始化 |
| `./docker-vpn-agent.sh start` | 启动容器 |
| `./docker-vpn-agent.sh stop` | 停止并删除容器 |
| `./docker-vpn-agent.sh status` | 查看状态 |
| `./docker-vpn-agent.sh exec <cmd>` | 在容器内执行命令 |
| `./docker-vpn-agent.sh proxy <cmd>` | 通过代理执行命令 |
| `./docker-vpn-agent.sh config` | 编辑配置 |
| `./docker-vpn-agent.sh logs` | 查看日志 |

---

## 🔧 与 Subagent 集成

### 方案 1: 在容器内运行 Subagent

```bash
# 在容器内启动 OpenClaw subagent
./docker-vpn-agent.sh exec "
  cd /workspace && \
  export http_proxy=http://127.0.0.1:7890 && \
  export https_proxy=http://127.0.0.1:7890 && \
  openclaw sessions_spawn --task '访问需要 VPN 的资源'
"
```

### 方案 2: 宿主机 Subagent 通过代理访问

```bash
# 创建 VPN 感知的 subagent 脚本
cat > skills/vpn-subagent/vpn-subagent.sh << 'EOF'
#!/bin/bash
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
export ALL_PROXY="http://127.0.0.1:7890"
exec "$@"
EOF
chmod +x skills/vpn-subagent/vpn-subagent.sh

# 使用
./skills/vpn-subagent/vpn-subagent.sh python3 vpn-task.py
```

---

## 🛡️ 安全最佳实践

### 1. 保护订阅信息
```bash
# ❌ 不要这样做
echo "subscription_url" >> config.yaml

# ✅ 正确做法
# 1. 使用订阅转换工具 (如 subconverter)
# 2. 转换为本地点配置
# 3. 删除原始订阅 URL
```

### 2. 限制容器权限
```bash
# 仅开放必要端口
-p 7890:7890  # HTTP 代理
-p 9090:9090  # API (可限制访问 IP)

# 不要开放
# -p 9091:9091  # Dashboard (除非必要)
```

### 3. 定期清理日志
```bash
docker logs --tail 100 "$CONTAINER_NAME" > /dev/null
docker system prune -f
```

---

## 🐛 故障排查

### 问题 1: 容器无法启动
```bash
# 检查 Docker
docker ps

# 查看日志
./docker-vpn-agent.sh logs

# 检查配置
docker exec mihomo-agent cat /root/.config/mihomo/config.yaml
```

### 问题 2: 代理不工作
```bash
# 检查 mihomo API
curl http://localhost:9090/proxies

# 测试代理连接
curl --proxy http://127.0.0.1:7890 https://httpbin.org/ip
```

### 问题 3: DNS 泄漏
```bash
# 在容器内测试
./docker-vpn-agent.sh exec "nslookup google.com"

# 应该返回代理服务器的 DNS，而不是本地 DNS
```

---

## 📊 性能监控

```bash
# 查看容器资源使用
docker stats mihomo-agent

# 查看连接数
curl http://localhost:9090/connections | jq '.downloadTotal'
```

---

## 🔗 相关资源

- **Mihomo GitHub:** https://github.com/MetaCubeX/mihomo
- **Docker 镜像:** https://github.com/MetaCubeX/mihomo/pkgs/container/mihomo
- **配置文档:** https://wiki.metacubex.one

---

**⚠️ 最后提醒:**
- 不要在公开场合分享订阅链接
- 定期更换订阅 URL
- 遵守当地法律法规

**🦐 小虾：配置框架已搭好，订阅配置你自己填。安全第一！**
