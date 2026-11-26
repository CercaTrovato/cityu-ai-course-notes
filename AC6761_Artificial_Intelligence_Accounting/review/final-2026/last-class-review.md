---
course: AC6761
module: final-review
week: null
date: 2026-11-25
source:
  - "考试内容(1).zip：9 份重点页，共 131 张；原件哈希见来源清单"
  - "Video Project.m4a：00:44:54–01:32:51 的期中复盘与期末复习"
  - "AI录音笔：11月25日20点02分_实时转写.docx：英文对照，中文机器翻译不作为原话"
transcript: merged
prerequisites: []
new_concepts: []
tags: [AC6761, final-exam, review]
status: v1.0
updated: 2026-11-26
readability_rules: v2
teaching_standard: novice-v1
---

# AC6761 最后复习课 · 考点、排除范围与英文作答

> 本文只认证本次来源与新增整理范围。材料 v1.0 表示已结合该段转录；旧各讲材料版本和本人学习状态不随之升级。最终审查范围与未核项见本目录 audit/last-class-20261126/。

## 0. 三分钟速览

这份笔记把 11 月 25 日最后复习课的考试要求，整理成逐页解释和可以练习的英文答题材料。

学完后应能完成以下任务：

- 解释至少三个会计假设和两个约束，识别会计交易，区分时点报表与期间报表。
- 用正确分母做共同比，并解释一两个结构变化。
- 在给定 REA 骨架中识别采购／销售的资源、事件、参与者和三类核心关联。
- 检查关系表的三个原则，按简单 SQL 写出结果表。
- 比较四类学习，解释五项所供 AI 技术，并为角色或分析模型写具体 Prompt。

**🎙️ 课堂实况**（`00:44:54`–`01:32:51`）：前段回顾期中题，`00:50:22` 起转入期末复习。本文保留整段复盘证据；原音前 `00:44:54` 的其他授课或活动不属于本次全面整理范围。

### 0.1 先按这个范围准备

下面每行是一组准备任务；右列是录音原时钟，不是按 Word 排版估计的时间。

| 周次 | 保留的重点与要求 | 录音定位 |
|---|---|---|
| W1 | 会计假设至少 3/4、两个约束、交易识别、读懂利润表与资产负债表 | `00:54:06`–`00:58:13` |
| W3 | 流动／非流动资产、共同比计算与简析 | `00:59:22`–`01:03:20` |
| W4 | REA 两优两缺、外键、三个关系表原则与错误识别 | `01:03:55`–`01:07:13` |
| W5 | 采购／销售核心图、三类核心关联、Proposition、Reservation 的作用 | `01:07:36`–`01:14:20` |
| W6 | 简单 SQL 给表推结果、比较、逻辑、范围、空值 | `01:15:25`–`01:18:39` |
| W8 | 四类学习的意思、例子和利弊、关键技术、AI 至少两优两缺 | `01:19:48`–`01:22:52` |
| W9 | 11 类角色至少准备 5 类、各两项关切、Question／Prompt、幻觉及缓解 | `01:23:30`–`01:27:15` |
| W10 | 8 个已讲模型至少熟悉 3–4 个、设计具体、相关的问题／Prompt | `01:27:52`–`01:29:55` |
| W11 | Bias 与 Fairness 的例子、影响和缓解，原课件 p.27–29 | `01:30:43`–`01:31:26` |

“至少准备”是复习要求，不能据此推出试卷一定让你任选相同数量。题数、每题分值、选答规则仍未取得。

### 0.2 明确排除与降权

这里把排除范围单列，防止沿用早期全课框架。

| 内容 | 最后课说明 | 录音定位 |
|---|---|---|
| 会计原则 | 已在期中考过，不再重考、不要和假设混淆 | `00:54:15` |
| 逐笔交易分析、T 形账户、W2 | 明确不考，W2 整章跳过 | `00:48:01`、`00:48:30`、`00:59:10` |
| 从零编制财务报表 | 不要求、给表后的识别和简释仍保留 | `00:56:38`–`00:57:31` |
| 现金流、权益变动表与附注 | 本次可忽略、不删历史笔记 | `01:03:20` |
| REA 属性、多重性、模型转关系表 | 排除细节与转换、核心图与外键原则仍保留 | `00:49:37`、`01:05:31`、`01:07:13` |
| Custody、Assignment、Responsibility | 排除、Stockflow、Participation、Duality 保留 | `01:08:08` |
| 其他扩展关系 | 只留 Proposition、Reservation 及相关发起／承诺事件 | `01:10:50`–`01:13:21` |
| Access 点击步骤、JOIN、QBE、原 p.52 起计算 | 转向纸笔简单 SQL、内外连接不考 | `01:14:54`、`01:17:17`、`01:18:51`–`01:19:15` |
| 回归、AI 历史／品牌工具介绍 | 回归明确忽略、介绍性内容降权 | `01:19:32`–`01:21:24` |
| Ratio 补充 PPT 手算 | 不要求计算、不能扩大为 W3 共同比也不算 | `01:29:55` |
| Value Chain 与 W11 其他部分 | Value Chain 未讲、W11 只强调偏见公平三页 | `01:27:58`、`01:31:15`–`01:31:26` |

### 0.3 考务安排与待核条件

考试为 2026 年 12 月 12 日（周六）09:30–12:30，香港时间，闭卷、纸笔。日期和开始时刻有本次录音 `00:51:12`–`00:51:28` 支持；结束时刻及 3 小时长度同时沿用本库 11 月 5 日 AIMS 快照与本学期 Outline，不冒称本次重新登录核过。

老师在 `00:51:34`–`00:52:10` 提到 LT13 和 B5 207，并提醒查看个人考场分配。旧个人快照是 YEUNG LT13；请以个人最新安排为准，不能从两间考场列表推定本人被改派。期末占总评 50% 来自本学期 Outline；录音中的及格数字另见 §9.3，不与权重混成一个数字。

## 1. 开始之前 · 来源和使用路线

### 1.1 本次材料

用户提供的压缩包有一段 `Video Project.m4a`、一份实时转写 DOCX、9 份“重点页”PPTX。9 份 PPT 合计 131 张；它们是节选和带标注的复习材料，未取得其制作人或教师正式发布身份的证明。

录音总长 `01:32:53.840`。本地 Whisper 重转后，本文采用原音 `00:44:54`–`01:32:51` 共 427 个带时戳段落。全部原时钟保留，不把截取后的 00:00 冒充原录音开头。

DOCX 的英文转写用于独立对照；附带中文机器翻译不当作教授原话。来源文本、原件哈希、提取方式和两处过滤恢复记录见 `sources/last-class-20261125/source-manifest.json`。没有逐字人工核听，不能把 ASR 原话称为人工听校稿。

### 1.2 需要唤醒的知识

资产是企业控制的资源，负债是企业须履行的义务，权益是扣除负债后的剩余权益。具体账户处理仍见 [[AC6761_Artificial_Intelligence_Accounting/notes/M01-会计与商业|M01]]，本次不再用逐笔交易训练替代新的范围重点。

数据库表的一行表示一条记录，一列表示同类属性。主键识别记录，外键引用别表记录；本次仍须会解释和找错，但不要求重做全部 REA 属性与多重性。

### 1.3 三条路线

- 第一次学：读 §0 后按 §2 的 W1 → W3 → W4 → W5 → W6 → W8 → W9 → W10 → W11 顺序，做相邻例题。
- 对照重点页：在 §8 找“周次＋节选物理页”，直接进入 §2 的独立页标题。原课件页号与节选页号分别记录，不混用。
- 考前复习：用 §4 查数量和边界，再遮住 §7 答案作答；回到 §2 检查理由。本人作答与掌握状态仍由实际学习证据决定。

## 2. 按重点页逐页整理

### 2.1 Week 1 · 课堂范围与逐页解释

**🎙️ 课堂补充**（Week 1）：另参看 `00:54:50` 两个约束、`00:55:39` 交易识别与 `00:57:31` 两张报表。

> *"So for these accounting assumptions, I only request you to get familiar with at least three out of four, okay?"*（`00:54:35`）

#### 2.1.01 W1 节选 p.1 · Accounting Principles

📄 来源：`Week 1 重点页.pptx`，物理页 1；本库主课件物理页：33。

四条会计原则是计量、收入确认、费用确认和充分披露。本页属于期中回顾；最后复习课明确说原则已考过、不再重考。不要把旁边的会计假设也一同划掉。旧题讲解保留在 M01 §2.6.3。

#### 2.1.02 W1 节选 p.2 · Accounting Assumptions

📄 来源：`Week 1 重点页.pptx`，物理页 2；本库主课件物理页：34。

公司买机器后仍计划持续经营，报表通常不按立刻清算的价格来编制，这是持续经营（Going Concern）。

货币单位（Monetary Unit）规定用货币表达可计量事项；主体（Business Entity）把公司与业主的个人生活分开；会计期间（Time Period）把持续经营切成月或年。

考试至少熟悉四个中的三个，要能用自己的话解释并举例。

#### 会计假设：从例子走到英文作答

以下例子和英文答案为笔记补充。先看企业发生什么，再选假设，不靠中文名称猜。

- 公司还会正常营运：不先假定下周清算，这是持续经营。英文可写：The going-concern assumption treats the business as continuing to operate rather than being liquidated.
- 业主的个人旅游费不与企业营业费用混记：这是主体假设。英文可写：The business entity assumption separates the business from its owner's personal affairs.
- 公司每年编报：这是会计期间。英文可写：The time-period assumption divides the life of a business into reporting periods, such as months or years.
- 用金额记录可计量的交易：这是货币单位。英文可写：The monetary-unit assumption expresses transactions and events in money units.

改条件：雇员士气下降虽可能影响经营，却不因为重要就自动具备可可靠计量、可直接入账的金额。假设用于解释记录框架，不是所有重要事项都必须列入资产。

#### 2.1.03 W1 节选 p.3 · Accounting Constraint

📄 来源：`Week 1 重点页.pptx`，物理页 3；本库主课件物理页：36。

成本效益（Cost-benefit）比较披露信息的价值与收集、处理成本。重要性（Materiality）问遗漏或错报是否可能改变合理使用者的决定。

前者问值不值得获取，后者问会不会影响判断；不能把金额小自动等同于不重要。

#### 两个约束怎样区别

笔记补充：为低价值管理报表采集某项极昂贵数据，需比较增加信息对决定的帮助与成本，这是 Cost-benefit。若遗漏一个金额不大但会影响使用者决定的事项，仍可能 Material，这是 Materiality。它们不是同一个“金额够不够大”判断。

英文参考：Under the cost-benefit constraint, the benefits of providing information should exceed its cost. Under materiality, information should be disclosed when its omission or misstatement could affect users' decisions.

这里用于课堂概念解释，不替代特定法域的现实披露准则。

#### 2.1.04 W1 节选 p.4 · Transaction Analysis

📄 来源：`Week 1 重点页.pptx`，物理页 4；本库主课件物理页：51。

先问某活动是否影响资产、负债或权益，再问影响能否可靠计量。买入设备会改变资产组合；只打电话询价而尚无交易，不因发生了业务接触就必然入账。自然灾害造成可计量资产损失，也可能需要记录。

本页的识别逻辑仍在重点内。

#### 2.1.05 W1 节选 p.5 · Transaction Analysis-Rules

📄 来源：`Week 1 重点页.pptx`，物理页 5；本库主课件物理页：52。

资产（Assets）是企业控制的资源；负债（Liabilities）是需要履行的债务；权益（Equity）是扣除负债后属于业主的部分。等式表达同一资源的资金来源。

逐笔交易分析计算本次排除，等式仍帮助识别要记录的业务。

#### 2.1.06 W1 节选 p.6 · Transaction Analysis-Exercises

📄 来源：`Week 1 重点页.pptx`，物理页 6；本库主课件物理页：53。

这页列 FastForward 交易 1–5，是旧交易分析练习。最后课明确排除这种逐笔计算；保留原题、原页与 M01 的既有完整解析，不把它继续排进期末刷题顺序。

<details><summary>保留旧原题（本次明确排除，完整解析沿用 M01）</summary>

Transaction Analysis-Exercises
Use the accounting equation to analyze the following transactions of FastForward for the month of December 2021.
On December 1, 2021, Chuck Taylor invested \$30,000 cash to start a consulting business: FastForward. 
purchased supplies paying \$2,500 cash.
purchased equipment paying \$26,000 cash.
purchased supplies of \$7,100 on account from CalTech Supply Co.
provided consulting services receiving \$4,200 cash.






[[AC6761_Artificial_Intelligence_Accounting/notes/M01-会计与商业|既有 M01 交易分析解析]]。本次不把归档当作重新验收。

</details>

#### 2.1.07 W1 节选 p.7 · Transaction Analysis-Exercises

📄 来源：`Week 1 重点页.pptx`，物理页 7；本库主课件物理页：54。

本页续交易 6–11，包括租金、工资、赊销、收欠款、还供应商和股利。它与上一页一样属于被排除的旧交易分析；收欠款不重复计收入等知识保留在 M01，不删除历史正文。

<details><summary>保留旧原题（本次明确排除，完整解析沿用 M01）</summary>

Transaction Analysis-Exercises
Paid \$1,000 rent to the landlord of the building where its facilities are located.
Paid salary of \$700 to its employees.
Provided consulting service of \$1600 on credit and rented its test facilities for \$300 to a sports club. 
Received the cash payment of \$1,900 from the sports club ten days later.
Paid CalTech Supply \$900 cash as partial payment for its earlier \$7,100 purchase of supplies.
Cash dividend to owner of \$200. 

[[AC6761_Artificial_Intelligence_Accounting/notes/M01-会计与商业|既有 M01 交易分析解析]]。本次不把归档当作重新验收。

</details>

### 2.3 Week 3 · 课堂范围与逐页解释

**🎙️ 课堂补充**（Week 3）：另参看 `01:00:55` 共同比资产负债表与 `01:03:20` 排除现金流、权益表及附注。

> *"again, common size income statement analysis is important."*（`01:02:29`）

#### 2.3.01 W3 节选 p.1 · Balance Sheet(Statement of financial position)

📄 来源：`Week 3 重点页.pptx`，物理页 1；本库主课件物理页：3。

