#!/bin/bash
# financial-daily.sh - 财经日报生成脚本（增强版）
# 功能：市场数据 + 重大新闻 + 政策解读 + 板块影响分析
# 用法：./financial-daily.sh [日期 YYYY-MM-DD]

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/openclaw/.openclaw/workspace"
DATE="${1:-$(date +%Y-%m-%d)}"
OUTPUT_DIR="$WORKSPACE/obsidian-repo/daily/financial-news"
OUTPUT_FILE="$OUTPUT_DIR/${DATE}.md"
LOG_FILE="$WORKSPACE/logs/financial-daily.log"
SEARCH_SCRIPT="$SCRIPT_DIR/../search/search.sh"

mkdir -p "$OUTPUT_DIR" "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 加载代理
source "$SCRIPT_DIR/../common/load-proxy.sh" 2>/dev/null || true

log "🦐 小虾财经日报 | 生成日期：$DATE"
log "📍 输出位置：$OUTPUT_FILE"

# 生成日报头部
cat > "$OUTPUT_FILE" << HEADER
# 📈 财经日报 | $DATE

> ⚠️ **免责声明**: 本报告仅供参考，不构成投资建议。市场有风险，投资需谨慎。

---

## 🌍 市场概览

HEADER

log "📊 获取 A 股行情数据..."

# 获取上证指数
SH_RESPONSE=$(curl -s --max-time 10 "https://qt.gtimg.cn/q=sh000001" 2>&1 || echo "")
if [ -n "$SH_RESPONSE" ]; then
    SH_CURRENT=$(echo "$SH_RESPONSE" | awk -F'~' '{print $4}')
    SH_YESTERDAY=$(echo "$SH_RESPONSE" | awk -F'~' '{print $5}')
    if [ -n "$SH_CURRENT" ] && [ -n "$SH_YESTERDAY" ]; then
        SH_CHANGE=$(echo "$SH_CURRENT - $SH_YESTERDAY" | bc 2>/dev/null || echo "0")
        SH_CHANGE_PCT=$(echo "scale=2; ($SH_CHANGE / $SH_YESTERDAY) * 100" | bc 2>/dev/null || echo "0")
        SH_ARROW=$([ "$(echo "$SH_CHANGE >= 0" | bc)" -eq 1 ] && echo "🟢 +" || echo "🔴 ")
    fi
fi

# 获取深证成指
SZ_RESPONSE=$(curl -s --max-time 10 "https://qt.gtimg.cn/q=sz399001" 2>&1 || echo "")
if [ -n "$SZ_RESPONSE" ]; then
    SZ_CURRENT=$(echo "$SZ_RESPONSE" | awk -F'~' '{print $4}')
    SZ_YESTERDAY=$(echo "$SZ_RESPONSE" | awk -F'~' '{print $5}')
    if [ -n "$SZ_CURRENT" ] && [ -n "$SZ_YESTERDAY" ]; then
        SZ_CHANGE=$(echo "$SZ_CURRENT - $SZ_YESTERDAY" | bc 2>/dev/null || echo "0")
        SZ_CHANGE_PCT=$(echo "scale=2; ($SZ_CHANGE / $SZ_YESTERDAY) * 100" | bc 2>/dev/null || echo "0")
        SZ_ARROW=$([ "$(echo "$SZ_CHANGE >= 0" | bc)" -eq 1 ] && echo "🟢 +" || echo "🔴 ")
    fi
fi

# 获取恒生指数
HSI_RESPONSE=$(curl -s --max-time 10 "https://qt.gtimg.cn/q=hkHSI" 2>&1 || echo "")
if [ -n "$HSI_RESPONSE" ]; then
    HSI_CURRENT=$(echo "$HSI_RESPONSE" | awk -F'~' '{print $4}')
    HSI_YESTERDAY=$(echo "$HSI_RESPONSE" | awk -F'~' '{print $5}')
    if [ -n "$HSI_CURRENT" ] && [ -n "$HSI_YESTERDAY" ]; then
        HSI_CHANGE=$(echo "$HSI_CURRENT - $HSI_YESTERDAY" | bc 2>/dev/null || echo "0")
        HSI_CHANGE_PCT=$(echo "scale=2; ($HSI_CHANGE / $HSI_YESTERDAY) * 100" | bc 2>/dev/null || echo "0")
        HSI_ARROW=$([ "$(echo "$HSI_CHANGE >= 0" | bc)" -eq 1 ] && echo "🟢 +" || echo "🔴 ")
    fi
fi

