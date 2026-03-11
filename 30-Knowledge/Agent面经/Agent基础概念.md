# Agent 基础概念 面经

> 更新时间：2026-03-11

---

## Q1: 什么是 AI Agent？和传统 Chatbot 有什么区别？

**A:** AI Agent 是一个能够感知环境、自主决策并执行行动的智能系统。与传统 Chatbot 的核心区别：

| 维度 | Chatbot | AI Agent |
|------|---------|----------|
| 交互模式 | 单轮/多轮对话 | 自主规划 + 多步执行 |
| 工具使用 | 无或有限 | 可调用外部工具、API |
| 记忆 | 上下文窗口内 | 短期 + 长期记忆 |
| 决策 | 被动响应 | 主动规划、分解任务 |
| 环境感知 | 仅文本输入 | 多模态感知 + 环境反馈 |

Agent 的核心能力：**感知 (Perception) → 规划 (Planning) → 行动 (Action) → 反思 (Reflection)**

---

## Q2: Agent 的核心组件有哪些？

**A:** 经典的 Agent 架构包含 4 个核心组件：

1. **LLM 大脑 (Brain)**: 负责推理、规划、决策。通常是 GPT-4、Claude 等大模型
2. **记忆系统 (Memory)**:
   - 短期记忆：对话上下文、工作记忆
   - 长期记忆：向量数据库存储的历史经验
3. **工具使用 (Tool Use)**: 调用外部 API、代码执行、搜索引擎等
4. **规划模块 (Planning)**: 任务分解、子目标设定、执行路径规划

参考框架：LangChain Agent、AutoGPT、BabyAGI、MetaGPT

---

## Q3: 解释一下 ReAct 框架

**A:** ReAct (Reasoning + Acting) 是 Yao et al. (2022) 提出的 Agent 推理框架，核心思想是交替进行推理和行动：

```
Thought: 我需要查找今天的天气
Action: search("北京今天天气")
Observation: 北京今天晴，25°C
Thought: 已经获取到天气信息，可以回答用户了
Action: finish("北京今天晴，气温25°C")
```

**优势**:
- 推理过程可解释
- 可以根据观察结果动态调整策略
- 减少幻觉（通过外部工具验证）

**局限**:
- 每步都需要 LLM 调用，延迟高
- 推理链过长时容易偏离目标

---

## Q4: Function Calling 和 Tool Use 的区别？

**A:** 本质上是同一件事的不同实现方式：

- **Function Calling**: OpenAI 提出的标准化接口，模型输出结构化的函数调用 JSON，由系统执行
- **Tool Use**: 更广义的概念，包括 Function Calling、代码执行、API 调用等

Function Calling 的流程：
1. 系统提供可用函数的 schema (名称、参数、描述)
2. 模型根据用户意图选择函数并生成参数
3. 系统执行函数，将结果返回给模型
4. 模型基于结果生成最终回答

**面试加分点**: 提到 Anthropic 的 Tool Use、Google 的 Function Calling、以及 MCP (Model Context Protocol) 标准化工具调用协议

---

## Q5: 什么是 Agent 的幻觉问题？如何缓解？

**A:** Agent 幻觉指模型生成不存在的工具调用、错误的参数、或虚构的执行结果。

**缓解策略**:
1. **工具 Schema 约束**: 严格定义可用工具和参数类型
2. **输出验证**: 对模型输出做 JSON Schema 校验
3. **Grounding**: 用 RAG 检索真实数据，减少凭空生成
4. **Self-Reflection**: 让 Agent 检查自己的输出是否合理
5. **Human-in-the-Loop**: 关键操作需要人类确认
6. **Few-shot Examples**: 提供正确的工具调用示例

---

## Q6: 单 Agent vs 多 Agent 系统的优劣？

**A:**

| 维度 | 单 Agent | 多 Agent |
|------|----------|----------|
| 复杂度 | 低 | 高 |
| 适用场景 | 简单任务 | 复杂协作任务 |
| 可扩展性 | 差 | 好 |
| 错误传播 | 局部 | 可能级联 |
| 代表框架 | ReAct, AutoGPT | MetaGPT, CrewAI, AutoGen |

**多 Agent 典型架构**:
- **层级式**: Manager Agent 分配任务给 Worker Agent
- **对等式**: Agent 之间平等协作、讨论
- **流水线式**: Agent 按顺序处理，前一个的输出是后一个的输入

---

## Q7: 什么是 Agent 的记忆机制？如何实现长期记忆？

**A:** Agent 记忆分三层：

1. **感知记忆 (Sensory)**: 当前输入的原始信息
2. **工作记忆 (Working)**: 对话上下文窗口，受 token 限制
3. **长期记忆 (Long-term)**: 持久化存储的历史经验

**长期记忆实现方案**:
- **向量数据库**: 将对话/经验 embedding 后存入 Chroma/Pinecone/Milvus
- **知识图谱**: 结构化存储实体关系
- **摘要压缩**: 定期将对话摘要存储，减少 token 消耗
- **MemGPT**: 模拟操作系统的虚拟内存管理，自动换入换出记忆

**面试加分点**: 提到 memory compaction（记忆压缩）、retrieval-augmented memory（检索增强记忆）

---

## Q8: 如何评估一个 Agent 系统的好坏？

**A:** Agent 评估维度：

1. **任务完成率**: 能否正确完成目标任务
2. **效率**: 完成任务所需的步骤数、API 调用次数、时间
3. **鲁棒性**: 面对异常输入、工具失败时的恢复能力
4. **安全性**: 是否会执行危险操作、泄露敏感信息
5. **可解释性**: 决策过程是否可追溯

**常用 Benchmark**:
- **AgentBench**: 综合评估 Agent 在多种环境中的表现
- **WebArena**: 网页操作任务
- **SWE-bench**: 软件工程任务（修 bug、写代码）
- **GAIA**: 通用 AI 助手评估

---