本页为资产负债表（Balance Sheet，又称 Statement of Financial Position）的分隔页。下一页解释它回答的时点问题；分隔页本身没有新增计算任务。

#### 2.3.02 W3 节选 p.2 · Snapshot of financial position on a given day

📄 来源：`Week 3 重点页.pptx`，物理页 2；本库主课件物理页：4。

资产负债表是某一天的财务位置快照：企业控制哪些资源，以及资源由债权人还是股东提供。资产总额与负债加权益相等。不要把某日余额解释成整年的收入；本次重点是识别报表和资产类别。

#### 2.3.03 W3 节选 p.3 · Balance Sheet

📄 来源：`Week 3 重点页.pptx`，物理页 3；本库主课件物理页：5。

流动资产（Current Assets）按课件的完整条件，在一年或一个营业周期内转为现金，取较长者。营业周期是从付钱买料到卖出并收回现金的一轮。

现金、应收款、库存通常属于这一组；长期厂房设备属于非流动资产。老师口头说“容易变现金”是简化，不能丢掉时间条件。

#### 2.3.04 W3 节选 p.4 · Non-Current Assets

📄 来源：`Week 3 重点页.pptx`，物理页 4；本库主课件物理页：6。

厂房设备（PP&E）用于持续经营，通常不会在短期内当作日常商品卖掉。长期投资预期持有超过一年或营业周期，因此与短期现金用途不同。考试识别资产分类即可；折旧政策和投资明细不据本页自动升级为单独计算题。

#### 2.3.05 W3 节选 p.5 · Intangibles

📄 来源：`Week 3 重点页.pptx`，物理页 5；本库主课件物理页：7。

无形资产（Intangibles）没有实物形态，例如专利。商誉（Goodwill）是并购支付价超过取得可辨认净资产公允价值的部分；企业自己培养的声誉通常不能直接列作同一资产。

分类时看用途和确认条件，不看名字是否带“资产”。

#### 2.3.06 W3 节选 p.6 · Current Assets

📄 来源：`Week 3 重点页.pptx`，物理页 6；本库主课件物理页：8。

库存（Inventories）虽然尚未是现金，但会随销售再收款而完成营业周期，所以通常列为流动资产。仓库积压会占用资金；库存高不自动表示经营更好。减值与舞弊例子是理解背景，本次不扩成新的准则计算题。

#### 2.3.07 W3 节选 p.7 · Accounts Receivables

📄 来源：`Week 3 重点页.pptx`，物理页 7；本库主课件物理页：9。

应收账款（Accounts Receivable）是已向客户提供商品或服务、尚未收回的款项；现金及现金等价物（Cash and Cash Equivalents）用于近期付款。

应收款通常可在短期收回，但不是已经到账的现金。

#### 2.3.08 W3 节选 p.8 · Current Liabilities

📄 来源：`Week 3 重点页.pptx`，物理页 8；本库主课件物理页：10。

流动负债与非流动负债按偿付期限区分。它们有助于理解整张表，但最后复习课对本章要求集中在资产分类，负债和权益细节降权；不能据此把下一节共同比表中这些行从题面删掉。

#### 2.3.09 W3 节选 p.9 · Key information:

📄 来源：`Week 3 重点页.pptx`，物理页 9；本库主课件物理页：13。

读表可看到资源规模、融资来源与短期偿债压力；历史成本与未确认项目限制了它表达当前市场价值的能力。本页作为理解背景保留，本次不要求额外展开全部弱点。

#### 2.3.10 W3 节选 p.10 · Common-size analysis converts financial statement line items into percentages of either total sales (for income statement) or total assets (for balance sheet).

📄 来源：`Week 3 重点页.pptx`，物理页 10；本库主课件物理页：16。

共同比分析（Common-size Analysis）先把每个项目除以同一基数，再乘 100%。资产负债表用总资产，利润表用营业收入。

它把大小不同的公司转换成可比较的结构，不能把占比变化直接说成金额变化。

#### 2.3.11 W3 节选 p.11 · Common-Size Balance Sheet

📄 来源：`Week 3 重点页.pptx`，物理页 11；本库主课件物理页：17。

A 的总资产为 3,000,000，B 为 35,000,000。先各用流动加非流动资产求出分母，再把每行除以本公司总资产。负债和权益同样使用总资产作分母，不能分别换成总负债或总权益。

完整复算见本节例题。

#### 原表完整复算：公司 A 与 B

给定数据来自节选 p.11／主课件 p.17，单位均为课件中的 $。每行表示一个报表项目；先保持原金额，再计算各公司的总资产。

| 项目 | Company A | Company B |
|---|---:|---:|
| Current Assets | 2,000,000 | 25,000,000 |
| Non-current Assets | 1,000,000 | 10,000,000 |
| Current Liabilities | 500,000 | 3,000,000 |
| Non-current Liabilities | 1,500,000 | 12,000,000 |
| Shareholders’ Equity | 1,000,000 | 20,000,000 |

A 的分母是流动资产加非流动资产：

$$
TA_A = 2{,}000{,}000 + 1{,}000{,}000 = 3{,}000{,}000
$$

B 同样求得总资产 35,000,000。对每一行，$x$ 表示该项目金额，$TA$ 表示同一公司的总资产；两者须同一天、同币种和单位。

$$
\text{Common-size percentage} = \frac{x}{TA}\times 100\%
$$

例如 A 的流动负债占比：$500{,}000/3{,}000{,}000\times100\%=16.7\%$。结果回答“每 100 元总资产由多少元流动负债支持”，不是流动负债增长了 16.7%。

以下按一位小数显示，已用 calculations.py 复算。

| 项目 | Company A | Company B |
|---|---:|---:|
| Current Assets | 66.7% | 71.4% |
| Non-current Assets | 33.3% | 28.6% |
| Current Liabilities | 16.7% | 8.6% |
| Non-current Liabilities | 50.0% | 34.3% |
| Shareholders’ Equity | 33.3% | 57.1% |

A 两类资产合计 100%，负债与权益三项另合计 100%。不能把这五行全部相加再要求等于 100%。舍入后尾差按给定精度解释。

英文参考：Company B has a larger share of current assets, 71.4% versus 66.7%. Its equity also represents a larger proportion of total assets. These structural differences alone do not establish which firm is better managed.

换成利润表时，分母换为同年 Revenue；不要沿用 Total Assets。若总资产或收入为零，百分比无法这样定义，需说明分母问题。

#### 2.3.12 W3 节选 p.12 · Common-Size Balance Sheet

📄 来源：`Week 3 重点页.pptx`，物理页 12；本库主课件物理页：18。

这是上一页的给定共同比结果。A 的流动资产为 66.7%，B 为 71.4%；A 的流动负债为 16.7%，B 为 8.6%。

同侧的互不重叠项目可加总核 100%，不能把资产侧与资金来源侧混加成一张 100% 分配。

#### 2.3.13 W3 节选 p.13 · Nike: Balance Sheet (Assets)

📄 来源：`Week 3 重点页.pptx`，物理页 13；本库主课件物理页：22。

Nike 原资产表按 2014、2015、2016 年排列。先认年份，再找 TOTAL ASSETS；Total current assets 是其下属小计，不与各项流动资产重复相加。

金额仅用于所给历史案例，不当作 Nike 现状。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w03-s013.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.3.14 W3 节选 p.14 · Nike: Common-Size Balance Sheet (Assets)

📄 来源：`Week 3 重点页.pptx`，物理页 14；本库主课件物理页：23。

左边 Common-Size 是该年项目除以该年总资产；右边 Percentage Change 是相对上年的金额变化率。

2016 年 PP&E 占比 16.5%，与其金额增长 16.9% 回答不同问题。不能把左列百分比当成右列增长率。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w03-s014.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.3.15 W3 节选 p.15 · Nike: Common-Size Balance Sheet (Liabilities and Shareholders’ Equity)

📄 来源：`Week 3 重点页.pptx`，物理页 15；本库主课件物理页：24。

本页把负债和权益也除以总资产。2016 年负债占 42.7%、权益占 57.3%，合计 100%。这些给定比例用于共同比读表；并不推翻老师对负债与权益细节的降权。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w03-s015.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.3.16 W3 节选 p.16 · Nike:  Excerpts from Notes

📄 来源：`Week 3 重点页.pptx`，物理页 16；本库主课件物理页：25。

附注（Notes）说明 PP&E 采用何种成本和折旧口径，也解释无形资产与商誉。它是理解原表的背景；最后课明确把附注排除。所示商誉句子没有充分区分可辨认无形资产与商誉，不能机械当作全部无形资产的定义。

#### 2.3.17 W3 节选 p.17 · Nike: Analyzing Balance Sheet

📄 来源：`Week 3 重点页.pptx`，物理页 17；本库主课件物理页：26。

原题问 Nike 的 PP&E 占总资产比例为何相对小。参考解释是生产外包减少自有生产设施需求；占比只是线索，不能单凭比例证明所有生产都外包。完整英文题面与参考答句见本节。

#### 保留原题与参考作答

原题（节选 p.17／主课件 p.26）：

> Refer to the common-size and percentage change balance sheets for Nike at the end of 2014, 2015, and 2016. What is the likely explanation for the relatively small percentages for property, plant, and equipment?

中文读题：解释 PP&E 占总资产比例相对小的可能业务原因；likely 表示有依据的可能解释，不要求仅靠比例证明因果。

⚪ 参考作答：外包生产可减少自有厂房与设备需求，所以 PP&E 在总资产中占比较小。旧课堂记录也给出这一方向；本次没有重新核 Nike 外部年报，不把可能解释写成刚核实的现实经营全貌。

英文参考：Nike's use of outsourced production can reduce its need to own manufacturing facilities and equipment. This helps explain the relatively small share of PP&E in total assets.

改条件：若题面说企业大量购置自有工厂，应重新检查外包解释是否仍符合事实。

#### 2.3.18 W3 节选 p.18 · Nike: Analyzing Balance Sheet

📄 来源：`Week 3 重点页.pptx`，物理页 18；本库主课件物理页：27。

原题问票据应付与长期债务占比为何相对小。参考解释是较少固定资产投入、内部产生现金较多，降低外部借款需求。低债务不是单凭这一比例即可证明的最佳资本结构。完整题面与参考答句见本节。

#### 保留原题与参考作答

原题（节选 p.18／主课件 p.27）：

> What is the likely explanation for the relatively small percentages for notes payable and long-term debt?

中文读题：解释借款占总资产比例小的可能原因，不是把低借款直接评价为更好。

⚪ 参考作答：较少的自有生产设施可能降低固定资产融资需求；若企业能产生充足经营现金，也可少依赖外部借款。两项都是需要业务事实支持的解释。

英文参考：Lower investment in owned production facilities can reduce financing needs. Strong internally generated cash can also reduce reliance on notes payable and long-term debt.

改条件：若企业现金紧张且有大规模新建厂项目，就不能照搬“内部资金充足”的理由。

#### 2.3.19 W3 节选 p.19 · Income Statement

📄 来源：`Week 3 重点页.pptx`，物理页 19；本库主课件物理页：28。

本页为利润表（Income Statement，又称 Statement of Profit or Loss）的分隔页。它接下来解释一段期间如何形成利润，与某日的资产负债表区分。

#### 2.3.20 W3 节选 p.20 · Shows financial performance over a given period

📄 来源：`Week 3 重点页.pptx`，物理页 20；本库主课件物理页：29。

利润表汇总一段期间的收入、费用及其他损益，得到净利润。关键是“期间”，例如一年截至某日，而非只看那一天。老师不要求背完整损益公式或细查每项确认规则。

#### 2.3.21 W3 节选 p.21 · Income Statement

📄 来源：`Week 3 重点页.pptx`，物理页 21；本库主课件物理页：30。

从销售收入扣销售成本得到毛利，再扣经营费用、融资成本及税项，逐层走到税后利润。此顺序帮助读懂给定报表；本次不要求从零编制一张完整利润表。

#### 2.3.22 W3 节选 p.22 · Revenues

📄 来源：`Week 3 重点页.pptx`，物理页 22；本库主课件物理页：31。

Revenue、Sales、Turnover 在本页都是主营收入的常见写法。

毛利（Gross Profit）是收入扣与已售商品对应的销售成本；Other income 来自其他来源，不与主营销售额随意混作同一分母。

#### 2.3.23 W3 节选 p.23 · Expenses

📄 来源：`Week 3 重点页.pptx`，物理页 23；本库主课件物理页：32。

Distribution 是销售配送相关费用；Administration 是维持日常管理的费用；Finance costs 是债务融资费用。

做共同比解释时，某类费用占收入比例升高，会压缩其他条件相同下的利润空间。

#### 2.3.24 W3 节选 p.24 · Income Statement

📄 来源：`Week 3 重点页.pptx`，物理页 24；本库主课件物理页：33。

读利润表既看利润金额，也看来源是否持续。一次性收益可能抬高当期利润，不能据此认定以后每年都能赚同样多。最后课只要求简洁解释明显变化，不逐项展开所有分析维度。

#### 2.3.25 W3 节选 p.25 · Nike: Income Statement

📄 来源：`Week 3 重点页.pptx`，物理页 25；本库主课件物理页：36。

Nike 原利润表依次给出 2014–2016 年收入、成本及净利润。2016 年收入 32,376、净利润 3,760；占比计算必须用同一年、同单位。每股指标不能作为普通金额行除以总收入。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w03-s025.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.3.26 W3 节选 p.26 · Nike: Common-Size Income Statement

📄 来源：`Week 3 重点页.pptx`，物理页 26；本库主课件物理页：37。

共同比利润表把每年收入固定为 100%。2014–2016 年净利率从 9.7% 升到 11.6%，与老师口头举的“净利率下降”泛例不是同一事实。

解释可选一两个明显因素，不能说收入自己的共同比从 100% 下降。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w03-s026.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 给表后的简短解释

用原表 2016 年净利润 3,760 除以收入 32,376，可得约 11.6%。同法 2014 年为 2,693／27,799，约 9.7%；差约 1.9 个百分点。比例按 calculations.py 复算。

原表销售成本占比从 55.2% 降到 53.8%，与毛利率提高一致；税费占比从约 3.1% 降到约 2.7%，也有助于解释净利率变化。经营开销占比却升高，不能说所有费用都降低。

