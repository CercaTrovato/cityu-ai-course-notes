# AGENTS.md — IS6400 Business Data Analytics（课程级 · 工具无关版）

> 通用方法论见 vault 根的 `AGENTS.md`。Claude Code 版见同目录 `CLAUDE.md`，两份规则等价。
> 课程背景见 `_prep/课程前置资料.md`（已读 Syllabus，**官方课程目录待对校**）。

---

## 1. 这门课是什么

CityU **IS6400 · Business Data Analytics**，2026/27 Sem A，授课教师 Junming Liu, Ph.D.，Offline 授课，每周 lecture + hands-on tutorial 近 3 小时。

**它是本笔记库五门课里集中训练数据分析技术实操的课程**——Python 编程 + 统计/机器学习模型 + 业务解读。其他四门讲"该不该做、怎么治理、用在哪"，这门讲"怎么做出来"。

---

## 2. 笔记形态与其他课不同

| | 其他四门 | IS6400 |
|---|---|---|
| 产出 | `notes/M<NN>-*.md`（讲义笔记） | `notes/M<NN>-*.md` **+** `notes/T<NN>-*.md`（**代码讲解笔记**） |
| 核心难点 | 陌生概念的解释密度 | **代码与理论的对应关系** |

一周通常产出两个文件（讲义 `M02` + tutorial `T02`），两者互链。

代码讲解笔记的结构见根级 `_meta/材料处理规则.md` §8.2。数据集卡的六项要求见 §7.1。

---

## 3. ⚠️ L0 基线待确认（写代码笔记前必须解决）

本库默认读者「只有 AI/ML 基础，其余零基础」。**这条在技术课需重新校准**：

| 内容 | 是否属 L0 |
|---|---|
| 线性回归、PCA、KMeans、DBSCAN、决策树、集成学习、ANN/RNN | **本讲核心使用时必须从零讲机制**，不能用 L0 免讲；见根 `_meta/机制理解与可读性标准.md` |
| Python 语法 | ❓ 未确认 |
| pandas / numpy / sklearn / statsmodels 的 API | ❓ 未确认 |
| 业务解读（系数的业务含义） | ❌ 不属 L0，必须讲 |

**确认前的默认口径**：按「Python 语法熟悉、特定库 API 不熟」写——不解释 `for` 循环，但解释 `fit/predict` 约定、参数含义、以及为什么选这个函数而不是别的。

---

## 4. 特殊规则：GenAI Prompt 单元格

Tutorial notebook 含形如 `🤖 AI Prompt (Copy this to AI): ...` 的 markdown 单元格。

**这是课程设计的一部分，不是噪音。** Syllabus 的 ILO 第 3 条明写 "Manage GenAI tools for BDA proposal and Python programming"，W11 还有 "Competition: GenAI for BDA"。

**规则**：保留进笔记，并单列一节讨论「教师期望你怎么向 AI 提问」——这是会被考核的能力。

---

## 5. 考核（决定笔记侧重）

| 项目 | 权重 |
|---|---|
| **Exam** | **40%** |
| Individual Assignments（约 8 次） | **25%** |
| Group Project（briefing 5 + 演示 15 + 报告 10） | **30%** |
| Class Participation | 5% |

**要点**
- ❗ **迟交惩罚最重**：个人作业每天 **-20%**（5 天归零），小组报告每天 -10%
- ❗ Participation 靠**随机堂上小测 + 签到**，按答对次数占比计分，缺课直接丢分
- ❗ **W6 就要 Project Briefing**（约 10 月上中旬）
- Exam 占 40%，说明**需要能笔答的概念与推导，不只是会跑代码**——代码笔记不能只讲"怎么调 API"

---

## 6. 跨课交叉：与 EF5560 回归内容重叠

**EF5560 的 `Lec02_Regression_Vibe_Coding.pdf` 与本课 `L2-Linear_Regression.pdf` 是同一周同一主题**，且两门课都在教用 AI 写代码。

处理这两讲时**必须互相建双链**，并点出两位老师侧重的差异。

---

## 7. 现有材料

✅ 材料已迁入 `course_files_export/`（2026-09-08），符合根级 `_meta/材料处理规则.md` §0 的存放约定。

