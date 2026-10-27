---
course: IS5113
type: assignment-notes
assignment: Assignment 1 · 交警 AI 摄像头案例
due: 2026-09-22 12:00
submitted: 2026-09-22 11:49
points: 10
status: 已提交，待讲评
files: [IS5113_Assignment1_60234350.docx, IS5113_Assignment1_60234350.pdf]
tags: [IS5113, assignment, 案例分析, 三角测量, 康德, 功利主义, 社会契约]
updated: 2026-10-27
readability_rules: v2
teaching_standard: novice-v1
---

# Assignment 1 · 交警 AI 摄像头案例 —— 作业笔记

这份学习解析教你把一段故事拆成可论证的问题，再分别回答五问。§1–§6 是本次参考分析，§7 保存真实已提交 PDF 的文字并逐段复盘，§8 用新案例检查迁移。参考分析不是教师标准答案，也不会替换本人已提交文件。

学完后，应能区分题面事实与猜测，解释五种伦理视角怎样使用同一事实，写出有条件的判断，并指出什么新增信息会改变判断。是否已学会、成绩和讲评仍由本人实际记录决定。

## 0. 题目与提交信息

既有记录为：2026-09-22 12:00 截止，2026-09-22 11:49 已提交，Canvas 分值 10。此处承接历史记录，本轮没有重新登录 Canvas，也没有核到新成绩。讲义 p.85 写 “DUE AT NOON, 22 SEPT”，p.86 要求 1–2 页；年份、10 分和提交时刻来自既有任务记录，不假称由 PDF 单独证明。10 分在课程总评中属于哪一项未核，不能把 10 分直接当 10%。

真实提交文件在 `assignment/graded/A01-traffic-camera/submission/`，与本篇 `notes/` 不是同一目录。原有已提交、待讲评状态保留；本次只修改学习解析。

### 0.1 完整英文原题

以下两段及五问来自 M02 讲义 p.10–11，原样重现在 p.85–86；只合并排版换行，不改题意。原题没有选择题选项。

> Trying to deter speeding offenders, the Traffic Police installs AI-video cameras on all road junctions. The AI-video cameras can reliably detect cars traveling more than five km per hour above the speed limit, read license plate numbers and capture high-resolution pictures of vehicle drivers, in real time. Equipped with AI face recognition ability (99% accuracy), the system automatically issues a speeding ticket to the driver, complete with photo evidence. 3 months after the system is put into operation, the number of people speeding is reduced by 90 percent.
>
> The Organized Serious Crimes Bureau (OSCB) asks the Traffic Police for real-time access to the information collected by the AI-video cameras. The Traffic Police complies. 3 months later, OSCB uses this information to successfully arrest 5 wanted serious criminals.

讲义 p.86：

> ANSWER IN 1-2 PAGES
>
> Did the Traffic Police do anything wrong?
>
> Who benefited from the actions of the Traffic Police?
>
> Who was harmed by the actions of the Traffic Police?
>
> What other courses of action could the Traffic Police have taken to achieve its objectives?
>
> What additional information, if any, would help you answer the previous questions?

### 0.2 中文读题入口：先找对象、动作和限定词

交警为了遏止超速，在所有道路路口装摄像头。摄像头识别“比限速高出超过 5 km/h”的车辆、读车牌、拍摄司机高清照片；系统凭人脸识别自动向司机开附照片证据的罚单。三个月后，超速人数比原来减少 90%。随后，有组织严重罪案调查机构（Organized Serious Crimes Bureau，OSCB）要求实时访问这些资料，交警同意；再过三个月，OSCB 据此抓到 5 名通缉重犯。

五问分别要求：评价行为是否有错；找受益者；找受害者；提出仍能实现目标的替代做法；说明哪些补充事实会改变前四问。它们没有要求选择指定立场，也没有给各问分值。

“超过 5 km/h”不包含恰好 5 km/h。“所有路口”扩大资料采集的场所范围，但不证明每位市民都被拍到。“实时访问”表示 OSCB 能及时访问系统资料，不只是事后索取一段录像；题面没有明确访问期限、每个字段或每次查看的范围。

## 1. 第一步：把决定、事实和未知分开

如果只问“摄像头好不好”，就会把交通目的和刑侦目的混在一起。先分两个决定，才能单独检查各自的理由。下面一行代表一个决定，“未知”不能在后文突然变成已知。

