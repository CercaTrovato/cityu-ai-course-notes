# AC6761 M02 最终发布元数据绑定（v3）

## 身份与绑定对象

- 原作者：`/root`、`/root/scope_classification`
- 本轮修文与元数据提案作者／主代理：`/root`
- 独立审查者：`/root/review_ac6761_m02`
- 当前教学本体：`candidate.md`
- 当前教学本体 SHA-256：`2C2496B8FD549DF15F280BD6707DC6E958E6EFFF14BDB4152B1D7919D723EF0E`
- 接受的元数据提案：`author/release-metadata-v3.md`
- 接受的元数据提案 SHA-256：`5C62D4A571B24381593BE3300ADD134EDBF5649D8D5E18977EDD30E14E1DEE5B`
- 变更说明：`author/material-map-changes.json`、`author/release-metadata-v3.json`

旧 `release-binding.md` 对 SHA `9D5C1476...` 的拒绝记录继续保留；本文件只绑定修正后的 v3 SHA，不覆盖或倒改旧历史。

## 最后三处教学本体变更

1. **A7 定位词**：候选 3363 已恢复为“当前反方视角”。该段实际列出最薄弱小节、未知考法与材料限制，定位词与材料 audit 所需语义一致；没有改动其结论。
2. **独立时钟说明**：候选 3152 明确 p.1–47 主表使用 W2 `M02-transcript.txt` 的时钟，表末 W3 与 S2 各用原文件独立时钟，避免把 `M03-transcript.txt` 的时间误当成 W2 连续时间。
3. **三条 W3 索引**：候选 3197–3199 与 `M03-transcript.txt` 实际窗口一致：
   - `00:01`–`17:43` 录到 Case 2 的交易 3–12 处理及期末余额方法；开头已在交易 3 中途，故候选保留交易 1–2 录音不足、完整题面与全余额依官方 DOCX 的边界。
   - `20:29`–`21:08` 要求为受影响账户补期末余额、会收取作参与证据、本次不评分，并写姓名/学号；候选没有推断本人已作答或提交。
   - `40:14`–`43:54` 讲试算表的内部用途、公开披露前仍需调整，并演示 Gemini 根据交易记账和生成试算表；候选明确没有把它扩成 p.46 三步原文或 p.47 的 45,300 具体表。

对比上一接受本体 `C0B67B...` 与当前本体，差异仅为上述一处定位词、一处时钟说明和新增三行既有事实索引，没有新增教学推断、个人行为、原题或数值变化。

## v3 元数据差异与接受

当前本体和 v3 提案均为 3435 行；逐行比较只有以下三行不同：

| 行 | 当前本体 | 接受的 v3 提案 |
|---|---|---|
| 14 | `mechanism_review: pending` | `mechanism_review: passed` |
| 15 | `mechanism_review_mode: efficient-20261002` | `mechanism_review_mode: full-independent-20261023` |
| 18 | `readability_review: pending` | `readability_review: passed` |

正文、图、原题、数值与其他 frontmatter 字节相同。三条状态与本次真实流程一致：先由同一独立审查者完整顺读全部教学内容，再核规则、逐页材料、原题、转录与重要计算；作者修复后，只对每轮实际变更做定向复核。旧 2026-10-02 简化审查只保留为候选中的历史记录，不再冒充当前 review mode。

因此，元数据提案 SHA `5C62D4A...` 在独立教学审查范围内接受，可由主代理采纳。

## 完整独审并集

最终接受由以下连续报告合并成立，而不是由最后三行状态自行证明：

- `stage-1.md`：完整高中知识起点盲读；SHA `A8512957D36546957E8C3184F03A875E9FD8FBC293A38DB5BC5B0B82DE60F4A7`。
- `independent-review.md`：规则、逐页讲义/DOCX、原题、转录与计算来源核对；SHA `2AB94CFFF5A20C057278377297CB0EF9245A573CFF86DE77A1B4D36AD4276FCB`。
- `targeted-recheck.md`、`targeted-final.md`、`targeted-accepted.md`：原 B1–B8 及首次修文关闭。
- `targeted-main-recheck.md`：45 项来源/视觉修文和 ASR 校词；SHA `BCF8ACB3D9D7D3BBFC80B76E68121DEB0A324C56644F0979207767EFE47EDA85`。
- `targeted-final-residuals.md`：视觉/警告补丁、R1–R3 关闭及 F1/S1 定位；SHA `B887B3E97EC486FCB1CB48D5F931A0EC4A11A42DB7D3D61CAD7DF04FDBCCC712`。
- `targeted-final-accepted.md`：最后四处来源修文接受；SHA `15BFDB545AD44E9CE5C6DD4E2DCF39A164623025A9A14F2AA129C11197533861`。
- 本文件：只核 A7、W3 映射和 v3 三行元数据，不重做全篇评分。

这些报告的并集覆盖本篇完整初读、来源阶段以及历轮受影响范围。当前 v3 在独立教学/可读性审查范围内无剩余阻塞。

## 不随本绑定认证的边界

- 当前 canonical 仍是本体 SHA `2C2496B...`，frontmatter 仍为 pending；只有主代理实际采纳 v3 后，canonical 才会成为提案 SHA `5C62D4A...`。
- 原始音频未由本独立审查者核听；ASR 方括号校词只按现存转录、讲义书面词和同段稳定上下文接受。
- `material-main-final.json`、机器 L/C/R 与 historical 输出不替代本独立结论；本文件也不认证主代理未向我展示的全部视觉操作。
- 主代理最终 full gate、root 来源/算术总核、原子写回、正式回读、台账/Notion/README 同步和 Git 状态仍须分别完成并据实报告。
- 不推断用户本人已听课、学会、作答、提交或取得成绩。

元数据提案状态：`accepted_for_adoption`。

未修改 candidate、元数据提案、vault、Notion 或 Git。
