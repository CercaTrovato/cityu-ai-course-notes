---
type: 作业与DDL
course: IS6400
updated: 2026-10-28
tags: [IS6400, DDL, 作业]
---

# IS6400 作业与 DDL

> 制作规则：[[作业规范|全局通用规则]] → [[IS6400_Business_Data_Analytics/_meta/IS6400作业制作规范|IS6400 课程细则]] → 本地私有 Axx 任务说明。本页维护作业事实与历史来源，不能覆盖制作规则。

> **2026-09-27 Canvas 提交复核**：Assignment Week 1（9/11 21:35）、Week 2、Week 3（9/22 00:06）详情页均显示 `Submitted!`，附件名与本地私有归档对应；远端字节哈希未比对，评分仍待 Canvas。旧 `assignments/Week1–3` 的个人文件已逐件 SHA-256 核对并迁入被 Git 忽略的 `assignment/`，旧路径从 Git index 移除；既往 Git 历史不因此消失。这段的 W01–W03 是 9/27 历史复核。W04 已于 9/30 核当前 Canvas：10/2 23:59 截止、10 points、HTML 或 PDF，新版四题共 100 内部分。

> ⚠️ **本文件里的日期分两类**：
> - **✅ 确认** = 材料里白纸黑字写的
> - **⚪ 推算** = 我按周次推算的（第 1 周 = 2026-08-31 至 09-05，逐周 +7 天；**未计入香港公众假期**）
>
> **动手前先用 Canvas 的实际日历核对一遍。** 本课迟交惩罚是五门课里最重的。

---

## ⏰ 最近的截止

### ✅ Tutorial 1 作业（Canvas 名 "Assignment Week 1"）—— 9/11（周四）23:59，已过

> ✅ Canvas 截图（2026-09-16）："Assignment Week 1 · Due Sep 11 at 11:59pm · -/10 pts · Not Yet Graded"——时刻是 **23:59**（不是"上课前"），Canvas 占 10 分，尚未批改。

