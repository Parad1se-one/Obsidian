# DeepRead | DIAL: Decoupling Intent and Action via Latent World Modeling for End-to-End VLA

> 自动生成时间：2026-04-02 08:28 UTC+08:00

## 论文信息
- 标题：DIAL: Decoupling Intent and Action via Latent World Modeling for End-to-End VLA
- 作者：Yi Chen, Yuying Ge, Hui Zhou, Mingyu Ding, Yixiao Ge, Xihui Liu
- 发布时间：2026-03-31
- 更新时间：2026-03-31 23:02
- arXiv：http://arxiv.org/abs/2603.29844v1
- PDF：http://arxiv.org/pdf/2603.29844v1
- 全文缓存：skills/rl-literature-pipeline/generated/fulltext/dial-decoupling-intent-and-action-via-latent-world-modeling-for-end-to-end-vla.pdf
- 分类：cs.RO, cs.AI, cs.CV, cs.LG
- 关注标签：world-model / robotics
- 证据等级：中

## 入选原因
- 命中主题词：world model
- 命中主题词：robot
- arXiv 分类匹配 RL/ML/机器人/多智能体
- 最近 14 天内更新
- 本地已有全文缓存，可进入高置信预精读

## 一句话总结
这篇论文瞄准的是：The development of Vision-Language-Action (VLA) models has been significantly accelerated by pre-trained Vision-Language Models (VLMs).；核心抓手是：This paradigm underutilizes the VLM's potential in high-level decision making and introd…

## 研究问题
- The development of Vision-Language-Action (VLA) models has been significantly accelerated by pre-trained Vision-Language Models (VLMs).

## 方法抓手
- This paradigm underutilizes the VLM's potential in high-level decision making and introduces training instability, frequently degrading its rich semantic representations.

## 实验与证据
- on the RoboCasa GR1 Tabletop benchmark demonstrate that DIAL establishes a new state of the art, achieving superior performance with fewer 10 demonstrations than prior methods. Furthermore, by leveraging heterogeneous human demonstrations, DIAL learns physica…
- 风险提示：, we introduce DIAL (Decoupling Intent and Action via Latent World Modeling), a framework that bridges high-level decision making and low-level motor execution through a differentiable latent intent bottleneck. Speci ca…

## 小虾初判
- 精读优先级：中
- 推荐动作：正文已拿到，但证据还不够硬，先做预精读，不要装成已经通读完。

## 批判性盯防点
- 它到底是在解决真实瓶颈，还是只是在特定 benchmark 上重新分配 reward / 结构模块？
- baseline 是否足够强、预算是否对齐、提升是不是靠更多数据/算力/筛选策略堆出来的？
- 如果方法核心是新目标函数或训练 trick，跨任务/跨规模时会不会立刻失效？
- 论文有没有主动暴露失败案例，还是只挑最好看的结果？

## 原始摘要
The development of Vision-Language-Action (VLA) models has been significantly accelerated by pre-trained Vision-Language Models (VLMs). However, most existing end-to-end VLAs treat the VLM primarily as a multimodal encoder, directly mapping vision-language features to low-level actions. This paradigm underutilizes the VLM's potential in high-level decision making and introduces training instability, frequently degrading its rich semantic representations. To address these limitations, we introduce DIAL, a framework bridging high-level decision making and low-level motor execution through a differentiable latent intent bottleneck. Specifically, a VLM-based System-2 performs latent world modeling by synthesizing latent visual foresight within the VLM's native feature space; this foresight explicitly encodes intent and serves as the structural bottleneck. A lightweight System-1 policy then decodes this predicted intent together with the current observation into precise robot actions via l…

## 正文预览线索
- Introduction 线索：1 Introduction The development of generalist embodied agents has been signi cantly accelerated by pre-trained Vision-Language Models (VLMs)[ 1 4]. By internalizing massive semantic knowledge from the internet, VLMs provide a uni ed cognitive foundation capabl…
- Method 线索：未稳定抽到方法段。
- Experiment 线索：experiments on the RoboCasa GR1 Tabletop benchmark demonstrate that DIAL establishes a new state of the art, achieving superior performance with fewer 10 demonstrations than prior methods. Furthermore, by leveraging heterogeneous human demonstrations, DIAL le…

## 下一步
- 若证据等级为高：补 8 模块深读模板（Executive Overview → For Busy Readers）
- 若证据等级为中/低：等全文解析更完整后再升级，不要提前下重结论

## 关联记录
- Papers 卡片：待补充
- 当日摘要引用：待补充
