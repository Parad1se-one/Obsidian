# DRAMA: Reward Machine-Enhanced Multi-Agent Reinforcement Learning for Collaborative Construction Tasks

> 📝 完整论文实验设计方案

---

## 🎯 论文核心贡献

1. **Reward Machine (RM) 增强框架**: 将高层任务规范集成到 MARL 训练中
2. **任务依赖感知奖励 shaping**: 基于 DAG 的任务分解和进度追踪
3. **多阶段奖励设计**: 任务完成奖励 + 协作奖励 + 进度奖励 + 效率奖励
4. **系统性实验验证**: 在 DRAMA 环境中验证有效性

---

## 📊 实验设计 (按论文章节组织)

### Section 5.1: 实验设置 (Experimental Setup)

#### 环境配置
| 难度 | 网格 | 施工单元 | 机器人 | 障碍物 | 任务复杂度 |
|------|------|----------|--------|--------|------------|
| Easy | 6×6 | 2 | 4 | 0 | 低 |
| Medium | 6×6 | 10 | 4 | 1 | 中 |
| Hard | 8×8 | 20 | 4 | 3 | 高 |

#### 评估指标
- **Episode Reward**: 每轮总奖励
- **Success Rate**: 任务完成率
- **Completion Ratio**: 平均完成进度
- **Sample Efficiency**: 达到收敛的步数
- **Training Time**: 训练耗时

---

### Section 5.2: 主实验 (Main Results)

**RQ1: RM 增强是否提升 MARL 性能？**

| 实验组 | 算法 | 难度 | Episodes | Seed | 状态 |
|--------|------|------|----------|------|------|
| **Baseline-1** | MAPPO | Easy | 500 | 42 | 🟢 运行中 |
| **Baseline-2** | IPPO | Easy | 500 | 42 | ⏳ 待运行 |
| **Baseline-3** | QMIX | Easy | 500 | 42 | ⏳ 待运行 |
| **Ours-1** | MAPPO-RM | Easy | 500 | 42 | ✅ 已完成 |
| **Ours-2** | MAPPO-RM | Medium | 500 | 42 | 🟢 运行中 |
| **Ours-3** | MAPPO-RM | Hard | 500 | 42 | ⏳ 待运行 |

**预期结果**: MAPPO-RM 在所有难度下均优于 Baseline

---

### Section 5.3: 消融实验 (Ablation Studies)

**RQ2: RM 各组件的贡献？**

| 实验组 | 任务完成奖励 | 协作奖励 | 进度奖励 | 效率奖励 | 预期影响 |
|--------|--------------|----------|----------|----------|----------|
| **Ablation-1** | ✅ | ❌ | ❌ | ❌ | 基础任务完成 |
| **Ablation-2** | ✅ | ✅ | ❌ | ❌ | +协作效应 |
| **Ablation-3** | ✅ | ✅ | ✅ | ❌ | +进度引导 |
| **Ablation-4 (Full)** | ✅ | ✅ | ✅ | ✅ | 完整 RM |

**实验配置**:
- 难度：Easy (快速验证)
- Episodes: 300
- Seed: 42, 123, 456 (3 种子取平均)

---

### Section 5.4: 敏感性分析 (Sensitivity Analysis)

**RQ3: 超参数对性能的影响？**

| 参数 | 取值范围 | 默认值 | 测试点 |
|------|----------|--------|--------|
| Learning Rate | [1e-5, 1e-3] | 3e-4 | 1e-4, 3e-4, 5e-4 |
| Rollout Length | [100, 1000] | 200 | 200, 400, 600 |
| γ (折扣因子) | [0.9, 0.99] | 0.99 | 0.95, 0.99 |
| RM 奖励权重 | [0.5, 2.0] | 1.0 | 0.5, 1.0, 2.0 |

---

### Section 5.5: 多随机种子验证 (Robustness Check)

**RQ4: 结果的统计显著性？**

| 算法 | Seed-1 (42) | Seed-2 (123) | Seed-3 (456) | Mean ± Std |
|------|-------------|--------------|--------------|------------|
| MAPPO | 🟢 运行中 | ⏳ | ⏳ | - |
| MAPPO-RM | ✅ 已完成 | ⏳ | ⏳ | - |

**统计检验**: t-test (p < 0.05 为显著)

---

### Section 5.6: 定性分析 (Qualitative Analysis)

**RQ5: RM 如何影响智能体行为？**

1. **轨迹可视化**: 对比 Baseline vs RM 的行动轨迹
2. **任务进度对比**: 各阶段完成时间
3. **协作模式分析**: 智能体间的协作频率
4. **RM 状态转移**: 奖励机器状态变化统计

---

## 📈 论文图表清单

### Figure 1: 方法框架图
- Reward Machine 与 MARL 的集成架构
- 任务依赖 DAG 示例
- 奖励信号流向

### Figure 2: 主实验结果 (Reward 曲线)
- 3 难度 × 4 算法 = 12 条曲线
- 滑动平均平滑 (window=20)
- 阴影表示 ±1 std (多种子)

