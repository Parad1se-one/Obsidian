#!/bin/bash
# quality-checker.sh - 输出质量自检脚本
# 用法：./quality-checker.sh <内容文件> <类型>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTENT_FILE="$1"
CONTENT_TYPE="${2:-general}"

if [ -z "$CONTENT_FILE" ] || [ ! -f "$CONTENT_FILE" ]; then
    echo "❌ 错误：请指定有效的内容文件"
    echo "用法：./quality-checker.sh <内容文件> [类型]"
    echo "类型：financial|academic|report|general"
    exit 1
fi

echo "🦐 小虾质量检查 | 文件：$CONTENT_FILE | 类型：$CONTENT_TYPE"
echo ""

# 读取文件内容
CONTENT=$(cat "$CONTENT_FILE")

# 初始化分数
DATA_AUTH=0
INFO_COMPLETE=0
ADVICE_ACTIONABLE=0
FORMAT_QUALITY=0

# 根据类型选择检查规则
case "$CONTENT_TYPE" in
    financial)
        echo "📊 财经类内容检查"
        echo ""
        
        # 数据真实性检查 (40%)
        echo "📋 检查数据真实性..."
        
        # 检查是否有数据来源标注
        if echo "$CONTENT" | grep -q "数据来源.*腾讯\|数据来源.*新浪\|数据来源.*东方财富"; then
            DATA_AUTH=90
            echo "✅ 数据来源明确"
        elif echo "$CONTENT" | grep -q "数据来源"; then
            DATA_AUTH=70
            echo "⚠️  有数据来源但不够具体"
        else
            DATA_AUTH=0
            echo "❌ 无数据来源标注"
        fi
        
        # 检查是否有编造痕迹（模拟数据）
        if echo "$CONTENT" | grep -q "模拟数据\|MVP 测试"; then
            DATA_AUTH=0
            echo "❌ 检测到模拟数据，直接不及格"
        fi
        
        # 信息完整性检查 (25%)
        echo "📋 检查信息完整性..."
        COMPLETE_COUNT=0
        
        # 检查关键模块
        echo "$CONTENT" | grep -q "市场概览" && COMPLETE_COUNT=$((COMPLETE_COUNT + 1))
        echo "$CONTENT" | grep -q "今日头条\|新闻" && COMPLETE_COUNT=$((COMPLETE_COUNT + 1))
        echo "$CONTENT" | grep -q "公司动态" && COMPLETE_COUNT=$((COMPLETE_COUNT + 1))
        echo "$CONTENT" | grep -q "行业热点\|板块" && COMPLETE_COUNT=$((COMPLETE_COUNT + 1))
        echo "$CONTENT" | grep -q "点评\|建议" && COMPLETE_COUNT=$((COMPLETE_COUNT + 1))
        echo "$CONTENT" | grep -q "明日关注" && COMPLETE_COUNT=$((COMPLETE_COUNT + 1))
        
        INFO_COMPLETE=$((COMPLETE_COUNT * 100 / 6))
        echo "✅ 模块覆盖率：$COMPLETE_COUNT/6 ($INFO_COMPLETE%)"
        
        # 建议可操作性检查 (20%)
        echo "📋 检查建议可操作性..."
        ADVICE_COUNT=0
        
        echo "$CONTENT" | grep -q "建议关注\|推荐" && ADVICE_COUNT=$((ADVICE_COUNT + 1))
        echo "$CONTENT" | grep -q "风险\|谨慎" && ADVICE_COUNT=$((ADVICE_COUNT + 1))
        echo "$CONTENT" | grep -q "仓位\|止损" && ADVICE_COUNT=$((ADVICE_COUNT + 1))
        
        if [ $ADVICE_COUNT -ge 3 ]; then
            ADVICE_ACTIONABLE=85
        elif [ $ADVICE_COUNT -ge 2 ]; then
            ADVICE_ACTIONABLE=70
        elif [ $ADVICE_COUNT -ge 1 ]; then
            ADVICE_ACTIONABLE=55
        else
            ADVICE_ACTIONABLE=40
        fi
        echo "✅ 建议质量：$ADVICE_ACTIONABLE/100"
        
        # 格式规范性检查 (15%)
        echo "📋 检查格式规范性..."
        FORMAT_COUNT=0
        
        echo "$CONTENT" | grep -q "^#" && FORMAT_COUNT=$((FORMAT_COUNT + 1))
        echo "$CONTENT" | grep -q "^|" && FORMAT_COUNT=$((FORMAT_COUNT + 1))
        echo "$CONTENT" | grep -q "免责声明" && FORMAT_COUNT=$((FORMAT_COUNT + 1))
        echo "$CONTENT" | grep -q "^\*" && FORMAT_COUNT=$((FORMAT_COUNT + 1))
        
        FORMAT_QUALITY=$((FORMAT_COUNT * 25))
        echo "✅ 格式质量：$FORMAT_QUALITY/100"
        ;;
        
    academic)
        echo "📚 学术类内容检查"
        # 学术论文检查逻辑
        DATA_AUTH=80
        INFO_COMPLETE=80
        ADVICE_ACTIONABLE=70
        FORMAT_QUALITY=85
        ;;
        
    *)
        echo "📝 通用检查"
        # 通用检查逻辑
        DATA_AUTH=75
        INFO_COMPLETE=75
        ADVICE_ACTIONABLE=70
        FORMAT_QUALITY=80
        ;;
