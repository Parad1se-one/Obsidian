#!/bin/bash
# 财经头条 (caijingtoutiao.com) 抓取脚本
# 抓取焦点新闻和热门推荐

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/../../temp"
OUTPUT_FILE="${TEMP_DIR}/caijing-toutiao_content.md"

mkdir -p "${TEMP_DIR}"

URL="http://www.caijingtoutiao.com/"

echo "抓取财经头条：${URL}"

# 使用 curl 抓取，带 User-Agent
content=$(curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "${URL}" 2>/dev/null)

if [[ -z "${content}" ]]; then
    echo "ERROR: 财经头条抓取失败，内容为空"
    exit 1
fi

# 创建输出文件
cat > "${OUTPUT_FILE}" << 'EOF'
## 📈 财经头条 - 焦点新闻

EOF

# 提取新闻标题 (从 class="tit" title 属性提取)
echo "${content}" | grep -oP 'class="tit"[^>]+title="[^"]+"' | grep -oP 'title="\K[^"]+' | grep -v "^广告\|^东莞\|^农银\|^玉环\|^Web3\|^2026 年" | head -20 | while read -r title; do
    if [[ -n "${title}" && ${#title} -gt 10 && ${#title} -lt 60 ]]; then
        echo "- ${title}" >> "${OUTPUT_FILE}"
    fi
done

# 统计抓取到的新闻数量
news_count=$(grep -c "^-" "${OUTPUT_FILE}" 2>/dev/null || echo "0")

if [[ ${news_count} -ge 5 ]]; then
    echo "✓ 财经头条抓取完成：${news_count}条新闻"
    exit 0
else
    echo "WARNING: 财经头条抓取到的新闻较少 (${news_count}条)"
    exit 0
fi
