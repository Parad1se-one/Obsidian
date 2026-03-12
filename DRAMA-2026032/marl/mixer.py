# marl/mixer.py
import torch
import torch.nn as nn
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class HyperNetwork(nn.Module):
    """用于生成 mixing weights 的小型超网络"""
    def __init__(self, input_dim, embed_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, embed_dim),
            nn.ReLU(),
            nn.Linear(embed_dim, embed_dim)
        )

    def forward(self, x):
        return self.net(x)

class Mixer(nn.Module):
    """
    简单的 QMIX mixing network:
      - 输入: 个体 Qs (batch, n_agents) 和 全局 state (batch, state_dim)
      - 输出: joint Q (batch, 1)
    使用两层 mixing，权重由 state 的 hyper-net 生成
    """
    def __init__(self, n_agents, state_dim, embed_dim=64):
        super().__init__()
        self.n_agents = n_agents
        self.state_dim = state_dim
        self.embed_dim = embed_dim

        # hyper nets
        self.hyper_w1 = nn.Sequential(nn.Linear(state_dim, embed_dim), nn.ReLU(), nn.Linear(embed_dim, n_agents * embed_dim))
        self.hyper_b1 = nn.Linear(state_dim, embed_dim)

        self.hyper_w2 = nn.Sequential(nn.Linear(state_dim, embed_dim), nn.ReLU(), nn.Linear(embed_dim, embed_dim))
        self.hyper_b2 = nn.Sequential(nn.Linear(state_dim, embed_dim), nn.ReLU(), nn.Linear(embed_dim, 1))

    def forward(self, agent_qs, states):
        """
        agent_qs: (B, n_agents)
        states: (B, state_dim)
        returns: joint_q: (B,)
        """
        B = agent_qs.size(0)
        # layer1
        w1 = torch.abs(self.hyper_w1(states))  # (B, n_agents*embed)
        b1 = self.hyper_b1(states)             # (B, embed)
        w1 = w1.view(B, self.n_agents, self.embed_dim)  # (B, n_agents, embed)
        # agent_qs unsqueeze
        agent_qs_ = agent_qs.unsqueeze(-1)  # (B, n_agents, 1)
        hidden = torch.bmm(w1.transpose(1,2), agent_qs_.float()).squeeze(-1)  # (B, embed)
        hidden = hidden + b1  # (B, embed)
        hidden = F.elu(hidden)

        # layer2
        w2 = torch.abs(self.hyper_w2(states))  # (B, embed)
        b2 = self.hyper_b2(states)             # (B, 1)
        # w2 as (B, embed) -> multiply with hidden
        joint = (w2 * hidden).sum(dim=1, keepdim=True) + b2  # (B,1)
        return joint.squeeze(1)  # (B,)