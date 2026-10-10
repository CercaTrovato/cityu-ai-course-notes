---
course: IS6400
module: 3
readability_rules: v2
readability_review: pending
type: tutorial
week: 3
date: 2026-09-16
source: "Week 3 Description.ipynb（48 cells：28 markdown / 20 code）"
runtime: "Python 3.13.5 · kernel conda-base-py"
libraries: [pandas, numpy, matplotlib, seaborn, scikit-learn]
data: "iris.txt（150 × 5）· Airbnb.csv（68,133 × 15）"
transcript: merged
prerequisites: [M01, T01, M02, T02, M03]
new_concepts: [read_csv(header=None), 自定义描述函数, quantile(), mode(), skew(), kurt(), value_counts(normalize=True), groupby().agg(), hist(bins=), boxplot(), 分组散点图, parallel_coordinates, isna().sum(), SimpleImputer, KNNImputer, fit_transform, IQR 离群点规则, Z 分数离群点规则, StandardScaler, RobustScaler, cov(), corr(), sns.heatmap, sort_values(key=abs)]
tags: [IS6400, tutorial, pandas, seaborn, sklearn, 描述统计, 缺失值, 离群点, 标准化, iris, Airbnb]
status: v1.0
updated: 2026-10-01
mechanism_spec: v1
mechanism_review: pending
---

# T03 · 数据探索实战：Iris 与 Airbnb 的描述统计

> **本讲一句话**：这个 notebook 把 [[M03-数据类型与描述性分析]] 的"描述性分析"部分**全部变成代码**——前半段用 150 行的 Iris 练手（描述统计、分位数、偏度峰度、分组、四种图），后半段换到 68,133 行的 Airbnb 处理**真实的脏数据**（缺失值三种填法、离群点两种规则、标准化两种尺度、相关矩阵与热力图）。notebook 自己说它是"**aligned with the Week 3 assignment difficulty**"——**它就是作业的模板**，作业第 2 题几乎逐条对应 cell 25–42。
> **原始材料**：`Week 3 Description.ipynb`（48 cells）｜ **配套讲义**：[[M03-数据类型与描述性分析]]｜ **数据**：[[IS6400_Business_Data_Analytics/_meta/数据集卡片#iris.txt|数据集卡片 › iris.txt]] · [[IS6400_Business_Data_Analytics/_meta/数据集卡片#Airbnb.csv|数据集卡片 › Airbnb.csv]] ｜ **转录**：`merged`（`M03-transcript.txt` 的 tutorial 段 `01:45:33`–`02:13:18`，2026-09-18 合并）
>
> ⚠️ **与 T01 / T02 的两个不同**：① notebook 里**没有任何 `🤖 AI Prompt` 单元格**——W1/W2 每个 code cell 后面都跟一段"把这段代码用自然语言要回来"的提示，本周没有；② notebook 末尾 **cell 44–48 直接附了 Week 3 Assignment（100 分，3 题）和提交清单**，题目比 T02 的 4 道题重得多。见 §7、§8。

---

## 0. 这个 notebook 在教什么

一句话：**怎么把一份新数据"看清楚"，并把看的过程写成一份能交的报告。**

notebook 第一个 cell 自己列了八件事，我按数据分成两段：

| 段 | cell | 数据 | 教什么 | 对应讲义 |
|---|---|---|---|---|
| **A · 干净的小数据** | 3–24 | Iris（150 × 5） | 读数据、认对象与属性（详见表后） | M03 §2.2、§2.8–2.10、§2.18 |
| **B · 真实的脏数据** | 25–42 | Airbnb（68,133 × 15） | 缺失值报告（详见表后） | M03 §2.6、§2.9–2.12 |
| C · 作业 | 44–48 | Airbnb + 自己的项目数据 | 3 题 100 分 | §7 |

**A · 干净的小数据 · 教什么**

读数据、认对象与属性。

描述统计（均值 / 中位数 / 众数 / 分位数 / IQR / 偏度 / 峰度）。

类别频数。

分组统计。

直方图 / 箱线图 / 散点图 / 平行坐标

**B · 真实的脏数据 · 教什么**

缺失值报告。

均值 / 中位数 / KNN 三种填补的比较。

IQR vs Z 分数两种离群点规则。

StandardScaler vs RobustScaler。

协方差、相关矩阵、热力图。

相关 ≠ 因果

**它和 M03 讲义的关系**：讲义 p.19 只问了"数据质量问题怎么发现、怎么办"没答，**答案全在段 B**。

讲义没讲"标准化"，段 B 的 cell 35–37 是新增内容（为 M04 的 PCA 和 W04 的聚类铺路——这两者都对尺度敏感）。

> 🎙️ **课堂实况**（2026-09-16 周三课，tutorial 段）：tutorial 段（`01:45:33`–`02:13:18`，约 28 分钟） 由教授本人主讲（不是助教），全程带着 Iris 与 Airbnb 两个 notebook 逐 cell 跑；时间最集中在 cell 28（三种缺失值填补，尤其 KNN 的 GPA 近邻类比，约 5.1 分钟）与 cell 5–8（描述统计函数与偏度峰度，约 3.8 分钟）；作业在最后约 2.9 分钟口头交代，重点是 Q3 由 TA 出题、同组必须用不同变量组合。


---

## 1. 前置

### 1.1 需要哪些库

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns                                   # 新：统计绘图库，heatmap 用它
from sklearn.impute import SimpleImputer, KNNImputer    # 新：缺失值填补
from sklearn.preprocessing import StandardScaler, RobustScaler   # 新：标准化
```

这些导入提供表格、数组、绘图、填补与缩放工具。在实际 kernel 检查依赖；安装了 Anaconda 本身不能保证每个环境都有这五个库。

seaborn 封装了 matplotlib 的统计绘图，本篇用它画热力图。原 metadata 是 Python 3.13.5、kernel conda-base-py；它是来源记录，不当作本轮运行版本。

两个数据文件应能由 kernel 的实际工作目录访问。工作目录恰好是 notebook 所在目录时，把 CSV 放同目录很方便；否则使用正确相对路径或明确路径。Canvas Week 3 提供 iris.txt 与 Airbnb.csv。

### 1.2 对应哪一讲的理论

| notebook 段 | 讲义 M03 | 一句话 |
|---|---|---|
| cell 2 "object / attribute" | §2.2（p.4） | 行 = 对象，列 = 属性 |
| cell 4–8 描述统计 | §2.9–2.10（p.24–28） | 集中趋势 / 离散 / 形状 |
| cell 9–12 频数与分组 | §2.8（p.23）、§2.16 聚合（p.51） | 类别只能数；分组 = 聚合 |
| cell 13–24 四种图 | §2.18（p.63–70） | 直方图 / 箱线图 / 散点 / 平行坐标 |
| cell 25–30 缺失值 | §2.6（p.19） | 数据质量三问的答案之一 |
| cell 31–34 离群点 | §2.6、§2.9（IQR） | 答案之二 |
| cell 35–37 标准化 | —（讲义没有；M04 PCA 前置） | 尺度问题 |
| cell 38–42 协方差 / 相关 | §2.11–2.12（p.30–34） | 相关 ≠ 因果 |

### 1.3 本 notebook 第一次出现的 API（读之前先认识）

| API | 一句话 | 首次出现 |
|---|---|---|
| `pd.read_csv(path, header=None)` | 文件没有表头行时，告诉 pandas 第一行就是数据 | cell 3 |
| `df.columns = [...]` | 事后给列命名 | cell 3 |
| `s.quantile(q)` / `s.mode()` / `s.skew()` / `s.kurt()` | 分位数 / 众数 / 偏度 / 峰度（`describe()` 不给后三个） | cell 5 |
| `s.value_counts(normalize=True)` | 类别频数 → 百分比 | cell 10 |
| `df.groupby(col)[cols].agg([...])` | 分组后一次算多个统计量 | cell 11 |
| `s.hist(bins=)` / `df.boxplot()` / `plt.scatter()` / `parallel_coordinates(df, class_col)` | 四种图 | cell 14–23 |
| `df.isna().sum()` | 每列缺失个数 | cell 27 |
| `SimpleImputer(strategy=)` / `KNNImputer(n_neighbors=)` + `.fit_transform()` | 三种填补 | cell 28 |
| `StandardScaler()` / `RobustScaler()` + `.fit_transform()` | 两种标准化 | cell 36 |
| `df.cov()` / `df.corr()` / `sns.heatmap()` | 协方差矩阵 / 相关矩阵 / 热力图 | cell 39–40 |
| `s.sort_values(key=abs, ascending=False)` | 按**绝对值**排序 | cell 41 |

> **sklearn 的 `fit_transform` 约定**（T02 §1.3 讲过 `fit` / `predict`，这里是它的兄弟）：**预处理器**（Imputer、Scaler、Encoder）用 `fit` 学统计量（均值、中位数、分位数），用 `transform` 套到数据上；`fit_transform` 一步做完。**返回的是 numpy 数组，不是 DataFrame**——列名会丢，要自己接回去（cell 28、36 都在做这件事）。

---

## 2. 逐块讲解 · 段 A：Iris（cell 1–24）

### 2.1 【cell 3】读数据、命名列、看前 10 行

**这块在干什么**：把 `iris.txt` 读成表，给五列起名，看一眼。顺手做了三件"环境设置"。

```python
np.random.seed(42)                          # 固定随机数（本 notebook 后面 KNN 不用随机，这是习惯）
plt.rcParams['figure.figsize'] = (9, 5)     # 所有图默认 9×5 英寸
plt.rcParams['axes.grid'] = True            # 所有图默认带网格
sns.set_style('whitegrid')                  # seaborn 风格：白底网格

data = pd.read_csv('iris.txt', header=None)
data.columns = ['sepal length', 'sepal width', 'petal length', 'petal width', 'class']
data.head(10)
```

**逐行**：`header=None` 是关键——`iris.txt` 第一行就是 `5.1,3.5,1.4,0.2,Iris-setosa`，没有列名；不写这个参数 pandas 会把第一朵花当表头，数据少一行、列名变成 "5.1"。`data.columns = [...]` 事后命名（列名带空格是可以的，但后面取列只能用 `data['sepal length']` 不能用 `data.sepal length`）。

**输出**：前 10 行全是 `Iris-setosa`（文件按品种排好了：前 50 行 setosa、中 50 行 versicolor、后 50 行 virginica）。

**为什么这么写**：`rcParams` 三行是 T02 §3.4 助教讲过的"全局样式"（🎙️ M02 转录 `01:52:40`），一次设定全 notebook 生效。`np.random.seed(42)` 在本 notebook 里其实没被用到，但作业要求 "Set random seeds where needed"，这一行是给你抄的。

**⚠️ 易错点**：文件叫 `.txt` 但内容是 CSV——`read_csv` 只看内容不看后缀。

**💡 两行文件怎样变成两行表（笔记补充）**

读取的输入是路径、分隔符和表头约定，输出是 DataFrame 及可核的行数/列数/类型。相对路径由 kernel 的工作目录解释；浏览器显示在哪个文件夹不自动决定读取位置。以下两行是教学小 CSV，不是原 Iris 数据：

```text
10,2,1,0.5,A
12,3,2,0.7,B
```

按 `header=None`，逗号拆成每行5字段，所有行都作数据，先得到2×5表；列标签暂为0/1/2/3/4，行标签为0/1。再赋原代码的五个列名：第0行的`sepal length=10`、`petal width=.5`、`class='A'`；第1行对应12/0.7/B。`head(10)`实际只返回现有两行，不造另外八行。

```mermaid
flowchart TD
    CSV0[路径；逗号分隔；表头规则] --> CSV1[由kernel工作目录定位并读文件]
    CSV1 --> CSV2[解析字段；按header规则保留数据行]
    CSV2 --> CSV3[形成DataFrame；核行列数与类型]
    CSV3 --> CSV4[赋五列名；检查首尾及shape]
```

若误用默认推断表头，第一行被当列名，剩下只有1×5，A那行丢了；API成功返回也可能读错。文件不存在或赋的列名数与字段数不符应报告并停下，不随手删列凑形状。读取完整文件后返回表，没有模型迭代；之后改列名是元数据操作，不是改原始文件。

**迁移自测**：再加第三行`14,4,3,0.9,A`，`header=None`与默认表头各几行？<details><summary>答案与理由</summary>正确读取3×5，默认推断表头2×5；`head(10)`分别显示3行或2行。先核原文件确无表头，再明确header约定，不能仅凭“输出有漂亮列名”判读取正确。来源：笔记补充。</details>

**所以呢**：先确认行没有被吞、列身份正确，再解释统计量；错读的文件也能算出看似合理的均值。

**术语唤醒（笔记补充）**：SKU（stock keeping unit，库存单位标识）用于区分一种商品或规格；它是标识，不是销售金额。课堂引文提到它用于说明“一行代表什么对象”。

**🎙️ 课堂补充**（`01:46:42`–`01:48:59`，约 2.3 分钟，A · 课上展开）

- 复述“行是对象、列是属性”这条定义：*"And the row is an object. And the column is the attributes we have."*（`01:46:56`–`01:46:58`）
- 逐句解释 `header=None` 的必要性：*"There are no definitions of the header. So the header equals to none. It means that we do not have the name for each column from the raw data."*（`01:47:43`–`01:47:51`）
- 补了 notebook 没写的业务背景——为什么原始文件会没有列名：*"[S]ometimes when the company is recording the data, they will prepare two different datasets. One is the pure values of SKU[s]. The second will be the name of different columns[,] in two different separate ones."*（`01:47:53`–`01:48:05`）
- **这段改变了什么**：确认了笔记对 `header=None` 的解读。

新增一条业务解释——公司常把“纯数值表”和“字段对照表”分开存，这是课堂说明“为什么有些文件可能无表头”的业务例子。

没有证据认证本 iris.txt 的实际制作来源。

### 2.2 【cell 5–7】自定义描述函数：一次算 12 个统计量

**这块在干什么**：`describe()` 只给 8 个数（count/mean/std/min/25%/50%/75%/max），作业要求 11 个（加众数、Q1/Q3、极差、IQR、偏度、峰度）。notebook 自己写了一个函数补齐。

```python
def describe_col(df, col):
    s = df[col]
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    return pd.Series({
        'mean': s.mean(), 'median': s.median(), 'mode': s.mode().iloc[0],
        'std': s.std(), 'min': s.min(), 'max': s.max(),
        'Q1': q1, 'Q3': q3, 'range': s.max() - s.min(), 'IQR': q3 - q1,
        'skew': s.skew(), 'kurt': s.kurt()
    })
describe_col(data, 'sepal length')
```

**逐行**：`s.mode()` 返回的是一个 **Series**（众数可能不止一个），所以要 `.iloc[0]` 取第一个；`pd.Series({...})` 把字典变成一列带名字的数，方便后面拼成表。cell 6 用**字典推导式**对四列各调一次再 `.T` 转置成"一行一个属性"的表；cell 7 用 `data[cols].quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])` 一次出六个分位数。

**输出**（cell 5，`sepal length`）：mean 5.843、median 5.80、mode 5.0、std 0.828、min 4.3、max 7.9、Q1 5.1、Q3 6.4、range 3.6、IQR 1.3、skew 0.315、kurt −0.552。
（cell 6 四列汇总）：petal length 的 std 最大（1.764）、IQR 最大（3.5）、峰度最负（−1.402）；这些数可提示进一步查分组，但单独不证明三个品种混合或有三个峰。
（cell 7）：petal width 的 90% 分位 2.2、99% 分位 2.5 = 最大值——**最大的 1% 花瓣宽度都是 2.5**。

**为什么这么写**：作业第 1 题的原话是 "mean, median, mode, std, min, max, Q1, Q3, IQR, skewness, kurtosis"——**正好是这个函数的输出**。cell 8 的 markdown 给了读数规则：偏度近0只表示三阶偏斜较小，不保证对称；正偏通常提示右尾较长；峰度近 0 像正态尾、大正值重尾（M03 §2.10）。

**⚠️ 易错点**：
- `s.std()` 是样本标准差（分母 n−1），与讲义 p.30 样本协方差口径一致；numpy 的 `np.std` 默认分母 n，两者会差一点。
- `kurt()` 是**超额峰度**（正态 = 0）。
- 众数对连续变量意义不大（M03 §2.9）。

**💡 从原始列走到十二个统计量（笔记补充）**

函数接收 DataFrame 与列名，输出一个带统计量名称的 Series；cell 6 将四份 Series 拼成 12×4 表，再转成 4×12。它汇总的是每列实际观测值，不会把缺失项当零。以下小列与 Iris 原例分开，用于看清函数内部动作：`[1,2,2,4,9,10,NaN]`。

1. 记录缺失 1 个、有效数 $n=6$，排序后仍为 $1,2,2,4,9,10$。和为 28，均值 $28/6=14/3$。不能除以原行数 7；最小 1、最大 10、极差 9。
2. 分位数的默认线性插值在零起算位置 $h=(n-1)q$。

$q$ 是目标比例，$h$ 是排序后的所在位置。

若 $h=j+f$，$j$ 是向下取整的位置、$0\le f<1$，结果为 $(1-f)x_{(j)}+fx_{(j+1)}$。

本例 Q1 的位置 1.25，两端都是 2，所以 Q1=2。

中位位置 2.5，两端 2、4，故为 3。

Q3 位置 3.75，两端 4、9，故 $4+0.75(9-4)=7.75$，IQR=5.75。

Q99 位置 4.95，结果 9.95，**并非最大值 10**。
3. 频数表为 1→1 次、2→2 次、4/9/10→各 1 次，众数为 2。若改成 `[1,1,2,2]`，`mode()` 返回两个众数 1、2；`.iloc[0]` 只保留第一个，不等于只有一个众数。
4. 均值处的偏差依次 $-11/3,-8/3,-8/3,-2/3,13/3,16/3$，平方和 $226/3$。样本方差除以 $n-1=5$，为 $226/15$，开根得到 std≈3.881580。总体口径除以 6 得到不同的数，不能混用。
5. 偏度与超额峰度不是“再看均值大小”：它们读取三、四次方偏差及样本校正。

本例三次方和 $1310/9$、四次方和 $38982/27$。

除以 6 得 $m_3,m_4$，平方和除以 6 得 $m_2$。

pandas 的样本偏度是 $\sqrt{n(n-1)}m_3/[(n-2)m_2^{3/2}]$。

样本超额峰度是 $\frac{n-1}{(n-2)(n-3)}[(n+1)(m_4/m_2^2-3)+6]$。

本例分别约 0.746662、−1.797909。

$m_r$ 表示偏差 r 次方的平均。

校正与形状解释见 [[M03-数据类型与描述性分析#2.10 数值变量 II：分布形状——偏度与峰度（讲义 p.27–28）|M03 偏度与峰度]]，不要由一个峰度数单独断言有几个群。

**下图是包含安全边界检查的笔记补充流程**；原cell5函数没有全缺失众数守卫，不能把图说成原函数已经实现的步骤。

**控制与边界**：全缺失列的 `mode()` 是空 Series，原 `.iloc[0]` 会失败；先检测有效数为零，输出“缺失、无统计量”并返回，不能给零均值。偏度至少需要三个有效值、样本峰度至少四个；常数列的标准化三/四阶矩在数学上无分母，应报告退化并按明确 API 约定处理。不同函数的缺失策略须逐项确认。

```mermaid
flowchart TD
    D0[列与缺失标记] --> D1{有效数为零？}
    D1 -->|是| D2[返回缺失报告；不索引空众数]
    D1 -->|否| D3[排序与计数；均值及中心偏差]
    D3 --> D4[分位插值；众数；方差与高阶矩]
    D4 --> D5[核分母及退化条件；组成统计Series]
    D5 --> D6[逐列拼表并转置；保留列名]
