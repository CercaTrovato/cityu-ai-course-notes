---
course: IS6400
module: Sample Final
type: 学习解析
source: Sample Final.docx（Canvas 2026-11-18 归档）
transcript: none
status: draft
learning_status: 参考解析候选，待独立审查
official_solution: 未取得，不能视为官方答案
readability_rules: v2
teaching_standard: novice-v1
updated: 2026-11-19
---

# IS6400 Sample Final：原题、中英参考作答与逐步复做

## 0. 先知道这份材料能回答什么

这是一份样卷学习解析，不是教师官方解答，也不是待提交学生答卷。本文保留取得的全部英文题面，再解释怎样判断、怎样计算，以及怎样用英文表达。

| 实际原题 | 你要完成的动作 | 当前能得到什么 |
|---|---|---|
| Question 1，两个小问 | 数 `Churn` 缺失记录，说明两种处理方法；计算交易额四分位距 | 方法、计算口径与可执行程序；缺原始 Excel，不能报两个数值结果 |
| Problem 3，四个小问 | 树误差计算与剪枝比较，以及模型设置 | 可从原图全部复算，含 9 种子树模型 |
| Question 5，三个小问 | 变量处理、五日预测和滚动验证设计 | 理由、程序及评估设计均提供；五天价格因缺 CSV 受阻 |

原文件的编号不连续：取得的正文只有 Question 1、Problem 3、Question 5。Question 1 题头写 20 分，但所见两小问只合计 7 分。不能因此自行补出不存在的小问。图中和正文中的题号、表号也不一致，见 §9。

建议第一次按 §2.1 → §2.2 → §2.3 顺读；复习时用 §4 和 §7。原题中 `keep two decimal places` 要求统计结果和预测价保留两位小数。计数的本质仍是整数，例如发现 5 条应理解为 5 条，而不是 5.00 条不同的记录。

## 1. 开始之前：一行数据、一个模型和一次评估

Question 1 中，一行（record / row）是一条客户记录，一列（variable）是一类信息，例如年龄。不能把某个客户的 6 列都算成 6 条客户记录。

Problem 3 的表格不是“一行一个人”。它把相同 A、B、C、D 的实例合并了。一行的正类数（Number of + instances）与负类数（Number of - instances）才告诉你代表多少实例。例如第一条训练行代表 4 个正类实例，不是 1 个实例。

训练集（training set）用于生成或拟合模型。验证集（validation set）用于比较已经拟合好的候选模型，模拟它遇到其他记录时的表现。把验证答案倒灌进去修改叶子标签，再计算同一批数据的成绩，会把评估变成“先看答案再考试”。

Question 5 的一行是一日的价格，顺序不能随机打散。预测明天时，只能使用今天以及以前已知的价格。

## 2. 按原题逐问复做

### 2.1 Question 1：客户缺失值与交易额分散程度

先分清两个任务：第 1 问只查 `Churn` 这一列缺了多少行；第 2 问只用 `LastTransaction` 计算中间 50% 金额跨度。不要先把 `Churn` 缺失客户删掉，再回答“all the customers”的交易额问题。

英文原题（完整保留取得内容）：

> Final. Exam. Sample
>
> Question 1 (20 points)
>
> A telecommunication company wants to investigate the customer churn phenomenon. Customer churn occurs when customers stop doing business with a company. The telecommunication company has collected some data. Please check the data file Q1.xlsx. The major variables are defined below:
>
> - Name: customer’s name,
> - Gender: a customer’s gender,
> - Age: a customer’s age when the data was collected,
> - Payment Method: the method a customer paid the bill,
> - Churn: churn status,
> - LastTransaction: the amount a customer paid for his/her last transaction.
>
> The company wants to perform some descriptive analytics and needs your help. Please answer the following questions (keep two decimal places):
>
> 1) In total, how many records (rows) have missing value in the variable “Churn”? Please provide two methods to process missing values. (4 points)
>
> 2) Among all the customers, what is the interquartile range (IQR) of last transaction? (3 points)

#### 2.1.1 第 1 问：缺了几行，不是所有列总共缺几格

客户流失（customer churn）指客户停止与公司做生意。`Churn` 是流失状态，不是最近一次交易额；金额大或小都不能直接代替流失标签。

缺失值（missing value）表示该条记录的此项信息没有被记录。先读 `Churn`，给每行一个“缺/不缺”的判断，再把“缺”的个数相加。例如 4 行为 `Yes`、空白、`No`、空白，就数到 2，不是 4。

当前缺少 `Q1.xlsx`，因此无法知道样卷数据的准确缺失行数。不能把下面的教学例子 2 当成原题答案。数据到手后可以按以下顺序操作：

1. 用 Excel 打开原始文件，确认工作表、表头与实际记录范围，排除空白整行或脚注。
2. 筛选 `Churn` 的空白项，数剩余真实客户行。不要用“空白格占比”代替“缺失行数”。
3. 若单元格只有空格，先确认它也应按缺失处理。`NA`、`Unknown` 等文字是否表示缺失，应核数据说明，不是看到不熟悉的标签就删掉。
4. 保留原表，另建分析副本。先报告原始缺失数量，再说明是否处理。

可以回答的两种常见处理方法如下，适用边界也属于答案的一部分。

| 方法 | 实际动作 | 本题中要注意什么 |
|---|---|---|
| 删除缺失记录（listwise deletion） | 分析需要真实 `Churn` 标签时，不纳入该列缺失的客户 | 会减少样本；若流失客户更容易漏记，删除可能使流失率偏低 |
| 填补（imputation） | 类别列可用已观察到的众数，即出现次数最多的类别填补 | 这是估计，不是找回真实标签；会夸大多数类，不宜把虚构的流失标签当真实监督答案 |

因此，“提供两种方法”可以写删除和众数填补，但不能进一步声称众数填补必定适合这家公司的目标。若只是描述资料完整性，可以保留“未知”类别并单独报告；若后续训练客户流失分类器，应优先从原系统补回真实标签，或剔除无法确认的训练标签，而不是随意填 `No`。

英文参考作答（笔记自拟，数值部分受阻）：

> The number of records with a missing Churn value cannot be determined without Q1.xlsx. Two common treatments are deleting records with missing values and imputing a categorical variable with its observed mode. Deletion reduces the sample and may introduce selection bias. Mode imputation changes the class distribution and should not be treated as a recovery of the true churn labels.

#### 2.1.2 第 2 问：IQR 是两个分位数相减