### Figure 3: 成功率对比
- 累积成功率曲线
- 最终成功率柱状图

### Figure 4: 消融实验结果
- 各组件贡献的柱状图
- 学习曲线对比

### Figure 5: 敏感性分析热力图
- 参数 × 性能 热力图
- 最优参数区域高亮

### Figure 6: 定性分析案例
- 典型 episode 的轨迹可视化
- RM 状态转移时间线

---

## 📋 实验执行顺序

### Phase 1: 主实验 (优先级：高)
```bash
# 1.1 MAPPO Baseline - Easy (运行中)
python3 train_mappo_easy_baseline_v2.py --episodes 500 --seed 42

# 1.2 IPPO Baseline - Easy (待运行)
python3 train_ippo_easy.py --episodes 500 --seed 42

# 1.3 QMIX Baseline - Easy (待运行)
python3 train_qmix_easy.py --episodes 500 --seed 42

# 1.4 MAPPO-RM - Medium (运行中)
python3 train_mappo_medium_rm_optimized.py --episodes 500 --seed 42

# 1.5 MAPPO-RM - Hard (待创建配置后运行)
```

### Phase 2: 消融实验 (优先级：中)
```bash
# 2.1 完整 RM (已有)
python3 train_mappo_easy_rm.py --episodes 300 --seed 42

# 2.2 无协作奖励
python3 train_mappo_easy_rm_ablation.py --ablation no_collab --episodes 300

# 2.3 无进度奖励
python3 train_mappo_easy_rm_ablation.py --ablation no_progress --episodes 300

# 2.4 仅任务完成奖励
python3 train_mappo_easy_rm_ablation.py --ablation task_only --episodes 300
```

### Phase 3: 敏感性分析 (优先级：中)
```bash
# 3.1 学习率敏感性
python3 sensitivity_analysis.py --param lr --values 1e-4 3e-4 5e-4

# 3.2 Rollout 长度敏感性
python3 sensitivity_analysis.py --param rollout --values 200 400 600
```

### Phase 4: 多种子验证 (优先级：高)
```bash
# 4.1 MAPPO 多种子
for seed in 42 123 456; do
    python3 train_mappo_easy_baseline_v2.py --episodes 500 --seed $seed
done

# 4.2 MAPPO-RM 多种子
for seed in 42 123 456; do
    python3 train_mappo_easy_rm.py --episodes 500 --seed $seed
done
```

---

## 📊 自动生成分析内容

### 实验完成后自动生成:

1. **实验结果摘要** (`results_summary.md`)
   - 表格汇总所有实验
   - 关键发现高亮

2. **统计分析** (`statistical_analysis.md`)
   - t-test 结果
   - 效应量 (Cohen's d)
   - 置信区间

3. **图表集** (`figures/`)
   - 所有论文图表 (PDF/PNG)
   - 可编辑源文件 (matplotlib .fig)

4. **Discussion 草稿** (`discussion_draft.md`)
   - 主要发现
   - 与预期对比
   - 局限性分析
   - 未来工作

5. **完整论文草稿** (`paper_draft/`)
   - Abstract
   - Introduction
   - Method
   - Experiments
   - Results & Discussion
   - Conclusion
   - References

---

## ⏰ 时间估算

| Phase | 实验数量 | 单实验时长 | 总时长 | 预计完成 |
|-------|----------|------------|--------|----------|
| Phase 1 (主实验) | 5 | 15-30 min | ~2h | 今晚 |
| Phase 2 (消融) | 4 | 10 min | ~40 min | 明早 |
| Phase 3 (敏感性) | 6 | 10 min | ~1h | 明早 |
| Phase 4 (多种子) | 6 | 15 min | ~1.5h | 明晚 |
| **总计** | **21** | - | **~5h** | **2 天** |

---

## 🎯 论文目标会议/期刊

### 首选
- **AAMAS 2026** (Multi-Agent Systems)
- **ICML 2026** (Machine Learning)
- **NeurIPS 2026** (ML/AI)

### 备选
- **AAAI 2026** (AI)
- **IJCAI 2026** (AI)
- **AAMAS Journal** (Autonomous Agents and Multi-Agent Systems)

---

## 📝 下一步行动

### 立即执行 (今晚)
1. ✅ 等待 MAPPO Baseline 完成 (~23:00)
2. ✅ 等待 MAPPO-RM Medium 完成 (~23:30)
3. ⏳ 启动 IPPO 和 QMIX Baseline
4. ⏳ 启动多随机种子实验

### 明天执行
1. 创建消融实验脚本
2. 创建敏感性分析脚本
3. 运行 Hard 难度实验
4. 生成初步分析结果

### 后天执行
1. 整理所有实验数据
2. 生成论文图表
3. 撰写 Results & Discussion
4. 完整论文初稿

---

*最后更新：2026-03-09 22:45*  
*维护者：小虾 🦐*
