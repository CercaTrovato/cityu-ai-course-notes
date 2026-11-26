# 五课 Canvas 全材料审计 · 2026-11-26

本批覆盖学生当前可见的全部文件入口，并将教师材料、本人成绩/交件记录和实际学习状态分开。完成的是文件身份核对、归档与三阶段处理判定；审计时的处理判定与本批实际制作结果分列，不能称全部笔记/全部外部来源已补齐。

## 覆盖与版本

- 教师/课程源 **153 个文件身份**：四课完整Files列表，加IS6400可见模块/公告附件。153份均已实际下载并记录SHA-256，与本地按哈希去重。
- **37条学期公告、29个作业入口、各课模块和大纲正文**已查；模块include items数量均完整。
- **29条本人交件/反馈记录、28个实际已交附件**已读，28附件均下载核验；历史交件与当前版本分别记录。
- 10份本地尚未表示的原始内容已补归档；姓名/学号名单、排期和组内交件走私有原件范围，公开矩阵不带下载令牌/评论原文。
- IS6400全Files列表返回未经授权；本批覆盖其可见12模块/75项、62个模块文件身份及1个公告附件，不声称取得教师后台隐藏文件。

AC6761的11份PPT远端与本地完全同字节，11/25的updated_at不是内容改写证据。Analyze balance sheet.docx与本地“2 Analyze balance sheet.docx”同字节，已有M03承接；两个IS5542模板ID也是同字节。配套Notebook导出、独立参考答案和同数据不同任务均在矩阵分列。

## 三阶段具体处理

> 下表保留本次审计时的来源判定；当前已制作/正式写回与仍受阻项见文末“当前制作结果”，不再将旧 pending 判定直接当作今日待办。

|优先级|课程|产出位置/类型|需处理内容|
|---|---|---|---|
|P0|EF5560|当前brief/大纲来源|新brief明确Tencent Meeting/video link；更新当前行政来源，旧原件保留。|
|P0|IS5113|报告提交/截止/格式|当前作业书面要求PDF、12/1 23:59:59；实际已提交记录，附件版本与旧收件分列。|
|P1|IS5542|M10 + U12|71页逐页精读、原图/题目、课中定位和课后自测；复习框架补来源，状态不自动升级。|
|P1|EF5560|M12 + U14/U15|40页新讲义、p16/27/35 MCQ、p36–38任务；需要正式外部基金文件的部分先补来源。|
|P1|AC6761|数据卡 + OLS任务|data1=36103×8/FYEAR2012–2020，非提示所写2011–2020 Excel；解释stockprice~bmratio+roe+size和字段单位/来源限制。|
|P1|IS6400|本人测验复盘|距离截图1956/1214复核、Quiz3单位/条件、去趋势与ADF图题，原题缺项不补造。|
|P2|AC6761|AI Bias入口|最后课已讲完整机制，复用现有内容并补M11精确回链，不重复造案例。|
|P2|IS6400|ProjectTemplate使用表|4页模板的章节→CRISP-DM→现有证据映射，补项目导览，不新增教师未要求的页数/期限。|
|P2|EF5560|课堂prompt参考卡|两分享页当前Shared chat not found；保留链接来源，取得有效正文再逐轮分析，不编造历史。|
|P2|AC6761/EF5560|配套数据/视频|AuditFee/Access2、class03两表精确卡入口、DEBS13视频依赖，按矩阵定向处理；不把链接存在当已教。|

课前检查前置桥梁、字段/环境与任务入口；课中检查源页/Cell/原题/图的精确对应；课后检查官方对照、真实原作答、反馈与有理由的再测。不能因为期末降权就省掉课程学习，也不为每个文件机械新增一篇笔记。

## 检索与证据

[153文件矩阵](teacher-file-matrix.json) · [逐源/ZIP成员三阶段矩阵](source-processing-matrix.json) · [本人原交件复盘矩阵](post-submission-matrix.json) · [处理队列](processing-queue.json) · [归档清单](archive-manifest.json) · [范围](scope.json) · [统计](summary.json)。

