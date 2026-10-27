# Olist Notebook v2 实质主报告

作者 /root/author_is6400_olist_a06_61；独审 /root/review_is6400_olist_a06_full_61；主发布者 /root。全部实际 included 教学范围为原生 35 cells（19 Markdown、16 code），不是新模型任务。

## 教学与来源

独审 stage-1.md 对全部 35 cells/29 保存输出顺读、复述与改条件判断；第二阶段 notebook-independent-review.md 对真实源/代码/diff核对。唯一阻塞 B1 已在 targeted-closure.md 对最终 v2 hash 定向关闭：orders.order_id 与方括号合法列名取列等价，取列后问唯一性，.sum() 为操作，冲突名称用方括号。S1 是未来候选比较量建议，不把非阻塞建议扩成训练任务。四个自拟理解题逐问完整，无教师英文原题，不伪造官方题；字段、候选方案、统计限制分来源。

source-audit-v1.json 和 independent-61/phase-2-independent-audit.json 分别记录真实 CSV/Decimal 算术、9 CSV/ZIP raw SHA 和 CRC。多对多 2x2 示例、日期/时间戳同分母、订单金额完整 98,665/异常303、评价记录与买家分母均核。没有任何直接 join 都重复支付的错误概括；没有把历史保存输出写成本次运行。

## 保持性与机器边界

final-preservation.json 是本批静态导出后的再次逐项核对：35 cell 结构、16 code source/AST/outputs/execution_count/metadata/id、顶层 metadata/nbformat 精确保留，Notebook 与入口字节 hash 不变。nbformat.validate 已执行，HTMLExporter 仅静态渲染，没有 ExecutePreprocessor 或内核执行。

Markdown-only proxy L 无问题、R.hard=0、37 warn，C_STRUCTURE 真实 FAIL 仍保留。完整同类警告位置与处置见 author-report-v1.md 和独审 notebook-independent-review.md：并列对象/分母条件有就地解释，32位订单ID与0.010001属于当前算例/阈值，许可不可拆改，表格具体读法及例子均在本篇。本报告不称 ipynb 通过 Markdown quality gate；native-acceptance.json 把适用项、不适用结构、未运行原因分开。绑定 checker 只核文件/hash，不认证语义或工具身份。

## 实际显示与静态导出

作者真实 CUA 截图字节、视口、候选hash 见 native-visual-v2.json。root 已实际 view B1 原生段和入口上下两帧并接受适用显示（root-native-acceptance-instruction.md）。原保存两PNG已实看；本轮不新跑图。不把 Jupyter Markdown Preview 的字面双链称为 Obsidian 导航通过。CUA 明确 Not allowed 后停止 UI；未强关用户标签。

html-export-manifest.json 绑定相同 Notebook v2，经本机标准 nbconvert.HTMLExporter 静态导出，35 cells/16 code/29 outputs/两张原PNG哈希匹配，HTML 未单独改写。HTML 最终浏览器显示尚未在本文件收批做，root 正式落地和回读另验。

## 发布边界

当前教学实质阻塞已关闭、root 接受本篇适用 native 检查；note-review-v2 与 source/candidate/独审/资产真实绑定可检查。本作者未运行 .ipynb Markdown fullgate、未写 vault/Notion/Git。完整既有行政与个人学习/团队/提交/评分状态保持；共享 typed 增量需 root 当前基线 CAS，派生 HTML 同批原子写回。Notion无新增所追踪任务/DDL/路径/个人状态/材料版本，不假称回读。
