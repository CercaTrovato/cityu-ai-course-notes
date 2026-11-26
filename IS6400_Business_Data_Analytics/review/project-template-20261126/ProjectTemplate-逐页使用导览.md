---
course: IS6400
module: project-template
week: project
date: 2026-11-26
source: [ProjectTemplate.pptx, supervision-repairs-20261126.md]
transcript: none
prerequisites: [高中知识起点]
new_concepts: [项目章节与CRISP-DM阶段的对应]
tags: [IS6400, project, template, guide]
status: draft
readability_rules: v2
teaching_standard: novice-v1
updated: 2026-11-26
---

# ProjectTemplate：四页原件怎样用于 A06

## 0. 三分钟速览

教师 `ProjectTemplate.pptx` 实际只有 **4 张幻灯片**。它说明项目分析的六个阶段，以及报告的六个章节怎样对应这些阶段。页脚 `2/55`、`3/59`、`4/59` 是原模板残留，不代表本文件有 55 或 59 页。

本导览帮助你从教师章节找到 A06 已有证据，再决定正文要回答什么。它不生成正式报告，不改模型或已交展示，不从模板推断页数、期限或团队认领。

学完应能：按 slide 找到原章节；解释为什么实验失败可能要求回到业务或数据准备；给一个 A06 结果配上正确阶段、运行身份和限制；把部署建议与实际业务试验分开。

## 1. 三条使用路线

先明确任务，再选入口，避免把“已有一包图表”当成“报告已经写完”。

