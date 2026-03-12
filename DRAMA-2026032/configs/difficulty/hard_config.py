"""
Hard 难度配置 - 6x6 网格，所有 36 个 grid 需要施工
适用于：完整训练、压力测试、最优策略研究
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
            "tasks": ["distribute_wall", "distribute_floor"],
            "init_positions": [(0, 0)]
        },
        "vibrator": {     # 振捣机器人
            "num": 1,
            "tasks": ["vibrate_wall", "vibrate_floor"],
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

    # 障碍物设置 - Hard 难度有多个障碍物
    "obstacles": {
        "static": [
            (0, 3),  # 上方障碍
            (3, 0),  # 左侧障碍
            (5, 5),  # 右下角障碍
        ],
        "dynamic": []
    },

    # 墙体信息
    "walls": {
        "init": [],
        "to_distribute": [],
        "to_vibrate": []
    },

    # 地面信息 - 所有 36 个 grid 需要施工 (减去障碍物)
    "floors": {
        "to_distribute": [
            # 第 0 行
            (0, 0), (0, 1), (0, 2),          # (0,3) 是障碍
            (0, 4), (0, 5),
            # 第 1 行
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
            # 第 2 行
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
            # 第 3 行
            # (3,0) 是障碍
            (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
            # 第 4 行
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
            # 第 5 行
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4),
            # (5,5) 是障碍
        ],
        "to_vibrate": [],
        "to_level": [],
        "to_cover": []
    },

    # 任务依赖关系（DAG 表示）
    "task_dependencies": {
        "distribute_wall": [],
        "vibrate_wall": ["distribute_wall"],
        "distribute_floor": ["distribute_wall"],
        "vibrate_floor": ["distribute_floor", "vibrate_wall"],
        "level_floor": ["vibrate_floor"],
        "cover_surface": ["level_floor"]
    }
}

# 难度元数据
DIFFICULTY = {
    "level": "Hard",
    "description": "33 个施工单元 - 完整训练/压力测试",
    "total_grids": 33,  # 36 - 3 个障碍物
    "expected_steps": "~500-1000+",
    "complexity": "高"
}
