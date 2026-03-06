#!/bin/bash
# newsapi-collector.sh - NewsAPI 新闻采集器
# 用法：./newsapi-collector.sh [关键词] [日期]

set -e

# 检查 API Key
if [ -z "$NEWS_API_KEY" ]; then
    echo "❌ 错误：NEWS_API_KEY 未设置"
    echo "请在 https://newsapi.org/register 获取免费 API Key"
    echo "然后设置：export NEWS_API_KEY=your_api_key"
    exit 1
fi

KEYWORD="${1:-business finance economy}"
DATE="${2:-$(date -d 'yesterday' +%Y-%m-%d)}"
COUNTRY="${3:-cn}"
LANGUAGE="${4:-zh}"

echo "🔍 采集新闻..."
echo "   关键词：$KEYWORD"
echo "   日期：$DATE"
echo "   国家：$COUNTRY"
echo "   语言：$LANGUAGE"
echo ""

# 调用 NewsAPI
# 文档：https://newsapi.org/docs/endpoints/top-headlines
RESPONSE=$(curl -s -G "https://newsapi.org/v2/top-headlines" \
    --data-urlencode "country=$COUNTRY" \
    --data-urlencode "category=business" \
    --data-urlencode "pageSize=10" \
    --data-urlencode "apiKey=$NEWS_API_KEY")

# 检查响应状态
STATUS=$(echo "$RESPONSE" | jq -r '.status // "error"')

if [ "$STATUS" != "ok" ]; then
    echo "❌ API 调用失败"
    echo "响应：$RESPONSE"
    exit 1
fi

# 解析并输出新闻
echo "✅ 获取成功，共 $(echo "$RESPONSE" | jq '.totalResults') 条新闻"
echo ""

# 输出前 5 条新闻
echo "$RESPONSE" | jq -r '.articles[:5] | .[] | "### \(.title)\n\n**来源:** \(.source.name) | **时间:** \(.publishedAt)\n\n\(.description // "无摘要")\n\n[阅读原文](\(.url))\n\n---\n\n"'

echo ""
echo "📊 剩余可用请求：$(echo "$RESPONSE" | jq '.totalResults // 0') 条"
