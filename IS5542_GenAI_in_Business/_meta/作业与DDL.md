---
type: 台账
course: IS5542
updated: 2026-09-15
---

# IS5542 作业与 DDL

> 与 Notion [📌 CityU 作业与 DDL](https://app.notion.com/p/c4bab444ac4f457fb3516cf13d19517d) 同步。
> Notion 负责提醒与状态流转，本文件保留完整要求原文与分析。

---

## ⏰ 现在该做的

**本课最近的硬截止日是 11/28 的小组项目**（Canvas 公告 9/11 定稿：**录像 + slides，不做现场演示**）；第一次反思要等 10/10 的客座讲座。现在就该动的三件事：

| 事 | 为什么现在 |
|---|---|
| **组队 5–7 人 —— ⚠️ Canvas 组队截止 9/30，无有效小组将随机分配** | 项目占 **30%**，且 🎙️ 教授明说**必须交出真正跑得起来的 agent**，不是概念提案。人越早定，越有时间做 demo；**同伴互评决定个人分**（模板 p.2 + 公告）。9/30 这条来自 Notion DDL 库登记的 Group Formation 邮件（9/5），本文件未见邮件原文，请核实 |
| **把 M02 §2.10 的评测协议当"模型选择理由"的模板** | 项目模板要求"模型选择及理由"和"与基线对比"（7 + 4 分钟）。M02 教的正是：固定任务集 → 受控比较 → 案例级记录 → 留出集 → 每接受任务成本。见 [[M02-模型全景-基准评测与提示设计]] §2.10 |
| **10/10 起六场客座：强制出席 + 每场一份反思（3%）+ 内容进期末** | Canvas 公告 9/11 原话："All students are required to attend all guest lectures" / "the content covered in the guest lectures will be included in the final examination" |

---

## 📋 全学期任务

| 任务 | 类型 | 权重 | 截止 | 状态 |
|---|---|---|---|---|
| **课后反思 ×6** | 个人 | **18%**（6 × 3%，✅ Canvas 公告 9/11 确认） | 随 6 场客座（10/10、10/17、10/24、10/31、11/7、11/14），每场一份；⚠️ 提交渠道、字数、截止仍未公布 | 未开始 |
| 客座讲座出席与参与 | 个人 | **2%**（积极提问、参与讨论可加分） | 六场**强制出席**（CMC M3017，9:00–12:00） | 进行中 |
| **Canvas 组队（5–7 人）** | 小组 | 门槛 | ⚠️ **2026-09-30**（Notion DDL 库登记的 Group Formation 邮件 9/5：无有效小组将随机分配；请核实邮件原文） | 未开始 |
| **小组项目** | 小组 | **30%** | ✅ **2026-11-28（最后教学日）**，录像 + slides，无现场演示；⚠️ 当天具体时间与提交渠道未公布 | 未开始 |
| **期末笔试** | 考试 | **50%** | 考试周，待 ARRO 公布 | — |

> ❗ **官方及格线（讲义与 Syllabus 都没写，只在官方课程目录里）**
> - 持续评估（20%+30%=50%）至少拿到**其 30%**
> - 笔试（50%）至少拿到**其 20%**
> - **"Students must pass BOTH coursework and examination in order to get an overall pass in this course."** —— 一边高分补不了另一边

---

## 1. 课后反思 ×6（18%）

**这是 Participation 里的绝对大头**，但很容易被忽略——因为教授说"我的课不计出勤"，容易连带以为整个 Participation 都无所谓。

| 项 | 内容 |
|---|---|
| 次数 | **6 次**，每次 **3%**——✅ Canvas 公告 9/11（TA Zhanye LI）原话 "A **mandatory reflection** (3% × 6 = 18% total) is required for each guest lecture." |
| 对应 | **6 场客座讲座**：10/10 Design Thinking · 10/17 Venture Capitalist · 10/24 Marketing · 10/31 Financial Services · 11/7 Digital Native · 11/14 Legal Industry（CMC M3017，9:00–12:00；预计有 Zoom 链接并可能录像） |
| 出席 | **强制**："All students are required to attend all guest lectures."——与教授本人课"不计出勤"正相反 |
| 期末 | **客座内容进期末**："the content covered in the guest lectures will be included in the final examination." |
| ⚠️ 待确认 | 提交渠道、字数要求、截止时间（讲义、Syllabus、公告均未写） |

**🎙️ 出勤政策（讲义 p.10 完全没有）**

> "…and that means **the attendance and the participation in my lectures will not be graded.** I totally understand that many of you are busy with internships, job applications, interviews or assignments from other courses, so I have designed this attendance policy **selectively**."（转录 `12:34`）

**→ 那 2% 的参与分只在客座讲座上拿。** 教授本人的 L1–L3 与 11/21 那一讲不计出勤。

但他花了近 4 分钟劝人还是要来（转录 `13:38`–`17:16`）：

1. 课堂框架与产业实际之间**有落差**，客座讲者补的正是这层
2. 系里请的是**资深**从业者，"before applying for job, many students usually try to arrange a coffee chat with industry practitioners, but usually **our guests are very senior — it's hard for you to directly find them**"
3. 每场都留了 **Q&A**

---

## 2. 小组项目（30%）· "Defensible GenAI Application"

**讲义 p.11 的标题很关键**：**defensible（站得住脚的）**，不是 impressive。页脚标语：**PROBLEM • WORKFLOW • DEMO**。

### 要求

| 要求 | 来源 |
|---|---|
| **5–7 人**一组，**同伴互评**确保贡献公平 | Syllabus + 讲义 p.11 |
| 定义**具体**业务问题 + **谁受影响** | 讲义 p.11 |
| 设计 GenAI 工作流、**数据来源**、rollout 计划 | 讲义 p.11 |
| 评估**业务价值 / 模型质量 / 成本 / 风险**四项 | 讲义 p.11 |
| 演示须含：业务背景与目标用户 ／ 架构、评估指标、预期结果 ／ **Demo, or storyboard** | 讲义 p.11 |
| 🔴 **必须有真正跑得起来的 agent**，不能只是概念提案 | 🎙️ 转录 `19:03` |
| ✅ **截止 2026-11-28（最后教学日）** | Canvas 公告 9/11 |
| ✅ **交付物：录制的视频演示 + slides；"There will be no on-site presentations."** | Canvas 公告 9/11 |
| ✅ 不要求每个成员都出镜，但**所有成员贡献必须均等**；学期后段用 Google Form 做同伴互评 | Canvas 公告 9/11 |

### 演示模板（`IS5542 Project Template.pptx`，9 页，9/12 发布）

模板自称"只提供结构指引"，但**时间分配就是评分口径**（合计 15 分钟，与 Syllabus 一致）：

| 段 | 时长 | 必须包含 |
|---|---|---|
| **Business Problem** | 2 min | 问题描述；**量化**负面影响（数据或合理估计）；现有方案及局限；目标用户 / 利益相关者 |
| **Proposed GenAI Solution** | 7 min | 高层方案（少术语、配流程图）→ 技术细节：所用生成技术（LLM / 扩散 / GAN / VAE…）、**模型选择及理由**（按问题需求、数据可得性、模型能力）、数据与预处理 → **Demo / Storyboard walkthrough** |
| **Results, Evaluation, and Business Impact** | 4 min | KPI 与量化结果；定性洞察；**与基线 / 现状对比**；业务价值与 ROI |
| **Future Work** | 2 min | 后续步骤；规模化与部署（可选）；改进建议（可选）；更广应用与研究方向 |

模板 p.2：团队内部要有分工与评价标准；不是每个人都要上台，**同伴互评决定个人最终分**。p.9 八条演示建议：多图少字、反复排练、按听众调技术深度、始终回到业务问题与价值、热情、专业、控时、准备问答。

> 🎙️ **教授把讲义留的退路口头收紧了**：讲义 p.11 与模板都写 "Demo, **or storyboard**"，转录里他说
> "this is **not only a conceptual proposal**… **your project should include an actual AI agent and a working demo of that agent.**"
> **按最严的口径准备。**

### 🎙️ 明确鼓励用 AI 写代码（转录 `19:03`）

> "with today's [AI] coding tools, you don't need to write every line of code manually in the traditional way, and **that is old fashioned**."

**但仍需你自己做的**（转录 `19:43`）：定义业务问题 · 设计工作流 · 指明数据来源 · 决定 agent 用什么工具 · 说明它如何在真实商业中落地。

> 🎙️ 一句很实在的提醒（`21:54`）：**"the practical skill cannot be developed simply by listening"** —— L2、L3 只给基础，动手要靠课后自己试。
>
> ✅ 官方 GenAI 政策：AT1 与 AT2 **都允许**使用生成式 AI。

### 💡 项目怎么用上 M01 的框架

| 讲义要求的一项 | 对应 M01 的哪一节 |
|---|---|
| 定义业务问题 + 谁受影响 | §2.10 NIST 的 **MAP** 功能（目的、利益相关者、危害、风险容忍度） |
| 设计架构 | §2.8 **六向量** —— 尤其要写出"主约束是什么、你牺牲了什么" |
| 评估指标 | §2.7.3 **Capability 支柱** + §2.9.1 **分布式评估** |
| 风险评估 | §4.3 的**失败模式 → 控制**对照表 |
| **为什么这个问题该用 GenAI 而不是一条 if-then 规则** | §2.4 **四范式并存**；平安的百万条规则就是反例素材 |

**💡 项目怎么用上 M02 的框架**（[[M02-模型全景-基准评测与提示设计]]）

| 模板要求的一项 | 对应 M02 的哪一节 |
|---|---|
| **模型选择及理由**（7 分钟段的核心） | §2.4 开放 vs 闭源七项 + §2.5 模型卡 / 一览表（带日期、带精确变体引用）+ §2.7 挑与任务相关的基准类别 |
| **与基线 / 现状对比** | §2.10.1 四步协议：同一任务集、受控比较、案例级失败与切片、留出集；报**每接受任务成本** |
| **Demo 的可靠性** | §2.8.7 **pass^k**：同一任务重跑多次的全通过率，别只报"跑通了一次" |
| **提示怎么写、怎么改** | §2.11 四要素 → 少样本边界例子 → 分解四步 → 对话状态 → 版本化迭代与错误三分类 |
| **KPI 与 ROI** | §2.6.4 请求成本公式 + §2.10.1 每接受任务成本；M01 §2.8.6 TCO |

> ⚠️ **一个容易翻车的点**：📝 讲义 p.88 备注明说 —— **"A single successful demonstration tells us almost nothing about reliability."**
> 演示时**主动说明你跑了多少次、失败率多少、失败时怎么兜底**，反而是加分项。

### 🎙️ L2 课上与项目相关的三句话（转录 2026-09-12）

| 内容 | 出处 |
|---|---|
| **可以直接从 L2 p.88 的五个资源仓库起步做项目**："not only include the slides, but also the supporting codes and even the API… you can even start your group project with this materials" | 🎙️ `02:07:20` |
| **9/19 讲 agent + RAG**（"I will elaborate this part in the next section" / "RAG project which I will elaborate in the next lecture"）——项目里的 agent 与 RAG 部分等下一讲再动手不迟 | 🎙️ `01:39:23`、`02:07:20` |
| **教授自己用 Claude Code**，按"出结果后要 debug 几轮"比较，认为优于 Codex；"if your target is to become an algorithm engineer, I highly recommend you to subscribe the Claude Code"；做 PM 面试则 Microsoft GenAI for Beginners 够用 | 🎙️ `26:45`–`27:45`、`33:22`、`02:07:20` |

> 💡 M02 §2.10.1 的面试题版评测协议（含第五步"谁拥有发布标准"）和 §2.10.2 的"点击涨转化跌"诊断，就是项目"Results, Evaluation and Business Impact"那 4 分钟该有的样子。

---

## 3. 期末笔试（50%）

| | |
|---|---|
| 形式 | 书面考试 |
| 时长 | **2 小时** |
| 语言 | 英文 |
| GenAI | **不允许** |

**题型（讲义 p.12，Syllabus 完全没有）**

| 题型 | 占考卷 | 考什么 |
|---|---|---|
| Multiple choice | 20% | — |
| Short answer | 30% | — |
| **Essay** | **50%** | ① 讲座覆盖的概念 ② **如何应用这些概念的案例分析题** |

> ⚠️ 讲义自标 "Exact question format will be confirmed by the instructor" —— 20/30/50 是**暂定值**，留意 Canvas。
> ❗ 但"**论述占一半 + 明写案例应用**"这个信号足够稳。**练"拿框架套场景"，不是背名词。**

答题框架见 [[M01-导论-生成式AI基础与企业落地]] §6.4、[[M02-模型全景-基准评测与提示设计]] §6.3。

---

## ⚠️ 待确认

| # | 事项 | 为什么重要 |
|---|---|---|
| ① | ~~**项目演示的形式与时间**~~ | ✅ **已确认（Canvas 公告 9/11）**：11/28 截止，录像 + slides，无现场演示——与 M01 时的推断一致。**新的待确认**：当天具体时间、提交渠道、视频时长上限（模板按 15 分钟设计） |
| ② | **6 次反思的提交渠道、字数、截止** | 占 18%；公告只确认了"每场一份、3%"，格式与截止仍未写 |
| ③ | ~~**客座讲座是否会合并**~~ | ✅ 公告列出六场、六个日期、六个主题，**没有合并迹象**；但讲义 p.6 仍标 "Tentative"，留意 Canvas |
| ④ | **官方目录与讲义的权重不一致** | 官方记 AT1 = 10% / AT2 = 40%，讲义记 20% / 30%。CA 合计都是 50%，**不影响及格判定**，但可能影响最终分数 |
| ⑤ | **9/19 讲什么** | ✅ 部分确认：🎙️ L2 转录说 9/19 讲 **agent + RAG**（`01:39:23`、`02:07:20`）；**微调与 function calling 仍无着落**——项目若用到工具调用，可能要靠 p.88 的 Anthropic / Hugging Face 课程自学 |

---

## 变更记录

| 日期 | 变更 |
|---|---|
| 2026-09-09 | 建表。登记反思 ×6、小组项目、期末笔试三项；补入官方及格线与 GenAI 政策；登记 4 条待确认（含最关键的"项目演示 2 周去哪了"） |
| 2026-09-12 | 并入 Canvas 两条公告（9/11，TA）：项目 11/28 截止、录像 + slides、无现场演示、同伴互评；六场客座主题与日期定稿、强制出席、每场反思 3%、内容进期末；转写 `IS5542 Project Template.pptx` 的 15 分钟结构；待确认 ① ③ 改为已确认，新增 ⑤；「现在该做的」改为项目 + M02 评测协议 + 客座要求 |
| 2026-09-15 | L2 转录合并：§2 新增"课上与项目相关的三句话"（从 p.88 资源起步、9/19 讲 agent + RAG、Claude Code 建议）；待确认 ⑤ 更新 |
