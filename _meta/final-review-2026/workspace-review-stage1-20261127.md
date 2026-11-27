# 五课复习工作区独立抽检：第一阶段

日期：2026-11-27。审查者：`/root/review_workspace_audit`。本阶段只读冻结候选，未查原始来源、旧审查报告或机器报告；不作最终通过结论。读取 progress 中随文件保存的旧审查元数据时，未将其当作本次证据，也未打开所指报告。

候选根：`E:/app-data/codex/scratchpad/review-workspaces-20261127/candidate`。

## 实际样本和边界

选两条接续风险不同的路径：

1. AC6761：最后课已经排除大量考试内容，但本人策略仍为全课覆盖；接替者如何开始、走过 U03 等排除内容、再进入新范围模拟。
2. IS5542：11/28 复习课尚未发生、两套考试结构冲突、M07 网页替代来源有边界；接替者如何先开展一小轮并在新增材料后接续。

已实读公共 WORKSPACE-PROTOCOL；两课 review/README、AGENTS、framework、exam-guide、preparation、route；两课 progress 的单元/学习状态/next_step/考试边界，以及框架锁。重点逐项读 AC6761 U01–U10、历史诊断/以后每轮章节与当前入口；IS5542 U01/D1、U09、U12A–E、稳定路线和学习枚举。

未抽范围：EF5560、IS5113、IS6400 的内容；两课所有外链教学正文和原题；任何真实 session/mistake（候选均为空，未测试已有多轮历史的恢复）；共享看板脚本、发布、远端；所有来源事实和旧审查结论；框架锁的完整单元结构逐字段校验。没有把框架缺少逐题教学正文视作缺陷，候选已给既有教学/来源回链。

## 路径一：AC6761 实际会怎样接续

1. 从 review/README → AGENTS → 统一协议，读考试依据、准备、固定框架、动态路线与 progress；另读最后课 §0，再核本人是否有未归档停点。0 条 session/错题只能表示文件没有记录，不能宣称本人从未学过。
2. 如果本人确未开始，按 route 从 U01 假设/约束、交易识别的一小点开始。先问已有理解，让本人尝试，卡住才逐级提示，再用未见小变式检测。不能一次发整套答案。
3. 将全课知识、考试范围和个人证据分开：U03 等仍在固定框架中；W2/T 账户不属当前期末必考训练；它们没有因排除而变成“已学会”。W3 共同比仍须计算，不能把 Ratio 不手算扩大为所有计算排除。U17 必须使用新范围，不沿旧蓝图把 JOIN/回归当必考。
4. 本人尚未决定“简讲不考内容后全课继续”或“先考试后补全课”时，应承接统一协议和 route 的全课覆盖，不自行跳过整个 U03；具体深浅、前置补桥和顺序依据记录在 route。这里存在下述 R1，当前文件还没有完全消除执行分歧。
5. 一轮结束，保存本人原问原答、提示顺序、讲解/纠错、题目来源与曝光、结果、未会处和下一步。AC6761 现有字段是 `status` 与 `mastery_level`，后者只用 `unknown/explanation_seen/solved_with_hints/solved_independently/retest_passed`，不能抄 IS5542 的 `mastery` 或 `independently_correct`。只有真实错答建 mistakes；未作答只能记等待。
6. 新解析做一次独立轻量抽检后原子写回；保留原始学习事件。同步 progress.next_step、route、README，并在 handover 交总监督做共享三端收尾，不能自行给其他会话发消息或改共享看板。

## 路径二：IS5542 实际会怎样接续

1. 读相同入口链，报告目前 12 主单元、U12A–E 子单元、0 条已落盘 session，先核本人实际停点；没有则只给 U01/D1 一道诊断。
2. 不等 11/28 资料才开课。D1 区分聊天窗口与实现，先收本人答案；若不会，给最小提示/解释后用改条件题。照 U01→U07→U02 等依赖走，U09 可用现有 M07 62 页网页与笔记，但保留原课堂 PPT/影片和 partial 录音缺口；材料已接入不生成本人掌握。
3. 当前 20/30/50 与 20/80、五选四均未定本学期最终结构；不据其编正式模拟或断言选答。11/28 后取得可靠说明，再更新 exam-guide/preparation/sources 和 route，保留原学习事件与单元 ID，不从一次新公告重建课程。
4. IS5542 用 `status`、`mastery`、`evidence`；学习政策给出 `explanation_seen/solved_with_hints/independently_correct/retest_passed` 等状态依据。只有提示后完成时记提示，不可升级为独立；延后复测是计划，发生后才记通过。
5. 记录 session 原问题/原作答/提示/纠错/讲解/方法/曝光/停点，真实错答才入 mistakes；本轮并未全单元学完，就不得用一次正确覆盖全单元。随后同步三份当前入口并按统一协议交共享收尾。

此路径在候选内部未发现会导致自行选择最终考试结构、等待缺源而完全停学或把材料接入当本人学会的阻塞。

## 本阶段发现