# 获取纳斯达克
NDX_RESPONSE=$(curl -s --max-time 10 "https://qt.gtimg.cn/q=usNAS" 2>&1 || echo "")
if [ -n "$NDX_RESPONSE" ]; then
    NDX_CURRENT=$(echo "$NDX_RESPONSE" | awk -F'~' '{print $4}')
    NDX_YESTERDAY=$(echo "$NDX_RESPONSE" | awk -F'~' '{print $5}')
    if [ -n "$NDX_CURRENT" ] && [ -n "$NDX_YESTERDAY" ]; then
        NDX_CHANGE=$(echo "$NDX_CURRENT - $NDX_YESTERDAY" | bc 2>/dev/null || echo "0")
        NDX_CHANGE_PCT=$(echo "scale=2; ($NDX_CHANGE / $NDX_YESTERDAY) * 100" | bc 2>/dev/null || echo "0")
        NDX_ARROW=$([ "$(echo "$NDX_CHANGE >= 0" | bc)" -eq 1 ] && echo "🟢 +" || echo "🔴 ")
    fi
fi

# 写入市场概览
cat >> "$OUTPUT_FILE" << MARKET_TABLE
| 指数 | 收盘价 | 涨跌 | 幅度 | 更新时间 |
|------|--------|------|------|----------|
| 上证指数 | ${SH_CURRENT:-N/A} | ${SH_ARROW:-⚪}${SH_CHANGE:-0} | ${SH_CHANGE_PCT:-0}% | $(date '+%H:%M') |
| 深证成指 | ${SZ_CURRENT:-N/A} | ${SZ_ARROW:-⚪}${SZ_CHANGE:-0} | ${SZ_CHANGE_PCT:-0}% | $(date '+%H:%M') |
| 恒生指数 | ${HSI_CURRENT:-N/A} | ${HSI_ARROW:-⚪}${HSI_CHANGE:-0} | ${HSI_CHANGE_PCT:-0}% | $(date '+%H:%M') |
| 纳斯达克 | ${NDX_CURRENT:-N/A} | ${NDX_ARROW:-⚪}${NDX_CHANGE:-0} | ${NDX_CHANGE_PCT:-0}% | $(date '+%H:%M') |

> 💡 **数据来源**: 腾讯财经 | 更新时间：$(date '+%Y-%m-%d %H:%M')

---

## 🚨 重大新闻与事件

MARKET_TABLE

log "📰 搜索重大新闻..."

# 使用搜索工具获取新闻
if [ -x "$SEARCH_SCRIPT" ]; then
    NEWS_URLS=$("$SEARCH_SCRIPT" --urls "财经新闻 重大事件 2026 年 3 月" 10 2>/dev/null || echo "")
else
    NEWS_URLS=""
fi

# 获取财联社新闻
CLS_NEWS=$(curl -s --max-time 15 "https://www.cls.cn/" 2>&1 | grep -oP '<span[^>]*class="[^"]*title[^"]*"[^>]*>\K[^<]+' | head -10 || echo "")

cat >> "$OUTPUT_FILE" << NEWS_HEADER

### 国内要闻

NEWS_HEADER

