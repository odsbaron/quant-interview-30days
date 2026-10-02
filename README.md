# 量化笔面试：30 天，每天 1 小时

从 **2026-10-02 到 2026-10-31**，用 30 个小时建立概率统计、常用算法和量化研究的基础训练闭环。路线偏量化研究，同时补开发与数据工程的共同基础。

每一天都有完整练习题面、时间分配、提示和验收条件。原资料库用于补充阅读；只使用这个仓库也能开始练习。

## 今天开始

1. 打开 [开始指南](START_HERE.md) 和 [Day 01](days/day01.md)。
2. 按当天时间块独立作答，把结果写入 [第一天笔记](notes/day01.md)。
3. 跑第一天起步练习：`python3 exercises/day01.py`。完成 TODO 后再运行 `python3 exercises/day01.py --check`。
4. 根据真实作答记录进度，示例见下方。首次仓库创建不计作学习完成。

```bash
python3 scripts/study.py today
python3 scripts/study.py day 1
python3 scripts/study.py status
```

仅需 Python 3.10 或更新版本，无须安装第三方依赖。推荐从仓库根目录执行命令。

## 30 天安排

完整路线：[30 天计划](plan/30_days.md) · [可编辑 CSV](plan/30_days.csv)

| 阶段 | 天数 | 主任务 |
|---|---|---|
| 建立起点 | 1—7 | 期望、条件概率、方差；哈希与窗口；首次复盘 |
| 学会验证 | 8—14 | 回归、检验、正则化、时序泄漏；二分与 DP |
| 接入研究 | 15—21 | IC、中性化、成本、时序验证；堆与树 |
| 串联业务 | 22—28 | 订单簿、做市、时间对齐；简化回测练习与复盘 |
| 验收与分流 | 29—30 | 原创限时模拟、总结、下一阶段岗位分支 |

默认每天 **5 分钟复习 + 10 分钟阅读 + 35 分钟练习 + 10 分钟记录**。检查日减少新内容；到 60 分钟就记录卡点，未通过项转入补练。复习方法和缺席处理见 [复盘规则](plan/review_rules.md)。

## 记录真实进度

先创建或打开当天笔记（存在时不会覆盖）：

```bash
python3 scripts/study.py note 1
```

当天实际通过验收后再使用以下示例；其中结果和总结由自己填写：

```bash
python3 scripts/study.py record 1 --status completed --minutes 60 --result pass --help-used no --summary "填写自己的推导、代码验收结果和易错点"
```

未通过或依赖提示时照实记录，例如：

```bash
python3 scripts/study.py record 1 --status needs_review --minutes 60 --result partial --help-used yes --summary "填写尚未完成的部分与下次复习任务"
```

状态由学习者自报，`completed` 表示当天验收通过，不能据此推定已长期掌握。工具会更新 [每日进度](progress/progress.csv)、追加 [作答日志](progress/log.csv)，并在有作答结果时设置两天后的复习日期。每次记录的分钟数是本次实际用时，日志保存每次尝试；总表显示该天累计用时。

## 材料与练习

- [本地材料索引](resources/README.md)：定位已有概率讲义、HOT100 和岗位 Wiki。
- [范围与来源](resources/scope.md)：说明题库标签、历史公司材料和覆盖边界。
- [练习入口](exercises/README.md)：第一天的代码起步模板。
- [回测练习](exercises/mini_project/README.md)：固定合成价格数据与实现脚手架。
- [每日笔记模板](templates/daily_note.md)：记录推导、代码、错误和口述。

从其他目录克隆后，可用 `--source-root` 指定原资料库，或设置 `QUANT_SOURCE_ROOT`。仓库中不包含原 PDF、录屏、Notebook 或开源镜像。

## 校验

```bash
python3 scripts/validate_plan.py
python3 -m unittest discover -s tests -v
```

以上只验证计划、引用和进度工具。第一天和回测脚手架的 `--check` 用于检查自己完成的代码，初始 TODO 状态下应当提示尚未完成。