| 决定 | 已给动作与结果 | 仍不知道什么 |
|---|---|---|
| A：交通执法 | 摄像、识别、自动罚单；超速人数下降 90% | 告知、申诉、保留期、实际误罚与事故变化 |
| B：刑侦访问 | 同意 OSCB 实时访问；抓到 5 名重犯 | 法律依据、授权条件、监督、必要范围及公众知情 |

例如 B 确有破案收益，但不能把 A 的全部交通收益再算成 B 的新增收益。比较 B 时应问：已有 A 的情况下，额外开放实时访问增加了什么收益和风险？这叫比较同一选择的增量，而不是把整段故事的好结果都归给最后一步。

### 1.1 三个会改变答案的读题陷阱

第一，减少 90% 的分母是原先的超速人数，不是全体司机。💡 笔记补充：若原来 100 人超速，后来剩 10 人，就是减少 90%；不知道总司机人数，仍算不出守法司机比例。所以不能写“90% 以上司机从不超速”，更不能写超速已经消失。

第二，99% 指题面的人脸识别准确率（accuracy），题面没有给测试方式、样本量或罚单统计。💡 假设同分布测试做 10,000 次识别、其中 99% 正确，才可算识别错误为 $10{,}000\times(1-99\%)=100$ 次。100 次是该假设中的识别错误，不是本案实际误罚数。是否识别错司机后必然开罚单、是否有复核，题面都没告诉。准确率也不能换名为精确率（precision）：后者通常问“被系统判为某身份的记录里有多少真的属于该身份”，分母不同。

第三，“The Traffic Police complies”只说明交警同意了请求。“没有写审批”不等于“肯定没有审批”；“装了可见摄像头”不等于“司机知道识脸和后续用途”。自动开罚单也不证明不存在后续申诉。可以批评题面缺少保障证据，不能发明其不存在。

相同原则适用于后果：超速下降支持威慑效果，但题面没有给交通死亡或伤害数据；群体识别差异、信任下降、寒蝉效应都可列为需要调查的风险，不能冒充本系统已发生的结果。

## 2. 第二步：为什么要讲理由，而不只说立场

“我觉得监控不好”表达态度；伦理论证还要说明谁受到什么影响，以及为什么这个影响足以支持某个判断。这里的伦理（ethics）讨论应该怎样对待人；合法性（legality）讨论行为是否符合适用法律。两者会相交，但一个行为合法仍可能不够尊重人，法律是否允许也必须回到法域、日期和具体规则核实。

M02 p.12–13、p.78 要求解释基于事实、共享价值和逻辑，并能说服愿意听理由的怀疑者。本案没有配套逐问评分表，因此这是一套论证方法，不能称作教师给本题的精确评分细则。

可以用一条短链检查自己的话：

1. 事实：交警把交通资料开放给另一个执法目的。
2. 规范前提：用途扩张应有与影响程度相称的理由和保障。这是本参考分析采用的判断标准。
3. 套用：题面给破案效果，却没交代为什么必须实时访问、为何更窄范围不足。
4. 结论：现有资料不足以充分辩护 B；应要求额外证据，而不是直接认定它必然违法。

反方可说严重犯罪侦查很紧急。回应必须接住这个理由：紧急性可能加强 B 的必要性，但仍须问范围、期限、复核和滥用代价。承认条件会改变结论，通常比虚构确定事实更有说服力。

## 3. 第三步：五个视角怎样实际使用

以下是 ⚪ 参考作答（笔记推断），不是五种理论对本题已有的教师判决。道德理论是用来检查理由的不同标准；它们不会自动给出固定票数。更完整的课程原理可回看 [[M02-道德理论及其应用]]，本节已提供完成本案所需的桥梁。

### 3.1 行为功利主义：这一具体选择，哪种后果整体更好？

功利主义（utilitarianism）不是自私自利，而是把所有受影响者的福祉都算入。行为功利主义（act utilitarianism）比较当前可选行为的总体后果；课程 p.46 以幸福变化的加总和最大化解释。这里的效用（utility）指福祉或痛苦的变化，不是警方绩效分数。

在 A 中，超速下降是可能改善安全的证据；在 B 中，抓到 5 名重犯是实得结果。另一边有采集范围、错误识别、调查误伤和滥用的风险。先列人群、再列每群收益/伤害的严重性、持续时间和可能性，才能比较。不能把“90%”和“5 人”直接相加，它们不是同一单位。

