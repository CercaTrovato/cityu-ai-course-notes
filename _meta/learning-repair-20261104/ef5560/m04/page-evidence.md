# M04 两版源页诊断

- `EF5560_Fintech_and_AI_in_Finance\course_files_export\Lec04_Nonlinear_Machine_Learning.pdf`，SHA-256 `62ca1f9191290baf426f4e950271723a2ae8baeac996fabd4b4c293350de187d`。
- `EF5560_Fintech_and_AI_in_Finance\course_files_export\canvas-20261020\Lec04_Nonlinear_Machine_Learning.pdf`，SHA-256 `d68f19775d74f9ca455f214a6ef1c0906da9a03e1a3f75d96ae123ef590f5c44`。
- 当前原笔记 SHA-256 `a555b07747ba3798dd70f392fc507772155043f4a8b67b12bb976358c82138ec`。

作者实际打开两版各 14 张联系表，旧版 54 页和新版 56 页。最终候选 SHA-256 `3f51148a64e7f6c893bbc39e14a88f1cf44e451bdef6a52e0d4367a714ab102d`；独审已回核两版全部 110 页。

| 新版物理页 | 旧版物理页 | 原题名 | 本页教学要素 | 图或页处置 |
|---:|---:|---|---|---|
| 01 | 1 | FinTech and AI in Finance | 非线性机器学习与收益预测。 | 封面或分隔 |
| 02 | 2 | Nonlinear ML for the Same Financial Questions | 输入及目标沿用 M03，允许信号效果随取值或其他特征改变；模型家族为树、树集成、前馈网络。 | 文字、公式、代码或表格 |
| 03 | 3 | Regimes and Nonlinear Forecasts | 进入回归树。 | 封面或分隔 |
| 04 | 4 | Linear and Tree Forecasts from the Same Data | 灰点 178 训练月，横轴滞后两月美国通胀，纵轴随后 SPY 月超额收益；蓝线连续一斜率，红线深度 1 过门槛跳变，均不是后测。 | 直线、阶梯和样本点 |
| 05 | 5 | Regression Trees: Forecasts by Regime | 回归树按条件分到叶，在训练叶子内用目标平均值。深度与最小叶量约束细分；预报新行只用可见输入。 | 文字、公式、代码或表格 |
| 06 | 8 | A Single Regression Tree: How the Splits Work | 新 p.06 为旧 p.08 图移位，旧标题误称一个分裂。根门槛通胀 2.482%，左支按失业率 7.65%，更左再按通胀 1.235%；True 左、False 右。四个叶的小数值约 −0.005、0.019、0.024、−0.014，输出要转百分数。 | 美国完整树 |
| 07 | 6 | Regression Trees: Fitting and Using the Rule | 新 p.07 对应旧 p.06。试候选变量 j 与门槛 s，比较两组各用均值时的误差平方和，最小者做分割。对子节点重复，受深度与叶量限制，再用后期验证选复杂度。 | 文字、公式、代码或表格 |
| 08 | 9 | How to Read the First Split | 新 p.08 对应旧 p.09。低通胀 132 月均值约 +1.5%，高通胀 46 月约 −1.4%。低通胀节点仍分裂，均值不等于最终叶预测；新版已明确。 | 文字、公式、代码或表格 |
| 09 | 新增 | The First and Second Splits | 新增简化图。根问通胀，右支 46 月已停止；左支 132 月再查失业率，右叶 +2.4%，左支还需回 p.06 的第三层。 | 根与次层简图 |
| 10 | 7 | Cross-Sectional Splits and Time-Series Splits | 截面同月分股票，时间序列同市场分月份；论文是按组学习不同规则和变量。事后 NBER 日期不能当当时可知状态。 | 文字、公式、代码或表格 |
| 11 | 10 | Similar Inflation Thresholds, Different Market Outcomes | 香港原图根约 2.456%，低侧 73.6% 样本预测约 +1.1%，高侧约 −2.4%。美国树 −2.6%、香港树 +4.7%，同样通胀输入也可有不同结果。 | 香港单门槛树 |
| 12 | 11 | Regression Trees: Choosing Depth on Validation Data | 示例深度 1/2/4/8 验证误差 28/26/29/35，选 2。训练误差随复杂度下降，验证反而先降后升；固定后重拟合。 | 文字、公式、代码或表格 |
| 13 | 12 | Tree Depth and Financial Regimes | 深度 1 只问一个条件，深度 2 可在波动状态内进一步看动量。更深每组样本少，需证据支持。 | 文字、公式、代码或表格 |
| 14 | 13 | Leaf Size Sets the Evidence Required for a Regime | 市场候选 12/24/36 月。小叶能保留少见状态但更噪，大叶稳定但会合并少见状态。 | 文字、公式、代码或表格 |
| 15 | 14 | Worked Example: Predicting with Two Leaves | 以 2.5% 滞后通胀切，低侧 3、1、2 均值 2%，高侧 0、−1、−2 均值 −1%。新月 2.0% 走左，3.5% 走右。 | 文字、公式、代码或表格 |
| 16 | 15 | Worked Example: Momentum Depends on Volatility | 低波动时高减低为 +0.6 个百分点，高波动时 −0.2。只相加的动量与波动斜率不能产生不同的动量差。树可先分波动再分动量。 | 文字、公式、代码或表格 |
| 17 | 16 | Using an Interaction in Stock Selection | 低波动 +0.6%、高波动 −0.2%；只做多可对前者相对加仓、后者减仓，权重仍须受约束且看后续排序/组合。 | 文字、公式、代码或表格 |
| 18 | 17 | Bagging and Boosting | 进入重复抽样与逐轮修正。 | 封面或分隔 |
| 19 | 18 | Bagging: Averaging Bootstrap Fits | 新增说明基学习器也可以是线性回归。每棵或每个模型的训练抽样有放回，预测同一新行再平均。共同误差比例留在平均中，更多模型主要减不相关部分。 | 文字、公式、代码或表格 |
| 20 | 19 | Bagging: From Resampled Data to One Forecast | 同一新月 0.8%、−0.2%、0.3%，等权平均 0.3%。新页补先每个抽样选变量再拟合线性、汇总；已有稳定 OLS 可能收益有限。 | 文字、公式、代码或表格 |
| 21 | 20 | Random Forests: Adding Random Predictor Selection | 每棵树抽训练行，每节点重新随机选候选列，再在其中找最优门槛。课件 30 列中抽 5；平均预测可受益于低相关。 | 文字、公式、代码或表格 |
| 22 | 新增 | Bootstrap Rows and Random Predictor Subsets | 新增双栏。左从 A–F 抽成 A、A、C、D、D、F，放回使重复与缺席并存。右一个节点选动量/Value，下一节点选 Vol./Size。图例 2/5，实际 5/30。 | 抽行/抽列对照原图 |
| 23 | 21 | Random Forests: Fitting a Weekly Stock Model | 78 周开发抽行，26 周验证选择深度叶量，104 周重拟合，后 52 周测。原例验证 300 棵，最终 500 棵，同周股票不拆。 | 文字、公式、代码或表格 |
| 24 | 22 | Gradient Boosting: Successive Forecast Corrections | 原图训练均值→实际减当前预测→拟合小修正→学习率缩放后加回并重复。新版明确树或简单回归都可作基学习器。 | Boosting 四格原图 |
| 25 | 23 | Gradient Boosting: Calculating One Update | 初值 0.5%，残差低组 +2.5/+0.5/+1.5、高组 −0.5/−1.5/−2.5。阈值 2.5% 叶均 +1.5/−1.5，学习率 .1 得 0.65%/0.35%。 | 文字、公式、代码或表格 |
| 26 | 24 | Tune Learning Rate and Tree Count Together on Validation | 预设候选对，在同一日期验证比较，测试前冻结。逐轮跟验证损失和停止点，与预设网格同属验证选择。 | 文字、公式、代码或表格 |
| 27 | 25 | Bagging and Boosting with Different Base Learners | 新版比较不同基学习器，袋装平均、提升求和。若各项均是同一输入的线性函数，求和平均仍线性。旧 p.25 有随机森林与梯度提升的对比表。 | 文字、公式、代码或表格 |
| 28 | 26 | Short-Answer Question: Is This Threshold Investable? | 只有四个月支撑、叶下限 12 时消失、较晚预测试拟合变阈值。挑两个警示，解释不足以做决策，提出不看测试的额外验证。 | 文字、公式、代码或表格 |
| 29 | 27 | Worked Example: Reading a Regression Tree | 先波动 1.5%≤2%，再动量 −0.4%≤0，走到 −0.2% 叶。旧 p.27 四选一及原选项保留。 | 文字、公式、代码或表格 |
| 30 | 28 | Why Random Predictor Subsets Help | 主导输入重复会令树误差相关；限制候选让部分节点看到其他信号，可能降低相关，仍须验证。旧 p.28 四选一保留。 | 文字、公式、代码或表格 |
| 31 | 29 | Neural Networks and Market Evidence | 进入前馈网络。 | 封面或分隔 |
| 32 | 30 | Feed-Forward Neural Networks | 动量 m 和波动 v 都接到 h1/h2/h3，每个隐藏单元有各自输入权重与非线性激活，输出再按三个权重合成下一周超额预测；偏置不在图上。 | 前馈 2→3→1 原图 |
| 33 | 新增 | Feed-Forward Networks: Why They Are Powerful | 新增三行表：输入效应随水平变、隐藏单元可表达交互、深层能复用先前组合。仅叠线性层仍线性；约束与验证仍需。 | 文字、公式、代码或表格 |
| 34 | 31 | Neural Networks: Fitting a Small Return Model | 训练平方误差加连接权重平方惩罚，偏置不惩罚；开发拟合尺度与候选，验证选节点数/惩罚/时长，再预测试重拟合。 | 文字、公式、代码或表格 |
| 35 | 32 | Worked Example: Reading a Hidden Unit | 输入动量权重 +1、波动 −1；ReLU 截断负数，输出权重 0.40% 和偏置 0.10%。A=0.5→0.30%，B=0→0.10%。 | 单隐藏单元 ReLU 图 |
| 36 | 33 | Early Stopping: Reading Training and Validation Loss | 10/30/60 轮验证 .0027/.0023/.0026，选 30。训练持续下降不足以放行。按日期验证，同周股票一起。 | 文字、公式、代码或表格 |
| 37 | 34 | Panel Size and the Number of Independent Dates | 市场 238 月；个股 12,281 行仅 156 周。同周共同冲击，行数不是独立次数。课程报告只列线性与树系，网络为教学扩展。 | 文字、公式、代码或表格 |
| 38 | 35 | Why Stock Panels Need Date-Based Splits | 新版把旧 p.35 三问变成讲解。30×156=4680 行，只有 156 个时点；随机行把更晚信息用来评较早，整周划分并在验证选网络大小、早停。 | 文字、公式、代码或表格 |
| 39 | 36 | Nonlinear Market Excess-Return Forecasts Struggle Out of Sample | 左上对 MA(12) 三模型三市场 R²，右上美国冻结提升预测 vs 实际；左下打乱列后的误差变化，右下各市场累计平方误差改善。日期、颜色和指标分别读。 | 宏观四图 |
| 40 | 37 | CSI 300: Policy Changes and Return Prediction | 横轴 2023-07 至 2026-06，黑色实现超额收益在 2024-09 标记附近跃升。所有模型仍用 2021-06 拟合，图例 R² 是这 36 月窗口，与全 60 月表不同。 | 沪深 36 月与标记原图 |
| 41 | 38 | Linear and Nonlinear Market Models on a Common Test | 美国旧 p.38 提升 +6.3%，新 p.41 +6.1%，不可静默统一。香港弹性网 +8.4%、树 +4.7%，内地 LASSO −0.6%、森林 −36.4%。冻结验证选择。 | 文字、公式、代码或表格 |
| 42 | 39 | What the Market Results Mean for an Investor | 阈值易说明但后测可能弱，强收缩平坦预测仍可能胜出；M05 将预测转市场敞口后核经济结果。 | 文字、公式、代码或表格 |
| 43 | 40 | Nonlinear Stock Return Forecasts | 旧 p.41 的市场/个股对照表在新版移除，仍保留旧入口。 | 封面或分隔 |
| 44 | 42 | How Much Data Support a Stock-Tree Leaf? | 候选最小叶 30、60、120 股周。若一周许多股票同跌，共同冲击并不会因股数多而变成很多独立证据。 | 文字、公式、代码或表格 |
| 45 | 43 | The Stock Tree Splits on Dollar-Volume Trend | 根问中心化成交额趋势排名≤0.15，左 64.4%、右 35.6%。图内 value 小数有舍入；预测按 p.46 表读。它是树族候选，选中非线性家族是森林。 | 成交额趋势树 |
| 46 | 44 | Reading the Dollar-Volume-Trend Split | 中心排名加 0.50 恢复百分位，0.15 约第 65 百分位。左 −0.01%、右 +0.43%；相对零测试约 −0.1%。 | 文字、公式、代码或表格 |
| 47 | 45 | Validation Separates Three Nonlinear Families by Very Little | 树 26.30、森林 26.25、提升 26.64（×10000），选森林；分别深度/叶量/学习率/树数，要把数与阶段分开。 | 文字、公式、代码或表格 |
| 48 | 46 | Multiple-Choice Question: Which Nonlinear Model Was Selected? | 四选一 B，按验证最小 MSE 0.0021；提升的测试 0.0018 不改变冻结结果，Discuss 要解释为什么。 | 文字、公式、代码或表格 |
| 49 | 47 | The Validation Winner Is Essentially Tied with Zero in the Test | 森林 21.89、提升 21.88、树 21.92（测试 ×10000）。前两项在一位小数显示 +0.0%，用 p.52 精确口径。 | 文字、公式、代码或表格 |
| 50 | 48 | Nonlinear Stock Return Forecasts Also Remain Weak | 验证误差、后测 R²、打乱特征的重要性、预测分组收益。右下五组曲线非同一误差，左下也不等于因果。 | 个股四图 |
| 51 | 49 | Worked Example: Read One Weekly Nonlinear Forecast | 2025-10-31 森林预测 +0.3%，实现超额约 −8.5%（−8.4% 减 +0.1% 无风险），方向和幅度均偏，需用全 52 周评估。 | 文字、公式、代码或表格 |
| 52 | 50 | Linear and Nonlinear Stock Return Forecasts Compared | 52 周 4108 行同样样本。验证选 PCR +0.02%、森林 +0.01%，其他提升 +0.04%，不能事后换赢家。 | 文字、公式、代码或表格 |
| 53 | 51 | Stock Ranking Evidence for the Nonlinear Models | 周均高减低，树 −0.01%、森林 +0.36%、提升 +0.34%，t 为 −0.06、1.04、0.87。两腿各一单位暴露、未扣费，证据有限。 | 文字、公式、代码或表格 |
| 54 | 52 | Accuracy, Ranking, and an Investment Mandate | 预期收益看 MSE 与 OOS R²，股票排序看分组价差，只做多还看仓位约束、风险和集中度。目标在开发验证确定。 | 文字、公式、代码或表格 |
| 55 | 53 | Forecast Accuracy and Stock Ranking Can Disagree | 新版讲解替代旧 p.53 两道短答。给 −1% 对零基准和未扣费 +0.08% 周价差；讲准度与排序，另看稳定性、精度、风险、集中度和成本。 | 文字、公式、代码或表格 |
| 56 | 54 | Interpreting the Weak Test Gains | 特征重叠、阈值只对短阶段有用、缺信号不能靠模型弥补。后续同时核信息、时间稳定性和算法。 | 文字、公式、代码或表格 |

