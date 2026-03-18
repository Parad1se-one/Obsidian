# Agent 高级系统设计 面经

> 更新时间：2026-03-18
> 难度：⭐⭐⭐⭐⭐
> 主题：记忆、上下文、工具路由、多 Agent 协作、工程优化

---

## 一、记忆系统设计

### Q1: 在 Agent 知识闭环中，如何设计，去决定哪些信息进入向量数据库（长期记忆），哪些进入上下文窗口（短期记忆），以及哪些直接转化为模型权重的元记忆？

**A:** 三级记忆架构设计：

```
┌─────────────────────────────────────────────────────────┐
│                    记忆分层决策器                        │
├─────────────────┬─────────────────┬─────────────────────┤
│   短期记忆       │   长期记忆       │    元记忆           │
│   (Context)     │   (Vector DB)   │   (Meta-Memory)     │
├─────────────────┼─────────────────┼─────────────────────┤
│ • 当前对话轮次   │ • 历史对话摘要   │ • 用户偏好配置       │
│ • 任务执行状态   │ • 关键事实知识   │ • 工具使用模式       │
│ • 临时中间结果   │ • 经验教训       │ • 领域专业知识       │
│ • 即时工具返回   │ • 用户画像      │ • 系统参数配置       │
└─────────────────┴─────────────────┴─────────────────────┘
```

**决策标准**:

| 维度 | 短期记忆 | 长期记忆 | 元记忆 |
|------|----------|----------|--------|
| **时效性** | 分钟级 | 天/月级 | 永久/季度级 |
| **访问频率** | 极高 (每轮) | 中 (按需检索) | 低 (启动时加载) |
| **信息粒度** | 原始对话 | 摘要/提取 | 结构化配置 |
| **更新方式** | 自动追加 | 触发式写入 | 人工/学习更新 |
| **容量限制** | Context Window | 向量库容量 | 模型权重/Config |

**具体实现策略**:

```python
def memory_router(turn_data):
    # 1. 短期记忆：直接加入上下文
    if turn_data.is_current_task or turn_data.is_tool_result:
        context_window.append(turn_data)
    
    # 2. 长期记忆：触发条件写入向量库
    if should_store_long_term(turn_data):
        # 触发条件：用户明确陈述事实、任务完成总结、关键决策点
        embedding = embed(turn_data.summary)
        vector_db.upsert(turn_data.id, embedding, turn_data.metadata)
    
    # 3. 元记忆：离线学习更新
    if turn_data.pattern_matches_user_preference():
        meta_memory.update_user_profile(turn_data.extracted_preference)
```

**关键判断逻辑**:
- **进入向量库**: 信息具有复用价值、可独立理解、非瞬时状态
- **进入上下文**: 当前任务必需、需要精确原文、短期引用
- **转化为元记忆**: 跨任务通用模式、用户稳定偏好、系统级知识

---

### Q2: 当对话轮数极多且上下文窗口严重不足时，如何在不丢失初始 Attention Sink 的前提下保持生成的连贯性？

**A:** Attention Sink 是指 Transformer 对序列开头 tokens 的注意力偏好现象。保留策略：

**方案 1: 滑动窗口 + 固定前缀**
```
[Fixed Prefix: 系统指令 + 关键事实] + [Sliding Window: 最近 N 轮] + [摘要压缩：中间历史]
```

**方案 2: 分层摘要链**
```
原始对话 → 轮次级摘要 (每 10 轮) → 会话级摘要 (每 100 轮) → 主题级摘要
```

**方案 3: 关键信息锚点**
```python
# 保留 Attention Sink 的关键位置
anchor_points = [
    system_prompt,           # 位置 0: 系统指令
    user_identity,           # 位置 1-10: 用户信息
    task_definition,         # 位置 11-50: 任务定义
    recent_context,          # 最后 N 轮：当前状态
    compressed_history       # 中间：压缩摘要
]
```

**方案 4: StreamingLLM 技术**
- 保留初始 tokens (Attention Sink)
- 保留最近 tokens (局部注意力)
- 中间 tokens 采用稀疏注意力或摘要替代

**工程实践**:
```python
def build_context_with_sink(history, max_tokens=8000):
    sink_tokens = history[:500]      # 保留开头 500 tokens
    recent_tokens = history[-3000:]  # 保留最近 3000 tokens
    middle_summary = summarize(history[500:-3000])  # 中间压缩
    return sink_tokens + middle_summary + recent_tokens
```

---

### Q3: 摘要总结往往会丢失关键细节，在长文本 Agent 中一般怎么来处理这一块？

**A:** 细节保留策略：

**1. 分层索引 + 按需展开**
```
摘要层 (快速浏览)
  ↓ 索引指向
细节层 (按需检索)
  ↓ 索引指向
原始层 (精确引用)
```

**2. 关键信息提取保留**
```python
def smart_summarize(text):
    summary = llm_summarize(text)
    # 同时提取并保留关键实体
    entities = extract_entities(text)  # 人名、地名、时间、数字
    decisions = extract_decisions(text)  # 关键决策点
    unresolved = extract_open_questions(text)  # 未解决问题
    return {
        "summary": summary,
        "anchors": entities + decisions + unresolved,  # 保留细节锚点
        "pointers": chunk_references  # 指向原文的指针
    }
```

**3. 问题感知摘要 (Question-Aware Summarization)**
- 记录历史对话中用户问过的所有问题
- 摘要时确保每个问题的答案被保留
- 建立 Q-A 索引对

**4. 向量检索兜底**
- 摘要作为主视图
- 原始文本分块存入向量库
- 当用户追问细节时，从向量库检索原文

