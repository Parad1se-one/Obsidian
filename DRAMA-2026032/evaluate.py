import argparse
import torch
import os
import numpy as np
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime
from envs.grid_env import GridAreaEnv
from reward_machines.reward_machine import RewardMachineMultiStage
from marl.agents import DQNAgent, CommAgentNet, QMIXAgent, DQNAgent
from configs.env_config import env_config
from utils.evaluater import *


def main():
    parser = argparse.ArgumentParser(description="Evaluate MARL models (IQL/VDN/CommVDN/QMIX)")
    parser.add_argument("--algo", type=str, default="qmix", choices=["iql", "vdn", "comm_vdn", "qmix"],
                        help="选择算法类型")
    parser.add_argument("--checkpoint_path", type=str, required=True,
                        help="加载点路径，e.g. checkpoints/vdn_ep500.pt")
    parser.add_argument("--episodes", type=int, default=50,
                        help="评估回合数")
    parser.add_argument("--render", action="store_true",
                        help="是否渲染环境")
    parser.add_argument("--log_dir", type=str, default="runs",
                        help="TensorBoard 日志目录")
    args = parser.parse_args()

    # 初始化环境和奖励机
    env = GridAreaEnv(env_config)
    rm = RewardMachineMultiStage(env_config["task_dependencies"])
    # num_agents = len(env.robots)
    # action_space = 5
    # obs_list0 = build_obs_list_from_env(env)

 
    # 根据算法类型加载不同模型
    if args.algo == "iql":
        agents = [DQNAgent(len(env.obs_list[0]), action_space) for _ in range(num_agents)]
    elif args.algo == "vdn":
        agents = [DQNAgent(env.observation_space, env.action_space) for _ in range(num_agents)]
    elif args.algo == "comm_vdn":
        agents = [CommAgentNet(env.observation_space, env.action_space, num_agents) for _ in range(num_agents)]
    elif args.algo == "qmix":
            evaluate_qmix(env, rm,
             checkpoint_path=args.checkpoint_path,
             episodes=args.episodes,
             render=args.render,
             log_dir= os.path.join(args.log_dir, "eval_qmix", f"{args.checkpoint_path}{datetime.now().strftime('%Y%m%d-%H%M%S')}")
             )
    else:
        raise ValueError(f"未知算法类型: {args.algo}")



if __name__ == "__main__":
    main()