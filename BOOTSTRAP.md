# BOOTSTRAP.md - 已完成 ✅

_上次启动时间：2026-03-05 | 状态：已配置完成_

---

## 🦐 当前身份

| 项目 | 配置 |
|------|------|
| **名字** | 小虾 (Xiao Xia / Little Shrimp) |
| **生物** | AI assistant (OpenClaw clawbot) |
| **风格** | Warm, helpful, concise — like a friendly companion who gets things done |
| **Emoji** | 🦐 |
| **用户** | Linyi Wang |
| **时区** | Asia/Shanghai |

---

## ✅ 已完成配置

### 核心技能
- [x] **财经日报** - 工作日 07:30 自动生成 + 质量检查 + Git push + 飞书通知
- [x] **RL 研究学习** - 每日心跳任务（上午/下午/晚间）
- [x] **质量检查** - 内容质量评分系统 (≥80 分通过)
- [x] **心跳任务** - 定期自学习 + 知识维护
- [x] **Feishu 集成** - 消息推送、文档管理

### Git 仓库
- [x] **Workspace**: `github.com/Parad1se-one/Obsidian` (master)
- [x] **Obsidian**: `github.com/Parad1se-one/Obsidian` (main)
- [x] **自动推送**: 财经日报自动生成后 commit + push

### Cron 定时任务
- [x] 财经日报：工作日 07:30
- [x] 心跳任务：09:00 / 14:00 / 20:00

---

## 📁 关键文件位置

```
/home/openclaw/.openclaw/workspace/
├── IDENTITY.md          # 身份配置
├── USER.md              # 用户信息
├── SOUL.md              # 行为准则（Cyber Lobster 风格）
├── AGENTS.md            # 安全红线/黄线规则
├── HEARTBEAT.md         # 心跳任务清单
├── memory/              # 每日记忆日志
├── logs/                # 运行日志
├── obsidian-repo/       # Obsidian 知识库 (Git 子模组)
└── skills/              # 技能脚本
    ├── financial-daily/ # 财经日报
    ├── rl-researcher/   # RL 研究学习
    ├── quality-checker/ # 质量检查
    └── self-learner/    # 自学习
```

---

## 🚀 快速命令

```bash
# 手动生成财经日报 (测试)
./skills/financial-daily/financial-daily-cron.sh --force

# 查看心跳状态
cat HEARTBEAT.md

# 查看今日记忆
cat memory/$(date +%Y-%m-%d).md

# 查看日志
tail -f logs/financial-daily.log
tail -f logs/heartbeat-exec.log

# Git 状态
cd obsidian-repo && git status
```

---

## 📝 下次启动检查清单

- [ ] 检查 Cron 任务是否正常运行：`crontab -l`
- [ ] 检查日志有无错误：`tail -100 logs/*.log`
- [ ] 检查 Git 仓库同步状态
- [ ] 检查 memory/ 目录是否正常记录

---

_Bootstrap 完成于 2026-03-05 | 最后更新：2026-03-09_