---

## 二、上下文与 Attention 优化

### Q4: Token 过长导致的 Attention 稀释现象为什么会导致 Agent 的指令遵循能力下降？

**A:** Attention 稀释机制：

**问题根源**:
```
Attention(Q, K, V) = softmax(QK^T / √d) · V

当序列长度 L 增长时:
1. 每个 token 分到的注意力权重 ≈ 1/L
2. 关键指令的注意力占比被稀释
3. 模型"忘记"系统指令和核心约束
```

**具体表现**:
- 系统指令被忽略（如"不要执行危险操作"）
- 输出格式要求被违反
- 角色设定逐渐偏离
- 安全约束失效

**解决方案**:

| 方案 | 原理 | 效果 |
|------|------|------|
| **指令重复** | 在长上下文中多次插入关键指令 | 增加注意力捕获概率 |
| **指令标记** | 用特殊 token 包裹指令 `<system>...</system>` | 增强边界识别 |
| **注意力重加权** | 对指令区域 attention score 乘系数 | 强制关注 |
| **上下文分段** | 将长文本分段处理，每段都带指令 | 避免稀释 |
| **RAG 式指令** | 将指令放入向量库，检索时一并返回 | 动态注入 |

---

### Q5: 在 Agent 多轮对话任务中，标准 Attention 机制的平方复杂度在工程落地上主要引发了哪些问题？

**A:** O(n²) 复杂度的工程问题：

**1. 内存爆炸**
```
序列长度 4K → Attention 矩阵 16M 元素
序列长度 32K → Attention 矩阵 1B 元素 (约 4GB 显存)
序列长度 128K → Attention 矩阵 16B 元素 (约 64GB 显存)
```

**2. 延迟问题**
- Prefill 阶段随长度平方增长
- 长文本首 token 延迟可达数秒到数十秒
- 实时交互场景不可接受

**3. 成本问题**
- 计算量平方增长 → GPU 时间增加 → 成本飙升
- 长文本任务成本可能是短文本的 10-100 倍

**4. 批处理效率低**
- 不同长度样本需 padding 到同一长度
- 短样本浪费计算资源

**优化方案**:

| 技术 | 复杂度 | 适用场景 |
|------|--------|----------|
| **FlashAttention** | O(n²) 但常数极小 | 通用优化 |
| **Sparse Attention** | O(n log n) | 长文档 |
| **Sliding Window** | O(n·w) | 对话 |
| **Linear Attention** | O(n) | 超长序列 |
| **PagedAttention** | O(n²) 但显存优化 | vLLM 使用 |

---

### Q6: 目前有哪些机制可以缓解模型在长上下文对话里的"信息遗忘"现象？

**A:** 遗忘缓解机制：

**1. 检索增强 (RAG)**
```python
# 对话历史存入向量库，每轮检索相关历史
def retrieve_relevant_history(current_query, history_db, top_k=5):
    query_embedding = embed(current_query)
    similar_turns = history_db.similarity_search(query_embedding, top_k)
    return format_as_context(similar_turns)
```

**2. 分层记忆**
- 工作记忆：当前对话窗口 (最近 10-20 轮)
- 情景记忆：会话级摘要
- 语义记忆：提取的事实和知识

**3. 持续性摘要 (Progressive Summarization)**
```
每 N 轮 → 生成阶段摘要
每 M 个阶段 → 生成会话摘要
摘要保留关键实体和决策指针
```

**4. 记忆网络 (Memory Networks)**
- 显式记忆矩阵存储历史
- 注意力机制读取相关记忆
- 支持记忆更新和删除

**5. 键值记忆 (Key-Value Memory)**
```python
# 将历史信息以 KV 对形式存储
memory = {
    "user_name": "张三",
    "preference": "喜欢简洁回答",
    "ongoing_task": "分析财报",
    "last_result": "营收增长 15%"
}
```

**6. 递归检索 (Recursive Retrieval)**
- 用户问题 → 检索相关历史
- 历史中提到的内容 → 进一步检索
- 构建知识链条

---

## 三、Agent 架构与推理

### Q7: 详细讲讲你设计的 Agent 是如何实现的？在"推理—行动"循环中，如何设计来纠正逻辑塌缩或无效工具调用？

**A:** Agent 实现架构：

```
┌─────────────────────────────────────────────────────────┐
│                    Agent Controller                      │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Perception│→│ Planning │→│ Execution│→│ Reflection│ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│       ↑                                        │        │
│       └────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

**推理 - 行动循环实现**:

```python
class AgentLoop:
    def __init__(self, max_iterations=10):
        self.max_iterations = max_iterations
        self.history = []
        
    def run(self, task):
        for i in range(self.max_iterations):
            # 1. 推理阶段
            thought = self.reason(task, self.history)
            
            # 2. 逻辑验证
            if not self.validate_logic(thought):
                thought = self.correct_logic_collapse(thought)
            
            # 3. 行动决策
            if thought.needs_tool_call:
                # 4. 工具调用验证
                tool_call = self.plan_tool_call(thought)
                if not self.validate_tool_call(tool_call):
                    tool_call = self.correct_invalid_tool(tool_call)
                
                # 5. 执行
                result = self.execute(tool_call)
                self.history.append((thought, tool_call, result))
            else:
                # 6. 直接输出
                return self.finalize(thought)
        
        # 达到最大迭代次数，强制收敛
        return self.force_converge(self.history)
