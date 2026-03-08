#!/bin/bash
# search.sh - 统一搜索工具 (基于 Whoogle)
# 用法：./search.sh "关键词" [引擎] [数量]
# 示例：./search.sh "python tutorial" google 10

set -e

WHOOGL_URL="${WHOOGL_URL:-http://127.0.0.1:5000}"
OUTPUT_FORMAT="${SEARCH_FORMAT:-text}"  # text|json|urls

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# 检查 Whoogle 是否可用
check_whoogle() {
    if ! curl -s -o /dev/null -w "%{http_code}" "$WHOOGL_URL/" 2>/dev/null | grep -q "200"; then
        return 1
    fi
    return 0
}

# 搜索函数
search() {
    local query="$1"
    local engine="${2:-google}"
    local count="${3:-10}"
    
    if [ -z "$query" ]; then
        log_error "请提供搜索关键词"
        echo "用法：$0 \"关键词\" [引擎] [数量]"
        echo "示例：$0 \"python tutorial\" google 10"
        exit 1
    fi
    
    # 检查 Whoogle 可用性
    if ! check_whoogle; then
        log_error "Whoogle 不可用 (地址：$WHOOGL_URL)"
        log_info "请检查容器状态：docker ps | grep whoogle"
        exit 1
    fi
    
    log_info "搜索：$query"
    
    # 获取搜索结果
    local response
    response=$(curl -s "$WHOOGL_URL/search?q=$(echo "$query" | sed 's/ /+/g')" --max-time 30)
    
    if [ -z "$response" ]; then
        log_error "搜索无响应"
        exit 1
    fi
    
    # 解析结果
    case "$OUTPUT_FORMAT" in
        json)
            echo "$response" | python3 -c "
import sys, re
from html import unescape

html = sys.stdin.read()

# 提取搜索结果
results = []
title_pattern = r'class=\"result__a\"[^>]*href=\"([^\"]+)\"[^>]*>([^<]+)'
desc_pattern = r'class=\"result__snippet\"[^>]*>([^<]+)'

for match in re.finditer(title_pattern, html):
    url = unescape(match.group(1))
    title = unescape(match.group(2))
    results.append({'title': title, 'url': url})

import json
print(json.dumps(results[:$count], ensure_ascii=False, indent=2))
"
            ;;
        urls)
            echo "$response" | grep -oP 'href="https?://[^"]+"' | sed 's/href="//g' | sed 's/"//g' | head -"$count"
            ;;
        text|*)
            echo "$response" | python3 -c "
import sys, re
from html import unescape

html = sys.stdin.read()

# 提取搜索结果 (Whoogle 格式)
# <a data-ved=\"...\" href=\"https://...\">Title</a>
title_pattern = r'<a[^>]*href=\"([^\"]+)\"[^>]*>([^<]+)'

print('=' * 60)
print(f'搜索结果')
print('=' * 60)

seen = set()
i = 0
for match in re.finditer(title_pattern, html):
    if i >= $count:
        break
    url = unescape(match.group(1).replace('&amp;', '&'))
    title = unescape(re.sub(r'<[^>]+>', '', match.group(2)))
    
    # 过滤无效结果
    if not url.startswith('http') or 'google.com/maps' in url:
        continue
    if url in seen:
        continue
    
    seen.add(url)
    i += 1
    print(f'\n{i}. {title}')
    print(f'   {url}')
"
            ;;
    esac
}

# 快速搜索 (只返回 URL)
search_urls() {
    local query="$1"
    local count="${2:-5}"
    
    OUTPUT_FORMAT="urls" search "$query" "" "$count"
}

# 搜索并返回第一条结果
search_first() {
    local query="$1"
    
    OUTPUT_FORMAT="urls" search "$query" "" 1 | head -1
}

# 主函数
main() {
    case "${1:-}" in
        --check)
            if check_whoogle; then
                log_success "Whoogle 运行正常 ($WHOOGL_URL)"
                exit 0
            else
                log_error "Whoogle 不可用 ($WHOOGL_URL)"
                exit 1
            fi
            ;;
        --urls)
            shift
            search_urls "$@"
            ;;
        --first)
            shift
            search_first "$@"
            ;;
        --help|-h)
            echo "用法：$0 [选项] \"关键词\" [引擎] [数量]"
            echo ""
            echo "选项:"
            echo "  --check     检查 Whoogle 状态"
            echo "  --urls      只返回 URL 列表"
            echo "  --first     只返回第一条结果的 URL"
            echo "  --help, -h  显示帮助"
            echo ""
            echo "环境变量:"
            echo "  WHOOGL_URL  Whoogle 地址 (默认：http://127.0.0.1:5000)"
            echo "  SEARCH_FORMAT 输出格式：text|json|urls (默认：text)"
            echo ""
            echo "示例:"
            echo "  $0 \"python tutorial\"           # 文本格式搜索"
            echo "  $0 --urls \"github\" 10          # 只返回 URL"
            echo "  $0 --first \"weather beijing\"   # 第一条结果"
            echo "  SEARCH_FORMAT=json $0 \"AI news\" # JSON 格式"
            ;;
        *)
            search "$@"
            ;;
    esac
}

main "$@"
