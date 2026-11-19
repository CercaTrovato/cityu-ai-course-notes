---
course: EF5560
module: M11
week: null
date: null
source:
  - course_files_export/canvas-20261118/Lec11_Lending_and_Crowdfunding.pdf（54 页，Canvas file 16566175）
transcript: pending
prerequisites: [M03, M05, M06, M08, M10]
new_concepts: [Underwriting, Origination, Funding, Probability of default, Loss given default, Calibration, First-loss guarantee, Crowdfunding]
tags: [EF5560, lending, crowdfunding, credit, calibration]
status: v0.9
updated: 2026-11-18
readability_rules: v2
teaching_standard: novice-v1
mechanism_review: pending
---

# M11 · 数字信贷与众筹：资金、权利和损失由谁承担

> 讲义候选，待独立审查；v0.9 表示未取得本讲转录。实际授课日、周次和课堂覆盖未知。公司、产品与法规按讲义版本记录，未逐站重核当前条款，不作为现实交易或法律操作指引。

## 0. 三分钟速览

数字入口能改变资料、处理成本和分发；贷款是否值得做，还取决于资金、偿还能力、合同权利及损失。

- 能沿申请到贷后流程指出承做、出资、服务和风险承担者。
- 能计算预期信用损失、贡献和首损担保下的实际损失分配。
- 能说明风险排序正确为何仍可能低估概率与损失。
- 能区分众筹达标、产品交付、贷款偿还与股权权利。

## 1. 开始之前 · 知识衔接

### 1.1 当前用到的旧知识

本金是借入后需要归还的钱，利息/费用是使用资金或服务的代价；本金回收不能全部当收入。M10 的 BNPL 先付商户、后收顾客，会产生资金时间差；本讲 p.19/26 重新给数计算。M08 的 Aave 用抵押品和协议限额决定借款能力，本讲 p.48 对照无抵押企业贷款。

必要前文：[[EF5560_Fintech_and_AI_in_Finance/notes/M03-线性机器学习与收益预测|M03 的样本外逻辑]]、[[EF5560_Fintech_and_AI_in_Finance/notes/M05-可解释机器学习与投资组合决策|M05 的模型解释]]、[[EF5560_Fintech_and_AI_in_Finance/notes/M08-DeFi-NFT与现实世界资产|M08 的抵押借款]]。历史登记不是掌握证明，当前核心在当地搭桥。

### 1.2 新概念入口

承做与出资在 p.5/14–16，十二个月违约评价在 p.12/24/46，概率与损失率在 p.26，担保在 p.27/49，众筹权利在 p.29–38，共有登记与信用判断在 p.39/45。§5 词表用于复习，不代替当地解释。

### 1.3 三条使用路线

L11 是本讲 54 个物理页，内容页页内号与物理页相同。预习顺读 §2 并遮住参考答案复做；课中由 §8 每页精确链接到本页和原图；复习用 §3–§7 按资金/风险/证据重组。原文块保留题面与讲义给定步骤，中文译解、笔记推断和英文自拟答案分别说明。无本讲转录，不推定老师略过某页。

## 2. 正文 · 按原课件页序

### 2.1 p.01 · 本讲范围与来源边界

本讲为 Class 11 Lending and Crowdfunding，讲授数字信贷与众筹。学期写 Semester A 2026/27，封面没有实际授课日期。本批没有 M11 转录，不能由文件生成时间推断上课日，也不替教师宣布重点或跳页。

### 2.2 p.02 · 数字信贷与信用决定

本页只有 Digital Lending and Credit Decisions 分隔标题。接下来的主问题是：资料不多的小商户能否借到钱，借款人、提供数据者、审核者和出资者分别承担什么责任。后续每页从这些对象继续，不以有 App 推定风险消失。

### 2.3 p.03 · 只有十二个月现金流怎样判断借款人

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Assessing a Borrower with Limited Credit History




Scenario: A small online seller has no long credit history but has twelve months of bank and
platform cash-flow data.

Evidence that may help                          Evidence still missing
- sales, cash inflows, and their                 - debts outside the platform and data
seasonality;                                     that may be inaccurate;

- repayment records, refunds, and                - recoveries if the borrower defaults.
disputes.





</details>

原情境的小网店没有很长信用记录，但有 12 个月银行和平台现金流。薄信用档案（Thin credit file）是可用信用历史有限，不等于已证实信用差。销售、入账和季节性帮助判断钱何时来；还款、退款和争议帮助核销售是否能转成稳定现金。

讲义也列出仍缺的平台外负债、资料准确性、违约后的回收。若只见平台每月卖 10 万，没见它另欠 20 万，就不能准确判断还款能力（Repayment capacity）。这不是要求凭常识补出外债；要把未知作为需核证据。英文原情境与两列材料保留在原文块，以下同。

### 2.4 p.04 · 小额贷款为何也可能很贵

网店要先备货，顾客以后才付款，形成营运资金（Working capital）需求。资料短使贷款人难判断未来还款，核身份与审文件又有固定人工工作；贷款金额小，不代表这些工作按比例变少。

数字记录可能减少取证和处理成本，但好销售没有揭示所有债务，也不保证下月销售。💡 笔记补充：同样花 100 元核资料，贷 1,000 元时占 10%，贷 100,000 元时占 0.1%；这只是成本比例例，不是实际费率或客户应付利息。

### 2.5 p.05 · 数字贷款四格流程

![L11 p.5：数字贷款四格](figures/m11/source-p05.png)

来源：L11 p.5，保留整页原图，可打开大图辨认原标签。

原图四格各回答一步：

1. Application：借款人填收入、目的并同意数据使用。
2. Credit assessment：资料进入违约概率估计和人工检查。
3. Offer and funding：报价写贷款额、利率、期限、月供，客户接受后贷款人提供资金。
4. Repayment monitoring：追踪还款与逾期、必要时催收。

沿一笔申请走图，给了资料不代表已获批，获批不代表无须出资，放款也没有结束责任。图上的同意框只是界面示意，不能据此认定客户已理解所有用途；报价、授权和资金转出是不同证据。贷款承做（Origination）包括接入、审核和建立贷款，资金提供（Funding）回答实际用谁的钱，两者可以由不同机构负责。

### 2.6 p.06 · 技术改变流程的哪三处

![L11 p.6：传统人工与数字流程比较](figures/m11/source-p06.png)

来源：L11 p.6，保留整页原图，可打开大图辨认原标签。

原图左侧传统路线是借款人→银行→文件和人工承贷→批准；右侧漫画对比纸面等待与数字处理。它展示理想化速度优势，不是秒级批准的普遍实测结果。

下方三列增量分别是：电子申请/签名和更清楚沟通；更多资料与自动化，让资料少的借款人也有可核证据；新分发渠道和持续监测，更早发现问题。自动化承贷（Automated underwriting）是用规则/模型支持评估，不会自动决定最终风险由谁承担；模型表现、公平、数据所有者与风险承担者仍须明确。

### 2.7 p.07 · Ant 的支付生态怎样支持贷款

![L11 p.7：Ant数据与出资示意](figures/m11/source-p07.png)

来源：L11 p.7，保留整页原图，可打开大图辨认原标签。

讲义以支付宝生态说明小额消费和商户资金需求：传统网点评估成本高，抵押物（Collateral，即支持债务的可处置资产）或信用记录有限时更明显。花呗面向购买融资，借呗提供信用贷款；这里保留讲义产品定位，不保证当前所有合同条款相同。

原图从支付宝用户、交易和行为数据走向放款，带有少于 3 分钟的示意标注。图是平台小贷概念图，不是所有贷款审批速度或必批的保证。要继续问哪方审核、出钱、收回款、承担违约，而不是把一个品牌当全部角色。

### 2.8 p.08 · 沿商户一次申请追踪三种责任

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Ant Case: Following a Digital Loan Application


Illustrative online seller using a lender connected to a payment platform.

- Apply. The seller states the amount and purpose of the loan and authorizes access to
relevant records.

- Assess. The lender reviews sales, refunds, and bank receipts, then checks other debts and
repayment capacity.

- Fund and collect. The lender or funding partner supplies the money. The contract
identifies who receives repayments and bears losses.

This is an illustrative platform-lending workflow, not a description of a specific Ant loan
contract.


</details>

这是讲义假设的平台贷款流程，不是某一份蚂蚁合同。申请时商户写金额、用途并授权查相关记录；评估时贷款人看销售、退款、银行实收，再查其他债务和偿还能力；出资与收款时由贷款人或伙伴供钱，合同指定收款权与损失归属。

