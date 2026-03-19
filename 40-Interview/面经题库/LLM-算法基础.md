# LLM 算法与基础面经

> 📅 整理时间：2026-03-19
> 📋 主题：LLM 基础、算法手撕、数据分析
> 🔖 标签：#LLM #算法 #深度学习 #面经

---

## 一、LLM 基础

### Q1: LLM 的上下文和长短期记忆是怎么做的？

### 上下文管理架构

```python
class LLMContextManager:
    def __init__(self):
        self.short_term_memory = deque(maxlen=20)  # 短期记忆
        self.long_term_memory = VectorStore(backend="milvus")  # 长期记忆
        self.semantic_memory = KeyValueStore(backend="redis")  # 语义记忆
        self.summary_memory = ""  # 摘要记忆
        
    def add_message(self, role: str, content: str):
        # 1. 加入短期记忆
        self.short_term_memory.append({
            "role": role, "content": content, "timestamp": time.time()
        })
        
        # 2. 提取关键信息到长期记忆
        if len(content) > 200:
            self._extract_to_long_term(content)
        
        # 3. 更新摘要（每 10 轮）
        if len(self.short_term_memory) % 10 == 0:
            self._update_summary()
    
    def build_context(self, max_tokens: int = 4096) -> list:
        context = []
        
        # 1. 系统提示
        context.append({"role": "system", "content": self._get_system_prompt()})
        
        # 2. 对话摘要
        if self.summary_memory:
            context.append({"role": "system", "content": f"对话摘要：{self.summary_memory}"})
        
        # 3. 最近对话（短期记忆）
        for msg in reversed(self.short_term_memory):
            if self._count_tokens(msg) > max_tokens * 0.7:
                break
            context.insert(2, msg)
        
        # 4. 相关长期记忆（向量检索）
        last_msg = self.short_term_memory[-1]["content"] if self.short_term_memory else ""
        relevant = self.long_term_memory.search(query=last_msg, k=3)
        for mem in relevant:
            context.append({"role": "system", "content": f"相关信息：{mem['content']}"})
        
        return context
```

### 长短期记忆对比

| 类型 | 存储内容 | 存储方式 | 访问速度 | 容量 |
|------|---------|---------|---------|------|
| 短期记忆 | 最近 10-20 轮对话 | 内存 (deque) | 毫秒级 | 有限 |
| 长期记忆 | 历史对话片段 | 向量数据库 | 秒级 | 大 |
| 语义记忆 | 用户画像/偏好/事实 | KV 存储 (Redis) | 毫秒级 | 中 |
| 摘要记忆 | 对话压缩摘要 | 字符串 | 毫秒级 | 小 |

---

### Q2: 讲一下你 vibe coding 做前端的策略？

### Vibe Coding 工作流

```
需求描述 → AI 生成原型 → 快速预览与反馈 → 迭代优化 → 人工精修
```

### 提示词模板

```markdown
# 前端开发 Prompt 模板

## 项目背景
{项目描述}

## 技术栈
- 框架：React 18 + TypeScript
- UI 库：Ant Design 5.x
- 状态管理：Zustand
- 构建工具：Vite

## 需求描述
{具体功能需求}

## 设计要求
- 风格：现代简洁
- 配色：主色 #1890ff
- 响应式：支持移动端

## 输出要求
1. 完整的组件代码
2. 必要的类型定义
3. 简单的使用示例
```

---

### Q3: 详细讲一下流式输出原理/应用？

### 流式输出架构

```
LLM Server
┌──────────────────────────────────────────────────────────┐
│ Token Generator                                          │
│ ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐            │
│ │Token│→ │Token│→ │Token│→ │Token│→ │Token│  ...      │
│ │  1  │  │  2  │  │  3  │  │  4  │  │  5  │            │
│ └─────┘  └─────┘  └─────┘  └─────┘  └─────┘            │
└──────────────────────────────────────────────────────────┘
         ↓         ↓         ↓         ↓         ↓
┌──────────────────────────────────────────────────────────┐
│ SSE (Server-Sent Events)                                 │
│ data: {"token": "你"}                                    │
│ data: {"token": "好"}                                    │
│ data: {"token": "，"}                                    │
│ ...                                                      │
│ data: [DONE]                                             │
└──────────────────────────────────────────────────────────┘
```

