# M07 逐页源诊断

- `EF5560_Fintech_and_AI_in_Finance\course_files_export\Lec07_Bitcoin_and_Ethereum.pdf`，SHA-256 `fcbcb8fc32059a353fdfd6d918dfa68086ab065554a4ae727f176222768c4874`。
- 当前原笔记 SHA-256 `f039b2dfee8d3d9ad7b96b5078da0e2e8285f55e3125384ff4f4a3d35776136e`。

作者实际打开对应的全部联系表，图义与布局文本互证。下表是已读源页和拟保留要素。最终候选 SHA-256 765eb00299015512ddabe45761b29005b0ae52cbc3bf6cbe51f109d2faeac150，独审已回核全部 54 页。

| 物理页 | 原题名 | 本页教学要素 | 图或页处置 |
|---:|---|---|---|
| 01 | FinTech and AI in Finance | 比特币与以太坊。 | 封面或分隔 |
| 02 | Bitcoin, Wallets, and Mining | 进入发行、钱包和相关商业模式。 | 封面或分隔 |
| 03 | Why Do People Hold or Use Bitcoin? | 投资承受波动、自托管自主授权、链上转账。与银行支付和受监管投资账户按具体任务比较。 | 文字、公式、代码或表格 |
| 04 | Bitcoin Supply: A Predetermined Issuance Rule | 约 2100 万上限、每 21 万块补贴减半，预计 2140 年附近发完最后部分；交易费独立，稀缺不推出需求。 | 文字、公式、代码或表格 |
| 05 | Bitcoin’s Issuance Schedule: 2009 to the Next Halving | 2009 首 50，2012/16/20/24 为 25/12.5/6.25/3.125 BTC，预计 105 万块到 1.5625。天发行量按 10 分目标估，虚框日期非固定。 | 补贴时间线 |
| 06 | Limited Block Space Creates a Fee Market | 提交→竞争容量→矿工收手续费。拥堵时加费或等更久，买的是处理；矿工还有补贴。 | 手续费流程 |
| 07 | The 2017 Fork Created BTC and BCH | 2017-08-01 前共享历史，后分 BTC 保守容量/SegWit 路线和 BCH 大区块路线，各有价格。 | BTC/BCH 分叉 |
| 08 | Ledger: Why Pay for a Hardware Wallet? | 选择交易或兑换→钱包准备并签→网络更新；资产在链上，设备保护密钥，备份责任由用户担。 | 硬件钱包签名流程 |
| 09 | Ledger: Security through Separate Signing | Coinbase.com 托管方控密钥，可有密码恢复；Ledger 用户掌握签名，降低在线暴露，但坏交易已授权仍可能损失。 | 文字、公式、代码或表格 |
| 10 | Ledger: Devices, Services, and Customer Trust | 课件按 2026-10-13 的 Nano/Flex/Stax 与连接买卖质押服务，硬件销售及合作服务和网络手续费分开。 | 文字、公式、代码或表格 |
| 11 | Crypto Markets: A Downturn Followed by a Rebound | 课件 10/20 BTC/ETH 是约价，图柱是加密总市值季度变化 −23.7/−20.4/−12.6/+39.6%，不能直接相加或当币价回报。 | 四季度总市值柱图 |
| 12 | Strategy: Financing a Bitcoin Treasury | 投资者给资本→公司发证券→资金可买 BTC；普通股剩余权、优先股条款、债务偿还各异，持股不能提走公司 BTC。 | 公司融资流程 |
| 13 | Strategy: Asset Value and Cash Needs | 普通股 NAV 先减负债及优先索取权。持币未实现收益不给现金。课件引用 2026-07-06 卖币披露，外部核验边界见旧稿。 | 文字、公式、代码或表格 |
| 14 | Strategy Case: Bitcoin Is Flat, but the Shares Fall | 资产 1 亿且无其他资产负债，权益市值由 1.5 亿到 1 亿，股东收益 −33.3%；初始 50% 溢价消失。 | NAV 溢价柱图 |
| 15 | Worked Example: Issuing Shares Above Asset Value | 初始 1 亿/1000 万股=10 美元。以 15 美元发 100 万股并买币，资产 1.15 亿、1100 万股，NAV/股约 10.45。 | 发股购币三步 |
| 16 | Worked Example: Mining Revenue and Costs | 1% 算力、网络月收入 1000 万美元，期望收入 10 万，运营 12 万，期望亏 2 万。不是固定奖励。 | 文字、公式、代码或表格 |
| 17 | Competition in Bitcoin Mining | 左长期纵轴对数，右近五年线性七日平均，课件标 2026-07-27 874 EH/s。全网涨时矿工需增算力才能维持份额。 | 双算力图 |
| 18 | IREN: From Bitcoin Mining to AI Infrastructure | 电力场址→GPU、冷却与联网→合同计算服务。2025-11 的五年 97 亿美元是协议规模，仍有交付、资本及集中风险。 | IREN 三步 |
| 19 | Ethereum and Smart Contracts | 进入可执行程序、质押与费用。 | 封面或分隔 |
| 20 | Bitcoin and Ethereum Serve Different Purposes | BTC 强调稀缺资产/支付和 PoW，ETH 用于计算费和质押，网络为可编程应用。 | 文字、公式、代码或表格 |
| 21 | A Smart Contract Executes a Program on the Ledger | 交易调用→代码查条件→更新余额或记录。部署不等于持续运行，输入能错。 | 合约执行三步 |
| 22 | Conditional Supplier Payment | 买家预存 1 万、供应商送货、外部确认、实际付款。预付资金在托管，确认与触发须有授权。 | 托管四格 |
| 23 | Staking: Commit Capital to Help Run the Network | 质押 ETH→检查/提议区块→奖励或惩罚。自行运行或服务机构各有费用、操作、退出和价格风险。 | 质押流程 |
| 24 | ETH Supply Reflects Both Issuance and Burning | 新发行加到供应，基础费销毁从供应扣掉；使用高可能多烧，供应净变化需两数，另有小费。 | 发行销毁三块 |
| 25 | Worked Example: Staking Yield and Dollar Return | 10 ETH 每 2000 美元，币数 +4% 到 10.4，价格降至 1600，终值 16640，美元回报 −16.8%。 | 文字、公式、代码或表格 |
| 26 | Worked Example: A Network Fee in Dollars | .001 ETH×2000=2 美元，转 20 美元费率 10%，转 500 为 .4%，固定费用对小额重。 | 网络费占比 |
| 27 | Multiple-Choice Question: A Bitcoin Holding Company’s Premium | 市值 150m 与资产 100m，差额除资产为 50% 选 B；若按市值算是另一问题。 | 文字、公式、代码或表格 |
| 28 | Multiple-Choice Question: A Halving and Miner Revenue | 补贴占 80%，费用占 20%。补贴减半而价格、手续费、块数不变，总收入降 40%，课堂确认 B。 | 文字、公式、代码或表格 |
| 29 | Multiple-Choice Question: Staking Income and Investment Risk | 币变多不保证美元回报，价格跌可盖过币奖励，选 D。 | 文字、公式、代码或表格 |
| 30 | A Smart-Contract Auction | 卖家预存 NFT，Alice 100、Bob 120、Charlie 110 被拒，Alice 可领回。截止后的结算交易同时转 NFT 和 120 USDC，题设管理员不能绕过。 | 文字、公式、代码或表格 |
| 31 | Building a Protocol and Building a Financial Company | Vitalik 提出通用可编程链，Armstrong 参与建 Coinbase 服务；应用开放基础设施与公司承担托管运营职责分开。人物插画。 | 文字、公式、代码或表格 |
| 32 | Delivery Data and the Oracle | 实际未送达→系统误记 Delivered→预言机转给合约→1 万提前付。输入正确是业务控制而非代码判断。 | 预言机错误四格 |
| 33 | Rollups: Share Settlement Costs across Transactions | 多交易→二层批处理→结果和数据交以太坊。分摊成本，提存、数据和可用性依具体方案。 | 二层批处理 |
| 34 | A Token Sale Is Not Necessarily a Share Issue | 股权、服务代币、治理代币分别核所有权、服务及投票/现金流；ICO 是销售融资形式，具体许可另核。 | 文字、公式、代码或表格 |
| 35 | Trading Platforms and Market Access | 进入池、费用与监管案例。 | 封面或分隔 |
| 36 | Uniswap: Trading against a Liquidity Pool | 交易者交 A，池持 A/B，输出 B。AMM 依规则报价，提供者收费用并承担库存风险。 | 池交易流程 |
| 37 | Who Supplies Capital and Who Pays Fees? | 左 LP 交资产入池、从池领份额和费，右交易者交输入与费用、收输出。接口或协议额外费用需看版本。 | 双边资金流 |
| 38 | AMM Pricing: Buying 10 ETH | 100 ETH 与 20 万 USDC，k=2000 万。池剩 90 ETH，USDC 到 222222.22，付 22222.22；均价 2222.22，末价 2469.14。 | 文字、公式、代码或表格 |
| 39 | The Same Trade in a Deeper Pool | 100 与 1000 ETH 初价都 2000，买 10 的均价分别 2222.22 与 2020.20。浅池末价高于外部，套利方向向池卖 ETH。 | 深浅池均价 |
| 40 | Worked Example: Liquidity-Provider Fee Income | 200 万量×0.3%=6000，5% 份额得 300。只在全费分 LP、份额固定的教学设定。 | 文字、公式、代码或表格 |
| 41 | Hyperliquid: A Small Team with a Large Trading Business | 2025-10 创始人说核心 11 人及年收入量级十亿美元，属于访谈；永续合约有杠杆，无到期，另有其他参与者。 | 文字、公式、代码或表格 |
| 42 | Hyperliquid: Where Trading Fees Go | 三箭头到 HLP、援助基金买 HYPE 销毁、市场创建者。图说明课件时点费用流向，不推出股东净收益。 | 交易费三路 |
| 43 | Worked Example: Trading Volume Is Not Profit | 10 亿量×0.03%=30 万毛费用，减返利 6 万得 24 万贡献；技术合规人员等成本再扣，例非真实平台报表。 | 毛费用流程 |
| 44 | Short-Answer Question: Automated Payment and Incorrect Data | 输入错、软件按规则执行。回答独立核交付和实际追回/争议流程。课堂 p.44 明确因时间不足略过，保留完整参考。 | 文字、公式、代码或表格 |
| 45 | HKSAR: Regulated Access to Virtual Assets | 课件示例持牌集中平台和 2024-04 现货 ETF，许可证适用地及价格风险另看法源和产品。 | 文字、公式、代码或表格 |
| 46 | Three Ways to Obtain Ether Exposure | 原三格自托管直接持 ETH；平台为托管账户；现货 ETF 持基金份额并付费用。权利、成本、控制和风险分开。 | 三种敞口 |
| 47 | Worked Example: The Cost of ETF Access | 1 万资产恒定，年费 .5% 加买卖各 10 得 70 美元/.7%；未含价差或折溢价。 | 文字、公式、代码或表格 |
| 48 | Stablecoins Account for Most Identified Illicit Flows | 2025 已识别非法地址收至少 1540 亿美元，图稳定币 84% 其他 16%，分母是已识别非法量。 | 非法量两柱 |
| 49 | A Trading Platform Is Also a Financial Intermediary | 托管保护资产和对账，市场监察操纵利益冲突，识别客户及核可疑交易。 | 文字、公式、代码或表格 |
| 50 | An ML Application: Prioritizing Transaction Review | 交易历史及账户特征→可疑评分→分析员查已标记；以后期数据验证，分数不等于定罪。 | 机器审核流程 |
| 51 | Chinese Mainland and HKSAR: Different Market Access | 按课件 2026-02 内地通知与香港持牌/授权产品并列；香港牌照不自动产生内地经营资格。 | 文字、公式、代码或表格 |
| 52 | Worked Example: A Model Flags 100 Transfers | 20 核为可疑、80 误报。查准率 20/100=20%。查全须另找未标记中确实漏掉的可疑量。 | 人工复核两柱 |
| 53 | Bitcoin Treasury Companies: Selling and Financing Risk | 现金需要→卖币超过需求→币价和资产跌→融资意愿弱→现金缺口仍在→再卖。是条件性压力，缓冲会中断。 | 压力反馈循环 |
| 54 | What Does a Crypto Downturn Reveal? | 矿工、持币公司、质押者直接受币价影响；平台交易量与费率为主，抛售有时使量升。100→50→75 仍亏 25%，50% 跌后回本需涨 100%。 | 文字、公式、代码或表格 |

## 待修方向

- EF5560-M07-01。按页顺序新增唯一入口及 §8 物理页精确链接，保留原主题深读和转录。
- EF5560-M07-02。核图清单、裁框、逐图读法和机制补图，按源位置核原题与答案。
- 具体缺口、题面和视觉验证在候选之后逐条更新；本诊断不表示教学验收。


## 最终正文与来源核验

54 页逐页入口、27 张原图。原有 17 页／20 单元加 p.03 英文比较指令及作答，为 18 页／21 单元；3 道选择题 12 个完整选项。p.28 的 40% 有课堂口述确认，p.27 B 和 p.29 D 保留参考，p.44 三问课上明确因时间略过，正文保留中英。