```

**迁移自测**：将最后的 10 改为缺失，先预测有效数、中位数、Q3，再调用函数。<details><summary>答案与理由</summary>有效数 5；排序1/2/2/4/9，中位数2；Q3位置3，等于4。原缺失与新缺失都排除，不能仍用六个观测的位置。来源：笔记补充，按上述默认插值规则。</details>

**所以呢**：统计函数先明确有效数据与位置，再给单列汇总；下一步按类别把数据拆开，重新计算每一组的有效分母。

**🎙️ 课堂补充**（`01:49:04`–`01:52:51`，约 3.8 分钟，A · 课上展开）

- 强调 pandas 已经内置了这些统计量的计算：*"[M]ost of the summary statistics calculations have been supported by the Pandas Data Frame."*（`01:49:15`–`01:49:26`）
- Q1/Q3 与 IQR 的口头公式：*"Q1, Q3, we will calculate it using S dot quantile. So this is a 25 quantile or 75 quantile. ... [F]or the IQR, it is Q3 minus Q1."*（`01:50:01`–`01:50:09`）
- 明确预告 `describe()` 要到下一讲才教：*"[N]ext week, I think, we will have a simple function called data.describe... [it] will generate all this information in a single command."*（`01:51:29`–`01:51:39`）
- 偏度 / 峰度的口头定义（ASR 把 skewness 识别成 "SKU needs"、kurtosis 识别成 "QNAS/quotasys"）：

> *"[T]he [skewness] tell[s] you whether it is [symmetric?]... and the [kurtosis] tell[s] you whether it is normally dis[tributed] or concentrated to the middle..."*

（`01:52:40`–`01:52:45`）
- **这段改变了什么**：确认了笔记对 `describe_col` 与六分位数的解读；新增一条时间线信息——手写统计函数是给 `data.describe()`（下一讲才教）打的铺垫，不是长期要用的写法。

### 2.3 【cell 10–11】频数与分组统计

**这块在干什么**：类别列只能数（M03 §2.8）；然后按品种分组，看四个数值属性在三类里各是什么水平——这是"分组 = 聚合"（M03 §2.16）。

```python
print(data['class'].value_counts())
print(data['class'].value_counts(normalize=True).round(3))

data.groupby('class')[['sepal length', 'sepal width', 'petal length', 'petal width']].agg(['mean', 'median', 'std'])
```

**逐行**：第一行按类别计数；第二行将各非缺失类别频数除以其总数；第三行按 `class` 拆组、只选四个数值列、对每组每列调用三个函数后合成表。原行不被改写，输出层级和分母见下方完整小例。

**输出**：三类各 50 朵、各 0.333——**完全平衡**的数据集。分组表：petal length 的均值 setosa 1.464 / versicolor 4.260 / virginica 5.552，三类差得很开；sepal width 的均值 3.418 / 2.770 / 2.974，几乎叠在一起。cell 12 的结论："petal length varies much more across species than sepal width"，并明说**这就是作业里要对 `log_price` 按 `city` / `property_type` 做的事**。

**为什么这么写**：`groupby(...)[cols].agg([list])` 是 pandas 做"透视表"的标准写法（M03 §2.7 的 pivot table）；输出是**多级列**（属性 × 统计量），看着乱但作业可以直接贴。

**⚠️ 易错点**：`value_counts()` 默认按频数降序排；`normalize=True` 给比例不是百分比（0.333 不是 33.3）。

**💡 分组的机制：拆开 → 汇总 → 合并（笔记补充）**

`groupby` 没有把每组压成一个原始样本，而是建立“键值→行集合”的分组状态；`agg` 按每组、每列、每个函数分别计算，再把结果合成新表。分组后的行索引是组名，列索引是“原列名/统计量”的两层。

| 原行 | class | x | y |
|---|---|---|---|
| 1 | A | 10 | 1 |
| 2 | A | 20 | 3 |
| 3 | A | 缺失 | 5 |
| 4 | B | 5 | 2 |
| 5 | B | 15 | 4 |
| 6 | 缺失 | 40 | 9 |

1. 默认缺失键不成组，得到 A={行1,2,3}、B={行4,5}。`size()` 数行，A=3、B=2；`count()` 数指定列的非缺失，x 列 A=2、B=2。第6行的 x=40 本来有效，却因键缺失被分组默认排除；若业务要它另成“未知组”，显式 `dropna=False`。
2. A 的 x 均值 $(10+20)/2=15$、中位15、样本 std=$\sqrt{(25+25)/(2-1)}\approx7.0711$；A 的 y 均值3、中位3、std=2。B 的 x 均值10、中位10、std≈7.0711；y 均值3、中位3、std≈1.4142。
3. 原命令选两列、算三函数，因此新表是 **2 行×6 列**。例如 `result.loc['A', ('x','mean')]` 为15，而 `('y','std')` 为2。元组表示列的两个层级，不是两次独立索引。
4. `class.value_counts(normalize=True)` 默认排除缺失键，比例 A=3/5=0.6、B=2/5=0.4；不是3/6和2/6。分母选全6行时须另做缺失类别计数，不能把两个口径并排比较后说结果算错。

```mermaid
flowchart TD
    G0[原行；分组键；指定数值列] --> G1[按缺失键策略建立组到行集合]
    G1 --> G2[逐组逐列取有效值；记录size与count]
    G2 --> G3[运行每个聚合函数；得到统计量]
    G3 --> G4[以组名和属性/统计量两层列合并结果]
```

均值的分母是该列非缺失数，因此两列可在同一组有不同分母；单个有效值的样本 std 无定义，pandas 返回 NaN。所有组的均值也不能不加权再当全表均值，且被排除的键必须说明。`groupby` 不会自动补出不存在的业务组或证明群之间有因果差别。

**迁移自测**：把第3行 x 补为30，并保留缺失键组，A 的 size/count/mean 怎样变？<details><summary>答案与理由</summary>A 的size仍3，count从2变3，mean从15变20；未知键组一行，x mean=40、sample std=NaN。指定两列三函数时新表3×6。不是把原来mean15与新值30简单平均。</details>

**所以呢**：分组表看见的是组内汇总，行到统计量的路径应能追踪；画图时又回到原行，不要把每个均值误当原始点。

**术语唤醒（笔记补充）**：透视表（pivot table）是按键分组、将汇总量按行列重排显示的表；本例groupby加agg给出同类分组汇总，但具体表布局与pivot函数的参数并不完全相同。

**🎙️ 课堂补充**（`01:52:51`–`01:55:48`，约 3.0 分钟，A · 课上展开）

- `value_counts(normalize=True)` 的口头解释与结果（ASR 把 setosa 识别成 "cytosine"）：*"[I]f we put in the value count[s] and do the normalization, and keep the three decimals here[,] then you will tell you that about 33.3% is the data point belonging to your [setosa]."*（`01:53:26`–`01:53:41`）
- 🔴 **notebook 和讲义都没有的增量：用银行“正常交易 vs 欺诈交易”举例讲类别不平衡**（ASR 把 fraud 识别成 "board"）：

> *"Now when you go to the bank, the number of normal transactions will be much, much larger than the [fraud?] transactions. So if we want to detect [fraud?] transactions, we are actually getting a very tiny group of labeled [fraud?] transactions from the large group of normal transactions."*

（`01:54:07`–`01:54:25`）
- 预告分类章节会专门处理不平衡数据，并点明数据探索的意义：

> *"[I]n the later classification lecture we will have one small section to illustrate how to deal with the imbalanced data classification. ... [T]he data exploration is very important at the very beginning for you to choose the right model."*

（`01:54:32`–`01:55:11`）
- **这段改变了什么**：`value_counts` 与 `groupby().agg` 本身与笔记一致。

新增了“三类各占 33.3%”这件事为什么重要——真实数据常常类别不平衡，这是选模型前必须先看的信号，教授用银行欺诈检测具体举了例子。

### 2.4 【cell 14–23】四种图

**这块在干什么**：把 M03 §2.18 的四种图各画一张，每张后面一句"看到了什么"。

```python
data['petal width'].hist(bins=20)
plt.title('Histogram of Petal Width')
plt.xlabel('Petal Width (cm)')
plt.ylabel('Frequency')
plt.show()

data.boxplot()
plt.title('Boxplot of Iris Attributes')
plt.ylabel('Value (cm)')
plt.show()

for name, group in data.groupby('class'):
    plt.scatter(group['petal length'], group['petal width'],
                alpha=0.7, label=name)
plt.xlabel('Petal Length (cm)')
plt.ylabel('Petal Width (cm)')
plt.title('Petal Length vs Petal Width by Class')
plt.legend()
plt.show()

