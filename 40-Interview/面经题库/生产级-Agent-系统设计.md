# 生产级 AI Agent 系统设计面经

> 📅 整理时间：2026-03-19
> 📋 主题：生产级 AI Agent 系统设计与工程实践
> 🏢 公司：淘天集团
> 🔖 标签：#Agent #系统设计 #工程实践 #淘天

---

## Q1: 设计一个生产级的 AI Agent 系统架构

### 核心组件

| 组件 | 职责 | 技术选型 |
|------|------|---------|
| API Gateway | 认证、限流、路由 | Kong / APISIX |
| Planning Agent | 任务规划与分解 | LLM + Prompt |
| Router Agent | 意图识别与路由 | 语义路由 + 分类模型 |
| Worker Agent | 具体任务执行 | 子 Agent 集群 |
| Review Agent | 质量审核与校验 | 规则引擎 + LLM |
| LLM Engine | 模型推理服务 | vLLM / TGI |
| RAG Engine | 检索增强生成 | Milvus + BM25 |
| Memory Manager | 上下文与记忆管理 | Redis + Vector DB |

### 数据流转

```
用户请求 → API Gateway → Planning Agent → Router Agent 
    → Worker Agent → (LLM/RAG/Memory/Tools) → Review Agent → 返回
```

---

## Q2: Agent 的"规划 - 执行 - 反思"闭环如何实现？

```python
class PlanningExecutionReflection:
    async def execute(self, task: str) -> dict:
        # 阶段 1: 规划
        plan = await self.planner.generate(f"""
        任务：{task}
        请制定详细执行计划：
        1. 任务目标是什么？
        2. 需要分解为哪些子任务？
        3. 子任务的依赖关系？
        """)
        
        # 阶段 2: 执行
        results = []
        for step in plan.steps:
            result = await self.executor.execute(step)
            results.append({"step": step, "result": result})
            if not result.success:
                plan = await self._replan(plan, step, result.error)
        
        # 阶段 3: 反思
        reflection = await self.reflector.generate(f"""
        原始任务：{task}
        执行计划：{plan}
        执行结果：{results}
        
        请反思：
        1. 哪些步骤执行得好？
        2. 哪些步骤出现问题？为什么？
        3. 如果重新执行，会如何改进？
        """)
        
        # 阶段 4: 记忆存储
        await self.memory.store_experience({
            "task": task, "plan": plan, 
            "results": results, "reflection": reflection
        })
        
        return {"plan": plan, "results": results, "reflection": reflection}
```

---

## Q3: 多轮对话中，记忆如何分级管理？缓存策略怎么设计？

### 记忆分级

| 层级 | 内容 | 存储 | 访问速度 | 容量 |
|------|------|------|---------|------|
| L1: Working | 最近 5-10 轮 | Redis | 毫秒级 | ~10KB |
| L2: Episodic | 历史对话片段 | Milvus | 秒级 | ~10MB/用户 |
| L3: Semantic | 用户画像/事实 | MySQL+ 向量 | 秒级 | ~1MB/用户 |

### 缓存策略

```python
class MemoryCacheManager:
    def __init__(self):
        self.l1_cache = RedisClient(ttl=1800)  # 30 分钟
        self.l2_cache = LRUCache(max_size=1000, ttl=300)  # 5 分钟
        
    async def get_conversation_context(self, session_id: str) -> list:
        # 1. 检查 L2 缓存 (最快)
        if session_id in self.l2_cache:
            return self.l2_cache[session_id]
        
        # 2. 检查 L1 缓存 (Redis)
        cached = await self.l1_cache.get(f"conversation:{session_id}")
        if cached:
            self.l2_cache[session_id] = cached
            return cached
        
        # 3. 从数据库加载
        messages = await self._load_from_db(session_id, limit=50)
        
        # 4. 写入缓存
        await self.l1_cache.set(f"conversation:{session_id}", messages)
        self.l2_cache[session_id] = messages
        
        return messages
```

---

## Q4: 向量数据库选型对比 (Milvus/Pinecone/Chroma)

### 选型对比

| 维度 | Milvus | Pinecone | Chroma |
|------|--------|----------|--------|
| 部署方式 | 自建/云 | SaaS only | 本地/自建 |
| 数据规模 | 10 亿 + | 10 亿 + | 百万级 |
| 查询延迟 | <10ms | <10ms | <50ms |
| 成本 | 中 | 高 | 低 |
| 运维复杂度 | 高 | 低 | 低 |

