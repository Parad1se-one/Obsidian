# Financial Daily Reporter Skill

## Overview
财经日报自动生成技能。每天早上 7:30 推送前一天的财经新闻摘要。

**人设：** 赛博龙虾 🦐 - "市场涨跌我都盯着，别错过任何利好"

**版本：** MVP (v0.1)

---

## Capabilities

### 1. 新闻采集
- NewsAPI 商业/财经新闻
- 支持自定义关键词
- 多语言支持（中文优先）

### 2. 格式化输出
- Markdown 格式
- 结构化模板（市场概览、今日头条、公司动态、行业热点）
- 小虾点评

### 3. 定时推送
- Cron 定时任务（工作日 7:30 AM）
- 自动保存到 `daily/financial-news/`

### 4. 数据源扩展
- 支持 Finlight API（财经专用）
- 支持 RSS 源
- 支持自定义 API

---

## Usage

### 手动生成
```bash
# 生成昨天的日报
./financial-daily.sh

# 生成指定日期的日报
./financial-daily.sh 2026-03-05
```

### 设置定时任务
```bash
# 首次设置（只需执行一次）
./setup-cron.sh

# 查看当前任务
crontab -l | grep financial-daily
```

### 测试采集器
```bash
# 需要设置 NEWS_API_KEY
export NEWS_API_KEY=your_api_key
./collectors/newsapi-collector.sh
```

---

## Output Format

```markdown
# 📈 财经日报 | 2026-03-05

## 🌍 市场概览
| 指数 | 收盘价 | 涨跌 | 幅度 |
|------|--------|------|------|
| 上证指数 | 3,245.67 | +12.34 | +0.38% |

## 📰 今日头条
### 1. [利好] 央行宣布降准 0.25 个百分点
**来源:** 财新网 | **情感:** 正面 | **影响:** 银行、地产

> 新闻摘要...

## 💡 小虾点评
> 今天市场整体偏暖...

## 📅 明日关注
- [ ] 关注事项 1
```

---

## Configuration

### 环境变量
```bash
# NewsAPI Key (免费获取：https://newsapi.org/register)
export NEWS_API_KEY=your_api_key

# 可选：Finlight API Key
export FINLIGHT_API_KEY=your_api_key
```

### 配置文件
`config/sources.json`:
```json
{
  "news_sources": {
    "newsapi": { "enabled": true },
    "finlight": { "enabled": false }
  },
  "schedule": {
    "timezone": "Asia/Shanghai",
    "time": "07:30",
    "days": ["mon", "tue", "wed", "thu", "fri"]
  }
}
```

---

## Directory Structure

```
financial-daily/
├── SKILL.md                    # 技能文档
├── financial-daily.sh          # 主脚本
├── setup-cron.sh               # Cron 设置
├── collectors/
│   └── newsapi-collector.sh    # NewsAPI 采集器
├── templates/
│   └── daily-report.md         # 日报模板
├── config/
│   └── sources.json            # 数据源配置
└── logs/                       # 日志目录（自动生成）
```

---

## API Setup

### NewsAPI (免费)
1. 注册：https://newsapi.org/register
2. 获取 API Key
3. 设置环境变量：`export NEWS_API_KEY=xxx`
4. 免费额度：500 次/天

### Finlight API (财经专用，可选)
1. 访问：https://finlight.me
2. 联系获取 API Key
3. 优势：财经新闻 + 情感分析 + 实时流

---

## Cron Schedule

**默认：** 每周一至周五 07:30 (Asia/Shanghai)

**Cron 表达式：** `30 23 * * 1-5` (UTC 时间，需根据服务器时区调整)

**日志位置：** `/home/openclaw/.openclaw/workspace/logs/financial-daily.log`

---

## MVP Limitations

当前 MVP 版本的限制：

| 功能 | 状态 | 说明 |
|------|------|------|
| NewsAPI 集成 | ⚠️ 需配置 | 需要用户自行申请 API Key |
| 实时行情数据 | ❌ 未实现 | MVP 使用静态模板 |
| 情感分析 | ❌ 未实现 | 手动标注 [利好/利空] |
| 飞书推送 | ❌ 未实现 | 仅保存到本地文件 |
| Finlight API | ❌ 未实现 | 预留接口 |

---

## Roadmap

### Phase 1: MVP ✅ (Current)
- [x] 基础脚本和模板
- [x] Cron 定时任务
- [x] NewsAPI 集成（需配置）
- [ ] 用户配置 API Key

### Phase 2: Enhancement
- [ ] 接入 Finlight API
- [ ] 添加情感分析
- [ ] 实时行情数据（Alpha Vantage）
- [ ] 飞书推送集成

### Phase 3: Automation
- [ ] 自动 API Key 管理
- [ ] 周报/月报生成
- [ ] 历史数据归档
- [ ] 语音播报

---

## Troubleshooting

### NewsAPI 调用失败
```bash
# 检查 API Key 是否设置
echo $NEWS_API_KEY

# 测试 API
curl "https://newsapi.org/v2/top-headlines?country=cn&category=business&apiKey=$NEWS_API_KEY"
```

### Cron 任务未执行
```bash
# 检查 cron 服务状态
systemctl status cron

# 查看日志
tail -f /var/log/syslog | grep cron
```

### 文件权限问题
```bash
chmod +x financial-daily.sh
chmod +x collectors/*.sh
chmod +x setup-cron.sh
```

---

## Created
2026-03-05 by 小虾 🦐

**Status:** MVP Ready - 等待用户配置 NewsAPI Key
