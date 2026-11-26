---
course: EF5560
module: M12
week: null
date: null
source:
  - course_files_export/canvas-20261126-review/Lec12_Robo_Cybersecurity_and_RegTech.pdf（40 页）
transcript: pending
prerequisites: [M01, M02, M03, M04, M05, M09, M10, M11]
new_concepts: [Robo-advising, Capacity for loss, Operational resilience, RegTech, Sanctions screening]
tags: [EF5560, 智能投顾, 网络安全, RegTech, 金融文本]
status: v0.9
updated: 2026-11-26
readability_rules: v2
teaching_standard: novice-v1
---

# M12 · 智能投顾、网络安全与监管科技

本篇按最新 40 页 Lec12 逐页解释。没有把其他课转录或考试公告当作本讲录音，课堂实际讲到哪页仍待核。题目的答案均标明参考推断；笔记制作不代表本人已练习或掌握。

## 0. 三分钟速览

本讲反复问同一个问题：软件产生一个建议、警报或摘要以后，金融机构还要核实什么，才能对客户采取行动？

学完应能：

- 对一个明年要买房的客户，分清想冒多少风险与实际能承受多少损失，说明为什么问卷高分不能直接变成高股票权重。
- 将股票权重从 50% 调回 40%，算出两边交易与成本，并说明再平衡为何不依赖预测涨跌。
- 沿网络事件追踪资金损失与服务中断，解释备份隔离和恢复测试分别解决什么。
- 对制裁名单同名警报，列出还缺的身份依据、应复核的证据及未解疑点的处置。
- 改正 LLM 财务抽取中的单位和可得时点错误，读出赎回资格与处理时间，保留未给出的到账时间。

## 1. 开始之前 · 知识衔接

### 1.1 需要唤醒的知识

下面每行是本讲将实际用到的一项旧知识。回链供深读，当前关键操作仍在 §2 重新说明。

| 概念 | 当前需要的一句话 | 既有入口 |
|---|---|---|
| 权重、收益与成本 | 权重是某资产价值占组合总值的比例；买卖金额和成本必须使用同一个总值作分母 | [[EF5560_Fintech_and_AI_in_Finance/notes/M05-可解释机器学习与投资组合决策\|M05]] |
| 数据可得时点 | 预测时只能用当时已公布的信息，财报所属年度不等于公众知道它的日期 | [[EF5560_Fintech_and_AI_in_Finance/notes/M01-金融数据与Vibe-Coding\|M01]] |
| 样本外评价 | 先用早期资料定方法，再在后来的未用于选方法的记录上比较误差 | [[EF5560_Fintech_and_AI_in_Finance/notes/M02-回归与样本外设计\|M02]] |
| 赎回与支付 | 发起赎回、发行人处理、银行实际到账和收款方可使用现金是不同环节 | [[EF5560_Fintech_and_AI_in_Finance/notes/M09-稳定币与中央银行数字货币\|M09]]、[[EF5560_Fintech_and_AI_in_Finance/notes/M10-支付系统与嵌入式金融\|M10]] |

### 1.2 本讲新概念

智能投顾（Robo-advising）是持续投资服务，展开于 p.5–14；亏损承受能力（Capacity for loss）取决于现金用途、期限和其他资源，展开于 p.8–9。网络安全的保密性、完整性和可用性在 p.19 区分；运营韧性（Operational resilience）在 p.26 解释如何恢复关键服务。监管科技（Regulatory technology, RegTech）在 p.29–35 连接身份、交易与名单核验。LLM 是大语言模型（Large language model），本讲使用它读取金融文本，而不把它的草稿当已证实事实。

### 1.3 三条使用路线与来源编号

本篇所有 p. 均指 `canvas-20261126-review/Lec12_Robo_Cybersecurity_and_RegTech.pdf` 的物理页，印刷页号与物理页一致；封面与分隔页没有印刷号。没有跨页改序。

- 预习：顺读 §2；遇到 p.16、27、35 先自己选，再读解析。p.36–38 的给定文本都是假设，不需要另找真实基金来替换。
- 课中：通过 §8 每页一行的精确链接到达当前页，原图在相应解释旁。无转录，未推断老师跳过哪些页。
- 复习：用 §4 找易混概念，再做 §7；答错时沿回链回到具体源页。U14 对应 p.2–16，U15 对应 p.17–38，p.39–40 串联全课。

## 2. 正文 · 按课件逐页跟读

### 2.01 p.1 · 本讲研究三种金融服务判断

封面题为 “Class 12: Robo-Advising, Cybersecurity, and RegTech”，作者 Gavin Feng，Semester A 2026/27。它将投资建议、安全响应与合规复核放在同一讲。下面分别检查每项服务的输入、动作、费用与责任；封面本身没有练习或新的行政要求。

### 2.02 p.2 · 智能投顾部分入口

“Robo-Advising and Investment Decisions” 是纯分隔页。接下来先解释小投资者的问题，再讨论软件能做与需要人工判断的步骤。实质内容从 [[#2.03 p.3 · 散户投资有三类障碍|p.3]] 开始。

### 2.03 p.3 · 散户投资有三类障碍

散户（Retail investor）是以个人资金投资的客户。第一类障碍是服务门槛：咨询费和最低投资金额可能让小账户用不起个人投顾。第二类是实际行为：看到最近上涨就追买，看到下跌就恐慌卖出，会使实际拿到的收益偏离原本计划。这里讲行为风险，不等于每次买入上涨资产都必然亏损。

第三类是组合不合身。投资组合（Portfolio）是同时持有的一组资产；“平衡型”标签没有告诉我们客户何时用钱、要用多少、用哪种货币。一个退休目标与明年首付即使账户金额相同，也可能需要不同配置。智能投顾的价值因此要从降低成本、减少重复操作和匹配客户需要分别检验。（讲义 p.3）

### 2.04 p.4 · 小账户收入为什么可能覆盖不了服务成本

课件给出的费率是资产每年 0.25%。用小数 0.0025 乘账户资产，才是美元收入：

$$\text{年管理费}=\mathrm{US\$}1{,}000\times0.0025=\mathrm{US\$}2.50.$$

这里的 US\$1,000 是客户账户金额；US\$2.50 是服务商一年的管理费收入，不是客户投资回报。即使客户资金很少，机构仍要核验身份、答疑和留合规记录。这些工作不会随资产规模同比例缩小。

标准组合、自动存入和自动再平衡能减少每个账户重复劳动，降低服务成本。但成本未必降到每年 US\$2.50 以下，因此课件说最低费用仍可能有必要；没有给实际公司利润，不能据此声称某公司的小账户已经盈利。（讲义 p.4）

### 2.05 p.5 · 智能投顾是一条持续服务链

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/m12/lec12-p05.png]]

按原图左上、右上、左下、右下读四格。第一格 “Understand the client” 收集目标（Goal）、期限（Horizon）与风险意愿；第二格 “Propose a portfolio” 将股票、债券和现金组成建议。股票（Stocks）代表持有企业权益，债券（Bonds）通常代表向发行人提供资金形成的债权；现金便于近期支出，但配置含义仍取决于具体产品。

第三格先有客户同意，再由托管人（Custodian）保管资产并执行开户等安排。托管解决资产如何持有的问题，选择权重的算法本身不会替代托管。第四格比较目标权重和当前权重，持续监测与再平衡（Rebalancing）；右侧 “Human support” 提醒需要人工支持。

图中的箭头表示服务推进，不保证收益。假设客户原目标是十年后退休，后来失业，第四格必须回头核现金需要，不能一直照旧买入。图为教学式服务设计，并非某公司的实证操作截图。（讲义 p.5）

### 2.06 p.6 · 自动化和人工分别处理什么

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/m12/lec12-p06.png]]

原页左右两列之间是加号，表示互补。左侧三项：开户接入（Onboarding）收标准客户信息；组合维护按同意的权重监测和调整；日常服务发提醒、保存记录。右侧三项：答案矛盾时澄清特殊需要；情况改变时重估目标、期限和现金需要；遇特殊决定时解释选择并讨论顾虑。