英文参考：The net profit margin increased from about 9.7% to 11.6%. A lower cost-of-sales share and a lower tax-expense share helped offset a higher operating-overhead share.

这里讨论的是原表历史案例，不复述录音中方向相反的泛例。

### 2.4 Week 4 · 课堂范围与逐页解释

**🎙️ 课堂补充**（Week 4）：另参看 `01:05:56` 三个原则、`01:07:00` 两种 One Fact, One Place 错误。

> *"Two strengths, two limitations you should be able to discuss."*（`01:04:02`）

#### 2.4.01 W4 节选 p.1 · AC6761 Artificial Intelligence Accounting

📄 来源：`Week 4 重点页.pptx`，物理页 1；本库主课件物理页：1。

章节封面；本章复习从 REA 的优缺点与关系数据库原则进入。历史复式记账题不自动因封面保留而重新成为期末重点。

#### 2.4.02 W4 节选 p.2 · Traditional Double-Entry Bookkeeping

📄 来源：`Week 4 重点页.pptx`，物理页 2；本库主课件物理页：2。

复式记账用借贷两边保持会计等式平衡，主要表达财务结果。这里用它与 REA 对比；最后课说传统系统的优缺点已在期中考过，复习应转向 REA 本身。

#### 2.4.03 W4 节选 p.3 · Strengths and limitations

📄 来源：`Week 4 重点页.pptx`，物理页 3；本库主课件物理页：3。

传统系统的优点是有标准化记录和借贷核对，局限是非财务过程信息不充分、偏重历史。课件写试算平衡“确保数学准确”需限定：借贷相等仍可能遗漏整笔交易，不能保证所有会计错误都不存在。

#### 2.4.04 W4 节选 p.4 · REA Accounting Model: A Paradigm Shift

📄 来源：`Week 4 重点页.pptx`，物理页 4；本库主课件物理页：4。

资源（Resources）是企业拥有或控制的对象，事件（Events）是业务中实际发生的动作，参与者（Agents）是企业内外的人或组织。

REA 把一笔销售和商品、客户、员工、收款联系起来，保留业务上下文。

#### 2.4.05 W4 节选 p.5 · Strengths and limitations

📄 来源：`Week 4 重点页.pptx`，物理页 5；本库主课件物理页：5。

准备 REA 的两个优点与两个局限，并给每点理由。优点可选同时记录财务和非财务信息、沿事件发现瓶颈；局限可选数据结构重建和人员训练成本、缺乏统一报告口径。

课件“成本下降 15%”没有来源，答题不用这个未经外证的数字。

#### 两优两缺：每点怎样展开

⚪ 英文参考（按本页意思自拟）：

1. REA links financial and non-financial information, so users can investigate operational causes rather than only final accounting balances.
2. REA maps business events and resources, which can help identify delays and resource bottlenecks.
3. Implementation can be complex because the organisation must redesign data structures and train staff to capture detailed events.
4. Limited standardisation can make reporting and comparisons across organisations more difficult.

中文检查：前两项说明改进什么，后两项说明为什么成本或比较困难。把四个标题列出但不解释，不足以证明会讨论。

#### 课堂口头问题：传统报表是否足够

**🎙️ 课堂练习**：*"Can traditional financial information system disclose all the information which is useful for external users?"*（`01:04:34`）

中文题意：传统财务信息系统能否披露外部使用者需要的所有信息？all 要求检查是否存在未包含的信息，不是只评价报表有没有用。

⚪ 参考作答：不能。报表主要汇总可确认、可计量的财务结果，客户满意度、流程延迟等非财务信息可能不足；部分有价值的财务相关信息也可能未完整反映。此处解释为何需要更丰富的数据，不表示 REA 能自动披露所有商业信息。

英文参考：No. Traditional financial reporting does not capture all useful information, especially non-financial details such as customer satisfaction or process delays. Richer event data can support additional analysis, but it still needs appropriate collection and interpretation.

#### 2.4.06 W4 节选 p.6 · REA 基本框架

📄 来源：`Week 4 重点页.pptx`，物理页 6；本库主课件物理页：17。

图从左到右读“什么资源—发生什么事件—谁参与”。连线表达业务关联，不能直接读成时间或因果箭头。例如库存与销售相关，销售又与员工和客户相关；具体流入流出在下一页展开。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w04-s006.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.4.07 W4 节选 p.7 · Duality

📄 来源：`Week 4 重点页.pptx`，物理页 7；本库主课件物理页：18。

交换关系（Duality）把企业付出的经济事件与得到的经济事件相连。销售付出商品，收款取得现金；二者是交易的两面，不保证在同一天发生，也不是把借方与贷方改名。

#### 2.4.08 W4 节选 p.8 · 销售与收款

📄 来源：`Week 4 重点页.pptx`，物理页 8；本库主课件物理页：19。

原图上部 Give 是库存经 Sale 减少，下部 Get 是 Cash Receipt 使现金增加。右边员工和客户分别参与对应事件。

两事件间的 Duality 连线表示经济交换，不能读成“销售后立即全额收现”。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w04-s008.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.4.09 W4 节选 p.9 · 关系数据库

📄 来源：`Week 4 重点页.pptx`，物理页 9；本库主课件物理页：36。

主键（Primary Key）识别本表的一条记录；外键（Foreign Key）把本表记录指向另一表的主键。

例如 Sale 中的 Salesperson 值 123456，指向 Salesperson 表中同编号员工。

#### 2.4.10 W4 节选 p.10 · 表、行与列

📄 来源：`Week 4 重点页.pptx`，物理页 10；本库主课件物理页：37。

一行是一条记录，一列是同类字段，每格只存一个值。关系含义不靠行的位置来维持，字段的数据类型和键值才重要。“关系表的逻辑列序不重要”不等于 SQL 输出列序可以不按 SELECT 作答。

#### 2.4.11 W4 节选 p.11 · 外键例子

📄 来源：`Week 4 重点页.pptx`，物理页 11；本库主课件物理页：38。

销售表三行的员工编号来自下方员工表。固定一笔 Sale，可沿 Salesperson 字段查到其员工；同一个员工编号可被多笔销售引用。外键重复合法，主键则用于唯一识别员工。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w04-s011.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.4.12 W4 节选 p.12 · 关系表三原则

📄 来源：`Week 4 重点页.pptx`，物理页 12；本库主课件物理页：39。

实体完整性（Entity Integrity）要求主键不能缺失；主键身份还应唯一。

参照完整性（Referential Integrity）要求非空外键能在被引用表找到匹配值；允许空值仍取决于字段业务约束。

一事一处（One Fact, One Place）避免同一事实重复保存或一个格塞入多值。

#### 2.4.13 W4 节选 p.13 · 参照完整性例子

📄 来源：`Week 4 重点页.pptx`，物理页 13；本库主课件物理页：40。

左图允许某销售的员工外键为空，前提是业务允许未指定；其他非空值都能找到员工。右图 234567 在员工表不存在，所以违反参照完整性。要找的是不存在的身份，不是因为销售表里编号重复。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w04-s013.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.4.14 W4 节选 p.14 · 一事多处

📄 来源：`Week 4 重点页.pptx`，物理页 14；本库主课件物理页：41。

CustomerID C422 的姓名地址被复制进多笔销售，这重复保存了“客户编号—客户地址”事实。地址更改时可能漏改一行，产生不一致。

把客户事实放 Customer，Sale 只引用 CustomerID，才更容易一次维护。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w04-s014.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.4.15 W4 节选 p.15 · 一格多值

📄 来源：`Week 4 重点页.pptx`，物理页 15；本库主课件物理页：42。

Degree Earned 一格写 BS,MBA 等多个值，属于重复组：一个单元格装了多个学位事实。把每个“员工—学位”组合分成记录，可以分别查询；只改逗号或排版不能消除这一结构问题。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w04-s015.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

### 2.5 Week 5 · 课堂范围与逐页解释

**🎙️ 课堂补充**（Week 5）：另参看 `01:08:40` 提供简化骨架、`01:11:07` 要求解释关系作用。

> *"But for now, let me get this clear. Let's only focus on these two, proposition and reservation."*（`01:10:50`）

#### 2.5.01 W5 节选 p.1 · AC6761 Artificial Intelligence Accounting

📄 来源：`Week 5 重点页.pptx`，物理页 1；本库主课件物理页：1。

本章封面；本次重点是采购和销售核心模式，以及 Proposition、Reservation 两种扩展关系的业务作用。

#### 2.5.02 W5 节选 p.2 · 核心类

📄 来源：`Week 5 重点页.pptx`，物理页 2；本库主课件物理页：2。

先站在本企业角度看资源进出。采购取得库存是流入事件，付款使现金流出；销售使商品流出，收款使现金流入。内部参与者代表企业做事，外部参与者是客户或供应商。

#### 2.5.03 W5 节选 p.3 · Core REA Modeling of Acquisition

📄 来源：`Week 5 重点页.pptx`，物理页 3；本库主课件物理页：9。

采购的增量经济事件（Economic Increment Event）是收到货物、取得使用权或取得服务。资源是库存或服务；供应商是外部参与者，采购人员是内部参与者。不要把下订单就当作货物已入库。

#### 2.5.04 W5 节选 p.4 · Core REA Modeling of Acquisition

📄 来源：`Week 5 重点页.pptx`，物理页 4；本库主课件物理页：10。

采购的减量经济事件（Economic Decrement Event）是现金支付（Cash Disbursement）。现金是减少的资源；供应商仍是外部参与者，应付职员或出纳负责付款。

采购事件与付款事件通过 Duality 配对。

#### 2.5.05 W5 节选 p.5 · 采购核心图

📄 来源：`Week 5 重点页.pptx`，物理页 5；本库主课件物理页：11。

采购核心图左边是库存和现金，中间是 Purchase 与 Cash Disbursement，右边是供应商及内部人员。

Stockflow 连事件与资源，Participation 连事件与参与者，Duality 连两经济事件。看清收到货和付钱分别影响哪一种资源，准备在给定骨架中补框与关系。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w05-s005.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 怎样沿采购原图走一笔业务

笔记补充：企业向供应商买库存，收货后再付款。先找 Purchase：它让库存流入，经 Stockflow1 连到 Inventory。沿 Participation 找供应商、采购员和收货员，说明是谁参与收货。再找 Cash Disbursement：它让 Cash Account 流出，经 Stockflow2 相连。最后用 Duality 把这两次经济事件配对。

这里的线表示关联，不规定一笔采购对应几笔付款；多重性本次排除，不能从空白原图猜数字。

英文参考：A purchase increases inventory, while a cash disbursement decreases cash. Stockflow links each event to its resource, participation links it to the agents, and duality links the two exchange events.

改成销售场景时，商品的方向反过来，Sale 是流出，Cash Receipt 是流入。

#### 2.5.06 W5 节选 p.6 · Revenue Core Pattern

📄 来源：`Week 5 重点页.pptx`，物理页 6；本库主课件物理页：21。

销售核心图把 Sale 作为商品流出事件，Cash Receipt 作为现金流入事件。客户取代采购图中的供应商，销售员和出纳参与各自动作。

三种核心关联仍是 Stockflow、Participation、Duality；场景变了，企业视角不变。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w05-s006.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.5.07 W5 节选 p.7 · 扩展模型

📄 来源：`Week 5 重点页.pptx`，物理页 7；本库主课件物理页：22。

扩展图在绿色核心外加入发起事件、承诺事件等。图中黄色 Proposition、Reservation1 都接到 ResourceType，分别标明推介与预留哪一类商品。Reservation2 另接具体 Resource，用于辨认具体资源；不要把两种线端混为一处。图中其余线用于辨认背景，本次按老师收窄不逐项背诵。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w05-s007.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.5.08 W5 节选 p.8 · 发起与承诺事件

📄 来源：`Week 5 重点页.pptx`，物理页 8；本库主课件物理页：23。

发起事件（Instigation Event）开始一个业务过程，例如销售人员向潜在客户介绍产品。

承诺事件（Commitment Event）承诺未来交换，例如双方订立销售订单；它还不是实际交货或现金到账。

#### 2.5.09 W5 节选 p.9 · 扩展事件高亮

📄 来源：`Week 5 重点页.pptx`，物理页 9；本库主课件物理页：24。

本页用红框强调发起事件与承诺事件。沿产品推介到订单承诺读：先向客户介绍某商品，之后签约为客户保留库存。

图中黄色 Proposition 与 Reservation1 的左端都接 ResourceType：前者说明推介哪种商品，后者说明承诺为客户保留哪类库存。另有 Reservation2 连到具体 Resource；这些线都不等于实际资源已转移。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w05-s009.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.5.10 W5 节选 p.10 · 冲回事件

📄 来源：`Week 5 重点页.pptx`，物理页 10；本库主课件物理页：25。

冲回事件（Economic Reversal Event）例如退货，会抵销原经济事件。老师这次将此类扩展排除；保留它作为图中背景，不把采购退货扩写成当前必做题。

#### 2.5.11 W5 节选 p.11 · 冲回事件高亮

📄 来源：`Week 5 重点页.pptx`，物理页 11；本库主课件物理页：26。

本页红框换到冲回事件，用于显示它在完整扩展图的位置；这一视觉增量属于排除范围。当前应把注意力放回发起、承诺与两条资源关联。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w05-s011.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.5.12 W5 节选 p.12 · 扩展关联

📄 来源：`Week 5 重点页.pptx`，物理页 12；本库主课件物理页：27。

Proposition 是发起事件与资源或资源类型的联系；Reservation 是承诺事件与资源或资源类型的联系。答题说明“在销售电话里向客户介绍什么商品”和“下订单后为客户保留什么库存”。

Fulfillment、Reversal、Reciprocal 等其他扩展关系本次排除，不与保留的两条混背。

#### 扩展关系的英文作答

⚪ Proposition 参考：In a revenue cycle, proposition links a sales call to the products introduced to a potential customer. It identifies what the salesperson is proposing.

⚪ Reservation 参考：Reservation links a sales order to the inventory or inventory type reserved for the customer after a commitment is made. The goods have not necessarily been delivered yet.

不要把两条线只译成“提议／预订”就结束。前者定位推介什么，后者定位承诺后为谁保留什么；实际交货与现金交换仍在核心经济事件里。