| 项 | 内容 |
|---|---|
| 题目 | notebook `Tutorial 1 - Introduction to Jupyter Notebook_Prompt.ipynb` **cell 24**，4 题 100 分 |
| 交什么 | **HTML**（"SAVE it as HTML and upload to canvas"），不是 `.ipynb` |
| 逐题攻略 | [[T01-Jupyter入门与Pandas基础#7. 本次作业（notebook cell 24 原文）\|T01-Jupyter入门与Pandas基础 › 7. 本次作业（notebook cell 24 原文）]] —— §7.1 逐题对应 cell，§7.2 **三个坑**，§7.3 导出方法 |

**动手顺序**（照 T01 §7 走，半小时内能做完）：

1. 把 cell 4 的 `StudentID='liujm8'` **换成你自己的**（`liujm8` 是教授的 ID，忘改是最容易丢分的地方）
2. 建表时**直接加上 `score` 列**（第 (3) 题要 expected scores，但第 (2) 题的表原本没有这列）
3. 第二行**重新取一次** `datetime.datetime.now()`，别复用第一行的 `x`
4. 第 (4) 题用 **cell 13 的 `df`**（那张才有 `grade` 列），不是 `mytable`
5. 每处你对题意的解读，**用 markdown 写一句**，避免被当成做错
6. `Kernel → Restart & Run All` 跑一遍，**再**导出 HTML
7. 自己留一份备份

---

### 🔴 Assignment Week 3 —— **9/25（周五）23:59**，Canvas 10 分

> ✅ **来源：Canvas 作业列表截图（2026-09-16 用户提供）**："Assignment Week 3 · Due Sep 25 at 11:59pm · -/10 pts"。题目在 `Week 3 Description.ipynb` cell 44–48（内部 100 分 ↔ Canvas 10 分）。⚠️ 不是我之前推算的 9/23，**比 W2 作业晚一周整**。

| 项 | 内容 |
|---|---|
| 题目 | notebook **cell 44–48**，**3 题 100 分**：Q1 Airbnb 描述性报告（35）· Q2 数据质量 / 可视化 / 与 `log_price` 的关系（45，至少 8 张图）· Q3 **自己的项目数据集**探索（20） |
| 数据 | `Airbnb.csv`（Q1–Q2）+ **你们小组的项目数据**（Q3；组员必须用不同变量） |
| 交什么 | notebook 明写：**`.ipynb` + 导出的 `.html`**（W2 的 Canvas 页限 html + pdf；本周 Canvas 页的文件类型限制截图未显示，**上传前看一眼**） |
| 逐题攻略 | [[T03-数据探索实战-Iris与Airbnb的描述统计#7. 本次作业：Week 3 Assignment（notebook cell 44–48 原文）\|T03 › 7. 本次作业]] —— §7.3 逐题、§7.4 自查 |

**学习口径**（详见 T03 §7.3）：① 本数据六个指定 price 分位与 exp(log 分位)在数值精度内相等；单调保序不保证样本线性插值与 exp 普遍交换。② `bedrooms` 无缺失，三种填补不改变该列。③ 本人历史 Q3 已用 NIC 10,000×16 数据，来源真实性未在本轮认证；原提交及评分记录不变。

### ✅ Week 4 Assignment —— **2026-10-02（周五）23:59，香港时间**

2026-09-30 实际检查 Canvas Assignments、Announcements、Files、Modules。[任务页](https://canvas.cityu.edu.hk/courses/71457/assignments/330603) 显示 10 points、上传 HTML／PDF，当前未提交。题目来自用户新下载的 [当前附件](https://canvas.cityu.edu.hk/courses/71457/files/16057486)：`Week4_Feature_Engineering_Tutorial.ipynb`，43 cells／475599 字节，SHA-256 `b41b08f5c22afb59286ad7c522e9cb0f70dc4de635b3a961298661d66c57376f`。

| 项 | 当前口径 |
|---|---|
| 四题内部评分 | Q1 ANOVA F／过滤判断 20；Q2 SFS 选二列／机制 40；Q3 Airbnb f_regression 选八列／为什么不用分类检验 20；Q4 随机森林 RFE 选八列／比较 20，共 100 |
| 提交 | HTML 或 PDF；本次制作 HTML，Notebook 保持可续写 |
| 进度 | 可提交（待本人审阅）；空内核运行与导出验收完成，本人学习未确认，未代提交 |
| 本地入口 | 私有 `assignment/00-overview/作业总览.md` → A05 → 中文指南／Notebook／HTML |
| 规则 | [[IS6400_Business_Data_Analytics/_meta/IS6400作业制作规范\|本课作业制作规范]]，有依据的加分深度为必做 |

**新旧变化：** 旧 37-cell 版本 cell 35 的 80 分任务（含三方法比较、Airbnb 三特征）不再是现行题面。T04 保留的旧材料解读有历史标记，不据此提交。没有将“按规律预计”继续当作正式截止。


### 📋 Week 3 Quiz（课堂小测，Participation 5% 的一次）

> ✅ Canvas 截图："Week 3 Quiz - Wed 12 PM · Due Sep 16 at 2:00pm · -/1 pts"。这就是 Syllabus 说的**随机抽课堂上小测**——W3（9/16）被抽中了，12:00 上课、14:00 截止、1 分。⚪ 推断：以后每次被抽中都会以 "Week N Quiz" 的形式出现在 Canvas，**上课时留意 Canvas 通知**。

⚠️ Week 2（9/18）、Week 3（9/25）、✅ Week 4（10/2）三份作业**连着三个周五**，且 W3 的 Q3 依赖项目数据——**9/16–10/2 是本课到目前最重的两周半**。

---

### 🔴 Assignment Week 2 —— **9/18（周五）23:59**

> ✅ **来源：Canvas 作业页（2026-09-09 用户截图确认）**。这条不是推算。

| 项 | 内容 |
|---|---|
| 名称 | **Assignment Week 2** |
| 截止 | **Sep 18 by 11:59pm** |
| 占分 | **10 points** |
| 提交方式 | **a file upload** |
| 文件类型 | 🔴 **html 和 pdf** |
| Canvas 页说明 | *"No additional details were added for this assignment."* |

**🔴 提交格式这条最容易踩坑**：文件类型限 **html 和 pdf**，意思是把 Jupyter notebook **导出**成这两种格式上传，**不是交 `.ipynb`**。

操作：`File → Save and Export Notebook As → HTML`；PDF 若直接导出报错（缺 LaTeX 环境很常见），**先导 HTML，再用浏览器打印成 PDF**。

**题目在哪**：Canvas 页面没有题目，**题干在 notebook `Week 2 Regression Analysis_With Prompt.ipynb` 的 cell 38**——4 道题，notebook 内部标注满分 100，对应 Canvas 上的 10 分。

> 所供 W02 转录未覆盖 cell 38；实际结尾缺失时长和作业口头宣布情况未知，不以关键词零命中证明课上从未布置。行政沿已有 Canvas 记录，本轮未在线重核。

**做题前先记住三条**（都来自课堂，讲义没有）：

1. 🔴 **用 `statsmodels` 不要用 `sklearn`** —— 助教明说（`02:33:25`），因为 **sklearn 给不了 p 值**，而本讲考点明确要求会解读系数与 p 值
2. 🔴 **显著性阈值取 0.05 / 0.1**（🎙️ `37:24`）—— 讲义完全没给阈值。落在两者之间的要**分档说**
3. ⚠️ **虚拟变量用 n−1 个**，并说清各系数是"相对基准类别"的比较（🎙️ `01:47:10`，全班几乎无人学过，本讲考试信号最强的技术点）

⚠️ **迟交每天 −20%**（见下），9/18 是周五，**别拖到周末**。

---

## 🔴 0. 最要紧的三条

### ① 个人作业迟交 **每天 −20%**，五天归零

> Syllabus："Assignments are highly related to the lectures and the tutorials conducted in class. **Late submission will result in 20% deduction per day delay.**"
> W1 讲义 p.10："Late submissions will be accepted. (**−20 points per day overdue**)"

| 迟交天数 | 一份满分作业还剩 |
|---|---|
| 0 天 | 100 |
| 1 天 | 80 |
| 2 天 | 60 |
| 3 天 | 40 |
| 4 天 | 20 |
| **5 天** | **0** |

**推论**：写不完也要**先交半成品**。交一份 60 分的完整作业，好过迟交 2 天的 100 分作业（同样是 60 分，但你还多花了两天）。

### ② 截止时刻是「上课开始前」，不是当天 23:59

> W1 讲义 p.10："**Submit before the beginning of the class** on the specified due day."

⚪ 若你在 **S02 & SA2（周三 12:00–14:50）**，那截止时刻就是**周三 12:00**，不是周三晚上。

### ③ ⚠️ 作业很可能是「下周交」

> W1 讲义 p.8："Individual Assignments (25 %) — **5~10 assignments due next WEEK**"

⚪ **最可能的含义**：某周课上发的作业，**下一周上课前交**。

这意味着：
- **Tutorial 1 的作业（notebook cell 24）→ ✅ 截止 2026-09-11**（用户 09-10 确认；⚠️ 具体时刻未知，讲义 p.10 说"上课开始前"，Canvas 可能是 23:59，**请核实**）
- **Tutorial 2 的作业（notebook cell 38）→ ✅ 截止 2026-09-18 23:59**（Canvas 截图确认，Points 10，交 html + pdf）

> ✅ **两份作业的截止日都已核实**（T01 = 9/11，T02 = 9/18）。⚠️ 注意 T02 是 **23:59**，说明"上课开始前"这条通用规则**并非每次都适用**，以 Canvas 为准。

---

## 1. 考核总表

| # | 项目 | 权重 | 次数 | 迟交惩罚 |
|---|---|---|---|---|
| 1 | Class Participation | **5%** | 随机抽课 | 缺课即失去该次机会 |
| 2 | **Individual Assignments** | **25%** | **约 8 次**（讲义说 5~10 次） | **每天 −20%** |
| 3 | Group Project Briefing | 5% | 1 次 | ⚪ 未明说 |
| 4 | Group Project Presentation | **15%** | 1 次 | — |
| 5 | Group Project Report | 10% | 1 次 | **每天 −10%** |
| 6 | **Exam** | **40%** | 期末，**2 小时** | — |

### ⚠️ 官方及格线（Syllabus 完全没写，只有官方目录有）

```
Minimum Continuous Assessment Passing Requirement (%)   30
Minimum Examination Passing Requirement (%)             20
```

**平时分（60% 那部分）至少要拿 30%，考试至少要拿 20%，两条都要过。** 一边高分补不了另一边。

### ✅ GenAI 政策（官方目录明写）

| 评估项 | Allow Use of GenAI? |
|---|---|
| AT1 = Class performance and **assignments** | **Yes** |
| AT2 = **Group Project** | **Yes** |
| Examination | **未标注**（考试不在 ATs 表内。⚪ 按惯例不允许，但没有白纸黑字） |

---

## 2. 个人作业清单

> 本课的作业**直接印在每周 tutorial notebook 的最后一个 markdown cell 里**，不是单独的文件。做作业 = 在同一个 notebook 里补全代码 → 导出 HTML → 传 Canvas。

### W01 个人作业（Tutorial 1）

| 项 | 内容 |
|---|---|
| **出处** | `Tutorial 1 - Introduction to Jupyter Notebook_Prompt.ipynb` **cell 24** |
| **笔记** | [[T01-Jupyter入门与Pandas基础#7. 本次作业（notebook cell 24 原文）\|T01-Jupyter入门与Pandas基础 › 7. 本次作业（notebook cell 24 原文）]] |
| **总分** | 100 分（20 + 20 + 30 + 30） |
| **提交格式** | ✅ **"SAVE it as HTML and upload to canvas"** |
| **截止** | ✅ **2026-09-11**（用户确认；具体时刻待核，见置顶块） |

**题目**（notebook 原文）：

1. **(20 分)** 用 Jupyter 打印：你的学号、姓名、当前时间
2. **(20 分)** 把上面的信息放进一个 pandas DataFrame（第 3 步里的那张表）
3. **(30 分)** **过几秒之后**，加上第二行：你的 id、姓名、时间、expected scores
4. **(30 分)** 用 numpy 做矩阵运算：
   - 把 score 和 grade 两列转成 numpy 矩阵
   - 打印矩阵及其转置
   - 计算并打印所有 score 的总和

**⚠️ 三个坑**（详见 [[T01-Jupyter入门与Pandas基础#7.2 ⚠️ 三个坑|T01-Jupyter入门与Pandas基础 › 7.2 ⚠️ 三个坑]]）：
- 第 (3) 题要 "expected scores"，但第 (2) 题建的表**没有 score 列** → 建表时就多加一列
- 第 (4) 题要 "score and grade columns"，但那张表也**没有 grade 列** → 指的是 cell 13 的 `df`
- "after a few seconds" 意味着两行的 time **必须不同** → 要重新调用 `datetime.datetime.now()`
- ⚠️ 记得把 `StudentID='liujm8'`（**教授本人的 ID**）改成你自己的

### W02 个人作业（Tutorial 2）

| 项 | 内容 |
|---|---|
| **出处** | `Week 2 Regression Analysis_With Prompt.ipynb` **cell 38** |
| **笔记** | [[T02-回归实战-从合成数据到Airbnb定价#8. 本次作业（notebook cell 38 原文）\|T02-回归实战-从合成数据到Airbnb定价 › 8. 本次作业（notebook cell 38 原文）]] |
| **总分** | 100 分（10 + 10 + 40 + 40） |
| **提交格式** | ✅ **"Upload your code and results as an HTML file to Canvas"** |
| **截止** | ✅ **2026-09-18 23:59**（Canvas 截图确认）· **Points 10** · 文件类型 **html + pdf** |

> ### 🔴 转录核实结果（2026-09-09）：**这份作业在整堂课的录音里从未被提及**
>
> 对 W02 转录（631 段，`00:02 → 02:34:37`）用 `assignment / homework / due / deadline / submit / grade / score` 全文检索，**命中数为 0**。
>
> **录音里与"课后要做什么"有关的，只有教授交班时的一句**（`01:48:15`）：
> > 🎙️ "**Please download all the materials on Canvas, including the data and [the] tutorial code template**, on your local desk[top], and you should be able to start from the template."
>
> ⚠️ **但这不能证明"课上没布置作业"**：录音在 `02:34:37`（助教讲到 notebook 的 cell 35）**戛然而止**，而课排到 **14:50**，**结尾缺了约 13–15 分钟**。**作业的宣布很可能就在那一段里。**
>
> 🔴 **必须去 Canvas 确认三件事**：① 截止日期与具体时刻；② 是否真的交 HTML；③ 这一次占 Take-home Assignments（30%）里的多少分。
>
> ⚠️ **按本课"迟交每天 −20%"的规则，宁可早交也不要等确认。** 见 §0 ①。

**🎙️ 助教在 tutorial 里给的五条项目/作业相关规则**（全部只在录音里，notebook 一个字没写）：

| # | 规则 | 原话（时间戳） | 对哪一题有用 |
|---|---|---|---|
| **P1** | ⭐⭐ **做项目/作业时用 `statsmodels` 而不是只用 sklearn，因为 sklearn 给不了 p 值** | `02:33:25` "[sklearn's] `LinearRegression` **is not quite useful, because [it] didn't give you anything about the p-values** … you can import [`statsmodels`] … **so you can [use it] to select the feature[s] that [have an] effect for your model**" | **第 4 题**（要论证新变量有没有用）· 小组项目 |
| **P2** | **特征不够时可以造 `x²`，但别造 `x³`、`x⁴`** | `02:12:08` "the x squared is okay. **Don't do like the x cube[d] or [x] to the power of four — it's too much for your … project.**" | 小组项目（⚠️ 与 notebook 自己造到 x¹⁵ 矛盾——那是**故意的反面教材**） |
| **P3** | **丢哪一个 dummy 都行，不必丢第一个** | `02:26:36` "**it doesn't matter. [You don't] have to drop the first one.**" | **第 4 题**（`cancellation_policy` 造 dummy） |
| **P4** | **训练/测试比例自己定** | `02:31:25` "[Maybe] 30% for the test, like [70] for the training. **It's your design.**" | **第 3、4 题**（⚪ 但报告里要写明用了多少） |
| **P5** | **特征要自己挑，notebook 的 5 个只是示例** | `02:21:53` "**when you do your [group project] you need to think about which feature I should select**" | 小组项目 |
| **P6** | ✅ **可以用 AI 帮你写代码** | `02:34:18`（**录音最后一句**）"if you don't understand and you want to … leverage the [LLM] … **you can just include this kind of [prompt] to the AI and it will help you to generate the code**" | 全部（⚠️ 仍受 syllabus 的 GenAI 政策约束，见 §1） |

**🎙️ 关于第 3 题（40 分）的一条重要空白**：

> ⚠️ **助教在 cell 23 上只停了 37 秒，`sqrt(MAE)` 的 bug 和"在训练集上选 alpha"这两个问题一个都没提。**
> ⚪ 由于**课上没有给出任何相反的口径**，两种做法都能自圆其说。
> 学习复盘应分别报告训练内比较与验证选择；没有“必选最小 alpha”或采用验证一定加分的保证。见 T02 §8.1 Q3 与 A02 官方对照。

**题目**（notebook 原文）：

1. **(10 分)** Dataset Generation：按 `y = 10x + 15` 生成训练数据，另生成一份评估数据
2. **(10 分)** 用 **MAE** 评估第 1 题的模型
3. **(40 分)** Ridge Regression：在 "Section 3.4" 里试 `alpha` = **0.001 / 0.01 / 0.1**，比较三个模型的表现，**指出哪个 alpha 最好**
4. **(40 分)** Airbnb Price Prediction：在 "Section 3.6" 里**加入 `cancellation_policy` 作为新的自变量**，评估新模型并**与原模型比较**

**读题与协议限制**（详见 [[T02-回归实战-从合成数据到Airbnb定价#8.1 逐题读题、答案来源与复盘|T02 §8.1]]）：

| 题 | 坑 |
|---|---|
| 1 | 原题未写噪声；官方参考选择加噪声，不能反写为必须。历史个人训练式调换斜率/截距，学习复盘已明确 |
| 3 | 原 tutorial 未缩放训练内比较；官方缩放后训练内最佳 0.001，个人固定留出验证最佳 0.01。必须连着协议说，训练内分数不单独证明泛化最佳 |
| 3 | notebook 里**根本没有 "Section 3.4"**（只有一个 "3.6"）。指的是 Ridge 那一段（cell 16–24） |
| 4 | `cancellation_policy` 有 5 个类别，其中 **`super_strict_60` 只有 8 行**（0.012%）。⚪ 建议先合并稀有类别 |
| 4 | 在相同留出行比较原/新模型。保存 MAE 0.438920→0.437968，按显示值相对下降约 0.217%；两份全表先 fit 编码器的限制保留 |

### W03 / W04 个人作业（已发布，见上方 ⏰ 最近的截止）

| 周 | 上课日 | 作业 | 截止 |
|---|---|---|---|
| W03 | 2026-09-16 | **Assignment Week 3**（3 题 100 分 ↔ Canvas 10 分，Airbnb + 项目数据） | ✅ **2026-09-25（五）23:59** |
| W04 | 2026-09-23 | **Week 4 Assignment**（新四题 100 内部分，Canvas 10 points） | ✅ 2026-10-02（五）23:59（香港时间，9/30 已核） |

> 📐 **规律**（三次一致）：作业在上课当天挂出，**截止 = 上课后第 9 天（下下周五）23:59**，Canvas 每次 10 分。

### W05–W11 个人作业

⏳ **尚未发布。** 按"约 8 次"推算，每周一次（W06 是 Project Briefing 周，可能跳过）。

> ⚠️ **Syllabus 与 Canvas 的周次错位一周**：Syllabus 写 W03 = Feature Selection / PCA、W04 = Clustering；实际 W3 讲了描述性分析（M03）、W4 讲特征工程（M04）。**下表 W05 起的主题按 Syllabus 顺延一周填写，仍是推算**——是否影响 Proposal（End of Week 5）与 Briefing（W6）的日期待核（§3.2、§6）。

| 周 | ⚪ 推算上课日 | ⚪ 推算作业截止 | 主题（⚪ 按顺延一周推算） |
|---|---|---|---|
| W05 | 2026-09-30 | 2026-10-07 | Clustering (Bisecting KMeans, DBSCAN)（Syllabus 原 W04） |
| W06 | 2026-10-07 | — | **Project Briefing，⚪ 可能无作业**；⚪ 或 Classification (Decision Trees, Ensemble)（Syllabus 原 W05）若顺延 |
| W07 | 2026-10-14 | 2026-10-21 | Time series (1) / Holt's Model（⚪ 若整体顺延则为分类） |
| W08 | 2026-10-21 | 2026-10-28 | Time series (2) / Exponential smoothing |
| W09 | 2026-10-28 | 2026-11-04 | ANN + RNN |
| W10 | 2026-11-04 | 2026-11-11 | Image Mining |
| W11 | 2026-11-11 | 2026-11-18 | Model Assessment / GenAI Competition |

---

## 3. 小组项目（合计 30%）

> **A06 项目准备**：2026-09-30 记录为已定 Olist、6 人各自探索角度；官方数据和九表学习导览位于 `assignment/graded/A06-group-project/`，入口为 [[IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/notes/开始这里|Olist A06 学习入口]]。35-cell Notebook 仅修订教学 Markdown，原代码与保存输出不变；本次没有运行单元格或训练模型。项目 draft、本人学习/团队分工/提交状态不变；Canvas 登录跳转是 2026-09-30 的历史记录，未作今天现行要求核验。教学发布与 HTML 重新标准导出的完成状态见本批回执。


出处：`IS6400 Project Guideline.pdf`（2 页）+ Syllabus + W1 讲义 p.11

### 3.1 时间线

```mermaid
timeline
    title IS6400 小组项目时间线（⚪ 日期为推算）
    W01–W04 : 组队 + 找数据 + 定题
            : Canvas → People → Group 加组员
    W05 (⚪ 09-30) : ⚠️ Proposal 交（Guideline 写 End of Week 5）
                  : 同周有 proposal 的指导与训练
    W06 (⚪ 10-07) : ⚠️ Project Briefing（课程表写 W6）
                  : 5% · ≤5 页 PPT · ≤3 分钟
    W07–W11 : 做分析
    W12–W13 (⚪ 11-18 / 11-25) : Final Presentation
                              : 15% · 8 分钟 + 2 分钟 Q&A
    学期末 : Final Report 10%
           : ⚠️ Guideline 写的 "May 1" 是残留，日期待定
```

### 3.2 ⚠️ Briefing 到底是 W5 还是 W6？

| 材料 | 说法 |
|---|---|
| **Project Guideline** | "Group Project Briefing 5% — **Begin: End of Week 5  Due: End of Week 5**"；"Each group must submit a Group Project Proposal **by the end of Week 5**" |
| **同一份 Guideline 下一句** | "detailed instructions, guidance, and training will be provided in **Week 5** (lecture + tutorial)" |
| **同一份 Guideline 再下一句** | "Preview: **Week 6** will be an engaging and meaningful session designed to equip you for success!!!" |
| **Syllabus 课程表** | **Week 6 = Project Briefing** |
| **W1 讲义 p.6 课程表** | 同 Syllabus |
| **Canvas 2026-09-22 公告** | [Project Briefing in Week 6](https://canvas.cityu.edu.hk/courses/71457/discussion_topics/635126)：明确说 **Week 6** 做 briefing，只介绍团队、数据与计划，**不需展示分析**；具体提交截止仍未给出 |

⚪ **最可能的真实安排**：W5 讲怎么写 proposal → **W5 末交书面 proposal** → **W6 上台做 briefing 演示**。

> ✅ **2026-09-16 用户曾确认 Briefing 顺延**；2026-09-22 Canvas 新公告直接写 **Week 6**，较早的 W07／10-14 推算不能再当当前安排。**具体日期与提交时刻仍以 Canvas 后续入口为准**，Notion 课表库未改。

### 3.3 组队

| 材料 | 人数 |
|---|---|
| **官方课程目录** | "Each team will contain **4 to 6** students" |
| **Project Guideline** | "Please form a project team (with **max 6** students) within your section" |
| **W1 讲义 p.11** | "**Max 6** students in a group" |
| **Syllabus** | "The maximum number of students in a group is **5**" |

⚪ **2 比 1 支持 6，且只有官方写了下限 4** → 建议按 **4–6 人**组队，**不要组 3 人以下**，并课上确认。

**怎么组队**：`Canvas → People → Group` 自己加组员。⚠️ 必须**在自己的 section 内**组队。

### 3.4 Proposal / Briefing（5%）

| 项 | 要求（Guideline 原文） |
|---|---|
| 时机 | 到这一步你**应该已经拿到数据集，或至少已经定位到数据并准备好去取** |
| 长度 | **No more than 5 pages of PPT** |
| 演示 | **No more than 3 minutes** |
| **必含五项** | ① **Business Problem** — 清楚说明项目要解决的商业问题<br>② **Dataset Description** — 说明打算用的数据集，**包括字段名与数据类型**<br>③ **Key Variables** — 打算分析哪些变量<br>④ **BDA Methods** — 打算用什么分析/建模方法<br>⑤ **Potential Contribution** — 预期的商业洞察或贡献 |

> 💡 **这五项正好是 CRISP-DM 的前四步**（见 [[M01-导论-商业数据分析全景与工具链#2.5 ⭐ BDA 流程：CRISP-DM 六步（本讲的项目过程核心）|M01-导论-商业数据分析全景与工具链 › 2.5 ⭐ BDA 流程：CRISP-DM 六步（本讲唯一的核心内容）]]）。讲义 p.31 也明说："**Your group project may follow this process (except deployment if not applicable)**"。
>
> ⚠️ **第 ② 项要求"字段名与数据类型"意味着 W5 之前必须真的拿到数据**，不能只有一个想法。参照 [[IS6400_Business_Data_Analytics/_meta/数据集卡片|数据集卡片]] 那种写法。

### 3.5 选题（Guideline 的两类）

| 类型 | 特征 | 期望 |
|---|---|---|
| **① 直接商业应用型** | 数据量可以小、方法可以不复杂，但**解决方案要能被企业直接用**（有 manager 背书更好） | "build some **gold-standard solutions** for the problems you may meet in future" |
| **② 大数据技术型** | 数据量大、技术较复杂，与商业相关但不一定有真实"客户" | 练技术，为行业的大数据趋势做准备 |

**Guideline 原文的偏好**：
> "You can examine problem encountered within your **team, department, student union, company, and family**."
> "**Problems with an application background are more preferred than problems copied from a textbook.**"

**推荐数据源**（W1 讲义 p.11）：
- [Kaggle Datasets](https://www.kaggle.com/datasets) · [Kaggle Competitions](https://www.kaggle.com/competitions)
- [UCI ML Repository](https://archive.ics.uci.edu/ml/index.php)
- [Google Dataset Search](https://datasetsearch.research.google.com/)

⚠️ **本课的 `Airbnb.csv` 也可以直接用**，但注意它**没有任何时间字段**，做不了时间序列（W07–W08）。见 [[IS6400_Business_Data_Analytics/_meta/数据集卡片#5.6 样本代表性 / 潜在偏见|数据集卡片 › 5.6 样本代表性 / 潜在偏见]]。

### 3.6 Final Presentation（15%）· W12–W13

| 项 | 要求（Guideline 原文） |
|---|---|
| 时长 | **8 mins + 2 min Q&A** |
| 内容 | business problem、data、your analysis、findings、conclusions |
| **口吻** | **"Please pretend that your audiences are managers in your company"** —— 用给经理汇报的方式讲 |
| ⚠️ 全员参与 | **"All team members need to present"** 且 **"All team members need to attend the Q&A session"** |
| 提交 | 组代表在截止前把 slides 传 Canvas |
| 状态 | 到这一步 major findings 应该已完成；报告里还可以做小幅调整 |

> ⚠️ **注意 Presentation（15%）比 Report（10%）分值更高。** 官方 CILO 4（"Creatively communicate analytical procedure and results effectively in **presentations** with oral, written and electronic formats"，权重 10%）就是它的依据。**别把演示当附属品。**
>
> ⚠️ 官方目录的 AT2 备注写的是 "an oral presentation (**about 10 min duration**)"，与 Guideline 的 "8 mins + 2 min Q&A" 合起来正好 10 分钟 ✓ 一致。

### 3.7 Final Report（10%）

| 项 | 要求 |
|---|---|
| **截止** | ⚠️ Guideline 原文写 **"Due by May 1, 11:59PM"** —— **这是上一学年的残留**（本课是 Semester A，9–12 月）。**日期必须以 Canvas 为准**，⚪ 推算在 W13（2026-11-25）之后 |
| 篇幅 | **20–25 页**（**11 号字、双倍行距**）。表格与图放正文，参考文献放附录，**附录计入页数** |
| 提交 | 组代表传电子版到 Canvas。**NO HARD COPY IS NEEDED** |
| 迟交 | **每天 −10%** |

**必含结构**（Guideline 原文逐条）：

1. **A Cover Page** with team members info
2. **An one-page Executive Summary**
3. Description of the specific **business problem**
4. Description of the **data** you collected（含数据收集过程，如果有）
5. **Description of your analytical procedure and related analytical results**
   > 原文举例："you first apply **descriptive statistics** to show XXX, then you apply **regression analysis** to show YYY, after that, you conduct **time series (or text analytics)** to find ZZZ."
   > ⚠️ **"Please interpret your results in the way that a layman can understand."**（要让外行看得懂）
6. **Conclusion**
7. **References**（期刊文章、教科书、网络杂志等；"may not need to be comprehensive since this is not an academic paper"）
8. Any other materials that you think are relevant and interesting

> 💡 **第 5 条那句举例很有用**：它暗示了教授期望的分析链条是 **描述统计 → 回归 → 时间序列/文本分析**，也就是**至少用两三种方法**，不是只跑一个模型。

### 3.8 官方目录的评分 criterion（Syllabus 没有）

| AT | Criterion |
|---|---|
| AT2（小组项目） | ③ **frame the problem to the models… push the ability of the model to a high level**（把问题框成模型；把模型能力推到高水平）<br>④ contribute to the project and deal with issues in collaboration（贡献与协作） |

> 💡 **criterion ③ 说明评分是两块**：**问题建模能力** + **技术深度**。报告写得漂亮但模型简单，或者模型很花哨但和商业问题脱节，都拿不到高分。

---

## 4. Class Participation（5%）

> Syllabus 原文："In **several classes that are chosen randomly**, an **in-class quiz (and signup sheet)** will be conducted during the class. **The portion of times that you conduct quiz correctly (and in class)** will be used to assess your participation grade."

**机制拆解**：

| 要素 | 说明 |
|---|---|
| 抽哪几节课 | **随机**，事先不知道 |
| 抽中时做什么 | **堂上小测（in-class quiz）+ 签到表（signup sheet）** |
| 怎么算分 | **"你答对的次数 ÷ 被抽中的次数"** |
| 缺课的后果 | 那一次直接记 0（分母不变，分子少 1） |

**W1 讲义 p.9 的补充要求**：
> "Regular attendance is **compulsory**. You are **not allowed to check your emails, access Web sites not related to the course** or work on something that is beyond the scope of this course during the class time."

**W1 讲义 p.3 的 Class Policy**：
> - **No Cell Phone in classroom**
> - Pay mutual respect to each other / Do not disturb your fellow classmates
> - **Attend the classes punctually**
> - **Academic Honesty** — "Plagiarism is a **SERIOUS** offense at CityU. Don't do it. If you're in doubt, discuss with your lecturer or tutor"

> ⚠️ **实际含义**：这 5% 不能靠"期末补"。**每一节课都可能是那一次。**

---

## 5. 期末考试（40%）

| 项 | 信息 | 出处 |
|---|---|---|
| 时长 | **2 小时** | 官方课程目录 `Examination Duration (Hours) = 2` |
| 开卷/闭卷 | ✅ **闭卷**（2026-09-09 用户确认：教授课上说了）。W1 讲义 p.8 印的 "2hour (**open/closed book**)" 是模板未删干净 | 🎙️ 教授口述，用户转述 2026-09-09 |
| 语言 | **英文** | 官方 `Medium of Assessment: English` |
| 及格线 | **至少拿 20%** | 官方 `Minimum Examination Passing Requirement (%) 20` |
| **范围** | **"will cover the readings assigned in class as well as the lectures, tutorials, and cases and examples mentioned in class"** | 官方目录 Additional Information for ATs |
| GenAI | **未标注**（不在 ATs 表内） | 官方目录 |

> 🔴 **"the readings assigned in class" 这一句很重要**：讲义每一讲的标题页右侧都写着指定阅读（W1 = **DM Chapter 1 + HM Chapter 1**，W2 = **HM Chapter 4**）。**只看 slides 可能不够。**
>
> - **DM** = Tan, Steinbach, Karpatne, Kumar, *Introduction to Data Mining*（官方列为 **Compulsory Reading**，2019 第 2 版）
> - **HM** = Aurélien Géron, *Hands-On Machine Learning with Scikit-Learn and TensorFlow*（官方列为 **Compulsory Reading**）

**已知的指定阅读**：

| 周 | Reading Material |
|---|---|
| W01 | DM Chapter 1 · HM Chapter 1 |
| W02 | **HM Chapter 4**（Training Models） |
| W03+ | ⏳ 待各讲讲义确认 |

---

## 6. ⏳ 待确认清单

> ⚠️ **2026-09-09 更新**：W02 转录已合并，**下表第 1–10 条中没有任何一条能从录音里得到答案** —— 教授和助教在整堂课里**没有提到过任何日期、任何占分、任何考试形式**。
> **原因有两个**：① 这类行政信息通常在 **W01 讲**（而 W01 无录音，永久缺失）；② W02 录音的**开头缺 p.1–p.2、结尾缺约 13–15 分钟**，作业宣布很可能落在缺口里。
> **→ 因此下表全部仍然待确认，且只能靠 Canvas 或直接问教授。**

| # | 待确认 | 怎么确认 | 紧急度 | 🎙️ 转录里有吗 |
|---|---|---|---|---|
| 1 | ~~T01 作业的真实截止日~~ | — | ✅ **已解决：9/11**（用户确认）。具体时刻待核 | ❌ 无 |
| 2 | **T02 作业的真实截止日** | Canvas / 课上 | 🔴 高 | ❌ **无**（作业本身都没被提到，见 §2 W02） |
| 3 | 作业到底 8 次还是 5~10 次 | 课上 | 🟡 | ❌ 无 |
| 4 | **Project Briefing 是 W5 交还是 W6 演示** | 课上 / Canvas | 🟡（✅ 9/16 已知**顺延**，⚪ 约 W07 10/14；精确日期待 Canvas） | ❌ 无 |
| 5 | **Final Report 的真实截止日**（Guideline 的 "May 1" 是残留） | Canvas | 🟡（学期末） | ❌ 无 |
| 6 | **小组人数**（4–6 / ≤5 / ≤6） | 课上 | 🟡 | ❌ 无 |
| 7 | **期末考开卷还是闭卷** | 课上 | 🟡（影响复习策略） | ❌ **无**。⚠️ W1 讲义 p.8 写的是 "2hour (**open/closed book**)"，两个词都在；转录也没有 → **必须直接问** |
| 8 | 期末考的具体日期与地点 | 学校考试时间表 | 🟢 | ❌ 无 |
| 9 | Participation 抽到几次课 | 无法预知 —— **每节都要到** | — | ❌ 无 |
| 10 | 香港公众假期是否会造成课程顺延 | 校历 | 🟢 | ❌ 无 |
| 11 | ~~Week 3 Assignment 的截止日~~ | — | ✅ **9/25（五）23:59，10 分**（Canvas 截图）；提交文件类型限制待上传时看 | — |
| 12 | Week 4 当前版本／截止／格式 | 2026-09-30 Canvas 与用户新下载附件 | ✅ 已核 | 10/2 23:59（香港时间），HTML／PDF，10 Canvas points／100 内部分 |
| 13 | **Syllabus 周次顺延一周后，W05 起的主题、Proposal 的精确日期** | 课上 / Canvas | 🟡（✅ Briefing 已确认顺延） | ⏳ |
| 15 | **W03 讲义是否讲完**（9/16 当天课未结束时记录）；若没讲完，W4 是否先补 W3 | 课后 / 转录 | 🟡 | ⏳ |
| 14 | **关联规则（M03 p.35–49）是否属于考试范围** | 课上 | 🟡 | ⏳ |

### ✅ 转录确实带来的三条新信息

| # | 内容 | 出处 |
|---|---|---|
| 1 | **W02 的材料要自己从 Canvas 下载**（数据 + tutorial 代码模板），并在本地跑 | 🎙️ `01:48:15` "Please download all the materials on Canvas, including the data and [the] tutorial code template" |
| 2 | **tutorial 在 2 pm 开始**（教授的讲义部分讲到约 13:48 结束，随后交给助教） | 🎙️ `01:48:41` "At [2] pm. That is all for the lecture part." |
| 3 | **W11 会讲 Model Selection** —— ✅ 与 Syllabus 一致（⚠️ 而 notebook cell 2 写的是 "to be continued in **week 10**"，**以教授口述的 W11 为准**） | 🎙️ `01:30:54` "we will learn that **in week 11** we will have model selection" |

---

## 7. 日历速览（⚪ 全部为推算，需 Canvas 核实）

| 日期 | 事件 |
|---|---|
| 2026-09-02（三） | W01 上课 · T01 作业发布 |
| **2026-09-09（三）** | **W02 上课** · T02 作业发布 |
| **2026-09-11（五）** | 🔴 **T01 作业截止**（✅ 用户确认；时刻待核） |
| **2026-09-16（三）** | W03 上课 · ~~⚪ T02 作业截止（上课前）~~ ✅ 实际 9/18 23:59（见 §2 W02） |
| **2026-09-16（三）** | **W03 上课（M03 描述性分析）** · ✅ **Week 3 Quiz（12:00–14:00，1 分）** · Assignment Week 3 发布 · W4 材料同日放出 |
| **2026-09-18（五）** | 🔴 **Assignment Week 2 截止 23:59** |
| 2026-09-23（三） | W04 上课（M04 特征工程） |
| **2026-09-25（五）** | 🔴 **Assignment Week 3 截止 23:59**（✅ Canvas） |
| 2026-09-30（三） | W05 上课（⚪ 聚类） |
| ✅ 2026-10-02（五） | Week 4 Assignment 截止 23:59（香港时间，9/30 Canvas 已核） |
| 2026-10-07（三） | W06（⚪ 分类，或 Proposal 讲解）· ⚪ **Proposal 截止顺延至 W6 末（≈ 10/09–10/10）** |
| ⚪ **2026-10-14（三）** | **W07 · Project Briefing（5%）——✅ 已确认顺延，⚪ 按一周计** |
| 2026-10-14（三） | W07 上课 |
| 2026-10-21（三） | W08 上课 |
| 2026-10-28（三） | W09 上课 |
| 2026-11-04（三） | W10 上课 |
| 2026-11-11（三） | W11 上课 · **Competition: GenAI for BDA** |
| **2026-11-18（三）** | **W12 · Group Presentation（15%）** |
| **2026-11-25（三）** | **W13 · Group Presentation（15%）** |
| ⏳ 待定 | **Final Report 截止（10%）** |
| ⏳ 待定 | **期末考试（40%，2 小时）** |

---

## 相关

- [[IS6400_Business_Data_Analytics/00-课程总览|00-课程总览]] ｜ [[IS6400_Business_Data_Analytics/_prep/课程前置资料|课程前置资料]]
- 作业原文与逐题攻略：[[T01-Jupyter入门与Pandas基础#7. 本次作业（notebook cell 24 原文）|T01-Jupyter入门与Pandas基础 › 7. 本次作业（notebook cell 24 原文）]] ｜ [[T02-回归实战-从合成数据到Airbnb定价#8. 本次作业（notebook cell 38 原文）|T02-回归实战-从合成数据到Airbnb定价 › 8. 本次作业（notebook cell 38 原文）]] ｜ [[T03-数据探索实战-Iris与Airbnb的描述统计#7. 本次作业：Week 3 Assignment（notebook cell 44–48 原文）|T03 › 7]] ｜ [[T04-特征选择与PCA实战-Iris#7. 本次作业：Week 4 Assignment（notebook cell 35 原文）|T04 › 7]]
- 项目要用的数据：[[IS6400_Business_Data_Analytics/_meta/数据集卡片|数据集卡片]]
- 考试重点：[[IS6400_Business_Data_Analytics/_meta/考点库|考点库]]


## 🎙️ M03 转录追加（2026-09-18）· 课堂口头信息（转录追加）

| 事项 | 内容 | 来源 |
|---|---|---|
| 课堂小测（Week 3 Quiz）提交方式与关闭时间 | 拍照上传或 Word 文件上传 Canvas，三分钟内完成、课间也能继续做，2 p.m. 关闭；教授明确要求不要把题目拍照发给缺勤的同学 | 🎙️`42:39`–`43:28`：*"you can write down and take a picture and upload a picture to Canvas… you can also get a word file and type the answer in the word and send the word file to Canvas… The quiz will be closed at 2 p.m."* |
| 期末考允许带 A4 cheat sheet | 教授用"文档数据"举例时确认：期末考可以带一张自己准备的 A4 小抄 | 🎙️`24:20`–`24:26`：*"the A4 cheat sheet you can bring to the final exam is actually a document data"* |
| Q3 出题来源 | 由助教（TA）出题，教授目的是让作业比之前更有挑战性 | 🎙️`02:11:38`–`02:11:51`「this question was prepared by the TAs. I just asked them one time to make the assignment more challenging than what I had before.」 |
| Q3 同组变量规则 | 同一小组若用同一份数据集，组员之间必须使用不同的变量组合（如一人用属性 1/2/3，另一人用 1/2/5），不可提交完全相同的变量选择 | 🎙️`02:12:43`–`02:13:09`「different [group?] members must use different variables... but you cannot use identical attributes[,] in a single group」 |
| Week 3 作业提交方式（口头补充） | 可以直接在 tutorial notebook 基础上继续写，也可以新建一份自己复制代码 | 🎙️`02:10:22`–`02:10:38`「You can just write on top of my tutorial. Or you can generate a new one and copy my command, and the library」 |


## 🎙️ M05 转录追加（2026-09-30）· 课堂口头信息（转录追加）

| 事项 | 内容 | 来源 |
|---|---|---|
| M05 early in-class quiz | 到场小测计 attendance；答对得 full credit；可交 Word 或纸面照片到 Canvas，禁止把题目拍给未到场同学 | 🎙️ A `02:08`–`03:33` |
| W4 / 既有作业提交质量 | Notebook 代码必须执行并展示结果，导出 HTML；答案位置与题号要清楚，解释所选特征；使用 AI 后须检查占位文本 | 🎙️ B `01:01:43`–`01:05:09` |
| W5 clustering assignment | 对 iris 做 K-means / K-means++、bisecting K-means、任选 density-based 方法并呈现结果；比较 linkage 适用数据；为 course project 选择聚类算法；执行代码、解释并导出 HTML | 🎙️ B `01:30:45`–`01:32:20` |
| Week 5 Assignment（5 题，截止未在录音中说明） | Q1 KMeans(K=3)+Iris 散点图；Q2 BisectingKMeans(K=3)+机制区别；Q3 自选密度聚类、调参并统计 noise；Q4 比较 4×4 linkage 网格并给选法；Q5 为项目数据选聚类算法 | `Week5_Clustering_Tutorial.ipynb` cell 34；课堂 B `01:30:45`–B `01:32:20` |
| 聚类作业提交 / 评分口径 | 所有代码必须实际运行并展示结果；逐题标清答案位置并解释；保存 HTML 提交；未运行代码会扣约一半题分；用 AI 后要检查残留占位文字。若已交但命中课堂指出的问题，可尝试重交 | B `01:01:47`–B `01:05:09`；补充 B `01:35:24` |

## Week 5 聚类作业新登记（2026-09-30）

Notebook cell 35：Iris KMeans（10）、BisectingKMeans（20）、密度聚类和噪声（20）、四种链接网格比较（20）、项目算法选择（30），内部共 100 分。课堂 B `01:30:45`–B `01:32:20` 要求运行、展示结果、解释并保存 HTML。2026-10-06 Canvas 已核：正式截止 **2026-10-09 23:59 HKT**、10 points、上传 HTML/PDF，10/1 公告要求 HTML。个人五题与拓展已完成并空内核运行，待本人审阅；尚未提交。公开方法见 [[T05-聚类实战-Kmeans层次密度与谱聚类]] §7；Notion 已登记 [Week 5 作业](https://app.notion.com/p/3eb8310b259681a0baead571c2cfcd01)。


## 🎙️ M04 转录追加（2026-10-07）· 课堂口头信息（转录追加）

| 事项 | 内容 | 来源 |
|---|---|---|
| 项目Briefing准备（9月23日口头提醒） | 第6周Briefing，先找到队伍、准备briefing；无具体新绝对截止时刻或提交渠道 | `01:35:51`–`01:36:01`；不覆盖现行Canvas/作业登记 |


## 🎙️ T04 转录追加（2026-10-07）· 课堂口头信息（转录追加）

| 事项 | 内容 | 来源 |
|---|---|---|
| W04 tutorial一般作业指导（录音补充） | 先按官方文档示例理解接口，再换自己的数据和参数；Q2须解释SFS机制，Q3连续目标log_price用F回归，Q4森林RFE留8列；录音未另给提交渠道/期限 | `02:08:24`–`02:11:54`；当前43cell题面及已核Canvas优先，旧§7历史段不适用 |

## Week 7 分类作业（2026-10-14 材料登记）

Notebook 第 23 格（0 起算 cell 22）三题内部 50／30／20 共 100 分：五分类器与五项评估；机制／性能比较；同一分类器有无 class_weight 的比较。使用 creditcard-reduced.csv；不能照搬合成例的“0 是少数类”编码。题面与方法见 [[IS6400_Business_Data_Analytics/notes/T07-分类实战-信用审批与欺诈识别|T07 分类实战]]；按2026-10-21现行规则，本人完整答案允许公开。此处材料登记未生成或提交个人评分结果；允许公开、教学解析、本人提交与成绩分别记录。

本次已只读核 Canvas [Assignments](https://canvas.cityu.edu.hk/courses/71457/assignments)、[Announcements](https://canvas.cityu.edu.hk/courses/71457/announcements)、[Modules](https://canvas.cityu.edu.hk/courses/71457/modules) 与 Files。Week 7 模块含五附件；Assignments 可见列表与模块未见独立提交入口；Files 列表重定向课程首页，已从 HTML 文件预览核题面。10/1 [通用公告](https://canvas.cityu.edu.hk/courses/71457/discussion_topics/637007) 要求执行全部代码、展示输出、Markdown 解释、HTML 提交及逐题定位。专属截止、Canvas points、允许文件类型和额外 rubric 仍待核，不按上周日期规律推算，也不称未发布。

来源：Week 7 Classification_Tutorial.ipynb cell22；Canvas file16237312 HTML 预览；module items666015/666018/666019/683043/683044。上课日期由用户说明、媒体日期与内容核为2026-10-14。[[IS6400_Business_Data_Analytics/_meta/M06-T07-制作验收记录-2026-10-14|制作验收记录]] 保留四入口核对边界。

2026-10-14 同步闭环：Notion [Week 7 分类进度](https://app.notion.com/p/3d58310b259681578796e1ea214affe9) 与 [Week 7 作业要求](https://app.notion.com/p/3f88310b259681e79cd4f84a1df78e40)已写入并逐字段回读；截止保持空缺，已有学习／录音／转录字段不变。文件安全及检查器误报明细见 [[IS6400_Business_Data_Analytics/_meta/M06-T07-同步回执-2026-10-14|同步回执]]。


### 🎙️ 2026-10-15 转录补充：Week 7要求

来源为10月14日教程B原时钟。以下只更新已核要求，不改变本人作答、审阅、提交或评分状态；没有录到专属截止或新的提交渠道。

| 事项 | 本次确认 | 来源 |
|---|---|---|
| 五分类器 | 可沿用教程五种，也可从链接选其他分类器；须用指定creditcard-reduced数据 | TA B `01:32:50`–`01:33:35` |
| 评价交付 | 混淆矩阵之外仍要题面所列accuracy、precision、recall、F-score | TA B `01:34:09`–`01:34:37`、B `01:35:55` |
| 第二题分析 | 用完整句子展示自己的分析思路，不只关键词 | TA B `01:35:06`–`01:35:14` |
| 第三题比较 | 同一分类器有/无class_weight前后比较 | TA B `01:35:31`–`01:35:55` |
| 分值边界 | 01:33:12的ASR转成15marks，与原题50分冲突；未回听，以书面50/30/20为准 | 原notebook cell22 |
| 截止与提交 | 本次录音无专属截止、points或新提交渠道；保留Canvas既有核对限制 | 完整教程通读 |

自动语音识别（ASR）的三条过滤记录保留原件；晚段两条可能为实质指标说明，未回听不直引，现有原题和未过滤段已支持上述要求。课堂参考解析不等于本人已提交。

## A09 · Week 8 时间序列（2026-10-21 已提交，本人确认）

2026-10-21 已在本地私人作业工作区完成 Week 8 四题、实际计算、基准拓展、英文 Notebook、标准 HTML 和中文学习导览。原题内部 20/20/40/20 共 100 分；77 格成品保留 51 格教师原件，42 个代码单元空内核运行、0 error。本人已在本对话确认提交。

当前 `已提交（本人确认）`；准确提交时刻、Canvas 回执与成绩未核。以下 Canvas 信息为提交前检查记录。本日已只读核 Canvas 四入口，Notebook 与 CSV 重新下载哈希一致；可见列表未发现专属提交项、截止及 points，不推算。本人学习和审阅未确认，既有 A01–A08 状态未改。完整个人答案本次保存于本地 assignment 工作区，尚未上传 GitHub；现行公开范围按《备份与公开发布规则》，本次不执行发布。

## 2026-10-21 G/E实质审修

本批只修公开教学笔记的G/E真实缺口与原题保真，没有新增作业、截止、评分或提交事实；现有DDL/本人状态保持，私人评分成品未改。[[G-E诊断与实质修复回执-2026-10-21|本次G/E回执]]。


2026-10-21 本人在本对话确认“已提交”。状态记为已提交（本人确认）；未回读 Canvas 提交回执、远端附件字节或准确提交时刻，未核成绩。

## 🎙️ M07三源课堂行政增量（2026-10-21）

本节只登记课堂明确行政说明，不改变A09等本人作业／提交／评分状态，也不补造新的截止、points或提交入口。课堂实际日期仍未核。

| 事项 | 已核内容 | 来源与限制 |
|---|---|---|
| 当日Participation／Quiz操作 | 教授说当天没有实际quiz，但会在Canvas建立quiz项；到场学生不要提交，不提交得到当天attendance 1分，提交反而会损失部分attendance分 | S17 `02:18`–`03:24`：*"Today we have no quiz"*、*"do not submit"*、*"if you do not submit, you get one point for today's attendance"*。这是当日特殊操作，不推广为其他周规则；没有替本人点击或登记提交 |
| 历年Quiz练习 | 课堂展示上一年SMA/SES题并给3–4分钟尝试；讲义已在Canvas，无需拍照 | S17 `02:52`–`06:46`；是课堂参考题型，不等于本日需要提交，也不冒充final真题 |
| Tutorial时段 | lecture在S17 `43:25`结束，`43:29`说明*"we have a tutorial at 2pm"* | 只确认该次课堂的2pm tutorial提示；本次未取得tutorial录音，T08继续pending |


## 2026-10-27 · M01 书面来源冲突补核

本次交叉核本地 Syllabus 3 页与 Project Guideline 2 页：讲义/指南 max6 与 Syllabus max5 并存；指南 Briefing End of Week5、最多5页PPT/3分钟，讲义暂定表列Week6；报告模板 May1 11:59PM 不可直接用于本学期。指南展示8+2分钟、报告20–25页/11号字/双倍行距等均为该版本书面条件，不认证最新Canvas或本组安排。M01保留来源差异，不由本次审修新填绝对截止、成员、本人提交或可提交。


## 2026-10-27 · M02 本地源与当前行政条件分开

本地39-cell Week 2 Regression Analysis_With Prompt.ipynb 的cell38列Week 2 Assignment四问（10+10+40+40），明确代码和结果导出HTML上传Canvas，未给绝对截止。这是本地源版本事实；本次未重新核当前Canvas最新题面、截止或提交字段。631段中due/submit各1次只是一般业务叙述，未见完整作业宣布，不能据缺尾断言课上没布置。保护原任务说明和本人已确认/已提交/成绩，不用本篇材料审修升级或降级。


## 2026-10-27 · A02 学习复盘增量

A02 任务说明现有官方对照教学段补齐四题英文原题、中文条件/机制与英文自拟复盘；T02 §8 对应互链。原 Canvas 10 points、2026-09-18 23:59、Submitted! 与成绩待核等本人/行政历史字段保持，不将学习解析等同可提交或重新提交。


## 2026-10-27 · Week 7 题面重审范围

原Cell22三问英文全文、中文限定词与方法、英文参考框架见T07§2.14；第一问原文误拼credictcard-reduced.csv，实际文件为creditcard-reduced.csv。三问真实五模型训练／比较／权重实验结果本批未制作，不据方法解释称答卷完成。上方Canvas与Notion回读是2026-10-14历史记录，本轮未刷新当前DDL/points/rubric；本人学习/提交/评分不动。

## 2026-10-28 时间序列正式入口核对

- Assignment Week 8 & 9，Canvas330590，2026-11-06 23:59 HKT、20points、file upload，页无附加描述。
- Week 9 Extra Assignment，Canvas330608，同为2026-11-06 23:59 HKT、2points、file upload；原Notebook Cell82要求一份Notebook，最终接受扩展名未单独验证。

[[IS6400_Business_Data_Analytics/notes/T09-时间序列II实战-变换恢复与模型评价|T09]] 已保留Extra完整原题与参考过程。既有A09本人已提交记录保持；它与本日新可见“Week8&9”合并入口的实际回执映射仍待核，不能据新入口没有记录就撤销旧提交状态，也不自动替本人重交。

## 2026-10-31 · S20 课堂小测来源

M08四图小测：S20 `59:51`末次要求解释C→D和检验平稳，`59:58`给5分钟并交Canvas，`01:29:47`提醒当日14:00前交。具体日期未确认，早前ASR C→B与末次指令不一致；不创建猜测的绝对DDL，不改现有Week8/9正式作业、本人提交／评分。滚动一步用于项目为课堂建议，不新增强制模型条款。
