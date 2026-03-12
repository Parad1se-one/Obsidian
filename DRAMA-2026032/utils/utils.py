import numpy as np
import torch

ACTION_STR = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT",
    4: "PERFORM",
    5: "STAY"
}
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_warmup_lr(base_lr, step, warmup_steps):
    if step < warmup_steps:
        return base_lr * (step + 1) / warmup_steps
    else:
        return base_lr


def build_obs_list_for_agents(env):
    state = env._get_state()
    robots_info = state["robots"]
    num_agents = len(robots_info)
    positions = [pos for (_, pos) in robots_info]
    pass_map = env.passable_map.astype(np.float32).flatten()
    distribute_map = env.distribute_map.astype(np.float32).flatten()
    vibrate_map = env.vibrate_map.astype(np.float32).flatten()
    level_map = env.level_map.astype(np.float32).flatten()
    cover_map = env.cover_map.astype(np.float32).flatten()
    obs_list = []
    for i in range(num_agents):
        own_pos = positions[i]
        others = []
        for j in range(num_agents):
            if j == i: continue
            others.extend(list(positions[j]))
        vec = np.array([own_pos[0], own_pos[1]] + others + list(pass_map) + list(distribute_map) + 
                          list(vibrate_map) + list(level_map) + list(cover_map), dtype=np.float32)
        obs_list.append(vec)
    return obs_list

def map_action_int_to_env_action(agent_idx, int_action, env):
    return ACTION_STR[int_action]
    

def build_state(env=None, obs_batch=None, num_agents=None):
    """
    通用接口：既支持从 env 构造单帧 state，也支持从 obs_batch 构造 batch state
    """
    if env is not None:
        # === 单帧模式 ===
        st = env._get_state()
        robots_info = st["robots"]
        positions = [pos for (_, pos) in robots_info]
        flat_pos = [c for p in positions for c in p]
        pass_map = env.passable_map.astype(np.float32).flatten()
        return np.array(flat_pos + list(pass_map), dtype=np.float32)

    elif obs_batch is not None and num_agents is not None:
        # === 批量模式 ===
        B = obs_batch[0].shape[0]
        obs_dim = obs_batch[0].shape[1]
        pass_map_len = obs_dim - 2*(num_agents-1) - 2
        state_batch = []
        for b_idx in range(B):
            pm = obs_batch[0][b_idx].cpu().numpy()[(2 + 2*(num_agents-1)):]
            pos_flat = []
            for i in range(num_agents):
                arr = obs_batch[i][b_idx].cpu().numpy()
                pos_flat.extend([arr[0], arr[1]])
            state_vec = np.concatenate([np.array(pos_flat, dtype=np.float32), pm])
            state_batch.append(state_vec)
        return torch.tensor(np.stack(state_batch, axis=0), dtype=torch.float32, device=device)
    else:
        raise ValueError("Must provide either env or obs_batch+num_agents.")
    

def compute_gae(rewards_agent, values, next_value, dones, gamma=0.99, lam=0.95):
    """
    返回 advantages, returns:
      advantages: (T, N)
      returns: (T, N)   (GAE + values broadcast)
    values: (T,) shared critic outputs
    next_value: scalar tensor
    """
    T, N = rewards_agent.shape
    advantages = torch.zeros((T, N), dtype=torch.float32, device=rewards_agent.device)
    returns = torch.zeros((T, N), dtype=torch.float32, device=rewards_agent.device)

    # expand values -> (T, N)
    vals = values.unsqueeze(-1).expand(T, N)  # (T, N)
    next_val = next_value.clone().detach().to(rewards_agent.device)
    gae = torch.zeros(N, dtype=torch.float32, device=rewards_agent.device)

    for t in reversed(range(T)):
        mask = 1.0 - dones[t]  # scalar or tensor (if dones is (T,))
        # δ_t^i = r_t^i + γ * V(s_{t+1}) * mask - V(s_t)
        delta = rewards_agent[t] + gamma * next_val * mask - vals[t]
        gae = delta + gamma * lam * mask * gae
        advantages[t] = gae
        returns[t] = advantages[t] + vals[t]
        # set next_val = V(s_t) for next iteration
        next_val = vals[t, 0]  # any column is V(s_t) (they are copies)
    return advantages, returns