from pandas.plotting import parallel_coordinates
parallel_coordinates(data, 'class')
plt.title('Parallel Coordinates Plot for Iris')
plt.show()
```

**逐行**：
- **直方图**（cell 14）：`bins=20` 对应讲义 p.63 右图；输出图左侧 0.1–0.3 一根高柱（setosa 的花瓣极窄），右侧多个峰。cell 15 的结论：**多峰 = 可能是多个总体的混合**，"an important warning about distributional shape"。
- **箱线图**（cell 17）：`data.boxplot()` 一次画四列（讲义 p.66 原图的 pandas 版）；petal length的四分位跨度最大，sepal width较窄且有被默认规则单独标出的点；盒子的纵向位置与跨度是两种量，不要混读。cell 18："No obvious extreme outliers"。
- **分组散点图**（cell 20）：`for name, group in data.groupby('class')` 是 pandas 的**按组循环**——每次拿到组名和该组的子表，各画一次 `scatter` 并用 `label=name` 生成图例。

`alpha=0.7` 半透明防重叠。

输出：setosa在花瓣两列中较易分离，versicolor与virginica仍有重叠。

按类别着色帮助观察，不能由图保证新样本分类无误。

cell 21 的结论：两个变量的关系可以"strong and **nonlinear** when a categorical variable is present"——M03 §2.11 说相关只抓线性，原notebook提出非线性观察，但类别存在本身不能证明非线性。

本图能直接支持的是组分布不同及两类有重叠，具体函数关系需再检验。
- **平行坐标**（cell 23）：`parallel_coordinates(data, 'class')` 第二个参数是**类别列名**，用来着色；输出与讲义 p.70 左图一致（轴序 sepal length → sepal width → petal length → petal width），三类在 petal 两根轴上分成三束。

**本轮将四个输出放到读法旁边**：同一 iris.txt 定向生成，散点另配点形，其余保原统计口径；不是旧保存像素。图源 figures/t03-readability/figures.py。

**直方图：花瓣宽度集中在哪些区间？**

![[IS6400_Business_Data_Analytics/notes/figures/t03-readability/iris-hist.svg]]

横轴花瓣宽 cm，纵轴区间内花数；每柱累计多行。首行 0.2 cm 给所在箱贡献 1 次，20 箱合计 150。文字替代：窄花瓣区间集中，较宽区间也有记录；多峰只提示进一步分组，改变分箱会改变形状。

**箱线图：哪列中间一半的跨度大？**

![[IS6400_Business_Data_Analytics/notes/figures/t03-readability/iris-box.svg]]

横向四项是测量列，纵轴 cm。盒底/中线/盒顶为 Q1/中位数/Q3；须到围栏内最远观测。sepal length 的 Q1=5.1、Q3=6.4，所以盒高为 1.3 cm。

文字替代：petal length 的 IQR 最大；盒位置表示水平，盒高表示离散。图沿原 boxplot 默认 1.5×IQR；课堂口头 10/90 百分位的版本冲突继续保留，不混用。

**散点：怎样保持同一朵花的两测量配对？**

![[IS6400_Business_Data_Analytics/notes/figures/t03-readability/iris-scatter.svg]]

横轴花瓣长、纵轴花瓣宽，均 cm；首行 (1.4,0.2) 是一个 Setosa 点。点形/颜色来自已知 class。文字替代：Setosa 较易分离，另两类部分重叠；它不是独立分类成绩。两列不能独立排序再画点。

**平行坐标：一朵花跨四属性是什么轮廓？**

![[IS6400_Business_Data_Analytics/notes/figures/t03-readability/iris-parallel.svg]]

横向依次四属性，纵轴原 cm；一条线连接同一原行，没有时间箭头。首行依次 5.1→3.5→1.4→0.2。文字替代：150 行各有一条原测量轮廓；默认未做各轴独立缩放，换轴序/尺度会改变视觉印象。

<details><summary>四图读图自测：箱须、跨列连线、直方频数与散点配对</summary>

1. 箱须是围栏值吗？须取围栏内真实观测，不直接画围栏。
2. 哪张连接首行四值？平行坐标；散点仅取同花的花瓣两值。
3. 首行 0.2 cm 对哪个直方箱贡献？20 等宽箱从 0.1 到 2.5，箱宽 0.12，所以进入 [0.1,0.22)，贡献 1。柱汇总该区间的多朵花，不代表单花。
4. 横纵两列独立排序后仍是同花吗？通常不是，原行配对已破坏。应按同一原行同时取两值。

</details>

**输出核对（2026-09-30 实跑）**：`render-t03-plots.py` 按原 Iris 数据生成并实际查看了四张图。20个直方箱计数合计150；平行坐标150条样本线直接使用原行的四个数，首行为5.1/3.5/1.4/0.2。散点中setosa分离较明显，另两类重叠，不能说三类完全分开。箱线图是petal length的IQR最大，sepal width较窄并有单独点。中间核对见`t03-plot-check.json`，图像为临时验收材料，不嵌入正文替代可编辑代码与解释。

**为什么这么写**：作业第 2.3 题要求"每个特征与 log_price 一个统计量 + 一张图，带标题、轴标签、2–3 句解释"，**且 "at least 8 plots"**——这四个 cell 每个都示范了"`plt.title` + `plt.xlabel` + `plt.ylabel` + 一段 markdown 解释"的完整格式，照着来。

**⚠️ 易错点**：
- `plt.show()` 之后再调 `plt.title` 无效（图已经画完了）；标题和轴标签要在 `show()` **之前**。
- `data.boxplot()` 会把所有数值列画在一起，如果量纲差几个数量级（Airbnb 的 `number_of_reviews` 0–600 与 `bathrooms` 0–8），小的那些会压成一条线——Airbnb 要分开画或先标准化。
- 平行坐标的轴序按 DataFrame 列顺序；想换序先 `data[[新顺序]]`。

**行怎样变成图（笔记补充）**：小列1/2/2/3/4/20，指定箱界[0,2,4,6,20]时，直方频数为1/3/1/1：通常左闭右开，最后一箱含20。

不能把柱高当该箱中心的值。

箱线图先用同列Q1=2/Q3=3.75，须截止于围栏内最远观察值1和4，20单独画点。

须不是围栏数−0.625/6.375本身。

散点把同一原行的横纵值组成一对，先按共同有效行处理。

组颜色是来源标签，非计算出的分类结果。

平行坐标一行(1,100)在第一轴取1、第二轴取100后连线。

pandas默认直接使用这些数，**不会自动给每轴做独立缩放**。

要改尺度须显式预处理并说明，折线交叉不能当变量间因果。

**所以呢**：图上每一柱、点和折线都应能回到原行或计数；换成Airbnb脏数据，先处理缺失与参照尺度再解释图形。

**四图的机制数据流（笔记补充）**：下图分支接收同一原表，但各图建立的中间表示不同。先明确有效数值、缺失处理、行身份和轴单位；没有有效观察时应报告空数据，不能从空图推断没有异常。

```mermaid
flowchart TD
    P0[原表；行身份；数值列；类别；尺度] --> PH[直方：选一列与箱边界]
    PH --> PH1[逐观察分箱；末箱含右端；各箱计数]
    PH1 --> PH2[柱位置为区间；柱高为频数]
    P0 --> PB[箱线：取一列有效观察并排序]
    PB --> PB1[算Q1/中位/Q3；IQR围栏]
    PB1 --> PB2[取围栏内最远观察为须；超界值单列]
    PB2 --> PB3[画盒、须、中位线及单独点]
    P0 --> PS[散点：同一原行的两列与类别]
    PS --> PS1[保留共同有效行；形成x/y/类的配对]
    PS1 --> PS2[每行一个点；类别只决定颜色]
    P0 --> PP[平行：指定轴顺序与原值或显式缩放值]
    PP --> PP1[每行取得各轴对应值；保留行身份]
    PP1 --> PP2[连接同一行的各轴点；按类别着色]
```

直方箱边界、箱须规则、类别色标与显式尺度都属于需要记录的输入约定；改它们会改变图形，原行不因此变化。

**🎙️ 课堂补充**（`01:55:48`–`01:59:12`，约 3.4 分钟，A · 课上展开）

- 直方图 bin 数与读图：*"[L]et me show you that there are 20 intervals here[,] because [bins equals] 20... [M]ost of the records[,] they have their petal width value to be very small."*（`01:56:09`–`01:56:41`）
- 🔴 **箱线图离群点边界，口头说法是百分位而非 1.5×IQR——与本笔记 §9.5 ⑤ 的疑问对上了**：*"[S]o the threshold[,] together with some outliers here[:] the outlier[s] above the [90th?] percentile or below the 10th percentile[,] they were labeled outliers."*（`01:56:58`–`01:57:07`）
- 分组散点图的读图描述：*"[A] simple visualization, a two-dimensional visualization is petal length and petal width. ... [W]e can see a very clear difference in the pattern[s] of the blue data points[.]"*（`01:57:14`–`01:57:29`）
- 平行坐标的工具来源：*"[P]andas has its own plotting library called pandas [dot] plotting[,] and one of the tool[s] in [that] library is called parallel coordinate[s]."*（`01:58:13`–`01:58:27`）
- **这段改变了什么**：确认了四张图的读法。

新增一条与本笔记 §9.5 ⑤ 直接相关的证据——教授口头描述箱线图须用的是 10/90 百分位，与 `data.boxplot()` 实际默认的 1.5×IQR **不是同一套口径**。

作业里若按讲义 10/90 百分位算须会与 notebook 输出的箱线图对不上，建议以 `boxplot()` 的 1.5×IQR 为准并注明。

---
## 3. 逐块讲解 · 段 B：Airbnb 的脏数据（cell 25–42）

### 3.1 【cell 26–27】读数据、缺失值报告

**这块在干什么**：换到真实数据，第一件事是数每列缺了多少。

```python
air = pd.read_csv('Airbnb.csv')
air.head()

missing = air.isna().sum()
missing_ratio = (missing / len(air)).round(4)
pd.DataFrame({'missing': missing, 'ratio': missing_ratio})[missing > 0]
```

**逐行**：`isna()` 把整张表变成 True/False，`.sum()` 按列数 True 的个数；除以 `len(air)`（行数 68,133）得比例；最后一行 `[missing > 0]` 用布尔索引只留有缺失的列。

**输出**：

| 列 | 缺失 | 比例 |
|---|---|---|
| host_has_profile_pic | 180 | 0.0026 |
| host_identity_verified | 180 | 0.0026 |
| review_scores_rating | **15,275** | **0.2242** |

（与 [[IS6400_Business_Data_Analytics/_meta/数据集卡片#Airbnb.csv|数据集卡片]] §3 一致；`verify_airbnb.py` 复核相同。）

**为什么这么写**：作业第 2.1 题第一条就是 "Missing-value report for all columns"——这三行就是模板。⚠️ 注意 `bedrooms` **没有缺失**，但 cell 28 仍然把它和 `review_scores_rating` 一起填补——见 §3.2 的坑。

**⚠️ 易错点**：`head()` 的第 4 行 `review_scores_rating` 已经是 `NaN`（该房源 `number_of_reviews = 0`）——**评分缺失的机制是"没评论就没评分"**，不是随机缺失（数据集卡片 §3.1）。这一点在作业里写出来是加分项：它说明"用中位数填"是在给没有记录评分的房源一个"典型"评分，得说清这个假设。

没有记录评论不等于无人入住。已核 15,275 条缺评分中，14,434 条评论数为 0；其余 841 条的缺评分原因仍未核，不能统称“没人住过”。

**💡 从单元格缺失到逐列报告（笔记补充）**

输入为一张带明确缺失标记的表；`isna()`输出同形状布尔表，沿行方向求和得到每列缺失数，再除以总行数得到比例。最后`[missing > 0]`筛报告中的**列条目**，不是删除原表缺失行。小表与当前Airbnb源数据分开：

| 原行 | rating | bedrooms | host_verified |
|---|---|---|---|
| 31 | 90 | 1 | t |
| 12 | NaN | 2 | NaN |
| 50 | 96 | NaN | f |

1. 布尔表按原行分别是(F,F,F)/(T,F,T)/(F,T,F)，形状仍3×3。缺失判断检验表示标记，不在猜测某个评分是否合理。
2. 每列True求和均为1；n=3，各比例1/3，保留四位小数为.3333，即约33.33%。类别列也可检查缺失，不必先变数值。
3. 合成以字段名为索引的3×2报告：三行都是`missing=1,ratio=.3333`；筛`missing>0`后仍三行。原表仍三行，原行12/50没被删除。

```mermaid
flowchart TD
    NA0[原表与约定缺失标记] --> NA1[isna得到同形状布尔表]
    NA1 --> NA2[逐列求和；保存原表行数n]
    NA2 --> NA3{n大于零？}
    NA3 -->|否| NA4[报告无样本；比例未定义]
    NA3 -->|是| NA5[计数除以n；组成字段报告]
    NA5 --> NA6[按missing大于0筛报告；原表不变]
```

“未知原因”字符串并不自动等于NaN；业务哨兵值需先明确转换规则，不能把0卧室或评分0一律当缺失。空表n=0时比例无定义，缺失计数0不表示已证明数据完整；缺失数0也不证明没有错值或选择偏差。

**迁移自测**：增加一行完整对象(88,1,t)，缺失数与比例怎样变？有人把报告筛选说成“已删掉缺失房源”，对吗？<details><summary>答案与理由</summary>每列计数仍1，总行数4，比例.25。报告仍三条字段记录，原表保留四行；筛的是报告索引，不是房源行。来源：笔记补充。</details>

**所以呢**：缺失报告只是定位范围，下一步须判断缺失机制与处理代价，再选择删除、保留标记或填补。

**🎙️ 课堂补充**（`01:59:12`–`02:01:20`，约 2.1 分钟，A · 课上展开）

- 切换数据集与确认缺失列（ASR 把 Airbnb 识别成 "LBNB"）：*"[W]e switch to the real data set of [Airbnb], and we know that it contains some missing values in the review[s] [scores] rating..."*（`01:59:19`–`01:59:34`）
- 🎙️ **notebook 没写的处理框架——“删除”与“填补”两条路怎么选**：

> *"[T]he first method... [is] if the number of missing values is very small compared with the whole data[,] and if we remove [them], we will not affect the whole population... we can just remove these... records."*

（`01:59:54`–`02:00:17`）
- 何时该填而不是删：*"[I]f we believe that these records... are very important for us[,] ... we want to keep them, so we need to fill the missing values."*（`02:00:17`–`02:00:33`）
- 缺失计数口头核对（`review_scores_rating` 的具体数字被 ASR 严重压缩，标 [?]）：

> *"[A]mong the whole data set, the host has 40 [profile pic?] pictures, we have 180 missing records. The host identif[ied] 180, and the review score[s rating], we have so many[?] missing values for this col[umn]."*

（`02:00:55`–`02:01:07`）
- **这段改变了什么**：确认了 §3.1 缺失值报告的三列结果（180 / 180 / review_scores_rating 大量缺失）。

新增一条 notebook 没写的决策框架——先判断“删了会不会影响整体分布”，不行再填补，这是本节“为什么选填补而不是删除”的理论依据。

### 3.2 【cell 28–30】三种缺失值填补：均值 / 中位数 / KNN

**这块在干什么**：对 `review_scores_rating` 和 `bedrooms` 各用三种方法填补，比较填补后的分布，选一种。

```python
cols = ['review_scores_rating', 'bedrooms']

imp_mean = SimpleImputer(strategy='mean')
air[['review_scores_rating_mean', 'bedrooms_mean']] = imp_mean.fit_transform(air[cols])

imp_med = SimpleImputer(strategy='median')
air[['review_scores_rating_median', 'bedrooms_median']] = imp_med.fit_transform(air[cols])

