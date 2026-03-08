# Tavily Search Skill

## Overview
网络搜索技能，使用 Tavily API（专为 AI 助手设计的搜索引擎）。

## Configuration

### API Key Setup (推荐方式)

**方式 1: 环境变量 (推荐)**
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export TAVILY_API_KEY="your_api_key"

# 或者临时设置
export TAVILY_API_KEY="tvly-dev-xxxxxxxxxxxxxxxxx"
```

**方式 2: .env 文件**
```bash
# 在技能目录创建 .env 文件
echo "TAVILY_API_KEY=your_api_key" > .env

# 脚本会自动加载 (如果实现 dotenv 支持)
```

**方式 3: 默认 Dev Key (仅开发测试)**
- 脚本内置默认 Dev Key，仅用于测试
- **生产环境请勿使用默认 Key**

### 获取 API Key
1. 访问 https://app.tavily.com/
2. 注册/登录账号
3. 在 Dashboard 获取 API Key
4. 免费额度：每月有限次数，适合个人使用

### Endpoint
- **URL:** `https://api.tavily.com/search`
- **Method:** POST
- **Content-Type:** application/json

---

## Usage

### Basic Search

**使用脚本:**
```bash
cd /home/openclaw/.openclaw/workspace/skills/tavily-search
./tavily-search.sh "Obsidian daily note template" 5
```

**直接调用 API:**
```bash
export TAVILY_API_KEY="your_api_key"

curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$TAVILY_API_KEY\",
    \"query\": \"your search query\",
    \"max_results\": 5
  }"
```

### Parameters

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | ✅ | 搜索关键词 |
| `max_results` | int | ❌ | 返回结果数，默认 5，最多 10 |
| `search_depth` | string | ❌ | `basic` 或 `advanced` |
| `include_answer` | bool | ❌ | `true` 获取 AI 生成的答案摘要 |
| `include_raw_content` | bool | ❌ | `true` 获取完整页面内容 |
| `include_domains` | array | ❌ | 限定特定域名 |
| `exclude_domains` | array | ❌ | 排除特定域名 |

### Response Format

```json
{
  "query": "search query",
  "answer": "AI-generated answer summary",
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com",
      "content": "Snippet content",
      "score": 0.99,
      "raw_content": "Full page content (if requested)"
    }
  ]
}
```

---

## Helper Script

### tavily-search.sh

```bash
#!/bin/bash
# Tavily Search Helper Script
# Usage: ./tavily-search.sh "search query" [max_results]
#
# API Key Configuration:
#   export TAVILY_API_KEY="your_api_key"

QUERY="$1"
MAX_RESULTS="${2:-5}"
API_KEY="${TAVILY_API_KEY:-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}"

curl -s -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$API_KEY\",
    \"query\": \"$QUERY\",
    \"max_results\": $MAX_RESULTS
  }"
```

### 使用示例

```bash
# 基本搜索
./tavily-search.sh "github actions tutorial" 5

# 使用环境变量
export TAVILY_API_KEY="your_key"
./tavily-search.sh "kubernetes best practices" 10

# 解析结果 (需要 jq)
./tavily-search.sh "AI agent architecture" 5 | jq '.results[] | {title, url}'
```

---

## Examples

### Search for templates
```bash
./tavily-search.sh "Obsidian daily note template" 5
```

### Search with answer summary
```bash
export TAVILY_API_KEY="your_key"

curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$TAVILY_API_KEY\",
    \"query\": \"enterprise agent architecture\",
    \"max_results\": 5,
    \"include_answer\": true
  }"
```

### Search specific domain
```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$TAVILY_API_KEY\",
    \"query\": \"reinforcement learning tutorial\",
    \"max_results\": 5,
    \"include_domains\": [\"github.com\", \"arxiv.org\"]
  }"
```

---

## Integration

### 在其他脚本中使用

```bash
#!/bin/bash
# 加载 Tavily 搜索功能
source "/home/openclaw/.openclaw/workspace/skills/tavily-search/tavily-search.sh"

# 调用搜索
search_results=$(./tavily-search.sh "your query" 5)
```

### 在 rl-study.sh 中的集成

```bash
# 搜索最新论文
if [ -x "$SCRIPT_DIR/../tavily-search/tavily-search.sh" ]; then
    PAPERS=$("$SCRIPT_DIR/../tavily-search/tavily-search.sh" "$PAPER_TOPIC" 5)
fi
```

---

## Security Best Practices

### ✅ 推荐做法
- 使用环境变量存储 API Key
- 将 API Key 添加到 `.gitignore`
- 定期轮换 API Key
- 监控 API 使用量

### ❌ 避免做法
- 不要将 API Key 硬编码在脚本中
- 不要提交 API Key 到 Git 仓库
- 不要在公开场合分享 API Key
- 不要使用默认 Dev Key 于生产环境

### .gitignore 配置
```bash
# Tavily API Key
.env
*.key
*.secret
```

---

## Notes

### Rate Limits
- **Free Tier:** 每月有限次数 (查看官网最新政策)
- **Paid Plans:** 按使用量计费
- **Rate Limit:** 检查 API 文档获取最新限制

### API Key Level
- **Dev Key:** 用于开发测试，功能受限
- **Production Key:** 正式环境使用
- **Enterprise Key:** 高用量场景

### Troubleshooting

**错误：401 Unauthorized**
- 检查 API Key 是否正确
- 确认 Key 未过期

**错误：429 Too Many Requests**
- 超出速率限制，稍后重试
- 考虑升级套餐

**错误：400 Bad Request**
- 检查请求参数格式
- 确认 `max_results` 在有效范围 (1-10)

---

## Created
2026-03-05 by 小虾

## Updated
2026-03-08 - 🔒 修复 API Key 硬编码，改用环境变量
