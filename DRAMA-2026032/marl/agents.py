# marl/agents.py
import random
import copy
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class RecurrentMAPPOActor(nn.Module):
    def __init__(self, obs_dim, action_dim, hidden_dim=64, rnn_layer_num=1):
        super(RecurrentMAPPOActor, self).__init__()
        self.fc1 = nn.Linear(obs_dim, hidden_dim)
        self.gru = nn.GRU(hidden_dim, hidden_dim, num_layers=rnn_layer_num, batch_first=True)
        self.fc2 = nn.Linear(hidden_dim, action_dim)
        self.rnn_layer_num = rnn_layer_num
        self.hidden_dim = hidden_dim

    def forward(self, x, h, masks=None):
        """
        x: (batch, seq_len, obs_dim)
        h: (rnn_layer_num, batch, hidden_dim)
        masks: (batch, seq_len, 1) 用于处理序列中的 done
        """
        # 先经过全连接提取特征
        x = F.relu(self.fc1(x))
        
        # GRU 前向传播
        if masks is None:
            # Inference 模式或不考虑 mask 的简单 batch
            output, h_new = self.gru(x, h)
        else:
            # Training 模式：如果序列中间有 done，需要重置 hidden state
            # 这是一个手动 unroll 的实现，为了正确处理 mask (Truncated BPTT within chunk)
            outputs = []
            seq_len = x.size(1)
            for t in range(seq_len):
                # 取出当前时刻的数据: (batch, 1, hidden_dim)
                x_t = x[:, t:t+1] 
                mask_t = masks[:, t].view(1, -1, 1) # (1, batch, 1)
                
                # GRU step
                # h: (layers, batch, hidden)
                out_t, h = self.gru(x_t, h) 
                
                # 如果当前时刻是 done (mask=0), 则将 hidden state 置零
                # 注意：这里的 mask 通常指的是 "not done" (1.0 表示继续, 0.0 表示结束)
                h = h * mask_t 
                
                outputs.append(out_t)
            
            output = torch.cat(outputs, dim=1) # (batch, seq_len, hidden)
            h_new = h # 最后一个时刻的 hidden

        logits = self.fc2(output)
        return logits, h_new
    
    def init_hidden(self, batch_size, device, std=1.0):
        """
        随机初始化 hidden state
        std: 控制初始化的标准差，默认 1.0 (标准正态分布)
        """
        # 使用 randn 生成标准正态分布
        return torch.randn(self.rnn_layer_num, batch_size, self.hidden_dim).to(device) * std


class MAPPOActor(nn.Module):
    def __init__(self, obs_dim, action_dim, hidden_dim=128):
        super().__init__()
        self.policy = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )

    def forward(self, obs):
        logits = self.policy(obs)
        return F.softmax(logits, dim=-1)
    

class MAPPOCritic(nn.Module):
    def __init__(self, state_dim, hidden_dim=256):
        super().__init__()
        self.v = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, state):
        return self.v(state)

#   QTRAN Agent Network
class QTRANAgent(nn.Module):
    """
    Individual agent for QTRAN with target network.
    Maps local observation -> individual Q-values.
    """

    def __init__(self, obs_dim, action_dim, hidden_dim=128, device="cuda"):
        super(QTRANAgent, self).__init__()
        self.device = device

        # 当前网络
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )

        # 目标网络（复制参数）
        self.target_net = copy.deepcopy(self.net)

        self.to(device)

    def forward(self, obs):
        """
        obs: (B, obs_dim)
        return: (B, action_dim)
        """
        return self.net(obs)

    def target(self, obs):
        """使用目标网络计算Q"""
        return self.target_net(obs)

    def update_target(self, tau=1.0):
        """
        软更新或硬更新target_net参数
        tau=1 -> 硬更新
        tau<1 -> 软更新
        """
        for target_param, param in zip(self.target_net.parameters(), self.net.parameters()):
            target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)