```

**逻辑塌缩检测与纠正**:

```python
def detect_logic_collapse(thought_history):
    """检测逻辑塌缩：循环论证、自相矛盾、跳跃推理"""
    issues = []
    
    # 1. 循环检测
    if has_circular_reasoning(thought_history):
        issues.append("circular_reasoning")
    
    # 2. 矛盾检测
    if has_contradiction(thought_history):
        issues.append("contradiction")
    
    # 3. 跳跃检测
    if has_logical_gap(thought_history):
        issues.append("logical_gap")
    
    return issues

def correct_logic_collapse(current_thought, issues):
    """纠正策略"""
    if "circular_reasoning" in issues:
        # 打破循环：强制引入新信息或改变推理角度
        return break_cycle(current_thought)
    
    if "contradiction" in issues:
        # 矛盾消解：识别更可信的前提
        return resolve_contradiction(current_thought)
    
    if "logical_gap" in issues:
        # 补充中间步骤
        return fill_logical_gaps(current_thought)
```

**无效工具调用纠正**:

```python
def validate_tool_call(tool_call):
    """验证工具调用有效性"""
    checks = [
        tool_exists(tool_call.name),
        parameters_match_schema(tool_call),
        preconditions_satisfied(tool_call),
        not_duplicate_recent_call(tool_call),  # 避免重复调用
        expected_output_defined(tool_call),     # 有明确的预期输出
    ]
    return all(checks)

def correct_invalid_tool(invalid_call, error):
    """纠正无效调用"""
    if error == "missing_parameter":
        return infer_missing_parameter(invalid_call)
    elif error == "wrong_tool":
        return suggest_alternative_tool(invalid_call)
    elif error == "precondition_failed":
        return plan_precondition_steps(invalid_call)
```

---

### Q8: 为什么在复杂的 Agent 闭环场景中，仅靠 RAG 无法彻底解决幻觉问题？

**A:** RAG 的局限性：

**1. 检索阶段的问题**
- **召回偏差**: 相关文档可能未被检索到
- **排序错误**: 正确信息排名靠后被忽略
- **知识冲突**: 检索到矛盾信息时模型无法判断

**2. 生成阶段的问题**
- **信息融合错误**: 模型可能错误组合多个文档的信息
- **过度推断**: 基于检索内容进行不合理推理
- **选择性忽略**: 模型可能忽略检索结果，依赖内部知识

**3. 闭环场景的特殊问题**
- **工具执行幻觉**: 声称执行了工具但实际没有
- **结果伪造**: 编造工具返回结果
- **状态不一致**: 多轮执行中状态跟踪错误

**综合解决方案**:

```
┌─────────────────────────────────────────────────────────┐
│              幻觉防护多层体系                            │
├─────────────────────────────────────────────────────────┤
│ Layer 1: 检索验证                                        │
│   • 多路召回 (语义 + 关键词 + 向量)                       │
│   • 来源可信度评分                                        │
│   • 信息一致性检查                                        │
├─────────────────────────────────────────────────────────┤
│ Layer 2: 生成约束                                        │
│   • 引用强制标注 (必须标注信息来源)                       │
│   • 置信度阈值 (低于阈值则说不知道)                       │
│   • 事实核查模块                                          │
├─────────────────────────────────────────────────────────┤
│ Layer 3: 执行验证                                        │
│   • 工具调用日志记录                                      │
│   • 执行结果哈希验证                                      │
│   • 状态机跟踪                                            │
├─────────────────────────────────────────────────────────┤
│ Layer 4: 后验检测                                        │
│   • 输出事实核查                                          │
│   • 自洽性检查                                            │
│   • 外部知识验证                                          │
└─────────────────────────────────────────────────────────┘
```

---

### Q9: 面对模型在 Agent 执行过程中出现的"循环调用"或陷入思维死循环问题，有哪些解决方式？

**A:** 循环检测与打破策略：

**1. 循环检测机制**
```python
class LoopDetector:
    def __init__(self, window_size=5):
        self.history = []
        self.window_size = window_size
    
    def detect(self, current_state):
        self.history.append(current_state)
        if len(self.history) > self.window_size:
            self.history.pop(0)
        
        # 检测状态重复
        if len(set(self.history)) < len(self.history) - 1:
            return True  # 检测到循环
        
        # 检测工具调用序列重复
        if self.has_repeating_tool_sequence():
            return True
        
        return False
```

**2. 打破循环策略**

| 策略 | 实现方式 | 适用场景 |
|------|----------|----------|
| **最大迭代限制** | 设置 max_iterations，超限强制退出 | 通用兜底 |
| **状态扰动** | 随机改变 temperature/top_p | 轻微循环 |
| **工具切换** | 强制使用备选工具 | 工具调用循环 |
| **问题重构** | 重新表述任务 | 推理循环 |
| **人类介入** | 请求用户澄清 | 复杂循环 |
| **回溯跳转** | 回到之前的有效状态 | 可恢复循环 |

**3. 实现示例**
```python
def execute_with_loop_protection(agent, task):
    max_iterations = 10
    loop_detector = LoopDetector()
    
    for i in range(max_iterations):
        state = agent.get_state()
        
        if loop_detector.detect(state):
            # 打破循环
            strategy = select_break_strategy(loop_detector.pattern)
            agent.apply_strategy(strategy)
            loop_detector.reset()
            continue
        
        agent.step()
        
        if agent.is_done():
            return agent.result()
    
    # 达到最大迭代，强制收敛
    return agent.force_complete()
