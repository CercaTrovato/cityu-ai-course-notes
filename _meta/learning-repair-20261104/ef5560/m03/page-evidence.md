# M03 两版源页诊断

- `EF5560_Fintech_and_AI_in_Finance\course_files_export\Lec03_Linear_Machine_Learning.pdf`，SHA-256 `8a84e4b1fe9bbe62e0a9fe1b9e41868a6d2cbad28088dfa306bf1c8a895eca44`。
- `EF5560_Fintech_and_AI_in_Finance\course_files_export\canvas-20261020\Lec03_Linear_Machine_Learning.pdf`，SHA-256 `f15a7e58ed66b633579df7bd26228a3ada2a071f3709c1df344f4b588f88212b`。
- 当前原笔记 SHA-256 `54251c42b560604fb0036f1ddb4a6f8c28e2ae5c08bf0a68b7fe1171c24069cb`。

主作者实际打开旧版与新版各 14 张联系表，旧版 p.01–56，新版 p.01–54；小字号图以源 PNG 可定向放大。下表为两版作者实际源页记录。最终候选 SHA-256 `0ba8d62580bd5d2325b816a7d02059e560028a41ad83577bb4516b4fa82c955f`；独审已回核两版全部 110 页。

| 新版物理页 | 旧版物理页 | 原题名 | 本页教学要素 | 图或页处置 |
|---:|---:|---|---|---|
| 01 | 01 | FinTech and AI in Finance | Lec03 线性机器学习预测收益。 | 封面或纯分隔 |
| 02 | 02 | Market Return Prediction and Stock Selection | 市场一月，用宏观输入预测超额收益，比滞后 MA(12)；股票一周，用技术特征预测超过同期无风险收益的部分，比零预测，并检查排序。 | 文字、公式、代码或表格 |
| 03 | 03 | Market Prediction with Linear Machine Learning | 分隔标题，先从市场模型进入。 | 封面或纯分隔 |
| 04 | 04 | A Landmark Paper for Machine Learning in Finance | Gu、Kelly、Xiu（2020）条目和首页截图。让不同模型在相同数据及样本外测试下比较，分别看预测误差与组合表现；对接三讲。 | 论文首页截图 |
| 05 | 05 | Four U.S. Macro Predictors across Three Equity Markets | 三个市场都用美国变量。期限利差和联邦基金利率滞后一月，失业率和通胀滞后两月；M02 沪深案例则用中国宏观。 | 文字、公式、代码或表格 |
| 06 | 06 | Ordinary Least Squares: A Monthly Market Excess-Return Forecast | 用训练月的实际超额收益减截距与各标准化输入乘斜率的和，平方后加总再除以两倍样本数。选使这个量最小的一组截距和斜率，没有斜率惩罚。 | 文字、公式、代码或表格 |
| 07 | 07 | OLS: Calculating Next Month’s Market Excess-Return Forecast | 教学给定截距 0.20%，期限利差 0.5 个训练标准差乘 0.40%，利率 −1 个标准差乘 −0.30%。贡献为 0.20、0.20、0.30 个百分点，合计 0.70%。 | 文字、公式、代码或表格 |
| 08 | 08 | Freeze the Market Chronology before Comparing Models | 142 个开发月、36 个验证月、60 个测试月。2006-07 和 08 给滞后输入，首个有效预测月为 09。设定选定后，用测试前 178 月重拟合。OLS 无惩罚参数，验证误差仍可作模型比较。 | 142/36/60 线 |
| 09 | 09 | Selection and Shrinkage | 分隔标题，接下来比较删去变量与缩小系数。 | 封面或纯分隔 |
| 10 | 10 | Forward Selection: Building a Short Predictor List | 新版把旧版的集合和最优化公式换成三步。先只用截距，每轮在相同开发月用普通回归试加每个未用输入，比较同一验证集。误差下降才纳入，未下降即停；只在联用时有用的两列可能都被漏掉。 | 文字、公式、代码或表格 |
| 11 | 11 | Worked Example: Forward Selection Stops when Validation Error Rises | 从 30.00 加利差降到 28.70，再加通胀降到 28.20，试加失业率回升到 28.40，停在两列；数值已乘 10000，是机制示例。 | 文字、公式、代码或表格 |
| 12 | 12 | Shrinkage in Market Excess-Return Prediction | 新版将旧版的大括号公式简化成训练误差加斜率代价。惩罚强度为零时回到 OLS，截距无惩罚；预测仍是线性，强度只用验证数据选。 | 文字、公式、代码或表格 |
| 13 | 13 | Ridge Regression: Keeping Related Signals | 斜率加倍则同一系数的平方惩罚变成四倍。相关输入如利率与利差能一起保留，缩小较大系数来限制不稳定；一般不会自动归零。 | 文字、公式、代码或表格 |
| 14 | 14 | Ridge: Choosing the Penalty and Making Predictions | 先用 142 月拟合尺度，再以 36 月验证。美国示例软件 alpha=100、验证误差乘 10000 后 27.02，测试 OOS R² −3.2%，优于 OLS 但仍输滞后 MA(12)。软件尺度依目标函数口径。 | 文字、公式、代码或表格 |
| 15 | 15 | LASSO: Selecting Signals through Shrinkage | 斜率加倍，绝对值代价也加倍；零点的折角可使弱斜率变成恰好零。输入高度相关时，留下哪列会随样本变化。 | 文字、公式、代码或表格 |
| 16 | 16 | LASSO: Reading the Selected Market Excess-Return Forecast | 课件教学系数只有期限利差保留 0.48，另两项为零。截距 0.10%、输入 0.5 个标准差，超额预测为 0.34%。课程实证路径不保证删变量。 | 文字、公式、代码或表格 |
| 17 | 17 | Elastic Net: Selection with Correlated Predictors | 总强度乘绝对值与平方的混合项；绝对值份额为 1 到 LASSO，为 0 到 Ridge，介于二者时兼顾稀疏与相关输入。 | 文字、公式、代码或表格 |
| 18 | 18 | Elastic Net: Choose Both Settings on Validation Data | 示例二维表中看最低 26.8，位于 LASSO 份额 0.25、惩罚 0.001。先定两项，再重拟合并测后期。 | 文字、公式、代码或表格 |
| 19 | 19 | How LASSO Coefficients Change with the Penalty | 横轴惩罚按对数刻度向右增大，纵轴一标准差的系数效应，四颜色对应四个宏观输入。虚线 0.001 处四条都离零，说明当前最优收缩保留了四列。 | LASSO 系数路径 |
| 20 | 20 | Choose the Penalty on Validation Data | 左 Ridge、右 LASSO，纵轴验证均方误差乘 10000，虚线为普通回归，星标各是网格最小。横轴都为对数尺度但两算法的值不可直接比强度。 | 验证网格两幅曲线 |
| 21 | 21 | Worked Example: Validation Chooses U.S. LASSO | 四行验证误差乘 10000 分别 29.21、27.02、26.93、27.15。最低是 LASSO，选择发生在测试前，差距小不能直接断言持续优势。 | 文字、公式、代码或表格 |
| 22 | 22 | Calculation Question: Evaluate the Market Excess-Return Forecast | 模型 SSE 0.018、滞后 MA(12) 0.015；代入得 −20%，模型平方误差多 20%。基准用预测时可见历史；符号是相对误差证据，另核交易。 | 文字、公式、代码或表格 |
| 23 | 23 | The Same Validation Rule Meets the Test in Three Markets | 相同 60 月中，验证选美国 LASSO −16.3%、香港弹性网 +8.4%、内地 LASSO −0.6%。香港 LASSO 测试 +10.1% 不能据后测反选。 | 文字、公式、代码或表格 |
| 24 | 24 | Market Excess-Return Forecasting Is Difficult in All Three Markets | 左上三市场滚动 12 月超额收益；右上四模型按市场列的样本外 R²；左下美国实际与选中 LASSO；右下各市场标准化系数。香港只有一个非零系数。 | 宏观四图 |
| 25 | 25 | Let Codex Fit Ridge and LASSO under One Specification | 把训练标准化和模型装在同一 pipeline，fit 在 train，predict 在 test。罚值先在 36 月验证选；同样的输入、切分与误差让比较公平。 | 文字、公式、代码或表格 |
| 26 | 26 | Multiple-Choice Question: Choosing a Market Excess-Return Rule | 英文四选一。用验证 MSE 选，0.0018 最小，为 LASSO，冻结后在开发加验证数据重拟合，再后测。 | 文字、公式、代码或表格 |
| 27 | 27 | Multiple-Choice Question: Predictor Units and Penalties | 英文四选一。0.03 变 3，使用开发期均值标准差对开发和验证同样转换。选 D，不能用测试缩放或在验证另学尺度。 | 文字、公式、代码或表格 |
| 28 | 28 | Stock Returns and | 分隔标题，开始股票周频。 | 封面或纯分隔 |
| 29 | 29 | The Observation Changes from Month to Stock-Week | 一个市场月份变成一只股票一个预测周。30 个滞后技术排名，12,480 理论行、12,281 可用行，按整周一起切分。零超额基准对应无风险收益。 | 文字、公式、代码或表格 |
| 30 | 30 | A Fixed July 2023 Stock Universe | 日期从 2023-07-07 至 2026-06-26，156 周乘 80 股。退出或缺值保留空项，不用后进成分填补；研究固定样本与跟踪指数成分是两个目标。 | 文字、公式、代码或表格 |
| 31 | 31 | Six Indicator Families Organize the Thirty Columns | 趋势、K 线几何、活跃、波动、振荡与市场风险。20 日动量用今日与 20 个交易日前收盘价，周横截面排名将不同单位换到共同尺度。 | 文字、公式、代码或表格 |
| 32 | 32 | Daily Data Become a Weekly Forecast Row without Leakage | 原图从上周前已知开高低收量，到计算特征、周内同组排名、给预测、最后才看实现收益。百分位排名减 0.50 得中心排名。6/19–26 的收益只能作 6/26 周目标。 | OHLCV 到目标的时序箭头 |
| 33 | 35 | Thirty Ranks Describe One Weekly Cross-Section | 横轴是一只股票（每五只标一号），纵轴一项特征。红表示较高中心排名，蓝表示较低；一列是该股整套相对特征。色值不是原始百分收益。 | 中心排名热图 |
| 34 | 36 | Characteristic-Sorted Quintile Portfolio Returns | 开发期每周先按一项已知特征排五组，同组等金额；随后算下一周平均超额收益，再跨周求平均。动量和均线差高组偏高，波动与非流动性高组偏低。 | 开发期按特征五分组四图 |
| 35 | 37 | Estimate One Linear Rule for the Cross-Section | 78 开发周 6123 行、26 验证周 2050 行、104 重拟合周 8173 行、52 后测周 4108 行。80 股仅 79 股提供目标，恒生银行无可用目标。 | 文字、公式、代码或表格 |
| 36 | 38 | Multiple-Choice Question: Which Linear Tool Fits the Job? | 同一标准误内按业务目标，岭保留 20 项太多，LASSO 留 4 项但常只保留家族代表，弹性网留 9 项且有分组保留。课堂旧 p.38，新 p.36；Discuss 解释 0.0001 不覆盖任务约束。 | 文字、公式、代码或表格 |
| 37 | 39 | Dimension Reduction | 分隔标题，下面用组合信号代替原始列。 | 封面或纯分隔 |
| 38 | 40 | Thirty Characteristics Are Not Thirty Signals | 左边是绝对秩相关矩阵，深色接近 1，不表示符号；右边横轴成分数，纵轴累计解释输入方差。3 个约 61%，5 个约 72%，10 个约 88%。 | 绝对相关热图与累计方差 |
| 39 | 41 | Principal Component Regression: Summarizing Many Inputs | 新版增加四格漫画：相关输入卡片、只用输入组成成分、把成分和训练收益送进回归、在验证集选成分数。旧 p.41 有选择最高方差单位方向及后续正交的公式，需独立保留。 | 新版 PCR 四格 |
| 40 | 42 | PCR: Calculating a Stock Excess-Return Forecast | 用 0.6×1+0.8×0.5 得成分 1，另一个成分 −0.5。截距 0.10%，乘两个回归系数后预测 0.50%。新股依次应用训练尺度、载荷和系数。 | 文字、公式、代码或表格 |
| 41 | 43 | PCR: What a Component Is Made Of | 两面板为第一、第二主成分，横轴是对各特征的权重。第一成分中多个趋势项向右、波动项向左，能理解为平稳上涨相对高波动的一种方向，载荷符号整体可翻转。 | PC1/PC2 载荷 |
| 42 | 44 | Partial Least Squares: Components That Use Returns | 第一方向找使投影与训练超额收益协方差平方最大的方向。后面用尚未解释的输入及收益信息提取，验证选成分数。组合与最后回归仍保持线性。 | 文字、公式、代码或表格 |
| 43 | 45 | PLS: From a Component to a Stock Excess-Return Forecast | 已给动量 0.5、波动 −1，按权重 0.8 与 −0.6 合成成分 1，截距 0.10% 加 0.30% 得 0.40%。示例数字用于演算。 | 文字、公式、代码或表格 |
| 44 | 46 | Weekly Prediction Evidence | 分隔标题，接下来按同一测试样本读模型和持仓排序。 | 封面或纯分隔 |
| 45 | 47 | Six Linear Models on the Same Stock Panel | 验证误差 26.20 最低，冻结五成分 PCR。测试 PCR +0.02%、PLS +0.05%，点估计小且 PLS 的测试高分不改选择。新版调整 LASSO/弹性网并列行顺序，数字未变。 | 文字、公式、代码或表格 |
| 46 | 48 | Linear Excess-Return Forecasts Remain Weak | 左上验证误差，右上对零超额的测试 R²，左下选中模型折回原特征的标准化斜率，右下只画有排序信息的模型分组实现收益。不要用最后一图给验证选模反向打分。 | 周频模型四图 |
| 47 | 49 | Three Stock Forecasts from One Test Week | 2025-07-04 的 CCB、美团、信义光能演示同向近、同向但幅度很错、方向相反三种情况。报告的是扣同期 +0.08% 无风险收益后的超额，全部测试有 4108 行。 | 文字、公式、代码或表格 |
| 48 | 50 | Vibe Coding: Compare Excess-Return Forecasts | 按整周验证挑参数，重拟合到 2025 年 6 月，测试相对零超额。第二张表指定同一股同一周，列事先预测和后来实现的超额收益。 | 文字、公式、代码或表格 |
| 49 | 51 | A Constant Excess-Return Forecast Cannot Rank Stocks | 本例 LASSO 与弹性网所选强度把 30 条斜率归零，股票预测都剩截距。误差可能尚可，却无法从中分辨高低；按 ticker 打破全平手不创造预测信息。 | 文字、公式、代码或表格 |
| 50 | 52 | Prediction Accuracy and Stock | 分隔标题，后续比较水平预测和排序效应。 | 封面或纯分隔 |
| 51 | 53 | Sorting Stocks by Their Return Forecasts | 每周在持有前按超额收益预测排队，分五组，记录各组实际收益，再比较测试期高减低。成本、仓位和风险评价留给 M05。 | 文字、公式、代码或表格 |
| 52 | 54 | Return Forecast Magnitude and Stock Ranking | A/B/C 实现 0.1%、0.2%、0.3%，B 模型将 A 模型的预测翻倍，保留同样次序。相同高低成员给 0.2 个百分点价差，但 B 的平方误差更大。 | 文字、公式、代码或表格 |
| 53 | 55 | Ridge: Weak Return-Forecast Accuracy, Positive Realized Spread | Ridge 对零基准 OOS R² −0.15%，Q5−Q1 周均 0.48 个百分点。52 周 t=1.46，前半 0.13、后半 0.83，未扣成本。 | 文字、公式、代码或表格 |
| 54 | 56 | The Question for Nonlinear ML | 线性模型每列系数固定；低波动与高波动股票的动量效应是否相同是经验问题。阈值及交互可以表达差异，要在后续同口径验证。 | 文字、公式、代码或表格 |

