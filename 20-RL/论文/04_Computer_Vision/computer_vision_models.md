# 计算机视觉主流模型整理

> 整理时间：2026-02-27  
> 涵盖：图像分类、图像分割、目标检测

---

## 一、图像分类模型 (Image Classification)

### 1. Vision Transformer (ViT) 系列

#### ViT (Vision Transformer, 2020)
- **机理**：将图像切分为固定大小的 patch，线性嵌入后输入 Transformer Encoder
- **架构**：Patch Embedding + Position Embedding + Transformer Encoder (Multi-Head Self-Attention + MLP) + Classification Head
- **优势**：
  - 全局感受野，能捕捉长距离依赖
  - 在大规模数据上预训练后性能卓越
  - 架构简洁，易于扩展
- **劣势**：
  - 需要大量数据预训练，小数据集表现不佳
  - 计算复杂度高 O(n²)
  - 缺少归纳偏置（平移不变性、局部性）

#### DeiT (Data-efficient Image Transformers, 2021)
- **机理**：引入蒸馏 token，通过知识蒸馏从 CNN 教师模型学习
- **架构**：ViT 基础 + Distillation Token
- **优势**：
  - 在中等规模数据集上也能训练好
  - 训练效率高于 ViT
- **劣势**：需要教师模型

#### DeiT-III / DeiT-T (2022-2023)
- **改进**：更好的训练策略、数据增强、正则化
- **优势**：性能接近或超越同规模 CNN

#### ViT-22B (2023)
- **规模**：22B 参数，当时最大视觉模型
- **优势**：大规模下性能 SOTA
- **劣势**：资源需求极高

---

### 2. ConvNeXt 系列 (2022-2024)

#### ConvNeXt (2022)
- **机理**：用 Transformer 设计思想改造 ResNet
- **架构改进**：
  - 大卷积核 (7×7 depthwise conv)
  - Inverted Bottleneck 结构
  - LayerNorm 替代 BatchNorm
  - 更少的激活函数
- **优势**：
  - CNN 架构，训练效率高
  - 性能匹敌 ViT
  - 保留 CNN 的归纳偏置
- **劣势**：感受野仍受限于卷积核

#### ConvNeXt V2 (2023)
- **改进**：
  - Global Response Normalization (GRN)
  - 全卷积设计，支持任意分辨率输入
- **优势**：性能进一步提升，效率更高

#### ConvNeXt V3 (2024)
- **改进**：更高效的架构设计
- **优势**：在效率和精度间取得更好平衡

---

### 3. EfficientNet 系列

#### EfficientNet V1 (2019)
- **机理**：复合缩放 (Compound Scaling) - 同时缩放深度、宽度、分辨率
- **架构**：MBConv (Mobile Inverted Bottleneck Convolution) + SE 注意力
- **优势**：
  - 参数量和计算量极小
  - 移动端友好
  - 精度-效率平衡优秀
- **劣势**：在大规模数据上不如 ViT

#### EfficientNet V2 (2021)
- **改进**：
  - Fused-MBConv (早期层)
  - 渐进式学习策略
- **优势**：训练速度提升 11 倍，参数减少 6.8 倍

---

### 4. Swin Transformer 系列

#### Swin Transformer (2021)
- **机理**：层次化 Transformer，引入移位窗口 (Shifted Window)
- **架构**：
  - Patch Merging 下采样
  - Window-based Self-Attention (局部窗口)
  - Shifted Window 连接不同窗口
- **优势**：
  - 计算复杂度线性 O(n)
  - 层次化特征，适合下游任务（检测、分割）
  - 全局+局部信息兼顾
- **劣势**：窗口大小固定，跨窗口依赖有限

#### Swin Transformer V2 (2022)
- **改进**：
  - 预训练分辨率与微调分辨率解耦
  - Post-LayerNorm 设计
- **优势**：支持更高分辨率，训练更稳定

---

### 5. 其他重要模型

#### ResNet (2015) - 经典基准
- **架构**：残差连接，解决梯度消失
- **地位**：CNN 时代里程碑，仍广泛使用

