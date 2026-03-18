# LLM/Agent 面试题目爬虫

> 自动抓取面试题目 + 生成答案 + Git 推送

---

## 📋 功能

- **自动抓取**: 牛客网、GitHub 面试题库
- **智能分类**: 基础概念、架构设计、算法优化、工程实践、前沿技术
- **答案生成**: 结构化答案 + 背景知识 + 常见追问
- **定时任务**: 每天 09:00 自动运行
- **Git 推送**: 自动 commit 并推送到 Obsidian 仓库

---

## 🚀 快速开始

### 安装依赖

```bash
cd /home/openclaw/.openclaw/workspace/skills/interview-crawler
pip install -r requirements.txt
```

### 手动测试

```bash
# 运行爬虫
python3 crawler.py

# 或使用 shell 脚本
./interview-crawler.sh
```

### 查看输出

```bash
# 面试题库目录
ls /home/openclaw/.openclaw/workspace/obsidian-repo/40-Interview/LLM 面试题库/

# 查看日志
tail -f logs/interview-crawler.log
```

---

## ⏰ 定时任务配置

```bash
# 编辑 crontab
crontab -e

# 添加每天 09:00 执行
0 9 * * * /home/openclaw/.openclaw/workspace/skills/interview-crawler/interview-crawler.sh >> /home/openclaw/.openclaw/workspace/logs/interview-crawler-cron.log 2>&1
```

---

## 📁 目录结构

```
interview-crawler/
├── crawler.py              # 主爬虫
├── processor.py            # 题目处理和答案生成
├── interview-crawler.sh    # 定时任务脚本
├── requirements.txt        # 依赖
├── sources/
│   ├── niuke.py           # 牛客网爬虫
│   └── github.py          # GitHub 爬虫
├── cache/                  # 题目缓存（去重）
└── logs/                   # 运行日志
```

---

## 📝 输出格式

```markdown
# LLM/Agent 面试题库 - 2026-03-18

> 抓取时间：2026-03-18
> 来源：牛客网、GitHub
> 本日新增：15 题

---

## 基础概念

### Q1: 请解释一下 Transformer 的 Self-Attention 机制

**难度**: ⭐⭐⭐
**来源**: 牛客网 - 字节 LLM 算法面经

#### 参考答案

**核心要点**：
1. Self-Attention 机制...
2. 位置编码...
3. 多头注意力...

**相关论文**：
- Attention Is All You Need (Vaswani et al., 2017)

**常见追问**：
- Transformer 相比 RNN 的优势？
...
```

---

## 🔧 配置

### 添加数据源

编辑 `crawler.py`，在 `keywords` 列表中添加新的搜索关键词：

```python
self.keywords = [
    "LLM 面试",
    "大模型 面试",
    "Agent 面试",
    # 添加新的关键词...
]
```

### 自定义答案模板

编辑 `processor.py` 中的 `AnswerGenerator` 类，添加新的答案模板。

---

## ⚠️ 注意事项

1. **反爬限制**: 牛客网有反爬机制，已设置请求限流
2. **答案质量**: MVP 版本使用模板答案，后续可接入 LLM API 生成
3. **去重逻辑**: 使用 MD5 哈希去重，避免重复题目
4. **Git 推送**: 需要配置 SSH 密钥

---

## 📈 后续优化

- [ ] 接入 LLM API 生成更详细的答案
- [ ] 添加知乎、小红书数据源
- [ ] 题目质量评分和过滤
- [x] 飞书通知集成 ✅
- [ ] 向量相似度去重

---

**维护**: 🦐 小虾
**最后更新**: 2026-03-18