```

---

## 四、工具与 MCP

### Q10: MCP 与传统 Agent Skills 的区别是什么？如何实现在多智能体环境中动态发现并注册跨协议工具？

**A:** MCP vs Agent Skills:

| 维度 | 传统 Agent Skills | MCP |
|------|------------------|-----|
| **接口标准** | 各框架自定义 | 统一协议标准 |
| **发现机制** | 静态注册 | 动态发现 |
| **跨框架** | 不支持 | 支持 |
| **远程调用** | 有限支持 | 原生支持 |
| **权限模型** | 框架内 | 协议级 |
| **生态** | 封闭 | 开放 |

**MCP 架构**:
```
┌─────────────┐     MCP Protocol     ┌─────────────┐
│   Agent A   │ ←──────────────────→ │ MCP Server  │
│ (LangChain) │                      │  (Tools)    │
├─────────────┤                      ├─────────────┤
│   Agent B   │ ←──────────────────→ │ MCP Server  │
│ (AutoGen)   │                      │ (Resources) │
└─────────────┘                      └─────────────┘
```

**动态发现与注册实现**:

```python
class MCPAgentRegistry:
    def __init__(self):
        self.discovered_tools = {}
        self.registry = ServiceRegistry()  # 服务发现
    
    async def discover_tools(self, agent_id):
        """动态发现可用工具"""
        # 1. 从服务注册中心获取 MCP Server 列表
        servers = await self.registry.lookup("mcp-server")
        
        # 2. 连接每个 Server 获取工具列表
        for server in servers:
            tools = await self.fetch_tool_manifest(server)
            for tool in tools:
                self.discovered_tools[tool.id] = {
                    "server": server,
                    "schema": tool.schema,
                    "protocol": tool.protocol,  # HTTP/gRPC/WebSocket
                }
        
        # 3. 根据 Agent 能力过滤
        compatible_tools = self.filter_by_capability(agent_id)
        return compatible_tools
    
    async def register_cross_protocol(self, tool):
        """注册跨协议工具"""
        # 协议适配器
        adapter = ProtocolAdapter(tool.protocol)
        wrapper = adapter.wrap(tool)
        
        # 统一接口注册
        self.tool_registry.register(wrapper)
```

---

### Q11: 当候选工具超过 100 个时，如何设计路由策略？怎么解决检索过程中的召回偏差？

**A:** 大规模工具路由策略：

**分层路由架构**:
```
用户请求
    ↓
┌─────────────────┐
│ 意图分类层       │ → 确定工具类别 (搜索/计算/查询/创作)
└────────┬────────┘
         ↓
┌─────────────────┐
│ 粗排检索层       │ → 从 100+ 工具中召回 Top 20 (向量检索)
└────────┬────────┘
         ↓
┌─────────────────┐
│ 精排评分层       │ → 基于多特征排序 Top 5
└────────┬────────┘
         ↓
┌─────────────────┐
│ 验证执行层       │ → 验证参数、执行工具
└─────────────────┘
```

**召回偏差解决方案**:

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| **语义偏差** | 向量嵌入不完美 | 多路召回 (语义 + 关键词 + 工具名) |
| **长尾工具** | 热门工具主导 | 类别配额、多样性采样 |
| **新工具冷启动** | 无使用历史 | 基于描述相似度、人工标注 |
| **上下文忽略** | 未考虑当前状态 | 上下文感知检索 |

**实现代码**:
```python
class ToolRouter:
    def __init__(self, tool_db):
        self.tool_db = tool_db
        self.vector_index = tool_db.build_vector_index()
    
    def route(self, query, context):
        # 1. 多路召回
        semantic_results = self.vector_search(query, top_k=30)
        keyword_results = self.keyword_search(query, top_k=20)
        category_results = self.category_filter(context.category, top_k=20)
        
        # 2. 合并去重
        candidates = self.reciprocal_rank_fusion([
            semantic_results, keyword_results, category_results
        ])
        
        # 3. 精排
        ranked = self.rerank(candidates, query, context)
        
        # 4. 多样性保证
        final = self.ensure_diversity(ranked[:10])
        
        return final
    
    def reciprocal_rank_fusion(self, result_lists, k=60):
        """RRF 融合多路召回结果"""
        scores = {}
        for results in result_lists:
            for rank, item in enumerate(results):
                scores[item.id] = scores.get(item.id, 0) + 1 / (k + rank)
        return sorted(scores.items(), key=lambda x: -x[1])
```

---

## 五、需求理解与澄清

### Q12: 在电商或导购场景下，用户的请求往往高度模糊，Agent 怎么来精准理解这种需求？

**A:** 模糊需求理解框架：

```
用户模糊请求 → 意图识别 → 槽位填充 → 置信度评估 → 澄清/执行
```

**1. 意图识别层**
```python
intent_classifier = {
    "browse": "浏览商品",
    "compare": "对比商品",
    "recommend": "寻求推荐",
    "purchase": "直接购买",
    "query_order": "查询订单",
    "after_sales": "售后问题"
}
```

**2. 槽位提取与填充**
```python
# 用户说："我想买个手机"
slots = {
    "category": "手机",           # 明确
    "brand": None,                # 缺失
    "price_range": None,          # 缺失
    "features": [],               # 缺失
    "urgency": "normal"           # 推断
}
```

**3. 上下文增强理解**
```python
def understand_with_context(user_query, history, profile):
    # 历史行为
    if history.recently_viewed("iPhone"):
        slots["brand_preference"] = "Apple"
    
    # 用户画像
    if profile.price_sensitivity == "high":
        slots["price_range"] = "budget"
    
    # 会话上下文
    if previous_turn.discussed("拍照"):
        slots["feature_priority"] = "camera"
    
    return slots
```

**4. 置信度评估与决策**
```python
confidence = calculate_confidence(slots)

if confidence > 0.8:
    # 直接执行
    return execute_search(slots)
