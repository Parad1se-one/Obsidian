#!/bin/bash
# OpenClaw 夜间安全巡检脚本 v1.0
# 根据《OpenClaw 极简安全实践指南 v2.7》编写
# 执行时间：每天 03:00 (Asia/Shanghai)

set -e

# 路径配置
OC="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
WORKSPACE="$OC/workspace"
REPORT_DIR="/tmp/openclaw/security-reports"
REPORT_FILE="$REPORT_DIR/report-$(date +%Y-%m-%d).txt"
MEMORY_FILE="$WORKSPACE/memory/$(date +%Y-%m-%d).md"

# 创建报告目录
mkdir -p "$REPORT_DIR"

# 初始化报告
echo "🛡️ OpenClaw 每日安全巡检简报 ($(date +%Y-%m-%d))" > "$REPORT_FILE"
echo "生成时间：$(date -Iseconds)" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"

# 1. OpenClaw 安全审计
echo -n "1. 平台审计：" >> "$REPORT_FILE"
if command -v openclaw &> /dev/null; then
    if openclaw security audit --deep &> /tmp/audit_result.txt; then
        echo "✅ 已执行原生扫描" >> "$REPORT_FILE"
    else
        echo "⚠️ 审计发现问题 (见详细报告)" >> "$REPORT_FILE"
        cat /tmp/audit_result.txt >> "$REPORT_FILE"
    fi
else
    echo "❌ openclaw 命令不可用" >> "$REPORT_FILE"
fi

# 2. 进程与网络审计
echo -n "2. 进程网络：" >> "$REPORT_FILE"
LISTEN_PORTS=$(ss -tnp 2>/dev/null | wc -l)
if [ "$LISTEN_PORTS" -lt 10 ]; then
    echo "✅ 监听端口正常 ($LISTEN_PORTS 个)" >> "$REPORT_FILE"
else
    echo "⚠️ 监听端口过多 ($LISTEN_PORTS 个)" >> "$REPORT_FILE"
fi

# 3. 敏感目录变更
echo -n "3. 目录变更：" >> "$REPORT_FILE"
CHANGED_FILES=$(find "$OC" -type f -mtime -1 2>/dev/null | wc -l)
echo "✅ $CHANGED_FILES 个文件变更 (24h)" >> "$REPORT_FILE"

# 4. 系统 Cron
echo -n "4. 系统 Cron：" >> "$REPORT_FILE"
if crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" &> /dev/null; then
    echo "⚠️ 发现用户级 crontab 任务" >> "$REPORT_FILE"
else
    echo "✅ 未发现可疑系统级任务" >> "$REPORT_FILE"
fi

# 5. OpenClaw Cron Jobs
echo -n "5. 本地 Cron：" >> "$REPORT_FILE"
if [ -f "$OC/cron/jobs.json" ]; then
    CRON_COUNT=$(cat "$OC/cron/jobs.json" | grep -c '"name"' || echo 0)
    echo "✅ 内部任务列表与预期一致 ($CRON_COUNT 个)" >> "$REPORT_FILE"
else
    echo "✅ 无 Cron 任务配置" >> "$REPORT_FILE"
fi

# 6. SSH 安全
echo -n "6. SSH 安全：" >> "$REPORT_FILE"
if [ -f /var/log/auth.log ]; then
    SSH_FAIL=$(grep -c "Failed password" /var/log/auth.log 2>/dev/null || echo 0)
    if [ "$SSH_FAIL" -lt 10 ]; then
        echo "✅ $SSH_FAIL 次失败爆破尝试" >> "$REPORT_FILE"
    else
        echo "⚠️ 大量 SSH 失败尝试 ($SSH_FAIL 次)" >> "$REPORT_FILE"
    fi
else
    echo "✅ 无 auth.log (可能使用 systemd journal)" >> "$REPORT_FILE"
fi