## 旧版独有及实质差异

- 旧 p.41 市场／个股任务对照页移除，须保留独立入口，含 238 月、12,480／12,281 行、四宏观变量对 30 排名变量、相应基准与日期划分。
- 旧 p.08 原图标题说一层，但画了三层。新版 p.06 改题，p.09 新增前两层简图。旧 p.09 叫左叶均值，新 p.08 说明是还要分裂的节点均值。旧版 p.27、28、35、53 的原题，在新版 p.29、30、38、55 已改成示例或讲解，旧题要独立保留。
- 旧 p.25 RF/Boosting 比较表，新 p.27 扩展为可选不同基学习器；旧 p.38 美股 +6.3%，新 p.41 +6.1%，需结合 class04 报对应版本及复算。p.37/新 p.40 为 36 月范围，不能与全 60 月评分混用。
- 新 p.22 真实原图示例抽 2/5 列，与实际 5/30 分开。新 p.32 三隐藏单元不能用 p.35 单 ReLU 例当原图解释，须逐箭头对齐输入/输出权重与偏置。

## 待修方向

- EF5560-M04-01。两版页级顺序和变化需独立定位，不能用旧版范围页码指代新图。
- EF5560-M04-02。保存课堂原图与机制，优先美国多层树、Bagging/Boosting、前馈网络和四图面板。
- EF5560-M04-03。把原题和各小问放对应页，保留 A/B 双录音与旧 p.40–54 顺延口径。


## 最终正文与来源核验

§2 按新版 56 页物理序，§8 逐页覆盖旧 54 页及新 56 页，逐页登记原图和非内容处置。课堂旧 p.41 及新版已替换的旧原题保留独立入口。A/B 转录保留两个原时钟；M05 既有检索未见旧 p.40–54 实质补讲，顺延范围仍可自学。
