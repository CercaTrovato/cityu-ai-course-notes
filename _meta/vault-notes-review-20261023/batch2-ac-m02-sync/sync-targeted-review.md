# AC6761 M02 依赖同步草稿定向审查

## 1. 身份、对象与范围

- 独立审查者：`/root/review_ac6761_m02`
- 教学正文作者／依赖同步主写者：`/root`
- 已正式写回的 M02 SHA-256：`5C62D4A571B24381593BE3300ADD134EDBF5649D8D5E18977EDD30E14E1DEE5B`
- 本次对象：`patches-main-v2.json` 的 55 条补丁、`proposed-main-v2.diff` 和 `proposed-main-v2/` 下 12 份快照。
- 本次不重审 M02 正文，不重跑全库教学评分，不修改 vault、Notion 或 Git。

关键输入哈希：

| 文件 | SHA-256 |
|---|---|
| `patches-main-v2.json` | `B8FB0C5B50FF49432AEBE77BBEBE32B512805A42F9B5A679986202487BF6ABDE` |
| `proposed-main-v2.diff` | `8EA001A7D4F7DF828288ED47A986FC5F6308DF7D238F109EBA4D32D82758848A` |
| `main-adjustments.json` | `68DBA21657FCD3FD61D6CA1F9729E2A141E33710AD76C97A1D50D352A1455BD6` |
| 原作者 `patches.json` | `E83690A961E22B192DC9BB5D2F1D2E1BCD27627581F03D5627593FCD14FF8123` |
| 原作者 `sync-audit.md` | `83ABB5A995A2A8AA39E68A296296766B618C0528CD6B8CB0925FB623AC9FF28C` |
| `replay-validation.json` | `33249F41486EB94AE0BF1440329124DB048915875DF697F1084D2A672429519F` |
| `inventory-scan.json` | `E083C37B3B3987086C8629913149695308B50F6D852F7BD4E789DF803B6CCB2B` |

## 2. 机械范围与库存复核

- 12 个正式源文件当前 SHA 全部仍等于补丁包登记的 `source_sha256`。
- 我从每份 `originals/*.snapshot` 独立按 v2 的 patch id 顺序重放：55 个 old 均恰好出现 1 次，12 个重放结果均逐字等于 `proposed-main-v2/*.snapshot`，实际 SHA 也均等于 v2 JSON 登记值。
- 12 文件的 patch 数为 5 + 5 + 8 + 5 + 10 + 1 + 3 + 7 + 5 + 1 + 2 + 3 = 55，没有隐藏的第 13 个目标。
- README 数字已用当前 vault 重新计数：43 篇 M/T，`v1.0 = 32`、`v0.9 = 11`，五门课 `transcripts/**/*.txt = 41`；与 R03/R04 一致。
- 这些机械结果只证明重放边界和计数，不替代下方语义核对。

## 3. 已接受的同步内容

### 当前状态、历史和个人字段

- R01–R05、O01–O02 将当前日期和第 4 篇正式写回状态更新为 AC6761 M02；历史日期段没有被追改，M08–M11 等其他讲没有升级。
- D01、D03、D06、X01–X05、A01 正确区分正式 M02 题块、官方 DOCX、独立 Case 2 学习解析和行政状态。独立 `M02-Case2-T形账户与试算表.md` 明确仍待本轮重审，没有继承 M02 正文通过。
- Case 2 保留“无需提交”；Quiz 1 保留“本次不评分、仅作 participation 证据”；没有代填本人作答、提交、成绩或自测状态。
- A01 保留 2026-10-07 历史段原文，只追加 2026-10-25 当前来源和“独立解析仍逐篇重审”的范围声明。

### 会计机制与来源地位

- K02–K05、K08，T01–T04，E02–E10 与 G01–G03 均与正式正文一致：正常侧不替代实际余额侧；PR 账户号与总账 `G1` 页码形成双向追溯但仍须逐行核；复合分录是一笔分录、每一行分别过账；四步排版只作检查顺序，不保证满分。
- 考点库已删除“完整评分标准”“当堂练就是考试形式”“期末极可能”等过强结论。明确失分只保留原话实际支持的范围；Quiz 1 的零余额规则限定到本次 T-account 展示，不推广为所有试算表必须列零。
- 官方 Case 2、Quiz 1 的题源地位、Quiz 1 的 150/350、转录 115/315 原音未核、Service Revenue 重复表只计一次，均与已接受正文一致。
- E07/E08 和 D02/D05 正确记录官方 DOCX 已取得，同时不猜哪个文件就是教授口述的特定 Word format。
- P01 只关闭本课待并入状态；根 `_meta/术语总表.md` 只修既有 Debit/Credit、Posting、审计轨迹三行，没有把 CFO/Closing 等课程专属词新增到根共享表。

### 录音边界

