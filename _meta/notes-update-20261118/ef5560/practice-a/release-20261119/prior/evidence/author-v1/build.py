from pathlib import Path
import json,re,sys,hashlib
sys.dont_write_bytecode=True
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
OUT=Path(__file__).parent
SOURCE=Path('D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance/course_files_export/canvas-20261118/practice_exam_A.pdf')
inventory=json.loads((OUT/'questions-extracted.json').read_text(encoding='utf-8'))
questions=inventory['questions']
answers=json.loads((OUT/'working-answers.json').read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compact(text):return re.sub(r'\s+',' ',re.sub(r'([A-Za-z])-\n\s*([A-Za-z])',r'\1-\2',text)).strip()
def currency(s):return s.replace('US$',r'US\$').replace('HK$',r'HK\$')
ZH={
'A1':'若干相关市场变量使 OLS 系数在相近样本中不稳定。保留原始输入改用 Ridge，问平方系数惩罚想改善什么，而不是保证所有样本都怎样。',
'A2':'在完全相同观测上，给 OLS 增添变量，大模型包含小模型。比较训练拟合误差与后来预测误差，注意 cannot rise 不等于 must fall strictly。',
'A3':'一人想用相关预测变量概括成分，另一人想让训练收益也参与构造成分。问 PCR 与 PLS 在这一步用什么资料。',
'A4':'月度绩效回归 alpha 为 0.20%，市场 beta 为 1.50；市场超额收益从 0 变 2.00%。求拟合组合超额收益的起点与终点，不是只求增量。',
'A5':'每周买入组合价值的 30%、卖出 30%，每次交易成本为交易金额的 10 bp。毛平均超额收益 0.30%、波动 3.00%，求扣费后的均值和周夏普，不要年化。',
'A6':'初始资本的 60% 做多、40% 做空；在价格变化之前，分别算不计方向的总敞口和保留方向的净敞口。',
'A7':'家族办公室把加密资产交交易平台托管；链上余额很大，但平台财困停提。问什么证据最能判断该客户取回资产的前景，不是问平台有没有某个钱包。',
'A8':'BTC 与 BCH 共享 2017 年分开前的交易史，之后遵守不同规则。问共享历史是否强迫后来的交易和价格相同。',
'A9':'代币化货币市场基金向投资者分配收入，单位在数字平台流转。问收入从哪来，而不是单位怎样换持有人。',
'A10':'买了关联数字艺术品的 NFT，代币历史可查，但媒体链接失效且未说明版权许可。把代币归属、媒体访问、法律使用权分开。',
'A11':'央行发行零售 CBDC，商行通过类似 App 提供普通存款。问谁对持有人承担货币负债，不按界面相似判断。',
'A12':'e-CNY 钱包注册数增长，但要判断开户之后是否真的使用支付。需要活跃与重复付款证据，并统一期间和分母。',
'A13':'银行运营的钱包入口停机，公共数字货币底层账本继续运行。区分无法操作与货币余额/请求权消失，不能互相代替。',
'A14':'两客户都表示愿承担投资损失，但一人明年需买房用钱，另一人二十年无短期现金需求。问风险配置应否只看心理意愿。',
'A15':'制裁筛查出现同名，但生日不同，证件尚未核。问当前最恰当的下一步，不是让你代银行作真实个案决定。',
'A16':'智能投顾每年收固定 AUM 的 0.4%，年度固定成本 60 万美元，变动服务成本为 AUM 的 0.1%。只有这些收入成本，求年度零利润所需 AUM。',
'B1':'题设借用 Class 1 的买 PDD、空 JD 思路，却明确历史窗口开始于 JD 外卖扩张之前。(a) 说明交易方向和至少一个未消除风险；(b) 解释正回测为何不是该业务事件的因果证据。',
'B2':'给神经网络三个训练轮数及两组损失，并对比按通胀分月份、按规模分同月公司。(a) 选候选时长并给准则；(b) 说清分组单位与经济含义。',
'B3':'两群组预测违约 1%/4%，同一完整期限实际 3%/7%，原定价使用原预测损失。(a) 分开判断排序与概率校准；(b) 解释定价/利润，并提出一个题面没给的实际结果检查。',
'B4':'同一应收款找两银行融资，平台登记文件和未偿融资，但只有参与银行可更新各自贷款。(a) 计算 80% 总垫款上限下的剩余额度并说要什么记录；(b) 区分文件没变、真实交货和还款能力。',
'C1':'四个月测试，题面保证预测只用先前资料，MA12 为此前 12 个月收益的平均。(a) 两种预测逐月求平方误差再加总；(b) 计算相对 MA12 的样本外决定系数，并回答能否证明投资盈利。',
'C2':'假想先买后付提供者为 2,000 港元购买垫款，从商户扣 4% 费，客户无息还本金。(a) 算费用、商户实收及扣三类成本后的贡献；(b) 只把预期损失从 30 改 55，重算并解释交易量不变为何仍亏。'
}
SUP={
'A1':r'''💡 **为什么相关输入会让系数不稳（笔记补充）**

若两个输入几乎重复，模型可能用“很大正数加很大负数”得到同一预测。给一个完全重复输入的极简例：一行中两个输入都为 1，目标为 1，不加截距。系数 10 与 −9、系数 0.5 与 0.5，都预测 1，训练平方误差均为 0。

但两种系数的平方和分别是 181 与 0.5。Ridge 在拟合误差外还惩罚系数平方和，所以有理由抑制极端抵销。这里展示取舍机制，不是完整训练演示，也不保证每个变量系数都逐项变小。

设训练误差平方和为 $mathrm{SSE}$，第 $j$ 个斜率是 $eta_j$，非负惩罚强度为 $lambda$。Ridge 比较的是 $mathrm{SSE}+lambdasum_jeta_j^2$；通常不惩罚截距，且输入尺度会影响惩罚比较，因此标准化需只用训练资料确定。''',
'A2':r'''💡 **“不增加”的证明只要一个可行解**

旧模型若是“截距加一个变量乘斜率”，新模型再添一个变量。新变量斜率设为零，旧预测一行不变；新模型寻找所有可行系数中训练 SSE 最小的组合，至少不会比这个可行旧解更差。

但这不约束新月份的误差。若新增变量只是训练噪声，训练更贴合却可能预测更差。这里假定两模型对同一目标、同一观测求真正的 OLS 最小值，不把不同样本、正则化或未收敛算法混入。''',
'A3':r'''💡 **成分不是重新挑几列**

一个成分可以是多个输入的加权组合，例如把两个相关财务指标压成一个综合刻度。PCR 先看输入怎样共同变化，再拿成分拟合收益；PLS 在造综合刻度时就让训练收益参与。后者能使用训练标签，不代表可偷看最终测试收益。

成分数量等设置可用验证资料选择，但构造与评估的时间边界必须保留。题目不要求手算成分权重，不能凭题面捏造某个最优权重。''',
'A4':r'''**用一个公式核单位与时点**

写 $widehat r_p^e=alpha+eta r_m^e$：上标 $e$ 表示超额收益，即收益减同期无风险收益；帽号表示回归拟合，不是保证的未来实现收益。

| 量 | 本题含义 | 单位/取值 | 何时可用 |
|---|---|---|---|
| $alpha$ | 市场超额为零时拟合值 | 月收益 0.20% | 已给拟合参数 |
| $eta$ | 市场每变 1 个百分点的响应 | 无量纲 1.50 | 已给拟合参数 |
| $r_m^e$ | 本题市场超额收益 | 月收益 0→2.00% | 两个题设情景 |
| $widehat r_p^e$ | 组合拟合超额收益 | 月收益，待算 | 给定情景后可算 |

市场为零时仍有 alpha 0.20%；市场变成 2.00% 时，市场项贡献 3.00 个百分点，加原 0.20% 得 3.20%。拟合值的变化是 3.00 个百分点，不是 3.20 个百分点。''',
'A5':r'''**从 100 元组合重走成本（笔记补充）**

10 bp（基点，basis points）是 0.10%，不是 10%。若组合价值 100 元，买 30 元收费 0.03 元，卖 30 元也收费 0.03 元；总费 0.06 元，即组合价值的 0.06%。成本从毛超额收益中扣除，0.30% 变 0.24%。

周夏普 $S_{m weekly}=mu_{m weekly}^e/sigma_{m weekly}$，分子是周平均超额收益，分母是同一频率的波动率（收益围绕均值的离散程度）。同用百分数算 $0.24/3.00=0.08$，或同用小数算 $0.0024/0.0300=0.08$，不能一边用百分数一边用小数。

每周都减同一个收益比例时，每周收益和它的新均值一起平移，离均差不变，所以本题波动不变。成本变化才可能改变波动，不能泛化“任何成本都不改变风险”。''',
'A6':r'''**一行先固定一个分母**

以初始资本 100 元为基准，60 元多头的有向金额为 +60，40 元空头为 −40。总敞口把绝对金额相加，得到 100 元/100 元；净敞口按方向相加，得到 20 元/100 元。

| 指标 | 计算对象 | 本题结果 |
|---|---|---:|
| 总敞口 | 两边绝对金额/资本 | 100% |
| 净敞口 | 多头金额减空头金额，再除资本 | 20% |

剩余资金或做空所得如何放置不在题面中，不能由净 20% 推出具体现金余额，更不能直接等同市场 beta。''',
'A7':r'''**本题的证据边界**

链上地址显示 100 单位资产，不告诉你平台是不是欠所有客户 150 单位，也不告诉你哪 10 单位依法属于这一客户。托管是替客户保存/控制资产；隔离是把客户资产与平台自身资产按适用安排分开。合同、资产归属与竞争请求共同影响回收。

这个 100/150/10 仅是笔记补充。题目未给法域、破产文件和完整资产负债，不能算具体回收比例或承诺优先顺位。''',
'A8':r'''**读“同一历史”与“分开以后”**

可把记录按时间分两列：分叉前的记录是共同前史；分叉后的新交易按各自网络规则验证。它们没有因历史相同而变成一份实时同步的账户。

本题不要求处理重放攻击等协议细节；“并非自动更新另一链”不表示每一种分叉机制在所有场景都绝无交互风险。只回答共享前史本身不强制交易、价格和收入权相同。''',
'A9':r'''**让钱和记录分开走**

底层存款/证券→产生投资收入→扣基金费用→按单位权益归投资者；代币登记→记录单位由谁持有。第二条改变收入归属的记录，不是第一条收入的经济来源。

即使平台转账非常频繁，底层资产不付息也不会因“记账次数多”自动生出同样收益；题目未给实际收益率，不能计算数额。''',
'A10':r'''**三层分别验什么**

| 层次 | 应查证据 | 修好媒体链接能否一起解决 |
|---|---|---|
| 代币持有 | 代币/合约及交易记录 | 不自动改变历史归属 |
| 媒体访问 | 存储位置、链接和持续可取用性 | 可修此层访问问题 |
| 法律使用权 | 版权许可或其他明确权利安排 | 不能因此自动补出许可 |

本题不是对具体 NFT 买卖作法律鉴定。未知许可不能写成“绝对没有任何权利”，只能说链上历史本身不足以证明所需使用权。''',
'A11':r'''**“谁欠钱”比“哪个 App”更重要**

中央银行数字货币（central bank digital currency, CBDC）在本题明确由央行发行；普通存款是银行对存款人的债务。商业银行帮用户展示或转移一种央行负债，不会单靠界面把它变成自己的存款债务，反之亦然。

本题没有要求估计风险大小、存款保障或具体 e-CNY 最新机制，勿擅自添加当前政策事实。''',
'A12':r'''**分母决定你在衡量什么（笔记补充）**

固定同一月份，可先定义活跃钱包为当月至少付款一次的钱包。若某注册批次有 1,000 个钱包，100 个活跃，活跃比例为 10%；活跃者中 40 个再次付款，重复付款者比例为 40%。这两个比例的分母不同，不能直接当同一采用指标。

这些数不是 e-CNY 真实数据。题目要的是比注册更直接的使用证据，不足以从单个月活动宣称长期留存或新增社会福利。''',
'A13':r'''**停机的两个问题要分开回答**

运营风险（operational risk）关注入口、系统和恢复过程是否正常；信用风险关注债务是否能获履行。入口暂时停机可造成实际不便和交易中断，但尚不能证明全部余额已经损失。

应核备用访问、身份/密钥恢复、银行与底层系统各自职责及对账。题目没说明备用通道存在，不能想当然说人人都可继续支付。''',
'A14':r'''**这不是对真实用户的投资建议**

两位客户的心理偏好相同，但明年必须付房款的人若遇短期跌价，可能无法按时履行支出。二十年无近期现金需求者的时间约束不同。配置判断要同时考虑意愿、承受能力、目标与流动性，不是只用一道“敢不敢亏”的问卷。

题目只支持 A 这个原则，不提供每人应买多少股票/债券的唯一比例。更频繁调仓或更低费率不直接消除期限错配。''',
'A15':r'''**从候选匹配到身份确认**

同名是一个支持线索，生日冲突是一个反向线索，证件未核是资料缺口。三者应保留而非强行改成一致。下一步核可靠额外标识、来源质量及处理规则，必要时升级人工；不能拿名单人物证件号填申请人空格。

本题没有给具体国家制裁制度和银行流程，所以不写法定冻结期限或保证批准/拒绝。D 是题设下的证据处理步骤，不是实际交易授权。''',
'A16':r'''**先算每一元 AUM 留下多少**

资产管理规模（assets under management, AUM）是管理的资产金额，不等于公司收入。设其全年不变的美元金额为 $A$；年收费收入是 $0.004A$，年度变动成本是 $0.001A$，剩下 $0.003A$ 才可用于覆盖固定成本。

| 符号/量 | 单位 | 何时已知 | 本题值 |
|---|---|---|---|
| $A$ | 美元资产存量 | 待求全年规模 | 待算 |
| 净贡献率 | 每年每元资产贡献 | 题设费率减成本率 | 0.003/年 |
| 固定成本 | 美元/年 | 已给 | 600,000 |

令年度收入减全部题给成本为零：

$$0.004A-0.001A-600{,}000=0$$

因此 $A=600{,}000/0.003=200{,}000{,}000$ 美元。回代：年收费 800,000，变动成本 200,000，扣固定 600,000 后为零。题面无获客成本等其他项目，不能自行加进标准数值；真实业务另当别论。'''
}
LONGSUP={
'B1':r'''**把多空反例按共同分母列出来（笔记补充）**

一行代表一条腿，所有损益相对同一 100 元资本记账，未扣交易/借券成本。

| 腿 | 初始绝对金额 | 股票收益 | 对资本的损益 |
|---|---:|---:|---:|
| 买 PDD | 50 元 | −20% | −10 元 |
| 空 JD | 50 元 | −5% | +2.5 元 |
| 合计 | 毛金额 100 元 | 不直接相加股票收益 | −7.5 元 |

空头在 JD 跌时赚钱，因为以后可较低价格买回所借股票；但它赚 2.5 元，不够抵 PDD 的 10 元损失。相对收益差是 −15 个百分点，乘每边 0.5 权重才是组合收益 −7.5%。

事件因果还要有时间顺序：历史窗口开始→JD 外卖扩张→后续观察。扩张前的收益不可能由“尚未发生的实际竞争”直接造成；若谈预期效应，必须另有当时已知信息证据，题面没给就不补造。''',
'B2':r'''**先看原始候选值，再读补充图**

每行固定一个训练时长。损失的具体函数和单位未给，所以只按同一题设损失比较大小，不叫它 MSE 或百分比。

| Epochs | Training loss | Validation loss | 用于选择的判断 |
|---:|---:|---:|---|
| 10 | 0.0030 | 0.0032 | 验证损失较高 |
| 30 | 0.0020 | 0.0024 | 三候选中验证最小 |
| 60 | 0.0015 | 0.0028 | 训练更低、验证反升 |

![B2(a) 相同题设数据的补充损失图](b2-loss.svg)

图横轴是训练轮数，纵轴是题目给的损失；蓝圆点为训练、橙方点为验证。沿橙色点看，30 轮最低；蓝线下降不改变这个选择准则。点间连线仅帮助读三候选，不证明每个中间轮次的真实轨迹，也不证明 30 是所有可能轮数的全局最优。

训练、验证和最终测试三者分工是：训练更新参数→验证挑轮数→固定方案后在最终测试评估。若看测试选轮数，测试已参与选择，不再是这次最终未见评估。

对 (b)，下表每行固定一种“资料行”的含义：

| 资料的一行 | 分组规则例（笔记补充） | 得到的组 |
|---|---|---|
| 一个历史月份 | 决策前已知通胀高/低 | 不同月份的宏观状态 |
| 同一月份的一家公司 | 该公司规模大/小 | 同时点的公司截面 |

两种树可以都给叶子内预测，但叶子里放的对象不同。“滞后”要按实际公布日核可得性，不是只把列名写成 lag 就自动没有前视。''',
'B3':r'''**违约频率不是损失率**

违约概率（probability of default, PD）是所定期限内违约的可能性；违约损失率（loss given default, LGD）是已经违约时有多少金额最终收不回；违约时敞口（exposure at default, EAD）是届时面临损失的金额。预期损失（expected loss, EL）的单期简化关系为 $EL=PD\times LGD\times EAD$。

| 量 | 单位 | 何时/条件 | 本题是否给数 |
|---|---|---|---|
| PD | 概率/比例 | 定价时的预测期限 | 给两组预测及事后频率 |
| LGD | 条件损失比例 | 违约后扣回收的结果 | 未给 |
| EAD | 货币金额 | 违约时的敞口 | 未给 |
| EL | 同币种金额 | 所定期限的预期损失 | 不能从频率单独算出 |

例如固定 EAD 为 1,000 元、LGD 为 50%，PD 从 1% 改 3%，EL 从 5 元变 15 元。这只是笔记补充的同条件例，不能把真实群组的 LGD、敞口假定成这些数。

两组汇总只支持本题的群组排序一致和两个点的低估。没有组人数/抽样模型，不能计算置信区间，也不能判定所有个体排序或全概率区间校准都好。完整期限减少未到期截尾问题，不自动给出净回收、折现和处置成本。''',
'B4':r'''**剩余额度与批准分成两步**

先固定同一笔 200 万元人民币应收款，并假定未偿融资记录完整且最新。每行是一个金额步骤：

| 步骤 | 金额（人民币元） | 含义 |
|---|---:|---|
| 200 万×80% | 1,600,000 | 所有融资合计上限 |
| 减 A 未偿贷款 | −1,300,000 | 已占用额度 |
| 计算余量 | 300,000 | 条件下最多剩余额度 |

这不是 B 自动可贷 30 万：若记录过时、存在不参与平台的融资或贷款政策更严，实际可用额度会变。若最新总融资已达 170 万，不能给负贷款额，应识别超限并停止新增，核清记录/风险。

平台记录需要对得上同一应收款的唯一身份、最新余额、变动时间和更新责任。only participating banks can update 只是写权限规则，不证明世界上不存在其他融资。

| 要验证的一层 | 记录能说明什么 | 仍需的现实证据 |
|---|---|---|
| 文件完整性 | 存档后是否被改 | 原文件真实性/授权 |
| 交易履行 | 文件写了交付 | 物流、收货验收、买方确认 |
| 还款能力 | 登记了应付款 | 买方现金流、到期、争议与信用 |

即使文件哈希一致，也可能把最初的假发票原样保存。不可篡改不等于初始输入真实，更不保证买方未来有钱。''',
'C1':r'''**符号、单位与一个月的演算入口**

令 $r_t$ 为测试月 $t$ 的实现收益，$\widehat r_t$ 为模型对该月的预测，$b_t$ 为 MA12 预测。三者均是月收益小数：0.03 表示 3%；$t$ 在这里是月份编号，不是检验统计量。预测在该月收益实现之前可用，实现收益在该月结束后才知道。

模型误差 $e_t=r_t-\widehat r_t$；平方使正负偏差都计为错误，再加总 $mathrm{SSE}=\sum_{t=1}^{4}e_t^2$。第 4 月模型误差是 $-0.02-(-0.01)=-0.01$，平方 0.0001；MA12 误差是 $-0.02-0.01=-0.03$，平方 0.0009。

样本外决定系数（out-of-sample R-squared）问“相对题设基准，平方误差减少了多少比例”：

$$R^2_{\mathrm{OOS}}=1-\frac{\mathrm{SSE}_{\rm model}}{\mathrm{SSE}_{\rm MA12}}.$$

分母非零才有定义。本题分母为正；若基准误差恰为零，不能继续除以零并强报一个分数。正 77.78% 不是投资回报 77.78%，也不是预测对了 77.78% 的月份。

题面已经给 MA12 的四个预测值，因此无需额外 12 个月原始收益才能完成本题。没有回测持仓规则、费用和风险，才是无法证明盈利的真正缺口，不是计算 SSE 的缺口。''',
'C2':r'''**按一笔交易追收入，而不是把本金算两次**

先买后付（buy now, pay later, BNPL）在题设中让客户无息偿还购买本金，提供者靠商户费获得这项收入。商户原应收 2,000，扣费 80 后实得 1,920；提供者未来收回客户本金，不等于又赚了整笔 2,000。

| 本笔交易的量 | 金额（港元） | 是否收入/成本 |
|---|---:|---|
| 购买本金 | 2,000 | 交易规模，不全是收入 |
| 扣留商户费 | 80 | 本题收费收入 |
| 商户净拨款 | 1,920 | 商户实收，不是额外收入 |
| 资金/预期损失/服务 | 18/30/12 | 三项题设成本 |
| 原预期贡献 | 20 | 收费减三项成本 |

这里的贡献（contribution）指只扣题设成本后的余额，未扣总部固定费用和税，不等于公司净利润。客户免息不代表提供者没有资金成本；预期损失是估计的平均损失，不是说每笔交易必定恰亏 30。

改为损失 55，费用和其他成本固定，所以贡献只会比原来少 25，20 变 −5。不能为保住原利润偷改收费率，也不能把新增 25 又重复扣两次。'''
}
PRE='''---
type: practice-guide
course: EF5560
assignment: Practice-Exam-A-learning-analysis
source: course_files_export/canvas-20261118/practice_exam_A.pdf
status: draft
official_solution: not_obtained
independent_review: pending
readability_rules: v2
teaching_standard: novice-v1
updated: 2026-11-19
---

# EF5560 Practice Examination A · 学习解析候选

> 供自学、复做与独立审查，不是学生提交稿，不是官方答案。本篇没有代填姓名、学号、答题纸或本人学习状态。计算与解释依据题面固定条件；改条件例均为笔记补充，不是真实投资或贷款建议。

## 0. 三分钟速览

整卷考的是把“模型分数、金融收益、数字记录、法律/业务权利”分开，不被看起来相似的表面证据误导。

- Section A：16 题，每题 2.5 分，全部四个选项都保留并分析。
- Section B：4 题，每题两问，共 40 分。要连接题面事实与理由，不能只报术语。
- Section C：2 题，每题两问，共 20 分。收益小数、分母和本金/收入不能混淆。
- 合计 22 大题、28 作答单元、100 分；物理页 1–14 全部实际查看。

## 1. 开始之前 · 卷面要求与学习路线

### 1.1 原封面怎么读（p.1）

这是 2026/27 Semester A 的 Practice Examination A，封面设定两小时、答所有题、A 部分写一个字母、C 部分写步骤。允许一张双面 A4 手写参考纸，并要求在参考纸写座号/学号、与全卷一起交回。这是练习封面的制度情境，不是本轮重新确认最终期末的公告；正式考试应以最新正式通知为准。

<details><summary>封面原文 · Directions and permitted aids</summary>

> CITY UNIVERSITY OF HONG KONG
> PRACTICE EXAMINATION A
> Course Code & Title: EF5560 FinTech and AI in Finance
> Semester / Term: Semester A 2026/27
> Duration: Two hours
> This paper has FOURTEEN pages (including this cover page).
> 1. Answer ALL 22 questions in three sections. Total: 100 marks.
> 2. Write ALL answers in this paper. For Section A, write A, B, C or D in the answer space. Show your working in Section C. Submit the entire paper.
> 3. Write your seat number and Student ID on your handwritten reference sheet. Submit it with this paper at the end of the examination.
> This is a closed-book examination with the aids listed below.
> Students are allowed to use the following materials/aids: One double-sided A4 sheet of handwritten notes.
> Materials/aids other than those stated above are not permitted. Students will be subject to disciplinary action if any unauthorized materials or aids are found on them.

</details>

### 1.2 怎样使用这份学习稿

预习从每题的中文任务入口读起，再对照原英文题，按中文推理和英文参考答案复述。模拟练习先遮住答案，只读原题，再回来看逐选项理由和误区。逐页跟读用 §8 的原页入口，p.13–14 是纯草稿纸，不是漏题。

“参考答案”只表明作者按题面推理，未取得官方解答不等于官方未发布。当前没有登录 Canvas 或核新公告；本稿也不宣称期末一定复用同题。中英答案用于理解及比较，不应复制冒充个人独立作业或在考试中使用未许可工具。

### 1.3 当前需要的前置区别

训练资料用于拟合参数；验证资料用于选设置；最终测试用于评价已固定方案。金额是元，收益率是损益除声明的资本；两个收益率之差用“百分点”。链上记录、实际资产和法律请求权是三个对象，不因为同一 App 或同一代币就合成一层。

本稿在第一次需要处解释术语和公式，不要求先会统计、机器学习或金融。没有给出的真实收益、回收、政策和法定优先顺位，不靠常识补为事实。

## 2. 原题、中文解析与英文参考答案

### 2.0 三部分的原始指令

> Section A Multiple-Choice Questions (40 marks)
> Write ONE letter (A, B, C or D) after each question. Each question carries 2.5 marks.
>
> Section B Short-Answer Questions (40 marks)
> Answer in the spaces provided. Each question carries 10 marks.
>
> Section C Calculation Questions (20 marks)
> Show your working in the spaces provided. Each question carries 10 marks.

下面 A1–A16、B1–B4、C1–C2 保留原部分和原题号；编号 2.1–2.22 仅是本解析导航。
'''
sections=[];manifest=[];headings={}
for idx,(qid,q) in enumerate(questions.items(),1):
    a=answers[qid]; sec=f'2.{idx}'
    heading=f'{sec} {qid} · {a["title"]}（原卷 p.{q["page"]}）'
    headings[qid]=heading
    lines=['### '+heading,'',ZH[qid],'',f'来源：Practice Exam A p.{q["page"]}，原 Section {q["section"]} 第 {q["number"]} 题，{q["marks"]:g} 分。','', '<details><summary>完整英文原题及选项/小问</summary>','']
    if q['section']=='A':
        original=f'{q["number"]}. {q["stem"]}\n'+'\n'.join(f'{k}. {v}' for k,v in q['options'].items())
        lines+=['> '+x for x in original.splitlines()]
        lines+=['','</details>','',f'**⚪ 参考选择：{a["answer"]}。**','',a['cn'],'','**逐选项判断**','']
        lines+=['- '+x for x in a['options']]
        lines+=['','**English reference answer (not official)**','',a['en'],'',SUP.get(qid,''),'','**改条件练习与边界**','',a['transfer'],'']
        units=[{'id':qid,'chinese':a['cn'].split('。')[0]+'。','english':a['en']}]
    else:
        stem=q['stem']
        if qid=='C1':
            stem=stem[:stem.index(' Month ')]
            table='''| Month | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| Realized return | 0.03 | -0.01 | 0.02 | -0.02 |
| Model forecast | 0.02 | 0.00 | 0.01 | -0.01 |
| MA12 forecast | 0.01 | 0.01 | 0.01 | 0.01 |'''
            original=f'{q["number"]}. {stem}\n\n{table}\n\n(a) {q["parts"]["a"]}\n\n(b) {q["parts"]["b"]}'
            lines+=['> '+f'{q["number"]}. {stem}','>','\n'.join('> '+row for row in table.splitlines()),'>','> (a) '+q['parts']['a'],'>','> (b) '+q['parts']['b']]
        else:
            original=f'{q["number"]}. {stem}\n\n(a) {q["parts"]["a"]}\n\n(b) {q["parts"]["b"]}'
            lines+=['> '+f'{q["number"]}. {stem}','','> (a) '+q['parts']['a'],'','> (b) '+q['parts']['b']]
        lines+=['','</details>','',a['intro'],'']
        units=[]
        for p in a['parts']:
            lines+=[f'#### {sec}.{1 if p["id"]=="a" else 2} ({p["id"]}) 中文参考解析','',p['cn'],'','**English reference answer (not official)**','',p['en'],'']
            units.append({'id':qid+p['id'],'chinese':p['cn'].split('。')[0]+'。','english':p['en']})
        lines+=[LONGSUP.get(qid,''),'','**本题学习总结**','',a['summary'],'']
    original=currency(original)
    # Original questions preserve words, punctuation, options and all numeric inputs;
    # currency escapes and C1 Markdown table are display-only transformations.
    manifest.append({'id':qid,'source_id':'ExamA','page':q['page'],'section':sec,'original':original,'options':{k:currency(v) for k,v in q.get('options',{}).items()},'answers':[{k:currency(v) if isinstance(v,str) else v for k,v in u.items()} for u in units]})
    sections.append('\n'.join(lines))
POST='''## 3. 一图看懂 · 全卷的六条判断链

每行固定一种任务，按左到右走，不把得到的中间证据当最终保证。

| 任务 | 先分对象 | 再用证据 | 能得出的有限结论 |
|---|---|---|---|
| 模型选择 | 训练/验证/测试 | 验证选设置，固定后测试 | 不是训练越低越好 |
| 投资绩效 | 收益/误差/敞口 | 同单位、分母、成本和时点 | 预测改善不直接等于净盈利 |
| 数字资产 | 记录/资产/请求权 | 合同、托管、媒体、许可 | 链上可见不等于完整回收 |
| 货币支付 | 发行债务/访问服务 | 看发行人和恢复安排 | 界面相似不等于同一负债 |
| 信贷模型 | 排序/概率/损失 | 违约频率加回收/敞口 | 排对高低仍可能收费不足 |
| 平台业务 | 交易规模/收入/贡献 | 收费减题设成本 | 量不变不保证利润不变 |

## 4. 参考答案速查

速查只供复做后核对，理由必须回到 §2。以下不是官方评分键。

| 题 | 参考结果 | 原题入口 |
|---|---|---|
<!-- KEY -->

## 5. 双语术语与符号速记

英文定义是本稿的参考表述，不是课件逐字定义；首次必要解释已在对应题旁。

| 中文 | English | English revision definition | 回读 |
|---|---|---|---|
| 误差平方和 | Sum of squared errors (SSE) | Add the squared differences between the same realized targets and their predictions. | A2、C1 |
| 岭回归 | Ridge regression | Fit with a squared-coefficient penalty, trading fit against coefficient magnitude. | A1 |
| 主成分回归 | Principal component regression (PCR) | Build components from predictors before fitting the target relation. | A3 |
| 偏最小二乘 | Partial least squares (PLS) | Let the training target help construct predictor components. | A3 |
| 超额收益 | Excess return | A return minus the comparable risk-free return for the same period. | A4、A5 |
| 基点 | Basis point (bp) | One hundredth of a percentage point. | A5 |
| 夏普比率 | Sharpe ratio | Mean excess return divided by volatility at a consistent frequency. | A5 |
| 总/净敞口 | Gross/net exposure | Sum absolute positions, or add signed positions, relative to a declared capital base. | A6 |
| 资产管理规模 | Assets under management (AUM) | The amount of managed assets, not fee revenue. | A16 |
| 校准 | Calibration | Agreement between predicted probability levels and comparable realized frequencies. | B3 |
| 违约损失率 | Loss given default (LGD) | The loss fraction conditional on default, after relevant recovery. | B3 |
| 样本外决定系数 | Out-of-sample R-squared | One minus model SSE divided by a declared benchmark SSE over the same test targets. | C1 |
| 先买后付 | Buy now, pay later (BNPL) | Financing a purchase with later customer repayment; revenue and costs depend on the stated arrangement. | C2 |

## 6. 答题框架与常见误判

本卷本身就是练习，不把这里的归纳叫“教授明示会考”。

选择题先找限定词：same observations、before market movements、constant、complete horizon、all other amounts unchanged。它们分别固定样本、时点、成本/资产条件、观察期限和变动输入；删掉条件，原答案可能不再成立。

短答先用一句直接回答，再把具体事实连到机制，最后写不能推出什么。计算题先写输入单位、关系和符号，再逐步代入；最后用一句中文或英文解释数值回答的是什么，不只留下孤立结果。

不要把 B3 的违约频率当 LGD，把 C1 的 77.78% 当收益率，把 C2 的 2,000 当收费收入，或把 B4 的 30 万当已经批准。

## 7. 改条件自测

这些是笔记补充，不来自原卷；先自行作答再展开，未替本人标通过。

### 7.1 成本与费用

A5 若仍买卖各 30%，但每笔费率变成 20 bp，其余输入不变，净周均值和夏普是多少？A16 若年收费降到 0.3%、变动成本仍 0.1%，固定成本不变，盈亏平衡 AUM 呢？

<details><summary>参考答案与理由</summary>

成本变为组合价值的 0.12%，净均值 0.18%，夏普为 0.18/3.00=0.06，仍按恒定成本情境。A16 净贡献率降到每年 0.2%，固定 600,000 美元需由 300,000,000 美元 AUM 覆盖，即 3 亿美元。两题都先把输入改在原公式的一处，不能照抄旧答案。

</details>

### 7.2 排序与概率

B3 若两个组预测仍是 1%/4%，实际改成 7%/3%，还可说群组排序正确吗？

<details><summary>参考答案与理由</summary>

不可以。预测认为第二组更危险，实际第一组违约频率更高，两组的方向已反。概率水平也分别不等于实际，但必须把排序和校准两个判断分开写。仍没有每组人数，不能编统计显著性。

</details>

### 7.3 基准与贡献

C1 若模型 SSE 恰等于 MA12，会得到什么指标？C2 给定原收费/资金/服务成本，预期损失最大到多少时贡献恰为零？

<details><summary>参考答案与理由</summary>

当相同正基准下两 SSE 相等，OOS R² 为零，表示没有平方误差改善。C2 收入 80，扣资金 18、服务 12 后剩 50 港元可吸收预期损失；50 时本笔贡献为零，但仍未算总部费用和税，不是整个公司零利润。

</details>

## 8. 原卷逐页入口

原件包含封面和两页空白草稿。下面一行对应一个物理页，印刷号 p.2–14 与物理页相同；封面没有印刷页号。原件所有页均已实际查看，候选最终排版则尚未作 UI 阅读核验。

| 物理页 | 原页内容 | 本稿精确入口 | 图/空白处置 |
|---|---|---|---|
<!-- PAGE_MAP -->

## 9. 来源、计算与待核事项

### 9.1 已使用的来源

原题唯一权威源为本地 `practice_exam_A.pdf`（14 页，SHA 见伴随 page-evidence）。旧批 `source.txt/pages.json` 只辅助提取；作者已逐张实际看完全部 14 页并对题面。C1 数字表保留原值。旧 `exam-a-content.json` 与 `exam-a-long.json` 是历史作者草稿，复用前已与原题比对，不是官方答案。

B1 的 Class 1 背景另回读本课 M01 的 p.8/p.15/p.16 讲解：PDD 被视为外卖竞争之外，JD 同时有投入成本/利润风险与潜在客流机会。这里仍只陈述投资假设，不宣称外卖扩张已经使某股票下跌。历史额外数据不影响本题可完成，但缺少它时不能估计因果效应。

### 9.2 真正做过的计算

伴随 `compute.py` 用 Decimal/Fraction 复算 A4/5/6/16、B1 多空变式、B2 选轮数、B3 概率差/损失变式、B4 额度、C1/2 全部数字；结果为 `computation-results.json`。这是固定题面计算，不是重新训练、交易或访问客户资料。

B2 补图由同一代码按原始三个候选数据生成。作者实际查看 PNG 静态图，轴、数值、图例与最低点可辨；未将其冒称候选 Markdown/Obsidian 的最终嵌入显示。

### 9.3 不应被伪造成“缺资料所以不能解”的部分

题面已经给出了 C1 的 MA12 预测、A16 的固定费率成本、C2 的预期损失和 B4 的条件数值，足以完成相应计算。无需下载新行情、取得 12 个原始月份或另找真实 BNPL 财报才能算这些数。

真正未知的是官方评分细则、当前 Canvas 是否有解答、最终考试最新通知、B1 的因果识别证据、B3 的真实回收/敞口、B4 现实记录完整性等。它们限制可声称的结论，不抹掉题面能回答的部分。

### 9.4 尚未完成的验收

本稿是冻结前作者候选；尚未独立两阶段审查、尚未完成最终 Markdown/图文实际阅读与正式发布门槛。机器和作者复算不能证明初学者已经能独立完成每题。未写回正式目录、元数据、Notion 或 Git，未改本人提交/通读/自测字段。

以上答案全部为学习参考，不能将此稿存在当作官方解答、已被接受或整门课完成。
'''
key=[]
for qid in questions:
    a=answers[qid]
    if qid[0]=='A': short=a['answer']
    else: short={'B1':'相对看好 PDD；风险未尽除；全窗正收益不证明因果','B2':'(a) 30 轮；(b) 月份宏观组与同月公司截面组','B3':'群组排序一致；两组低估 2/3 个百分点；另查回收/LGD','B4':'(a) 条件余量人民币 300,000；(b) 文件完整≠交付/可还款','C1':'SSE 0.0004/0.0018；OOS R²=7/9≈77.78%；非盈利证明','C2':'费用80，净拨款1920，原贡献20，变动后−5（港元）'}[qid]
    if qid[0]=='A':
        key.append(f'| {qid} | {short} | [[#{headings[qid]}\\|{qid}解析]] |')
    else:
        small={'B1':['相对业务假设支撑方向，仍有未对冲风险','全历史窗口正收益不足以证明因果'],'B2':['三个候选中选30轮','月份宏观状态组与同月公司截面组'],'B3':['群组排序一致，概率低估2/3个百分点','原定价可能不足，另查回收或LGD'],'B4':['条件剩余额度为人民币300,000','文件完整不保证交付或偿还'],'C1':['模型/MA12的SSE为0.0004/0.0018','OOS R²=7/9≈77.78%，不证明盈利'],'C2':['费80、拨款1920、贡献20港元','预期贡献变为−5港元']}[qid]
        for label,brief in zip('ab',small):key.append(f'| {qid}({label}) | {brief} | [[#{headings[qid]}\\|{qid}解析]] |')
POST=POST.replace('<!-- KEY -->','\n'.join(key))
page_map=[]
for p in range(1,15):
    ids=[k for k,q in questions.items() if q['page']==p]
    if p==1:
        label='封面/考试情境';link='[[#1.1 原封面怎么读（p.1）\\|封面解析]]';disp='文字要求完整保留，未代填个人资料'
    elif p>=13:
        label='SCRAP PAPER';link='[[#1.2 怎样使用这份学习稿\\|空白页说明]]';disp='纯草稿，无漏题或教学图'
    else:
        label='、'.join(ids);link=' / '.join(f'[[#{headings[k]}\\|{k}]]' for k in ids);disp='C1原数字表完整转写' if p==11 else '文字题，无教学原图；不复制答题留白'
    page_map.append(f'| {p} | {label} | {link} | {disp} |')
POST=POST.replace('<!-- PAGE_MAP -->','\n'.join(page_map))
candidate=currency(PRE+'\n'+'\n'.join(sections)+'\n'+POST)
for number in ('.004','.001','.003'):
    candidate=candidate.replace('0'+number+'A','0'+number+r'\times A')
atomic_write(str(OUT/'candidate.md'),candidate)
atomic_write(str(OUT/'source-checks.json'),json.dumps({'schema':'note-source-checks-v1','sources':{'ExamA':{'path':str(SOURCE),'sha256':sha(SOURCE)}},'questions':manifest,'note':'Source manually visual-checked. Formatting transforms: normalized wrapped whitespace, currency dollar escaped, C1 data formatted as a Markdown table. Original extracted raw retained in questions-extracted.json. This manifest does not certify answer correctness.'},ensure_ascii=False,indent=2)+'\n')
atomic_write(str(OUT/'candidate-record.json'),json.dumps({'candidate_sha256':sha(OUT/'candidate.md'),'bytes':len(candidate.encode('utf-8')),'questions':22,'answer_units':28,'MC_options':64,'source_pages_viewed':14,'independent_review':'pending','final_UI':'not performed (task forbids UI)'},ensure_ascii=False,indent=2)+'\n')
print('Candidate',len(candidate.encode('utf-8')),sha(OUT/'candidate.md'))
