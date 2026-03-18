#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
面试题目处理器和答案生成器
"""

import json
from typing import Dict, List
from datetime import datetime


class QuestionProcessor:
    """题目处理器"""
    
    def __init__(self):
        self.categories = {
            "基础概念": ["什么是", "解释", "定义", "概念", "原理"],
            "架构设计": ["架构", "设计", "组件", "模块", "系统"],
            "算法优化": ["优化", "加速", "效率", "性能", "显存"],
            "工程实践": ["部署", "实践", "工程", "落地", "生产"],
            "前沿技术": ["最新", "前沿", "趋势", "发展", "未来"],
        }
    
    def classify(self, question_text: str) -> str:
        """题目分类"""
        text_lower = question_text.lower()
        
        scores = {}
        for category, keywords in self.categories.items():
            score = sum(1 for kw in keywords if kw.lower() in text_lower)
            scores[category] = score
        
        # 返回得分最高的分类
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return "综合"


class AnswerGenerator:
    """答案生成器"""
    
    def __init__(self):
        # MVP 版本使用预设答案模板
        # 后续可以接入 LLM API 生成更详细的答案
        self.templates = self.load_templates()
    
    def load_templates(self) -> Dict:
        """加载答案模板"""
        return {
            "Transformer": {
                "keywords": ["transformer", "attention", "self-attention"],
                "answer": self._get_transformer_answer(),
            },
            "LLM 基础": {
                "keywords": ["llm", "大模型", "预训练", "微调"],
                "answer": self._get_llm_basics_answer(),
            },
            "Agent": {
                "keywords": ["agent", "reAct", "规划", "工具"],
                "answer": self._get_agent_answer(),
            },
            "优化": {
                "keywords": ["优化", "lora", "peft", "显存", "加速"],
                "answer": self._get_optimization_answer(),
            },
            "RAG": {
                "keywords": ["rag", "检索", "向量", "知识库"],
                "answer": self._get_rag_answer(),
            },
        }
    
    def generate(self, question_text: str, category: str) -> str:
        """生成答案"""
        text_lower = question_text.lower()
        
        # 匹配模板
        for template_name, template in self.templates.items():
            if any(kw in text_lower for kw in template["keywords"]):
                return template["answer"](question_text)
        
        # 默认答案
        return self._get_default_answer(question_text, category)
    
    def _get_transformer_answer(self):
        return lambda q: f"""**核心要点**：

1. **Self-Attention 机制**
   - QKV 三矩阵计算注意力权重
   - 并行计算，捕捉长距离依赖
   - 公式：Attention(Q,K,V) = softmax(QK^T/√d)V

2. **位置编码**
   - 正弦余弦位置编码或学习式位置编码
   - 解决 Transformer 无序列顺序信息问题

3. **多头注意力**
   - 多个注意力头并行，捕捉不同子空间信息
   - 增强模型表达能力

4. **LayerNorm + Residual**
   - 层归一化稳定训练
   - 残差连接缓解梯度消失

**相关论文**：
- Attention Is All You Need (Vaswani et al., 2017)

**常见追问**：
- Transformer 相比 RNN 的优势？
- 为什么用 LayerNorm 而不是 BatchNorm？
- 多头注意力的物理意义？"""

    def _get_llm_basics_answer(self):
        return lambda q: f"""**核心要点**：

1. **预训练 (Pre-training)**
   - 在大规模无标注数据上学习语言表示
   - 任务：Next Token Prediction / Masked LM
   - 学到通用语言知识和世界知识

2. **微调 (Fine-tuning)**
   - 在有标注数据上适配特定任务
   - 全量微调 vs 参数高效微调 (LoRA, Prefix Tuning)
   - 指令微调 (Instruction Tuning) 提升泛化

3. **RLHF (Reinforcement Learning from Human Feedback)**
   - 收集人类偏好数据
   - 训练奖励模型 (Reward Model)
   - PPO 优化策略对齐人类偏好

**训练流程**：
```
预训练 → SFT (监督微调) → RLHF → 部署
```

**相关论文**：
- GPT 系列论文
- InstructGPT (Ouyang et al., 2022)

**常见追问**：
- 全量微调和 LoRA 的区别？
- RLHF 的替代方案？(DPO, IPO)"""

    def _get_agent_answer(self):
        return lambda q: f"""**核心要点**：

1. **Agent 核心组件**
   - **感知 (Perception)**: 理解用户意图和环境
   - **规划 (Planning)**: 任务分解和步骤规划
   - **记忆 (Memory)**: 短期/长期记忆管理
   - **执行 (Execution)**: 工具调用和动作执行

2. **ReAct 框架**
   - Reason + Act 交替进行
   - Thought → Action → Observation 循环
   - 支持多步推理和工具使用

3. **记忆机制**
   - 短期记忆：上下文窗口
   - 长期记忆：向量数据库
   - 元记忆：用户偏好和系统配置

4. **工具调用**
   - 函数调用 (Function Calling)
   - MCP 协议标准化
   - 工具路由和负载均衡

