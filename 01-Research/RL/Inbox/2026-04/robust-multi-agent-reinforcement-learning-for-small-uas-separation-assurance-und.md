# Robust Multi-Agent Reinforcement Learning for Small UAS Separation Assurance under GPS Degradation and Spoofing

- 来源：arXiv
- 主题：marl / safe-rl / robust-rl / rl-llm
- 链接：http://arxiv.org/abs/2603.28900v1
- 作者：Alex Zongo, Filippos Fotiadis, Ufuk Topcu, Peng Wei

## 摘要
We address robust separation assurance for small Unmanned Aircraft Systems (sUAS) under GPS degradation and spoofing via Multi-Agent Reinforcement Learning (MARL). In cooperative surveillance, each aircraft (or agent) broadcasts its GPS-derived position; when such position broadcasts are corrupted, the entire observed air traffic state becomes unreliable. We cast this state observation corruption as a zero-sum game between the agents and an adversary: with probability R, the adversary perturbs the observed state to maximally degrade each agent's safety performance. We derive a closed-form expression for this adversarial perturbation, bypassing adversarial training entirely and enabling linear-time evaluation in the state dimension. We show that this expression approximates the true worst-case adversarial perturbation with second-order accuracy. We further bound the safety performance gap between clean and corrupted observations, showing that it degrades at most linearly with the corruption probability under Kullback-Leibler regularization. Finally, we integrate the closed-form adversarial policy into a MARL policy gradient algorithm to obtain a robust counter-policy for the agents. In a high-density sUAS simulation, we observe near-zero collision rates under corruption levels up to 35%, outperforming a baseline policy trained without adversarial perturbations.
