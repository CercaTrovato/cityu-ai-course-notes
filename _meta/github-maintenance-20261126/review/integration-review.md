# 整合候选独立轻量抽检

结论：需定向修复后再发布。当前清单 137 项；未写 vault、未做 Git 或浏览器操作。

73 个单元全部未开始／掌握未知，学习会话和证据全空；新首页与五课当前主导航可解析。首页没有夸大提交／掌握，A07 回执与六次反思状态正确。

## I01 · IS5113 当前管理口径仍催本人 Q&A

当前顶层/管理快照仍说本人只准备 Q&A，与本人不登台、无 Q&A、展示完成和 E 段已交统筹冲突。历史 decisions/history 保留原话即可。

仅更新当前字段和相应来源绑定，写展示已完成、报告正式回执待核；旧问答仅历史材料。

路径：`IS5113_AI_Ethics_and_Regulations/assignment/graded/A02-group-project/coordination.json`、`IS5113_AI_Ethics_and_Regulations/assignment/graded/A02-group-project/thinking.json`、`IS5113_AI_Ethics_and_Regulations/assignment/graded/A02-group-project/timeline.json`

字段：`coordination.summary`、`thinking.management.current / decision（底部管理快照）`、`timeline.items[id=handoff].next_action`

## I02 · IS5542 A01 下一步仍有已关闭的第 6 次反思提交待办

summary 已正确写六篇均交，但下一步仍写第6次由专属会话推进。

关闭反思提交待办，保留 gaga 录制、本人终检提交及官方互评后置；不重交。

路径：`IS5542_GenAI_in_Business/assignment/graded/A01-genai-project/assignment.json`、`IS5542_GenAI_in_Business/assignment/graded/A01-genai-project/thinking.json`

字段：`assignment.next_action.title / owner`、`thinking.decision`

## I03 · 其他课程时间线当前字段仍有已结束的展示/录制要求

AC 仍先核11/18实际展示，EF merge 仍称最终PDF/录像待证据并要求再录制，IS6400 my-delivery 仍称准备11/25展示。上方当前摘要和新证据分别已确认展示完成或录像收到。

当前待办转为反馈、最终核阅/提交或报告分工；完成的讲稿/提词制作项标历史资料保留。保留原history和未知实际排练状态，不把材料制作倒推掌握。

路径：`AC6761_Artificial_Intelligence_Accounting/assignment/graded/A01-ai-accounting-project/timeline.json`、`EF5560_Fintech_and_AI_in_Finance/assignment/graded/A02-fintech-company-case/timeline.json`、`IS6400_Business_Data_Analytics/assignment/graded/A06-group-project/timeline.json`

字段：`AC items[id=personal].next_action`、`EF items[id=merge].summary / next_action`、`IS6400 items[id=my-delivery].title / target / state_basis`、`IS6400 date-slides/mobile-presenter/manager-script 的当前 next_action`

## I04 · 公开候选中仍有第三方组员实名与角色对应

这些本地文件出现技术组员实名；任务说明把含组员姓名的会议原件列为不公开。本批未包含含学号 v5 原件，但只排除二进制仍不能保护元数据内的身份对应。

公开发布副本按已知角色替换第三方姓名（包括history）；本地原件和原SHA保留，记录公开副本映射。不需要删除有用项目事实或用户本人姓名。

路径：`IS5542_GenAI_in_Business/assignment/graded/A01-genai-project/assignment.json`、`IS5542_GenAI_in_Business/assignment/graded/A01-genai-project/thinking.json`、`IS5542_GenAI_in_Business/assignment/graded/A01-genai-project/timeline.json`

字段：`assignment.my_role`、`thinking.nodes[].owner`、`timeline 当前 owner 及 history 内姓名`

## I05 · IS5113 历史复习入口将指向公开树不存在的问答文件

目标本地存在，但不在 origin/main 或当前发布名单；相对 Markdown 链接将404。

若确需公开该历史资料，先核隐私后精确加入；否则移除超链接并说明仅本地历史材料。不要因此重开当前Q&A待办。

路径：`IS5113_AI_Ethics_and_Regulations/review/README.md`

字段：`A02-E-English-QA.md 链接`

## 样本和限制

本次读首页、五课当前入口、24份assignment摘要/提交/下一步、5份timeline、5份thinking、4份coordination的当前及隐私高风险字段，未逐字重审全部历史，更未重审教学正文。全部候选文本做凭据和编号模式扫描，未命中明显凭据/第三方学号；IS5542实名对应需生成公开副本。

ZIP只含7个框架/独审文本；v5含学号原件、members.json、全组报告和录像不在候选。原生页面显示、最终发布树、Git和看板均未核。维护README引用的3份收尾JSON仍待实际生成纳入；不能将本报告视为其放行。

精确绑定、逐项字段、机器结果和未抽范围见 `integration-review.json`。修复后只需定向复核，不重开全篇教学审查。
