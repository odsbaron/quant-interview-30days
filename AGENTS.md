# 维护约定

- 这是 30 天、每天 60 分钟的量化笔面试训练仓库。调整计划时保持时间预算，并解释范围变化。
- `days/` 保存当天任务，`notes/` 保存实际作答，`progress/` 保存用户自报进度。不要把创建模板、运行校验或 AI 生成答案记作用户完成学习。
- 保留已有笔记、进度和日志。修改计划不能覆盖历史作答。
- 原资料库只通过 `resources/materials.csv` 的相对路径引用；不上传原 PDF、视频、Notebook、镜像或凭证。
- 学习脚手架故意保留 TODO。基础 CI 只验证计划与工具；学习者运行 `--check` 的失败不自动等同工具错误。
- 合成数据和教学回测只能说明方法，不能声称策略有投资价值。
- 修改跟踪工具后运行 `python3 scripts/validate_plan.py` 与 `python3 -m unittest discover -s tests -v`。