**参考理解**：数据平台让信息可取得，不能据此断言它就是出借人。若合同改为伙伴出资但平台担保首笔损失，资金来源与风险归属便分开了，后面 p.27 会计算这种判断。原文明确不是具体合同，这一限制与流程一并保留。

### 2.9 p.09 · 贷款服务与最终信用责任分开

课件列蚂蚁为金融机构伙伴提供技术，App 提供分发与信息；贷款人/出资伙伴提供本金并按合同收贷款收入。借款本金是需要偿还的资金，不是平台收费收入。

商业上要看更低获客/评估成本能否覆盖资金成本与违约损失；责任上要看合同写谁承担。讲义注明公司材料核于 2026-10-13、安排因产品不同。本批未另查最新产品合同，不把平台外观推成确定责任。

### 2.10 p.10 · 自动化怎样降成本又保留复核

![L11 p.10：自动贷款四图标](figures/m11/source-p10.png)

来源：L11 p.10，保留整页原图，可打开大图辨认原标签。

认识你的客户（Know your customer，KYC）是核实客户身份等所需资料；自动承贷把资料按规则或模型处理，减少重复人工工作。新还款和现金流可支持更新额度，异常和借款人申诉仍需工作人员处理。

原图四块是 Application、AI underwriting、Data monitoring、Instant disbursement，并用箭头构成示意循环。不能把漫画的排版误读为首次贷款一定先有该笔还款监测再放款；实际流程按 p.5 先申请/审核/出资，再收集贷后结果用于后续监测与更新。少人工不等于无人负责。

### 2.11 p.11 · 变量重要为何不能证明因果

在批准以前已经可得的销售与支付记录，可构建销售增长和现金流波动（Cash-flow volatility，即不同时期入账起伏程度）。构造变量先固定期间，例如用过去 12 个月，而不是借款后才出现的结果。

变量重要性（Variable importance）高，表示模型预测较依赖这个输入，不等于人为降低波动就必使违约下降。可能还有经营规模、行业或外债共同影响两者。讲义特别提醒平台外负债可能不可见；不要把缺记录当零负债。这里连接 M01/M05 的时点与解释原则，没有真实数据便不造重要性分数。

### 2.12 p.12 · 十二个月违约预测如何公平评估

目标是判断借款人在未来 12 个月是否违约。训练（Train）用较早且结果已知的贷款建立预测关系，调参（Tune）用另一段旧贷款选择设置；更晚贷款留作测试，且须走完完整 12 个月观察窗。

例如一笔刚贷出 2 个月、尚未违约，不能自动当“12 个月内不违约”。和既有信用分比较时，用同一批测试贷款、同一目标与观察长度；否则差异可能来自借款人不同。预测更准还要核利息是否覆盖资金、服务和信用损失，模型指标与可盈利决策分开。

### 2.13 p.13 · 四种贷款模式是重叠路线

![L11 p.13：四种模式演变](figures/m11/source-p13.png)

来源：L11 p.13，保留整页原图，可打开大图辨认原标签。

原时间图以约 2005/2010/2015/2020 标出 P2P lending、Marketplace lending、Embedded lending、Credit infrastructure。P2P 是出资者与借款人经平台联系；市场平台可连接机构资金；嵌入式贷款放进购物等已有流程；信用基础设施向其他机构提供评估或服务工具。

图下注明阶段重叠并随技术和监管演化。因此不是过了 2020 年所有 P2P 必然消失，也不是每家企业都依次经过四步。先识别当前合同和资金结构，再用时间图理解发展方向。

### 2.14 p.14 · LendingClub 案例怎样分留存与出售

讲义声称 LendingClub 于 2021 年收购银行并于 2026 年 6 月成为 Happen，引用名称变更申报。本批未独立核该名称与申报，不将其当已验证现行公司身份；它不影响下面的课堂合同机制。

消费者可把昂贵信用卡余额合并为固定偿还日程的个人贷款。银行留在账上的贷款可用存款支持并收利息；平台也可承做后卖给投资者。卖出与留存会改变资金占用和损失承担，须看担保等合同。下一页是贷款现金流示意，不是当前零售 P2P 产品说明。

### 2.15 p.15 · 投资者的回款先扣什么

![L11 p.15：贷款投资者现金流四格](figures/m11/source-p15.png)

来源：L11 p.15，保留整页原图，可打开大图辨认原标签。

原四格依次是投资者经平台把钱分给 A/B/C 三借款人；借款人还本金和利息回平台；平台扣服务费后把净现金给投资者；若 C 漏还，投资者收到更低现金、承担该示意合同的贷款损失。

钱从投资者流出是本金投入，回来的一部分只是本金归还，不能全部算收益。服务费是平台留存，违约损失会减少投资者净回款。本页特指假设的直接贷款投资，其他平台可能有担保或留存风险，不能把原图“投资者承担”推为一切产品通则。

### 2.16 p.16 · Upstart 的两个判断问题

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Upstart: AI Lending and Outside Funding


- Banks and credit unions use Upstart’s technology to reach borrowers and assess repayment
risk.

- Upstart earns platform, referral and servicing fees. Loans can be held by lending partners,
outside investors or Upstart itself.

- AI can reduce manual review, but investors still decide whether to supply funds. Loan
holdings and contractual guarantees can leave a platform with credit exposure.


Compare two questions: Does the model predict default well? And can the lending
business fund profitable loans?

Source: Upstart 2025 Annual Report.



</details>

按讲义，银行/信用合作机构用 Upstart 技术获客和评估，平台赚平台、转介和服务费；贷款可由合作机构、外部投资者或 Upstart 自己持有。AI 降低审核工作并不会迫使投资者供钱，持有贷款或提供担保还可能使平台保留信用风险。

**⚪ 两问参考作答（笔记推断）**：模型能否预测好违约，需要同条件样本外证据、校准与实际损失；业务能否融资并获利，还需稳定资金、定价收入和全部成本。一个模型排序好而资金伙伴退出，仍可能无法新放贷。

**English reference answer**: Test prediction quality on comparable out-of-sample loans, including calibration and losses. Separately test whether available funding and loan income cover funding, servicing and credit costs. These are related but different questions.（笔记自拟）

### 2.17 p.17 · 微业贷为何需要无抵押评估

小企业先备货/付供应商，后收客户钱；抵押少和网点审核贵可能限制贷款。课件以微众银行微业贷的线上无抵押营运贷款为例，数字资料替代部分现场申请步骤。

无抵押（Unsecured）表示这类贷款没有按本页设定提供特定抵押保障，不等于没有偿还义务或贷款人不会损失。微众仍需给违约风险定价并准备出资。讲义产品资料日期为 2026-10-13，本批不作当前申请资格或利率建议。

### 2.18 p.18 · 额度与价格怎样接到贷后结果

申请人授权相关商业资料，贷款人核身份与记录能否支持偿还。信用评估影响额度和价格，借款人按合同提款及还款；贷后再用真实还款检验原评估。

这是一套简化教学框架，不是微众内部专有模型。💡 笔记补充：预测违约率为 2% 也不能单凭这个数自动批款，还要知道违约损失大小、收费、资金和服务成本。p.26 给完整数字例，不能把“预测准确”直接改写成“必盈利”。

### 2.19 p.19 · 一千美元小贷款能留多少贡献

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

WeBank Case: Can a Small Loan Cover Its Costs?

Hypothetical \$1,000 one-year loan, not WeBank results:

Interest and origination revenue             +\$120
Expected credit loss                          -\$55
Funding cost                                  -\$25
Acquisition, verification, and servicing      -\$30
Expected contribution before overhead         +\$10


- Faster approval helps only if pricing covers loss, funding, fraud, and servicing.

- A small error in expected loss can remove the entire margin.

- For WeBank, digital processing must lower costs without allowing fraud or credit losses to
absorb the saving.


</details>

讲义假设一笔一年期 1,000 美元贷款，不是微众真实经营结果。收入是利息及承做收入 120；预期信用损失 55；资金成本 25；获客、核验、服务合计 30。全部同一笔贷款和一年口径。

逐项扣减得 $120-55-25-30=10$ 美元，是管理间接费用以前的预期贡献。预期损失是事前估计的不可回收金额，不是本笔已实际亏 55。再多 10 美元损失即可抹平贡献；只把审核加快，却让坏账增加超过节约成本，不能改善经济结果。