### 2.6 Week 6 · 课堂范围与逐页解释

**🎙️ 课堂补充**（Week 6）：另参看 `01:17:17` 排除 JOIN、`01:18:17` BETWEEN、`01:18:51` 原 p.52 起排除。

> *"Show me the query results here."*（`01:16:36`）

#### 2.6.01 W6 节选 p.1 · AC6761 Artificial Intelligence Accounting

📄 来源：`Week 6 重点页.pptx`，物理页 1；本库主课件物理页：1。

章节封面。本次是纸笔考试，Access 的界面点击不作为主要练习，重点转向给定表与简单 SQL 的结果推演。

#### 2.6.02 W6 节选 p.2 · Link between tables

📄 来源：`Week 6 重点页.pptx`，物理页 2；本库主课件物理页：19。

本页讲在 Access 里建表间关系以表达外键。它帮助理解数据如何相连，但属于建库操作背景；不把点 Relationships 的路径当作这次必背步骤。

#### 2.6.03 W6 节选 p.3 · Access 表关联界面

📄 来源：`Week 6 重点页.pptx`，物理页 3；本库主课件物理页：20。

截图展示拖动员工主键到销售外键、启用完整性检查等动作。读懂是怎样约束匹配即可；本次不要求复现界面，右侧 1/多也不等于 UML 的全部最小参与条件。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w06-s003.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.6.04 W6 节选 p.4 · SQL 基本结构

📄 来源：`Week 6 重点页.pptx`，物理页 4；本库主课件物理页：39。

SQL（Structured Query Language，结构化查询语言）中，FROM 指明读哪张表，WHERE 决定保留哪些行，SELECT 决定输出哪些列。

纸上推演时先找表、再逐行检查条件、最后按 SELECT 顺序写列。没有 ORDER BY 不保证固定行序。

#### 2.6.05 W6 节选 p.5 · SQL 与关系代数

📄 来源：`Week 6 重点页.pptx`，物理页 5；本库主课件物理页：40。

注意同一个单词在不同体系的区别：SQL SELECT 选列，相当于关系代数的 Project；SQL WHERE 筛行，相当于关系代数的 Select。理解操作对象即可，不要只背英文名称。

#### 2.6.06 W6 节选 p.6 · SQL 筛客户收款

📄 来源：`Week 6 重点页.pptx`，物理页 6；本库主课件物理页：41。

原题从 Cash Receipt 表筛 Customer Number 为 C-2 的行，SELECT * 保留全部列。RA-1、RA-2、RA-5 满足条件；RA-3 和 RA-4 属于其他客户。

原题面、完整输入表与结果见本节例题。课件未给 C-2 加文本引号，实际语法须用 'C-2'。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w06-s006.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 原题、输入、结果与步骤

原题：

> Find the cash receipts from Customer #2 (keeping all the details of those cash receipts)

课件原 SQL 如下，按原样保留；它把文本编号 C-2 的引号省略了。

```sql
Select *
From [Cash Receipt]
Where [Customer Number] = C-2;
```

中文题意：只保留客户编号 C-2 的收款，但保留这些收款的全部字段。星号 * 是全部列，不是所有行；WHERE 仍筛行。原图上 Customer 表提供身份背景，实际 FROM 读取 Cash Receipt。

输入原表包含 RA-1 到 RA-5。RA-1、RA-2、RA-5 的 Customer Number 为 C-2；RA-3 为 C-1，RA-4 为 C-5，因此后两行不进入结果。

结果分成两张窄表，Remittance Advice# 是同一行的对应键；这是排版拆分，不是做两个查询。

| Remittance Advice# | Amount | Bank Account# |
|---|---:|---|
| RA-1 | 1,666 | BA-6 |
| RA-2 | 10,000 | BA-7 |
| RA-5 | 1,666 | BA-6 |

其余三列仍按同一收款编号对应，全部保留。

| Remittance Advice# | Date | Customer Number | Cashier Number |
|---|---|---|---|
| RA-1 | 25 July | C-2 | E-39 |
| RA-2 | 26 July | C-2 | E-39 |
| RA-5 | 25 Aug | C-2 | E-39 |

完整结果按源图核过，并用 calculations.py 作了单表筛选复算；未在真实 Access 原库执行。

正确的文本条件形式应写 `WHERE [Customer Number] = 'C-2';`。改条件为 C-1，则只剩 RA-3；改 SELECT 为 Amount，就只显示金额列，不保留其他字段。

英文参考：The query returns RA-1, RA-2 and RA-5 because their customer number is C-2. SELECT * retains every column of those rows. The C-2 text literal should be quoted in executable SQL.

#### 2.6.07 W6 节选 p.7 · SQL 选择列

📄 来源：`Week 6 重点页.pptx`，物理页 7；本库主课件物理页：42。

本题从 Customer 只取 Customer#、Name、SP# 三列，未写 WHERE，五名客户都保留。

Bill、Mick、Keith、Charlie、Ron 的顺序只是课件展示；实际查询若需固定顺序须另指定 ORDER BY。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w06-s007.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 原题与结果

原题：

> Find the customer number, name, and salesperson number for all customers

课件给定 SQL：

```sql
Select Customer#, Name, SP#
From Customer;
```

每行是一个客户，输出保留原要求的三列；A/R Amt 没在 SELECT 中，因此不显示。

| Customer# | Name | SP# |
|---|---|---|
| C-1 | Bill | E-12 |
| C-2 | Mick | E-10 |
| C-3 | Keith | E-10 |
| C-4 | Charlie | E-99 |
| C-5 | Ron | E-10 |

英文参考：All five customers remain because there is no WHERE condition. Only the customer number, name and salesperson number are projected.

改条件：若加 `WHERE [SP#] = 'E-10'`，只剩 C-2、C-3、C-5；列仍只有指定三列。

#### 2.6.08 W6 节选 p.8 · 内连接

📄 来源：`Week 6 重点页.pptx`，物理页 8；本库主课件物理页：43。

内连接（Inner Join）按共同员工编号配对两表；可能增加输出列或产生多行匹配。本页为被明确排除的 JOIN 内容，保留原题及 M06 既有解题位置，不把它混入本次单表结果训练。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w06-s008.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.6.09 W6 节选 p.9 · 外连接

📄 来源：`Week 6 重点页.pptx`，物理页 9；本库主课件物理页：44。

外连接（Outer Join）除匹配行外还保留一侧未匹配记录。原图 S-6、S-7 未收款仍出现；此类连接本次明确排除。

原页教学 SQL 不是可直接执行的标准 Access JOIN 写法，避免照抄为可运行语句。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w06-s009.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.6.10 W6 节选 p.10 · 比较运算符

📄 来源：`Week 6 重点页.pptx`，物理页 10；本库主课件物理页：45。

比较符 =、<、<=、>、>=、<> 分别检验相等、较小、不大于、较大、不小于、不等。日期早于较晚日期，文本依排序规则比较。先看字段值，再判断每行真假；>= 会保留刚好等于门槛的行。

#### 2.6.11 W6 节选 p.11 · 金额比较

📄 来源：`Week 6 重点页.pptx`，物理页 11；本库主课件物理页：46。

给定 Cash 表，Balance >= 50,000 仅保留 BA-8 的 75,000。BA-9 为 0，不满足；BA-6 与 BA-7 是缺失值，不是 0，不能当作已知余额来比较。

英文参考：Only BA-8 is returned, with a balance of 75,000. The zero balance does not satisfy the condition, and null balances do not establish that the condition is true.

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w06-s011.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.6.12 W6 节选 p.12 · 文本比较

📄 来源：`Week 6 重点页.pptx`，物理页 12；本库主课件物理页：47。

题目要求 SalesRep# <> E-10，按原表只留下 S-1 的 7,200 和 S-7 的 23,000。符号 <> 是不等于；筛选用员工列，输出却只显示 Sale# 与 Amount。

文本编号在真实 SQL 应加引号。

英文参考：The query returns S-1 with 7,200 and S-7 with 23,000 because their salesperson numbers are not E-10. Only Sale# and Amount appear in the output.

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w06-s012.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.6.13 W6 节选 p.13 · 逻辑运算符

📄 来源：`Week 6 重点页.pptx`，物理页 13；本库主课件物理页：48。

AND 要两条件都成立，OR 至少一条件成立，NOT 取反。先给每行分别判条件，再组合；OR 不表示只能二选一。若条件中有 Null，要避免把未知一律当作 False 后再取反。

#### 改成 NOT 时，空值怎样处理

条件判断除了成立（True）与不成立（False），还可能是未知（Unknown）。Balance 为 Null 时，不知道它是否至少 50,000，因此 `Balance >= 50000` 的结果是 Unknown。

WHERE 只保留结果为 True 的行。NOT 会把 True 与 False 对调，但 `NOT Unknown` 仍为 Unknown；它不会因为“没有证据成立”就变成 True。

用上面同一个 Cash 表追踪，下面每行是一条原记录的判断。

| Account# | Balance | >= 50,000 | NOT (>= 50,000) |
|---|---:|---|---|
| BA-6 | Null | Unknown | Unknown |
| BA-7 | Null | Unknown | Unknown |
| BA-8 | 75,000 | True | False |
| BA-9 | 0 | False | True |

所以 `WHERE NOT (Balance >= 50000)` 只保留 BA-9。若想同时保留缺失余额，需明确加入 `OR Balance IS NULL`；“低于门槛”和“余额未知”仍是两类理由。

英文参考：WHERE retains only rows whose condition is true. NOT does not turn an unknown comparison into true, so only BA-9 is returned by NOT (Balance >= 50000).


#### 2.6.14 W6 节选 p.14 · BETWEEN

📄 来源：`Week 6 重点页.pptx`，物理页 14；本库主课件物理页：49。

BETWEEN 7/1 AND 7/31 包含两端日期，原表保留 S-1 到 S-5。7 月 31 日不能遗漏，8 月两行不保留。

实际 Access 日期常量需 #...#；这里按课件给定日期推结果，不把简写当通用可运行代码。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w06-s014.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 原日期范围题

课件给定 SQL：

```sql
Select Sale#, Amount, Date
From Sale
Where Date BETWEEN 7/1 and 7/31;
```

按原题日期语义保留 7 月 1 日至 7 月 31 日，两个端点都包含。完整输入在原图；S-6 与 S-7 的日期为 8 月，不满足。

| Sale# | Amount | Date |
|---|---:|---|
| S-1 | 7,200 | 1 July |
| S-2 | 10,000 | 21 July |
| S-3 | 16,000 | 22 July |
| S-4 | 10,000 | 26 July |
| S-5 | 16,600 | 31 July |

英文参考：Sales S-1 to S-5 are included. BETWEEN includes both endpoints, so the sale on 31 July remains.

实际 Access 需按真实年份写 `#7/1/yyyy#` 与 `#7/31/yyyy#` 等日期常量；原题未给年份，不补造某年。若字段含时分秒，末日午夜不自动覆盖该日全部时间，要另核边界。本题只给日期，不扩为时间戳题。

#### 2.6.15 W6 节选 p.15 · IS NULL

📄 来源：`Week 6 重点页.pptx`，物理页 15；本库主课件物理页：50。

IS NULL 检查缺失或未知的值。原表 BA-6、BA-7 的 Balance 为空，因此保留；BA-9 的 0 是已知数值，不属于 Null。不能用 = NULL 代替此判断。

英文参考：BA-6 and BA-7 are returned because their balances are null. BA-9 has a known zero balance and is not returned by IS NULL.

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w06-s015.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.6.16 W6 节选 p.16 · EXISTS 勘误

📄 来源：`Week 6 重点页.pptx`，物理页 16；本库主课件物理页：51。

课件把 Balance EXISTS 解释为非空，其展示结果是 BA-8 与 BA-9。

真正 Access SQL 检查非空应写 Balance IS NOT NULL；EXISTS 是判断子查询是否返回行的另一种操作。考试读到该页写法可说明课件意图，同时标出正确语法。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w06-s016.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 空值与零的同表比较

原页 SQL 为 `Select * From Cash Where Balance EXISTS;`，其用意是取非空余额；源图显示 BA-8 的 75,000 和 BA-9 的 0。正确可执行的非空条件是 `WHERE Balance IS NOT NULL`。

0 表示已知没有余额，Null 表示缺失或未知，两者不同。`EXISTS (subquery)` 则问子查询有没有记录，不能放在 Balance 后面替代非空谓词。这个纠正由 Microsoft 官方文档支持，见 §9.4。

英文参考：BA-8 and BA-9 have non-null balances. Zero is a known value, not a null value. In executable Access SQL, use IS NOT NULL for this test.

#### 2.6.17 W6 节选 p.17 · 汇总函数

📄 来源：`Week 6 重点页.pptx`，物理页 17；本库主课件物理页：52。

COUNT、AVG、SUM、MIN、MAX 分别汇总记录数、平均、合计、最小、最大。它们对整列多行汇总，区别于下一页逐行相乘。

老师从原 p.52 起排除后续计算要求，所以本页不安排计算训练；课件 AVERAGE 也不宜照抄作 Access SQL 函数名。

#### 2.6.18 W6 节选 p.18 · 逐行计算

📄 来源：`Week 6 重点页.pptx`，物理页 18；本库主课件物理页：53。

横向计算（Horizontal Calculation）在同一行把不同字段组合，例如数量乘单价；汇总则把多行放到一起。此页同属原 p.52 起排除范围，保留概念和旧正文入口即可。

### 2.8 Week 8 · 课堂范围与逐页解释

**🎙️ 课堂补充**（Week 8）：另参看 `01:21:38` 技术简答与 `01:22:52` 两优两缺。

> *"examples, including the basic idea, including the pro and cons for each"*（`01:20:07`）

#### 2.8.01 W8 节选 p.1 · AC6761 Artificial Intelligence Accounting

📄 来源：`Week 8 重点页.pptx`，物理页 1；本库主课件物理页：1。

章节封面。本次从四类机器学习进入，历史和 AI 与 ML/DL 的分类对比降权；关键技术自身的用途仍需会解释。

#### 2.8.02 W8 节选 p.2 · Types of machine learning

📄 来源：`Week 8 重点页.pptx`，物理页 2；本库主课件物理页：9。

