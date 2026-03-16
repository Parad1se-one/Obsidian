#!/bin/bash
# 财经头条 (caijingtoutiao.com) 抓取脚本
# 抓取涨停复盘和收评

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/../../temp"
OUTPUT_FILE="${TEMP_DIR}/caijing-toutiao_content.md"

mkdir -p "${TEMP_DIR}"

URL="http://www.caijingtoutiao.com/"

echo "抓取财经头条：${URL}"

content=$(curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "${URL}" 2>/dev/null)

if [[ -z "${content}" ]]; then
    echo "ERROR: 财经头条抓取失败，内容为空"
    exit 1
fi

echo "## 📈 财经头条" > "${OUTPUT_FILE}"
echo "" >> "${OUTPUT_FILE}"

# 提取涨停复盘内容
echo "${content}" | grep -oP '涨停.{10,40}' | head -10 | while read -r line; do
    echo "- ${line}" >> "${OUTPUT_FILE}"
done

echo "✓ 财经头条抓取完成：${OUTPUT_FILE}"
exit 0