两份课堂ChatGPT分享在实际侧栏截图中均显示Shared chat not found；未取得正文。Zoom辅导录像等外部视频只登记依赖，没有自动加入会议或虚称看完。学生原作答不是教师标准答案；课程题面、官方答案、本人理解与本次审计结论分别保留。

本批未重写59篇既有M/T正文，未替本人提交、撤回、重新评分或标记学会。独立检查只验本报告的身份、范围、分类和重点证据，不冒称全库存量教学/视觉重审。

既有练习索引另作定向核对：IS5113 P01–P05/79页题索引，IS5542 M01备注四问及M02 p45缺图。先确认索引与正文版本，避免把旧待办重复派成整篇重审。


## 当前制作结果 · 课程正式写回后

- [AC6761-T01](../../AC6761_Artificial_Intelligence_Accounting/notes/T01-股价OLS回归实操.md)：完整 OLS 实操、三份精确数据卡、M11 两处回链；数据/图/代码已核，字段字典/单位/时间限制保留。 [写回/gate证据](../../AC6761_Artificial_Intelligence_Accounting/_meta/material-completion-20261126/writeback-receipt.json)。
- [EF5560-M12](../../EF5560_Fintech_and_AI_in_Finance/notes/M12-智能投顾网络安全与监管科技.md)：40 页、13 原图、三道 MCQ 与财报/条款练习；class03 两表卡已补。p36–38 已核为假设 filing/issuer policy，无指定真实基金，不再以外部基金文件阻塞；转录/失效分享等限制保留。 [写回/gate证据](../../EF5560_Fintech_and_AI_in_Finance/_meta/material-completion-20261126/m12/writeback-receipt.json)。
- [IS5542-M10](../../IS5542_GenAI_in_Business/notes/M10-责任AI-公平解释与治理落地.md)：71 页、60 原图；B1/B2 定向关闭，U12 接入。视频全文、旧考试页现行性及 M07 原件仍有缺口。 [写回/gate证据](../../_meta/material-completion-20261126/is5542/m10/publication-result.json)。
- [IS6400-Quiz复盘](../../IS6400_Business_Data_Analytics/review/canvas-submissions-20261126/课后复盘-原作答与纠错.md)：三份历史 Quiz 原作答复盘、同源条件纠错及中英变式；完整 Canvas 题面/教师评分/原始数列缺口保留，不替换原附件。 [写回/gate证据](../../IS6400_Business_Data_Analytics/review/material-completion-review-20261126/publication-receipt.json)。
- [IS6400-ProjectTemplate导览](../../IS6400_Business_Data_Analytics/review/project-template-20261126/ProjectTemplate-逐页使用导览.md)：ProjectTemplate 实际 4 页与 CRISP-DM/现有证据映射已补，原页 3 图；只是模板使用导览，不表示 A06 正式报告已写完。 [写回/gate证据](../../IS6400_Business_Data_Analytics/review/material-completion-review-20261126/publication-receipt.json)。

逐项当前结果：[production-status.json](production-status.json)；保留原 processing-queue／teacher-file／source-processing 矩阵字节与历史判定。IS5113 旧索引只做来源对应/导航维护，见 [原维护证据](is5113-index-maintenance.json)，原检查器因无§2 不适用的 FAIL 保留。两份 ChatGPT 分享失效、IS5542 M07 与 M02 p45 源图、DEBS13/三段外部视频等缺口不记完成。


## 2026-11-27 M07 补源覆盖

原矩阵保留11/26审计时事实。M07现已另取得62页网页review版，逐页笔记与12演示/10输入已核，见[正式回执](../../IS5542_GenAI_in_Business/review/m07-web-review-20261127/publication-receipt.json)。课堂原始PPT与完整影片、录音缺首尾/接缝仍待补；“网页资料已取得”与“课堂原件全齐”分开记录。M10及EF M12讲义版此前已完成。
