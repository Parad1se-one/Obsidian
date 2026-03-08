# 🔍 Search Skill - 统一搜索工具

基于 Whoogle (Google 无追踪前端) 的统一搜索解决方案。

---

## 📦 安装

无需安装，脚本已部署在：
```
/home/openclaw/.openclaw/workspace/skills/search/
```

**依赖:**
- Whoogle 容器运行中 (`docker ps | grep whoogle`)
- Python 3.8+
- requests 库 (`pip install requests`)

---

## 🚀 快速开始

### Bash 脚本

```bash
# 文本格式搜索
./skills/search/search.sh "python tutorial"

# JSON 格式
SEARCH_FORMAT=json ./skills/search/search.sh "AI news"

# 只返回 URL
./skills/search/search.sh --urls "github" 10

# 第一条结果
./skills/search/search.sh --first "weather beijing"

# 检查状态
./skills/search/search.sh --check
```

### Python 模块

```python
from search_tool import search, search_urls, search_first

# 搜索并返回结果列表
results = search("python tutorial", count=10)
for r in results:
    print(f"{r['title']}: {r['url']}")

# 只返回 URL
urls = search_urls("github", count=5)

# 第一条结果
first = search_first("weather beijing")
```

---

## 📖 API 参考

### Bash 脚本

| 选项 | 说明 |
|------|------|
| `--check` | 检查 Whoogle 状态 |
| `--urls` | 只返回 URL 列表 |
| `--first` | 只返回第一条结果 |
| `--help` | 显示帮助 |

**环境变量:**
- `WHOOGL_URL` - Whoogle 地址 (默认：`http://127.0.0.1:5000`)
- `SEARCH_FORMAT` - 输出格式：`text`|`json`|`urls` (默认：`text`)

### Python 函数

#### `search(query, count=10, timeout=30)`
搜索并返回结果列表

```python
results = search("python tutorial", count=10)
# 返回：[{'title': str, 'url': str}, ...]
```

#### `search_urls(query, count=5, timeout=30)`
搜索并返回 URL 列表

```python
urls = search_urls("github", count=5)
# 返回：['https://...', ...]
```

#### `search_first(query, timeout=30)`
返回第一条结果的 URL

```python
first = search_first("weather beijing")
# 返回：'https://...' 或 None
```

#### `search_with_snippet(query, count=10, timeout=30)`
搜索并返回包含摘要的结果

```python
results = search_with_snippet("AI news")
# 返回：[{'title': str, 'url': str, 'snippet': str}, ...]
```

---

## 🔧 集成示例

### 在 RL 研究中使用

```python
# rl-researcher/paper_search.py
from search_tool import search

def find_papers(topic):
    """搜索 RL 论文"""
    query = f"reinforcement learning {topic} paper arxiv"
    results = search(query, count=20)
    
    arxiv_papers = [r for r in results if 'arxiv' in r['url']]
    return arxiv_papers[:10]

papers = find_papers("PPO algorithm")
for p in papers:
    print(f"{p['title']}\n{p['url']}\n")
```

### 在财经日报中使用

```bash
# financial-daily/financial-daily.sh
QUERY="股票市场分析 今日"
./skills/search/search.sh --urls "$QUERY" 5 > /tmp/finance_urls.txt

# 读取 URL 并抓取内容
while read url; do
    curl -s "$url" | python3 parse_news.py
done < /tmp/finance_urls.txt
```

### 在 Heartbeat 中使用

```bash
# heartbeat/heartbeat-exec.sh
check_news() {
    local headline=$(/skills/search/search.sh --first "tech news today")
    if [ -n "$headline" ]; then
        log "📰 头条：$headline"
    fi
}
```

---

## 🛠️ 故障排除

### Whoogle 不可用

```bash
# 检查容器状态
docker ps | grep whoogle

# 重启容器
docker restart whoogle

# 查看日志
docker logs whoogle --tail 20
```

### 搜索无结果

1. 检查代理配置 (需要访问外网)
2. 尝试简化搜索关键词
3. 增加超时时间

### 代理问题

```bash
# 测试代理
curl -x "http://127.0.0.1:7890" https://www.google.com -o /dev/null -w "%{http_code}"

# 应该返回 200 或 302
```

---

## 📊 对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| **Whoogle (本方案)** | 无追踪、轻量、稳定 | 仅支持 Google |
| SearXNG | 多引擎、功能丰富 | Python 3.14 兼容性 bug |
| Brave Search API | 稳定、快速 | 需要 API Key、有配额限制 |

---

## 🔄 自动维护

已配置 Cron 任务：
```bash
*/30 * * * *  # 每 30 分钟健康检查 + 自动修复
```

**日志:** `/home/openclaw/.openclaw/workspace/logs/whoogle-maintenance.log`

---

## 📝 许可证

MIT License

---

**最后更新:** 2026-03-08
**版本:** v1.0
