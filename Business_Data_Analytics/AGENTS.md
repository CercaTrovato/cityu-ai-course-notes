# AGENTS.md — IS6400 Business Data Analytics（课程级 · 工具无关版）

> 通用方法论见 vault 根的 `AGENTS.md`。Claude Code 版见同目录 `CLAUDE.md`，两份规则等价。
> 课程背景见 `_prep/课程前置资料.md`（已读 Syllabus，**官方课程目录待对校**）。

---

## 1. 这门课是什么

CityU **IS6400 · Business Data Analytics**，2026/27 Sem A，授课教师 Junming Liu, Ph.D.，Offline 授课，每周 lecture + hands-on tutorial 近 3 小时。

**它是本笔记库五门课里唯一的技术实操课**——Python 编程 + 统计/机器学习模型 + 业务解读。其他四门讲"该不该做、怎么治理、用在哪"，这门讲"怎么做出来"。

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
| 线性回归、PCA、KMeans、DBSCAN、决策树、集成学习、ANN/RNN | ✅ 属 L0，不必从零讲原理 |
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
| `IS6400-W3-DataMining.pdf`（72 页）· `Week 3 Description.ipynb`（48 cells） | ✅ 已读 → `notes/M03-*.md`、`notes/T03-*.md`（2026-09-16）。⚠️ PDF 本地副本于 9/16 12:42 后被截断，建议重下 |
| `IS6400-W4-Feature.pdf`（69 页）· `Week 4 Feature Engineering.ipynb`（37 cells，kernel Python 3.7.6） | ✅ 已读 → `notes/M04-*.md`、`notes/T04-*.md`（课前建稿）。⚠️ PDF 同上 |
| `iris.txt` | 150 × 5，无表头 → `_meta/数据集卡片.md` |

| `*.html` | **忽略**（notebook 导出，内容重复） |

**转录**：W02 已合并；W03 待导出；W04 未上课。

> ⚠️ W3 / W4 的 notebook **没有** `🤖 AI Prompt` 单元格；Syllabus 与 Canvas 周次错位一周，笔记编号跟 Canvas。

---

## 8. 待办

- [ ] 抓官方课程目录对校：`https://www.cityu.edu.hk/catalogue/pg/202627/course/IS6400.pdf`（找学分、**及格线**、**GenAI 政策**、CILO）
- [ ] 确认班次（周一 15:00 / 周三 12:00 / 周三 19:00）
- [ ] 读 Project Guideline，登记作业与 DDL
- [ ] **确认 L0 基线**（见 §3）
- [ ] 建 `_meta/知识层级台账.md`、`_meta/数据集.md`