最强支持意见是：若 B 阻止严重伤害且成本较低，开放资料可能产生较大的总体收益。最强质疑是：成本和替代方案未知，尚不能算出净收益为正；即使加总为正，受损者是否承担不公平负担也需单独讨论。p.56 批评总量原则不自带分配正义规则，不是说任何功利主义者都不关心个人痛苦。

💡 笔记补充：两方案总收益都为 100，甲分为 25、25、25、25，乙分为 97、1、1、1。若只看总数，两者一样；若关心最弱者，就必须另说明分配标准。这个例子解释总量和分配为何是不同问题，不是本案效用计算。

如果查明 B 的实际伤害很高、窄范围调证也能抓到同样罪犯，行为功利主义也可能反对 B。它不是本案必然的“唯一支持票”。

### 3.2 康德主义：准则能成立吗，是否尊重人的地位？

康德主义（Kantianism）强调义务和对人的尊重，不能只靠好结果抵消不当手段。准则（maxim）是自己准备遵循的行动规则，要写出情境、行动和目的，例如“为保障道路安全，政府在必要范围内按公开规则自动执法”。

定言令式（categorical imperative）第一表述在 p.30 要求只按能够同时愿为普遍法则的规则行动，不是只问“人人这样会不会令我不舒服”。本节先用 p.31 虚假承诺展示的一种检验路径：看行为所依赖的实践是否会被同一规则摧毁。该例依靠别人相信承诺；若人人都打算违约，取得信任的前提就自我瓦解。没有发现这种自毁，并不自动说明准则已通过第一表述，仍须按 p.30 的一般标准判断。

套到 B：若机构先保证资料只作交通用途，却暗中为了方便转作其他用途，就利用了对限定用途的信任。把“可以靠虚假用途保证获取资料”普遍化，会破坏自己所依赖的可信保证。但本题没说曾作这种保证；“任何未告知的转用都必然产生同一概念矛盾”还缺前提。隐私风险或公众不信任本身也不是逻辑矛盾证明。

第二表述在 p.33 要求把人也当目的，不能仅仅（merely）当手段。这里要检查机构有没有尊重人的理性判断、自主和尊严。若无告知、无正当公共理由、无约束地把所有司机当破案资料来源，就有强烈质疑。公众执法不一定需要每人可自由拒绝；合理授权、必要性、程序与救济也要一起判断，不能用“司机没同意”自动推出所有执法都错。

A 不会仅因摄像头可见就自动通过两项检验。B 若有公开的严格限定、紧急理由和独立复核，相关反对理由会减弱；若查明故意欺骗，则第一表述的论证会更强。把缺的前提说出来，才算真正应用理论。

### 3.3 规则功利主义：常态规则和替代规则哪一种后果更好？

规则功利主义（rule utilitarianism）在 p.52–55 评价普遍遵循一条规则的后果。与行为功利主义的区别是比较对象：前者评估长期采用什么规则，后者直接比较眼前可选行为。

不要只比较“永远共享”和“永不共享”。可比较三条规则：无限制实时共享；限于重大案件、特定目标和期限且留痕复核；完全不共享。第一条可能增加滥用与信任成本，第三条可能错失救人机会，第二条试图在收益和风险之间取得更好结果。这里的“可能”需要经验材料支持，不是题面已经证实公众失信。

如果限定规则能保留大部分破案收益并减少伤害，它有理由优于无限制规则。若所有限制会导致不可接受的严重风险，还需重估。规则功利主义问的是规则后果，康德第一表述问的是能否一致地愿为普遍法则，两者不能混写成“规则不好，所以概念矛盾”。

### 3.4 社会契约论：理性的人能接受怎样的共同制度？

社会契约论（social contract theory）关注人们为共同利益能够相互接受的规则，以及政府如何执行规则（p.58–59）。不是问“警方想不想共享”，而是让可能成为受保护者、受监控者或误认者的人都能看懂并质疑同一制度。

消极权利（negative right）要求他人不干预，例如不任意追踪；积极权利（positive right）要求他人采取行动，例如提供保护。p.60 还把“无例外的绝对权利”和“随情境可受限的权利”分开；p.61 说两类存在倾向，不能把倾向当逻辑同一。隐私保障也可能需要监管、纠错等积极行动，公共安全也含不受伤害的消极要求。

本案要问：共享权限由谁决定、为何必要、谁监督、被误认的人怎样申诉，以及理性人会否接受这种风险分配。不能只把“隐私=消极=绝对、安全=积极=有限”串起来就裁决冲突。p.65 本身指出权利冲突仍是难点。

