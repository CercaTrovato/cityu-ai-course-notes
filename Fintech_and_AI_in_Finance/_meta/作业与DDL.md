---
type: 作业与DDL
course: EF5560
updated: 2026-09-17
---

# EF5560 作业与 DDL

> **来源**：`syllabus_EF5560_2026.pdf` ＋ `EF5560_FinTech_Company_Case_Requirements.pdf` ＋ `Lec01` 讲义 p.5 ＋ `M01-transcript.txt`。
> ⚠️ **Canvas 是唯一权威**。syllabus 自己写着「Later Canvas or University announcements take precedence.」讲义 p.5 也写着「**Canvas is the source of truth for rubrics, submission links, and any administrative updates.**」下面凡标 ⚪ 的日期都是推算，**不要据此安排最后一天**。

---

## 1. 时间线总表

| 日期 | 事项 | 类型 | 来源 | 可信度 |
|---|---|---|---|---|
| **2026-09-03（周四）** | Class 1 · Financial data and vibe coding | 上课 | 文件时间戳 + 转录 | 🟡 |
| **本周内（≤ 下次上课前）** | ★ **在 Canvas 上组队**（≤3 人） | **硬性要求** | 🎙️`02:15:07` | 🔴 |
| 课后（不计分） | 自己拿 HSTECH / CSI 300 / S&P 500 的股票玩一遍 vibe coding：画图、下财报、看会发生什么 | Take-home（不交） | 🎙️`02:13:16` | 🔴 |
| **2026-09-27（周日 10:00）** | **TA tutorial #1**：ML 投资作业准备 · Zoom · **有录像** | 辅导 | syllabus | 🔴 |
| **2026 年 9 月下旬 ⚪** | **ML 投资作业发布** | 作业发布 | 🎙️`11:10`「I will probably send you the assignment **in late September**」 | ⚠️ 与 syllabus 冲突，见 §4 |
| **2026-10-01（周四）** | 🚫 **国庆假期，停课** | 停课 | ⚪ 推断（🎙️`13:51` + 10/01 确为周四） | ⚪ |
| **Week 7 结束前 ⚪** | **ML 投资作业截止** | **DDL** | syllabus「due two weeks later, in Week 7」；讲义 p.5「due at the **end of Week 7**」 | ⚠️ 见 §4 |
| **2026 年 11 月中旬** | 模拟卷（mock paper）发布到 Canvas | 复习材料 | syllabus | 🟡 |
| **Week 12 ⚪（约 2026-11-16 ~ 11-20）** | **FinTech 案例报告 + 录像展示 双双截止** | **DDL** | syllabus + 案例 brief + 讲义 p.5 | 🟡 |
| **2026-11-29（周日 10:00）** | **TA tutorial #2**：期末考准备，**逐题讲模拟卷** · Zoom · **有录像** | 辅导 | syllabus | 🔴 |
| **2026-11-30（周一）** | ⚠️ **学术诚信在线课程 + 测验 + 声明**（**Semester A 2026/27 全体新生**） | **硬性 DDL** | syllabus | 🔴 |
| **2026-12 考试周 ⚪** | **期末考**：2 小时、线下、手写、闭卷 | **考试** | syllabus + 🎙️`10:20` | 🟡 |

---

## 2. 三项要交的东西

### 2.1 ★ 组队（本周唯一的硬性要求）

| 项 | 内容 |
|---|---|
| 规模 | **最多 3 人** |
| 在哪做 | **Canvas 的 group 功能**（🎙️`02:14:29`：「form your study group. There [is a] Canvas here… you see fintech group one to one. You just put three names here.」） |
| 截止 | **下次上课之前**——🎙️`02:15:07`「**This is the only thing I require. You have to finish before our [next class].**」 |
| 用途 | **同一个组同时做 ML 投资作业和 FinTech 案例**（🎙️`02:15:07`：「you will finish the assignment with your groupmate. You finish[ed] the [case] with the [same] mate.」） |

> ⚠️ **两项作业共用同一个组**，所以选人要慎重——一个组要一起交 20% 的 ML 作业和 30% 的案例 + 录像，**合计 50% 的成绩**。

### 2.2 ML 投资作业（20%）

| 项 | 内容 |
|---|---|
| 权重 | **20%** |
| 团队 | 最多 3 人，**一份联合报告** |
| 发布 | Week 5 课后（syllabus）／ Class 5 后（讲义 p.5）／「late September」（🎙️）→ **见 §4 的冲突** |
| 截止 | 发布后**两周**，Week 7 结束前 |
| **要交三样** | ① 报告 ② **组合权重 CSV** ③ **可复现的代码包（reproducible code package）** |
| 封面要求 | 列出**全部组员姓名 + CityU 学号**；指定**一位提交人** |
| 内容 | 🎙️`10:32`「I'll give you some **predictors, some stocks**, and then you run your investment analysis… based on everything we show you for the **first five lectures**」 |
| 详细要求 | 另有 assignment brief（发布时一并给出） |

