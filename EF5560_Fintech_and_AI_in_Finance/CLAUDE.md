# CLAUDE.md — EF5560 Fintech and AI in Finance（课程级）

> 🚧 **骨架，待填。** 通用方法论见 vault 根的 [CLAUDE.md](../CLAUDE.md)。工具无关版见 [AGENTS.md](AGENTS.md)。
> **开工前必做**：读 `syllabus_EF5560_2026.pdf` + 抓官方课程目录对校 → 产出 `_prep/课程前置资料.md`。

---

## 1. 已知情况

| 项 | 内容 |
|---|---|
| 课程码 | EF5560 |
| 定位 | MScAIB (P85) **商业核心**（9 学分组内选一）；开课单位为 EF（经济与金融系） |
| 上课时间 | **周四**（⚠️ 据文件时间戳推断，待确认） |
| 首课 | 2026-09-03 |

**材料**（`course_files_export/`，✅ 已符合存放约定）

| 文件 | 状态 |
|---|---|
| `syllabus_EF5560_2026.pdf` | ⚠️ 未读 |
| `Lec01_Data_and_Vibe_Coding.pdf` | ⚠️ 未读 |
| `Lec02_Regression_Vibe_Coding.pdf` | ✅ → M02 v1.0 |
| `Lec03_Linear_Machine_Learning.pdf`（56 页）+ `class03/class03/`（2026-09-22 重下更新版：15 CSV + manifest + README，含五个共享面板） | ✅ → M03 v1.0（2026-09-17）；`stock_linear_test_predictions.csv` 曾被同步截断，9/22 已恢复复核；`Lec03_Linear_Machine_Learning.pdf` 曾被截为 32 KB，9/22 已重下（56 页） |
| `Lec04_Nonlinear_Machine_Learning.pdf`（54 页）+ `class04/class04/`（5 共享面板 + 11 结果表 + manifest + README） | ✅ → M04 v0.9 课前预习版（2026-09-21）；三棵树用共享面板重训一致；转录待 9/24 |
| `class01/class01/`（6）· `class02/class02/`（12，含 8 张官方结果表） | ✅ 2026-09-21 补发；输入表 = `data/`（sha256 一致）；M02 数字 22 项全部对上 → 数据集卡片 §12 |
| `EF5560_FinTech_Company_Case_Requirements.pdf` | ⚠️ 未读 → 读完登记作业与 DDL |
| `data/*.csv` ×8 | 未处理 → 建 `_meta/数据集.md` |
| `course_image/canvas_course_card_2026.png` | 杂项，忽略 |

**转录**：`transcripts/M01-transcript.txt`（118KB，2013 行，带 `MM:SS` 时间戳）✅ 已导出，**是目前最完整的一份**

---

## 2. 这门课的性质：金融 + 代码，且明确教"用 AI 写代码"

两讲的文件名都带 **"Vibe Coding"**，转录里教授自陈：

> "all the slides for this year… are totally different from last year because I have a chance to redo almost… And you can guess how I do, how to prepare my slide. **With the help from AI.**"（`M01-transcript.txt` 00:28）

且转录 00:03 说明了课程来历：**AIB 项目去年成立后，请 EF 系为其开设一门 AI in Finance 课，教授从去年开始新建这门课**。所以这是一门**很新的课**，网络上不会有口碑。

**这与 IS6400 的 "GenAI for BDA" 是同一类取向**——见 §4。

---

## 3. 八个数据集已就位，规则已备好

`course_files_export/data/` 下：

| 文件 | 提示 |
|---|---|
| `aapl_weekly_prices_returns_156w.csv` | 苹果 156 周价格与收益 |
| `pdd_jd_daily_close_2023-06-26_2026-06-26.csv` · `pdd_jd_pair_example_156w.csv` | 拼多多 / 京东配对交易 |
| `csi300_macro_panel.csv` · `macro_240m.csv` | 沪深 300 与宏观面板，240 个月 |
| `market_index_prices_240m.csv` · `market_index_returns_240m.csv` | 市场指数价格与收益 |
| `spy_monthly_features_240m.csv` | SPY 月度特征 |

处理规则见 [[材料处理规则#7. `.csv` / `.xlsx` 数据文件 ✅|材料处理规则 › 7. `.csv` / `.xlsx` 数据文件 ✅]]，产出**统一写进 `_meta/数据集.md`**（一课一文件，一数据集一节，六项固定内容），**不要每个数据集单独建笔记**。

⚠️ **只做描述性概览，不做分析**。分析属于讲义/作业笔记。

---

## 4. 跨课交叉：与 IS6400 的回归内容重叠 ★

**`Lec02_Regression_Vibe_Coding.pdf`（本课）与 `L2-Linear_Regression.pdf`（IS6400）是同一周、同一主题**，且两门课都在教用 AI 辅助写代码。

**规则**：处理这两讲时**必须互相建双链**，并在笔记中点出两位老师侧重的差异（金融场景 vs 通用商业分析）。这能省掉大量重复工作。

其他交叉：本课的金融风控内容 ↔ IS5113 W8「AI in Finance & Risk Management」的伦理视角。

---

## 5. 待确认

- [ ] 抓官方目录对校：`https://www.cityu.edu.hk/catalogue/pg/<学年>/course/EF5560.pdf` — 学分、**及格线**、**GenAI 政策**、CILO
- [ ] 读 syllabus，确认周数与主题地图
- [ ] 读 `EF5560_FinTech_Company_Case_Requirements.pdf` → 登记 `_meta/作业与DDL.md` + Notion（该行目前标着 ❗待补）
- [ ] **L0 基线**：读者有 ML 基础，但**金融概念（收益率、波动率、因子、配对交易）零基础**，必须就地解释

---

## 6. Claude Code 操作提示

```bash
cd "/d/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance/course_files_export"
pdftotext -layout "Lec01_Data_and_Vibe_Coding.pdf" "$SCRATCH/EF_L01.txt"
```

转录质量优于 AC6761，但仍需按 [[转录处理规则]] §3 校正金融专名（ticker、指标名、机构名）。

**Notion**：进度库 `collection://500c1c03-e1ff-4bce-b190-efaa39e2185b`。

**回复语言**：简体中文。
