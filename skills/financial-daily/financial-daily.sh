#!/bin/bash
# financial-daily.sh - 财经日报 MVP 生成脚本
# 用法：./financial-daily.sh [日期 YYYY-MM-DD]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATE="${1:-$(date -d 'yesterday' +%Y-%m-%d)}"
OUTPUT_DIR="/home/openclaw/.openclaw/workspace/obsidian-repo/daily/financial-news"
TEMPLATE_FILE="$SCRIPT_DIR/templates/daily-report.md"
CONFIG_FILE="$SCRIPT_DIR/config/sources.json"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
OUTPUT_FILE="$OUTPUT_DIR/${DATE}.md"

echo "🦐 小虾财经日报 | 生成日期：$DATE"
echo "📍 输出位置：$OUTPUT_FILE"
echo ""

# 检查 NewsAPI Key
if [ -z "$NEWS_API_KEY" ]; then
    echo "⚠️  警告：NEWS_API_KEY 未设置，使用模拟数据"
    USE_MOCK=true
else
    USE_MOCK=false
    echo "✅ NewsAPI 已配置"
fi

# 读取配置
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ 配置文件已加载"
else
    echo "⚠️  配置文件不存在，使用默认配置"
fi

# 生成日报
echo "📝 正在生成财经日报..."

# 调用生成函数
generate_report() {
    local date=$1
    local use_mock=$2
    
    if [ "$use_mock" = true ]; then
        # 模拟数据（用于测试）
        cat << 'MOCK_DATA'
# 📈 财经日报 | {{DATE}}

## 🌍 市场概览
| 指数 | 收盘价 | 涨跌 | 幅度 |
|------|--------|------|------|
| 上证指数 | 3,245.67 | +12.34 | +0.38% |
| 深证成指 | 10,234.56 | -23.45 | -0.23% |
| 恒生指数 | 17,890.12 | +56.78 | +0.32% |
| 纳斯达克 | 15,678.90 | +89.01 | +0.57% |

## 📰 今日头条

### 1. [利好] 央行宣布降准 0.25 个百分点
**来源:** 财新网 | **情感:** 正面 | **影响:** 银行、地产

> 中国人民银行决定于 2026 年 3 月 15 日下调金融机构存款准备金率 0.25 个百分点，释放长期资金约 1 万亿元...

### 2. [中性] 美联储维持利率不变
**来源:** 华尔街日报 | **情感:** 中性 | **影响:** 美股、美元

> 联邦公开市场委员会决定将联邦基金利率目标区间维持在 5.25%-5.50%，符合市场预期...

### 3. [利空] 某科技公司财报不及预期
**来源:** 彭博社 | **情感:** 负面 | **影响:** 科技股

> 该公司 Q4 营收同比增长 5%，低于市场预期的 12%，盘后股价下跌 3%...

## 🏢 公司动态
| 公司 | 事件 | 影响 |
|------|------|------|
| 宁德时代 | 发布新电池技术 | 🟢 利好 |
| 贵州茅台 | 股价创新高 | 🟢 利好 |
| 阿里巴巴 | 财报发布 | 🟡 中性 |

## 📊 行业热点
- **新能源:** 锂电池板块上涨 2.3%
- **AI 概念:** 多家公司发布大模型
- **房地产:** 政策利好持续发酵

## 💡 小虾点评
> 今天市场整体偏暖，央行降准是个大利好。科技股分化，注意财报季风险。

## 📅 明日关注
- [ ] 中国 CPI/PPI 数据发布
- [ ] 美联储主席讲话
- [ ] 某公司财报

---
*生成时间：{{TIMESTAMP}} | 数据来源：NewsAPI (模拟数据)*
MOCK_DATA
    else
        # 真实 API 数据（待实现）
        echo "🔍 正在获取新闻数据..."
        # TODO: 调用 NewsAPI
        # curl -s "https://newsapi.org/v2/top-headlines?category=business&apiKey=$NEWS_API_KEY"
    fi
}

# 生成内容并替换日期
CONTENT=$(generate_report "$DATE" "$USE_MOCK")
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# 替换模板变量
CONTENT="${CONTENT//\{\{DATE\}\}/$DATE}"
CONTENT="${CONTENT//\{\{TIMESTAMP\}\}/$TIMESTAMP}"

# 写入文件
echo "$CONTENT" > "$OUTPUT_FILE"

echo ""
echo "✅ 财经日报生成完成！"
echo "📄 文件：$OUTPUT_FILE"
echo ""

# 显示文件统计
WORD_COUNT=$(wc -l < "$OUTPUT_FILE")
echo "📊 统计：$WORD_COUNT 行"
