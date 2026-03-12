"""
Easy 难度配置 - 6x6 网格，仅 2 个 grid 需要施工 (无墙体)

适用于：快速测试、算法验证、教学演示

任务阶段 (仅地面):
    Stage 1: distribute_floor  (布料)
    Stage 2: vibrate_floor     (振捣)
    Stage 3: level_floor       (整平)
    Stage 4: cover_surface     (覆膜)

作者: DRAMA Runner 🎭
日期: 2026-03-11 (移除墙体作业)
"""

ACTION_STR = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT",
    4: "PERFORM",
    5: "STAY"
}

env_config = {
    # 基础网格信息
    "grid_width": 6,
    "grid_height": 6,

    # 机器人信息
    "num_robots": 4,
    "robots": {
        "material_distributer": {  # 智能布料机
            "num": 1,
            "tasks": ["distribute_floor"],  # 仅地面布料
            "init_positions": [(0, 0)]
        },
        "vibrator": {     # 振捣机器人
            "num": 1,
            "tasks": ["vibrate_floor"],  # 仅地面振捣
            "init_positions": [(1, 1)]
        },
        "leveler": {      # 整平机器人
            "num": 1,
            "tasks": ["level_floor"],
            "init_positions": [(2, 0)]
        },
        "film_cover": {   # 覆膜机器人
            "num": 1,
            "tasks": ["cover_surface"],
            "init_positions": [(2, 2)]
        }
    },

    # 障碍物设置 - Easy 难度无障碍物
    "obstacles": {
        "static": [],
        "dynamic": []
    },

    # 墙体信息 - 已删除，无墙体作业
    "walls": {
        "init": [],
        "to_distribute": [],
        "to_vibrate": []
    },

    # 地面信息 - 仅 2 个 grid 需要施工
    "floors": {
        "to_distribute": [
            (2, 2),  # Region A
            (2, 3),  # Region B
        ],
        "to_vibrate": [],
        "to_level": [],
        "to_cover": []
    },

    # 任务依赖关系（DAG 表示）— 无墙体依赖
    "task_dependencies": {
        "distribute_floor": [],                    # 无前置依赖
        "vibrate_floor":    ["distribute_floor"],  # 依赖地面布料
        "level_floor":      ["vibrate_floor"],     # 依赖地面振捣
        "cover_surface":    ["level_floor"]        # 依赖地面整平
    }
}

# 难度元数据
DIFFICULTY = {
    "level": "Easy",
    "description": "2 个施工单元 (仅地面) - 快速测试/算法验证",
    "total_grids": 2,
    "expected_steps": "~20-40",
    "complexity": "低"
}