#### MobileNet 系列 (V1/V2/V3/V4)
- **特点**：深度可分离卷积，极致轻量化
- **应用**：移动端、嵌入式设备

#### MLP-Mixer (2021)
- **机理**：纯 MLP 架构，无注意力、无卷积
- **架构**：Token-mixing MLP + Channel-mixing MLP
- **优势**：架构极简，硬件友好
- **劣势**：性能略逊于 ViT

---

## 二、图像分割模型 (Image Segmentation)

### 1. SAM 系列 (Segment Anything)

#### SAM (Segment Anything Model, 2023)
- **机理**：提示驱动 (promptable) 的通用分割模型
- **架构**：
  - Image Encoder: ViT-H/16 提取图像特征
  - Prompt Encoder: 编码点、框、掩码提示
  - Mask Decoder: 轻量级解码器生成分割掩码
- **优势**：
  - Zero-shot 泛化能力强
  - 支持多种提示方式（点、框、文本）
  - SA-1B 数据集规模空前
- **劣势**：
  - 不能分割特定类别（需要提示）
  - 模型较大，推理速度慢
  - 对细小物体分割效果一般

#### SAM 2 (2024)
- **改进**：
  - 支持视频分割（时序一致性）
  - 记忆机制追踪物体
- **优势**：视频场景 SOTA

---

### 2. MaskFormer / Mask2Former 系列

#### MaskFormer (2021)
- **机理**：将分割任务重新定义为集合预测问题
- **架构**：
  - Backbone (ResNet/Swin) 提取特征
  - Transformer Decoder 生成 mask embeddings
  - 二分图匹配 (Hungarian) 优化
- **优势**：统一语义/实例分割框架
- **劣势**：训练复杂度高

#### Mask2Former (2022)
- **改进**：
  - Masked Attention 机制
  - 支持全景、语义、实例分割统一框架
- **优势**：
  - 多任务 SOTA
  - 架构简洁统一
- **劣势**：计算开销较大

---

### 3. SegFormer 系列

#### SegFormer (2021)
- **机理**：层次化 Transformer + 轻量级解码器
- **架构**：
  - Encoder: MiT (Mix Transformer) 层次化特征
  - Decoder: 简单的 MLP 融合多尺度特征
- **优势**：
  - 无需位置编码
  - 效率高，速度快
  - 支持多分辨率输入
- **劣势**：全局建模能力弱于纯 Transformer

#### SegFormer V2 / 后续改进
- **改进**：更好的训练策略、数据增强

---

### 4. DeepLab 系列 (经典 CNN)

#### DeepLab V3+ (2018)
- **机理**：空洞卷积 + 多尺度上下文 + 解码器细化
- **架构**：
  - ASPP (Atrous Spatial Pyramid Pooling)
  - Encoder-Decoder 结构
- **优势**：
  - 边界分割质量好
  - 成熟稳定，工业界广泛使用
- **劣势**：
  - 感受野有限
  - 被 Transformer 方法超越

---

### 5. 其他重要模型

#### U-Net (2015) - 医学图像经典
- **架构**：对称 Encoder-Decoder + 跳跃连接
- **应用**：医学图像分割事实标准

#### Segmenter (2021)
- **机理**：纯 Transformer 分割，引入 mask transformers
- **优势**：全局上下文建模

#### OneFormer (2023)
- **改进**：统一语义、实例、全景分割的单一模型
- **优势**：多任务统一框架

---

## 三、目标检测模型 (Object Detection)

### 1. YOLO 系列 (You Only Look Once)

#### YOLOv5 (2020)
- **架构**：
  - Backbone: CSPDarknet
  - Neck: PAN-FPN
  - Head: 解耦头
- **优势**：
  - 推理速度极快
  - 工程化成熟，生态完善
  - 易于部署
- **劣势**：小物体检测较弱

#### YOLOv6 (2022)
- **改进**：
  - RepVGG 风格 Backbone
  - 更高效的结构重参数化
- **优势**：速度-精度平衡更好

#### YOLOv7 (2022)
- **改进**：
  - E-ELAN 架构
  - 模型缩放策略