elif confidence > 0.5:
    # 部分澄清
    missing = find_missing_critical_slots(slots)
    return ask_clarification(missing)
else:
    # 完全澄清
    return ask_open_questions()
```

---

### Q13: 如何设计一套"主动澄清"决策逻辑？在什么情况下 Agent 应该反问用户，什么情况下应该结合历史画像强行推断？

**A:** 主动澄清决策框架：

**决策矩阵**:
```
                    信息重要性
                  高          低
              ┌──────────┬──────────┐
         高   │ 必须澄清  │ 建议澄清  │
置信度        ├──────────┼──────────┤
         低   │ 必须澄清  │ 可推断    │
              └──────────┴──────────┘
```

**决策逻辑**:
```python
def should_clarify(slot, confidence, context):
    # 1. 关键槽位判断
    is_critical = slot in ["price_range", "category", "deadline"]
    
    # 2. 置信度阈值
    high_conf_threshold = 0.8
    low_conf_threshold = 0.5
    
    # 3. 用户偏好
    user_tolerates_assumption = context.profile.tolerates_assumptions
    
    # 4. 决策
    if is_critical and confidence < high_conf_threshold:
        return CLARIFY  # 关键信息，必须澄清
    
    if not is_critical and confidence < low_conf_threshold:
        if user_tolerates_assumptions:
            return INFER  # 非关键，可推断
        else:
            return CLARIFY
    
    if confidence >= high_conf_threshold:
        return INFER  # 高置信度，直接推断
    
    return CLARIFY
```

**澄清策略选择**:
```python
def generate_clarification(missing_slots):
    if len(missing_slots) == 1:
        # 单一问题，直接问
        return f"您更倾向于{missing_slots[0].options}？"
    
    if len(missing_slots) <= 3:
        # 少量问题，选择题
        return generate_multiple_choice(missing_slots)
    
    # 问题太多，分步澄清
    return generate_step_by_step_clarification(missing_slots)
```

**推断策略**:
```python
def infer_slot(slot, context):
    # 1. 历史行为推断
    if slot == "brand_preference":
        return infer_from_purchase_history(context)
    
    # 2. 画像推断
    if slot == "price_range":
        return infer_from_income_level(context.profile)
    
    # 3. 默认值
    return slot.default_value
```

---

## 六、性能优化

### Q14: 针对包含 3 个以上工具调用且高频请求的任务，通过什么方式可以压低系统整体的端到端延迟？

**A:** 延迟优化策略：

**1. 并行化**
```python
# 串行 (慢)
result1 = tool1()
result2 = tool2(result1)
result3 = tool3(result2)

# 并行 (快) - 无依赖时
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(tool1())
    task2 = tg.create_task(tool2())
    task3 = tg.create_task(tool3())
results = [task1.result(), task2.result(), task3.result()]
```

**2. 依赖分析 + 流水线**
```python
# 分析工具依赖图
dependency_graph = {
    "tool1": [],
    "tool2": ["tool1"],  # tool2 依赖 tool1
    "tool3": []
}

# 执行计划
# Stage 1: tool1, tool3 (并行)
# Stage 2: tool2 (等 tool1 完成)
```

**3. 缓存策略**
```python
@cache(ttl=300)  # 5 分钟缓存
def expensive_tool_call(params):
    return tool.execute(params)

# 预热缓存
def prefetch_cache(predicted_requests):
    for req in predicted_requests:
        cache.warmup(req)
```

**4. 流式输出**
```python
# 边执行边返回
async def stream_results(tasks):
    for task in asyncio.as_completed(tasks):
        result = await task
        yield result  # 立即返回已完成的部分
```

**5. 模型分级**
```python
def route_by_complexity(task):
    if task.complexity < 0.3:
        return small_model  # 快、便宜
    elif task.complexity < 0.7:
        return medium_model
    else:
        return large_model  # 慢、贵
```

**端到端优化架构**:
```
用户请求
    ↓
┌─────────────────┐
│ 请求预测 + 缓存检查 │ ← 命中则直接返回
└────────┬────────┘
         ↓ 未命中
┌─────────────────┐
│ 依赖分析 + 并行规划 │
└────────┬────────┘
         ↓
┌─────────────────┐
│ 工具并行执行     │ ← 流式返回中间结果
└────────┬────────┘
         ↓
┌─────────────────┐
│ 结果聚合 + 缓存写入│
└─────────────────┘
```

---

### Q15: 任务执行远大于单次 Token 限制时，如何设计以支持断点继续生成？

**A:** 断点续生成设计：

**1. 状态持久化**
```python
class CheckpointManager:
    def save(self, task_id, state):
        checkpoint = {
            "task_id": task_id,
            "completed_steps": state.completed,
            "pending_steps": state.pending,
            "accumulated_results": state.results,
            "context_summary": summarize(state.context),
            "timestamp": time.now()
        }
        db.save(checkpoint)
    
    def load(self, task_id):
        checkpoint = db.load(task_id)
        return restore_state(checkpoint)
```

**2. 任务分片**
```python
def chunk_large_task(task, max_tokens_per_chunk=4000):
    """将大任务拆分为可管理的子任务"""
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for step in task.steps:
        step_tokens = estimate_tokens(step)
        if current_tokens + step_tokens > max_tokens_per_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_tokens = 0
        current_chunk.append(step)
        current_tokens += step_tokens
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks
```

**3. 恢复执行**
```python
async def resume_task(task_id):
    # 1. 加载检查点
    state = checkpoint_manager.load(task_id)
    
    # 2. 恢复上下文
    context = rebuild_context(state.accumulated_results)
    
    # 3. 从断点继续
    for step in state.pending_steps:
        result = await execute_step(step, context)
        state.accumulated_results.append(result)
        checkpoint_manager.save(task_id, state)
    
    return finalize(state.accumulated_results)