- O04 正确撤回“最多只缺问候”，改为开头是否短缺未知；W2 只确认缺尾且缺失长度不可估，不再用课时倒推出约 20 分钟。
- O05/TR01 保留 W3 的 Case 2、Quiz 1、试算表片段和独立时钟，并说明 p.46 三步与 p.47 的 45,300 具体表未录到。
- TR01 不再把 `01:43:33`–`01:47:42` 严重乱码直接认证为自读；原音未核、性质未知，且不据此升级 M03 教学状态。
- TR02 只把 S2 `06:09`–`24:54` 作为 M02 Quiz 1 讲评来源；S3/S4 只作同批来源登记。`6938.178166` 秒明确是旧媒体登记、未复算、不是课堂墙钟或 M02 教学时长。

### 题源、DDL 与 Notion边界

- Q01/Q02 将 M02 从旧“原件受阻”改为来源限定完整，并继续保留录音缺段/原音未核，不影响其他课程受阻项。
- `notion-ddl-draft.json` 是 no-op：root fresh read 的 AC6761 5 行没有 Quiz 1、Case 2 或 W02 关联，不创建练习行、不改本人提交/评分/截止字段。本审查没有重新查询 Notion。
- 正式 `notion-readback.json` 只证明 root 已对正确页面完成路径/备注回读、旧史 exact suffix 和其他属性不变。本审查没有重复写入，也没有把四个布尔值当作同步草稿的语义证明。

## 4. 正式 CAS 前仍需修复

### F1｜三处“W3 只补……”漏掉 Quiz 1，范围与正式正文不一致

正式 M02 §8 和 W3 原转录已经确认三段：Case 2 `00:01`–`17:43`、Quiz 1 布置/课堂活动 `20:29`–`21:08`（小测活动范围更长）、试算表用途与 AI 演示 `40:14`–`43:54`。但 v2 中三处用了带排他含义的“只补”，遗漏 Quiz 1：

1. O03，`00-课程总览.md` 拟议第 104 行：`W3 只补 Case 2 后段、试算表用途与 AI 演示`。
2. K01，`知识层级台账.md` 拟议第 167 行：`W3 只补试算表用途/AI 演示`。
3. TR03，`转录处理规则.md` 拟议第 239 行：`后到 W3 只补试算表用途/AI 演示`。

这些句子会让读者误以为 W3 没有 Quiz 1，也使 K01/TR03 看起来否认同一包内 O05、D04 和正式 M02 §8 的 W3 题源。

最小修复：

- O03 改为：`W3 补 Case 2 后段、Quiz 1 布置/课堂活动、试算表用途与 AI 演示……`。
- K01 改为：`W3 还含 Case 2/Quiz 1 顺延；就试算表而言，只补用途与 AI 演示，没有录到……`。
- TR03 改为：`后到 W3 补 Case 2 交易 3–12/余额方法和 Quiz 1；就试算表而言，只补用途/AI 演示，未录……`。

`notion-module-draft.json` 的 superseded 备注也用了 `W3 只补 Case 2 后段、试算表……`，同样漏 Quiz 1。它已标明不得重复写，本审查不要求再次执行 Notion；但若正式 Notion 当前备注确实采用该句，root 应把这项语义差异另列为待决定的受控修正，不能由本地依赖 CAS 自动宣称已解决。

### F2｜CFO/CFI/CFF 英文全称被斜杠压缩，未保持逐个缩写的精确对应

K06 与 T05 目前写：

`Cash Flows from Operating / Investing / Financing Activities (CFO / CFI / CFF)`

正式 M02 首用是三个完整对应：

- CFO = `Cash Flows from Operating Activities`
- CFI = `Cash Flows from Investing Activities`
- CFF = `Cash Flows from Financing Activities`

斜杠合写可以猜出含义，但对高中知识起点读者不是精确的一一映射，也弱化了这次专门补全英文全称的目的。

最小修复：K06 与 T05 都改为逐个完整展开，例如：

`Cash Flows from Operating Activities / Cash Flows from Investing Activities / Cash Flows from Financing Activities (CFO / CFI / CFF)`。

这只是把正文已有全称同步准确，不是新增学习概念。

## 5. 历史证据文件的使用边界

原作者 `sync-audit.md` 保留了 main 调整前的结论，例如仍写 P03/P12“详细解析已核”，并引用 `patches.json`、`proposed/`，而 v2 已改成独立详细解析待本轮重审。它可以保留为原作者历史包，但不能作为 `patches-main-v2.json` 的当前通过报告；当前语义结论以 `main-adjustments.json`、v2 快照和本报告为准。

`replay-validation.json` 的 source/replay/anchor 结果已独立复算为真；它仍只是机械证据，不证明 F1/F2 的语义。

## 6. 当前结论

- 55 条补丁的范围、精确重放、12 个源 SHA、README 43/32+11/41 计数、个人字段保护及绝大多数来源/会计边界均成立。
- 没有发现超出正式 M02 的新学习定义：实际余额侧、PR/G1、复合分录、CFO/CFI/CFF 和 Closing 都已在正式正文解释；本批是在依赖表中同步。
- 当前仍有 F1 三处 W3 范围遗漏和 F2 两处英文全称压缩。修复并生成新的 patch/diff/snapshot SHA 后，只需对这 5 处和受影响快照定向复核。

独立同步审查状态：`pending_two_sync_fix_groups`。

未修改 vault、Notion、正式正文或 Git；仅新增本 scratch 报告。