**英文结果说明（笔记自拟）**：The expected contribution is \$10 before overhead. An additional \$10 of expected credit losses removes that contribution; faster approval alone does not establish profitability. 原给定表和条件见原文块。

### 2.20 p.20 · WeLab Bank 案例保留银行责任

课件以香港数字银行 WeLab Bank 为例，手机开户和数字服务改变客户入口。贷款收入仍要覆盖资金、服务和违约成本，外部伙伴参与并不会使银行对信用决定及客户保护的责任消失。

这页是讲义的银行模式概览；本批没有重新核香港金管局名册或公司现行产品，不将课程案例扩写成现实开户/借款建议。后面把银行留贷、无担保出售、带担保出售分别比较，而非认为“数字”自动代表只做技术不承担风险。

### 2.21 p.21 · CDI 研究图能证明到哪一步

![L11 p.21：CDI贷款条款估计图](figures/m11/source-p21.png)

来源：L11 p.21，保留整页原图，可打开大图辨认原标签。

商业数据通（Commercial Data Interchange，CDI）按同意共享商业资料，可能减少承贷信息缺口。原图两条横杆是相对样本均值的估计减少：利率低 36 个基点（Basis point，1 bp 是 0.01 个百分点），约为均值的 6%；抵押物数量少 1.1 项，约为均值的 22%。6% 不是利率低 6 个百分点。

图注说研究覆盖 2022 年 1 月至 2025 年 3 月 80,097 笔新中小企贷款，用双重差分（Difference-in-differences）比较 2022 年 10 月上线后六家较多用 CDI 银行与其他银行的变化。双重差分扣去对照组同期变化，仍依赖两组本应可比等假设。研究没有每笔贷款是否用 CDI 的指标，银行级使用不等于每笔贷款的处理记录，不能把估计当任一贷款直接降息保证。原始数据未提供，本批读图未复跑研究。

### 2.22 p.22 · 互联网助贷政策在课堂模型中的作用

讲义把 NFRA（National Financial Regulatory Administration，国家金融监督管理总局）2025 年通知概括为三项：

- 互联网助贷纳入银行总行风险管理。
- 银行在贷款全生命周期监测伙伴集中和质量。
- 平台可供技术和分发，银行仍负责信用风险与客户保护。讲义注明 2025-10-01 生效。

本批没有核现行法条或后续修订，以上是有日期的讲义陈述，不是现实合规结论。用于课堂比较时，关键是技术合作不能遮住银行角色；须按功能查谁承做、出资、服务、担保和最终负担损失。

### 2.23 p.23 · 三地相似 App 的资金与脆弱点

![L11 p.23：三地资金结构表](figures/m11/source-p23.png)

来源：L11 p.23，保留整页原图，可打开大图辨认原标签。

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>


| Market and case | Origination and funding | Distribution / data edge | Vulnerability to test |
|---|---|---|---|
| U.S.: Upstart | partner banks originate. 2025 facilitated principal: 64% institutional investors; 26% lending partners; 10% Upstart balance sheet | online acquisition, partner APIs, and AI underwriting | investor funding supply and lending-partner concentration |
| Chinese Mainland: WeBank / Ant ecosystem | a digital bank or partner bank originates and funds; platforms may provide distribution, data, and technology | super-app or SME ecosystem lowers acquisition and information costs | bank ownership of whole-lifecycle credit risk and partner concentration |
| HKSAR: WeLab Bank | licensed digital bank with deposit and balance-sheet responsibility | mobile onboarding; account and bureau data; CDI available to participants | affordability, conduct, operational resilience, and credit discipline |

Compare funding, risk ownership, acquisition cost, losses, and accountability.

Sources: Upstart 2025 10-K; NFRA 2025 internet-lending rule; HKMA bank register and CDI.


</details>

原表三行比较 Upstart、内地微众/蚂蚁生态、香港 WeLab。Upstart 行称 2025 facilitated principal 的最终持有资金约 64% 机构投资者、26% 贷款伙伴、10% 平台资产负债表，三项合计 100%；不是平台收入构成。本批按讲义表记录，未另核 10-K。

内地行重点是数字/合作银行承做和出资、平台可分发数据技术；香港行重点是有存款与资产负债表责任的持牌数字银行。获客优势分别来自在线/API/AI、超级 App 或小企生态、手机接入与账户/征信/CDI。

**参考比较**：Upstart 要测外部资金供给与伙伴集中；内地生态要明确全生命周期风险由银行管理并测集中；香港数字银行要测负担能力、行为、运营韧性和信用纪律。English reference: Compare funding, risk ownership, acquisition costs, losses and accountability, rather than treating similar apps as the same lending model.（笔记自拟）

### 2.24 p.24 · 选择题：新 AI 是否真的改进

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Multiple-Choice Question: Did the AI Model Really Improve?

Approval rises and defaults fall after a lender deploys a new AI model,
but borrower mix and credit policy also changed. What evidence best
supports model improvement?
A) A higher training-sample AUC.

B) More input variables and a deeper model.

C) Out-of-sample cohort evidence under comparable policy and risk, including calibration and
losses.

D) Faster approvals with fewer manual reviews.


Discuss
Identify which changes affect borrower selection, model performance, and realized losses.


</details>

**中文题意**：部署新模型后批准率升、违约降，但借款人组成和信用政策也变了，问什么证据最支持模型改进。A 是训练样本 AUC 更高；B 是更多变量和更深模型；C 是可比政策和风险条件下的样本外批次证据，含校准和损失；D 是批准更快、人工更少。完整英文题与四选项在原文块。

**⚪ 参考答案（笔记推断）：C。** AUC 是排序指标的一种，训练表现可能只是记住旧数据；B 的模型复杂度不是实际改进证据；D 是处理效率，不能分离借款人选择和风险。C 用可比后来贷款检验排序、概率水平与损失，最接近要问的模型效果。

Discuss 的分层：借款人组成和信用政策改变获批的人；模型改变预测关系；后来实际违约受两者及经济环境共同影响。

**English reference answer**: C. Comparable out-of-sample cohorts, including calibration and losses, provide stronger evidence than training AUC, model complexity or approval speed. Changes in borrower selection and credit policy must be separated from model performance.（笔记自拟）

### 2.25 p.25 · 四种模式没有把风险消掉

![L11 p.25：四模式新增风险](figures/m11/source-p25.png)

来源：L11 p.25，保留整页原图，可打开大图辨认原标签。

原图复用四阶段分类，但下方新增各模式风险：

- P2P 是筛选、服务、投资者保护和激励。
- 市场平台是资金周期、伙伴集中和保留风险。
- 嵌入式是过度消费、信息披露、负担能力与商户激励。
- 基础设施是供应商依赖、模型治理与数据权利。

沿具体一项读：平台只提供模型工具，仍可能因系统停机或模型错误影响银行，但这不等于它自动承担贷款全部违约。技术会改变分发和资金连接，信用、行为和运营风险仍须依合同、职责和证据分别定位。

### 2.26 p.26 · 选择题：预期损失与税前利润

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Multiple-Choice Question: Expected Profit on One Loan



A one-year \$1,000 loan has expected interest income of \$80. Funding costs are \$30 and operating
costs are \$15. Default probability is 4%, with a loss of 50% of principal if default occurs.

Using expected credit loss $PD\times LGD\times\mathrm{principal}$, what is expected profit before tax?

A) \$35

B) \$50

C) \$65

D) \$15




</details>

**中文题意**：一年期本金 1,000 美元，预期利息 80，资金成本 30、经营成本 15；违约概率 4%，违约时损失本金的 50%。A/B/C/D 分别为 35/50/65/15 美元。

先固定三个量：违约概率（Probability of default，PD）是 4%；违约损失率（Loss given default，LGD）是在已违约条件下损失的本金比例 50%；本题本金是 1,000 美元。预期信用损失按题给规则 $PD\times LGD\times本金=0.04\times0.50\times1,000=20$ 美元。概率与损失率都是比例，相乘后再乘美元才得到美元。

**⚪ 参考答案（笔记推断）：D，15 美元。** $80-30-15-20=15$。A 忽略信用损失，B 只扣资金成本，C 只扣经营成本；三者都少扣题设项目。

**English reference answer**: D. Expected credit loss is \$20, and expected profit before tax is \$80 − \$30 − \$15 − \$20 = \$15.（笔记自拟）

若 PD 改成 8% 而其他条件固定，损失为 40，利润为 −5 美元；本例用题设预期利息，不能另行重复扣一遍已包含的收入损失。

### 2.27 p.27 · 选择题：银行出资是否消除平台风险

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Multiple-Choice Question: Funding and Retained Credit Risk