```

**4. 增量摘要**
```python
# 避免上下文爆炸
def incremental_summary(old_summary, new_content):
    """增量更新摘要而非追加全文"""
    prompt = f"""
    旧摘要：{old_summary}
    新内容：{new_content}
    
    请生成合并后的摘要，保留关键信息，控制长度。
    """
    return llm.generate(prompt)
```

---

## 七、多 Agent 协作

### Q16: 在多 Agent 协作系统中，不同 Agent 之间的记忆如何实现隔离与共享？如何避免不同工具间的上下文污染？

**A:** 多 Agent 记忆管理：

**记忆隔离与共享架构**:
```
┌─────────────────────────────────────────────────────────┐
│                    全局记忆管理器                        │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Agent A     │  │ Agent B     │  │ Agent C     │     │
│  │ 私有记忆    │  │ 私有记忆    │  │ 私有记忆    │     │
│  │ (Private)   │  │ (Private)   │  │ (Private)   │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │            │
│         └────────────────┼────────────────┘            │
│                          ↓                              │
│              ┌───────────────────────┐                 │
│              │    共享记忆区          │                 │
│              │    (Shared Memory)    │                 │
│              │  • 任务状态           │                 │
│              │  • 公共知识           │                 │
│              │  • 协调信息           │                 │
│              └───────────────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

**实现方案**:

```python
class MultiAgentMemory:
    def __init__(self):
        self.private_memories = {}  # agent_id → private memory
        self.shared_memory = SharedMemory()
        self.access_control = AccessControl()
    
    def get_memory(self, agent_id, key, scope="private"):
        if scope == "private":
            return self.private_memories[agent_id].get(key)
        elif scope == "shared":
            if self.access_control.can_access(agent_id, key):
                return self.shared_memory.get(key)
    
    def set_memory(self, agent_id, key, value, scope="private", visibility=None):
        if scope == "private":
            self.private_memories[agent_id].set(key, value)
        elif scope == "shared":
            # 设置访问控制
            self.shared_memory.set(key, value, visibility)
```

**上下文污染防护**:

```python
class ContextIsolation:
    def __init__(self):
        self.context_namespaces = {}
    
    def create_isolated_context(self, agent_id, task_id):
        """创建隔离的上下文命名空间"""
        namespace = f"{agent_id}:{task_id}"
        self.context_namespaces[namespace] = Context()
        return namespace
    
    def add_to_context(self, namespace, content, tags=None):
        """添加内容到隔离上下文"""
        context = self.context_namespaces[namespace]
        context.add(content, tags)
    
    def get_relevant_context(self, agent_id, query):
        """获取相关上下文，避免污染"""
        # 1. 优先私有上下文
        private = self.get_private_context(agent_id, query)
        
        # 2. 有控制地获取共享上下文
        shared = self.get_shared_context(query, agent_id)
        
        # 3. 合并时添加来源标记
        return self.merge_with_provenance(private, shared)
```

**工具调用隔离**:
```python
class ToolExecutionContext:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.tool_history = []
        self.state_snapshot = {}
    
    def execute_tool(self, tool_name, params):
        # 1. 记录调用前状态
        pre_state = self.capture_state()
        
        # 2. 执行工具
        result = tool.execute(params)
        
        # 3. 记录调用后状态
        post_state = self.capture_state()
        
        # 4. 验证状态变化符合预期
        if not self.validate_state_change(pre_state, post_state):
            self.rollback(pre_state)
            raise ToolExecutionError("Unexpected state change")
        
        return result
```

---

### Q17: 如何衡量 Agent 的 Planning 能力 vs Hallucination Rate？请列举具体的量化评估指标或自动化评估框架。

**A:** 评估指标体系：

**Planning 能力指标**:

| 指标 | 定义 | 计算方式 |
|------|------|----------|
| **计划完成率** | 成功完成的计划步骤比例 | completed_steps / total_steps |
| **计划效率** | 实际步骤数 / 最优步骤数 | actual_steps / optimal_steps |
| **重规划次数** | 需要调整计划的次数 | replan_count |
| **任务成功率** | 最终完成任务的比例 | success_count / total_tasks |
| **平均执行时间** | 从计划到完成的时间 | avg(execution_time) |
| **依赖正确率** | 正确识别步骤依赖的比例 | correct_deps / total_deps |

**Hallucination Rate 指标**:

| 指标 | 定义 | 计算方式 |
|------|------|----------|
| **事实错误率** | 陈述中可验证错误的比例 | false_claims / total_claims |
| **引用准确率** | 引用来源与实际一致的比例 | correct_citations / total_citations |
| **工具调用真实性** | 声称执行 vs 实际执行 | verified_calls / claimed_calls |
| **数字准确率** | 数字信息的准确比例 | correct_numbers / total_numbers |
| **自洽性得分** | 输出内部无矛盾的比例 | consistent_outputs / total_outputs |

**自动化评估框架**:

