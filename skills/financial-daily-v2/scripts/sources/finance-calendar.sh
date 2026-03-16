#!/bin/bash
# 财经日历数据源
# 生成明日重点关注内容

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/../../temp"
OUTPUT_FILE="${TEMP_DIR}/finance_calendar_content.md"

mkdir -p "${TEMP_DIR}"

echo "生成财经日历..."

# 获取明天日期
TOMORROW=$(date -d "+1 day" '+%Y-%m-%d')
TOMORROW_WEEKDAY=$(date -d "+1 day" '+%A')

# 创建输出文件
cat > "${OUTPUT_FILE}" << EOF
## 📅 财经日历

**明日**: ${TOMORROW} (星期${TOMORROW_WEEKDAY})

### 重点关注
EOF

# 根据今日新闻推断明日关注点
echo "" >> "${OUTPUT_FILE}"

# 检查是否有芯片/半导体相关新闻
if grep -q "芯片\|半导体\|存储" "${TEMP_DIR}/cls_content.md" 2>/dev/null; then
    echo "- 🔹 **科技股**：芯片/半导体板块延续性观察" >> "${OUTPUT_FILE}"
fi

# 检查是否有储能/绿电新闻
if grep -q "储能\|绿电\|新能源" "${TEMP_DIR}/cls_content.md" 2>/dev/null; then
    echo "- 🔹 **新能源**：储能/绿电概念超跌反弹机会" >> "${OUTPUT_FILE}"
fi

# 检查是否有金属/大宗商品新闻
if grep -q "钨\|金属\|大宗商品\|期货" "${TEMP_DIR}/cls_content.md" 2>/dev/null; then
    echo "- 🔹 **大宗商品**：钨价持续走高，关注相关概念股" >> "${OUTPUT_FILE}"
fi

# 检查是否有 AI 相关新闻
if grep -q "AI\|智能体\|阿里巴巴\|钉钉" "${TEMP_DIR}/cls_content.md" 2>/dev/null; then
    echo "- 🔹 **AI 概念**：阿里巴巴企业级 AI Agent 发布进展" >> "${OUTPUT_FILE}"
fi

# 检查是否有 C919/航空新闻
if grep -q "C919\|航空\|大飞机" "${TEMP_DIR}/cls_content.md" 2>/dev/null; then
    echo "- 🔹 **大飞机**：C919 新航线运营情况跟踪" >> "${OUTPUT_FILE}"
fi

# 检查是否有港股新闻
if grep -q "港股\|恒生" "${TEMP_DIR}/21jingji_content.md" 2>/dev/null; then
    echo "- 🔹 **港股**：关注港股科技股延续表现" >> "${OUTPUT_FILE}"
fi

# 默认关注点 (如果上面没有匹配到)
if [[ $(grep -c "🔹" "${OUTPUT_FILE}") -lt 1 ]]; then
    echo "- 🔹 **市场情绪**：观察两市成交量变化" >> "${OUTPUT_FILE}"
    echo "- 🔹 **北向资金**：关注外资流向" >> "${OUTPUT_FILE}"
fi

# 添加通用关注点
echo "" >> "${OUTPUT_FILE}"
echo "### 经济数据" >> "${OUTPUT_FILE}"
echo "" >> "${OUTPUT_FILE}"
echo "- [待更新：次日将公布的经济数据]" >> "${OUTPUT_FILE}"

echo "✓ 财经日历生成完成"
exit 0
