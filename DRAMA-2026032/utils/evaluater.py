import os
import torch
import numpy as np
from datetime import datetime
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter
from marl.agents import *
from marl.mixer import Mixer
from utils.utils import *


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

@torch.no_grad()
def evaluate_qtran_base(env, rm, checkpoint_path, episodes=20, render=False, save_log=True):
    """
    Evaluate trained QTRAN-base agents.
    Args:
        env: environment object
        rm: reward machine
        checkpoint_path: path to saved checkpoint (.pth)
        episodes: number of evaluation episodes
        render: whether to visualize env
        save_log: whether to save evaluation logs
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    ckpt = torch.load(checkpoint_path, map_location=device)
    num_agents = ckpt["num_agents"]
    obs_dim = ckpt["obs_dim"]
    state_dim = ckpt["state_dim"]
    action_n = ckpt["action_n"]

    # Rebuild agents & QTRAN components
    agents = [QTRANAgent(obs_dim, action_n).to(device) for _ in range(num_agents)]
    qtran = QTRANBase(num_agents=num_agents, state_dim=state_dim, action_dim=action_n).to(device)

    for i in range(num_agents):
        agents[i].net.load_state_dict(ckpt[f"agent_{i}"])
    qtran.load_state_dict(ckpt["qtran"])

    print(f"[Evaluate] Loaded QTRAN-base checkpoint from {checkpoint_path}")

    all_rewards = []
    for ep in tqdm(range(episodes), desc="Evaluating"):
        obs_list = build_obs_list_from_env(env)
        state = build_state_from_env(env)
        rm.reset()
        done = False
        ep_reward = 0.0
        steps = 0

        while not done:
            # greedy action selection
            actions_int = []
            for i in range(num_agents):
                obs_tensor = torch.tensor(obs_list[i], dtype=torch.float32, device=device).unsqueeze(0)
                q_values = agents[i].net(obs_tensor)
                action = torch.argmax(q_values, dim=1).item()
                actions_int.append(action)

            env_actions = [map_action_int_to_env_action(i, a, env) for i, a in enumerate(actions_int)]
            rewards_env, infos = env.step(env_actions)
            next_obs_list = build_obs_list_from_env(env)

            events = [info.get("status", None) for info in infos]
            rm_rewards, _ = rm.step(events)
            total_rewards = [(rewards_env[i] if i < len(rewards_env) else 0.0) +
                             (rm_rewards[i] if i < len(rm_rewards) else 0.0) for i in range(num_agents)]

            ep_reward += sum(total_rewards)
            obs_list = next_obs_list
            steps += 1

            if render:
                env.render()

            # stopping condition: all construction tasks done or step limit reached
            st = env._get_state()
            if len(st.get("walls_to_build", [])) == 0:
                done = True
            if steps > (env.width * env.height * 4):
                done = True

        all_rewards.append(ep_reward)
        print(f"[Ep {ep+1}] reward={ep_reward:.2f}, steps={steps}")

    avg_reward = np.mean(all_rewards)
    std_reward = np.std(all_rewards)
    print(f"\n[Evaluate Result] QTRAN-base AvgReward={avg_reward:.2f} ± {std_reward:.2f}")

    if save_log:
        os.makedirs("logs/eval_qtran", exist_ok=True)
        with open(f"logs/eval_qtran/eval_{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt", "w") as f:
            f.write(f"Checkpoint: {checkpoint_path}\n")
            f.write(f"Episodes: {episodes}\n")
            f.write(f"Average Reward: {avg_reward:.4f}\n")
            f.write(f"Std: {std_reward:.4f}\n")
            f.write("Per-episode rewards:\n")
            for i, r in enumerate(all_rewards):
                f.write(f"Ep{i+1}: {r:.4f}\n")

    return avg_reward, std_reward

def evaluate_qmix(env, rm, checkpoint_path, episodes=50, render=False, log_dir="runs", exp_name="eval_qmix"):
    """
    使用训练好的 QMIX 模型在环境中进行评估
    Args:
        env: 环境对象（需实现 reset()、step() 等方法）
        rm: 奖励机对象（可为空）
        checkpoint_path: 已训练模型的路径
        episodes: 评估回合数
        render: 是否可视化
        log_dir: tensorboard 日志路径
        exp_name: 实验名称
    """
    # === 载入 checkpoint ===
    print(f"[Load] QMIX checkpoint from {checkpoint_path}")
    ckpt = torch.load(checkpoint_path, map_location=device)

    num_agents = ckpt["num_agents"]
    obs_dim = ckpt["obs_dim"]
    state_dim = ckpt["state_dim"]
    action_n = ckpt["action_n"]

    # === 初始化 agent 与 mixer ===
    agents = [QMIXAgent(obs_dim, action_n) for _ in range(num_agents)]
    for i in range(num_agents):
        agents[i].net.load_state_dict(ckpt[f"agent_{i}"])
        agents[i].net.eval()

    mixer = Mixer(n_agents=num_agents, state_dim=state_dim).to(device)
    mixer.load_state_dict(ckpt["mixer"])
    mixer.eval()

    # === TensorBoard ===
    writer = SummaryWriter(log_dir=os.path.join(log_dir, f"{exp_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}"))

    episode_rewards = []

    for ep in tqdm(range(episodes), desc="Evaluating"):
        env.reset()
        rm.reset()
        obs_list = build_obs_list_from_env(env)
        state = build_state_from_env(env)
        done = False
        ep_reward = 0.0
        steps = 0

        while not done:
            # === greedy 动作选择 ===
            with torch.no_grad():
                actions_int = [agents[i].act(obs_list[i]) for i in range(num_agents)]
            env_actions = [map_action_int_to_env_action(i, a, env) for i, a in enumerate(actions_int)]

            # === 环境交互 ===
            rewards_env, infos = env.step(env_actions)
            next_obs_list = build_obs_list_from_env(env)
            next_state = build_state_from_env(env)

            events = [info.get("status", None) for info in infos]
            rm_rewards, _ = rm.step(events)

            total_rewards = [
                (rewards_env[i] if i < len(rewards_env) else 0.0)
                + (rm_rewards[i] if i < len(rm_rewards) else 0.0)
                for i in range(num_agents)
            ]

            ep_reward += sum(total_rewards)
            obs_list = next_obs_list
            state = next_state
            steps += 1

            if render:
                env.render()

            # 终止条件
            st = env._get_state()
            if len(st.get("walls_to_build", [])) == 0:
                done = True

            if steps > (env.width * env.height * 4):
                done = True

        episode_rewards.append(ep_reward)
        writer.add_scalar("eval/episode_reward", ep_reward, ep + 1)
        print(f"[Eval] Episode {ep+1}/{episodes} reward={ep_reward:.2f}")

    avg_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)
    print(f"\n✅ Evaluation completed: {episodes} episodes | Avg reward = {avg_reward:.2f} ± {std_reward:.2f}")

    writer.add_scalar("eval/avg_reward", avg_reward, 0)
    writer.close()

    return avg_reward, std_reward



# if __name__ == "__main__":
#     import argparse
#     from envs.grid_env import GridAreaEnv
#     from reward_machines.reward_machine import RewardMachineMultiStage

#     parser = argparse.ArgumentParser()
#     parser.add_argument("--checkpoint", type=str, required=True, help="Path to QMIX checkpoint")
#     parser.add_argument("--episodes", type=int, default=50)
#     parser.add_argument("--render", action="store_true")
#     parser.add_argument("--log_dir", type=str, default="runs")
#     parser.add_argument("--exp_name", type=str, default="eval_qmix")
#     args = parser.parse_args()

#     env = GridAreaEnv(env_config)
#     rm = RewardMachineMultiStage(env_config["task_dependencies"])
#     evaluate_qmix(env, rm,
#                   checkpoint_path=args.checkpoint,
#                   episodes=args.episodes,
#                   render=args.render,
#                   log_dir=args.log_dir,
#                   exp_name=args.exp_name)