**常见架构**：
```
用户输入 → 意图识别 → 任务规划 → 工具执行 → 结果整合 → 输出
```

**相关论文**：
- ReAct (Yao et al., 2023)
- Chain of Thought (Wei et al., 2022)

**常见追问**：
- Agent 和 Workflow 的区别？
- 如何避免 Agent 陷入循环？"""

    def _get_optimization_answer(self):
        return lambda q: f"""**核心要点**：

1. **参数高效微调 (PEFT)**
   - **LoRA**: 低秩适配器，只训练少量参数
   - **Prefix Tuning**: 学习前缀向量
   - **Adapter**: 插入小型神经网络模块

2. **显存优化**
   - **梯度检查点**: 用计算换显存
   - **混合精度训练**: FP16/BF16
   - **ZeRO**: 分片优化器状态

3. **推理加速**
   - **量化**: INT8/INT4 量化
   - **蒸馏**: 大模型→小模型
   - **推测解码**: Draft + Verify

4. **分布式训练**
   - 数据并行、模型并行、流水线并行
   - DeepSpeed, FSDP, Megatron-LM

**LoRA 原理**：
```
W' = W + ΔW = W + BA
其中 B∈R^(d×r), A∈R^(r×k), r<<d,k
```

**相关工具**：
- PEFT (HuggingFace)
- DeepSpeed
- vLLM (推理)

**常见追问**：
- LoRA 的秩 r 如何选择？
- 量化对模型性能的影响？"""

    def _get_rag_answer(self):
        return lambda q: f"""**核心要点**：

1. **RAG 流程**
   ```
   用户查询 → 检索相关文档 → 拼接上下文 → LLM 生成答案
   ```

2. **检索策略**
   - **稠密检索**: 向量相似度 (Embedding)
   - **稀疏检索**: BM25, TF-IDF
   - **混合检索**: 多路召回 + RRF 融合

3. **关键组件**
   - **Embedding 模型**: text-embedding, BGE, M3E
   - **向量数据库**: Milvus, Pinecone, Chroma
   - **重排序**: Cross-encoder reranker

4. **优化技巧**
   - Chunk 策略：固定大小 vs 语义分割
   - 多粒度检索：段落 + 文档级
   - 查询改写：HyDE, 多查询

**GraphRAG 优势**：
- 支持多跳推理
- 实体关系显式建模
- 可解释性更强

**相关论文**：
- RAG (Lewis et al., 2020)
- GraphRAG (Microsoft, 2024)

**常见追问**：
- RAG 和 Fine-tuning 如何选择？
- 如何处理检索到的矛盾信息？"""

    def _get_default_answer(self, question: str, category: str) -> str:
        """默认答案模板 - 根据问题类型生成"""
        
        # 检测问题类型并生成针对性答案
        text_lower = question.lower()
        
        # 位置编码类
        if any(x in text_lower for x in ["rope", "位置编码", "positional"]):
            return f"""**核心要点**：

1. **RoPE (Rotary Positional Embedding)**
   - 旋转位置编码，将位置信息编码为旋转矩阵
   - 保持相对位置关系，外推性更好
   - 公式：f_q(x,m) = R_m · f_q(x)

2. **优势**
   - 支持长度外推（比正弦编码更好）
   - 保持注意力分数的相对位置依赖
   - 计算高效，只需矩阵乘法

3. **应用**
   - LLaMA、PaLM 等现代 LLM 采用
   - 替代传统正弦位置编码

**相关论文**：
- RoFormer: Enhanced Transformer with Rotary Position Embedding (Su et al., 2021)

**常见追问**：
- RoPE 相比正弦编码的优势？
- 如何实现长度外推？"""

        # Flash Attention
        if any(x in text_lower for x in ["flash attention", "flash-attention"]):
            return f"""**核心要点**：

1. **优化原理**
   - IO 感知：减少 HBM 访问次数
   - 分块计算：将注意力矩阵分块处理
   - 重计算：用计算换显存

2. **性能提升**
   - 速度：2-4x 加速
   - 显存：O(n²) → O(n)

3. **实现细节**
   - 融合 softmax 和 matmul 操作
   - 利用 GPU shared memory

**相关代码**：
```python
from flash_attn import flash_attn_qkvpacked_func
output = flash_attn_qkvpacked_func(qkv, dropout_p=0.0, causal=True)
```

**相关论文**：
- FlashAttention: Fast and Memory-Efficient Exact Attention (Dao et al., 2022)

**常见追问**：
- FlashAttention 的近似误差？
- 支持哪些注意力变体？"""

        # Tokenizer
        if any(x in text_lower for x in ["tokenizer", "分词", "bpe", "wordpiece"]):
            return f"""**核心要点**：

1. **常见方案**
   - **BPE**: Byte-Pair Encoding (GPT 系列)
   - **WordPiece**: BERT 使用
   - **Unigram**: SentencePiece 默认
   - **BBPE**: Byte-level BPE (GPT-2/3)

2. **设计考虑**
   - 词表大小：32K-100K
   - 未知词处理：UNK token
   - 多语言支持

