# Learnings Log

> 自动记录纠正、知识缺口、最佳实践
> Skill: self-improving-agent

---

## [LRN-20260311-001] best_practice

**Logged**: 2026-03-11T09:40:00+08:00
**Priority**: high
**Status**: resolved
**Area**: backend

### Summary
训练脚本必须追踪真实任务完成度 (completed_ratio)，而非仅用 reward 做对比

### Details
之前的 DRAMA 训练脚本只记录 episode reward，不同算法使用不同的 reward function（有的正数有的负数），导致横向对比无意义。用户指出"单纯的 Reward 横向比较没有意义"，需要追踪真实的任务完成度。

### Suggested Action
- 环境 `grid_env.py` 新增 `get_completion_ratio()` 和 `is_all_done()` 方法
- 所有训练脚本在每个 episode 结束时调用这两个方法
- `training_stats.json` 必须包含 `completed_ratio` 和 `success` 字段

### Resolution
- **Resolved**: 2026-03-11T09:45:00+08:00
- **Notes**: 已修复 grid_env.py，创建 train_unified.py 统一训练框架

### Metadata
- Source: user_feedback
- Related Files: envs/grid_env.py, train_unified.py
- Tags: drama, training, metrics, completion_ratio

---

## [LRN-20260311-002] correction

**Logged**: 2026-03-11T09:42:00+08:00
**Priority**: high
**Status**: resolved
**Area**: backend

### Summary
grid_env.py 的 reset() 硬编码了默认 env_config，导致 Medium 配置无法正确重置

### Details
`GridAreaEnv.reset()` 方法中 `config = env_config` 硬编码了默认配置，而不是使用构造时传入的 config。这导致 Medium 难度的环境在 reset 后会回到 Easy 的默认配置。

### Suggested Action
在 `__init__` 中保存 `self._config = config`，`reset()` 使用 `self._config`

### Resolution
- **Resolved**: 2026-03-11T09:43:00+08:00
- **Notes**: 已修复，reset() 现在使用构造时的 config

### Metadata
- Source: error
- Related Files: envs/grid_env.py
- Tags: drama, environment, bug, reset

---

## [LRN-20260311-003] best_practice

**Logged**: 2026-03-11T08:16:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
OpenClaw 模型配置需要同时修改 openclaw.json 和 agents/main/agent/models.json

### Details
修改 models.json 后模型没有切换，因为 openclaw.json 中的 `agents.defaults.model.primary` 仍指向旧模型。两个文件都需要更新，且需要重启 Gateway 才能生效。

### Suggested Action
修改模型配置时，检查清单：
1. `~/.openclaw/agents/main/agent/models.json` — provider + 模型定义
2. `~/.openclaw/openclaw.json` — `agents.defaults.model.primary` 指向
3. `openclaw gateway restart` — 重启生效

### Metadata
- Source: error
- Related Files: openclaw.json, agents/main/agent/models.json
- Tags: openclaw, config, model, gateway

---