把所有有效最近交易额从小到大排序。第一四分位数（first quartile，$Q_1$）是 25% 分位点，第三四分位数（third quartile，$Q_3$）是 75% 分位点。四分位距（interquartile range，IQR）衡量中间 50% 数据的跨度，不是最大金额减最小金额。

$$
\mathrm{IQR}=Q_3-Q_1.
$$

这里两个 $Q$ 都是金额，IQR 也用相同金额单位。原题未说明币种，所以不能擅自标美元或港币。

笔记补充小例：假设金额排序后是 10、20、30、40、50。采用含端点的线性插值口径时，$Q_1=20$、$Q_3=40$，所以 IQR 为 $40-20=20$。这是方法演示，不是原题数据。

不同软件的四分位数约定可能给出不同结果，特别是小样本。本解析事先采用 Excel `QUARTILE.INC` / pandas 线性插值口径。

若有 $n$ 个排序值，分位点 $p$ 的零起点位置为 $(n-1)p$。位置落在两个观测之间，就按距离在它们之间插值。

例如 10、20、30、40，25% 位置是 $3\times0.25=0.75$，所以 $Q_1=10+0.75(20-10)=17.50$。75% 位置是 2.25，所以 $Q_3=30+0.25(40-30)=32.50$，IQR 为 15.00。

Excel 操作：把实际数据区的 `LastTransaction` 一列作为同一个范围，分别用 `=QUARTILE.INC(范围,1)` 和 `=QUARTILE.INC(范围,3)`，再用后者减前者。`范围` 是需要替换的说明文字，不能原样键入；若金额在 F2:F101，就替换为 `F2:F101`。只用有效数值；若金额也有缺失，要报告用了多少条有效金额，不能无声补 0。

英文参考作答（笔记自拟，数值部分受阻）：

> The IQR is the 75th percentile of LastTransaction minus its 25th percentile, in the same monetary unit as LastTransaction. I would use all non-missing numeric LastTransaction values, independently of whether Churn is observed, and report the quartile convention. The numerical IQR cannot be calculated without Q1.xlsx.

#### 2.1.3 用真实 Excel 运行，不制造输出

配套程序是同目录的 `reproduce.py`。在终端执行下列命令，最后一个路径改成真正拿到的原始 Excel 路径。

```powershell
& D:\anaconda3\python.exe -X utf8 .\reproduce.py --q1 '实际目录\Q1.xlsx'
```

这一入口用 `pd.read_excel` 读表，用 `df['Churn']` 取一列，`.isna()` 为每行生成缺失判断，`.sum()` 把判断为真的行相加。它把纯空格视为缺失；pandas 默认识别的空值标记也会被视为缺失，实际数据说明若把其中某个文本定义为合法类别，需先调整读取口径。

`pd.to_numeric` 把交易额检查为数字。不能转换的非空文字会触发错误，请先查看原值，不能把它们假装成 0。程序计算 `quantile(.25)`、`quantile(.75)`，保留未舍入数值再相减。输出 `missing_churn` 回答第 1 问，`IQR` 回答第 2 问，`valid_LastTransaction` 是后者的有效分母。

程序不会修改 Excel。此处没有运行原题数据，也没有伪造一张“计算结果”截图。

### 2.2 Problem 3：先沿树预测，再按实例数计错

本题的关键不是再训练一棵树，而是按照给定树处理表中的记录。随后才剪去局部分支，比较“背熟训练样本”与“预测另一批实例”有什么区别。

英文原题（含所有四个小问）：

> Problem 3 Decision Tree (20 points).
>
> Consider the decision tree shown in Figure 1below, and the corresponding training and validation sets in Tables 1 and 2 respectively.
>
> (1) Estimate the error rate of the tree using both the training error and the pessimistic error considering model complexity. While computing the error with pessimistic approach, to account for model complexity, use a penalty value of 1 to each leaf node. (2 points)
>
> (2) Compute the validation error of the tree using the validation set shown in Table 2. (2 points)
>
> (3) Comment on the behavior of training and validation set errors with respect to model complexity by evaluating the pruned tree models. (8 points)
>
> (4) Which library can be used for implementing a decision tree model? Please write down the code for model importing and model setting for a decision tree of maximum 8 layers. (8 points)

源文件正文图注：`Figure 1 Decision Tree structure for Question 2`。图内另印 `Figure 1: Decision tree for Exercise 2.`，二者都不是本题标题的 Problem 3，原文保留，不按这个错位另造一题。

![Sample Final 原始决策树：根 A，左 B-C-D，右 B](../media/media/image1.png)

源文件正文表注：`Table 1 Training Dataset`。嵌入图片内印 `Table 2: Training set for Problem 2`。

![Sample Final 原始训练表](../media/media/image2.png)

源文件正文表注：`Table 2 Validation Dataset`。嵌入图片内印 `Table 3: Test set for Problem 2`。本解析按正文实际提问把它作为验证集，不把 “Test” 这个图片旧标题当成一个额外、未参与选模的测试集。

![Sample Final 原始验证表，图片内部旧标题 Test set](../media/media/image3.png)

#### 2.2.1 先读懂节点与计数表

决策树（decision tree）的圆圈表示检查哪一列，箭头上的 0、1 表示取哪条路径。方框表示已经做出预测的叶节点（leaf node）；`+`、`-` 是类别，不是本题误差的加减号。到叶子就停，后面没有检查的变量不再影响预测。

A、B、C、D 是四个取值为 0 或 1 的输入特征，原件没有说明它们的业务含义。后文 `A0` 简写 A=0，`B1` 简写 B=1。表中 T1–T6 是训练行编号，V1–V6 是验证行编号；这些编号帮助定位原表，不是额外特征。

从 A 开始读图：

- 若 A=1，再看右边 B。B=0 预测 `+`，B=1 预测 `-`。
- 若 A=0，进入左边 B。B=1 预测 `-`；B=0 才检查 C。
- 在左侧 C，C=1 预测 `-`；C=0 才检查 D。
- 在 D，D=0 预测 `+`，D=1 预测 `-`。

例如验证第 2 行 A=0、B=0、C=1、D=1：依次走 A 的 0 分支、B 的 0 分支、C 的 1 分支，到 `-` 就停止。D=1 根本没被使用。这行有 3 个实际 `+`，所以造成 3 次错误，不是 1 次。

下面忠实转录两张源表。每行最后两列分别是真实正类和真实负类的实例数量。

| 训练行 | A | B | C | D | 正类数 | 负类数 |
|---:|---:|---:|---:|---:|---:|---:|
| T1 | 0 | 0 | 0 | 0 | 4 | 0 |
| T2 | 0 | 0 | 0 | 1 | 0 | 1 |
| T3 | 0 | 0 | 1 | 0 | 0 | 1 |
| T4 | 0 | 1 | 0 | 1 | 0 | 1 |
| T5 | 1 | 0 | 1 | 0 | 3 | 0 |
| T6 | 1 | 1 | 0 | 1 | 0 | 5 |

