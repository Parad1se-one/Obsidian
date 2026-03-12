# marl/buffer.py
import random
import torch
import numpy as np
from collections import namedtuple, deque

Transition = namedtuple("Transition", ["obs", "actions", "rewards", "next_obs", "done", "state", "next_state"])

class ReplayBuffer:
    def __init__(self, capacity=50000):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)

    def push(self, obs, actions, rewards, next_obs, done, state=None, next_state=None):
        """
        obs, next_obs: list of per-agent observations (each is array-like)
        actions: list of ints per agent
        rewards: list of floats per agent
        done: bool
        state, next_state: global state vectors (optional, for QMIX)
        """
        self.buffer.append(Transition(obs, actions, rewards, next_obs, done, state, next_state))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        return batch
    
    def sample_torch(self, batch_size, device, return_state=False):
        batch = self.sample(batch_size)
        B = len(batch)
        num_agents = len(batch[0].obs)
        obs_batch = []
        next_obs_batch = []
        for i in range(num_agents):
            obs_i = np.array([b.obs[i] for b in batch], dtype=np.float32)
            next_obs_i = np.array([b.next_obs[i] for b in batch], dtype=np.float32)
            obs_batch.append(torch.from_numpy(obs_i).to(device))
            next_obs_batch.append(torch.from_numpy(next_obs_i).to(device))
        actions_batch = torch.tensor([b.actions for b in batch], dtype=torch.long, device=device)
        rewards_batch = torch.tensor([b.rewards for b in batch], dtype=torch.float32, device=device)
        done_batch = torch.tensor([float(b.done) for b in batch], dtype=torch.float32, device=device)
        
        if return_state and batch[0].state is not None:
            state_batch = torch.tensor(np.array([b.state for b in batch], dtype=np.float32), dtype=torch.float32, device=device)
            next_state_batch = torch.tensor(np.array([b.next_state for b in batch], dtype=np.float32), dtype=torch.float32, device=device)
            return obs_batch, next_obs_batch, actions_batch, rewards_batch, done_batch, state_batch, next_state_batch
        
        return obs_batch, next_obs_batch, actions_batch, rewards_batch, done_batch
    
    def __len__(self):
        return len(self.buffer)