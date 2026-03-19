# AI Agent 架构设计面经

> 📅 整理时间：2026-03-19
> 📋 主题：AI Agent 系统设计与多 Agent 协作
> 🏢 公司：多 Agent 系统面试
> 🔖 标签：#Agent #架构设计 #Multi-Agent #系统设计

---

## 一、项目与自我介绍相关问题

### Q1: 语义路由怎么实现？怎么评估效果？

**实现方案：**

```python
class SemanticRouter:
    def __init__(self):
        self.embedding_model = "text-embedding-3-small"
        self.routes = {}  # 路由表：意图→处理函数
        
    def register_route(self, intent: str, handler: callable, examples: list):
        """注册路由"""
        self.routes[intent] = {
            'handler': handler,
            'embeddings': self._embed_batch(examples),
            'examples': examples
        }
    
    def route(self, query: str) -> str:
        """语义路由决策"""
        query_emb = self._embed(query)
        
        # 计算与各意图的相似度
        scores = {}
        for intent, data in self.routes.items():
            scores[intent] = cosine_similarity(query_emb, data['embeddings'].mean(axis=0))
        
        # 返回最高分意图（超过阈值）
        best_intent = max(scores, key=scores.get)
        if scores[best_intent] > 0.75:
            return best_intent
        return "default"  # 默认路由
```

**评估指标：**

| 指标 | 计算方法 | 目标值 |
|------|---------|--------|
| 准确率 | 正确路由数/总请求数 | >95% |
| 延迟 | P99 路由决策时间 | <50ms |
| 覆盖率 | 有明确意图的请求占比 | >90% |
| 人工复核率 | 需要人工干预的比例 | <5% |

---

### Q2: Skill 和 Agent 的关系？为什么不用 Skill 而用子 Agent？

**架构对比：**

```
Skill 模式 (函数式)
Agent → Skill1() → Skill2() → Skill3()
- 扁平调用
- 无状态
- 适合简单任务

子 Agent 模式 (分层式)
Parent Agent
    ↓
┌──────┐  ┌──────┐  ┌──────┐
│Child1│  │Child2│  │Child3│
│Agent │  │Agent │  │Agent │
└──────┘  └──────┘  └──────┘
- 有独立状态和记忆
- 可自主决策
- 适合复杂任务分解
```

**选择子 Agent 的原因：**

| 场景 | Skill | 子 Agent | 选择理由 |
|------|-------|----------|---------|
| 简单工具调用 | ✅ | ❌ | Skill 更轻量 |
| 复杂任务分解 | ❌ | ✅ | 子 Agent 可独立规划 |
| 需要记忆/状态 | ❌ | ✅ | 子 Agent 有独立上下文 |
| 多轮对话 | ❌ | ✅ | 子 Agent 可维护对话状态 |
| 错误隔离 | ❌ | ✅ | 子 Agent 失败不影响其他 |

---

### Q3: 上下文管理？如何避免遗忘或幻觉？

**上下文管理架构：**

```python
class ContextManager:
    def __init__(self):
        self.short_term = []  # 短期记忆（最近 N 轮）
        self.long_term = VectorStore()  # 长期记忆（向量检索）
        self.summary = ""  # 对话摘要
        self.entities = {}  # 关键实体
        
    def add_message(self, role: str, content: str):
        # 1. 加入短期记忆
        self.short_term.append({"role": role, "content": content})
        
        # 2. 提取关键信息到长期记忆
        if len(content) > 100:
            self._extract_and_store(content)
        
        # 3. 定期摘要（每 10 轮）
        if len(self.short_term) % 10 == 0:
            self.summary = self._generate_summary()
    
    def get_context(self, max_tokens: int) -> list:
        # 1. 系统提示 + 摘要
        context.append({"role": "system", "content": self.summary})
        
        # 2. 最近 N 轮对话
        context.extend(self.short_term[-5:])
        
        # 3. 相关长期记忆
        relevant = self.long_term.search(query=context[-1]["content"], k=3)
        context.append({"role": "system", "content": f"相关记忆：{relevant}"})
        
        return truncate_to_tokens(context, max_tokens)
```

**避免遗忘：**
1. 分层记忆：短期（完整）+ 长期（向量检索）+ 摘要（压缩）
2. 关键实体追踪：人名、地名、时间等单独存储
3. 定期回顾：每 N 轮对话后生成摘要

**避免幻觉：**
1. 引用溯源：所有回答必须标注信息来源
2. 置信度阈值：低于阈值时明确说"不确定"
3. 事实核查：关键信息通过工具验证
4. 边界声明：明确说明知识截止日期

---

### Q4: 多 Agent 如何实现通信？怎么协作？

**通信架构：**

```python
class AgentCommunication:
    def __init__(self):
        self.message_bus = MessageBus()  # 消息总线
        self.blackboard = Blackboard()   # 共享黑板
        self.registry = AgentRegistry()  # Agent 注册表
        
    def broadcast(self, sender: str, message: dict):
        self.message_bus.publish("global", {"from": sender, "content": message})
    
    def direct_message(self, from_agent: str, to_agent: str, message: dict):
        self.message_bus.publish(f"agent:{to_agent}", {"from": from_agent, "content": message})
    
    def write_blackboard(self, key: str, value: any, ttl: int = 3600):
        self.blackboard.set(key, value, ttl=ttl)
```

**协作模式：**