如果有必要范围、独立监督、救济和相互可接受的理由，B 可能更可辩护；若只有机构方便而没有受影响者保障，反对理由更强。这是伦理评估，不是宣布本案已违法。

### 3.5 德性伦理：审慎和正义怎样变成机构行动？

德性伦理（virtue ethics）关注行动者应具备的品格，例如审慎（prudence）、诚实和正义（p.66–75）。用于公共机构时，是借品格标准评估其决策方式，不是声称机构有和个人完全相同的心理。

审慎不是“什么都不做”，而是在影响扩大前调查必要性、考虑替代方案、记录理由并愿意纠错。用于 B，可建议先限定案件和权限，再设审计与复查；用于 A，可建议核误认和申诉。单凭 “complies” 不能诊断警方不审慎，因为题面可能省略了它已做的工作。应写“如果没有这些步骤，则体现审慎不足”。

### 3.6 辅助工具怎样接到本案

用途扩张（function creep）指资料或系统逐渐被用于原始目的以外的任务；A 到 B 正好提示你检查目的边界，但跨用途不自动等于违法。差别性影响（disparate impact）指某规则或系统对不同群体造成不成比例的结果；本题没有分群体数据，应该在 Q5 请求，而不是在 Q3 宣布本系统某群体错误更高。

程序公平（procedural fairness）问决定过程是否给人发声、解释和纠错机会，所以 Q4 可以加人工复核与申诉。模型卡（model card）是说明系统用途、测试和限制的文件，可记录什么算预期用途、什么需重新批准；有文件不保证实际执行。这些工具帮助把伦理理由变成检查项，不能代替五问的直接答案。关联课程入口为 [[M03-偏见与公平]] 与 [[M04-AI透明-从看得见到信得过]]。

## 4. 第四步：交叉检验理由，不是数理论票数

三角测量（triangulation）在这里指用不同视角检查同一判断。M02 part3 `40:35` 出现 “triangulate it”，周围说明从规则与德性等角度再看；转录有多处 ASR 错词，本篇不把重写的流畅英文伪装为教授逐字原话。

下面的流程是 💡 笔记补充。每一行的“产物”是下一步可以检查的东西，不是固定标准答案。

| 顺序 | 做什么 | 留下什么 |
|---|---|---|
| 1 | 分 A/B，列事实和未知 | 两个待评价决定 |
| 2 | 比较各决定及替代方案的后果 | 收益、风险及证据缺口 |
| 3 | 检验准则、尊重和制度可接受性 | 有条件的支持与反对理由 |
| 4 | 处理最强反方，检查审慎过程 | 理由冲突及回应 |
| 5 | 给判断、边界和重判条件 | 可辩护的结论 |

以 B 走一遍：已抓到 5 名重犯，支持其有执法价值；实时访问范围和保障未知，妨碍必要性判断。不能因此把功利主义记一张支持票、另四种记反对票。多种理论也可能共享同一事实假设，票数不代表独立证据数量。

本参考结论是：A 的安全目标和题示效果提供初步理由，但其数据与罚单程序仍需核实；B 所示额外收益不足以单独证明实时访问的广泛性和持续性正当。应先要求更窄范围、独立监督和救济，或以证据说明为何较少侵入的方案不足。这个判断明确偏向限制 B，同时保留新事实改变评价的空间。

## 5. 五问逐问解析与英文参考

以下英文均为本次学习参考，不是本人当时提交原文，也不是官方答案。每一问先看中文任务，再看英文怎样压缩同一论证。

### Q1 · Did the Traffic Police do anything wrong?

问题问的是交警行为有无伦理问题，应拆 A/B。A 有正当目的和题示威慑效果，但尚不能自动证明所有采集都必要；B 增加用途和访问能力，需额外辩护。论证依次使用 §3 的后果、对人的尊重和制度保障；最强反方是严重犯罪的公共安全收益，回应是收益不能省去范围和替代方案比较。题面没给法律与保障，结论用“现有事实不足以充分辩护”，不把未知写成警方已做错的具体事实。