### R1：AC6761 有两条仍有效的默认动作指令，可能把未决定的全课策略改成先只学考试范围

位置：`AC6761.../review/final-2026/framework.md` 第 21、23、240 行；对照同课 route 的“答复到达前，承接11/23全课覆盖策略”及统一协议的“按清楚的知识依赖把全课教一遍”。

framework 当前入口仍直接写“先学其保留点并完成自测”，给仅含保留点的复习建议顺序；末尾又写“接下来先按已取得的最后复习课保留范围学习并做对应自测”。这不是单纯保留旧考试事实，而是在候选新启动入口下仍可读成下一步操作。当前 route 表主要列考试处置，未明确 U03 等排除单元在全课默认路线中的教学动作。接替者可以同样遵循候选，却走出“先考试后补全课”的未获决定路线。

影响：不会阻塞第一小点 U01 开始，但会在 U02→U03/U04 分岔时让执行偏离本人默认策略，属于需要在交付前消除的接续歧义。它不要求改掉框架单元，也不要求制作逐题正文。

建议：明确 framework 中上述段落只说明“考试训练优先级”，直接声明当前教学执行顺序由 route 决定；route 明确在本人回复前如何继续覆盖 U03 等不考内容，且不把它们列为期末模拟必做。不得把询问中的选项记成本人已经选择。

### 非阻塞观察

- README 的早期维护段仍有“未开始本人学习或诊断”等措辞，但上方明确仅报告已落盘记录，并要求核本人停点；按规定入口顺序可避免“无记录=零基础”。可顺手弱化旧句，但不作为本次放行阻塞。
- 两课学习字段/枚举确有差异，公共协议要求沿用；AC6761 mastery_policy 有明确字段与枚举，可执行，不需要统一格式。
- 缺教师 mock 和允许材料阻塞正式条件模拟的认证，不阻塞小点教学；候选已正确区分。

## 候选 SHA-256（本次实际读取版本）

```text
ada8fdc3128d951417ff9b15fce914e7c8bb790e7138b55942931ed84de6748c _meta/final-review-2026/WORKSPACE-PROTOCOL.md
0aa632c82458d711110c071d930479432b2504408168a84a818dac8edd7be36a AC6761_Artificial_Intelligence_Accounting/review/README.md
0fd01322f227acc90e71099342c46295a396d170f44bf3c579d9a493bace9933 AC6761_Artificial_Intelligence_Accounting/review/AGENTS.md
4fcda74e64f6ecadee20b20d900f35f8cb9931f941e5a0e2caec04cfe9393501 AC6761_Artificial_Intelligence_Accounting/review/final-2026/framework.md
5d6870155d53f22e792478cdc105bc6f231c17ae8fb6530fae155d6763d0b96b AC6761_Artificial_Intelligence_Accounting/review/final-2026/exam-guide.md
81a7d0ae1b9d695afa3ea96d19535d10b2ad4a1bb5b253fb890c375e012ce388 AC6761_Artificial_Intelligence_Accounting/review/final-2026/preparation.md
cdc61c959df26aab35b5915d7aa4c378f02675ad16e0d0008a62822df80f15d9 AC6761_Artificial_Intelligence_Accounting/review/final-2026/route.md
4e4cc773747856748607f2cfa0e78593d9bda7f57553862b4bfb27837802964a AC6761_Artificial_Intelligence_Accounting/review/final-2026/progress.json
dbddbbba07a018587ea3d4a18ca7925d5aa6084e36c182e22103b1936fbe88d5 AC6761_Artificial_Intelligence_Accounting/review/final-2026/framework-lock.json
29e756025fde9835e35882b079b5458274b0160dc58f6d86a544d7fa8250423d IS5542_GenAI_in_Business/review/README.md
7226f0466e95051dbafa06128106a984bfa686ae00f80676194bc04ab5cb5d22 IS5542_GenAI_in_Business/review/AGENTS.md
9560393b29dddb00123adee5d85b46bfee830a379d24aefe675a991800e3008c IS5542_GenAI_in_Business/review/final-2026/framework.md
22febd4958a05dcc2e2c1043000376e9f45358aa6cafd7cb4050f0fe56e764ee IS5542_GenAI_in_Business/review/final-2026/exam-guide.md
a9a750243be750da9f7193bfa4d4e699f5685d58ef8bc6dbb288e5b123dab17d IS5542_GenAI_in_Business/review/final-2026/preparation.md
e6abf69cd29ac2c1fa146af963ad43876ca8a9475a0850a67daa86bf2a38ef2a IS5542_GenAI_in_Business/review/final-2026/route.md
82475163a7f28035df3b654aa5867d4c8f75ec00caaf189e209c821582d13c8f IS5542_GenAI_in_Business/review/final-2026/progress.json
3ec64c6242b0757ecc09af8e5f46d0eab7ab149155629481610bc387c0dde2e7 IS5542_GenAI_in_Business/review/final-2026/framework-lock.json
```

第一阶段结束，等待第二阶段规则、原始策略/来源与定向修订；尚未作最终通过判断。
