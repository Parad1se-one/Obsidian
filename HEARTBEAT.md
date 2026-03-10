# HEARTBEAT.md - 心跳任务清单

> 🦐 小虾：心跳时不只是报平安，还要做有意义的事。
> 
> **自动执行机制:** ✅ 已配置 cron
> **手动触发:** 用户 heartbeat poll 时显示待执行任务状态
> 
> **最后更新**: 2026-03-10 - Cron 简化配置

---

## 📋 Cron 定时任务 (2026-03-10 简化配置)

### 📈 财经日报 (工作日 07:30)
- **脚本**: `skills/financial-daily/financial-daily-cron.sh`
- **推送**: 飞书消息 + Git 自动提交
- **日志**: `logs/financial-daily-cron.log`

### 🤖 RL 每日简报 (每天 09:00)
- **脚本**: `skills/rl-researcher/rl-daily-brief.sh`
- **推送**: 飞书消息 (研究方向 + 热点话题)
- **日志**: `logs/rl-daily-brief.log`

### 🔍 RL 探索学习 (每 2 小时，10:00-20:00)
- **脚本**: `skills/rl-researcher/rl-exploration.sh`
- **推送**: 每次执行都通知
- **日志**: `logs/rl-exploration.log`
- **输出**: `obsidian-repo/knowledge/rl/explorations/`

### 📅 每日总结 (每天 23:59)
- **脚本**: `skills/daily-summary/daily-summary.sh`
- **推送**: 飞书消息 (当日任务统计 + 重要事件)
- **日志**: `logs/daily-summary.log`
- **输出**: `obsidian-repo/daily/summaries/`

---

## 🧹 系统维护

### 每日任务
- **00:00** - Obsidian 日志生成
- **04:00** - SearXNG 清理

### 每周任务
- **周日 03:00** - SearXNG 更新

### 定期检查
- **每 30 分钟** - SearXNG/Whoogle 健康检查

---

## 📝 心跳响应规则

**如果无事发生:** 回复 `HEARTBEAT_OK`

**如果有学习内容:** 简要汇报学习收获

**如果有紧急事项:** 立即通知用户

**如果质量检查失败:** 说明原因并重做

---

*最后更新：2026-03-09 | 版本：v2.1 (财经日报自动 Git push)*

---

## 🔄 更新日志

### 2026-03-09 - 财经日报自动化增强
- ✅ 财经日报 Cron 增加自动 Git commit + push 功能
- ✅ 流程更新：生成 → 质检 → Git 推送 → 飞书通知
- ✅ 提交格式：`📈 财经日报 YYYY-MM-DD [auto]`

---

## 🤖 自动执行机制 (2026-03-08 新增)

### OpenViking 记忆同步
**脚本:** `skills/openviking/openviking-sync.sh`
**触发:** 每小时 heartbeat 检查时自动同步
**日志:** `logs/openviking-sync.log`

### Heartbeat 任务执行
**配置脚本:** `skills/heartbeat/setup-heartbeat-cron.sh`

**执行逻辑:**
- 每小时检查一次 (cron: `0 * * * *`)
- 自动判断当前时间是否在任务执行窗口内
- 检查日志避免重复执行
- 自动执行 + 记录日志

**任务窗口:**
| 任务 | 目标时间 | 执行窗口 | 说明 |
|------|----------|----------|------|
| 财经日报 | 工作日 07:30 | 07:00-08:00 | 自动执行 |
| RL 学习 (上午) | 09:00 | 08:30-09:30 | 自动执行 |
| RL 学习 (下午) | 14:00 | 13:30-14:30 | 自动执行 |
| RL 学习 (晚间) | 20:00 | 19:30-21:30 | 自动执行 |
| 周日维护 | 周日 10:00 | 10:00-12:00 | 提醒 + 待确认 |

**启用自动执行:**
```bash
./skills/heartbeat/setup-heartbeat-cron.sh
```

**查看执行日志:**
```bash
tail -f /home/openclaw/.openclaw/workspace/logs/heartbeat-exec.log
```

---