A platform arranges loans funded by a partner bank. Under their contract, the platform reimburses the bank for the first \$2 million of credit losses.

Which statement best describes the platform’s risk?

A) It bears no credit risk because the loans do not use its funding.

B) It retains credit exposure through the guarantee even though the bank supplies the loan
funding.

C) Its maximum credit loss must equal the origination fees it receives.

D) Its credit exposure disappears when underwriting uses an AI model.



</details>

**中文题意**：合作银行出钱，平台承诺补偿最先发生的 200 万美元信用损失。A 说无自有出资就无信用风险；B 说担保保留敞口；C 说最大损失一定等于承做费；D 说用 AI 承贷风险就消失。

**⚪ 参考答案（笔记推断）：B。** 首损担保（First-loss guarantee）使平台先承担约定范围内的信用损失，谁出本金与谁补损失是两种合同角色。A 忽略补偿承诺，C 没有题设依据，D 把预测工具当消除义务。

💡 笔记补充：总信用损失 50 万时按题设平台补 50 万；损失 300 万时平台首损层 200 万，剩 100 万未由这条担保覆盖，仍按其他合同处理。仅这条担保的最高补偿为 200 万，不据此断言平台全部业务最大损失。

**English reference answer**: B. The platform retains credit exposure through its first-loss guarantee even though the bank provides the funding. Using AI does not remove the contractual obligation.（笔记自拟）

### 2.28 p.28 · 众筹分隔

本页只有 Crowdfunding 分隔标题。众筹（Crowdfunding）把许多参与者的支持汇集起来，但参与者拿回什么权利因模式不同；先辨认捐赠、奖励、股权还是债权，才可比较收益和风险。

### 2.29 p.29 · 作品未完成为什么先有人支持

![L11 p.29：众筹生态](figures/m11/source-p29.png)

来源：L11 p.29，保留整页原图，可打开大图辨认原标签。

Kickstarter 创作者在游戏、电影、书籍完成以前就需资金，支持者承诺（Pledge）小额支持项目和奖励，平台汇集并增加可见度。原图把 Backers、Creator、Payments、Social sharing 和 Platform 放入关系网，区分资金支持与社交传播。

沿一个桌游例，支持者先承诺钱，创作者才有机会生产；分享消息可带来更多支持，不是平台代创作者保证交货。原图 CREATO 字样不完整，保留原貌，不为图中未注明的每条装饰箭头编造合同义务。

### 2.30 p.30 · 四类众筹先看支持者请求权

表的每行先问给钱者收到什么，再看控制重点。

- 捐赠（Donation）无财务回报，核真实性、用途和付款完整。
- 奖励（Reward）得到产品/体验/认可，核生产、交付、质量、退款。
- 股权（Equity）有所有权或证券请求权，核估值、稀释、披露、托管及证券规则。
- 债务/P2P（Debt/P2P）有还本付息请求权，核承贷、资金、服务、违约和借贷规则。

稀释（Dilution）是发行更多权益后原持有者占比可能下降。给同样 40 元买奖励与买股权，前者不会只因付款自动拥有公司；平台名称像“投资”也不能改变真实合同权利。以上为讲义分类，不推断各法域现行许可范围。

### 2.31 p.31 · 全有或全无解决哪种筹资门槛

创作者先写目标、截止和承诺奖励。全有或全无（All-or-nothing）指截止前达到目标才收取承诺金额；未达标创作者得不到资金。课件列平台费为已收资金 5%，另有支付处理费，剩余还要生产和交付。

门槛避免项目只拿到很少钱就启动，但达标没有证明成本估算正确或交付必成功。创作者负责项目与奖励，平台不保证交付。💡 笔记补充：目标 20,000，承诺 19,000 未达标，与“收到 19,000 后少做一点产品”不同；必须按该规则理解何时真正收款。

### 2.32 p.32 · 五百人支持桌游怎样分资金

讲义假设 500 人每人支持 US\$40，目标 US\$20,000 已达成且所有承诺成功收取。总额 $500\times40=20,000$ 美元；平台费 $20,000\times5\%=1,000$；创作者得 19,000，但还没有扣独立支付处理费。

每人得到的是承诺的游戏，不是股票或利息；创作者仍需用可用资金完成生产和交付。达标证实足够承诺需求，不证明每套成本足够低。若处理费假设为总筹款 3%，还需扣 600，创作者余 18,400（笔记补充，不是实际平台报价），不能把 19,000 当净利润。

### 2.33 p.33 · Kiva 与 Kickstarter 的资金权利

Kiva 的个人出借人期待本金偿还、不收利息且可能损失；回收的资金可再支持另一借款人。借款人仍可能向当地放贷伙伴付息，所以“个人出借人零利息”不等于借款人零成本。

Kickstarter 支持者期待奖励，单纯支持并不产生贷款偿还请求权或股权。**英文参考说明（笔记自拟）**：A Kiva lender expects principal repayment without interest and may lose money; the borrower may still pay a local partner. A Kickstarter backer seeks a reward, not a loan repayment claim or ownership merely by backing a project. 这是按讲义作比较，不补造当前个别合同。

### 2.34 p.34 · 创办理念怎样变成合同规则

![L11 p.34：创办规则与AI插画](figures/m11/source-p34.png)

来源：L11 p.34，保留整页原图，可打开大图辨认原标签。

原表用 Affirm 的 Max Levchin 与 Kickstarter 创办团队 Perry Chen 作对照；人物肖像注明为 AI 插画，不是照片。Affirm 在结账重新作承贷决定并在客户承诺前披露付款安排，商户可能为转化付费、消费者可能付息，Affirm/资金伙伴承担信用与融资风险。

Kickstarter 用达标才收承诺款的规则，成功项目创作者付平台费；创作者仍承交付风险，支持者无保证产品。用理念解释规则可以帮助记忆，但风险分配仍看具体产品合同，不把人物故事当每份条款的证明。

### 2.35 p.35 · 贷款运营与信用风险分隔

本页只有 Lending Operations and Credit Risk 标题。前半已经区分出资和请求权；后半把许可、资料、模型、服务中断和债权记录接入同一条运营链，继续核责任和证据。

### 2.36 p.36 · 一个数字入口不等于一种许可

![L11 p.36：四功能监管边界](figures/m11/source-p36.png)

来源：L11 p.36，保留整页原图，可打开大图辨认原标签。

原表四行按功能比较法域：放贷出资、在线分发、使用客户资料、自动决定。香港列分别提：

- 持牌机构/贷款人；
- 行为披露、适当性和投诉；
- 私隐、同意、安全与 CDI；
- 模型核验、公平、记录和人工复核。

内地列按四行相应列出：机构及放贷规则，银行主导的伙伴风险管理，PIPL/数据安全的目的必要性，以及机构拥有模型并监测伙伴。

PIPL 指《个人信息保护法》（Personal Information Protection Law）。课堂意思是不同功能触及不同责任，不能有了 App 就把所有活动装进一种许可。此页是法规分类框架，未逐条核现行法；用来作现实结论前要回当时当地一手条文。

### 2.37 p.37 · 监管要求要能找到哪种证据

![L11 p.37：控制证据及失败](figures/m11/source-p37.png)

来源：L11 p.37，保留整页原图，可打开大图辨认原标签。

每行连要求、证据和失败例。授权许可要识别贷款人/分发/出资/服务方与法域，避免技术平台无许可做受管活动；客户保护要保存总成本、还款表、逾期后果、投诉和困难援助，避免快界面隐藏费用。

资料治理要证明目的合法、必要、访问权限、来源链、保存期和安全，避免无关/未经授权资料驱动决定。

模型治理要有验证、理由、公平、人工改判与监测，避免漂移无人发现/无法申诉。报告与韧性要有表现、事件、供应商、恢复和监管报表，避免故障同时中断服务和证据。不是列齐字段就证明合规，要核它对应的实际行为。

### 2.38 p.38 · 简答：众筹达标证明了什么

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Short-Answer Question: What Did the Funding Threshold Prove?



An all-or-nothing reward-based crowdfunding campaign crosses its funding
threshold on the final day.
1. Explain what the threshold establishes about pledged demand.

2. Identify two risks that remain after the threshold is reached.

3. State one item a backer should verify before contributing.



Answer in three or four sentences
Separate demand evidence from production capability, delivery, and contractual protection.




</details>

**中文题意**：奖励式全有或全无项目在最后一天过门槛。第 1 问说明承诺需求，第 2 问要两项剩余风险，第 3 问要支持前核一项，用 3–4 句英文回答。

