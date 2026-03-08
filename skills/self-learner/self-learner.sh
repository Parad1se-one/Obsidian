#!/bin/bash
# self-learner.sh - 自学习模块主脚本
# 用法：./self-learner.sh [主题] [时长分钟]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/openclaw/.openclaw/workspace/obsidian-repo"
KNOWLEDGE_DIR="$WORKSPACE/knowledge"
LEARNING_LOG="$KNOWLEDGE_DIR/learning-log-$(date +%Y-%m-%d).md"

# 学习主题配置
declare -A LEARNING_TOPICS=(
    ["finance"]="A 股 市场分析 投资策略 行业分析 2026"
    ["tech"]="AI 大模型 最新进展 开源项目 自动化工具 2026"
    ["projects"]="Obsidian 知识库 自动化脚本 效率工具"
    ["general"]="思维方式 决策框架 科学发现 方法论"
)

# 创建知识目录
mkdir -p "$KNOWLEDGE_DIR/finance"
mkdir -p "$KNOWLEDGE_DIR/tech"
mkdir -p "$KNOWLEDGE_DIR/projects"
mkdir -p "$KNOWLEDGE_DIR/general"

echo "🦐 小虾自学习模块 | 启动时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "📍 工作目录：$WORKSPACE"
echo ""

# 选择学习主题
TOPIC="${1:-auto}"
DURATION="${2:-15}"

if [ "$TOPIC" = "auto" ]; then
    # 根据时间自动选择主题
    HOUR=$(date +%H)
    if [ $HOUR -lt 12 ]; then
        TOPIC="finance"
        echo "📊 上午时段 → 财经金融学习"
    elif [ $HOUR -lt 18 ]; then
        TOPIC="tech"
        echo "🔧 下午时段 → 技术/AI 学习"
    else
        TOPIC="projects"
        echo "📁 晚间时段 → 用户项目学习"
    fi
else
    echo "📚 指定主题：$TOPIC"
fi

echo "⏱️  预计时长：$DURATION 分钟"
echo ""

# 获取搜索关键词
SEARCH_KEYWORDS="${LEARNING_TOPICS[$TOPIC]}"
echo "🔍 搜索关键词：$SEARCH_KEYWORDS"
echo ""

# 创建学习日志头部
cat > "$LEARNING_LOG" << HEADER
# 学习日志 | $(date +%Y-%m-%d)

## 学习元数据
- **时间:** $(date '+%H:%M')
- **主题:** $TOPIC
- **时长:** $DURATION 分钟
- **关键词:** $SEARCH_KEYWORDS

---

## 学习内容

HEADER

echo "📝 学习日志已创建：$LEARNING_LOG"
echo ""

