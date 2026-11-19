# 五课管理进度候选 · 独立风险抽样审查

审查日期：2026-11-20。结论：**需定向修正后发布**。本次共 6 项实质阻塞，1 项建议；不是历史全文独审。

冻结核对：candidate-freeze.json 的 25 个文件 SHA-256 全部匹配：True。

## 实际抽样与边界

五课 current/decision/叙述头；AC 当前展示/邮件/讲稿；EF 当前合稿/收入边界与旧管理版本；IS5113 终版/提交/Q&A行动链；IS5542 分支、prototype/test、web/p01/p23/acceptance；IS6400 当前稿、投票/冻结/四月历史节点、所有未完成时间线及当前delivery的依赖/管理边。

结构核对覆盖 57 个思路节点、109 条时间线；五课稳定时间线 ID 无删除，开始/完成日期无变动，既有 acceptance 未升级，旧 history 前缀保留。未新增完成日期，已提交和本人只 Q&A 的事实没有回退。

来源回核：EF 远端 9d7ebd5 对 b87083f 的英文报告差异及实际文件 SHA；IS5542 origin/feat/ord001-local-web 的 11/10交付报告与历史模拟模型/接收待核边界；IS5113 work/final-version-20261117.md；IS6400 submitted-reader.md 当前更正与最终13页记录；IS6400 origin/main:progress/timeline.json（只读 sparse 对象，不物化）。

未全篇重审历史金融/论文/实验结论；未逐页重看PPT/PDF；未新跑课程模型、服务、真实模型或网页；未查独立Canvas回执/收件人实际验收；未认证个人已练习或已掌握。

## 阻塞清单

### R1 · AC6761 · management.json

定位：`deliverables[presentation].actual`。

仍写“11 月 18 日课堂展示仍待进行”，而当前复核日为 11/20，current 已正确写日期已过但结果未回传。该字段是当前管理验收，未置于历史区。

最小修法：改为“PPT 邮件发送截图已核；11 月 18 日为已过排期，实际展示及计时结果未回传”；保留 email pass、rehearsal unknown，不推断完成。

### R2 · EF5560 · management.json

定位：`deliverables[merge].actual / checks[draft]`。

当前合稿 actual 仍指定 b87083f、报告 SHA a50173b…，但本轮 current/assignment 已以 9d7ebd5 为当前英文候选，integrated 来源实际文件也已是 SHA fd2eae5e1d5efcbc68881b5e7b483308f6d99eb2e809e1517df5b88cabaecf8c。旧版本没有历史限定，两个当前入口给出不同定稿依据。

最小修法：actual 明确旧 b87083f 是此前已审增量、当前可读候选为 9d7ebd5，并写当前 SHA 或删除旧 SHA 作为当前依据；draft 检查只表达候选已存在/已核文本增量，不能升级全组确认、PDF、录像。

### R4 · IS6400 · timeline.json

定位：`items[date-method-freeze].summary/next_action/my_next_action`。

旧“用已核 A 资料制作新 PPT、未获新授权不得提交”仍是当前个人行动，且旧 agreed 11/12 日期已过。这与最终 13 页已提交、当前只准备 11/25 展示直接冲突。

最小修法：保留稳定 ID、旧 agreed 日期和 history；当前 summary/next/my_next 改为旧冻结排期的结果/记录待核，仅保留研究记录缺口，不再制作或重交 PPT；不把该旧日期改成新承诺，也不凭提交推断科研冻结完成。

### R5 · IS6400 · timeline.json + management.json

定位：`timeline.items[delivery].dependency_gates; management.edges[scope→delivery,team-april→delivery,ppt-a-first-draft-review→delivery,round3-handoff→delivery]`。

当前 delivery 已转为展示与报告，但时间线仍 required 依赖 scope.final=unknown、team-april.wording=gap；管理图仍写“已选 B，可开始制作”“已核 B 素材”“A 稿可组审，不授权提交”。这些是旧制作阶段门槛/标签，会把科研记录修订或旧提交禁令继续挂在当前展示路径。

最小修法：当前展示依赖固定最终文件与已确认分工；科研冻结/四月措辞/3、5号记录修订保留在报告/研究记录条目，并行于展示，不改 unknown/gap 为 pass。同步修正管理边标签为最终已提交 A 稿、展示准备；历史 B 和不得提交指令只留历史。

### R6 · IS6400 · thinking.json

定位：`nodes[local-mainline-role05].next; nodes[time].next; nodes[common-candidate-comparison,ae-followup-validation].next`。

local-mainline-role05.next 仍明确“D14当前pending，团队A/B先投票共同确认”；time.next 仍要求 6 号确认“冻结后的四月回测安排”。另两节点仍未限定地说正式采用待决定。虽部分标题标历史，next 仍给出与当前已提交 A 稿冲突的行动，尤其 D14“当前”会重开投票。

最小修法：将 D14 先投票、四月新安排明确封为当时历史；当前展示不重开投票或回测。若报告研究口径确仍未决，限定为“最终报告的研究采用/披露另待决定”，不要泛写团队尚未采用。

### R7 · IS5542 · thinking.json

定位：`nodes[prototype,test].evidence`。

新增的开发分支/历史 API 与浏览器自检事实仍只引用 report/frontend/eligibility/plan；这些登记文件没有 feat/ord001-local-web、9c8fdbc 或历史交付报告入口。新依据目前只放在顺读稿头部，点击新节点的来源无法直接追到这次新增事实。

最小修法：最小补法是在 prototype/test 的 evidence 中增加已有 narrative 来源；该冻结顺读稿头部已给 9c8fdbc 及两份历史报告链接。若另增稳定来源快照更好，但无需因此重跑服务或把作者自检升级为团队验收。

## 非阻塞建议

- S1 · IS6400 · `timeline.items[round3-member-returns].acceptance[result]`：该项仍写成员回件待收，但 summary 已明确 1–5号收到。它是旧未完成检查且未升级 pass，本轮不必扩大重审；可把标签限定为仍缺的 3/5号修订/实际承诺，保留 received 的历史证据。

## 已确认可承接的边界

- AC 11/18 已过但实际展示/计时仍未知；邮件发送截图不扩展为教师回执。
- EF 的文本增量与当前 9d7ebd5 有对应差异；全组确认、最终 PDF、录像和正式提交仍未知。
- IS5113 终版采用、提交确认及本人只 Q&A 保留；两项历史建议为依决定结案，未冒充技术修复。
- IS5542 9c8fdbc 是开发分支已见；作者历史模拟模型自检不等于当前服务或接收人 P01 通过。
- IS6400 最终13页、11/25 Week13第2组、本人1/2/9页与提交确认保留；独立回执、真人计时与报告分别待证。

PENDING_AFTER_CAS 为约定写回阶段字段，本次不列缺陷；AC新增讲稿边及IS5542实际任务ID定向补丁已在最新候选见到，不重复列缺陷。IS5542管理p01/p23/acceptance的旧交件文案已定向回读并结案。

## 冻结指纹与复核

本报告对应的 25 个候选文件 SHA-256 及逐课不变量结果保存在同目录 `result.json`。修复后只需定向检查本表字段及受影响依赖，不重开历史全审。
