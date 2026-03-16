#!/bin/bash
# 21 经济网 (21jingji.com) 抓取脚本
# 抓取深度报道和热文排行

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/../../temp"
OUTPUT_FILE="${TEMP_DIR}/21jingji_content.md"

mkdir -p "${TEMP_DIR}"

URL="https://www.21jingji.com/"

echo "抓取 21 经济网：${URL}"

content=$(curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "${URL}" 2>/dev/null)

if [[ -z "${content}" ]]; then
    echo "ERROR: 21 经济网抓取失败，内容为空"
    exit 1
fi

echo "## 📰 21 经济网" > "${OUTPUT_FILE}"
echo "" >> "${OUTPUT_FILE}"

# 提取证券频道新闻
echo "${content}" | grep -oP '(?<=\[).{10,50}(?=\])' | head -10 | while read -r line; do
    echo "- ${line}" >> "${OUTPUT_FILE}"
done

echo "✓ 21 经济网抓取完成：${OUTPUT_FILE}"
exit 0
