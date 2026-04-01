# ShapE-GRPO: Shapley-Enhanced Reward Allocation for Multi-Candidate LLM Training

- 来源：arXiv
- 主题：theory / rl-llm / exploration
- 链接：http://arxiv.org/abs/2603.29871v1
- 作者：Rui Ai, Yu Pan, David Simchi-Levi, Chonghuan Wang

## 摘要
In user-agent interaction scenarios such as recommendation, brainstorming, and code suggestion, Large Language Models (LLMs) often generate sets of candidate recommendations where the objective is to maximize the collective utility of the entire set rather than individual candidates independently. However, existing reinforcement learning post-training paradigms, such as Group Relative Policy Optimization (GRPO), typically assign the same set-level scalar reward to every candidate in the set. This leads to noisy training signals where poor candidates free-ride on the high reward produced by a single strong peer, resulting in suboptimal exploration. To address this, we propose Shapley-Enhanced GRPO (ShapE-GRPO). By leveraging the permutation-invariant nature of set-level utility, we derive a Shapley-enhanced formulation from cooperative game theory to decompose set-level rewards into granular, candidate-specific signals. We show that our formulation preserves the fundamental axioms of the Shapley value while remaining computationally efficient with polynomial-time complexity. Empirically, ShapE-GRPO consistently outperforms standard GRPO across diverse datasets with accelerated convergence during training.
