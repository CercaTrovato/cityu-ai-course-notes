# M06 逐页源诊断

- `EF5560_Fintech_and_AI_in_Finance\course_files_export\Lec06_FinTech_Overview_and_Blockchain.pdf`，SHA-256 `de9e13012989b16db317851fb1c698aa2fa0b6b46bc4fa2330d25fda3ba4ad17`。
- 当前原笔记 SHA-256 `ee55bc961b3c7a0f86520c50131a85ecb71ebaab903e517c4f8afd86afd946ce`。

作者实际打开对应的全部联系表，图义与布局文本互证。下表是已读源页和拟保留要素。最终候选 SHA-256 f9aa542d074d5720f0dc9e0fa95bc3ef5b1695038c5d1d2eedf4f7d83a8503c1，独审已回核全部 54 页。

| 物理页 | 原题名 | 本页教学要素 | 图或页处置 |
|---:|---|---|---|
| 01 | FinTech and AI in Finance | FinTech 概览与区块链。 | 封面或分隔 |
| 02 | FinTech Businesses | 进入金融服务成本与技术商业模式。 | 封面或分隔 |
| 03 | What Do We Need Financial Services For? | 收款、先融资付供应商、留现金付工资。问技术在哪里减少等候或手工核对。 | 文字、公式、代码或表格 |
| 04 | Why Are Financial Services Costly? | 了解借款人信息、处理文件和异常、跨商户/支付方/银行核账，即使小额也要做。 | 文字、公式、代码或表格 |
| 05 | What Can Technology Change? | 授权销售数据支持授信、软件自动对账、系统共享状态减少重复检查。服务变快仍要覆盖技术成本。 | 文字、公式、代码或表格 |
| 06 | FinTech: Payments and Funding | 支付宝和 Stripe 支付服务，WeBank 放贷，Kickstarter 奖励众筹。费用由谁付、贷款与项目失败分别由谁承担，按合约辨别。Logo 装饰。 | 文字、公式、代码或表格 |
| 07 | FinTech: Investment and Risk Management | Betterment/AQUMON 自动投顾；Darktrace 检测，RegTech 可处理客户核验与文本。比较费用能否覆盖小户成本、误报警后的净节省。Logo 装饰。 | 文字、公式、代码或表格 |
| 08 | FinTech: Digital Assets | Ledger 硬件钱包管密钥，Aave 抵押借贷，Circle/Tether 美元挂钩代币。问谁控制资产、谁承担损失、储备能否兑付。Logo 装饰。 | 文字、公式、代码或表格 |
| 09 | The Layers of a FinTech Product | 从客户向下看界面、金融服务、支付数据基础设施、治理风险。支付按钮在界面，真正的扣款清算在底层，规则和授权管得住才可用。 | 产品五层 |
| 10 | Transaction Volume and Fee Revenue | 10 万笔×40 美元=400 万美元；按 0.5% 收费得 2 万美元，处理、欺诈、客服和合规仍须扣。 | 文字、公式、代码或表格 |
| 11 | Scale and Average Processing Cost | 固定 1 万、每笔变动 .05。横轴 1 万/5 万/10 万笔，纵轴每笔美元，柱高 1.05/.25/.15；固定部分被更多笔分担。 | 规模成本柱图 |
| 12 | What Do Economists Mean by Money? | 支付媒介、记账单位、价值储藏。问题用支付采用、标价和购买力稳定三个证据判断比特币。 | 文字、公式、代码或表格 |
| 13 | Bitcoin Began as a Two-Person Test | 课件例 2009-01-12 中本聪向 Hal Finney 转 10 BTC。后者独立运行并反馈。编辑插画不作身份鉴证。 | 文字、公式、代码或表格 |
| 14 | Bitcoin as Money | 课件认为支付部分满足、价值储藏有争议、广泛记账仍有限，说明采用范围和波动的条件。 | 文字、公式、代码或表格 |
| 15 | How a Blockchain Works | 进入账本、签名和共识。 | 封面或分隔 |
| 16 | Ledgers, Blockchains, and Tokens | 账本记录余额权属或义务，区块链把记录批次相连并维护共享历史，代币是账本上的数字单位。发票账本可不发公开交易代币。 | 文字、公式、代码或表格 |
| 17 | The Exporter’s Working-Capital Gap | 原图今天发货→银行先垫现金→60 日买方付钱。贷款弥补付工资与收款错期，纠纷可延迟回款。 | 应收时序 |
| 18 | Two Banks, One Export Receivable | 应收 100 万、A 已贷 60 万、B 再申请 60 万。总额上限 80 万，查既有融资后才知只余 20 万，未上报会漏。 | 文字、公式、代码或表格 |
| 19 | Who May Read and Update the Ledger? | 对照参与、读记录和治理。公有按协议开放，许可仅授权机构读写，可限制敏感贸易记录。 | 文字、公式、代码或表格 |
| 20 | Hashing: A Digital Fingerprint of a Record | 原 1 万发票得 Hash A，可信记录存 A；改 9 万得 B；比较 A≠B 触发异常。检的是字节与可信副本，不证明贸易真实。 | 发票哈希四格 |
| 21 | Private Keys, Public Keys, and Signatures | 私钥授权→签过的指令→公钥核验。验证者无需得到私钥，签名也不等于真实姓名或有业务审批。 | 密钥签名流程 |
| 22 | A Signature Exercise without Code | Alice 签消息 A，Bob 用公钥核验。换成消息 B 哈希变化，旧签名失效；另核资金和双花。 | 文字、公式、代码或表格 |
| 23 | A Transfer from Instruction to Confirmation | 提交签名、节点查授权与可用资金、收入区块、等待确认再交付。 | 交易确认流程 |
| 24 | Blocks Link the Transaction History | 100 引 99、101 引 100、102 引 101。沿箭头往过去读，改 100 会影响后续链接；共识选有效历史。 | 引用前一块 |
| 25 | The Double-Spending Problem | 原图同一个 1 BTC 分向 Bob/Carol；两条指令可以都签得对，共识接受的历史至多承认其中一条。 | 双花两支 |
| 26 | Consensus and Economic Incentives | PoW 矿工投入设备和电力；PoS 验证者质押。奖励和惩罚影响出块动机，节点仍核交易是否有效。 | 文字、公式、代码或表格 |
| 27 | Confirmations and Settlement Confidence | 原图入块→下一块→更多块。等待时间按金额及规则，降低重组风险，价格与托管风险另在。 | 确认时序 |
| 28 | Private Keys and Authorization Failures | Bybit 课件估约 14.6 亿美元且界面误导授权，Ronin 约 6.2 亿美元且拿到 9 键中的 5 键。问能批准谁、批准什么，分别核内容与独立控制。 | 文字、公式、代码或表格 |
| 29 | Multiple-Choice Question: Custody and Access Control | 共用管理口令使两个审批账户可被同一人控制；分开凭据并限制改权限，课堂确认 B。 | 文字、公式、代码或表格 |
| 30 | Recorded Information and Business Reality | 发票未变与发货、签名有效与员工授权、贷款已记与可还款是三对不同核查。 | 文字、公式、代码或表格 |
| 31 | When a Shared Ledger Is Useful | 多个独立主体共用记录，对账有损耗，且能协商访问、纠错和治理；单一可信主体可用数据库。 | 文字、公式、代码或表格 |
| 32 | Multiple-Choice Question: Export Finance in China | D 核贸易单据及已有融资。未改文件、平台用户多、同软件分别无法证明信用与应收状态。 | 文字、公式、代码或表格 |
| 33 | Multiple-Choice Question: A Shared Ledger for US Banks | 合约和资金安排不变时，C 减少对账与差错处理；资金义务、违约承担和存款保障不自动变化。 | 文字、公式、代码或表格 |
| 34 | Blockchain in Financial Services | 进入已有案例与收益证据。 | 封面或分隔 |
| 35 | Blockchain Applications in China | 课件列 SAFE 出口融资、深圳区块链发票、法院电子记录。分别解决既有融资、重复报销和证据后续校验。 | 文字、公式、代码或表格 |
| 36 | SAFE: Export Receivables Financing | 申请提交单据、银行核报关和已有融资、参与银行记贷与还。授权后可看收付汇；授信仍银行作决定。 | 文字、公式、代码或表格 |
| 37 | Worked Example: Duplicate Receivables Financing | 深色 A 已贷 .6 百万，浅色 B 新贷。左 B 再贷 .6，总 1.2 超 .8 虚线；右 B .2 总 .8。上限仅教学设定。 | 贷款两柱 |
| 38 | Worked Example: Financing a Receivable | 60 万×6%×60/360=6000 元，无其他费用。单据更快验证影响到账时点，计息仍按金额、利率、期间。 | 文字、公式、代码或表格 |
| 39 | Shenzhen: Electronic Invoice Records | 商户开票→客户报销→雇主查状态，统一票号串联多系统。关键输入是更新的报销状态。 | 发票报销三步 |
| 40 | Worked Example: Two Claims for One Invoice | SZ-1048 已报 800 元，B 再提交同号触发复核，挡下可避免多付 800 元。 | 文字、公式、代码或表格 |
| 41 | China: Electronic Evidence in Courts | 原文件→带时间的登记→以后核验。链可协助核登记后是否改，来源和关联由法院审查。 | 电子证据三步 |
| 42 | LLMs and Shared Trade Records | LLM 提取 EX-204、人民币 100 万、60 天→银行对单据合同→账本记录融资。字段提取和贷款判断分开。 | LLM 与人工银行核验 |
| 43 | J.P. Morgan: Corporate Cash across Time Zones | 课件 Kinexys 区块链存款账户在支持网络内近实时，Siemens 例扩展链上外汇；账户和币种仍受约束。公司标识装饰。 | 文字、公式、代码或表格 |
| 44 | J.P. Morgan: Programmable Treasury Payments | 余额 70 万→司库转 30 万→回到 100 万。企业设授权并供现金，银行提供执行。 | 可编程补款 |
| 45 | J.P. Morgan Case: The Value of Faster Cash Transfers | 柱高从 2.0 降 1.2 百万美元，释放 .8 百万，按 4% 年替代收益为 3.2 万。教学假设，扣实际服务成本再判断。 | 闲置现金柱图 |
| 46 | Short-Answer Question: Evaluating a Trade-Finance Platform | 辨重复融资、已验证仍不还的原因、前后可比较指标。课堂讲评不完整，按原题保留。 | 文字、公式、代码或表格 |
| 47 | Broadridge: Funding a Dealer during the Day | 以证券作抵押借现金，事后反向交割。DLR 协调现金和抵押品的记录，不只隔夜。 | 回购对象图 |
| 48 | Broadridge DLR: Settlement and Commercial Use | 10 点出借 1200 万和交抵押品；16 点还现金加利息及释抵押。课件 3680 亿美元日均成交量是处理规模。 | 日间回购时间线 |
| 49 | Broadridge Case: Would a Bank Pay for DLR? | 年节省 18 万、年运维 6 万，净 12 万；初始 30 万/12 万=2.5 年。假设无折现和税，参与程度影响结果。 | 采用成本柱图 |
| 50 | TradeLens: Would Your Company Join? | 承运人关注权限，港口/货代关注集成负担，货主关注覆盖。选一主体给加入条件。 | 文字、公式、代码或表格 |
| 51 | TradeLens: Why the Network Did Not Continue | 课件引 2022-11 停止公告，称行业合作和商业可持续性不足。成员各负集成，收益依其他参与；亦可比较单运营者数据库。 | 文字、公式、代码或表格 |
| 52 | Evaluating an Export-Finance Pilot | 人工时间 40→25 分、对账 12→4%、一年违约 2.0→2.1%。流程改善可读，信用风险/因果须对照。 | 文字、公式、代码或表格 |
| 53 | Worked Example: Verification Cost and Loan Profit | 借 10 万年 8% 利息 8000，资金与预期损失 6000；服务成本 1500→1000，利润 500→1000，违约假设没变。 | 文字、公式、代码或表格 |
| 54 | The Same Technology Meets Two Policy Boundaries | 按课件区分内地商业区块链/数字人民币与虚拟货币服务，以及香港持牌平台、2024 ETF、代币化存款和债券。法律准确条款及历史边界沿用已核深读。 | 文字、公式、代码或表格 |

## 待修方向

- EF5560-M06-01。按页顺序新增唯一入口及 §8 物理页精确链接，保留原主题深读和转录。
- EF5560-M06-02。核图清单、裁框、逐图读法和机制补图，按源位置核原题与答案。
- 具体缺口、题面和视觉验证在候选之后逐条更新；本诊断不表示教学验收。


## 最终正文与来源核验

原题及给定演示对应 p.03、06、07、08、12、18、22、28、29、32、33、46、49、50；三道选择题全部 12 项已按原 PDF 对照。p.29 B 有课堂确认，p.32／33 D／C 保留笔记参考，p.46 第 2 问中途截断。p.41／54 保留既有历史官方全文核验范围，未作当前业务合规结论。
