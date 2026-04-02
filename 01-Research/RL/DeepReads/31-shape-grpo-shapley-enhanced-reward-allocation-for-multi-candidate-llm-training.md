# DeepRead | ShapE-GRPO: Shapley-Enhanced Reward Allocation for Multi-Candidate LLM Training

> 自动生成时间：2026-04-02 08:07 UTC+08:00

## 论文信息
- 标题：ShapE-GRPO: Shapley-Enhanced Reward Allocation for Multi-Candidate LLM Training
- 作者：Rui Ai, Yu Pan, David Simchi-Levi, Chonghuan Wang
- 发布时间：2026-03-31
- 更新时间：2026-03-31 23:24
- arXiv：http://arxiv.org/abs/2603.29871v1
- PDF：http://arxiv.org/pdf/2603.29871v1
- 全文缓存：skills/rl-literature-pipeline/generated/fulltext/shape-grpo-shapley-enhanced-reward-allocation-for-multi-candidate-llm-training.pdf
- 分类：cs.AI
- 关注标签：general-rl
- 证据等级：中

## 入选原因
- 本地已有全文缓存，可进入高置信预精读

## 一句话总结
这篇论文瞄准的是：In user-agent interaction scenarios such as recommendation, brainstorming, and code suggestion, Large Language Models (LLMs) often generate sets of candidate recommendations where…；核心抓手是：leads to a signi cant reward allocation pro…

## 研究问题
- In user-agent interaction scenarios such as recommendation, brainstorming, and code suggestion, Large Language Models (LLMs) often generate sets of candidate recommendations where…

## 方法抓手
- leads to a signi cant reward allocation problem. For example, in a brainstorming task where a model generates K ideas, a single brilliant suggestion might result in a high set-level reward. Under traditional frameworks, the remaining K 1 mediocre or poor idea…

## 实验与证据
- Empirically, ShapE-GRPO consistently outperforms standard GRPO across diverse datasets with accelerated convergence during training.
- 风险提示：discussion to Section A.1. 2 Preliminaries In this section, we brie y review the GRPO objective and the de nition of Shapley value from cooperative game theory. GRPO Algorithm. GRPO is a reinforcement learning objective…

## 小虾初判
- 精读优先级：中
- 推荐动作：正文已拿到，但证据还不够硬，先做预精读，不要装成已经通读完。

## 批判性盯防点
- 它到底是在解决真实瓶颈，还是只是在特定 benchmark 上重新分配 reward / 结构模块？
- baseline 是否足够强、预算是否对齐、提升是不是靠更多数据/算力/筛选策略堆出来的？
- 如果方法核心是新目标函数或训练 trick，跨任务/跨规模时会不会立刻失效？
- 论文有没有主动暴露失败案例，还是只挑最好看的结果？

## 原始摘要
In user-agent interaction scenarios such as recommendation, brainstorming, and code suggestion, Large Language Models (LLMs) often generate sets of candidate recommendations where the objective is to maximize the collective utility of the entire set rather than individual candidates independently. However, existing reinforcement learning post-training paradigms, such as Group Relative Policy Optimization (GRPO), typically assign the same set-level scalar reward to every candidate in the set. This leads to noisy training signals where poor candidates free-ride on the high reward produced by a single strong peer, resulting in suboptimal exploration. To address this, we propose Shapley-Enhanced GRPO (ShapE-GRPO). By leveraging the permutation-invariant nature of set-level utility, we derive a Shapley-enhanced formulation from cooperative game theory to decompose set-level rewards into granular, candidate-specific signals. We show that our formulation preserves the fundamental axioms of t…

## 正文预览线索
- Introduction 线索：1 Introduction In many user agent interaction scenarios, LLM-based agents generate multiple candidate recommendations from which users select one to execute. Examples include shopping (Li et al., 2023), summarization (Zhang et al., 2025a), brainstorming ideas…
- Method 线索：approach leads to a signi cant reward allocation problem. For example, in a brainstorming task where a model generates K ideas, a single brilliant suggestion might result in a high set-level reward. Under traditional frameworks, the remaining K 1 mediocre or…
- Experiment 线索：未稳定抽到实验段。

## 下一步
- 若证据等级为高：补 8 模块深读模板（Executive Overview → For Busy Readers）
- 若证据等级为中/低：等全文解析更完整后再升级，不要提前下重结论

## 关联记录
- Papers 卡片：待补充
- 当日摘要引用：待补充
