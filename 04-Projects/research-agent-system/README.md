# 科研 Agent System 使用指南

**版本:** v1.0
**创建日期:** 2026-03-05
**Supervisor:** 小虾 🦐

---

## 🚀 快速开始

### 1. 启动系统

```bash
cd projects/research-agent-system
./supervisor.sh full "DisCoRL knowledge distillation"
```

### 2. 查看状态

```bash
./supervisor.sh status
```

### 3. 单独调用 Agent

```bash
# 文献调研
./supervisor.sh literature "RL distillation"

# 研究设计
./supervisor.sh research

# 代码实现
./supervisor.sh code

# 运行实验
./supervisor.sh experiment

# 结果分析
./supervisor.sh analysis

# 论文撰写
./supervisor.sh writing
```

---

## 📋 Agent 列表

| Agent | 职责 | 输出 |
|-------|------|------|
| **Literature Agent** | 文献搜索、阅读、总结 | knowledge/rl/papers/ |
| **Research Agent** | 研究问题定义、实验设计 | knowledge/rl/research/ |
| **Code Agent** | 算法实现、实验运行 | code/ + results/ |
| **Analysis Agent** | 统计分析、可视化 | results/*/analysis.md |
| **Writing Agent** | 论文撰写、报告生成 | papers/*/draft.md |

---

## 🔄 工作流

```
用户指令
   ↓
Supervisor (小虾)
   ↓
┌──────────────────────────────────────┐
│ 1. Literature Agent → 文献调研       │
│    输出：论文笔记、文献综述          │
└────────────────┬─────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│ 2. Research Agent → 研究设计         │
│    输出：研究提案、实验设计          │
└────────────────┬─────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│ 3. Code Agent → 代码实现             │
│    输出：算法代码、实验结果          │
└────────────────┬─────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│ 4. Analysis Agent → 结果分析         │
│    输出：统计报告、可视化图表        │
└────────────────┬─────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│ 5. Writing Agent → 论文撰写          │
│    输出：论文草稿、技术报告          │
└────────────────┬─────────────────────┘
                 ↓
Git 提交 + 用户汇报
```

---

## 📁 目录结构

```
obsidian-repo/
├── knowledge/
│   ├── rl/
│   │   ├── papers/           # Literature Agent 输出
│   │   ├── research/         # Research Agent 输出
│   │   └── literature-review.md
│   └── KNOWLEDGE-INDEX.md
├── code/
│   └── rl-distillation/      # Code Agent 输出
├── results/
│   └── discorl/              # Analysis Agent 输出
├── papers/
│   └── discorl-distillation/ # Writing Agent 输出
└── projects/
    └── research-agent-system/
        ├── ARCHITECTURE.md
        ├── README.md
        └── supervisor.sh
```

---

## 🎯 使用示例

### 示例 1: 完整研究 DisCoRL 知识蒸馏

```bash
# 启动完整流程
./supervisor.sh full "DisCoRL knowledge distillation"

# 预计输出:
# - knowledge/rl/papers/discorl-notes.md
# - knowledge/rl/research/discorl-proposal.md
# - code/rl-distillation/discorl-cartpole.py
# - results/discorl/analysis.md
# - papers/discorl-distillation/draft.md
```

### 示例 2: 仅文献调研

```bash
./supervisor.sh literature "world model reinforcement learning"

# 预计输出:
# - knowledge/rl/papers/world-models-notes.md
# - knowledge/rl/papers/muzero-notes.md
# - knowledge/rl/literature-review.md
```

### 示例 3: 仅代码实现

```bash
./supervisor.sh code

# 预计输出:
# - code/rl-distillation/*.py
# - results/*/metrics.json
```

---

## 📊 性能指标

| 阶段 | 预计时间 | 输出质量 |
|------|----------|----------|
| 文献调研 | 30 分钟 | 5-10 篇论文笔记 |
| 研究设计 | 20 分钟 | 完整研究提案 |
| 代码实现 | 60 分钟 | 可运行代码 |
| 实验运行 | 30 分钟 | 性能指标 |
| 结果分析 | 20 分钟 | 统计报告 |
| 论文撰写 | 40 分钟 | 完整草稿 |
| **总计** | **~3.5 小时** | **完整研究周期** |

---

## 🔧 配置选项

### 环境变量

```bash
export AGENT_SYSTEM_LOG_LEVEL=debug  # debug, info, warn, error
export AGENT_SYSTEM_TIMEOUT=300      # 每个 Agent 超时时间 (秒)
export AGENT_SYSTEM_MAX_RETRIES=3    # 失败重试次数
```

### 自定义 Agent

在 `agents/` 目录添加新 Agent:

```bash
agents/
├── literature-agent.sh
├── research-agent.sh
├── code-agent.sh
├── analysis-agent.sh
├── writing-agent.sh
└── custom-agent.sh  # 自定义
```

---

## 🐛 故障排除

### 问题 1: Agent 无响应

```bash
# 检查 Agent 状态
./supervisor.sh status

# 重启特定 Agent
# (等待当前任务超时或手动终止)
```

### 问题 2: 输出质量不佳

```bash
# 增加 Agent 思考时间
export AGENT_SYSTEM_TIMEOUT=600

# 或手动审查输出后重试
```

### 问题 3: Git 冲突

```bash
cd obsidian-repo
git status
git merge origin/main
# 解决冲突后继续
```

---

## 📝 最佳实践

1. **明确研究主题** - 给 Supervisor 清晰的研究方向
2. **阶段性审查** - 每个阶段完成后检查输出质量
3. **及时 Git 提交** - 避免数据丢失
4. **复用已有成果** - 检查 knowledge/ 目录避免重复工作
5. **反馈优化** - 根据输出质量调整 Agent 参数

---

## 🦐 小虾提示

**这个系统的核心优势:**

1. ✅ **自动化** - 减少重复劳动
2. ✅ **标准化** - 统一输出格式
3. ✅ **可追溯** - 完整研究记录
4. ✅ **可扩展** - 轻松添加新 Agent

**但记住:**

- AI 是助手，不是替代者
- 关键决策仍需人类判断
- 质量把控最重要
- 保持批判性思维

---

**最后更新:** 2026-03-05
**维护者:** 小虾 🦐
