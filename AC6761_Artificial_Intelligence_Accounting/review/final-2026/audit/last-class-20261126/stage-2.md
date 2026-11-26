# 阶段二：来源核样本与当前发现

- 审查者：`/root/independent_review`；未参与候选写作；作者／统筹：`/root`。
- 日期：2026-11-26。承接 `stage-1.md`，没有覆盖阶段一观察。
- 当前仍核原候选 SHA-256：`0F61CF7912577292F09587B590E836C271A5CC1F70B082FE927E4B54FB74B8B9`，阶段二结束时哈希未变。
- 本次是复习课、节选材料及新增笔记的轻量抽检；不把 00:44:54 前原音或旧 M 笔记重新纳入制作／验收范围。
- 已读制作流程 §3、逐页图示规范、可读性总规则、AC6761 可读性细则；通用规则自动注入的限制见阶段一。

## 实际来源与查看条件

1. 转录：`last-class-transcript.txt`，定向核 01:07:36–01:14:20（REA）、01:15:38–01:19:08（SQL）、01:24:11–01:26:43（Stakeholder Prompt）、01:27:47–01:29:55（模型 Prompt）。未人工核听原音，结论是与所给带原时钟转录相符，不是音频逐字认证。
2. `slides.json`：核 W5／5–9、12；W6／6–7、13–17；W9／4–6；W10／2–3 的抽取文字和可用备注。抽取文件不是另一独立教师来源。
3. 实际看清 9 张 1920×1440 源页渲染图：W5／5、6、7、9、12；W6／6、13、14、15。W5／12 是发现 ResourceType 差异后定向补看的一页，不扩大为全篇重审。
4. 图像查看载体是工具返回的完整源页图，可以读清上述图的节点、关联标签、颜色、题面与输入／输出数字。不是正式 Obsidian 候选显示；后者仍由主代理核。
5. 查看了 `exam-content.md` 中范围表和来源限制，仅作候选的范围草稿对照，不把它当录音证据。
6. 未看机器报告，也未修改源 PPTX 或候选。为原页映射作了只读 XML 结构比较，结果见下文限制。

## 来源核对结果

### REA 方向、三种核心关联与扩展

- W5／5 图中 Inventory／Inventory Type—Stockflow1—Purchase，Cash Account—Stockflow2—Cash Disbursement，两经济事件之间是 Duality。Purchase 连 Purchase Agent、Receiving Clerk、Supplier；Cash Disbursement 连 Supplier、Payables Clerk。候选的收货／付款方向及参与者读法与源图一致。
- W5／6 图中 Sale or Service Engagement or Rental 是减量事件、Cash Receipt 是增量事件；客户取代供应商，Salesperson／Cashier 分别参与。候选销售变式没有把商品与现金方向倒置。图中的线是关联线，不应读成规定时间或付款笔数的箭头；候选已明确不从空白骨架猜多重性。
- 转录 01:08:40–01:09:08 支持“给简化骨架、熟悉框与关联”，01:10:50 与 01:13:18–21 支持只保留 Proposition／Reservation 与相关的两种事件，其他扩展可以忽略。
- 转录 01:11:30–01:12:47 支持推介商品→客户签约承诺→之后交付收款，以及承诺后保留商品的业务解释。候选英文参考与该段意思一致，并已标自拟；没有把承诺误当成已交货。
- W5／7、9 的黄色 Proposition 连 `ResourceType` 与 `InstigationEvent`；黄色 Reservation1 连 `ResourceType` 与 `CommitmentEvent`。另有 Reservation2 连资源与承诺，不能把所有资源侧关联概括成只有两根线。W5／9 新增红框突出两种事件，候选已辨认该增量，但对 ResourceType 的正式线端尚有 F3。

### SQL 题面、输入、输出与原写法

