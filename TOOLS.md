# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

**最后更新**: 2026-03-09

---

## 🦐 小虾的本地配置

### Git 仓库

| 仓库 | 路径 | 分支 | 说明 |
|------|------|------|------|
| **Workspace** | `/home/openclaw/.openclaw/workspace` | `master` | 主工作区 |
| **Obsidian** | `obsidian-repo/` (子模组) | `main` | 知识库/财经日报 |
| **Remote** | `github.com/Parad1se-one/Obsidian` | - | 统一仓库 |

### Cron 定时任务

| 任务 | 时间 | 脚本 | 日志 |
|------|------|------|------|
| **财经日报** | 工作日 07:30 | `skills/financial-daily/financial-daily-cron.sh` | `logs/financial-daily-cron.log` |
| **心跳检查** | 每小时 | `skills/heartbeat/heartbeat-cron.sh` | `logs/heartbeat-cron.log` |

### 代理配置

```bash
# Mihomo 代理
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

### Feishu 配置

- **Channel**: `feishu`
- **User ID**: `ou_519fce3fc3512f400ecc41a440758fc1` (Linyi)
- **推送**: 财经日报、心跳通知、警报

### 快速命令

```bash
# 查看 Cron
crontab -l

# 查看今日日志
tail -f logs/financial-daily.log
tail -f logs/heartbeat-exec.log

# 手动测试财经日报
./skills/financial-daily/financial-daily-cron.sh --force

# Git 状态检查
cd obsidian-repo && git status
```

---

## 通用模板

### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod

---

Add whatever helps you do your job. This is your cheat sheet.