imp_knn = KNNImputer(n_neighbors=5)
knn_vals = imp_knn.fit_transform(air[cols])
air['review_scores_rating_knn'] = knn_vals[:, 0]
air['bedrooms_knn'] = knn_vals[:, 1]
```

**逐行**：
- `SimpleImputer(strategy='mean')`：`fit` 时算每列的均值，`transform` 时把 NaN 换成它。`strategy` 还可以是 `'median'`、`'most_frequent'`（众数，类别列用）、`'constant'`。
- `fit_transform(air[cols])` 返回 **numpy 数组**（两列），赋给两个**新列**——原列保留，这样才能比较。
- `KNNImputer(n_neighbors=5)`：对每个有缺失的行，在**其他列**上找 5 个最像的行，用它们该列的均值填。这里 `cols` 只有两列，所以填 `review_scores_rating` 时只看 `bedrooms` 像不像——**邻居的定义很弱**（见易错点）。
- `knn_vals[:, 0]`：numpy 二维数组取第 0 列。

然后 `summary()` 函数对六个新列各算 mean / std / min / max / skew：

**输出**：

下面每行是一种填补后列的摘要。review 的 mean/std 单位为评分分值，bed 的单位为卧室个数；skew（偏度）无单位。

std 按样本分母 n−1 计算，n 是该列填补后有效数。读 review_mean：平均 94.013 分、样本 std 6.899 分、偏度 −3.778；这是均值填补后的分布，未证明缺失评分的真值。

| 列 | mean | std | skew |
|---|---|---|---|
| review_mean | 94.013 | 6.899 | −3.778 |
| review_median | 94.458 | 6.948 | −3.885 |
| review_knn | 94.381 | 6.958 | −3.834 |
| bed_mean / bed_median / bed_knn | 1.272 | 0.855 | 2.005（三者**完全相同**） |

**读法**（cell 29 原文 + 补充）：
- `review_scores_rating` **左偏**（偏度 −3.8，堆在 100 附近）：均值填补把 15,275 个空位全填成 94.01（均值被低分拖低），中位数填补填 96（notebook 没直接打印中位数，`verify_airbnb.py` 实跑：median = 96，mean = 94.013。

另外 15,275 个缺失里有 14,434 个是 `number_of_reviews = 0` 的房源）——中位数描述已观察评分的中心位置。

选择它需要说明缺失机制假设。

填补后的分布接近已观察部分不证明未评论房源具有相同评分，真实缺失值仍未知。
- `bedrooms` 三种结果**一模一样**，因为它**本来就没有缺失值**（cell 27 的报告里没有它）——三个 Imputer 什么都没填。
- notebook 的选择：**两列都用中位数**（"simple and robust"），KNN 是"valid alternative if local similarity matters"。

cell 30 建 `air_clean`：复制一份，把两列替换成中位数版本，`isna().sum()` 确认为 0。

**为什么这么写**：作业第 2.1 题原话："Comparison of mean, median, and KNN (k=5) imputation for `review_scores_rating` and `bedrooms`. Report mean, std, and skewness for each method, and justify your preferred choice."——cell 28–29 就是答案模板。但**作业要你自己写 justify**——照抄 cell 29 那三句会被看出来。

**⚠️ 易错点**：
- **`bedrooms` 没有缺失**——作业题干说 "It contains missing values in `review_scores_rating` and `bedrooms`" 是错的（notebook cell 25 也这么说）。作业里如实指出"bedrooms 无缺失，三种方法结果相同"是正确做法，不要硬编一个差异。
- KNN 的邻居只在 `cols` 那两列里找。

要让 KNN 有意义，应该把 `accommodates`、`bathrooms`、`beds` 等也放进去（`KNNImputer` 会用所有传入的列算距离）。

**KNN距离对参与列的尺度敏感**。

本两列例填评分时距离实际上只用已观察的卧室列，不能把评分差也加进去。

扩展多列后先检查尺度贡献，必要时用训练状态缩放并保留NaN，填后回原单位（§3.4）。

这是 T03 第一个"改参数"点（§5）。
- 用整张表算均值再填补，**测试集的信息会泄漏到训练集**（M02 §2.9.3 的验证集纪律）。作业不要求，但项目里应 `fit` 训练集、`transform` 测试集。

**💡 KNN 填补如何真正执行（笔记补充）**

输入是保留 NaN 的数值矩阵、邻居数 $k$、距离与权重规则；输出是同形状的已填矩阵（全缺失训练列的默认移除策略另述）。`fit` 保存训练矩阵作为供体库，`transform` 为新行找供体；它不是训练一个分类标签模型。以下统一用 $k=2$、均匀权重和 sklearn 默认 `nan_euclidean`，与课件的 k=5 区分。

**先看哪些列能比较**：两行都观察到的列才有真实差值。默认距离把共同列平均平方差外推到全部列的尺度。

| 符号 | 角色 | 本例值 |
|---|---|---|
| $a,b$ | 比较的两行 | 如 r1/r2 |
| $d$ | 总列数 | A/B/C 共 3 |
| $O_{ab}$ | 共同观察列集合 | r1/r2 只有 A |
| $m$ | 共同观察列数 | r1/r2 为 1 |
| $D(a,b)$ | 算出的距离 | 原测量尺度的欧氏型距离 |

$$D(a,b)=\sqrt{\frac d m\sum_{j\in O_{ab}}(a_j-b_j)^2}.$$

读 r1/r2：共同 A 列差平方为 1，乘 $3/1$ 得平方距离 3，开根才是距离。按平方距离排序得到相同近邻。

本步边界：$m=0$ 距离未定义，不给 0。尺度须事先声明；不同单位未经选择不能解释成公平相似性。$d/m$ 是距离估计政策，不保证补回真值。

| 行 | A | B | C |
|---|---|---|---|
| r1 | 1 | 2 | 缺失 |
| r2 | 2 | 缺失 | 6 |
| r3 | 3 | 4 | 9 |
| r4 | 缺失 | 6 | 12 |

**同一输入的完整运行**（所有距离以原始观察值计算，不把刚填出的数再充作观察值）：

1. 填 r1 的 C，先筛出 C 已观察的 r2/r3/r4。一行一个供体，距离只用原观察。

| 供体 | 共同列 | 差平方和 | $d/m$ | 平方距离 |
|---|---|---:|---:|---:|
| r2 | A | 1 | 3 | 3 |
| r3 | A/B | 8 | 3/2 | 12 |
| r4 | B | 16 | 3 | 48 |

逐列读法：共同列决定原差来源；差平方和衡量这些列；乘数校正共同列数；最后一列排序。读 r3：两列各差 2，平方和 8，乘 3/2 得 12。

最近 r2/r3 的 C 为 6/9，均匀权重填 $(6+9)/2=7.5$。填值仍是估计，不成为新增观察。

2. 填 r2 的 B，合格供体 r1/r3/r4。距离平方为3、$\frac32[(2-3)^2+(6-9)^2]=15$、$3(6-12)^2=108$，最近 r1/r3 的 B 为2/4，所以填3。r1刚填的C=7.5**不参与**这次距离。
3. 填 r4 的 A，合格供体 r1/r2/r3。距离平方为48、108、$\frac32[(6-4)^2+(12-9)^2]=19.5$，选 r3/r1，其 A 为3/1，所以填2。
4. 最后矩阵为 r1=(1,2,7.5)、r2=(2,3,6)、r3=(3,4,9)、r4=(2,6,12)；原非缺失项完全保留。三个待填单元都处理完便返回，没有 K-means 那样反复更新到收敛。

```mermaid
flowchart TD
    I0[fit保存训练供体矩阵及列顺序] --> I1[transform接收待填行；记录原缺失位置]
    I1 --> I2{还有待填单元？}
    I2 -->|否| I8[返回填补数组；接回原索引与列名]
    I2 -->|是| I3[按待填列筛非缺失训练供体；计算共同观察距离]
    I3 --> I4{有可定义距离的供体？}
    I4 -->|是| I5[选至多k个最近供体；按约定权重汇总目标列]
    I4 -->|否| I6[用该训练列观察均值；全缺失列按明确策略处理]
    I5 --> I7[只填当前缺失单元；保留原观察距离依据]
    I6 --> I7
    I7 --> I2
```

**为什么是这些供体**：同一行缺 A 或 C，合格供体集合可能不同；“整行找五个邻居”不能免去待填列非缺失条件。均匀权重使输出为所选目标值平均；`weights='distance'` 会让近者更重，不能继续套简单平均。默认算法是相似行共享目标值的局部假设；若实际缺失有系统原因或输入列不相关，距离再精确也可能填偏。

**边界与失败**：定义了距离的供体少于 k 时，用实际可用者，不复制凑够 k。

没有定义距离时，默认回到该训练列均值。

本例全缺失新行得到训练观察均值 (2,4,9)，它没有任何“最近同学”证据。

训练全缺失列默认会被移除。

需要保持形状时，显式 `keep_empty_features=True` 并说明其0占位与缺失信息，不当已估真实值。

尺度不合适会改变邻居顺序。

先用训练观察数据估缩放参数、保留NaN后找邻居，填完再反变换到原单位。

重复距离的 kth 边界没有天然唯一答案，必须固定顺序/版本或报告敏感性。

稀疏区域、错配特征与非随机缺失分别需要检验。

**均值/中位数对照**：训练列 `[1,2,3,100,NaN]` 的均值为26.5、中位数为2.5。SimpleImputer 保存26.5或2.5，此后新缺失值沿用它们；不是把未来样本加入再 fit。二者都把所有缺失填同一个数，会制造集中峰并改变方差，不能只看填后偏度接近原值便证明找回真值。

数值由 `verify_t03_mechanisms.py` 复算（sklearn 1.5.1），输出 `t03-mechanism-results.json`；缺失距离、供体与形状条件回源 🔗 [KNNImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html) 和 [nan_euclidean_distances](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.nan_euclidean_distances.html)（获取：2026-09-30）。

**迁移自测**：同表改为 k=1，r1C/r2B/r4A 分别多少？为何不能用 r1 的新 C 重新挑 r2 的邻居？<details><summary>答案与理由</summary>最小距离对应r2/r1/r3，依次填6/2/3。距离使用原共同观察列，填入值是估计结果，不是增加的新观察；回用会改成另一种迭代填补算法。来源：笔记补充，按上表逐距离复算。</details>

**所以呢**：填补先定义供体与尺度，输出仍是估计数据。下一节保留标记检查极端值，不能把填过的数据自动当作完全可信。

**🎙️ 课堂补充**（`02:01:20`–`02:06:26`，约 5.1 分钟，A · 课上展开）

- `sklearn.impute` 库的口头介绍（ASR “costiller” = scikit-learn）：

> *"[Scikit-learn] dot impute. [B]ut the impute is a library that we can use[,] ... [and] so many tools in the library to impute or to fill the missing values in your data set. So there are two big imputer[s]. One is a simple imputer[,] the other is the K[NN] imputer."*

（`02:01:47`–`02:02:09`）
- `strategy='mean'` 的口头解释：*"[I]f we set the strategy equal to mean, ... it asks the machine to use the mean value of this column to fill the missing value[,] ... [using] all the non-missing values of this column to calculate the average value."*（`02:02:38`–`02:02:55`）
- `fit_transform` 拆两步：*"[F]it transform will do two things. First, the fit will get the mean value of the non-missing vector[s]... So after that, the new columns will have the... average value filled."*（`02:03:19`–`02:03:43`）
- 🔴 **notebook 完全没有的 KNN 类比——用“不知道某学生 GPA，但知道他离哪些同学最近”讲 K 近邻填补**（ASR "hitting around" 疑为 "clustered close to"）：

> *"[T]hat student, I do not know his GPA[,] but I know that he is [close?] around 5 other students, around 10. ... I will use five closest neighbors['] ... average value of the five closest neighbors' GPA to fill the missing value of his missing GPA. ... I only use the neighbors. I will not use the whole population's average."*

（`02:04:56`–`02:05:44`）
- **这段改变了什么**：确认了 §3.2 三种填补方法的操作流程。

新增了“KNN 邻居定义很弱”这条易错点背后教授自己给的直觉类比——K 近邻只看“最像的 k 个”，不看全体，这条类比可以直接写进作业的 justify 段落。

### 3.3 【cell 32–34】两种离群点规则：IQR vs Z 分数

**这块在干什么**：给三列各用两种规则标记离群点，数各有多少个，比较。

```python
def iqr_flag(s, k=1.5):
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    return (s < q1 - k * iqr) | (s > q3 + k * iqr)

def z_flag(s, threshold=3):
    z = (s - s.mean()) / s.std()
    return z.abs() > threshold

for col in ['log_price', 'accommodates', 'bathrooms']:
    print(f"{col}: IQR -> {iqr_flag(air_clean[col]).sum()}, Z-score -> {z_flag(air_clean[col]).sum()}")
```

**逐行**：`quantile`估两个参照位置，`iqr`计算它们的差；`|`逐行合并“低于下界/高于上界”的布尔结果。`z_flag`以本列均值和样本std作尺子，`.abs()>threshold`逐行判断；最后`.sum()`把True当1计数。函数返回与输入索引相同的flag，不会删除数据。

**公式**（IQR与Z规则，实际统计口径就地解释）：

$$\text{IQR 规则：} x < Q_1 - k\cdot\text{IQR} \;\text{或}\; x > Q_3 + k\cdot\text{IQR}\ (k=1.5), \qquad \text{Z 规则：} \left|\frac{x-\bar{x}}{s}\right| > 3$$

| 符号 | 含义 |
|---|---|
| $Q_1, Q_3$、IQR | 25%、75% 分位数与它们的差 |
| $k$ | 须的倍数，Tukey 惯例 1.5 |
| $\bar{x}, s$ | 均值、标准差 |
| 3 | 阈值：正态分布下超过 3 个标准差的概率约 0.27% |

**输出**：

| 列 | IQR 标记 | Z 标记 | 为什么差这么多 |
|---|---|---|---|
| log_price | 1,453 | 453 | Q1 = 4.29，Q3 = 5.19，IQR = 0.90（详见表后） |
| accommodates | 3,299 | 1,378 | Q1 = 2，Q3 = 4，须 −1 到 7；**所有 ≥ 8 人的房源全被 IQR 标记** |
| bathrooms | **14,307** | 1,878 | **Q1 = Q3 = 1 → IQR = 0 → 须就是 [1, 1]**：凡是不等于 1 的浴室数（0、1.5、2……）全被标成离群点——占 21% |

**log_price · 为什么差这么多**

Q1 = 4.29，Q3 = 5.19，IQR = 0.90。

须 2.94–6.55。

两端都有长尾

cell 33：`log_price` 的 IQR 离群比例 = **0.0213**（1,453 / 68,133）；这个 `outlier_iqr` 列留在 `air_clean` 里（作业要求 "keep an `outlier_iqr` flag column"）。

**读法**（cell 34 原文）："IQR usually flags more points because it does not assume a normal distribution. Z-score assumes an approximately Gaussian variable, so it can miss heavy-tail outliers and over-flag variables that are not normal."

**为什么这么写**：作业第 2.1 题原话："Outlier detection on `log_price`, `accommodates`, and `bathrooms` using **both IQR (1.5 × IQR)** and **Z-score (threshold 3)**. Compare the two methods."——这三个数就是答案，但**比较**要你自己写。

`bathrooms` 那一行是最值得写的：**IQR规则在此离散集中列上退化**（IQR=0），许多正常差异也被标记。

Z规则给另一尺度参照，是否更合业务须核查，不能自动判为更合理。

**⚠️ 易错点**：
- `bathrooms` 的 14,307 不是"真的有两万个离群点"，是 IQR 规则退化——作业里指出这点比照抄数字有价值得多。
- Z 分数用的是含离群点的均值和标准差，离群点会"拉大"标准差、掩盖自己（masking）；RobustScaler 用中位数和 IQR 就是为了这个（§3.4）。
- 标记 ≠ 删除。notebook 只加了一列 flag，没有删行；M02 §2.6.4 讲过离群点的两条路（删 / 找解释变量）。

**💡 从一列数据到逐行离群标记（笔记补充）**

输入为一列带原索引的数、IQR 倍数 k 或 Z 阈值；输出是同索引布尔标记及计数。方法没有训练类别或删行；若用于未来样本，必须另存参照阈值。取六值 `[1,2,2,3,4,20]`，按原 notebook 的样本 std 与默认线性分位数：

1. Q1位置1.25，两端2/2，Q1=2；Q3位置3.75，两端3/4，Q3=3.75，IQR=1.75。k=1.5，低界−0.625、高界6.375。
2. 逐值比较低/高界，得到 `False,False,False,False,False,True`；只有20超高界。布尔求和为1，均值为1/6；比较符号是严格小于/大于，恰在界上不会被标记。
3. 同列均值16/3，平方偏差和790/3，样本方差158/3，std≈7.257180。六个Z约为−0.5971/−0.4593/−0.4593/−0.3215/−0.1837/2.0210。阈值3时**一个都不标记**：20自己也拉大了标准差；两法回答的是各自规则，不能由“多数标记”投票得真值。
4. 将Z阈值降为2，20会被标记；将IQR k降为.5，界为1.125/4.625，1与20都被标记。参数变化留下的是规则敏感性，不是数据本身变坏。

```mermaid
flowchart TD
    O0[原列与索引；规则参数] --> O1[单独记录缺失；在参照有效值上估统计量]
    O1 --> O2{采用IQR还是Z？}
    O2 -->|IQR| O3[Q1/Q3与IQR；求两界并检查退化]
    O2 -->|Z| O4[均值与样本std]
    O3 --> O5[逐行比较；保持缺失状态与原索引]
    O4 --> O41{参照数据足够且std有限非零？}
    O41 -->|是| O5
    O41 -->|否| OFAIL[返回退化报告；不将NaN当正常]
    O5 --> O6[返回flag和计数；由业务另决定是否处理]
