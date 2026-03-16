# Financial Daily V2 - 财经日报自动生成技能

> 📈 基于多平台稳定数据源的财经日报自动生成
> 
> **版本**: v2.0
> **最后更新**: 2026-03-16

---

## 📋 功能说明

自动抓取多个财经平台的最新内容，生成结构化的财经日报，并推送到飞书。

### 支持的数据源

| 平台 | 类型 | 优先级 | 状态 |
|------|------|--------|------|
| **财联社** (cls.cn) | 24 小时电报/快讯 | P0 | ✅ 优秀 |
| **21 经济网** (21jingji.com) | 深度报道/热文 | P0 | ✅ 优秀 |
| **财经头条** (caijingtoutiao.com) | 焦点新闻/热门 | P1 | ✅ 良好 |
| **东方财富财富号** | 热门话题 | P1 | ✅ 良好 |
| **华尔街见闻** (wallstreetcn.com) | 全球财经/快讯 | P1 | ✅ 良好 |

### 可扩展性

新增数据源只需：
1. 在 `scripts/sources/` 目录添加抓取脚本
2. 在主脚本中注册数据源
3. 更新本文档

---

## 🚀 使用方法

### 手动触发
```bash
cd /home/openclaw/.openclaw/workspace/skills/financial-daily-v2
./financial-daily.sh [--force]
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
├── SKILL.md                    # 技能说明
├── financial-daily.sh          # 主脚本
├── scripts/
│   ├── sources/                # 数据源抓取脚本
│   │   ├── cls.sh              # 财联社
│   │   ├── 21jingji.sh         # 21 经济网
│   │   ├── caijing-toutiao.sh  # 财经头条
│   │   └── eastmoney.sh        # 东方财富
│   ├── generator.sh            # 日报生成器
│   └── quality-check.sh        # 质量检查
└── templates/
    └── daily-template.md       # 日报模板
```

---

## 📝 输出格式

生成文件位置：`obsidian-repo/daily/financial-news/YYYY-MM-DD.md`

### 日报结构
1. 📊 市场概览
2. ⚡ 重要快讯 (财联社)
3. 📰 深度报道 (21 经济网)
4. 📈 涨停复盘 (财经头条)
5. 🔥 热门话题 (东方财富)
6. 📅 财经日历

---

## 🔧 配置项

| 配置 | 默认值 | 说明 |
|------|--------|------|
| `OUTPUT_DIR` | `obsidian-repo/daily/financial-news/` | 输出目录 |
| `MIN_SCORE` | `80` | 质量检查最低分数 |
| `PUSH_GIT` | `true` | 是否自动 Git 推送 |
| `FEISHU_NOTIFY` | `true` | 是否发送飞书通知 |

---

## 📊 日志

- **执行日志**: `logs/financial-daily-v2.log`
- **错误日志**: `logs/financial-daily-v2-error.log`

---

*最后更新：2026-03-16 | 状态：✅ 已激活*
