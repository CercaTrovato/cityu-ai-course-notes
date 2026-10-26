---
course: AC6761
type: classroom-exercise
status: draft
learning_status: 参考解析已制作，结果已只读核验
official_solution: 题面给出操作步骤；无独立官方结果表
updated: 2026-10-22
source: Quiz 2.docx + ExampleTables1.accdb
---

# Quiz 2 · 查出 E-10 经手的销售

## 要做什么、最后交什么

题目给了一份 Access 数据库。你要在销售表里，找出销售员 E-10 实际经手的销售，显示销售编号、销售金额和销售员编号，并将查询保存为 `QueryA`。

教师文件要求最后发送更新后的 `ExampleTables1`。本轮只制作学习解析并在库外副本只读验证结果，没有发送邮件，没有替本人登记提交或完成练习。

## 英文原题与全部步骤

以下逐字保留 `Quiz 2.docx` 正文，换行按步骤整理。

> Quiz 2
>
> Based on the ACCESS database “ExampleTables1”, construct a query: Sales made by E-10.
>
> 1. Open ExampleTables1
> 2. Create query design
> 3. Choose sale table
> 4. Select Sale Number, Amount, and SalesRepNumber
> 5. Criteria is E-10
> 6. Run
> 7. Save as QueryA
> 8. Close ExampleTables1
> 9. Send the updated ExampleTables1 to [CONTACT REDACTED IN PUBLIC COPY; SEE LOCAL ORIGINAL]

中文读题：`made by E-10` 指一笔销售由哪位销售员经手。这里限定的是 `Sale` 表里的 `SalesRepNumber`，不等于客户平时被指派给哪位销售员。

`Select` 在此是选显示字段；`Criteria` 是筛选条件；`Run` 才是执行查询。保存查询与改变销售记录也是两回事：本题要求保存一个查询定义，不要求改销售金额。

## 先看数据库里究竟有什么

源数据库有 8 张用户表。下面每行是一张表，行数来自本次 ODBC 只读枚举，不包括 Access 系统表。

| 表 | 记录数 | 业务含义 |
|---|---|---|
| Cash | 4 | 银行/现金账户 |
| CashReceipt | 5 | 收款事件 |
| Customer | 5 | 客户及指派销售员 |
| Inventory | 6 | 商品类别 |
| Inventory-SaleStockflow | 13 | 销售与商品的明细关联 |
| Sale | 7 | 销售事件 |
| Sale-CashRecDuality | 6 | 销售与收款的分配关联 |
| Salesperson | 4 | 销售员 |

表名表示对象，记录数表示该表行数，不是销售总额。读 `Sale` 一行：该库共 7 笔销售，本题只需从中筛选，无需连接其他表。

**题面字段有一处差异**：题目写 `Sale Number`，实际表列名为 `SaleNumber`，中间没有空格。其余所需列 `Amount`、`SalesRepNumber` 实际存在。使用错误列名会被 Access 当作未知参数。

## 一步一步完成查询

先保留原始数据库，另做工作副本。副本用于练习，课程 `course_files_export/ExampleTables1.accdb` 原件保持只读。

1. 在 Access 中打开工作副本 `ExampleTables1.accdb`。
2. 选择 `Create` → `Query Design`，进入查询设计视图。
3. 添加 `Sale` 表，关闭添加表窗口。
4. 第一列选实际字段 `SaleNumber`，勾选 `Show`。
5. 第二列选 `Amount`，勾选 `Show`。
6. 第三列选 `SalesRepNumber`，勾选 `Show`。
7. 在第三列的 `Criteria` 行输入 `"E-10"`；保留普通半角连字符。
8. 点击 `Run`，查看数据表视图中的筛选结果。
9. 保存查询名称为 `QueryA`，关闭工作副本后再核保存状态。

每步为何这样做：

- 选 `Sale`：题目问实际销售事件，经手人就在该表，不需要借客户指派关系推断。
- 保留三列：销售编号区分事件，金额显示业务值，销售员编号证明每行符合筛选。
- 条件放第三列：`E-10` 是文本身份码；若放在金额列，查询对象就错了。
- 保存为 `QueryA`：保存的是这套选列和条件，重新打开时可再次执行。

已有 M06 讲义的完整先修可从 [[AC6761_Artificial_Intelligence_Accounting/notes/M06-ACCESS数据库构建与查询|M06：Access 构建与查询]] 查看。这里查询（query）是从表取符合条件的记录，条件（criterion）是每行必须满足的测试。

## SQL 对照与逐行解释

下面是与设计视图等价的参考 SQL。它只读取三列，不更新或删除销售数据。

```sql
SELECT SaleNumber, Amount, SalesRepNumber
FROM Sale
WHERE SalesRepNumber = 'E-10';
```

