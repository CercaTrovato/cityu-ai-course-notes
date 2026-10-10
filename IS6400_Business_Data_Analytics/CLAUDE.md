# CLAUDE.md — IS6400 Business Data Analytics（课程级）

> 通用方法论见 vault 根的 [CLAUDE.md](../CLAUDE.md)。工具无关版见 [AGENTS.md](AGENTS.md)。
> 课程背景见 [[IS6400_Business_Data_Analytics/_prep/课程前置资料|课程前置资料]]（已读 Syllabus，**官方目录待对校**）。

---

## 1. 这门课与其他四门的根本差异

**IS6400 是本 vault 集中训练数据分析技术实操的课程。** 其他四门讲"该不该做、怎么治理、用在哪"，这门讲"怎么做出来"。

这意味着**笔记形态不同**：

| | 其他四门 | IS6400 |
|---|---|---|
| 主体产出 | `notes/M<NN>-*.md` 讲义笔记 | `notes/M<NN>-*.md` 讲义笔记 **+** `notes/T<NN>-*.md` **代码讲解笔记** |
| 核心难点 | 陌生概念的解释密度 | **代码与理论的对应关系** |
| 配套材料 | — | `.ipynb`、`.csv`，规则见 [[材料处理规则#7. `.csv` / `.xlsx` 数据文件 ✅\|材料处理规则 › 7. `.csv` / `.xlsx` 数据文件 ✅]] 与 [[材料处理规则#8. `.ipynb` / `.py` 代码文件 ✅\|材料处理规则 › 8. `.ipynb` / `.py` 代码文件 ✅]] |

**每周是 lecture + hands-on tutorial 两段（近 3 小时）**，所以一周通常产出两个文件：讲义笔记 `M02` + tutorial 笔记 `T02`，两者互链。

---

## 2. ⚠️ L0 基线待确认（写代码笔记前必须解决）

本库的默认读者假设是"只有 AI/ML 基础，其余零基础"。**这条假设在这门课需要重新校准**：

| 内容 | 是否属 L0 |
|---|---|
| 线性回归、PCA、KMeans、DBSCAN、决策树、集成学习、ANN/RNN | **本讲核心使用时必须从零讲机制**，不能用 L0 免讲；见根 `_meta/机制理解与可读性标准.md` |
| Python 语法（循环、函数、类） | ❓ **未确认** |
| pandas / numpy / sklearn / statsmodels 的具体 API | ❓ **未确认** |
| 业务解读（"这个系数在业务上意味着什么"） | ❌ **不属 L0**，必须讲 |

**在用户确认之前的默认口径**：按「Python 语法熟悉、但特定库 API 不熟」来写——**不解释 `for` 循环，但解释 `sklearn` 的 `fit/predict` 约定、参数含义、以及为什么选这个函数**。

这条一旦确定，写进本课 `_meta/知识层级台账.md` 的 L0 节。

---

## 3. 这门课的特殊规则：GenAI Prompt 单元格

Tutorial notebook 里有形如下面的 markdown 单元格：

> `🤖 AI Prompt (Copy this to AI): Write Python code to import the 'datetime' library...`

**这是课程设计的一部分，不是噪音。** Syllabus 的 ILO 第 3 条明写 "Manage GenAI tools for BDA proposal and Python programming"，W11 还有一场 "Competition: GenAI for BDA"。

**规则**：这些 prompt **必须保留进代码讲解笔记**，并单列一节讨论「教师期望你怎么向 AI 提问」。这是会被考核的能力。

---

## 4. 考核决定笔记侧重

| 项目 | 权重 | 对笔记的要求 |
|---|---|---|
| **Exam** | **40%** | 需要能笔答的概念与推导，不只是会跑代码 |
| **Individual Assignments** ×约 8 | **25%** | 代码讲解笔记要能直接支撑做作业——**逐块讲清、参数可改** |
| Group Project（briefing 5 + 演示 15 + 报告 10） | **30%** | W6 就要开题 |
| Class Participation | 5% | **随机堂上小测 + 签到**，按答对次数占比计分 |

> ❗ **迟交惩罚是五门课里最重的**：个人作业**每天 -20%**（5 天归零），小组报告每天 -10%。
> ❗ **Participation 靠随机小测**——不知道哪节课抽，缺课直接丢分。
> ❗ **W6 就 Project Briefing**（约 10 月上中旬），开学一个月出头要定题。

---

## 5. 现有材料与阻塞项

✅ **材料已迁入 `course_files_export/`**（2026-09-08），符合 [[材料处理规则#0. 文件存放约定|材料处理规则 › 0. 文件存放约定]]。

| 文件 | 状态 |
|---|---|
| `IS6400_Syl_SemA_2026-27.pdf` | ✅ 已读，产出前置资料 |
| `IS6400-Week1.pdf` | ⚠️ 未读 |
| `L2-Linear_Regression.pdf` | ⚠️ 未读 |
| `IS6400 Project Guideline.pdf` | ⚠️ 未读 → 读完登记 `_meta/作业与DDL.md` + Notion |
| `Tutorial 1 - …_Prompt.ipynb` | 25 cells，Python 3.13.5，kernel `conda-base-py` |
| `Week 2 Regression Analysis_With Prompt.ipynb` | 39 cells，线性回归 + 岭回归 |
| `Airbnb.csv` | **68,133** × 15，目标变量 `log_price` → [[IS6400_Business_Data_Analytics/_meta/数据集卡片\|数据集卡片]]（W2–W4 三周共用） |
| `IS6400-W3-DataMining.pdf` | ✅ M03 / T03 已成 v1.0，W3 转录已合并；曾被同步截断的 PDF 于 9/22 重下复核 |
| `Week 3 Description.ipynb` | ✅ 已读 → [[T03-数据探索实战-Iris与Airbnb的描述统计]]（48 cells，Python 3.13.5；**含 Week 3 Assignment**；⚠️ **无 AI Prompt 格**） |
| `IS6400-W4-Feature.pdf` | ✅ M04 / T04 已成 v1.0（2026-10-07已融合9/23原录音）；曾被同步截断的 PDF 于 9/22 重下复核 |
| `Week 4 Feature Engineering.ipynb` | ✅ 已读 → [[T04-特征选择与PCA实战-Iris]]（37 cells，⚠️ kernel Python 3.7.6；**含 Week 4 Assignment**；无 AI Prompt 格） |
| `IS6400-L5-Clustering.pdf` | ✅ 已读 → [[M05-聚类-Kmeans层次与DBSCAN]]（67 页，2026-09-22 课前建稿；30 页图逐页视觉复核；Reading = DM Chapter 7, 8）。⚠️ Syllabus / Notion 原排 W05 = 决策树，实为聚类 |
| `iris.txt` | 150 × 5，无表头，CRLF → [[IS6400_Business_Data_Analytics/_meta/数据集卡片#iris.txt\|数据集卡片 › iris.txt]] |

| `*.html` | **忽略**（notebook 导出，与 ipynb 重复） |

**转录**：W02/W03/W04均已融合，W04为 `M04-transcript-partial.txt`（9/23Windows原录音，1058段，缺开头、结尾完整）。M04/T04课堂与现行评分部分分别维护，现场修改不冒充原保存源码执行。

> ⚠️ **W3 / W4 的 notebook 没有 `🤖 AI Prompt` 单元格**（§3 的规则对它们不适用，T03 / T04 在 §0 注明即可）。
> ⚠️ **Syllabus 与 Canvas 周次错位一周**（Syllabus W03 = PCA，实际 W3 = 描述性分析、W4 = 特征工程）：笔记编号跟 Canvas 的 Week，不跟 Syllabus。

---

## 6. 跨课交叉：与 EF5560 的回归内容重叠

**EF5560 `Lec02_Regression_Vibe_Coding.pdf` 与 IS6400 `L2-Linear_Regression.pdf` 是同一周同一主题**，且两门课都在教"用 AI 写代码"（EF5560 叫 Vibe Coding，IS6400 叫 GenAI for BDA）。

**规则**：处理这两讲时**必须互相建双链**，并在笔记里点出两位老师侧重的差异。这能省掉大量重复工作，也是用一个 vault 装五门课的直接收益。

---

## 7. Claude Code 操作提示

```bash
cd "/d/上课资料/CityU/IS6400_Business_Data_Analytics"
pdftotext -layout "L2-Linear_Regression.pdf" "$SCRATCH/L2.txt"
```

notebook 解析用 `json`（标准库即可，不需要 nbformat）：

```python
import json
nb = json.load(open(path, encoding='utf-8'))
for i, c in enumerate(nb['cells'], 1):
    print(i, c['cell_type'], ''.join(c['source'])[:200])
```

数据集用 pandas 出六项概览（规模 / 字段 / 缺失率 / 目标变量 / 已知坑 / 与讲义对应）。
⚠️ **不做分析，只做描述**——分析属于 tutorial 笔记。

**Notion**：进度库 `collection://500c1c03-e1ff-4bce-b190-efaa39e2185b`。

**回复语言**：简体中文。

## 9. 作业续写与验收（2026-09-30）

本课计分作业执行 `_meta/IS6400作业制作规范.md` 和根级 `_meta/作业规范.md`：从当前 Canvas Notebook 的副本续写，保留原题与教学顺序；先核前三周的实际经验，再逐问完成答案与必做拓展；零基础教学、自测与提交检查放私人导览，正式 Notebook 保留解题所需的方法、代码、输出和讨论，最后标准导出与实看。作业的 Python 入场基线是零基础，覆盖本文件 §3 的讲义默认假设。`*.html` 中的个人提交是需要复核的历史材料，不因 §7“重复导出”而忽略。

W04 于 2026-09-30 核到当前 `Week4_Feature_Engineering_Tutorial.ipynb`（43 cells），新题合计 100 内部分；旧 37-cell 版本的题号与分值仅作历史材料，不用于当前作业。当前 Canvas 提交类型为 HTML 或 PDF。完整个人答案只在 Git 忽略的 `assignment/`，公开笔记不反向链接私有答案。

**Notebook 提交导出（2026-09-30 用户明确）**：HTML 必须直接通过 Jupyter 菜单或标准 nbconvert 从已保存的 `.ipynb` 导出；内容、顺序、输出与字号均在 Notebook 维护，不另做 HTML 页面。导出脚本仅允许调用标准导出器和保存，不重排或单改 HTML。

## 可读性规则入口（2026-10-09）

先读根级 `_meta/可读性总规则.md`，它是教学语言、表格读法与版面的唯一现行规则；再读本课 `_meta/IS6400可读性细则.md` 的学科补充。先把概念对应的对象、动作、理由与完整例子讲清，再按阈值拆句、分段和拆表。总规则已替代旧语言规范，不并行执行旧摘要。

新写或整篇整改加 `readability_rules: v2`，用 `note_quality.py <笔记> --readability` 辅助检查。机器 ✗ 清零；语义 △ 要人工判断，不以词表或标记命中充当理解验收。不恢复重复盲读与评分；当前任务的来源、原件和文件安全要求照旧。

## 教学图示规则入口（2026-10-07）

讲义或练习涉及核心步骤、分支／循环、对象关系、多重性、跨时点／账户或数值趋势时，先读根级 `_meta/教学图示规范.md` 与 `_meta/教学图示工具流程.md`，在理解难点附近主动配图。普通流程用 Mermaid，密集 REA／UML／关系模型用 Graphviz，真实数值图用 Matplotlib，小型并列／账户信息用表格。先逐项回源建立语义清单，再生成、反解关系／运行小例、查看最终图；渲染成功不等于含义正确。复杂图保留同源结构图与全属性图、图源和来源／假设，不能删条件或缩成看不清。矢量 SVG 须有可编辑 JSON／DOT／代码来源，原件与私人边界照旧。


## 课堂／课间练习规则入口（2026-10-07）

处理所有课程的 Case、Quiz、Worksheet、照片题、代码题与口头练习前，必须读根级 `_meta/课堂练习完成与解析规范.md`，再读本课作业细则及原题。逐小问给答案与过程，难句拆清对象、动作、条件及它改变哪一步，用具体例子解释最难逻辑，并给学习总结和改条件练习。参考解析、官方核对、可提交、本人已学会／已提交分别记录；不计分也不减讲解深度。沿用 2026-10-02 一次实质修文与必要核对，不恢复重复全量盲读或补造评分。


## 作业规则入口（2026-10-06）

本课作业依次读取根级 `_meta/作业规范.md` → 本课 `_meta/IS6400作业制作规范.md` → 对应 Axx 任务说明。全局规定通用语言、学习/提交分工、AI 声明和安全验收；本课文件只补学科方法，当前题目、格式和期限在任务层回源。讲义笔记的自测与模板不直接套到正式答卷。
