#!/bin/bash
# 华尔街见闻 (wallstreetcn.com) 抓取脚本
# 抓取快讯和热门文章

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/../../temp"
OUTPUT_FILE="${TEMP_DIR}/wallstreetcn_content.md"

mkdir -p "${TEMP_DIR}"

URL="https://www.wallstreetcn.com/"

echo "抓取华尔街见闻：${URL}"

# 使用 curl 抓取，带 User-Agent
content=$(curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "${URL}" 2>/dev/null)

if [[ -z "${content}" ]]; then
    echo "ERROR: 华尔街见闻抓取失败，内容为空"
    exit 1
fi

# 创建输出文件
cat > "${OUTPUT_FILE}" << 'EOF'
## 🌐 华尔街见闻

EOF

# 提取文章标题
echo "${content}" | grep -oP 'title="[^"]{20,80}"' | sed 's/title="//g; s/"$//g' | sort -u | grep -v "^广告\|^直播\|^华尔街" | head -15 | while read -r title; do
    if [[ -n "${title}" && ${#title} -gt 15 ]]; then
        echo "- ${title}" >> "${OUTPUT_FILE}"
    fi
done

# 统计抓取到的新闻数量
news_count=$(grep -c "^-" "${OUTPUT_FILE}" 2>/dev/null || echo "0")

if [[ ${news_count} -ge 3 ]]; then
    echo "✓ 华尔街见闻抓取完成：${news_count}条新闻"
    exit 0
else
    echo "WARNING: 华尔街见闻抓取到的新闻较少 (${news_count}条)"
    exit 0
fi
