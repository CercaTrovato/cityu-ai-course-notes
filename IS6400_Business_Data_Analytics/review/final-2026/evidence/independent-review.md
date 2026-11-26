# IS6400 期末复习框架：独立轻量抽检

日期：2026-11-23。作者/主写者：`/root`；独立审查者：`/root/framework_review`。审查者未参与候选撰写，未修改正式库或 assignment。本报告为同一次先候选、后来源抽检的第二阶段；不重审全课，也不证明本人已学会。

## 阅读条件与候选绑定

第一阶段只主动打开 framework.md，保存了 stage-1.md 原文。平台上下文已自动带入用户根级 AGENTS.md、全局规则和历史摘要，因此不是完全盲审；第一阶段报告中的“未读规则”指没有主动打开规则文件，不能理解为没有被注入规则。没有读取作者通过结论、机器分数或旧独审报告。

第二阶段实际读取《笔记制作与融合验收流程》§2.1–§3、课程 AGENTS.md，并按派单核以下样本来源与数据结构。规则文件一次读取输出还显示了相邻段落，实际审查依据限定上述章节。正式目标尚未写回、原先不存在，无基线正文或 diff 可审。

- 第一阶段 framework.md SHA-256：`eadbbc8d159644f3386a04d3e783da34a05780d727eb1e1fbd79a51bffb1f53c`。
- 最终抽检 framework.md SHA-256：`002c04b1e2597798437cc6a4ef0d7db960bf5355742bfa0c93a4f682c4a1b87d`。
- sources.json SHA-256：`830d30aea2dbaf6872ef0ad57954aaf087c3d328e47c4ddb46ddd96771867521`。
- progress.json SHA-256：`a0ace4780f8b45fab19d91e60de2c1425a0c0f3aeb82f8a1887ec744ebafca69`。

审查期间主写者通知末段维护变化：补 LibraryFind 未登录实际结果、小红书登录提示及来源直链，sources.json 补 search_log。我实际回读最终候选末段并核上述最终哈希。这些是来源限制和入口的维护说明，未改变本次抽检的考试范围、U 单元或诊断含义，承接第一阶段观察；未将主写者的浏览观察冒称审查者再次联网实做。

## 实际样本、选择理由与来源支持

### 1. 考试范围和学习范围的分离

选择理由：错误地按 M/T 或文件名 L11 认周次，会直接使读者漏复习模型评估或把深度学习当考试重点。

实际读取 S32 `M10-T11-transcript-source32-partial.txt` 的 43:49–45:24 与 01:25:56–01:32:20。01:26:11 原文为“from week 1 to week 11 excluding week 10”；01:30:32 指明 week 10 deep learning 可忽略；01:30:49 转到 week 11；01:32:13–20 再说明 model assessment 与有效评价框架。它支持候选的“考试主线排除 Week 10 深度学习、保留 Week 11 模型评估”，不支持把深度学习从完整课程学习中删掉，候选也未这样做。

核本地 M09/M10/T10/T11 的文件标题和头部元数据：M09/T10 为深度学习/序列预测，M10/T11 为模型评估/模型选择；sources.json 也将 S-ASSESS 指向 `canvas-20261118/L11-IS6400-Model Assessment.pdf`，而 S-DL98 指向 `L11-IS6400-DeepLearning.pdf`，足以说明 L11 文件名本身不能判考试范围。该映射核对不等于逐页重审这四份笔记或全部讲义。

43:54 仅有 one page / single page 的 ASR 陈述，45:07–20 有13题口头表述且带与往年比较。候选不据此确定单面/双面、手写/打印、计算器和最终卷面，处理恰当。本次只核文本，未回听原音，未取得最新 Canvas 正式通知；S32 的 verified 应结合 partial ASR/未回听限制理解。

### 2. 样卷题型到路线与现有解析的导航

选择理由：树的实例数/行数、时间序列验证的“下一天”目标都是有限样卷中容易误读的条件，并能兼顾概念、计算和评价设计。

第一阶段走过两条导航：Problem 3(2) → U05/U06/U09；Q5(3) → U07/U08/U09/U11。第二阶段读取 sample-final-full.txt 全文，并只读原 DOCX 的 XML 对照 Problem 3(1)(2)(4) 与 Q5(3) 原段落。原 DOCX 确实要求用验证表求误差、每叶 penalty=1、最多8层设置；Q5(3) 确实要求 next-day 滚动评价、验证数据、指标/计算与模型比较，明确无需编程。候选映射没有把 Q5(3) 误作必须写代码，也未把题面 penalty 改成课件常用的0.5。