> Decision A has a defensible safety objective and a reported deterrent effect, but its data collection and ticketing safeguards still need examination. Decision B requires a separate justification: five arrests show a benefit, but do not establish that real-time access is necessary or proportionate. A utilitarian assessment must compare benefits and harms with less intrusive alternatives. A Kantian assessment asks whether the policy respects people as rational agents, while social-contract reasoning asks whether its powers and safeguards are mutually acceptable. On the facts provided, I would restrict B unless its scope, oversight and necessity can be justified. I cannot infer from “complies” that no authorisation or notice existed.

### Q2 · Who benefited from the actions of the Traffic Police?

直接可确认的是 5 名通缉重犯被抓；道路使用者可能因超速减少而更安全，但事故减少数未知。警方得到执法帮助，不等于题面证明绩效指标已提高；潜在受害者获得保护是合理可能收益，不是已避免了多少案件的统计。

> Road users may benefit from reduced speeding. The public and potential victims may benefit from the arrest of five wanted serious criminals. The Traffic Police and OSCB gain enforcement assistance. However, the scenario does not report accident reductions, crimes prevented or changes in institutional performance scores, so those benefits should not be quantified as established outcomes.

### Q3 · Who was harmed by the actions of the Traffic Police?

先列暴露于采集和用途扩张的人，再列可能被误认或遭滥用的人。被拍摄和访问本身已经扩大了隐私暴露，但实际损害强度取决于存储、访问和保障；不能证明人人均被持续追踪。错误识别、特定群体不成比例受损和寒蝉效应是风险清单，需数据区分已发生与可能发生。

> Drivers whose images and identifying data are collected face privacy exposure, including drivers who do not speed. Those misidentified could face wrongful penalties or investigation, if errors pass through the enforcement process. Unequal error rates could impose disproportionate burdens on some groups, and broad monitoring could affect trust or freedom of movement. These latter harms are risks requiring evidence: the scenario does not report the number of wrongful tickets, group-specific error rates or actual chilling effects. A 90% reduction in speeding is not the percentage of drivers who never speed.

### Q4 · What other courses of action could the Traffic Police have taken to achieve its objectives?

“to achieve its objectives”限定替代方案仍须服务遏止超速，不能只提停掉全部执法。可以先检验只收必要字段、现场处理、较短保留期能否保持效果；若需对司机而非车主执法，车牌方案的责任归属和有效性仍须核实。再加人审、申诉、清楚公告。对 B，比较逐案、特定目标和限时访问，保留访问日志并安排独立复核。司法授权或监管批准是应按当地法律核的机制，不是本案已知普遍法定义务。

> The police could test whether plate-based enforcement or local processing would achieve the speeding objective with less personal data, subject to identifying the legally responsible person. They could limit retention, publish purposes, review disputed identifications and provide accessible appeals. For OSCB, they could compare blanket real-time access with targeted, time-limited requests, access logs and independent review. Any judicial or regulatory authorisation should follow the applicable jurisdiction; the scenario does not establish one universal approval requirement. The effectiveness and costs of these alternatives need testing.

### Q5 · What additional information, if any, would help you answer the previous questions?

好的问题会指明“答案怎样改变判断”。下面一行是一组待补事实，右列是它影响的论证。

| 待补事实 | 对判断的具体影响 |
|---|---|
| 法域、法律权限、独立审批和复核 | 判断是否合法及制度保障是否可接受 |
| 实际访问字段、对象、期限、日志和告知 | 判断用途扩张与自主受影响的程度 |
| 99% 的测试口径、样本、人群与部署误罚 | 判断风险是否被低估或不均分配 |
| 纠错、申诉、举证与实际补救 | 判断错误是否直接转为不可逆损害 |
| 事故变化、破案新增贡献与窄方案效果 | 比较后果、必要性与比例性 |

比例性（proportionality）在这里问为达到正当目标施加的负担是否过度，包含比较效果和较少侵入的可行办法。若车牌方案同样有效且可靠归责，人脸采集的额外必要性会减弱；若确有只能及时识脸避免的严重伤害，理由可能增强。相同数字因附加事实不同，会导向不同判断。

> I would ask about the applicable law, authorisation and independent oversight; what data OSCB can access, for whom and for how long; notification, retention and audit arrangements; how the 99% accuracy was tested and how often errors lead to wrongful enforcement; appeal and remedy procedures; and whether less intrusive alternatives achieve comparable results. These facts could change my assessment of consequences, respect for persons, institutional legitimacy and proportionality.

## 6. 写成 1–2 页：先保证五问都有答案

讲义只给 1–2 页和五问，没有给本题各问权重。因此可以给 Q1 较多空间解释中心判断，但不能说它“分值最重”，也不能说不点理论名就必然不得分。写出标准如何应用比报理论名称更重要。