| 文件 | 状态 |
|---|---|
| `IS6400_Syl_SemA_2026-27.pdf` | ✅ 已读 |
| `IS6400-Week1.pdf` · `L2-Linear_Regression.pdf` | ⚠️ 未读 |
| `IS6400 Project Guideline.pdf` | ⚠️ 未读 → 读完登记作业与 DDL |
| `Tutorial 1 - …_Prompt.ipynb`（25 cells）· `Week 2 Regression…ipynb`（39 cells） | Python 3.13.5，kernel `conda-base-py` |
| `Airbnb.csv` | **68,133** 行 × 15 列，目标变量 `log_price` → `_meta/数据集卡片.md`（W2–W4 共用） |
| `IS6400-W3-DataMining.pdf`（72 页）· `Week 3 Description.ipynb`（48 cells） | ✅ M03 / T03 已成 v1.0；W3 转录已合并。曾被同步截断的 PDF 于 9/22 重下复核 |
| `IS6400-W4-Feature.pdf`（69 页）· `Week 4 Feature Engineering.ipynb`（37 cells，kernel Python 3.7.6） | ✅ M04 / T04 已成 v1.0（2026-10-07已融合9/23原录音）；曾被同步截断的 PDF 于 9/22 重下复核 |
| `IS6400-L5-Clustering.pdf`（67 页） | ✅ M05 v0.9 课前预习版，30 页图已视觉复核；转录待后续课堂 |
| `iris.txt` | 150 × 5，无表头 → `_meta/数据集卡片.md` |

| `*.html` | **忽略**（notebook 导出，内容重复） |

**转录**：W02/W03/W04均已融合，W04为 `M04-transcript-partial.txt`（9/23Windows原录音，1058段，缺开头、结尾完整）。M04/T04课堂与现行评分部分分别维护，现场修改不冒充原保存源码执行。

> ⚠️ W3 / W4 的 notebook **没有** `🤖 AI Prompt` 单元格；Syllabus 与 Canvas 周次错位一周，笔记编号跟 Canvas。

---

## 8. 待办

- [ ] 抓官方课程目录对校：`https://www.cityu.edu.hk/catalogue/pg/202627/course/IS6400.pdf`（找学分、**及格线**、**GenAI 政策**、CILO）
- [ ] 确认班次（周一 15:00 / 周三 12:00 / 周三 19:00）
- [ ] 读 Project Guideline，登记作业与 DDL
- [ ] **确认 L0 基线**（见 §3）
- [x] 已建 `_meta/知识层级台账.md`、`_meta/数据集卡片.md`；后续逐讲增量维护

## 9. 作业续写与验收（2026-09-30）

本课计分作业执行 `_meta/IS6400作业制作规范.md` 和根级 `_meta/作业规范.md`：从当前 Canvas Notebook 的副本续写，保留原题与教学顺序；先核前三周的实际经验，再逐问完成答案与必做拓展；零基础教学、自测与提交检查放私人导览，正式 Notebook 保留解题所需的方法、代码、输出和讨论，最后标准导出与实看。作业的 Python 入场基线是零基础，覆盖本文件 §3 的讲义默认假设。`*.html` 中的个人提交是需要复核的历史材料，不因 §7“重复导出”而忽略。

W04 于 2026-09-30 核到当前 `Week4_Feature_Engineering_Tutorial.ipynb`（43 cells），新题合计 100 内部分；旧 37-cell 版本的题号与分值仅作历史材料，不用于当前作业。当前 Canvas 提交类型为 HTML 或 PDF。完整个人答案只在 Git 忽略的 `assignment/`，公开笔记不反向链接私有答案。

**Notebook 提交导出（2026-09-30 用户明确）**：HTML 必须直接通过 Jupyter 菜单或标准 nbconvert 从已保存的 `.ipynb` 导出；内容、顺序、输出与字号均在 Notebook 维护，不另做 HTML 页面。导出脚本仅允许调用标准导出器和保存，不重排或单改 HTML。

## 作业规则入口（2026-10-06）

本课作业依次读取根级 `_meta/作业规范.md` → 本课 `_meta/IS6400作业制作规范.md` → 对应 Axx 任务说明。全局规定通用语言、学习/提交分工、AI 声明和安全验收；本课文件只补学科方法，当前题目、格式和期限在任务层回源。讲义笔记的自测与模板不直接套到正式答卷。
