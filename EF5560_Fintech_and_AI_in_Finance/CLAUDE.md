# CLAUDE.md — EF5560 Fintech and AI in Finance（课程级）

> 课程特有口径以本文件补充；现行进度以 `00-课程总览.md`、笔记 frontmatter 与原始材料核对。通用融合与验收规则见 vault 根文件及 `.claude/skills/transcript-merge/SKILL.md`。
> **开工前必做**：读 `syllabus_EF5560_2026.pdf` + 抓官方课程目录对校 → 产出 `_prep/课程前置资料.md`。

---

## 1. 已知情况

| 项 | 内容 |
|---|---|
| 课程码 | EF5560 |
| 定位 | MScAIB (P85) **商业核心**（9 学分组内选一）；开课单位为 EF（经济与金融系） |
| 上课时间 | 周四；2026-09-24 晚场 M04 双录音和 `10/1` 停课口头通知已核实。具体时段以 Canvas 为准 |
| 首课 | 2026-09-03 |

**材料**（`course_files_export/`，✅ 已符合存放约定）

| 文件 | 状态 |
|---|---|
| `syllabus_EF5560_2026.pdf` | ✅ 已读 → `_prep/课程前置资料.md`；M04 教师说 9/24 又更新过，更新版需到 Canvas 复核 |
| `Lec01_Data_and_Vibe_Coding.pdf` | ✅ → M01 v1.0，58 页全覆盖、转录已融合 |
| `Lec02_Regression_Vibe_Coding.pdf` | ✅ → M02 v1.0 |
| `Lec03_Linear_Machine_Learning.pdf`（56 页）+ `class03/class03/`（2026-09-22 重下更新版：15 CSV + manifest + README，含五个共享面板） | ✅ → M03 v1.0（2026-09-17）；`stock_linear_test_predictions.csv` 曾被同步截断，9/22 已恢复复核；`Lec03_Linear_Machine_Learning.pdf` 曾被截为 32 KB，9/22 已重下（56 页） |
| `Lec04_Nonlinear_Machine_Learning.pdf`（54 页）+ `class04/` | ✅ M04 v1.0（2026-09-26）；同课 A/B 双录音互补，37 个 🎙️ 格已回填；实际课堂至 p.39，p.40–54 明确顺延；课件 54 页仍全覆盖 |
| `class01/class01/`（6）· `class02/class02/`（12，含 8 张官方结果表） | ✅ 2026-09-21 补发；输入表 = `data/`（sha256 一致）；M02 数字 22 项全部对上 → 数据集卡片 §12 |
| `EF5560_FinTech_Company_Case_Requirements.pdf` | ✅ 已读 → `_meta/作业与DDL.md` §2.3；个人作业成品不入公开仓库 |
| `data/*.csv` ×8 | 数据集说明以本课 `_meta/数据集卡片.md` 为准；原始文件保持只读 |
| `course_image/canvas_course_card_2026.png` | 杂项，忽略 |

**转录**：M01–M03 已融合；M04 的 `M04-transcript-A-partial.txt` 和 `M04-transcript-B-partial.txt` 是**同一晚场的重叠录音**，两者互补而非前后分段。课堂至 p.39，p.40–54 明确顺延，细节见 M04 §8–9。

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

- [x] 官方目录、syllabus 与课程前置资料已对校；学分、GenAI 政策及 CILO 差异见 `_prep/课程前置资料.md`。
- [ ] 对照 syllabus、课程前置资料与后续课堂口径，确认仍未核实的周次与主题
- [x] 案例 brief 已读并登记 `_meta/作业与DDL.md` §2.3；M04 口头复述了录像上限与每人时长，正式 DDL 仍看 Canvas。
- [ ] **L0 基线**：读者有 ML 基础，但**金融概念（收益率、波动率、因子、配对交易）零基础**，必须就地解释

---

## 6. Claude Code 操作提示

```bash
cd "/d/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance/course_files_export"
pdftotext -layout "Lec01_Data_and_Vibe_Coding.pdf" "$SCRATCH/EF_L01.txt"
```

转录质量优于 AC6761，但仍需按 [[转录处理规则]] §3 校正金融专名（ticker、指标名、机构名）；拿不准的标 `[?]`，不要猜。

**Notion**：进度库 `collection://500c1c03-e1ff-4bce-b190-efaa39e2185b`。

**回复语言**：简体中文。
