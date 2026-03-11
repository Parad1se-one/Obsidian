# Errors Log

> 命令失败、异常、意外行为记录
> Skill: self-improving-agent

---

## [ERR-20260311-001] feishu_doc_read

**Logged**: 2026-03-11T07:44:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
feishu_doc read 操作返回 400 错误

### Error
```
Request failed with status code 400
```

### Context
- 尝试读取飞书文档 `ISeFwuMdVif2rMkLuMRc14Tdnhb`
- URL: `https://my.feishu.cn/wiki/ISeFwuMdVif2rMkLuMRc14Tdnhb`
- 可能是 wiki 链接需要先通过 feishu_wiki 获取 doc_token

### Suggested Fix
wiki 链接可能需要先用 `feishu_wiki` 的 `get` action 获取实际的 doc_token，再用 `feishu_doc` 读取

### Metadata
- Reproducible: unknown
- Related Files: N/A
- Tags: feishu, wiki, doc, api

---

## [ERR-20260311-002] subagent_medium_trainer

**Logged**: 2026-03-11T07:42:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: infra

### Summary
Medium 训练 subagent 中 MAPPO-RM 和 DQN 训练异常

### Error
```
MAPPO-RM: 29/500 (6%) - 进程死亡
DQN: 0/500 (0%) - 卡死 9+ 小时
```

### Context
- 2026-03-10 启动的 medium-trainer subagent
- MAPPO, IPPO-RM, IPPO 正常完成 500 episodes
- MAPPO-RM 进程在 29 episodes 后死亡
- DQN 进程 CPU 93% 但无进展

### Suggested Fix
检查 MAPPO-RM 和 DQN 的内存使用和日志，可能是 OOM 或死循环

### Resolution
- **Resolved**: 2026-03-11T09:40:00+08:00
- **Notes**: 清理旧实验，使用 train_unified.py 重新跑

### Metadata
- Reproducible: unknown
- Related Files: train_mappo_medium_rm.py, train_dqn_medium.py
- Tags: drama, training, crash, oom

---
