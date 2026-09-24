# CLAUDE.md — AC6761 Artificial Intelligence Accounting（课程级）

> 通用方法论见 vault 根的 [CLAUDE.md](../CLAUDE.md)。工具无关版见 [AGENTS.md](AGENTS.md)。
> **开工前必做**：核对现有 `_prep/课程前置资料.md` 与 `AC6761 Outline 2627.docx`、官方课程目录；新材料到位后再更新课程笔记。

---

## 1. 已知情况

| 项 | 内容 |
|---|---|
| 课程码 | AC6761 |
| 定位 | MScAIB (P85) **商业核心**（组内选修，9 学分中的一门） |
| 上课时间 | **周三**（⚠️ 据文件时间戳推断，待确认） |
| 首课 | 2026-09-02 |

**现有材料**（`course_files_export/`）

| 文件 | 说明 |
|---|---|
| `AC6761 Outline 2627.docx` | 课程大纲；现行分析见 `_prep/课程前置资料.md`，具体要求仍回原件核对 |
| `Week 1 PPT.pptx` ~ `Week 6 PPT.pptx` | 六周讲义，教授**一次性提前放出** |
| `Accounting principles.docx` | W1 四条原则例题 → M01 §2.6.3 |
| `Transaction analyses for Lecture 1.docx` · `Case 1 with solution.docx` · `Case 2 with solution.docx` · `2 Analyze balance sheet.docx` | ✅ 2026-09-21 补发、9/22 已并入：官方解答表 → M01 §2.8.4；两份案例 → M01 / M02 §7 第 9 题（含解答，`verify_ac6761_cases.py` 复核）；AI 提示词 → M03 §2.2.10 |

**转录**：`transcripts/M01-transcript.txt` 已导出（356 段，`00:01→02:03:38`），但首句已在讲复式记账流程，**开头内容未录到**；`01:41:09→01:44:57` 为课堂练习，不当作内容丢失。详见 `00-课程总览.md` 的转录状态表。

---

## 2. 处理 pptx 讲义的两条要点

**① `python-pptx` 已就绪**

本课讲义是 `.pptx` 而非 PDF。`python-pptx` 1.0.2 已于 2026-09-08 安装，可直接处理。

**② `.pptx` 优先于导出的 PDF，且必须读 speaker notes**

见 [[材料处理规则#6. `.pptx`|材料处理规则 › 6. `.pptx`]]。`.pptx` 相对 PDF 的关键优势是**能读到演讲者备注**——教授常把不写进正文的要点放在备注里，这是 PDF 拿不到的。处理时务必检查每一页的 `notes_slide`。

**⚠️ 会计转录的 ASR 质量很差**：已有 `general letter of account` → `general ledger of accounts`、`trial about food` → `trial balance` 等真实错例。先从讲义建立术语表，再校正转录；数字、金额、科目编号回到讲义核对，拿不准的术语标 `[?]`，绝不猜。详见工具无关版 §3 与根级 `_meta/转录处理规则.md` §3。

---

## 3. 待确认的课程特性

产出 `_prep/课程前置资料.md` 时需要弄清：

- [ ] 学分、考核权重与**及格线**（IS5113 的经验：官方课程目录里有讲义没写的硬性规则，务必抓 `https://www.cityu.edu.hk/catalogue/pg/<学年>/course/AC6761.pdf` 对校）
- [ ] **GenAI 使用政策**（官方目录会写明每项评估任务是否允许）
- [ ] 是否有编程/数据作业 → 若有，先补 [[材料处理规则]] §7/§8 的空槽位
- [ ] 会计专业概念的深度 → **读者会计零基础**，需确定 L0 基线里要不要纳入基础会计概念，还是全部就地解释
- [ ] 与 IS5113 的交叉点（审计、内控、合规 ↔ IS5113 W5 问责）

---

## 4. 术语处理

会计术语的中英对应比哲学术语稳定，但**港式/内地/台湾译法有差异**（如 audit trail、materiality、internal control）。建立本课 `_meta/术语表.md` 时统一一次，并把跨课概念登记到 [[术语总表]]。

⚠️ **读者会计零基础**。诸如权责发生制、实质重于形式、重要性水平这类概念，必须就地解释，不能默认。

---

## 5. 进度

本地 `notes/` 的 M01–M03 为 v1.0（已合并转录），M04–M06 为 v0.9（仅讲义）；M02 录音缺尾，M03 录音只覆盖讲义到 p.27。Notion 进度库为 `collection://500c1c03-e1ff-4bce-b190-efaa39e2185b`；勾选状态需与笔记 frontmatter 逐项核对，不能沿用旧的 W01 快照。
