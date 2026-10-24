# AC6761 M02 依赖同步草稿 v3 定向接受

## 身份与绑定对象

- 独立审查者：`/root/review_ac6761_m02`
- 教学正文作者／依赖同步主写者：`/root`
- 正式 M02 SHA-256：`5C62D4A571B24381593BE3300ADD134EDBF5649D8D5E18977EDD30E14E1DEE5B`
- v3 补丁包：`patches-main-v3.json`
- v3 补丁包 SHA-256：`D8982315C7712BD499CB28C55EA80A031E106FAA4203029D1F22043939677EFC`
- v3 聚合差异：`proposed-main-v3.diff`
- v3 聚合差异 SHA-256：`67A3CDC111F24D84CCF6B7F1B89313E32634C4BBBC53CE4E86E3BA51B61FA261`
- 五处定向修正：`final-targeted-adjustments.json`
- 五处定向修正 SHA-256：`93BEC8C867C4BAA546C103EE915FB57078DDC5F070A418737291B6FAED40DDB2`
- 当前同步决定：`main-current-sync-decision.md`
- 当前同步决定 SHA-256：`E90481F2CC76A73C754CEE07963958B75667395EB6B553EF728EBBB03BE6410C`

本报告只接受依赖同步草稿供 root 最终 preflight/CAS 使用；不重审 M02 正文，不写 vault、Notion 或 Git，不替 root 正式原子写回、精确回读和收批检查通过。

## 五处 v2 → v3 修正

### W3 三段来源范围

1. **O03**：课程总览现在列出 W3 补 Case 2 后段、Quiz 1 布置/课堂活动、试算表用途与 AI 演示；不再用排他的“只补”漏掉 Quiz 1。
2. **K01**：知识台账先说明 W3 含 Case 2/Quiz 1 顺延，再把“只补用途/AI 演示”明确限定到试算表；p.46 三步和 p.47 的 45,300 仍没有课堂录音。
3. **TR03**：转录规则明确 W3 补 Case 2 交易 3–12/余额方法与 Quiz 1；试算表部分才是只补用途/AI 演示。该句与同表 M03 转录行、正式 M02 §8 和 W3 原转录一致。

三处均保留 W2 缺尾长度未知、W1 p.77–83 覆盖未知、书面完整不等于课堂录音完整的边界。

### CFO / CFI / CFF 全称

4. **K06**：知识台账改为逐项写明 `CFO = Cash Flows from Operating Activities`、`CFI = Cash Flows from Investing Activities`、`CFF = Cash Flows from Financing Activities`。
5. **T05**：课程术语表使用同一组三个完整对应，不再用斜杠压缩英文。

这两处与正式 M02 首次定义完全一致，没有新增教学概念；分类按现金流业务性质、不等于收入/费用分类的解释未变。

## v3 包与其余 50 条的并集

- v3 仍为 55 条补丁、12 个文件；四个快照文件发生上述五处变化，其余八份 v2/v3 快照逐字相同。
- 12 个正式源文件当前 SHA 仍全部等于 v3 登记的 source SHA。
- 我重新从 12 份 originals 按 v3 patch id 顺序重放：55 个 old 均恰好出现一次；全部结果逐字等于 `proposed-main-v3/` 快照，实际 SHA 均等于 v3 JSON 登记值。
- 上一轮 `sync-targeted-review.md`（SHA `C62A7BD7CC365EA9B8FF0E2774E6F759DC537A96355C316B34DB01DB41B51F43`）已语义接受其余 50 条：README 43/32+11/41、正常侧/实际侧、PR/G1、复合分录、Closing、官方 Case 2/Quiz 1、150/350、题源/考试条件、W2/W3/S2 边界、6938 秒未复核状态、个人字段保护和课程/根术语分工。
- 本次五处修复没有改变上述已接受内容，也没有新增独立 Case 2 解析、M03 或其他课程的通过状态。

## Notion 受控 no-op

- `main-current-sync-decision.md` 保存的 root 实际新写前缀使用“W3 补试算表用途和 AI 演示”，没有“W3 只补 Case 2/试算表”的排他表述；前文已列 Case 2 与 Quiz 1 题块，完整三段时间索引仍在正式 M02 §8。
- `notion-module-draft.json` 中带“只补”的文本位于 `superseded_local_draft_fields`，其 instruction 明确不得再次写入；它不是实际外端内容。
- 因此无需为 F1 重写已经正确的 Notion 页面。本审查没有重新查询或写入 Notion，只接受 root 提供的实际非私人摘录与正式 readback 边界。
- 正式 `notion-readback.json` SHA 仍为 `98A1C39126EA0CFF42D167FDFE9BA38FB1D699D8204076D3D2ED8474083A4F4B`；其 private evidence SHA 为 `57C132B7F7335223E61FA9BDD0853C8A4D851D6873A02FCE0B0B023974FAAA3F`。这些证据证明既有写入/回读状态，不授权或要求本审查重复执行。

## 历史文件边界与最终结论

- 原 `sync-audit.md` 和 `patches.json` 保留作者原包历史，其中“独立详细解析已核”等表述已被 main 调整覆盖；它们不作为 v3 通过依据。
- 当前接受依据是 v3 bundle、v3 diff、12 份 v3 快照、`main-adjustments.json`、五处定向修正、上一轮独立语义报告与本报告的并集。
- 机器 replay/锚点只能证明字节和目标定位；本次接受还包括对五处语义及其与正式 M02/W3 来源的人工核对。

v3 依赖同步草稿状态：`accepted_for_root_preflight_and_cas`。

未修改 vault、Notion、正式正文或 Git；仅新增本 scratch 接受报告。