### 服务端实现 (FastAPI)

```python
@app.post("/chat/stream")
async def chat_stream(request: dict):
    async def generate_tokens(prompt: str):
        tokens = ["你", "好", "，", "我", "是", "AI", "助手"]
        for token in tokens:
            await asyncio.sleep(0.1)
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate_tokens(request.get("prompt", "")),
        media_type="text/event-stream"
    )
```

### 客户端实现 (React)

```javascript
function ChatComponent() {
  const [response, setResponse] = useState('');

  const sendMessage = async (message) => {
    const eventSource = new EventSource(`/chat/stream?prompt=${message}`);
    
    eventSource.onmessage = (event) => {
      if (event.data === '[DONE]') {
        eventSource.close();
        return;
      }
      const data = JSON.parse(event.data);
      setResponse(prev => prev + data.token);
    };
  };

  return <div className="response">{response}</div>;
}
```

---

### Q4: 如果数据维度很多，你怎么分析影响因素？

### 高维数据分析方法

```python
class HighDimensionalAnalyzer:
    def analyze(self, X: pd.DataFrame, y: pd.Series) -> dict:
        results = {}
        
        # 1. 相关性分析
        results['correlation'] = self._correlation_analysis(X, y)
        
        # 2. 特征重要性（树模型）
        results['feature_importance'] = self._tree_importance(X, y)
        
        # 3. 降维可视化
        results['pca_components'] = self._pca_analysis(X)
        
        # 4. SHAP 值分析
        results['shap_values'] = self._shap_analysis(X, y)
        
        return results
    
    def _tree_importance(self, X, y):
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        })
        return importance.sort_values('importance', ascending=False)
    
    def _shap_analysis(self, X, y):
        import shap
        model = RandomForestRegressor()
        model.fit(X, y)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)
        mean_shap = np.abs(shap_values).mean(axis=0)
        
        return pd.DataFrame({
            'feature': X.columns,
            'shap_importance': mean_shap
        }).sort_values('shap_importance', ascending=False)
```

### 分析方法对比

| 方法 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| 相关性分析 | 线性关系 | 简单快速 | 只能检测线性 |
| 树模型重要性 | 非线性关系 | 捕捉复杂交互 | 可能有偏 |
| SHAP 值 | 模型解释 | 理论完备 | 计算量大 |
| LASSO | 特征选择 | 自动稀疏化 | 线性假设 |

---

### Q5: 讲一下 CNN/RNN/LSTM？

### 三种网络架构对比

```
CNN (卷积神经网络)
输入 → [Conv] → [ReLU] → [Pool] → [Conv] → [FC] → 输出
特点：局部感知、参数共享、平移不变性
适用：图像、空间数据

RNN (循环神经网络)
x₁ → [RNN] → h₁ → y₁
         ↓
x₂ → [RNN] → h₂ → y₂
特点：序列建模、记忆能力
问题：梯度消失/爆炸、长依赖困难
适用：短序列、时间序列

LSTM (长短期记忆网络)
┌─────────────────────────────────────────────────────────┐
│ Cell State: Cₜ₋₁ ──────────────→ Cₜ                    │
│                 ↓         ↓         ↓                   │
│ 输入：xₜ ─→ [Forget] → [Input] → [Output] → hₜ         │
│        │     Gate      Gate       Gate                 │
│        └────────────→ hₜ₋₁ ────────────────────→       │
└─────────────────────────────────────────────────────────┘
特点：门控机制、长依赖建模
适用：长序列、NLP、语音
```