训练总实例数是 $4+1+1+1+3+5=15$，其中正类 7，负类 8。不能用“表只有 6 行”把误差分母写成 6。

| 验证行 | A | B | C | D | 正类数 | 负类数 |
|---:|---:|---:|---:|---:|---:|---:|
| V1 | 0 | 0 | 0 | 1 | 4 | 0 |
| V2 | 0 | 0 | 1 | 1 | 3 | 0 |
| V3 | 0 | 1 | 0 | 0 | 0 | 1 |
| V4 | 0 | 1 | 1 | 0 | 0 | 2 |
| V5 | 1 | 0 | 0 | 0 | 2 | 0 |
| V6 | 1 | 0 | 0 | 1 | 3 | 0 |

验证总实例数也是 $4+3+1+2+2+3=15$，其中正类 12，负类 3。两个集合碰巧同样大，不意味着它们的类别分布相同。

#### 2.2.2 第 1 问：训练误差为零，但复杂性惩罚不为零

先逐行用原树预测。表中“错数”按该行所代表的全部实例计算。

| 训练行 | 到达叶子的路径 | 预测 | 实际类别及数量 | 错数 |
|---|---|---|---|---:|
| T1 | A0 → B0 → C0 → D0 | + | 4 个 + | 0 |
| T2 | A0 → B0 → C0 → D1 | - | 1 个 - | 0 |
| T3 | A0 → B0 → C1 | - | 1 个 - | 0 |
| T4 | A0 → B1 | - | 1 个 - | 0 |
| T5 | A1 → B0 | + | 3 个 + | 0 |
| T6 | A1 → B1 | - | 5 个 - | 0 |

训练误差率（training error rate）是错分实例数除以训练实例总数：

$$
E_{\mathrm{train}}=\frac{0}{15}=0.00\%.
$$

悲观误差（pessimistic error）在这里采用题目明确要求的惩罚规则。每增加一个最终预测的叶子，就按 1 个额外错误计入，防止只因增加分支、把训练记录分得更细就得到无条件奖励。

设 $e$ 是训练错数、$L$ 是叶子数、$N$ 是训练实例数，题目指定每叶惩罚 1，则：

$$
E_{\mathrm{pess}}=\frac{e+1\times L}{N}.
$$

原图最底层 D 有 2 个叶子，左侧 C 的 1 分支有 1 个叶子，左侧 B 的 1 分支有 1 个叶子，右侧 B 有 2 个叶子，共 $L=6$。分支圆圈 A、B、C、D 不算叶子。

$$
E_{\mathrm{pess}}=\frac{0+6}{15}=40.00\%.
$$

这 40.00% 是“实际训练错数 + 人为复杂性惩罚”的评分。训练表实际错数仍是 0；额外加入的 6 来自惩罚约定。它与验证误差、置信上限是不同的量。

其他教材的悲观估计可能用不同修正，本题明确要求每叶惩罚 1，应按这个数计算。

英文参考作答（笔记自拟）：

> The original tree correctly classifies all 15 training instances, so its training error is 0/15 = 0.00%. It has six leaf nodes. Using the required penalty of one error per leaf, the pessimistic error estimate is (0 + 6)/15 = 40.00%.

#### 2.2.3 第 2 问：验证误差为 7/15，不是 2/6

按照同一棵原树处理验证实例，不为了让验证表现好而改叶子标签。

| 验证行 | 路径 | 预测 | 实际类别及数量 | 错数 |
|---|---|---|---|---:|
| V1 | A0 → B0 → C0 → D1 | - | 4 个 + | 4 |
| V2 | A0 → B0 → C1 | - | 3 个 + | 3 |
| V3 | A0 → B1 | - | 1 个 - | 0 |
| V4 | A0 → B1 | - | 2 个 - | 0 |
| V5 | A1 → B0 | + | 2 个 + | 0 |
| V6 | A1 → B0 | + | 3 个 + | 0 |

验证误差率（validation error rate）为：

$$
E_{\mathrm{val}}=\frac{4+3}{15}=46.67\%.
$$

表中 2 行预测错了，但它们代表 7 个实例，所以分子不是 2、分母也不是 6。训练 0.00% 而验证 46.67%，说明原树在这批未用于拟合的实例上明显变差。这是当前数据中的过拟合（overfitting）迹象，不是“任何深树都必定差”的定理。

英文参考作答（笔记自拟）：

> The tree misclassifies the four positive instances in the first validation row and the three positive instances in the second row. All remaining validation instances are classified correctly. Therefore, the validation error is 7/15 = 46.67%.

#### 2.2.4 第 3 问：剪枝时，叶子标签从训练数据决定

剪枝（pruning）指把一个内部节点连同它以下的分支，用一个预测叶子替代。这里明确采用“该节点收到的训练实例中，哪一类多就预测哪一类”。不是看验证集哪个标签多，也不是想象剪枝后仍保留原来子分支的不同答案。

先计算每个可剪节点收到的训练实例。每行是一个可替换子树，正负数量取自前面的训练表。

| 被替换的子树根 | 到达条件 | 正类数 | 负类数 | 新叶子预测 |
|---|---|---:|---:|---|
| D | A0、B0、C0 | 4 | 1 | + |
| C | A0、B0 | 4 | 2 | + |
| 左 B | A0 | 4 | 3 | + |
| 右 B | A1 | 3 | 5 | - |
| 根 A | 全体 | 7 | 8 | - |

例如剪掉 C 子树后，T1、T2、T3 全部到新的 `+` 叶子。T1 的 4 个正类正确；T2、T3 各 1 个负类都被错分，训练错数成为 2。验证 V1、V2 也到新的 `+`，它们合计 7 个正类反而全部正确。V3、V4 仍沿 B1 到 `-`，V5、V6 仍沿右 B0 到 `+`，所以验证错数降为 0。

为避免只挑有利模型，下面列全所有通过“保留原分支或整棵替换为多数类叶子”可以得到的剪枝子树。左侧有 4 种状态，右侧有 2 种状态，再加根节点直接成为叶子，共 $4\times2+1=9$ 种。

- L0：左侧完整保留。
- L1：只把 D 子树换成 `+` 叶子，保留左 B 与 C。
- L2：把 C 整棵子树换成 `+` 叶子，保留左 B。
- L3：把左 B 整棵子树换成 `+` 叶子。
- R0：右 B 保留；R1：右 B 整棵换成 `-` 叶子。
- Root：根 A 整棵换成 `-` 叶子，不再检查任何特征。

