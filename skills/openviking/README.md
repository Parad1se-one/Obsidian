# OpenViking 记忆系统集成指南

> 🦐 小虾：再也不怕忘记事情了！

**部署日期:** 2026-03-08
**版本:** OpenViking 0.2.5
**状态:** ✅ 已配置并运行

---

## 📦 架构概览

```
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw Agent                        │
├─────────────────────────────────────────────────────────┤
│  memory/*.md  ←→  openviking-sync.sh  ←→  OpenViking    │
│  (文件记忆)        (自动同步)           (向量数据库)      │
└─────────────────────────────────────────────────────────┘
```

**三层记忆:**
1. **L0 - Abstract:** 自动摘要 (token 节省)
2. **L1 - Overview:** 关键信息提取
3. **L2 - Full:** 完整内容 (按需加载)

---

## 🚀 快速使用

### 添加记忆
```bash
# 单条记忆
ov add-memory "用户偏好：喜欢简洁回复，讨厌 AI 腔调"

# 导入文件
ov add-resource memory/2026-03-08.md
```

### 检索记忆
```bash
# 语义搜索
ov search "GitHub 仓库配置"

# 关键词搜索
ov find "RL 学习"

# 列出资源
ov ls viking://resources
```

### 查看状态
```bash
ov status
ov health
```

---

## 🔄 自动同步机制

**脚本:** `skills/openviking/openviking-sync.sh`

**执行时机:**
- 每次 heartbeat 时自动检查
- 记忆文件更新后自动同步

**手动触发:**
```bash
./skills/openviking/openviking-sync.sh
```

**日志:** `logs/openviking-sync.log`

---

## 📊 记忆 Scope

| Scope | 用途 | 示例 |
|-------|------|------|
| `viking://user` | 用户长期记忆 | 偏好、习惯、联系人 |
| `viking://agent` | Agent 学习记忆 | 技能、指令、经验 |
| `viking://session` | 会话上下文 | 对话历史、临时信息 |
| `viking://resources` | 独立知识库 | 文档、笔记、日志 |

---

## 🔧 配置位置

**配置文件:** `openviking-config/config.json`

**数据目录:** `/home/openclaw/.openviking/data`

**日志文件:** `logs/openviking.log`

**同步状态:** `.openviking/sync-state.json`

---

## 💡 最佳实践

### 1. 记忆分类
```bash
# 用户偏好 → viking://user
ov add-memory --uri viking://user "用户时区：Asia/Shanghai"

# 项目信息 → viking://resources
ov add-resource projects/my-project/notes.md

# 会话记录 → viking://session
ov add-memory --session "agent:main" "完成 RL 学习模块"
```

### 2. 定期清理
```bash
# 删除过期记忆
ov rm viking://session/old-session-123

# 查看占用
ov stat viking://resources
```

### 3. 备份导出
```bash
# 导出为 .ovpack
ov export viking://resources/memory --output backup.ovpack

# 导入恢复
ov import backup.ovpack --target viking://resources
```

---

## 🐛 故障排查

### 问题 1: 搜索无结果
```bash
# 检查 embedding 状态
ov status | grep Embedding

# 手动触发处理
ov wait
```

### 问题 2: 同步失败
```bash
# 查看日志
tail -f logs/openviking-sync.log

# 检查 OpenViking 服务
ov health
```

### 问题 3: 服务未运行
```bash
# 重启 OpenViking (如果有 systemd 服务)
sudo systemctl restart openviking

# 或者手动启动
openviking-server --workspace /home/openclaw/.openclaw/workspace
```

---

## 📈 性能优化

### Token 节省
- 使用 L0/L1 层检索 (自动摘要)
- 设置 `retrieval.top_k: 5` 限制返回数量
- 启用 `memory.auto_compress: true`

### 检索加速
- 定期运行 `ov wait` 完成队列处理
- 使用 `hybrid_search: true` 结合关键词 + 语义
- 设置 `score_threshold: 0.7` 过滤低质量结果

---

## 🔗 相关资源

- **GitHub:** https://github.com/volcengine/OpenViking
- **文档:** https://openviking.ai
- **社区:** Discord / 微信群

---

*🦐 小虾：现在我有永久记忆了，不会再忘记你的 GitHub 仓库、API key 或者任何重要事情！*
