---
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

### 2.1 A1 · Ridge 怎样稳定相关变量的系数（原卷 p.2）

若干相关市场变量使 OLS 系数在相近样本中不稳定。保留原始输入改用 Ridge，问平方系数惩罚想改善什么，而不是保证所有样本都怎样。

来源：Practice Exam A p.2，原 Section A 第 1 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 1. Several correlated market predictors produce unstable OLS coefficients across nearby samples. An analyst uses Ridge while retaining the same original inputs. Which change is most consistent with the purpose of its squared-coefficient penalty?
> A. Unchanged slopes with a smaller reported standard error, because the penalty affects only inference.
> B. Smaller, more stable slopes, at the possible cost of a worse fit to the training observations.
> C. A separate forecast for every training observation, eliminating the need to estimate common coefficients.
> D. Larger slopes on every predictor, because retaining all inputs requires increasing their individual contributions.

</details>

**⚪ 参考选择：B。**

题目固定原始输入，只问岭回归（Ridge regression）的平方系数惩罚要做什么。普通最小二乘（Ordinary least squares，OLS）选让训练误差平方和最小的系数；Ridge 另外让大系数付出代价，在训练贴合程度与稳定之间取舍。相关变量可互相代替，OLS 在邻近样本中可能把很大正/负系数互相抵销；惩罚抑制这种极端配合，不是把每行各自记成一个预测。

**逐选项判断**

- A 说斜率不变、只缩小标准误，错：惩罚参与系数选择，本身会改变拟合。
- B 说系数较小/较稳定但训练拟合可能变差，符合目的。这里不承诺每一个相关变量的系数都逐项按同一比例缩小。
- C 说每个训练行单独预测就不用共同系数，错：仍学习可用于新样本的共同关系。
- D 说保留所有输入就要把每个斜率增大，错：保留变量与增加系数不是同一件事。

**English reference answer (not official)**

B. Ridge penalizes large squared coefficients and can trade some training fit for more stable coefficient estimates while retaining the original inputs.

💡 **为什么相关输入会让系数不稳（笔记补充）**

若两个输入几乎重复，模型可能用“很大正数加很大负数”得到同一预测。给一个完全重复输入的极简例：一行中两个输入都为 1，目标为 1，不加截距。系数 10 与 −9、系数 0.5 与 0.5，都预测 1，训练平方误差均为 0。

但两种系数的平方和分别是 181 与 0.5。Ridge 在拟合误差外还惩罚系数平方和，所以有理由抑制极端抵销。这里展示取舍机制，不是完整训练演示，也不保证每个变量系数都逐项变小。

设训练误差平方和为 $\mathrm{SSE}$，第 $j$ 个斜率是 $\beta_j$，非负惩罚强度为 $\lambda$。Ridge 比较的是 $\mathrm{SSE}+\lambda\sum_j\beta_j^2$；通常不惩罚截距，且输入尺度会影响惩罚比较，因此标准化需只用训练资料确定。

**改条件练习与边界**

若增加惩罚强度，通常更强调抑制系数；不能由此保证未来预测一定改善，仍需验证。

### 2.2 A2 · 嵌套 OLS 的训练误差为何不会增加（原卷 p.2）

在完全相同观测上，给 OLS 增添变量，大模型包含小模型。比较训练拟合误差与后来预测误差，注意 cannot rise 不等于 must fall strictly。

来源：Practice Exam A p.2，原 Section A 第 2 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 2. A researcher adds several predictors to an OLS return regression using exactly the same observations. The larger model contains the smaller one. Which statement about their fitting errors is correct?
> A. The larger model must have lower forecast error on later observations.
> B. The larger model's training SSE must fall strictly for every additional predictor.
> C. The larger model's training SSE cannot rise, but later forecast error can rise.
> D. The smaller model must have the higher in-sample R-squared.

</details>

**⚪ 参考选择：C。**

larger model contains the smaller one 表示新模型保留全部旧变量；同一批观测很关键。新模型至少可以把新增系数设为零，复现旧模型，所以在自由寻找最小训练误差时不可能比旧解更差。但后来的资料没参与这个最小化，可能因拟合噪声反而更差。误差平方和（Sum of squared errors，SSE）是每行真实值与拟合值之差先平方再相加。

**逐选项判断**

- A 说后来预测误差必降，错：训练改进不保证样本外。
- B 说每增变量 SSE 必严格下降，错：无帮助变量可能系数为零，SSE 只保持不变。
- C 说训练 SSE 不升、后来误差可升，正确。
- D 说小模型样本内决定系数一定更高，错：同一目标和观测下，训练 SSE 不升意味着通常的含截距 R² 不降，而非小模型必更高。

**English reference answer (not official)**

C. The larger model can reproduce the smaller model by setting new coefficients to zero, so its minimum training SSE cannot rise. Its forecast error on later observations may nevertheless increase.

💡 **“不增加”的证明只要一个可行解**

旧模型若是“截距加一个变量乘斜率”，新模型再添一个变量。新变量斜率设为零，旧预测一行不变；新模型寻找所有可行系数中训练 SSE 最小的组合，至少不会比这个可行旧解更差。

但这不约束新月份的误差。若新增变量只是训练噪声，训练更贴合却可能预测更差。这里假定两模型对同一目标、同一观测求真正的 OLS 最小值，不把不同样本、正则化或未收敛算法混入。

**改条件练习与边界**

若两模型换了样本，原有“不升”比较失去同一组误差对象，不能直接套用。

### 2.3 A3 · PCR 与 PLS 在构造成分时用什么（原卷 p.2）

一人想用相关预测变量概括成分，另一人想让训练收益也参与构造成分。问 PCR 与 PLS 在这一步用什么资料。

来源：Practice Exam A p.2，原 Section A 第 3 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 3. An analyst wants components that summarize correlated predictors before fitting a return equation. Another analyst wants training returns to influence component construction. Which distinction between PCR and PLS addresses these two objectives?
> A. Both use training returns to construct components, but only PCR retains the original predictors.
> B. PCR selects original predictors by significance, whereas PLS groups observations by tree thresholds.
> C. PCR forms components from predictors alone; PLS also uses training returns when constructing components.
> D. PLS uses final test returns to construct components, whereas PCR must use validation returns.

</details>

**⚪ 参考选择：C。**

主成分回归（Principal component regression，PCR）先用预测变量自身构造成分，再用成分预测收益；偏最小二乘（Partial least squares，PLS）构造成分时也参考训练收益。成分是原变量的组合，减少相关输入的重复表达，不是把企业按树分组。训练目标可用，最终测试收益不能提前进入成分。

**逐选项判断**

- A 说两者都用训练收益且只有 PCR 保留原变量，错：PCR 构造成分本身不使用收益目标。
- B 把 PCR 说成显著性选原变量、PLS 说成树阈值分组，均错。
- C 分清 PCR 仅用输入、PLS 同时用训练收益，正确。
- D 要用最终测试收益或强制验证收益构造成分，错：会泄漏或混淆训练与选择阶段。

**English reference answer (not official)**

C. PCR constructs components from predictors alone, whereas PLS also uses training returns in component construction. Neither should use final test outcomes to build those components.

💡 **成分不是重新挑几列**

一个成分可以是多个输入的加权组合，例如把两个相关财务指标压成一个综合刻度。PCR 先看输入怎样共同变化，再拿成分拟合收益；PLS 在造综合刻度时就让训练收益参与。后者能使用训练标签，不代表可偷看最终测试收益。

成分数量等设置可用验证资料选择，但构造与评估的时间边界必须保留。题目不要求手算成分权重，不能凭题面捏造某个最优权重。

**改条件练习与边界**

最终测试期只用于评估；不能看到其收益以后重构 PLS 再称未见测试。

### 2.4 A4 · Alpha 与 Beta 的水平和变化分开算（原卷 p.3）

月度绩效回归 alpha 为 0.20%，市场 beta 为 1.50；市场超额收益从 0 变 2.00%。求拟合组合超额收益的起点与终点，不是只求增量。

来源：Practice Exam A p.3，原 Section A 第 4 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 4. A fitted monthly performance regression has alpha 0.20% and market beta 1.50. Market excess return changes from zero to 2.00%. What happens to the fitted portfolio excess return?
> A. It rises from 1.50% to 1.70%.
> B. It rises from zero to 3.00%.
> C. It rises from 0.20% to 3.20%.
> D. It rises from 0.20% to 2.20%.

</details>

**⚪ 参考选择：C。**

