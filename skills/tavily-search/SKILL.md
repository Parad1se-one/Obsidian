# Tavily Search Skill

## Overview
网络搜索技能，使用 Tavily API（专为 AI 助手设计的搜索引擎）。

## Configuration
- **API Key:** `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`
- **Endpoint:** `https://api.tavily.com/search`

## Usage

### Basic Search
```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "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",
    "query": "your search query",
    "max_results": 5
  }'
```

### Parameters
- `query` (required): 搜索关键词
- `max_results` (optional): 返回结果数，默认 5，最多 10
- `search_depth` (optional): `basic` 或 `advanced`
- `include_answer` (optional): `true` 获取 AI 生成的答案摘要
- `include_raw_content` (optional): `true` 获取完整页面内容

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
      "score": 0.99
    }
  ]
}
```

## Helper Script
```bash
#!/bin/bash
# tavily-search.sh
QUERY="$1"
MAX_RESULTS="${2:-5}"

curl -s -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"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\",
    \"query\": \"$QUERY\",
    \"max_results\": $MAX_RESULTS
  }" | jq '.results[] | {title, url, content}'
```

## Examples

### Search for templates
```bash
tavily-search "Obsidian daily note template" 5
```

### Search with answer summary
```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "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",
    "query": "enterprise agent architecture",
    "max_results": 5,
    "include_answer": true
  }'
```

## Notes
- Free tier: Limited searches per month
- Rate limit: Check API docs for current limits
- API key is development level - upgrade for production use

## Created
2026-03-05 by 小虾
