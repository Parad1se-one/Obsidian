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
- **推送**: 财经日报、心跳通知、警报、RL 研究日报
- **权限**: ✅ 已授权所有必要权限
- **重要**: 不要申请新的权限，当前权限已足够

---

## 📁 Obsidian 路径配置

### 日报存储路径

| 类型 | 路径 | 命名格式 |
|------|------|---------|
| 财经日报 | `10-Daily/财经日报/` | `财经日报 YYYY-MM-DD.md` |
| RL 研究日报 | `20-RL/论文/` | `YYYY-MM-DD-RL 研究日报.md` |
| 每日总结 | `10-Daily/每日总结/` | `daily-summary-YYYY-MM-DD.md` |
| RL 探索记录 | `20-RL/探索记录/` | `rl-exploration-YYYY-MM-DD-HHh.md` |

### 快速命令

```bash
# 查看今日财经日报
cat obsidian-repo/10-Daily/财经日报/财经日报\ $(date +%Y-%m-%d).md

# 查看今日 RL 日报
cat obsidian-repo/20-RL/论文/$(date +%Y-%m-%d)-RL\ 研究日报.md

# Git 状态检查
cd obsidian-repo && git status

# 手动推送
cd obsidian-repo && git add . && git commit -m "📅 日报 $(date +%Y-%m-%d)" && git push
```

---

## 📚 RL 研究日报 - 数据来源配置

### 核心来源
| 来源 | 类型 | 更新频率 |
|------|------|---------|
| arXiv cs.LG/cs.AI | 论文预印本 | 每日 |
| arXiv cs.MA (多智能体) | 论文预印本 | 每日 |
| DeepMind Blog | 官方博客 | 不定期 |
| OpenAI Blog | 官方博客 | 不定期 |
| Google AI Blog | 官方博客 | 不定期 |
| Meta AI Blog | 官方博客 | 不定期 |

### 顶级会议/期刊
| 名称 | 类型 | 重点领域 |
|------|------|---------|
| ICLR | 会议 | 深度学习表征学习 |
| NeurIPS | 会议 | 神经信息处理系统 |
| ICML | 会议 | 机器学习 |
| CoRL | 会议 | 机器人学习 |
| AAMAS | 会议 | 多智能体系统 |
| JMLR | 期刊 | 机器学习研究 |
| TMLR | 期刊 | 机器学习研究 |

### 其他来源
- Nature Machine Intelligence
- Science Robotics
- PNAS (AI/ML 方向)
- 各大实验室 GitHub (DeepMind, OpenAI, FAIR 等)

### Cron 定时任务

| 任务 | 时间 | 脚本 | 输出位置 |
|------|------|------|---------|
| 财经日报 V2 | 工作日 07:30 | `skills/financial-daily-v2/financial-daily.sh` | `10-Daily/财经日报/` |
| RL 研究日报 V2 | 工作日 09:00 | `skills/rl-researcher/rl-daily.sh` | `20-RL/论文/` |
| RL 探索学习 | 10:00/14:00/20:00 | `skills/rl-researcher/explore.sh` | `20-RL/探索记录/` |
| 心跳检查 | 每小时 | `skills/heartbeat/heartbeat-cron.sh` | `logs/heartbeat-exec.log` |

---

## 📊 日报 V2 格式

### 财经日报 V2
- 🔢 市场速览 (4 指数表格)
- 💡 核心摘要 (≤3 条)
- 🏭 行业快讯 (≥5 个分类)
- 📰 深度报道 (精选 5 条)
- 📅 财经日历 (3-5 天)
- 🎯 明日关注 (≥3 条)

### RL 研究日报 V2
- 🔥 必读 Top 3 (带 arXiv 链接)
- 📄 全部论文 (按主题分类表格)
- 📊 趋势洞察 (热度标记🔥)
- 🎯 小虾点评 (行动建议)
- 📅 近期会议/截稿

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