写作顺序可先草拟每问一句答案，再为 Q1 保留最有力论证、反方与边界；Q2/Q3 分清实得与可能；Q4 说明替代方案为何仍能达目标；Q5 把信息缺口接到结论。重复定义、重复案例叙事和没有证据的肯定句应优先删减。

字数不能直接换算页数。§7 的真实提交 PDF 为 2 页；原笔记所谓约 900 词≈1.5 页不是可靠排版规则。将来制作新的答卷应看实际最终 PDF 的字号、行距和分页，不能通过把字缩得很小满足页数。

结尾参考句：

> My assessment therefore distinguishes a potentially justified safety use from a secondary use that needs stronger justification. Public-safety benefits matter, but so do the scope of access, less intrusive alternatives and effective safeguards. Additional evidence could strengthen or weaken this conclusion.

这是学习参考；不得把它当作已提交稿结尾或教师评语。课程 AI 使用权限和披露按具体任务核实，本次没有生成或修改新的正式提交件。

## 7. 提交稿逐段解读

本节依据实际 `submission/IS5113_Assignment1_60234350.pdf` 的 2 页文字。旧笔记给出的长英文段落与真实 PDF 并非逐字相同，本次以 PDF 替换学习笔记中的误引；PDF 和 DOCX 原件保持不动。下面折叠块仅去除反复页眉、合并 PDF 排版换行，保留原稿措辞与错误。它是历史个人作答，不是本次推荐照抄的答案，也不是官方范例。

<details>
<summary>来源核验：真实已提交 PDF 全文（历史作答，含原有错误）</summary>

> Assignment 1 – The Traffic Police AI Camera Case
>
> 1. Was there any misconduct by the Traffic Police? There are two distinct decisions in the case. Decision A is to install the cameras, monitor speeding and fine drivers automatically. Decision B is to allow real-time access of the data collected to the Organized Serious Crimes Bureau (OSCB). In my opinion, decision A is justifiable, but decision B is not. I argue so through application of three ethical theories covered in the course.
>
> Act utilitarianism. In terms of a simple cost–benefit assessment, both decisions are reasonable: speeding dropped by 90%, meaning lower number of deaths and injuries, and five dangerous criminals have been caught. Costs of continuous monitoring of everybody driving and 1% erroneous identification appear to be small. Nevertheless, there is an inherent flaw in utilitarianism: it ignores distribution. The benefits of both decisions are shared by everyone, while the costs of being mistakenly fined and being constantly monitored by a crime bureau fall on particular individuals who never agreed to carry them out. Total benefit doesn't justify unfair distribution.
>
> Kantianism. For decision A, the maxim is "A government may employ automated measures to enforce prohibitions of dangerous behaviour on public roads." It passes both Kant's tests: it can be universalised and drivers are aware of camera presence at junctions. For decision B, the maxim is "Data collected for purpose A may be used for purpose B without notifying individuals the data concerns." If everybody acts on this maxim, there will be no predictable purpose in any data collection and consent as a concept becomes logically contradictory. It also fails Kant's second formulation: drivers were not notified about face recognition and tracking their movements by crime bureau, hence they couldn't possibly consent; they were used only as means to catch dangerous criminals.
>
> Rule utilitarianism and social contract theory. Made into a rule – "law-enforcement agencies may exchange the data collected for one purpose with any other agency without requesting extra authorization" – decision B results in poor long-term consequences: distrust in data collection by governments increases, cooperation becomes harder and governance more expensive. Fewer arrests cannot outweigh it. From the viewpoint of social contract, privacy is a negative right (the government only needs to restrain from data collection) and such rights are typically absolute, while public safety is a positive one which is usually limited. The Traffic Police may have acted legally, but as was discussed in the class, legality is only the minimum of the social contract; "it was legal" is not an ethical justification. Finally, the case says that the police simply "complies" – no proportionality assessment, no court order, no notification to the public – thus demonstrating lack of prudence expected of a virtuous institution.
>
> 2. Who benefited?
>
> Law-abiding motorists, who don't have to face speeding drivers anymore; the society as a whole, which is safer with the arrest of five serious criminals; the Traffic Police and the OSCB, whose performance metrics have improved; and potentially the victims of both traffic accidents and organized crime.
>
> 3. Who was harmed?
>
> All motorists driving by junctions, including the 90%+ who don't speed, since their faces and movements are recorded constantly, and after Decision B, are being monitored in real-time by a crime bureau to which they never consented. Motorists who are erroneously identified by the system: 99% precision still leaves one error per hundred identifications, which is a big absolute number at junction traffic volume, with the burden of proof shifted to the wrongly fined motorist. Groups of people for whom facial recognition algorithms are less precise (e.g., people with dark skin, females, seniors), who will suffer from the higher number of false positives – 99% is an average value, hiding disparate impact. The society as a whole is facing a chilling effect on mobility and loss of trust in data collection by government agencies.
>
> 4. What else could the Traffic Police have done?
>
> In order to reach the goal of speeding suppression: collect licence plates instead of performing face recognition; process images locally and upload only speeding incidents, deleting everything else; establish short period of retention and automatic deletion; perform human review and allow appeals before a ticket becomes final; and announce what kind of data is being collected and for what purposes. In order to respond to the OSCB request: reject blanket real-time access and require instead a request on a per-case basis and judicial authorization for every particular suspect; log all access and conduct audits; and receive approval from the Privacy Commissioner or an independent oversight agency before every data exchange agreement.
>
> 5. What additional information would have been useful?
>
> Is real-time access by the OSCB authorized by the law? Is any court or privacy authority ever asked to review this access? How long is data stored, who has access to it, and is there a logging of any access? On what population the 99% precision was tested and are error rates the same across genders, ages and ethnicities? Are wrongly fined motorists given a chance to appeal and who carries the burden of proof in an appeal? Was the motorists notified of the secondary use of the collected data? And is 90% suppression of speeding possible with less intrusive measures, e.g., using only plate recognition?
>
> Conclusion
>
> The Traffic Police had justification for using AI cameras to suppress speeding, but were unethical to provide real-time access to the collected data to the OSCB. There are three independent ways to reach this conclusion, Kant's two formulations, rule-utilitarian test, and the negative-right analysis of the social contract and only one theory supporting the exchange, act utilitarianism, is inherently weak when it comes to the question of who pays the cost.

