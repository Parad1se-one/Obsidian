# Agent 前沿话题 面经

> 更新时间：2026-03-11

---

## Q1: 什么是 Agentic RAG？和传统 RAG 有什么区别？

**A:** Agentic RAG 是将 Agent 能力融入 RAG 流程，让检索过程更智能。

**传统 RAG**: Query → Retrieve → Generate (固定流程)
**Agentic RAG**: Query → Agent 判断 → 多轮检索/工具调用 → 验证 → Generate

**核心区别**:
- **自适应检索**: Agent 决定是否需要检索、检索什么、检索几次
- **查询改写**: Agent 自动优化检索 query
- **多源融合**: Agent 从多个数据源检索并融合
- **结果验证**: Agent 检查检索结果是否充分，不够则继续检索

**代表工作**: Self-RAG, CRAG (Corrective RAG), Adaptive RAG

---

## Q2: 什么是 Agent 的 Reflection 和 Self-Correction？

**A:**

**Reflection**: Agent 回顾自己的行为和结果，总结经验教训
**Self-Correction**: Agent 检测到错误后自主修正

**Reflexion 框架** (Shinn et al., 2023):
```
Episode 1: 执行任务 → 失败
Reflection: "我忘记了检查边界条件"
Episode 2: 执行任务 (带反思经验) → 成功
```

**实现方式**:
1. **输出验证**: 用规则或另一个 LLM 检查输出
2. **自我批评**: 让 Agent 评价自己的回答
3. **对比学习**: 对比成功和失败的案例
4. **经验存储**: 将反思结果存入长期记忆

---

## Q3: Code Agent 是什么？有哪些代表性工作？

**A:** Code Agent 是专门用于编程任务的 Agent，能够理解代码、编写代码、调试代码。

**代表性工作**:
| 系统 | 特点 |
|------|------|
| **Devin (Cognition)** | 全栈软件工程 Agent |
| **SWE-Agent** | 基于 SWE-bench 的代码修复 Agent |
| **Cursor** | IDE 集成的 AI 编程助手 |
| **Kiro** | AWS 的 AI IDE |
| **Codex CLI** | OpenAI 的命令行编程 Agent |
| **Claude Code** | Anthropic 的终端编程 Agent |

**核心能力**:
- 代码理解和导航
- Bug 定位和修复
- 测试生成
- 代码重构
- 多文件编辑

**面试加分点**: 提到 SWE-bench 排行榜、代码 Agent 的沙箱安全机制

---

## Q4: 什么是 Agent 的 Tool Learning？

**A:** Tool Learning 是让 Agent 学会使用新工具的能力，而不是硬编码工具列表。

**三个层次**:
1. **Tool Selection**: 从已有工具中选择合适的
2. **Tool Creation**: Agent 自己创建新工具（写代码）
3. **Tool Composition**: 组合多个工具完成复杂任务

**Toolformer** (Schick et al., 2023):
- 训练模型自主决定何时、如何调用工具
- 通过自监督学习，模型学会在文本中插入 API 调用

**LATM** (Large Language Models as Tool Makers):
- LLM 先创建工具（Python 函数）
- 然后用小模型调用这些工具
- 降低推理成本

---

## Q5: Agent 在企业落地的主要挑战？

**A:**

1. **可靠性**: Agent 的输出不够稳定，同样的输入可能产生不同结果
2. **安全合规**: 企业数据安全、隐私保护、审计要求
3. **成本**: LLM API 调用成本高，大规模部署昂贵
4. **延迟**: 多步推理导致响应时间长
5. **可解释性**: 决策过程难以向业务方解释
6. **集成复杂度**: 与现有系统的集成成本高
7. **评估困难**: 缺乏标准化的评估方法

**解决思路**:
- 渐进式落地：从简单场景开始，逐步扩展
- 人机协作：Agent 辅助人类，而非完全替代
- 本地部署：敏感数据使用本地模型
- 标准化：采用 MCP 等标准协议降低集成成本

---

## Q6: 什么是 Agent 的 World Model？

**A:** World Model 是 Agent 对环境的内部表示，用于预测行动的后果。

**在 LLM Agent 中的体现**:
- LLM 本身就是一个隐式的 World Model
- 通过训练数据学到了世界知识
- 可以"想象"行动的结果（mental simulation）

**显式 World Model**:
- 环境模拟器：Agent 在模拟环境中试错
- 状态转移模型：预测 action → next_state
- 用于 planning：在 World Model 中搜索最优策略

**与 RL 的关系**:
- Model-based RL 使用 World Model 进行规划
- Dreamer、IRIS 等算法在学习的 World Model 中训练策略
- LLM Agent 可以看作是用语言作为 World Model 的 planning

---

## Q7: Agent 和 Workflow 的区别？什么时候用 Agent，什么时候用 Workflow？

**A:**

| 维度 | Workflow | Agent |
|------|----------|-------|
| 执行路径 | 预定义、确定性 | 动态、自适应 |
| 灵活性 | 低 | 高 |
| 可预测性 | 高 | 低 |
| 调试难度 | 低 | 高 |
| 适用场景 | 流程固定的任务 | 开放性任务 |

**选择建议**:
- **用 Workflow**: 流程明确、步骤固定、需要高可靠性（如审批流程、数据 ETL）
- **用 Agent**: 任务开放、需要灵活决策、步骤不确定（如研究、创意、问题排查）
- **混合**: Workflow 中嵌入 Agent 节点，兼顾可靠性和灵活性

**Anthropic 的建议**: "Start with workflows, add agents where needed"

---

## Q8: 2025-2026 年 Agent 领域的最新趋势？

**A:**

1. **Computer Use Agent**: Claude Computer Use、Operator — Agent 直接操作电脑
2. **MCP 生态爆发**: 标准化工具协议，工具市场兴起
3. **Agent OS**: OpenClaw、Claude Desktop — Agent 作为操作系统层
4. **多模态 Agent**: 视觉 + 语言 + 代码的融合
5. **Agent 安全**: 红队测试、沙箱隔离、权限管理成为标配
6. **小模型 Agent**: 用 7B/14B 模型跑 Agent，降低成本
7. **Agent 评估标准化**: 更多 benchmark 和评估框架
8. **垂直领域 Agent**: 金融、医疗、法律等专业 Agent

---