回归拟合的组合超额收益等于截距 Alpha 加市场 Beta 乘市场超额收益。Alpha 是市场超额为零时的拟合值；Beta 是市场超额每变 1 个百分点，拟合组合变化多少个百分点。本题月度 Alpha 0.20%，Beta 1.50，市场由 0 到 2.00%。先算起点 0.20%；终点 $0.20\%+1.50\times2.00\%=3.20\%$，上升 3.00 个百分点。

**逐选项判断**

- A 的 1.50% 起点把无单位 Beta 当成收益率，错。
- B 起点为零，漏掉 Alpha，虽算对变化量 3.00 个百分点却没答拟合水平。
- C 从 0.20% 到 3.20%，正确。
- D 只加市场 2 个百分点，忽略 Beta=1.50 的斜率。

**English reference answer (not official)**

C. The fitted excess return rises from 0.20% to 0.20% + 1.50 × 2.00% = 3.20%, an increase of 3.00 percentage points.

**用一个公式核单位与时点**

写 $\widehat r_p^e=\alpha+\beta r_m^e$：上标 $e$ 表示超额收益，即收益减同期无风险收益；帽号表示回归拟合，不是保证的未来实现收益。

| 量 | 本题含义 | 单位/取值 | 何时可用 |
|---|---|---|---|
| $\alpha$ | 市场超额为零时拟合值 | 月收益 0.20% | 已给拟合参数 |
| $\beta$ | 市场每变 1 个百分点的响应 | 无量纲 1.50 | 已给拟合参数 |
| $r_m^e$ | 本题市场超额收益 | 月收益 0→2.00% | 两个题设情景 |
| $\widehat r_p^e$ | 组合拟合超额收益 | 月收益，待算 | 给定情景后可算 |

市场为零时仍有 alpha 0.20%；市场变成 2.00% 时，市场项贡献 3.00 个百分点，加原 0.20% 得 3.20%。拟合值的变化是 3.00 个百分点，不是 3.20 个百分点。

**改条件练习与边界**

若 Beta 为零，市场变化不改变拟合值；Alpha 仍留在原水平。

### 2.5 A5 · 双边换手成本与周夏普比率（原卷 p.3）

每周买入组合价值的 30%、卖出 30%，每次交易成本为交易金额的 10 bp。毛平均超额收益 0.30%、波动 3.00%，求扣费后的均值和周夏普，不要年化。

来源：Practice Exam A p.3，原 Section A 第 5 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 5. Each week a portfolio buys 30% and sells 30% of its value at 10 bp per trade. Gross mean excess return is 0.30% and volatility 3.00%. What are net mean and weekly Sharpe ratio?
> A. 0.24% and 0.10, because a constant cost leaves both risk and risk-adjusted performance unchanged.
> B. 0.24% and 0.08, because a constant cost lowers the mean but not the volatility.
> C. 0.30% and 0.08, because transaction costs affect the Sharpe ratio without changing mean return.
> D. 0.24% and 0.24, because the mean return itself is the weekly Sharpe ratio.

</details>

**⚪ 参考选择：B。**

10 个基点（Basis points，bp）等于每笔交易金额的 0.10%。买 30%、卖 30% 都要收费，费用占组合价值 $(30\%+30\%)\times0.10\%=0.06\%$。净平均超额收益为 $0.30\%-0.06\%=0.24\%$。题设每周同样比例和费率，扣固定收益量不改变周波动率 3.00%；周夏普比率（Sharpe ratio）为净平均超额收益除同频波动率，$0.24/3.00=0.08$。

**逐选项判断**

- A 净平均值对，但夏普仍写毛值 0.10，错：分子已下降。
- B 净均值 0.24%、周夏普 0.08，正确。
- C 平均值仍写 0.30%，忽略交易成本；改变夏普却不扣分子不一致。
- D 把净平均收益 0.24 当夏普，遗漏除波动率。

**English reference answer (not official)**

B. Total weekly trading cost is 0.06% of portfolio value, so net mean excess return is 0.24%. With constant costs and 3.00% weekly volatility, the weekly Sharpe ratio is 0.08.

**从 100 元组合重走成本（笔记补充）**

10 bp（基点，basis points）是 0.10%，不是 10%。若组合价值 100 元，买 30 元收费 0.03 元，卖 30 元也收费 0.03 元；总费 0.06 元，即组合价值的 0.06%。成本从毛超额收益中扣除，0.30% 变 0.24%。

周夏普 $S_{\mathrm{weekly}}=\mu_{\mathrm{weekly}}^e/\sigma_{\mathrm{weekly}}$，分子是周平均超额收益，分母是同一频率的波动率（收益围绕均值的离散程度）。同用百分数算 $0.24/3.00=0.08$，或同用小数算 $0.0024/0.0300=0.08$，不能一边用百分数一边用小数。

每周都减同一个收益比例时，每周收益和它的新均值一起平移，离均差不变，所以本题波动不变。成本变化才可能改变波动，不能泛化“任何成本都不改变风险”。

**改条件练习与边界**

若换手每周变化，成本也会变化，不能继续假定扣费完全不改变波动率；本题不要求年化。

### 2.6 A6 · 总敞口和净敞口分别加减（原卷 p.3）

初始资本的 60% 做多、40% 做空；在价格变化之前，分别算不计方向的总敞口和保留方向的净敞口。

来源：Practice Exam A p.3，原 Section A 第 6 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 6. A portfolio invests 60 percent of initial capital in long positions and sells short 40 percent. The manager reports both gross and net exposure. Which pair correctly describes this position before market movements?
> A. Gross 20 percent and net 100 percent.
> B. Gross 60 percent and net minus 40 percent.
> C. Gross 100 percent and net zero.
> D. Gross 100 percent and net 20 percent.

</details>

**⚪ 参考选择：D。**

做多（Long）是买入并持有，做空（Short）是借资产卖出以后再买回归还。都以初始资本为分母。总敞口（Gross exposure）按两边金额绝对值相加，$60\%+40\%=100\%$；净敞口（Net exposure）保留方向相减，$60\%-40\%=20\%$。这是交易前持仓口径，不是各资产未来实际市场 Beta。

**逐选项判断**

- A 把总/净两种算法换反。
- B 只报多头和空头各自大小，没算组合的总/净。
- C 总 100% 对，但两边不是相等，净不能是零。
- D 总 100%、净 20%，正确。

**English reference answer (not official)**

D. Gross exposure is 60% + 40% = 100% of initial capital, while net exposure is 60% − 40% = 20%.

**一行先固定一个分母**

以初始资本 100 元为基准，60 元多头的有向金额为 +60，40 元空头为 −40。总敞口把绝对金额相加，得到 100 元/100 元；净敞口按方向相加，得到 20 元/100 元。

| 指标 | 计算对象 | 本题结果 |
|---|---|---:|
| 总敞口 | 两边绝对金额/资本 | 100% |
| 净敞口 | 多头金额减空头金额，再除资本 | 20% |

剩余资金或做空所得如何放置不在题面中，不能由净 20% 推出具体现金余额，更不能直接等同市场 beta。

**改条件练习与边界**

若改多 50%、空 50%，总仍 100%、净才为零；零净金额也不保证所有风险对冲。

### 2.7 A7 · 链上有资产不等于客户能完整取回（原卷 p.4）

家族办公室把加密资产交交易平台托管；链上余额很大，但平台财困停提。问什么证据最能判断该客户取回资产的前景，不是问平台有没有某个钱包。

来源：Practice Exam A p.4，原 Section A 第 7 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 7. A family office leaves crypto assets with a trading platform. The platform reports large holdings on the blockchain but suspends withdrawals during financial distress. Which evidence best informs the office's prospects of recovering its assets?
> A. Its custody contract, client-asset segregation and the claims that other creditors have against the assets.
> B. The platform's visible wallet balance alone, treating every recorded asset as available to this client.
> C. The speed of withdrawals before the suspension, used as evidence of legal priority in insolvency.
> D. The proportion held offline, treated as a substitute for verifying the office's ownership rights.

</details>

**⚪ 参考选择：A。**

这里是给定托管危机场景，不是要求判断某家真实公司的破产法律。客户需分清代持合同给什么权利、客户资产是否与平台自有资产隔离（Segregation）、其他债权人能主张哪些资产。链上数量只是资产可见性的一部分，不直接说明负债或各客户权利。

**逐选项判断**

- A 合同、隔离及其他债权主张直接关系回收前景，正确。
- B 仅看大钱包余额就当全部属于该客户，忽略归属和其他债权。
- C 危机前提款快不证明破产时法定或合同优先。
- D 离线比例可能关乎访问安全，却不能替代资产所有权/请求权核查。

**English reference answer (not official)**

A. The custody contract, segregation of client assets and competing creditor claims are more informative about recovery than a visible wallet balance or past withdrawal speed alone.