四类按学习时能得到的反馈区分：监督有正确标签，无监督没有标签，半监督同时用少量标签与大量无标签，强化靠行动后的奖励。每类都准备基本意思、会计例子及优缺点。

#### 2.8.03 W8 节选 p.3 · Supervised learning

📄 来源：`Week 8 重点页.pptx`，物理页 3；本库主课件物理页：10。

监督学习（Supervised Learning）用已知正确答案的历史样本学习输入与输出的对应。原图中 Supervisor 提供期望类别；新样本再经模型预测。

发票文字和金额是输入，人工标的费用科目是标签。预测阶段不是再让老师把新样本答案先告诉模型。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w08-s003.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.8.04 W8 节选 p.4 · Supervised learning – Key characteristics

📄 来源：`Week 8 重点页.pptx`，物理页 4；本库主课件物理页：11。

有标签就能把预测与已知答案比较来评估，但收集标签要专家时间。未来数据若变了，历史学到的关系未必继续有效。监督方法是否易解释还取决于模型结构，不能说所有监督模型天然透明。

#### 2.8.05 W8 节选 p.5 · Supervised learning – Example

📄 来源：`Week 8 重点页.pptx`，物理页 5；本库主课件物理页：12。

课件原例把已由会计标过科目的历史发票用于训练，例如出租车归 Travel、Adobe 订阅归 Software/IT。模型根据供应商、描述、金额等建议新发票科目；建议仍需复核，尤其碰到混合用途发票时。

#### 2.8.06 W8 节选 p.6 · Supervised learning – Pros and Cons

📄 来源：`Week 8 重点页.pptx`，物理页 6；本库主课件物理页：13。

优点是任务目标清晰、可用正确标签检验；局限是标签成本与未来分布变化。解释时连接输入和后果：旧标签错会把错误分类规则教给模型，而非只写“accuracy/cost”两个词。

#### 2.8.07 W8 节选 p.7 · Unsupervised learning

📄 来源：`Week 8 重点页.pptx`，物理页 7；本库主课件物理页：14。

无监督学习（Unsupervised Learning）没有每条记录的正确类别，按相似性找结构或异常。原图把水果分组，分组名称由人解释；它不能仅凭分到异常组就认定存在舞弊。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w08-s007.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.8.08 W8 节选 p.8 · Unsupervised learning – Key characteristics

📄 来源：`Week 8 重点页.pptx`，物理页 8；本库主课件物理页：15。

没有标签或想探索未知模式时适用。输出可能是群组或异常分数，需要人检查其业务含义；不以“没有标签”推论无需任何验证。

#### 2.8.09 W8 节选 p.9 · Unsupervised learning – Example

📄 来源：`Week 8 重点页.pptx`，物理页 9；本库主课件物理页：16。

原例检查大量日记账的金额、科目组合、时间和操作者，标记偏离常态的记录。统计罕见只是进一步检查线索；合法的大额调整也可能罕见，所以人工追凭证不可省。

#### 2.8.10 W8 节选 p.10 · Unsupervised learning – Pros and Cons

📄 来源：`Week 8 重点页.pptx`，物理页 10；本库主课件物理页：17。

优点是无需先标完数据，并可能发现旧规则没想过的异常；局限是结果难客观评价、群组需解释。异常检测适合排查顺序，不能单独产生审计定罪结论。

#### 2.8.11 W8 节选 p.11 · Semi-supervised learning

📄 来源：`Week 8 重点页.pptx`，物理页 11；本库主课件物理页：18。

半监督学习（Semi-supervised Learning）让少量已标数据与大量未标数据共同参与学习。原图左侧给狗猫标签，右侧只有图片；只把未标图片存起来而训练完全不用，不叫半监督。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w08-s011.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.8.12 W8 节选 p.12 · Semi-supervised learning – Key characteristics

📄 来源：`Week 8 重点页.pptx`，物理页 12；本库主课件物理页：19。

专家标注贵时，可用有代表性的小批标签引导大量未标材料。省标注不等于无需优质标签；若少量标签只覆盖一种合同，模型对其余合同可能学偏。

#### 2.8.13 W8 节选 p.13 · Semi-supervised learning – Example

📄 来源：`Week 8 重点页.pptx`，物理页 13；本库主课件物理页：20。

原例让专家标一部分合同，模型同时利用其余未标合同，依据条款、当事人、付款条件等学习分类边界。识别合同类别可帮助复核，不自动代替法律或会计判断。

#### 2.8.14 W8 节选 p.14 · Semi-supervised learning – Pros and Cons

📄 来源：`Week 8 重点页.pptx`，物理页 14；本库主课件物理页：21。

优点是降低标注负担，可能优于只用那一小批标签；局限是样本代表性和错误传播。改条件：如果所有训练材料均已标注且未用无标签数据，方法应归监督而非半监督。

#### 2.8.15 W8 节选 p.15 · Reinforcement learning

📄 来源：`Week 8 重点页.pptx`，物理页 15；本库主课件物理页：22。

强化学习（Reinforcement Learning）中的行动者（Agent）根据环境观察选动作，再接收奖励或惩罚，调整以追求累计回报。

图中动作箭头指向环境，奖励和观察返回 Agent；不要把它与普通已标答案配对混淆。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w08-s015.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.8.16 W8 节选 p.16 · Reinforcement learning – Key characteristics

📄 来源：`Week 8 重点页.pptx`，物理页 16；本库主课件物理页：23。

适合多次决策会影响后续结果的任务，靠试错反馈学习。是否学得好取决于奖励是否代表真正目标；仅奖励速度可能让系统少检查最难的记录。

#### 2.8.17 W8 节选 p.17 · Reinforcement learning – Example

📄 来源：`Week 8 重点页.pptx`，物理页 17；本库主课件物理页：24。

原例把审计抽样策略视作 Agent，交易总体是 Environment，下一笔查哪项是 Action；发现错误、覆盖风险或单位时间有效发现量可作为 Reward 的设计。

它是应用构想，不表示本课已部署或证明真实收益。

#### 2.8.18 W8 节选 p.18 · Reinforcement learning – Pros and Cons

📄 来源：`Week 8 重点页.pptx`，物理页 18；本库主课件物理页：25。

优点是能随反馈改进连续决策；局限是奖励与环境难设计、数据和算力成本高、解释审计较难。它不保证找到全局最优，也不能靠真实财务系统中的无限试错来学习。

#### 2.8.19 W8 节选 p.19 · Applications of Machine learning

📄 来源：`Week 8 重点页.pptx`，物理页 19；本库主课件物理页：26。

推荐、语言处理、医学影像、识别追踪和异常检测是应用类别。考试举例把任务、输入和输出讲清即可；不需要背品牌。医疗和投资效果不在本笔记中外推为现实建议。

#### 2.8.20 W8 节选 p.20 · Predictions using machine learning

📄 来源：`Week 8 重点页.pptx`，物理页 20；本库主课件物理页：27。

本页用线性方程预测目标，属于老师明确排除的线性回归段。保留历史知识与 M08 完整例，不因文件叫“重点页”就安排回归公式计算。

#### 2.8.21 W8 节选 p.21 · Linear regression

📄 来源：`Week 8 重点页.pptx`，物理页 21；本库主课件物理页：28。

原图横轴是输入 X，纵轴是待预测 Y，斜线表达预测关系；点偏离线说明并非每个样本都完美符合。该图仍属被排除的回归段，仅保留辨图背景。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w08-s021.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.8.22 W8 节选 p.22 · The best-fit line

📄 来源：`Week 8 重点页.pptx`，物理页 22；本库主课件物理页：29。

最小二乘法选择使纵向误差平方和较小的线。它是本课已有的算法背景，本次不要求推导或算参数；不把“最好拟合”说成保证所有未来预测正确。

#### 2.8.23 W8 节选 p.23 · Least squared errors

📄 来源：`Week 8 重点页.pptx`，物理页 23；本库主课件物理页：30。

左图点都在直线上，右图用竖直虚线显示偏差；这是回归误差示意，不是按图读出新的真实数据集。本次明确排除，不倒造原始数值来算。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/final-review-20261125/w08-s023.png]]

原图保留整页标注；读图方法见本页解释。可在 Obsidian 点开大图核对小字。

#### 2.8.24 W8 节选 p.24 · AI in Daily Life in general

📄 来源：`Week 8 重点页.pptx`，物理页 24；本库主课件物理页：31。

本页列家庭与健康应用，作为背景。节能 12–15%、92% 等效果是课件声称，缺可追溯出处；不用作考试论证中的已证实统计数字。

#### 2.8.25 W8 节选 p.25 · AI in Daily Life in general

📄 来源：`Week 8 重点页.pptx`，物理页 25；本库主课件物理页：32。

推荐、交通导航和辅助驾驶说明 AI 用数据模式支持选择。列出的品牌效果数字没有逐项外核，不能当作现实服务的当前性能或安全保证。

#### 2.8.26 W8 节选 p.26 · AI in Business in particular

📄 来源：`Week 8 重点页.pptx`，物理页 26；本库主课件物理页：33。

客服自动处理与金融风控是业务应用方向。使用时要说明什么输入被处理、帮助什么判断；本页 85%、20% 等数字属于未外证课件声称，不背成事实。

#### 2.8.27 W8 节选 p.27 · AI in Business in particular

📄 来源：`Week 8 重点页.pptx`，物理页 27；本库主课件物理页：34。

零售预测、设备维护和质检体现不同任务：预测需求、识别故障征兆、从图片找瑕疵。品牌案例仍是导入，不因声称精度高就推出无需人工复核。

#### 2.8.28 W8 节选 p.28 · The application of AI in accounting

📄 来源：`Week 8 重点页.pptx`，物理页 28；本库主课件物理页：35。

会计应用包括录入自动化、异常识别、财务预测、合规与分析。可选一项说明“原始凭证或财报 → 处理 → 建议或警报 → 人工核验”，把用途落到实际信息流。

#### 2.8.29 W8 节选 p.29 · Key Technologies in AI Accounting

📄 来源：`Week 8 重点页.pptx`，物理页 29；本库主课件物理页：36。

所供课件列五项：深度学习、自然语言处理、生成式 AI、RPA、OCR。录音说选六项，与此不一致；先完整准备可核的五项，不擅自补第六项。每项会定义、用途和一个会计例子。

#### 五项技术的英文参考

以下均为笔记自拟，不是教师逐字答案。每个句子把技术与一个会计动作连起来。

- Deep learning uses multilayer neural networks to learn complex patterns, for example from invoice images. Its output still needs validation.
- NLP processes human language and can extract payment terms from contracts or summarise financial disclosures.
- Generative AI creates content in response to prompts and can draft an analysis using supplied financial statements. The draft must be checked against the source.
- RPA executes rules-based workflow steps, such as matching invoices to purchase orders and routing exceptions for review.
- OCR converts text in scanned invoices into machine-readable fields, reducing manual entry while requiring checks of amounts and currencies.

不要把 OCR 的“读出字”当作 NLP 的“解释条款”，也不要把 RPA 的规则执行当作必然训练了模型。

#### 2.8.30 W8 节选 p.30 · Deep Learning

📄 来源：`Week 8 重点页.pptx`，物理页 30；本库主课件物理页：37。

深度学习（Deep Learning）用多层神经网络学习复杂数据表示，可处理发票图像或文字。这里需要会说明用途，不重讲网络训练数学。课件说持续优于前代是泛化表述，实际表现仍受任务、数据与验证影响。

#### 2.8.31 W8 节选 p.31 · Natural Language Processing

📄 来源：`Week 8 重点页.pptx`，物理页 31；本库主课件物理页：38。

自然语言处理（Natural Language Processing，NLP）让系统处理人类语言，例如从合同提取付款条款、从财报归纳风险。

它不仅“看单词”，也可能读文本中的数字；提取结果仍要回到原文核对。

#### 2.8.32 W8 节选 p.32 · Generative AI

📄 来源：`Week 8 重点页.pptx`，物理页 32；本库主课件物理页：39。

生成式 AI（Generative AI）根据提示生成新的文字或其他内容，例如依据所给报表草拟分析。能写得流畅不等于证据真实；不能把生成的报表数字代替原始年报。

#### 2.8.33 W8 节选 p.33 · Robotic Process Automation

📄 来源：`Week 8 重点页.pptx`，物理页 33；本库主课件物理页：40。

机器人流程自动化（Robotic Process Automation，RPA）按预设规则执行重复操作，例如比对发票与采购单后转入审批。

RPA 本身可不包含机器学习，遇异常转人工；和 ML 结合才可能增加识别能力。

#### 2.8.34 W8 节选 p.34 · Optical Character Recognition

📄 来源：`Week 8 重点页.pptx`，物理页 34；本库主课件物理页：41。

光学字符识别（Optical Character Recognition，OCR）把扫描件里的文字转换成可读取字段。

发票图片中的“金额”被提成文本或数字后，仍需核对小数点和币种；OCR 不等于已经判断发票业务合法。

#### 2.8.35 W8 节选 p.35 · Advantages of AI in accounting

📄 来源：`Week 8 重点页.pptx`，物理页 35；本库主课件物理页：44。

准备至少两个优点并给过程。自动化减少重复录入，释放核验和分析时间；及时整理数据可支持较快发现异常。课件的准确性与安全性是潜在收益，不是每个系统必然达到的保证。

#### 2.8.36 W8 节选 p.36 · Disadvantages of AI in accounting

📄 来源：`Week 8 重点页.pptx`，物理页 36；本库主课件物理页：45。

准备至少两个缺点并给后果。培训和迁移会耗时花钱；过度相信自动建议会把错误分类传进账簿。把风险对应控制，例如异常单人工复核，不能只写“high cost/errors”。

### 2.9 Week 9 · 课堂范围与逐页解释

**🎙️ 课堂补充**（Week 9）：另参看 `01:24:55` 至少五类、`01:26:26` 每类两项、`01:25:48` Prompt 明确指导、`01:27:15` 幻觉缓解。

> *"any out of the eleven stakeholders will be counted"*（`01:25:28`）

#### 2.9.01 W9 节选 p.1 · AC6761 Artificial Intelligence Accounting

📄 来源：`Week 9 重点页.pptx`，物理页 1；本库主课件物理页：1。

章节封面。本次重点是利益相关者需求与 Prompt 设计，以及幻觉定义、例子、影响和缓解；会计师事务所品牌介绍降权。