表中每行是一棵确定的候选树。错数分母都是对应集合的 15 个实例，悲观误差仍按同一个每叶 1 的规则。

| 模型 | 叶子数 | 训练错数 / 15 | 训练误差 | 悲观误差 | 验证错数 / 15；验证误差 |
|---|---:|---:|---:|---:|---:|
| L0-R0，原树 | 6 | 0 | 0.00% | 40.00% | 7；46.67% |
| L1-R0，剪 D | 5 | 1 | 6.67% | 40.00% | 3；20.00% |
| L2-R0，剪 C | 4 | 2 | 13.33% | 40.00% | 0；0.00% |
| L3-R0，剪左 B | 3 | 3 | 20.00% | 40.00% | 3；20.00% |
| L0-R1，只剪右 B | 5 | 3 | 20.00% | 53.33% | 12；80.00% |
| L1-R1，剪 D 及右 B | 4 | 4 | 26.67% | 53.33% | 8；53.33% |
| L2-R1，剪 C 及右 B | 3 | 5 | 33.33% | 53.33% | 5；33.33% |
| L3-R1，剪左右 B | 2 | 6 | 40.00% | 53.33% | 8；53.33% |
| Root，整树一个叶子 | 1 | 7 | 46.67% | 53.33% | 12；80.00% |

读 L1-R0：D 的 2 个叶子合并成 1 个，叶子从 6 减为 5；T2 由预测 `-` 改成 `+`，所以新增 1 个训练错分；V1 的 4 个正类由错变对，验证错数从 7 降为 3。悲观分子从 $0+6$ 变成 $1+5$，总和仍是 6，所以它的悲观误差没变。

为使全部剪枝错数也能逐行复做，下一表列出每棵树的每行错误贡献。序列按 T1–T6 或 V1–V6 顺序，不是预测标签。

| 模型 | 六条训练行的错数贡献 | 六条验证行的错数贡献 |
|---|---|---|
| L0-R0 | 0, 0, 0, 0, 0, 0 | 4, 3, 0, 0, 0, 0 |
| L1-R0 | 0, 1, 0, 0, 0, 0 | 0, 3, 0, 0, 0, 0 |
| L2-R0 | 0, 1, 1, 0, 0, 0 | 0, 0, 0, 0, 0, 0 |
| L3-R0 | 0, 1, 1, 1, 0, 0 | 0, 0, 1, 2, 0, 0 |
| L0-R1 | 0, 0, 0, 0, 3, 0 | 4, 3, 0, 0, 2, 3 |
| L1-R1 | 0, 1, 0, 0, 3, 0 | 0, 3, 0, 0, 2, 3 |
| L2-R1 | 0, 1, 1, 0, 3, 0 | 0, 0, 0, 0, 2, 3 |
| L3-R1 | 0, 1, 1, 1, 3, 0 | 0, 0, 1, 2, 2, 3 |
| Root | 4, 0, 0, 0, 3, 0 | 4, 3, 0, 0, 2, 3 |

这张表也解释了为什么“同样叶子数就同样好”不成立：5 叶的 L1-R0 验证错 3 个，5 叶的 L0-R1 却错 12 个。保留了什么判断，比单纯数叶子更重要。

可以据此写三个明确结论：

1. 沿原树 → 剪 D → 剪 C → 剪左 B → 只留根的嵌套路线，训练误差依次为 0.00%、6.67%、13.33%、20.00%、46.67%。合并叶子减少了针对训练实例的区分能力，训练误差没有下降。
2. 同一路线验证误差是 46.67%、20.00%、0.00%、20.00%、80.00%。适度剪枝改善，过度剪枝又恶化。这里最好的验证候选是剪 C、保留两边 B 的 L2-R0，而不是最深或最浅的模型。
3. 前四个只剪左侧的模型悲观误差都为 40.00%，所以这个惩罚本身不能唯一挑出 L2-R0。若只准用悲观评分，需要另说明同分规则；若按此题验证表现选，则 L2-R0 唯一达到 0/15。用同一验证集选完的 0.00% 是选模成绩，不能宣称未来必定零错误。

只留根时，模型连 A、B 的有用区分也丢掉，所有实例都预测 `-`。这种模型过于简单、忽略重要预测结构的情况称为欠拟合（underfitting）。

英文参考作答（笔记自拟）：

> I replace each pruned subtree with the majority class among the training instances reaching its root. Along the nested sequence of the original tree, pruning D, pruning C, pruning the left B, and replacing the root, the training errors are 0.00%, 6.67%, 13.33%, 20.00%, and 46.67%. The corresponding validation errors are 46.67%, 20.00%, 0.00%, 20.00%, and 80.00%. Moderate pruning therefore improves validation performance in this example, whereas excessive pruning leads to underfitting. The best validation model prunes the C subtree to a positive leaf and retains both B splits. The first four models tie at a pessimistic error of 40.00%, so that criterion alone does not uniquely select the best validation model.

#### 2.2.5 第 4 问：代码参数数的是边，不是图上标的层

可以使用 scikit-learn 的 `DecisionTreeClassifier`。`from ... import ...` 把库中的模型类导入；后一行创建一个尚未训练的分类器。设置模型不等于已经用表 1 拟合，也不等于重建了给定的那棵树。

常见题目预期写法如下，把“最大 8”解释为库中的最大深度参数：

```python
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(max_depth=8, random_state=42)
```

但要认识本题的计数歧义：scikit-learn 的根深度是 0，`max_depth` 数根到最深叶子的边数。原图把根标成 level 1。因此：

- 若题目“8 layers”实际上指 `max_depth=8`，上面代码是通常的参数答案，允许根到叶最多 8 条边，即最多 9 个含根层。
- 若严格沿原图的 level 1 口径，要求整树含根最多 8 层，则应设 `max_depth=7`。

这不是两个参数都同时设，而是同一句自然语言的两种数法。答题时写出采用口径即可避免无声的差一层。`random_state=42` 固定涉及随机性的选择以便复做，不是层数，也不保证任何准确率。

英文参考作答（笔记自拟）：

> The scikit-learn library provides DecisionTreeClassifier. If “maximum 8 layers” means the usual maximum-depth parameter, I would instantiate DecisionTreeClassifier(max_depth=8, random_state=42). In scikit-learn the root has depth zero; if the question literally counts the root as layer one, eight total layers instead require max_depth=7.

### 2.3 Question 5：价格变化、五步预测与滚动验证