**本题的证据边界**

链上地址显示 100 单位资产，不告诉你平台是不是欠所有客户 150 单位，也不告诉你哪 10 单位依法属于这一客户。托管是替客户保存/控制资产；隔离是把客户资产与平台自身资产按适用安排分开。合同、资产归属与竞争请求共同影响回收。

这个 100/150/10 仅是笔记补充。题目未给法域、破产文件和完整资产负债，不能算具体回收比例或承诺优先顺位。

**改条件练习与边界**

即使资产证明成立，还要核负债和权利；题面不足以给出确定回收比例。

### 2.8 A8 · 共享分叉前历史不等于以后同链（原卷 p.4）

BTC 与 BCH 共享 2017 年分开前的交易史，之后遵守不同规则。问共享历史是否强迫后来的交易和价格相同。

来源：Practice Exam A p.4，原 Section A 第 8 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 8. BTC and BCH shared transaction history before their 2017 split but followed different rules afterwards. An investor compares their subsequent prices and transfers. Which interpretation of the fork is consistent with the class discussion?
> A. The shared history requires both assets to retain the same market price.
> B. The networks can develop separate transactions and prices despite sharing the earlier history.
> C. A later transaction on one network must automatically update balances on the other.
> D. The larger block capacity gives BCH a contractual claim on Bitcoin mining revenue.

</details>

**⚪ 参考选择：B。**

题面已给 BTC/BCH 于 2017 年分开后使用不同规则。分叉（Fork）表示共享部分历史后，各网络可独立接受交易和形成后续状态。它不是两个资产之间的固定兑换承诺，也没有自动创造对另一网络收入的合同权利。

**逐选项判断**

- A 共享过去不强制以后同价。
- B 两网可有分开的交易和价格，正确。
- C 一网的新交易不因旧历史相同而自动更新另一网。
- D 更大区块容量是协议特征，不是分配比特币矿业收入的合同。

**English reference answer (not official)**

B. Shared pre-fork history does not prevent the networks from developing separate later transactions, balances and market prices under different rules.

**读“同一历史”与“分开以后”**

可把记录按时间分两列：分叉前的记录是共同前史；分叉后的新交易按各自网络规则验证。它们没有因历史相同而变成一份实时同步的账户。

本题不要求处理重放攻击等协议细节；“并非自动更新另一链”不表示每一种分叉机制在所有场景都绝无交互风险。只回答共享前史本身不强制交易、价格和收入权相同。

**改条件练习与边界**

若要跨网络转移价值，需要另外的交易/桥接安排及其风险，不能凭历史共同性假定已转移。

### 2.9 A9 · 代币化基金的收益从哪里来（原卷 p.4）

代币化货币市场基金向投资者分配收入，单位在数字平台流转。问收入从哪来，而不是单位怎样换持有人。

来源：Practice Exam A p.4，原 Section A 第 9 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 9. A tokenized money-market fund distributes income to investors while allowing its units to move on a digital platform. A student attributes the income to token transfers. Which explanation correctly identifies the source of that return?
> A. Every transfer creates new interest because ownership is recorded on a shared ledger.
> B. The fund manager's management fee is an extra investment return credited to each unit holder.
> C. The underlying deposits or securities generate income, which accrues to investors after fund expenses.
> D. Issuing more units raises income per existing unit even if the additional cash is not invested.

</details>

**⚪ 参考选择：C。**

货币市场基金（Money-market fund）持有存款或短期证券等资产，它们的利息/收益先产生，再扣基金费用并按单位权益归投资者。代币转让记录持有人变化，记录动作本身不会让底层资产多付利息。

**逐选项判断**

- A 每次转移都新生利息，错：把记录技术当收益来源。
- B 管理费是费用扣减，不是额外送给持有人的收益。
- C 底层资产收入扣费用后归投资者，正确。
- D 新发单位若现金没投资，不保证每个旧单位收入提高；单位数也改变分配分母。

**English reference answer (not official)**

C. Income comes from the fund's underlying deposits or securities and accrues to investors after expenses. Token transfers record ownership changes rather than generate the return.

**让钱和记录分开走**

底层存款/证券→产生投资收入→扣基金费用→按单位权益归投资者；代币登记→记录单位由谁持有。第二条改变收入归属的记录，不是第一条收入的经济来源。

即使平台转账非常频繁，底层资产不付息也不会因“记账次数多”自动生出同样收益；题目未给实际收益率，不能计算数额。

**改条件练习与边界**

同一底层资产改用普通登记册，利息来源仍是资产，未因不代币化就归零。

### 2.10 A10 · NFT 的代币、媒体和使用权三层（原卷 p.5）

买了关联数字艺术品的 NFT，代币历史可查，但媒体链接失效且未说明版权许可。把代币归属、媒体访问、法律使用权分开。

来源：Practice Exam A p.5，原 Section A 第 10 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 10. An investor buys an NFT associated with a digital artwork. The token's ownership history is verifiable, but the metadata link stops working and no copyright licence is stated. Which assessment best separates the relevant issues?
> A. Token ownership, access to the media and legal usage rights require separate checks.
> B. The broken link cancels every past token transfer automatically.
> C. Verifiable token ownership establishes permanent access to the image and full copyright.
> D. The purchase price determines which copyright rights accompany the token.

</details>

**⚪ 参考选择：A。**

非同质化代币（Non-fungible token，NFT）链上记录可验证，不等于链接指向的图片永远可访问，也不自动产生版权许可。元数据（Metadata）链接是找到媒体的路径；法律使用权来自相关许可或权利安排，题面明确未载明。

**逐选项判断**

- A 三层分别查，正确。
- B 链接坏不会自动撤销过去所有代币交易。
- C 把可验证代币持有升级为永久媒体/完整版权，超出题设。
- D 价格高低不能单独决定附带版权范围。

**English reference answer (not official)**

A. Verify token ownership, continued access to the media and legal usage rights separately. A verifiable token history alone establishes neither permanent image access nor a copyright licence.

**三层分别验什么**

| 层次 | 应查证据 | 修好媒体链接能否一起解决 |
|---|---|---|
| 代币持有 | 代币/合约及交易记录 | 不自动改变历史归属 |
| 媒体访问 | 存储位置、链接和持续可取用性 | 可修此层访问问题 |
| 法律使用权 | 版权许可或其他明确权利安排 | 不能因此自动补出许可 |

本题不是对具体 NFT 买卖作法律鉴定。未知许可不能写成“绝对没有任何权利”，只能说链上历史本身不足以证明所需使用权。

**改条件练习与边界**

即使链接修好，版权许可仍需单独核；不要用解决一层问题代替三层。

### 2.11 A11 · 界面相似时看谁承担货币负债（原卷 p.5）

央行发行零售 CBDC，商行通过类似 App 提供普通存款。问谁对持有人承担货币负债，不按界面相似判断。

来源：Practice Exam A p.5，原 Section A 第 11 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 11. A central bank issues a retail CBDC, while a commercial bank offers ordinary deposits through a similar mobile interface. Which distinction matters when comparing the financial claims rather than the appearance of the applications?
> A. Both are central-bank liabilities whenever customers access them through a licensed banking application.
> B. The deposit becomes a central-bank liability as soon as its payment instructions are processed digitally.
> C. Neither has an issuer liability because digital balances are only entries on an electronic ledger.
> D. The CBDC is a central-bank liability; the deposit is a claim on the commercial bank.

</details>

**⚪ 参考选择：D。**

题目明确第一项是央行发行的零售中央银行数字货币（CBDC），第二项是商业银行普通存款。请求权（Claim）要问谁欠持有人钱；App 属于谁和指令数字化不改变发行负债身份。本题按这两个明确设定回答，不把所有名为 e-CNY 的特定版本安排一概套入。

**逐选项判断**

- A 持牌银行 App 并不会使两种余额都变成央行负债。
- B 数字处理存款指令不会把商行债务转成央行债务。
- C 电子记录仍可代表负债，不因数字化就无发行人。
- D CBDC 是央行负债，普通存款是对商业银行的请求权，正确。

**English reference answer (not official)**

D. Under the stated setup, the CBDC is a central-bank liability and an ordinary deposit is a claim on the commercial bank; a similar interface does not make the claims identical.

**“谁欠钱”比“哪个 App”更重要**

中央银行数字货币（central bank digital currency, CBDC）在本题明确由央行发行；普通存款是银行对存款人的债务。商业银行帮用户展示或转移一种央行负债，不会单靠界面把它变成自己的存款债务，反之亦然。

本题没有要求估计风险大小、存款保障或具体 e-CNY 最新机制，勿擅自添加当前政策事实。

**改条件练习与边界**

