# 在线资料索引

30 天计划的每日题目、迷你练习和验收标准在本仓库内提供，单独克隆仓库即可执行。以下 15 项补充资料均提供仓库内的 **在线阅读正文**，点击每项的“在线阅读”即可打开，无需原资料库。补充阅读用于查漏，不计入必须完成的全量阅读任务。

`readers/` 保存可读的派生 Markdown；[导出清单](publish_manifest.json) 记录来源与哈希，便于核对正文版本。Notebook 正文保留相关说明与代码，去除输出和运行 metadata，并排除与学习任务无关的计费、网络与凭证单元；原文件在本地保留。

如需查看本地原文件，`materials.csv` 保存稳定材料 ID 和原资料的相对路径。`relative_path` 相对于你自己的原始资料库根目录；原始文件不随本仓库上传。**本地定位是可选功能**，可设置 `SOURCE_ROOT` 后从本仓库根目录执行：

```bash
export SOURCE_ROOT='/path/to/your/source-materials'
python3 scripts/study.py material core_questions --source-root "$SOURCE_ROOT"
```

把命令里的 `core_questions` 换成下列 ID 即可。命令只定位原文件，不执行源 Notebook。没有原资料库时，使用下方在线正文和当天仓库内练习即可。

## 题库与概率

<a id="core_questions"></a>
### core_questions · 可直接训练题库

- [在线阅读](readers/core_questions.md)
- 原路径：`datasets/reclassified/题库_可直接训练.csv`
- 用法：按当天主题选择少量补充题，先闭卷解题，再核对来源和题面。
- 边界：“可直接训练”是整理阶段标签，仍可能有多题合并、截断或公式问题。遇到不完整记录时跳过并留下问题，不猜补题意。
- 定位：`python3 scripts/study.py material core_questions --source-root "$SOURCE_ROOT"`

<a id="probability_notes"></a>
### probability_notes · 量化紫皮书概率笔记

- [在线阅读](readers/probability_notes.md)
- 原路径：`数学知识刷题/量化紫皮书.tex`
- 用法：查对应概率模型、条件概率或期望推导，一次只补一个知识点。
- 边界：本地整理讲义；计划无需读完全书或编译 TeX，优先完成当天自带题。
- 定位：`python3 scripts/study.py material probability_notes --source-root "$SOURCE_ROOT"`

## 算法与数据结构

<a id="hot100_hash"></a>
### hot100_hash · 哈希母题专项

- [在线阅读](readers/hot100_hash.md)
- 原路径：`hot100/哈希母题专项Notebook.ipynb`
- 用法：对照映射、计数和查找模板，写出键和值的含义，再手写一道变式。
- 边界：阅读示例不计作独立解题；原 Notebook 不搬入本仓库。
- 定位：`python3 scripts/study.py material hot100_hash --source-root "$SOURCE_ROOT"`

<a id="hot100_window"></a>
### hot100_window · 窗口母题专项

- [在线阅读](readers/hot100_window.md)
- 原路径：`hot100/窗口母题专项Notebook.ipynb`
- 用法：说明何时扩张、何时收缩，以及窗口内状态如何更新。
- 边界：先自己写出不变量，再查模板；不自动执行源 Notebook。
- 定位：`python3 scripts/study.py material hot100_window --source-root "$SOURCE_ROOT"`

<a id="hot100_binary"></a>
### hot100_binary · 二分母题专项

- [在线阅读](readers/hot100_binary.md)
- 原路径：`hot100/二分母题专项Notebook.ipynb`
- 用法：查区间定义、循环条件和左右边界更新，补空输入与重复值案例。
- 边界：以自己能解释终止条件和复杂度为完成标准。
- 定位：`python3 scripts/study.py material hot100_binary --source-root "$SOURCE_ROOT"`

<a id="hot100_dp1"></a>
### hot100_dp1 · 动态规划 I 母题专项

- [在线阅读](readers/hot100_dp1.md)
- 原路径：`hot100/动态规划I母题专项Notebook.ipynb`
- 用法：对照状态、转移、初始化和遍历顺序，写出小规模手算表。
- 边界：30 小时只覆盖基础动态规划的一轮训练，扩展题可留到后续。
- 定位：`python3 scripts/study.py material hot100_dp1 --source-root "$SOURCE_ROOT"`

<a id="hot100_stack"></a>
### hot100_stack · 栈队列堆母题专项

- [在线阅读](readers/hot100_stack.md)
- 原路径：`hot100/栈队列堆母题专项Notebook.ipynb`
- 用法：核对栈、队列的题型信号，解释元素入队出队和总复杂度。
- 边界：材料还包含堆等内容，按当天范围选择，不追加整本任务。
- 定位：`python3 scripts/study.py material hot100_stack --source-root "$SOURCE_ROOT"`

