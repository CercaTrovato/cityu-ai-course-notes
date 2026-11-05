# M02 两版源页诊断

- `EF5560_Fintech_and_AI_in_Finance\course_files_export\Lec02_Regression_Vibe_Coding.pdf` · SHA-256 `9b97ce71cd43b176e572c9d6d691d315f154eac4fa5f6f12d56eda85795fa44e`
- `EF5560_Fintech_and_AI_in_Finance\course_files_export\canvas-20261020\Lec02_Regression_Vibe_Coding.pdf` · SHA-256 `95c1299e9011f35ccb2a20a18b858ddba9ad5db22862dc1cfc3b0b9c8705f676`
- 原笔记基线 `bbe947f74ccc94a15be7d53174701d5c51d6ace378240f711fb4cb9f15e64064`。

实际打开两版逐页联系表，旧 p.01–54 与 Canvas p.01–56 各 14 张。旧版 p.25 的左横轴百分比格式错误；新版 p.25 正常以年份标注。新版 p.26–27 是新增单选，旧题对应新版 p.54。最终候选 SHA-256 `89d58fb2992359a58464325579e37be3e86a48172d60be8dd17109338c584dd9`。作者及独审均完成两版源页核对与本版回读。

| Canvas 物理页 | 旧版物理页 | 原标题 | 视觉核到的内容 | 原图或页面处置 |
|---:|---:|---|---|---|
| 01 | 1 | FinTech and AI in Finance | 课程封面，Lec02 主题为收益预测与样本外设计。 | 封面或纯分隔 |
| 02 | 2 | From the Data Work to the Regression Work | 左侧 M01 建日历、定义已知时点并造特征；右侧 M02 比拟合、样本外和投资评价，冻结预测交 M05。 | 源表、正文或代码解释 |
| 03 | 3 | Return Predictability Has Several Meanings | 依次区分条件均值、样本内统计精度、后续预测误差、方向和实际投资。一个斜率不能同时证明五件事。 | 源表、正文或代码解释 |
| 04 | 4 | Regression with AI-Assisted | 分隔页，后续先定问题和输入。 | 封面或纯分隔 |
| 05 | 5 | James Simons: Prediction as a Research Process | 历史例讲团队把数学、物理和计算机组织进研究流程。教学动作是先保护时点，后测未来数据，再接可监控投资规则。肖像为编辑插画。 | 编辑插画可省，历史例保留 |
| 06 | 6 | What Regression Can Tell Us | 给定预测月前已知的输入，拟合值是截距加斜率乘输入；残差为实际减拟合。课件的四个追问各是外部条件，关联无法独立证明因果、稳定、可交易或新期间有效。 | 源表、正文或代码解释 |
| 07 | 7 | A Clear Instruction Specifies the Regression | 说清关联问题、2006-07 至 2026-06 的预测月行、目标与输入截止、拟合与报告对象、按日期验证。 | 源表、正文或代码解释 |
| 08 | 8 | Explore Before You Fit | 分隔页，接下来先查文件、时间与图。 | 封面或纯分隔 |
| 09 | 9 | Reload the Market Feature Table | 解析预测月日期、按时间排序、核 240 行、复制 2021-07 前 180 月。必须核本次实际加载的文件。 | 源表、正文或代码解释 |
| 10 | 10 | Restate the Forecast Clock | 箭头从上月底输入到本月实际收益。12 月动量、12 月波动和 10 月均线差都截至上月。讲义展示简单收益式，数据列按数据源分别核。 | 预测时钟公式箭头 |
| 11 | 11 | Ask Codex to Plot before Fitting | 横轴先知动量，纵轴实现月收益；透明点显示重叠，标签明确时点和单位。只画前 180 月以保护测试。 | 源表、正文或代码解释 |
| 12 | 12 | One Regression Question Looks Different across Markets | 左 SPY、中恒生、右沪深 300，浅点是单月，深点及连线为等频箱均值。沪深横轴可到约 300%，跨市场须先读坐标。 | 三市场散点与等频均值 |
| 13 | 13 | Why Equal-Count Bins Help | 按先知输入排队，分成约等人数十组，各组平均输入与目标，画一个点；把原始点留作离群诊断。 | 源表、正文或代码解释 |
| 14 | 14 | Ask Codex to Build Equal-Count Bins | 先 rank，再 qcut 取十个相近人数段，groupby 求两列均值，画十点。并列值受 rank(method=first) 的行序影响。 | 源表、正文或代码解释 |
| 15 | 15 | Correlation Is a Useful First Summary | 协方差除以两个标准差。在前 180 月，动量、波动率和均线差与目标的相关为 0.02、0.12、0.05，均弱。 | 源表、正文或代码解释 |
| 16 | 16 | Scale and Outliers Matter | 动量差 0.01 是 1 个百分点；年化波动与月收益分开。原题要求列绝对收益最大的五个月、是否删除及证据，旧新版同页。 | 源表、正文或代码解释 |
| 17 | 17 | Simple Regression | 分隔页，后续用一个预测量拟合。 | 封面或纯分隔 |
| 18 | 18 | The Fitted Line | OLS 找使各月残差平方和最小的一组截距和斜率。先算拟合值，再用实际减拟合得到残差。 | 源表、正文或代码解释 |
| 19 | 19 | Four Questions to Ask about a Regression | 斜率与单位、标准误和区间、拟合值残差和拟合度、后续行如何预测且不重拟合。 | 源表、正文或代码解释 |
| 20 | 20 | Fit the Simple Regression | 课件在 2006-07 至 2021-06 的 180 月估计下月收益与上月已知动量的直线。写方程后才知道输出每列含义。 | 源表、正文或代码解释 |
| 21 | 21 | Interpret the Momentum Coefficient in Units | 截距约 0.8%；动量上升 0.10 时用未舍入斜率算约 6.3 bp。结论范围是前 180 月拟合关联。 | 源表、正文或代码解释 |
| 22 | 22 | Reading the Standard Error | 动量估计 0.6 个百分点，标准误 2.1 个百分点，报告 t=0.31、p=0.76，显示四舍五入。大 p 无法证实零效应；误差假设另核。 | 源表、正文或代码解释 |
| 23 | 23 | R 2 Is a Variance Summary | 先以同样样本的均值为参照，再比较直线残差平方和。动量回归约 0.1%，解释极少波动；后续预测和投资问题还需检验。 | 源表、正文或代码解释 |
| 24 | 24 | Compare the Three Simple Regressions | 波动率的样本内 R² 约 1.5%，动量 0.1%、均线差 0.3%。不同单位、相关输入与同一拟合样本下，p 值不可直接排序预测性能。 | 源表、正文或代码解释 |
| 25 | 25 | Residuals Are Data, Not Waste | 左图按时间看成簇误差，右图横轴为拟合收益。旧 p.25 的日期刻度误格式化成百分比，新 p.25 改成年份；应各保留来源和勘误。 | 两幅残差图，新版已修时间轴；旧版独立保留 |
| 26 | 新增 | Multiple-Choice Question: Interpreting a Regression Slope | Canvas 新增 p.26。两变量均用百分点，动量从 2 到 4，预测变化 0.60 个百分点，笔记答案 D。旧 p.26 是另一题。 | 源表、正文或代码解释 |
| 27 | 新增 | Multiple-Choice Question: Statistical Precision and Model Fit | Canvas 新增 p.27。斜率 0.40、标准误 0.10、样本内 R²=0.03，p<0.05。笔记答案 A，精度不等同解释份额或未来准确率。 | 源表、正文或代码解释 |
| 28 | 27 | Multiple Regression | Canvas p.28 对应旧 p.27，只是分隔。 | 封面或纯分隔 |
| 29 | 28 | Why Add More Than One Predictor? | 同时给动量、波动和均线差，斜率读为另外两列保持不变时的变化。变量相关可改系数符号与大小，增加变量也可能增加估计噪声。 | 源表、正文或代码解释 |
| 30 | 29 | Our Predictors Are Strongly Related | 矩阵对角线 1 是自己与自己，找动量与均线差的交格 0.74。两者反复利用相近价格历史，不能当成独立赌注。 | 源表、正文或代码解释 |
| 31 | 30 | Correlated Predictors Make Individual Slopes Unstable | 多变量共同变化时，数据很难分清谁承担影响。换一段样本、去一列或比较系数稳定性，再将预测表现与单系数解释分开。 | 源表、正文或代码解释 |
| 32 | 31 | Standardize Using Training Data Only | 先用训练均值和训练标准差把每列转成距均值几个训练标准差。验证和测试应用已经定下的量，不重新计算。 | 源表、正文或代码解释 |
| 33 | 32 | Compare the Multiple Regression | 在训练集计算三个 z 分数的斜率。每个系数回答该列增加一个训练标准差、其余两列固定时的拟合收益变动。 | 源表、正文或代码解释 |
| 34 | 33 | What Changed in the Multiple Regression? | 斜率约 0.4、0.7、0.0 个百分点，波动最大且 p≈0.07，联合训练 R²=2.2%。解释时同时读标准误。 | 源表、正文或代码解释 |
| 35 | 34 | CSI 300 Case: Can China Macro Data Predict Next-Month Returns? | 预测月是沪深 300 的对数收益；四列为进出口同比、OECD 领先指标距 100、实际有效汇率 12 月变化。用 t−2 参考月，有历史修订限制。 | 源表、正文或代码解释 |
| 36 | 35 | CSI 300: Traditional Predictor Significance | 进口增速上升 1 个百分点，对应拟合月收益约低 0.15 个百分点，p=0.001；联合 F 检验 p=0.026、R²=6.1%。预留下一阶段看是否改善预测。 | 源表、正文或代码解释 |
| 37 | 36 | Out-of-Sample Design and Evaluation | 课件用 Campbell 与 Thompson、Welch 与 Goyal 的论文条目引出与历史均值比样本外结果。原页是论文条目信息截图，非空分隔。 | 论文条目信息原图 |
| 38 | 37 | Keep Financial Time Series in Date Order | 随机打乱可能用 2025 年拟合去评价 2010 年。按日期划分确保数据变换、选特征和估计均发生在被评估时点之前。 | 源表、正文或代码解释 |
| 39 | 38 | Training, Validation, and Test Have Different Jobs | 训练估参数；验证比较与选择；测试只评已冻结方案。看了最终测试再调，它就变成开发数据。 | 源表、正文或代码解释 |
| 40 | 39 | Use a Fixed Timeline for Today’s Exercise | 原图划分 2006-07–2018-06 开发、2018-07–2021-06 验证、2021-07–2026-06 测试。选完才可用全部 180 月重拟合，测试仍不可用。 | 固定切分时间线 |
| 41 | 40 | Fixed, Expanding, and Rolling Tests Answer Different Questions | 蓝段拟合、红段后测。固定保留一个切口；扩展起点不动右端向前；滚动两端都移动，宽度固定。每次都先蓝后红。 | 固定、扩展和滚动三行 |
| 42 | 41 | Tell Codex to Split by Date before Fitting | develop 估候选；valid 选择；train 重拟合定好的规格；test 单次评价。train 包含 develop 与 valid，test 另置。 | 源表、正文或代码解释 |
| 43 | 42 | How We Will Judge a Return Forecast | 样本关联、绝对误差、相对基准、方向、稳定性和净经济价值。每项对应不同输出。 | 源表、正文或代码解释 |
| 44 | 43 | Three Forecast Criteria Stay Fixed across Classes 2–4 | 均方误差对每月误差平方再平均；样本外 R² 用模型与基准平方误差比；命中率数同号预测。切分决定何时选择与何时计分。 | 源表、正文或代码解释 |
| 45 | 44 | The OOS R 2 Benchmark Must Match the Prediction Target | 市场月收益基准为此前已知 12 月收益均值；个股周主动收益基准为零，即预期跟随本地市场。方向另比正收益基准。 | 源表、正文或代码解释 |
| 46 | 45 | Let Codex Generate the Frozen Test Forecasts | 复制测试输入，用前 180 月学习的均值与标准差处理，调用已有系数；不在测试期重新拟合。保留日期和行序。 | 源表、正文或代码解释 |
| 47 | 46 | Compare with Lagged MA(12) in Every Market | 左图 OOS R² 均正，右图方向分数横跨 50% 参考线。画线并非各市场基准，方向须用各自多数方向对照。 | 双柱状图 |
| 48 | 47 | SPY Result Walkthrough: Direction Needs a Baseline | 三变量 63.3%，MA(12) 61.7%，始终预测正也是 63.3%（38/60）。样本含分配，而恒生与沪深价格指数不含。 | 源表、正文或代码解释 |
| 49 | 48 | Hang Seng and CSI 300: Direction against Their Own Base Rates | 恒生 OOS R² 4.4%，方向 25/60 低于 28/60；沪深 OOS R² 4.3%，方向 31/60 高于 29/60。此处用课件的始终为正参照。 | 源表、正文或代码解释 |
| 50 | 49 | SPY Result Walkthrough: Forecasts Move Little | 上图实际线比两条预测线起伏大。下图零以下为回归当月平方误差较小，不能把单月柱当累计分数；60 月汇总约 +6.6%。 | 两幅预测与误差差图 |
| 51 | 50 | SPY Result Walkthrough: Read the Full Dashboard | 按顺时针看拟合线、箱均、累计误差增益、后 60 月预测。累计增益上升表示相对 MA(12) 的差累计增加，波动不是投资回报。 | SPY 四图面板 |
| 52 | 51 | CSI 300 Macro Model: OOS Evaluation against Lagged MA(12) | 左边实际与两套预测，右边宏观模型误差条约 31.65、基准 27.97，纵向比较低者更好。OOS R² −13.2%，方向 48.3% 低于基准 56.7%。 | 宏观模型预测与损失双图 |
| 53 | 52 | When the Regression Output Looks Wrong | 先列名与前五行、手核三行时点、查缺失单位与极端值，再用单变量和独立实现核斜率，最后才加复杂度。 | 源表、正文或代码解释 |
| 54 | 26 | Multiple-Choice Question: Would You Use This Forecast? | 旧 p.26 移至新 p.54。正确证据是当时可知信息下击败滞后 MA(12) 的后续正 OOS R²，课堂确认 C。Discuss 区分样本内关系与后测。 | 源表、正文或代码解释 |
| 55 | 53 | In-Class Check: From Plot to Forecast | 对应旧 p.53。先读散点和箱均、系数和评分，再解释投资限制，最后给会改变结论的证据。当前已有的联合模型分数不能代替单变量。 | 源表、正文或代码解释 |
| 56 | 54 | What to Remember | 先画图再读斜率单位；为点预测与方向分别定基准；验证选择、测试一次并把冻结结果带到 M05 与买入持有比。 | 源表、正文或代码解释 |

## 待修缺口

- EF5560-M02-01。原 §2 混排两版页序，旧题、新题和日期轴版本定位需要分离。拟用 Canvas 物理页序作主入口，旧版 54 页另给逐行回指并保留旧 p.25 原图勘误。
- EF5560-M02-02。散点、相关矩阵、时间线、损失图及论文条目尚无同页原图和图义入口。资产仅在候选阶段按语义裁切。
- EF5560-M02-03。新版斜率题、拟合度题、移位旧题、离群讨论及动量检查题，须迁到 §2 题页并保留各自证据级别。


## 写回前绑定

正文 §2 按新 56 页物理序，§8 两张逐页表。旧 p.25 轴保留独立正文入口；其余旧映射页的去页尾页码文本与对应新版一致。图的具体正文锚点和裁框见 asset-evidence.json，机制流程与题面见 independent-review.md。独审 B1–B6 已闭合。
