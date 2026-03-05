# 科研 Agent System 架构

**版本:** v1.0
**创建日期:** 2026-03-05
**Supervisor:** 小虾 🦐

---

## 🎯 系统目标

建立一套完整的科研自动化系统，覆盖从文献调研到论文撰写的全流程，形成逻辑闭环。

**应用场景:**
- RL 算法研究 (如 DisCoRL 知识蒸馏)
- 论文复现与改进
- 实验自动化
- 技术报告生成

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         SUPERVISOR                               │
│                         (小虾 🦐)                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  - 任务分解与分配                                         │   │
│  │  - Agent 间协调                                          │   │
│  │  - 质量把控与审核                                         │   │
│  │  - 进度跟踪与汇报                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
    ┌─────────┐         ┌─────────┐         ┌─────────┐
    │ Agent 1 │         │ Agent 2 │         │ Agent 3 │
    │Literature│        │Research │         │  Code   │
    │ 文献调研 │        │ 研究设计 │         │ 代码实现 │
    └────┬────┘         └────┬────┘         └────┬────┘
         │                   │                   │
         │ 输出：            │ 输出：            │ 输出：
         │ - 论文笔记        │ - 研究提案        │ - 可运行代码
         │ - 文献综述        │ - 实验设计        │ - 实验结果
         │ - SOTA 分析       │ - 假设定义        │ - 性能指标
         │                   │                   │
         └───────────────────┼───────────────────┘
                             ▼
                    ┌─────────────────┐
                    │    Agent 4      │
                    │   Analysis      │
                    │    结果分析     │
                    └────────┬────────┘
                             │
                             │ 输出：
                             │ - 统计分析
                             │ - 可视化图表
                             │ - 结论提炼
                             │
                             ▼
                    ┌─────────────────┐
                    │    Agent 5      │
                    │    Writing      │
                    │    论文撰写     │
                    └────────┬────────┘
                             │
                             │ 输出：
                             │ - 论文草稿
                             │ - 技术报告
                             │ - 演示文稿
                             │
                             ▼
                    ┌─────────────────┐
                    │    Git/Repo     │
                    │    知识沉淀     │
                    └─────────────────┘
                             │
                             └──────┐
                                    │
                          (反馈到 Literature)
                          新一轮研究开始
```

---

## 📋 Agent 详细设计

### Agent 1: Literature Agent (文献调研)

**职责:**
- 搜索相关论文 (arXiv, Google Scholar, etc.)
- 下载并解析 PDF
- 生成结构化笔记
- 维护文献数据库

**输入:**
- 研究主题/关键词
- 时间范围
- 目标会议/期刊

**输出:**
- `knowledge/rl/papers/<paper>-notes.md`
- `knowledge/rl/literature-review.md`
- 文献索引和标签

**工具:**
- web_search (搜索论文)
- web_fetch (获取内容)
- 文件写入

**Prompt 模板:**
```
你是 Literature Agent，负责文献调研。

任务：搜索并总结关于 {topic} 的最新研究
要求：
1. 搜索近 3 年的顶会论文 (NeurIPS, ICML, ICLR, etc.)
2. 为每篇论文创建结构化笔记
3. 提取核心方法、实验、结论
4. 识别研究空白和机会

输出格式：
- knowledge/rl/papers/{paper-name}-notes.md
- 更新 knowledge/rl/literature-review.md
```

---

### Agent 2: Research Agent (研究设计)

**职责:**
- 定义研究问题
- 提出研究假设
- 设计实验方案
- 评估可行性

**输入:**
- 文献综述
- 研究兴趣领域
- 可用资源 (算力、时间)

**输出:**
- `knowledge/rl/research/proposal-{name}.md`
- `knowledge/rl/research/experiment-design.md`
- 研究时间线

**工具:**
- 文件读写
- 逻辑推理
- 可行性分析

**Prompt 模板:**
```
你是 Research Agent，负责研究设计。

基于以下文献综述：
{literature_review}

任务：
1. 识别 2-3 个研究空白
2. 提出具体研究问题
3. 设计可验证的假设
4. 规划实验方案 (环境、基线、指标)
5. 评估资源和时间需求

输出：
- knowledge/rl/research/proposal-{name}.md
- 包含：问题、假设、方法、实验、时间线
```

---

### Agent 3: Code Agent (代码实现)

**职责:**
- 实现算法
- 搭建实验环境
- 运行实验
- 记录结果

**输入:**
- 研究提案
- 实验设计
- 基线代码 (如有)

**输出:**
- `code/{project}/{algorithm}.py`
- `code/{project}/experiments/`
- `results/{experiment}/metrics.json`

**工具:**
- exec (运行代码)
- 文件写入
- 环境配置

**Prompt 模板:**
```
你是 Code Agent，负责代码实现。

基于以下研究设计：
{experiment_design}

任务：
1. 实现核心算法 ({algorithm_name})
2. 搭建实验环境 (Gym/Gymnasium)
3. 运行对比实验 (vs 基线)
4. 记录性能指标

要求：
- 代码可运行、有注释
- 实验可复现
- 结果保存为 JSON/CSV