如果新题改变发行人或钱包合同，须按新条件重新判断，不能只背名称。

### 2.12 A12 · 开户量与真实支付采用分开（原卷 p.5）

e-CNY 钱包注册数增长，但要判断开户之后是否真的使用支付。需要活跃与重复付款证据，并统一期间和分母。

来源：Practice Exam A p.5，原 Section A 第 12 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 12. A bank reports rapid growth in e-CNY wallet registrations, but an evaluation team wants to know whether customers actually use the payment service. Which additional evidence most directly addresses adoption beyond account opening?
> A. Active wallets and repeat payments, compared over the same period and against a clear transaction denominator.
> B. Cumulative wallet registrations alone, because each registration represents continuing use of the service.
> C. The largest wallet balance, treated as the typical customer's daily payment activity.
> D. The number of application downloads, without distinguishing inactive wallets or repeat users.

</details>

**⚪ 参考选择：A。**

本题问 beyond account opening，即超过“开过户”的证据。活跃钱包与重复付款能看持续使用，但仍要统一观察期间和分母，例如固定注册批次中后续真正付款者比例；下载总量、最大余额不能代表典型使用。

**逐选项判断**

- A 同期间活跃/重复付款与明确分母最直接，正确。
- B 累计注册不是每个账户都持续活跃。
- C 最大余额是极端个案，不是典型日常支付。
- D 下载数未区分停用、重复或从不付款，不能直接代表采用。

**English reference answer (not official)**

A. Active wallets and repeat payments, measured over comparable periods with a clear denominator, directly address use beyond registration.

**分母决定你在衡量什么（笔记补充）**

固定同一月份，可先定义活跃钱包为当月至少付款一次的钱包。若某注册批次有 1,000 个钱包，100 个活跃，活跃比例为 10%；活跃者中 40 个再次付款，重复付款者比例为 40%。这两个比例的分母不同，不能直接当同一采用指标。

这些数不是 e-CNY 真实数据。题目要的是比注册更直接的使用证据，不足以从单个月活动宣称长期留存或新增社会福利。

**改条件练习与边界**

若期间长度改变，更多累计交易可能只因观察更久；先固定期间再比较。

### 2.13 A13 · 钱包停机不等于货币请求权消失（原卷 p.6）

银行运营的钱包入口停机，公共数字货币底层账本继续运行。区分无法操作与货币余额/请求权消失，不能互相代替。

来源：Practice Exam A p.6，原 Section A 第 13 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 13. Customers access a public digital-money system through a bank-operated wallet. The wallet service goes offline while the underlying ledger continues running. Which response best distinguishes the outage from failure of the monetary claim?
> A. Treat every wallet balance as a realized credit loss because the application cannot currently display it.
> B. Assume all customers can spend normally because the underlying ledger has not stopped.
> C. Conclude that the bank no longer has operational responsibilities once the monetary system is publicly operated.
> D. Check the access and recovery arrangements; a wallet outage alone does not show that the underlying balances have disappeared.

</details>

**⚪ 参考选择：D。**

题面底层账本仍运行，但用户入口停机。运营风险（Operational risk）影响访问/恢复，不自动等于信用损失（Credit loss，即应收资产无法回收）。也不能反过来因为账本还在就声称用户仍能正常支付。

**逐选项判断**

- A 把暂时无法显示直接算全部已实现信用损失，没有证据。
- B 忽略用户入口不可用，不能保证正常花钱。
- C 公共货币系统不消除银行钱包运营责任。
- D 检查访问和恢复安排，且单凭停机不能证明余额消失，正确。

**English reference answer (not official)**

D. Check access and recovery arrangements. A wallet outage may interrupt use without proving that the underlying balances or claims have disappeared.

**停机的两个问题要分开回答**

运营风险（operational risk）关注入口、系统和恢复过程是否正常；信用风险关注债务是否能获履行。入口暂时停机可造成实际不便和交易中断，但尚不能证明全部余额已经损失。

应核备用访问、身份/密钥恢复、银行与底层系统各自职责及对账。题目没说明备用通道存在，不能想当然说人人都可继续支付。

**改条件练习与边界**

如果题目另给资产损失或账本损坏证据，再扩展调查；不能从本题缺信息补出结论。

### 2.14 A14 · 愿意冒险与能够承担损失不同（原卷 p.6）

两客户都表示愿承担投资损失，但一人明年需买房用钱，另一人二十年无短期现金需求。问风险配置应否只看心理意愿。

来源：Practice Exam A p.6，原 Section A 第 14 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 14. Two clients express high willingness to accept investment losses. One needs most of the funds for a house purchase next year; the other has a twenty-year horizon and no near-term cash need. Which response is appropriate?
> A. Distinguish willingness from capacity; the near-term liability can justify lower portfolio risk.
> B. Use the same allocation but rebalance the first client's portfolio more frequently.
> C. Give the same allocation because willingness is the measured risk preference.
> D. Use the lower-fee equity fund for the first client to compensate for the short horizon.

</details>

**⚪ 参考选择：A。**

风险意愿（Risk willingness）是心理上愿不愿接受波动，承受能力（Risk capacity）是损失会不会妨碍现实目标。明年买房要用钱的人，即使愿意承受，若短期跌价也可能无法完成刚性付款；20 年无近期现金需求者的约束不同。

**逐选项判断**

- A 区分两者并考虑近期负债，正确。
- B 相同配置只多调仓不能保证明年资金目标，也可能增加成本。
- C 只按同样意愿配置忽略期限与现金需要。
- D 换低费股票基金不消除短期市场下跌风险，费用节省不能替代期限匹配。

**English reference answer (not official)**

A. Risk willingness and capacity differ. A near-term house-payment obligation can justify a lower-risk allocation even when the client expresses high willingness to accept losses.

**这不是对真实用户的投资建议**

两位客户的心理偏好相同，但明年必须付房款的人若遇短期跌价，可能无法按时履行支出。二十年无近期现金需求者的时间约束不同。配置判断要同时考虑意愿、承受能力、目标与流动性，不是只用一道“敢不敢亏”的问卷。

题目只支持 A 这个原则，不提供每人应买多少股票/债券的唯一比例。更频繁调仓或更低费率不直接消除期限错配。

**改条件练习与边界**

若房款已另存安全流动资金，投资部分约束会不同；题面未给不能擅自假定。

### 2.15 A15 · 制裁筛查同名但生日冲突怎么办（原卷 p.6）

制裁筛查出现同名，但生日不同，证件尚未核。问当前最恰当的下一步，不是让你代银行作真实个案决定。

来源：Practice Exam A p.6，原 Section A 第 15 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 15. A sanctions-screening tool finds an applicant with the same name as a listed person, but the dates of birth differ. The bank has not yet verified identification documents. What is the most appropriate next step?
> A. Reject automatically because name similarity establishes that both records refer to the same person.
> B. Approve automatically because one conflicting field proves the match is false.
> C. Replace the missing identification field with the listed person's document number to complete the record.
> D. Verify additional identifiers and resolve the conflicting evidence before reaching or escalating the screening decision.

</details>

**⚪ 参考选择：D。**

制裁筛查（Sanctions screening）找到的是候选匹配，不是已经证明同一人。一个一致字段不够确认，一个冲突字段也不一定足以排除，尤其证件尚未验证。应核更多可靠标识、记录冲突与处理理由，再决定或交人工升级。

**逐选项判断**

- A 同名直接拒绝，把候选匹配当确认身份。
- B 生日不同直接批准，把一项冲突当绝对排除证据。
- C 拿名单人员证件号填缺失，伪造了申请人的资料，不能做。
- D 验更多标识并解决冲突后作/升级决定，正确。

**English reference answer (not official)**

D. Verify additional identifiers and resolve the conflicting evidence before deciding or escalating the match. Neither name similarity nor one unverified conflicting field is conclusive.

**从候选匹配到身份确认**

同名是一个支持线索，生日冲突是一个反向线索，证件未核是资料缺口。三者应保留而非强行改成一致。下一步核可靠额外标识、来源质量及处理规则，必要时升级人工；不能拿名单人物证件号填申请人空格。

本题没有给具体国家制裁制度和银行流程，所以不写法定冻结期限或保证批准/拒绝。D 是题设下的证据处理步骤，不是实际交易授权。

**改条件练习与边界**

若可靠证件明确属于不同人，可据已核证据排除；本题还未达到该证据条件。

### 2.16 A16 · 按管理资产收费的盈亏平衡（原卷 p.6）

智能投顾每年收固定 AUM 的 0.4%，年度固定成本 60 万美元，变动服务成本为 AUM 的 0.1%。只有这些收入成本，求年度零利润所需 AUM。

