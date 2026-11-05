# M05 逐页源诊断

- `EF5560_Fintech_and_AI_in_Finance\course_files_export\Lec05_Interpretable_Machine_Learning_and_Portfolio_Decisions.pdf`，SHA-256 `02eb0d14e1ada91fe73d3c1f933aa7d1e4c96b17297e0c855f33b8ef675f731f`。
- 当前原笔记 SHA-256 `365c6086f9f03d173b1ecbcfbf9c9a4020fb36c309c9bd10c81e3478e25d44a3`。

作者实际打开对应的全部联系表，图义与布局文本互证。下表是已读源页和拟保留要素。最终候选 SHA-256 3cf47f2f9ac7b50bec67a92a372c955c5a5ee8b7090877baccc209efb13312a9，独审已回核全部 54 页。

| 物理页 | 原题名 | 本页教学要素 | 图或页处置 |
|---:|---|---|---|
| 01 | FinTech and AI in Finance | 可解释机器学习与组合决策。 | 封面或分隔 |
| 02 | Interpreting Characteristics and Forecasts | 进入线性贡献与非线性解释。 | 封面或分隔 |
| 03 | OLS Coefficients: Size and Statistical Significance | 动量系数 +0.30、SE 0.10、p=.003；波动 −0.20、SE .25、p=.42。单位为输入增加一训练标准差对应的收益百分点。 | 文字、公式、代码或表格 |
| 04 | Linear Coefficients: Calculating Forecast Contributions | 截距 +0.10%、动量贡献 +0.30%、波动贡献 −0.10%，合计 +0.30%。波动不显著仍进入 OLS。 | 文字、公式、代码或表格 |
| 05 | LASSO Coefficients: Selected or Set to Zero | 惩罚选定后动量变 +0.24，波动为零。动量 z=1 得 +0.34%。预测选择与统计显著两回事。 | 文字、公式、代码或表格 |
| 06 | A Weekly Momentum Ranking | 周末 2026-06-26，79 个有效排名中的最高/最低五。横轴中心化排名、纵轴股票，右红左蓝；联想 +0.500、中升（0881）−0.487。排名是输入。 | 79 股动量极端五股原图 |
| 07 | Drop-to-Zero Importance: Which Inputs Does the Model Use? | 四格原图先记原误差、只置零一列、同模型复算、比较误差。零是中间排名，分母为零预测 SSE。差为负表示置零改善原样本拟合。 | 置零重要性四格 |
| 08 | Drop-to-Zero Importance: A Worked Calculation | 基准 SSE 20，模型 9.6→11.2，R² .52→.44，减少 8 个百分点。保持行、模型和分母固定。 | 文字、公式、代码或表格 |
| 09 | Characteristic Importance in Our Fitted Model | 横轴训练 R² 下降，市场 beta、成交额趋势和短长波动率比率最靠前；相关变量能相互替代，条无方向。轴写百分点需和附件口径核。 | 训练拟合重要性条形图 |
| 10 | Response Curves: How Predictions Change | 三幅示意原图横轴从低到高，纵轴模型预测；虚线惩罚线性、蓝实线非线性。固定其他特征，动量上升、波动下降、活动近乎平；模型结果不等于因果。 | 三条响应示意 |
| 11 | Response Curves: Calculating One Curve | 波动固定 0，动量从 −.5、0、+.5，预测 0.10%、0.10%、0.30%。先走 max 函数，再用输出系数，画前平后升。 | 文字、公式、代码或表格 |
| 12 | Response Curves in Our Fitted Stock Model | 横轴特征百分位，其他中心化排名固定零；纵轴周预测超额。beta 高段下降、成交额趋势升、波动比有台阶、ATR 末端急降；原森林和输入网格边界保留。 | 四条森林真实响应 |
| 13 | Cross-Sectional Portfolio Decisions | 进入按股票排序与权重。 | 封面或分隔 |
| 14 | A Top-Bottom Spread Tests a Ranking | 两腿各一单位，总暴露 2、净暴露 0。要总暴露 1 则收益减半。金额中性不保证 beta 或行业中性。 | 文字、公式、代码或表格 |
| 15 | Replace the Characteristic with a Forecast | 保持形成日、持有周和分组方式。特征排单列，预测排模型组合。MSE 看数值误差，高减低看极端组排序。 | 文字、公式、代码或表格 |
| 16 | Class 3’s Six Forecasts, Sorted | 冻结 52 周中 Ridge 周均高减低 +.48%，PCR +.46% 且由验证选出。LASSO/EN 常数无法排序。命中为正价差周比例。 | 文字、公式、代码或表格 |
| 17 | Long-Only and Long-Short Answer Different Mandates | 只做多非负权重、和为 1；美元中性两腿金额抵消。成本、集中度、借券、保证金和基准各不同。 | 文字、公式、代码或表格 |
| 18 | Three Ways to Turn One Forecast into Weights | 先横截面去均值，按五分组、绝对值总和归一，或对基准做只做多倾斜。全零信号多空跳过、只做多保留基准。 | 文字、公式、代码或表格 |
| 19 | Put the Three Rules on the Same Footing | 总暴露为绝对值和，净为带符号和。相同总暴露也可能风险不同；事先估计同频风险再按目标波动缩放，遵守上限与现金条件。 | 文字、公式、代码或表格 |
| 20 | Worked Example: Forecast-Weighted Positions | 去均值 0.3/0.1/−0.1/−0.3%，绝对和 0.8%，权重 ±37.5/±12.5%，按实现收益加权 1.75%，净零总一。 | 文字、公式、代码或表格 |
| 21 | Calculation Question: Forecast-Weighted Positions | 从 .8/.4/−.2/−.6% 预测和四股实现收益求均值、信号、权重、总/净敞口及未扣费收益。 | 文字、公式、代码或表格 |
| 22 | Cumulative Wealth Shows the Path, Not Just the Average | 横轴 2023-07 至 2026-06，纵轴 1 元财富；蓝低、灰中、红高、绿虚线高减低。恒生动量三分位，高低两腿各一单位，逐周连乘。 | 三分位财富与价差 |
| 23 | Return and Risk at a Common Frequency | 月 12、周 52。算术均值乘期数，波动和夏普在假设下按根号，复合增长从财富路径算。先标现金假设。 | 文字、公式、代码或表格 |
| 24 | Worked Example: Average Return and Compounded Wealth | 先涨 10% 再跌 10%，均值零、终值 0.99。夏普分子用平均超额，复合是财富增长。 | 文字、公式、代码或表格 |
| 25 | Multiple-Choice Question: Annualized Sharpe Ratio | 周均 .30%、无风险 .05%、波动 1.80%；用超额 .25% 除波动再乘根号 52，约 1.00。讨论用总收益和乘 52 的错。 | 文字、公式、代码或表格 |
| 26 | Multiple-Choice Question: Drop-to-Zero Importance | 原 SSE 80、置零 100、基准 200，下降 .10，选 A。 | 文字、公式、代码或表格 |
| 27 | Multiple-Choice Question: Portfolio Weights and Exposure | 四腿 .30/.20/−.25/−.25，绝对和 1，带符号加权收益 1.90%，选 B。 | 文字、公式、代码或表格 |
| 28 | Market Timing and Risk | 从横截面转时间序列。 | 封面或分隔 |
| 29 | Switching from Stock Selection to Market Timing | 择时选市场敞口，行是市场期；选股比较同日多个资产。前者目标市场对数收益，后者个股次期超额。 | 文字、公式、代码或表格 |
| 30 | Buy-and-Hold as the Investment Benchmark | 市场权重每月 1，用对数收益转换简单收益。对比同市场代理的 60 月择时，不含交易成本，择时现金在本例为零。 | 文字、公式、代码或表格 |
| 31 | One Forecast Sets Next Month’s Market Weight | 上月底看对数收益预测是否高于训练均值，若高就持有，否则现金。真实对数收益转换简单后乘已知权重。阈值不等于滞后 MA(12)。 | 文字、公式、代码或表格 |
| 32 | One Forecast, Two Benchmarks, Three Markets | 相对滞后 MA(12) 的预测误差和相对买入持有的投资表现分开。预测用 log，资金用 simple；167 预测试月份，60 测试，现金/成本零。 | 文字、公式、代码或表格 |
| 33 | One Timing Rule Creates Three Investment Paths | 同一长仓/现金规则给三种路径。黑买持，彩色择时，横轴日期纵轴每 1 元财富；沪深择时终点领先，SPY 与恒生落后。 | 三市场两规则财富路径 |
| 34 | U.S. Timing Still Trails Buy-and-Hold | 上图持有 45/60 月，0 为空仓；下图择时红线平坦期对照黑买持，年化均值 7.1 对 13.8%。 | 美国持仓开关与财富 |
| 35 | Hang Seng and CSI 300: The Same Rule, Opposite Outcomes | 恒生持 25 月均 −.9%，空 35 月市场 +.4%，终值 .72 对 .79；沪深持 50 月均 +.2%，空 10 月市场 −.6%，终值 1.02 对 .95。 | 文字、公式、代码或表格 |
| 36 | Position Sizing with the Current Market Excess-Return Forecasts | 均值方差权重等于超额预测除风险厌恶与方差乘积，再限 0–1。用滞后 SPY 波动，现金在此赚同期无风险，区别前例。 | 文字、公式、代码或表格 |
| 37 | Worked Example: Forecast and Risk Determine the Weight | 预测 .337%，年化波动 19.09% 换月方差，γ=5 得 22.2%。SPY −1.63%、现金 .45%，组合约 −.01%。 | 文字、公式、代码或表格 |
| 38 | Continuous Weights Change Return and Risk | 2021-07 到 2026-06，美国买持、LASSO、提升。年复合 13.3/4.9/11.1%，Sharpe .65/.57/.81，换手 0/4.6/23.2%。口径与滚动仓位。 | 文字、公式、代码或表格 |
| 39 | Portfolio Outcomes over the Same Market Path | 左侧三条复利财富线，右侧相对此前峰值回撤。颜色黑买持、蓝 LASSO、红提升，风险路径与终点分开。 | 财富和回撤 |
| 40 | Forecasts and Volatility Jointly Determine Weights | 横轴月份、纵轴市场百分比，蓝 LASSO、红提升。0 时资本按同期无风险收益计，波动升高可降低给定正预测的权重。 | 连续仓位路径 |
| 41 | Transaction Costs: A 10 bp Example | A 买 20%，B 卖 20%，总成交 40%，成本 0.001×.4=.0004，即 4 bp；100 万港元成本 400。 | 文字、公式、代码或表格 |
| 42 | Gross and Net Sharpe Ratios | 毛周超额 .20%、风险 2%、每周固定成本 .04%，净超额 .16%，风险不变；年化 .72 降 .58。 | 文字、公式、代码或表格 |
| 43 | Calculation Question: Trading Costs and Sharpe Ratios | 买卖各 30%，每边 10 bp，成本 .06%；均净 .24%、净超额 .19%。毛/净 Sharpe 约 1.00/.76，常数扣除不改波动。 | 文字、公式、代码或表格 |
| 44 | Maximum Drawdown Measures the Largest Peak-to-Trough Loss | 原图纵轴回撤%，横轴后测时间，三线最深点分别看历史高点跌幅；财富起点 1 也计入峰值。 | 最大回撤原图 |
| 45 | Alpha and Beta | 进入本地市场基准回归。 | 封面或分隔 |
| 46 | Two People behind the Portfolio Framework | 均值方差、有效前沿与 CAPM、beta 各有研究分工。1990 年奖与 Merton Miller 共享；人物为编辑插画。 | 生成肖像属装饰；保留作者贡献 |
| 47 | Alpha and Beta Separate Performance from Market Exposure | 拟合组合超额 = 截距 + beta×本地市场超额。beta 1.10 表示市场变一百分点，拟合超额变 1.10；残差均值零不要求 alpha 零。 | 文字、公式、代码或表格 |
| 48 | Beta Moves with the Market; Alpha Shifts the Fitted Return | 月 alpha .2%、beta 1.10；市场超额 −2/0/2% 得拟合 −2/.2/2.4%。总收益加无风险，实际另含残差。 | 文字、公式、代码或表格 |
| 49 | Calculation Question: What Is the CAPM Benchmark Return? | 周 rf .10%、市场超额 1%、beta 1.10，基准 1.20%，实际 1.40% 超出 .20 个百分点；一周不足以证明正 alpha。 | 文字、公式、代码或表格 |
| 50 | CAPM Alpha Must Use a Local Market Benchmark | 买持择时回归相对 SPY、恒生、沪深；年化 alpha −4.05、−4.77、+1.10%，全未显著。样本 60 月、现金同口径、费用零。 | 文字、公式、代码或表格 |
| 51 | Interpreting Estimated CAPM Alpha | alpha 是扣本地 beta 后的平均超额；标准误衡量精度。基准和遗漏暴露会改变结果，三市场 t 都弱。 | 文字、公式、代码或表格 |
| 52 | Alpha and Beta for Five Large HSI Constituents | 权重是 2026-08 快照，收益回归是 156 周。汇丰权重 8.91%、beta .53、年 alpha 32.4%、NW(4) t=3.61；区分权重、收益和检验口径。 | 文字、公式、代码或表格 |
| 53 | Assignment Data and Portfolio Rules | 80 股、17 个模拟信号，78+26 周有答案，隐藏 156 周只出权重。只做多、满仓、每股最多 10%；投资基准等权，预测基准零超额。 | 文字、公式、代码或表格 |
| 54 | The ML Investment Assignment | 源页记 20%、最多三人、10/15 14:00、8 页 PDF、156×81 权重、10MB ZIP 及评分表。与后续 brief/Canvas 分开，历史 15 页已由 10/6 更正为 8＋1 页；不代填本人状态。 | 文字、公式、代码或表格 |

## 待修方向

- EF5560-M05-01。按页顺序新增唯一入口及 §8 物理页精确链接，保留原主题深读和转录。
- EF5560-M05-02。核图清单、裁框、逐图读法和机制补图，按源位置核原题与答案。
- 具体缺口、题面和视觉验证在候选之后逐条更新；本诊断不表示教学验收。


## 最终正文与来源核验

§2/§8.1 均按 54 页物理顺序。p.21、25、26、27、43、49 原题中英、适用选项和 14 作答单元已逐项回源；p.25 B 附课堂确认，p.43 讲完 p.42 演示后明确留作自行计算，p.49 保留课堂方法与笔记逐题演算。p.46 编辑肖像按装饰处置。M04 顺延未见实质补讲。
