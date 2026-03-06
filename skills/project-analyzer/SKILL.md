# Project Analyzer Skill

## Overview
快速分析代码库结构、依赖关系、技术栈。帮你在新项目里不迷路。

**人设：** 赛博龙虾 🦐 - 一眼看穿你的烂项目结构

## Capabilities

### 1. 项目结构分析
- 扫描目录结构
- 识别主要模块/组件
- 生成可视化结构图

### 2. 技术栈识别
- 检测编程语言
- 识别框架和库
- 分析依赖关系

### 3. 代码质量评估
- 统计代码行数
- 识别复杂度过高的文件
- 检测重复代码

### 4. 文档检查
- 检查 README 完整性
- 识别缺失的文档
- 建议改进点

## Usage

### 分析当前目录
```bash
./project-analyzer.sh
```

### 分析指定目录
```bash
./project-analyzer.sh /path/to/project
```

### 深度分析
```bash
./project-analyzer.sh --deep /path/to/project
```

## Output Format

```markdown
## 🦐 项目分析报告

### 📁 项目结构
```
project/
├── src/          # 主要源代码
├── tests/        # 测试文件
├── docs/         # 文档
└── config/       # 配置文件
```

### 🛠 技术栈
- **语言:** Python 3.11, JavaScript
- **框架:** FastAPI, React
- **数据库:** PostgreSQL
- **依赖:** 47 个包 (3 个过时)

### 📊 代码统计
- 总行数：12,450
- 文件数：89
- 平均复杂度：中等

### ⚠️ 注意事项
- `src/legacy/` - 这玩意儿为什么还在？
- 测试覆盖率 23% - 你管这叫测试？

### 💡 建议
1. 更新过时的依赖
2. 增加测试覆盖率
3. 清理 legacy 代码
```

## Script Implementation

```bash
#!/bin/bash
# project-analyzer.sh

PROJECT_DIR="${1:-.}"

echo "🦐 让我看看这是什么项目..."

# Count files by type
echo "### 文件统计"
find "$PROJECT_DIR" -type f -name "*.py" | wc -l | xargs echo "Python 文件:"
find "$PROJECT_DIR" -type f -name "*.js" | wc -l | xargs echo "JavaScript 文件:"
find "$PROJECT_DIR" -type f -name "*.ts" | wc -l | xargs echo "TypeScript 文件:"

# Check for package files
if [ -f "$PROJECT_DIR/package.json" ]; then
    echo "✅ Node.js 项目 (package.json 存在)"
fi

if [ -f "$PROJECT_DIR/requirements.txt" ] || [ -f "$PROJECT_DIR/pyproject.toml" ]; then
    echo "✅ Python 项目 (requirements 存在)"
fi

if [ -f "$PROJECT_DIR/README.md" ]; then
    echo "✅ 有 README"
else
    echo "⚠️ 没有 README？认真的吗？"
fi

# Send full analysis to LLM
echo ""
echo "详细分析中..."
# ... (send to OpenClaw for LLM analysis)
```

## Integration with OpenClaw

```bash
# In OpenClaw session
openclaw ask "Analyze this project structure: $(tree -L 2)"
```

## Example Analysis Output

```markdown
## 🦐 项目分析报告：Obsidian Knowledge Base

### 📁 项目结构
```
Obsidian/
├── daily/          # 日常记录
│   └── work/       # 工作相关
├── projects/       # 项目文档
├── resources/      # 参考资料
├── templates/      # 模板文件
└── .obsidian/      # Obsidian 配置
```

### 🛠 技术栈
- **格式:** Markdown
- **工具:** Obsidian
- **同步:** Git + GitHub

### 📊 统计
- 文件夹：6 个
- 模板：1 个
- 配置：完整

### ⚠️ 注意事项
- 暂无明显问题

### 💡 建议
1. 考虑添加索引文件
2. 可以加个标签系统说明
```

## Created
2026-03-05 by 小虾
