# EF5560 M02 最终发布元数据绑定核验

## 0. 对象、身份与范围

- 独立绑定核验者：`/root/review_ef5560_m02_main`。
- 本轮元数据作者：`/root`。
- 元数据来源候选：`author/main-bridge-proposed.md`，SHA-256 `2fd0501e90f9892a07604b896e13f3d52f7db17eadf83bb8edbd05ebd5235102`。
- 最终拟发布候选：`author/release-metadata-proposed.md`，SHA-256 `bbe947f74ccc94a15be7d53174701d5c51d6ace378240f711fb4cb9f15e64064`。
- 精确变化：`author/release-metadata-changes.json`，5 项非教学元数据替换。
- 本轮未重开教学、来源、视觉或机械评分。

## 1. 精确差异核验

五个 `old` 在 `2fd0501e...` 中均恰好出现一次。按 JSON 顺序在内存执行五次 old→new 替换，所得全文与 `release-metadata-proposed.md` 完全相等；因此不存在登记外差异。

五项实际变化为：

1. `updated: 2026-10-23` → `updated: 2026-10-25`；
2. `mechanism_review: pending` → `mechanism_review: passed`；
3. `mechanism_review_mode: efficient-20261002` → `mechanism_review_mode: full-independent-20261023`；
4. `readability_review: pending` → `readability_review: passed`；
5. 历史 2026-10-02 段落中“当前 pending”的旧指针，改为“历史状态不作为本次全篇审查依据；现行结论由本任务 full/v2 回执与当前 frontmatter 共同记录”。

第 5 项保留了历史事实：2026-10-02 当时写过 `mechanism_review: passed`、当时没有独立全量 Q/R 盲读、未补造评分。它只更新现行状态指针，没有把旧简化流程改写成本次 full 独审。

## 2. full + targeted 审查并集绑定

最终 `bbe947f...` 的教学状态由以下真实证据链共同支持，不由 frontmatter 自证：

| 阶段 | 审查者 / 作者边界 | 报告与 SHA-256 | 绑定结果 |
|---|---|---|---|
| 原 full 两阶段独审 | 作者 `/root`；独审 `/root/review_ef5560_m02` | `independent-review.md` · `f199130e4029879f451c4fe8237c1c45f3e07ad795f228fe8f10fb62951e8c99` | 全篇范围、来源、原题、图表、代码和初始阻塞 |
| 原三轮定向关闭 | 作者 `/root/review_is5113_m01`，主代理 `/root`；独审 `/root/review_ef5560_m02` | `targeted-accepted.md` · `a51cc84457a1671bc28db3525e6f87306341fe9fa949273a6094ed516ec84315` | 绑定 `3786742...`，关闭原 full 阻塞 |
| 84 项主修变化 | 作者 `/root`、`/root/review_is5113_m01`、`/root/repair_ef5560_m02_main`；独审 `/root/review_ef5560_m02_main` | `targeted-main-recheck.md` · `96e330ace2f4789512053c66882c8a8568c061bc977dbd81ccab2eaec633673c` | 绑定 `31a6336...`，理解/来源通过；留纯标点 |
| 三处小桥 | 作者 `/root`；独审 `/root/review_ef5560_m02_main` | `targeted-bridge-recheck.md` · `41e9a1e699fa8cbebdd21c2985efac5e1ec6929a78147b013f9028c3b77cc4ef` | 绑定 `2fd0501e...`，关闭 corr/CPI/标点，`unresolved=[]` |
| 本轮元数据 | 作者 `/root`；绑定核验 `/root/review_ef5560_m02_main` | 本报告 | 仅把已完成审查状态映射进最终候选 |

真实作者集合为：`/root`、`/root/review_is5113_m01`、`/root/repair_ef5560_m02_main`。独立审查者 `/root/review_ef5560_m02` 与 `/root/review_ef5560_m02_main` 不应写入作者集合。

据此，`mechanism_review: passed`、`readability_review: passed` 与 `mechanism_review_mode: full-independent-20261023` 能准确概括这条 full + targeted 并集；不是沿用 2026-10-02 的历史简化状态。

## 3. 材料 audit 的解释边界

主代理提供的三源材料 audit 已实跑 PASS：总计 1245 条记录来自 M01 + P1 + P2；其中 M02 P1/P2 仍分别为 379/260 段和独立时钟。11 条机验引文、422 个时间戳只证明机械登记与匹配，不替代逐源语义核对。现行来源接受仍以原 full、后续定向报告及主代理全文源核为依据。

本轮没有把材料 audit PASS 写成“教学自动通过”，也没有将 1245 误写成单个 M02 转录的段数。

## 4. 条件性接受与正式生效边界

五项元数据变化作为**最终拟发布候选**可接受，绑定 SHA 为 `bbe947f74ccc94a15be7d53174701d5c51d6ace378240f711fb4cb9f15e64064`。

但 frontmatter 的 `passed` 不是自动发布开关，也不证明 canonical 已更新。只有在主代理完成并记录以下事项后，才可将该候选正式写入：

1. current full gate 与其要求的机械、来源、视觉、链接和完整性证据完成；
2. 写回前确认真实基线未变化，并以 CAS/原子方式写入；
3. 写回后精确回读，确认正式文件 SHA/内容与批准候选一致；
4. 后续台账、Notion、Git 或发布分别按各自流程验收，不由本元数据推定完成。

若 full gate 或 CAS 失败，正式文件不得获得这组 `passed` 元数据；候选报告仍保留为待处理证据。若候选正文或状态再发生实质变化，须重新绑定新 SHA 和相应复核范围。

## 5. 结论

- 五项变化：`accepted_non_teaching_metadata`。
- 登记外差异：无。
- 最终候选绑定：`bbe947f74ccc94a15be7d53174701d5c51d6ace378240f711fb4cb9f15e64064`。
- 独立教学并集：原 full + 原定向 + 84 项定向 + 三小桥定向，作者/审查者身份已如实分开。
- 正式写回：`conditional_on_root_full_gate_and_CAS`。
- 自动发布、Notion、Git：`not_evaluated`。
