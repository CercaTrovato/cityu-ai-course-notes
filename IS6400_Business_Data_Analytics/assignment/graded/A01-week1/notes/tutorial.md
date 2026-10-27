---
course: IS6400
type: assignment-tutorial
assignment: A01-week1
status: 已提交
due: 2026-09-11T23:59:00+08:00
updated: 2026-10-27
readability_rules: v2
teaching_standard: novice-v1
readability_review: passed
---

# A01 · Week 1：从当前时间到 NumPy 矩阵

这篇是历史作业的事后学习教程。要学会的是：打印三个值 → 把值存成表的一行 → 几秒后追加第二行 → 取指定数字列做矩阵运算。下文用 `DEMO_ID`、`DEMO_NAME` 和虚构分数讲操作，不把它们当作本人资料或真实成绩。

既有记录：[Canvas 作业页](https://canvas.cityu.edu.hk/courses/71457/assignments/330586) 曾显示 2026-09-11 23:59、10 points，详情页曾确认 **9/11 21:35 Submitted!** 与同名 HTML。本次只读本地材料，没有刷新 Canvas，也没有核教师评分；保留既有已提交字段，不据本教程升级本人学习或评分状态。原题在 `course_files_export/Tutorial 1 - Introduction to Jupyter Notebook_Prompt.ipynb` 的 cell 24（本文从 1 开始计数），原先从 0 计数的记录称 cell 23。

## 0. 四题究竟要做什么

先看完成动作，再对照下面完整英文原题。表中内部配分共 100；Canvas 的 10 points 是另一记分尺度，不能自行推算课程总评。

| 题 | notebook 内部配分 | 直接完成条件 |
|---|---:|---|
| Q1 | 20 | 打印本人学号、姓名、运行当时的时间 |
| Q2 | 20 | 把以上信息放入带列名的 pandas 表 |
| Q3 | 30 | 几秒后加第二行，包含 expected scores；重新读取时间 |
| Q4 | 30 | 将 score 和 grade 两列转 NumPy 数组，打印数组及转置，只求所有 score 的和 |

<details><summary>完整英文原题（源 notebook cell 24；只统一换行）</summary>

> ## Tutorial 1:
> ### Please complete the following questions using this jupyter notebook, SAVE it as HTML and upload to canvas.
> 
> #### (1) (20 points) use the jupyter notebook to print the following information:
> #### Your student ID, your name, and your current time.
> #### (2) (20 points) put the information above into a pandas dataframe (the table in step 3)
> #### (3) (30 points) after a few seconds, add the second row of your id, name, time, expected scores
> #### (4) (30 points) Perform matrix operations with numpy:
> - Convert the score and grade columns into a numpy matrix.
> - Print the matrix and its transpose.
> - Calculate and print the sum of all scores.
</details>

中文限定词：`current time` 要运行时读时钟；`the information above` 指 Q1 的三项信息；`after a few seconds` 要实际隔几秒；`add the second row` 要保留第一行；`all scores` 只加分数，不能把 grade 编码也加进去。原件未定义 `grade` 的业务含义；本篇仅把它当数值编码。`category` 才是 Excellent/Good 等分档，两者不同。

原题有衔接缺口：Q2 只提三项，Q3 才提 expected scores，Q4 又提 grade，未唯一指定 Q4 用哪张表。官方参考 HTML 在 Q2 提前建五列，用 `expected scores` 作为分数列名；本人保存 HTML 则让 Q2/Q3 用个人 `mytable`，Q4 用课堂已有的 `df`。下文选择第三种教学写法：提前建 `score` 和 `grade` 两列，用一张虚构表贯穿四题。这是明确的笔记补充假设，不是教师已澄清的唯一答案。

## 1. 从干净环境理解执行顺序

Jupyter 的单元格（cell）是页面上一块文字或代码，内核（kernel）是实际执行 Python 的后台进程。变量存在内核中。只编辑或保存代码，不会重新计算输出；先运行创建变量的块，再运行使用它的块。重启内核会清掉旧变量，文档里保存的旧输出仍可能看得见。

本篇代码按 §2 → §3 → §4 → §5 连续执行，输入是虚构的两次记录，不读外部数据文件。预期输出依次为三个值、一行表、两行表、$2\times2$ 数组及转置、分数总和 170。它们只说明教学数据，不能代替本人答卷。

既有[完整教学脚本](../work/week1_practice.py) 与下文相同；这是新练习的运行入口，本次重审没有执行该评分任务脚本，也没有执行官方／本人保存 HTML 的代码。在新练习需要运行时，从 vault 根 `D:\上课资料\CityU` 使用：

```powershell
D:\anaconda3\python.exe -B -X utf8 IS6400_Business_Data_Analytics\assignment\graded\A01-week1\work\week1_practice.py
```

下面逐块说明代码与可手算结果。本次核查读取源代码及保存输出，并另核数组算术；没有更改 notebook、kernel 配置或历史输出。`datetime`、`time` 随 Python 自带；pandas、NumPy 须在所选环境中已有。遇缺库先核环境，不自行安装。

## 2. Q1：把一次时钟读数存下来

### 2.1 本题输入、操作与输出

本小问英文原题（源 cell 24）：

> #### (1) (20 points) use the jupyter notebook to print the following information:
> #### Your student ID, your name, and your current time.


任务是取得学号、姓名和一次运行时刻并显示。输入是两个示例字符串，输出是它们与新取得的时间；下面不预写固定时间。

```python
import datetime
student_id = "DEMO_ID"
student_name = "DEMO_NAME"
first_time = datetime.datetime.now()
print("Q1:", student_id, student_name, first_time)
```

单个 `=` 是赋值（assignment）：把右边的值用左边名字保存。`student_id` 是变量名，引号中的 `"DEMO_ID"` 是字符串（string），即文字值。以后用变量名，就取出已经保存的值；名字的大小写必须一致。

`import datetime` 加载日期模块（module），不安装软件。`datetime.datetime.now()` 从模块里的 `datetime` 类取得当前时间。圆括号表示调用：请求工具现在做这件事。`print(...)` 将逗号隔开的几项显示出来。保存 `first_time` 后，后续 Q2 可明确复用同一次读数；变量不会自己随时钟更新。

英文参考答案（笔记自拟）："I read the current time with `datetime.datetime.now()`, store it in `first_time`, and print it together with the student ID and name. The time is obtained during execution rather than hard-coded."

来源地位：取时与打印方式由课堂 cells 4、7 和官方参考 HTML 支持；本段变量名及虚构身份是教学补充。教师的 `liujm8` 示例不能当作本人学号。

## 3. Q2：把三个值放进同一行

### 3.1 本题输入、操作与输出

本小问英文原题（源 cell 24）：

> #### (2) (20 points) put the information above into a pandas dataframe (the table in step 3)


数据表（DataFrame）像带列名的表格，一行是一条记录，一列是一种信息。输入是 Q1 的三个变量，另加教学假设中的分数 80 与 grade 编码 1；输出先是一张零行五列表，再加入一行。

```python
import pandas as pd
table = pd.DataFrame(columns=["id", "name", "time", "score", "grade"])
table.loc[0] = [student_id, student_name, first_time, 80, 1]
print(table)
```

`as pd` 给 pandas 起短名。方括号 `[...]` 是列表（list）：按写下的次序放值。`columns=` 是有名称的参数，告诉建表工具用哪些列名。右侧五个值依次进入五列：`student_id` 对 id，`student_name` 对 name，`first_time` 对 time，80 对 score，1 对 grade。值数不同会报长度错误；数目相同但次序错了，可能不报错却把信息放错列。

`.loc[0]` 按行标签（row label）0 写入。标签尚不存在时新增这一行，已经存在时覆盖；它不是“永远追加”。Q2 为衔接后题增加 score/grade，是本文先声明的设计；官方示例的 `expected scores` 是另一个列名，不能直接用 `table["score"]` 访问它。

英文参考答案（笔记自拟）："I create a DataFrame and insert the ID, name and first timestamp into row label 0. In this teaching version, I also include `score` and `grade` from the start so that the later tasks use the same table."

## 4. Q3：等几秒，读新时间，追加第二行

### 4.1 本题输入、操作与输出

本小问英文原题（源 cell 24）：

> #### (3) (30 points) after a few seconds, add the second row of your id, name, time, expected scores


输入是 Q2 留下的一行表。先暂停，再读取新的时钟值，写尚未使用的标签 1；输出应保留标签 0，并多出标签 1。示例第二次预期分数改为 90，是虚构数据，不表示真实成绩变化。

```python
import time
time.sleep(3)
second_time = datetime.datetime.now()
table.loc[1] = [student_id, student_name, second_time, 90, 1]
assert second_time > first_time
assert len(table) == 2
print(table)
```

`time.sleep(3)` 暂停约 3 秒，调度可能让实际等待更长；之后重新 `.now()`。若复用 `first_time`，第二行仍是旧读数。若只改成 `loc[0]`，会覆盖第一行；若从 Q2 开始整块重跑，建空表也会抹掉旧表，因此要区分“只追加这一句”和“重新建表后追加”。

`>` 比较是否更晚；`len(table)` 取行数；`== 2` 比较是否等于 2。`assert` 是检查：条件为真就继续，为假就报 `AssertionError` 停下。这里既查新时刻也查两行仍在。系统时钟若被调整，时间比较也可能失败，应查实际读数，不修改输出伪造等待证据；断言不能证明整份答案正确。

英文参考答案（笔记自拟）："I wait about three seconds, read the clock again, and insert a second row with `table.loc[1]`. The first row remains in the table, and the second row contains a newly obtained timestamp and the expected score."

来源地位：原题要求等几秒，`sleep(3)` 是满足这一要求的一种实现。官方保存的两次时间只差 0.067639 秒；本人历史 HTML 的两次时间差为 3.004368 秒。这是保存证据的比较，没有在本次重新运行两份答卷。

## 5. Q4：先固定两列顺序，再只加分数

### 5.1 本题输入、操作与输出

本小问英文原题（源 cell 24）：

> #### (4) (30 points) Perform matrix operations with numpy:
> - Convert the score and grade columns into a numpy matrix.
> - Print the matrix and its transpose.
> - Calculate and print the sum of all scores.


矩阵（matrix）在这里是按行列排好的数字；NumPy 数组（ndarray）保存这些数字供计算。输入是教学表的 score/grade 两列，列顺序固定为分数在前、grade 编码在后；输出是两行两列数组、转置和分数和。

```python
import numpy as np
matrix = table[["score", "grade"]].to_numpy(dtype=float)
print(matrix)
print(matrix.T)
print(np.sum(matrix[:, 0]))
```

`table[["score", "grade"]]` 的内层方括号先组成列名列表，外层从表里取这两列。`to_numpy(dtype=float)` 转为小数型数字数组，姓名和日期不参与。转换后列名与行标签不在数组里，须另记第一列是 score；形状相同不能证明列次序正确。

教学输入只有下表四个数；每行是一次记录，score 的单位为分，grade 是业务含义未定义的数值编码。

| 记录 | score（分） | grade |
|---|---:|---:|
| 第一次 | 80 | 1 |
| 第二次 | 90 | 1 |

数组与转置如下。转置（transpose）把原每一行变成一列，`.T` 是取属性，不加圆括号。

$$
\begin{bmatrix}80&1\\90&1\end{bmatrix}
\quad\longrightarrow\quad
\begin{bmatrix}80&90\\1&1\end{bmatrix}.
$$

`matrix[:, 0]` 的逗号前选行，冒号 `:` 表示所有行；逗号后选列，0 是从零开始数的第一列。因此取到 80、90，`np.sum(...)` 得 $80+90=170$。若列顺序改为 grade/score，同样代码只会加 grade 编码，必须同步改列位置。数组大小写作 shape=(2,2)，意为两行两列。

英文参考答案（笔记自拟）："I convert the `score` and `grade` columns, in that order, to a NumPy array and print the array and its transpose. I sum only the first column, so the synthetic scores total 170. The grade values are excluded from the score total."

Q4 只要求矩阵、转置、分数和，没有要求课堂 cell 22 的点积；不能把课堂的额外演示误当本题小问。三种求和各回答不同问题：

| 写法 | 教学结果 | 实际加了什么 |
|---|---|---|
| `np.sum(matrix[:, 0])` | 170 | 只加 score |
| `np.sum(matrix, axis=0)` | `[170, 2]` | 分别给两列的和 |
| `np.sum(matrix)` | 172 | 全部四个数字 |

`axis=0` 把行这个维度合并，保留每列一个结果。因此结果的第一个数才是分数总和，第二个数是 grade 编码和；把两者再加起来不回答 all scores。

## 6. 怎样判断三个不同总分

先确认矩阵来自哪张表，再比较数值。本段不改历史答案，只解释来源。

| 材料 | Q4 输入与分数和 | 应怎样读 |
|---|---|---|
| 本文教学示例 | 虚构表的 80、90，合计 170 | 用同一张五列表贯穿四题 |
| 官方参考 HTML | `mytable` 的 expected scores 为 95、100，分数和 195 | 保存输出 `[195,3]` 还含 grade 编码和 3 |
| 本人保存 HTML | 明说沿用课堂 `df` 的 87、92、78、88，合计 345 | 不是本人两行预期分数的合计 |

原题没有唯一说清 Q4 用哪张表。官方示例支持一表方案；本人历史说明支持两表方案。两种选择必须把输入来源说清，不凭答案不同就断言一方算错，也不因此认定教师已给任何一份答卷评分。

本题最容易错的是把“程序有数字输出”当成“回答了题目”。顺序应是读限定词 → 声明表及列 → 核每次状态变化 → 只取题目所问的结果。更完整的历史差异见 [[IS6400_Business_Data_Analytics/assignment/00-overview/官方参考答案对照与复盘-2026-10-20|Week 1–5 官方参考答案对照]] §2。

## 7. 导出与历史提交事实

原 cell 24 要求保存为 HTML 上传 Canvas；既有 Canvas 记录还曾允许 PDF，实际回执是 HTML。这些是历史记录，本次未在线刷新，不据此给出当前提交建议或执行提交。

以后在新练习中，先保存必要成果，再用专用练习内核选择 `Kernel → Restart & Run All`，按顺序重新建立所有依赖。确认没有错误、各格输出对应当前代码，再标准导出 HTML：经典 Notebook 用 `File → Download as → HTML`；JupyterLab / Notebook 7 常用 `File → Save and Export Notebook As… → HTML`，具体菜单随版本而变。

HTML 保存的是导出时文档中的代码与输出。只把 ID 文本改掉但没重新执行，代码可能已变，输出仍可能显示旧 ID；若相关单元格从未执行，则可能没有输出。保存不替代运行，导出也不证明代码成功。

讲义 p.10 的历史一般要求是指定到期日上课前交、迟交每天扣 20 points、交自己的作品并留备份；Syllabus 写的是每天扣 20%，两者口径须分开。既有本次作业记录为 9/11 23:59，不用讲义一般文字覆盖它，也不推算罚分基数或最低分。

本人历史 HTML 在本目录 `submission/`，迁移时曾核 SHA-256 一致；本次只读其当前本地字节及保存内容。远端附件字节没有比较，只能沿用既有同名提交回执，不能称远端内容已逐字节核实。原答卷、教师评分和本人是否学会均不因重审教程而改变。

## 8. 换条件自测与答案

先尝试解释动作，再展开答案；这些是学习题，没有代填本人“已通过”。

1. 已有标签 0、1 两行时再运行 `table.loc[1] = [...]`，会新增第三行吗？若整段从建空表重跑，又会怎样？
2. 新矩阵两行为 (75,2)、(85,3)。只求 score、按 axis=0 求和、整个矩阵求和分别是多少？若调换两列，`matrix[:,0]` 仍是分数吗？
3. `=`、`==`、`assert` 分别做什么？检查失败以后能把旧输出当新结果吗？
4. 改完 ID 不运行 cell，导出的 HTML 能证明新 ID 已运行吗？

<details><summary>参考答案（笔记补充）</summary>

1. 覆盖标签 1，仍两行。重新运行建空表会先清掉原表，只留下本次重新插入的行；必须查自己执行了哪些语句。
2. 分数和 $75+85=160$；列和 `[160,5]`；全和 165。调换后第一列是 grade，`matrix[:,0]` 只得 2、3，应改取分数的位置，或在转数组前按列名求和。
3. `=` 保存值；`==` 比较相等；`assert` 在条件为假时报错停止。旧输出仍可能留在文档中，须查执行记录和实际错误；检查通过也只覆盖写出的条件。
4. 不能。文档可出现新代码与旧输出并存，必须执行后核新输出，再保存导出。

</details>

来源核查范围：完整题面来自源 notebook cell 24；API 与虚构教学代码对应既有 `work/week1_practice.py`；官方参考和本人 HTML 只读比较。没有重新执行评分作业，没有改源 notebook、输出、历史提交或评分字段。教学候选仍待本次独立审查。