来源：Practice Exam A p.6，原 Section A 第 16 题，2.5 分。

<details><summary>完整英文原题及选项/小问</summary>

> 16. A robo-adviser charges 0.4 percent of constant assets under management each year. Annual fixed costs are US\$600,000 and variable servicing costs are 0.1 percent of assets. With no other revenue or costs, what asset level breaks even?
> A. US\$150 million.
> B. US\$200 million.
> C. US\$120 million.
> D. US\$600 million.

</details>

**⚪ 参考选择：B。**

管理资产规模（Assets under management，AUM）记为美元金额 $A$，全年固定且只有题设收入成本。收费每年 $0.004\times A$，变动服务成本 $0.001\times A$，每年固定成本600,000。剩余每元资产贡献0.003，令 $0.003\times A-600,000=0$，得 $A=200,000,000$ 美元，即2亿美元。年度比例与年度成本同期间。

**逐选项判断**

- A 1.5亿美元是只用0.4%除固定成本、漏掉0.1%变动成本。
- B 2亿美元，正确。
- C 1.2亿美元不是题给净贡献率对应值。
- D 6亿美元相当于只用0.1%覆盖固定成本，把成本率误当净收入率。

**English reference answer (not official)**

B. Annual contribution is (0.4% − 0.1%) × AUM = 0.3% × AUM. Setting it equal to US\$600,000 gives break-even AUM of US\$200 million.

**先算每一元 AUM 留下多少**

资产管理规模（assets under management, AUM）是管理的资产金额，不等于公司收入。设其全年不变的美元金额为 $A$；年收费收入是 $0.004\times A$，年度变动成本是 $0.001\times A$，剩下 $0.003\times A$ 才可用于覆盖固定成本。

| 符号/量 | 单位 | 何时已知 | 本题值 |
|---|---|---|---|
| $A$ | 美元资产存量 | 待求全年规模 | 待算 |
| 净贡献率 | 每年每元资产贡献 | 题设费率减成本率 | 0.003/年 |
| 固定成本 | 美元/年 | 已给 | 600,000 |

令年度收入减全部题给成本为零：

$$0.004\times A-0.001\times A-600{,}000=0$$

因此 $A=600{,}000/0.003=200{,}000{,}000$ 美元。回代：年收费 800,000，变动成本 200,000，扣固定 600,000 后为零。题面无获客成本等其他项目，不能自行加进标准数值；真实业务另当别论。

**改条件练习与边界**

若收费降到0.3%但成本不变，净率0.2%，需3亿美元；这是自拟变式而非真实收费。

### 2.17 B1 · 多 PDD、空 JD：假设与回测不能互换（原卷 p.7）

题设借用 Class 1 的买 PDD、空 JD 思路，却明确历史窗口开始于 JD 外卖扩张之前。(a) 说明交易方向和至少一个未消除风险；(b) 解释正回测为何不是该业务事件的因果证据。

来源：Practice Exam A p.7，原 Section B 第 1 题，10 分。

<details><summary>完整英文原题及选项/小问</summary>

> 1. A student considers the Class 1 long-PDD, short-JD trade after discussing JD's food-delivery expansion. The historical illustration starts before that expansion. The student must separate the investment thesis from what the backtest establishes.

> (a) Explain why the business hypothesis suggests buying PDD and selling JD, and identify one risk that the short leg does not eliminate. (5 marks)

> (b) Explain why a positive return over the full historical window does not establish that food-delivery competition caused the result. (5 marks)

</details>

题面先给一个投资想法，又指出历史图开始于外卖扩张以前。long-PDD 是买入 PDD，short-JD 是借到 JD 股票卖出、以后买回归还；多空差不是自动无风险。以下为按题面组织的业务假设，不声称真实竞争已带来某个利润结果。

#### 2.17.1 (a) 中文参考解析

**直接答案**：假设是 JD 扩张外卖的补贴、履约或投入成本可能压低其相对利润/估值，而 PDD 相对少受该项投入负担或在其他业务上更有利。因此用买 PDD、空 JD 表达看好前者相对后者的观点。做空 JD 可对冲部分共同市场/行业变动，但不会消除 PDD 自身经营风险、两家公司不同的市场敏感度或 JD 反而上涨的挤空/借券风险。

**为什么**：多头赚股价上涨，空头赚被卖股票下跌；组合目标是两者相对表现。以 100 元资本为计算基准，买入 50 元 PDD，做空 50 元 JD。若 PDD 跌 20%、JD 只跌 5%，多头亏 10 元，空头赚 2.5 元，净亏 7.5 元，即相对资本亏 7.5%。若另用每条腿 100 元的基准，差额才是 −15%；必须先声明分母。以上是笔记补充，不是原回测。

**English reference answer (not official)**

The thesis is that JD's food-delivery expansion may impose costs or margin pressure relative to PDD, motivating long PDD and short JD. The short leg may offset part of common market exposure but does not remove firm-specific risk, unequal sensitivities, or losses if JD outperforms. This is a hypothesis rather than an established outcome.

#### 2.17.2 (b) 中文参考解析

**直接答案**：全历史窗口正收益不能证明外卖竞争导致收益。图在扩张前已经开始，扩张前的盈利不可能由尚未发生的事件解释；总窗口还混入市场、估值、其他经营新闻及选择窗口的影响。

**怎么查**：先把事件时点与观察窗口对齐，再比较事件前后及合理对照，核是否早已知道并用于形成策略。即使事件后赚钱，也仍需排除其他解释，不能只由同时发生下因果结论。题面未给事件日、逐期收益和对照，不能编一个归因百分比。

**English reference answer (not official)**

A positive full-window backtest does not identify the causal effect of food-delivery competition, especially when the window starts before the expansion. Market movements and other firm news can also drive relative returns. Event timing, appropriate comparisons and information available when the trade was formed are needed before making a causal claim.

**把多空反例按共同分母列出来（笔记补充）**

一行代表一条腿，所有损益相对同一 100 元资本记账，未扣交易/借券成本。

| 腿 | 初始绝对金额 | 股票收益 | 对资本的损益 |
|---|---:|---:|---:|
| 买 PDD | 50 元 | −20% | −10 元 |
| 空 JD | 50 元 | −5% | +2.5 元 |
| 合计 | 毛金额 100 元 | 不直接相加股票收益 | −7.5 元 |

空头在 JD 跌时赚钱，因为以后可较低价格买回所借股票；但它赚 2.5 元，不够抵 PDD 的 10 元损失。相对收益差是 −15 个百分点，乘每边 0.5 权重才是组合收益 −7.5%。

事件因果还要有时间顺序：历史窗口开始→JD 外卖扩张→后续观察。扩张前的收益不可能由“尚未发生的实际竞争”直接造成；若谈预期效应，必须另有当时已知信息证据，题面没给就不补造。

**本题学习总结**

先讲相对业务假设与交易方向，再讲未对冲风险，最后把时间对齐、收益证据与因果证据分开。

### 2.18 B2 · 神经网络选轮数与树的分组单位（原卷 p.8）

给神经网络三个训练轮数及两组损失，并对比按通胀分月份、按规模分同月公司。(a) 选候选时长并给准则；(b) 说清分组单位与经济含义。

来源：Practice Exam A p.8，原 Section B 第 2 题，10 分。

<details><summary>完整英文原题及选项/小问</summary>

> 2. A research team applies nonlinear models to return prediction. It must choose how long to train a neural network and explain why a tree applied to monthly market data differs from one applied to stocks.

> (a) Training losses at epochs 10, 30 and 60 are 0.0030, 0.0020 and 0.0015; validation losses are 0.0032, 0.0024 and 0.0028. Select a duration and explain the criterion. (5 marks)

> (b) One tree splits months by lagged inflation; another splits firms within each month by size. Explain the different economic groupings produced by these splits. (5 marks)

</details>

这题两个小问分别处理模型选择和数据行代表什么。轮次（Epoch）是训练资料被用于更新模型的一轮；训练损失是旧样本贴合程度，验证损失用来选设置，不是最后测试分数。

#### 2.18.1 (a) 中文参考解析

**直接答案：30轮。** 三个候选的验证损失依次为0.0032、0.0024、0.0028，最小值在30轮。训练损失从0.0030降到0.0015，只说明对训练资料贴得更近；到60轮验证损失反而由0.0024升到0.0028，不能因训练值更小就选60。

规则是先用验证集选训练时长，再固定方案，在未参与选择的最终测试上评估。验证最小不保证未来也最好，题面只要求在三个已给候选中选择。

**English reference answer (not official)**

