#!/bin/bash
# paper-deep-reader.sh - 学术论文精读技能
# 用法：./paper-deep-reader.sh [PDF 路径/URL] [输出文件名]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="/home/openclaw/.openclaw/workspace/obsidian-repo/survey/paper-deep-reading"
TEMPLATE_FILE="$SCRIPT_DIR/templates/deep-reading-template.md"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 检查参数
if [ -z "$1" ]; then
    echo "🦐 小虾论文精读 | 学术论文深度阅读工具"
    echo ""
    echo "用法:"
    echo "  ./paper-deep-reader.sh <PDF 路径或 URL> [输出文件名]"
    echo ""
    echo "示例:"
    echo "  ./paper-deep-reader.sh /path/to/paper.pdf"
    echo "  ./paper-deep-reader.sh https://arxiv.org/pdf/xxxx.xxxxx.pdf \"RLVR_Survey_2026\""
    echo ""
    echo "输出位置：$OUTPUT_DIR/"
    exit 0
fi

PAPER_INPUT="$1"
OUTPUT_NAME="${2:-$(date +%Y%m%d_%H%M%S)}"
OUTPUT_FILE="$OUTPUT_DIR/${OUTPUT_NAME}.md"

echo "🦐 小虾论文精读"
echo "📄 输入：$PAPER_INPUT"
echo "📍 输出：$OUTPUT_FILE"
echo ""

# 检查是否为 URL
if [[ "$PAPER_INPUT" =~ ^https?:// ]]; then
    echo "🔍 检测到 URL，正在下载论文..."
    # TODO: 实现 PDF 下载
    # curl -L -o "$TEMP_PDF" "$PAPER_INPUT"
    echo "⚠️  PDF 下载功能待实现，请先手动下载 PDF 到本地"
    exit 1
fi

# 检查 PDF 文件是否存在
if [ ! -f "$PAPER_INPUT" ]; then
    echo "❌ 错误：文件不存在 $PAPER_INPUT"
    exit 1
fi

echo "✅ 开始精读论文..."
echo ""

# 读取模板
if [ -f "$TEMPLATE_FILE" ]; then
    cp "$TEMPLATE_FILE" "$OUTPUT_FILE"
    echo "✅ 模板已加载"
else
    echo "⚠️  模板不存在，创建基础结构"
    cat > "$OUTPUT_FILE" << 'TEMPLATE'
# 论文精读 | [论文标题]

**阅读日期**: {{DATE}}  
**论文来源**: [URL/DOI]  
**作者**: [作者列表]  
**Venue**: [会议/期刊]  
**年份**: [YYYY]

---

## 0) Executive Overview

- **研究问题**: 
- **核心想法**: 
- **主要改进**: 
- **主效果与边界**: 
- **总体判断**: 

---

## 1) Background（相关脉络与定位）

- 

---

## 2) Motivation（痛点与研究空白）

- **具体缺口**: 
- **既有方法的不足**: 

---

## 3) Claimed Contributions

| 贡献 | 一句话描述 | 证据锚点 | 可复用产出 | 原创性 | 可复用价值 |
|------|-----------|---------|-----------|--------|-----------|
| C1 | | | | | |
| C2 | | | | | |

---

## 4) Method（可落地复述）

### 4.1 核心思想


### 4.2 关键假设与前提
- 

### 4.3 形式化与目标
- 变量:
- 目标函数:
- 约束:
- 推断策略:

### 4.4 算法/流程
1. 
2. 
3. 

### 4.5 设计权衡
- 

### 4.6 失败模式
- 

---

## 5) Results（证据、效应大小与鲁棒性）

### 5.1 数据与设置
- 数据来源:
- 样本量:
- 预处理:
- 超参/硬件:

### 5.2 基线与公平性
- 

### 5.3 主要结果
| 任务 | 数据集 | 指标 | 本方法 | 最佳基线 | 增益 | 页码 |
|------|--------|------|--------|---------|------|------|
| | | | | | | |

### 5.4 消融与归因
- 

### 5.5 鲁棒与外推
- 

### 5.6 可复现性
- [ ] 代码公开
- [ ] 数据公开
- [ ] 权重公开
- 最小复现方案:

---

## 6) Limitations & Threats to Validity（批判性审视）

### 内在局限
- 

### 有效性威胁
| 威胁类型 | 描述 |
|---------|------|
| 内部威胁 | |
| 外部威胁 | |
| 构造威胁 | |
| 结论威胁 | |

### 伦理与风险
- 

---

## 7) Future Directions（未来改进方向）

1. 
2. 
3. 
4. 
5. 

---

## 8) For Busy Readers

### 3 条 Takeaway
1. 
2. 
3. 

### 复现建议
**是否建议投入复现？** 是/否  
**理由**: 

---

*阅读完成时间：{{TIME}} | 审稿人：小虾 🦐*
TEMPLATE
fi

echo ""
echo "✅ 论文精读模板已创建！"
echo "📄 文件：$OUTPUT_FILE"
echo ""
echo "📝 下一步:"
echo "   1. 打开文件填写论文信息"
echo "   2. 按照模板结构完成精读"
echo "   3. 保存到 survey/paper-deep-reading/ 文件夹"
echo ""
echo "💡 提示：可以使用 Obsidian 打开编辑，支持 Markdown 预览"
