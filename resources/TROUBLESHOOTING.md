# 资料阅读与页面加载

## 在线正文入口

[资料索引](README.md) 中的 15 个“在线阅读”入口均指向仓库内 Markdown。Notebook 学习内容已经转为静态正文和代码块，概率讲义按章节拆分，题库按分类拆分。原文件留在本地，用于继续运行或追溯来源。

## GitHub 预览临时失败

如果 GitHub 显示 `Error loading page` 或 `An unexpected error occurred`，先使用 Markdown 入口。CSV 原文也可直接读取，不依赖 GitHub 的表格预览：

- [30 天计划 Markdown](../plan/30_days.md) · [计划 CSV 原文](https://raw.githubusercontent.com/odsbaron/quant-interview-30days/main/plan/30_days.csv)
- [资料索引 Markdown](README.md) · [材料 CSV 原文](https://raw.githubusercontent.com/odsbaron/quant-interview-30days/main/resources/materials.csv)
- [合成数据说明](../exercises/mini_project/README.md) · [价格 CSV 原文](https://raw.githubusercontent.com/odsbaron/quant-interview-30days/main/exercises/data/synthetic_prices.csv)
- [进度记录说明](../progress/README.md) · [进度 CSV 原文](https://raw.githubusercontent.com/odsbaron/quant-interview-30days/main/progress/progress.csv)

GitHub 页面或网络临时失败与文件损坏需要分别验证。上传后的完整性由 [发布清单](publish_manifest.json) 中的文件长度、SHA-256 与远端文件校验确认；页面错误文案本身不能证明文件损坏。

## 本地校验

```bash
python3 scripts/validate_plan.py
python3 -m unittest discover -s tests -v
```

重新生成可读正文时才需要 Pandoc 与原资料库；日常学习与 CI 不需要它们：

```bash
python3 scripts/export_readers.py --source-root "$QUANT_SOURCE_ROOT"
```

导出不执行源 Notebook，不改变当天笔记或学习进度。再次导出后必须重新校验相对链接、锚点、发布清单与凭证清理结果。