例如 app 能自动收集“明年买房”和“能承受大跌”，但这两个答案冲突。系统把两项都收齐，不等于已经解决冲突。先请客户说明首付金额和其他储蓄，再决定是否改变建议或交顾问复核，才完成右侧职责。（讲义 p.6；该小例连接 p.9）

### 2.07 p.7 · 从目标到监测，每一步都有条件

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/m12/lec12-p07.png]]

从左到右读原图：目标（GOAL）先给期限、流动性与币种。流动性（Liquidity）在这里指需要时能否及时取得可用现金；“十年后用钱”和“下月付学费”对可等待程度的要求不同。风险（RISK）同时问愿意承担与能够承担多少。假设（ASSUMPTIONS）包括市场输入和配置约束，并要确定谁批准这些假设。

组合（PORTFOLIO）才进入资产配置（Allocation）和产品选择，并核费用与利益冲突：例如机构是否因卖某产品额外获利。监测（MONITOR）检查权重偏离及需要上报人工（Escalation）的情况。箭头不能理解成客户填一次问卷就永久结束；监测发现失业或用途变化，要回看前面的输入。

“Conditional recommendation” 的意思是建议依赖客户资料和明确假设。同一客户的现金需求一变，条件就变了；模型输出不能脱离条件被称为无条件的最佳组合。（讲义 p.7）

### 2.08 p.8 · 风险能力怎样影响股债比例

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/m12/lec12-p08.png]]

原图左侧是收入稳定、目标遥远的情境，示例配置为 80% 股票、20% 债券；右侧是短期目标和现金需要，示例是 20% 股票、80% 债券。中间的不等号强调两类需要不同，不是让所有人按年龄或期限机械套用这两组比例。

风险意愿（Willingness to take risk）是主观愿不愿接受波动；亏损承受能力（Capacity for loss）是发生损失后能否仍满足必要支出。近期要用的钱一旦亏损，未必来得及等待价格恢复。长期目标、稳定收入和其他资源可能增加可承受空间，但不能推出股票必定在期限内回本。

图中的配置都是教学例。债券也可能有价格、信用、货币和流动性风险，80% 债券并不等于首付被保证。实际税项、币种、产品可得性和支出时点都能改变答案。（讲义 p.8；债券风险提示为笔记补充）

### 2.09 p.9 · 问卷高分怎样与明年首付冲突

客户说跌 20% 也可以接受，这是意愿；同一笔钱明年用于买房首付，这是用途约束。若账户有 100 万，跌 20% 后只余 80 万，客户的心理接受不会自动补回少掉的 20 万。这一数额例是笔记补充，不是课件新增报价。

课件要求进一步问：需多少首付、确切何时付、还有多少储蓄、买房能否推迟。若首付无法延期且没有其他资金，就要先把首付与可长期投资的钱分开。若另有充足安全资金，则可能得到不同判断。不能把“问卷分数高”当作化解矛盾的方法。（讲义 p.9）

### 2.10 p.10 · 再平衡先算交易，再算成本

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/m12/lec12-p10.png]]

原表每行是一类资产；Target Weight 是同意的目标，After Market Gains 是涨跌后的当前占比。股票目标 40%、当前 50%，债券目标 60%、当前 50%。股票占比过高 10 个百分点，要卖掉组合总值的 10% 股票，买入等额债券，才能在未扣成本的总值下回到 40/60。

💡 换个说法（笔记补充）：设调整前总值 HK\$100,000，股票 HK\$50,000、债券 HK\$50,000。卖 HK\$10,000 股票，股票余 HK\$40,000；将所得 HK\$10,000 买债券，债券为 HK\$60,000。交易前后使用相同的 HK\$100,000 总值，所以能核出 40% 和 60%。

基点（Basis point, bp）是百分之一的一个百分点，1 bp = 0.01%，10 bp = 0.1% = 0.001。课件假设每一笔购买或出售都付 10 bp，费率乘的是各自交易金额：

$$\text{组合成本比例}=0.001\times(0.10+0.10)=0.0002=0.02\%=2\text{ bp}.$$

在 HK\$100,000 的例子中，卖出成本 HK\$10、买入成本 HK\$10，合计 HK\$20。10% 是卖出交易金额占比；买、卖总成交占比是 20%，不等于股票权重改变 20 个百分点。费用实际扣除后组合总值减少，精确净权重须按扣费与资金安排重算；课件 40/60 是成本前说明。

再平衡的理由是恢复客户同意的风险配置，并不要求预测哪只股票下一步上涨。更频繁调整可能减少偏离，却增加累计交易成本。这 10 bp 是课堂假设，不能移作 Betterment 当前实际每笔收费。（讲义 p.10）

### 2.11 p.11 · Betterment 卖的持续服务

Betterment 案例从小客户需要分散投资及持续维护出发。分散（Diversification）是把资金分到不同资产，降低单一资产问题对全部资金的影响；它不保证市场整体下跌时没有损失。数字账户把目标与偏好转成组合，再自动存入与再平衡。

客户付的是持续管理费用。服务商要让每年的监测、维护和支持价值足以让合适的客户继续留下。目标复杂时，人工咨询可能有额外价值；这需要看具体客户，不是“用了 AI 就比顾问强”的结论。（讲义 p.11；课件所引公司资料日期为 2026-10-13）

### 2.12 p.12 · 固定金额与按资产收费怎样比较

课件 Digital 方案：达到条件时年费 0.25%；未达家庭余额与定期存入门槛时每月 US\$5。门槛为家庭余额 US\$24,000，或至少每月 US\$200 的定期存入，任一满足即适用 0.25%。Premium 要求至少 US\$100,000 投资余额，首 US\$1m 的年费 0.65%，并可接触认证理财规划师（Certified Financial Planner, CFP）。

💡 换个说法（笔记补充）：假设余额始终 US\$1,000，全年均按月费，US\$5 × 12 = US\$60，占余额 6%；达到百分比资格时，0.25% × US\$1,000 = US\$2.50。这里 6% 是固定余额下的费用占比，不是收益率，也没有把每月新增存入当作免费。余额 US\$24,000 时 0.25% 的年度金额恰为 US\$60，但实际资格仍按官方规则而非这条等式判断。

🔗 [Betterment 费用说明](https://www.betterment.com/help/fees)，2026-11-26 回读，页面标 2026-06-18 更新，支持上述条件及价格。官网也区分基金自身费用；本页不是某客户全部实际成本账单。p.4 的纯 0.25% 教学算例与本页未达标月费情境要分开。（讲义 p.12）

### 2.13 p.13 · 扣费后价值来自哪些动作

再平衡能保持约定的风险敞口（Risk exposure），即组合承受哪种风险、承受多少；这项服务可以在不预测赢家的情况下成立。税损收割（Tax-loss harvesting）是通过实现符合条件的投资损失来处理税务结果的服务；是否有价值取决于客户适用税制、交易与个人情况。本讲没有税额输入，不计算税收节省。

客服、税务相关操作和账户维护都是运营任务，都会有成本。若客户近期需要现金，先重新核配置是否适合，再考虑继续服务的价值。不能只用历史毛收益证明每个客户付费都划算，也不能把某个税务功能当成全球客户都有同样利益。（讲义 p.13；无本讲转录，不将 “classroom analysis” 写成教授口述）

### 2.14 p.14 · 投顾治理会回到客户生活变化

适当性（Suitability）问建议是否符合这个客户的条件：明年首付需要可能与高股票权重冲突。持续监测（Monitoring）不仅看价格，失业可能让原本能等待的钱变成生活费；应重新核资金需要、调整配置并记下理由。

人工建议（Human advice）处理矛盾与变化，例如先询问还能维持多少月支出，而不是仅重跑同一份风险分数。Betterment Premium 提供规划师接触渠道是公司服务；首付和失业是课件示例，不能写成公司已发生的客户个案。（讲义 p.14）

### 2.15 p.15 · 余额宝：分销便利不改变产品权利

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/m12/lec12-p15.png]]

