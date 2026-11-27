# 五课层级复习路线独立抽检：第一阶段

日期：2026-11-27。审查者未参与候选撰写。本阶段先读候选，不查旧审查、原课件、框架来源或正式库；结论仅限导航与执行逻辑，不是知识正确性、全课教学完整性或真实学习效果认证。

## 样本与范围

通读统一 WORKSPACE-PROTOCOL、五课 review/AGENTS.md、五份 learning-map 和 route；查看五份 progress 的当前 next_step、sessions、teaching_sequence、单元状态/证据字段。progress 的未抽学科内容不作正确性判断。

深入模拟两条最有风险的恢复路径：

1. AC6761：已有全景导览且题目被暂停的会话恢复 → 财报/业务数据/AI 连接唤醒 → U01 企业与老板边界 → 小情境与理由 → 本人小题 → 财报/业务数据两支 → 考内模拟 → 考外完整补学。风险在于重复导览、把暂停题写成错题、强迫先学排除的记账内容。
2. IS5113：已有地图但尚无学科作答的会话恢复 → 五层关系/招聘情境唤醒 → U01 事实与判断 → 一个小情境的理由 → D1 或同型练习 → 标准与风险/场景连接 → 陌生案例。风险在于抽象伦理术语堆叠、把场景关系当整章先修、把地图理解记成学科掌握。

## 第一阶段结论

两条样本路径未发现需阻止本批落盘的导航阻塞。五课入口、route 的停点和 progress 的自然语言下一步均明确先整体、后分支、小点/例子后再作答。未把地图本身要求成逐题教程。

| 检查项 | AC6761 实际观察 | IS5113 实际观察 |
|---|---|---|
| 新会话是否冷启动出题 | AGENTS §4 与 route 授课顺序禁止用零散题替代导览；next_step.type 为 overview_awaiting_feedback，下一步先连财报、业务数据、分析和 AI，再到 U01。 | AGENTS §4 与 next_step.orientation_check 先接既有地图；route 明示原 D1 曝光未答，并要求 U01 小点讲解后再诊断。 |
| 并列是否被写成严格先修 | 地图明说财报和数据库是互补视角，无须先完成全部记账；route 第一阶段跳过 U03 等排除项，只补必要前置。 | 主干有工具依赖，但表格明示横向关系不限定唯一顺序，案例反复调取标准。没有要求先完成 U03–U10 才能接触任何场景。 |
| 能否从整体降到点再练 | 地图以两表用途→资产/占比→共同比小表为示范，当前路线以企业边界为小点，统一协议补足任务、例子、动作理由、独立尝试/变式。导航足以组织下一轮；实际例题仍由课程会话制作。 | 地图以判断标准关注点→一种标准/小情境→解释理由→英文短答→换标准为示范；当前 U01 路径由 route 指明。无需地图承担完整理论教程。 |
| 考试与全课补学是否冲突 | 第一/二阶段清楚；T 账户、REA 多重性转换、JOIN/QBE 等不会因出现在总图就进入考前必练。 | 未有明确排除表则保留 U01–U17，不能自行以低优先级删课；若后续明确排除才延后。与“先考试、再补全”相容。 |
| 是否重置/虚构掌握 | sessions 保留一次导览、暂停未答题与无答案记录；17 单元仍 not_started/unknown，未把全景曝光升级为独立会做。 | sessions 保留一次 orientation、无本人回答、未更新学科掌握；17 单元未由地图推进；原 D1 曝光不再冒充未见题。 |
| 是否增加过重仪式 | 协议规定一屏左右首次地图、已有导览只唤醒，不反复要求确认；讲清到可做当前考试任务即练题，无固定字数/题量。每轮落盘按一组互动而非每句话。 | 同左；现有“先确认地图清楚”可按一次真实反馈处理，统一协议已禁止反复要求“确认已懂”才前进。无需另加地图考试或全图背诵门槛。 |

## 非阻塞观察与第二阶段核对点

- EF5560/IS5542/IS6400 的 next_step 仍保留 diagnostic 类旧枚举/action，但 description 清楚要求先地图、分支和小例。面向阅读全部入口的代理无实际冲突；若存在只读取 action/type 的自动派题器，需第二阶段核其行为。不能仅凭字段名称认定已发生冷启动。
- AC6761 与 IS5113 都已发生导览；当前“确认”指接既有反馈，不应再次完整重讲。本次未读取实际 session 正文，因此只确认 route/progress 之间自洽，尚未验证导览内容与原对话事实完全一致。
- 两课导览状态均未被升为学科掌握，这是合理区分；不要求把整个 U01 改为已开始来追求表面一致。
- 统一协议“每次进入”第 4 步的“先让本人尝试”在完整上下文中指已完成地图/小点讲解后的练习；其他多处次序明确，未形成实质阻塞。可保持当前文本，避免为防理论误读继续堆规则。

