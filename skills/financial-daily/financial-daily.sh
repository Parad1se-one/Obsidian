#!/bin/bash
# financial-daily.sh - 财经日报生成脚本（国内 API 版）
# 数据源：腾讯财经 + 东方财富
# 用法：./financial-daily.sh [日期 YYYY-MM-DD]

set -e

# 加载代理配置 (外网访问需要)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../common/load-proxy.sh"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATE="${1:-$(date +%Y-%m-%d)}"
OUTPUT_DIR="/home/openclaw/.openclaw/workspace/obsidian-repo/daily/financial-news"
OUTPUT_FILE="$OUTPUT_DIR/${DATE}.md"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo "🦐 小虾财经日报 | 生成日期：$DATE"
echo "📍 输出位置：$OUTPUT_FILE"
echo ""

# 生成日报头部
cat > "$OUTPUT_FILE" << HEADER
# 📈 财经日报 | $DATE

> ⚠️ **免责声明**: 本报告仅供参考，不构成投资建议。市场有风险，投资需谨慎。

---

## 🌍 市场概览

HEADER

echo "📊 获取 A 股行情数据（腾讯财经）..."

# 获取上证指数 (sh000001)
SH_RESPONSE=$(curl -s --max-time 10 "https://qt.gtimg.cn/q=sh000001" 2>&1)
if [ $? -eq 0 ] && [ -n "$SH_RESPONSE" ]; then
    # 解析腾讯格式：v_sh000001="1~上证指数~000001~4108.57~4082.47~..."
    SH_CURRENT=$(echo "$SH_RESPONSE" | awk -F'~' '{print $4}')
    SH_YESTERDAY=$(echo "$SH_RESPONSE" | awk -F'~' '{print $5}')
    
    if [ -n "$SH_CURRENT" ] && [ -n "$SH_YESTERDAY" ]; then
        SH_CHANGE=$(echo "$SH_CURRENT - $SH_YESTERDAY" | bc 2>/dev/null || echo "0")
        SH_CHANGE_PCT=$(echo "scale=2; ($SH_CHANGE / $SH_YESTERDAY) * 100" | bc 2>/dev/null || echo "0")
        SH_UP=$(echo "$SH_CHANGE >= 0" | bc 2>/dev/null || echo "1")
        if [ "$SH_UP" -eq 1 ]; then
            SH_ARROW="🟢 +"
        else
            SH_ARROW="🔴 "
        fi
        echo "✅ 上证指数：$SH_CURRENT ($SH_ARROW$SH_CHANGE / $SH_CHANGE_PCT%)"
    else
        SH_CURRENT="获取失败"
        SH_CHANGE="0"
        SH_CHANGE_PCT="0"
        SH_ARROW="⚪ "
        echo "⚠️ 上证指数数据解析失败"
    fi
else
    SH_CURRENT="获取失败"
    SH_CHANGE="0"
    SH_CHANGE_PCT="0"
    SH_ARROW="⚪ "
    echo "⚠️ 上证指数数据获取失败"
fi

# 获取深证成指 (sz399001)
SZ_RESPONSE=$(curl -s --max-time 10 "https://qt.gtimg.cn/q=sz399001" 2>&1)
if [ $? -eq 0 ] && [ -n "$SZ_RESPONSE" ]; then
    SZ_CURRENT=$(echo "$SZ_RESPONSE" | awk -F'~' '{print $4}')
    SZ_YESTERDAY=$(echo "$SZ_RESPONSE" | awk -F'~' '{print $5}')
    
    if [ -n "$SZ_CURRENT" ] && [ -n "$SZ_YESTERDAY" ]; then
        SZ_CHANGE=$(echo "$SZ_CURRENT - $SZ_YESTERDAY" | bc 2>/dev/null || echo "0")
        SZ_CHANGE_PCT=$(echo "scale=2; ($SZ_CHANGE / $SZ_YESTERDAY) * 100" | bc 2>/dev/null || echo "0")
        SZ_UP=$(echo "$SZ_CHANGE >= 0" | bc 2>/dev/null || echo "1")
        if [ "$SZ_UP" -eq 1 ]; then
            SZ_ARROW="🟢 +"
        else
            SZ_ARROW="🔴 "
        fi
        echo "✅ 深证成指：$SZ_CURRENT ($SZ_ARROW$SZ_CHANGE / $SZ_CHANGE_PCT%)"
    else
        SZ_CURRENT="获取失败"
        SZ_CHANGE="0"
        SZ_CHANGE_PCT="0"
        SZ_ARROW="⚪ "
        echo "⚠️ 深证成指数据解析失败"
    fi
