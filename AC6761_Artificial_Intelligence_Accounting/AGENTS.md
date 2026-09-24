# AGENTS.md — AC6761 Artificial Intelligence Accounting（课程级 · 工具无关版）

> 通用方法论见 vault 根的 `AGENTS.md`。Claude Code 版见同目录 `CLAUDE.md`。
> **开工前必做**：核对现有 `_prep/课程前置资料.md` 与 `AC6761 Outline 2627.docx`、官方课程目录；新材料到位后再更新课程笔记。

---

## 1. 已知情况

| 项 | 内容 |
|---|---|
| 课程码 | AC6761 |
| 定位 | MScAIB (P85) **商业核心**（9 学分组内选一） |
| 上课时间 | **周三**（⚠️ 据文件时间戳推断，待确认） |
| 首课 | 2026-09-02 |

**材料**（`course_files_export/`，✅ 已符合存放约定）

| 文件 | 说明 |
|---|---|
| `AC6761 Outline 2627.docx` | 课程大纲；现行分析见 `_prep/课程前置资料.md`，具体要求仍回原件核对 |
| `Accounting principles.docx` | W1 四条原则例题 → M01 §2.6.3 |
| `Transaction analyses for Lecture 1.docx` · `Case 1 with solution.docx` · `Case 2 with solution.docx` · `2 Analyze balance sheet.docx` | ✅ 2026-09-21 补发、9/22 已并入 M01 §2.8.4 / M01 §7 / M02 §7 / M03 §2.2.10 |
| `Week 1 PPT.pptx` ~ `Week 6 PPT.pptx` | 六周讲义，教授**一次性提前放出** |

**转录**：`transcripts/M01-transcript.txt` 已导出，但首句已在讲复式记账流程，**开头内容未录到**；`01:41:09→01:44:57` 为课堂练习，不当作内容丢失。详见 `00-课程总览.md` 的转录状态表。

---

## 2. 处理 pptx 讲义的两条要点

**① 讲义是 `.pptx`（依赖已就绪）**

`python-pptx` 1.0.2 已于 2026-09-08 安装，可直接处理。

**② 必须读 speaker notes**

见根级 `_meta/材料处理规则.md` §6。`.pptx` 相对 PDF 的关键优势是**能读到演讲者备注**——教授常把不写进正文的要点放在那里。处理每一页时务必检查 `notes_slide`。

---

## 3. ⚠️ 这份转录的 ASR 质量很差，会计术语被严重打乱

已在 `M01-transcript.txt` 开头几段发现的错误（**这些是真实样本，不是假设**）：

| 转录原文 | 应为 |
|---|---|
| `general so-called general letter of account` | general ledger of accounts |
| `we have a new trial about food` | we have a new trial balance |
| `the account of computer and the tier console cache` | （整句乱码，需对照讲义还原） |
| `See all the financial statements` | These are the financial statements |

**规则（见根级 `_meta/转录处理规则.md` §3）**：
1. **先用讲义（PPT）建会计术语表，再拿它逐一校正转录**
2. **拿不准的术语标 `[?]`，绝不猜一个填上**——一个被猜错的会计术语比一个空缺危害大得多
3. 数字、金额、科目编号**一律以讲义为准**

> 这门课的转录校正工作量会明显高于其他课。**不要跳过这一步直接用转录内容写笔记。**

---

## 4. 待确认的课程特性

产出 `_prep/课程前置资料.md` 时必须弄清：

- [ ] 学分、考核权重与**及格线**（抓 `https://www.cityu.edu.hk/catalogue/pg/<学年>/course/AC6761.pdf` 对校；IS5113 的经验是官方目录写了讲义没写的硬性规则）
- [ ] **GenAI 使用政策**（官方目录会逐项写明）
- [ ] 是否有编程/数据作业 → 若有，数据与代码的处理规则已就绪（`材料处理规则` §7/§8）
- [ ] **会计概念的深度**——读者**会计零基础**。权责发生制、试算平衡、总账、重要性水平这类概念必须就地解释，不能默认
- [ ] 与 IS5113 的交叉点（审计、内控、合规 ↔ IS5113 W5 问责）

---

## 5. 术语处理

会计术语的中英对应比哲学术语稳定，但**港式 / 内地 / 台湾译法有差异**（audit trail、materiality、internal control、accrual 等）。建本课 `_meta/术语表.md` 时统一一次，跨课概念登记到根级 `_meta/术语总表.md`。

---

## 6. 进度

本地 `notes/` 的 M01–M03 为 v1.0（已合并转录），M04–M06 为 v0.9（仅讲义）；M02 录音缺尾，M03 录音只覆盖讲义到 p.27。Notion 勾选状态需与笔记 frontmatter 逐项核对，不能沿用旧的 W01 快照。