</details>

读稿时按下面顺序检查“它想完成什么”和“这一步证据是否足够”。这些是本次复盘，不是教师评分。

1. Q1 第一段正确拆出 A 与 B，并提前给立场。它说 “three ethical theories”，后文实际同时写行为功利主义、康德主义、规则功利主义、社会契约论和德性伦理；计数/归类应解释清楚，不能靠数字增强说服力。
2. 行为功利主义段想先处理安全收益，再讨论分配。问题在于 “meaning lower number of deaths and injuries” 把可能联系写成已知结果；“costs…appear to be small” 没有成本数据。§3.1 示范了怎样保留支持理由又承认净效用未知。
3. 康德段把“司机知道摄像头存在”当双重检验都通过，也把未经通知转用直接当概念矛盾。§3.2 解释了缺少用途保证前提、告知事实和公共执法条件；不能把后果很坏等同逻辑自毁。
4. 规则功利/契约/德性段把多种理由挤在一起。“Fewer arrests cannot outweigh it” 是原稿原句，语义也不够清楚，不能改引成不同英文。“无比例评估、无法院命令、无告知”均不由 complies 推得。消极/积极权利的教学分类不等于绝对优先级。§3.3–§3.5 给出更稳妥的条件分析。
5. Q2 的 “don't have to face speeding drivers anymore” 超过了下降 90% 的事实；Q3 的 “90%+ who don't speed” 混淆分母，accuracy 被改称 precision，也把识别错直接变成误罚。Q3 中特定群体、举证转移和社会失信未获本题证实，今后应改为待检风险。纠正方法在 §1.1 和 Q2/Q3。
6. Q4 提供了与目标相连的具体改法，是可复用的结构；但车牌能否归责、当地是否要求法院/隐私监管批准要核。Q5 每条都接论证前提，也应继续保留不确定性，见本篇 Q4/Q5。
7. 结论清楚表态，但“只有一种理论支持”“三条独立路径”不等于已经证明。应解释各理由的前提，并承认有充分保障时可能重判；不能靠四比一盖过未解决事实。

本节的意义是学会识别论证中的证据缺口，不据此改写本人已提交状态、成绩或实际课堂参与经历。原稿的 “as was discussed in the class” 只能作为原稿文字保存，不能由本轮资料复盘证明本人当时到课或发言。

## 8. 换一个案例，检查能否迁移