> ★ **"可复现代码包"这一项直接呼应 M01 的课堂强调**：🎙️`01:06:31`「every time you ask your AI to use the vibe coding for you, **please also save the file for the code**」。**从第一周就开始存代码，不要到交作业时才想起来。** 见 [[M01-金融数据与Vibe-Coding#2.2.4 🎙️ 三条只有课堂上才有的操作要点|M01 §2.2.4]]。
>
> ★ **数据集准备**：`spy_monthly_features_240m.csv` 是一张**已经做对了的无泄漏特征表**，可以直接当模板对照。见 [[Fintech_and_AI_in_Finance/_meta/数据集卡片|数据集卡片]] §7。

### 2.3 FinTech 公司案例：报告（10%）+ 录像展示（20%）

**共 30%，是全课最大的单块成绩。**

| 项 | 报告 | 录像 |
|---|---|---|
| 权重 | **10%** | **20%** |
| 上限 | **≤ 10 页**（含图、表、参考文献、附录，全部计入） | **≤ 10 分钟** |
| 文件 | — | **一个 MP4，≤ 80 MB** |
| 截止 | **Week 12**（两项同时） | 同左 |
| 团队 | 最多 3 人 | 同左 |
| 个人要求 | — | **每位成员必须可辨识、且至少讲 2 分钟实质分析**；开头或屏幕上写出发言人姓名 |
| 现场展示 | — | **没有**。🎙️`14:31`：因国庆停课导致今年只有 12 讲，取消了现场展示 |

**要回答的核心问题（brief 原文）**
> 「**Does this company solve a real financial problem, and can its business model scale without taking unacceptable risks?**」

**报告六节骨架（brief 原文）**
1. **公司与范围**——公司、产品、司法辖区、研究期间、案例问题
2. **金融问题与用户**——客户痛点、目标用户、现有方案的局限
3. **产品与技术**——服务怎么运作；数据、AI、区块链、支付通道等技术的**实际**作用
4. **商业模式与经济性**——谁付钱、收入模型、主要成本、伙伴、激励、规模化或盈利的条件
5. **证据与竞争**——**带日期的**采用量/交易量/客户/收入/定价/业绩/市场份额数据，并做一个相关对比
6. **风险、监管与判断**——最重要的风险，以及团队的结论与后续要盯的指标

**录像五点（brief 原文）**：① 公司、案例问题、主要结论 ② 问题、用户、产品与相关技术 ③ 商业模式与价值如何创造和获取 ④ 最强的证据 + 一个竞争对手/基准 ⑤ 最重要的风险、监管与最终判断
> **「Do not read the report aloud.」** 用少量可读的幻灯片，讲**一个**清晰的论点。
> **「The sections should add up to one team argument, not three separate summaries.」**

**证据与评分标准（brief 原文）**
- **每一条非显而易见的事实主张、每一张借用的图或图片都要引用**。要分清：**公司自己说的 / 独立来源报道的 / 你们团队的结论**
- 优先用**带日期的一手或权威来源**；图表上要标注单位、日期、司法辖区、定义
- **报告**按七项评分：问题定义、机制、商业模式经济性、证据、风险与监管分析、判断、组织
- **录像**按六项评分：取舍与综合、证据与视觉、组织、清晰度、表达、**每位成员的有效参与**
- **必须披露生成式 AI 的实质性使用**。「Your team is still responsible for every claim, source, calculation, visual, and conclusion.」

**🎙️ 教授对这项作业的额外说明**
- `12:27`：「find a fintech company to prepare one report… tell me about the **business model** for the company and then what do you think about the industry」
- `13:07`：**允许（甚至预期）你用 AI 来做前期调研**——「I do not expect you will search by Google. So use AI to prepare those [materials]. It is totally fine. **But at least [cite] sources.**」
- `01:52:59`：**如果是上市公司，要自己做数字分析**——「**you should have some number analysis for the company you introduce.** …If that is not a public company, you can tell me something about [the] industry, about the [economics]」。他现场演示了用 vibe coding 拉 **MicroStrategy（现名 Strategy）** 的财报做图。
- `14:14`：录像自己用手机拍就行；文件太大就问 AI 怎么压缩。

**💡 复用提示（笔记补充）**：案例报告的六节骨架 ＝ [[Fintech_and_AI_in_Finance/_meta/考点库|考点库]] §2 框架 C ＝ 期末 FinTech 简答题的答题结构。**准备一次，三处都能用。**

---

## 3. 参与分（10%）——它是逐周结算的

| 规则 | 内容 |
|---|---|
| 起点 | **每人 5 分（满分 10）** |
| **点名** | 教授**按名单点名**，不等志愿者。syllabus：「I call on students by name rather than wait for volunteers, **so expect to be asked**.」 |
| 答对 / 推理合理 | **+1**。「Sound reasoning counts even when the final answer is not the expected one.」 |
| 答错 / 跳过 | **不扣分**。「A wrong answer costs nothing.」 |
| **被点名时不在** | **−1** |
| 请假 | **提前至少一天**发邮件说明，则不扣 |
| 其他加分 | 提问、小练习、给同学有用的反馈，都算进这 10 分 |

**🎙️ 教授的原话（`14:43`–`15:37`）**：「I **cold call** from time to time… if I call your name, if you're not here, then you will have [a] deduction. …every student start[s] with five points, five out of ten.」
另一段（`15:48`）：「for those students who can answer the question, [you get a] bonus point. **If you cannot answer, that's fine too. Nothing loose.**」
> 转录里确实出现了三次现场点名与加分（`38:17`、`01:29:29`、`02:01:45`），**说明这不是空话**。
> **🎙️ 第 2 讲再次确认**（M02 转录 `P1 09:28`–`16:47`）：开场按名单点名（缺席的同学提前发了邮件，教授说"我记住这些名字了"）；两位同学被点起来复述 M01 要点；「This might be **the only way you get bonus point**」（`P1 16:20`）——加分只有课上回答/提问这一条路。整堂课又有 4 次当堂提问给分（`P1 59:24`、`P2 11:40`、`P2 25:28`、`P2 26:01`）。

**🎙️ 期末的三条口头信息（M02 转录 `P1 01:19:13`–`01:22:02`）**
- **题型**：每讲讲义里那道"四选一 + Discuss"就是期末题型，「These are the questions you will see」；题库由教授用 AI 按讲义生成
- **模拟卷**：「At the end of the semester, I will show you practice exam. If you want to do more of them, I always have more.」（与 syllabus 的"11 月中旬发 Canvas"一致）
- **及格线**：「As long as you finish all homework and show up in exam, it is very hard for me to fail you」——三年挂 3 人：2 人缺考、1 人没做项目展示

---

## 4. ⚠️ 一个必须核对的时间冲突

**四份材料对"ML 作业什么时候发"的说法对不上：**

| 来源 | 说法 |
|---|---|
| syllabus | 「released after the **Week 5** class and due two weeks later, in **Week 7**」 |
| 讲义 p.5 | 「released after **Class 5** and due at the **end of Week 7**」 |
| 🎙️ 转录 `11:10` | 「I will probably send you the assignment **in late September**」 |
| syllabus | **TA tutorial #1（作业准备）定在 2026-09-27** |

**为什么会冲突**：若 Class 1 = 9/03（周四）且 10/01 国庆停课，则 **Class 5 落在 10/08，属于第 6 个教学周**——"Class 5" 与 "Week 5" 从此错开一周。而作业辅导 tutorial 却排在 9/27，比 Class 5 早了 11 天。

**⚪ 两种自洽的解读**：
- **解读 A**：作业其实在 **Class 4（9/24）** 后就发，9/27 辅导，两周后（约 10/08–10/16）交。符合"late September"。
- **解读 B**：syllabus 的周次是按**原定 13 周日历**写的，没有把停课算进去；实际以 Canvas 公告为准。

**结论：不要按 syllabus 的周次自行推算最后一天。盯 Canvas 公告和邮件。**

**推算日历（⚪，仅供规划，非权威）**

| Class | 日期（周四） | 教学周 | 主题 |
|---|---|---|---|
| 1 | 2026-09-03 | W1 | 金融数据与 vibe coding |
| 2 | 2026-09-10 | W2 | 回归、收益可预测性、样本外设计 |
| 3 | 2026-09-17 | W3 | 线性机器学习 |
| 4 | 2026-09-24 | W4 | 非线性机器学习 |
| — | 🚫 2026-10-01 | W5 | **国庆停课** |
| 5 | 2026-10-08 | W6 | 从预测到组合 |
| 6 | 2026-10-15 | W7 | FinTech 概览与区块链 |
| 7 | 2026-10-22 | W8 | Bitcoin 与 Ethereum |
| 8 | 2026-10-29 | W9 | DeFi、NFT、RWA |
| 9 | 2026-11-05 | W10 | 稳定币与 CBDC |
| 10 | 2026-11-12 | W11 | 支付系统 |
| 11 | 2026-11-19 | W12 | 借贷与众筹 |
| 12 | 2026-11-26 | W13 | 机器人投顾 / 网络安全 / RegTech / 文本 AI + 总结 |

> 这份日历与「模拟卷 11 月中旬发」「第二次 TA tutorial 11/29（周日，紧接最后一课）」「案例 Week 12 交」都能对上，所以**大方向应该没错**，但**每一个具体日期仍需 Canvas 确认**。

---

## 5. 提交规则速查

| 项 | 规则 | 来源 |
|---|---|---|
| 提交入口 | **一律 Canvas** | syllabus |
| 邮件主题 | **必须以 `[EF5560]` 开头** | syllabus + 🎙️`07:43` |
| 给 TA 发信 | **必须抄送教授**，主题同样加 `[EF5560]` | syllabus |
| **不要用** | Canvas message（🎙️`08:07`「that one is hard [to] reply」） | 🎙️ |
| 录像文件 | **一个 MP4，≤ 80 MB，≤ 10 分钟**；上传前**自己完整播放一遍确认没坏** | 案例 brief |
| 报告 | **≤ 10 页**，含所有图表附录 | 案例 brief |
| GenAI | 作业可用，**必须披露**；最终版必须是自己的作品，**不能复制粘贴 AI 答案**；考试禁用 | 官方目录 + syllabus + brief |
| 引用 | 每条非显而易见的事实、每张借用的图都要引用；优先**带日期的**一手来源 | brief + syllabus |
| 可复现性 | 「Empirical work must preserve the data timing and transformation steps needed to reproduce the reported result.」 | syllabus |

---

## 6. 待确认清单

| # | 事项 | 怎么解决 |
|---|---|---|
| 1 | ML 投资作业的**实际发布日与截止日** | 盯 Canvas + 教授邮件（见 §4） |
| 2 | 案例报告 + 录像的**具体截止日期与时刻** | Canvas |
| 3 | 期末考的**日期、地点、允许携带的材料**（含一页手写小抄） | Canvas；syllabus 说以学校最终考试指引为准 |
| 4 | Zoom office hour 的**具体周日日期** | Canvas |
| 5 | TA tutorial 的 Zoom 链接 | 教授说会在会前发（🎙️`12:11`） |
| 6 | 10/01 是否真的停课 | ⚪ 目前是推断；第 2 讲转录里**没有提到**，仍待确认 |
| 7 | Canvas 上是否有**更新版 Lec02 PDF** | 🎙️ 教授说已修了 p.25 那张图的时间轴（M02 转录 `P1 01:17:45`） |
| 8 | 恒生 / CSI 300 的三变量特征表是否在 Canvas | 🎙️ 教授说"数据在 Canvas 上"（`P2 41:03`）；本地 `data/` 只有 SPY 的 |
| 9 | ❗ **`class03/README.md` 引用的 `shared/` 四个面板文件**（`market_excess_return_panel.csv`、`hsi_stock_excess_return_panel.csv`、`technical_characteristics_dictionary.csv`、`risk_free_yields_monthly.csv`）不在导出包里 | **Canvas 上也没有**（2026-09-17 核实：Lecture 3 只有 PDF + `class03.zip`）。等 ML 作业发布时看是否附带；否则邮件问 TA（抄送教授，主题 `[EF5560]`） |
| 10 | Lec03（9/17）课上有没有更新 ML 作业的发布日 / 数据 / 组队要求 | 待 M03 转录 |

> 📝 **2026-09-09 版 syllabus 更新（2026-09-17 收到）**：考核权重、截止、TA tutorial（9/27、11/29）、参与规则**全部未变**；只改了 ML 板块的描述——Class 5 主题改为 "Interpretable machine learning and portfolio decisions"，ILO 2 加 "including the limits of coefficients, feature importance, and response profiles"。本文件的日期与权重无需修改。

---

## 相关

- [[Fintech_and_AI_in_Finance/00-课程总览|00-课程总览]]
- [[Fintech_and_AI_in_Finance/_prep/课程前置资料|课程前置资料]]（含 GenAI 政策的官方原文）
- [[Fintech_and_AI_in_Finance/_meta/考点库|考点库]]（案例简答题与报告共用同一个框架）
- [[Fintech_and_AI_in_Finance/_meta/数据集卡片|数据集卡片]]（ML 作业的现成数据）