原表一行拆一个层次。Launch 是支付宝和天弘基金于 2013 年 6 月推出，Access 是一元门槛和 app 内申购或取出。Product 是嵌入支付场景的货币市场基金（Money market fund）敞口，也就是客户资金随基金资产表现承担相应收益和风险。Distribution 是高频支付生态触点，Risk 列出流动性、集中、客户理解与平台权力。

平台把产品带到客户面前，基金管理人管理投资，二者职责不同。客户每天支付时都能看到入口，可能降低获客摩擦并形成习惯；这解释分销的重要性，不证明组合技术特别新。界面像钱包，所持有的仍可能是基金权益，不能因此读成银行存款。

“一元”和“2013 年 6 月”按课件历史案例理解。规模扩大时，客户同一时间取款、操作故障或误解产品性质的影响也扩大；方便不能消除流动性与运营风险。课件只给 Ant Group 公司时间线，不提供真实基金净值、财报或本人的适用条款，本文不另造这些数字。（讲义 p.15）

### 2.16 p.16 · 原题：风险偏好与亏损能力

先看关键条件：多数投资资金一年后用于买房，建议却只依据一项高风险意愿。

> **Multiple-Choice Question: Risk Preference and Capacity for Loss**
>
> A client selects high risk tolerance in an app, but needs most of the invested money for a house purchase in one year. The robo-adviser recommends an equity-heavy portfolio based only on that answer.
>
> What should the adviser reconsider first?
>
> A) Whether a higher expected equity return is enough to offset the cash requirement.
>
> B) Whether a cheaper fund removes the need to assess the client’s time horizon.
>
> C) The short horizon and cash requirement limit the client’s capacity to bear losses, regardless of stated preference.
>
> D) Whether using an automated questionnaire makes the recommendation suitable by itself.

中文题意：客户在 app 选了高风险偏好，但多数钱一年后必须买房。只凭偏好配置大量股票，顾问首先应重新考虑什么？`most` 表示大部分资金受约束；`one year` 给短期限；`based only` 指出缺失其他条件。

⚪ 参考作答（笔记推断）：选 C。即使愿意接受下跌，首付仍需按时凑足；应先核实际亏损能力与现金需要，再谈配置。

- A 把较高的预期收益当作现金保障，忽略预期不保证实现。
- B 降费可能改善净结果，却不会消除明年用钱的期限约束。
- C 同时抓住短期限和必要现金，正是题面缺失的评估。
- D 自动问卷是收集信息的方法，不能自行证明建议适合客户。

英文参考答案：**C. The short horizon and cash requirement constrain the client’s capacity for loss even if the client states a high willingness to take risk. The adviser should clarify the cash need before proposing an equity-heavy allocation.**

改条件（笔记补充）：若首付已另放在充足的低风险资金中，此账户是十年不用的钱，就不能继续用“同一笔首付”拒绝一切风险；仍须核其他条件。本题未给这个事实，不能擅自补入。

### 2.17 p.17 · 网络安全部分入口

“Cybersecurity” 为纯分隔页。接下来从热钱包事件看一项技术问题怎样变成财务损失和客户无法使用服务，再学习恢复与检测的取舍。实质案例从 [[#2.18 p.18 · 同一网络事件有资金损失与服务中断|p.18]] 开始。

### 2.18 p.18 · 同一网络事件有资金损失与服务中断

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/m12/lec12-p18.png]]

热钱包（Hot wallet）联网以支持转账和提现。原图从左至右：钱包基础设施被攻破 → 未授权资金外流约 US\$6.3bn（63 亿美元）→ 暂停提现、客户使用受影响。箭头表示事件传播的因果链；财产损失和暂时取不了钱是两个结果。

课件以香港时间 2026-10-30 Binance 事件为例，并写其承诺用 SAFU 与自有资金承担损失。SAFU 是用户安全资产基金（Secure Asset Fund for Users），这里承担损失缓冲角色。赔偿承诺不会自动让受影响系统安全恢复；恢复提现也不自动证明所有冻结资产已取回。

🔗 [Binance 官方事件更新](https://www.binance.com/en/square/post/382790902938294)，2026-11-26 回读，支持约 US\$6.3bn、资金承担、暂停提现及当时未发现私钥泄露证据。这里保留**当时调查口径**：没有发现证据不等于已证明私钥绝不泄露，也不等于攻击序列已经最终查清。课件的机制分析不依赖擅自补出攻击者身份。（讲义 p.18）

### 2.19 p.19 · 保密、完整、可用分别保护什么

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/m12/lec12-p19.png]]

原图左侧盾牌围住金融信息，下面三词是保密性（Confidentiality）、完整性（Integrity）、可用性（Availability）。盾牌内的 “20%” 是插图元素，没有统计来源，不能当风险概率或实际收益。右侧三个问句给出本页判断标准。

💡 换个说法（笔记补充）：银行转账 HK\$1,000。无权者读到客户资料，损害保密性；把转账金额改成 HK\$10,000，损害完整性；客户无法打开系统完成转账，损害可用性。同一攻击可以同时损害三项，强加密也未必解决系统停机。

金融服务连接资金、身份、应用程序接口（Application programming interface, API）和外部供应商。API 是系统之间提交请求和接收结果的接口；权限若过大，一个被盗账户可能通过接口影响多个系统，因此失败会跨服务扩散。（讲义 p.19）

### 2.20 p.20 · 遏制、追踪冻结与恢复不可互相替代

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/m12/lec12-p20.png]]

沿原图从左至右读：遏制（Contain）撤销相关访问授权、隔离受影响系统，先防继续外流；追踪与冻结（Trace and freeze）识别地址、在具备条件时冻结代币；恢复（Restore）检查系统后分阶段重开。冻结使资产暂时不能被转走，正式追回还需后续程序，不能当作已经回到账户。

课件记载 11 月 1 日安全检查后公布分阶段开放。🔗 [Binance 官方后续更新](https://www.binance.com/en/square/post/384133235759486)，2026-11-26 核对，回顾 11 月 1 日第一阶段并宣布 11 月 3 日扩大提现范围，支持“分阶段恢复”而非“立即全部正常”的读法。课件本页记录的是当时阶段，不据此宣布截至今日所有风险清零。

事故前的权限限制、额外认证和交易监测属于一般预防控制：限制能做什么、验证操作者、发现异常转账。它们与事故后复原配合，不能因有赔偿基金就省略。（讲义 p.20）

### 2.21 p.21 · 香港事件图：总量与占比要分开读

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/m12/lec12-p21.png]]

左图横轴是 2024、2025 年，纵轴是香港电脑保安事故协调中心（Hong Kong Computer Emergency Response Team Coordination Centre, HKCERT）收到的事件报告数：12,536 → 15,877。增量为 3,341，以 2024 年作分母，增幅约 26.65%，课件取整为 27%。这是报告总数，不是金融机构损失额或全港所有实际攻击的普查。

右图每条整条代表该年的全部报告。蓝色网络钓鱼（Phishing）占比 62% → 57%；绿色僵尸网络（Botnet）23% → 18%；红色恶意软件（Malware）8% → 15%；灰色其他 7% → 10%。网络钓鱼用假信息诱使人交出凭据或付款；僵尸网络是被控制设备组成的网络；恶意软件是执行有害动作的软件。课件各比例为舍入数，其他内含细分类别，不能据图精确反推每类件数。

网络钓鱼占比下降不表示件数一定下降：总数同时上升。单用舍入比例估算，12,536 × 62% 约 7,772，而 15,877 × 57% 约 9,050，已足以说明这种可能性；这两个估算不是官方精确分类计数。恶意软件份额增加 7 个百分点，也不等于仅增加 7%。