## 旧版特有内容

- 旧 p.33。保留各市场无风险收益代理表、上月底可知、不同频率换算以及零超额的含义。
- 旧 p.34。保留 2.0% 减 0.1% 得 1.9%，零预测误差 1.9%、1.7% 预测误差 0.2%，再扩展到整个面板相对零基准。
- 旧 p.10 的前向选择公式、新 p.10 的过程文字同机制，入口须保留旧符号对象。旧 p.12 完整目标与新简写分别解释。
- 旧 p.41 的最大方差单位向量及正交约束与新版 p.39 四格互补。四格为有教学含义的原图。旧 p.56 的低流动性/高波动交互追问在旧版入口保留。

## 待修

- EF5560-M03-01。原稿主题入口横跨多个页组，按新版物理页作主线，旧版逐页映射和独有两页分开。
- EF5560-M03-02。保留适用原图并核 p.39 四格机制、p.19–20 的轴与星标，以及 p.24、46 四图不同指标。
- EF5560-M03-03。按题页迁移既有原题与解析，核算法、周数及分数，维护 Class 3 数据包差异与旧 p.56 课堂结尾缺失边界。


## 最终正文与来源核验

§2 按新版 54 页物理序，§8 分列旧 56 页及新 54 页。旧 p.10、12、41 的数学表述和 p.33、34、56 独立定位。新版 p.39 的 PCR 四格保留原图。p.22、26、27、38 和旧 p.56 的英语题面及答案地位已逐项人工核对。独立报告保留计算、原题与资料口径证据。