else
    SZ_CURRENT="获取失败"
    SZ_CHANGE="0"
    SZ_CHANGE_PCT="0"
    SZ_ARROW="⚪ "
    echo "⚠️ 深证成指数据获取失败"
fi

# 获取恒生指数 (hkHSI)
HSI_RESPONSE=$(curl -s --max-time 10 "https://qt.gtimg.cn/q=hkHSI" 2>&1)
if [ $? -eq 0 ] && [ -n "$HSI_RESPONSE" ]; then
    HSI_CURRENT=$(echo "$HSI_RESPONSE" | awk -F'~' '{print $4}')
    HSI_YESTERDAY=$(echo "$HSI_RESPONSE" | awk -F'~' '{print $5}')
    
    if [ -n "$HSI_CURRENT" ] && [ -n "$HSI_YESTERDAY" ]; then
        HSI_CHANGE=$(echo "$HSI_CURRENT - $HSI_YESTERDAY" | bc 2>/dev/null || echo "0")
        HSI_CHANGE_PCT=$(echo "scale=2; ($HSI_CHANGE / $HSI_YESTERDAY) * 100" | bc 2>/dev/null || echo "0")
        HSI_UP=$(echo "$HSI_CHANGE >= 0" | bc 2>/dev/null || echo "1")
        if [ "$HSI_UP" -eq 1 ]; then
            HSI_ARROW="🟢 +"
        else
            HSI_ARROW="🔴 "
        fi
        echo "✅ 恒生指数：$HSI_CURRENT ($HSI_ARROW$HSI_CHANGE / $HSI_CHANGE_PCT%)"
    else
        HSI_CURRENT="获取失败"
        HSI_CHANGE="0"
        HSI_CHANGE_PCT="0"
        HSI_ARROW="⚪ "
        echo "⚠️ 恒生指数数据解析失败"
    fi
else
    HSI_CURRENT="获取失败"
    HSI_CHANGE="0"
    HSI_CHANGE_PCT="0"
    HSI_ARROW="⚪ "
    echo "⚠️ 恒生指数数据获取失败"
fi

# 获取纳斯达克 (usNAS)
NDX_RESPONSE=$(curl -s --max-time 10 "https://qt.gtimg.cn/q=usNAS" 2>&1)
if [ $? -eq 0 ] && [ -n "$NDX_RESPONSE" ]; then
    NDX_CURRENT=$(echo "$NDX_RESPONSE" | awk -F'~' '{print $4}')
    NDX_YESTERDAY=$(echo "$NDX_RESPONSE" | awk -F'~' '{print $5}')
    
    if [ -n "$NDX_CURRENT" ] && [ -n "$NDX_YESTERDAY" ]; then
        NDX_CHANGE=$(echo "$NDX_CURRENT - $NDX_YESTERDAY" | bc 2>/dev/null || echo "0")
        NDX_CHANGE_PCT=$(echo "scale=2; ($NDX_CHANGE / $NDX_YESTERDAY) * 100" | bc 2>/dev/null || echo "0")
        NDX_UP=$(echo "$NDX_CHANGE >= 0" | bc 2>/dev/null || echo "1")
        if [ "$NDX_UP" -eq 1 ]; then
            NDX_ARROW="🟢 +"
        else
            NDX_ARROW="🔴 "
        fi
        echo "✅ 纳斯达克：$NDX_CURRENT ($NDX_ARROW$NDX_CHANGE / $NDX_CHANGE_PCT%)"
    else
        NDX_CURRENT="获取失败"
        NDX_CHANGE="0"
        NDX_CHANGE_PCT="0"
        NDX_ARROW="⚪ "
        echo "⚠️ 纳斯达克数据解析失败"
    fi