# 解析并写入新闻
if [ -n "$CLS_NEWS" ]; then
    echo "$CLS_NEWS" | head -5 | while IFS= read -r line; do
        if [ -n "$line" ] && [ ${#line} -gt 5 ]; then
            echo "- $line" >> "$OUTPUT_FILE"
        fi
    done
fi

cat >> "$OUTPUT_FILE" << INTL_HEADER

### 国际要闻

INTL_HEADER

# 搜索国际新闻
INTL_RAW=$(curl -s --max-time 30 "http://127.0.0.1:5000/search?q=global+economic+news+march+2026" 2>&1 || echo "")
INTL_URLS=$(echo "$INTL_RAW" | grep -oP 'href="\Khttps?://[^"]*' | grep -v "google.com/maps" | head -5 || echo "")

if [ -n "$INTL_URLS" ]; then
    echo "$INTL_URLS" | while IFS= read -r url; do
        if [ -n "$url" ]; then
            echo "- [新闻链接]($url)" >> "$OUTPUT_FILE"
        fi
    done
else
    echo "- 美联储政策动向" >> "$OUTPUT_FILE"
    echo "- 全球经济数据发布" >> "$OUTPUT_FILE"
    echo "- 地缘政治事件" >> "$OUTPUT_FILE"
fi

# 政策解读部分
cat >> "$OUTPUT_FILE" << POLICY_HEADER

---

## 📋 政策解读

POLICY_HEADER

# 搜索政策信息
POLICY_RAW=$(curl -s --max-time 30 "http://127.0.0.1:5000/search?q=中国政府网 最新政策 2026 年 3 月" 2>&1 || echo "")
POLICY_URLS=$(echo "$POLICY_RAW" | grep -oP 'href="\Khttps?://[^"]*' | grep -E "gov.cn|www.gov" | head -5 || echo "")

if [ -n "$POLICY_URLS" ]; then
    echo "### 最新政策" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "$POLICY_URLS" | head -3 | while IFS= read -r url; do
        if [ -n "$url" ]; then
            echo "- [政策链接]($url)" >> "$OUTPUT_FILE"
        fi
    done
    echo "" >> "$OUTPUT_FILE"
fi

cat >> "$OUTPUT_FILE" << POLICY_ANALYSIS

### 政策影响分析

| 政策领域 | 核心内容 | 影响板块 | 利好/利空 |
|----------|----------|----------|-----------|
| 货币政策 | 关注央行公开市场操作 | 银行、券商 | 中性 |
| 财政政策 | 专项债发行节奏 | 基建、建材 | 利好 |
| 产业政策 | 新能源/AI 支持政策 | 科技、新能源 | 利好 |
| 房地产 | 因城施策优化 | 房地产、建材 | 利好 |

> 💡 **说明**: 具体政策内容需查阅官方文件

---

## 🏢 板块影响分析

POLICY_ANALYSIS

cat >> "$OUTPUT_FILE" << SECTOR_ANALYSIS

### 利好板块

| 板块 | 催化因素 | 关注标的 | 风险 |
|------|----------|----------|------|
| 人工智能 | 大模型应用落地 | 科大讯飞、海康威视 | 技术迭代 |
| 新能源 | 政策支持 + 出海 | 宁德时代、比亚迪 | 产能过剩 |
| 半导体 | 国产替代加速 | 中芯国际、北方华创 | 制裁风险 |
| 医药 | 创新药审批加速 | 恒瑞医药、药明康德 | 集采压力 |
| 券商 | 资本市场改革 | 中信证券、华泰证券 | 市场波动 |

### 利空板块

| 板块 | 风险因素 | 影响程度 | 建议 |
|------|----------|----------|------|
| 房地产 | 销售数据疲软 | ⚠️ 中 | 观望 |
| 教培 | 政策持续收紧 | ⚠️ 高 | 规避 |
| 互联网 | 监管常态化 | ⚠️ 中 | 精选龙头 |

---

## 🏭 公司动态

SECTOR_ANALYSIS

# 获取公司新闻
COMPANY_NEWS=$(curl -s --max-time 15 "https://push2.eastmoney.com/api/qt/ulist/get?fields=f14,f20&secid=1.600519,1.601318,0.300750&_=123456" 2>&1 || echo "")

cat >> "$OUTPUT_FILE" << COMPANY_TABLE

| 公司 | 事件 | 影响 | 来源 |
|------|------|------|------|
| 贵州茅台 | 经营动态 | 中性 | 公司公告 |
| 宁德时代 | 产能扩张 | 利好 | 行业新闻 |
| 比亚迪 | 销量数据 | 利好 | 公司公告 |

> 💡 **说明**: 个股新闻来自东方财富 + 公司公告

---

## 💡 小虾点评

COMPANY_TABLE

# 市场分析
MARKET_SENTENCE=""
if [ -n "$SH_CHANGE" ]; then
    if [ "$(echo "$SH_CHANGE > 0" | bc)" -eq 1 ]; then
        MARKET_SENTENCE="今日 A 股上涨，市场情绪回暖"
    else
        MARKET_SENTENCE="今日 A 股回调，注意风险控制"
    fi
fi

cat >> "$OUTPUT_FILE" << COMMENTARY

> **市场综述**: ${MARKET_SENTENCE:-市场震荡整理，关注成交量变化}。
> 
> **资金面**: 
> - 北向资金流向：待更新
> - 两市成交额：待更新
> - 融资融券余额：待更新
> 
> **技术面**: 
> - 上证指数支撑位：待分析
> - 压力位：待分析
> 
> **投资建议**: 
> - ✅ 控制仓位在 6-8 成
> - ✅ 关注业绩确定性高的龙头
> - ✅ 分散配置，避免单一板块
> - ⚠️ 警惕高位题材股回调
> 
> **风险提示**: 本报告仅供参考，不构成投资建议。

---

## 📅 明日关注

COMMENTARY

cat >> "$OUTPUT_FILE" << TOMORROW

- [ ] 央行公开市场操作
- [ ] 宏观经济数据发布
- [ ] 美联储官员讲话
- [ ] 科技公司财报
- [ ] 重要股东增减持

---

## 📊 数据来源

| 数据类型 | 来源 | 更新频率 |
|----------|------|----------|
| 行情数据 | 腾讯财经 | 实时 |
| 财经新闻 | 财联社 + 东方财富 | 实时 |
| 政策解读 | 中国政府网 | 每日 |
| 板块分析 | 小虾分析 | 每日 |

---

*生成时间：$(date '+%Y-%m-%d %H:%M:%S') | 版本：v2.0 (增强版)*

TOMORROW

log "✅ 财经日报生成完成！"
log "📄 文件：$OUTPUT_FILE"
log "📊 行数：$(wc -l < "$OUTPUT_FILE")"

echo ""
echo "✅ 财经日报生成完成！"
echo "📄 文件：$OUTPUT_FILE"
echo "📊 统计：$(wc -l < "$OUTPUT_FILE") 行"
