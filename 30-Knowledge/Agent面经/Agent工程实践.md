# Agent 工程实践 面经

> 更新时间：2026-03-11

---

## Q1: 如何设计 Agent 的 Prompt？

**A:** Agent Prompt 设计的核心原则：

1. **角色定义**: 明确 Agent 的身份、能力边界
2. **工具描述**: 清晰描述每个工具的用途、参数、返回值
3. **输出格式**: 约束输出为结构化格式 (JSON/XML)
4. **Few-shot 示例**: 提供正确的工具调用示例
5. **安全约束**: 明确禁止的行为

```
你是一个数据分析助手。
可用工具：
- query_database(sql): 执行 SQL 查询
- plot_chart(data, type): 生成图表

规则：
- 只能执行 SELECT 查询，禁止 DELETE/UPDATE
- 每次最多返回 1000 行数据

示例：
用户：查看上月销售额
Thought: 需要查询上月销售数据
Action: query_database("SELECT SUM(amount) FROM sales WHERE month='2026-02'")
```

---

## Q2: Agent 的上下文窗口不够用怎么办？

**A:** 上下文管理策略：

1. **滑动窗口**: 只保留最近 N 轮对话
2. **摘要压缩**: 将历史对话压缩为摘要
3. **分层记忆**: 重要信息存长期记忆，细节存短期
4. **RAG 检索**: 需要时从长期记忆中检索相关内容
5. **Compaction**: OpenClaw 等框架的自动压缩机制

**实际方案**:
```python
if context_tokens > max_tokens * 0.8:
    # 压缩策略
    summary = llm.summarize(old_messages)
    context = [system_prompt, summary] + recent_messages[-5:]
```

---

## Q3: 如何实现 Agent 的流式工具调用？

**A:** 流式工具调用的挑战是模型边生成边决定是否调用工具。

**方案 1: 后处理模式**
- 等模型完整输出后解析工具调用
- 简单但延迟高

**方案 2: 流式解析模式**
- 边接收 token 边解析 JSON
- 检测到工具调用 pattern 时立即执行
- 需要增量 JSON 解析器

**方案 3: Parallel Function Calling**
- OpenAI 支持一次输出多个工具调用
- 无依赖的调用并行执行

---

## Q4: 多 Agent 系统中如何处理通信和协调？

**A:**

**通信模式**:
1. **共享黑板 (Blackboard)**: 所有 Agent 读写共享状态
2. **消息传递 (Message Passing)**: Agent 之间直接发消息
3. **事件驱动 (Event-Driven)**: Agent 订阅/发布事件

**协调策略**:
1. **中心化**: Manager Agent 统一调度
2. **去中心化**: Agent 自主协商
3. **混合式**: 层级结构 + 同级协作

**实际案例 (MetaGPT)**:
```
ProductManager → 需求文档
    ↓
Architect → 系统设计
    ↓
Engineer → 代码实现
    ↓
QA → 测试用例
```

---

## Q5: 如何做 Agent 的可观测性 (Observability)？

**A:** Agent 可观测性三大支柱：

1. **Logging**: 记录每步决策、工具调用、结果
2. **Tracing**: 端到端追踪请求链路
3. **Metrics**: 延迟、成本、成功率、token 使用量

**工具**:
- **LangSmith**: LangChain 官方追踪平台
- **Langfuse**: 开源 LLM 可观测性平台
- **Phoenix (Arize)**: LLM 评估和追踪
- **OpenTelemetry**: 通用可观测性框架

**关键指标**:
- 任务完成率
- 平均步骤数
- 工具调用成功率
- 端到端延迟
- Token 消耗 / 成本

---

## Q6: Agent 如何处理长时间运行的任务？

**A:**

1. **异步执行**: 任务提交后返回 task_id，轮询或回调获取结果
2. **Checkpoint**: 定期保存中间状态，支持断点续跑
3. **超时控制**: 设置最大执行时间，超时自动终止
4. **进度汇报**: Agent 定期汇报进度
5. **子任务拆分**: 将长任务拆分为多个短任务

**OpenClaw 的做法**:
- Subagent 机制：spawn 子 Agent 处理长任务
- 自动完成通知：子 Agent 完成后自动通知主 Agent
- Heartbeat：定期心跳检查任务状态

---

## Q7: 如何做 Agent 的 A/B 测试和评估？

**A:**

**离线评估**:
1. 构建测试集：(输入, 期望输出, 期望工具调用)
2. 运行 Agent，对比实际输出和期望输出
3. 指标：准确率、F1、工具调用正确率

**在线评估**:
1. A/B 测试：新旧 Agent 分流
2. 用户反馈：点赞/点踩
3. 隐式指标：任务完成率、重试率、放弃率

**LLM-as-Judge**:
- 用另一个 LLM 评估 Agent 输出质量
- 需要精心设计评估 prompt
- 注意评估模型的偏见

---

## Q8: 生产环境部署 Agent 的注意事项？

**A:**

1. **限流**: 控制 LLM API 调用频率，避免超额
2. **熔断**: API 连续失败时自动熔断，避免雪崩
3. **降级**: LLM 不可用时提供基础功能
4. **监控告警**: 异常检测、成本告警
5. **版本管理**: Prompt 版本化，支持回滚
6. **安全审计**: 记录所有操作，定期审查
7. **成本控制**: 设置每用户/每天的 token 上限
8. **多模型冗余**: 主模型不可用时切换备用模型

---