输出：
- code/{project}/ 目录
- results/{experiment}/ 目录
```

---

### Agent 4: Analysis Agent (结果分析)

**职责:**
- 统计分析实验结果
- 生成可视化图表
- 提炼关键发现
- 验证/证伪假设

**输入:**
- 实验结果 (metrics.json)
- 原始假设
- 基线性能

**输出:**
- `results/{experiment}/analysis.md`
- `results/{experiment}/figures/`
- 统计检验结果

**工具:**
- 数据分析 (pandas, numpy)
- 可视化 (matplotlib)
- 统计检验

**Prompt 模板:**
```
你是 Analysis Agent，负责结果分析。

基于以下实验结果：
{experiment_results}

任务：
1. 统计显著性检验 (t-test, ANOVA)
2. 生成性能对比图表
3. 分析失败案例
4. 验证/证伪研究假设
5. 提炼关键发现

输出：
- results/{experiment}/analysis.md
- 包含：统计结果、图表、结论
```

---

### Agent 5: Writing Agent (论文撰写)

**职责:**
- 撰写论文草稿
- 生成技术报告
- 准备演示材料
- 格式化参考文献

**输入:**
- 研究提案
- 实验分析
- 文献综述

**输出:**
- `papers/{paper-name}/draft.md`
- `papers/{paper-name}/figures/`
- `papers/{paper-name}/references.bib`

**工具:**
- 文件写入
- LaTeX/Markdown 格式化
- 参考文献管理

**Prompt 模板:**
```
你是 Writing Agent，负责论文撰写。

基于以下材料：
- 研究提案：{proposal}
- 实验分析：{analysis}
- 文献综述：{literature_review}

任务：
1. 撰写完整论文草稿
2. 遵循目标会议格式 (NeurIPS/ICML/ICLR)
3. 生成摘要、引言、方法、实验、结论
4. 整理参考文献

输出：
- papers/{paper-name}/draft.md
- 包含所有标准章节
```

---

## 🔄 工作流示例

### 场景：DisCoRL 知识蒸馏研究

```
1. Supervisor (小虾) 接收用户指令
   → "调研 DiscoRL，实现知识蒸馏"

2. 调用 Literature Agent
   → 搜索 DisCoRL 论文
   → 创建论文笔记
   → 输出：knowledge/rl/papers/discorl-notes.md

3. 调用 Research Agent
   → 基于文献设计研究方案
   → 输出：knowledge/rl/research/discorl-distillation-plan.md

4. 调用 Code Agent
   → 实现 DisCoRL 框架
   → 运行 CartPole 实验
   → 输出：code/rl-distillation/discorl.py + results/

5. 调用 Analysis Agent
   → 分析蒸馏效果
   → 生成性能对比图
   → 输出：results/discorl/analysis.md

6. 调用 Writing Agent
   → 撰写技术报告
   → 输出：papers/discorl-distillation/draft.md

7. Supervisor 审核并推送给用户
   → Git 提交
   → 用户汇报
```

---

## 📊 Agent 间通信协议

### 消息格式

```json
{
  "from": "supervisor",
  "to": "literature-agent",
  "task_id": "lit-001",
  "task_type": "literature_search",
  "parameters": {
    "topic": "DisCoRL knowledge distillation",
    "time_range": "2019-2026",
    "target_venues": ["NeurIPS", "ICML", "ICLR", "arXiv"]
  },
  "deadline": "30m",
  "output_path": "knowledge/rl/papers/"
}
```

### 状态跟踪

| 状态 | 说明 |
|------|------|
| PENDING | 等待执行 |
| RUNNING | 执行中 |
| COMPLETED | 完成 |
| FAILED | 失败 (需重试) |
| BLOCKED | 阻塞 (等待依赖) |

---

## 🛠️ 实现方案

### Subagent 创建

使用 `sessions_spawn` 创建专用 subagent 会话：

```python
# 示例：创建 Literature Agent
sessions_spawn(
    task="你是 Literature Agent，负责文献调研...",
    label="literature-agent",
    runtime="subagent",
    mode="session",
    cleanup="keep"
)
```

### 任务分发

使用 `sessions_send` 向 subagent 发送任务：

```python
sessions_send(
    sessionKey="literature-agent-001",
    message="搜索关于 DisCoRL 的论文..."
)
```

### 结果收集

使用 `sessions_history` 获取 subagent 输出：

```python
sessions_history(
    sessionKey="literature-agent-001",
    limit=50
)
```

---

## 📈 性能指标

| 指标 | 目标 |
|------|------|
| 文献调研速度 | 10 篇论文/小时 |
| 代码实现速度 | 1 算法/2 小时 |
| 实验运行时间 | <30 分钟/实验 |
| 论文草稿生成 | 2 小时/初稿 |
| 整体闭环时间 | 1 天/研究周期 |

---

## 🔐 安全与质量

### 质量控制

1. **Supervisor 审核** - 所有输出经 supervisor 审核
2. **质量检查** - 使用 quality-checker 评估
3. **用户确认** - 关键决策需用户确认

### 安全边界

1. **不执行危险命令** - 无 sudo、无 rm -rf
2. **不泄露敏感信息** - 不输出 API keys
3. **不修改系统文件** - 仅操作 workspace

---

## 📝 待办事项

- [ ] 创建 5 个 subagent 会话
- [ ] 实现任务分发机制
- [ ] 测试完整工作流 (DisCoRL 案例)
- [ ] 优化 Agent 间通信
- [ ] 添加进度可视化

---

**下一步:** 创建 subagent 并测试工作流

---
