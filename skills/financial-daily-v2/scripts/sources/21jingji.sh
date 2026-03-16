#!/bin/bash
# 21 经济网 (21jingji.com) 抓取脚本
# 抓取深度报道和热门新闻

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/../../temp"
OUTPUT_FILE="${TEMP_DIR}/21jingji_content.md"

mkdir -p "${TEMP_DIR}"

URL="https://www.21jingji.com/"

echo "抓取 21 经济网：${URL}"

# 使用 curl 抓取，带 User-Agent
content=$(curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "${URL}" 2>/dev/null)

if [[ -z "${content}" ]]; then
    echo "ERROR: 21 经济网抓取失败，内容为空"
    exit 1
fi

# 创建输出文件
cat > "${OUTPUT_FILE}" << 'EOF'
## 📰 21 经济网 - 热门新闻

EOF

# 提取新闻标题 (从 title 属性提取)
echo "${content}" | grep -oP 'title="[^"]{20,80}"' | sed 's/title="//g; s/"$//g' | grep -v "^21 视频\|^21 直播\|^广告\|^湾区" | head -20 | while read -r title; do
    if [[ -n "${title}" && ${#title} -gt 15 ]]; then
        echo "- ${title}" >> "${OUTPUT_FILE}"
    fi
done

# 统计抓取到的新闻数量
news_count=$(grep -c "^-" "${OUTPUT_FILE}" 2>/dev/null || echo "0")

if [[ ${news_count} -ge 5 ]]; then
    echo "✓ 21 经济网抓取完成：${news_count}条新闻"
    exit 0
else
    echo "WARNING: 21 经济网抓取到的新闻较少 (${news_count}条)"
    exit 0
fi
