# AC6761 期末复习框架：同一次独立抽检第二阶段

## 版本、身份与阅读条件

- 日期：2026-11-23。
- 作者／主代理：/root；独立审查者：/root/ac6761_framework_review，未参与候选撰写。
- 候选：framework.md，SHA-256 为 87bdbb50367bd8c00430782a35e3218799cd045f1dc7c04a46e848ac0a07dbb4；第二阶段结束前已确认未变。
- stage-1.md SHA-256：7d0cf53a16c4126412cfe6be3c8d0f47ca99c67132098251cb0626aff8e10ada，保留原文件未覆盖。
- sources.json SHA-256：4cbb0c8f2c8959c166aa098d13d7bc0d89eda2e50c1d1c8ece220279377f9e81。
- progress.json SHA-256：94408aa59fc4da15712c437adf262abe6459cd2c4e6936588377765a621cd61f。
- 第一阶段先读候选全文并自行选样，随后主代理明确允许第二阶段，才主动查规则文件、来源和状态 JSON。会话环境已自动带入用户粘贴的根规则及任务背景，故不称完全盲审；第一阶段“未读规则正文”应理解为未主动打开规则文件，不代表隔离了平台注入的全部规则。
- 第二阶段读根／课程 AGENTS.md，并重点核《笔记制作与融合验收流程》§2.1、§3.2–3.4。本次是路线框架抽检，不按完整 M 笔记要求补写演算、图或授课。

## 结论与待处理项

本次样本未发现阻断路线使用的教学／来源误导，也未发现来源已核或框架完成被换算成本人已学会。可将独立轻量抽检记为完成；只覆盖下列样本，不是全课独审通过，最终复习课／参考卷等线上缺口继续 pending。

F1 的题型速查入口确实可补；但核规则后应明确为非阻塞建议：U12、U13 本身已写学习动作、难点和可定位来源，速查表并非唯一导航。第一阶段“建议冻结前处理”不应被扩成必须新增教学或重审全课的门槛。F2、F3 仍为非阻塞建议。若主代理实际修改含义，由原审查者仅复核这些变化及受影响定位。

## 样本 A：比率、杜邦与 Z-score 的入口和页码

选择理由：这是第一阶段 F1，读者可能从“试题要求算什么”反查单元。

实际动作：从 U12／U13 与题型表定位到 Week 10 主讲义及 Ratio 补充讲义，读提取全文，再直接读取原始 PPTX 的 slide XML 核物理页码与正文；原文件哈希均与 sources.json 相符。

- Week 10 PPT.pptx p.3 为 Ratio 定义，p.4 明列流动性／盈利／偿债／效率／市场指标及公式，p.5 为对应 AI 提问；p.16 已是趋势提问。U12 的 p.3–16 范围能覆盖比率与趋势。
- p.17 为 DuPont 的三项乘积分解，p.18–19 为分解、比较与解释问题。U13 的 p.17–42 包含这些内容。
- p.33 为 Altman Z-score 公式与分区，p.34 为五变量定义，p.35 为计算和解释提问。U13 来源确有模型计算，不是仅按标题推断。
- Ratio 补充讲义共 16 页；抽核 p.1、2、7、16，p.7 明确把 ROE 接到 DuPont。补充讲义为 U12 辅助来源的安排合理。

初读观察承接：题型速查表没有单列 ratio、DuPont、Z-score 触发词，仍是可改善的检索点。最小修复为两行：比率计算 → 口径／分子分母／期间 → U12；DuPont／Altman Z-score → 指定版本／变量／单位／边界 → U13，并给 p.17–19、33–35 精确入口即可。

核源后额外确认：p.17 混用 Average Total Assets 与 Total Assets／Shareholders' Equity，框架已提醒分母一致，没有默把课件写法当无条件恒等式；框架也明确 Z-score 不是破产概率。未要求在路线页展开公式纠错或适用行业推导，后续单元仍须负责。

限制：本样本是文本与物理页定位核验，未独立观看 PPT 全部图像，也未核所有公式图像或运行 Excel。

