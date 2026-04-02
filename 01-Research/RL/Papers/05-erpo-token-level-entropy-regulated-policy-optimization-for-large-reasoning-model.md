# Paper | ERPO: Token-Level Entropy-Regulated Policy Optimization for Large Reasoning Models

- arXiv: http://arxiv.org/abs/2603.28204v1
- PDF: https://arxiv.org/pdf/2603.28204v1.pdf
- 本地归档: `01-Research/RL/Sources/05-erpo-token-level-entropy-regulated-policy-optimization-for-large-reasoning-model.pdf`
- 发布时间: 2026-03-30
- 分类: rlvr, robust-rl, rl-llm, exploration
- 作者: Song Yu, Li Li
- 证据等级: 中
- 全文缓存: skills/rl-literature-pipeline/generated/fulltext/erpo-token-level-entropy-regulated-policy-optimization-for-large-reasoning-model.pdf
- 方法家族: reward-allocation
- 关注标签: rlvr, general-rl

---

## 这篇论文到底在解决什么

Reinforcement learning from verifiable rewards (RLVR) has significantly advanced the reasoning capabilities of large language models.

更具体地说，它瞄准的是一个带明确方法瓶颈的 RL 问题，而不是泛泛讲一个大方向。

---

## 核心方法

**方法主轴**  
These pivots represent the "forks in the road" where effective multi-path exploration is most crucial yet often suppressed by uniform advantage signals.

**从正文/摘要里能稳定抽到的线索**
- Problem / Intro: 1 Introduction With the advancement of large language models (LLMs), reinforcement learning has emerged as a central paradigm for post-training base models in complex agent tasks 1]. OpenAI’s [ o1 [2] demonstrates the capability of solving complex logical pro…
- Method: These pivots represent the "forks in the road" where effective multi-path exploration is most crucial yet often suppressed by uniform advantage signals.
- Experiment: experiments on competitive mathematical benchmarks (e.g., MATH, AIME) demonstrate that ERPO signi cantly outperforms GRPO. Notably, ERPO not only boosts reasoning accuracy but also yields signi cantly more concise and robust derivation paths, establishing a n…

---

## 实验到底测了什么

on competitive mathematical benchmarks (e.g., MATH, AIME) demonstrate that ERPO signi cantly outperforms GRPO. Notably, ERPO not only boosts reasoning accuracy but also yields signi cantly more concise and robust derivation paths, establishing a new ef ciency…

**任务 / Benchmark 线索**
- safe MPE
- MPE
- math reasoning

**Baseline 线索**
- GRPO
- RLOO
- rlvr

---

## 这篇论文目前可确认的贡献

- 它落在 `rlvr, general-rl` 这条主线上。
- 已经拿到全文，可继续做方法/实验判断。
- 当前证据表明，这篇至少不是纯口号文，已经有明确的问题定义、方法抓手和实验验证线索。

---

## 为什么它会进我的池子

- 来自已筛选 RL 全文候选池：arXiv
- 主题：rlvr, robust-rl, rl-llm, exploration
- 本地已有全文缓存，可按当前模板重建 DeepRead

---

## 我现在最该盯的风险点

- baseline 是否足够强、预算是否对齐。
- 提升是不是来自额外训练技巧、筛选策略或算力堆叠，而不是核心方法本身。
- 方法是否只在少数 benchmark / 任务设置上成立。
- 作者有没有主动暴露失败模式和边界条件。
- 当前风险提示：当前没在前几页看到清晰 limitations/风险讨论，先按证据不足处理，别急着吹。
- reward allocation 可能引入新的 reward hacking 路径
- 需要更多 candidate / group credit 计算

---

## 下一步动作

- 正文已拿到，但证据还不够硬，先做预精读，不要装成已经通读完。
- 如果证据等级高：优先进入 heavy deepread。
- 如果证据等级中/低：继续补全文结构化抽取，不急着下硬结论。