| 场景 | 建议动作 | 精确入口 |
|---|---|---|
| 课前／开始写作前 | 顺读 slide 2 的六阶段，拿一个业务问题走完一圈 | [[#2.2 Slide 2：六阶段是可回退的分析过程\|slide 2]] |
| 课中／按教师页跟读 | slide 3 找讲次背景；slide 4 对照正在讲的章节 | [[#2.3 Slide 3：讲次标签说明知识从哪里来\|slide 3]]、[[#2.4 Slide 4：把六个章节接到已有证据\|slide 4]] |
| 课后／实际写 A06 | 按 §3 一行选证据，先核 run 和条件，再组织一段经理能读懂的论证 | [[#3. 章节、分析阶段与 A06 证据使用表\|使用表]] → [[#4. 写作前可执行的检查\|检查]] → §7 自测 |

当前 A06 权威准备包是 [[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/README|11/26 的 18 项修补处理报告]]。[[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/notes/supervision-repairs-20261126|本日回传]]说明正式报告正文尚未开始、展示已完成且无教师反馈。这些状态沿用其真实证据，不由本导览升级。

## 2. 按四张幻灯片跟读

### 2.1 Slide 1：识别模板来源

原页题为 `Project Template`，署 `Dr. LIU Junming`、`City University of Hong Kong`。这是封面，作用是标识教师模板，没有题目、提交指令或页数规定；不把封面标题当作一章报告内容。

结构提取与实际渲染均已核对：slide 1 的 speaker notes 只有页码 1，slide 2 只有页码 2；slide 3/4 无独立备注正文。未发现额外备注要求，4 页均未设隐藏标记。

### 2.2 Slide 2：六阶段是可回退的分析过程

原页标题 `Agenda`。图给出 Business Understanding、Data Understanding、Data Preparation、Model Building、Testing and Evaluation、Deployment 六阶段。

![[IS6400_Business_Data_Analytics/notes/figures/material-completion-20261126/project-slide-2.png|900]]

先从上部左侧的 1 号框开始：业务理解（Business Understanding）问“谁要做什么决定”。2 号数据理解（Data Understanding）问“手上数据记录了什么”。3 号数据准备（Data Preparation）把记录变成能比较的行和列。

4 号建模（Model Building）把输入映射为输出。5 号测试与评价（Testing and Evaluation）检查对新时期或留出数据是否有用。6 号部署（Deployment）说明怎样把结果放进实际决策。

绿色实线沿 1→2→3→4→5→6 前进；红色虚线表示需要回看较早阶段，外圈表示整个过程仍会继续。图中间 Data 是共同的数据对象，并非额外第七个工作阶段。不能把这张图读成“跑完一个模型就直达落地”。

💡 用本项目走一条具体路径（笔记补充）：如果目的是给有限触达名额排客户，先写清容量条件。再检查一行是否真是一位客户快照，只用预测日前可得字段准备输入。模型给分后，比较相同人数名单的命中。

如果后期月份表现弱，应回看时间变化、字段可得性或业务用途，不能只把不利月份删掉。最后提出试验方案，也不代表已经联系客户或获得新增利润。

这种六阶段安排对应跨行业数据挖掘标准过程（CRISP-DM）。本导览保留图上的 `Model Building`、`Testing and Evaluation` 用词。对应理论总览可回 [[IS6400_Business_Data_Analytics/notes/M01-导论-商业数据分析全景与工具链#2.5 ⭐ BDA 流程：CRISP-DM 六步（本讲的项目过程核心）|M01 §2.5]]；正式段落仍应直接说明当前对象、操作和依据。

### 2.3 Slide 3：讲次标签说明知识从哪里来

原页 `Lecture References` 在同一六阶段图上加红字：`Week 1&2`、`Week 2&3`、`Week 4-9,11`、`Week 10`。

![[IS6400_Business_Data_Analytics/notes/figures/material-completion-20261126/project-slide-3.png|900]]

读新增的红字：上部 Week 1&2 位于业务／数据理解附近；Week 2&3 位于数据准备一侧；Week 4-9,11 对着建模；Week 10 在评价下方。这些是教师模板内的讲次参考，不能当成现在 Canvas 的行政周次、考试范围或截止日期。

实际复习时按内容找 M/T：变量与回归看 [[IS6400_Business_Data_Analytics/notes/M02-预测分析-线性回归#2.2.1 三套术语说同一件事（讲义 p.5）|M02 变量角色]]；特征表示看 [[IS6400_Business_Data_Analytics/notes/M04-特征工程-特征重要性与降维#p.13 · Introduction · 哪组水果特征好|M04 p.13]]。评价协议看 [[IS6400_Business_Data_Analytics/notes/M10-模型评估-交叉验证正则化与AB测试#2.16 训练验证测试与上线（讲义 p.16）|M10 p.16]]，实际预处理时点可对照 [[IS6400_Business_Data_Analytics/notes/T11-模型选择实战-Ridge剪枝与交叉验证#2.06 cell 6 · 先划分再拟合MinMax|T11 Cell 6]]。模板红字用于知识导航，当前 A06 的具体划分与结果仍从修补包取证。

### 2.4 Slide 4：把六个章节接到已有证据

原页 `Project Agenda` 左侧给出六章，右侧重复阶段图。下面按原语言保留全部章节和对应说明：

> Introduction — Business understanding  
> Problem Statement — Business understanding  
> Data Description and Preparation — Data Understanding; Data Preparation  
> Methodology — Model building  
> Experiment and Discussion — Testing and evaluation  
> Conclusion — Deployment: what we can do using your model?

![[IS6400_Business_Data_Analytics/notes/figures/material-completion-20261126/project-slide-4.png|1100]]

先读左侧黑字作为章节，再读其下红字作为章节应完成的工作。Introduction 和 Problem Statement 都归业务理解，但前者交代背景与受众，后者把背景收紧为可评价的问题。数据章必须同时讲数据是什么和怎样处理；方法章讲如何建模；实验章用结果和比较支撑判断；结论章回答模型能用于什么。

右侧仍有返程箭头，表示章节之间有依赖。例如实验表如果比较不同人数名单，须回到 Problem Statement 核容量，再回数据／方法核对象是否一致；不能只在讨论章用一句“模型更好”跳过条件。

## 3. 章节、分析阶段与 A06 证据使用表

每行是一章。证据来自 11/26 已核修补包，引用时仍按文件里的 run、样本、日期和局限写；表内“怎样写”是本导览的学习建议，不冒充教师额外要求。

| 教师章节 | 对应阶段与要回答的问题 | A06 已有可核入口 | 怎样使用，避免哪种误读 |
|---|---|---|---|
| Introduction | 业务理解：谁面对什么决策？ | [[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/scope-decision\|scope-decision]] | 交代客户优先级与有限触达容量；10% 只是比较条件 |
| Problem Statement | 业务理解：输入、输出、比较标准各是什么？ | 同一 scope-decision；[[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/data/claim-uncertainty.csv\|claim-uncertainty]] | 定义未来 90 天复购标签、同容量名单与命中；把“找出原本会买的人”和“触达使更多人买”分开，现有预测不能识别营销因果 |
| Data Description and Preparation | 数据理解＋准备：一行是谁，何时可知道字段？ | [[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/methods-and-data\|methods-and-data]]、[[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/data/dataset-flow.csv\|dataset-flow]]、[[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/data/feature-availability.csv\|feature-availability]] | 客户＋快照日为一行；核历史窗、标签窗与字段可得性 |
| Methodology | 建模：相同对象怎样产出分数和名单？ | [[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/data/experiment-registry.csv\|45 行 run 身份]]、[[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/data/model-parameters.csv\|model-parameters]]、[[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/RUN-REPORT\|RUN-REPORT]] | 按运行身份解释预处理和排序；分数不自动等于概率 |
| Experiment and Discussion | 测试评价：同协议下比谁、差多少？ | [[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/results-for-writing\|results-for-writing]]、[[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/cv-and-uncertainty\|cv-and-uncertainty]]、[[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/figures/README\|10 张图与读法]] | 同容量对照并保留不利月份；开发结果不称新盲测 |
| Conclusion | 部署：支持什么行动，还缺什么证据？ | [[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/business-experiment\|business-experiment]]、[[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/limitations-and-use\|limitations-and-use]] | 两组均联系，只比指南内容；不能检验联系增量或利润 |

### 3.1 怎样核一条运行记录，再引用结果

一次运行（run）是一条可追溯的分析记录。它固定用了哪些数据、怎样处理、采用哪些参数和模型权重，以及在什么条件下评价。参数可以是预先指定的设置，模型权重则是训练学出的数值；名字相同不保证这些内容相同。

先分清数据在做什么。训练（training）让模型从数据中学习参数，也在训练数据上确定填补、缩放等处理。开发（development）用来比较方法或选择方案；用过它来作选择，就不能再称它是完全未见的最终测试。

冻结后期检查（fixed-model later-period check）把已经定好的模型用于后来的月份，观察跨期表现；本项目不拿这些已见结果重新选模型。概率扩展另把训练期数据按 80/20 分为拟合（fit）和校准（cal）两部分：80% 学基础模型，20% 用来学习把分数转成概率的校准关系，之后才去评价。

因此，fit/cal 是训练期内部的不同用途，不等于“80% 训练、20% 最终测试”。本项目扩展的 43 与全十月模型的 50 也不能当作“只增加校准后的变化”，因为拟合与校准协议同时不同。

实际操作时，打开上表的 `experiment-registry.csv`，先找 `run_id` 和 `method`，再依次读训练、校准、评价和名单条件。以下是一条真实记录，不是新运行：

| 要核的字段 | 本例原值 | 读成普通话 |
|---|---|---|
| `run_id` | `repair-G1G2-20261126` | 本日固定新字段对照的运行身份 |
| `method` | `F0` | 其中的基础字段版本 |
| `train` | `2017-10-01 full` | 用十月全部训练快照学习模型 |
| `calibration` | `none` | 此次没有另分校准数据 |
| `evaluation` | `2018-01-01 additional development, already seen` | 一月是已见的额外开发比较 |
| `class_weight` | `balanced` | 训练时提高少数类别的重要性 |
| `cohort_N`、`positives` | `29368`、`230` | 评价中有29368位客户，230位发生复购 |
| `K`、`hits` | `2937`、`50` | 固定选2937位，其中50位复购 |
| `source_table` | `data/feature-experiment-results.csv` | 这些结果对应的原表位置 |

再核该记录的 `preprocessing`，确认填补、标准化等处理来自训练数据；核 `model_sha256`，辨认保存的具体权重文件。SHA-256 是文件指纹，用于分辨版本，不是准确率指标。本例模型指纹以 `f80dbec2` 开头，完整值保留在登记表；不要用另一条同名 F0 的文件替换。

最后打开 `source_table` 指向的结果表，核同一方法、客户范围、名额和命中，才写“本次开发比较选2937人、命中50人”。若换成其他 run，必须重新核这些字段；不能只看最后的50恰好相同。

### 3.2 把数据和比较条件写进章节

数据章的时间解释应完整：历史窗为预测日前六个月，标签看未来 90 天。配送／评价字段按当时可得性解释；没有变更日志不能声称绝对没有历史回写。

方法章区分 H04、R3、冻结检查和新 F0/G1/G2。说明训练时拟合预处理、加权损失、分数排序和并列处理。实验章先交代 run 和月份，再写指标；三期冻结检查保留不利五月，不因已见结果重选模型。

例如新特征实验为十月训练、一月开发，同取 2937 人。F0/G1/G2 命中 50/49/48，只回答这次开发比较，不回答线上收益。方法章先交代三版差别，实验章放同协议数值，结论章说明新字段未改善该开发指标及后续怎么验证。

概率校准（calibration）要让给出的概率与实际发生频率较相称；它与把谁排进前 10% 是不同问题。按 §3.1 的用途区分，该扩展中的 43 人结果不能与全十月 R3 的 50 直接排名，也不把商品金额当作利润。细节以 [[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/work/report-repairs-20261126/scope-decision|范围说明]] 和结果文件为准。

现有 `business-experiment` 方案让两组都收到联系，比较通用购物指南与家居用品主题指南，只检验内容主题差异。它不能回答“联系比完全不联系多带来多少购买”；若要研究这个问题，还需另设合适的不联系对照。利润则还需要成本与利润口径，这里不修改已有内容试验方案。

## 4. 写作前可执行的检查

先选一行使用表，打开对应证据，写出要回答的一个问题。随后确认以下四件事：

1. 数字对应哪个 run、月份、客户数和容量；同名 F0 不自动代表相同权重。
2. 训练、开发、冻结后期检查和校准扩展分开；后期结果不回流重选已冻结模型。
3. 图和表的准用版本来自 11/26 包。旧错误置信区间（confidence interval，CI）图禁用，不从旧展示直接剪贴复用。
4. 每个结论能接到一个表／图和影响结论的限制；“代码跑通”本身不是业务结论。

写作示例（笔记自拟）：在固定一月开发比较中，三版同选 2937 位客户，命中分别为 50、49、48。这个结果支持“新增配送／评价字段没有改善这一次同容量命中”；不能推广成所有未来月份都无用。

## 5. 双语术语卡

以下定义用于读懂图和章节，不增加教师题目。

| 中文 | 图中英文 | 本导览中的操作含义 |
|---|---|---|
| 业务理解 | Business Understanding | 明确决策者、目标、约束和成功标准 |
| 数据理解 | Data Understanding | 确认一行是谁、字段记录什么以及质量限制 |
| 数据准备 | Data Preparation | 按正确时间和单位生成模型输入 |
| 建模 | Model Building | 学习输入到分数／预测的关系 |
| 测试与评价 | Testing and Evaluation | 在约定协议下比较表现并检查结论边界 |
| 部署 | Deployment | 说明结果怎样进入实际流程，以及仍需验证什么 |

## 6. 用英文组织章节的最小句型

下面是笔记自拟，不是教师原文或正式稿。Introduction 可写 “The business decision is ...”。Problem Statement 写 “Given ... at the snapshot date, we aim to ...”。数据章写 “Each row represents ...”。

方法章写 “Preprocessing is fitted on ...”。实验章写 “Under the same protocol and capacity ...”。结论写 “The evidence supports ...; the proposed trial would test ...”。

每句的省略号须用真实对象和证据填入。若不能填清 run 或单位，应先回证据，不把通用句型当正文完成。

## 7. 迁移自测

这些题只用于学习，不改变本人掌握记录。

**题 A。** 一位同学写：“新增字段有更多信息，所以模型一定更好。”使用表的哪一行能核？现有证据支持什么？

<details><summary>答案与理由</summary>

先看方法行确认 F0/G1/G2 及预处理，再看实验行同容量结果。固定一月开发命中为 50/49/48，新字段没有改善这次指标。更多字段不保证更多可预测信息；不能忽略样本、过拟合或时间可得性。

</details>

**题 B。** “一月名单命中更多，因此客户触达会带来更多利润。”缺了哪一步？

<details><summary>答案与理由</summary>

名单命中是观察性预测表现，不识别触达引起的新增购买，也没有成本和利润证据。现有 `business-experiment` 让两组都收到联系，只比较通用购物指南与家居主题指南的内容差异。

这个方案仍不能证明联系比不联系多带来多少购买；研究触达增量需另设合适的不联系对照，研究利润还需成本与利润口径。已有内容试验仍是未执行的方案，不把它写成利润主张已经得到验证。

</details>

**题 C。** 页脚有 `4/59`，是否应写 59 页？slide 3 写 Week 10，是否就能确定目前考试范围？

<details><summary>答案与理由</summary>

都不能。文件实际为 4 张，页脚为模板残留；Week 标签是模板知识参考。页数、截止、考务范围须查各自当前正式要求，不从这两处推断。

</details>

## 8. 逐页映射与原图处置

本表每行对应一张真实源 slide；源图作为原件渲染保存，没有重绘成另一套关系。

| 物理 slide | 原标题 | 正文精确入口 | 原图／备注处置 |
|---|---|---|---|
| 1 | Project Template | [[#2.1 Slide 1：识别模板来源\|slide 1]] | 纯封面，正文说明来源，不另嵌装饰封面；备注仅页码 |
| 2 | Agenda | [[#2.2 Slide 2：六阶段是可回退的分析过程\|slide 2]] | 六阶段原图整页保留，解释顺序、返程、数据中心；备注仅页码 |
| 3 | Lecture References | [[#2.3 Slide 3：讲次标签说明知识从哪里来\|slide 3]] | 原图和全部红色讲次标签保留，解释相对上页增量；无备注正文 |
| 4 | Project Agenda | [[#2.4 Slide 4：把六个章节接到已有证据\|slide 4]] | 章节及阶段图整页保留，§3 接真实证据；无备注正文 |

## 9. 来源、状态与不增加的要求

本篇来源为本轮已取得的 ProjectTemplate 四页、A06 11/26 回传及修补准备包。教师模板只给流程和章节；本篇没有从它推导新页数、期限、考核或实际部署状态。A06 的 23 页分工是已有写作建议，不是这份四页模板要求，也没有在这里重新安排团队。

四页来源已逐张视觉查看，并核 speaker notes、隐藏标记和媒体。最终导览供学习和写作导航；正式报告正文、成员认领、最终人工核稿与提交继续按真实后续记录。现有项目算法、元数据、原展示与报告准备文件均未由本导览修改。
