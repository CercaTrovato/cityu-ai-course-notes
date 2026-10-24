# AC6761 M02 发布元数据提案核对

## 对象

- 独立审查者：`/root/review_ac6761_m02`
- 已接受教学本体 SHA-256：`C0B67BFB14E795132A183E9FD2FE55B21F9E876F58E7B5B271EBB8D0ECAA6BA6`
- 待核元数据提案：`author/release-metadata-proposed.md`
- 待核提案 SHA-256：`9D5C14761E13B013321DB93DBBF19EE90D5FA33D05129138CD3E6F59BCE565D2`
- 当前 canonical 仍保留 `mechanism_review: pending`、`readability_review: pending`；本文件不表示提案已采纳。

## 精确差异

当前本体与该提案均为 3432 行，逐行比较仅有两行不同：

| 行 | 当前本体 | 元数据提案 |
|---|---|---|
| 14 | `mechanism_review: pending` | `mechanism_review: passed` |
| 18 | `readability_review: pending` | `readability_review: passed` |

正文、图、原题、数值及其他 frontmatter 字节均相同。

## 未接受原因

该提案把当前机制与可读性状态升级为 `passed`，却在相邻第 15 行保留：

`mechanism_review_mode: efficient-20261002`

这会把本次真实审查误标成旧 2026-10-02 简化模式。当前通过依据实际是：完整独立高中知识起点初读、规则/逐页材料/原题/转录/计算来源核对，以及随后只对实质修文做的多轮定向复核。候选 3389 也明确旧 `mechanism_review: passed` 只是历史记录，不代表本轮验收。

因此两条 `passed` 值本身有当前审查证据支持，但这份具体 SHA 不能作为最终发布元数据接受。

## 最小修复与后续绑定条件

请生成新的元数据提案，仅做以下三条状态变化：

1. `mechanism_review: pending` → `passed`
2. `mechanism_review_mode: efficient-20261002` → `full-independent-20261023`
3. `readability_review: pending` → `passed`

新提案须保持已接受教学本体其余字节完全一致，并提供新的 SHA。独立审查者核对该 SHA 和三行 diff 后，才能把发布元数据正式绑定为接受。

当前元数据提案状态：`not_accepted_stale_review_mode`。

未修改 candidate、`release-metadata-proposed.md`、vault、Notion 或 Git；未运行或认证正式 full gate、写回与同步。