金融上的读法是警惕账户凭据、终端与共享基础设施，不能把全经济统计直接当银行攻击概率。🔗 [HKCERT 2026 展望发布](https://www.hkcert.org/press-centre/hkcert-releases-hong-kong-cybersecurity-outlook-2026-security-incidents-hit-record-high-with-27-annual-increase-ai-related-attacks-and-supply-chain-risks-emerge-as-top-concerns-nearly-30-of-enterprises-lack-dedicated-cybersecurity-personnel)，2026-11-26 核对，支持 2025 年 15,877 宗及约 27% 增长。（讲义 p.21）

### 2.22 p.22 · Darktrace 解决的是调查资源不足

银行每天产生登录、网络通信、文件下载等活动日志。员工来不及逐条检查，固定的已知攻击规则也可能漏掉没见过的模式。邮箱和网络工具互不连接时，同一事件的线索还会分散。

Darktrace 的产品叙述是学习正常行为，找出异常并协助调查。异常检测（Anomaly detection）先问“与平时不同在哪里”，不等于已经证明恶意。银行买的是更早发现问题和可用的调查支持，要通过客户试用检验产品声明，不能用“用了 AI”代替效果证据。（讲义 p.22）

### 2.23 p.23 · 一次异常下载怎样从线索走到判断

课件假设某员工账户突然下载远超平时的客户记录。软件可以标出数量异常、新设备以及跨系统的相关活动；调查人员仍要核是谁批准导出、账户是否被盗、哪些资料已离开、还有哪些动作能阻止。

例如合法迁移也可能造成大量下载，低频攻击也未必很显眼。先限制可疑会话或设备、保全日志并核审批记录，比单凭“异常”就认定员工攻击更合适。限制范围应与证据相称，同时维持无关服务。此处是课件假设银行情境，不是 Darktrace 已被证实阻止的真实事件。（讲义 p.23）

### 2.24 p.24 · 警报从 100 降到 20 为什么还不够

课件要求把可疑会话或设备限制住，让未受影响的支付继续；恢复访问前保留日志并复核。试用软件时要同时比较漏掉的事件、错误警报、员工耗时和服务中断。

误报（False positive）是本来合法却被报为可疑；漏报（False negative）是真实问题未被报出。每日警报 100 → 20 可能省工，也可能只是把阈值提高，连严重攻击一并忽略。要核减少的是无用提醒还是有用线索，不能只看总数。

💡 换个说法（笔记补充）：若每条需 5 分钟，100 条是 500 分钟，20 条是 100 分钟，名义节省 400 分钟；但如果少掉的 80 条包含唯一一次严重入侵，这个工时收益不足以说明服务更好。100、20 是课件示意，5 分钟是笔记假设，均不是客户试用实测。（讲义 p.24）

### 2.25 p.25 · 凭据、软件和供应商带来不同故障

第一类是被盗凭据（Stolen credentials）：钓鱼拿走员工登录资料，可能暴露客户记录；限制访问与额外认证减少暴露范围。第二类是软件漏洞（Software flaw）：课件用 2017 Equifax 未修补网页应用为例，说明延迟安全更新可能暴露信用与身份资料。

第三类是供应商故障（Vendor failure）：2024 年 7 月 CrowdStrike 更新使部分 Windows 系统中断。它说明即使没有恶意攻击，也要有可测试的恢复安排；依赖同一供应商的关键服务可能一起受影响。

三者分别引导我们问：谁能进来、软件弱点有没有修、外部依赖坏了怎么办。🔗 [CrowdStrike 技术说明](https://www.crowdstrike.com/en-us/blog/falcon-update-for-windows-hosts-technical-details/)，2026-11-26 核对，支持 2024-07-19 配置更新引发 Windows 故障。不要把这个案例改写成黑客入侵已成立。（讲义 p.25）

### 2.26 p.26 · 运营韧性以客户服务为验收对象

运营韧性（Operational resilience）问银行在严重中断时能否维持或恢复客户依赖的关键服务。先指定对象，例如客户完成付款；再定可容忍中断（Tolerance for disruption），包括最多可以停多久等限制；最后联合人员、系统和关键外部提供商测试恢复。

备份文件复制成功只说明有副本，没证明数据库能加载、权限可用、支付接口正常以及员工懂得切换。完整恢复测试应走到指定服务重新可用，并比较是否在容忍范围内；这里没有给任何机构统一的“允许停机几小时”，不能补一个当法定标准。

🔗 香港金融管理局（Hong Kong Monetary Authority, HKMA）的 [OR-2《Operational Resilience》](https://brdr.hkma.gov.hk/chi/doc-ldg/docId/getPdf/20220531-2-EN/OR-2.pdf)，2026-11-26 核对，版本 V.1，2022-05-31，支持识别关键运营、容忍中断和严重但合理情境下的测试。本文解释课件原则，不代某机构判定合规。（讲义 p.26）

### 2.27 p.27 · 原题：勒索软件以后怎样恢复

本题问“恢复能力”，先找导致两份记录一起失效的共同权限。

> **Multiple-Choice Question: Recovery after Ransomware**
>
> A payment firm keeps live records and backups under the same administrator account. An attacker takes over that account and encrypts both copies.
>
> Which change most directly improves the firm’s ability to recover?
>
> A) Maintain separately protected backups and test restoration regularly.
>
> B) Replicate records more often under the same administrator account.
>
> C) Encrypt the live database more strongly under the same access rules.
>
> D) Retain more login alerts without changing how backups are protected.

中文题意：支付公司把在线记录与备份交同一个管理员账户控制。攻击者夺取此账户，把两份一起加密。哪一项最直接改善恢复？勒索软件（Ransomware）在此通过加密让公司无法正常读取记录；已有副本也因同一权限一并失效。

⚪ 参考作答（笔记推断）：选 A。独立保护备份，减少同一次权限失守同时毁掉两份的机会；定期实际还原，验证剩下副本能恢复服务。

- A 同时处理副本的保护隔离与恢复可用性，直接对应题目。
- B 复制更频繁能缩短正常情况下的数据间隔，却保留同一账户可毁两份的原因。
- C 更强加密可能保护保密性，没有解决已被接管管理员的破坏权限和恢复来源。
- D 更多日志帮助发现或调查，但不使已被加密的备份自行可恢复。

英文参考答案：**A. Separately protected backups reduce the common point of compromise, and regular restoration tests check whether the firm can actually recover its service.**

改条件（笔记补充）：若备份已隔离但从未成功还原，也不能仅增加备份数量宣布韧性达标；下一步仍要测试还原与服务链。

### 2.28 p.28 · RegTech 与金融文本部分入口

“RegTech and Financial Text” 是纯分隔页。从 [[#2.29 p.29 · 同名只是需要核查的线索|p.29]] 开始，问题由系统是否异常转为记录中的人或陈述是否真实对应。最后 p.36–38 把这种核验方法用于 LLM 文本草稿。

### 2.29 p.29 · 同名只是需要核查的线索

课件示例：开户人姓名与制裁名单（Sanctions list）条目相同，出生日期却不同。银行真正要回答“申请人和名单中人是不是同一个人”。姓名相同是支持匹配的线索，生日冲突是反向线索；单凭其中一个字段无法自动完成核验。

软件的任务是比较姓名和身份标识，找可能匹配并展示证据。复核人员解决缺项和冲突、记录决定。监管科技（Regulatory technology, RegTech）帮助机构执行并记录这些检查，不能替银行免除决定责任。后文是课件工作流，不援引某国具体制裁法来扩大题目。（讲义 p.29）

### 2.30 p.30 · KYC、AML 与制裁筛查有不同对象

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/m12/lec12-p30.png]]

原图是合规（Compliance）仪表板的示意，KYC、AML ALERTS、REPORTS 等格子表示不同工作入口。图上的勾或叉是示意状态，不证明某客户通过核验或违法；本页右侧文字才给三类任务。

了解你的客户（Know your customer, KYC）核身份以及谁拥有或控制账户。反洗钱（Anti-money-laundering, AML）监测从交易中找需调查的异常。制裁筛查（Sanctions screening）把客户资料与相关名单比对，复核可能命中。

💡 换个说法（笔记补充）：开户时核身份证属于身份核验；开户后发现异常交易属于监测；名字像名单条目属于筛查。真实机构可能把流程连接，但“出现一条 AML 警报”并不等于已证实洗钱，“完成身份图像读取”也不等于完成全部 KYC。（讲义 p.30）

### 2.31 p.31 · 合规软件的价值要能追溯到工作和证据

机构面对很多客户和付款，人工时间有限。软件可自动取文件、匹配记录，把人力留给不确定案例；名单或客户信息更新后，旧决定也可能需要复查。每条警报和决定都要连回源记录，使另一人能重建当时为什么这样判断。