- W6／6 完整题面是保留 Customer #2 收款的全部详情。Cash Receipt 中 RA-1、RA-2、RA-5 的 Customer Number 为 C-2；完整结果六字段分别为候选两张窄表所列内容，金额 1,666／10,000／1,666、账户 BA-6／BA-7／BA-6、日期 25 July／26 July／25 Aug、Cashier E-39 均吻合。排版拆表没有删除列；原图保留了完整输入表。候选说明文本编号引号缺失是勘误，没有把原 SQL 静默改掉。
- W6／14 的完整 Sale 输入为 S-1 至 S-7。7 月五行及金额／日期与候选结果相符，S-6（15 Aug）、S-7（21 Aug）不满足日期范围。源页明确端点包含；候选没有删掉 31 July。原题未给年份，候选未补造年份。
- 同一 Sale 输入还支持 §7.4 自测：非 E-10 只有 S-1／E-12 和 S-7／E-99，再加 Amount >= 10000 后仅剩 S-7／23,000。该自测是自编，没有冒充源题。
- W6／15 的 Cash 表 BA-6、BA-7 为空，BA-8 为 75,000，BA-9 为 0；IS NULL 输出前两行，与候选一致。W6／13 明列 AND／OR／NOT，说明逻辑是当前材料的一部分。
- 转录 01:16:17–01:17:00 支持给表、给 SQL、改条件后写结果；01:17:17 明确忽略内外连接；01:18:51 说从原 p.52 开始可以忽略、不要求计算。此处不能弱化成仍属低权重必算。

### Prompt 来源地位与任务迁移

- 转录 01:24:55、01:25:11–28 支持至少五类、角色不局限详讲五类；01:25:48–58 支持 Prompt 给清楚指导、Question 可简洁；01:26:26–43 支持每类至少两项且相关即可。
- W9／6 抽取只见标题和“Stakeholder Prompt 设计模板”，没有实际教师模板正文。候选将完整英文示例标自拟，来源地位处理成立。
- 转录 01:27:52–01:29:43 支持八个已介绍模型、熟悉三至四个、提具体相关问题、无需解释模型本身或列全五力；Value Chain 未介绍。候选的四个重点示例没有变成“卷上必任选这四个”。
- 这些结论核的是教学任务和来源地位，不证明英文示例在真实考试中的分数，也没有运行 AI 输出。

## 当前待处置项

### F1：维持定向教学阻塞；属于笔记补充桥梁，不声称教师考过组合题

原页逻辑和空值分别在范围内，转录也明确会改 SQL 条件。候选已经主动提醒未知与 NOT，但没有给出足以执行该提醒的规则，阶段一的复做断点仍成立。只需用原 Cash 四行补足一例，不要求展开完整 SQL 理论。

来源核查进一步确认：`Balance >= 50000` 对空余额不能按已知零处理；`NOT` 不会让未知自动变真。官方外部说明可作为补充准确性依据，不能当考试范围证据：

