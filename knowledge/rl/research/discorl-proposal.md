# Knowledge Distillation for Continual Reinforcement Learning: A Research Proposal

**Based on:** DisCoRL: Continual Reinforcement Learning via Policy Distillation (Traoré et al., 2019)

**Date:** 2026-03-06  
**Author:** Research Agent (Subagent)

---

## 1. Background & Motivation

### 1.1 The DisCoRL Foundation

DisCoRL addresses three core challenges in reinforcement learning:
1. **Multi-task learning**: Learning different policies with a single model at training time
2. **Task inference**: Inferring which policy to apply at test time without external signals
3. **Continual learning**: Learning tasks sequentially without catastrophic forgetting

The key innovation is combining **state representation learning (SRL)** with **policy distillation**:
- SRL component: Inverse model + auto-encoder for learning compact state representations from raw observations
- Policy distillation: Transfers multiple sequentially-learned policies into a single unified policy

### 1.2 Limitations & Open Questions

While DisCoRL demonstrates promising results on 2D navigation tasks with a 3-wheel omni-directional robot, several limitations remain:

1. **Scalability**: Evaluated only on 3 sequential tasks; unclear how it scales to 10+ tasks
2. **Distillation efficiency**: Uses standard KL-divergence; newer distillation losses may improve performance
3. **Representation quality**: SRL trained separately from policy; joint training may yield better features
4. **Task complexity**: Limited to navigation; applicability to manipulation, locomotion unknown
5. **Sample efficiency**: Policy distillation requires collecting data from each teacher policy

---

## 2. Research Questions

### RQ1: Adaptive Distillation Scheduling
**Can we improve continual learning performance by adaptively scheduling distillation updates based on task similarity and forgetting metrics?**

- Hypothesis: Dynamic distillation frequency reduces interference between tasks while maintaining knowledge retention
- Motivation: Fixed distillation schedules may over-distill similar tasks or under-distill dissimilar ones

### RQ2: Joint SRL-Policy Optimization
**Does end-to-end joint training of state representation learning and policy distillation improve sample efficiency and final performance compared to DisCoRL's two-stage approach?**

- Hypothesis: Joint optimization creates task-invariant representations better suited for distillation
- Motivation: DisCoRL trains SRL first, then policy; representations may not be optimal for distillation

### RQ3: Hierarchical Distillation Architecture
**Can a hierarchical distillation architecture (task-specific heads + shared backbone) outperform DisCoRL's single-policy distillation for long task sequences?**

- Hypothesis: Hierarchical architecture balances specialization and generalization better for 10+ tasks
- Motivation: Single policy may suffer from capacity bottleneck as task count increases

### RQ4: Cross-Domain Transfer
**Does DisCoRL-style distillation enable positive transfer across domains (simulation→real, one robot morphology→another)?**

- Hypothesis: Distilled policies capture task-agnostic skills that transfer better than individual policies
- Motivation: DisCoRL tested sim→real for same robot; cross-morphology transfer unexplored

---

## 3. Experimental Design

### 3.1 Environments

| Environment | Task Sequence | Complexity |
|-------------|---------------|------------|
| **MetaWorld** | 10 manipulation tasks (reach, push, pick-place, etc.) | Medium |
| **DMC Continual** | 5 locomotion tasks (walk, run, jump, flip, climb) | Medium-High |
| **Custom Navigation** | 20 goal-reaching tasks with increasing obstacles | Low-Medium |
| **Sim2Real Manipulation** | 3 pick-place tasks (sim training, real evaluation) | High |

### 3.2 Baselines

1. **DisCoRL** (original implementation)
2. **Progressive Networks** (Rusu et al., 2016)
3. **PACKNET** (Mallya et al., 2018)
4. **A-GEM** (Chaudhry et al., 2019)
5. **Multi-task Oracle** (upper bound: joint training with task labels)

### 3.3 Proposed Methods

#### Method A: AdaDistill (Addresses RQ1)
- **Core idea**: Adaptive distillation triggered by:
  - Task similarity metric (representation cosine similarity)
  - Forgetting score (performance drop on previous tasks)
- **Algorithm**:
  ```
  For each new task T_i:
    1. Train policy π_i on T_i
    2. Compute similarity S(T_i, T_j) for all previous tasks
    3. If S < threshold OR forgetting > threshold:
       Distill {π_1...π_i} → π_distilled
    4. Else: Continue without distillation
  ```

#### Method B: Joint-SRL-Distill (Addresses RQ2)
- **Core idea**: End-to-end training with combined loss:
  ```
  L_total = L_RL + λ1·L_inverse + λ2·L_recon + λ3·L_distill
  ```
- **Architecture**: Shared encoder feeds both SRL heads and policy head
- **Training**: Single-stage optimization instead of DisCoRL's two-stage

