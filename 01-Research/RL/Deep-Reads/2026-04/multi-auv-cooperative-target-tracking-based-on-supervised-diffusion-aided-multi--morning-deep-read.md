以下是 昨天（2026-03-31）强化学习 / RL 方向 我整理出的最新论文与研究动态摘要：

昨天更值得关注的，不是传统 benchmark 上的局部刷分，而是 RL 继续向 agent、机器人、多智能体、世界模型和生成模型后训练这些方向扩张。整体感觉是：RL 正在从‘一个优化算法’变成‘复杂智能系统的通用后训练层’。

- 本次候选池规模：`264`
- 本次精选：`8` 篇
- 覆盖来源：`arXiv`
- 顶会/正式 venue 命中：`0` 篇

1. 昨天最值得看的 RL 新论文
- Multi-AUV Cooperative Target Tracking Based on Supervised Diffusion-Aided Multi-Agent Reinforcement Learning
  这篇论文主要在解决：In recent years, advances in underwater networking and multi-agent reinforcement learning (MARL) have significantly expanded multi-autonomous underwater vehicle (AUV) applications in marine exploration and target tracking。
  方法上看，它属于 **多智能体 RL** 路线；来源是 `arXiv`，场合/venue 是 `arXiv`。
  它的新意不只是做协同控制，而是试图把生成式或结构化先验引入多智能体真实任务。
  值得盯住，因为这条线直接关系到协同 agent、无人系统和复杂环境决策。
  它代表的更大趋势是：RL 正从训练动作策略，转向训练完整智能体闭环。
- COIN: Collaborative Interaction-Aware Multi-Agent Reinforcement Learning for Self-Driving Systems
  这篇论文主要在解决：Multi-Agent Self-Driving (MASD) systems provide an effective solution for coordinating autonomous vehicles to reduce congestion and enhance both safety and operational efficiency in future intelligent transportation systems。
  方法上看，它属于 **多智能体 RL** 路线；来源是 `arXiv`，场合/venue 是 `arXiv`。
  它的新意不只是做协同控制，而是试图把生成式或结构化先验引入多智能体真实任务。
  值得盯住，因为这条线直接关系到协同 agent、无人系统和复杂环境决策。
  它代表的更大趋势是：MARL 正在从 benchmark 走向真实世界受约束系统。
- A Pontryagin Method of Model-based Reinforcement Learning via Hamiltonian Actor-Critic
  这篇论文主要在解决：Model-based reinforcement learning (MBRL) improves sample efficiency by leveraging learned dynamics models for policy optimization。
  方法上看，它属于 **Offline RL** 路线；来源是 `arXiv`，场合/venue 是 `arXiv`。
  它的新意在于把 latent world modeling / model-based 思路继续往更复杂决策系统推进。
  值得盯住，因为世界模型仍是样本效率、规划能力和可扩展性的关键抓手。
  它代表的更大趋势是：RL 正继续和表示学习、世界建模、规划机制深度融合。
- Trojan-Speak: Bypassing Constitutional Classifiers with No Jailbreak Tax via Adversarial Finetuning
  这篇论文主要在解决：Fine-tuning APIs offered by major AI providers create new attack surfaces where adversaries can bypass safety measures through targeted fine-tuning。
  方法上看，它属于 **Safe RL** 路线；来源是 `arXiv`，场合/venue 是 `arXiv`。
  它的新意在于把 RL 从传统控制问题外溢到 agent、推理或生成模型后训练。
  值得盯住，因为 RL 正越来越像大模型/agent 的后训练基础设施。
  它代表的更大趋势是：RL 正从训练动作策略，转向训练完整智能体闭环。
- ERPO: Token-Level Entropy-Regulated Policy Optimization for Large Reasoning Models
  这篇论文主要在解决：Reinforcement learning from verifiable rewards (RLVR) has significantly advanced the reasoning capabilities of large language models。
  方法上看，它属于 **RLVR / 后训练** 路线；来源是 `arXiv`，场合/venue 是 `arXiv`。
  它的新意在于把 RL 从传统控制问题外溢到 agent、推理或生成模型后训练。
  值得盯住，因为 RL 正越来越像大模型/agent 的后训练基础设施。
  它代表的更大趋势是：RL 正从训练动作策略，转向训练完整智能体闭环。

2. 这批论文背后更大的研究信号
- 趋势 A：RL 正在和 agent / reasoning / tool use 更深度融合。
- 趋势 B：MARL、Safe RL、World Models 继续往真实系统和复杂环境推进。
- 趋势 C：RL 在机器人和生成模型里，越来越像 credit assignment / post-training 层。
- 趋势 D：真正值得盯的核心变量，不是单次分数，而是 reward、memory、skill reuse、credit assignment 这些机制。

3. 我今天最建议重点跟的 3 个信号
- Multi-AUV Cooperative Target Tracking Based on Supervised Diffusion-Aided Multi-Agent Reinforcement Learning：RL 正从训练动作策略，转向训练完整智能体闭环。
- COIN: Collaborative Interaction-Aware Multi-Agent Reinforcement Learning for Self-Driving Systems：MARL 正在从 benchmark 走向真实世界受约束系统。
- A Pontryagin Method of Model-based Reinforcement Learning via Hamiltonian Actor-Critic：RL 正继续和表示学习、世界建模、规划机制深度融合。

一句话总结：
RL 正在从“训练动作策略”升级成“训练整个智能体系统”——包括奖励、记忆、推理、技能复用和多步决策。

附：完整结构化版本已落库到 `obsidian-repo/01-Research/RL/Daily/Morning/2026-04-01-RL-文献早报.md`。
