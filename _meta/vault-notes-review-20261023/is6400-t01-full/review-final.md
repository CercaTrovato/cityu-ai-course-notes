# is6400-t01 最终作者主核对报告

作者 `/root/author_is6400_t01_a01_61`，模型 `gpt-6.1-sol`；独审者 `/root/review_is6400_t01_a01_full_61`，模型 `gpt-6.1-sol`，未参与撰写。日期2026-10-27。本文是作者对实际来源/计算/显示/警告及独审证据的逐文汇总，不冒root正式写回或同步报告。

正式目标：`IS6400_Business_Data_Analytics/notes/T01-Jupyter入门与Pandas基础.md`。真实基线SHA `a58b2f670aab0df3f4c36c9e06def01e1eb0877850749bbf95de405df3408722`；最终raw候选SHA `f09e1d6294be25313f6863402ba5df9d8f50c2cd3303b13220794e029872d5fd`，115503 bytes。scope为full，已有文件的真实source必须传给门槛。

## 教学范围与独审

T01 本次全篇范围包含§0–§9及相关、全部正文/图源/折叠内容、七Prompt与其10个作答单元、cell24四题及Q4三个动作的6个作答单元，共8父项16作答单元。R1 source代码AST七段一致，原25cells逐一定位；源Prompt完整英文、中文题意、自拟英文参考答案均回原件核查。原source七个非空课堂cell在作者新Python命名空间实际执行；本人/官方评分代码、A01脚本没有执行。新R2只做切片/二维@/参数同步改名的隔离检查，详calculations-r2.json。原七段fenced Python未变，10个图源仅8改变。

原独立审查者完成R1全篇后指出B1二维切片、B2首次@、B3参数改名三个阻塞。作者修正文，原审者逐项定向复核关闭并核全部11修改、8diff hunk及实际显示。原R1报告pending是历史状态，最终由targeted-closure.md明确绑定f09e...候选passed；没有重写旧报告或假称R2又整篇重读。

独立理解依据：R1全部1664行两阶段全文报告 + targeted-closure.md对R2全部11项变化与依赖的关闭，范围并集覆盖最终1670行；B1/B2/B3均真实关闭。

## 来源、计算与限制

六份只读源SHA在sources/source-manifest.json，本文绑定其实际字节。作者与独审者已逐源核25cell notebook、官方9cell和本人27cell HTML代码/保存输出、教学脚本、W1讲义必要页和Syllabus三页。原metadata Python3.13.5不是当前运行版本，作者隔离课堂执行为Python3.12.3/pandas2.3.3/NumPy1.26.4。源describe只存两列，而当前含time，区分源版本未知与本次结果。

重要算术包括四分数sum345、4×4对象Gram、2×2特征Gram29861/613/15、样本std5.909033和分位插值、新非方阵及边界；保存时刻差官方0.067639秒/本人3.004368秒不当新执行。具体输入/结果/执行边界见classroom-calculations.json与逐文独审手推。R2另calculations-r2.json。它们不证明本人已学会或教师评分。

无本讲转录仍v0.9/pending，不认证口头澄清/略过/考试政策。官方目录只有2026-09-09、effective2025/26旧引用，当前原页/政策未重核，T01已就地限定；不由历史引用推出新任务许可。Canvas未在线刷新、远端提交附件字节未比、教师评分未核，这些明确限定不伪造补齐。

## 显示与机械疑点

作者首轮实际看10图与矩阵窗口；最终仅图8变，作者和原独审者实看visuals-r2图8及B1/B2/B3四窗口，其余9图同源未变承接原证据。浏览器，非Obsidian。

R2 current-check-r2.json L/C/R硬项0、R.warn127；independent-61/warnings-adjudication.json全类型原位置与targeted-closure.md新增内容核查；historical FAIL照实保留。

 source-checks.json只检查原题源哈希/字面/逐问中英锚点；T018父项、A01四题按各自契约，语义来自实际回源/独审。未提供或未核的范围不写源契约通过。机器PASS不替代独立理解或实际显示。

## 状态与后续

当前本篇教学/来源/警告及必要显示无未决阻塞，可绑定本raw候选。formal writeback、共享3grade修正、本地适用同步、Notion和Git仍未执行；root须按真实基线CAS、原子写和回读，按publication-plan-final.md一次应用共用增量，保护个人字段。回执unresolved=[]仅指本次发布前教学核对，不表示外部同步已完成。
