# EF5560 代码库 · 设计说明

> 这个目录存放**对课程数据集的可复现分析**。每个脚本对应笔记里的一个小节，笔记里给出脚本路径，脚本头部写明它对应哪一页讲义、哪一节笔记。
> **原则：笔记里出现的每一个由数据算出来的数字，都能在某个脚本的输出里找到。**

---

## 1. 怎么跑

```bash
# 在本目录（code/）下运行，路径都是相对本目录的
cd "D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance/code"

# 跑单个脚本
D:\anaconda3\python.exe -X utf8 L01_data/03_drawdown.py

# 跑全部（按编号顺序）
D:\anaconda3\python.exe -X utf8 run_all.py

# 单独核对讲义练习（只读课程 CSV，不写 output/，不计入 run_all 的脚本数）
D:\anaconda3\python.exe -X utf8 L01_data/check_exercises.py
```

**环境**：本机 `D:\anaconda3\python.exe` 为 Python 3.12.3；依赖见 `requirements.txt`（pandas / numpy / matplotlib / statsmodels / scipy / scikit-learn）。运行前核对实际环境，不沿用旧 `/d/python/python` 路径。
**Windows 编码**：命令中的 `-X utf8` 防止中文输出遇到 GBK 编码错误。

每个脚本跑完会：
1. 在 `output/` 下生成 **同名的 `.png`**（图）和可能的 **`.csv`**（数字表）
2. 在 stdout 打印**笔记里引用的全部关键数字**

---

## 2. 目录约定

```
code/
├─ README.md            ← 本文件
├─ requirements.txt
├─ run_all.py           按编号跑全部脚本
├─ common/              共用模块，所有脚本只从这里读数据、只用这里的绘图风格
│   ├─ load.py          统一数据入口（见 §3）
│   └─ plot.py          统一绘图风格（中文字体、配色、保存）
├─ L01_data/            对应 [[M01-金融数据与Vibe-Coding]]
├─ L02_regression/      对应 [[M02-回归与样本外设计]]
├─ L03_linear_ml/       对应 [[M03-线性机器学习与收益预测]]（数据来自 class03 结果表，loader 为 common.load.c03_*）
├─ L04_nonlinear/       对应 [[M04-非线性机器学习与收益预测]]（class04 结果表 + 共享面板，loader 为 common.load.c04_*；需 scikit-learn）
├─ L0N_.../             以后每讲一个目录
└─ output/              图与表的输出，笔记用 ![[...]] 引用
```

**脚本命名**：`<两位序号>_<内容>.py`，序号决定 `run_all.py` 的执行顺序。
**输出命名**：`output/L01_03_drawdown.png` —— 讲次 + 序号 + 内容，全库唯一，笔记里直接 `![[L01_03_drawdown.png]]`。

---

## 3. 三条硬规则

### ① 单一数据入口

所有脚本**只能**通过 `common.load` 读数据，不许自己 `pd.read_csv`。原因：

- 八个 csv 的**日期列都是字符串**，必须 `to_datetime` 否则排序按字典序——集中处理一次，不让每个脚本各踩一遍
- **收益率口径两套并存**（周频简单收益 / 月频对数收益），`load` 里每个 loader 的 docstring 写死口径，脚本里不许再猜
- 路径固定相对 `code/`，脚本从哪里启动都能找到数据

### ② 不改原始数据

`course_files_export/data/` 只读。任何清洗、衍生列都在内存里做，要落盘就写到 `output/`。

### ③ 每个脚本开头两行路径引导（固定写法）

```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))   # 让 common 可导入
```

没有这两行，`python L01_data/xx.py` 会报 `No module named 'common'`——因为 Python 只把脚本所在目录放进 `sys.path`。加了之后从任何目录启动都能跑。

### ④ 每个脚本的头部 docstring 固定格式

```python
"""
L01_03 · PDD-JD 配对交易的完整路径
=====================================
目的      讲义 p.16 只报了终点 +20.62%，本脚本画出全程净值与回撤，回答"路径长什么样"
讲义      Lec01 p.15–16
笔记      [[M01-金融数据与Vibe-Coding]] §2.10.2
输入      pdd_jd_pair_example_156w.csv（周频，简单收益）
输出      output/L01_03_drawdown.png · output/L01_03_drawdown.csv
关键决定  回撤按 (当前净值 / 历史最高净值 − 1) 定义；净值从 1.0 起算
"""
```

**"关键决定"这一格是给读者看的设计说明**：每个会影响结果的选择（口径、窗口、起点、是否年化）都写在这里，让人不读代码也知道数字是怎么来的。

---

## 4. 脚本 ↔ 笔记映射表