#### 2.9.02 W9 节选 p.2 · Use of AI in stakeholders

📄 来源：`Week 9 重点页.pptx`，物理页 2；本库主课件物理页：15。

本页五类角色分别关注投资回报、偿债、供货赊账风险、分析建议及审计可靠性。先选角色的决定，再设计问题；不能把同一句泛泛分析分别贴给五个角色。

#### 2.9.03 W9 节选 p.3 · Use of AI in stakeholders

📄 来源：`Week 9 重点页.pptx`，物理页 3；本库主课件物理页：16。

管理层要改善经营与配置资源；员工关注工作、薪酬与稳定；长期客户关心持续供货或服务。各自可以读同一报表，但提问目标不同。

#### 2.9.04 W9 节选 p.4 · Financial statement analyses - stakeholders

📄 来源：`Week 9 重点页.pptx`，物理页 4；本库主课件物理页：17。

监管者关心披露与合规，竞争者关心可比表现及策略，社区关心企业持续经营对本地和环境的影响。十一类中至少准备五类，合理选择即可，不限于老师详讲的那五类。

#### 2.9.05 W9 节选 p.5 · The perspective of investors

📄 来源：`Week 9 重点页.pptx`，物理页 5；本库主课件物理页：18。

投资者可从核心经营、地区敞口、外部风险、创新、治理及风险评价中选两项。题目要 Prompt 就补公司、资料、期间、任务和输出；题目只要 Question 才可以用一个简洁问题。

#### 2.9.06 W9 节选 p.6 · 老师明确可能考Prompt设计

📄 来源：`Week 9 重点页.pptx`，物理页 6；本库主课件物理页：新增总结页，无主课件对应页。

这是提供者新增的中文复习提示页，只有“Stakeholder Prompt 设计模板”标题，没有模板正文。它不是教师原课件页，不能据此补造教师模板；本笔记的完整英文示例明确为自拟。

#### 先分 Question 与 Prompt

Question 可以是：Can the company repay its debt on time? 这只问一个问题。Prompt 应给工具足够明确的任务边界，例如谁作决定、用哪份材料、比较哪些期间、查哪些证据、输出什么。

下面五类每类给两个关切，并给一条较完整的英文 Prompt。公司、2023–2025 和所给年报是笔记示范条件，考试时按题面替换；不能把这些条件写成教师规定模板。

**投资者（Investors）**：关心盈利能否持续，以及增长与风险是否匹配。

英文 Prompt：Act as an investor. Using only the supplied 2023–2025 annual reports, assess whether profit growth is supported by the core business and identify major growth risks. Distinguish recurring earnings from one-off items, cite the figures and report pages, and flag missing evidence. Do not invent data.

**债权人（Creditors）**：关心近期现金能否还债，以及长期债务负担。

英文 Prompt：Act as a lender. Using the supplied financial statements, examine operating cash flow, near-term debt repayments and longer-term obligations. Explain the main repayment risks using the relevant periods and evidence. Present missing information separately from your conclusions.

**供应商（Suppliers）**：关心赊账后能否按时收款，以及长期合作是否稳定。

英文 Prompt：Act as a supplier considering trade credit. Review the supplied reports for payment capacity and financial stability. Identify warning signs that could delay payment and explain what additional evidence is needed before setting a credit limit. Cite the supporting information.

**审计师（Auditors）**：关心报表是否存在重大错报风险，以及哪些异常需要追证据。

英文 Prompt：Act as an auditor planning risk assessment. From the supplied statements and notes, identify unusual movements in revenue and receivables. Explain why each movement may require further evidence and suggest relevant verification work. Do not treat an anomaly as proof of fraud.

**监管者（Regulators）**：关心披露是否符合题面指定要求，以及遗漏是否影响使用者。

英文 Prompt：Act as a regulator reviewing the supplied disclosures. Compare them with the reporting requirements provided in the question. Identify possible omissions and inconsistencies, cite the relevant passages, and separate confirmed findings from matters requiring clarification. Do not invent legal requirements.

改条件：题目若指定员工，就围绕薪酬、就业稳定及企业持续经营；不能原样抄投资者的股利问题。教师不限定必须使用其详讲的五类，合理关联需求更重要。

#### 2.9.07 W9 节选 p.7 · AI hallucination - definition

📄 来源：`Week 9 重点页.pptx`，物理页 7；本库主课件物理页：33。

AI 幻觉（Hallucination）指生成没有事实支持、错误或虚构的内容。模型生成合适的语言序列，不等于逐句验证了现实；数据错误只是诱因之一，不能把所有幻觉都解释成训练数据有错。

#### 2.9.08 W9 节选 p.8 · AI hallucination - examples

📄 来源：`Week 9 重点页.pptx`，物理页 8；本库主课件物理页：34。

会计例子包括编造不存在的审计发现、财务数字或引用。检查点是能否追到所给原始材料；“自信、专业、有引用格式”都不能替代真实性。

#### 2.9.09 W9 节选 p.9 · AI hallucination - impact

📄 来源：`Week 9 重点页.pptx`，物理页 9；本库主课件物理页：35。

把虚构利润放进报告会改变分析与决策，也会损害使用者信任。回答影响时交代错误怎样从输出传到财务结论，不只列“trust/financial risk”。

#### 2.9.10 W9 节选 p.10 · AI hallucination - mitigation

📄 来源：`Week 9 重点页.pptx`，物理页 10；本库主课件物理页：36。

缓解按三个层次：把数字和引文对回权威原件；让专业人员复核关键判断；改善数据和模型评估。提示“不要编造”有帮助但不能保证零幻觉，资料缺失应明确报缺。

### 2.10 Week 10 · 课堂范围与逐页解释

**🎙️ 课堂补充**（Week 10）：另参看 `01:27:58` Value Chain 未讲、`01:29:35` 不要求列全五力、`01:29:55` Ratio 补充不手算。

> *"So I hope you can at least be familiar with the three to four types of the analytical models."*（`01:28:06`）

#### 2.10.01 W10 节选 p.1 · AC6761 Artificial Intelligence Accounting

📄 来源：`Week 10 重点页pptx.pptx`，物理页 1；本库主课件物理页：1。

章节封面。重点转向为分析模型设计有具体对象与目的的问题或 Prompt，不要求手算 Ratio 补充讲义。

#### 2.10.02 W10 节选 p.2 · Financial statement analyses – analytical models

📄 来源：`Week 10 重点页pptx.pptx`，物理页 2；本库主课件物理页：2。

本页共列九个名称；老师说 Value Chain 没介绍，其余八个中至少熟悉三至四个。可先选比率、趋势、情景与五力，但给定其他模型时仍需有识别入口。

问题应对应模型的一个真实分析内容，不能只写“analyze the company”。

#### 八个模型怎样提出相关问题

已讲八个的任务不同。先重点准备下面四个；后四个保留识别入口，不把“准备四个”误当作卷上一定任选四个。

**Ratio Analysis（比率分析）**：关心某方面表现，例如流动性，也就是用近期可用资源应对近期义务的能力。

英文 Prompt：Using the supplied balance sheets, compare liquidity across 2023–2025. Ask whether current assets can support current obligations, identify which asset components drive the change, and explain limits caused by slow-moving inventory or missing data. Use the relevant figures and cite their source.

**Trend Analysis（趋势分析）**：关心同一指标随时间怎样变。

英文 Prompt：Using the supplied 2023–2025 statements, examine the trends in revenue, operating profit and operating cash flow. Identify whether cash generation keeps pace with reported growth and discuss possible reasons for divergence. Cite comparable periods and flag changes in reporting scope.

**Scenario Analysis（情景分析）**：明确改变某个条件，检查影响和假设。

英文 Prompt：Using the supplied baseline, assess how a fall in sales volume could affect profit and cash needs. State which cost assumptions change, distinguish fixed from variable costs, and identify the information required before quantifying the scenario. Do not invent input values.

**Porter’s Five Forces（波特五力）**：问题对应竞争力量之一即可，不要求把五力全部默写。

英文 Prompt：Using the supplied company and industry information, assess supplier bargaining power. Explain whether supplier concentration or switching costs could pressure input costs and margins. Cite the evidence and identify missing information rather than assuming the firm can pass all costs to customers.

其余四个可用这些问题检验是否切题：

- DuPont：Which components of profitability, asset use and financial leverage explain changes in return on equity? 中文看利润率、资产使用和融资杠杆各影响什么，不必本次手算。
- SWOT：Which reported capabilities support the firm's strengths, and which external changes create threats? 中文区分企业内部能力与外部环境。
- Z-score：What additional model inputs and an appropriate model version are needed before evaluating financial distress? 中文先问资料和模型是否适用，不能只抄一个分数宣布会破产。
- Financial Statement Forecasting：Which assumptions link future sales to expenses, working capital and cash needs? 中文让预测假设与报表项目相互对得上，不凭空生成未来实际值。

这些是笔记自拟问题，未运行 AI 工具或生成真实预测。老师要求问题具体且与模型相关；只写“Please analyse trends for me”可能只能得到很有限分数。

#### 2.10.03 W10 节选 p.3 · 复习要求

📄 来源：`Week 10 重点页pptx.pptx`，物理页 3；本库主课件物理页：新增总结页，无主课件对应页。

这是提供者新增的中文“复习要求”页，概括三至四个模型、问题/Prompt 及不必解释模型或列全五力。录音可独立支持这些要点；该页本身仍是摘要，不是官方题面或逐字原话。

### 2.11 Week 11 · 课堂范围与逐页解释

**🎙️ 课堂补充**（Week 11）：三页编号见 `01:31:15`；其余忽略见 `01:31:26`。BBT 是 PPT 的 ASR 错词，按课件原件定位。

> *"So these three pages in today's BBT are important"*（`01:31:21`）

#### 2.11.01 W11 节选 p.1 · AC6761 Artificial Intelligence Accounting

📄 来源：`Week 11 重点页.pptx`，物理页 1；本库主课件物理页：1。

章节封面。老师这次只保留原 p.27–29 的偏见与公平，不把预测实作、其他伦理题或未来趋势全部当作期末必背。

#### 2.11.02 W11 节选 p.2 · Bias and fairness - concept

📄 来源：`Week 11 重点页.pptx`，物理页 2；本库主课件物理页：27。

偏见（Bias）可来自不具代表性的训练数据，使不同群体得到系统性不利或较不准确结果。公平（Fairness）问这种差异是否合理且可接受；一次随机出错与持续对某组不利不是同一问题。

#### 2.11.03 W11 节选 p.3 · Bias and fairness - Impact

📄 来源：`Week 11 重点页.pptx`，物理页 3；本库主课件物理页：28。

贷款、招聘或审计资源分配若依赖偏差模型，可能使某组更难得到机会或被不合理多查，进而破坏信任。案例须说清谁受什么影响，不只写“discrimination”。

#### 2.11.04 W11 节选 p.4 · Bias and fairness – Strategies for mitigation

📄 来源：`Week 11 重点页.pptx`，物理页 4；本库主课件物理页：29。

缓解要对原因施策：补足有代表性的数据；分组检查错误与公平指标；让多样化团队参与评估和人工复核。整体平均表现好不能证明每组都公平；控制要持续复查而非做一次就结束。

#### 偏见例子的完整答题链

笔记补充：贷款模型的训练样本主要来自某类借款人，对其他群体数据不足。若模型据此系统性高估其他群体风险，可能不合理拒贷，损害机会与信任。

控制要对着原因：增加有代表性且质量合格的数据；分别评估各组错误；由合适人员复核重大拒贷和申诉，并持续监测变化。不能因为整体平均准确率高就停止分组检查，也不能虚构本例真实实验结果。

英文参考：Unrepresentative training data can cause systematic errors for under-represented groups. In lending, this may lead to unfair rejection and loss of trust. Mitigation includes representative data, group-specific evaluation and human review of consequential decisions.

改条件：若各组数据充分但奖励目标鼓励单纯压低成本，仍可能产生不公平；补数据不是唯一控制。


## 3. 一图看懂 · 题型如何选择准备方法

先按题目要求辨认操作，再回到对应正文；这张表是导航，不代替逐页解释。

| 看到的任务 | 真正要交的结果 | 回到正文 |
|---|---|---|
| Explain／Discuss | 名称＋意思＋具体例子或后果 | W1、W4、W8、W11 |
| Common-size | 统一分母后的百分比＋一两个变化解释 | W3 |
| Complete the pattern | 图中框与关联，站稳企业视角 | W5 |
| Show query results | 符合条件的记录＋指定输出列 | W6 |
| Design a prompt | 角色／任务、材料、期间、具体分析及输出 | W9、W10 |

## 4. 考前速查

数字是老师提出的准备量，不是本笔记猜的试卷题数。

| 项目 | 需要准备到的程度 |
|---|---|
| Assumptions | 至少 3/4，解释和举例 |
| Constraints | Cost-benefit、Materiality 两项 |
| Statements | Balance Sheet 是时点、Income Statement 是期间 |
| Common-size | 资产负债表除总资产、利润表除当年收入 |
| REA | 至少两优两缺、采购／销售、三种核心关联 |
| [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.5.12 W5 节选 p.12 · 扩展关联\|Expanded REA]] | Proposition 推介、Reservation 为未来交换保留资源 |
| Database | Entity Integrity、Referential Integrity、One Fact, One Place |
| [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.04 W6 节选 p.4 · SQL 基本结构\|SQL]] | FROM 找表，WHERE 筛行，SELECT 按要求输出列、BETWEEN 包含两端 |
| ML | 四种学习各会意思、会计例子及利弊 |
| Key technologies | 可核五项全部准备、“六项”不补造 |
| AI benefits／costs | 至少两个优点与两个缺点，并说明理由 |
| [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.9.06 W9 节选 p.6 · 老师明确可能考Prompt设计\|Stakeholders]] | 至少五类，每类至少两项关切、不限指定五类 |
| [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.10.02 W10 节选 p.2 · Financial statement analyses – analytical models\|Analytical models]] | 已讲八个，至少熟悉三至四个，能提出具体相关问题 |
| Hallucination／Bias | 分别会定义、例子、影响与缓解，不混成同一现象 |

## 5. 双语术语卡