实际打开 image1.png/image2.png/image3.png：图中 A/B/C/D 分支、正负叶、level1–5 标记清晰；两张表各6行，分别有15个实例，而非6个实例。逐图 SHA 与 DOCX `word/media/` 对应文件相同。原图自带 Exercise/Problem2 与 Test set 等旧标签，正文以 DOCX 当前 Problem 3 和 validation 题意定位是合理的；框架没有靠图中旧题号重新编造问题。

正式目标目录计算出的 `../../assignment/practice/sample-final/notes/学习解析.md` 存在；实际检查标题，§2.2 是树题且有验证误差小节，§2.3 是 Bitcoin 与滚动预测、§2.3.3 是逐日比较。候选当前只有相对文件入口、再提示按 §2.1–§2.3 查找，路径可以实际定位。本次没有对整份学习解析教学或答案正确性重新验收。

### 3. D4/D5 与学习状态、必要结构

保留 stage-1.md 对 D4/D5 的判断：D4 定位正类/评价分母/不平衡，D5 定位时间顺序和泛化；只是诊断起点，不是整单元掌握认证。D5 开放排查可有多种合理顺序，候选未规定唯一答案。

实际解析 sources.json/progress.json：schema_version 均为1；progress 包含 course、updated_at、framework_status、units、sessions、mistakes、next_step。12个单元都有 id/title/source_ids/prerequisite_ids/question_types/status，引用来源与先修 id 未发现悬空；所有 status 为 not_started、mastery 为 unknown，sessions/mistakes 为空，last_learning_position 为 null，next_step 等待本人尝试。没有因为制作框架而写入本人答题或掌握。来源包含年份/学期、类别、路径/URL和状态、读取范围与限制；已读本地样卷另设 latest_canvas_verified=false、official_solution=false，未把本地旧下载冒称本轮 Canvas 新核。

## 结论、阻断与建议

结论仅覆盖上述独立样本及必要结构：未发现会导致本阶段路线任务做不完、选错考试范围或误记本人掌握的阻断项。可按现有框架进入后续用户选择/起点诊断；正式来源条件待核项应继续保留，不能因此称考试信息全部确认或整课独审完成。

无须为本次抽检新增教学正文。非阻断建议承接第一阶段：U 编号做成本页锚点可减少长页面查找；D5 施测时接受有依据的不同排查顺序。这两项不要求延迟交付。

## 未抽与未核

- 未逐页核全部理论讲义、全部 cell、完整概念覆盖与计算；未重跑 notebook，未审全份已有样卷解析。
- 未回听 S32；未确认它是最后完整复习课或完整首尾，也未认证课堂日期。
- 未再次访问 Canvas、LibraryFind、小红书、Studocu、BIS 或其他站点；无法独立认证主写者新补的联网观察、第三方试卷真实性或全部外部搜索范围。最新 Canvas、校方历年卷及官方答案仍待取得。
- 未核考试日期/地点新状态、辅助纸细则、最终题量权重；保留候选所标历史基线与待核状态。
- 未验证真实用户理解、诊断耗时、授课成效或最终模拟卷。
- 未操作正式库、共享看板、跨会话发送或 Git。stage-1.md 原文保留，审查者写入只限本 scratch 下报告及核对脚本。

## 正式写入前：来源清单元数据追加核对

2026-11-23 定向回读 sources.json 新增的 S-DIAG 及 updated_at（`2026-11-23T18:07:15+08:00`）。S-DIAG 将 D1–D6 明确列为“自编”，path 指向本框架，sha256 为 `002c04b1e2597798437cc6a4ef0d7db960bf5355742bfa0c93a4f682c4a1b87d`，与此前抽检的框架一致；readable_scope/limitations 保留“未给答案、未施测、无官方分值、不代表教师原题或独立掌握检测”。其中 verified 指自编来源已登记可读，不代表学生已通过诊断。此项仅补来源元数据，不改变路线、诊断内容或上述样本结论，无新增阻断。最终 sources.json SHA-256 为 `4c5ad54e87b58793673f91cea6464f8d3d69af63a8e71106dfc4c1d79b8a0af3`；前文旧哈希保留作实际审查历史。本次未重新读取教学正文或扩大审查范围，未写正式库。