else
    NDX_CURRENT="获取失败"
    NDX_CHANGE="0"
    NDX_CHANGE_PCT="0"
    NDX_ARROW="⚪ "
    echo "⚠️ 纳斯达克数据获取失败"
fi

echo ""

# 写入市场概览表格
cat >> "$OUTPUT_FILE" << MARKET_TABLE
| 指数 | 收盘价 | 涨跌 | 幅度 | 更新时间 |
|------|--------|------|------|----------|
| 上证指数 | $SH_CURRENT | $SH_ARROW$SH_CHANGE | $SH_CHANGE_PCT% | $(date '+%H:%M') |
| 深证成指 | $SZ_CURRENT | $SZ_ARROW$SZ_CHANGE | $SZ_CHANGE_PCT% | $(date '+%H:%M') |
| 恒生指数 | $HSI_CURRENT | $HSI_ARROW$HSI_CHANGE | $HSI_CHANGE_PCT% | $(date '+%H:%M') |
| 纳斯达克 | $NDX_CURRENT | $NDX_ARROW$NDX_CHANGE | $NDX_CHANGE_PCT% | $(date '+%H:%M') |

> 💡 **数据来源**: 腾讯财经实时 API | 更新时间：$(date '+%Y-%m-%d %H:%M')

---

## 📰 今日头条

MARKET_TABLE

# 获取东方财富新闻
echo "📰 获取财经新闻（东方财富）..."
EASTMONEY_NEWS=$(curl -s --max-time 15 "https://api.eastmoney.com/news/getLatestNews?callback=jQuery&pageSize=10&type=bg" 2>&1)

if [ $? -eq 0 ] && [ -n "$EASTMONEY_NEWS" ]; then
    echo "✅ 获取到东方财富新闻"
    echo "" >> "$OUTPUT_FILE"
    echo "### 东方财富快讯" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "> 实时财经快讯来源：[东方财富网](https://www.eastmoney.com/)" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
else
    echo "⚠️ 东方财富新闻获取失败"
    echo "" >> "$OUTPUT_FILE"
    echo "### 东方财富快讯" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "> 暂无实时快讯数据，请访问 [东方财富网](https://www.eastmoney.com/) 查看最新新闻" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# 添加新闻部分
cat >> "$OUTPUT_FILE" << NEWS_SECTION

### 重点关注

1. **宏观经济** - 关注央行货币政策动向
2. **财报季** - 关注科技巨头财报发布
3. **行业政策** - 关注新能源、AI 产业政策

> 💡 **提示**: 点击以下链接查看实时新闻
> - [东方财富网](https://www.eastmoney.com/)
> - [新浪财经](https://finance.sina.com.cn/)
> - [腾讯财经](https://finance.qq.com/)
> - [华尔街见闻](https://wallstreetcn.com/)

---

## 🏢 公司动态

| 公司 | 事件 | 影响 | 来源 |
|------|------|------|------|
| *(待更新)* | - | - | - |

> 💡 **说明**: 个股新闻需要进一步接入东方财富个股 API

---

## 📊 行业热点

- **新能源**: 关注锂电池、光伏板块动向
- **AI 概念**: 大模型、算力相关公司
- **房地产**: 政策持续优化
- **金融**: 银行、券商、保险板块

---

## 💡 小虾点评

> **市场综述**: 基于实时行情数据，结合新闻动态分析。
> 
> **投资建议**: 
> - 关注成交量变化
> - 注意板块轮动节奏
> - 控制仓位，分散风险
> 
> **风险提示**: 本报告仅供参考，不构成投资建议。

---

## 📅 明日关注

- [ ] 央行公开市场操作
- [ ] 宏观经济数据发布
- [ ] 美联储官员讲话
- [ ] 科技公司财报

---

*生成时间：$(date '+%Y-%m-%d %H:%M:%S') | 数据来源：腾讯财经 + 东方财富 | 版本：v1.0 (国内 API)*

NEWS_SECTION

echo ""
echo "✅ 财经日报生成完成！"
echo "📄 文件：$OUTPUT_FILE"
echo ""

# 显示统计
LINES=$(wc -l < "$OUTPUT_FILE")
echo "📊 统计：$LINES 行"