下面英文是笔记自拟应试表述；教师原话另在课堂证据块引用。

| 中文 | English | 可用的英文解释 |
|---|---|---|
| 持续经营 | Going Concern | The business is assumed to continue operating rather than to liquidate. |
| 主体假设 | Business Entity | Business records are kept separate from the owner's personal affairs. |
| 重要性 | Materiality | Information is material if omitting or misstating it could affect users' decisions. |
| 共同比分析 | Common-size Analysis | Each item is expressed as a percentage of a common base. |
| 交换关系 | Duality | It links the give and get economic events of an exchange. |
| 资源流 | Stockflow | It links an economic event to the resource affected. |
| 参与关系 | Participation | It links an event to an internal or external agent. |
| 推介关联 | Proposition | It links an instigation event to the resource being proposed. |
| 预留关联 | Reservation | It links a commitment event to a resource or resource type reserved for the exchange. |
| 参照完整性 | Referential Integrity | A non-null foreign key must match a referenced key value. |
| 幻觉 | Hallucination | The model generates incorrect or unsupported content. |
| 偏见 | Bias | Systematic differences can disadvantage some groups. |

## 6. 考点证据与答题方式

### 6.1 本次来源层级

🔴 表示录音的 ASR 与所供英文转写支持老师明确提出范围、数量或形式。它不表示已取得试卷，更不表示本次原音逐字人工听校。题面未给出的题数、分值、选答和允许材料仍未知。

重点页中的高亮与中文提示只记作“所供总结”。自拟例题、数字演算和英文答句都标笔记补充；不能把它们变成教师给定答案。

### 6.2 最后课考试明示

以下三条是高风险边界的原话样本，全部其他要求仍须结合 §0 与逐周证据；不是只有这三条才有课堂依据。

| 级别 | 原话与原时钟 | 如何准备 |
|---|---|---|
| 🔴 范围 | *"We ignore the chapter 2 and go to the chapter 3."*（`00:59:10`） | W2 本次排除 |
| 🔴 题型 | *"Show me the query results here."*（`01:16:36`） | 根据表和 SQL 写结果 |
| 🔴 数量 | *"So I hope you can at least be familiar with the three to four types of the analytical models."*（`01:28:06`） | 准备 3–4 个模型的相关问题 |

### 6.3 高分题不要只交关键词

**🎙️ 课堂补充**（`01:31:43`–`01:32:20`）：老师让学生按分值分配时间和解释深度。

> *"So you try to allocate your time and effort based on the allocated points"*（`01:32:14`）

可用作答顺序是：先直接回应题目，再解释它怎样工作，再给一个与题目情境相连的例子。大题若只列五个关键词，阅卷者看不到你是否理解对象和因果。这个结构是笔记建议，不是额外评分 rubric。

例如问 RPA 的作用，不能只写“automation, efficiency”。应写：系统按规则匹配供应商发票和采购单，将不匹配项目转人工，因而减少重复核对，同时保留异常处理。

## 7. 自测 · 自编参考题

以下为笔记自编，没有冒充教师 mock 或留存试卷。先独立作答，再展开答案。

### 7.1 规则判断

老板用公司账户支付个人旅游费用，为什么不能直接当作公司的日常营业费用？再说出另一项会计假设及一个例子。

<details><summary>参考答案</summary>

主体假设把企业与业主分开，个人旅游没有因此变成公司经营费用。它可能需要作为业主往来或权益相关事项另按事实处理，本题没有足够条件指定唯一分录。

另一例：持续经营假设让仍将营运的企业按持续使用资源的情境编报，而非假设下周全部清算。

英文参考：The business entity assumption separates business transactions from the owner's personal affairs. A personal holiday should not automatically be recorded as an operating expense of the business.

</details>

### 7.2 共同比与变化

笔记补充数据：两年收入分别为 200、250，净利润均为 20，单位相同。净利率怎样变？能否说“收入占比下降”？

<details><summary>参考答案</summary>

净利率是 10% 和 8%，下降 2 个百分点。收入增加而净利润没增加，所以每一元收入留下的利润变少。共同比利润表中收入自己每年都是 100%，不能说其占比下降。

英文参考：The net profit margin fell from 10% to 8%, a decrease of 2 percentage points. Revenue remains 100% in each common-size income statement.

</details>

### 7.3 REA 改场景

企业先向客户介绍商品，客户签订单后企业预留商品，一周后才交货收款。哪一步是 Proposition，哪一步是 Reservation？签订单等于库存已经流出吗？

<details><summary>参考答案</summary>

介绍商品的发起事件与商品相连，是 Proposition；订单承诺与预留商品相连，是 Reservation。签订单是未来交换的承诺，不等于已经交货。实际销售交付才使本例中的商品流出。

英文参考：Proposition links the sales call to the products introduced. Reservation links the sales order to the inventory reserved. The commitment does not itself establish that the goods have already been delivered.

</details>

### 7.4 SQL 改条件

对正文原 Sale 表，若条件改为 `SalesRep# <> 'E-10' AND Amount >= 10000`，输出 `Sale#` 和 `Amount`，剩哪些？

<details><summary>参考答案</summary>

非 E-10 的记录为 S-1（7,200）和 S-7（23,000），再要求金额至少 10,000，只剩 S-7、23,000。先分别判两个条件，再取交集；>= 包括刚好等于门槛。

英文参考：Only sale S-7 remains, with an amount of 23,000, because it meets both conditions.

</details>

### 7.5 学习类别与 AI 风险

专家标注少量合同，模型同时利用其余未标合同学习分类，属于哪类？若 AI 为某合同编造不存在的条款，属于幻觉还是仅仅偏见？

<details><summary>参考答案</summary>

属于半监督学习，因为训练同时利用了两种数据。编造条款首先是幻觉；只有还存在系统性地对某些群体不利的差异，才有额外依据讨论偏见。核验应回原合同，不能用另一段流畅生成文字证明条款存在。

英文参考：This is semi-supervised learning. A fabricated clause is a hallucination and should be checked against the original contract.

</details>

### 7.6 Prompt 是否切题

题目指定“债权人＋趋势分析”。`Please analyse the company.` 缺什么？请写一个具体英文 Prompt。

<details><summary>参考答案</summary>

缺债权人的偿付关切、资料与期间、具体趋势及输出。可写：Act as a lender. Using only the supplied 2023–2025 financial statements, examine the trends in operating cash flow and debt repayments. Explain whether repayment capacity is improving, cite the supporting figures and pages, and flag missing information. Do not invent data.

这是自拟示例，不保证教师给定题会采用同一公司、期间或格式。

</details>

## 8. 重点页与正文精确映射

每个节选物理页一行。W 表示源 PPT 的 Week；“原页”指本库同周主课件的物理幻灯片序号；中文新增总结页不伪造原课件页号。

