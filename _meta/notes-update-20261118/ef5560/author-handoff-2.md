# EF5560 第二断点（作者证据，不给独审第一阶段）

M10 按原一次两阶段独审12项一次批修，冻结 SHA a46ee187143f6f155d496d29e0ea0d4e1e2c0c285bf13d3059d70842a8ccdae0。旧候选保存在scratch/M10-frozen-v1.md；精确差异 v1-to-v2.diff，定向ID清单 directed-fixes.json。原审为/root/ef5560_m10_review，尚未恢复定向复核，必须只核这些缺陷及依赖，不再重开54页。root实际UI受限，没有绕过或豁免，最终显示pending。预览ef5560-m10-v2已生成供root日后查details/金额/可见标签，生成不是实际核验。

M11 完整候选SHA 1ad3390aa655ef3ba82e95b4fbec1e776f00231ce34fa293327f87ef5beb62b9，78696字节。源54/54作者已实际看完（前次断点），17整页教学原图，18原文情境/题目块，4页MCQ共16选项，3问简答p38和2问p52完整；所有答案标自拟/来源地位。内容按同一54页顺序、有54锚点和逐页映射；五题details自测。current机械预检L/C.hard/R硬项0，C.warn/R.warn需真实主核对而不以分数放行；question-evidence/calculations/source-assets/page-evidence已持久化。作者自查把宽英文原表改为保真Markdown表，未改条件/数值；原题和给定步骤在details markdown=1，最终UI未看，不能称全图显示通过。

M11需一位未参与作者的新gpt-6.1-sol/high做一次两阶段独审，第一阶段只给候选、scratch/figures/m11和必要教学依赖(M03/M05/M08/M10候选，M10本身仍待定向核)，不要给本文件、机器分数或来源证据；落盘stage1后再给全部源PDF54页/对应渲染、根与本课规则及原稿不存在基线、source-assets/page-evidence/原题计算记录。作者未调用新代理，root负责排槽。

M11预览 http://127.0.0.1:8796/ef5560-m11/已生成，有17原图和12数学节点，未实际浏览。当前IAB限制由root处理，我未开其他浏览器。

A/B各14页仅抽文和渲染，尚未实际查看或写解析。下次继续，权威解析写assignment/practice，review/README只给入口。原件已归档4文件到course_files_export/canvas-20261118；旧原件未改。9篇旧核心与18TXT库存保护，未改任一现有教学正文/元文件/个人状态；根Git统一收尾，我未暂存/提交/拉取。Notion还未更新，不预填笔记生成。未新建metadata重复来源或重审M09/syllabus。

注意build_m10.py若重跑，会覆盖其fix_m10.py后处理的details和货币归一；当前冻结候选为唯一准稿，不盲重跑旧构建。fix_m10.py已执行一次，断言旧SHA阻止误重跑。M11生成脚本build_m11.py读取m11-content.json、m11-original-tables.json，当前可复现；不要再执行一次性selfcheck-fix脚本。正式发布前回CAS、新文件仍不存在，所有v2 gate和课程/Notion/共享同步仍待办。
