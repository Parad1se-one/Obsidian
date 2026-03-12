# DRAMA 难度配置实验

> 🎯 三种不同难度的建筑施工多智能体强化学习环境

---

## 📊 难度概览

| 难度 | 施工单元 | 障碍物 | 预期步数 | 复杂度 | 适用场景 |
|------|---------|--------|---------|--------|---------|
| **EASY** | 2 个 | 0 个 | ~20-40 | ⭐ 低 | 快速测试、算法验证、教学演示 |
| **MEDIUM** | 10 个 | 1 个 | ~100-200 | ⭐⭐ 中 | 中等复杂度训练、协作策略测试 |
| **HARD** | 33 个 | 3 个 | ~500-1000+ | ⭐⭐⭐ 高 | 完整训练、压力测试、最优策略研究 |

---

## 📁 文件结构

```
configs/
├── difficulty_loader.py      # 配置加载器
└── difficulty/
    ├── easy_config.py        # Easy 难度配置
    ├── medium_config.py      # Medium 难度配置
    └── hard_config.py        # Hard 难度配置
```

---

## 🚀 快速开始

### 1. 查看所有难度信息

```bash
cd /home/openclaw/.openclaw/DRAMA/DRAMA
python3 run_difficulty.py info
```

### 2. 运行难度实验

```bash
# Easy 难度 (2 个施工单元)
python3 run_difficulty.py easy

# Medium 难度 (10 个施工单元)
python3 run_difficulty.py medium

# Hard 难度 (33 个施工单元)
python3 run_difficulty.py hard
```

### 3. 自定义参数

```bash
# 指定最大步数和运行次数
python3 run_difficulty.py easy --steps 100 --runs 5
```

### 4. 在代码中加载配置

```python
from configs.difficulty_loader import load_config

# 加载指定难度
config, meta = load_config('easy')  # 或 'medium', 'hard'

print(f"难度：{meta['level']}")
print(f"施工单元：{meta['total_grids']} 个")
print(f"预期步数：{meta['expected_steps']}")

# 创建环境
from envs.grid_env import GridAreaEnv
env = GridAreaEnv(config=config)
```

---

## 🎮 难度详解

### Easy 难度
**配置**: `configs/difficulty/easy_config.py`

```
6x6 网格，仅 2 个施工单元
位置：(2,2), (2,3) - 靠近中心
无障碍物
```

**适用场景**:
- ✅ 新算法快速验证
- ✅ 调试环境代码
- ✅ 教学演示
- ✅ 超参数搜索

**预期性能**:
- 随机策略：难以完成
- 简单启发式：~30-50 步
- 训练后 MARL: ~20-30 步

---

### Medium 难度
**配置**: `configs/difficulty/medium_config.py`

```
6x6 网格，10 个施工单元
分散布局：左上/右上/左下/右下四个区域
1 个中心障碍物 (3,3)
```

**适用场景**:
- ✅ 协作策略训练
- ✅ 路径规划研究
- ✅ 中等规模实验
- ✅ 论文对比实验

**预期性能**:
- 随机策略：几乎无法完成
- 简单启发式：~150-250 步
- 训练后 MARL: ~80-150 步

---

### Hard 难度
**配置**: `configs/difficulty/hard_config.py`

```
6x6 网格，33 个施工单元 (几乎全覆盖)
3 个障碍物：(0,3), (3,0), (5,5)
最大复杂度
```

**适用场景**:
- ✅ 完整训练 benchmark
- ✅ 算法压力测试
- ✅ 最优策略研究
- ✅ 长期规划能力评估

**预期性能**:
- 随机策略：无法完成
- 简单启发式：~500-800 步
- 训练后 MARL: ~300-500 步

---

## 📈 实验输出

运行实验后，结果保存在：
```
runs/difficulty_<level>/result_<timestamp>.txt
```

**输出格式**:
```
Difficulty: easy
Runs: 3
Avg Steps: 45.3
Avg Reward: -28.50

Details:
  Run 1: steps=42, reward=-25.30
  Run 2: steps=48, reward=-30.10
  Run 3: steps=46, reward=-30.10
```

---

## 🔬 研究建议

### 对比实验设计

1. **算法对比**:
   ```bash
   # 同一难度下对比不同算法
   python3 run.py --algo ippo --config easy
   python3 run.py --algo qmix --config easy
   python3 run.py --algo vdn --config easy
   ```

2. **难度递进**:
   ```bash
   # 同一算法在不同难度下表现
   python3 run_difficulty.py easy --runs 10
   python3 run_difficulty.py medium --runs 10
   python3 run_difficulty.py hard --runs 10
   ```

3. **消融实验**:
   - 移除任务依赖
   - 改变机器人数量
   - 调整奖励函数

---

## 🎯 与天蝉可视化集成

启动天蝉可视化后，可以实时观察不同难度的环境：

```bash
# 启动可视化
./start_tianchan.sh

# 在另一个终端运行实验
python3 run_difficulty.py easy --steps 100
```

访问 http://localhost:8000 查看实时可视化。

---

## 📝 待办扩展

- [ ] 添加 Expert 难度 (更大网格/更多机器人)
- [ ] 支持自定义施工单元布局
- [ ] 添加随机障碍物生成
- [ ] 支持多任务并行训练
- [ ] 集成到 Ray/RLlib

---

_最后更新：2026-03-09 | 版本：v1.0_