## 未抽范围

没有审查原课件/录音、考试范围事实、具体知识/题目/答案、框架依赖合理性、README/启动文件是否有旧冲突、真实 session 原文、链接解析/脚本运行、最终写回/三端同步。EF5560、IS5542、IS6400 只检查入口和当前下一步，不做同深度完整恢复演练；未检查所有单元跨分支迁移。第二阶段收到规则/来源后再核指定证据，不重开全课。

## 候选 SHA-256

候选根：`E:/app-data/codex/scratchpad/hierarchical-review-20261127/candidate`。

| 相对路径 | SHA-256 |
|---|---|
| _meta/final-review-2026/WORKSPACE-PROTOCOL.md | 2f8039d01dd588fea6261020a11808c1d764ac7c53f792758fbfde1532c66b2e |
| AC6761_Artificial_Intelligence_Accounting/review/AGENTS.md | 7eb915f31d799dde815f222a00f7377fc862736fea67c425efd7de5944dbbe8d |
| AC6761_Artificial_Intelligence_Accounting/review/final-2026/learning-map.md | 3f14b4046b6e8a7cef35714e89cccf7877f7e82e0d1d9aa939f1d10c57f3881b |
| AC6761_Artificial_Intelligence_Accounting/review/final-2026/route.md | 08070d8170583399c269138a5357d2910f37676b07b15ad8a4e51730300991c3 |
| AC6761_Artificial_Intelligence_Accounting/review/final-2026/progress.json | 92fd87473e9d5b9b9bf0e82a33fbca39cc9dede2397c052efef418e43c72b106 |
| EF5560_Fintech_and_AI_in_Finance/review/AGENTS.md | 9209521569034349432e443d46b4c0fa65bc0b5be2829480ed5d9663967c16d1 |
| EF5560_Fintech_and_AI_in_Finance/review/final-2026/learning-map.md | 4f80a420bc292050c5065829717e2406c82ff30787a9e82a2fb6528df72dbbe7 |
| EF5560_Fintech_and_AI_in_Finance/review/final-2026/route.md | 8f4925c0855d569302891de03819d21b44db349a01c98a7ea1547744c5e83d82 |
| EF5560_Fintech_and_AI_in_Finance/review/final-2026/progress.json | 44303de285a6979123d9694e0ca870336bfc9b06d6f17d3ca0c0335a4b7fd1f3 |
| IS5113_AI_Ethics_and_Regulations/review/AGENTS.md | d0c212592e1287cdd9dbc6239ccffb7593dba4eee736059ca8bad87712b63fde |
| IS5113_AI_Ethics_and_Regulations/review/final-2026/learning-map.md | 9943d838a979cb5198be980f6e6f9933d22e06983fb5c7a3047f5735b6b8efd3 |
| IS5113_AI_Ethics_and_Regulations/review/final-2026/route.md | c657da62e6558e2d89ab7e78d517aa0687f2d37f9489c1d786f96532c16b6fb2 |
| IS5113_AI_Ethics_and_Regulations/review/final-2026/progress.json | e59e5b03ab24542b05f2cedfe5eb5ee7de2411e8c5ed6c92ba9933d71ace047c |
| IS5542_GenAI_in_Business/review/AGENTS.md | 25765c829454af0699893282f69978a620e7feda24c7be6ab5b0fc8ea6a6a046 |
| IS5542_GenAI_in_Business/review/final-2026/learning-map.md | d950a8e9961a9018b75d3d716a9a4f2109259572a0d34ca335eb9c25afdfeed6 |
| IS5542_GenAI_in_Business/review/final-2026/route.md | 034718f9788efaee8b25b85d5b54b90f79904d621f24465fa8c25f9e0f321d50 |
| IS5542_GenAI_in_Business/review/final-2026/progress.json | 2be9cbc4eb352978b609c04c2a4b3ba62b1797f9afc26a78ffd6b3db18090ca1 |
| IS6400_Business_Data_Analytics/review/AGENTS.md | 45fd38cb8f951ae9a36de540124f82744e86dea5519caac5f8648f68f200a02e |
| IS6400_Business_Data_Analytics/review/final-2026/learning-map.md | 60f52ead08506c3ce8a0f6444f21fd8974fcfdf46e2281c8b770d63fd950e016 |
| IS6400_Business_Data_Analytics/review/final-2026/route.md | aa54019337ea7370b9f5cbbc73648729ccd940383c70e369b84c22c85a894e85 |
| IS6400_Business_Data_Analytics/review/final-2026/progress.json | c37de76269c326ff105bc4eb5a06b6b802439d8ad9a1f1be899a6549c21fb69e |
