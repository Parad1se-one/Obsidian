#!/bin/bash
# 财经日报生成器
# 将各数据源内容整合成结构化日报

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/../temp"
OUTPUT_FILE="$1"

if [[ -z "${OUTPUT_FILE}" ]]; then
    echo "ERROR: 未指定输出文件"
    exit 1
fi

DATE_STR=$(date '+%Y-%m-%d')
WEEKDAY=$(date '+%A')

# 创建输出文件
cat > "${OUTPUT_FILE}" << EOF
# 📈 财经日报 ${DATE_STR}

> 生成时间：$(date '+%Y-%m-%d %H:%M:%S') | 星期${WEEKDAY}

---

EOF

# 1. 财联社快讯
if [[ -f "${TEMP_DIR}/cls_content.md" ]]; then
    echo "## ⚡ 重要快讯" >> "${OUTPUT_FILE}"
    echo "" >> "${OUTPUT_FILE}"
    cat "${TEMP_DIR}/cls_content.md" | tail -n +3 >> "${OUTPUT_FILE}"
    echo "" >> "${OUTPUT_FILE}"
    echo "---" >> "${OUTPUT_FILE}"
    echo "" >> "${OUTPUT_FILE}"
fi

# 2. 21 经济网
if [[ -f "${TEMP_DIR}/21jingji_content.md" ]]; then
    content=$(cat "${TEMP_DIR}/21jingji_content.md" | tail -n +3)
    if [[ -n "${content}" && "${content}" != "## 📰 21 经济网 - 热门新闻" ]]; then
        echo "## 📰 深度报道" >> "${OUTPUT_FILE}"
        echo "" >> "${OUTPUT_FILE}"
        echo "${content}" >> "${OUTPUT_FILE}"
        echo "" >> "${OUTPUT_FILE}"
        echo "---" >> "${OUTPUT_FILE}"
        echo "" >> "${OUTPUT_FILE}"
    fi
fi

# 3. 财经头条
if [[ -f "${TEMP_DIR}/caijing-toutiao_content.md" ]]; then
    content=$(cat "${TEMP_DIR}/caijing-toutiao_content.md" | tail -n +3)
    if [[ -n "${content}" && "${content}" != "## 📈 财经头条 - 焦点新闻" ]]; then
        echo "## 📊 焦点新闻" >> "${OUTPUT_FILE}"
        echo "" >> "${OUTPUT_FILE}"
        echo "${content}" >> "${OUTPUT_FILE}"
        echo "" >> "${OUTPUT_FILE}"
        echo "---" >> "${OUTPUT_FILE}"
        echo "" >> "${OUTPUT_FILE}"
    fi
fi

# 4. 东方财富
if [[ -f "${TEMP_DIR}/eastmoney_content.md" ]]; then
    content=$(cat "${TEMP_DIR}/eastmoney_content.md" | tail -n +3)
    if [[ -n "${content}" && "${content}" != "## 🔥 东方财富热门话题" ]]; then
        echo "## 🔥 热门话题" >> "${OUTPUT_FILE}"
        echo "" >> "${OUTPUT_FILE}"
        echo "${content}" >> "${OUTPUT_FILE}"
        echo "" >> "${OUTPUT_FILE}"
    fi
fi

# 5. 华尔街见闻
if [[ -f "${TEMP_DIR}/wallstreetcn_content.md" ]]; then
    content=$(cat "${TEMP_DIR}/wallstreetcn_content.md" | tail -n +3)
    if [[ -n "${content}" && "${content}" != "## 🌐 华尔街见闻" ]]; then
        echo "" >> "${OUTPUT_FILE}"
        echo "---" >> "${OUTPUT_FILE}"
        echo "" >> "${OUTPUT_FILE}"
        echo "## 🌐 华尔街见闻" >> "${OUTPUT_FILE}"
        echo "" >> "${OUTPUT_FILE}"
        echo "${content}" >> "${OUTPUT_FILE}"
        echo "" >> "${OUTPUT_FILE}"
    fi
fi

# 6. 财经日历
echo "---" >> "${OUTPUT_FILE}"
echo "" >> "${OUTPUT_FILE}"
if [[ -f "${TEMP_DIR}/finance_calendar_content.md" ]]; then
    cat "${TEMP_DIR}/finance_calendar_content.md" >> "${OUTPUT_FILE}"
else
    echo "## 📅 财经日历" >> "${OUTPUT_FILE}"
    echo "" >> "${OUTPUT_FILE}"
    echo "*明日重点关注：*" >> "${OUTPUT_FILE}"
    echo "- [待补充]" >> "${OUTPUT_FILE}"
fi

echo "✓ 日报生成完成：${OUTPUT_FILE}"
exit 0
