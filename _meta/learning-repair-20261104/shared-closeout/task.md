# 本批单一共享收尾任务

你是已完成 EF5560 的原会话，现由统筹明确指定为本批唯一共享文件写入者；不重开 EF5560 或其他课程的教学审查，不改教学正文。

## 已核实前提

五课真实结果已收回，核心原路径共48个：AC6761 10、EF5560 8、IS5113 7、IS6400 17、IS5542 6。IS5542 M07只是录音导航维护，缺讲义/演示；不要把48写成全部材料完整或全部达到逐页课件验收。IS6400有3篇原生显示实测，其余14篇及IS5542剩余显示按本批用户明确选择跳过，使用waived_by_user，不冒充实际通过。来源与教学已审证据按各课真实回执；旧回执不改。

用户已明确不再逐篇检查后续界面，不操作GUI、不重新索取前台，不开启新的全篇审查。只做共享信息与文件完整性收尾。不提交、推送、上传或改Git索引，不改个人学习/提交/评分状态，不修改原件。

## 只读输入

- 本批五个课程子目录的 course-result.md/json、inventory、shared-updates.md/json 和对应写回/同步证据。
- monitor 下已核收回执：ef5560-result-accepted、is5113-result-accepted、ac6761-result-accepted、is5542-writeback-accepted、is6400-final-result-accepted；以真实当前文件为准。
- decisions/user-skip-remaining-display.json 和用户豁免说明；不要把源材料缺口一并豁免。
- 自有开批全库基线：E:/app-data/codex/scratchpad/learning-repair-orchestration-20261104/integrity-before.json（608份Markdown）。这个基线保留开批状态，后续不要覆盖。各课自己的当前核验范围和本批新增规则、报告亦作为变动归属证据。

## 允许写入

只写根 README.md、_meta/术语总表.md、_meta/转录处理规则.md 内本批确有增量的对应位置，以及本目录 shared-closeout/ 中的交接、差异与验证报告。必要的批次 README 当前状态可写，但 threads.json/task_plan/progress 和其他课程状态由统筹维护。

根 README 当前库存/各课入口/待办/当前状态准确反映已写回事实，不把旧日期历史统计改写；加入本批正式入口与真实限制。术语只从已审课程定义精准合并，冲突给具体依据；不引入未经审查的新教学解释。转录只合并确有证据的范围/来源边界修正，不改原始转录，不把本次无新录音写成新增融合。

Notion：EF5560 8条、IS5113 7条、IS6400 9条已有逐字段回读。AC6761 10条和IS5542 6条拟追加备注因连接器无法可靠保留原富文本而未写，精确清单已在各课目录。此任务不代写这些受限字段，不换渠道绕过；明确16条未同步。原值及个人字段保持。

## 执行顺序

1. 再核五课确已停止正文写入，读最新 course-result，冻结允许写的共享文件原始字节/哈希到 E:/app-data/codex/scratchpad/learning-repair-shared-closeout-20261104/。已有并发差异先合并，不覆盖。
2. 合并真实已发布增量。只修共享入口的实际悬空链接/当前状态矛盾；不扩大为全库润色，不动历史候选和冻结审查来清警告。
3. 按CAS和safe_write.atomic_write写入并精确回读。
4. 一次完成全库 link_check.py、readme_check.py 和自有全库基线完整性核对。可import integrity_check并把files()结果一次缓存后复用，避免其重复枚举所有目录；MANIFEST指向自有基线，不覆盖共享快照。核对本批/其他任务/历史问题的归属。若缺陷涉及课程正文或超出允许范围，给精确位置交统筹，不越权修。
5. 交付 shared-closeout/README.md 和 result.json：本批正式核心入口数量、配套范围（按实际路径去重）、共享写回文件与前后哈希、检查结果及全部剩余问题、Notion未同步16条、来源缺口和用户UI豁免。明确没有Git提交/推送。

这个任务完成后停止。报告用“本地收尾完成，外部/来源限制保留”等准确口径，不能写“全库全部通过”。不追加用户已经要求免除的界面检查。