**⚪ 参考作答（笔记推断）**：达标说明承诺支持达到预设金额条件；生产能力/成本超支与交付延误仍是两项风险。支持前可核创作者生产计划和预算证据，不能只看筹款人数。平台不保证产品的边界仍在。

**English reference answer**: Reaching the threshold establishes that pledged demand meets the campaign's funding rule. It does not establish production capability or guarantee delivery. Cost overruns and delivery delays remain risks. Before contributing, a backer should verify the creator's production plan and supporting budget evidence.（笔记自拟）

若改成股权众筹，就不能沿用“只拿产品奖励”的权利判断，须重查证券/所有权条款。

### 2.39 p.39 · 卖掉整笔应收款与抵押借款不同

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Invoice Finance: Cash Now, Payment Later


Hypothetical case: Alice delivered goods to a retailer. Invoice R-104 is HK\$1 million due in
60 days.

- Alice needs cash now for wages and suppliers. Bank A buys the entire payment claim at
an agreed discount.

- A shared registry records the transfer. Before buying the same claim, Bank B checks
whether Alice still owns it.

- Bank A must separately assess whether the retailer can pay. Clear ownership does not
establish repayment capacity.

Here the bank buys a claim. On page 45, banks lend against a receivable subject to an
aggregate financing cap. These are different contracts.


</details>

讲义假设 Alice 已交货，R-104 发票 HK\$100 万 60 天到期，眼下要付工资/供应商；Bank A 按折价买下整笔付款请求权。共有登记记录转让，Bank B 买同一债权前查 Alice 是否还拥有。这里卖的是请求权，不是只借其中一个比例。

登记可防止同一已转让债权再卖，却不能证明零售商会付款；A 仍要核零售商的偿还能力。折价金额、追索/担保条款未知，不能算 Alice 到手净钱或最终损失。p.45 是以应收款支持有总额上限的借贷，两种合同不得混用。

**English reference explanation**: Bank A buys the entire payment claim at an agreed discount. The registry helps check ownership and prevent a duplicate sale, but repayment capacity still requires credit assessment. This differs from lending against a receivable under an aggregate financing cap.（笔记自拟）

### 2.40 p.40 · 两种制度共同要问哪三个对象

![L11 p.40：两制度四问](figures/m11/source-p40.png)

来源：L11 p.40，保留整页原图，可打开大图辨认原标签。

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>


| A case must answer | HKSAR | Chinese Mainland |
|---|---|---|
| Who is the regulated lender? | a digital bank inside a prudential licensing and supervision framework | the bank, which must state the partner's role, funding, guarantees, servicing, and the ultimate loss bearer |
| What limits the platform? | outsourcing to cloud and analytics vendors does not transfer regulatory responsibility | the 2025 NFRA notice puts platform and product concentration inside the bank's own risk management |
| What is the data basis? | Commercial Data Interchange is consent-based; it supports credit assessment without replacing bank judgment | the Personal Information Protection Law and data-security rules require lawful purpose, necessity, protection, and lifecycle governance |
| What else is supervised? | OR-2 resilience testing, plus AML, privacy, fairness, and consumer protection in onboarding and alternative data | servicing, collections, marketing, pricing, consent, complaints, and model decisions |

The common question: Name the regulated entity, the lawful basis for the data, and the party that absorbs the default loss. Both regimes ask for all three.

Sources: HKMA Supervisory Policy Manual OR-2; HKMA Commercial Data Interchange; NFRA 2025 internet-assisted-lending notice; PRC Personal Information Protection Law.


</details>

原表的四问保留在英文原文块。按讲义框架回答：①受监管贷款人是谁——香港例是审慎许可框架内的数字银行，内地例是应说明伙伴职责/资金/担保/服务/损失归属的银行。②平台受何限制——香港例外包云和分析不转移责任；内地例把平台/产品集中纳入银行风险管理。

③资料根据是什么——香港 CDI 以同意为基础，支持评估不替代银行判断；内地列合法目的、必要性、保护和生命周期治理。④还有何监管——香港例列 OR-2 运营韧性及 AML、私隐、公平、客户保护；内地例列服务、催收、营销、定价、同意、投诉与模型。

**英文课堂归纳（笔记自拟）**：Identify the regulated entity, the lawful basis for data use, and the party bearing default losses. Outsourcing does not by itself transfer accountability. The slide compares regulatory functions, not a verified statement of every current legal requirement. 这里按课件有日期比较，未另核现行法。

### 2.41 p.41 · 三十秒批准却仍可能失败

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Fast Approval Can Still Be a Regulatory Failure

Scenario: A platform approves a loan in thirty seconds using phone and transaction data, but
the customer does not understand the data consent or total repayment.


Control                  Evidence the platform should preserve
Consent                  which data were collected, for what purpose, and for how long
Fair decision            model inputs, adverse-action reason, override, and appeal
route
Affordability            income, obligations, repayment schedule, and stress assump-
tions
Disclosure               total cost, late consequences, complaints, and collections pro-
cess

A smooth interface does not substitute for informed consent and accountable credit judgment.

</details>

给定情境中平台用手机和交易数据 30 秒批准，但客户不懂数据同意与总还款。讲义已经列四种应保留证据：

- 同意须说明什么数据/目的/多久。
- 公平决定留输入、不利决定理由（Adverse-action reason）、人工改判和申诉。
- 可负担性（Affordability）留收入、其他义务、还款表和压力假设。
- 披露留总成本、逾期后果、投诉及催收。

**⚪ 笔记分析**：快界面不能代替知情同意与可追责判断。不能仅由情境断言某项现行法律已违反，但足以识别需要修复的控制缺口。

**English reference answer**: Preserve meaningful consent, decision inputs and reasons, affordability evidence, and the full repayment and complaint terms. A fast approval does not show that the customer understood the data use or repayment obligation.（笔记自拟）

### 2.42 p.42 · 信用分只是整条服务链的一环

![L11 p.42：贷款系统五层职责](figures/m11/source-p42.png)

来源：L11 p.42，保留整页原图，可打开大图辨认原标签。

原图复用 p.10 四图标，但右侧新增五层职责：

1. 申请层有界面、电子签名和 API，负责同意记录。
2. 身份/欺诈层核文件、设备、网络及异常。
3. 信用决定层有特征、分数和政策引擎，负责负担能力、价格、理由、公平。
4. 出资/服务层有银行接口和流程，负责贷款人、流动性、结算及困难客户。
5. 监测层有数据仓库/看板，负责批次损失、漂移、供应商与纠正。

模型漂移（Model drift）指模型面对的资料/关系改变使原预测不再保持表现。即使分数输出成功，云服务失败、扣款错或资金不足仍会使服务失败。因此不能把“模型 API 返回了分数”当全链完成。

### 2.43 p.43 · 服务中断先保住哪些动作

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Lending Services during a System Outage




Scenario: The identity or cloud provider fails during a peak shopping period.

Immediate product choices                         Controls needed beforehand
- pause new approvals or queue                    - tested recovery arrangements and data
applications for review;                          backups;

- keep existing repayment services                - clear responsibility for customer
available.                                        communication and service restoration.





</details>

情境是购物高峰身份或云供应商失效。讲义给的立即选择是暂停新批准或把申请排队复核，同时尽量维持既有还款服务；事前控制是经过测试的恢复安排/备份，以及清楚的客户沟通和恢复责任。

**⚪ 笔记分析**：不要为维持表面批准率而跳过缺失身份核查；也不能把新批暂停理解为所有客户都无需还款。恢复后要核重复申请、状态和账目，避免排队期间重复放款（补充）。

**English reference answer**: Pause new approvals or queue applications for review while maintaining existing repayment services where possible. Use tested recovery arrangements, backups and clear communication responsibilities rather than bypassing the missing control.（笔记自拟）

### 2.44 p.44 · API 接起服务不改变风险归属

应用程序接口（Application programming interface，API）让软件按约定交换请求和结果，例如商户收银页面向贷款人请求报价，再显示给客户。它可连接数据提供者、支付网络、商户及银行，把贷款嵌进购物、工资或银行流程。

课件用 Affirm 在销售点结账提供融资为例。经济问题仍是获客、承贷、出资、服务和客户关系分别归谁；接口只是连接方法。一个商户页面展示某贷款人报价，不自动使商户承担全部贷款损失，须看合同。

### 2.45 p.45 · 共享登记与八成融资上限

