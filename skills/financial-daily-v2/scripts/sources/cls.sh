#!/bin/bash
# 财联社 (cls.cn) 抓取脚本
# 抓取 24 小时电报/快讯

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/../../temp"
OUTPUT_FILE="${TEMP_DIR}/cls_content.md"

mkdir -p "${TEMP_DIR}"

# 使用 curl 抓取财联社电报
# 注意：实际使用中可能需要处理反爬机制
URL="https://www.cls.cn/telegraph"

echo "抓取财联社：${URL}"

# 使用 web_fetch 或 curl 抓取
# 这里使用 curl + 简单解析
content=$(curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "${URL}" 2>/dev/null)

if [[ -z "${content}" ]]; then
    echo "ERROR: 财联社抓取失败，内容为空"
    exit 1
fi

# 解析内容 (简化版，实际可能需要更复杂的解析)
# 提取时间戳和新闻标题
echo "## ⚡ 财联社快讯" > "${OUTPUT_FILE}"
echo "" >> "${OUTPUT_FILE}"

# 使用 grep/sed 提取关键信息 (示例)
echo "${content}" | grep -oP '\d{2}:\d{2}:\d{2}.*?(?=</span>|<br)|【.*?】' | head -20 | while read -r line; do
    echo "- ${line}" >> "${OUTPUT_FILE}"
done

echo "✓ 财联社抓取完成：${OUTPUT_FILE}"
exit 0
