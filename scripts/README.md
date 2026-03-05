# 自动化脚本和工具

**创建时间**: 2026-03-05  
**整理者**: 小虾 🦐 (OpenClaw Assistant)

---

## 📁 文件夹用途

`scripts/` 存放常用的自动化脚本和工具，帮助你：
- 自动化日常任务
- 批量处理文件
- 快速生成报告
- 系统配置和管理

---

## 📄 脚本清单

### 日常日志相关

| 脚本 | 用途 | 状态 |
|------|------|------|
| `daily-logger.sh` | 手动创建每日日志 | ✅ 可用 |
| `auto-daily-log.sh` | 自动整理每日内容 | ✅ 可用 |

---

## 🔧 使用说明

### daily-logger.sh
手动创建今日日志：
```bash
./daily-logger.sh
```

**功能**:
- 创建 `daily/work/YYYY-MM-DD.md`
- 添加基础模板结构
- 记录创建时间

---

### auto-daily-log.sh
自动整理每日内容（建议配置 cron）：
```bash
./auto-daily-log.sh
```

**功能**:
- 扫描未归档的对话记录
- 自动分类到对应文件夹
- 生成摘要

---

## 🤖 Cron 配置示例

### 每日凌晨自动整理
```bash
# 编辑 crontab
crontab -e

# 添加任务（每天 00:00）
0 0 * * * /home/openclaw/.openclaw/workspace/obsidian-repo/scripts/auto-daily-log.sh >> /var/log/auto-daily.log 2>&1
```

### 财经日报（工作日 7:30）
```bash
# 在 financial-daily 目录执行
cd /home/openclaw/.openclaw/workspace/skills/financial-daily
./setup-cron.sh
```

---

## 📝 脚本开发规范

### Bash 脚本模板
```bash
#!/bin/bash
# script-name.sh - 简短描述
# 用法：./script-name.sh [参数]

set -e  # 遇到错误立即退出

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 函数定义
log_info() {
    echo "✅ $1"
}

log_error() {
    echo "❌ 错误：$1" >&2
}

# 主逻辑
main() {
    log_info "开始执行..."
    # 你的代码
    log_info "执行完成"
}

main "$@"
```

### 权限设置
```bash
chmod +x script-name.sh
```

---

## 🛡️ 安全提示

1. **审查脚本**: 运行前阅读脚本内容
2. **备份重要数据**: 特别是涉及文件操作的脚本
3. **最小权限**: 不要随意使用 `sudo`
4. **日志记录**: 关键操作记录到日志文件

---

## 📦 依赖检查

### 检查脚本依赖
```bash
# 检查是否安装了必要的工具
which jq curl git
```

### 安装依赖（Ubuntu/Debian）
```bash
sudo apt update
sudo apt install -y jq curl git
```

---

## 🦐 小虾备注

- 脚本不在多，在精。每个脚本都应该解决实际问题
- 写好注释，未来的你会感谢现在的你
- 测试充分再投入使用
- 需要新脚本随时叫我，我帮你写

**最后更新**: 2026-03-05
