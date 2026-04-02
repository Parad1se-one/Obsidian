# Paper | Solving Multi-Agent Safe Optimal Control with Distributed Epigraph Form MARL

- arXiv: http://arxiv.org/abs/2504.15425
- PDF: http://arxiv.org/pdf/2504.15425.pdf
- 本地源 HTML: `[[01-Research/RL/Sources/2026-04/22-solving-multi-agent-safe-optimal-control-with-distributed-epigraph-form-marl-arxiv.html]]`
- 本地归档 PDF: `[[01-Research/RL/Sources/2026-04/22-solving-multi-agent-safe-optimal-control-with-distributed-epigraph-form-marl-arxiv-html.pdf]]`
- 本地全文: `[[01-Research/RL/Sources/2026-04/22-solving-multi-agent-safe-optimal-control-with-distributed-epigraph-form-marl-arxiv-html-fulltext.md]]`
- Venue: RSS 2025
- 发布时间: 2025-04-22
- 分类: cs.RO, cs.AI, cs.LG, cs.MA, math.OC
- 作者: Songyuan Zhang, Oswin So, Mitchell Black, Zachary Serlin, Chuchu Fan
- 证据等级: 高
- 证据来源: arXiv 摘要 + arXiv HTML 正文 + 项目页 + OpenReview 摘要
- 本地 PDF: 已使用 arXiv HTML 生成阅读版归档 PDF（非原始 arXiv 排版 PDF）
- 项目页: https://mit-realm.github.io/def-marl/

---

## 这篇论文到底在解决什么

这篇盯的是 **离散时间 multi-agent safe optimal control**，不是泛泛 safe MARL。

它的核心问题是：

- 现有 safe MARL 很多写成 CMDP
- CMDP 常用的是“平均约束违反低于阈值”
- 但真实机器人系统经常要的是 **zero constraint violation**
- 一旦把阈值真设成 0，Lagrangian / CMDP 训练就容易发疯
- 多智能体场景下再要求 distributed execution，问题更难

所以这篇真正想解决的是：

> **在离散时间、多智能体、分布式执行的 setting 下，如何做 hard-safety optimal control，同时避免 zero-threshold Lagrangian 训练崩掉。**

---

## 核心方法

### 1. 不再停留在 CMDP 零阈值修补
作者直接把问题写成 **MASOCP（multi-agent safe optimal control problem）**：

- 最小化全局任务 cost
- 同时保证各 agent 的安全约束全程满足

### 2. 用 epigraph form 重写约束优化
论文定义：

- 任务 cost value `V^l`
- 每个 agent 的 constraint value `V_i^h`

然后构造一个 `z`-条件化的 epigraph 目标：

`V(x, z; π) = max{ max_i V_i^h(o_i; π), V^l(x; π) - z }`

这个结构的好处是：
- 约束紧时，constraint branch 主导
- 安全满足后，cost branch 才主导

比 Lagrange multiplier 那种在 zero-threshold 下容易乱跳的训练方式更稳。

### 3. 证明外层问题能 distributed solve
这篇最关键的地方不只是“用了 epigraph”。
而是它证明：

- centralized epigraph outer problem
- 可以被拆成各个 agent 局部求 `z_i`
- 最后再组合成全局可执行的 distributed policy

所以它才能真正站在 **CTDE** 这边，而不是假装 distributed、实际还是 centralized。

---

## 它为什么重要

这篇就是后面那篇 continuous-time epigraph 论文的离散时间前作。

你可以把关系理解成：

- **Def-MARL**：离散时间 epigraph-safe-MARL 主线
- **Safe Continuous-time MARL via Epigraph Form**：把这条线继续推进到 continuous-time，并进一步修传统 epigraph 的训练/执行缺点

也就是说，后作不是凭空出现。  
它是在这篇基础上继续改：

- 这篇：传统 epigraph，执行期还要认真处理外层 `z`
- 后作：进一步想把 inner / outer optimization 搞得更稳，并减少 root-finding / z-sampling 的麻烦

---

## 实验到底测了什么

实验覆盖：

- 8 个任务
- 2 个 simulator
  - MPE
  - Safe Multi-agent MuJoCo
- varying numbers of agents
- Crazyflie 硬件实验

作者给出的主结论：

- Def-MARL 训练更稳定
- 在满足安全约束的同时保持强性能
- 既不像保守 baseline 那样安全但笨，也不像激进 baseline 那样快但违规
- 硬件上能比 centralized / decentralized MPC 做得更好

如果这些都成立，那它的价值就不只是“仿真上有效”，而是对真实 multi-robot safe coordination 也有一定说服力。

---

## 这篇论文目前可确认的贡献

### C1. 把 epigraph form 从单智能体 hard-constraint RL 扩到 MARL
这是主线贡献。

### C2. 证明 outer problem 可做 distributed execution
这是它能落在 CTDE 范式里的关键。

### C3. 提出 Def-MARL 算法
不是只给理论，还给了可训练的算法流程。

### C4. 给出仿真 + 硬件实验
这让它不只是数学故事。

---

## 我现在最该盯的风险点

### 1. outer `z` 求解到底有多贵
这是这篇最值得追问的工程问题。
因为 continuous-time 后作已经在点名批它这套“traditional epigraph”设计会带来：

- 训练时 z 相关噪声
- 执行时 root-finding / outer solve 成本

### 2. baseline 公平性
我最想继续核对：

- 所有 baseline 是否都在 zero-threshold 下公平比较
- 超参数有没有偏置
- safety / performance 指标到底怎么平衡

### 3. 扩展性
分布式是对的。  
但 agent 数和约束复杂度上去之后，还能不能稳，这才是真问题。

### 4. 安全定义是否足够真实
constraint function 设计得不对，数学上“安全”也可能不等于真实系统安全。

---

## 一句话结论

**这篇值得读，而且很关键。**

不是因为它名字大。  
而是因为它是：

> **离散时间 epigraph-safe-MARL → continuous-time epigraph-safe-MARL**

这条路线里非常像样的桥梁论文。

如果你要读后面那篇 continuous-time EPI，  
这篇基本就是前置阅读材料。

---

## 下一步该怎么读

如果继续深读，我建议优先盯：

1. distributed outer `z` solve 的理论条件
2. `z` 在训练/执行中的实际代价
3. baseline 是否公平
4. Crazyflie 实验到底有多接近真实难度
5. 它和后续 continuous-time EPI 到底改了哪些传统 epigraph 弱点
