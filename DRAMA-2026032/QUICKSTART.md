# DRAMA 快速入门指南

> ⚡ 5 分钟快速开始训练

---

## 1️⃣ 安装依赖 (1 分钟)

```bash
cd /home/openclaw/.openclaw/workspace/DRAMA-2026032
pip install -r requirements.txt
```

### 核心依赖
- `torch` - 深度学习框架
- `numpy` - 数值计算
- `matplotlib` - 可视化
- `tensorboard` - 训练监控

---

## 2️⃣ 训练第一个模型 (3 分钟)

### 选项 A: MAPPO-RM (推荐，核心算法)

```bash
python train_mappo_easy_rm.py --episodes 100 --seed 42
```

### 选项 B: MAPPO Baseline (无 RM 对比)

```bash
python train_mappo_easy_baseline_v2.py --episodes 100 --seed 42
```

### 训练输出
```
Episode 10/100, Reward: 1234.56, Success: False
Episode 20/100, Reward: 1356.78, Success: True
...
Training completed! Model saved to checkpoints/
```

---

## 3️⃣ 查看训练结果 (1 分钟)

```bash
tensorboard --logdir runs/
```

浏览器打开：http://localhost:6006

### 关键指标
- **Episode Reward**: 越高越好
- **Success Rate**: 任务完成率
- **Completion Ratio**: 平均完成进度

---

## 4️⃣ 评估模型

```bash
python evaluate.py \
    --algo mappo \
    --model_path checkpoints/mappo_rm/mappo_rm_final.pth \
    --episodes 50
```

---

## 5️⃣ 对比分析

训练多个算法后运行：

```bash
python analyze_baselines.py
```

生成对比图表：
- `reward_comparison_easy.png` - Reward 曲线对比
- `success_rate_comparison_easy.png` - 成功率对比
- `comparison_table.md` - 性能对比表格

---

## 🎯 常用命令速查

### 训练
```bash
# 快速测试 (100 episodes)
python train_mappo_easy_rm.py --episodes 100

# 完整训练 (500 episodes)
python train_mappo_easy_rm.py --episodes 500 --seed 42

# 修改学习率
python train_mappo_easy_rm.py --lr 5e-4

# 指定实验名称
python train_mappo_easy_rm.py --exp_name my_experiment
```

### 监控
```bash
# 实时查看日志
tail -f logs/training.log

# 查看训练进度
grep "Episode" logs/training.log | tail -20
```

### 可视化
```bash
# 绘制结果图表
python plot_results.py --exp_name mappo_rm

# 对比多个实验
python plot_results.py --exp_names mappo_rm mappo_baseline
```

---

## 📊 环境难度选择

### Easy (快速测试)
```python
# 默认配置，无需修改
# 6×6 网格，2 个施工单元，~15 分钟完成 500 episodes
```

### Medium (论文实验)
```bash
# 使用 medium 配置文件
# 6×6 网格，10 个施工单元，~30 分钟完成 500 episodes
```

### Hard (待实现)
```bash
# 8×8 网格，20 个施工单元
```

---

## 🐛 常见问题

### Q: CUDA out of memory
**A**: 减小 batch_size 或使用 CPU:
```bash
python train_mappo_easy_rm.py --batch_size 32
```

### Q: 训练不收敛
**A**: 尝试调整学习率：
```bash
python train_mappo_easy_rm.py --lr 1e-4
```

### Q: 如何修改任务依赖？
**A**: 编辑 `configs/env_config.py` 中的 `task_dependencies`

---

## 📚 下一步

- 📖 详细文档：`docs/` 目录
- 🔬 实验设计：`docs/PAPER_EXPERIMENT_DESIGN.md`
- 📊 进度追踪：`docs/EXPERIMENT_PROGRESS.md`
- 🎓 算法详解：`marl/algos/` 源码注释

---

*Happy Training! 🚀*
