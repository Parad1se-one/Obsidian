# Obsidian 配置和模板

**创建时间**: 2026-03-05  
**整理者**: 小虾 🦐 (OpenClaw Assistant)

---

## 📁 文件夹用途

`.obsidian/` 是 Obsidian 的配置文件目录，包含：
- 应用设置
- 插件配置
- 模板文件
- 工作区布局
- 自定义样式

> ⚠️ **注意**: 这是 Obsidian 的系统目录，不要手动修改 JSON 配置文件，除非你知道自己在做什么。

---

## 📄 目录结构

```
.obsidian/
├── README.md                          # 本说明文件
├── app.json                           # 应用设置
├── appearance.json                    # 外观设置
├── core-plugins.json                  # 核心插件配置
├── workspace.json                     # 工作区布局
├── graph.json                         # 关系图设置
└── templates/                         # 模板文件夹
    └── Daily Conversation Template.md # 每日对话模板
```

---

## 📝 模板说明

### Daily Conversation Template.md
每日对话记录模板。

**使用方式**:
1. 在 Obsidian 中创建新笔记
2. 点击模板按钮或按快捷键
3. 选择 "Daily Conversation Template"

**模板内容**:
```markdown
# 📅 每日对话 | {{date}}

## 🕐 时间线
- **开始**: {{time}}
- **结束**: 

## 📋 今日主题
- 

## 💬 关键对话
### 话题 1
**时间**: 
**内容**: 

## ✅ 决策记录
- [ ] 

## 📌 待办事项
- [ ] 

## 🧠 灵感笔记
- 

---
*生成时间：{{date}} {{time}}*
```

---

## 🔧 Obsidian 配置建议

### 推荐插件
| 插件 | 用途 | 类型 |
|------|------|------|
| Templates | 模板管理 | 核心 |
| Daily Notes | 每日笔记 | 核心 |
| Calendar | 日历视图 | 社区 |
| Dataview | 数据查询 | 社区 |
| Kanban | 看板管理 | 社区 |
| Excalidraw | 绘图工具 | 社区 |

### 安装社区插件
1. 设置 → 第三方插件
2. 关闭安全模式
3. 浏览插件 → 搜索安装

---

## 🎨 外观定制

### 主题推荐
- **默认**: 简洁高效
- **Minimal**: 极简风格
- **Things**: 类似 Things 3
- **Blue Topaz**: 功能丰富

### 安装主题
1. 设置 → 外观 → 主题
2. 管理 → 浏览
3. 选择并安装

---

## 📊 工作区布局

当前配置的工作区包含：
- 左侧：文件浏览器
- 中间：编辑区域
- 右侧：大纲/反向链接

可以通过 `workspace.json` 保存和恢复工作区布局。

---

## 🔗 同步配置

### Git 同步
当前仓库已通过 Git 管理，配置会自动同步到 GitHub。

```bash
# 拉取最新配置
git pull origin main

# 提交配置更改
git add .obsidian/
git commit -m "🔧 Update Obsidian config"
git push
```

### 注意事项
- `.obsidian/workspace.json` 包含个人化布局，可能不适合多设备
- 建议在个人设备上单独配置工作区
- 模板和核心配置可以安全同步

---

## 📝 最佳实践

### 1. 模板使用
- 为常用笔记类型创建模板
- 使用变量：`{{date}}`, `{{time}}`, `{{title}}`
- 模板放在 `templates/` 文件夹

### 2. 文件组织
- 使用一致的命名规范
- 合理分类到不同文件夹
- 使用标签（#tag）进行跨分类关联

### 3. 双向链接
- 多使用 `[[链接]]` 建立知识网络
- 定期查看反向链接发现关联
- 使用关系图可视化知识结构

---

## 🦐 小虾备注

- `.obsidian/` 是 Obsidian 的核心配置，不要乱动 JSON 文件
- 模板可以随时修改，我会帮你同步
- 需要新模板或配置调整，跟我说
- 配置冲突时，优先保留你的个人偏好设置

**最后更新**: 2026-03-05
