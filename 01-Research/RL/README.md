# RL Vault Structure

当前按两条独立流水线来跑：

## 1. DeepRead 生产线
- 来源：arXiv + 高可信会议/期刊线索
- 频率：每 2 小时一轮
- 目标：挑值得精读的 RL 相关论文
- 输出目录：`DeepReads/`

## 2. 日报生产线
- 频率：每天早上 / 晚上各一次
- 输入：扫描当天新增的 `DeepReads/`
- 输出目录：`Daily/`

## 目录说明
- `DeepReads/`：自动精读产物池
- `Daily/`：早报 / 晚报
- `Papers/`：轻量论文卡片与长期资料
- `Archive/`：历史遗留内容，默认不参与新工作流

## 目前约定
- 新的深读结果直接写入 `DeepReads/YYYY-MM/`
- 当天摘要从 `DeepReads/` 抽取，不再经过 Inbox
- 历史旧目录全部视为归档，不再作为主入口
