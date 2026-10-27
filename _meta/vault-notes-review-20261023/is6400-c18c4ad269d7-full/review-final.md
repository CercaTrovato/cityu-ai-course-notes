# is6400-c18c4ad269d7 最终作者主核对报告

作者 `/root/author_is6400_t01_a01_61`，模型 `gpt-6.1-sol`；独审者 `/root/review_is6400_t01_a01_full_61`，模型 `gpt-6.1-sol`，未参与撰写。日期2026-10-27。本文是作者对实际来源/计算/显示/警告及独审证据的逐文汇总，不冒root正式写回或同步报告。

正式目标：`IS6400_Business_Data_Analytics/assignment/graded/A01-week1/notes/tutorial.md`。真实基线SHA `7f9ba99e7acf09e7e3d87a7c8150640e1b8ccdc161077322142b80719def8157`；最终raw候选SHA `64a76a0de436f17b7d4f67df632fce65f15965388f8625092ce5c35f0fccbdab`，16899 bytes。scope为full，已有文件的真实source必须传给门槛。

## 教学范围与独审

A01 本次单独范围为完整241行学习教程，含§0完整英文原题、Q1–Q4逐题原文/中文限定词/代码及语法解释/输出口径/英文参考、历史来源比较、导出边界及全部自测答案。Q4三个动作，原题无点积要求。原独审者逐单元实际顺读/手推/回源后passed，不依赖T01。

教学用虚构80/90是170；官方保存expected scores95/100是195并给出grade和3；本人保存HTML明确用课堂四行df得345。它们不是同输入不同答案；grade原件业务含义未定义，仅编码。本人已提交和due字段沿真实基线，不升级学习/自测/评分。不运行work/week1_practice.py、评分代码或用户kernel；仅只读代码/保存输出与独立算术。

独立理解依据：independent-review-a01.md对64a76候选241行单独完成两阶段全文审查passed，当前字节未变；不借T01通过替代。

## 来源、计算与限制

六份只读源SHA在sources/source-manifest.json，本文绑定其实际字节。作者与独审者已逐源核25cell notebook、官方9cell和本人27cell HTML代码/保存输出、教学脚本、W1讲义必要页和Syllabus三页。原metadata Python3.13.5不是当前运行版本，作者隔离课堂执行为Python3.12.3/pandas2.3.3/NumPy1.26.4。源describe只存两列，而当前含time，区分源版本未知与本次结果。

重要算术包括四分数sum345、4×4对象Gram、2×2特征Gram29861/613/15、样本std5.909033和分位插值、新非方阵及边界；保存时刻差官方0.067639秒/本人3.004368秒不当新执行。具体输入/结果/执行边界见classroom-calculations.json与逐文独审手推。R2另calculations-r2.json。它们不证明本人已学会或教师评分。

无本讲转录仍v0.9/pending，不认证口头澄清/略过/考试政策。官方目录只有2026-09-09、effective2025/26旧引用，当前原页/政策未重核，T01已就地限定；不由历史引用推出新任务许可。Canvas未在线刷新、远端提交附件字节未比、教师评分未核，这些明确限定不伪造补齐。

## 显示与机械疑点

作者实际看A01 Q4代码/两行表/转置LaTeX/求和表窗口；原独审者实际看a01-q4-formula.png。原64a76字节未变承接，浏览器非Obsidian。

current-check.json L/C/R硬项0、R.warn9；independent-review-a01.md逐类说明及warnings-adjudication.json，historical FAIL照实保留。

 source-checks.json只检查原题源哈希/字面/逐问中英锚点；T018父项、A01四题按各自契约，语义来自实际回源/独审。未提供或未核的范围不写源契约通过。机器PASS不替代独立理解或实际显示。

## 状态与后续

当前本篇教学/来源/警告及必要显示无未决阻塞，可绑定本raw候选。formal writeback、共享3grade修正、本地适用同步、Notion和Git仍未执行；root须按真实基线CAS、原子写和回读，按publication-plan-final.md一次应用共用增量，保护个人字段。回执unresolved=[]仅指本次发布前教学核对，不表示外部同步已完成。
