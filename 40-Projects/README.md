# 项目管理和开发日志

**创建时间**: 2026-03-05  
**整理者**: 小虾 🦐 (OpenClaw Assistant)

---

## 📁 文件夹用途

`projects/` 用于存放：
- 项目管理文档
- 开发日志
- 技术方案设计
- 进度追踪
- 代码审查记录

---

## 📄 建议的文件结构

```
projects/
├── README.md                          # 本说明文件
├── project-name-1/                    # 项目 1
│   ├── overview.md                    # 项目概述
│   ├── dev-log.md                     # 开发日志
│   ├── design-docs/                   # 设计文档
│   └── meeting-notes/                 # 会议记录
├── project-name-2/                    # 项目 2
│   └── ...
└── archive/                           # 已归档项目
    └── completed-project/
```

---

## 📋 推荐模板

### 项目概述模板 (`overview.md`)
```markdown
# 项目名称

## 基本信息
- **创建日期**: YYYY-MM-DD
- **负责人**: 
- **状态**: 🟢 进行中 / 🟡 暂停 / 🔴 已完成

## 目标
简要描述项目目标和预期成果

## 技术栈
- 语言:
- 框架:
- 工具:

## 关键里程碑
| 日期 | 里程碑 | 状态 |
|------|--------|------|
| | | ⬜ |

## 相关链接
- GitHub:
- 文档:
- 设计稿:
```

### 开发日志模板 (`dev-log.md`)
```markdown
# 开发日志

## YYYY-MM-DD
### 完成
- [ ] 

### 问题
- 

### 下一步
- [ ] 

## YYYY-MM-DD
...
```

---

## 🔧 技能集成

### Task Master
使用 `skills/task-master/` 管理项目任务：
```bash
./task-master.sh add "任务描述" --project project-name
./task-master.sh list --project project-name
```

### Git Auto Review
代码提交前自动审查：
```bash
git diff --cached | ./git-review.sh
```

### Project Analyzer
新项目上手分析：
```bash
./project-analyzer.sh /path/to/project
```

---

## 📊 项目状态追踪

### 状态标识
| 标识 | 含义 | 说明 |
|------|------|------|
| 🟢 | Active | 正在进行中 |
| 🟡 | On Hold | 暂停/等待中 |
| 🔴 | Completed | 已完成 |
| ⚫ | Archived | 已归档 |

### 优先级标识
| 标识 | 含义 |
|------|------|
| 🔴 | P0 - 紧急重要 |
| 🟠 | P1 - 重要 |
| 🟡 | P2 - 一般 |
| 🟢 | P3 - 低优先级 |

---

## 📝 最佳实践

### 1. 每日更新
- 记录当天完成的工作
- 记录遇到的问题和解决方案
- 规划下一步任务

### 2. 决策记录
重要技术决策使用 ADR (Architecture Decision Record) 格式：
```markdown
## ADR-001: 技术选型

### 背景
需要选择 XX 技术

### 决策
选择 XXX

### 理由
1. ...
2. ...

### 后果
- 正面：...
- 负面：...
```

### 3. 会议记录
- 会前：明确议程
- 会中：记录决策和行动项
- 会后：24 小时内整理并发出

---

## 🦐 小虾备注

- 项目文件夹按需创建，不要预先建一堆空的
- 每个项目保持简洁，避免过度文档化
- 重要决策一定要记录，未来你会感谢现在的自己
- 需要项目分析或任务拆解，随时叫我

**最后更新**: 2026-03-05
