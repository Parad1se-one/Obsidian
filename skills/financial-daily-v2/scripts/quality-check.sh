#!/bin/bash
# 财经日报质量检查脚本
# 检查生成内容的质量和完整性

INPUT_FILE="$1"
MIN_SCORE=80

if [[ -z "${INPUT_FILE}" ]]; then
    echo "ERROR: 未指定输入文件"
    exit 1
fi

if [[ ! -f "${INPUT_FILE}" ]]; then
    echo "ERROR: 文件不存在：${INPUT_FILE}"
    exit 1
fi

SCORE=0
MAX_SCORE=100

# 检查项 1: 文件非空 (20 分)
if [[ -s "${INPUT_FILE}" ]]; then
    SCORE=$((SCORE + 20))
    echo "✓ 检查 1: 文件非空 (+20)"
else
    echo "✗ 检查 1: 文件为空"
fi

# 检查项 2: 包含标题 (20 分)
if grep -q "# 📈 财经日报" "${INPUT_FILE}"; then
    SCORE=$((SCORE + 20))
    echo "✓ 检查 2: 包含标题 (+20)"
else
    echo "✗ 检查 2: 缺少标题"
fi

# 检查项 3: 包含日期 (20 分)
if grep -q "$(date '+%Y-%m-%d')" "${INPUT_FILE}"; then
    SCORE=$((SCORE + 20))
    echo "✓ 检查 3: 包含日期 (+20)"
else
    echo "✗ 检查 3: 缺少日期"
fi

# 检查项 4: 至少有一个数据源内容 (20 分)
if grep -qE "## (⚡|📰|📊|🔥)" "${INPUT_FILE}"; then
    SCORE=$((SCORE + 20))
    echo "✓ 检查 4: 包含数据源内容 (+20)"
else
    echo "✗ 检查 4: 缺少数据源内容"
fi

# 检查项 5: 内容长度合理 (20 分)
LINE_COUNT=$(wc -l < "${INPUT_FILE}")
if [[ ${LINE_COUNT} -ge 20 ]]; then
    SCORE=$((SCORE + 20))
    echo "✓ 检查 5: 内容长度合理 (${LINE_COUNT}行) (+20)"
else
    echo "✗ 检查 5: 内容过短 (${LINE_COUNT}行)"
fi

echo ""
echo "总得分：${SCORE}/${MAX_SCORE}"

if [[ ${SCORE} -ge ${MIN_SCORE} ]]; then
    echo "✓ 质量检查通过"
    exit 0
else
    echo "✗ 质量检查未通过 (最低要求：${MIN_SCORE}分)"
    exit 1
fi