3. **影响**
   - 词表大小影响序列长度
   - 分词质量影响模型理解

**代码示例**：
```python
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("llama-2-7b")
tokens = tokenizer("Hello world", return_tensors="pt")
```

**常见追问**：
- BPE 和 WordPiece 的区别？
- 如何处理多语言分词？"""

        # MoE
        if any(x in text_lower for x in ["moe", "混合专家", "mixture of experts"]):
            return f"""**核心要点**：

1. **MoE 架构**
   - 多个专家网络并行
   - 门控网络 (Gating) 选择激活哪些专家
   - 稀疏激活：每次只用部分参数

2. **优势**
   - 参数量大但计算量小
   - 训练效率高
   - 模型容量大

3. **挑战**
   - 专家负载均衡
   - 通信开销
   - 训练稳定性

**代表模型**：
- Switch Transformer
- Mixtral 8x7B
- Grok-1

**相关论文**：
- Switch Transformers: Scaling to Trillion Parameter Models (Fedus et al., 2022)

**常见追问**：
- MoE 的负载均衡策略？
- 稀疏 MoE vs 稠密模型？"""

        # 数据清洗
        if any(x in text_lower for x in ["数据清洗", "训练数据", "数据预处理"]):
            return f"""**核心要点**：

1. **清洗流程**
   ```
   原始数据 → 去重 → 过滤 → 标准化 → 质量评分 → 最终数据集
   ```

2. **关键步骤**
   - **去重**: MinHash + LSH
   - **过滤**: 移除低质量、有毒内容
   - **标准化**: 统一格式、编码
   - **质量评分**: 启发式规则 + 模型评分

3. **工具**
   - deduplication: datasketch
   - 过滤：custom rules + classifier
   - 数据处理：Spark, Dask

**相关论文**：
- The Pile: An 800GB Dataset of Diverse Text (Gao et al., 2020)
- LLaMA: Open and Efficient Foundation Language Models

**常见追问**：
- 如何处理重复数据？
- 质量评分的标准？"""

        # Instruction Tuning
        if any(x in text_lower for x in ["instruction", "指令微调", "sft"]):
            return f"""**核心要点**：

1. **Instruction Tuning 流程**
   ```
   预训练模型 → 收集指令数据 → 监督微调 → 指令遵循能力提升
   ```

2. **数据构成**
   - 指令-回答对 (Instruction-Response)
   - 多任务覆盖：问答、写作、代码、推理
   - 数据量：1K-1M 条

3. **效果**
   - 提升zero-shot 能力
   - 更好遵循用户意图
   - 为 RLHF 打基础

**代表工作**：
- FLAN (Finetuned Language Models Are Zero-Shot Learners)
- Alpaca
- Vicuna

**常见追问**：
- Instruction Tuning 和预训练的区别？
- 数据质量如何保证？"""

        # 评估
        if any(x in text_lower for x in ["评估", "benchmark", "评测"]):
            return f"""**核心要点**：

1. **评估维度**
   - **知识**: MMLU, CMMLU
   - **推理**: GSM8K, MATH
   - **代码**: HumanEval, MBPP
   - **理解**: GLUE, SuperGLUE
   - **长文本**: Needle In A Haystack

2. **评估方法**
   - 客观题：准确率
   - 主观题：人工评分 / LLM-as-a-Judge
   - 开放式：Rouge, BLEU

3. **主流榜单**
   - LMSys Chatbot Arena
   - Open LLM Leaderboard (HuggingFace)
   - C-Eval (中文)

**常见追问**：
- LLM-as-a-Judge 的可靠性？
- 如何评估 Agent 能力？"""

        # 幻觉
        if any(x in text_lower for x in ["幻觉", "hallucination", "事实错误"]):
            return f"""**核心要点**：

1. **幻觉类型**
   - **事实错误**: 编造不存在的信息
   - **矛盾**: 前后不一致
   - **过度推断**: 超出输入范围

2. **解决方案**
   - **RAG**: 检索增强生成
   - **引用标注**: 强制标注信息来源
   - **事实核查**: 后验验证
   - **知识图谱**: 结构化知识约束

3. **评估指标**
   - 事实准确率
   - 引用准确率
   - 自洽性得分

**相关论文**：
- Survey of Hallucination in Natural Language Generation
- RAG (Lewis et al., 2020)

**常见追问**：
- RAG 如何减少幻觉？
- 如何检测模型幻觉？"""

        # 默认模板
        return f"""**回答思路**：

1. **先给结论**
   - 用 1-2 句话概括核心观点

2. **展开细节**
   - 分点阐述关键要点
   - 配合代码示例或公式

3. **举例说明**
   - 实际应用场景
   - 对比其他方案

4. **延伸讨论**
   - 相关论文/技术
   - 潜在问题和优化方向

**建议准备**：
- 复习相关基础概念
- 准备 1-2 个项目案例
- 了解最新技术动态

---
*注：此答案为模板，建议根据具体问题补充详细内容*"""
