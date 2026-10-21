---
course: IS6400
type: assignment-tutorial
assignment: A01-week1
status: 已提交
due: 2026-09-11T23:59:00+08:00
updated: 2026-10-20
---

# A01 · Week 1：从当前时间到 NumPy 矩阵

[Canvas 作业页](https://canvas.cityu.edu.hk/courses/71457/assignments/330586) 显示 2026-09-11 23:59、10 points；详情页确认 **9/11 21:35 Submitted!** 与同名 HTML。原题在 `course_files_export/Tutorial 1 - Introduction to Jupyter Notebook_Prompt.ipynb` 的 **cell 24**；原有教学解释见 [[IS6400_Business_Data_Analytics/notes/T01-Jupyter入门与Pandas基础|T01]] §7。个人 HTML 已按 SHA-256 迁入私有 `submission/`，远端字节未比对。本篇是**事后学习教程**，不冒充当时提交稿。

## 0. 四题究竟要做什么

| 题 | notebook 内部配分 | 直接完成条件 |
|---|---:|---|
| Q1 | 20 | 打印本人的学号、姓名、**运行当时**的时间 |
| Q2 | 20 | 将这三项放入带列名的 pandas 表 |
| Q3 | 30 | 几秒后加第二行，包含 expected score；时间必须重新读取 |
| Q4 | 30 | 只选 `score` 和 `grade` 两个数值列，转 NumPy 矩阵、打印转置、求所有 `score` 的和 |

原题在 Q2 只提三项，Q3 才提 expected score，Q4 又提 grade。这个**题面衔接缺口**需要显式说明。教学版在建表时增加 `score` 和 `grade` 两列，使四题能够用同一张表按顺序完成；另一种做法是 Q4 使用原 notebook cell 13 教授给的 `df`。下文的 `DEMO_ID`、80、90、grade=1 都是**虚构示例**，不能写成用户本人资料或实际成绩。

## 1. 从干净环境直接运行

[完整教学脚本](../work/week1_practice.py) 按 Q1→Q4 顺序执行，从 vault 根目录运行：

```powershell
D:\anaconda3\python.exe -X utf8 IS6400_Business_Data_Analytics\assignment\graded\A01-week1\work\week1_practice.py
```

脚本依次打印第一次时间、一行表、约 3 秒后的两行表、$2\times2$ 矩阵和转置，以及示例总分 **170.0**。它只在屏幕输出，绝不改课堂 notebook 或已提交 HTML。在 Jupyter 做新练习时把代码按以下小节放到先后几个 code cell；前一个 cell 运行完成，再运行后一个。

## 2. Q1：变量、`import`、函数和时间

```python
import datetime
student_id = "DEMO_ID"
student_name = "DEMO_NAME"
first_time = datetime.datetime.now()
print("Q1:", student_id, student_name, first_time)
```

`import datetime` 是加载 Python 自带日期工具。单个 `=` 是**赋值**，把右侧内容存进左侧变量；引号中的 `DEMO_ID` 才是文字值。`datetime.datetime.now()` 的两个 `datetime` 分别是模块和其中的类，`.now()` 调用计算机时钟。`print(...)` 用逗号隔开多个要显示的值。时间不能预先写死，也不能复制教授样例。若填本人学号，只在私有文件操作。**所以呢**：Q1 要让这一次运行产生新的时间证据。

## 3. Q2：DataFrame 与列顺序

```python
import pandas as pd
table = pd.DataFrame(columns=["id", "name", "time", "score", "grade"])
table.loc[0] = [student_id, student_name, first_time, 80, 1]
print(table)
```

DataFrame 像带列名的 Excel 表；`as pd` 只是给 pandas 起短名。`columns=[...]` 的方括号表示一个**有顺序的列表**。`table.loc[0]` 定位行标签 0，右侧五个值依次放进五列。为了 Q3 和 Q4，教学版提前加入两列，这是**笔记补充的设计**，不是老师原 Q2 明写的五列。若列数与右侧值数不同，pandas 会报长度错误。先数列名，再数值。

## 4. Q3：追加而不是覆盖

```python
import time
time.sleep(3)
second_time = datetime.datetime.now()
table.loc[1] = [student_id, student_name, second_time, 90, 1]
assert second_time > first_time
assert len(table) == 2
print(table)
```

`time.sleep(3)` 暂停约 3 秒；之后再次 `.now()`，不能复用第一行的时间。`loc[1]` 是新增第二行，误写 `loc[0]` 就覆盖了原行。`len(table)` 是行数，`== 2` 是**比较**，不同于赋值 `=`；`assert` 在条件不成立时停止，让错误不会混进结果。Q3 的证据是**两行都还在，第二次时间更晚**。

## 5. Q4：数值矩阵、转置与只加分数列

```python
import numpy as np
matrix = table[["score", "grade"]].to_numpy(dtype=float)
print(matrix)
print(matrix.T)
print(np.sum(matrix[:, 0]))
```

`table[["score", "grade"]]` 的内层方括号是两个列名组成的列表，外层是从表中选这两列。`to_numpy(dtype=float)` 转成可计算的小数矩阵，**不把文字姓名和日期带进去**。示例矩阵和转置分别是

$$\begin{bmatrix}80&1\\90&1\end{bmatrix}
\quad\longrightarrow\quad
\begin{bmatrix}80&90\\1&1\end{bmatrix}.$$

`.T` 交换行列。`matrix[:, 0]` 的冒号代表所有行，0 代表第一列 `score`（Python 从 0 数起），所以 `np.sum(...)` 得到 $80+90=170$。直接对整个矩阵 `np.sum(matrix)` 会连两个 grade=1 一起加，错成 **172**。换一组数据时也应先找准列，而不是记住 170。

## 6. 加分深度：解释题面缺口与数据结构

| 我的理解 | 用实际运行怎样证明 | 限制 |
|---|---|---|
| Q3 突然要 expected score，Q4 又要 grade；表应先规划字段 | 展示 `table.columns` 和两次打印的表 | 这是教学版的合理解释，并非题面原来就有五列 |
| “几秒后”要求真实的新观测时间 | `second_time > first_time`，两行仍在 | 时钟输出随运行而变，不能硬编码 |
| “所有 score”是**一列**求和，不是所有数字求和 | 手算 80+90=170，与 `np.sum(matrix[:,0])` 对照 | 示例分数为虚构，真实作业须用本人数据 |

这些解释比堆更多 API 更能展示是否真正懂表与矩阵。这里是历史作业的**教学复盘**，不声称提交稿已写入这些拓展。

## 7. 导出和提交事实

原 notebook cell 24 要求导出 HTML 上传 Canvas；当前 Canvas 页面允许 html 或 pdf，实际回执为 HTML。导出前在 Jupyter 选择 `Kernel → Restart & Run All`，确认每个 code cell 都显示正确结果，再 `File → Save and Export Notebook As… → HTML`。HTML 保存的是**已运行的输出**；只改代码但不重新运行，导出的还是旧值。早期讲义“上课开始前交”的一般说法与本次 Canvas **9/11 23:59** 不同，以本次 Canvas DDL 为准。

旧个人 HTML 位于本目录 `submission/`，迁移前后 SHA-256 相同，未在 Git 保留新副本；Canvas 远端字节尚未比对，只能说**同名附件已有提交回执**。

## 8. 自测与验收

1. Q3 若把 `loc[1]` 改为 `loc[0]`，会怎样？
2. Q4 直接 `np.sum(matrix)` 为何得到 172？
3. `=`、`==`、`assert` 分别做什么？
4. 改完 ID 不运行 cell，导出的 HTML 会显示新 ID 吗？

<details><summary>参考答案</summary>

1. 覆盖第一行，表仍只有一行。2. 连两个 grade=1 一起加了。3. `=` 保存值、`==` 比较、`assert` 让失败的比较立即停下。4. 不会；HTML 仍保存旧输出，须重跑全部 cell。

</details>

**核查结果**：原题已回 notebook cell 24；教学脚本从干净运行连续输出两行、矩阵和 170；Canvas 详情页显示历史提交。教师最终评分与真实提交稿的质量仍以 Canvas 讲评为准。

## 7.1 2026-10-20 官方参考答案对照

官方示例确认了四题的基本 API，但不是每处都比历史答卷更贴题。Q3 的两次时间只差约 0.068 秒，私人答卷实际等待约 3 秒；Q4 官方用 `np.sum(matrix, axis=0)` 同时输出 score 与 grade 两列总和，而原题只要求 all scores，私人答卷用 `matrix[:, 0]` 得到 345 更符合字面要求。完整证据见 [[IS6400_Business_Data_Analytics/assignment/00-overview/官方参考答案对照与复盘-2026-10-20|Week 1–5 官方参考答案对照]] §2。此处只更新学习复盘，不修改历史答卷或本人学习、提交、评分字段。
