#!/bin/bash
# searxng-search.sh - 使用 SearXNG 进行搜索
# 用法：./searxng-search.sh <查询词> [引擎] [数量]
# 示例：./searxng-search.sh "强化学习论文" google 10

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SEARXNG_URL="http://127.0.0.1:8080"

# 参数
QUERY="${1:-}"
ENGINE="${2:-}"
LIMIT="${3:-10}"

if [ -z "$QUERY" ]; then
    echo "用法：$0 <查询词> [引擎] [数量]"
    echo ""
    echo "参数说明:"
    echo "  查询词  - 搜索关键词 (必填)"
    echo "  引擎    - 指定搜索引擎 (可选): google, bing, duckduckgo, google scholar, arxiv, github"
    echo "  数量    - 返回结果数量 (默认：10)"
    echo ""
    echo "示例:"
    echo "  $0 \"强化学习论文\" google 10"
    echo "  $0 \"python tutorial\" duckduckgo"
    echo "  $0 \"transformer architecture\""
    exit 1
fi

# 检查 SearXNG 是否运行
if ! sudo docker ps --format '{{.Names}}' | grep -q searxng; then
    echo "❌ SearXNG 容器未运行"
    echo "💡 运行：cd /home/openclaw/.openclaw/workspace/.docker/searxng && docker compose up -d"
    exit 1
fi

# 构建查询
if [ -n "$ENGINE" ]; then
    ENGINE_PARAM="--data-urlencode"
    ENGINE_VAL="engines=$ENGINE"
else
    ENGINE_PARAM=""
    ENGINE_VAL=""
fi

# 执行搜索
echo "🔍 搜索：$QUERY"
[ -n "$ENGINE" ] && echo "🎯 引擎：$ENGINE"
echo "📊 数量：$LIMIT"
echo ""

# 使用 curl 的 --get和 --data-urlencode 自动处理 URL 编码
if [ -n "$ENGINE_PARAM" ]; then
    RESPONSE=$(curl -s --get "$SEARXNG_URL/search" \
      --data-urlencode "q=$QUERY" \
      --data-urlencode "$ENGINE_VAL" \
      --data-urlencode "language=zh-CN")
else
    RESPONSE=$(curl -s --get "$SEARXNG_URL/search" \
      --data-urlencode "q=$QUERY" \
      --data-urlencode "language=zh-CN")
fi

# 解析结果
echo "$RESPONSE" | python3 << PYTHON
import sys
import json

try:
    data = json.load(sys.stdin)
    results = data.get('results', [])[:$LIMIT]
    
    if not results:
        print("❌ 未找到相关结果")
        sys.exit(1)
    
    print(f"✅ 找到 {len(results)} 条结果\n")
    print("=" * 60)
    
    for i, r in enumerate(results, 1):
        title = r.get('title', '无标题')
        url = r.get('url', '无链接')
        content = r.get('content', '')[:200]  # 截取前 200 字
        engine = r.get('engine', 'unknown')
        
        print(f"\n{i}. {title}")
        print(f"   🔗 {url}")
        if content:
            print(f"   📝 {content}...")
        print(f"   🎯 来源：{engine}")
    
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"❌ 解析错误：{e}")
    print(f"原始响应：{sys.stdin.read()[:500]}")
    sys.exit(1)
PYTHON
