# CV SOTA 论文速递 (2026-03-04)

> 搜索来源：arXiv, CVPR/ICCV/ECCV 2025-2026, Google Scholar

---

## 1️⃣ 语义分割 (Semantic Segmentation)

### ① Understanding Personal Concept in Open-Vocabulary Semantic Segmentation
- **Venue**: ICCV 2025
- **链接**: https://openaccess.thecvf.com/content/ICCV2025/html/Park_Understanding_Personal_Concept_in_Open-Vocabulary_Semantic_Segmentation_ICCV_2025_paper.html
- **摘要**: 提出个性化开放词汇语义分割任务，基于文本提示调优的插件方法，解决用户自定义概念的分割问题。

### ② SemiDAViL: Semi-supervised Domain Adaptation with Vision-Language Guidance
- **Venue**: CVPR 2025
- **链接**: https://openaccess.thecvf.com/content/CVPR2025/html/Basak_SemiDAViL_Semi-supervised_Domain_Adaptation_with_Vision-Language_Guidance_for_Semantic_Segmentation_CVPR_2025_paper.html
- **摘要**: 首个语言引导的半监督域适应语义分割方法，利用视觉 - 语言模型的语义泛化能力。

### ③ Weakly Supervised Semantic Segmentation via Progressive Refinement
- **Venue**: CVPR 2025
- **链接**: https://cvpr.thecvf.com/virtual/2025/poster/32410
- **摘要**: 弱监督语义分割新进展，通过渐进式优化策略有效降低标注成本。

### ④ MixerCSeg: Efficient Mixer Architecture for Crack Segmentation
- **Venue**: CVPR 2026
- **链接**: https://github.com/Paper2Chinese/CVPR-2026-reading-papers-with-code
- **摘要**: 基于解耦 Mamba 注意力的高效裂缝分割架构，适用于工业检测场景。

---

## 2️⃣ 视频分割 (Video Segmentation)

### ① VidSeg: Training-free Video Semantic Segmentation based on Diffusion Models
- **Venue**: CVPR 2025
- **链接**: https://openaccess.thecvf.com/content/CVPR2025/html/Wang_VidSeg_Training-free_Video_Semantic_Segmentation_based_on_Diffusion_Models_CVPR_2025_paper.html
- **摘要**: 基于扩散模型的免训练视频语义分割方法，利用预训练扩散模型实现零样本迁移。

### ② Segment Any Motion in Videos
- **Venue**: CVPR 2025
- **链接**: https://cvpr.thecvf.com/virtual/2025/poster/32979
- **摘要**: 结合长程轨迹运动线索与 DINO 语义特征，利用 SAM2 实现运动物体分割。

### ③ EntitySAM: Segment Everything in Video
- **Venue**: CVPR 2025
- **链接**: https://cvpr.thecvf.com/virtual/2025/poster/32400
- **摘要**: 引入实体解码器促进物体间通信，使用可学习对象查询的自动提示生成器。

### ④ M3-VOS: Multi-Phase Multi-Transition Multi-Scenery Video Object Segmentation
- **Venue**: CVPR 2025
- **链接**: https://openaccess.thecvf.com/content/CVPR2025/html/Chen_M3-VOS_Multi-Phase_Multi-Transition_and_Multi-Scenery_Video_Object_Segmentation_CVPR_2025_paper.html
- **摘要**: 引入"阶段"概念，根据视觉特征和运动模式对真实世界物体进行分类分割。

---

## 3️⃣ 图像分类 (Image Classification)

### ① Decoding Vision Transformer Variations for Image Classification
- **Venue**: ScienceDirect / Elsevier 2026
- **链接**: https://www.sciencedirect.com/science/article/pii/S2666827026000095
- **摘要**: 综合基准测试 22 种 ViT 和混合 CNN-ViT 模型，建立统一分类体系，识别混合架构在效率和精度上的最佳平衡。

### ② Disentangling Visual Transformers: Patch-level Interpretability
- **Venue**: CVPR 2025 Workshop
- **链接**: https://openaccess.thecvf.com/content/CVPR2025W/XAI4CV/html/Jeanneret_Disentangling_Visual_Transformers_Patch-level_Interpretability_for_Image_Classification_CVPRW_2025_paper.html
- **摘要**: 解决 ViT 可解释性问题，提出 patch 级别的可解释性方法，在保持性能的同时提升模型透明度。

### ③ Vision Transformers 2026: State of the Art & Business Impact
- **Venue**: Industry Report 2026
- **链接**: https://medium.com/@API4AI/vision-transformers-2026-state-of-the-art-business-impact-4b1e216c6b86
- **摘要**: ViT 在 2026 年已在工业界广泛应用，PEFT(LoRA 等) 技术使企业能够低成本微调定制模型，适用于制造、物流、零售等行业。

---

## 4️⃣ 人体骨架检测 (Human Pose/Skeleton Detection)

### ① PoseAnchor: Robust Root Position Estimation for 3D Human Pose Estimation
- **Venue**: ICCV 2025
- **链接**: https://openaccess.thecvf.com/content/ICCV2025/html/Kim_PoseAnchor_Robust_Root_Position_Estimation_for_3D_Human_Pose_Estimation_ICCV_2025_paper.html
- **摘要**: 提出 PoseAnchor 统一框架，通过 ITRR(迭代信任根回归) 实现零样本根节点定位，无需重新训练即可估计绝对根位置。

### ② PersPose: 3D Human Pose Estimation with Perspective Encoding
- **Venue**: ICCV 2025
- **链接**: https://openaccess.thecvf.com/content/ICCV2025/html/Hao_PersPose_3D_Human_Pose_Estimation_with_Perspective_Encoding_and_Perspective_ICCV_2025_paper.html
- **摘要**: 提出透视编码和透视旋转技术，解决裁剪图像中关节相对深度估计问题，减少透视畸变。

### ③ Detection, Pose Estimation and Segmentation for Multiple Bodies
- **Venue**: ICCV 2025
- **链接**: https://iccv.thecvf.com/virtual/2025/poster/2243
- **摘要**: 解决多人近距离场景下的人体姿态估计难题，统一检测、姿态估计和分割任务。

### ④ Global 3D Human Poses (G3P) Workshop
- **Venue**: CVPR 2026 Workshop
- **链接**: https://cvpr.thecvf.com/virtual/2025/workshop/32341
- **摘要**: 聚焦将轨迹数据融入姿态估计的创新技术，推动全局 3D 人体姿态研究。

---

## 📊 趋势总结

| 领域 | 核心趋势 |
|------|----------|
| 语义分割 | 开放词汇 + 个性化定制、视觉 - 语言多模态引导 |
| 视频分割 | 扩散模型零样本迁移、SAM2 系列扩展 |
| 图像分类 | ViT 持续主导、混合 CNN-ViT 架构兴起、可解释性增强 |
| 人体姿态 | 3D 绝对位置估计、透视畸变校正、多人场景优化 |

---

**生成时间**: 2026-03-04 17:00  
**搜索工具**: Tavily Search
