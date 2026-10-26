# IS5542 M01 主代理审修记录

日期：2026-10-27。作者／合并者：主代理 /root（本聊天01a17880-c969-7903-8d68-5ede38386267）。模型实测证据见model-check.json；独审工具派遣显式gpt-6.1-sol、fork_turns none。任务只写本篇scratch，正式主写者仍为原全库重审聊天。

## 范围与候选

本次完整顺读、审修原稿§0–§9、折叠、自测、全部数学／代码式机制和图文；冻结首读candidate-stage1.md与最终candidate.md分开保存，不让独审追逐可变稿。baseline.md为真实原始字节，SHA 8bda44c851eddeb2deae3dc53c0d78bb12761a99d33f855dad581b20b6aa2708。candidate.diff是原稿到最终候选的真实差异；review-repair.diff是首读冻结稿到集中修复稿差异。

作者集中13组：高中起点与跨课依赖；p.1–12人员／四模块／日历；p.30整层与课堂覆盖；欺诈指标分母；并行／ITL／batch条件；矩阵／指数／对数／梯度前置；token身份条件；p.15/40/53/54/101完整英文任务；推理／人工／公平／神经符号边界；实课日期与转录完整性；CA内部权重影响门槛；AlexNet／Hinton来源；NIST有限测试。对应精确操作author-repair-operations.json。

独审共10组，第一阶段7组：B1真实制表符损坏乘号；B2批处理条件丢失；B3人工挂名复核；B4产品／模型层级；B5证据不足被写成否定或普遍因果；B6考试依据标签；B7概览图预算／EOS状态歧义。集中修复也纳入来源核查发现的目录原文口径、NIST三图差别、GPU/CPU最短桥梁以及N1–N3低成本澄清。review-repair-operations.json列完整精确变更；没有为建议重新全篇评分。来源阶段新增B8 Syllabus题型来源、B9 ASR／核音／平台与文本缺检边界、B10 p.71任务准确率／56%闭卷基线，已按实际来源修入；source-findings-repair-operations.json及diff记录33项，原审已实际定向关闭，不重开未变单元。

## 来源、计算及原题

完整来源矩阵和逐页范围在source-audit.md。117页含隐藏22/34/112、6页真实教学备注、无OLE、59媒体、Syllabus3页、转录全文均区分。官方目录本轮未取得PDF，历史2026-09-09记录明确保留为历史；date null、转录merged不升级原音完整或本人状态。外链视频未本轮观看，不编其内容。

source-checks.json人工回源登记10项，机器仅核字面／逐问中英锚点。完整英文原问及情境在正文，参考作答与讲义原答分开；行政项目要求和给定演示不冒充本人执行。

calculations.json本轮回算8组：1000交易的99.2%/0召回；CA40/20反例；整层乘加与ReLU；CNN四窗口与softmax；带遮罩注意力、多头、LN/FF及泄漏变式；三温度概率；bias更新损失；NIST7/8与9/10分母。没有重训真实模型、没有复现AlexNet赛事；修后10/10是给定教学假设。独审复做证据另覆盖约束上限、请求trace、RAG分数与公平对照。

## 机械疑点与链接

当前L=0、C.hard=0、R.hard=0、C.warn=0，10项源题契约通过。277项R.warn按19类列齐实际位置与判断，见warning-resolution.md；未增加豁免标记或改仓库检查器。旧G/E为FAIL，原值保留quality-current.json historical，不能称旧strict通过。机器不认证教学。

28个真实WikiLink目标／锚点核对0错。唯一初始误报是§9历史记录中的行内代码模板“标题原文”，自有scratch链接脚本跳过示范代码后通过；没有篡改历史回执消警告。

## 实际显示

同源浏览器1280×1050、KaTeX213公式、Mermaid10图：解析错误0、浏览器错误0、横向溢出0。主代理逐张看diagram-01至10，实际看course、p15、fraud、matrix-basics、cnn、residual、layer、matrix-actions、attention、ln、sampling、update、video、p101、govern等窗口中的关键受影响部分，另看CA、范数、预算边界、人工复核4张定向窗口。

原首读图与窗口保存在stage1-render/。图8是本批实质变更，实际看修后diagram-08.png，沿预算0／1、首EOS／非EOS及hat→EOS变式核状态；view-ca.png实看4乘号与40/20结果。其余图源码未变，按真实哈希承接首读时已实际观看；未声称原生Obsidian查看。来源修复后另实看view-context／asr-boundary／syllabus／cnn-steps／govern-steps，p.71表清楚区分横纵轴、56%无文档基线和中部约47%，没有把示意读数作真实重跑；CNN与NIST编号已恢复。browser-focused-report.json绑定最终源修版。

## 独立审查

已完成。真实独审者 /root/is5542_m01_independent，候选SHA e63754c35ca229a2c2ec5c227f464285df2b7e7530c51c2d1c6cf5f3eae9b171；52学习单元一次全篇首读，随后来源阶段及两批具体缺陷定向复核。B1–B10和M1/M2全部关闭；原stage-1、来源发现和两批关闭原文保留。证据reviewer/independent-review.md及targeted-recheck.md；未核材料限制仍紧邻正文保留。

独审第一阶段3925行／52单元，先候选、后规则／来源／diff；stage-1.md不覆盖。reviewer独立报告、来源阶段与定向复核是本次教学依据，不用本主报告代写审查者身份或结论。

## 写回、同步、安全与外部状态

本任务未写vault、共享完整性快照、README／台账、原件、Notion、Canvas、Git或配置。同步是否关闭由正式主写者在真正写回前再确认；本次没有agent修改vault，不能代用户声称手机同步已关。

publication-plan.json仅本篇精确共享镜像，逐目标精确操作（以publication-plan.json当前清单计数为准），逐项当前原始UTF-8基线、SHA、replace_exact或append及预期写后SHA；虚拟应用保留M05和其他篇新增，不改README全库计数，不向根规则追加逐篇进度。仅转录来源行做精确事实更正。作业总览无增量有理由；Notion提供正确数据库／行选择器、拟追加备注和个人保护字段，当前row_id／原值未读取，不捏造同步完成。主写者必须读当前行、去重追加并回读。

自有完整性verify见integrity-verify.json：正式M01、原PPTX、Syllabus、转录4项真实SHA均与开工相同，未发现快照文件丢失。全库自有快照观察到并发变动，不能写“全库未变”；逐项清单保留，非本聊天执行的写入。共享目标正式应用前必须重新CAS，漂移停止对应目标重基，不覆盖其他会话。

正式写回、逐目标同步／Notion回读与Git提交／推送均未执行，全部留主写者；本候选就绪不代表这些状态已完成，也不代表本人通读／自测／提交。
