# marl/trainer.py
import torch
import torch.nn as nn
import numpy as np
import os
import json
from torch.distributions import Categorical
from torch.utils.tensorboard import SummaryWriter
from marl.buffer import ReplayBuffer
from marl.agents import *
from marl.mixer import *
from datetime import datetime
from tqdm import tqdm
import torch.nn.utils as nn_utils
from utils.utils import *

ACTION_STR = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT",
    4: "STAY"
}


# ---------------- QTRAN-base ----------------
def train_qtran_base(env, rm,
                     episodes=1000,
                     batch_size=2048,
                     buffer_capacity=50000,
                     eps_start=0.5,
                     eps_end=0.05,
                     eps_decay=5e-4,
                     lr=5e-4,
                     gamma=0.99,
                     lambda_opt=0.1,
                     lambda_nopt=0.1,
                     log_dir="runs",
                     exp_name="qtran_base",
                     save_interval=500):
    
    os.makedirs("checkpoints/qtran_base", exist_ok=True)
    writer = SummaryWriter(log_dir=os.path.join(log_dir, f"{exp_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}"))
    B = batch_size
    env.reset()
    num_agents = len(env.robots)

    # build initial dims
    obs_list0 = build_obs_list_from_env(env)
    obs_dim = len(obs_list0[0])
    state0 = build_state(env=env)
    state_dim = len(state0)
    action_n = 5

    # create agents and QTRAN model
    agents = [QTRANAgent(obs_dim, action_n).to(device) for _ in range(num_agents)]
    qtran_net = QTRANBase(num_agents=num_agents, state_dim=state_dim, action_dim=action_n).to(device)
    qtran_target = QTRANBase(num_agents=num_agents, state_dim=state_dim, action_dim=action_n).to(device)
    qtran_target.load_state_dict(qtran_net.state_dict())

    # optimizer: agent nets + qtran params
    params = []
    for ag in agents:
        params += list(ag.net.parameters())
    params += list(qtran_net.parameters())
    optimizer = torch.optim.Adam(params, lr=lr)

    buffer = ReplayBuffer(capacity=buffer_capacity)

    global_step = 0
    update_count = 0

    for ep in tqdm(range(episodes), desc="Training QTRAN-Base"):
        env.reset()
        rm.reset()

        obs_list = build_obs_list_from_env(env)
        state = build_state(env=env)
        done = False
        ep_reward = 0.0
        steps = 0

        while not done:
            eps = max(eps_end, eps_start - (global_step / eps_decay) * (eps_start - eps_end))

            # select actions (epsilon-greedy)
            actions_int = []
            for i in range(num_agents):
                if np.random.rand() < eps:
                    a = np.random.randint(action_n)
                else:
                    with torch.no_grad():
                        q_vals = agents[i](torch.tensor(obs_list[i], dtype=torch.float32, device=device).unsqueeze(0))
                        a = torch.argmax(q_vals).item()
                actions_int.append(a)
            
            env_actions = [map_action_int_to_env_action(i, a, env) for i, a in enumerate(actions_int)]
            rewards_env, infos = env.step(env_actions)

            next_obs_list = build_obs_list_from_env(env)
            next_state = build_state(env=env)

            events = [info.get("status", None) for info in infos]
            rm_rewards, _ = rm.step(events)

            total_rewards = [
                (rewards_env[i] if i < len(rewards_env) else 0.0) +
                (rm_rewards[i] if i < len(rm_rewards) else 0.0)
                for i in range(num_agents)
            ]

            buffer.push(obs_list, actions_int, total_rewards, next_obs_list, done)

            obs_list = next_obs_list
            state = next_state
            ep_reward += sum(total_rewards)
            global_step += 1
            steps += 1

            # 训练
            if len(buffer) >= batch_size:
                obs_batch, next_obs_batch, actions_batch, rewards_batch, done_batch = buffer.sample_torch(batch_size, device)
                state_batch = build_state(obs_batch=obs_batch, num_agents=num_agents)
                next_state_batch = build_state(obs_batch=next_obs_batch, num_agents=num_agents)

                # Individual Q-values (per-agent)
                q_vals = []
                q_next_vals = []
                for i in range(num_agents):
                    q_i = agents[i].net(obs_batch[i])              # (B, action_n)
                    q_next_i = agents[i].target_net(next_obs_batch[i])  # (B, action_n)
                    q_taken = q_i.gather(1, actions_batch[:, i].unsqueeze(1)).squeeze(1)
                    q_vals.append(q_taken)
                    q_next_vals.append(q_next_i.max(dim=1)[0])
                
                q_vals = torch.stack(q_vals, dim=1)           # (B, n_agents)
                q_next_vals = torch.stack(q_next_vals, dim=1) # (B, n_agents)            

                # === one-hot joint actions ===
                actions_onehot = F.one_hot(actions_batch, num_classes=action_n).float()  # (B, n, action_n)
                actions_onehot = actions_onehot.reshape(B, -1)  # (B, n*action_n)

                # forward through QTRAN network
                q_joint, v = qtran_net(state_batch, actions_onehot)

                # === target计算 ===
                with torch.no_grad():
                    q_next_values = [ag.target_net(next_obs_batch[i]) for ag in agents]
                    next_actions_max = torch.stack(
                        [torch.argmax(q_next_values[i], dim=1) for i in range(num_agents)], dim=1
                    )  # (B, n_agents)
                    next_actions_onehot = torch.cat(
                        [F.one_hot(next_actions_max[:, i], num_classes=action_n)
                         for i in range(num_agents)], dim=1).float()

                    q_joint_next, v_next = qtran_target(next_state_batch, next_actions_onehot)

                    td_target = rewards_batch.sum(dim=1, keepdim=True) + (1 - done_batch.unsqueeze(1)) * gamma * q_joint_next

                # === QTRAN 损失 ===
                loss_td = nn.MSELoss()(q_joint, td_target.detach())

                # 最优约束：joint Q 与 individual Q 差异最小化
                q_opt = q_joint - v 
                q_ind = q_vals.sum(dim=1)
                loss_opt = nn.MSELoss()(q_opt, q_ind.unsqueeze(1).detach())

                # 非最优约束（负采样）
                diff = q_ind - q_opt
                loss_nopt = torch.mean(torch.where(diff < 0, diff ** 2, torch.zeros_like(diff)))

                loss = loss_td + lambda_opt * loss_opt + lambda_nopt * loss_nopt

                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(qtran_net.parameters(), 10)
                optimizer.step()

                update_count += 1
                writer.add_scalar("loss/td", loss_td.item(), update_count)
                writer.add_scalar("loss/opt", loss_opt.item(), update_count)
                writer.add_scalar("loss/nopt", loss_nopt.item(), update_count)

                # Soft update
                if global_step % 1000 == 0:
                    qtran_target.load_state_dict(qtran_net.state_dict())
                    for ag in agents:
                        ag.update_target()

            # 提前结束条件
            st = env._get_state()
            if len(st.get("walls_to_build", [])) == 0:
                done = True
            if steps > env.width * env.height * 4:
                done = True

        writer.add_scalar("episode_reward", ep_reward, ep + 1)
        if (ep + 1) % 10 == 0:
            print(f"\nEp {ep+1}/{episodes} reward={ep_reward:.2f} steps={steps}", flush=True)
        # 保存检查点
        if (ep + 1) % save_interval == 0:
            checkpoint = {
                "num_agents": num_agents,
                "obs_dim": obs_dim,
                "state_dim": state_dim,
                "action_n": action_n,
                "qtran_net": qtran_net.state_dict()
            }
            for i, ag in enumerate(agents):
                checkpoint[f"agent_{i}"] = ag.net.state_dict()
            torch.save(checkpoint, f"checkpoints/qtran_base/qtran_{datetime.now().strftime('%Y%m%d-%H%M%S')}_ep{ep+1}.pth")
            print(f"[Checkpoint] Saved QTRAN-Base at episode {ep+1}", flush=True)

    # === 训练结束后（或中途某次checkpoint） ===
    hparams = {
        "episodes": episodes,
        "batch_size": batch_size,
        "buffer_capacity": buffer_capacity,
        "eps_start": eps_start,
        "eps_end": eps_end,
        "eps_decay": eps_decay,
        "lr": lr,
        "gamma": gamma,
        "lambda_opt": lambda_opt,
        "lambda_nopt": lambda_nopt,
        "steps" : steps
    }

    metrics = {
        "final_reward": ep_reward,
        "final_loss_td": loss_td.item(),
        "final_loss_opt": loss_opt.item(),
        "final_loss_nopt": loss_nopt.item(),
    }

    config_path = os.path.join(writer.log_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump(hparams, f, indent=4)

    writer.add_hparams(hparams, metrics)
    writer.close()
    return agents, qtran_net

# ---------------- QTRAN-alt ----------------
def train_qtran_alt(env, rm,
                     episodes=1000,
                     batch_size=128,
                     buffer_capacity=500,
                     eps_start=0.5,
                     eps_end=0.05,
                     eps_decay=5e-4,
                     lr=5e-4,
                     gamma=0.99,
                     lambda_opt=0.1,
                     lambda_nopt=0.1,
                     log_dir="runs",
                     exp_name="qtran_alt",
                     save_interval=200):
    
    os.makedirs("checkpoints/qtran_alt", exist_ok=True)
    writer = SummaryWriter(log_dir=os.path.join(log_dir, f"{exp_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}"))
    B = batch_size
    env.reset()
    num_agents = len(env.robots)

    # 获取维度
    obs_list0 = build_obs_list_from_env(env)
    obs_dim = len(obs_list0[0])
    state0 = build_state(env=env)
    state_dim = len(state0)
    action_n = 5

    # 初始化智能体与 QTRAN 模型
    agents = [QTRANAgent(obs_dim, action_n).to(device) for _ in range(num_agents)]
    qtran_net = QTRANAlt(num_agents=num_agents, state_dim=state_dim, action_dim=action_n).to(device)
    qtran_target = QTRANAlt(num_agents=num_agents, state_dim=state_dim, action_dim=action_n).to(device)
    qtran_target.load_state_dict(qtran_net.state_dict())

    optimizer = torch.optim.Adam(qtran_net.parameters(), lr=lr)
    buffer = ReplayBuffer(capacity=buffer_capacity)

    global_step = 0
    update_count = 0

    for ep in tqdm(range(episodes), desc="Training QTRAN-Alt"):
        env.reset()
        rm.reset()

        obs_list = build_obs_list_from_env(env)
        state = build_state(env=env)
        done = False
        ep_reward = 0.0
        steps = 0

        while not done:
            eps = max(eps_end, eps_start - (global_step / eps_decay) * (eps_start - eps_end))

            # 动作选择
            # choose actions (epsilon-greedy)
            actions_int = []
            for i in range(num_agents):
                if np.random.rand() < eps:
                    a = np.random.randint(action_n)
                else:
                    with torch.no_grad():
                        q_vals = agents[i](torch.tensor(obs_list[i], dtype=torch.float32, device=device).unsqueeze(0))
                        a = torch.argmax(q_vals).item()
                actions_int.append(a)
            
            env_actions = [map_action_int_to_env_action(i, a, env) for i, a in enumerate(actions_int)]
            rewards_env, infos = env.step(env_actions)

            next_obs_list = build_obs_list_from_env(env)
            next_state = build_state(env=env)

            events = [info.get("status", None) for info in infos]
            rm_rewards, _ = rm.step(events)

            total_rewards = [
                (rewards_env[i] if i < len(rewards_env) else 0.0) +
                (rm_rewards[i] if i < len(rm_rewards) else 0.0)
                for i in range(num_agents)
            ]

            buffer.push(obs_list, actions_int, total_rewards, next_obs_list, done)

            obs_list = next_obs_list
            state = next_state
            ep_reward += sum(total_rewards)
            global_step += 1
            steps += 1

            # 训练
            if len(buffer) >= batch_size:
                obs_batch, next_obs_batch, actions_batch, rewards_batch, done_batch = buffer.sample_torch(batch_size, device)
                state_batch = build_state(obs_batch=obs_batch, num_agents=num_agents)
                next_state_batch = build_state(obs_batch=next_obs_batch, num_agents=num_agents)

                # Individual Q-values (per-agent)
                q_vals = []
                q_next_vals = []
                for i in range(num_agents):
                    q_i = agents[i].net(obs_batch[i])              # (B, action_n)
                    q_next_i = agents[i].target_net(next_obs_batch[i])  # (B, action_n)
                    q_taken = q_i.gather(1, actions_batch[:, i].unsqueeze(1)).squeeze(1)
                    q_vals.append(q_taken)
                    q_next_vals.append(q_next_i.max(dim=1)[0])
                
                q_vals = torch.stack(q_vals, dim=1)           # (B, n_agents)
                q_next_vals = torch.stack(q_next_vals, dim=1) # (B, n_agents)            

                # === one-hot joint actions ===
                actions_onehot = F.one_hot(actions_batch, num_classes=action_n).float()  # (B, n, action_n)
                actions_onehot = actions_onehot.reshape(B, -1)  # (B, n*action_n)

                # forward through QTRAN network
                q_joint, v = qtran_net(state_batch, actions_onehot, q_vals)

                # === target计算 ===
                with torch.no_grad():
                    q_next_values = [ag.target_net(next_obs_batch[i]) for ag in agents]
                    next_actions_max = torch.stack(
                        [torch.argmax(q_next_values[i], dim=1) for i in range(num_agents)], dim=1
                    )  # (B, n_agents)
                    next_actions_onehot = torch.cat(
                        [F.one_hot(next_actions_max[:, i], num_classes=action_n)
                         for i in range(num_agents)], dim=1).float()

                    q_joint_next, v_next = qtran_target(next_state_batch, next_actions_onehot, next_actions_max)

                    td_target = rewards_batch.sum(dim=1, keepdim=True) + (1 - done_batch.unsqueeze(1)) * gamma * q_joint_next
                # === 修正维度对齐 ===
                if td_target.dim() == 1:
                    td_target = td_target.unsqueeze(1)

                # === QTRAN 损失 ===
                loss_td = nn.MSELoss()(q_joint, td_target.detach())

                # 最优约束：joint Q 与 individual Q 差异最小化
                q_opt = q_joint - v 
                q_ind = q_vals.sum(dim=1)
                loss_opt = nn.MSELoss()(q_opt, q_ind.unsqueeze(1).detach())

                # 非最优约束（负采样）
                diff = q_ind - q_opt
                loss_nopt = torch.mean(torch.where(diff < 0, diff ** 2, torch.zeros_like(diff)))

                loss = loss_td + lambda_opt * loss_opt + lambda_nopt * loss_nopt

                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(qtran_net.parameters(), 10)
                optimizer.step()

                update_count += 1
                writer.add_scalar("loss/td", loss_td.item(), update_count)
                writer.add_scalar("loss/opt", loss_opt.item(), update_count)
                writer.add_scalar("loss/nopt", loss_nopt.item(), update_count)

                # Soft update
                if global_step % 1000 == 0:
                    qtran_target.load_state_dict(qtran_net.state_dict())
                    for ag in agents:
                        ag.update_target()

            # 提前结束条件
            st = env._get_state()
            if len(st.get("walls_to_build", [])) == 0:
                done = True
            if steps > env.width * env.height * 4:
                done = True

        writer.add_scalar("episode_reward", ep_reward, ep + 1)
        if (ep + 1) % 10 == 0:
            print(f" \nEp {ep+1}/{episodes} reward={ep_reward:.2f} steps={steps}", flush=True)
        # 保存检查点
        if (ep + 1) % save_interval == 0:
            checkpoint = {
                "num_agents": num_agents,
                "obs_dim": obs_dim,
                "state_dim": state_dim,
                "action_n": action_n,
                "qtran_net": qtran_net.state_dict()
            }
            for i, ag in enumerate(agents):
                checkpoint[f"agent_{i}"] = ag.net.state_dict()
            torch.save(checkpoint, f"checkpoints/qtran_alt/qtran_{datetime.now().strftime('%Y%m%d-%H%M%S')}_ep{ep+1}.pth")
            print(f"[Checkpoint] Saved QTRAN-Alt at episode {ep+1}", flush=True)

    writer.close()
    return agents, qtran_net

# ---------------- VDN ----------------


def train_comm_vdn(env, rm, episodes=1000, batch_size=64, buffer_capacity=50000,
                   eps_start=0.5, eps_end=0.05, eps_decay=5e4,
                   lr=1e-4, gamma=0.99, log_dir="runs", exp_name="comm_vdn",
                   save_interval=100, warmup_steps=5000, grad_clip=10.0,
                   comm_steps=1, hidden_dim=128):
    """
    Comm-VDN:
    - 每个 agent 使用一个包含 communication 的 Q 网络（CommNet-like: encode -> message mean -> decode -> q）
    - 训练采用 VDN 思想：Q_total = sum_i Q_i
    - comm_steps: 消息传递轮数（目前实现为在网络中执行一次聚合；若 comm_steps>1 可迭代）
    """

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    os.makedirs("checkpoints", exist_ok=True)
    writer = SummaryWriter(log_dir=os.path.join(log_dir, f"{exp_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}"))

    # build initial dims
    env.reset()
    num_agents = len(env.robots)
    obs_list0 = build_obs_list_from_env(env)
    obs_dim = len(obs_list0[0])
    action_n = len(ACTION_STR)

    # define CommAgent network (inside function to keep self-contained)
    

    # create agents and target agents
    agents = []
    targets = []
    for _ in range(num_agents):
        net = CommAgentNet(obs_dim, hidden_dim, action_n).to(device)
        target = CommAgentNet(obs_dim, hidden_dim, action_n).to(device)
        target.load_state_dict(net.state_dict())
        agents.append(net)
        targets.append(target)

    # optimizer for all agent params
    params = []
    for net in agents:
        params += list(net.parameters())
    optimizer = torch.optim.Adam(params, lr=lr)

    buffer = ReplayBuffer(capacity=buffer_capacity)


    global_step = 0
    update_count = 0

    for ep in range(episodes):
        env.reset()
        rm.reset()
        obs_list = build_obs_list_from_env(env)
        done = False
        ep_reward = 0.0
        steps = 0

        while not done:
            eps = max(eps_end, eps_start - (global_step / eps_decay) * (eps_start - eps_end))
            # --- action selection with communication (inference) ---
            # build obs tensors per agent
            obs_tensors = [torch.tensor(obs_list[i], dtype=torch.float32, device=device).unsqueeze(0) for i in range(num_agents)]
            # first encode to get hid representations
            with torch.no_grad():
                hids = []
                for i in range(num_agents):
                    hid = agents[i].encoder(obs_tensors[i])  # (1, hidden)
                    hids.append(hid)
                # aggregate message: mean of hids
                stacked = torch.cat(hids, dim=0) if len(hids) > 0 else torch.zeros((num_agents, hidden_dim), device=device)
                message = stacked.mean(dim=0, keepdim=True)  # (1, hidden)
                # if comm_steps>1 you could iterate; here simple one-step
                # decode and pick action
                actions_int = []
                for i in range(num_agents):
                    q, _ = agents[i].forward(obs_tensors[i], message)
                    if np.random.rand() < eps:
                        a = np.random.randint(action_n)
                    else:
                        a = int(torch.argmax(q, dim=1).item())
                    actions_int.append(a)

            env_actions = [map_action_int_to_env_action(i, a, env) for i, a in enumerate(actions_int)]
            rewards, infos = env.step(env_actions)
            next_obs_list = build_obs_list_from_env(env)

            events = [info.get("status", None) for info in infos]
            rm_rewards, _ = rm.step(events)
            total_rewards = [(rewards[i] if i < len(rewards) else 0.0) + (rm_rewards[i] if i < len(rm_rewards) else 0.0)
                             for i in range(num_agents)]

            buffer.push(obs_list, actions_int, total_rewards, next_obs_list, False)
            obs_list = next_obs_list
            ep_reward += sum(total_rewards)
            steps += 1
            global_step += 1

            # --- training update ---
            if len(buffer) >= batch_size and global_step > warmup_steps:
                batch = buffer.sample(batch_size)
                B = len(batch)
                # construct obs_batch tensors for each agent: list of (B, obs_dim)
                obs_batch, next_obs_batch, actions_batch, rewards_batch, done_batch = buffer.sample_torch(batch_size, device)

                # forward pass current obs to get q_taken per agent
                q_taken_list = []
                hid_list = []
                for i in range(num_agents):
                    # we need to compute all agents' hid to form messages per batch
                    # encode all obs to hid_i: (B, hidden)
                    hid_i = agents[i].encoder(obs_batch[i])  # (B, hidden)
                    hid_list.append(hid_i)
                # build message per batch: mean across agents -> (B, hidden)
                stacked_hids = torch.stack(hid_list, dim=1)  # (B, n_agents, hidden)
                message_batch = stacked_hids.mean(dim=1)     # (B, hidden)

                # compute q values using decoder with message
                for i in range(num_agents):
                    q_vals = agents[i].decoder(torch.cat([hid_list[i], message_batch], dim=1))  # (B, action_n)
                    acts_i = actions_batch[:, i].unsqueeze(1)
                    q_taken = q_vals.gather(1, acts_i).squeeze(1)  # (B,)
                    q_taken_list.append(q_taken)

                q_taken_stack = torch.stack(q_taken_list, dim=1)  # (B, n_agents)

                # compute joint next max using target networks
                q_next_max_list = []
                # encode next obs through target encoders to get next_hids
                next_hid_list = []
                for i in range(num_agents):
                    next_hid_i = targets[i].encoder(next_obs_batch[i])  # (B, hidden)
                    next_hid_list.append(next_hid_i)
                next_stacked = torch.stack(next_hid_list, dim=1)
                next_message_batch = next_stacked.mean(dim=1)

                for i in range(num_agents):
                    q_next = targets[i].decoder(torch.cat([next_hid_list[i], next_message_batch], dim=1))  # (B, action_n)
                    max_q_next, _ = torch.max(q_next, dim=1)  # (B,)
                    q_next_max_list.append(max_q_next)
                q_next_max_stack = torch.stack(q_next_max_list, dim=1)  # (B, n_agents)

                # VDN joint max: sum of per-agent max
                joint_next_max = q_next_max_stack.sum(dim=1)  # (B,)

                r_global = rewards_batch.sum(dim=1)  # (B,)
                td_target = r_global + (1 - done_batch) * gamma * joint_next_max  # (B,)

                # joint current q_total
                q_tot = q_taken_stack.sum(dim=1)  # (B,)

                loss = nn.MSELoss()(q_tot, td_target.detach())

                optimizer.zero_grad()
                loss.backward()
                # gradient clipping
                torch.nn.utils.clip_grad_norm_(params, grad_clip)
                optimizer.step()
                update_count += 1

                writer.add_scalar("loss", loss.item(), update_count)
                writer.add_scalar("epsilon", eps, global_step)

                # update target networks periodically
                if global_step % 1000 == 0:
                    for i in range(num_agents):
                        targets[i].load_state_dict(agents[i].state_dict())

            # prevent infinite loops
            if steps > (env.width * env.height * 4):
                break

            st = env._get_state()
            if len(st.get("walls_to_build", [])) == 0:
                done = True

        writer.add_scalar("episode_reward", ep_reward, ep + 1)
        if (ep + 1) % save_interval == 0:
            # save all agent weights
            ckpt = {"num_agents": num_agents, "obs_dim": obs_dim, "hidden_dim": hidden_dim, "action_n": action_n}
            for i in range(num_agents):
                ckpt[f"agent_{i}"] = agents[i].state_dict()
            torch.save(ckpt, f"checkpoints/{exp_name}_ep{ep+1}.pth")
            print(f"[Checkpoint] Saved at episode {ep+1}")

        if (ep + 1) % 10 == 0:
            print(f"\n[{exp_name}] Ep {ep+1}/{episodes} reward={ep_reward:.2f} steps={steps}")

    # final save
    ckpt = {"num_agents": num_agents, "obs_dim": obs_dim, "hidden_dim": hidden_dim, "action_n": action_n}
    for i in range(num_agents):
        ckpt[f"agent_{i}"] = agents[i].state_dict()
    torch.save(ckpt, f"checkpoints/{exp_name}_final.pth")
    writer.close()

    return agents


# ---------------- MAPPO ----------------
def train_mappo(env, rm, episodes=1000, rollout_len=256, ppo_epochs=4, mini_batch_size=64, clip_eps=0.2,
               lr=5e-4, gamma=0.99, lam=0.95, log_dir="runs", exp_name="mappo", save_interval=100):

    os.makedirs("checkpoints/mappo", exist_ok=True)
    writer = SummaryWriter(log_dir=os.path.join(
        log_dir, f"{exp_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    ))

    env.reset()
    num_agents = len(env.robots)

    # ---- dims ----
    obs_list0 = build_obs_list_from_env(env)
    obs_dim = len(obs_list0[0])
    state_dim = len(build_state(env))
    action_n = 5

    # ---- networks ----
    actors = [MAPPOActor(obs_dim, action_n).to(device) for _ in range(num_agents)]
    critic = MAPPOCritic(state_dim).to(device)

    # Optimizers
    actor_optim = optim.Adam([p for a in actors for p in a.parameters()], lr=lr)
    critic_optim = optim.Adam(critic.parameters(), lr=lr)

    global_step = 0

    for ep in tqdm(range(episodes), desc="Training MAPPO"):
        obs_list = build_obs_list_from_env(env)
        state = build_state(env)
        rm.reset()
        done = False
        ep_reward = 0

        rollout_data = {
            "obs": [],
            "actions": [],
            "logprobs": [],
            "values": [],
            "rewards": [],
            "dones": [],
            "states": [],
        }

        # =============================
        #   Rollout phase
        # =============================
        for t in range(rollout_len):
            obs_tensor_list = [torch.tensor(o, dtype=torch.float32, device=device).unsqueeze(0)
                               for o in obs_list]
            state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)

            # get value from critic
            value = critic(state_tensor).squeeze(0)

            # select actions for each agent
            actions = []
            logprobs = []
            for i in range(num_agents):
                probs = actors[i](obs_tensor_list[i])
                dist = Categorical(probs)
                act = dist.sample()
                actions.append(act.item())
                logprobs.append(dist.log_prob(act))

            # env step
            env_actions = [map_action_int_to_env_action(i, a, env) for i, a in enumerate(actions)]
            rewards_env, infos = env.step(env_actions)
            next_obs_list = build_obs_list_from_env(env)
            next_state = build_state(env)

            # reward machine
            events = [info.get("status", None) for info in infos]
            rm_rewards, _ = rm.step(events)

            total_rewards = [
                rewards_env[i] + (rm_rewards[i] if i < len(rm_rewards) else 0.0)
                for i in range(num_agents)
            ]
            global_reward = sum(total_rewards)

            done_flag = 0
            st = env._get_state()
            if len(st.get("walls_to_build", [])) == 0:
                done_flag = 1

            # store batch
            rollout_data["obs"].append(obs_list)
            rollout_data["states"].append(state)
            rollout_data["actions"].append(actions)
            rollout_data["logprobs"].append([lp.item() for lp in logprobs])
            rollout_data["values"].append(value.item())
            rollout_data["rewards"].append(global_reward)
            rollout_data["dones"].append(done_flag)

            ep_reward += global_reward

            obs_list = next_obs_list
            state = next_state

            if done_flag:
                break

            global_step += 1

        # ==========================================
        #   Compute GAE for this rollout
        # ==========================================
        rewards = torch.tensor(rollout_data["rewards"], dtype=torch.float32, device=device)
        dones = torch.tensor(rollout_data["dones"], dtype=torch.float32, device=device)
        values = torch.tensor(rollout_data["values"], dtype=torch.float32, device=device)

        # last next_value
        next_state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        next_value = critic(next_state_tensor).detach().squeeze(0)
        next_values = torch.cat([values[1:], next_value], dim=0)

        advantages, returns = compute_gae(rewards, values, next_values, dones, gamma, lam)

        # ==========================================
        #   PPO Update (multiple epochs)
        # ==========================================
        T = len(rewards)
        old_logprobs = torch.tensor(rollout_data["logprobs"], dtype=torch.float32, device=device)
        actions = torch.tensor(rollout_data["actions"], dtype=torch.long, device=device)

        for _ in range(ppo_epochs):
            idxs = np.arange(T)
            np.random.shuffle(idxs)

            for start in range(0, T, mini_batch_size):
                end = start + mini_batch_size
                mb = idxs[start:end]

                mb_adv = advantages[mb]
                mb_ret = returns[mb]
                mb_states = torch.tensor(rollout_data["states"], dtype=torch.float32, device=device)[mb]
                mb_obs = rollout_data["obs"][0]  # list of per-agent obs, index with mb inside loop

                # Critic loss
                values_pred = critic(mb_states).squeeze(-1)
                critic_loss = F.mse_loss(values_pred, mb_ret)

                critic_optim.zero_grad()
                critic_loss.backward()
                critic_optim.step()

                # Actor update (for each agent)
                actor_loss_total = 0

                for i in range(num_agents):
                    # collect obs for this agent at mb indices
                    obs_i = [rollout_data["obs"][t][i] for t in mb]
                    obs_i = torch.tensor(obs_i, dtype=torch.float32, device=device)

                    probs = actors[i](obs_i)
                    dist = Categorical(probs)
                    logprobs_now = dist.log_prob(actions[mb, i])

                    ratio = torch.exp(logprobs_now - old_logprobs[mb, i])
                    obj1 = ratio * mb_adv
                    obj2 = torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * mb_adv
                    actor_loss = -torch.min(obj1, obj2).mean()

                    actor_loss_total += actor_loss

                actor_optim.zero_grad()
                actor_loss_total.backward()
                actor_optim.step()

        writer.add_scalar("episode_reward", ep_reward, ep + 1)

        if (ep + 1) % 10 == 0:
            print(f"Ep {ep+1}/{episodes}, reward={ep_reward:.2f}", flush=True)

        if (ep + 1) % save_interval == 0:
            ckpt = {
                "actors": [a.state_dict() for a in actors],
                "critic": critic.state_dict(),
                "num_agents": num_agents,
                "obs_dim": obs_dim,
                "state_dim": state_dim,
                "action_n": action_n
            }
            torch.save(ckpt, f"checkpoints/mappo/mappo_{datetime.now().strftime('%Y%m%d-%H%M%S')}_ep{ep+1}.pth")

    writer.close()
    return actors, critic


# ---------------- IQL ----------------
def train_iql(env, rm, episodes=1000, batch_size=64, buffer_capacity=50000,
              lr=1e-4, gamma=0.99, log_dir="runs", exp_name="iql",
              save_interval=100, warmup_steps=5000, grad_clip=10.0):
    """Independent Q-Learning (每个agent各自训练DQN)"""
    os.makedirs("checkpoints/iql", exist_ok=True)
    writer = SummaryWriter(
        log_dir=os.path.join(log_dir, f"{exp_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    )

    num_agents = len(env.robots)
    obs_list0 = build_obs_list_from_env(env)
    obs_dim = len(obs_list0[0])
    action_n = len(ACTION_STR)

    agents = [DQNAgent(obs_dim, action_n, lr=lr) for _ in range(num_agents)]
    buffers = [ReplayBuffer(capacity=buffer_capacity) for _ in range(num_agents)]

    eps_start, eps_end, eps_decay = 1.0, 0.05, 5e4
    global_step, update_count = 0, 0

    for ep in tqdm(range(episodes), desc="Training"):
        env.reset()
        rm.reset()
        obs_list = build_obs_list_from_env(env)
        done = False
        ep_reward, steps = 0.0, 0

        while not done:
            eps = max(eps_end, eps_start - (global_step / eps_decay) * (eps_start - eps_end))
            actions_int = [agents[i].act(obs_list[i], eps) for i in range(num_agents)]
            env_actions = [map_action_int_to_env_action(i, a, env) for i, a in enumerate(actions_int)]
            rewards, infos = env.step(env_actions)
            next_obs_list = build_obs_list_from_env(env)

            events = [info.get("status", None) for info in infos]
            rm_rewards, _ = rm.step(events)
            total_rewards = [
                (rewards[i] if i < len(rewards) else 0.0) + (rm_rewards[i] if i < len(rm_rewards) else 0.0)
                for i in range(num_agents)
            ]

            # 独立存储到每个agent的buffer
            for i in range(num_agents):
                buffers[i].push(
                    [obs_list[i]],  # 仅自己的观测
                    [actions_int[i]],
                    [total_rewards[i]],
                    [next_obs_list[i]],
                    False
                )

            obs_list = next_obs_list
            ep_reward += sum(total_rewards)
            steps += 1
            global_step += 1

            # --- train update ---
            for i in range(num_agents):
                if len(buffers[i]) >= batch_size and global_step > warmup_steps:
                    batch = buffers[i].sample(batch_size)
                    obs_array = np.array([b.obs[0] for b in batch], dtype=np.float32)
                    next_obs_array = np.array([b.next_obs[0] for b in batch], dtype=np.float32)
                    obs_batch = torch.from_numpy(obs_array).to(device)
                    next_obs_batch = torch.from_numpy(next_obs_array).to(device)
                    actions_batch = torch.tensor([b.actions[0] for b in batch], dtype=torch.long, device=device)
                    rewards_batch = torch.tensor([b.rewards[0] for b in batch], dtype=torch.float32, device=device)
                    done_batch = torch.tensor([1.0 if b.done else 0.0 for b in batch],
                                              dtype=torch.float32, device=device)

                    q_next = agents[i].target(next_obs_batch)
                    max_q_next, _ = torch.max(q_next, dim=1)
                    td_target = rewards_batch + (1 - done_batch) * gamma * max_q_next

                    q_vals = agents[i].net(obs_batch)
                    q_taken = q_vals.gather(1, actions_batch.unsqueeze(1)).squeeze(1)

                    loss = nn.MSELoss()(q_taken, td_target.detach())
                    agents[i].opt.zero_grad()
                    loss.backward()
                    nn_utils.clip_grad_norm_(agents[i].net.parameters(), grad_clip)
                    agents[i].opt.step()

                    update_count += 1
                    writer.add_scalar(f"loss_agent{i}", loss.item(), update_count)

            if steps > (env.width * env.height * 4):
                break
            if len(env._get_state().get("walls_to_build", [])) == 0:
                done = True

        writer.add_scalar("episode_reward", ep_reward, ep + 1)
        if (ep + 1) % save_interval == 0:
            for i, ag in enumerate(agents):
                torch.save(ag.net.state_dict(), f"checkpoints/iql/agent{i}_{datetime.now().strftime('%Y%m%d-%H%M%S')}_ep{ep+1}.pth")
            print(f"[Checkpoint] Saved at episode {ep+1}", flush=True)

        if (ep + 1) % 10 == 0:
            print(f"\n[{exp_name}] Ep {ep+1}/{episodes} reward={ep_reward:.2f} steps={steps}", flush=True)

    for i, ag in enumerate(agents):
        torch.save(ag.net.state_dict(), f"checkpoints/iql/agent{i}_{datetime.now().strftime('%Y%m%d-%H%M%S')}_final.pth")
    writer.close()
    return agents