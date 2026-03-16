# Financial Daily V2 - 财经日报自动生成技能

> 📈 基于多平台稳定数据源的财经日报自动生成
> 
> **版本**: v2.1
> **最后更新**: 2026-03-16
> **状态**: ✅ 生产环境运行中

---

## 📋 功能说明

自动抓取多个财经平台的最新内容，生成结构化的财经日报，并自动推送到飞书 + Git 仓库。

### 核心特性

- ✅ **多数据源聚合** - 5 个稳定财经平台
- ✅ **智能财经日历** - 基于今日新闻自动生成明日关注点
- ✅ **质量检查** - ≥80 分自动通过，否则告警
- ✅ **Git 自动推送** - 生成后自动 commit + push
- ✅ **可扩展架构** - 新增数据源只需添加脚本

---

## 📊 支持的数据源

| 平台 | 类型 | 优先级 | 状态 | 抓取内容 |
|------|------|--------|------|----------|
| **财联社** (cls.cn) | 24 小时电报/快讯 | P0 | ✅ 优秀 | 15-20 条带【】标记快讯 |
| **21 经济网** (21jingji.com) | 深度报道/热文 | P0 | ✅ 优秀 | 15-20 条深度新闻 |
| **财经头条** (caijingtoutiao.com) | 焦点新闻/热门 | P1 | ✅ 良好 | 15-20 条焦点新闻 |
| **东方财富财富号** | 热门话题 | P1 | ✅ 良好 | 10-15 条热门话题 |
| **华尔街见闻** (wallstreetcn.com) | 全球财经/快讯 | P1 | ✅ 良好 | 10-15 条全球财经 |

---

## 🚀 使用方法

### 手动触发
```bash
cd /home/openclaw/.openclaw/workspace/skills/financial-daily-v2
./financial-daily.sh --force
```

### Cron 定时任务
```cron
# 工作日 07:30 生成财经日报
30 7 * * 1-5 /home/openclaw/.openclaw/workspace/skills/financial-daily-v2/financial-daily.sh >> /home/openclaw/.openclaw/workspace/logs/financial-daily-v2.log 2>&1
```

---

## 📁 文件结构

```
skills/financial-daily-v2/
├── SKILL.md                    # 技能说明文档
├── financial-daily.sh          # 主脚本 (入口)
├── scripts/
│   ├── sources/                # 数据源抓取脚本
│   │   ├── cls.sh              # 财联社 ✅
│   │   ├── 21jingji.sh         # 21 经济网 ✅
│   │   ├── caijing-toutiao.sh  # 财经头条 ✅
│   │   ├── eastmoney.sh        # 东方财富 ✅
│   │   ├── wallstreetcn.sh     # 华尔街见闻 ✅
│   │   └── finance-calendar.sh # 财经日历 (智能生成) ✅
│   ├── generator.sh            # 日报生成器 (整合所有内容)
│   └── quality-check.sh        # 质量检查 (≥80 分通过)
└── temp/                       # 临时文件目录 (每次执行清理)
```

---

## 📝 输出格式

**生成文件位置**: `obsidian-repo/daily/financial-news/YYYY-MM-DD.md`

### 日报结构

```markdown
# 📈 财经日报 2026-03-16

## ⚡ 重要快讯          (财联社)
## 📰 深度报道          (21 经济网)
## 📊 焦点新闻          (财经头条)
## 🔥 热门话题          (东方财富)
## 🌐 华尔街见闻        (华尔街见闻)
## 📅 财经日历          (智能生成)
    - 明日重点关注 (基于今日新闻关键词)
    - 经济数据预告
```

---

## 🔧 配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `OUTPUT_DIR` | `obsidian-repo/daily/financial-news/` | 输出目录 |
| `MIN_SCORE` | `80` | 质量检查最低分数 |
| `PUSH_GIT` | `true` | 是否自动 Git 推送 |
| `FEISHU_NOTIFY` | `true` | 是否发送飞书通知 |

---

## 📊 质量检查标准

| 检查项 | 分值 | 说明 |
|--------|------|------|
| 文件非空 | 20 分 | 文件必须有内容 |
| 包含标题 | 20 分 | 必须有 `# 📈 财经日报` 标题 |
| 包含日期 | 20 分 | 必须包含当日日期 |
| 数据源内容 | 20 分 | 至少有一个数据源有内容 |
| 内容长度 | 20 分 | 总行数 ≥20 行 |

**≥80 分**: 通过，继续推送  
**<80 分**: 失败，终止流程并告警

---

## 🔄 工作流程

```
1. 初始化 (创建目录/日志)
   ↓
2. 抓取数据源 (并行执行 5 个脚本)
   ↓
3. 生成日报 (整合所有内容 + 财经日历)
   ↓
4. 质量检查 (≥80 分通过)
   ↓
5. Git 提交推送 (commit + push)
   ↓
6. 飞书通知 (发送日报摘要)
   ↓
7. 清理临时文件
```

---

## 📊 日志

| 日志文件 | 说明 |
|----------|------|
| `logs/financial-daily-v2.log` | 主执行日志 |
| `logs/financial-daily-v2-error.log` | 错误日志 |

**查看日志**:
```bash
tail -f logs/financial-daily-v2.log
tail -f logs/financial-daily-v2-error.log
```

---

## ➕ 扩展指南

### 新增数据源

1. 在 `scripts/sources/` 目录创建抓取脚本:
```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/../../temp"
OUTPUT_FILE="${TEMP_DIR}/your_source_content.md"

# 抓取逻辑...
# 输出格式:
cat > "${OUTPUT_FILE}" << 'EOF'
## 📌 你的数据源名称

- 新闻 1
- 新闻 2
EOF
```

2. 在主脚本 `financial-daily.sh` 中注册:
```bash
declare -a DATA_SOURCES=(
    "cls"
    "21jingji"
    "your_source"  # 新增
)
```

3. 在 `generator.sh` 中添加整合逻辑

4. 更新本文档

---

## 📝 更新日志

### v2.1 - 2026-03-16 ✨
- ✅ 新增财经日历自动生成 (基于今日新闻关键词)
- ✅ 优化 21 经济网抓取逻辑 (title 属性提取)
- ✅ 优化财经头条抓取逻辑 (class=tit 提取)
- ✅ 优化东方财富抓取逻辑 (去重 + 过滤)
- ✅ 新增华尔街见闻数据源
- ✅ 质量检查优化 (≥80 分通过)

### v2.0 - 2026-03-16 🚀
- ✅ 重构财经日报技能 (多数据源架构)
- ✅ 支持 5 个稳定财经平台
- ✅ 自动 Git 推送
- ✅ 质量检查系统

---

## 🛠️ 故障排查

### 抓取内容为空
1. 检查网站是否可访问：`curl -I <URL>`
2. 检查 User-Agent 是否被屏蔽
3. 检查正则表达式是否匹配

### Git 推送失败
1. 检查 Git 配置：`git config --list`
2. 检查远程仓库权限
3. 查看日志：`tail logs/financial-daily-v2.log`

### 质量检查失败
1. 查看质量检查日志
2. 检查各数据源抓取是否正常
3. 调整 `MIN_SCORE` 阈值 (不推荐)

---

*最后更新：2026-03-16 | 状态：✅ 生产环境运行中*