---

### Q6: NLP 生成时如何选择最优序列？

### 解码策略对比

| 策略 | 确定性 | 多样性 | 质量 | 适用场景 |
|------|-------|-------|------|---------|
| Greedy | 100% | 低 | 一般 | 简单任务 |
| Beam Search | 100% | 中 | 高 | 翻译/摘要 |
| Top-K | 随机 | 高 | 中高 | 创意写作 |
| Top-P | 随机 | 自适应 | 高 | 通用 |
| Temperature | 可调 | 可调 | 可调 | 通用 |

### 推荐配置

```python
# 高质量生成（翻译/摘要）
config_translation = {
    "beam_size": 5,
    "length_penalty": 0.6,
    "no_repeat_ngram_size": 3
}

# 创意写作
config_creative = {
    "top_k": 50,
    "top_p": 0.95,
    "temperature": 0.8,
    "repetition_penalty": 1.1
}

# 对话生成
config_chat = {
    "top_k": 40,
    "top_p": 0.9,
    "temperature": 0.7
}
```

---

## 二、手撕代码

### 手撕 1: 统计字符出现频率并找 TopK

```python
from collections import Counter
import heapq

def top_k_frequent_chars(s: str, k: int) -> list:
    # 方法 1: Counter + most_common
    counter = Counter(s)
    return counter.most_common(k)

def top_k_frequent_chars_heap(s: str, k: int) -> list:
    # 方法 2: 最小堆（适合 k 远小于 n）
    counter = Counter(s)
    heap = []
    for char, count in counter.items():
        if len(heap) < k:
            heapq.heappush(heap, (count, char))
        elif count > heap[0][0]:
            heapq.heapreplace(heap, (count, char))
    return sorted(heap, key=lambda x: x[0], reverse=True)
```

---

### 手撕 2: LeetCode 153 旋转数组找最小值

```python
def findMin(nums: list[int]) -> int:
    """O(log n) 二分查找"""
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = (left + right) // 2
        
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    
    return nums[left]

# 测试
print(findMin([3, 4, 5, 1, 2]))  # 输出：1
print(findMin([4, 5, 6, 7, 0, 1, 2]))  # 输出：0
```

---

### 手撕 3: SQL 统计

```sql
-- 统计每个用户的订单数量
SELECT 
    u.user_id,
    u.user_name,
    COUNT(o.order_id) AS order_count,
    SUM(o.amount) AS total_amount,
    AVG(o.amount) AS avg_amount
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.user_name
HAVING COUNT(o.order_id) > 0
ORDER BY total_amount DESC
LIMIT 10;
```

---

## 三、算法题

### 有放回组合问题（n 选 k 组合数）

```python
# 方法 1: 数学公式
from math import comb
def combinations_with_replacement(n: int, k: int) -> int:
    # 公式：C(n+k-1, k) = (n+k-1)! / (k! * (n-1)!)
    return comb(n + k - 1, k)

# 方法 2: 动态规划
def combinations_with_replacement_dp(n: int, k: int) -> int:
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # 边界条件：选 0 个只有 1 种方式
    for i in range(n + 1):
        dp[i][0] = 1
    
    # 状态转移：dp[i][j] = dp[i-1][j] + dp[i][j-1]
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    return dp[n][k]

# 方法 3: 递归 + lru_cache 优化
from functools import lru_cache

@lru_cache(maxsize=None)
def combinations_optimized(n: int, k: int) -> int:
    if k == 0:
        return 1
    if n == 0:
        return 0
    return combinations_optimized(n - 1, k) + combinations_optimized(n, k - 1)

# 测试
print(combinations_with_replacement(3, 2))  # 输出：6
# 解释：从{1,2,3}中选 2 个（可重复）：(1,1), (1,2), (1,3), (2,2), (2,3), (3,3)
```

---

**整理完成！** 🦐

---

*标签：#LLM #算法 #深度学习 #面经*
