# IS5113 全库学习笔记检查与修补任务

你是本课程实际执行者，不是只做建议的顾问。用户已授权你完整检查并修补本课程学习笔记；主会话负责规则／决策／派单／监督，不亲自修正文。使用 `gpt-6.1-sol`、`high`，独审同样显式设置此模型与强度，不可换模型。

工作目录：`D:/上课资料/CityU`。课程：`IS5113_AI_Ethics_and_Regulations`。核心笔记 7 篇，见本目录 inventory.json；还须清点实际学习解析／导览，纳入或排除有据。第一篇：`IS5113_AI_Ethics_and_Regulations/notes/M01-导论-AI与伦理.md`。不要停在清单或首篇；逐篇闭环推进本课全部范围，真阻塞分列并推进其他可做篇目。

## 必读与恢复

先读根及本课 AGENTS、`_meta/全库笔记检查与精准修补工作流.md`、`_meta/逐页学习与课件图示规范.md`、可读性总规则／本课细则、机制标准、模板、制作流程；涉及原题、练习、图、转录按对应规则。规则真实版本见批次 rule-manifest.json。恢复只读本 task、status、当前缺陷／候选／报告，不重开已完成流程。

## 所有权

允许写：本课程内学习笔记、对应图资产、配套学习解释和课程元文件；`_meta/learning-repair-20261104/is5113/` 下本课证据。课程规则只读，正式作业稿／原件只读。其他课程及根共享文件禁止写，根 README／总术语／转录登记的增量写本目录 shared-updates。主会话之后指定单一共享收尾者。

临时目录：`E:/app-data/codex/scratchpad/learning-repair-is5113-20261104/`。最终必要的页清单、原图来源、独审、gate 和写回记录在本目录各篇 ASCII 子目录保存；正文引用的图资产放课程 notes/figures，不指向 scratch。不要改他课或旧审查副本。

本聊天用户已明确确认电脑和手机自动同步均关闭，本批继续有效，不重复问。保留当前未提交改动；每次写前校验真实基线与原子写，出现冲突停该项。禁止提交／推送、自动同步、外部作业提交、修改原始课件、代填个人已学会／已提交。浏览器需要时先检查 iab，优先连接器。

## 隔离完整性

不要运行会覆盖全局清单的默认 snapshot。首先在任务 scratch 建课程独立基线；续接已有基线用 verify，不能覆盖它：

```powershell
New-Item -ItemType Directory -Force -Path 'E:/app-data/codex/scratchpad/learning-repair-is5113-20261104' | Out-Null
& 'D:/anaconda3/python.exe' -X utf8 _meta/tools/course_integrity.py snapshot --course 'IS5113_AI_Ethics_and_Regulations' --manifest 'E:/app-data/codex/scratchpad/learning-repair-is5113-20261104/integrity-baseline.json'
& 'D:/anaconda3/python.exe' -X utf8 _meta/tools/course_integrity.py verify --course 'IS5113_AI_Ethics_and_Regulations' --manifest 'E:/app-data/codex/scratchpad/learning-repair-is5113-20261104/integrity-baseline.json' --report 'E:/app-data/codex/scratchpad/learning-repair-is5113-20261104/integrity-final.json'
```

初始 snapshot 若发现既存结尾／编码异常，记录并停该文件，不凭记忆重建；其余可独立推进。该快照不含原件字节恢复，实际拟改正文还要保留完整原始字节和 SHA。明显缩短必须有真实重构依据与逐项保留证据，再精确 --allow 该文件，不能普遍豁免。

## 执行与收敛

按工作流：一次全范围诊断及源页视觉→一张缺陷清单→按问题精准修补或连续单元重构→冻结候选→一位未参与写作的独审先候选、stage-1 落盘后再来源→批量修复与原审定向复核→机械／真实视觉／CAS 写回→本课台账／Notion 同步。不得以既有 PASS 或有 Mermaid 块判完整。

每个内容页有本页实质解释和定位；教学原图入正文并讲清；必要机制图另判断；预习／课中／复习分别验收。完整原题、英文答案、条件、原例及转录不能在重构中丢失。保留正确内容，避免从零重写。

同一缺陷两次定向修补不收敛，或反复出现系统性新缺陷，落盘两种方案交统筹判断；不无限重审，也不把未解问题标通过。写 status 的 decision_needed 和具体问题即可，主会话会读回；无需向其他聊天发消息。模型／工具限制如实记录，不伪造独审。

## 状态与交付

每阶段／每篇完成及阻塞时更新本目录 status.json，长任务约 10 分钟写真实断点；若能从上下文取得自己的 thread_id 则填，不猜 ID。进度用页清单、候选、缺陷关闭、gate 或写回等实际产物证明，不能只刷新时间。需要统筹决策也继续其他不依赖项。

每篇完成后保存真实审查证据并推进下一篇，不因本次回复长度止于首篇。全部本课范围做完时产出 course-result.md/json 和共享增量清单，阶段标 course_done_awaiting_shared；有外部实质阻塞标 blocked_with_partial_results，列已完成／未完成，不称全课完成。保护本人学习字段。