- **优势**：同规模下精度提升

#### YOLOv8 (2023)
- **改进**：
  - Anchor-free 设计
  - 解耦头 + C2f 模块
  - 支持检测、分割、姿态估计多任务
- **优势**：
  - 当前最流行的实时检测器
  - 生态完善（Ultralytics）
- **劣势**：极端小物体检测仍有提升空间

#### YOLOv9 (2024)
- **改进**：
  - PGI (Programmable Gradient Information)
  - GELAN 架构
- **优势**：信息瓶颈问题改善

#### YOLOv10 (2024)
- **改进**：
  - 无 NMS 训练 (NMS-free training)
  - 双重标签分配策略
- **优势**：推理延迟进一步降低

---

### 2. DETR 系列 (DEtection TRansformer)

#### DETR (2020)
- **机理**：将检测视为集合预测，端到端 Transformer
- **架构**：
  - CNN Backbone (ResNet) 提取特征
  - Transformer Encoder-Decoder
  - 二分图匹配损失
- **优势**：
  - 端到端，无需 NMS、Anchor
  - 全局上下文建模
- **劣势**：
  - 收敛慢（需 500 epoch）
  - 小物体检测弱

#### Deformable DETR (2021)
- **改进**：
  - 可变形注意力 (Deformable Attention)
  - 只关注关键采样点
- **优势**：
  - 收敛快（50 epoch）
  - 高分辨率特征图友好
- **劣势**：实现复杂

#### DINO (2022)
- **改进**：
  - Contrastive Denoising
  - Mixed Query Selection
- **优势**：性能 SOTA，收敛稳定

#### RT-DETR (2023)
- **改进**：
  - 实时 DETR 设计
  - 混合编码器 (Hybrid Encoder)
- **优势**：
  - 首个实时端到端检测器
  - 速度匹敌 YOLO，精度更高
- **劣势**：生态不如 YOLO 成熟

---

### 3. 其他重要模型

#### Faster R-CNN (2015) - 经典 Two-Stage
- **架构**：RPN + ROI Align + 分类回归头
- **地位**：Two-Stage 检测器基准

#### Cascade R-CNN (2018)
- **改进**：多级级联 refinement
- **优势**：高精度，竞赛常用

#### FCOS (2019) - Anchor-free 先驱
- **机理**：像素级预测，无 Anchor
- **优势**：避免 Anchor 超参数

#### CenterNet (2019)
- **机理**：关键点检测范式
- **优势**：简洁高效

---

## 四、模型选择建议

| 任务 | 推荐模型 | 理由 |
|------|----------|------|
| **分类 - 高精度** | ViT-22B, ConvNeXt V2 | 大规模预训练，SOTA 精度 |
| **分类 - 移动端** | MobileNet V4, EfficientNet V2 | 极致效率 |
| **分类 - 平衡** | ConvNeXt, Swin Transformer | 精度效率兼顾 |
| **分割 - 通用** | SAM 2 | Zero-shot 能力强 |
| **分割 - 特定类别** | Mask2Former, SegFormer | 监督训练，类别固定 |
| **分割 - 医学** | U-Net, Swin-UNet | 领域标准 |
| **检测 - 实时** | YOLOv10, RT-DETR | 速度优先 |
| **检测 - 高精度** | DINO, Cascade R-CNN | 精度优先 |
| **检测 - 端到端** | RT-DETR, DINO | 无需 NMS |

---

## 五、趋势总结 (2024-2026)

1. **架构融合**：CNN 与 Transformer 边界模糊，互相借鉴
2. **统一框架**：单一模型支持多任务（检测 + 分割 + 姿态）
3. **实时端到端**：RT-DETR 引领无 NMS 检测趋势
4. **大模型化**：SAM 等基础模型支持 Zero-shot 泛化
5. **效率优化**：结构重参数化、蒸馏、量化成为标配

---

> ⚠️ **注**：如需获取 2025-2026 最新论文（CVPR/ICCV/ECCV 等），需配置 Brave API key 使用 web_search，或指定具体论文/仓库用 browser 访问。
