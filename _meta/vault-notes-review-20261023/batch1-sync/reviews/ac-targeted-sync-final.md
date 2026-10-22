# AC / 根级同步 v2 定向复核

- 审查者：`/root/review_ac6761_m01`
- 审查日期：2026-10-23
- 本轮范围：只复核 `ACP02`、`ACO02`、README `R01` 的更新文字及三份 Notion 最终回读证据；不重扫上一轮已经关闭的 26 项，也不审 EF v2 新增补丁。
- 上一轮报告：`ac-targeted-sync-review.md`，SHA-256 `a1d12623a43017280653892dce49002455800c6bdce4cfec2c1c4336ce599245`。
- v2 补丁包：`patches-main-v2.json`，SHA-256 `8f9bdf0bf91bc83b7f919fe184cc8280dabf77b2c5057c4afb8d3e076d7e0d3a`，65 项。
- 写入边界：本轮读取 scratch 预览与回读 JSON；未改 vault、候选或旧报告，未执行依赖写入、Notion 写入、Git 提交或推送。

## 1. 两处 AC 残余

### ACP02：正文语义已关闭

- v2 预览：`preview-main-v2/AC6761_Artificial_Intelligence_Accounting/_prep/课程前置资料.md`，SHA-256 `de70adc6ba993bc4635b563904365f6e0c98c7f076308e62d1acfc726300a2f3`。
- 实际位置：第 259 行，“W1 转录首句已在讲课中段，只能确认开头缺失、缺失长度未知，不能用考试时段估算缺口长度”。
- 判断：已把“可能缺失”改为已知的“开头缺失”，同时明确缺失长度未知；没有再从期中考试时段反推常规课时或录音缺口长度。上一轮 ACP02 残余关闭。

### ACO02：正文语义已关闭

- v2 预览：`preview-main-v2/AC6761_Artificial_Intelligence_Accounting/00-课程总览.md`，SHA-256 `eadc97da9b2cd060ad10a8fd959284a87d817a1ec3ddcea11f228e8ee6233b98`。
- 实际位置：第 103 行，“W1 开头缺失、W2 转录尾部缺失，p.77–83 的课堂覆盖仍未知”。
- 判断：“W2 顺延尾部缺失”的歧义已消除，缺失对象明确为 W2 转录；p.77–83 仍保持未知，不把时间戳连续或零关键词命中写成完整覆盖结论。上一轮 ACO02 残余关闭。

## 2. README R01 与三份 Notion 回读

- v2 预览：`preview-main-v2/README.md`，SHA-256 `be2b87228f0e27354fe26f1fd7067673e41dd25e29d15ea3bffd217e48550c8c`。
- 实际位置：第 9 行写明 AC6761 M01、EF5560 M01、IS5113 M01 三篇已正式写回，三篇对应 Notion 均已写并回读，且本人字段未变；其余依赖、Notion 与 Git 分别追踪。

三份实际回读证据为：

| 页面 | 证据文件与 SHA-256 | 路径 / 备注 | 其他字段 | 材料版本状态 |
|---|---|---|---|---|
| AC6761 M01 | `notion-verified-final-3d58310b259681529000fc553d526571.json`；`fd8f29eda83fa5ea0ba63bad509dd264c3e80fb4b53f6b093c5af53310be7484` | `path_equal: true`；`remark_equal_after_markdown_escape_normalization: true`；旧备注完整保留 | `all_other_fields_unchanged: true` | 回读仍为 `状态: 笔记v1.0`，与写前相同 |
| EF5560 M01 | `notion-verified-final-3d58310b259681d1a6caeb000d9a7dc9.json`；`baeedc6fa2216bb99cc256eff5995c08a2e08a1345898dd95a49ec9ccf137a13` | `path_equal: true`；`remark_equal_after_markdown_escape_normalization: true`；旧备注完整保留 | `all_other_fields_unchanged: true` | 回读为 `状态: 笔记v1.0`；证据声明除路径/备注外字段未变 |
| IS5113 M01 | `notion-verified-final-3d58310b2596814db0f7dac4f73c5459.json`；`4f596418b0e09f5791fcdc30870198f64e9592a2889c5ac08e6c552de2b04141` | `path_equal: true`；`remark_equal_after_markdown_escape_normalization: true`；旧备注完整保留 | `all_other_fields_unchanged: true` | 回读仍为 `状态: 笔记v0.9`，与写前相同 |

判断：三份文件对应三个不同页面，均证明路径和备注写后回读相符，并明确记录其他字段未变；AC / IS 的写前与回读状态可直接逐值对照，EF 的证据以 `all_other_fields_unchanged: true` 记录同一结论。因此 README 可见文字中的“三篇均已写并回读（本人字段未变）”及材料版本未升级有证据支撑。README 没有把其余同步或 Git 状态升级为完成。

## 3. v2 补丁包元数据仍有一项未闭合

虽然三份目标预览已经实质正确，`patches-main-v2.json` 内仍有两处历史计数没有随 R01 更新：

1. 顶层 `main_refinements.reason` 仍写 `Current first batch now 3 formal writes/2 Notion verified`，应为 3 份 Notion 已验证。
2. `R01.reason` 仍写“将顶部当前状态从未开工改为首批两篇已写回、同步仍未完成”，与同一补丁的 `new` 字段所列三篇正式写回不一致。

这两处不会进入 README 预览，但属于本轮要求绑定的补丁包自身元数据，与实际三份证据冲突。最小修复是只更新上述两个 reason 字符串，不改 `R01.new`、三份目标预览或任何教学内容。修复并重新生成补丁包哈希前，不能把 v2 包整体记为“元数据计数一致”。

## 4. 本轮结论

- `ACP02`：关闭。
- `ACO02`：关闭。
- README `R01.new` 可见状态：由三份最终回读证据支持，关闭。
- 上一轮已关闭的 26 项：维持原结论，本轮未重扫。
- 剩余问题：仅 `patches-main-v2.json` 的两处 reason 元数据仍写旧的“两篇 / 2 Notion”；这是实质内容之外的包内一致性问题，但属于本轮明确要求核对的元数据。需最小修复后再绑定最终 v2 SHA。