### 淘天场景推荐：Milvus (自建)

**理由：**
- 数据规模大，需要 10 亿级支持
- 数据主权：自建保证数据不出域
- 成本可控：大规模下自建成本远低于 SaaS
- 定制能力：可根据业务定制索引

---

## Q5: Function Calling 的可靠性如何保障？

```python
class FunctionCallingReliability:
    async def execute_with_reliability(self, tool_name: str, args: dict):
        # 1. 工具存在性校验
        tool = self.tool_registry.get(tool_name)
        if not tool:
            raise ToolNotFoundError(f"工具 {tool_name} 不存在")
        
        # 2. 参数校验
        validation = await self.validator.validate(tool_name, args)
        if not validation.valid:
            raise ValidationError(f"参数校验失败：{validation.errors}")
        
        # 3. 熔断器检查
        if self.circuit_breaker.is_open(tool_name):
            raise CircuitBreakerError(f"工具 {tool_name} 熔断中")
        
        # 4. 执行 (带重试)
        try:
            result = await self.retry_policy.execute(
                func=tool.execute, args=args,
                max_retries=3, backoff="exponential"
            )
            return result
        except Exception as e:
            self.circuit_breaker.record_failure(tool_name)
            # 5. 降级策略
            fallback = self.tool_registry.get_fallback(tool_name)
            if fallback:
                return await fallback.execute(args)
            raise
    
    async def detect_loop(self, call_history: list) -> bool:
        """检测重复调用循环"""
        recent_calls = call_history[-5:]
        tool_counts = Counter([c["tool_name"] for c in recent_calls])
        for tool_name, count in tool_counts.items():
            if count >= 4:
                return True
        return False
```

---

## Q6: 工具的描述 (description) 怎么写才能让模型准确调用？

### STAR 法则

| 要素 | 说明 | 示例 |
|------|------|------|
| S | 使用场景 | "当用户查询商品时..." |
| T | 任务目标 | "...获取商品详细信息..." |
| A | 执行动作 | "...调用商品查询 API..." |
| R | 预期结果 | "...返回商品名称、价格、库存" |

### 淘天场景示例

```python
tool_description = """
【工具名称】商品详情查询

【使用场景】
当用户询问具体商品的信息时，如价格、库存、规格、配送等。

【输入参数】
- item_id (必填): 商品 ID，格式为数字字符串
- fields (可选): 需要返回的字段，默认 ["title", "price", "stock"]

【输出格式】
{"item_id": "123456789", "title": "商品名称", "price": 99.99, "stock": 1000}

【使用示例】
用户问："这个商品多少钱？有货吗？"
→ 调用此工具，传入 item_id
→ 返回价格和库存信息

【注意事项】
- 商品 ID 必须有效，否则返回错误
- 价格单位为元，保留 2 位小数
- 库存为 0 时表示售罄
"""
```

---

## Q7: RAG 系统中，chunk 大小怎么确定？

### 不同业务场景策略

| 场景 | Chunk 大小 | 重叠 | 理由 |
|------|----------|------|------|
| 商品详情 | 512-1024 tokens | 50-100 | 商品属性独立，小 chunk 精确 |
| 客服 FAQ | 256-512 tokens | 50 | 问答对独立，小 chunk 足够 |
| 技术文档 | 1024-2048 tokens | 100-200 | 需要上下文理解 |
| 法律合同 | 512-1024 tokens | 100 | 条款独立但需精确引用 |
| 新闻文章 | 1024-2048 tokens | 200 | 保持叙事完整性 |

---

## Q8: 检索结果相关性不高，怎么优化召回？

### 优化策略金字塔

1. **Query 优化**（最快见效）
   - Query 扩展（同义词）
   - Query 改写（LLM）
   - 拼写纠错

2. **索引优化**
   - 分块策略调整
   - 元数据增强

3. **检索策略优化**
   - 混合检索（向量+BM25）
   - 元数据过滤

4. **重排序优化**
   - Cross-Encoder 重排序
   - RRF 融合

```python
class HybridRetriever:
    def retrieve(self, query: str, k: int = 10):
        # 1. 向量检索（语义）
        query_emb = self.embed(query)
        vector_results = self.vector_db.search(query_emb, k=k*2)
        
        # 2. 关键词检索（精确匹配）
        keyword_results = self.bm25.search(query, k=k*2)
        
        # 3. 结果融合（RRF）
        fused = self.reciprocal_rank_fusion(vector_results, keyword_results, k=60)
        
        return fused[:k]
```

