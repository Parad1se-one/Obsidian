# A Pontryagin Method of Model-based Reinforcement Learning via Hamiltonian Actor-Critic

- 来源：arXiv
- 主题：offline-rl / world-models / robust-rl / theory
- 链接：http://arxiv.org/abs/2603.28971v1
- 作者：Chengyang Gu, Yuxin Pan, Hui Xiong, Yize Chen

## 摘要
Model-based reinforcement learning (MBRL) improves sample efficiency by leveraging learned dynamics models for policy optimization. However, the effectiveness of methods such as actor-critic is often limited by compounding model errors, which degrade long-horizon value estimation. Existing approaches, such as Model-Based Value Expansion (MVE), partially mitigate this issue through multi-step rollouts, but remain sensitive to rollout horizon selection and residual model bias. Motivated by the Pontryagin Maximum Principle (PMP), we propose Hamiltonian Actor-Critic (HAC), a model-based approach that eliminates explicit value function learning by directly optimizing a Hamiltonian defined over the learned dynamics and reward for deterministic systems. By avoiding value approximation, HAC reduces sensitivity to model errors while admitting convergence guarantees. Extensive experiments on continuous control benchmarks, in both online and offline RL settings, demonstrate that HAC outperforms model-free and MVE-based baselines in control performance, convergence speed, and robustness to distributional shift, including out-of-distribution (OOD) scenarios. In offline settings with limited data, HAC matches or exceeds state-of-the-art methods, highlighting its strong sample efficiency.