```python
class AgentEvaluator:
    def __init__(self):
        self.metrics = {}
    
    def evaluate_planning(self, task, execution_trace):
        """评估 Planning 能力"""
        plan = execution_trace.plan
        executed = execution_trace.executed
        
        metrics = {
            "completion_rate": len(executed) / len(plan),
            "efficiency": self.calculate_optimal_ratio(task, executed),
            "replan_count": execution_trace.replan_events,
            "success": self.verify_task_completion(task, executed),
        }
        return metrics
    
    def evaluate_hallucination(self, output, ground_truth=None):
        """评估幻觉率"""
        metrics = {}
        
        # 1. 事实核查 (如果有 ground truth)
        if ground_truth:
            metrics["fact_accuracy"] = self.fact_check(output, ground_truth)
        
        # 2. 引用验证
        metrics["citation_accuracy"] = self.verify_citations(output)
        
        # 3. 自洽性检查
        metrics["consistency"] = self.check_self_consistency(output)
        
        # 4. 工具调用验证
        metrics["tool_call_authenticity"] = self.verify_tool_calls(output)
        
        return metrics
    
    def aggregate_score(self, planning_metrics, hallucination_metrics):
        """综合评分"""
        planning_score = np.mean(list(planning_metrics.values()))
        hallucination_score = 1 - np.mean(list(hallucination_metrics.values()))
        
        # 加权综合
        total_score = 0.6 * planning_score + 0.4 * hallucination_score
        return total_score
```

**评估数据集**:

- **AgentBench**: 多任务 Agent 评估
- **WebArena**: Web 操作 Agent 评估
- **GAIA**: 通用 Agent 能力评估
- **SWE-bench**: 软件工程任务评估

---

## 八、GraphRAG 与高级检索

### Q18: GraphRAG 在处理 Agent 复杂关联查询时的优势在哪里？

**A:** GraphRAG vs 传统 RAG:

| 维度 | 传统 RAG | GraphRAG |
|------|----------|----------|
| **检索单元** | 文本块 (Chunk) | 实体 + 关系 |
| **关联发现** | 语义相似度 | 图遍历 |
| **多跳推理** | 困难 | 天然支持 |
| **可解释性** | 低 | 高 (可展示推理路径) |
| **知识融合** | 困难 | 容易 (实体对齐) |

**GraphRAG 优势**:

**1. 多跳查询能力**
```
查询："A 公司的竞争对手的主要产品是什么？"

传统 RAG: 难以关联 A 公司 → 竞争对手 → 产品
GraphRAG: A 公司 -[competitor]→ B 公司 -[product]→ 产品 X
```

**2. 实体消歧**
```python
# 传统 RAG 可能混淆
"Apple" → 水果？公司？

# GraphRAG 通过图结构消歧
"Apple" -[type]→ Company
"Apple" -[founder]→ Steve Jobs
→ 确定是公司
```

**3. 隐含关系发现**
```python
# 通过图算法发现隐含关系
common_competitors = graph.find_common_neighbors(company_a, company_b)
if len(common_competitors) > threshold:
    # A 和 B 可能是竞争对手
    infer_competitive_relationship(company_a, company_b)
```

**4. 社区发现**
```python
# 发现相关实体群组
communities = graph.louvain_community_detection()
# 同一社区内的实体高度相关
```

**GraphRAG 实现架构**:
```
文档 → 实体抽取 → 关系抽取 → 知识图谱构建
                           ↓
查询 → 实体链接 → 图遍历 → 子图提取 → 生成答案
```

---

## 九、综合设计题

### Q19: 设计一个智能导购助手 Agent？描述其感知、规划、记忆和执行四大模块在分布式架构下的协同逻辑。

**A:** 智能导购 Agent 系统设计：

**整体架构**:
```
┌─────────────────────────────────────────────────────────────────┐
│                        API Gateway                              │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                     Load Balancer                               │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
        ┌────────────────────┼────────────────────┐
        ↓                    ↓                    ↓
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Agent Node 1 │   │  Agent Node 2 │   │  Agent Node N │
│  ┌─────────┐  │   │  ┌─────────┐  │   │  ┌─────────┐  │
│  │Perception│  │   │  │Perception│  │   │  │Perception│  │
│  └────┬────┘  │   │  └────┬────┘  │   │  └────┬────┘  │
│  ┌────┴────┐  │   │  ┌────┴────┐  │   │  ┌────┴────┐  │
│  │Planning │  │   │  │Planning │  │   │  │Planning │  │
│  └────┬────┘  │   │  └────┬────┘  │   │  └────┬────┘  │
│  ┌────┴────┐  │   │  ┌────┴────┐  │   │  ┌────┴────┐  │
│  │Execution│  │   │  │Execution│  │   │  │Execution│  │
│  └────┬────┘  │   │  └────┬────┘  │   │  └────┬────┘  │
│  ┌────┴────┐  │   │  ┌────┴────┐  │   │  ┌────┴────┐  │
│  │ Memory  │  │   │  │ Memory  │  │   │  │ Memory  │  │
│  └─────────┘  │   │  └─────────┘  │   │  └─────────┘  │
└───────────────┘   └───────────────┘   └───────────────┘
        ↓                    ↓                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Message Queue (Kafka)                      │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
        ┌────────────────────┼────────────────────┐
        ↓                    ↓                    ↓
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  User Profile │   │  Product DB   │   │  Order System │
│    Service    │   │    Service    │   │    Service    │
└───────────────┘   └───────────────┘   └───────────────┘
```

**四大模块详细设计**:

**1. 感知模块 (Perception)**
```python
class PerceptionModule:
    def __init__(self):
        self.nlp = NLPEngine()
        self.context_fetcher = ContextFetcher()
    
    def process_input(self, user_message, session_id):
        # 1. 意图识别
        intent = self.nlp.classify_intent(user_message)
        
        # 2. 槽位提取
        slots = self.nlp.extract_slots(user_message)
        
        # 3. 情感分析
        sentiment = self.nlp.analyze_sentiment(user_message)
        
        # 4. 上下文获取
        context = self.context_fetcher.get(session_id)
        
        # 5. 用户画像
        profile = self.context_fetcher.get_user_profile(session_id.user_id)
        
        return PerceptionResult(
            intent=intent,
            slots=slots,
            sentiment=sentiment,
            context=context,
            profile=profile,
            raw_input=user_message
        )
```