esac

echo ""

# 计算综合得分（加权平均）
TOTAL_SCORE=$((DATA_AUTH * 40 / 100 + INFO_COMPLETE * 25 / 100 + ADVICE_ACTIONABLE * 20 / 100 + FORMAT_QUALITY * 15 / 100))

# 输出评估报告
echo "================================"
echo "## 质量评估报告"
echo ""
echo "| 维度 | 得分 | 说明 |"
echo "|------|------|------|"
echo "| 数据真实性 | $DATA_AUTH/100 | 权重 40% |"
echo "| 信息完整性 | $INFO_COMPLETE/100 | 权重 25% |"
echo "| 建议可操作性 | $ADVICE_ACTIONABLE/100 | 权重 20% |"
echo "| 格式规范性 | $FORMAT_QUALITY/100 | 权重 15% |"
echo ""
echo "**综合得分：$TOTAL_SCORE/100**"
echo ""

# 判断等级
if [ $TOTAL_SCORE -ge 90 ]; then
    echo "🟢 优秀 - 直接输出"
    RESULT="PASS"
elif [ $TOTAL_SCORE -ge 80 ]; then
    echo "🟡 良好 - 通过（标注改进点）"
    RESULT="PASS_WITH_NOTES"
elif [ $TOTAL_SCORE -ge 70 ]; then
    echo "🟠 及格 - 询问用户是否接受"
    RESULT="ASK_USER"
else
    echo "🔴 不及格 - 必须重做"
    RESULT="FAIL"
fi

echo ""
echo "================================"
echo "处理决定：$RESULT"
echo ""

# 输出改进建议
if [ $DATA_AUTH -lt 80 ]; then
    echo "⚠️  改进建议：补充数据来源，确保真实性"
fi
if [ $INFO_COMPLETE -lt 80 ]; then
    echo "⚠️  改进建议：补充缺失的关键模块"
fi
if [ $ADVICE_ACTIONABLE -lt 75 ]; then
    echo "⚠️  改进建议：细化建议，增加可操作性"
fi
if [ $FORMAT_QUALITY -lt 80 ]; then
    echo "⚠️  改进建议：优化格式和排版"
fi

echo ""

# 返回结果
case "$RESULT" in
    PASS)
        exit 0
        ;;
    PASS_WITH_NOTES)
        exit 0
        ;;
    ASK_USER)
        exit 2
        ;;
    FAIL)
        exit 1
        ;;
esac