#### Method C: Hierarchical Distillation (Addresses RQ3)
- **Architecture**:
  - Shared backbone encoder (task-agnostic features)
  - Task-specific policy heads (gated by task inference module)
  - Distillation applied to both backbone and heads
- **Task inference**: Attention-based gating network learns to select heads

### 3.4 Evaluation Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **Forward Transfer (FWT)** | Performance on T_i after training on T_1...T_{i-1} | Higher is better |
| **Backward Transfer (BWT)** | Performance change on T_j after training on T_i (j<i) | Closer to 0 is better |
| **Average Performance (AP)** | Mean performance across all tasks after final training | Higher is better |
| **Forgetting Measure (FM)** | max performance - final performance on each task | Lower is better |
| **Sample Efficiency** | Environment steps to reach 80% of final performance | Lower is better |
| **Task Inference Accuracy** | % of correct task identification without labels | Higher is better |

### 3.5 Experimental Protocol

**Phase 1: Reproduction (Weeks 1-4)**
- Reproduce DisCoRL results on original navigation task
- Establish baseline performance metrics

**Phase 2: Method Development (Weeks 5-12)**
- Implement AdaDistill, Joint-SRL-Distill, Hierarchical Distillation
- Ablation studies on MetaWorld (5 tasks)

**Phase 3: Comprehensive Evaluation (Weeks 13-20)**
- Full evaluation on all environments
- Compare against all baselines
- Statistical significance testing (5 seeds per experiment)

**Phase 4: Sim2Real Transfer (Weeks 21-24)**
- Deploy best method on real robot manipulation tasks
- Measure sim2real gap vs. baselines

---

## 4. Expected Contributions

### 4.1 Theoretical Contributions
1. **Distillation scheduling theory**: Framework for when/how often to distill in continual RL
2. **Joint optimization analysis**: Characterization of SRL-policy interaction in distillation context
3. **Capacity bounds**: Analysis of task count limits for single-policy vs. hierarchical distillation

### 4.2 Empirical Contributions
1. **Benchmark results**: Comprehensive evaluation on MetaWorld, DMC Continual, and custom tasks
2. **Best practices**: Guidelines for distillation hyperparameters, architecture choices
3. **Open-source release**: PyTorch implementation of all methods with reproduction scripts

### 4.3 Practical Contributions
1. **Sim2Real demonstration**: Real-robot validation of continual distillation approach
2. **Sample efficiency improvements**: Reduced training time for multi-task robot learning
3. **Task-agnostic deployment**: Single policy handling multiple tasks without task labels

---

## 5. Potential Challenges & Mitigations

| Challenge | Risk Level | Mitigation Strategy |
|-----------|------------|---------------------|
| **Computational cost** of joint training | Medium | Use gradient accumulation; distributed training |
| **Hyperparameter sensitivity** | High | Extensive ablation studies; automated HPO |
| **Real-robot experimental variance** | High | Multiple trials; domain randomization |
| **Negative transfer** in hierarchical method | Medium | Regularization; task clustering pre-processing |
| **Reproduction difficulties** | Low | Early engagement with original authors; detailed logs |

---

## 6. Timeline & Milestones

| Month | Milestone | Deliverable |
|-------|-----------|-------------|
| M1 | DisCoRL reproduction complete | Reproduction report + code |
| M2 | AdaDistill implemented & tested | Preliminary results on MetaWorld |
| M3 | Joint-SRL-Distill complete | Ablation study results |
| M4 | Hierarchical Distill complete | All methods implemented |
| M5 | Full evaluation complete | Comparison tables, statistical analysis |
| M6 | Sim2Real experiments | Real-robot video demonstrations |
| M7 | Paper writing | Draft manuscript |
| M8 | Submission | Camera-ready + code release |

---

## 7. References

1. Traoré, R., Caselles-Dupré, H., Lesort, T., Sun, T., Cai, G., Díaz-Rodríguez, N., & Filliat, D. (2019). **DisCoRL: Continual reinforcement learning via policy distillation**. arXiv:1907.05855.

2. Rusu, A. A., et al. (2015). **Policy distillation**. arXiv:1511.06295.

3. Raffin, A., et al. (2019). **Decoupling feature extraction from policy learning**. arXiv:1906.04452.

4. Czarnecki, W. M., et al. (2019). **Distilling policy distillation**. AISTATS.

5. Chaudhry, A., et al. (2019). **Efficient lifelong learning with A-GEM**. ICLR.

---

## 8. Notes for Future Work

- Explore **online distillation** (distill while learning, not after)
- Investigate **multi-teacher distillation** with attention mechanisms
- Consider **meta-learning initialization** for faster task adaptation
- Extend to **multi-agent continual RL** settings

---

*This proposal builds directly on DisCoRL's foundation while addressing its key limitations. The four research questions target fundamental challenges in continual RL that remain open despite recent advances.*
