# IS5113 M09 独立审查当前索引

- 作者：`/root/is5113_update`；审查者：`/root/is5113_m09_review`；视角：模拟高中知识起点初学者，未参与创作或修稿。
- 当前受审冻结候选：`E:/app-data/codex/scratchpad/cityu-notes-20261118/is5113/m09/candidate-v2-frozen.md`。
- 实际候选 SHA-256：`1dea4025e1726bb88a1e6541f0a7b2027b132b0c40647e6a92c385036db7e4fd`，165583 字节。
- 原 v1 SHA-256：`9de1b5071280cf0226a15a18077294090ea4c1372787a1a9e16a984a19a6d689`；原件保留 `frozen-v1/candidate.md`，v1 的 changes_requested 是历史状态，不被追改。
- 来源 SHA-256：`d006d7a05a82b8fb256041a86efcd7ef129f0228681a0089b0643bab69a8ba6b`；97 页源证据不变。
- 全篇范围：§0–§9；97 个逐页入口、全部题面/中英参考、10 道自测及导航、15 个原图、8 个补充 Mermaid。
- 阅读顺序：stage-1 先候选并披露自动注入 AGENTS；root 确认落盘后才给 stage-2 规则/来源/作者证据。stage-2 从全部源页反查候选。随后本次只定向复核 20 个变化/受影响位置，未重开全篇盲审；不声称真人理解。

## 当前独立教学状态

`passed`。两阶段合并 8 项实质缺陷 B1/B2/B3、S1/S2/S3/S4、E-A1 已在冻结 v2 关闭；逐项正文位置、学习动作和关闭依据由原独审者写在 [directed-review.md](directed-review.md)。M1–M3 与 P1/P2 已处理。

本次发现的 L935 `+English reference:` 多余加号是纯维护字符，建议发布前删除，不作为教学阻塞；只作该单字符维护时，可由 root 保存真实 diff 和新哈希并回读后承接本教学报告，不需重开独审。该纯维护尚未在本报告写入时发生，本索引实际绑定仍为上述冻结 v2 SHA。

## 分离的证据与限制

- 第一阶段：[stage-1.md](stage-1.md)，保留原首次发现。
- 第二阶段：[stage-2.md](stage-2.md)，保留原合成清单、来源核正与 E1–E8 的适用限制。
- 全源逐页独立观察：[independent-source-audit.json](independent-source-audit.json)，97 / 97 实际视觉查看；15 嵌图另开单图。
- 本次定向复核：[directed-review.md](directed-review.md)；34 英文原文块、8 Mermaid 源码、15 图引用和标题序列直接比较确认未变。
- `visuals=pending-root`：8 Mermaid 的实际渲染、完整正文/公式/链接最终 UI 尚未由本报告核验；复制 HTML/本地依赖不是显示验收。未绕过现有 URL 策略停止或使用 Edge。
- `transcript=pending / material=v0.9`、官方答案、原始案例/数值未核限制不因教学审查关闭而升级；本人学习/提交/评分字段不触碰。
- 正式写回、Notion、GitHub 与看板同步由 root 依据各自实际证据完成，本索引不替代这些状态。

两阶段及当前报告由审查者自己原子写入并精确回读。后续实质解释/条件/图义变化必须核真实差异；不能仅替换 SHA 将额外教学修改冒充本报告已审。