**2. 规划模块 (Planning)**
```python
class PlanningModule:
    def __init__(self):
        self.planner = LLMPlanner()
        self.validator = PlanValidator()
    
    def create_plan(self, perception: PerceptionResult):
        # 1. 根据意图选择规划模板
        template = self.select_template(perception.intent)
        
        # 2. LLM 生成具体计划
        plan = self.planner.generate(
            template=template,
            slots=perception.slots,
            context=perception.context,
            profile=perception.profile
        )
        
        # 3. 验证计划可行性
        if not self.validator.validate(plan):
            plan = self.repair_plan(plan)
        
        # 4. 分解为可执行步骤
        steps = self.decompose(plan)
        
        return Plan(steps=steps, metadata=plan.metadata)
```

**3. 执行模块 (Execution)**
```python
class ExecutionModule:
    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.executor = ParallelExecutor()
    
    async def execute(self, plan: Plan, session_id):
        results = []
        
        for step in plan.steps:
            # 1. 获取工具
            tool = self.tool_registry.get(step.tool_name)
            
            # 2. 准备参数
            params = self.prepare_params(step, results)
            
            # 3. 执行 (支持并行)
            if step.can_parallel:
                result = await self.executor.execute_parallel(tool, params)
            else:
                result = await tool.execute(params)
            
            # 4. 验证结果
            if not self.validate_result(result):
                result = self.handle_error(step, result)
            
            results.append(result)
            
            # 5. 更新会话状态
            self.update_session_state(session_id, step, result)
        
        return ExecutionResult(steps=results)
```

**4. 记忆模块 (Memory)**
```python
class MemoryModule:
    def __init__(self):
        self.short_term = RedisMemory()  # 短期记忆
        self.long_term = VectorMemory()   # 长期记忆
        self.profile_db = ProfileDB()     # 用户画像
    
    def store(self, session_id, interaction: Interaction):
        # 1. 短期记忆 (会话级)
        self.short_term.append(session_id, interaction)
        
        # 2. 提取长期记忆
        if self.should_store_long_term(interaction):
            summary = self.summarize(interaction)
            self.long_term.store(
                user_id=session_id.user_id,
                content=summary,
                metadata=interaction.metadata
            )
        
        # 3. 更新用户画像
        preferences = self.extract_preferences(interaction)
        if preferences:
            self.profile_db.update(session_id.user_id, preferences)
    
    def retrieve(self, session_id, query):
        # 1. 获取短期记忆
        recent = self.short_term.get_recent(session_id, limit=10)
        
        # 2. 检索长期记忆
        long_term = self.long_term.search(
            user_id=session_id.user_id,
            query=query,
            top_k=5
        )
        
        # 3. 获取用户画像
        profile = self.profile_db.get(session_id.user_id)
        
        return MemoryContext(
            recent=recent,
            long_term=long_term,
            profile=profile
        )
```

**模块协同逻辑**:

```python
class ShoppingAssistantAgent:
    def __init__(self):
        self.perception = PerceptionModule()
        self.planning = PlanningModule()
        self.execution = ExecutionModule()
        self.memory = MemoryModule()
    
    async def handle_request(self, user_message, session_id):
        # 1. 获取历史记忆
        memory_context = self.memory.retrieve(session_id, user_message)
        
        # 2. 感知理解
        perception = self.perception.process_input(
            user_message, 
            session_id,
            memory_context
        )
        
        # 3. 规划任务
        plan = self.planning.create_plan(perception)
        
        # 4. 执行计划
        execution_result = await self.execution.execute(plan, session_id)
        
        # 5. 生成回复
        response = self.generate_response(
            perception=perception,
            plan=plan,
            execution_result=execution_result
        )
        
        # 6. 存储记忆
        interaction = Interaction(
            input=user_message,
            perception=perception,
            plan=plan,
            execution_result=execution_result,
            response=response
        )
        self.memory.store(session_id, interaction)
        
        return response
```

**分布式协同关键点**:

1. **状态同步**: 通过 Redis 共享会话状态
2. **消息队列**: Kafka 处理异步任务 (如推荐更新、画像计算)
3. **负载均衡**: 根据会话 ID 一致性哈希路由到同一 Agent Node
4. **缓存层**: 商品数据、用户画像多级缓存
5. **熔断降级**: 下游服务不可用时的降级策略

---

## 十、快速参考表

### 核心公式与阈值

| 场景 | 推荐值/公式 |
|------|-------------|
| 上下文窗口分配 | 系统指令 10% + 关键事实 20% + 最近对话 50% + 摘要 20% |
| 澄清置信度阈值 | 关键信息 >0.8, 非关键 >0.5 |
| 工具路由召回数 | 向量 30 + 关键词 20 + 类别 20 → 精排 Top 5 |
| 循环检测窗口 | 5-10 轮 |
| 最大迭代次数 | 10-15 次 |
| 缓存 TTL | 热点数据 5min, 一般数据 30min |
| 并行工具数 | 3-5 个 (避免过载) |

### 常用评估指标

```
Planning Score = 0.3×完成率 + 0.3×成功率 + 0.2×效率 + 0.2×重规划质量
Hallucination Rate = (事实错误 + 伪造引用 + 虚假工具调用) / 总陈述数
Overall Agent Score = 0.6×Planning - 0.4×Hallucination
```

---

**最后更新**: 2026-03-18
**维护**: 🦐 小虾
