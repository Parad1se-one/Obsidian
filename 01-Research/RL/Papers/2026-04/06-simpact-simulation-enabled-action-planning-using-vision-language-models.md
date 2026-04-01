# Paper | SIMPACT: Simulation-Enabled Action Planning using Vision-Language Models

- arXiv: http://arxiv.org/abs/2512.05955v2
- PDF: http://arxiv.org/pdf/2512.05955v2
- 发布时间: 2025-12-06
- 分类: cs.RO, cs.CV
- 作者: Haowen Liu, Shaoxiong Yao, Haonan Chen, Jiawei Gao, Jiayuan Mao, Jia-Bin Huang, Yilun Du

## 摘要
Vision-Language Models (VLMs) exhibit remarkable common-sense and semantic reasoning capabilities. However, they lack a grounded understanding of physical dynamics. This limitation arises from training VLMs on static internet-scale visual-language data that contain no causal interactions or action-conditioned changes. Consequently, it remains challenging to leverage VLMs for fine-grained robotic manipulation tasks that require physical understanding, reasoning, and corresponding action planning. To overcome this, we present SIMPACT, a test-time, SIMulation-enabled ACTion Planning framework that equips VLMs with physical reasoning through simulation-in-the-loop world modeling, without requiring any additional training. From a single RGB-D observation, SIMPACT efficiently constructs physics simulations, enabling the VLM to propose informed actions, observe simulated rollouts, and iteratively refine its reasoning. By integrating language reasoning with physics prediction, our simulation-enabled VLM can understand contact dynamics and action outcomes in a physically grounded way. Our method demonstrates state-of-the-art performance on five challenging, real-world rigid-body and deformable manipulation tasks that require fine-grained physical reasoning, outperforming existing general-purpose robotic manipulation models. Our results demonstrate that embedding physics understanding via efficient simulation into VLM reasoning at test time offers a promising path towards generalizable

## DeepRead
- ../DeepReads/2026-04/06-simpact-simulation-enabled-action-planning-using-vision-language-models.md