评价时比较每案复核时间、漏掉的案例和误报警报的额外工时。速度快却缺依据，或压低警报但漏更多问题，都不能单独证明价值。可追溯记录（Audit trail）在这里是从输入、版本到决定理由的链，不只是留一份 AI 摘要。（讲义 p.31）

### 2.32 p.32 · WeLab 开户效率连接怎样的经济问题

课件介绍汇立银行（WeLab Bank）为香港持牌数字银行，通过 app 提供存款、贷款与财富服务。贷款收入要覆盖资金成本、信用损失和运营成本；信用损失是借款人未按约偿还造成的损失。远程开户可能减少分行文书劳动，但没有给利润或节省金额，不能自行补百分比。

真实客户要顺利完成申请，同时缺失或冲突身份资料仍需复核。业务取舍是减少合法客户的无谓等待，并保留必要检查，不是审核越快越好。这里按课件公司情境说明，本讲没有账户申请或修改操作。（讲义 p.32）

### 2.33 p.33 · 从身份图片到开户决定

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/m12/lec12-p33.png]]

原页三列从左到右读：Capture 提交身份证件与必要同意；Check 核文件真伪与标识、比相关记录；Resolve 中图片不清就补清晰版，证据冲突就交复核。先读清证件上的字，再核字对应的人，是不同步骤，识别准确不代表真实性自动成立。

Persona 是课件列举的身份核验服务商。银行设决定规则并负责开户决定。课件明确说此页不是“WeLab 使用 Persona”的声明，因此只把它看作可能的服务分工：供应商提供工具，银行负责规则与决定。不能把教学并列变成真实采购关系。（讲义 p.33）

### 2.34 p.34 · 缺身份证号时还缺哪一步

本页假设名字近似名单、生日不同、证件号码还没核实。先把匹配字段和冲突字段都对源记录，再取得缺失证据，记下究竟哪条资料消除了疑点。按银行筛查规则作决定，未解决的疑点上报，不把相似姓名自动写成同一个人。

课件给出复核产能例：40 条警报待处理，当天只能复核 10 条，则仍有 40 − 10 = 30 条需要排序与临时控制决定。这 30 条是未处理工作，不是已证实违规数。AI 可汇总材料、帮助排序，最终身份问题仍要由证据解决；提高阈值让这 30 条“消失”不等于真的完成复核。（讲义 p.34）

### 2.35 p.35 · 原题：可能的制裁名单匹配

本题有一个匹配、一个冲突和一个缺项，不能只读姓名。

> **Multiple-Choice Question: A Possible Sanctions Match**
>
> A screening system flags a customer whose name matches a sanctions entry. The date of birth differs, and the record has no verified passport number.
>
> What is the best next step?
>
> A) Reject the customer automatically because the name matches exactly.
>
> B) Close the alert automatically because one field differs.
>
> C) Verify identity evidence, document the review, and escalate unresolved doubt.
>
> D) Raise the screening threshold for all customers to reduce similar alerts.

中文题意：系统因姓名匹配而警报，生日不同，护照号码未验证。`no verified` 是未核实，不能读成确定没有护照或确定身份不同。问下一步，不是要求此刻宣布客户清白或应拒绝。

⚪ 参考作答（笔记推断）：选 C。验证身份依据、记录匹配和冲突如何被核实、将仍未解决的疑点上报。

- A 把同名直接当同一身份，会造成错误拒绝。
- B 把单个不同字段直接当排除依据，忽视录入错误、资料质量和缺失标识。
- C 用补证、留痕、上报解决当前不确定性，符合 p.29–34 的工作流。
- D 改所有人的阈值只改变警报量，没有核实此客户身份，也可能增加漏报。

英文参考答案：**C. Verify the identity evidence, document how matching and conflicting identifiers were resolved, and escalate any remaining uncertainty. A name match alone does not establish identity, and one differing field does not by itself resolve the alert.**

改条件（笔记补充）：若后来取得可靠、可验证的完整标识，才按相应规则利用新证据决定；“取得新证据”和“全局调低警报”是两种不同动作。

### 2.36 p.36 · 原题：LLM 财务抽取漏了单位和公布时点

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/m12/lec12-p36.png]]

从左框到右框读：左侧是题目给定的假设文件，箭头上的 LLM 表示抽取动作；右侧标题已经写 “Draft — not yet checked”。以下保留题面，数字只用于这个教学例，没有真实基金名称。

> **Check an LLM’s Financial-Data Extraction**
>
> Hypothetical filing. First published 15 March 2026.
>
> “For the year ended 31 December 2025, revenue was HK\$120 million, compared with HK\$100 million in 2024.”
>
> Draft — not yet checked:
>
> 2025 revenue: 120
>
> Currency and unit: HK dollars
>
> Information available from: 31 December 2025
>
> Which fields need correction before using this record as a return predictor?

中文题意：文件于 2026 年 3 月 15 日首次公布，讲的是 2025 全年收入 HK\$120 million，2024 年为 HK\$100 million。LLM 把数值记成 120，单位记成港元，把可用日期记为年末。要把这份记录拿去预测收益，哪些字段必须修正？

⚪ 参考作答（笔记推断）：2025 年度与收入 120 这两个字段结合“百万港元”才正确；币种是港元（HKD），缩放单位是 million。也可存成 120,000,000 HKD，但不能把 120 与“港元”连成 120 港元。必须保留 2024 年 100 million 的比较数及各自期间。

可得日期要改为 2026-03-15，依据是 first published。2025-12-31 是报告期间结束日，不是市场当时已知数据的证明。原题只给日期，没给一天中的发布时间；实做日内交易或同日收盘预测时还要核时刻和决策时间，不能假设开盘前已知。

下面每行是一个要存的字段，右列给这个假设例的正确值。

| 字段 | 正确值与理由 |
|---|---|
| 2025 收入 | 120，缩放为 million；或 120,000,000，单位 HKD |
| 2024 比较收入 | 100 million HKD，期间 2024 |
| 报告期间 | 截至 2025-12-31 的全年 |
| 信息首次公开日期 | 2026-03-15，不能回填为 2025-12-31 |
| 可追溯依据 | 保存原句、来源与定位；当前只有教学假设文件 |

英文参考答案：**Record revenue as HK\$120 million for 2025 and HK\$100 million for 2024, preserving currency, scale and reporting periods. Replace the availability date with 15 March 2026. The accounting year-end does not establish when the information became public.**

若把 2025 年收入放进 2026 年 1 月的预测输入，就把当时尚未公开的未来信息偷带进模型，构成前视偏差（Look-ahead bias）。单位错误可能把量级缩小百万倍；时点错误则让历史测试看似提前知道答案。两者要分别检查。（讲义 p.36）

### 2.37 p.37 · 从抽取到增长率，再到真正的后期预测检验

课件续用同一假设：收入 HK\$100 million → HK\$120 million。先确保币种、缩放单位和期间可比，再算增长：

$$g=\frac{R_{2025}-R_{2024}}{R_{2024}}=\frac{120-100}{100}=\frac{120}{100}-1=20\%.$$

$R_{2025}$ 是 2025 全年收入，$R_{2024}$ 是 2024 全年收入，均以百万港元计；$g$ 是相对旧年收入的增长比例。单位相同在比值里消去，新增 20 million 除旧年 100 million，所以是 20%，不是 20 个百分点的利润率，也不是股票收益 20%。

课件的 Extraction 要求保存金额、期间和源句；Timing 要求自公布后才可用；Evaluation 要问它是否改善后期预测。不能因为提取正确或收入增长，就宣布股价会涨。

💡 换个说法（笔记补充）：假设有许多按真实公开时点对齐的历史记录，先用较早记录定模型和参数，再在较晚记录上同时比较“原模型”和“同设置加收入增长变量”的预测误差。两者测试对象、收益定义和基准一致，才看得出增加变量是否有帮助。用测试期反复挑最好的提取方式会把测试资料变成选方法的资料，不能再称独立后期检验。

