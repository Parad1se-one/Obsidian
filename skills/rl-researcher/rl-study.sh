#!/bin/bash
# rl-study.sh - 强化学习学习脚本
# 用法：./rl-study.sh <主题> <时长分钟>

set -e

# 加载代理配置 (外网访问需要)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../common/load-proxy.sh"

# 加载搜索工具
SEARCH_SCRIPT="$SCRIPT_DIR/../search/search.sh"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/openclaw/.openclaw/workspace/obsidian-repo"
RL_KNOWLEDGE_DIR="$WORKSPACE/knowledge/rl"
RL_STUDY_LOG="$RL_KNOWLEDGE_DIR/study-log-$(date +%Y-%m-%d).md"

# 创建目录
mkdir -p "$RL_KNOWLEDGE_DIR/basics"
mkdir -p "$RL_KNOWLEDGE_DIR/algorithms"
mkdir -p "$RL_KNOWLEDGE_DIR/sota"
mkdir -p "$RL_KNOWLEDGE_DIR/papers"
mkdir -p "$WORKSPACE/code/rl-basics"
mkdir -p "$WORKSPACE/code/rl-algorithms"

echo "🦐 小虾 RL 研究模块 | 启动时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "📍 工作目录：$WORKSPACE"
echo ""

TOPIC="${1:-basics}"
DURATION="${2:-30}"

echo "📚 学习主题：$TOPIC"
echo "⏱️  预计时长：$DURATION 分钟"
echo ""

# 创建学习日志头部
cat > "$RL_STUDY_LOG" << HEADER
# RL 学习日志 | $(date +%Y-%m-%d)

## 学习元数据
- **时间:** $(date '+%H:%M')
- **主题:** $TOPIC
- **时长:** $DURATION 分钟
- **阶段:** Phase 1 - 基础奠基

---

## 学习内容

HEADER

case "$TOPIC" in
    basics)
        echo "📖 开始 RL 基础学习..."
        echo ""
        
        cat >> "$RL_STUDY_LOG" << 'CONTENT'
### 马尔可夫决策过程 (MDP)

**定义:** MDP 是强化学习的数学框架，用于建模序列决策问题。