💡 笔记补充案例，不是课堂原题：某大学为防网课考试作弊，要求全程开摄像头与麦克风、记录屏幕，用视线追踪和人脸识别（准确率 98%）标记“可疑行为”。被标记者成绩暂扣、需自证清白。一学期后作弊举报下降 70%。随后学生事务处要求获取录像排查校园欺凌，教务处同意；两个月后据此处理 3 起欺凌事件。

尝试按本篇顺序写五问：先分监考决定 A 和反欺凌转用 B，再列已知/未知、双方理由、替代方案和信息缺口。特别检查：98% 的分母是什么；举报减少是否等于作弊减少；暂扣与自证给谁造成负担；B 是否有比全部录像访问更窄的办法。不要先看答案。

<details>
<summary>参考答案与改条件例</summary>

Q1：防作弊和反欺凌都有合理目的，但不能由举报下降或处理 3 起事件直接批准全程采集和转用。成绩暂扣且需自证是本题明示程序，与交通题“申诉未知”不同，可以直接分析它给学生增加的负担。后果视角比较公平考试收益、错误指控和隐私代价；尊重与契约视角检查学生能否知悉、质疑和得到救济。建议在保障不足时限制采集和转用。

Q2：诚实学生、教师、潜在欺凌受害者可能受益；已处理 3 起是事实，但具体减少多少伤害未知。Q3：被全程记录者承担隐私暴露，误标者可能失去及时成绩或付出自证成本；特定群体是否更容易误标仍需数据。98% 识别准确率不能直接变成 2% 学生作弊误判率，举报减少也可能来自举报渠道或行为变化。

Q4：比较开卷/口试、降低采集字段、限定保存、人工核查后再处理成绩、清楚申诉；反欺凌需求可先按具体事件和时段调取，经适当独立批准并留痕。每个方案需验证是否仍能保障考试与学生安全。Q5：要问准确率测试、误标到暂扣的流程、实际申诉、录像用途告知、访问权限和替代方案效果；每项分别影响后果、尊重或程序评价。

改条件：若学校原先清楚说明特定严重欺凌事件可限时调取录像，且独立复核后才允许访问，那么“完全未告知转用”的反对前提减弱；但错误标记与成绩暂扣的问题仍在。若又把成绩规则改为人审、提供证据、先让学生回应，程序公平会改善；仍不能只因存在告知就认定全部监控必要。

> The two decisions require separate assessments. Reduced reports do not establish reduced cheating, and recognition accuracy is not the rate of false cheating accusations. Targeted access, human review and a meaningful appeal may reduce harm, but their effectiveness and proportionality still need evidence.

</details>

自检时能说出“哪条事实影响哪条判断”比给所有理论凑相同立场更重要。本篇不替本人勾选已学会或自测通过。

## 9. 待回填与来源限制

- 成绩与评语沿用既有待核，不因重审推测教师评价。
- 若取得教师讲评或官方范例，先核真实原话/页码，再比较与本参考分析的不同；目前未取得。
- 本次核本地 M02 讲义、相关已有转录片段及真实提交 PDF，未重新核 Canvas 四入口，未重听原音。
- 法域、实际通知、授权、访问范围、误罚、人群数据和替代方案效果均未提供；学习参考不会把它们补成事实。

## 10. 参考索引与材料地位

| 内容 | 可回源位置 |
|---|---|
| 完整案例、五问、1–2 页与 9/22 中午 | M02 讲义 p.10–11、p.85–86；本篇 §0 |
| 论证判据与康德 | M02 p.12–13、p.30–33、p.78；本篇 §2、§3.2 |
| 行为/规则功利、分配批评 | M02 p.46–47、p.52–56；本篇 §3.1、§3.3 |
| 契约、权利与德性 | M02 p.58–61、p.64–75；本篇 §3.4、§3.5 |
| triangulate 一词与课堂方法 | `M02-transcript-part3.txt` 40:35 及周边；ASR 未逐声核 |
| 真实已提交原文 | `assignment/graded/A01-traffic-camera/submission/IS5113_Assignment1_60234350.pdf` p.1–2 |
| 行政历史与个人状态 | [[IS5113_AI_Ethics_and_Regulations/_meta/作业与DDL\|作业与 DDL]]；本篇 frontmatter 沿用 |

本次参考分析由 OpenAI Codex 辅助整理；此说明属于学习笔记，不追改 2026-09-22 的历史提交件及其披露。