![L11 p.45：登记与融资上限三步](figures/m11/source-p45.png)

来源：L11 p.45，保留整页原图，可打开大图辨认原标签。

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Shared Records Do Not Replace Credit Assessment

Return to Class 6: One RMB1 million receivable, an 80% financing cap, and RMB600,000
already lent by Bank A.

1. Check the record                         2. Apply the cap                      3. Decide whether to lend
Bank B sees the same                                                              Will the buyer pay the
receivable and Bank A’s                           800, 000 − 600, 000             invoice? Bank B still
existing RMB600,000 loan.                                                         assesses repayment capacity
At most RMB200,000                    and expected loss.
remains available against
this receivable.

Shared records help prevent duplicate financing; they do not guarantee repayment.

Hypothetical example; assume the shared record captures all existing financing.



</details>

讲义沿 Class 6 的假设：应收款人民币 100 万，总融资上限 80%，A 银行已有 60 万贷款，且登记完整捕捉现有融资。B 先查记录，再算总上限 $1,000,000\times80\%=800,000$，扣已有 600,000，最多余 200,000 元额度。

“最多”不是银行必须再贷 20 万。B 还要判断买方是否会付款、预期损失和其他贷款条件；登记支持防重复融资，不保证还款。若已有贷款改为 75 万，剩余上限为 5 万；若登记不完整，20 万计算的输入本身也可能不可靠。

**English reference answer**: At most RMB200,000 remains under the aggregate cap, assuming the shared record is complete. Bank B must still assess repayment capacity and expected losses before lending.（笔记自拟）

### 2.46 p.46 · 排序正确而概率偏低可以同时发生

给定表每行是一个已完整观察 12 个月的借款群：A 预测 2%、实际 4%；B 预测 5%、实际 8%。排序（Ranking）在两列都是 B 比 A 风险高；校准（Calibration）问预测概率水平是否与实际比例相符，这里两组都低估。

A 低估 2 个百分点、B 低估 3 个百分点，不是“两组各低 2%/3%”的相对百分比。应先核可比群组和资料，再重估损失、价格和批准规则；两行汇总没有样本量与不确定性，不能据此证明任意精度或必然因果变化。排名有用不等于预计损失可不改。

### 2.47 p.47 · 选择题：上线后应怎样监测

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Multiple-Choice Question: A Credit Model after Launch



A lender’s model still ranks riskier borrowers above safer ones. Across several completed loan
cohorts, actual default rates exceed its predicted rates. The recorded borrower mix is similar.

What is the most appropriate next step?

A) Keep loss estimates unchanged because the risk ranking still works.

B) Increase approvals to spread the observed losses over more loans.

C) Investigate the forecast gap and reassess expected losses and pricing.

D) Remove default outcomes from monitoring until the model is retrained.




</details>

**中文题意**：数个已完成贷款批次中，实际违约率持续高于预测，而风险排序仍有用、记录中的借款人组成相似。A 保持损失估计；B 多批贷款摊薄损失；C 查预测差并重估损失/价格；D 在重训前移除违约监测。

**⚪ 参考答案（笔记推断）：C。** 排序没有保证概率校准正确；A 延续低估损失，B 增加放款可能扩大风险而非修复估计，D 主动隐藏最重要反馈。记录组成相似也不排除遗漏变量或环境变化，应调查而不是直接确定原因。

**English reference answer**: C. Investigate the forecast gap and reassess expected losses and pricing. Useful risk ranking does not justify keeping underestimated loss levels unchanged, and default outcomes must remain in monitoring.（笔记自拟）

### 2.48 p.48 · Aave 与无抵押小企贷的决定依据不同

原表左边 Alice 保留 ETH 风险敞口，以价值 US\$30,000 的 10 ETH 抵押借 15,000 USDC；借款能力由抵押值和协议限额决定。价格下跌可能在她还没漏还任何款项前触发清算（Liquidation，即按协议处理抵押物偿债）。

右边微业贷为小企备货提供线上无抵押营运贷，重点是企业未来还款能力，不是其是否持币；销售差可导致漏还和贷款损失。两边都叫借款，却不能拿 Aave 的抵押率直接代替企业承贷判断。金额是 Class 8 的课堂例，不是实时协议报价。

### 2.49 p.49 · 卖出贷款后四百美元损失谁承担

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Who Bears the Loss on a Sold Loan?

WeLab Bank reports customer loans on its balance sheet. Compare three hypothetical con-
tracts for a loan that subsequently defaults:
Principal loss = \$1, 000 − \$600 recovered = \$400 .



Bank retains the loan                      Sale without a guarantee                   Sale with a \$100 first-loss
Bank loses \$400.                           Investor loses \$400.                       guarantee
Bank loses \$100; investor
It funded and still holds the              The bank has no contractual                loses \$300.
loan.                                      credit-loss obligation.
The bank retains some
credit exposure.
Principal losses only; guarantees honoured. Contracts are illustrative, not WeLab’s terms. Company context: WeLab Bank 2025
Interim Report, note 13.


</details>

讲义假设本金 1,000、回收 600，所以仅本金损失 $1,000-600=400$ 美元，且担保按承诺履行；这不是 WeLab 实际合同。

三种合同逐项比较：银行留贷，由银行损失 400；无担保售出且无其他信用补偿义务，由投资者损失 400；售出但银行担保首损 100，银行承担 100、投资者承担余下 300。三种都加回总损失 400，不能把销售收入或服务费当自动抵销损失。

**English reference answer**: The principal loss is \$400. The bank bears it if it retains the loan; the investor bears it after a sale without a guarantee. With an honoured \$100 first-loss guarantee, the bank bears \$100 and the investor bears \$300.（笔记自拟）

若回收改为 950、损失 50，首损担保下银行只补 50，不是每次违约一律付满 100。

### 2.50 p.50 · 降低成本与增加信用损失分开重算

![L11 p.50：同基准三场景贡献柱图](figures/m11/source-p50.png)

来源：L11 p.50，保留整页原图，可打开大图辨认原标签。

柱图纵轴是每笔贡献美元，三根从同一 p.19 基准开始：基准 10；经营成本从 30 降为 20、其余不变，贡献 $120-55-25-20=20$；预期损失从 55 升为 65、其余沿原基准，贡献 $120-65-25-30=0$。

图下强调 Two separate changes，不能把后一场景错误接成“已经省 10 再多亏 10”的连续变化。若同时发生，贡献是 10（笔记补充），但那是第四种情境，不是原图第三根柱。数字为一年期假设、未扣管理间接费用。

### 2.51 p.51 · 预测增长前先问四种压力

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Stress the Lending Model before Forecasting Growth


Shock                      Cash-flow question                Evidence to monitor
Borrower stress           Who absorbs higher defaults        delinquency, roll rates, recoveries
and collections cost?
Funding withdrawal        Can originations and existing      funding concentration, maturity,
loans still be funded?             covenants
Acquisition inflation     Does growth still cover cus-       repeat use, contribution margin,
tomer acquisition cost?            payback period
Control failure           Who pays for fraud, bias, cy-      complaints, overrides, incidents,
ber loss, or remediation?          audit findings

A growth forecast is incomplete until the platform survives plausible credit, funding, and operating
shocks.


</details>

原表四行分别是借款人压力、资金退出、获客涨价、控制失败，每行都有现金流问题。**参考逐行解释**：

- 违约变多时核谁吸收损失/催收成本，监测逾期、从轻度到重度逾期的迁移率（Roll rate）和回收。
- 资金退出时核新贷与旧贷是否都能继续融资，监测集中、期限和合同约束。

- 获客涨价时核交易增长是否仍覆盖新客成本，看重复使用、贡献率与回本期。
- 控制失败时核欺诈、偏差、网络攻击和补救由谁付，看投诉、人工改判、事故和审计发现。

**English reference summary**: Stress borrower losses, funding availability, acquisition costs and control failures separately. Trace who pays, which cash flows change, and which evidence would reveal the deterioration before forecasting growth.（笔记自拟）

### 2.52 p.52 · 简答：七成新贷资金退出

<details markdown="1">
<summary>讲义英文原题／给定情境与步骤（非笔记答案）</summary>

Short-Answer Question: A Lending Platform Loses a Funder


A marketplace lender earns origination and loan-servicing fees. An investor providing 70% of
new-loan funding stops financing new loans.

Existing loans remain fully funded to maturity and perform as agreed. The platform provides
no credit guarantees.


1. Explain the likely effects on new lending, origination fees, and fees from servicing existing
loans.