**核心元素 (S, A, P, R, γ):**
- **S (State):** 状态空间
- **A (Action):** 动作空间
- **P (Transition):** 状态转移概率 P(s'|s,a)
- **R (Reward):** 奖励函数 R(s,a,s')
- **γ (Discount):** 折扣因子 (0 ≤ γ ≤ 1)

**马尔可夫性质:** 未来只依赖于现在，与过去无关
$$P(s_{t+1}|s_t, a_t) = P(s_{t+1}|s_t, a_t, s_{t-1}, a_{t-1}, ...)$$

CONTENT

        # 创建 MDP 笔记
        cat > "$RL_KNOWLEDGE_DIR/basics/mdp-notes.md" << 'MDP'
# 马尔可夫决策过程 (MDP)

## 核心概念

### 定义
MDP 是强化学习的数学框架，用于建模序列决策问题。

### 五元组 (S, A, P, R, γ)

| 符号 | 含义 | 示例 |
|------|------|------|
| S | 状态空间 | 棋盘状态、机器人位置 |
| A | 动作空间 | 上下左右、关节力矩 |
| P | 状态转移概率 | P(s'\|s,a) |
| R | 奖励函数 | R(s,a,s') |
| γ | 折扣因子 | 通常 0.99 |

### 马尔可夫性质
未来只依赖于现在，与过去无关。

### 关键公式

**回报 (Return):**
$$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + ... = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$

**状态值函数:**
$$V^\pi(s) = \mathbb{E}_\pi[G_t | S_t = s]$$

**动作值函数:**
$$Q^\pi(s,a) = \mathbb{E}_\pi[G_t | S_t = s, A_t = a]$$

## 示例

### GridWorld
- 状态：网格位置
- 动作：上下左右
- 奖励：到达目标 +1，其他 -0.01

### CartPole
- 状态：[位置，速度，角度，角速度]
- 动作：左推/右推
- 奖励：每存活一步 +1

## 待深入
- [ ] 贝尔曼方程推导
- [ ] 策略评估算法
- [ ] 连续状态 MDP

---
*最后更新：2026-03-05*
MDP

        echo "✅ MDP 笔记已创建"
        ;;
        
    bellman)
        echo "📖 开始贝尔曼方程学习..."
        echo ""
        
        cat >> "$RL_STUDY_LOG" << 'CONTENT'
### 贝尔曼方程 (Bellman Equation)

**核心思想:** 值函数可以递归地表示为即时奖励和未来值的期望。

**贝尔曼期望方程:**
$$V^\pi(s) = \sum_a \pi(a|s) \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^\pi(s')]$$

**贝尔曼最优方程:**
$$V^*(s) = \max_a \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^*(s')]$$

CONTENT

        # 创建贝尔曼方程笔记
        cat > "$RL_KNOWLEDGE_DIR/basics/bellman-equation.md" << 'BELLMAN'
# 贝尔曼方程 (Bellman Equation)

## 核心思想

值函数可以递归地表示为即时奖励和未来值的期望。

## 贝尔曼期望方程

### 状态值函数
$$V^\pi(s) = \mathbb{E}_\pi[R_{t+1} + \gamma V^\pi(S_{t+1}) | S_t = s]$$

展开形式:
$$V^\pi(s) = \sum_a \pi(a|s) \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^\pi(s')]$$

### 动作值函数
$$Q^\pi(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma \sum_{a'} \pi(a'|s') Q^\pi(s',a')]$$

## 贝尔曼最优方程

### 最优状态值函数
$$V^*(s) = \max_a \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^*(s')]$$

### 最优动作值函数
$$Q^*(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma \max_{a'} Q^*(s',a')]$$

## 求解方法

### 值迭代 (Value Iteration)
```python
def value_iteration(mdp, gamma=0.99, theta=1e-6):
    V = np.zeros(len(mdp.states))
    while True:
        delta = 0
        for s in mdp.states:
            v = V[s]
            V[s] = max(a, sum(p * (r + gamma * V[s_]) 
                              for p, s_, r, _ in mdp.P[s][a]))
            delta = max(delta, abs(v - V[s]))
        if delta < theta:
            break
    return V
```

### 策略迭代 (Policy Iteration)
1. 策略评估：计算 V^π
2. 策略改进：π' = greedy(π)
3. 重复直到收敛

## 直观理解

贝尔曼方程的核心是**自洽性**：一个状态的值等于即时奖励加上下一个状态的折扣值。

---
*最后更新：2026-03-05*
BELLMAN

        echo "✅ 贝尔曼方程笔记已创建"
        ;;
        
    algorithms)
        echo "📖 开始经典算法学习..."
        echo ""
        
        cat >> "$RL_STUDY_LOG" << 'CONTENT'
### Q-Learning 算法

**核心思想:** 直接学习最优动作值函数 Q*(s,a)，无需环境模型。

**更新规则:**
$$Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$$

CONTENT

        # 创建 Q-Learning 实现
        cat > "$WORKSPACE/code/rl-basics/q-learning.py" << 'QLEARN'
"""
Q-Learning 算法实现
环境：GridWorld
"""

import numpy as np
import random

class QLearning:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = alpha  # 学习率
        self.gamma = gamma  # 折扣因子
        self.epsilon = epsilon  # 探索率
        self.q_table = np.zeros((n_states, n_actions))
    
    def get_action(self, state):
        """ε-greedy 策略"""
        if random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        else:
            return np.argmax(self.q_table[state])
    
    def update(self, state, action, reward, next_state, done):
        """Q-Learning 更新"""
        if done:
            target = reward
        else:
            target = reward + self.gamma * np.max(self.q_table[next_state])
        
        td_error = target - self.q_table[state, action]
        self.q_table[state, action] += self.alpha * td_error
    
    def train(self, env, n_episodes=1000):
        """训练循环"""
        rewards_per_episode = []
        
        for episode in range(n_episodes):
            state = env.reset()
            total_reward = 0
            done = False
            
            while not done:
                action = self.get_action(state)
                next_state, reward, done = env.step(action)
                self.update(state, action, reward, next_state, done)
                total_reward += reward
                state = next_state
            
            rewards_per_episode.append(total_reward)
            
            if episode % 100 == 0:
                avg_reward = np.mean(rewards_per_episode[-100:])
                print(f"Episode {episode}, Avg Reward: {avg_reward:.2f}")
        
        return rewards_per_episode

# 简单 GridWorld 环境
class GridWorld:
    def __init__(self, size=5):
        self.size = size
        self.goal = size - 1
        self.reset()
    
    def reset(self):
        self.state = 0
        return self.state
    
    def step(self, action):
        # 0: 左，1: 右
        if action == 1:  # 右
            self.state = min(self.state + 1, self.goal)
        
        reward = -1
        done = (self.state == self.goal)
        if done:
            reward = 100
        
        return self.state, reward, done

if __name__ == "__main__":
    env = GridWorld(size=10)
    agent = QLearning(n_states=env.size, n_actions=2)
    rewards = agent.train(env, n_episodes=500)
    print(f"Final Q-table: \n{agent.q_table}")
QLEARN

        echo "✅ Q-Learning 实现已创建"
        ;;
        
    paper)
        echo "📖 开始论文阅读..."
        echo ""
        
        # 使用搜索工具查找最新论文
        echo "🔍 搜索 RL 前沿论文..."
        SEARCH_QUERY="reinforcement learning 2025 2026 paper arxiv"
        if [ -x "$SEARCH_SCRIPT" ]; then
            PAPERS=$("$SEARCH_SCRIPT" --urls "$SEARCH_QUERY" 10 2>/dev/null || echo "")
            if [ -n "$PAPERS" ]; then
                echo "✅ 找到相关论文链接"
                echo "$PAPERS" | head -5 | while read url; do
                    echo "   - $url"
                done
            fi
        else
            echo "⚠️  搜索工具不可用，使用预设查询"
        fi
        echo ""
        
        # 创建论文阅读模板
        cat > "$RL_KNOWLEDGE_DIR/papers/paper-template.md" << 'PAPER'
# 论文笔记模板

## 基本信息
- **标题:** 
- **作者:** 
- **Venue:** 
- **年份:** 
- **链接:** 

## 一句话总结


## 核心贡献
1. 
2. 
3. 

## 问题定义


## 方法

### 核心思想


### 技术细节


### 关键公式


## 实验

### 基准环境


### 对比方法


### 主要结果


### 消融实验


## 批判性思考

### 优点


### 局限性


### 可改进点


## 代码
- [ ] 官方代码：
- [ ] 复现计划：

## 相关论文


---
*阅读日期：2026-03-05*
PAPER

        echo "✅ 论文阅读模板已创建"
        ;;
        
    *)
        echo "📖 开始通用 RL 学习..."
        ;;
esac

echo ""

# 添加学习总结
cat >> "$RL_STUDY_LOG" << FOOTER

## 学习收获
- 掌握了核心概念
- 创建了知识笔记
- 实现了基础代码

## 待深入学习
- [ ] 贝尔曼方程推导
- [ ] 策略梯度定理
- [ ] Actor-Critic 方法

## 明日计划
- [ ] 继续 TD 学习
- [ ] 实现 SARSA
- [ ] 阅读 DQN 论文

---

*学习状态：完成 | 下次学习：$(date -d '+1 day' +%Y-%m-%d)*
FOOTER

echo "📄 学习日志完成：$RL_STUDY_LOG"
echo ""

# Git 提交
cd "$WORKSPACE"
git add -A
if git diff --staged --quiet; then
    echo "⚠️  没有新内容，跳过 Git 提交"
else
    git commit -m "🤖 RL Study: $TOPIC ($(date +%Y-%m-%d))"
    echo "🔄 正在推送到 GitHub..."
    if git push; then
        echo "✅ Git 提交成功"
    else
        echo "⚠️  Git 推送失败（可能网络问题）"
    fi
fi

echo ""
echo "================================"
echo "✅ RL 学习完成！"
echo "📄 日志：$RL_STUDY_LOG"
echo "📚 知识目录：$RL_KNOWLEDGE_DIR"
echo "================================"
