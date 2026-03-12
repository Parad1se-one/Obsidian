"""
难度配置加载器
根据难度级别加载对应的环境配置
"""

from pathlib import Path
import importlib.util

DIFFICULTY_CONFIGS = {
    "easy": "easy_config.py",
    "medium": "medium_config.py",
    "hard": "hard_config.py",
}

def load_config(difficulty: str):
    """
    加载指定难度的环境配置
    
    Args:
        difficulty: 难度级别 ("easy", "medium", "hard")
    
    Returns:
        env_config: 环境配置字典
        difficulty_meta: 难度元数据
    """
    difficulty = difficulty.lower()
    
    if difficulty not in DIFFICULTY_CONFIGS:
        raise ValueError(f"未知难度：{difficulty}, 可选：{list(DIFFICULTY_CONFIGS.keys())}")
    
    config_file = DIFFICULTY_CONFIGS[difficulty]
    config_path = Path(__file__).parent / "difficulty" / config_file
    
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在：{config_path}")
    
    # 动态导入配置模块
    spec = importlib.util.spec_from_file_location("difficulty_config", config_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module.env_config, module.DIFFICULTY

def get_all_difficulties():
    """获取所有可用难度级别的信息"""
    info = []
    for difficulty in DIFFICULTY_CONFIGS.keys():
        try:
            config, meta = load_config(difficulty)
            info.append({
                "level": difficulty,
                "description": meta["description"],
                "total_grids": meta["total_grids"],
                "expected_steps": meta["expected_steps"],
                "complexity": meta["complexity"]
            })
        except:
            pass
    return info

def print_difficulty_info():
    """打印所有难度级别的信息"""
    print("\n" + "="*60)
    print("  DRAMA 难度配置")
    print("="*60)
    
    info_list = get_all_difficulties()
    
    for info in info_list:
        print(f"\n📊 {info['level'].upper()} 难度")
        print(f"   描述：{info['description']}")
        print(f"   施工单元：{info['total_grids']} 个")
        print(f"   预期步数：{info['expected_steps']}")
        print(f"   复杂度：{info['complexity']}")
    
    print("\n" + "="*60)
    print("使用方法:")
    print("  from configs.difficulty_loader import load_config")
    print("  config, meta = load_config('easy')  # 或 'medium', 'hard'")
    print("="*60 + "\n")

if __name__ == "__main__":
    print_difficulty_info()
