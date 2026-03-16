#!/bin/bash
# 财联社 (cls.cn) 抓取脚本
# 抓取 24 小时电报/快讯

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/../../temp"
OUTPUT_FILE="${TEMP_DIR}/cls_content.md"

mkdir -p "${TEMP_DIR}"

URL="https://www.cls.cn/telegraph"

echo "抓取财联社：${URL}"

# 使用 curl 抓取，带 User-Agent
content=$(curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "${URL}" 2>/dev/null)

if [[ -z "${content}" ]]; then
    echo "ERROR: 财联社抓取失败，内容为空"
    exit 1
fi

# 创建输出文件
cat > "${OUTPUT_FILE}" << 'EOF'
## ⚡ 财联社快讯

EOF

# 提取新闻内容 (从 "content":"..." 提取)
echo "${content}" | grep -oP '"content":"\【[^"]+' | sed 's/"content":"//g' | head -20 | while read -r title; do
    if [[ -n "${title}" && ${#title} -gt 5 ]]; then
        echo "- ${title}" >> "${OUTPUT_FILE}"
    fi
done

# 统计抓取到的新闻数量
news_count=$(grep -c "^-" "${OUTPUT_FILE}" 2>/dev/null || echo "0")

if [[ ${news_count} -ge 5 ]]; then
    echo "✓ 财联社抓取完成：${news_count}条快讯"
    exit 0
else
    echo "WARNING: 财联社抓取到的新闻较少 (${news_count}条)"
    exit 0
fi