#   QTRAN-base Central Mixer
class QTRANBase(nn.Module):
    """
    Centralized Q-network for QTRAN-base:
    It maps (state, joint actions, joint individual Qs) -> joint Q_total.

    Components:
      - Q_joint: centralized Q(s, a_1,...,a_n)
      - V: centralized V(s)
    """

    def __init__(self, num_agents, state_dim, action_dim, hidden_dim=256):
        super(QTRANBase, self).__init__()
        self.num_agents = num_agents
        self.state_dim = state_dim
        self.action_dim = action_dim

        # Q(s, a_joint) network
        self.q_joint_net = nn.Sequential(
            nn.Linear(state_dim + num_agents * action_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

        # V(s) network
        self.v_net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, state, actions_onehot):
        """
        Args:
            state: (B, state_dim)
            actions_onehot: (B, n_agents * action_dim)
        Returns:
            q_joint: (B, 1)
            v: (B, 1)
        """
        x = torch.cat([state, actions_onehot], dim=-1)
        q_joint = self.q_joint_net(x)
        v = self.v_net(state)
        return q_joint, v

class QTRANAlt(nn.Module):
    """
    QTRAN-alt: uses (state, joint action, individual Qs) as input.
    """
    def __init__(self, num_agents, state_dim, action_dim, hidden_dim=256):
        super(QTRANAlt, self).__init__()
        self.num_agents = num_agents
        self.state_dim = state_dim
        self.action_dim = action_dim

        # 输入 = 状态 + joint actions + individual Qs
        input_dim = state_dim + num_agents * (action_dim + 1)  # +1 表示每个agent的Q_i值
        self.q_joint_net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

        self.v_net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, state, actions_onehot, q_individual):
        """
        state: (B, state_dim)
        actions_onehot: (B, n_agents * action_dim)
        q_individual: (B, n_agents)
        """
        x = torch.cat([state, actions_onehot, q_individual], dim=-1)
        q_joint = self.q_joint_net(x)
        v = self.v_net(state)
        return q_joint, v

class q_net(nn.Module):
    def __init__(self, input_dim, output_dim, hidden=[128,128]):
        super().__init__()
        layers = []
        last = input_dim
        for h in hidden:
            layers.append(nn.Linear(last, h))
            layers.append(nn.ReLU())
            last = h
        layers.append(nn.Linear(last, output_dim))
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)

class DQNAgent:
    def __init__(self, obs_dim, action_dim, lr=1e-3):
        self.obs_dim = obs_dim
        self.action_dim = action_dim
        self.net = q_net(obs_dim, action_dim).to(device)
        self.target = q_net(obs_dim, action_dim).to(device)
        self.target.load_state_dict(self.net.state_dict())
        self.opt = optim.Adam(self.net.parameters(), lr=lr)

    def act(self, obs, eps):
        # obs: numpy array (obs_dim,)
        if random.random() < eps:
            return random.randrange(self.action_dim)
        obs_t = torch.tensor(obs, dtype=torch.float32, device=device).unsqueeze(0)
        with torch.no_grad():
            q = self.net(obs_t)  # (1,action_dim)
        return int(torch.argmax(q, dim=1).item())

    def update_target(self):
        self.target.load_state_dict(self.net.state_dict())

class AgentNetwork(nn.Module):
    def __init__(self, obs_dim, action_dim, hidden=[128,128]):
        super().__init__()
        layers = []
        last = obs_dim
        for h in hidden:
            layers.append(nn.Linear(last, h)); layers.append(nn.ReLU()); last = h
        layers.append(nn.Linear(last, action_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)  # (batch, action_dim)

class QMIXAgent:
    def __init__(self, obs_dim, action_dim, lr):
        self.obs_dim = obs_dim
        self.action_dim = action_dim
        self.net = AgentNetwork(obs_dim, action_dim).to(device)
        self.target = AgentNetwork(obs_dim, action_dim).to(device)
        self.target.load_state_dict(self.net.state_dict())
        self.opt = optim.Adam(self.net.parameters(), lr=lr)

    def act(self, obs, eps):
        """eps-greedy, obs: numpy array"""
        if random.random() < eps:
            return random.randrange(self.action_dim)
        import torch
        obs_t = torch.tensor(obs, dtype=torch.float32, device=device).unsqueeze(0)
        with torch.no_grad():
            q = self.net(obs_t)  # (1,action_dim)
        return int(torch.argmax(q, dim=1).item())

    def q_values(self, obs_batch):
        """给 batch obs 返回 q-values，obs_batch: tensor (B, obs_dim)"""
        return self.net(obs_batch)  # (B, action_dim)

    def target_q_values(self, obs_batch):
        return self.target(obs_batch)

    def update_target(self):
        self.target.load_state_dict(self.net.state_dict())

class CommAgentNet(nn.Module):
    def __init__(self, obs_dim, hidden_dim, action_n):
        super().__init__()
        # encoder: obs -> hidden
        self.encoder = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        # decoder: concat(hidden, message) -> q-values
        # message will have same dim as hidden
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_n)
        )

    def forward(self, obs_batch, message):
        """
        obs_batch: (B, obs_dim)
        message: (B, hidden_dim)  -- aggregated message
        returns q_vals: (B, action_n), and hidden encoding (B, hidden_dim)
        """
        hid = self.encoder(obs_batch)  # (B, hidden)
        inp = torch.cat([hid, message], dim=1)
        q = self.decoder(inp)
        return q, hid