| 节选物理页 | 主课件物理页 | 正文精确入口 | 课堂覆盖 | 原图／处置 |
|---|---|---|---|---|
| W1／1 | 33 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.1.01 W1 节选 p.1 · Accounting Principles\|Accounting Principles]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W1／2 | 34 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.1.02 W1 节选 p.2 · Accounting Assumptions\|Accounting Assumptions]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W1／3 | 36 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.1.03 W1 节选 p.3 · Accounting Constraint\|Accounting Constraint]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W1／4 | 51 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.1.04 W1 节选 p.4 · Transaction Analysis\|Transaction Analysis]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W1／5 | 52 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.1.05 W1 节选 p.5 · Transaction Analysis-Rules\|Transaction Analysis-Rules]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W1／6 | 53 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.1.06 W1 节选 p.6 · Transaction Analysis-Exercises\|Transaction Analysis-Exercises]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W1／7 | 54 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.1.07 W1 节选 p.7 · Transaction Analysis-Exercises\|Transaction Analysis-Exercises]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／1 | 3 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.01 W3 节选 p.1 · Balance Sheet(Statement of financial position)\|Balance Sheet(Statement of financ…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／2 | 4 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.02 W3 节选 p.2 · Snapshot of financial position on a given day\|Snapshot of financial position on…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／3 | 5 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.03 W3 节选 p.3 · Balance Sheet\|Balance Sheet]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／4 | 6 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.04 W3 节选 p.4 · Non-Current Assets\|Non-Current Assets]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／5 | 7 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.05 W3 节选 p.5 · Intangibles\|Intangibles]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／6 | 8 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.06 W3 节选 p.6 · Current Assets\|Current Assets]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／7 | 9 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.07 W3 节选 p.7 · Accounts Receivables\|Accounts Receivables]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／8 | 10 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.08 W3 节选 p.8 · Current Liabilities\|Current Liabilities]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／9 | 13 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.09 W3 节选 p.9 · Key information:\|Key information:]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／10 | 16 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.10 W3 节选 p.10 · Common-size analysis converts financial statement line items into percentages of either total sales (for income statement) or total assets (for balance sheet).\|Common-size analysis converts fin…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／11 | 17 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.11 W3 节选 p.11 · Common-Size Balance Sheet\|Common-Size Balance Sheet]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／12 | 18 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.12 W3 节选 p.12 · Common-Size Balance Sheet\|Common-Size Balance Sheet]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／13 | 22 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.13 W3 节选 p.13 · Nike: Balance Sheet (Assets)\|Nike: Balance Sheet (Assets)]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W3／14 | 23 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.14 W3 节选 p.14 · Nike: Common-Size Balance Sheet (Assets)\|Nike: Common-Size Balance Sheet (…]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W3／15 | 24 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.15 W3 节选 p.15 · Nike: Common-Size Balance Sheet (Liabilities and Shareholders’ Equity)\|Nike: Common-Size Balance Sheet (…]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W3／16 | 25 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.16 W3 节选 p.16 · Nike:  Excerpts from Notes\|Nike:  Excerpts from Notes]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／17 | 26 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.17 W3 节选 p.17 · Nike: Analyzing Balance Sheet\|Nike: Analyzing Balance Sheet]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／18 | 27 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.18 W3 节选 p.18 · Nike: Analyzing Balance Sheet\|Nike: Analyzing Balance Sheet]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／19 | 28 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.19 W3 节选 p.19 · Income Statement\|Income Statement]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／20 | 29 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.20 W3 节选 p.20 · Shows financial performance over a given period\|Shows financial performance over …]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／21 | 30 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.21 W3 节选 p.21 · Income Statement\|Income Statement]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／22 | 31 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.22 W3 节选 p.22 · Revenues\|Revenues]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／23 | 32 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.23 W3 节选 p.23 · Expenses\|Expenses]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／24 | 33 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.24 W3 节选 p.24 · Income Statement\|Income Statement]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W3／25 | 36 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.25 W3 节选 p.25 · Nike: Income Statement\|Nike: Income Statement]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W3／26 | 37 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.3.26 W3 节选 p.26 · Nike: Common-Size Income Statement\|Nike: Common-Size Income Statement]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W4／1 | 1 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.01 W4 节选 p.1 · AC6761 Artificial Intelligence Accounting\|AC6761 Artificial Intelligence Ac…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W4／2 | 2 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.02 W4 节选 p.2 · Traditional Double-Entry Bookkeeping\|Traditional Double-Entry Bookkeep…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W4／3 | 3 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.03 W4 节选 p.3 · Strengths and limitations\|Strengths and limitations]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W4／4 | 4 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.04 W4 节选 p.4 · REA Accounting Model: A Paradigm Shift\|REA Accounting Model: A Paradigm …]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W4／5 | 5 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.05 W4 节选 p.5 · Strengths and limitations\|Strengths and limitations]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W4／6 | 17 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.06 W4 节选 p.6 · REA 基本框架\|REA 基本框架]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W4／7 | 18 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.07 W4 节选 p.7 · Duality\|Duality]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W4／8 | 19 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.08 W4 节选 p.8 · 销售与收款\|销售与收款]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W4／9 | 36 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.09 W4 节选 p.9 · 关系数据库\|关系数据库]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W4／10 | 37 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.10 W4 节选 p.10 · 表、行与列\|表、行与列]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W4／11 | 38 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.11 W4 节选 p.11 · 外键例子\|外键例子]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W4／12 | 39 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.12 W4 节选 p.12 · 关系表三原则\|关系表三原则]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W4／13 | 40 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.13 W4 节选 p.13 · 参照完整性例子\|参照完整性例子]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W4／14 | 41 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.14 W4 节选 p.14 · 一事多处\|一事多处]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W4／15 | 42 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.4.15 W4 节选 p.15 · 一格多值\|一格多值]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W5／1 | 1 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.5.01 W5 节选 p.1 · AC6761 Artificial Intelligence Accounting\|AC6761 Artificial Intelligence Ac…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W5／2 | 2 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.5.02 W5 节选 p.2 · 核心类\|核心类]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W5／3 | 9 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.5.03 W5 节选 p.3 · Core REA Modeling of Acquisition\|Core REA Modeling of Acquisition]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W5／4 | 10 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.5.04 W5 节选 p.4 · Core REA Modeling of Acquisition\|Core REA Modeling of Acquisition]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W5／5 | 11 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.5.05 W5 节选 p.5 · 采购核心图\|采购核心图]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W5／6 | 21 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.5.06 W5 节选 p.6 · Revenue Core Pattern\|Revenue Core Pattern]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W5／7 | 22 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.5.07 W5 节选 p.7 · 扩展模型\|扩展模型]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W5／8 | 23 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.5.08 W5 节选 p.8 · 发起与承诺事件\|发起与承诺事件]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W5／9 | 24 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.5.09 W5 节选 p.9 · 扩展事件高亮\|扩展事件高亮]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W5／10 | 25 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.5.10 W5 节选 p.10 · 冲回事件\|冲回事件]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W5／11 | 26 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.5.11 W5 节选 p.11 · 冲回事件高亮\|冲回事件高亮]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W5／12 | 27 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.5.12 W5 节选 p.12 · 扩展关联\|扩展关联]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W6／1 | 1 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.01 W6 节选 p.1 · AC6761 Artificial Intelligence Accounting\|AC6761 Artificial Intelligence Ac…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W6／2 | 19 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.02 W6 节选 p.2 · Link between tables\|Link between tables]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W6／3 | 20 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.03 W6 节选 p.3 · Access 表关联界面\|Access 表关联界面]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W6／4 | 39 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.04 W6 节选 p.4 · SQL 基本结构\|SQL 基本结构]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W6／5 | 40 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.05 W6 节选 p.5 · SQL 与关系代数\|SQL 与关系代数]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W6／6 | 41 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.06 W6 节选 p.6 · SQL 筛客户收款\|SQL 筛客户收款]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W6／7 | 42 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.07 W6 节选 p.7 · SQL 选择列\|SQL 选择列]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W6／8 | 43 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.08 W6 节选 p.8 · 内连接\|内连接]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W6／9 | 44 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.09 W6 节选 p.9 · 外连接\|外连接]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W6／10 | 45 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.10 W6 节选 p.10 · 比较运算符\|比较运算符]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W6／11 | 46 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.11 W6 节选 p.11 · 金额比较\|金额比较]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W6／12 | 47 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.12 W6 节选 p.12 · 文本比较\|文本比较]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W6／13 | 48 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.13 W6 节选 p.13 · 逻辑运算符\|逻辑运算符]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W6／14 | 49 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.14 W6 节选 p.14 · BETWEEN\|BETWEEN]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W6／15 | 50 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.15 W6 节选 p.15 · IS NULL\|IS NULL]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W6／16 | 51 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.16 W6 节选 p.16 · EXISTS 勘误\|EXISTS 勘误]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W6／17 | 52 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.17 W6 节选 p.17 · 汇总函数\|汇总函数]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W6／18 | 53 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.6.18 W6 节选 p.18 · 逐行计算\|逐行计算]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／1 | 1 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.01 W8 节选 p.1 · AC6761 Artificial Intelligence Accounting\|AC6761 Artificial Intelligence Ac…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／2 | 9 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.02 W8 节选 p.2 · Types of machine learning\|Types of machine learning]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／3 | 10 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.03 W8 节选 p.3 · Supervised learning\|Supervised learning]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W8／4 | 11 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.04 W8 节选 p.4 · Supervised learning – Key characteristics\|Supervised learning – Key charact…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／5 | 12 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.05 W8 节选 p.5 · Supervised learning – Example\|Supervised learning – Example]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／6 | 13 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.06 W8 节选 p.6 · Supervised learning – Pros and Cons\|Supervised learning – Pros and Cons]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／7 | 14 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.07 W8 节选 p.7 · Unsupervised learning\|Unsupervised learning]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W8／8 | 15 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.08 W8 节选 p.8 · Unsupervised learning – Key characteristics\|Unsupervised learning – Key chara…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／9 | 16 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.09 W8 节选 p.9 · Unsupervised learning – Example\|Unsupervised learning – Example]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／10 | 17 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.10 W8 节选 p.10 · Unsupervised learning – Pros and Cons\|Unsupervised learning – Pros and …]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／11 | 18 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.11 W8 节选 p.11 · Semi-supervised learning\|Semi-supervised learning]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W8／12 | 19 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.12 W8 节选 p.12 · Semi-supervised learning – Key characteristics\|Semi-supervised learning – Key ch…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／13 | 20 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.13 W8 节选 p.13 · Semi-supervised learning – Example\|Semi-supervised learning – Example]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／14 | 21 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.14 W8 节选 p.14 · Semi-supervised learning – Pros and Cons\|Semi-supervised learning – Pros a…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／15 | 22 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.15 W8 节选 p.15 · Reinforcement learning\|Reinforcement learning]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W8／16 | 23 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.16 W8 节选 p.16 · Reinforcement learning – Key characteristics\|Reinforcement learning – Key char…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／17 | 24 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.17 W8 节选 p.17 · Reinforcement learning – Example\|Reinforcement learning – Example]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／18 | 25 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.18 W8 节选 p.18 · Reinforcement learning – Pros and Cons\|Reinforcement learning – Pros and…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／19 | 26 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.19 W8 节选 p.19 · Applications of Machine learning\|Applications of Machine learning]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／20 | 27 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.20 W8 节选 p.20 · Predictions using machine learning\|Predictions using machine learning]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／21 | 28 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.21 W8 节选 p.21 · Linear regression\|Linear regression]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W8／22 | 29 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.22 W8 节选 p.22 · The best-fit line\|The best-fit line]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／23 | 30 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.23 W8 节选 p.23 · Least squared errors\|Least squared errors]] | 本次范围复盘，逐页停留未确认 | 原图及读法 |
| W8／24 | 31 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.24 W8 节选 p.24 · AI in Daily Life in general\|AI in Daily Life in general]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／25 | 32 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.25 W8 节选 p.25 · AI in Daily Life in general\|AI in Daily Life in general]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／26 | 33 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.26 W8 节选 p.26 · AI in Business in particular\|AI in Business in particular]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／27 | 34 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.27 W8 节选 p.27 · AI in Business in particular\|AI in Business in particular]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／28 | 35 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.28 W8 节选 p.28 · The application of AI in accounting\|The application of AI in accounting]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／29 | 36 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.29 W8 节选 p.29 · Key Technologies in AI Accounting\|Key Technologies in AI Accounting]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／30 | 37 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.30 W8 节选 p.30 · Deep Learning\|Deep Learning]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／31 | 38 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.31 W8 节选 p.31 · Natural Language Processing\|Natural Language Processing]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／32 | 39 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.32 W8 节选 p.32 · Generative AI\|Generative AI]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／33 | 40 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.33 W8 节选 p.33 · Robotic Process Automation\|Robotic Process Automation]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／34 | 41 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.34 W8 节选 p.34 · Optical Character Recognition\|Optical Character Recognition]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／35 | 44 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.35 W8 节选 p.35 · Advantages of AI in accounting\|Advantages of AI in accounting]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W8／36 | 45 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.8.36 W8 节选 p.36 · Disadvantages of AI in accounting\|Disadvantages of AI in accounting]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W9／1 | 1 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.9.01 W9 节选 p.1 · AC6761 Artificial Intelligence Accounting\|AC6761 Artificial Intelligence Ac…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W9／2 | 15 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.9.02 W9 节选 p.2 · Use of AI in stakeholders\|Use of AI in stakeholders]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W9／3 | 16 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.9.03 W9 节选 p.3 · Use of AI in stakeholders\|Use of AI in stakeholders]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W9／4 | 17 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.9.04 W9 节选 p.4 · Financial statement analyses - stakeholders\|Financial statement analyses - st…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W9／5 | 18 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.9.05 W9 节选 p.5 · The perspective of investors\|The perspective of investors]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W9／6 | 新增总结页，无主课件对应页 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.9.06 W9 节选 p.6 · 老师明确可能考Prompt设计\|老师明确可能考Prompt设计]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W9／7 | 33 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.9.07 W9 节选 p.7 · AI hallucination - definition\|AI hallucination - definition]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W9／8 | 34 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.9.08 W9 节选 p.8 · AI hallucination - examples\|AI hallucination - examples]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W9／9 | 35 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.9.09 W9 节选 p.9 · AI hallucination - impact\|AI hallucination - impact]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W9／10 | 36 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.9.10 W9 节选 p.10 · AI hallucination - mitigation\|AI hallucination - mitigation]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W10／1 | 1 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.10.01 W10 节选 p.1 · AC6761 Artificial Intelligence Accounting\|AC6761 Artificial Intelligence Ac…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W10／2 | 2 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.10.02 W10 节选 p.2 · Financial statement analyses – analytical models\|Financial statement analyses – an…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W10／3 | 新增总结页，无主课件对应页 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.10.03 W10 节选 p.3 · 复习要求\|复习要求]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W11／1 | 1 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.11.01 W11 节选 p.1 · AC6761 Artificial Intelligence Accounting\|AC6761 Artificial Intelligence Ac…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W11／2 | 27 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.11.02 W11 节选 p.2 · Bias and fairness - concept\|Bias and fairness - concept]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W11／3 | 28 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.11.03 W11 节选 p.3 · Bias and fairness - Impact\|Bias and fairness - Impact]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |
| W11／4 | 29 | [[AC6761_Artificial_Intelligence_Accounting/review/final-2026/last-class-review#2.11.04 W11 节选 p.4 · Bias and fairness – Strategies for mitigation\|Bias and fairness – Strategies fo…]] | 本次范围复盘，逐页停留未确认 | 正文解释／范围处置 |

### 8.1 课堂时间分配与全程对齐

下表按复盘内容分段，原时钟首尾相接。区间只用于材料去向，不推算逐页停留或各章分值。

| 原录音区间 | 实际内容与去向 | 约时长 |
|---|---|---|
| `00:44:54`–`00:50:22` | 期中复盘与排除线索，见 §0.2、§9.2 | 5 分 28 秒 |
| `00:50:22`–`01:03:35` | 考务、W1–W3，见 §0.3、§2.1、§2.3 | 13 分 13 秒 |
| `01:03:35`–`01:14:42` | W4–W5，见 §2.4–§2.5 | 11 分 7 秒 |
| `01:14:42`–`01:22:58` | W6、W8，见 §2.6、§2.8 | 8 分 16 秒 |
| `01:22:58`–`01:32:51` | W9–W11、答题深度与收束，见 §2.9–§2.11、§6 | 9 分 53 秒 |

## 9. 延伸、勘误与材料边界

### 9.1 本次覆盖与未覆盖

9 份重点页共 131 张，已按真实演示顺序提取文字、表格与可用备注，并实际查看全部渲染页。正文为每张提供入口和解释／范围处置；课堂排除项保留原件及旧知识入口，不等于它们从课程知识中消失。

所有录音考点来自原音 `00:44:54` 以后；`00:50:22` 开始正式期末复习。427 段无时间倒退、无 ≥120 秒时戳空档；这只说明所用转录的时序，不能证明整堂课从头录全。首 `00:44:54` 不在本次全面分析范围；转录末有祝期末顺利的收束语。

本次整理范围按实际取得的材料划定；未整理不等于未录到。

| 范围 | 判定 | 依据与影响 |
|---|---|---|
| 原音开头到 `00:44:54` | 本次范围外 | 不据此推断缺录或课堂略过 |
| `00:44:54`–`00:50:22` | 期中复盘 | 不当作期末试卷或正式解答文件 |
| `00:50:22`–`01:32:51` | 期末复习 | 依本次口头范围安排准备 |

### 9.2 课件没有但录音有的信息

最有用的增量是排除范围、准备数量、给骨架补 REA 图、SQL 给表推结果、Question 与 Prompt 的要求差异，以及按分值展开解释。它们分别就地放入 §0、对应 W 页和 §6。

以下每行是一项跨页增量，其页码去向已在正文展开。

| 增量 | 原时钟 | 正文位置 |
|---|---|---|
| REA 给定简化骨架 | `01:08:40`–`01:09:15` | §2.5 采购／销售核心图 |
| SQL 给表推结果且更换数字／顺序 | `01:16:17`–`01:17:00` | §2.6 |
| Prompt 要明确指导，Question 可简洁 | `01:25:35`–`01:26:03` | §2.9 |
| 根据题目分值展开解释 | `01:31:43`–`01:32:20` | §6.3 |

录音还说期中答案因部门规定不能上传；这是材料获得限制，不把口头复盘说成正式期中答案文件。老师提到可邮件约见查卷；本次没有代发邮件或预约。

### 9.3 必须保留的矛盾与纠正

- 及格数字：DOCX 将其转成 15，本地 ASR 在 `00:50:55` 转为 50。正式 Outline 仅能确认作业与考试分项须通过。现暂记“录音 ASR 为 50，需官方确认具体门槛和分母”，不写成总评 50 就一定过课。
- 考场：录音提 LT13 和 B5 207，提醒核个人分配；旧 AIMS 快照为 YEUNG LT13。不能自行认定本人改去 B5 207，房间代码的正式写法和个人考场仍需查看个人安排。
- 关键技术：录音说六项，所供页和本库主课件列五项。第六项未知，不编造。
- W10：目录列九个，录音说明 Value Chain 未讲，实际讲八个；不是“九个全部必背”。
- 共同比利润表：老师用口头泛例说净利率下降，但所供 Nike 表 2014–2016 是上升；收入作为分母每年为 100%。不照口误反写案例结论。
- SQL：`Balance EXISTS` 为课件问题，实际非空检查应为 `IS NOT NULL`；文本与日期常量也须补合适引号或日期定界符。正文保留原写法并分开给正确可执行形式。
- REA 15% 及品牌性能数字没有可核来源；不把课件声称推广成实证或当前产品效果。

### 9.4 外部补证

仅为 SQL 语法勘误查 Microsoft 官方说明，获取日期 2026-11-26。没有查到它们能证明任何考试范围；范围始终来自本次课。

- [Access 比较、空值与日期字面量](https://support.microsoft.com/en-us/access/comparing-access-sql-with-sql-server-tsql)：`IS NULL`／`IS NOT NULL` 以及 `#date#`。
- [Between...And](https://support.microsoft.com/en-us/access/between-and-operator)：包括两端。
- [Access SQL 子查询](https://learn.microsoft.com/en-us/office/client-developer/access/desktop-database-reference/sql-subqueries-microsoft-access-sql)：EXISTS 检查子查询有无记录。

### 9.5 仍需补的材料与反方检查

老师提及 Canvas 中的 AI bias Word 文件，本次压缩包与本地原件目录未定位到该文件。偏见三页可先学，不能声称已整理 Word 中的全部案例；其案例仍待补源。

题数、选答、各题分值、计算器、字典和公式表规则未取得。考试日期与时间有录音及旧快照相互支持，个人房间与最新安排尚未重登核实。不要把这个范围表当作完整考务公告。

反方视角：最容易误读的是“所有计算不考”——实际只排除了 W6 后段及 Ratio 补充等，W3 共同比仍明确保留。最容易答不完整的是 Prompt 题——只给标题缺角色关切与明确任务。最有争议的事实是数字及格门槛和第六项技术，均保留未知，不用常识补定。

### 9.6 变更与学习状态

本次只登记实际变更，不改变本人的学习与提交记录。

| 日期 | 变更记录 |
|---|---|
| 2026-11-26 | 融合最后课转录，新增 131 页对照、范围收窄、英文参考与自测 |

首次整理最后复习课，新增带原时钟转录、131 页对照、范围收窄、英文自拟参考与自测。旧 M01–M11 的材料版本与历史教学验收不因此整篇升级；本人的通读、自测、复习次数、作答和提交状态不变。