```

本图是带退化报告的补充流程；原`z_flag`并未实现该守卫，常数列会产生NaN并在比较中变False，不能将其解释为已证明正常。

IQR=0 并非程序无法运行，两界会重合；这样可能把离散变量的正常少数值全部标出。std=0 时 Z 无定义，不应将 NaN 比较得到的 False 当作“已证明无异常”。缺失也不应被 False 静默当正常。Z 可对任何非退化数值列计算，但“3倍标准差对应约0.27%”需要正态分布假设；IQR 与Z哪种更多没有普遍次序。固定阈值用于新样本时不重算，确保评估口径一致。

**迁移自测**：一个新值6.375会被上述IQR规则标记吗？<details><summary>答案</summary>不会，因为比较用严格大于；6.376会。不能为判断一个新值而把它并入原六值重新fit四分位数，那会变成新的参照规则。</details>

**所以呢**：标记给出可检查的原行，方法差异应回到分母、分布与参数解释；选择缩放器时继续保留这些区别。

**🎙️ 课堂补充**（`02:06:26`–`02:07:42`，约 1.3 分钟，B · 讲了同讲义）：教授只是简讲了一遍 IQR 与 Z 分数两条离群点规则的公式，没有给出 Airbnb 三列（`log_price` / `accommodates` / `bathrooms`）任何具体计数或对比结论——

> *"[I]f we want to identify some [outlier] data points, we can use the IQR. I already informed [you] that IQR is Q3 minus Q1. ... [A]lternatively we can use this kind of Z-score[:] ... the X value minus mean value divided by the standard deviation."*

（`02:06:34`–`02:07:21`）与笔记 §3.3 的公式一致。

notebook 里 `bathrooms` 的 IQR=0 退化、14,307 个“离群点”这条最有价值的发现，本段没有口头提及。

### 3.4 【cell 36–37】标准化：StandardScaler vs RobustScaler

**这块在干什么**：五个数值特征量纲不同（`accommodates` 1–16，`review_scores_rating` 20–100），把它们压到可比的尺度上；两种压法，一种用均值 / 标准差，一种用中位数 / IQR。

```python
feats = ['accommodates', 'bathrooms', 'bedrooms', 'beds', 'review_scores_rating']
X = air_clean[feats].copy()
X_std = pd.DataFrame(StandardScaler().fit_transform(X), columns=[f + '_std' for f in feats])
X_rob = pd.DataFrame(RobustScaler().fit_transform(X), columns=[f + '_rob' for f in feats])
print(X_std.describe().T[['mean', 'std', 'min', 'max']])
print(X_rob.describe().T[['mean', 'std', 'min', 'max']])
```

**公式**（cell 35 原文 + 补充）：

StandardScaler 先减训练均值，再除训练总体标准差：

$$z=\frac{x-\mu}{\sigma_0}.$$

RobustScaler 先减训练中位数，再除训练 IQR；IQR=0 的软件政策在输出旁说明：

$$z=\frac{x-\text{median}}{\text{IQR}}.$$

| 符号 | 含义 |
|---|---|
| $\mu,\sigma_0$ | 训练列均值、ddof=0的总体口径标准差（对离群点敏感） |
| median、IQR | 该列的中位数、$Q_3 - Q_1$（对离群点稳健） |
| $z$ | 缩放输出（详见表后） |

**该计算 · 含义**

缩放输出。

非退化训练列的StandardScaler均值0/总体std1，RobustScaler中位0/IQR1。

新数据不保证这些统计量

**逐行**：`fit_transform` 返回 numpy 数组 → 用 `pd.DataFrame(..., columns=[f + '_std' for f in feats])` 接回列名（列表推导式，T02 §3 助教讲过）。

**输出**（StandardScaler）：五列 mean 全是 `e-17` 量级（就是 0，浮点误差）、std 全是 1.000007（分母 n−1 的微小差）；`review_scores_rating_std` 的 min 是 **−10.7**（评分 20 分的房源离均值 10 个标准差），max 只有 0.80。
（RobustScaler）：`accommodates_rob` mean 0.57、min −0.5、max 7；`bathrooms_rob` std 0.56——⚠️ 按定义 IQR = 0 应该除零，sklearn 遇到 IQR = 0 会**把分母置 1**，所以 `bathrooms_rob = bathrooms − 1`，没有报错但也没有"缩放"。

**读法**（cell 37 原文）：StandardScaler 用于"roughly symmetric and outliers are rare"；RobustScaler 用于"have outliers or skewed distributions"。

**为什么这么写**：作业第 2.2 题原话："Apply `StandardScaler` and `RobustScaler` to at least five numerical features (excluding `log_price`). Report mean, std, min, max for both scalers. Explain when each scaler is preferable."——cell 36 输出就是那张表。**讲义 M03 没有讲标准化**，它是为 M04 PCA（对方差敏感，尺度大的列会霸占第一主成分）和 W04 聚类（距离对尺度敏感）铺路的。

**⚠️ 易错点**：
- 标准化**不改变分布形状**（偏度不变），只改位置和尺度；左偏的评分标准化后还是左偏。
- `fit_transform` 用全表统计量，同样有训练 / 测试泄漏问题。
- 标准化后列名要自己接，否则一堆无名数组（cell 36 的 `columns=` 就是在做这件事）。

**💡 fit保存一把尺子，transform给新点用（笔记补充）**

输入是训练矩阵、按列计算的中心与尺度约定；fit 输出可复用的 `mean_/var_/scale_` 或 `center_/scale_` 状态，transform 输出保持行列次序的数值矩阵。缩放不移动样本之间的排序关系，也不把异常值删除。

sklearn StandardScaler 的分母为总体口径 $\sigma_0=\sqrt{\sum_i(x_i-\mu)^2/n}$（ddof=0），不是本篇 Z 离群规则使用的样本 $s$（ddof=1）。

$\mu$ 是训练列平均，$n$ 是有效训练数，$\sigma_0$ 是保存尺度。

只有非零方差训练列，缩放后的总体 std=1。

pandas `describe()` 用样本 std，所以显示 $\sqrt{n/(n-1)}$。

新测试数据并不保证均值0或std1。

RobustScaler 默认保存 median 与Q3−Q1。

IQR非零的训练列才有训练IQR1。

同一训练列 `[10,20,30]`，一个新值40：

| 状态/动作 | StandardScaler | RobustScaler |
|---|---|---|
| fit中心 | mean=20 | median=20 |
| fit尺度 | variance=200/3；scale≈8.164966 | Q1=15，Q3=25；scale=10 |
| transform训练三值 | −1.224745 / 0 / 1.224745 | −1 / 0 / 1 |
| transform新40 | (40−20)/8.164966≈2.449490 | (40−20)/10=2 |
| inverse_transform新输出 | 2.449490×8.164966+20=40 | 2×10+20=40 |

这是一条完整可逆的计算路径。若又拿测试40参加fit，中心会改成25、尺子也变了；之后变的是参照状态，不是先前输出自动被重写。对预测实验先分数据，fit仅训练，在验证/测试上transform；探索整份数据可描述性fit全表，但不得将结果冒充样本外建模过程。

**用新 40 走图**：S0 输入训练 10/20/30，S1 保存均值 20、scale≈8.165。40 到 S2 只减 20、除 8.165，得约 2.449；S3 保行索引，S4 可还原 40。

箭头表示状态依次产生与复用，不让新值回 S1 重训。文字替代：先存训练尺子，新行沿用；下方既有新值 5 自测检验同一路径。

```mermaid
flowchart TD
    S0[训练矩阵；列顺序；尺度规则] --> S1[fit估中心和尺度；保存状态]
    S1 --> S2[transform训练/新行；复用同一状态]
    S2 --> S3[返回同形状数组；保留原索引及列名]
    S3 --> S4[需要原单位时inverse_transform]
```

`pd.DataFrame(array, columns=names, index=X.index)` 才同时接回列名与原行索引；本 notebook 恰为默认连续索引，没有显出遗漏 `index=` 的风险。若删行/排序后索引是31/12/50，新输出仍配这三个标签；重建默认0/1/2再按标签join可能错位。常数列训练scale设1，训练输出0；新值不同于原常数时仍可能不为0。RobustScaler的IQR0也要明确退化尺度策略；它不等于所有含离群数据必优。

**迁移自测**：原尺子不变，新值5得到多少？若新批均值不为0，是程序坏了吗？<details><summary>答案与理由</summary>StandardScaler为−15/8.164966≈−1.837117；RobustScaler为−1.5。新批分布可能不同，复用训练状态不保证新批均值0，这是预期行为；不能为得到0再fit测试集。来源：笔记补充。</details>

数值由 `verify_t03_mechanisms.py` 核对；参数口径回源 🔗 [StandardScaler 文档](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)（获取：2026-09-30）。**所以呢**：尺度与行身份保存好后，计算成对关系时再检查有效成对样本；缩放本身不是因果分析。

**后续概念预告**：主成分分析（PCA）将多列变成组合坐标；第一主成分是训练数据中保留方差最大的单位方向。M04正式推导，本节只说明缩放为什么会影响哪个方向占大方差，不要求现在执行PCA。

**🎙️ 课堂补充**（`02:07:42`–`02:08:48`，约 1.1 分钟，B · 讲了同讲义）：只念了两个公式，没有展开“何时用哪个”的取舍标准，也没有提 Airbnb 五个特征的具体输出——

> *"[F]or the standardization... the actual value [minus] the mean divided by the standard deviation. ... [A]fter... standardization[,] all the columns' mean value will become zero, and the standard deviation will become one. ... [W]e can use... robust scaler... [subtracting] median and divid[ing] it by the IQR."*

（`02:07:56`–`02:08:40`）与笔记 §3.4 的两个公式一致。

`bathrooms_rob` 因 IQR=0 退化成“减 1”这条易错点没有被提及。

### 3.5 【cell 39–42】协方差、相关矩阵、热力图、相关 ≠ 因果

**这块在干什么**：算 7 列（目标 + 6 个数值特征）的协方差矩阵和相关矩阵，画热力图，找与 `log_price` 最相关的特征，然后说一遍"相关不是因果"。

```python
corr_cols = ['log_price', 'accommodates', 'bathrooms', 'bedrooms', 'beds', 'number_of_reviews', 'review_scores_rating']
cov_matrix = air_clean[corr_cols].cov()
corr_matrix = air_clean[corr_cols].corr()
corr_matrix.round(3)

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm'); plt.title('Correlation Heatmap'); plt.show()

air_clean[corr_cols].corr()['log_price'].drop('log_price').sort_values(key=abs, ascending=False).head(5)
```

**逐行**：`df.cov()` / `df.corr()` 一次算所有列两两的协方差 / Pearson 相关（M03 §2.11 的公式，分母 n−1）。

`sns.heatmap(annot=True, fmt='.2f', cmap='coolwarm')`——在格子里标数、两位小数、采用coolwarm色带。

原代码自动色域不保证零居中，颜色先读色标再读数值。

最后一行取 `log_price` 那一列，去掉自己（1.0），**按绝对值**排序（`key=abs`，这样负相关也能排前面），取前 5。

**输出**（相关矩阵，cell 39）：

一行是一项填补后特征与 log_price 的相关，r 无单位，数值沿用原输出。

| 特征 | 与 log_price 的 r |
|---|---:|
| accommodates | 0.578 |
| bedrooms | 0.483 |
| beds | 0.470 |
| bathrooms | 0.377 |
| number_of_reviews | −0.025 |
| review_scores_rating | 0.081 |

读第一行：容量较大房源通常具有较高 log 价格，相关 0.578；没有控制地点等共同因素。第一列给原数值字段身份，第二列来自两列有效成对行，不是美元效应。

原宽表中其它已显示格拆出保留；空格只表示原未展示，不当作 0。

| 列对 | r |
|---|---:|
| accommodates / bathrooms | 0.523 |
| accommodates / bedrooms | 0.724 |
| accommodates / beds | 0.829 |
| accommodates / number_of_reviews | 0.052 |
| accommodates / review_scores_rating | −0.023 |
| bedrooms / bathrooms | 0.609 |
| bedrooms / beds | 0.730 |
| bedrooms / number_of_reviews | −0.032 |
| bedrooms / review_scores_rating | 0.012 |

列对就是该交叉格来源，r 是同口径相关。原对角为各非退化列与自己相关 1；对称格相同，不再横向重复成 8 列宽表。

cell 41 的前 5：accommodates 0.578、bedrooms 0.483、beds 0.470、bathrooms 0.377、review_scores_rating 0.081。`cov_matrix` 算了但没显示（协方差带单位，看不出强弱——M03 §2.11）。

**读法**（cell 42 原文）："A larger `accommodates` is strongly correlated with a higher `log_price`, but size does not *cause* price by itself. **Location, amenities, and demand are confounding factors** that affect both. This is exactly the kind of reasoning required in the assignment."

**为什么这么写**：作业第 2.4 题四条要求（相关矩阵、带数字的热力图、前 3 相关特征、一个混杂变量）逐条对应 cell 39–42。

⚠️ 热力图里 **accommodates–beds 0.829、accommodates–bedrooms 0.724、bedrooms–beds 0.730** 这三个数比与 `log_price` 的相关更值得写——它们提示相关特征可能影响T02 §5.5的条件系数解释。

仅这些相关数不能证明 `beds` 负系数的唯一原因（多重共线性，[[IS6400_Business_Data_Analytics/_meta/数据集卡片#Airbnb.csv|数据集卡片]] §5.1）。

**⚠️ 易错点**：
- 本例显式选七个数值列再 `corr()`，所以`city`、`property_type`没有进入矩阵。

现代pandas默认并不保证混合字符串表自动跳过非数值列——它们与 `log_price` 的关系要用分组箱线图（§2.4）或分组中位数（§2.3）看。
- `review_scores_rating` 与价格相关只有 0.08——这份数据中已填补评分与log价格的线性相关较弱，不能推出所有非线性或分组关系都不存在，作业写 insight 时这是一个反直觉的好例子。
- 热力图的颜色尺度默认按数据范围，两张图不可直接比色；作业要比就固定 `vmin=-1, vmax=1`。

**💡 从三列原行到矩阵、格子与排序（笔记补充）**

输入为数值列矩阵，输出为“列×列”的关系矩阵；对角相关一般为1，但常数列相关无定义。用三行 a=[1,2,3]、b=[2,4,6]、c=[3,2,1]：各均值2/4/2，偏差a=−1/0/1，b=−2/0/2，c=1/0/−1。以样本分母2，协方差矩阵如下。

| cov | a | b | c |
|---|---|---|---|
| a | 1 | 2 | −1 |
| b | 2 | 4 | −2 |
| c | −1 | −2 | 1 |

例如 cov(a,b)=[(−1)(−2)+0+1×2]/2=2；各 std 为1/2/1，相除后相关矩阵为 `[[1,1,-1],[1,1,-1],[-1,-1,1]]`。热力图的(a,c)格来自这两列的−1；只有明确以零为中心的色域，才能将红/蓝对应为正/负，默认颜色先表示当前色标上的大小，不会画出变量发生改变的因果方向。目标为a时，去掉自相关后 b=1、c=−1；按绝对值两者平局，须报告两者或指定平局顺序，不能将负号误当不重要。

pandas在存在缺失时默认按每一对的共同非缺失行计算，两格可能有不同样本数；需要同时列有效数矩阵。先填补再相关也会改变关系，原始观测相关与填补后相关应分开标。全常数/成对不足/混合字符串须先处理，NaN不能转成“关系为0”；0相关也不能证明无非线性关系。正文 M03 §2.11 已展开缺失成对的正/负反例。图若要跨数据对比，明确 `vmin=-1,vmax=1`；固定颜色只统一编码，不消除样本差异。

**一个格怎样读颜色与数值**：只画上述 a/b/c 三行教学表，不重跑 Airbnb 完整预处理。

![[IS6400_Business_Data_Analytics/notes/figures/t03-readability/toy-correlation.svg]]

横纵是列名，格值是两列 Pearson r；色域固定 [−1,1]，0 居中。每格由 3 对有效观测计算，没有因果箭头。

走 (a,c)：a 上升 1→2→3，c 下降 3→2→1；样本 cov=−1，两 std 均 1，所以 r=−1。文字替代：a/b 完全正线性，另两列对完全负线性；有缺失时各格有效数不一定都是 3。

<details><summary>读图自测：c 的 −1 会在绝对值排名里输给 b 的 +1 吗？</summary>

不会，两者绝对值都是 1，平局。符号给方向，绝对值给线性强度；都不证明因果。

</details>

**迁移自测**：把b改为原来的十倍，cov(a,b)与corr(a,b)怎样变？<details><summary>答案</summary>cov从2到20，b的std从2到20，corr仍1。协方差改变单位，相关抵消正尺度；若乘负数则相关符号翻转。来源：笔记补充，逐偏差乘积可核。</details>

**关系矩阵的控制流（笔记补充）**：每个格使用同一对列的有效行；常数列的协方差可为0，但相关无定义，不能将两者一起当缺失或一起填0。

```mermaid
flowchart TD
    CM0[指定数值列与原行] --> CM1[取下一对列；筛共同有效行并保存n]
    CM1 --> CM2{有效数至少2？}
    CM2 -->|否| CM3[记录协方差/相关未定义及原因]
    CM2 -->|是| CM4[各列中心化；偏差乘积和除以n减1得cov]
    CM4 --> CM5{两列std均非零？}
    CM5 -->|是| CM6[cov除以两std得corr]
    CM5 -->|否| CM7[保留cov；corr记NaN]
    CM3 --> CM8[写回对称矩阵及有效数矩阵]
    CM6 --> CM8
    CM7 --> CM8
    CM8 --> CM9{还有未计算列对？}
    CM9 -->|是| CM1
    CM9 -->|否| CM10[矩阵输出；指定色域画图；去自相关再排序]