英文参考说明：**Check the extracted values and timing first. Then compare forecasts on later observations from the same model with and without the extracted predictor. Accurate extraction alone does not establish predictive value.**

改条件：若旧年收入为 0，增长式的分母为 0，就不能照算百分比；若文件日后更正，应保存当时版本，不能把更正后资料静默回填到早期决策。本题未给这些情形，属于方法边界。（讲义 p.37；变式为笔记补充）

### 2.38 p.38 · 原题：赎回资格与现金到账

此页的发行人政策是课堂假设，不是实际发行人、基金或稳定币的条款。先保留 `Only`、`approved`、`Complete` 和 `processed`，它们各会改变判断。

> **Check an LLM’s Reading of Redemption Terms**
>
> Hypothetical issuer policy:
>
> “Only approved business account holders may request direct USD redemption. Complete requests received after 15:00 HKSAR time are processed on the next business day.”
>
> LLM draft — not yet checked:
>
> • Eligible customer: any token holder.
>
> • Cash available in the bank: next business day for requests after 15:00.
>
> Who is actually eligible? Does the passage specify when bank funds become available?
>
> Classroom policy, not an actual issuer’s terms. Connect the review to the Class 9 CFO and Class 10 supplier payment.

中文题意：只有获批准的企业账户持有人能直接申请美元赎回；香港时间 15:00 之后收到的完整请求在下个营业日处理。LLM 却写成任何持币人都可申请，并把“处理”写成“银行现金可用”。要分别回答资格与到账。

⚪ 参考作答（笔记推断）：第一问，合资格者是获批准的企业账户持有人（Approved business account holders），不是所有代币持有人；持有代币本身不足以满足账户与批准条件。第二问，原文只说完整请求在何时处理，没有给银行入账或现金可用时刻，因此不能确定到账日。

一句话中还有三个条件。`Complete` 指请求资料完整；资料不齐何时补齐及如何排队，原文没说。`after 15:00` 是晚于 15:00，不能推断恰好 15:00 如何处理。`next business day` 是下个营业日，不能把周末或假日一律当自然日下一天；本题没有完整营业日历。

为了看清支付依赖，下面按时间列步骤。前两行来自原文，后两行是为区分概念而列的待核环节，不是原文承诺。

| 步骤 | 本题能确定的事 |
|---|---|
| 身份与资格 | 须为获批准企业账户持有人，才可提出直接美元赎回 |
| 收到完整申请并处理 | 15:00 后收到的完整申请，在下个营业日处理 |
| 银行实际入账与现金可用 | 原文未给，需要其他真实结算与银行依据 |
| 供应商收款 | 还依赖付款提交、清算和收款方安排，不能仅凭赎回处理日保证 |

英文参考答案：**Only approved business account holders are eligible to request direct USD redemption. The passage specifies processing on the next business day for complete requests received after 15:00 HKSAR time. It does not specify when funds are credited to a bank account or become available.**

连接 Class 9 的公司财务负责人（Chief financial officer, CFO）现金安排和 Class 10 的供应商付款：如果周一必须支付供应商，不能仅因赎回将于某日“处理”，就记作当天可用银行现金。本讲不修改原作业，也不新造真实交易。（讲义 p.38）

### 2.39 p.39 · 一张分析画布怎样连起公司案例

“Canvas” 在本页是分析画布，不是网课平台的提交按钮。下面每行是一项应回答的问题及证据，六行共同描述同一服务。

| 原页问题 | 原页要求的证据 | 怎样读成分析动作 |
|---|---|---|
| Customer problem | whose friction or loss is reduced, and by how much? | 指出谁的等待、费用或损失减少；没数字就保留未量化 |
| Product workflow | what happens from the first click to settlement or service completion? | 从客户首次动作追到结算或服务完成，中途责任不省略 |
| Technology | which step genuinely requires data, AI, API, cloud, or blockchain? | 把技术放到具体步骤，并说明不用它会缺什么 |
| Economics | who pays, who funds the activity, and what drives contribution margin? | 分开付款人、资金提供者、收入与随业务变化的成本 |
| Risk and regulation | who can lose, which control should prevent it, and who is accountable? | 把损失对象、控制与责任连接，不只列风险名词 |
| Competitive advantage | what remains difficult for a bank, platform, or new entrant to copy? | 核真实难复制因素，不把一个功能名自动当壁垒 |

贡献毛益（Contribution margin）在这里看业务收入扣除随该项业务变化的成本，还剩多少支持其他成本；不能直接当公司最终净利润。比如投顾的客户问题是小账户服务难，流程从目标到持续维护，自动化减少重复劳动，收入是管理费，风险是建议不适合，优势要靠可证实的获客和服务能力说明。这个读法把六行串成一条证据链，避免写成公司年表与技术名录。（讲义 p.39；投顾串联为笔记补充）

### 2.40 p.40 · 全课两半分别在核哪一种主张

Classes 1–5 研究金融 AI：预测收益、比较预测误差、评价组合风险和交易成本。例如周股票超额收益（Excess return）是股票收益减同周无风险收益；零超额收益基准预测为 0，比较谁更少犯错，再看按预测做组合是否有净价值。它不是用随便一个价格作误差基准。

Classes 6–12 研究金融科技产品、收入成本与金融权利。课件对照 Aave 借款人欠的是债务，Kickstarter 支持者支持奖励型项目，不能写成购买企业股权。界面都能“付钱”，合同权利却不同。

因此复习时有两条检查：AI 的数字是否按正确时点、样本和基准检验；FinTech 的权利、流程、付费者、风险与责任是否说清。p.39 的画布和本页是综合复习入口，不提供正式期末许可、题量或新的作业提交要求。（讲义 p.40）

## 3. 一图看懂 · 软件输出之后的三条核验链

每行从左向右读，最后一列指出实际服务终点；这张总览表不能代替 §2 的原页与步骤。

| 服务 | 输入 → 软件动作 | 还要核什么 | 到哪一步才回答客户问题 |
|---|---|---|---|
| 智能投顾 | 目标/现金需要 → 组合建议 | 意愿与能力、假设、费用、客户同意 | 执行、托管、持续监测与必要人工复核 |
| 网络安全 | 活动记录 → 异常警报 | 是否攻击、受影响范围、漏报误报 | 遏制并保全证据，验证关键服务恢复 |
| RegTech | 身份与交易资料 → 可能匹配 | 标识冲突、缺项、源记录与名单版本 | 留痕作决定并上报未解疑点 |
| 金融文本 | 原文 → 抽取草稿 | 金额/单位/期间/公开时点、资格/处理/到账 | 正确数据后再评价预测或支付安排 |

## 4. 速查表 · 最容易混淆的六处

先遮住第三列，尝试用第二列事实自行判断，再回正文核理由。