Choose 30 epochs because validation loss is lowest at 0.0024. Training loss keeps falling, but validation loss rises by epoch 60, indicating worse generalization among the given candidates. Fix the duration before final test evaluation.

#### 2.18.2 (b) 中文参考解析

**直接答案**：按滞后通胀（Lagged inflation）分月份，是把不同时点分成宏观状态较高/较低的时间组；按同月企业规模（Size）分股票，是在同一个时点把企业分成大/小等横截面组。前者一行单位是月，后者一行单位是某月的一家公司。

例如门槛通胀2%可把月份分开，规模门槛100亿元可把同月企业分开，两个数仅作笔记补充。滞后表示决策前已可得，不把本月尚未发布通胀偷作输入；组内预测对应各自数据单位，不是前者选企业、后者选历史月份。

**English reference answer (not official)**

A tree splitting months by lagged inflation forms time-series macroeconomic regimes. A tree splitting firms by size within a month forms cross-sectional groups of firms at the same date. The observational unit and economic interpretation differ, and lagged information must be available before prediction.

**先看原始候选值，再读补充图**

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

两种树可以都给叶子内预测，但叶子里放的对象不同。“滞后”要按实际公布日核可得性，不是只把列名写成 lag 就自动没有前视。

**本题学习总结**

选轮数看验证，不看训练单调下降；读树先问一行是月份还是公司，再读分支的经济含义。

### 2.19 B3 · 信用排序尚可却低估违约率（原卷 p.9）

两群组预测违约 1%/4%，同一完整期限实际 3%/7%，原定价使用原预测损失。(a) 分开判断排序与概率校准；(b) 解释定价/利润，并提出一个题面没给的实际结果检查。

来源：Practice Exam A p.9，原 Section B 第 3 题，10 分。

<details><summary>完整英文原题及选项/小问</summary>

> 3. A credit model predicts default rates of 1% and 4% for two borrower groups. Their realized rates over the same complete horizon are 3% and 7%. Pricing used the original predicted losses.

> (a) Assess the model's risk ranking and its calibration. Explain why these are separate assessments. (4 marks)

> (b) Explain how the results affect loan pricing and expected profit. Identify one further outcome that the lender should check before revising expected credit losses. (6 marks)

</details>

两组未来同一完整期限内预测违约1%和4%，实际3%和7%。排序回答哪组较危险；校准（Calibration）回答概率水平与真实比例是否相符，两种任务不能互相替代。

#### 2.19.1 (a) 中文参考解析

**直接答案**：排序在这两个群组层面仍正确，第二组预测4%大于1%，实际7%也大于3%。但校准偏低：第一组少估2个百分点，第二组少估3个百分点。

如果每组100人，预测1/4人、实际3/7人违约的理解小例能看出：即使排对谁危险，仍低估要准备多少损失。100人是解释比例的自拟例，题面没给真实组人数。两组汇总也不能证明每个个体的排序都好。

**English reference answer (not official)**

The model correctly orders the two groups by risk: the second group has both the higher prediction and realized default rate. It is undercalibrated, underpredicting default by 2 and 3 percentage points. Correct ordering does not establish accurate probability levels.

#### 2.19.2 (b) 中文参考解析

**直接答案**：若其他条件不变，按原低概率定价会低估预期信用损失，可能收费不足，使利润低于原预计。应查违约后净回收/违约损失率（Loss given default，LGD），这是题目已给实际违约率以外的重要结果；不能只重复“查违约率”。

预期损失的简化关系为 $EL=PD\times LGD\times EAD$：PD是所定期限违约概率，LGD是违约条件下损失比例，EAD是违约时敞口金额。实际违约率更高并不唯一确定EL变多少，回收、敞口和时点也可能改变。因此先核可比群组与实际回收再修估计/价格，不直接把3%或7%当损失金额比例。

**English reference answer (not official)**

Underpredicted default can make the original loan price too low and reduce expected profit, other things equal. Before revising expected credit losses, check realized recoveries or loss given default, along with comparable exposures. Default frequency alone does not determine the monetary loss because severity and exposure also matter.

**违约频率不是损失率**

违约概率（probability of default, PD）是所定期限内违约的可能性；违约损失率（loss given default, LGD）是已经违约时有多少金额最终收不回；违约时敞口（exposure at default, EAD）是届时面临损失的金额。预期损失（expected loss, EL）的单期简化关系为 $EL=PD\times LGD\times EAD$。

| 量 | 单位 | 何时/条件 | 本题是否给数 |
|---|---|---|---|
| PD | 概率/比例 | 定价时的预测期限 | 给两组预测及事后频率 |
| LGD | 条件损失比例 | 违约后扣回收的结果 | 未给 |
| EAD | 货币金额 | 违约时的敞口 | 未给 |
| EL | 同币种金额 | 所定期限的预期损失 | 不能从频率单独算出 |

例如固定 EAD 为 1,000 元、LGD 为 50%，PD 从 1% 改 3%，EL 从 5 元变 15 元。这只是笔记补充的同条件例，不能把真实群组的 LGD、敞口假定成这些数。

两组汇总只支持本题的群组排序一致和两个点的低估。没有组人数/抽样模型，不能计算置信区间，也不能判定所有个体排序或全概率区间校准都好。完整期限减少未到期截尾问题，不自动给出净回收、折现和处置成本。

**本题学习总结**

先分排序/概率，再从概率走到PD×LGD×敞口；新增检查必须超出题面已经给出的违约率。

### 2.20 B4 · 共享发票登记不能替代实物与偿还证据（原卷 p.10）

同一应收款找两银行融资，平台登记文件和未偿融资，但只有参与银行可更新各自贷款。(a) 计算 80% 总垫款上限下的剩余额度并说要什么记录；(b) 区分文件没变、真实交货和还款能力。

来源：Practice Exam A p.10，原 Section B 第 4 题，10 分。

<details><summary>完整英文原题及选项/小问</summary>

> 4. An exporter uses the same receivable when approaching two banks. A shared platform records verified documents and outstanding financing, but only participating banks can update their loans. Bank B must decide whether to lend.

> (a) The receivable is RMB2 million, Bank A has lent RMB1.3 million and the aggregate advance cap is 80%. Calculate Bank B's remaining capacity and state what record it needs. (5 marks)

> (b) Explain why an unchanged invoice file does not prove that goods were delivered or that the borrower can repay. What should Bank B verify before approving the loan? (5 marks)

</details>

出口商用同一应收款接洽两银行，平台记录核验文件和现有融资，但只有参与银行能更新各自贷款。这一权限安排提供来源责任，同时留下非参与者或未及时更新资料的完整性风险。

#### 2.20.1 (a) 中文参考解析

**直接答案**：总上限为人民币 $2,000,000\times80\%=1,600,000$，扣A已有1,300,000，余 $300,000$ 元。它是完整记录条件下的最大剩余额度，不是自动批准数额。

B需要同一应收款的最新全部未偿融资、A贷款余额、更新时点和负责机构，核A的130万是否仍准确，以及非参与银行的融资是否漏记。only participating banks can update 只说明写入者，不证明融资只可能来自参与银行；若无法确认完整，30万是条件计算，不是可靠可贷保证。

**English reference answer (not official)**

The remaining capacity is RMB2 million × 80% − RMB1.3 million = RMB300,000, assuming complete and current financing records. Bank B needs the latest outstanding financing against the same receivable, including update responsibility and checks for financing outside participating banks.

#### 2.20.2 (b) 中文参考解析

**直接答案**：文件未改变只支持“该记录与原存档一致”，不证明原文件真实、货已交付或买方有钱偿还。B应核合同/发票与交付验收证据、向买方确认应付金额和到期日、债权所有权与争议、全部已有融资，并评估还款现金流和信用风险。

可按三层复查：记录层核真伪和更新，业务层核发货/验收/应付确认，信用层核实际偿还能力。即使三层都通过，也不保证未来绝不违约；题面没有合同价格、实际物流或财务数据，不能代作肯定事实。

**English reference answer (not official)**

An unchanged file shows record integrity, not necessarily genuine delivery or repayment capacity. Bank B should verify the underlying contract, delivery and acceptance, buyer confirmation, ownership and existing financing, and the relevant repayment cash flows before approval.

**剩余额度与批准分成两步**

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

即使文件哈希一致，也可能把最初的假发票原样保存。不可篡改不等于初始输入真实，更不保证买方未来有钱。

**本题学习总结**

先按完整输入算最多30万，再核记录是否全、业务是否真、债务能否还；不把写权限或哈希当现实真相。

### 2.21 C1 · 四个月样本外误差与MA12基准（原卷 p.11）

