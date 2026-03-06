# 小虾的技能工具箱 🦐

这是我（赛博龙虾）安装的自定义技能集合。每个技能都符合我的人设：**暴躁但靠谱**。

## 已安装技能

### 🔍 Tavily Search (`tavily-search/`)
**用途：** 网络搜索  
**状态：** ✅ 已激活  
**API：** Tavily (dev key 配置完成)

```bash
./tavily-search.sh "搜索关键词" [结果数量]
```

---

### 📰 Financial Daily Reporter (`financial-daily/`) ⭐ NEWEST
**用途：** 自动生成财经日报，每天早上 7:30 推送  
**状态：** 🚀 MVP 就绪，需配置 API Key  
**推送位置：** `daily/financial-news/`

```bash
# 手动生成
./financial-daily.sh

# 设置定时任务（只需一次）
./setup-cron.sh
```

**适用场景：**
- 每日财经新闻摘要
- 市场动态追踪
- 投资决策参考

---

### 📚 Paper Deep Reader (`paper-deep-reader/`) ⭐ NEWEST
**用途：** 学术论文深度阅读，按照"跨学科教授与顶级期刊审稿人"框架输出  
**状态：** 🚀 MVP 就绪  
**输出位置：** `survey/paper-deep-reading/`

```bash
# 创建精读报告
./paper-deep-reader.sh /path/to/paper.pdf "论文简称"

# 输出位置
# survey/paper-deep-reading/论文简称.md
```

**适用场景：**
- 论文精读与复现评估
- 文献综述撰写
- 组会报告准备
- 批判性论文审查

**输出框架:** 8 模块结构化分析（Executive Overview → Method → Results → Limitations → Future Directions）

---

### 🧩 Task Decomposer (`task-decomposer/`)
**用途：** 把复杂任务拆成可执行的小步骤  
**状态：** 📦 已创建，待集成  
**风格：** "别跟我说你要做 XXX，告诉我第一步是什么"

```
拆解任务：完成年度技术分享
截止：2 周后
```

**适用场景：**
- 大项目拆解
- 拖延症治疗
- 进度追踪

---

### 📊 Daily Summary (`daily-summary/`)
**用途：** 自动生成每日/每周工作摘要  
**状态：** 📦 已创建，待集成  
**风格：** "今天干了啥？我帮你记着呢"

```
生成今日摘要
生成周报
```

**适用场景：**
- 日报自动生成
- 周报统计
- 工作总结

---

### 🧠 Memory Curator (`memory-curator/`)
**用途：** 记忆管理、归档、检索  
**状态：** 📦 已创建，待集成  
**风格：** "你说过的事我都记着，别想赖账"

```
记住：用户偏好早上开会
搜索记忆：GitHub 配置
```

**适用场景：**
- 重要信息存储
- 快速检索
- 记忆整理

---

### 📝 Git Auto Review (`git-auto-review/`)
**用途：** 代码审查、PR 分析  
**状态：** 📦 已创建，待集成  
**风格：** 犀利直接，指出问题不废话

```bash
git diff --cached | ./git-review.sh
```

**适用场景：**
- PR 审查
- Commit 前检查
- 代码质量评估

---

### 📊 Project Analyzer (`project-analyzer/`)
**用途：** 项目结构分析、技术栈识别  
**状态：** 📦 已创建，待集成  
**风格：** 一眼看穿你的烂项目

```bash
./project-analyzer.sh /path/to/project
```

**适用场景：**
- 新项目上手
- 代码库审计
- 技术文档生成

---

### ✅ Task Master (`task-master/`)
**用途：** 任务管理、日程安排、习惯追踪  
**状态：** 📦 已创建，待集成  
**风格：** 比你妈还唠叨你的待办事项

```bash
./task-master.sh {add|list|complete|summary}
```

**适用场景：**
- 日常任务管理
- 截止日期提醒
- 习惯养成追踪

---

## 技能目录结构

```
skills/
├── tavily-search/        # ✅ 网络搜索 (已激活)
│   ├── SKILL.md
│   └── tavily-search.sh
├── financial-daily/      # 🚀 财经日报 (MVP READY)
│   ├── SKILL.md
│   ├── financial-daily.sh
│   ├── setup-cron.sh
│   ├── collectors/
│   ├── templates/
│   └── config/
├── paper-deep-reader/    # 🚀 论文精读 (MVP READY)
│   ├── SKILL.md
│   ├── paper-deep-reader.sh
│   └── templates/
├── task-decomposer/      # 📦 任务拆解
│   └── SKILL.md
├── daily-summary/        # 📦 每日摘要
│   └── SKILL.md
├── memory-curator/       # 📦 记忆管理
│   └── SKILL.md
├── git-auto-review/      # 📦 代码审查
│   └── SKILL.md
├── project-analyzer/     # 📦 项目分析
│   └── SKILL.md
└── task-master/          # 📦 任务管理
    └── SKILL.md
```

---

## 使用指南

### 激活技能
技能创建后需要在 OpenClaw 配置中注册才能使用。

### 技能开发规范
每个技能包含：
- `SKILL.md` - 技能说明文档
- 可选的脚本文件
- 必要的配置文件

### 人设要求
所有技能的输出风格必须保持一致：
- 直接、不废话
- 可以有吐槽，但要有建设性
- 专业但不高冷
- 偶尔用 🦐 emoji

---

## 待开发技能

- [ ] Calendar Integration (日历集成)
- [ ] Email Summarizer (邮件摘要)
- [ ] Meeting Notes Auto-generator (会议纪要生成)
- [ ] Security Auditor (安全审计)

---

*最后更新：2026-03-05 by 小虾*