| 对照 | 判定线索 | 本讲结论与回指 |
|---|---|---|
| 意愿 / 能力 | 说能接受大跌，但明年必须付首付 | 先核必要现金，[[#2.09 p.9 · 问卷高分怎样与明年首付冲突\|p.9]]、[[#2.16 p.16 · 原题：风险偏好与亏损能力\|p.16]] |
| 再平衡 / 预测 | 从 50% 股票调回目标 40% | 恢复风险配置，买卖双边共 2 bp 成本，[[#2.10 p.10 · 再平衡先算交易，再算成本\|p.10]] |
| 复制 / 恢复 | 两份资料共用已失守管理员 | 独立保护加实际还原测试，[[#2.27 p.27 · 原题：勒索软件以后怎样恢复\|p.27]] |
| 警报 / 证实 | 异常下载或名字相同 | 是待查线索，[[#2.23 p.23 · 一次异常下载怎样从线索走到判断\|p.23]]、[[#2.35 p.35 · 原题：可能的制裁名单匹配\|p.35]] |
| 期末 / 可得日期 | 2025-12-31 年结，2026-03-15 首次公布 | 输入时点从公布开始，[[#2.36 p.36 · 原题：LLM 财务抽取漏了单位和公布时点\|p.36]] |
| 赎回处理 / 到账 | 条款只承诺下个营业日处理 | 不推断银行现金可用日，[[#2.38 p.38 · 原题：赎回资格与现金到账\|p.38]] |

## 5. 双语术语卡

英文定义为笔记参考表述，供解释与复习，不冒称教师逐字标准答案。

| 中文 | English | 考试可用的英文定义 | 首现位置 |
|---|---|---|---|
| 智能投顾 | Robo-advising | A digital investment service that links client information to a portfolio and ongoing monitoring. | p.5 |
| 风险意愿 | Willingness to take risk | The degree of investment risk a client says they are willing to accept. | p.8 |
| 亏损承受能力 | Capacity for loss | The ability to absorb losses while still meeting required financial needs. | p.8–9 |
| 适当性 | Suitability | The fit between a recommendation and the client’s circumstances, goals and constraints. | p.14 |
| 再平衡 | Rebalancing | Trading to bring a portfolio back toward agreed target weights. | p.5、10 |
| 基点 | Basis point | One hundredth of a percentage point. | p.10 |
| 保密性 | Confidentiality | Restricting access to information to authorized parties. | p.19 |
| 完整性 | Integrity | Protecting data and instructions from unauthorized changes. | p.19 |
| 可用性 | Availability | Keeping a service accessible and operating when needed. | p.19 |
| 误报 / 漏报 | False positive / False negative | A benign case incorrectly flagged / a genuine problem missed. | p.24 |
| 运营韧性 | Operational resilience | The ability to maintain or restore critical operations through disruption. | p.26 |
| 监管科技 | Regulatory technology, RegTech | Technology that helps institutions perform and document compliance checks. | p.29 |
| 了解你的客户 | Know your customer, KYC | Verifying identity and understanding who owns or controls an account. | p.30 |
| 反洗钱监测 | Anti-money-laundering monitoring | Flagging unusual transaction activity for investigation. | p.30 |
| 制裁筛查 | Sanctions screening | Comparing customer details with relevant lists and reviewing possible matches. | p.30 |
| 前视偏差 | Look-ahead bias | Using information in a historical decision before it was actually available. | p.36 |

## 6. 考点预判与答题框架

没有本讲转录，本节没有“教授明示”项。讲义内原题只证明课堂材料有这些问题，不证明正式考试一定考。

| 可信度 | 能力与答题顺序 | 定位 |
|---|---|---|
| 🟡 ILO 反推 | 客户条件 → 意愿/能力冲突 → 补问 → 配置与复核 | p.7–16；复习 U14 |
| 🟡 ILO 反推 | 服务对象 → 事件传播 → 控制 → 恢复验证 → 费用/漏报误报取舍 | p.18–27；复习 U15 |
| 🟡 ILO 反推 | 匹配与冲突字段 → 缺失证据 → 复核留痕 → 上报未解疑点 | p.29–35；复习 U15 |
| ⚪ 笔记推断 | 原句 → 纠正字段 → 公开时点/资格/处理/到账 → 能确定和仍缺的事实 | p.36–38 |

英文短答可沿此结构写：**The relevant condition is ___. The software output is only ___. The institution should verify ___, because ___. It should record the decision and escalate any remaining uncertainty.** 空格必须填题目事实；答恢复题时把最后一步换成实际服务恢复测试，不能把所有题硬套成身份复核。

全课公司案例可按 p.39 六行组织。收益预测题仍用 M01–M05 的数据、样本和基准规则；本讲没有替换它们，也没有给两份 mock 的标准答案。

## 7. 自测 · 先作答再展开

### 7.1 两个客户都说能忍受 20% 下跌，组合是否应相同？

客户甲用这笔钱支付下年学费；客户乙已有独立学费资金，这笔钱十年不用。哪些事实改变判断？

<details><summary>参考答案与理由</summary>

风险意愿表述相同，亏损能力不同。甲的必要近期支出会被下跌影响；乙有其他资金、期限较长，可能有更多承担空间。仍需核收入、币种、金额与其他约束，不能自动断言乙应持有固定 80% 股票。回到 [[#2.08 p.8 · 风险能力怎样影响股债比例|p.8]]、[[#2.09 p.9 · 问卷高分怎样与明年首付冲突|p.9]]。

</details>

### 7.2 组合 HK\$200,000，股票从当前 55% 调回目标 50%

按每次购买或出售 10 bp，卖多少股票、买多少债券、成本多少？忽略扣费对目标权重的微小影响。

<details><summary>参考答案与理由</summary>

需卖股票占总值 5%，即 HK\$10,000；买债券 HK\$10,000。双边成本为 0.001 × (10,000 + 10,000) = HK\$20。占 HK\$200,000 为 0.01%，即 1 bp。不能只算卖方 HK\$10，也不能把源页 2 bp 不加判断照搬。回到 [[#2.10 p.10 · 再平衡先算交易，再算成本|p.10]]。

</details>

### 7.3 安全软件把警报降八成就值得续费吗？

<details><summary>参考答案与理由</summary>

还不能。要核减少了哪些误报，是否漏掉更多严重事件，调查耗时与对正常支付的中断如何变化。降低数量可能只是提高阈值，不能单凭数量证明质量。回到 [[#2.24 p.24 · 警报从 100 降到 20 为什么还不够|p.24]]。

</details>

### 7.4 KYC 完成、名字命中、生日不同，能否自动拒绝？

<details><summary>参考答案与理由</summary>

不能仅凭这些事实自动拒绝。要知道 KYC 实际核了哪些资料，比较匹配和冲突，补核身份标识，记录依据并上报未解疑点。一次流程标签不能替代本次证据。回到 [[#2.35 p.35 · 原题：可能的制裁名单匹配|p.35]]。

</details>

### 7.5 财报 4 月公布，讲的是去年；赎回条款说下日处理

能把收入放进今年 1 月预测吗？能把赎回处理日写成供应商一定收到现金之日吗？

<details><summary>参考答案与理由</summary>

两者都不能。去年所属期不使尚未公布的收入提前可得；处理赎回没有给银行可用资金或供应商到账时间。前者核信息时间，后者核支付步骤。回到 [[#2.36 p.36 · 原题：LLM 财务抽取漏了单位和公布时点|p.36]]、[[#2.38 p.38 · 原题：赎回资格与现金到账|p.38]]。

</details>

## 8. 讲义页码映射

每行对应一个物理页；“原图”指该页在正文保留并解释的源页资产。纯文字或文字表页已展开独有知识与题目，不因没有位图而略去。

| 源/物理页 | 原页标题 | 正文精确链接 | 原图或处置 |
|---|---|---|---|
| Lec12 / 1 | FinTech and AI in Finance | [[#2.01 p.1 · 本讲研究三种金融服务判断\|p.1 讲解]] | 纯封面/分隔，说明并接下页 |
| Lec12 / 2 | Robo-Advising and Investment Decisions | [[#2.02 p.2 · 智能投顾部分入口\|p.2 讲解]] | 纯封面/分隔，说明并接下页 |
| Lec12 / 3 | Barriers to Retail Investment | [[#2.03 p.3 · 散户投资有三类障碍\|p.3 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 4 | Why Small Accounts Are Hard to Serve | [[#2.04 p.4 · 小账户收入为什么可能覆盖不了服务成本\|p.4 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 5 | What a Robo-Advisor Does | [[#2.05 p.5 · 智能投顾是一条持续服务链\|p.5 讲解]] | 原图保留并逐项读图 |
| Lec12 / 6 | What Automation Can Handle in Advice | [[#2.06 p.6 · 自动化和人工分别处理什么\|p.6 讲解]] | 原图保留并逐项读图 |
| Lec12 / 7 | A Robo-Advisor Converts a Goal into a Monitored Portfolio | [[#2.07 p.7 · 从目标到监测，每一步都有条件\|p.7 讲解]] | 原图保留并逐项读图 |
| Lec12 / 8 | Risk Tolerance Changes the Portfolio | [[#2.08 p.8 · 风险能力怎样影响股债比例\|p.8 讲解]] | 原图保留并逐项读图 |
| Lec12 / 9 | When a Risk Questionnaire Gives Conflicting Answers | [[#2.09 p.9 · 问卷高分怎样与明年首付冲突\|p.9 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 10 | Portfolio Rebalancing and Transaction Costs | [[#2.10 p.10 · 再平衡先算交易，再算成本\|p.10 讲解]] | 原图保留并逐项读图 |
| Lec12 / 11 | Betterment: Affordable Ongoing Investment Advice | [[#2.11 p.11 · Betterment 卖的持续服务\|p.11 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 12 | Betterment: Digital and Premium Service | [[#2.12 p.12 · 固定金额与按资产收费怎样比较\|p.12 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 13 | Betterment: The Value after Fees | [[#2.13 p.13 · 扣费后价值来自哪些动作\|p.13 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 14 | Robo-Advice Model Governance | [[#2.14 p.14 · 投顾治理会回到客户生活变化\|p.14 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 15 | Yu’e Bao: Distribution Can Dominate Advice | [[#2.15 p.15 · 余额宝：分销便利不改变产品权利\|p.15 讲解]] | 原图保留并逐项读图 |
| Lec12 / 16 | Multiple-Choice Question: Risk Preference and Capacity for Loss | [[#2.16 p.16 · 原题：风险偏好与亏损能力\|p.16 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 17 | Cybersecurity | [[#2.17 p.17 · 网络安全部分入口\|p.17 讲解]] | 纯封面/分隔，说明并接下页 |
| Lec12 / 18 | Binance: A Cyber Incident Becomes a Financial Loss | [[#2.18 p.18 · 同一网络事件有资金损失与服务中断\|p.18 讲解]] | 原图保留并逐项读图 |
| Lec12 / 19 | Cybersecurity in Financial Services | [[#2.19 p.19 · 保密、完整、可用分别保护什么\|p.19 讲解]] | 原图保留并逐项读图 |
| Lec12 / 20 | Binance: Contain Losses and Restore Withdrawals | [[#2.20 p.20 · 遏制、追踪冻结与恢复不可互相替代\|p.20 讲解]] | 原图保留并逐项读图 |
| Lec12 / 21 | HKSAR Cyber Incidents Reached a Record in 2025 | [[#2.21 p.21 · 香港事件图：总量与占比要分开读\|p.21 讲解]] | 原图保留并逐项读图 |
| Lec12 / 22 | Darktrace: The Security Team’s Problem | [[#2.22 p.22 · Darktrace 解决的是调查资源不足\|p.22 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 23 | Darktrace Case: One Unusual Download | [[#2.23 p.23 · 一次异常下载怎样从线索走到判断\|p.23 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 24 | Darktrace Case: Is the Service Worth Its Cost? | [[#2.24 p.24 · 警报从 100 降到 20 为什么还不够\|p.24 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 25 | Sources of Cyber Risk | [[#2.25 p.25 · 凭据、软件和供应商带来不同故障\|p.25 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 26 | Operational Resilience: Can the Bank Keep Serving Clients? | [[#2.26 p.26 · 运营韧性以客户服务为验收对象\|p.26 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 27 | Multiple-Choice Question: Recovery after Ransomware | [[#2.27 p.27 · 原题：勒索软件以后怎样恢复\|p.27 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 28 | RegTech and Financial Text | [[#2.28 p.28 · RegTech 与金融文本部分入口\|p.28 讲解]] | 纯封面/分隔，说明并接下页 |
| Lec12 / 29 | A Customer Matches a Sanctions-List Name | [[#2.29 p.29 · 同名只是需要核查的线索\|p.29 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 30 | What RegTech Does | [[#2.30 p.30 · KYC、AML 与制裁筛查有不同对象\|p.30 讲解]] | 原图保留并逐项读图 |
| Lec12 / 31 | Why Banks Buy Compliance Software | [[#2.31 p.31 · 合规软件的价值要能追溯到工作和证据\|p.31 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 32 | WeLab Bank: The Business behind Mobile Onboarding | [[#2.32 p.32 · WeLab 开户效率连接怎样的经济问题\|p.32 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 33 | WeLab Case: From an Identity Image to a Review | [[#2.33 p.33 · 从身份图片到开户决定\|p.33 讲解]] | 原图保留并逐项读图 |
| Lec12 / 34 | WeLab Case: A Similar Name Creates an Alert | [[#2.34 p.34 · 缺身份证号时还缺哪一步\|p.34 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 35 | Multiple-Choice Question: A Possible Sanctions Match | [[#2.35 p.35 · 原题：可能的制裁名单匹配\|p.35 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 36 | Check an LLM’s Financial-Data Extraction | [[#2.36 p.36 · 原题：LLM 财务抽取漏了单位和公布时点\|p.36 讲解]] | 原图保留并逐项读图 |
| Lec12 / 37 | LLM-Extracted Filings as Return Predictors | [[#2.37 p.37 · 从抽取到增长率，再到真正的后期预测检验\|p.37 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 38 | Check an LLM’s Reading of Redemption Terms | [[#2.38 p.38 · 原题：赎回资格与现金到账\|p.38 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 39 | Use One Canvas for the FinTech Company Case | [[#2.39 p.39 · 一张分析画布怎样连起公司案例\|p.39 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |
| Lec12 / 40 | The Two Parts of the Course | [[#2.40 p.40 · 全课两半分别在核哪一种主张\|p.40 讲解]] | 纯文字/文字表或原题完整解释；装饰Logo不搬入 |

## 9. 延伸与勘误

### 9.1 课件有但课堂是否讲到仍待核

本讲无可绑定的完整转录，40 页均按讲义解释，没有标某页“教授略过”。现有跨课来源提到 Lec12 未讲完可自行看 slides，只能作为材料待核提示，不能反推本讲逐页课堂覆盖。材料状态为 v0.9、transcript pending。

### 9.2 课堂独有内容仍缺

未加入本讲录音、课堂问答、口述强调或考试明示。没有用其他模型的补充假装教授说法。已有两条 ChatGPT 分享失效的访问证据由总监督保留；没有正文，就不能补造提示词链。

### 9.3 来源边界与容易误读处

- p.12 收费为课件版本，另于 2026-11-26 核 Betterment 官方页面；p.10 的 10 bp 是课堂成本假设，不能当实际公司收费。
- p.18、20 是事件当时的 Binance 更新，官方回读支持核心事实；调查初步口径与最终取证不同，本文不推全损已追回或今日所有服务状态。
- p.21 图是 HKCERT 全经济事件报告，不限银行。分类比例已舍入，不能当精确计数；p.19 插图的 20% 没有统计含义。
- p.33 明确不声称 WeLab 使用 Persona；p.36–38 明确是假设文件与条款，没有真实基金财报可以由此推导。
- p.38 末句的 Class 9 CFO 与 Class 10 supplier payment 指前讲知识连接，不是本 PDF 的 p.9/p.10。
- 本讲三个 MCQ 与 p.36–38 没有官方答案页；本文给出的直接答案为注明来源的参考作答。

### 9.4 延伸资料怎样使用

🔗 本次在线核验仅用于上述具体事实：[Betterment 费用](https://www.betterment.com/help/fees)、[Binance 事件更新](https://www.binance.com/en/square/post/382790902938294)、[Binance 分阶段恢复回顾](https://www.binance.com/en/square/post/384133235759486)、[HKCERT 2026 展望](https://www.hkcert.org/press-centre/hkcert-releases-hong-kong-cybersecurity-outlook-2026-security-incidents-hit-record-high-with-27-annual-increase-ai-related-attacks-and-supply-chain-risks-emerge-as-top-concerns-nearly-30-of-enterprises-lack-dedicated-cybersecurity-personnel)、[HKMA OR-2](https://brdr.hkma.gov.hk/chi/doc-ldg/docId/getPdf/20220531-2-EN/OR-2.pdf)、[CrowdStrike 技术说明](https://www.crowdstrike.com/en-us/blog/falcon-update-for-windows-hosts-technical-details/)。获取日均为 2026-11-26；课件里的其他公司描述仍明确标为课件来源，没有扩称每条现行公司条款都已外部核实。

DEBS13 视频尚未实际观看，保留来源及学习依赖卡，不在本篇声称看完或根据视频填充教学。本人复习状态与作业提交状态均不因本篇制作而改变。