---

## Q9: Agent 推理链路包含多个串行工具，响应延迟高，该如何优化？

### 延迟优化策略

| 策略 | 延迟降低 | 实现难度 |
|------|---------|---------|
| 并行化 | 40-60% | 中 |
| 缓存 | 30-50% | 低 |
| 流式响应 | 感知延迟 -70% | 中 |
| 预计算 | 20-40% | 高 |

```python
# 并行执行
async def execute_parallel(self, steps: list):
    # 1. 分析依赖关系
    dag = self._build_dependency_graph(steps)
    
    # 2. 拓扑排序，找出可并行的步骤
    levels = self._topological_sort(dag)
    
    # 3. 按层级并行执行
    results = {}
    for level in levels:
        tasks = [
            self.execute_tool(step).then(lambda r, s=step: results.update({s: r}))
            for step in level
        ]
        await asyncio.gather(*tasks)
    
    return results
```

---

## Q10: 高并发场景下，如何设计 Agent 服务的弹性伸缩策略？

### 多级伸缩策略

| 层级 | 触发条件 | 响应时间 | 说明 |
|------|---------|---------|------|
| L1: Pod 内 | CPU>80% | 秒级 | 增加 Worker 线程 |
| L2: HPA | 平均 CPU>70% | 分钟级 | Kubernetes HPA |
| L3: Cluster | 资源不足 | 分钟级 | 增加节点 |
| L4: 降级 | 过载保护 | 秒级 | 限流/熔断 |

### 过载保护

```python
class OverloadProtection:
    async def handle_request(self, request):
        # 1. 限流
        if not self.rate_limiter.allow():
            raise RateLimitError("请求过多，请稍后重试")
        
        # 2. 熔断检查
        if self.circuit_breaker.is_open():
            raise CircuitBreakerError("服务过载，已熔断")
        
        # 3. 队列长度检查
        if self.queue.size() > 1000:
            raise OverloadError("系统过载")
        
        return await self.process(request)
```

---

## Q11: Agent 系统的核心监控指标有哪些？

### 核心监控指标

**业务指标：**
- 请求成功率 (<95% 告警)
- 任务完成率 (<90% 告警)
- 平均响应时间 P50 (>2s 告警)
- 用户满意度 (<80% 告警)

**技术指标：**
- CPU 使用率 (>80% 告警)
- 内存使用率 (>85% 告警)
- 错误率 (>1% 告警)
- 队列长度 (>1000 告警)

**LLM 特定指标：**
- Token 消耗
- 模型延迟 (>5s 告警)
- 幻觉率 (>5% 告警)
- 安全拦截数

---

## Q12: 如何追踪 Agent 的单次请求完整链路？

```python
class DistributedTracing:
    async def process_request(self, request: dict):
        trace_id = str(uuid4())
        span_id = str(uuid4())
        
        context = {
            "trace_id": trace_id,
            "span_id": span_id,
            "parent_span_id": None
        }
        
        with self.tracer.start_span("agent_request", context=context) as root_span:
            root_span.set_attribute("request_id", request["id"])
            
            # Planning
            with self.tracer.start_span("planning", parent=root_span) as planning_span:
                plan = await self.planner.execute(request)
                planning_span.set_attribute("plan_steps", len(plan.steps))
            
            # 执行各个步骤
            for i, step in enumerate(plan.steps):
                with self.tracer.start_span(f"step_{i}", parent=root_span) as step_span:
                    step_span.set_attribute("step_type", step.type)
                    step_span.set_attribute("tool_name", step.tool)
                    result = await self.execute_step(step)
                    step_span.set_attribute("success", result.success)
```

### Trace 传播

```python
class TraceContextPropagation:
    def inject(self, context: dict, carrier: dict):
        carrier["X-Trace-ID"] = context["trace_id"]
        carrier["X-Span-ID"] = context["span_id"]
        carrier["X-Parent-Span-ID"] = context["parent_span_id"]
    
    def extract(self, carrier: dict) -> dict:
        return {
            "trace_id": carrier.get("X-Trace-ID"),
            "span_id": str(uuid4()),
            "parent_span_id": carrier.get("X-Span-ID")
        }
```

---

**整理完成！** 🦐

---

*标签：#Agent #系统设计 #工程实践 #淘天 #面经*
