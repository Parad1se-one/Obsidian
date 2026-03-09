# HEARTBEAT.md - 心跳任务清单

> 🦐 小虾：心跳时不只是报平安，还要做有意义的事。
> 
> **自动执行机制:** ✅ 已配置 cron，每小时自动检查并执行到期任务
> **手动触发:** 用户 heartbeat poll 时显示待执行任务状态

---

## 🤖 RL 研究学习 (每日核心任务)

### 上午心跳 (09:00) - RL 基础/算法
- [ ] 运行 `./skills/rl-researcher/rl-study.sh basics 30`
- [ ] 或 `./skills/rl-researcher/rl-study.sh algorithms 30`
- [ ] 检查 knowledge/rl/study-log-$(date).md 是否生成
- [ ] 确认 Git 提交成功

### 下午心跳 (14:00) - 论文阅读
- [ ] 运行 `./skills/rl-researcher/rl-study.sh paper 30`
- [ ] 搜索并阅读 1 篇 RL 论文
- [ ] 更新 knowledge/rl/papers/ 目录
- [ ] 记录批判性思考

### 晚间心跳 (20:00) - 代码实现/实验
- [ ] 运行 `./skills/rl-researcher/rl-study.sh code 60`
- [ ] 实现/调试 RL 算法
- [ ] 运行实验并记录结果
- [ ] 更新 research/experiments/ 目录

---

## 📚 通用自学习 (轮换)

### 财经学习
- [ ] 运行 `./skills/self-learner/self-learner.sh finance 15`
- [ ] 更新 knowledge/finance/learning-log-<date>.md

### 技术学习
- [ ] 运行 `./skills/self-learner/self-learner.sh tech 15`
- [ ] 学习 AI/自动化工具新进展

### 项目学习
- [ ] 运行 `./skills/self-learner/self-learner.sh projects 10`
- [ ] 检查 obsidian-repo 结构优化点

---

## 📈 财经日报 (工作日 07:30)

- [ ] 运行 `./skills/financial-daily/financial-daily.sh`
- [ ] 运行 `./skills/quality-checker/quality-checker.sh <输出文件> financial`
- [ ] 质量评分 ≥80 分 → 推送给用户
- [ ] 质量评分 <80 分 → 重新生成

---

## 🧹 知识维护 (每周日)

- [ ] 整理本周 RL 学习日志
- [ ] 更新 knowledge/rl/RL-INDEX.md
- [ ] 整理财经学习日志
- [ ] 更新 knowledge/KNOWLEDGE-INDEX.md
- [ ] 清理临时文件
- [ ] Git 归档

---

## 💡 主动检查 (2-4 次/天)

- [ ] 有无紧急邮件/消息
- [ ] 日历 upcoming events（24-48h）
- [ ] 天气（如果用户可能外出）
- [ ] GitHub 项目动态

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
