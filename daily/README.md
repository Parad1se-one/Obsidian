# 每日工作日志和知识库

**创建时间**: 2026-03-05  
**整理者**: 小虾 🦐 (OpenClaw Assistant)

---

## 📁 文件夹结构

```
daily/
├── README.md                          # 本说明文件
├── work/                              # 日常工作对话和会议记录
├── financial-news/                    # 财经日报（自动推送）
├── knowledge/                         # 知识库摘要和学习笔记
└── rl/                                # 强化学习相关日志
```

---

## 📄 各子文件夹说明

### work/ - 日常工作对话
每日工作对话、会议记录、任务讨论。

| 文件 | 说明 |
|------|------|
| `YYYY-MM-DD.md` | 每日工作日志（按日期命名） |

**内容包含**:
- 对话记录摘要
- 任务分配和进展
- 决策记录
- 待办事项

**示例**: `2026-03-05.md` - 技能系统搭建、Obsidian 工作流配置

---

### financial-news/ - 财经日报 📈
自动生成的每日财经新闻摘要。

| 文件 | 说明 |
|------|------|
| `YYYY-MM-DD.md` | 财经日报（每个工作日早上 7:30 自动推送） |

**内容包含**:
- 🌍 市场概览（上证指数、纳斯达克等）
- 📰 今日头条（财经新闻摘要）
- 🏢 公司动态
- 📊 行业热点
- 💡 小虾点评
- 📅 明日关注

**自动化**: 
- 生成时间：每周一至周五 07:30 (Asia/Shanghai)
- 技能：`skills/financial-daily/`
- API: NewsAPI（免费额度 500 次/天）

**示例**: `2026-03-05.md` - MVP 测试版本

---

### knowledge/ - 知识库摘要
知识管理相关的摘要、模板、快速参考。

| 文件 | 说明 |
|------|------|
| `knowledge-daily-YYYYMMDD.md` | 每日知识摘要 |

**内容包含**:
- 学习笔记
- 技术文档摘要
- 重要概念整理
- 模板和最佳实践

---

### rl/ - 强化学习日志
强化学习相关的调研日志和笔记。

**内容包含**:
- 论文阅读笔记
- 实验记录
- 代码实现心得
- 技术讨论

---

## 📊 统计信息

| 子文件夹 | 文件数量 | 更新频率 | 自动化 |
|----------|----------|----------|--------|
| work/ | 1+ | 每日 | 半自动 |
| financial-news/ | 1+ | 工作日每日 | ✅ 全自动 |
| knowledge/ | 1+ | 不定期 | 手动 |
| rl/ | 若干 | 不定期 | 手动 |

---

## 🔧 使用说明

### 查看今日工作日志
```bash
cat daily/work/$(date +%Y-%m-%d).md
```

### 查看今日财经日报
```bash
cat daily/financial-news/$(date +%Y-%m-%d).md
```

### 手动生成财经日报（测试）
```bash
cd /home/openclaw/.openclaw/workspace/skills/financial-daily
./financial-daily.sh
```

---

## 🤖 自动化配置

### 财经日报定时任务
```bash
# 设置定时任务（只需执行一次）
cd /home/openclaw/.openclaw/workspace/skills/financial-daily
./setup-cron.sh

# 查看当前任务
crontab -l | grep financial-daily
```

### 工作日志自动归档
使用 OpenClaw 会话结束时自动保存到 `daily/work/` 文件夹。

---

## 📝 命名规范

- **日期格式**: `YYYY-MM-DD.md` (如 `2026-03-05.md`)
- **编码**: UTF-8
- **格式**: Markdown (Obsidian 兼容)
- **时区**: Asia/Shanghai (GMT+8)

---

## 🦐 小虾备注

- `daily/` 是你的日常工作记忆库，所有重要对话和决策都会在这里归档
- 财经日报是 MVP 版本，后续会接入真实 API 数据
- 需要调整格式或添加新类别，随时跟我说

**最后更新**: 2026-03-05