四个月测试，题面保证预测只用先前资料，MA12 为此前 12 个月收益的平均。(a) 两种预测逐月求平方误差再加总；(b) 计算相对 MA12 的样本外决定系数，并回答能否证明投资盈利。

来源：Practice Exam A p.11，原 Section C 第 1 题，10 分。

<details><summary>完整英文原题及选项/小问</summary>

> 1. A monthly market-return model is tested over four months. Forecasts use only prior information; MA12 averages the preceding twelve monthly returns. Using the decimal returns below, compare squared forecast errors and assess the model's performance.
>
> | Month | 1 | 2 | 3 | 4 |
> |---|---:|---:|---:|---:|
> | Realized return | 0.03 | -0.01 | 0.02 | -0.02 |
> | Model forecast | 0.02 | 0.00 | 0.01 | -0.01 |
> | MA12 forecast | 0.01 | 0.01 | 0.01 | 0.01 |
>
> (a) Calculate the model and MA12 sums of squared errors. (4 marks)
>
> (b) Calculate OOS R-squared relative to MA12 and interpret it. Does the result establish investment profitability? An exact fraction is acceptable. (6 marks)

</details>

本题收益以小数给出，0.03是3%而非0.03%。MA12是只用此前12个月收益算的移动平均（Moving average），题面保证预测使用过去信息。比较同一4个月、相同目标和同一误差定义，不能换样本或改成训练拟合。

#### 2.21.1 (a) 中文参考解析

**直接答案**：模型SSE为0.0004，MA12为0.0018，单位均为小数收益的平方。

先逐月算误差（真实收益减预测），再平方。每行代表一个测试月份，列出两个预测各自误差，负误差平方后也为正：

| 月 | 模型误差 | 模型平方 | MA12误差 | MA12平方 |
|---|---:|---:|---:|---:|
| 1 | 0.01 | 0.0001 | 0.02 | 0.0004 |
| 2 | −0.01 | 0.0001 | −0.02 | 0.0004 |
| 3 | 0.01 | 0.0001 | 0.01 | 0.0001 |
| 4 | −0.01 | 0.0001 | −0.03 | 0.0009 |

例如第4月真实−0.02减MA12的0.01，误差为−0.03，平方0.0009。模型4项相加0.0004；MA12四项相加0.0018。不能先把正负误差抵销再平方，那会漏掉预测错误。

**English reference answer (not official)**

The model's four squared errors are each 0.0001, giving SSE = 0.0004. MA12 squared errors are 0.0004, 0.0004, 0.0001 and 0.0009, giving SSE = 0.0018, in squared decimal-return units.

#### 2.21.2 (b) 中文参考解析

**直接答案**：相对基准的样本外决定系数为 $R^2_{OOS}=1-SSE_{model}/SSE_{MA12}=1-0.0004/0.0018=7/9\approx77.78\%$。分母是本题MA12在同4个月的SSE，不是收益本身的方差；正值表示模型在这4个月的平方误差比MA12低约77.78%。

这不证明投资盈利：题目没有把预测变成什么持仓、承担多大风险、换手和费用，也只有4个月，不能据此宣称统计显著或长期稳定。评估预测错误与评估可交易净收益是两项任务。

改条件的笔记小例：模型SSE若等于0.0018，指标为0；若大于基准则为负。它可以为负，不必强行放在0到1。

**English reference answer (not official)**

OOS R-squared is 1 − 0.0004/0.0018 = 7/9, about 77.78%. The model has lower squared forecast error than MA12 over these four months. This does not establish investment profitability without a trading rule, risk and transaction-cost analysis, or evidence over a sufficiently informative sample.

**符号、单位与一个月的演算入口**

令 $r_t$ 为测试月 $t$ 的实现收益，$\widehat r_t$ 为模型对该月的预测，$b_t$ 为 MA12 预测。三者均是月收益小数：0.03 表示 3%；$t$ 在这里是月份编号，不是检验统计量。预测在该月收益实现之前可用，实现收益在该月结束后才知道。

模型误差 $e_t=r_t-\widehat r_t$；平方使正负偏差都计为错误，再加总 $\mathrm{SSE}=\sum_{t=1}^{4}e_t^2$。第 4 月模型误差是 $-0.02-(-0.01)=-0.01$，平方 0.0001；MA12 误差是 $-0.02-0.01=-0.03$，平方 0.0009。

样本外决定系数（out-of-sample R-squared）问“相对题设基准，平方误差减少了多少比例”：

$$R^2_{\mathrm{OOS}}=1-\frac{\mathrm{SSE}_{\rm model}}{\mathrm{SSE}_{\rm MA12}}.$$

分母非零才有定义。本题分母为正；若基准误差恰为零，不能继续除以零并强报一个分数。正 77.78% 不是投资回报 77.78%，也不是预测对了 77.78% 的月份。

题面已经给 MA12 的四个预测值，因此无需额外 12 个月原始收益才能完成本题。没有回测持仓规则、费用和风险，才是无法证明盈利的真正缺口，不是计算 SSE 的缺口。

**本题学习总结**

收益统一小数→逐月差→逐月平方→各自加总→相对同基准；预测改善不自动变成利润。

### 2.22 C2 · BNPL交易量不变而贡献可转负（原卷 p.12）

假想先买后付提供者为 2,000 港元购买垫款，从商户扣 4% 费，客户无息还本金。(a) 算费用、商户实收及扣三类成本后的贡献；(b) 只把预期损失从 30 改 55，重算并解释交易量不变为何仍亏。

来源：Practice Exam A p.12，原 Section C 第 2 题，10 分。

<details><summary>完整英文原题及选项/小问</summary>

> 2. A hypothetical BNPL provider finances a HK\$2,000 purchase and deducts a 4% merchant fee. The customer repays principal without interest. Funding, expected credit losses and servicing cost HK\$18, HK\$30 and HK\$12 respectively. Ignore overhead and tax.

> (a) Calculate the merchant fee, the merchant's net payout and the provider's expected contribution after the stated costs. (5 marks)

> (b) Expected credit losses rise to HK\$55; all other amounts stay unchanged. Recalculate contribution and explain why unchanged purchase volume does not preserve profitability. (5 marks)

</details>

购买额HK\$2,000、商户费4%，客户只还本金无利息；资金、预期信用损失、服务成本分别为HK\$18、30、12。ignore overhead and tax表示只算题给成本后的贡献，不算公司最终税后利润。

#### 2.22.1 (a) 中文参考解析

**直接答案**：商户费80港元；商户净拨款1,920港元；提供者预期贡献20港元。

逐项追资金：费用为 $2,000\times4\%=80$ 港元，商户收到 $2,000-80=1,920$。提供者从这笔交易得到的收费收入是80，不是整笔2,000；再扣资金18、预期损失30和服务12，贡献为 $80-18-30-12=20$ 港元。

客户偿还本金是回收先提供的资金，不再把同一2,000当额外利润；若那样算会重复计算。顾客免息没有消除提供者垫款与违约成本。

**English reference answer (not official)**

The merchant fee is HK\$80 and the merchant's net payout is HK\$1,920. Expected contribution is HK\$80 − HK\$18 − HK\$30 − HK\$12 = HK\$20, ignoring overhead and tax.

#### 2.22.2 (b) 中文参考解析

**直接答案**：预期信用损失改为55港元，贡献 $80-18-55-12=-5$ 港元。其余输入固定，损失比原来多25，恰使原20贡献下降到−5。

购买额与收费率不变只能保持80收入，并不保持扣成本后的结果。新增交易如果每笔都沿这个负贡献条件，更多量可能扩大损失。零贡献对应损失为 $80-18-12=50$ 港元（笔记补充），不是平台整个业务税后盈亏平衡。

**English reference answer (not official)**

Expected contribution becomes HK\$80 − HK\$18 − HK\$55 − HK\$12 = −HK\$5. Unchanged purchase volume keeps the fee revenue unchanged but does not offset the higher expected credit loss. Profitability therefore deteriorates despite unchanged transaction value.

**按一笔交易追收入，而不是把本金算两次**

先买后付（buy now, pay later, BNPL）在题设中让客户无息偿还购买本金，提供者靠商户费获得这项收入。商户原应收 2,000，扣费 80 后实得 1,920；提供者未来收回客户本金，不等于又赚了整笔 2,000。

| 本笔交易的量 | 金额（港元） | 是否收入/成本 |
|---|---:|---|
| 购买本金 | 2,000 | 交易规模，不全是收入 |
| 扣留商户费 | 80 | 本题收费收入 |
| 商户净拨款 | 1,920 | 商户实收，不是额外收入 |
| 资金/预期损失/服务 | 18/30/12 | 三项题设成本 |
| 原预期贡献 | 20 | 收费减三项成本 |