```

**所以呢**：矩阵每格都应能回到原始成对行，随后再给业务解释；一张红色热力图不能证明某个特征使价格提高。

**术语唤醒（笔记补充）**：条件系数是回归中在其余输入固定的模型条件下解释的系数，不自动等于因果效应。多重共线性是输入列存在完全或较强线性依赖，使分别估计各系数的信息不足或不稳定；两列相关高是线索，不能单独证明某个系数的负号来源。

**原热力图的实际色域检查（笔记补充，2026-10-01）**：本轮用原Airbnb及中位数填补评分后重算7×7矩阵，原代码自动色域为约−0.040035至1；价格/评分相关约+0.08却画成蓝色。因此不能只凭“蓝”判负相关。固定−1至1并以0为中心后，弱正相关才接近中性的浅红色。原notebook和课堂引文保持原样；以下是明确改色域的补充代码，不冒称原代码已有这些参数。

```python
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
            vmin=-1, vmax=1, center=0)
plt.title('Correlation Heatmap with Fixed Color Scale')
plt.show()
```

**逐行**：新建画布；沿用同一`corr_matrix`，三个新增参数只固定颜色映射，不重算相关；最后设置标题再显示。**输出**：实际两版对照已渲染并查看，色域分别为[−0.040035,1]/[−1,1]，矩阵数字相同；见临时`t03-heatmap-check.py`和`t03-heatmap-check.json`。课堂关于红正蓝负的描述可作为零居中图的读法，不能当作此原代码默认色域已保证的性质。

**🎙️ 课堂补充**（`02:08:48`–`02:09:51`，约 1.1 分钟，A · 课上展开）

- 热力图颜色编码的口头说明（notebook 只写了 `cmap='coolwarm'`，没有解释）：*"[T]o see... all the correlation metrics, the [heatmap][:] if they are positively correlated, it's closer to the red[;] if they are negatively correlated... it will be close to the dark blue."*（`02:09:15`–`02:09:24`）
- 相关系数低 ≠ 无关系的补充（ASR "field correlation" 疑为 "zero correlation"）：*"[Z]ero[?] correlation does not mean they do not have [a] relationship[;] maybe they have non-linear correlation, non-linear relationship."*（`02:09:36`–`02:09:41`）
- **这段改变了什么**：确认了 §3.5 热力图与“相关≠因果”的读法。

补上了 notebook 没写的热力图配色规则，以及一条独立于因果问题的提醒——低（线性）相关不代表没有关系，可能是非线性关系。

---

## 4. 完整流程串讲

把 20 个 code cell 串成一条线，就是作业第 2 题的骨架，也是任何新数据集的"体检流程"：

```mermaid
flowchart TD
    A["读数据<br/>read_csv · head · columns"] --> B["认属性类型<br/>名义 / 序数 / 区间 / 比率（M03 §2.3）"]
    B --> C["单变量描述<br/>describe_col · quantile · value_counts"]
    C --> D["分组比较<br/>groupby().agg（= 聚合）"]
    D --> E["画图<br/>hist · boxplot · scatter(按组) · parallel_coordinates"]
    E --> F["数据质量<br/>isna → Imputer 三选一<br/>IQR / Z 标记离群点"]
    F --> G["标准化<br/>StandardScaler / RobustScaler"]
    G --> H["关系<br/>corr · heatmap · 前 3 特征"]
    H --> I["结论<br/>相关 ≠ 因果：说出混杂变量"]