| 脚本 | 讲义 | 笔记小节 | 回答什么问题 |
|---|---|---|---|
| `L01_data/01_return_conventions.py` | Lec01 p.19–21 | M01 §2.3.1、§9.3 | 简单收益 vs 对数收益：同一份数据两种口径差多少？（5.87× vs 4.59×） |
| `L01_data/02_index_20y.py` | Lec01 p.17–21 | M01 §2.3.4、§2.9.2 | 四个指数 20 年累计与回撤：恒生的高点为什么还没收复？ |
| `L01_data/03_drawdown.py` | Lec01 p.15–16 | M01 §2.10.2–2.10.3 | PDD-JD 配对交易：终点 +20.6% 的路上跌了多少？ |
| `L01_data/04_leakage_audit.py` | Lec01 p.43–48 | M01 §2.7.3、数据集卡片 §7 | 特征表的每一列真的没用到未来信息吗？（逐列验算，误差应为 0） |
| `L01_data/05_prediction_clock.py` | Lec01 p.43 | M01 §2.5.4、§2.7.3 | 预测时钟：预测 2026-06 时，每个特征分别用到了哪个月的数据？ |
| `L02_regression/01_reproduce_lecture.py` | Lec02 p.9–33 | M02 §2.9 | 讲义上每一个已发布的数字（相关、斜率、p 值、R²）能否复现？ |
| `L02_regression/02_oos_rolling.py` | Lec02 p.37–50 | M02 §2.6–2.8 | 样本外 R² 随窗口怎么变？滚动 vs 扩展窗口 |
| `L02_regression/03_r2_scale.py` | Lec02 全篇 + 跨课 | M02 §2.9、M01 §2.9.3、术语总表 §2.2 | R²=1% 的散点图长什么样？为什么金融 1% 算好、IS6400 0.5 算正常 |
| `L02_regression/04_hit_rate.py` | Lec02 p.43–48 | M02 §2.7.4 | 方向命中率 vs 多数类基线：63.3% 到底强不强？ |
| `L03_linear_ml/01_reproduce_lecture.py` | Lec03 p.7–55 | M03 §2.2–2.9、§9.5 | 讲义每个数字能否复现：假数算例按公式重算；真数从 class03 五个 CSV 逐格重算（12 个市场 OOS R²、6 个个股 OOS R²、五分组价差与 t）；笔记补充的迷你例子 |
| `L03_linear_ml/02_forecast_sort.py` | Lec03 p.47–55 | M03 §2.8.1、§2.9.3 | MSE 看水平、分组看次序：六模型 OOS R² 柱状 + 四个可排序模型的五组收益曲线 |
| `L02_regression/05_official_scorecards.py` | Lec02 p.24 / 33 / 46–51 | M02 §9.5、数据集卡片 §12 | class02 补发的 8 张官方结果表 vs 本库复现：22 项逐格对照全部一致；打印 Class 5 预告的择时成绩单 |
| `L04_nonlinear/01_reproduce_lecture.py` | Lec04 p.9–51 | M04 §2.2–2.9、§4.2 | 讲义每个数字能否复现：假数算例（p.11/14/19/23/27/32/33/46）+ 真数（12 + 4 个 OOS R²、CSI 300 子窗口、三棵树的叶子人数、Techtronic、五分组价差与 t）|
| `L04_nonlinear/02_refit_trees.py` | Lec04 p.6–10、21–22、43–47 | M04 §2.2.5–2.2.6、§2.6.3、§9.5 | 用共享面板按汇总表设置重训树 / 森林 / 提升：树逐位一致（阈值 2.482 / 2.456 / 0.150），森林 / 提升近似 |
| `L04_nonlinear/03_nonlinear_sort.py` | Lec04 p.36 / 38 / 47–51 | M04 §2.5.1、§2.7.1 | 两张图：市场六模型 OOS R² + 美国提升曲线；个股三族 OOS R² + 五组曲线 + 森林重要性前 15 |

> 每写一个新脚本，在这张表加一行；在对应笔记小节加一行 `📁 代码：` 链接。

---

## 5. 笔记里怎么引用

在笔记对应小节末尾加：

```markdown
> 📁 **代码**：[`code/L01_data/03_drawdown.py`](../code/L01_data/03_drawdown.py) —— 跑一遍即可复现本节全部数字
> ![[L01_03_drawdown.png]]
```

第一行给路径（Obsidian 里可点开），第二行嵌图。**数字写进笔记时带上来源脚本名**，例如"最大回撤 −38.66%（`L01_03`）"。

---

## 6. 已知限制

- **class03/stock_linear_test_predictions.csv 曾被同步截断**（358 / 4,108 行，2026-09-21 发现，2026-09-22 重下恢复）：`L03_01` / `L03_02` 保留行数断言，文件再被截断会主动失败
- **随机森林 / 梯度提升只能近似复现**：树是确定性的（`L04_02` 逐位一致），森林差随机种子、提升的讲义实现与 sklearn 不同（美国 GB 验证 24.28 vs 表 23.35）；笔记里森林 / 提升的数字一律取结果表
- **无交易成本、无换手约束**：所有策略类计算都是"纸面"结果，M05 讲组合时要自己加
- **`csi300_macro_panel.csv` 的 `cli_gap_lag2` 含义未知**，脚本里只当普通特征用，不解释
- **前 12 行的滚动统计量用了样本前的数据**（见数据集卡片 §7），`04_leakage_audit.py` 只验证 2007-07 之后的行
- 图上中文依赖 `Microsoft YaHei`；换机器若没有，`common/plot.py` 会退到 `SimHei`，再没有就只显示英文标签

---

## 7. 变更记录

| 日期 | 变更 |
|---|---|
| 2026-09-10 | 建库。定目录约定、三条硬规则、docstring 格式、9 个脚本的映射表 |
| 2026-09-10 | 补齐其余 8 个脚本（L01_02–05、L02_01–04），`run_all.py` 9/9 ✅；映射表小节号校正（L01_02 → §2.9.2、L02_04 → §2.7.4）；`load.spy_features` docstring 的"16 个特征"改为"1 个目标 + 15 个预测变量" |
| 2026-09-21 | 加 `L04_nonlinear/` 三个脚本与 `L02_regression/05`；`common/load.py` 加 class02（8）/ class04（16）共 24 个 loader；`requirements.txt` 加 scikit-learn；发现 class03 预测表截断，L03_01 / 02 加断言；`run_all.py` 13/15（L03_01 / 02 按预期失败；9/22 class03 恢复后 15/15） |
