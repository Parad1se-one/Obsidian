# utils/visualize_env.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from configs.env_config import env_config
import datetime

def visualize_env(env_config, save_path=None):
    width = env_config["grid_width"]
    height = env_config["grid_height"]

    fig, ax = plt.subplots(figsize=(width/2, height/2))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_xticks(range(width+1))
    ax.set_yticks(range(height+1))
    ax.grid(True)

    # 绘制障碍物
    for (x, y) in env_config["obstacles"]["static"]:
        ax.add_patch(patches.Rectangle((x, y), 1, 1, facecolor="black"))

    # 绘制初始墙体（灰色）
    for (x, y) in env_config["walls"]["init"]:
        ax.add_patch(patches.Rectangle((x, y), 1, 1, facecolor="dimgray"))

    # 绘制待建墙体（黄色）
    for (x, y) in env_config["walls"]["to_build"]:
        ax.add_patch(patches.Rectangle((x, y), 1, 1, facecolor="gold"))

    # 绘制机器人
    colors = {
        "material_distributer": "blue",
        "vibrator": "red",
        "leveler": "green",
        "film_cover": "purple"
    }

    for robot_type, info in env_config["robots"].items():
        for (x, y) in info["init_positions"]:
            ax.add_patch(patches.Circle((x+0.5, y+0.5), 0.3,
                                        facecolor=colors.get(robot_type, "cyan"),
                                        label=robot_type))

    # 去掉重复图例
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

    ax.set_aspect("equal")
    plt.title("Environment Visualization")

    # 保存带时间戳的图片
    if save_path is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"{timestamp}_env_config.png"
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Environment visualization saved to {save_path}")

if __name__ == "__main__":
    visualize_env(env_config)