## 样本 B：考试事实和口头线索的条件

选择理由：范围与题型误读会直接影响复习取舍。

实际核原始 AC6761 Outline 2627.docx 的 document.xml，含表格的 w:p 顺序定位；文件哈希与 sources 相符：

- 段落 36／39 为 English；214 为 Examination: 50%、3 hours、Closed book。
- 217 确写答全部 essay and case questions；225 为 No，对应本表 GenAI 列。
- 232 写 coursework 与 examination 两部分通过的要求；所抽区段未给具体数字及格线。
- 框架没有把这些文字扩成“必无选择题”、固定题数或确定权重，也没有把期中模板沿用到期末。

回读三份转录原件的指定时间与邻近语境，并核哈希匹配：

- M01 01:53:06 明确是 if we are testing such transaction analysis；01:53:20／37 接三栏与逐笔交易后数值。框架称“条件式答题格式线索”，保留了 if，不是宣称必考。
- source19 12:29–12:40 明说 final examination is paper-based；附近 Microsoft Express、FIDO 是 ASR 错词。框架保留未核音限制，仅降低菜单记忆优先级，未据此删除纸笔查询或 REA，处置合理。
- source28 01:00:05–01:00:54 的“if in the examination”与后文 prompt／stakeholders' interest 可定位。框架称早期课堂例示，不称最终复习范围；首句 product 的纠正有后文支持，仍未回听原音。

考试安排快照的 AC6761 条目确为 2026-12-12 09:30–12:30、YEUNG LT13，文件哈希匹配。快照自身声明是用户提供计划的保存证据，原监督未重开 AIMS；框架和 progress 都注明日期与本轮未实时复核，不存在冒称本轮 AIMS 核验。

不据本次抽检认定：最后复习课是否已发生、教师是否已发布 mock、Canvas 最新考试公告、计算器／字典／公式表规则、今年完整考试范围。

## 样本 C：sources／progress 的核验状态与本人学习状态

选择理由：用户要求保留真实问答与掌握层次，框架完成不能产生学习成绩。

实际读取两个 JSON 并逐单元检查：

- sources 有 61 个来源，verification_semantics 明确 verified 只表示所列本轮范围，不代表线上最新版、完整教学验收或本人学会。抽核的主讲义、补充、Outline、转录、快照均有范围限制；7 份实际核哈希均匹配。
- 最后复习课课件、录音／转录、考试公告、mock、官方答案五项保持 pending；未取得材料没有被标成已发布／已完成读取。
- s-self-diagnostic-plan 为 verified，但 kind 为 self_authored_plan，scope 清楚写“仅任务规格；无完整题面、答案、施测或作答记录”。因此不等于诊断已制作完毕或本人已答题。s-self-mock-plan 为 pending；holdout 为 planned_not_generated，questions 为空。
- progress 的 framework_status 为 draft_pending_independent_review；17/17 单元均 status=not_started、mastery_level=unknown、learning_evidence=[]；sessions 和 mistakes 均为空。
- next_step 为 diagnostic_proposed_not_started，requires_user_response=true；掌握政策区分 explanation_seen、solved_with_hints、solved_independently、retest_passed，并要求真实作答证据。
- 全部单元 source_ids 可在 sources 中找到，无悬空来源 ID。本项只核引用存在，不等于核尽 61 个来源内容。
- exam 保留 source_observed_at=2026-11-05、rechecked_live_this_round=false；final_scope／question_count／marks_by_type／calculator_rule／formula_sheet_rule 为 null。未把早期线索填为最终考试条件。

F2 承接：D6 的 prompt／证据探针不能代表 U11–U16 全能力，候选目前仅把它当起点设计，没有据此跳课或升级状态；建议后续为方法计算和预测流程另做微型入门判断。
F3 承接：U15 可写清代入、差值与平方误差的小桥接，属非阻塞预期管理建议。

## 未抽范围、阻塞与收敛边界