这里的贡献（contribution）指只扣题设成本后的余额，未扣总部固定费用和税，不等于公司净利润。客户免息不代表提供者没有资金成本；预期损失是估计的平均损失，不是说每笔交易必定恰亏 30。

改为损失 55，费用和其他成本固定，所以贡献只会比原来少 25，20 变 −5。不能为保住原利润偷改收费率，也不能把新增 25 又重复扣两次。

**本题学习总结**

交易额、收费收入、净拨款与预期贡献四个量分开；改一项成本只重算该路径，不偷改其他输入。

## 3. 一图看懂 · 全卷的六条判断链

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
| A1 | B | [[#2.1 A1 · Ridge 怎样稳定相关变量的系数（原卷 p.2）\|A1解析]] |
| A2 | C | [[#2.2 A2 · 嵌套 OLS 的训练误差为何不会增加（原卷 p.2）\|A2解析]] |
| A3 | C | [[#2.3 A3 · PCR 与 PLS 在构造成分时用什么（原卷 p.2）\|A3解析]] |
| A4 | C | [[#2.4 A4 · Alpha 与 Beta 的水平和变化分开算（原卷 p.3）\|A4解析]] |
| A5 | B | [[#2.5 A5 · 双边换手成本与周夏普比率（原卷 p.3）\|A5解析]] |
| A6 | D | [[#2.6 A6 · 总敞口和净敞口分别加减（原卷 p.3）\|A6解析]] |
| A7 | A | [[#2.7 A7 · 链上有资产不等于客户能完整取回（原卷 p.4）\|A7解析]] |
| A8 | B | [[#2.8 A8 · 共享分叉前历史不等于以后同链（原卷 p.4）\|A8解析]] |
| A9 | C | [[#2.9 A9 · 代币化基金的收益从哪里来（原卷 p.4）\|A9解析]] |
| A10 | A | [[#2.10 A10 · NFT 的代币、媒体和使用权三层（原卷 p.5）\|A10解析]] |
| A11 | D | [[#2.11 A11 · 界面相似时看谁承担货币负债（原卷 p.5）\|A11解析]] |
| A12 | A | [[#2.12 A12 · 开户量与真实支付采用分开（原卷 p.5）\|A12解析]] |
| A13 | D | [[#2.13 A13 · 钱包停机不等于货币请求权消失（原卷 p.6）\|A13解析]] |
| A14 | A | [[#2.14 A14 · 愿意冒险与能够承担损失不同（原卷 p.6）\|A14解析]] |
| A15 | D | [[#2.15 A15 · 制裁筛查同名但生日冲突怎么办（原卷 p.6）\|A15解析]] |
| A16 | B | [[#2.16 A16 · 按管理资产收费的盈亏平衡（原卷 p.6）\|A16解析]] |
| B1(a) | 相对业务假设支撑方向，仍有未对冲风险 | [[#2.17 B1 · 多 PDD、空 JD：假设与回测不能互换（原卷 p.7）\|B1解析]] |
| B1(b) | 全历史窗口正收益不足以证明因果 | [[#2.17 B1 · 多 PDD、空 JD：假设与回测不能互换（原卷 p.7）\|B1解析]] |
| B2(a) | 三个候选中选30轮 | [[#2.18 B2 · 神经网络选轮数与树的分组单位（原卷 p.8）\|B2解析]] |
| B2(b) | 月份宏观状态组与同月公司截面组 | [[#2.18 B2 · 神经网络选轮数与树的分组单位（原卷 p.8）\|B2解析]] |
| B3(a) | 群组排序一致，概率低估2/3个百分点 | [[#2.19 B3 · 信用排序尚可却低估违约率（原卷 p.9）\|B3解析]] |
| B3(b) | 原定价可能不足，另查回收或LGD | [[#2.19 B3 · 信用排序尚可却低估违约率（原卷 p.9）\|B3解析]] |
| B4(a) | 条件剩余额度为人民币300,000 | [[#2.20 B4 · 共享发票登记不能替代实物与偿还证据（原卷 p.10）\|B4解析]] |
| B4(b) | 文件完整不保证交付或偿还 | [[#2.20 B4 · 共享发票登记不能替代实物与偿还证据（原卷 p.10）\|B4解析]] |
| C1(a) | 模型/MA12的SSE为0.0004/0.0018 | [[#2.21 C1 · 四个月样本外误差与MA12基准（原卷 p.11）\|C1解析]] |
| C1(b) | OOS R²=7/9≈77.78%，不证明盈利 | [[#2.21 C1 · 四个月样本外误差与MA12基准（原卷 p.11）\|C1解析]] |
| C2(a) | 费80、拨款1920、贡献20港元 | [[#2.22 C2 · BNPL交易量不变而贡献可转负（原卷 p.12）\|C2解析]] |
| C2(b) | 预期贡献变为−5港元 | [[#2.22 C2 · BNPL交易量不变而贡献可转负（原卷 p.12）\|C2解析]] |

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
| 1 | 封面/考试情境 | [[#1.1 原封面怎么读（p.1）\|封面解析]] | 文字要求完整保留，未代填个人资料 |
| 2 | A1、A2、A3 | [[#2.1 A1 · Ridge 怎样稳定相关变量的系数（原卷 p.2）\|A1]] / [[#2.2 A2 · 嵌套 OLS 的训练误差为何不会增加（原卷 p.2）\|A2]] / [[#2.3 A3 · PCR 与 PLS 在构造成分时用什么（原卷 p.2）\|A3]] | 文字题，无教学原图；不复制答题留白 |
| 3 | A4、A5、A6 | [[#2.4 A4 · Alpha 与 Beta 的水平和变化分开算（原卷 p.3）\|A4]] / [[#2.5 A5 · 双边换手成本与周夏普比率（原卷 p.3）\|A5]] / [[#2.6 A6 · 总敞口和净敞口分别加减（原卷 p.3）\|A6]] | 文字题，无教学原图；不复制答题留白 |
| 4 | A7、A8、A9 | [[#2.7 A7 · 链上有资产不等于客户能完整取回（原卷 p.4）\|A7]] / [[#2.8 A8 · 共享分叉前历史不等于以后同链（原卷 p.4）\|A8]] / [[#2.9 A9 · 代币化基金的收益从哪里来（原卷 p.4）\|A9]] | 文字题，无教学原图；不复制答题留白 |
| 5 | A10、A11、A12 | [[#2.10 A10 · NFT 的代币、媒体和使用权三层（原卷 p.5）\|A10]] / [[#2.11 A11 · 界面相似时看谁承担货币负债（原卷 p.5）\|A11]] / [[#2.12 A12 · 开户量与真实支付采用分开（原卷 p.5）\|A12]] | 文字题，无教学原图；不复制答题留白 |
| 6 | A13、A14、A15、A16 | [[#2.13 A13 · 钱包停机不等于货币请求权消失（原卷 p.6）\|A13]] / [[#2.14 A14 · 愿意冒险与能够承担损失不同（原卷 p.6）\|A14]] / [[#2.15 A15 · 制裁筛查同名但生日冲突怎么办（原卷 p.6）\|A15]] / [[#2.16 A16 · 按管理资产收费的盈亏平衡（原卷 p.6）\|A16]] | 文字题，无教学原图；不复制答题留白 |
| 7 | B1 | [[#2.17 B1 · 多 PDD、空 JD：假设与回测不能互换（原卷 p.7）\|B1]] | 文字题，无教学原图；不复制答题留白 |
| 8 | B2 | [[#2.18 B2 · 神经网络选轮数与树的分组单位（原卷 p.8）\|B2]] | 文字题，无教学原图；不复制答题留白 |
| 9 | B3 | [[#2.19 B3 · 信用排序尚可却低估违约率（原卷 p.9）\|B3]] | 文字题，无教学原图；不复制答题留白 |
| 10 | B4 | [[#2.20 B4 · 共享发票登记不能替代实物与偿还证据（原卷 p.10）\|B4]] | 文字题，无教学原图；不复制答题留白 |
| 11 | C1 | [[#2.21 C1 · 四个月样本外误差与MA12基准（原卷 p.11）\|C1]] | C1原数字表完整转写 |
| 12 | C2 | [[#2.22 C2 · BNPL交易量不变而贡献可转负（原卷 p.12）\|C2]] | 文字题，无教学原图；不复制答题留白 |
| 13 | SCRAP PAPER | [[#1.2 怎样使用这份学习稿\|空白页说明]] | 纯草稿，无漏题或教学图 |
| 14 | SCRAP PAPER | [[#1.2 怎样使用这份学习稿\|空白页说明]] | 纯草稿，无漏题或教学图 |

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