| 模式 | 描述 | 适用场景 |
|------|------|---------|
| 流水线 | Agent1→Agent2→Agent3 | 文档处理、数据清洗 |
| 投票 | 多个 Agent 输出→投票决策 | 内容审核、质量评估 |
| 主从 | Master 分配任务→Workers 执行 | 并行搜索、批量处理 |
| 黑板 | 所有 Agent 读写共享状态 | 复杂问题求解 |

---

### Q5: Agent 如何评估？有什么指标？数据集哪里来？

**评估指标体系：**

| 指标 | 说明 | 目标值 |
|------|------|--------|
| task_completion_rate | 任务完成率 | >95% |
| success_rate | 一次成功率 | >92% |
| accuracy | 答案准确率 | >94% |
| avg_latency | 平均延迟 | <1.2s |
| hallucination_rate | 幻觉率 | <2% |

**数据集来源：**
1. 公开数据集：MMLU、HumanEval、GSM8K
2. 自建数据集：历史对话日志（脱敏）、人工标注测试用例
3. 合成数据：使用更强模型生成

---

## 二、工程安全问题

### Q6: 如何防止模型输出敏感/涉密内容？

**多层防护架构：**

```
输入层防护
├─ 提示词注入检测
├─ 敏感词过滤（输入）
└─ 用户权限校验

模型层防护
├─ System Prompt 安全约束
├─ 安全微调（RLHF）
└─ 输出长度限制

输出层防护
├─ 敏感词过滤（输出）
├─ 内容分类审核
└─ 人工审核队列（可疑内容）
```

**具体实现：**

```python
class ContentSafetyFilter:
    def filter_output(self, text: str) -> tuple[bool, str]:
        # 1. 敏感词过滤
        for word in self.sensitive_words:
            text = text.replace(word, "***")
        
        # 2. 安全分类
        risk_score = self.classifier.predict(text)
        if risk_score > 0.8:
            return False, "内容风险过高"
        
        # 3. 涉密检测
        if self._detect_secret(text):
            return False, "可能包含涉密内容"
        
        return True, text
```

---

## 三、手撕代码

### Q7: Agent 调用环检测（类似力扣课程表）

```python
class AgentCallGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.max_depth = 5
        
    def has_cycle(self) -> bool:
        """检测是否有环（DFS）"""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {node: WHITE for node in self.graph}
        
        def dfs(node):
            color[node] = GRAY
            for neighbor in self.graph[node]:
                if color[neighbor] == GRAY:
                    return True
                if color[neighbor] == WHITE and dfs(neighbor):
                    return True
            color[node] = BLACK
            return False
        
        for node in self.graph:
            if color[node] == WHITE:
                if dfs(node):
                    return True
        return False
    
    def execute_with_depth_limit(self, agent: str, depth: int = 0):
        if depth > self.max_depth:
            raise RecursionError(f"超过最大调用深度 {self.max_depth}")
        
        result = self._execute_agent(agent)
        for callee in self.graph[agent]:
            child_result = self.execute_with_depth_limit(callee, depth + 1)
            result = self._merge_results(result, child_result)
        
        return result
```

---

## 四、二面问题

### Q8: 记忆管理？长上下文处理？持久化？

**记忆分层：**

| 层级 | 内容 | 存储 | 过期 |
|------|------|------|------|
| L1: Working Memory | 最近 10 轮对话 | 内存 (Redis) | 30 分钟 |
| L2: Episodic Memory | 历史对话片段 | 向量数据库 | 90 天 |
| L3: Semantic Memory | 用户画像/事实 | MySQL+ 向量 | 长期 |

---

### Q9: Skills 实现？Skills 和 MCP 区别？

**对比：**

| 特性 | Skills | MCP |
|------|--------|-----|
| 定位 | 内部函数库 | 标准化协议 |
| 调用方式 | 直接调用 | 协议通信 |
| 扩展性 | 需修改代码 | 热插拔 |
| 生态 | 私有 | 开放生态 |

---

### Q10: Planning & Solve 架构？还了解什么架构？

**架构对比：**

| 架构 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| ReAct | Reason + Act 交替 | 可解释性强 | 延迟高 |
| Reflexion | 自我反思改进 | 持续优化 | 需要多轮 |
| Chain of Thought | 逐步推理 | 简单直接 | 容易偏离 |
| Tree of Thoughts | 多路径探索 | 全局最优 | 计算量大 |

---

### Q11: 数据格式设置？包含什么元素？

```python
class AgentMessage(BaseModel):
    id: str
    timestamp: float
    sender: str
    receiver: str
    message_type: Literal["request", "response", "event"]
    content: dict
    trace_id: str  # 链路追踪
    parent_id: Optional[str]  # 父子关系
    correlation_id: str  # 关联 ID
    ttl: int = 3600
    priority: int = 5
```

---

## 五、NLP 基础

### Q12: NLP 生成时如何选择最优序列？

**解码策略对比：**

| 策略 | 确定性 | 多样性 | 适用场景 |
|------|-------|-------|---------|
| Greedy | 100% | 低 | 简单任务 |
| Beam Search | 100% | 中 | 翻译/摘要 |
| Top-K | 随机 | 高 | 创意写作 |
| Top-P | 随机 | 自适应 | 通用 |

---

**整理完成！** 🦐

---

*标签：#Agent #架构设计 #Multi-Agent #系统设计 #面经*
