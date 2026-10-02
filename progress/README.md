# 进度记录

`progress.csv` 是 30 个学习日的当前总表；`log.csv` 是追加式作答日志。创建仓库时所有学习日均为 `not_started`，累计分钟为 0。源资料库原有的 `study_state/` 不受此仓库修改影响。

| 状态 | 含义 |
|---|---|
| not_started | 尚未记录该日训练 |
| in_progress | 已开始，还未完整验收 |
| needs_review | 当日核心验收未通过，需要补练 |
| completed | 学习者确认当日验收通过 |

`result` 可为 `pass`、`partial`、`fail`，`help_used` 可为 `yes`、`no`、`unknown`。完成状态要求正的实际用时、`pass` 结果和非空总结；它仍属于用户自报，并非工具对知识掌握度的认证。

`actual_minutes` 是当天各次记录的累计分钟。日志逐次保留本次用时、结果、提示使用情况和总结。记录超过 60 分钟时工具会提醒超出原预算，并保存真实用时。

有作答结果时，`review_date` 使用实际记录日期加两天。记录命令也会将这次总结追加到 `notes/dayNN.md`，已有笔记不会覆盖。

GitHub 上编辑笔记后，先拉取同步再记录本地进度；发生冲突时保留双方真实作答记录。
