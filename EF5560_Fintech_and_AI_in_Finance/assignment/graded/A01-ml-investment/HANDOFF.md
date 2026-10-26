# EF5560 A01 与五课作业区：新窗口交接

更新：2026-09-27。工作目录 `D:\上课资料\CityU`。**先只读，确认电脑与手机自动同步关闭后再写入。** 本轮用户已确认两端关闭；后续会话须重新确认。原始 `course_files_export/` 只读。不提交 Canvas，不 Git commit/push，不重置现有暂存或 `.obsidian/graph.json`。

## 1. 第一眼看哪里

- 五课均从 `assignment/00-overview/作业总览.md` 进入，知识首现见同目录 `知识地图.md`。
- 本任务 [开始这里](notes/开始这里.md) 连接课程笔记、Jupyter 和提交草稿，完整教学仅维护在 [逐步实操 Notebook](work/EF5560-A01-逐步实操.ipynb)。
- **第一步：读根 AGENTS.md、`_meta/作业规范.md`、本交接，再 `git status --short`。** 不要运行已归档的旧分析脚本。

## 2. 已完成的返工

五课共 70 个 Pxx 占位目录、140 个 Markdown 文件已重新逐项盘点，无新增成果文件。按课程分布：AC6761 13、EF5560 21、IS5113 5、IS5542 10、IS6400 21。来源、链接、缺件与受阻信息合入各课 `practice/练习索引.md`，原目录移出 vault。**这只是清理与登记，不代表 70 项练习已写成精读。** 以后按讲次回填，有实质内容后才创建 `Mxx-练习精读.md`，不再创建 Pxx/tutorial 空壳。

18 项计分任务仍保留独立 `graded/Axx-*` 目录。未完成教学的条目改称 `notes/任务说明.md`；已有实质教程保留。尚未发生的客座讲座不预写课堂内容。总览首屏给下一步，后续用任务卡列评分、交付与缺口。

EF5560 Notebook 共 36 个代码 cell，Q1–Q5 逐步展示核心计算，每步有目的、新概念、可运行代码、结果解释和「所以呢」。数据路径只在第一格配置。代码使用现有工具格式化，AST 与已验收计算一致；Q4 用简短公式并解释 base、zero,j 和正负例子。

## 3. 数值与复现证据

- 20,800 行；训练 78 周/6,240 行，验证 26 周/2,080 行，隐藏 156 周/12,480 行；每周 80 股、17 特征。
- Table 1、2、3 分别 4、18、5 行，与归档基线最大绝对数值差均 **0**。LASSO alpha 0.003727593720314938；森林 depth=5、leaf=10、200 棵树、seed=2026。最终 OLS / top16-sector-cap6 不变。
- 权重 SHA-256：`D7A74ECD2730FFC8790AB703BA6F6BA8EFCCB55BE752133C7645F347925ECCF8`。旧 output 使用 CRLF，旧 submission 用 LF；Notebook 改为直接写 LF，仅统一换行，与指定提交草稿逐字节一致。
- 已用 `D:\anaconda3\python.exe` 的 `python3` 空内核运行；也在 Jupyter 界面点击 **Restart the kernel and run all cells**、确认重启、运行并保存。Jupyter 扩展会占用部分执行序号，代码格有序且无异常，不要求界面序号相邻。
- Figure 1–4 与 Figure A1 齐全；官方 `check_submission_2026.py` PASS（156 dates、80 stocks）。
- 源码 ZIP 为同一 Notebook 的清除输出副本 + `build_report.py`、`package_draft.py`、`safe_write.py`，无数据、无旧单体分析源码。Notebook 在 ZIP 内名为 `EF5560-A01-step-by-step.ipynb`，便于 PDF 正文显示文件名；单元格正文与本地教学版一致。
- 已在 vault 外解压源码 ZIP，第一格填写官方数据路径，空内核运行；三表与权重一致。报告构建仍读原文件名与 JSON 结构。
- PDF 保持 **A4 共 8 页：7 页正文含封面 + 1 页附录**。8 页逐页查看：p.2 Figure 1/目标与误差，p.3 Table 1/Figure 2，p.4 Table 2/Q3，p.5 Q4/Figure 3–4，p.6 Table 3/风险，p.7 实现与边界，p.8 Figure A1；图表标签和公式可读、无溢出。
- Obsidian 实走 `assignment → 00-overview → 作业总览 → 开始这里`，首屏见当前任务/截止/下一步，侧栏无 Pxx。Q4 已在 Obsidian 真实阅读视图检查；Jupyter 的 8 个独立公式逐式查看，无原始 LaTeX、缺字或溢出。