- 实际读取阻塞：无。浏览器与外部来源访问没有由本审查者重试；sources 中原作者的访问失败记录仅检查其表述边界，不独立认证工具过程。
- 未独立抽核：其余 Week 1–11 源页、Case／Quiz 全部题干及答案、Excel 全表、数据库执行、课程目录新版本、全课视觉样本清单、历年卷／小红书实际检索过程。
- 不要求为这些未抽范围新增全课独审；完整制作范围来源核对仍由主代理负责。本次报告没有认证本人练习、掌握或正式提交。
- 本次只写 independent-review.md，不改候选、stage-1、vault、其他成果或学习状态。


## 最终候选的定向复核（2026-11-23）

本节追加保留前两阶段记录，只复核 framework-final.diff 所列变化及受影响链接／状态；没有重审全文来源。

版本绑定：

- 原审候选 framework-reviewed-v0.md 实测 SHA-256 仍为 87bdbb50367bd8c00430782a35e3218799cd045f1dc7c04a46e848ac0a07dbb4。
- 最终 framework.md SHA-256：31e6707f8232188b8b197bc3852e58e53308f2728d0acad22502ee8aaadefeb4。
- 最终 sources.json SHA-256：5fb3e3498fad57ea8817a68b914f85f472dcc032af02fa30b7cd95849b95763d。
- 最终 progress.json SHA-256：7ffbbba535093a8819ebe37ce328b9bda9b7b719a09d2159c1145da262295dbf。

实际变化与结果：

1. F1 已处置：题型表新增 ratio／liquidity／profitability／turnover → U12，以及 DuPont／ROE decomposition／Altman Z-score → U13 两行；步骤含口径、期间、平均余额和模型版本。p.3–16、17–19、33–35 的入口与前阶段核源证据一致。
2. F2 已处置：D6 主要定位 U14 的角色关切与证据意识，另记英文表达；新增 U11、U13、U15 各单元前微型判断，不以 D6 跳过整段内容。仍只表示诊断规格，没有新增虚构题面／成绩。
3. F3 已处置：U15 明写少量数字的公式代入、实际与预测差值、平方误差求和，然后读训练／测试；平均数、百分比与语法依实际卡点补。符合框架层面的桥接规格。
4. U08 新增 linkage 的用途，定向回原 Week 5 PPT 的 p.35 核到 Resource-Resource／Linkage（link two resources），p.36 注 Linkage not shown。新增列表项有课件依据，不形成与原图冲突的结构断言。
5. 新增 10 个中文笔记双链：10/10 路径存在，且各文件当前哈希与 sources 所记匹配；链接带完整课程目录。可读材料名没有替换或新增未知 source ID，框架中的 source token 均能解析。笔记仍被定位为查讲解入口，教师原件的事实来源地位保留。
6. framework 与 progress 的框架状态均为 ready_with_source_gaps；framework learning_status 仍为 not_started。17/17 单元仍 not_started／unknown、learning_evidence=[]，sessions／mistakes 仍为空。状态变化只表示路线可用，未扩成学习／授课／最终考试条件完成。
7. sources 仍 61 项。Transaction 附件的 79 个非空段落计数，经原 DOCX XML 定向计数相符，字节哈希匹配；“已回读”是作者本轮动作记录，本审查不冒称代理自己见证作者阅读。Outline 等 locator 改为 nonempty_paragraph_count，并明示空段落仍计定位索引，消除了计数与段落号的混淆。
8. sources 追加 2025-2026／2024-2025／2023-2024 + Semester A 三条官方库检索日志，均写空结果不证明无卷；没有将未取得来源升级为确定存在／不存在。此处只核新增记录的语义与状态，本审查未重新执行这些在线检索。

最终结论：本次修改及受影响导航／状态定向复核无阻塞，F1–F3 的建议已按实际变化关闭。该路线框架的独立轻量抽检与本次定向复核完成，可按 ready_with_source_gaps 交付。原报告所列最终复习课／mock／最新考试说明、全课教学与视觉等未抽／未核范围继续保留，不据此推定本人已学会。
