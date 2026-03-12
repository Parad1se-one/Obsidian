"""
Medium 难度配置 - 6x6 网格，10 个 grid 需要施工 (无墙体)

适用于：中等复杂度训练、协作策略测试

任务阶段 (仅地面):
    Stage 1: distribute_floor  (布料)
    Stage 2: vibrate_floor     (振捣)
    Stage 3: level_floor       (整平)
    Stage 4: cover_surface     (覆膜)

Spatial Regions (4 个):
    - TOP_LEFT:     3 grids
    - TOP_RIGHT:    3 grids
    - BOTTOM_LEFT:  2 grids
    - BOTTOM_RIGHT: 2 grids

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

    # 障碍物设置 - Medium 难度有少量障碍物
    "obstacles": {
        "static": [(3, 3)],  # 中心障碍物，增加路径规划难度
        "dynamic": []
    },

    # 墙体信息 - 已删除，无墙体作业
    "walls": {
        "init": [],
        "to_distribute": [],
        "to_vibrate": []
    },

    # 地面信息 - 10 个 grid 需要施工 (分散布局，4 个 Region)
    "floors": {
        "to_distribute": [
            # TOP_LEFT Region (3 grids)
            (0, 1), (0, 2), (1, 2),
            # TOP_RIGHT Region (3 grids)
            (0, 4), (1, 4), (1, 5),
            # BOTTOM_LEFT Region (2 grids)
            (4, 0), (5, 0),
            # BOTTOM_RIGHT Region (2 grids)
            (4, 4), (5, 5),
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
    "level": "Medium",
    "description": "10 个施工单元 (仅地面, 4 Regions) - 中等复杂度/协作策略",
    "total_grids": 10,
    "expected_steps": "~100-200",
    "complexity": "中"
}