详细验证文件在 `C:\Users\BenLi\.codex\scratchpad\cityu-assignment-20260927`：`numeric-verification.json`、`ui-run-verification.json`、`zip-verification.json`、`final-safety.json` 与检查日志。下次应重新运行必要检查，不能用旧 PASS 代替新改动验收。

## 4. 备份、恢复与保护项

- 全库开工备份：`D:\上课资料\CityU_backups\CityU-20260927-1334.zip`。
- 本轮完整作业备份、哈希与可恢复目录：`D:\上课资料\CityU_backups\assignment-readability-20260927`。`before.zip` 保存迁移前 212 个作业文件，`before-sha256.json` 是逐文件哈希；`practice/` 保存原 70 个目录。
- 旧 EF5560 单体分析、长教程分别为归档中的 `legacy-run_analysis.py`、`legacy-tutorial.md`。归档前已完成三表、模型和权重核对，不再作为日常入口。
- Git 既有 4 项 IS6400 删除保持暂存；它们是上轮已按哈希迁入私有目录的历史文件。本轮不更改暂存区。私有 `assignment/` 仍被忽略，新 worktree 不带这些内容。
- `.obsidian/graph.json` 保持开工时字节。Obsidian/Jupyter 的视图状态、checkpoint 属本轮实际打开操作产生的应用状态，不要混同原始课件。

## 5. 当前运行入口

本机 Jupyter 使用 8897 端口，入口见 [开始这里](notes/开始这里.md)。若已退出，按其中启动命令重启；使用显式 `KernelSpecManager` 是为了保留 `python3` 名称，不改整机配置、不安装插件。

Notebook 运行后，在 vault 根依次运行报告与打包：

```powershell
C:\Users\BenLi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe EF5560_Fintech_and_AI_in_Finance\assignment\graded\A01-ml-investment\work\build_report.py
D:\anaconda3\python.exe -X utf8 EF5560_Fintech_and_AI_in_Finance\assignment\graded\A01-ml-investment\work\package_draft.py
```

首次改动前备份/快照，原子写入；完成后跑 `link_check.py`、`readme_check.py`、`integrity_check.py verify`，并复查实际阅读/运行效果。原始文件损坏时停下并从备份恢复，不重建。

## 6. 仍为 draft，尚待用户／新材料

1. 组长学号、全员英文姓名和学号仍未提供；保留 `DRAFT/LEAD_ID`。团队须逐句审读报告、确认 AI 使用说明与亲自完成的检查。不能把计算通过标成“本人已学会”。
2. 提交前重新核 Canvas Assignments、Announcements、Files、Modules。本轮没有重新联网核行政信息：此前记录正式截止 2026-10-15 14:00 香港时间，PDF 写 12:00，内部按 12:00。原 ZIP SHA-256 `CE4B9E0ECCB4BBBA5468DACC3D501A05DE7A2D3D9AEDBCDC24E03956B31F8CD9`。
3. 本轮没有更新 Notion 外部看板，计分状态未改变。可手动记：EF5560 A01 状态 draft；学习入口＝Obsidian 导览＋Notebook；分析/报告/权重复现已通过；下一步＝团队复核与身份补齐；提交状态不变。其他四课保持各自既有状态。
4. 后续按课逐讲补练习精读，先取得原题与官方解答，优先有明确材料的条目；受阻项保持受阻。当前不创建空壳 Mxx 文件。


## 2026-10-27 · A01 本次教学重审记录

A01导览与115格实操Notebook已分别完成全范围独审及原审定向复核；新增原题中英对照、模型手例与行业上限流程图。仅20格Markdown source变化，全部代码/保存输出/执行计数/metadata保持；未重训或改正式报告/CSV/ZIP。结构/AST与实际标准HTML显示已核，主写者已在隔离副本补核原生JupyterLab的LASSO公式、旧输出与行业cap流程；Markdown检查器仍不支持ipynb，不冒称其PASS。原生结构/36代码AST/全cell保持性、实际独审与原生必要显示构成本次适用验收，不代表新执行。10/21既有邮件库记录已见10/12提交，本次不改本人状态；当前Canvas/评分/上传附件未新核。原主写者已接受真实候选并完成CAS原子写回/精确回读；原发布计划内两个整文件candidate_file为过期副本，已按同计划operations.source及真实独审SHA使用最终原字节，未使用过期副本。新增SVG仅尺寸维护530×1662，节点/边/文字不变。