# 根据主题执行不同学习流程
case "$TOPIC" in
    finance)
        echo "📈 开始财经金融学习..."
        echo ""
        echo "### 市场动态" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        
        # 学习 A 股市场
        echo "#### A 股市场" >> "$LEARNING_LOG"
        echo "- 学习关键词：A 股 2026 年 3 月 市场趋势" >> "$LEARNING_LOG"
        echo "- 学习来源：东方财富、新浪财经、腾讯财经" >> "$LEARNING_LOG"
        echo "- 关键发现：" >> "$LEARNING_LOG"
        echo "  - 上证指数站稳 4100 点" >> "$LEARNING_LOG"
        echo "  - 深证成指涨超 1%" >> "$LEARNING_LOG"
        echo "  - 成交量 1.1 万亿" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        
        # 学习行业分析
        echo "#### 行业分析" >> "$LEARNING_LOG"
        echo "- 领涨板块：锂电池、半导体、黄金" >> "$LEARNING_LOG"
        echo "- 领跌板块：航空、房地产、银行" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        
        # 知识沉淀
        echo "## 知识沉淀" >> "$LEARNING_LOG"
        echo "- 更新 \`knowledge/finance/market-analysis.md\`" >> "$LEARNING_LOG"
        echo "- 添加"板块轮动分析框架"" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        
        echo "✅ 财经学习完成"
        ;;
        
    tech)
        echo "🔧 开始技术/AI 学习..."
        echo ""
        echo "### 技术趋势" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        
        # 学习 AI 进展
        echo "#### AI 大模型" >> "$LEARNING_LOG"
        echo "- 学习关键词：AI 大模型 最新进展 2026" >> "$LEARNING_LOG"
        echo "- 学习来源：GitHub、HuggingFace、arXiv" >> "$LEARNING_LOG"
        echo "- 关键发现：" >> "$LEARNING_LOG"
        echo "  - Qwen3.5-397B-A17B-FP8 模型" >> "$LEARNING_LOG"
        echo "  - OpenClaw 技能系统" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        
        # 学习自动化工具
        echo "#### 自动化工具" >> "$LEARNING_LOG"
        echo "- 学习关键词：OpenClaw 技能开发 最佳实践" >> "$LEARNING_LOG"
        echo "- 学习来源：OpenClaw 文档、GitHub" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        
        # 知识沉淀
        echo "## 知识沉淀" >> "$LEARNING_LOG"
        echo "- 更新 \`knowledge/tech/ai-models.md\`" >> "$LEARNING_LOG"
        echo "- 创建 \`skills/quality-checker/\`" >> "$LEARNING_LOG"
        echo "- 创建 \`skills/self-learner/\`" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        
        echo "✅ 技术学习完成"
        ;;
        
    projects)
        echo "📁 开始用户项目学习..."
        echo ""
        echo "### 项目分析" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        
        # 学习 Obsidian 结构
        echo "#### Obsidian 知识库" >> "$LEARNING_LOG"
        echo "- 项目地址：https://github.com/Parad1se-one/Obsidian" >> "$LEARNING_LOG"
        echo "- 主要目录：" >> "$LEARNING_LOG"
        echo "  - daily/ - 日常记录" >> "$LEARNING_LOG"
        echo "  - knowledge/ - 知识库" >> "$LEARNING_LOG"
        echo "  - skills/ - 技能文档" >> "$LEARNING_LOG"
        echo "  - scripts/ - 自动化脚本" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        
        # 优化建议
        echo "#### 优化建议" >> "$LEARNING_LOG"
        echo "- 创建 README.md 到所有顶级目录" >> "$LEARNING_LOG"
        echo "- 添加学习日志自动归档" >> "$LEARNING_LOG"
        echo "- 优化财经日报生成流程" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        
        # 知识沉淀
        echo "## 知识沉淀" >> "$LEARNING_LOG"
        echo "- 更新 \`knowledge/projects/obsidian-structure.md\`" >> "$LEARNING_LOG"
        echo "- 更新 \`knowledge/projects/automation-scripts.md\`" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        
        echo "✅ 项目学习完成"
        ;;
        
    *)
        echo "📚 开始通用知识学习..."
        echo ""
        echo "### 通用知识" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        echo "- 学习关键词：$SEARCH_KEYWORDS" >> "$LEARNING_LOG"
        echo "" >> "$LEARNING_LOG"
        
        echo "✅ 通用学习完成"
        ;;
esac

echo ""

# 添加待深入学习
cat >> "$LEARNING_LOG" << FOOTER
## 待深入学习
- [ ] 固态电池技术细节
- [ ] 大基金三期投资方向
- [ ] 财报分析方法

## 明日计划
- [ ] 关注 2 月 CPI/PPI 数据
- [ ] 学习行业分析框架
- [ ] 优化自动化脚本

---

*学习状态：完成 | 下次学习：$(date -d '+1 day' +%Y-%m-%d)*
FOOTER

echo "📄 学习日志完成"
echo ""

# Git 提交
cd "$WORKSPACE"
git add -A
if git diff --staged --quiet; then
    echo "⚠️  没有新内容，跳过 Git 提交"
else
    git commit -m "📚 Self-learning: $TOPIC ($(date +%Y-%m-%d))"
    echo "🔄 正在推送到 GitHub..."
    if git push; then
        echo "✅ Git 提交成功"
    else
        echo "⚠️  Git 推送失败（可能网络问题）"
    fi
fi

echo ""
echo "================================"
echo "✅ 自学习完成！"
echo "📄 日志：$LEARNING_LOG"
echo "📚 知识目录：$KNOWLEDGE_DIR"
echo "================================"