```

**总览读法**：箭头是讲解与处理状态顺序。真实建模先分训练/评估，填补和缩放只在训练内 fit；这项条件不能由总览顺序替代。

缺评分房源到 F：先数缺失、判断机制，再按已声明规则建 air_clean。G 换尺子，不恢复真实缺评分；H 得到处理后的相关。

1. 看分布与业务目标选择中心/尺度，中位数和 RobustScaler 都非无条件更好。
2. 保存图标题、轴、单位和读法，每个数字可回到输入。
3. 缺 22% 是范围；填中位数假设未评论房源具有典型评分。缺失真值仍未知。

<details><summary>总览自测：经过 G，缺评分已经是真实观察吗？</summary>

没有。F 只是估计，G 只改尺度；后续关系仍须承认填补假设。

</details>

---

## 5. 自己动手 —— 改哪个参数会发生什么

| 改什么 | 改成 | 会看到 | 学到 |
|---|---|---|---|
| cell 14 `bins=20` | `bins=5` / `bins=50` | 5 箱看不到多峰；50 箱全是锯齿 | 直方图形状随箱数变（M03 p.63） |
| cell 20 分组散点的两列 | `sepal length` × `sepal width` | 三类混在一起 | 特征的"可分性"不同 → M04 特征重要性 |
| cell 23 列顺序 | `data[['sepal width','sepal length','petal length','petal width','class']]` | 三束从第二根轴就分开（讲义 p.70 右图） | 平行坐标轴序重要 |
| cell 28 `KNNImputer` 的输入 | 加上 `accommodates, bathrooms, beds` | `review_knn` 的 mean / skew 会变 | KNN 的"邻居"由传入的列决定 |
| cell 28 `n_neighbors=5` | 1 / 50 | 1 个邻居噪声大；50 个邻居趋近全局均值 | k 的偏差–方差权衡 |
| cell 32 `k=1.5` | `k=3` | IQR 标记数大幅下降 | 须的倍数是主观门槛 |
| cell 32 `threshold=3` | `2` | 按固定参照尺度，降阈值会使标记数不减少；Airbnb实际比例须复算，约4.6%仅是理想正态下的理论双尾比例 | 正态下 2σ 外约 4.6% |
| cell 32 的列 | 加 `number_of_reviews` | IQR 会标出几千个 | 右偏计数变量的"离群点"其实是长尾 |
| cell 36 `feats` | 加 `log_price` | 也被标准化——但作业明说 excluding `log_price` | 目标变量通常不标准化（要保留可解释性） |
| cell 40 `cmap` | `'RdBu_r'`，加 `vmin=-1, vmax=1` | 颜色与相关值固定对应 | 多图可比 |
| cell 41 `key=abs` | 去掉 | `number_of_reviews`（−0.025）排到最后 | 负相关也是相关 |

---

## 6. 与讲义理论的对应

| notebook cell | 讲义 M03 页 | 概念 |
|---|---|---|
| 2（object / attribute） | p.4 | 对象与属性 |
| 3 `read_csv(header=None)` | p.61 | Iris 数据集 |
| 5–7 描述统计 | p.24–26 | 集中趋势、分位数、IQR |
| 6 skew / kurt | p.27–28 | 偏度、峰度 |
| 10 `value_counts` | p.23 | 类别变量计数 |
| 11 `groupby().agg` | p.22（pivot）、p.51（聚合） | 表 / 聚合 |
| 14 直方图 | p.63 | 分箱 |
| 17 箱线图 | p.65–66 | 分位数、离群点 |
| 20 散点图 | p.67–68 | 用颜色加第三属性 |
| 23 平行坐标 | p.69–70 | 高维可视化 |
| 27 缺失值 | p.19 | 数据质量：missing values |
| 28 三种填补 | p.19（"What can we do about these problems?"） | 讲义只提问，notebook 给答案 |
| 32 离群点 | p.19、p.26 | noise and outliers；IQR |
| 36 标准化 | —（讲义无；M04 PCA 前置） | 尺度 |
| 39 `cov()` / `corr()` | p.30–33 | 协方差、相关 |
| 42 相关 ≠ 因果 | p.34 | 混杂变量 |
| 44–48 作业 | 全讲 | — |

---
## 7. 本次作业：Week 3 Assignment（notebook cell 44–48 原文）

> ⚠️ **本周没有 AI Prompt 单元格**——T01 有 7 个、T02 有 1 个整段 prompt，本 notebook 一个都没有。但 ILO 3 "Manage GenAI tools for … Python programming" 没变，官方 GenAI 政策也允许在作业里用 AI。**建议**：把 cell 45–47 的题干直接当 prompt 用（它们本身就写成了"要什么、用什么列、报什么数、什么格式"的四要素形式，见 T01 §6.2），让 AI 生成骨架，再逐格核对数字——**核对数字这一步不能省**，因为本 notebook 已经有一处题干与数据不符（`bedrooms` 无缺失）。

### 7.1 原文（一字不改）

**cell 44**
> # IS6400 Week 3 Assignment
> **Total: 100 points**
> **Submit:** `.ipynb` and exported `.html`.
> **Data:** `Airbnb.csv` for Q1 and Q2. Your own project dataset for Q3.
> You may use `pandas`, `numpy`, `matplotlib`, `seaborn`, `sklearn`.
> All code must be reproducible. Set random seeds where needed.

**cell 45 · Question 1 – Descriptive Analytics on Airbnb (35 points)**
> Produce a complete descriptive report of `Airbnb.csv`. Your report must include:
> - **Attribute type table** for every column: nominal / ordinal / interval / ratio; discrete / continuous; symmetric or asymmetric binary. Include one short reason per column.
> - **Full descriptive statistics** for every numerical variable: mean, median, mode, std, min, max, Q1, Q3, IQR, skewness, kurtosis.
> - **Frequency and percentage tables** for every categorical variable.
> - **Percentile analysis** on both `log_price` and `price = exp(log_price)`: report the 25th, 50th, 75th, 90th, 95th and 99th percentiles. Explain why the percentiles of `price` are **not** simply `exp()` of the percentiles of `log_price`.
> - **Group comparison:** for each `city` and each `property_type`, report mean, median, std and IQR of `log_price`. Identify which city and which property type show the highest median price and the highest variability.
> - **At least 5 insights**, each citing a specific number from your tables.
>
> **Presentation:** structure your answer as a short analytical report (markdown cells + code + tables), not as a list of tiny tasks.

**cell 46 · Question 2 – Data Quality, Visualization, and Relationships with `log_price` (45 points)**
> Perform a full exploration of the relationship between features and the target `log_price`, together with data quality handling. Your answer must include:
> **2.1 Data quality**
> - Missing-value report for all columns.
> - Comparison of **mean**, **median**, and **KNN (k=5)** imputation for `review_scores_rating` and `bedrooms`. Report mean, std, and skewness for each method, and justify your preferred choice.
> - Outlier detection on `log_price`, `accommodates`, and `bathrooms` using **both IQR (1.5 × IQR)** and **Z-score (threshold 3)**. Compare the two methods.
> - Build `air_clean` using your preferred imputation and keep an `outlier_iqr` flag column.
> **2.2 Standardization**
> - Apply `StandardScaler` and `RobustScaler` to at least five numerical features (excluding `log_price`).
> - Report mean, std, min, max for both scalers. Explain when each scaler is preferable.
> **2.3 Feature–target relationships**
> - For each of the following features, describe its relationship with `log_price` using **one statistic and one plot**: `property_type`, `accommodates`, `bathrooms`, `review_scores_rating`, `bedrooms`, `beds`.
> - Each plot must have a title, axis labels, and 2–3 sentences of interpretation.
> **2.4 Correlation and causation**
> - Compute the correlation matrix for `log_price` plus all numerical features you used above.
> - Plot a heatmap with annotated values.
> - Identify the top 3 features most correlated with `log_price`.
> - Pick one of them and explain why the correlation does **not** imply causation. Provide a concrete confounding variable.
>
> **Presentation:** at least **8 plots** in total; each with title, labels, and interpretation. The narrative should read as a coherent exploration, not as disjoint answers.

**cell 47 · Question 3 – Project Dataset Exploration (20 points)**
> Import the dataset you may use for your course project. Deliver a short structured report containing:
> - Shape, dtypes, missing values.
> - Attribute type table: for every column, nominal / ordinal / interval / ratio and discrete / continuous.
> - Choose **at most three** variables and explore their relationships with summary statistics and plots.
> - Write a 150–200 word paragraph explaining what you learned and how it could inform later modeling.
> **Note:** Different group members must use different variables if working in a group.

**cell 48 · Submission Checklist**
> - `ipynb` file with all cells executed.
> - Exported `HTML` file.
> - All plots have titles, axis labels, and interpretations.
> - All code is reproducible.
> - The submission is well-structured and easy to follow.

### 7.2 三件先要知道的事

1. **截止日不在 notebook 里，在 Canvas 上**：✅ **Assignment Week 3 · Due Sep 25 at 11:59pm · 10 pts**（2026-09-16 Canvas 截图）——比"下周上课前"晚两天，与 W2 一样是上课后第 9 天的周五。迟交每天 −20%。
2. **提交两个文件**：`.ipynb` **和** `.html`（T01 只要 HTML、T02 要 html + pdf，每周不一样）。导出：`File → Save and Export Notebook As → HTML`；交之前 `Kernel → Restart & Run All`，让 cell 编号从 1 连续到底（"all cells executed"）。
3. **Q3 要你自己的项目数据**——也就是说**到 W3 就必须已经有一份候选数据集**（[[IS6400_Business_Data_Analytics/_meta/作业与DDL|作业与DDL]] §3.5 的选题）。没有的话至少先从 Kaggle / UCI 下一份能代表你选题方向的公开数据；且"不同组员用不同变量"，组内先分工。

### 7.3 逐题攻略

**Q1（35 分）—— 用 M03 §2.3 + T03 §2.2–2.3**

| 要求 | 用哪个 cell 改 | 坑 |
|---|---|---|
| 属性类型表（15 列，三套标签 + 一句理由） | 手写 markdown 表 | 三套标签都要：名义/序数/区间/比率、离散/连续、**对称/非对称二元**（`cleaning_fee`、`host_has_profile_pic` 是二元——"是否收清洁费"两个值同等重要 → 对称；⚪ 若把"有头像"当作只有 1 才重要也可论证为非对称，写理由即可）。`id` 名义、`log_price` 区间、`price` 比率、`cancellation_policy` 序数。答案骨架见 M03 §2.3 💡 与 §7 概念题 1 |
| 全部数值列 11 个统计量 | cell 5–6 的 `describe_col`，把 `cols` 换成 Airbnb 的数值列（`log_price, accommodates, bathrooms, number_of_reviews, review_scores_rating, bedrooms, beds`；`id` 不算） | `review_scores_rating` 有 NaN，pandas 统计会自动跳过，但要说明 |
| 类别列频数 + 百分比 | cell 10，对 `property_type, bed_type, cancellation_policy, cleaning_fee, city, host_has_profile_pic, host_identity_verified` 各做一次 | `value_counts(normalize=True)` 是比例，乘 100 才是百分比 |
| `log_price` 与 `price` 六个分位数 + 解释 | cell 7，`air['price'] = np.exp(air['log_price'])` | ⚠️ **题设有坑，见下** |
| 按 `city` / `property_type` 的 mean / median / std / IQR | cell 11 的 `groupby().agg`，IQR 要自定义：`lambda s: s.quantile(.75) - s.quantile(.25)` | 实跑（`verify_airbnb.py`）：**中位数最高的城市是 SF（5.075 → 约 \$160）**，**标准差最高的城市是 DC（0.816）**；**中位数最高的房型是 Loft（4.977）**，**IQR 最大的房型是 House（1.173）**——把这些数写进 insight |
| ≥ 5 条 insight，每条引一个数 | — | 例："22.4% 的房源没有评分，其中 94% 是零评论房源"；"SF 中位价最高但 DC 价差最大"；"评分与价格相关仅 0.08" |

⚠️ **分位数换算要区分样本事实与一般规则**：本轮只读复算Airbnb六个指定分位数，`price.quantile(q)`与`exp(log_price.quantile(q))`在这份数据上相等（73/110/180/299/412/950）；这是相关排序位置的取值/并列情况，不是所有pandas线性插值都与exp交换。💡反例：log值[0,2]，先在价格[1,exp(2)]上取中位数，得(1+exp(2))/2≈4.194528；先取log中位1再exp，得exp(1)≈2.718282。exp单调保证排序不变，但不保证两种插值相同。报告应保留实际数据相等结果，同时解释一般为何可能不同；均值与标准差另有不同的换算问题，不能把“题干真正想考什么”当事实。复算材料：`airbnb-quantile-recheck.json`与`verify_t03_mechanisms.py`。

**Q2（45 分，分值最重）—— 几乎就是 cell 25–42**

| 小题 | cell | 必须自己加的 |
|---|---|---|
| 2.1 缺失报告 | 27 | 报**所有列**（含缺失为 0 的）：`air.isna().sum()` 不加 `[missing > 0]` |
| 2.1 三种填补比较 | 28–29 | **如实写 `bedrooms` 无缺失、三法相同**；对 `review_scores_rating` 用偏度（−3.78 / −3.88 / −3.83）和"缺失机制 = 无评论"论证选中位数；⚪ 加分：KNN 时把 `accommodates, bathrooms, beds` 也传进去，看结果怎么变 |
| 2.1 离群点两法比较 | 32–33 | 解释 `bathrooms` 14,307 是 IQR = 0 的退化；Z可计算于任何非退化数值列；正态条件只支持3倍std约0.27%的尾概率解释；`accommodates` 的 IQR 把 ≥ 8 人全标掉（3,299 个） |
| 2.1 `air_clean` + `outlier_iqr` | 30, 33 | 列名必须叫 `outlier_iqr`（题干原话） |
| 2.2 两种 scaler | 36–37 | 五列 mean/std/min/max 两张表；说明 `bathrooms` 的 IQR = 0 让 RobustScaler 退化为减 1 |
| 2.3 六个特征 × (一个统计量 + 一张图) | 11 + 14/17/20 | `property_type` → 分组中位数 + 分组箱线图；五个数值特征 → 相关系数 + 散点图（`alpha` 调低）或按取值分组的箱线图（`accommodates` 只有 1–16 这几个值，分组箱线图比散点清楚）。**每图 title / xlabel / ylabel + 2–3 句** |
| 2.4 相关矩阵 + 热力图 + top 3 + 混杂变量 | 39–42 | top 3 = accommodates 0.578、bedrooms 0.483、beds 0.470；混杂变量写**地段 / 城市**（大房子集中在贵城市）或**房型**；顺手指出 accommodates–beds 0.829 的共线性 |
| ≥ 8 张图 | — | 2.3 就有 6 张 + 热力图 + 至少 1 张分布图（`log_price` 直方图）= 8；每张都要解释 |

**Q3（20 分）—— 用 Q1 的方法套自己的数据**

- `df.shape`、`df.dtypes`、`df.isna().sum()` 三行；属性类型表（两套标签）；**最多三个**变量，用 `describe_col` + 一两张图（分布 + 关系）；150–200 词的段落——写"看到了什么分布 / 关系 / 质量问题，所以建模时打算怎么处理（取对数？填补？删列？）"。
- 这题其实是 **Project Proposal 的 Dataset Description 部分**（Guideline 要求"字段名 + 数据类型"）的预演——写好了直接复用。

### 7.4 提交前自查

- [ ] `Restart & Run All` 无报错，cell 编号连续
- [ ] `.ipynb` + `.html` 两个文件
- [ ] 每张图三件套 + 解释；总数 ≥ 8
- [ ] Q1 ≥ 5 条 insight 各引一个数字
- [ ] `air_clean` 里有 `outlier_iqr` 列
- [ ] 随机种子（若用了抽样 / KNN 以外的随机操作）
- [ ] 报告式的 markdown 叙述，不是"任务 1 / 任务 2"清单

---

## 8. cell ↔ 讲义页码映射 · 课堂覆盖

**20 个 code cell 全部在 §2–§3 有讲解**；28 个 markdown cell 中，cell 1、2、4、8、9、12、13、15、16、18、19、21、22、24、25、29、31、34、35、37、38、42、43 的内容已并入对应小节，cell 44–48 见 §7。「课堂覆盖」列来自 `M03-transcript.txt` tutorial 段（2026-09-18 合并）。

| cell | 类型 | 内容 | 笔记小节 | 讲义页 | 课堂覆盖 |
|---|---|---|---|---|---|
| 1 | md | 标题与八项清单 | §0 | — | ✅ 简讲 `01:46:09`–`01:46:40`（口头概述本讲八件事） |
| 2 | md | object / attribute | §2.1 | p.4 | ✅ 详讲 `01:46:56`–`01:46:58` |
| 3 | code | import · 样式 · 读 iris | §2.1 | p.61 | ✅ 详讲 `01:46:42`–`01:48:59` |
| 4 | md | 描述统计说明 | §2.2 | p.24 | ⚡ 一句带过（并入 cell 5 讲解） |
| 5 | code | `describe_col` | §2.2 | p.24–26 | ✅ 详讲 `01:49:04`–`01:51:08` |
| 6 | code | 四列汇总表 | §2.2 | p.24–28 | ✅ 详讲 `01:51:08`–`01:51:49` |
| 7 | code | 六个分位数 | §2.2 | p.25 | ✅ 详讲 `01:51:49`–`01:52:11` |
| 8 | md | 偏度峰度读法 | §2.2 | p.27–28 | ✅ 详讲 `01:52:11`–`01:52:51` |
| 9 | md | 频数与分组说明 | §2.3 | p.23 | ⚡ 一句带过（并入 cell 10 讲解） |
| 10 | code | `value_counts` | §2.3 | p.23 | ✅ 详讲 `01:52:51`–`01:53:41` |
| 11 | code | `groupby().agg` | §2.3 | p.22, p.51 | ✅ 简讲 `01:55:18`–`01:55:48` |
| 12 | md | insight | §2.3 | — | ⏭️ 没有专门念 insight 原文，前后 `01:55:11`→`01:55:18` 直接跳到 groupby 演示 |
| 13 | md | 4.1 标题 | §2.4 | — | ⚡ 隐含（标题未单独念） |
| 14 | code | 直方图 | §2.4 | p.63 | ✅ 详讲 `01:55:48`–`01:56:41` |
| 15 | md | 多峰 = 混合 | §2.4 | p.63 | ⏭️ 没有念“多峰=混合”这条 insight，`01:56:41` 直接转到箱线图 |
| 16 | md | 4.2 标题 | §2.4 | — | ⚡ 隐含 |
| 17 | code | 箱线图 | §2.4 | p.65–66 | ✅ 详讲 `01:56:41`–`01:57:10` |
| 18 | md | 读法 | §2.4 | — | ⏭️ 没有念 "no obvious extreme outliers"，`01:57:10` 直接转到散点图 |
| 19 | md | 4.3 标题 | §2.4 | — | ⚡ 隐含 |
| 20 | code | 分组散点 | §2.4 | p.67–68 | ✅ 详讲 `01:57:10`–`01:58:00` |
| 21 | md | 强且非线性 | §2.4 | p.33 | ⏭️ 没有念“强且非线性”这条 insight，`01:58:00` 直接转到平行坐标 |
| 22 | md | 4.4 标题 | §2.4 | — | ⚡ 隐含 |
| 23 | code | 平行坐标 | §2.4 | p.69–70 | ✅ 详讲 `01:58:07`–`01:59:07` |
| 24 | md | 读法 | §2.4 | — | ⏭️ 没有专门念读法，`01:59:07` 直接切换到 Airbnb |
| 25 | md | 切换到 Airbnb | §3.1 | p.5, p.19 | ✅ 简讲 `01:59:12`–`01:59:19` |
| 26 | code | 读 Airbnb | §3.1 | p.5 | ✅ 简讲 `01:59:19`–`01:59:34` |
| 27 | code | 缺失报告 | §3.1 | p.19 | ✅ 详讲 `01:59:34`–`02:01:14` |
| 28 | code | 三种填补 | §3.2 | p.19 | ✅ 详讲 `02:01:20`–`02:04:20`（mean/median 两种 SimpleImputer） |
| 29 | md | 解读与选择 | §3.2 | — | ⏭️ 没有念选中位数的理由，只讲了操作步骤 |
| 30 | code | `air_clean` | §3.2 | — | ✅ 简讲 `02:06:26`（“no missing value from the original data table”） |
| 31 | md | 6 标题 | §3.3 | — | ⚡ 隐含 |
| 32 | code | IQR / Z 标记 | §3.3 | p.19, p.26 | ✅ 简讲 `02:06:26`–`02:07:21`（只讲公式，无 Airbnb 具体数字） |
| 33 | code | `outlier_iqr` 比例 | §3.3 | — | ⏭️ 没有提 `outlier_iqr` 具体比例数字 |
| 34 | md | 两法比较 | §3.3 | — | ⏭️ 没有专门比较两法结论 |
| 35 | md | 两种 scaler 定义 | §3.4 | —（讲义无） | ✅ 简讲 `02:07:42`–`02:08:04` |
| 36 | code | 标准化 | §3.4 | — | ✅ 简讲 `02:08:04`–`02:08:31` |
| 37 | md | 何时用哪个 | §3.4 | — | ⏭️ 没有展开“何时用哪个”的取舍标准 |
| 38 | md | 协方差 / 相关定义 | §3.5 | p.30–32 | ✅ 简讲 `02:08:48`–`02:09:11` |
| 39 | code | `cov` / `corr` | §3.5 | p.30–33 | ✅ 简讲 `02:09:04`–`02:09:15` |
| 40 | code | 热力图 | §3.5 | — | ✅ 简讲 `02:09:15`–`02:09:28` |
| 41 | code | top 5 相关 | §3.5 | — | ⏭️ 没有提 top 5 相关系数具体数字 |
| 42 | md | 相关 ≠ 因果 | §3.5 | p.34 | ✅ 详讲 `02:09:28`–`02:09:51` |
| 43 | md | Wrap-up | §4 | — | ✅ 简讲 `02:09:51`–`02:10:18` |
| 44–48 | md | Week 3 Assignment + 清单 | §7 | — | ✅ 详讲 `02:10:22`–`02:13:18`（Q1/Q2/Q3 口头交代，含 TA 出题背景与 Q3 同组不同变量规则） |

**课堂时间分配**（tutorial 段 `01:45:33 → 02:13:18`，约 28 分钟（同一份 `M03-transcript.txt`），按时间戳）：

| 内容块 | 时间戳 | 用时 | 占比 |
|---|---|---|---|
| 开场：tutorial 预告与本讲内容概述 | `01:45:33`–`01:46:42` | ~1.1 min | 4.1% |
| cell 3 读 iris 数据、命名列 | `01:46:42`–`01:48:59` | ~2.3 min | 8.3% |
| cell 5–8 描述统计函数、偏度峰度 | `01:49:04`–`01:52:51` | ~3.8 min | 13.7% |
| cell 10–11 频数/分组统计 + 类别不平衡举例 | `01:52:51`–`01:55:48` | ~3.0 min | 10.8% |
| cell 14–23 四种图 | `01:55:48`–`01:59:12` | ~3.4 min | 12.3% |
| cell 26–27 切换 Airbnb、缺失值报告 | `01:59:12`–`02:01:20` | ~2.1 min | 7.6% |
| cell 28–30 三种缺失值填补（含 KNN GPA 类比） | `02:01:20`–`02:06:26` | ~5.1 min | 18.4% |
| cell 32–34 IQR / Z-score 离群点 | `02:06:26`–`02:07:42` | ~1.3 min | 4.7% |
| cell 36–37 两种标准化 | `02:07:42`–`02:08:48` | ~1.1 min | 4.0% |
| cell 39–42 协方差/相关/热力图/相关≠因果 | `02:08:48`–`02:09:51` | ~1.1 min | 4.0% |
| cell 43 总结 | `02:09:51`–`02:10:22` | ~0.5 min | 1.8% |
| cell 44–48 Week 3 作业口头交代 | `02:10:22`–`02:13:18` | ~2.9 min | 10.5% |


---

## 9. 延伸与勘误

### 9.1 notebook 有但课上略过

| 讲义页 | 内容 | 课上处理 | 笔记处理 |
|---|---|---|---|
| cell 12 | insight（petal length 比 sepal width 更能区分品种） | ⏭️ 没有专门念这句结论，`01:55:11`→`01:55:18` 直接跳到 groupby 演示 | ⚪ 内容仍成立，读者按 notebook 原句理解即可 |
| cell 15 | “多峰=可能是混合总体”读法 | ⏭️ 讲完直方图后 `01:56:41` 直接转箱线图，没有念这条解读 | ⚪ 保留在正文，属于笔记补充性质的解读，不降权 |
| cell 18 | “No obvious extreme outliers” | ⏭️ 没有念，`01:57:10` 直接进入散点图 | ⚪ 原notebook这一读图判断可保留，但默认1.5×IQR与教授口头10/90百分位不是同一须口径（见§2.4），不据此宣称二者相符 |
| cell 21 | “strong and nonlinear”结论 | ⏭️ 没有念，`01:58:00` 直接转平行坐标 | ⚪ 与 §3.5 🎙️ 里“低相关不代表无关系”的口头提醒逻辑一致，保留 |
| cell 29 | 选中位数而非均值/KNN 的理由 | ⏭️ 只讲了 SimpleImputer/KNNImputer 怎么操作，没有口头给出“为什么选中位数” | ⚠️ 作业要求自己 justify，教授没有代劳，读者仍需自己论证（笔记 §3.2 已给论证） |
| cell 33/41 | `outlier_iqr` 比例、top 5 相关系数等具体输出数字 | ⏭️ 只讲操作步骤和公式，没有口头核对任何具体数字 | ⚪ 以 notebook 输出与 `verify_airbnb.py` 复核结果为准 |

### 9.2 课上讲了但 notebook 没有

| # | 内容 | 时长 | 时间戳 | 小节 | 为什么值钱 |
|---|---|---|---|---|---|
| 1 | 🔴 **KNN 填补的“不知道 GPA 但知道最近 5 个同学”类比** | ~48 s | `02:04:56`–`02:05:44` | T03 §3.2 | 完整解释了 K 近邻填补“只看最像的 k 个，不看全体”的直觉，notebook 和讲义都没有；可直接写进作业的 justify 段落 |
| 2 | 🔴 **银行“正常交易 vs 欺诈交易”讲类别不平衡** | ~34 s | `01:54:07`–`01:54:41` | T03 §2.3 | 解释了“三类各占 33.3%”为什么值得注意——真实数据常不平衡，这是选模型前的必要一步；notebook 完全没有这段 |
| 3 | ⭐ **缺失值“删 vs 填”的决策框架** | ~39 s | `01:59:54`–`02:00:33` | T03 §3.1 | notebook 直接跳到三种填补方法，没有说明什么时候该删、什么时候该填；这段补上了决策依据 |
| 4 | ⭐ **箱线图离群点用 10/90 百分位而非 1.5×IQR 的口头说法** | ~9 s | `01:56:58`–`01:57:07` | T03 §2.4 | 直接回应本笔记 §9.5 ⑤ 的悬案——教授描述的须与 `data.boxplot()` 实际默认（1.5×IQR）不是同一套口径，作业里要注明用哪种 |
| 5 | ⚪ **热力图颜色编码口头说明** | ~9 s | `02:09:15`–`02:09:24` | T03 §3.5 | notebook 只写了 `cmap='coolwarm'`，没解释红/深蓝分别代表什么 |
| 6 | ⚪ **`describe()` 要到下一讲才正式教** | ~10 s | `01:51:29`–`01:51:39` | T03 §2.2 | 说明手写 `describe_col` 是过渡写法，给出了时间线信息 |
| 7 | ⚪ **原始数据无表头的业务背景** | ~12 s | `01:47:53`–`01:48:05` | T03 §2.1 | 解释了为什么公司会把“纯数值表”和“字段名对照表”分开存 |

### 9.3 notebook 自身的问题

| # | cell | 问题 | 处理 |
|---|---|---|---|
| ① | 25、46 | 说 Airbnb "contains missing values in `review_scores_rating` **and `bedrooms`**"——**`bedrooms` 实际没有缺失**（cell 27 的输出里就没有它；`verify_airbnb.py` 实跑 0 缺失），所以 cell 28 对 `bedrooms` 的三种填补结果完全相同 | 作业里如实指出 |
| ② | 45 | 原题询问price分位数为何不能普遍直接exp换算；本数据六个指定分位恰相等，但样本线性插值一般不与exp交换，不能虚构本数据差异或把相等推广为一般定理 | 答法见 §7.3 Q1 |
| ③ | 32 | `bathrooms` 的 IQR = 0，1.5×IQR 规则退化，标出 14,307 个（21%）"离群点" | notebook 未解释；作业要写 |
| ④ | 36 | `bathrooms_rob` 的分母 IQR = 0，sklearn 静默置 1 | notebook 未解释 |
| ⑤ | 28 | KNN只传两列，填评分时仅靠卧室定义邻居；这一单一观察维度的正缩放不改变邻居顺序，增加多列后须检查尺度 | §3.2 易错点 |
| ⑥ | 3 | `np.random.seed(42)` 在本 notebook 里没有被任何随机操作用到 | 无害；作业模板 |
| ⑦ | 1 | 自称 "follows the original 'Week 3 - Description' notebook"——说明这是**改写版**，原版（可能带 AI Prompt cell）没有发 | 与 T01/T02 风格不同的原因 |
| ⑧ | 35 | 旧记录列 Week 4 kernel 为 Python 3.7.6，本周为 3.13.5；版本不同不能证明制作年份 | 保留历史版本记录；当前 T04 的 43-cell 源 metadata 为 Python 3.9.12，详见 [[T04-特征选择与PCA实战-Iris]] §9.3 |

### 9.4 课外补充

| 主题 | 内容 | 来源 |
|---|---|---|
| `SimpleImputer` 的 `strategy` | `'mean'` / `'median'` / `'most_frequent'` / `'constant'`（配 `fill_value`）；类别列只能用后两种 | 🔗 scikit-learn 文档常识，2026-09-16 |
| `KNNImputer` | 用 `nan_euclidean` 距离在传入的所有列上找邻居；`weights='distance'` 可按距离加权；对尺度敏感，通常先标准化 | 🔗 同上 |
| RobustScaler 的默认分位 | 默认 `quantile_range=(25.0, 75.0)` 即 IQR；IQR = 0 的列分母置 1（`_handle_zeros_in_scale`） | 🔗 同上 |
| 相关矩阵与多重共线性 | accommodates–beds 0.829 等三对 > 0.7，可作为T02 §5.5条件系数诊断的候选线索，不能仅凭相关数证明负号原因；可用方差膨胀因子（VIF，`statsmodels.stats.outliers_influence.variance_inflation_factor`）量化 | 本库 + 🔗 统计通识 |
| Jensen 不等式 | 对凸函数 exp，$E[e^X] \ge e^{E[X]}$，所以 mean(price) = 158.6 > exp(mean(log_price)) = 118.5；分布分位的保序性质与样本线性插值须区分；样本中位数也可能不与exp交换（§7.3给反例） | 🔗 概率论通识，2026-09-16 |
| 本笔记的实跑 | `verify_airbnb.py`：分位数、缺失、离群点计数、相关、分组统计全部在原始 `Airbnb.csv` 上复核与 notebook 输出一致 | scratchpad |

### 9.5 待核对

| # | 事项 | 说明 |
|---|---|---|
| ① | ~~Week 3 作业截止日、Canvas 占分~~ | ✅ 9/25（五）23:59，Canvas 10 分（2026-09-16 截图）；上传的文件类型限制待上传时看 |
| ② | ~~转录~~ | ✅ 2026-09-18 已合并 tutorial 段（`01:45:33`–`02:13:18`）：§8 课堂覆盖列、§9.1–9.2、9 个 🎙️ 格 |
| ③ | Q1 分位数题的出题本意 | 实跑分位数一致；是出题人笔误还是想考均值 / 插值——**建议课上或 Canvas 讨论区问一句**，答题时两种可能都覆盖（§7.3） |
| ④ | Q3 的项目数据集 | 需要用户自己的选题；本笔记无法代写 |
| ⑤ | 讲义 p.65 须（10/90 百分位）与 notebook 箱线图（1.5×IQR）口径不同 | 作业里注明用哪种 |
| ⑥ | ✅ **本片段转录已核对（shard_3，`01:45:33`–`02:13:18`）** | 段 [1056]–[1359]，共 304 段，时长约 27 分 45 秒；无时序倒退；本片段内无 ≥120 秒空档 |
| ⑦ | 〔?〕`review_scores_rating` 缺失计数被 ASR 压缩，听不出具体数字 | `02:00:55`–`02:01:07` 只留下“review score 18”一类残缺读数，与[[IS6400_Business_Data_Analytics/_meta/数据集卡片#Airbnb.csv\|数据集卡片]] §3 的 15,275（22.42%）明显不符；笔记数字以数据集卡片与 `verify_airbnb.py` 复核结果为准，转录原文标 [?] 不采信 |
| ⑧ | 〔?〕“board transactions”疑为 “fraud transactions” | `01:54:07`–`01:54:15`，按上下文（银行“正常交易 vs 极少数被标记的交易”）推断为 fraud，未能 100% 确认，笔记引文标 [fraud?] |
| ⑨ | 〔?〕“the 19th percentile”疑为 “the 90th percentile” | `01:57:02`，与紧邻的 “below the 10th percentile” 对称推断为 90th，笔记引文标 [90th?] |
| ⑩ | ✅ 本片段新增的 ASR 错误样本（已列入 findings 的 asr_rows，供追加到 asr-dictionary.md） | 详见 `asr_rows` |

### 9.6 反方视角（对抗自检第 12 项）

1. **最薄弱的一节**：§3.2 KNN 填补——notebook 只传两列，我指出这样邻居定义很弱，但没有实际跑"传五列"的版本给出数字（读者做作业加分项时得自己跑）。
2. **现在答不上来的**：作业 Q1 分位数题出题人到底想要什么答案；助教在 tutorial 上有没有口头补充截止日和评分细则。
3. **推断**：① ~~截止日 9/23~~（已由 Canvas 更正为 9/25）；② "把题干当 prompt 用"是我在 AI Prompt cell 缺席情况下的建议，不是教授的要求；③ 二元属性对称 / 非对称的判定（`cleaning_fee` 等）有主观性，我给的是一种可辩护的答案。

**历史中间检查点（2026-09-30，非当前验收状态）**：上述迷你数据均标为笔记补充；脚本位于`C:/Users/BenLi/.codex/scratchpad/cityu-depth-20260930/verify_t03_mechanisms.py`，结果`t03-mechanism-results.json`。六组机制的独立数值/恒等式检查通过，另只读核原数据68133×15、评分缺15275、卧室缺0、观察评分mean94.012789/median96。原48cells的20个code已通读；完整KNN68k原输出本轮未重跑，不能把历史输出写成新实跑。旧strict、全部渲染与隔离R1–R4仍待验收，`mechanism_review: pending`。

### 9.6.1 本轮机制理解验收（2026-10-01）

独立只读`t03_final_reader`不继承作者上下文，只读成稿，在内存实际做九主题R1–R4。每项各2分，不按平均抵消。原文后的五处冲突、四处未唤醒词和四图数据流均修正后复验；全篇9个leaf的Q1–Q6各6分。代理阅读检验不是真人试读，原源/图形由主代理另核。

| 核心主题/证据位置 | R1/R2/R3/R4 | 实际新输入与结果/诊断 |
|---|---|---|
| CSV读取与列身份，§2.1 | 2/2/2/2 | 新3行×5字段：header=None保3×5，默认表头吞首行成2×5；赋6列名实际Length mismatch；路径由kernel工作目录决定 |
| 描述统计，§2.2 | 2/2/2/2 | 新0/1/1/3/7/NaN：有效5、mean2.4、sample variance7.8、std2.792848、median1、Q3=3、mode1；全缺失mode索引实际失败 |
| 分组，§2.3 | 2/2/2/2 | key A/A/B/B/缺失、x2/NaN/4/8/10：size2/2、count1/2、mean2/6；默认类别比例.5/.5；保未知组则比例.4/.4/.2 |
| 四图，§2.4 | 2/2/2/2 | 新0/1/1/2/3/18与箱界−1/1/3/5/18：计数1/3/1/1、最后箱含18；箱须0/3不是围栏；散点/折线保持原行配对 |
| 缺失报告，§3.1 | 2/2/2/2 | 新4×3缺失布尔表，缺失数2/1/0、比例.5/.25/0；筛报告只剩2字段，不删除原4行；空表比例未定义 |
| 填补，§3.2 | 2/2/2/2 | 新4×3矩阵：缺失距离按共同列3/m校正，k2目标单元填7/2/1；全缺失新行回退1/3/9；填入估计不回流为观察值 |
| IQR/Z，§3.3 | 2/2/2/2 | 新0/1/1/2/3/18：Q1=1/Q3=2.75，围栏−1.625/5.375，仅18标；Z样本std6.853223，阈3全不标、阈2标18；计算不等于正态假设 |
| Scaler，§3.4 | 2/2/2/2 | 训练5/15/25→新35：mean15、总体scale8.164966，new z2.44949；robust center15/scale10→2；inverse35；遗漏索引31/12/50重建join实际全NaN |
| cov/corr/热图，§3.5 | 2/2/2/2 | 新a0/1/2、b1/3/5、c4/3/2：cov为[[1,2,−1],[2,4,−2],[−1,−2,1]]，corr为正负1；常数列cov0/corrNaN，绝对排序正负平局，非因果 |

适用D证据均在对应正文：问题/输入输出、状态与步骤、就近数据流或控制图、原理/符号、同一输入到输出的完整小例、停止/边界、错误机制及调整限制、折叠迁移答案。原describe_col和z_flag没有安全守卫，补充图明确是增强流程，未篡改原代码。纯课前类型目录与PCA预告只作唤醒和具体回指，不伪装本篇重新训练PCA。

主代理独立复算`verify_t03_mechanisms.py`与`verify_t03_reader_cases.py`通过，结果为`t03-mechanism-results.json`和`t03-reader-case-results.json`。两阶段代理哈希DE2079A0…及C66A3C54…分别对应完整复验和四图/术语增补；后续纵排、Z退化出口、热图色域澄清由主代理核，不改变九个变式数值。

原48cells（20code/28markdown）均已通读；当前原数据68133×15，评分缺15275、卧室缺0，median96。四张实际Iris图已重画并查看，hist总150/parallel原行150核对；Airbnb热图两版实际渲染，原自动色域−.040035至1使+.08也蓝，补版固定−1至1，不改矩阵。未重跑原68k全KNN输出，相关历史数字仍标历史依据，不冒称新实跑。

IAB实际解析10个Mermaid、2个独立公式、57段行内数学，错误0/横向溢出0；全部10图实际看图，线性图改竖排以避免字体压小。源码绘图可编辑，不用临时位图代替正文。旧strict结构PASS：20code cells、9leaf、逐块中文9481（474/code cell）；结构不代替R证据。

转录机器复核PASS：9课堂格、186时戳、26引文，未匹配0、数字改写0。A8提示为tutorial无独立§6.2，要求在配套M03登记；A12的21%是本篇约27:40 tutorial段除整堂2:13:18，非本篇漏掉79%。只覆盖原有tutorial时段，未自行重合并转录。§7.1原题逐字保留，不产出个人评分成品。所有脚本/图和锁定候选在`C:/Users/BenLi/.codex/scratchpad/cityu-depth-20260930/`。

### 9.7 变更记录

| 日期 | 变更 |
|---|---|
| 2026-10-01 | 机制-v1验收：九主题R各2、九leaf Q各6；补完整数据流/算例/迁移、修缺失分母/距离供体/尺度口径/索引/插值/图色域/全篇旧解释；10图与数学实际预览、原48cells核对；保留原题与转录引文 |
| 2026-09-16 | v0.9 建稿：20 个 code cell 逐块讲解；notebook 全部数值输出用 `verify_airbnb.py` / `verify_w3w4.py` 在原始数据上复核一致；发现题干两处与数据不符（`bedrooms` 无缺失、分位数 exp 一致）；无转录，无 AI Prompt cell |
| 2026-09-18 | **合并 W3 转录 tutorial 段**（`M03-transcript.txt` `01:45:33 → 02:13:18`，本地 Whisper）→ v1.0：新增 9 个 🎙️ 格（A 7 / B 2 / C 0 / D 0）；§8 48 个 cell 加课堂覆盖列与时间分配表；§9.1 / 9.2 / 9.5 重写；作业口头规则回写 `作业与DDL` 与考点库 |

---

## 相关

- 配套讲义：[[M03-数据类型与描述性分析]] ｜ 下一个 tutorial：[[T04-特征选择与PCA实战-Iris]] ｜ 上一个：[[T02-回归实战-从合成数据到Airbnb定价]]
- 数据：[[IS6400_Business_Data_Analytics/_meta/数据集卡片|数据集卡片]] ｜ 作业：[[IS6400_Business_Data_Analytics/_meta/作业与DDL|作业与DDL]] ｜ 课程入口：[[IS6400_Business_Data_Analytics/00-课程总览|00-课程总览]]
