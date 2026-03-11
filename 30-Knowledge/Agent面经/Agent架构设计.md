# Agent 架构设计 面经

> 更新时间：2026-03-11

---

## Q1: 介绍一下主流的 Agent 框架

**A:**

| 框架 | 核心特点 | 适用场景 |
|------|----------|----------|
| **LangChain/LangGraph** | 链式调用、状态图、工具集成 | 通用 Agent 开发 |
| **AutoGPT** | 全自主、目标驱动 | 探索性任务 |
| **MetaGPT** | 多角色协作、SOP 驱动 | 软件开发 |
| **CrewAI** | 角色定义、任务分配 | 团队协作模拟 |
| **AutoGen (Microsoft)** | 多 Agent 对话、代码执行 | 研究、数据分析 |
| **Dify** | 低代码、可视化编排 | 企业应用 |
| **Coze** | 字节跳动、插件生态 | 消费级应用 |

---

## Q2: LangChain 和 LangGraph 的区别？

**A:**

- **LangChain**: 线性链式调用，适合简单的 prompt → tool → response 流程
- **LangGraph**: 基于有向图的状态机，支持循环、条件分支、并行执行

LangGraph 核心概念：
- **State**: 全局状态对象，在节点间传递
- **Node**: 处理函数，接收 state 返回更新
- **Edge**: 节点间的连接，支持条件路由
- **Checkpoint**: 状态持久化，支持断点恢复

```python
# LangGraph 示例
graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", call_tools)
graph.add_conditional_edges("agent", should_continue, {"continue": "tools", "end": END})
graph.add_edge("tools", "agent")
```

**面试加分点**: LangGraph 解决了 LangChain 的"链式调用不够灵活"问题，特别是需要循环推理的场景

---

## Q3: 如何设计一个 RAG + Agent 系统？

**A:** RAG-Agent 混合架构：

```
用户查询 → Agent 规划 → 判断是否需要检索
                          ├── 需要 → RAG Pipeline → 检索 → 重排 → 生成
                          ├── 需要工具 → Tool Calling → 执行 → 返回结果
                          └── 直接回答 → LLM 生成
```

**关键设计决策**:
1. **检索策略**: 语义检索 vs 关键词检索 vs 混合检索
2. **Chunk 策略**: 固定大小 vs 语义分割 vs 递归分割
3. **重排序**: Cross-encoder reranker (Cohere, BGE-reranker)
4. **Agent 路由**: 根据查询类型选择不同的处理管道
5. **Self-RAG**: Agent 自己判断检索结果是否足够，不够则重新检索

---

## Q4: 什么是 MCP (Model Context Protocol)？

**A:** MCP 是 Anthropic 提出的开放协议，标准化 LLM 与外部工具/数据源的连接方式。

**核心概念**:
- **MCP Server**: 提供工具和资源的服务端
- **MCP Client**: LLM 应用端，调用 MCP Server
- **Resources**: 数据源（文件、数据库、API）
- **Tools**: 可执行的操作
- **Prompts**: 预定义的提示模板

**优势**:
- 统一接口，一次开发多处复用
- 解耦 LLM 应用和工具实现
- 支持本地和远程工具

**类比**: MCP 之于 AI Agent，就像 USB 之于外设 — 标准化的连接协议

---

## Q5: Agent 的安全性如何保障？

**A:** Agent 安全是核心问题，主要风险和对策：

**风险**:
1. **Prompt Injection**: 恶意输入劫持 Agent 行为
2. **工具滥用**: Agent 执行危险操作（删除文件、发送邮件）
3. **数据泄露**: Agent 暴露敏感信息
4. **权限提升**: Agent 获取超出预期的系统权限

**对策**:
1. **沙箱执行**: 代码在隔离环境中运行
2. **权限最小化**: Agent 只能访问必要的工具和数据
3. **Human-in-the-Loop**: 高风险操作需要人类确认
4. **输入过滤**: 检测和过滤 prompt injection
5. **输出审计**: 记录所有 Agent 操作，支持回溯
6. **红线机制**: 定义不可逾越的安全边界（如不能执行 `rm -rf /`）

---

## Q6: 如何处理 Agent 的错误恢复？

**A:** Agent 错误恢复策略：

1. **重试机制**: 工具调用失败时自动重试（指数退避）
2. **降级策略**: 主工具不可用时切换到备选方案
3. **Self-Correction**: Agent 检测到错误后自我修正
4. **Checkpoint/Resume**: 保存中间状态，从断点恢复
5. **Escalation**: 无法自行解决时上报给人类

```python
# 错误恢复伪代码
for attempt in range(max_retries):
    try:
        result = agent.execute(task)
        if agent.validate(result):
            return result
        else:
            agent.reflect_and_correct()
    except ToolError:
        agent.switch_to_fallback_tool()
    except Exception:
        agent.escalate_to_human()
```

---

## Q7: 什么是 Agent 的 Planning 能力？有哪些实现方式？

**A:** Planning 是 Agent 将复杂任务分解为可执行子任务的能力。

**实现方式**:

1. **Chain-of-Thought (CoT)**: 逐步推理，但不显式分解任务
2. **Task Decomposition**: 显式将任务拆分为子任务列表
3. **Tree of Thoughts (ToT)**: 探索多条推理路径，选择最优
4. **Plan-and-Execute**: 先生成完整计划，再逐步执行
5. **Reflexion**: 执行后反思，动态调整计划

**Plan-and-Execute 模式**:
```
Step 1: Planner 生成任务计划 [T1, T2, T3, T4]
Step 2: Executor 执行 T1 → 获得结果 R1
Step 3: Replanner 根据 R1 调整后续计划
Step 4: 重复直到完成
```

**面试加分点**: 提到 LATS (Language Agent Tree Search)，结合 MCTS 和 LLM 的规划方法

---

## Q8: 如何优化 Agent 的延迟和成本？

**A:**

**延迟优化**:
1. **并行工具调用**: 无依赖的工具调用并行执行
2. **流式输出**: 边生成边返回
3. **缓存**: 相同查询/工具调用结果缓存
4. **小模型路由**: 简单任务用小模型，复杂任务用大模型
5. **预测性执行**: 预判下一步可能需要的工具，提前调用

**成本优化**:
1. **Prompt 压缩**: 减少不必要的上下文
2. **模型分级**: 规划用大模型，执行用小模型
3. **批处理**: 合并多个 LLM 调用
4. **本地模型**: 非关键任务用本地部署的开源模型
5. **记忆摘要**: 定期压缩对话历史，减少 token 消耗

---