2. Propose one way to reduce dependence on this funder. Explain a cost or trade-off of your
proposal.




</details>

**中文拆题**：提供新贷款资金 70% 的投资者停止新出资；题面明确旧贷已足额融资到期且正常还款，平台没有信用担保。不能擅自把它改成旧贷款也抽资或已违约。

**⚪ 第 1 问参考作答（笔记推断）**：若无替代资金，新放贷能力下降，承做费随新业务减少；既有贷款仍正常运行，其服务费可继续按原合同赚取，不因新资金退出立刻归零。70% 是新资金占比，不证明总收入必跌 70%，也不唯一决定实际贷款降幅，其他出资者可能调整。

**第 2 问**：引入更多资金伙伴并分散到期安排可降低单一依赖，代价是关系维护、尽调和可能较高资金价格；不必为凑答案建议用高风险自有资金填满所有缺口。

**English reference answer**: Without replacement funding, new lending and origination fees are likely to fall, while servicing fees on fully funded, performing existing loans can continue under their contracts. The 70% funding share does not imply a 70% decline in total revenue. Diversifying investors can reduce concentration, but adds due-diligence costs and may raise funding prices.（笔记自拟）

若改题为旧贷也需短期续资，就要另查到期流动性；本题刻意排除该条件。

### 2.53 p.53 · 把资金、贡献与理由串起来

本页三条复习：Upstart 促成贷款可由伙伴银行、机构或自身持有；假设千元小企贷多 10 损失即消除 10 贡献；课件称 Upstart 给被拒申请人解释原因的不利决定通知。最后一项是讲义产品服务陈述，未另核当前法定义务或网站。

这三点分别回答谁持风险、业务是否划算、决定能否说明。不能以资金不在平台账上就忽略担保，也不能以接口能很快拒绝就忽略客户理解和申诉。

### 2.54 p.54 · 三条结论应能迁移到新案例

本页总结：承做不等于最终出资，Upstart 的发起银行未必是最终投资者；数字贷款仍有信用风险，微业贷的无抵押客户可能违约；支持项目未必是投资，Kickstarter 的奖励不是股权或利息。

遇到新 App，先画借款人、审核/承做者、出资者、服务者与损失承担者，再看费用和权利。名字叫科技、平台或银行都不能替代真实合同；众筹筹足钱也不能替代交付能力证据。无本讲转录，不把这三条写成教授明示考试题。

## 3. 一图看懂

下表是一笔贷款的职责追踪，每行回答一种问题，不能用同一个 App 名字跳过其他行。

| 问题 | 查什么 | 本文位置 |
|---|---|---|
| 谁把申请变成贷款 | 承做、审核与报价 | p.5/8 |
| 谁现在付本金 | 银行、投资者或平台 | p.14–16/23 |
| 谁最终亏钱 | 持有与担保合同 | p.27/49 |
| 谁维护还款与客户 | 服务、申诉、恢复 | p.37/41–43 |
| 什么证明模型有用 | 同批样本外、校准和损失 | p.12/24/46 |

例如平台不出本金，也可能因首损担保承担最后一行以外的信用损失；模型排名好也不能代替资金供给。

## 4. 速查表

每行金额仅限原假设，先看单位和合同再复用。

| 任务 | 结果 | 条件 |
|---|---|---|
| 小企贷贡献 p.19 | 120−55−25−30 = 10 美元 | 一年期，管理费前 |
| 预期损失 p.26 | 4% × 50% × 1,000 = 20 美元 | 同一笔本金 |
| 税前利润 p.26 | 80−30−15−20 = 15 美元 | 按题给预期收入 |
| 众筹费 p.32 | 筹 20,000，平台费 1,000 美元 | 5%，支付费另扣 |
| 融资余量 p.45 | 800,000−600,000 = 200,000 元 | 人民币，总登记完整 |
| 首损分配 p.49 | 总损 400，银行 100、投资者 300 | 首损担保履行 |

## 5. 双语术语卡

英文定义为笔记自拟，原例与当地解释在所列页。

| 中文 | English | 英文定义 | 位置 |
|---|---|---|---|
| 承贷评估 | Underwriting | Assessment of borrower risk and proposed loan terms. | p.6/10 |
| 贷款承做 | Origination | Work to arrange, assess and establish a new loan. | p.5 |
| 资金提供 | Funding | Supply of money supporting the loan. | p.5/14 |
| 违约概率 | Probability of default | The estimated probability of default over a stated horizon. | p.26 |
| 违约损失率 | Loss given default | The fraction lost conditional on default under the stated definition. | p.26 |
| 校准 | Calibration | Agreement between predicted probabilities and observed outcome rates. | p.46 |
| 首损担保 | First-loss guarantee | A contractual promise to absorb losses up to an agreed first-loss amount. | p.27/49 |
| 全有或全无 | All-or-nothing funding | Collection of pledges only if the campaign meets its target by the deadline. | p.31 |
| 请求权 | Claim | An identified contractual right to payment, ownership or performance. | p.30/39 |

## 6. 考点预判与英文答题顺序

本讲没有可核转录，不标教授明示。本节为 🟡 讲义目标反推和 ⚪ 笔记推断。

贷款模式题先写 borrower、originator、funder、servicer、loss bearer，再用合同支持归属；盈利题先固定期间/本金，再扣预期损失、资金和经营成本；模型题先固定同批测试与完整观察窗，再分 ranking/calibration/losses。众筹题先识别支持者 claim，再分“筹款条件达成”与“生产交付有能力”。p.24/26/27/38/47/52 已有完整英文题与自拟回答，不把参考答案当官方。

## 7. 自测

以下为笔记补充，不代表本人已作答或通过。

### 7.1 概率排名正确，能保持原损失估计吗？

<details>
<summary>查看答案</summary>

不能仅凭排名不变保留估计。p.46 的 A/B 排序都对，但预测 2%/5% 对实际 4%/8% 低估概率，应查可比性和预测差，再重估损失与价格。

</details>

### 7.2 千元贷款 PD 由 4% 升到 8%，其余沿 p.26，税前利润多少？

<details>
<summary>查看答案</summary>

预期损失 $0.08\times0.5\times1,000=40$ 美元，利润 $80-30-15-40=-5$ 美元。只改 PD，不把经营成本也改成别页数字。

</details>

### 7.3 卖出贷款后担保首损 100，实际本金损失只有 50，银行付多少？

<details>
<summary>查看答案</summary>

沿 p.49 条款银行只承担实际首损 50，投资者此例承担 0。100 是约定层上限，不是每次固定赔款。

</details>

### 7.4 众筹达标并收钱，证明产品能按期完成吗？

<details>
<summary>查看答案</summary>

不证明。p.31/38 的规则只建立足够承诺需求并允许收款；成本、生产、质量和交付仍待证据，不产生平台保证。

</details>

### 7.5 新出资者退出，旧贷服务费是否必定归零？

<details>
<summary>查看答案</summary>

按 p.52 的明确条件，旧贷已足额融资到期且正常，服务费可按合同继续。新贷承做费会受资金缺口影响；不能把新资金退出偷换成旧贷款抽资或违约。

</details>

## 8. 讲义页码映射

每页一行；课堂覆盖均未知。原图页给阅读入口，文字表格仍逐项解释。

