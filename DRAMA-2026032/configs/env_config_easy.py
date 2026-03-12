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
    "grid_width": 5,
    "grid_height": 5,

    # 机器人信息
    "num_robots": 4,
    "robots": {
        "material_distributer": {  # 智能布料机
            "num": 1,
            "tasks": ["distribute_wall", "distribute_floor"],
            "init_positions": [(0, 0)]
        },
        "leveler": {      # 整平机器人
            "num": 1,
            "tasks": ["level_floor"],
            "init_positions": [(2, 0)]
        }
    },

    # 障碍物设置
    "obstacles": {
        # 固定障碍物：不可通行
        "static": [(3, 0)],
        # 动态障碍物：例如随施工进度变化的堆料区
        "dynamic": []
    },

    # 墙体信息：完成后格子自动转为不可通行
    "walls": {
        "init": [],
        # "to_distribute": [(0, 2), (1, 2),  (2, 4), (3, 4)],   # 待施工的墙体
        "to_distribute": [],
        "to_vibrate": []
    },

    "floors": {
        "to_distribute": [(0, 3), (0, 4), (1, 3), (1, 4),
                 (3, 0), (3, 1), (4, 0), (4, 1),],
        # "to_distribute": [(1,5), (2,5), (3,5)],
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