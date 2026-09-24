# AGENTS.md — EF5560 Fintech and AI in Finance（课程级 · 工具无关版）

> 🚧 **骨架，待填。** 通用方法论见 vault 根的 `AGENTS.md`。Claude Code 版见同目录 `CLAUDE.md`。
> **开工前必做**：读 `syllabus_EF5560_2026.pdf` + 抓官方课程目录对校 → 产出 `_prep/课程前置资料.md`。

---

## 1. 已知情况

| 项 | 内容 |
|---|---|
| 课程码 | EF5560 |
| 定位 | MScAIB (P85) **商业核心**；开课单位为 EF（经济与金融系） |
| 上课时间 | **周四**（⚠️ 据文件时间戳推断，待确认） |
| 首课 | 2026-09-03 |

**材料**（`course_files_export/`，✅ 已符合存放约定）

| 文件 | 状态 |
|---|---|
| `syllabus_EF5560_2026.pdf` | 课程口径见 `_prep/课程前置资料.md`；原件细节仍以原件核对 |
| `Lec01_Data_and_Vibe_Coding.pdf` · `Lec02_Regression_Vibe_Coding.pdf` | ✅ 对应 M01 / M02 v1.0，转录已合并 |
| `Lec03_Linear_Machine_Learning.pdf`（56 页）+ `class03/` | ✅ M03 v1.0；9/22 重下受同步截断影响的课件与数据 |
| `Lec04_Nonlinear_Machine_Learning.pdf`（54 页）+ `class04/` | ✅ M04 v0.9 课前预习版；转录待处理 |
| `class01/` · `class02/` | ✅ 已补发并与 M02 数字核对；细节见课程总览与数据集卡片 |
| `EF5560_FinTech_Company_Case_Requirements.pdf` | ⚠️ 未读 → 读完登记作业与 DDL |
| `data/*.csv` ×8 | 数据集说明以本课 `_meta/数据集卡片.md` 为准；原始文件保持只读 |

**转录**：`transcripts/M01-transcript.txt`（118KB，2013 行，`MM:SS` 时间戳）✅ 已导出，**是五门课里最完整的一份**

---

## 2. 这门课的性质

金融 + 代码，且**明确教"用 AI 写代码"**——两讲文件名都带 "Vibe Coding"。

转录里教授自陈本课的来历与做法：AIB 项目去年成立后请 EF 系为其新开一门 AI in Finance 课；今年的讲义与去年**完全不同**，且是**借助 AI 重做**的（`M01-transcript.txt` 00:03 与 00:28）。

**含义**：这是一门很新的课，网络上不会有学长口碑；同时教师本人对 AI 辅助工作持开放态度。

---

## 3. 八个数据集已就位，规则已备好

`course_files_export/data/`：苹果周度价格收益、拼多多/京东配对交易、沪深300 与宏观面板、市场指数价格与收益、SPY 月度特征。

处理规则见根级 `_meta/材料处理规则.md` §7。产出**统一写进 `_meta/数据集.md`**（一课一文件，一数据集一节，六项固定内容：规模 / 字段清单 / 缺失率 / 目标变量 / 已知坑 / 与讲义的对应）。

⚠️ **只做描述性概览，不做分析**；分析属于讲义或作业笔记。**不修改原始数据文件，也不生成清洗后的副本落进库里。**

---

## 4. 跨课交叉：与 IS6400 的回归内容重叠 ★

**本课 `Lec02_Regression_Vibe_Coding.pdf` 与 IS6400 `L2-Linear_Regression.pdf` 是同一周同一主题**，两门课都在教用 AI 辅助写代码。

处理这两讲时**必须互相建双链**，并点出两位老师侧重的差异（金融场景 vs 通用商业分析）。

其他交叉：本课的金融风控内容 ↔ IS5113 W8「AI in Finance & Risk Management」的伦理视角。

---

## 5. L0 基线的特殊之处

读者**有 ML 基础**，但**金融概念零基础**。以下必须就地解释，不能默认：

收益率与对数收益、波动率、因子模型、配对交易、宏观面板数据、指数与基准、回撤、夏普比率等。

---

## 6. 待确认

- [ ] 抓官方目录对校：`https://www.cityu.edu.hk/catalogue/pg/<学年>/course/EF5560.pdf` — 学分、**及格线**、**GenAI 政策**、CILO
- [ ] 对照 syllabus、课程前置资料与后续课堂口径，确认仍未核实的周次与主题
- [ ] 读 `EF5560_FinTech_Company_Case_Requirements.pdf` → 登记作业与 DDL（Notion 该行目前标着 ❗待补）

---

## 7. 转录处理注意

质量优于 AC6761，但仍需按根级 `_meta/转录处理规则.md` §3 校正金融专名（ticker 代码、指标名、机构名、人名）。拿不准的标 `[?]`，不要猜。