<a id="hot100_tree"></a>
### hot100_tree · 二叉树母题专项

- [在线阅读](readers/hot100_tree.md)
- 原路径：`hot100/二叉树母题专项Notebook.ipynb`
- 用法：对照递归函数返回值、终止条件与层序遍历，手写树的最小案例。
- 边界：通过例子不等于能处理所有树形结构，保留空树和单节点测试。
- 定位：`python3 scripts/study.py material hot100_tree --source-root "$SOURCE_ROOT"`

<a id="ds_notes"></a>
### ds_notes · 数据结构系统笔记优化版

- [在线阅读](readers/ds_notes.md)
- 原路径：`数据结构笔记与Notebook/数据结构系统笔记_优化版.md`
- 用法：查概念、题型识别、模板原因和复杂度，用来解释自己的解法。
- 边界：这是较完整的长笔记，30 天按需读取相关章节。
- 定位：`python3 scripts/study.py material ds_notes --source-root "$SOURCE_ROOT"`

## 量化岗位与业务

<a id="qr_wiki"></a>
### qr_wiki · 量化交易策略研究员岗位地图

- [在线阅读](readers/qr_wiki.md)
- 原路径：`业务复习/量化岗位笔试Wiki/01_岗位地图/量化交易策略研究员.md`
- 用法：用“假设、点时数据、样本外、组合、成本、实盘归因”串起一道研究题。
- 边界：来自跨资料归纳，不代表任何公司现行考纲或出题频率。
- 定位：`python3 scripts/study.py material qr_wiki --source-root "$SOURCE_ROOT"`

<a id="qd_wiki"></a>
### qd_wiki · 量化开发工程师岗位地图

- [在线阅读](readers/qd_wiki.md)
- 原路径：`业务复习/量化岗位笔试Wiki/01_岗位地图/量化开发工程师.md`
- 用法：沿输入契约、状态、并发、故障、观测与验证回答系统设计题。
- 边界：延迟预算和技术选型需要结合负载测量；笔记中的规则需另行核实。
- 定位：`python3 scripts/study.py material qd_wiki --source-root "$SOURCE_ROOT"`

<a id="data_wiki"></a>
### data_wiki · 量化数据工程师岗位地图

- [在线阅读](readers/data_wiki.md)
- 原路径：`业务复习/量化岗位笔试Wiki/01_岗位地图/量化数据工程师.md`
- 用法：解释数据何时可见、字段语义、质量校验、血缘和事故恢复。
- 边界：阅读用于建立框架，生产管道正确性还需实现与回放验证。
- 定位：`python3 scripts/study.py material data_wiki --source-root "$SOURCE_ROOT"`

<a id="factor_ic"></a>
### factor_ic · 因子研究与 IC 测试入口

- [在线阅读](readers/factor_ic.md)
- 原路径：`业务复习/factor_research_ic/README.md`
- 用法：从入口选择未来收益对齐、IC、分层回测或中性化的一个小节。
- 边界：该专题侧重向量化筛选；订单、排队和撮合敏感策略需另建事件驱动仿真。
- 定位：`python3 scripts/study.py material factor_ic --source-root "$SOURCE_ROOT"`

<a id="microstructure"></a>
### microstructure · 高频做市基本知识

- [在线阅读](readers/microstructure.md)
- 原路径：`业务知识/高频做市基本知识.md`
- 用法：解释订单簿、价差、库存、逆向选择、延迟与费用对净收益的作用。
- 边界：本地业务笔记的经验数字、市场规则和产品能力不视作当前核验结论。
- 定位：`python3 scripts/study.py material microstructure --source-root "$SOURCE_ROOT"`

<a id="optiver_overview"></a>
### optiver_overview · 2026 三类测评知识点总览

- [在线阅读](readers/optiver_overview.md)
- 原路径：`Optiver_笔试资料整理/03_notes/2026_三类测评知识点总览.md`
- 用法：补充概率估算、数列识别与短时练习，并区分题面证据和整理者推断。
- 边界：文件名中的 2026 是本地材料标签。部分内容来自 OCR 与录屏推断，不能据此确认当前官方测评名称、时长、评分或题型规则。
- 定位：`python3 scripts/study.py material optiver_overview --source-root "$SOURCE_ROOT"`

材料统计与计划完成口径见 [scope.md](scope.md)。页面预览临时失败时，使用 [Markdown 与 CSV 原文备用入口](TROUBLESHOOTING.md)。