把这三问分开：第 1 问是变量处理判断；第 2 问是在 2018-04-30 收盘时连续预测未来五天；第 3 问是历史上反复模拟“只预测明天”，评估方案而非要求编程。

英文原题（保留原句及两项选择）：

> Question 5 (20 points)
>
> Bitcoin is a cryptocurrency. Its price has increased dramatically in the past five years. The Q4 BTC-USD.csv contains Bitcoin close prices from 30/04/2013 to 30/04/2018 in column “Close.” Please use this data set to answer the following questions:
>
> (1) If you are asked to use autoregressive models to generate foresting, which variable do you think will work better as dependent variable or variable processing. Why? (5 points)
>
> (a) The original value of Bitcoin prices $Close_t$, or
>
> (b) The first order differenced value $D\_Close_t=Close_t-Close_{t-1}$.
>
> (2) Pls use an autoregressive method to forecast for Bitcoin Prices in the next five trading days (keep the answers to two decimal places) (5 points). Pls submit the code and the screenshot of results for your analysis.

下表是原题待填写的五个目标日，左列为日期，右列为该日预测价格。

| Trading date | Forecast |
|---|---|
| May 1, 2018 | |
| May 2, 2018 | |
| May 3, 2018 | |
| May 4, 2018 | |
| May 5, 2018 | |

> 3) Design a rolling-forecasting evaluation method to evaluate the “next-day” prediction performance. Please illustrate the validation dataset, evaluation metrics and calculation, and model comparison in your method. (This is a method design question; NO programming is needed.) (10 points)

原文 `foresting` 按原样保留；这里的任务显然是在谈 forecasting，即预测。上面的下标和减法为原 DOCX 数学式的正常排版，不改变变量或运算。

#### 2.3.1 第 1 问：优先尝试差分，但不要假称已检验平稳

自回归（autoregression，AR）用一个变量过去的值预测它自己接下来的值。例如“用昨天的变化预测今天的变化”，并不是“必须加入别的公司的价格”。因变量（dependent variable）是模型要预测的量；这里要先决定这个量是价格本身还是每日价格变化。

`Close` 是价格水平。题干说过去五年显著上升，意味着整段时期的价格围绕一个固定水平波动这一假设可疑。例如早期常在 100 附近、后期常在 10000 附近，用一个不变中心理解全段价格就不合理。均值、方差和随时间间隔变化的相关关系相对稳定，是常规平稳性（stationarity）考虑的内容；标准的平稳 AR 解释依赖这样的稳定结构。

一阶差分（first-order difference）把问题改为“今天比昨天涨跌多少”：

$$
d_t=Close_t-Close_{t-1}.
$$

这里 $t$ 是当天，$t-1$ 是前一天，$d_t$ 是金额变化，不是百分比收益率。差分可削弱某些趋势，若价格是带随机趋势的累积过程，差分通常比水平更适合常规 AR 建模。因此，在题目给定 (a)/(b) 两个选项中，优先尝试 (b)。

笔记补充例：价格为 100、110、121，差分为 10、11，而收益率为 10%、10%。它们不是同一个量，不能把本题的一阶价格差分直接称为“10% 收益”。

“差分更适合”是待检验的建模判断，不是已观察到的结论。差分后方差仍可能随价格水平变大，也可能仍非平稳。拿到真实文件后，应先比较价格与差分的时序图、检查结构变化，再结合训练范围内的平稳性诊断和滚动预测误差判断。不能在没读数据时报告某个检验 p 值，也不能承诺差分一定预测更准。

英文参考作答（笔记自拟）：

> I would initially use (b), the first-order difference of Close. The strong rise described in the question suggests that the price level may be non-stationary, whereas differencing can remove a stochastic trend and make a conventional stationary AR model more appropriate. Differencing does not guarantee stationarity or better forecasts; I would check the transformed series and compare out-of-sample price forecasts. The price difference is an absolute change, not a percentage return.

#### 2.3.2 第 2 问：预测差分后，要累加回价格

本解析选一个明确且简洁的教学规格：对一阶差分拟合带截距的 AR(1)。题目只要求一种 autoregressive method，没有指定滞后阶数，所以 AR(1) 是一种允许复做的参考方案，不冒称教师指定的唯一模型或最佳阶数。

“1” 表示只用前一天的差分，不表示只用一天训练数据。拟合仍使用截至 2018-04-30 的全部连续历史差分。

$$
d_t=c+\phi d_{t-1}+\varepsilon_t.
$$

式中 $c$ 是截距，$\phi$ 是前一天变化的系数，二者从历史数据估计；$\varepsilon_t$ 是模型没有解释的当天变化。预测时对未来误差取条件均值 0，不能提前知道未来误差。

令 $T$ 表示 2018-04-30，先用已知的 $d_T$ 预测下一天，再把前一次预测作为更下一天的输入：

$$
\hat d_{T+1}=\hat c+\hat\phi d_T,\qquad
\hat d_{T+h}=\hat c+\hat\phi\hat d_{T+h-1}\quad(h=2,3,4,5).
$$

帽子表示估计值或预测值。因为差分是“增加了多少”，最终价格必须从最后一个真实价格开始累加：

$$
\widehat{Close}_{T+h}=Close_T+\sum_{j=1}^{h}\hat d_{T+j}.
$$

求和符号 $\sum$ 在这里就是把第 1 天到第 $h$ 天的预测变化全部相加。不能对每一天都只计算 $Close_T+\hat d_{T+h}$，这样会丢掉中间几天的累计变化。

笔记补充完整两步例：最后真实价格为 100，最后真实差分为 2，假设拟合得到 $\hat c=1$、$\hat\phi=0.5$。第 1 天预测差分为 $1+0.5\times2=2$，价格为 102；第 2 天差分仍为 $1+0.5\times2=2$，价格为 $100+2+2=104$。第二步没有读取第 1 天未来真实价格，也不是再次从 100 直接加 2 得到 102。这个例子只教递推，不是 Bitcoin 原题结果。

原题的五个目标日期已明确给出 May 1 至 May 5，应照列填写，不擅自把周末跳到下周。配套程序按日历日产生这五个日期。

下面的代码按读取、拟合、还原三块解释。它与配套 `reproduce.py --btc` 的核心方法一致；配套入口另有列名、日期连续、重复日期、缺失值和非有限值检查。

首先读真实 CSV，并将日期从早到晚排序。`Date`、`Close` 是本程序的列名要求；若实文件用其他表头，应先查看并据实调整，不是盲改数值。

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.ar_model import AutoReg