- `SELECT`：指定最终显示的三个实际字段，顺序与题目相同。
- `FROM Sale`：输入是 7 行销售记录。
- `WHERE`：逐行检查销售员编号是否精确等于文本 `E-10`，只有真值行进入输出。

Access 设计器可能自动添加表名前缀、方括号或括号，这些显示差异不改变上述筛选含义。

## 本次实际结果与核对

在库外副本用 Access ODBC 驱动执行参数化等价查询，得到以下 5 行。下表按销售编号整理以便阅读；原题未要求排序，SQL 也未保证排序。

| SaleNumber | Amount | SalesRepNumber |
|---|---|---|
| S-2 | 10,000 | E-10 |
| S-3 | 16,000 | E-10 |
| S-4 | 10,000 | E-10 |
| S-5 | 16,600 | E-10 |
| S-6 | 35,000 | E-10 |

每行是一笔实际销售，第一列为事件身份码，第三列为经手销售员身份码，两者都不是数量。第二列采用库中 Currency 数值，币种未给，不擅自写 HKD。

读第一行：销售 `S-2` 金额 10,000，由 `E-10` 经手。金额合计 87,600，仅用于复核，没有作为额外输出列加入原题查询。

**英文参考答案（笔记自拟）**：

> QueryA selects SaleNumber, Amount and SalesRepNumber from Sale where SalesRepNumber equals 'E-10'. The supplied database returns five sales: S-2, S-3, S-4, S-5 and S-6. The total amount is 87,600 in the database's unspecified currency units.

结果来源是本次数据库查询；题面只提供操作步骤，不把该结果冒称为另一个官方答案文件。

## 最难的区别：指派给谁，不等于本次由谁经手

`Customer.SalespersonNumber` 描述客户的指派关系，`Sale.SalesRepNumber` 描述某笔销售实际参与者。假设客户平时归 E-12，但这次销售由 E-10 经手，本题仍应保留这笔销售。

这个情境是笔记补充，用来说明为什么不用客户表。把客户表连进来再筛其销售员，会把题目的“本次经手”换成“长期指派”，回答另一个问题。

## 排错、总结与改条件练习

- 弹出参数框：检查是否把 `SaleNumber` 写成了 `Sale Number`，也检查表名及字段拼写。
- 结果为空：检查引号是否为普通引号、编号是否有多余空格、连字符是否正确。
- 出现 7 行：检查条件是否真的放在 `SalesRepNumber` 的 `Criteria` 行。
- 行数异常增加：检查是否无意加入多对多关联表，导致一笔销售按明细重复。
- 保存后找不到 `QueryA`：查看 Access 导航窗格的查询分类；不要只保存结果截图。

本题的判断顺序是：先确定所问事件，找到真实字段，再选列、加条件、执行、核每行、保存定义。

**改条件练习**：若还要销售金额至少 16,000，应在哪里加什么条件？

<details><summary>答案</summary>

在 `Amount` 的 `Criteria` 行输入 `>=16000`，并与销售员条件放在同一行，表示两项同时成立。参考 SQL 使用 `WHERE SalesRepNumber='E-10' AND Amount>=16000`。本库符合的是 S-3、S-5、S-6，共 3 行，金额合计 67,600。若把两项放在不同 OR 行，可能变成“由 E-10 经手或金额够大”，题意会扩大。

</details>

## Canvas 与本人状态边界

2026-10-22 已检查四入口：Files 28 项，含 `Quiz 2.docx`（file 16328652）和数据库（file 16324717）；Announcements 5 条，最新为 10/20 小组项目；Assignments 显示该课程已禁用；Modules 访问重定向课程首页，无可访问独立模块列表。

Quiz 2 文件未写计分、截止日或具体提交时刻。不能因名称是 Quiz 就补造分数，也不能因没有 Canvas 提交入口就断言不计分。邮件要求按原题保留，实际发送属于独立动作，本轮没有发送。

`status: draft` 表示行政与本人提交条件仍待核。学习解析、数据库结果核验、本人已练习、保存过 QueryA 和本人已提交分别记录；后四项本轮不代填。

## 来源与本轮记录

原件：[[AC6761_Artificial_Intelligence_Accounting/course_files_export/Quiz 2.docx|Quiz 2]] 与 [[AC6761_Artificial_Intelligence_Accounting/course_files_export/ExampleTables1.accdb|原始数据库]]。

本次只读检查使用库外副本，8 表、50 行用户记录（各表相加），不把跨表记录数当销售笔数。源库 7 笔销售，筛选 5 笔。原始 SHA-256 与核验范围见本次 Canvas 材料清单；没有改变原件。

2026-10-22：制作参考解析、核对实际字段与 5 行结果、补最小变式。未改变本人学习、提交和评分状态。
