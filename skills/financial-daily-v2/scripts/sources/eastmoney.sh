#!/bin/bash
# 东方财富财富号 (caifuhao.eastmoney.com) 抓取脚本
# 抓取热门话题

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/../../temp"
OUTPUT_FILE="${TEMP_DIR}/eastmoney_content.md"

mkdir -p "${TEMP_DIR}"

URL="https://caifuhao.eastmoney.com/"

echo "抓取东方财富财富号：${URL}"

content=$(curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "${URL}" 2>/dev/null)

if [[ -z "${content}" ]]; then
    echo "ERROR: 东方财富抓取失败，内容为空"
    exit 1
fi

echo "## 🔥 东方财富热门话题" > "${OUTPUT_FILE}"
echo "" >> "${OUTPUT_FILE}"

# 提取热门话题
echo "${content}" | grep -oP '(?<=#).{5,30}(?=#)' | head -10 | while read -r line; do
    echo "- #${line}" >> "${OUTPUT_FILE}"
done

echo "✓ 东方财富抓取完成：${OUTPUT_FILE}"
exit 0