df = pd.read_csv('Q4 BTC-USD.csv')
df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True)
df['Close'] = pd.to_numeric(df['Close'], errors='raise')
df = df.sort_values('Date').set_index('Date')
close = df.loc['2013-04-30':'2018-04-30', 'Close']
```

`sort_values` 防止来源倒序导致“昨天”其实变成明天；`set_index` 让日期成为定位行的索引；`.loc[起日:末日, 'Close']` 只取题目范围的收盘价。`dayfirst=True` 对应题干的日/月/年显示口径，ISO 年-月-日形式也可读取。若真实文件的日期格式存在歧义，应直接检查原值。

接着把相邻价格相减，再用差分序列拟合模型。

```python
delta = close.diff().dropna()
model = AutoReg(delta.to_numpy(), lags=1, trend='c', old_names=False).fit()
future_delta = np.asarray(
    model.predict(start=len(delta), end=len(delta)+4, dynamic=False)
)
```

`.diff()` 对每一行做“本行减前行”；第一行没有前一天，产生一个缺失，所以这里只删除差分必然产生的第一项。不能把原始价格中间的缺日也用 `.dropna()` 无声跳过，否则差分可能跨两天却仍称一天变化。配套入口遇到这种情况会停止。

`lags=1` 指一个滞后差分；`trend='c'` 包含截距；`.fit()` 用历史样本估计系数。`.to_numpy()` 取出按顺序排列的数值，避免让不规范的日期频率隐式改变预测定位。

Python 的第一个元素位置是 0，所以若有 $n$ 个差分，历史位置是 0 到 $n-1$，下一天从位置 $n$ 开始。`start=len(delta)` 到 `end=len(delta)+4` 的终点包含在内，因此恰好输出五项。它们都在历史终点外，后几步仍必须递推使用预测差分；`dynamic=False` 并不会神奇地提供未来真实值。

最后使用累计和还原五个价格，并格式化显示。

```python
future_price = float(close.iloc[-1]) + np.cumsum(future_delta)
result = pd.DataFrame({
    'Trading date': pd.date_range('2018-05-01', periods=5, freq='D'),
    'Forecast': future_price
})
print(result.to_string(index=False, float_format=lambda x: f'{x:.2f}'))
```

`.iloc[-1]` 取最后一项真实价格；`np.cumsum` 输出“第 1 项、第 1+2 项、……前 5 项之和”。`periods=5` 控制五个日期，`freq='D'` 按一天递增。`:.2f` 只在显示时保留两位小数，不把中间差分提早舍入。

运行配套完整检查入口：

```powershell
& D:\anaconda3\python.exe -X utf8 .\reproduce.py --btc '实际目录\Q4 BTC-USD.csv'
```

输出 `n_prices`、`training_end` 和 `last_actual_close` 用于核训练范围，随后五行是预测价；同时产生 `btc-forecast.csv` 和模型元数据。运行成功后，截图应包含代码所用模型规格、五个日期及对应预测值，不能截图一个未运行的空表冒称结果。

当前没有取得 `Q4 BTC-USD.csv`。因此下面明确留下缺口，而不是使用其他网站价格、随机生成数据或另一时间段替代：

| 原题目标日 | 当前数值状态 |
|---|---|
| May 1, 2018 | 缺原始 CSV，未计算 |
| May 2, 2018 | 缺原始 CSV，未计算 |
| May 3, 2018 | 缺原始 CSV，未计算 |
| May 4, 2018 | 缺原始 CSV，未计算 |
| May 5, 2018 | 缺原始 CSV，未计算 |

英文参考作答（笔记自拟，数值部分受阻）：

> I specify an AR(1) with an intercept for the first differences of Close and fit it using observations available through April 30, 2018. I recursively forecast five future differences and cumulatively add them to the last observed closing price to obtain forecasts for May 1–5, 2018. The required numerical forecasts and a genuine results screenshot cannot be produced until the original Q4 BTC-USD.csv is available.

#### 2.3.3 第 3 问：一天一天往前走，比较同一天的预测

“next-day” 是每次站在当天预测明天，不是只在一个起点一次预测之后全部天数。滚动预测评估（rolling-forecasting evaluation）让预测起点随时间向前移动，重复记录明天的预测与明天真实值之差。

以下是一个完整、可直接写成方法答案的设计。日期划分是本解析提出的方案，不是题目已经规定的数据划分，也没有声称已经执行。

1. 初始训练期：2013-04-30 至 2017-04-30；验证目标期：2017-05-01 至 2018-04-30。前者用于起步拟合，后者有 365 个每日目标。如果实文件不连续，必须先解决日期和观测缺口，再核实际目标数量，不能随意把缺日补为真实价格。
2. 预先固定候选：差分 AR(1)、差分 AR(7)、价格水平 AR(1)，再加朴素基线（naive baseline）“明天价格等于今天价格”。AR(7) 用前 7 天同变量值，代表明确的另一个模型复杂度；不把它宣称为最优阶数。比较价格水平与差分，也直接检验第 1 问的变量判断。
3. 第一个起点在 2017-04-30 收盘后。每个候选只用这一天及以前的观测拟合，预测 2017-05-01 的价格。差分模型的单日预测还原为“当天真实价 + 明天预测差分”。保存预测，此时不读取 2017-05-01 的真实价来改预测。
4. 2017-05-01 的实际价格出现后，计算预测误差，再把这个已发生的观测加入训练历史，重新拟合并预测 2017-05-02。持续到预测并评估 2018-04-30。这里采用扩展窗口（expanding window）：训练起点不变，终点逐日向前；若改用固定长度窗口，要预先说明长度并对全部模型保持一致。
5. 所有候选在完全相同的 365 个目标日比较，统一使用原价格单位。不能用差分 AR 的“差分误差”与水平 AR 的“价格误差”直接比较，也不能随机拆分未来记录进训练集。

读下面的时间表时，一行是一轮预测，不是一个新的随机划分。“允许训练到”是每轮能见到的最后真实日。

| 轮次 | 允许训练到 | 本轮目标日 | 目标真值何时可用 |
|---:|---|---|---|
| 1 | 2017-04-30 | 2017-05-01 | 发出该预测之后，目标日收盘时 |
| 2 | 2017-05-01 | 2017-05-02 | 发出该预测之后，目标日收盘时 |
| … | … | … | … |
| 365 | 2018-04-29 | 2018-04-30 | 发出最后一次预测之后 |

前轮验证观测可用于后轮训练，是因为在后轮时间点它已经是过去。错误的是在预测某个目标日之前，就利用了该目标日或更晚的价格。这叫数据泄漏（data leakage）。

对每个模型，每个目标日先记录真实收盘价与预测价，再计算两者之差。下面的符号用于把全部目标日的误差汇总。

| 符号 | 含义 |
|---|---|
| $i$ | 目标日编号，从 1 开始 |
| $y_i$ | 第 i 个目标日的真实收盘价 |
| $\hat y_i$ | 对同一天发出的预测价 |
| $e_i=y_i-\hat y_i$ | 该日实际价减预测价，单位与价格相同 |
| $H$ | 共同评估的目标日总数，本方案无缺日时为 365 |

采用平均绝对误差（mean absolute error，MAE）作为预先指定的主要指标，均方根误差（root mean squared error，RMSE）作为辅助指标：

$$
\mathrm{MAE}=\frac{1}{H}\sum_{i=1}^{H}|e_i|,
\qquad
\mathrm{RMSE}=\sqrt{\frac{1}{H}\sum_{i=1}^{H}e_i^2}.
$$

绝对值 $|e_i|$ 忽略高估还是低估，只看相差多远；MAE 是每天误差距离的平均数。RMSE 先平方，使大错误受到更重惩罚，再开根号回到价格单位。两者越小越好，但可能给出不同排序，因此不能看完结果才换“主要指标”。

笔记补充算例，非原题实测：若两日真实价为 100、110，模型预测 98、113，则误差为 2、-3。MAE 为 $(2+3)/2=2.50$；RMSE 为 $\sqrt{(4+9)/2}=\sqrt{6.5}=2.55$。只把误差直接平均得 -0.50 会让正负互相抵消，不能作为这里的误差大小指标。

模型比较按主要 MAE 最小者优先，并同时报告 RMSE。与朴素基线比较时，可报告相对 MAE 改善：

$$
\mathrm{Improvement}=\frac{\mathrm{MAE}_{\mathrm{naive}}-\mathrm{MAE}_{\mathrm{model}}}{\mathrm{MAE}_{\mathrm{naive}}}\times100\%.
$$

例如基线 MAE=10、模型 MAE=8，改善为 20.00%。若基线 MAE=0，不能除以 0，应直接报告各模型误差。若两个模型同分，可预先选较低阶、较简单者；如果 MAE 和 RMSE 排名不同，按主要 MAE 选，并说明大误差敏感性，而不是隐去不利指标。

如果最终根据这段验证成绩选模型，它就是验证集而不是完全独立的最终测试集。若要报告选模后的最终泛化成绩，应另留更晚的一段完全未用于选择的测试期，或使用时间顺序的嵌套评估。本题仅要求评估方法设计，可以清楚报告“这些结果用于模型比较”，不凭空增加一段不存在的未来真值。

英文参考作答（笔记自拟，方法设计）：

> I propose an expanding-window, rolling-origin evaluation. The initial training period is April 30, 2013 to April 30, 2017, and the validation targets are May 1, 2017 to April 30, 2018. At each origin, I fit each pre-specified candidate using only observations available by that date and forecast the next day's price. After the actual next-day price is observed, I score that forecast, append the observation, and refit for the following day. With complete daily data, this yields 365 common one-day-ahead targets.
>
> I would compare an AR(1) and AR(7) on first differences, an AR(1) on price levels, and a naive forecast equal to the last observed price. Differenced forecasts are converted back to price levels before scoring. For each model, MAE is the mean absolute price error and RMSE is the square root of the mean squared price error over the same target dates. I pre-specify MAE as the primary criterion, report RMSE as a secondary criterion, and compare both with the naive baseline. This validation period is used for model selection; an additional untouched later test period would be needed for a separate final assessment after selection.

## 3. 把三类任务放在一张判断表里

这张表是复习路线，不替代前面的推理。先识别题目在要“数、评估、预测”中的哪一种，再决定分母和允许看到的数据。

| 题目动作 | 从哪里开始 | 关键检查 | 输出 |
|---|---|---|---|
| 数缺失 | 原始 `Churn` 列 | 一行只数一次，先定义缺失 | 缺失行数 |
| 算 IQR | 全体有效交易额排序 | 同一四分位算法，不因缺标签删金额 | $Q_3-Q_1$ |
| 算树误差 | 从根沿条件走到叶 | 用实例数加权，不用表行数 | 错数 / 实例数 |
| 比较剪枝 | 用训练多数类替换子树 | 验证不改标签，复杂度相同未必同分 | 训练、悲观、验证三列 |
| 连续五步预测 | 最后真实历史日 | 后几步只能递推，用累计差分还原 | 五日价格 |
| 滚动一步评估 | 每天重设预测起点 | 目标真值只能事后计错 | 共同目标日上的 MAE、RMSE |

## 4. 考前速查

- 原树：训练实例 15，错 0，叶子 6，训练误差 0.00%，悲观误差 40.00%，验证错 7/15，验证误差 46.67%。
- 验证最优剪枝：C 子树 → `+`，两边 B 保留；4 叶，训练错 2/15，13.33%，验证错 0/15，0.00%，悲观误差仍为 40.00%。
- 剪枝标签从训练多数类决定。只按叶子数不能唯一决定验证误差。
- “8 layers” 若严格含根数层，对应 `max_depth=7`；若指库中的最大深度 8，对应 `max_depth=8`。要说明口径。
- 差分是价格相减，不是百分比收益；差分预测要累加回价格。
- 第 2 问：一个固定起点递推五天；第 3 问：每次有新真值后，重新站在当天预测下一天。
- 缺 `Q1.xlsx`，就不能给缺失总数或 IQR 数字；缺原 BTC CSV，就不能给五天价格。

## 5. 双语术语卡

每行是一项已在正文解释的识别词，英文定义是自拟应试用语，不是教师原句。

| 中文 | English | 英文参考定义 | 本文位置 |
|---|---|---|---|
| 缺失值 | Missing value | A value that is not observed or recorded for a variable in a record. | §2.1.1 |
| 四分位距 | Interquartile range | The difference between the 75th and 25th percentiles. | §2.1.2 |
| 叶节点 | Leaf node | A terminal node that assigns a prediction. | §2.2.1 |
| 训练误差 | Training error | The fraction of training instances misclassified by the model. | §2.2.2 |
| 剪枝 | Pruning | Replacing a subtree with a simpler terminal prediction. | §2.2.4 |
| 过拟合 | Overfitting | Fitting training-specific patterns that do not generalize well. | §2.2.3 |
| 欠拟合 | Underfitting | Using a model too simple to capture important predictive structure. | §2.2.4 |
| 一阶差分 | First-order difference | The current observation minus its immediately preceding observation. | §2.3.1 |
| 自回归 | Autoregression | Predicting a variable using its own lagged values. | §2.3.1 |
| 滚动起点评估 | Rolling-origin evaluation | Repeatedly forecasting future observations from successively later origins. | §2.3.3 |
| 平均绝对误差 | Mean absolute error | The average absolute difference between actual and predicted values. | §2.3.3 |
| 均方根误差 | Root mean squared error | The square root of the average squared prediction error. | §2.3.3 |

## 6. 英文应试时，怎样组织一段答案

本样卷本身是考试练习材料，但未取得官方评分细则，不推定这些句式有额外得分。

计算题按“实例总数 → 错数 → 公式 → 百分比”写。例如 `There are 15 validation instances. Seven are misclassified. The validation error is 7/15 = 46.67%.` 必须说明 15 是实例不是表行。

比较题按“我怎样构造候选 → 数字怎样变 → 对应结论 → 结论适用范围”写。本题不要只写 `complex models overfit`，要给剪 C 后训练 13.33%、验证 0.00% 的具体比较，以及剪到根后验证 80.00% 的反向变化。

方法设计按“训练/目标日期 → 每轮可见范围 → 更新顺序 → 共同指标 → 选择规则”写。只列 `MAE, RMSE, rolling window` 三个名称，没有说每天用哪些记录、先预测还是先看真值，仍未回答第 3 问。

## 7. 改条件自测：检查是否真正会迁移

### 自测 A：一行代表几个实例？

假设一条验证行到 `-` 叶子，表中正类 4、负类 2。它为误差分子和分母各贡献多少？

<details><summary>参考答案</summary>

分子贡献 4 个错误，分母贡献 $4+2=6$ 个实例。两个负类预测正确。不能因“只有一行”只加 1，也不能把此行全部 6 个都算错。

</details>

### 自测 B：每叶惩罚变了，哪一步要改？

若原树仍为 6 叶、训练错 0，但题目将每叶惩罚从 1 改为 0.5，原树的训练误差、悲观误差、验证误差分别如何变化？

<details><summary>参考答案</summary>

实际预测不变，训练仍为 0.00%，验证仍为 46.67%。只有悲观分子改为 $0+0.5\times6=3$，悲观误差变为 $3/15=20.00\%$。原题明确惩罚 1 时不能使用这个结果。

</details>

### 自测 C：为什么明天真实值不能提前喂给模型？

站在 2017-05-01 收盘后预测 2017-05-02，可以把 2017-05-01 的真实价加入训练吗？可以把 2017-05-02 的真实价加入训练吗？

<details><summary>参考答案</summary>

前者可以，它在当前起点已经发生。后者不可以，它正是未来要预测的目标。滚动更新允许已发生的旧目标加入后轮训练，但不允许每轮提前看自己的目标答案。

</details>

### 自测 D：累计价格会不会漏掉一天？

最后真实价格为 200，未来三天预测差分为 3、-2、4。三天的预测价格分别是什么？

<details><summary>参考答案</summary>

第 1 天为 $200+3=203$；第 2 天为 $200+3-2=201$；第 3 天为 $200+3-2+4=205$。差分单位是价格金额，不是百分比。不能写成 203、198、204，那是把每一项单独加回 200，漏掉了累计变化。

</details>

## 8. 原件定位与覆盖清单

DOCX 未提供固定渲染页码，本解析按题号、正文图注与嵌入图定位，避免把转换工具生成的页码当原始页码。每个小问一行，原文、中文和英文参考答案均在对应 §2 小节。

| 原件定位 | 原文位置 | 中文步骤 / 英文答案 | 选择项或图表 | 数值状态 |
|---|---|---|---|---|
| Question 1(1) | §2.1 原题 | §2.1.1 | 无选项，6 个变量定义保留 | 缺原始 Excel，数值受阻 |
| Question 1(2) | §2.1 原题 | §2.1.2 | IQR 口径、手算例 | 原题 IQR 受阻 |
| Problem 3(1) | §2.2 原题 | §2.2.2 | 原树及训练表 | 0.00%、40.00% |
| Problem 3(2) | §2.2 原题 | §2.2.3 | 原验证表 | 46.67% |
| Problem 3(3) | §2.2 原题 | §2.2.4 | 9 模型及逐行错数 | 全部重算 |
| Problem 3(4) | §2.2 原题 | §2.2.5 | 两种层数解释，代码 | 模型设置，不冒称拟合 |
| Question 5(1) | §2.3 原题 | §2.3.1 | (a)/(b) 全文保留，分别说明 | 初步选择 (b)，待实数检验 |
| Question 5(2) | §2.3 原题及五日表 | §2.3.2 | 递推、代码、五个目标日 | 缺原始 CSV，价格/结果截图受阻 |
| Question 5(3) | §2.3 原题 | §2.3.3 | 时间划分、365 轮、MAE/RMSE、模型比较 | 完整方法设计，未冒称已执行 |

## 9. 来源边界与题面勘误

本解析实际使用：归档 `IS6400_Business_Data_Analytics/course_files_export/canvas-20261118/Sample Final.docx` 的正文、1 个原生表格、3 张原始嵌图。三图均已逐张实际打开核对，源表数字不是只凭文本转换结果。

1. 正文标题为 Problem 3；正文图注说 Question 2，图内说 Exercise 2；正文训练表叫 Table 1，图内叫 Table 2；正文验证表叫 Table 2，图内叫 Table 3 / Test set for Problem 2。当前答案依据正文问法使用训练表和验证表，未悄悄改原图。
2. Question 1 只有两个已取得的小问，分值 4+3 与题头 20 不一致；Question 2、Question 4 不在取得的正文中。未推定残缺部分的题意。
3. `maximum 8 layers` 与图内根为 level 1 存在计数歧义，§2.2.5 给出两种参数口径，不把其中一种冒充教师确认。
4. BTC 段的 `foresting` 原词保留；题干说 trading days，但实际五日日期明列 May 1–5。按所给目标日预测，不自行删日。
5. 本地重新查找仍未取得 `Q1.xlsx` 和 `Q4 BTC-USD.csv`，原 DOCX 也没有附嵌这两个数据文件。因此 Q1 两个数据数值和 BTC 五个预测价保持受阻；没有采用替代网站数据。
6. 树误差和剪枝是参考推算，不是官方答案。`reproduce.py` 的原树及 9 种剪枝已本地执行，复算证据另存；Q1/BTC 程序只在原始输入缺失时做了真实失败路径核查，未冒称跑过原数据。

本稿教学状态待独立审查。它不改变本人是否学会、是否提交，也不等同于正式课程材料已发布。