- [Access 运算符](https://support.microsoft.com/en-us/access/table-of-operators)：比较可能返回 True、False 或 Null；与 Null 比较仍未知。
- [Access 与 SQL Server 的 Null 比较说明](https://support.microsoft.com/en-us/access/comparing-access-sql-with-sql-server-tsql)：Access 的三值逻辑及 WHERE 中误处理空值的风险。
- [Office VBA Not 运算符](https://learn.microsoft.com/en-us/office/vba/language/reference/user-interface-help/not-operator)：表中明确 Null 经 Not 后仍是 Null。此项用于确认 Office 表达式语义；仍应和 Access 的空值说明合用，不拿 VBA 文档冒充课程原页。

获取日期均为 2026-11-26。未在真实 Access 数据库运行；不要写成已作 Access 执行测试。

### F2：回源确认应统一排除强度

- REA：01:11:00 与 01:13:18–21 明说其他扩展可忽略；候选 755 行的“本次降权”比来源弱，应统一为本次排除／可忽略的范围处置。
- SQL：01:18:51 对原 p.52 起“不要求计算”表述明确；1026 行的“不作为当前计算重点”容易被读成低权重仍必算。建议直接写清本次不要求该页计算，不扩大为 W3 共同比也不算。
- 此项是小范围实质边界修复；无需删除源页或旧知识。阶段一未据此判整篇阻塞，现依据来源把它列为应修的准确性问题。

### F3：新增的源图线端缺口，需要定向修复

- 位置：候选 707、727、753 行，关联到 §4 Expanded REA 和术语卡的简写。
- 来源：W5／7、9 黄色 Reservation1 实际连 ResourceType；W5／12 原定义对 Proposition 与 Reservation 都写 resources or resource types。
- 现稿：Proposition 在 753 行保留“资源或资源类型”，Reservation 只写“资源”；727 行把图上资源关联概括为“两条”，没有限定是黄色高亮的两类关系。
- 影响：读者从该页回图找 Reservation1 时，可能错找成只连具体 Resource 的 Reservation2，或以为 ResourceType 不是合法线端。这是样本内的图文对象缺口。
- 最小处置：Reservation 的正式解释同时保留资源／资源类型；原图读法指认黄色 Proposition、Reservation1 的线端，并说明 Reservation2 仍是同一类关联的另一个实例。避免要求记全部扩展和多重性。不必新建复杂图。

### S1：导航建议的规则地位说明

阶段一已实际通过搜索完成 §4→§2，故不伪称无法定位。但总规则 §11 要求速查有回指；四个高风险速查行可加精确正文链接，符合本次考前回查目的。仍不把它当作专业知识缺失，也不据此扩查全部链接。

## W5 原主课件页映射的核查边界

主代理报告节选 7／9／11 应分别来自原 22／24／26；原候选写 37，须更正正文与 §8 等对应位置。本人用只读 XML 比较了原 `course_files_export/Week 5 PPT.pptx` 与节选的文本／形状位置：原 26 对节选 11 完全同签名；原 22 对节选 7、原 24 对节选 9 因节选高亮等编辑未完全同签名。本人没有额外渲染并实际观看原主课件这三页，不以这次非完全相同的结构比较冒充视觉确认；22／24 的精确原页身份承接主代理的实际源图核对，最终须在其证据记录中保留。

结构核查脚本 `review-source-map.py` 最初因本解释器缺 python-pptx 而报 ModuleNotFoundError，随后改为标准库 ZIP/XML 只读解析，不安装依赖。脚本不写原件；输出不等同图形颜色／样式校验。

## 样本资产 SHA-256

| 源页图 | SHA-256 |
|---|---|
| render-w05/s005.png | F9B0767EFFB986EBE7B5CF2FA7B72A6CAFB87D4BE310FBF6799F1307312ED04B |
| render-w05/s006.png | 8FF4D9B9E7F16E2DDE1AC20258691EC8E8A73A3B6809AD978A1392C54B956D2F |
| render-w05/s007.png | 09101713FC31CE4FDC0730F54766249D1B09232D77B83FBAAE81F8635447F9F1 |
| render-w05/s009.png | 5F072FEA1EE5FD097598FB6F832931279E932E7BD4EF298C4DB440335C37983C |
| render-w05/s012.png | 0CF90A5077D91F943BE15A8607FF3FF15072CEE82C7DF114CE7BF632672ACD6A |
| render-w06/s006.png | BFCBF13520853E1C4695D19610557E019F593BD187703D5BEA37B161765EFF39 |
| render-w06/s013.png | BBDB078D99F1E19456BA91687815FCF76766EB51765627E9D29EF7324CF4CAB4 |
| render-w06/s014.png | B07F769B33C58456AFD299E64FDC0551F2C949710658F678F85848A87D8D408E |
| render-w06/s015.png | D6DEB4EDEA2EE129765E6BD2427F7AA0CAA4F58C1F683E0FB4D7E56062C276E6 |

## 当前结论与未抽范围

抽样 SQL 的原题面、原图完整输入及给定结果、REA 核心方向、Prompt 的来源地位与迁移要求有对应证据。F1 尚待补闭，F2 尚待统一，新增 F3 尚待修复；不能签教学完成。等待修后候选，对这三项及精确链接／映射变更定向复核，不重审无关章节。

阶段一所列未抽范围继续有效。未逐字核听原音、未看未抽 122 张源页、未核全部题目与全篇算式、未看正式 Obsidian 文字与嵌图显示、未核机器报告、Git、看板或用户学习状态。9 张独立源页视觉样本不等于全 131 张独审，主代理仍承担全范围来源、最终显示与写回责任。