| L11 物理页 | 原页标题 | 精确正文 | 原图／处置 |
|---|---|---|---|
| 1 | FinTech and AI in Finance | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.1 p.01 · 本讲范围与来源边界\|p.1]] | 纯封面/分隔 |
| 2 | Digital Lending and Credit Decisions | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.2 p.02 · 数字信贷与信用决定\|p.2]] | 纯封面/分隔 |
| 3 | Assessing a Borrower with Limited Credit History | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.3 p.03 · 只有十二个月现金流怎样判断借款人\|p.3]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 4 | Why a Small Business May Struggle to Borrow | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.4 p.04 · 小额贷款为何也可能很贵\|p.4]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 5 | The Digital Lending Process | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.5 p.05 · 数字贷款四格流程\|p.5]] | 原图整页保留并解释 |
| 6 | Where FinTech Changes the Lending Model | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.6 p.06 · 技术改变流程的哪三处\|p.6]] | 原图整页保留并解释 |
| 7 | Case 1: Ant Group — Ecosystem Lending | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.7 p.07 · Ant 的支付生态怎样支持贷款\|p.7]] | 原图整页保留并解释 |
| 8 | Ant Case: Following a Digital Loan Application | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.8 p.08 · 沿商户一次申请追踪三种责任\|p.8]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 9 | Ant Group: Credit Services and Lending Responsibility | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.9 p.09 · 贷款服务与最终信用责任分开\|p.9]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 10 | Automation and Scalability in Lending | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.10 p.10 · 自动化怎样降成本又保留复核\|p.10]] | 原图整页保留并解释 |
| 11 | Credit Predictors and Model Interpretation | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.11 p.11 · 变量重要为何不能证明因果\|p.11]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 12 | Evaluating Default Predictions | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.12 p.12 · 十二个月违约预测如何公平评估\|p.12]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 13 | How Digital Lending Models Evolved | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.13 p.13 · 四种贷款模式是重叠路线\|p.13]] | 原图整页保留并解释 |
| 14 | LendingClub: From P2P Lending to Happen Bank | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.14 p.14 · LendingClub 案例怎样分留存与出售\|p.14]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 15 | Investor Cash Flows in Marketplace Lending | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.15 p.15 · 投资者的回款先扣什么\|p.15]] | 原图整页保留并解释 |
| 16 | Upstart: AI Lending and Outside Funding | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.16 p.16 · Upstart 的两个判断问题\|p.16]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 17 | WeBank: Working Capital for Small Firms | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.17 p.17 · 微业贷为何需要无抵押评估\|p.17]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 18 | WeBank: Data, Approval, and Repayment | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.18 p.18 · 额度与价格怎样接到贷后结果\|p.18]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 19 | WeBank Case: Can a Small Loan Cover Its Costs? | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.19 p.19 · 一千美元小贷款能留多少贡献\|p.19]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 20 | Case 2B: WeLab Bank — A Hong Kong Digital Bank | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.20 p.20 · WeLab Bank 案例保留银行责任\|p.20]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 21 | HKSAR Evidence: CDI and SME Loan Terms | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.21 p.21 · CDI 研究图能证明到哪一步\|p.21]] | 原图整页保留并解释 |
| 22 | China’s Policy on Internet-Assisted Lending after 2025 | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.22 p.22 · 互联网助贷政策在课堂模型中的作用\|p.22]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 23 | Similar Apps Can Hide Different Lending Models | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.23 p.23 · 三地相似 App 的资金与脆弱点\|p.23]] | 原图整页保留并解释 |
| 24 | Multiple-Choice Question: Did the AI Model Really Improve? | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.24 p.24 · 选择题：新 AI 是否真的改进\|p.24]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 25 | Where the Risk Sits in Each Lending Model | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.25 p.25 · 四种模式没有把风险消掉\|p.25]] | 原图整页保留并解释 |
| 26 | Multiple-Choice Question: Expected Profit on One Loan | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.26 p.26 · 选择题：预期损失与税前利润\|p.26]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 27 | Multiple-Choice Question: Funding and Retained Credit Risk | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.27 p.27 · 选择题：银行出资是否消除平台风险\|p.27]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 28 | Crowdfunding | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.28 p.28 · 众筹分隔\|p.28]] | 纯封面/分隔 |
| 29 | Kickstarter: Why Creators and Backers Need Each Other | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.29 p.29 · 作品未完成为什么先有人支持\|p.29]] | 原图整页保留并解释 |
| 30 | Types of Crowdfunding | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.30 p.30 · 四类众筹先看支持者请求权\|p.30]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 31 | Kickstarter: How the Business Model Works | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.31 p.31 · 全有或全无解决哪种筹资门槛\|p.31]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 32 | Kickstarter: A Board Game Example | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.32 p.32 · 五百人支持桌游怎样分资金\|p.32]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 33 | Kiva and Kickstarter: What Does the Funder Receive? | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.33 p.33 · Kiva 与 Kickstarter 的资金权利\|p.33]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 34 | Aﬀirm and Kickstarter: Two Funding Models | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.34 p.34 · 创办理念怎样变成合同规则\|p.34]] | 原图整页保留并解释 |
| 35 | Lending Operations and Credit Risk | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.35 p.35 · 贷款运营与信用风险分隔\|p.35]] | 纯封面/分隔 |
| 36 | Digital Lending Crosses Several Regulatory Perimeters | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.36 p.36 · 一个数字入口不等于一种许可\|p.36]] | 原图整页保留并解释 |
| 37 | Key Regulatory Requirements and Violations | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.37 p.37 · 监管要求要能找到哪种证据\|p.37]] | 原图整页保留并解释 |
| 38 | Short-Answer Question: What Did the Funding Threshold Prove? | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.38 p.38 · 简答：众筹达标证明了什么\|p.38]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 39 | Invoice Finance: Cash Now, Payment Later | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.39 p.39 · 卖掉整笔应收款与抵押借款不同\|p.39]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 40 | Two Regimes Ask the Same Questions Differently | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.40 p.40 · 两种制度共同要问哪三个对象\|p.40]] | 原图整页保留并解释 |
| 41 | Fast Approval Can Still Be a Regulatory Failure | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.41 p.41 · 三十秒批准却仍可能失败\|p.41]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 42 | A Credit Score Is One Part of the Lending Workflow | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.42 p.42 · 信用分只是整条服务链的一环\|p.42]] | 原图整页保留并解释 |
| 43 | Lending Services during a System Outage | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.43 p.43 · 服务中断先保住哪些动作\|p.43]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 44 | APIs Turn a Lender into an Embedded Service | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.44 p.44 · API 接起服务不改变风险归属\|p.44]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 45 | Shared Records Do Not Replace Credit Assessment | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.45 p.45 · 共享登记与八成融资上限\|p.45]] | 原图整页保留并解释 |
| 46 | Model Monitoring: Good Ranking, Wrong Default Rates | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.46 p.46 · 排序正确而概率偏低可以同时发生\|p.46]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 47 | Multiple-Choice Question: A Credit Model after Launch | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.47 p.47 · 选择题：上线后应怎样监测\|p.47]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 48 | Aave and WeBank: Different Borrowers, Different Decisions | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.48 p.48 · Aave 与无抵押小企贷的决定依据不同\|p.48]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 49 | Who Bears the Loss on a Sold Loan? | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.49 p.49 · 卖出贷款后四百美元损失谁承担\|p.49]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 50 | The Same Loan: Lower Costs or Higher Credit Losses | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.50 p.50 · 降低成本与增加信用损失分开重算\|p.50]] | 原图整页保留并解释 |
| 51 | Stress the Lending Model before Forecasting Growth | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.51 p.51 · 预测增长前先问四种压力\|p.51]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 52 | Short-Answer Question: A Lending Platform Loses a Funder | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.52 p.52 · 简答：七成新贷资金退出\|p.52]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 53 | Lending Business Model Review | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.53 p.53 · 把资金、贡献与理由串起来\|p.53]] | 文字/表格逐项解释；品牌Logo不作机制图 |
| 54 | What to Remember | [[EF5560_Fintech_and_AI_in_Finance/notes/M11-数字信贷与众筹#2.54 p.54 · 三条结论应能迁移到新案例\|p.54]] | 文字/表格逐项解释；品牌Logo不作机制图 |

## 9. 延伸与勘误

### 9.1 课堂未核范围

没有 M11 转录，课堂跳页、教授补充、考试暗示、实际日期/周次均未知；54 页书面内容保持学习范围，没有把无录音当成课上略过。

### 9.2 来源地位

原文块为讲义题面和给定步骤，中文推理与英文答案据实际标注，未当作教师官方解答。假设交易/公司例不等于真实产品条款；没有替用户贷款、付款、投资或提交练习。

### 9.3 课件与原图限制

p.10/42 的自动贷款图以图标循环呈现，不按图面空间顺序推定首次贷款先有还款监测；实际主链按 p.5，贷后反馈用于未来更新。p.29 原图 CREATO 标签不完整，保留原貌。p.34 肖像注明 AI 插画，不作真实人物照片。

### 9.4 外部事实待核

p.14 的 LendingClub/Happen 2026 变更，p.21 研究方法细节，p.22/36/40 政策与法条现行性，以及所有公司产品/资金比例，均仅据讲义版本。本批未重新取得全部一手外源，不将其写成实时公司身份、现行法律建议或最新产品保证；公式机制不依赖补造外部事实。

### 9.5 计算和剩余数据

本讲给定 p.19/26/27/32/45/46/49/50 的数字可按正文复做；CDI 原始样本、公司合同、具体发票折价和模型训练资料未提供，不冒称完整复跑或唯一责任判定。p.39 卖整笔债权与 p.45 抵押式总额上限借贷是不同合同，不能把二者合并计算。