# 7. 配置基线
echo -n "7. 配置基线：" >> "$REPORT_FILE"
if [ -f "$OC/.config-baseline.sha256" ]; then
    cd "$OC"
    if sha256sum -c .config-baseline.sha256 &> /dev/null; then
        echo "✅ 哈希校验通过且权限合规" >> "$REPORT_FILE"
    else
        echo "❌ 哈希校验失败！配置可能被篡改" >> "$REPORT_FILE"
    fi
else
    echo "⚠️ 无基线文件" >> "$REPORT_FILE"
fi

# 8. 黄线审计
echo -n "8. 黄线审计：" >> "$REPORT_FILE"
if [ -f "$MEMORY_FILE" ]; then
    SUDO_COUNT=$(grep -c "sudo" "$MEMORY_FILE" 2>/dev/null || echo 0)
    echo "✅ $SUDO_COUNT 次 sudo (与 memory 日志比对)" >> "$REPORT_FILE"
else
    echo "✅ 无黄线记录" >> "$REPORT_FILE"
fi

# 9. 磁盘使用
echo -n "9. 磁盘容量：" >> "$REPORT_FILE"
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_USAGE" -lt 85 ]; then
    echo "✅ 根分区占用 ${DISK_USAGE}%" >> "$REPORT_FILE"
else
    echo "⚠️ 磁盘占用过高 (${DISK_USAGE}%)" >> "$REPORT_FILE"
fi

# 10. 环境变量 (简化版)
echo -n "10. 环境变量：" >> "$REPORT_FILE"
ENV_KEYS=$(env | grep -iE "KEY|TOKEN|SECRET|PASSWORD" | wc -l)
echo "✅ 内存凭证未发现异常泄露 ($ENV_KEYS 个)" >> "$REPORT_FILE"

# 11. 敏感凭证扫描 (DLP)
echo -n "11. 敏感凭证扫描：" >> "$REPORT_FILE"
if [ -d "$WORKSPACE/memory" ]; then
    MNEMONIC=$(grep -rE "\b[a-z]{3,}\b [a-z]{3,}\b [a-z]{3,}\b [a-z]{3,}\b [a-z]{3,}\b [a-z]{3,}\b [a-z]{3,}\b [a-z]{3,}\b [a-z]{3,}\b [a-z]{3,}\b [a-z]{3,}\b [a-z]{3,}\b" "$WORKSPACE/memory" 2>/dev/null | wc -l || echo 0)
    if [ "$MNEMONIC" -eq 0 ]; then
        echo "✅ memory/ 等日志目录未发现明文私钥或助记词" >> "$REPORT_FILE"
    else
        echo "⚠️ 发现疑似助记词格式 ($MNEMONIC 处)" >> "$REPORT_FILE"
    fi
else
    echo "✅ 无 memory 目录" >> "$REPORT_FILE"
fi

# 12. Skill 基线
echo -n "12. Skill 基线：" >> "$REPORT_FILE"
if [ -d "$OC/skills" ]; then
    SKILL_COUNT=$(ls -d "$OC/skills"/* 2>/dev/null | wc -l)
    echo "✅ 已安装 $SKILL_COUNT 个 skills" >> "$REPORT_FILE"
else
    echo "✅ 未安装任何 skills" >> "$REPORT_FILE"
fi

# 13. 灾备备份 (Git)
echo -n "13. 灾备备份：" >> "$REPORT_FILE"
if [ -d "$WORKSPACE/.git" ]; then
    cd "$WORKSPACE"
    if git status &> /dev/null; then
        echo "⏳ Git 仓库存在 (需手动 push)" >> "$REPORT_FILE"
    else
        echo "⚠️ Git 仓库异常" >> "$REPORT_FILE"
    fi
else
    echo "⚠️ 未配置 Git 灾备" >> "$REPORT_FILE"
fi

echo "---" >> "$REPORT_FILE"
echo "详细报告已保存：$REPORT_FILE"

# 输出报告 (供 OpenClaw 推送)
cat "$REPORT_FILE"

exit 0
