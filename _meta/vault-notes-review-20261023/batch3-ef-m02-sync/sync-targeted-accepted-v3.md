# EF5560 M02 依赖同步最终定向接受记录 v3

## 0. 身份、对象与结论

- 草稿作者：`/root/draft_ef5560_m02_sync`。
- 最终合并与 3 项语义精度作者：`/root`。
- 独立审查者：`/root/review_ef5560_m02_main`；未参与本轮 14 项新增操作撰写。
- 正式正文：`D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance/notes/M02-回归与样本外设计.md`，SHA-256 `bbe947f74ccc94a15be7d53174701d5c51d6ace378240f711fb4cb9f15e64064`，本轮未改变。
- 原 82 条包：`patches.json`，SHA-256 `93f62d27d05798ad113cdbe884d295582a607d8c3d528831721ba6f9ad248276`。
- 定向 overlay：`patches-v2.json`，SHA-256 `860db432a0b47949513c5b8d24d6ef6c173e940d851258c87caecde13455fbb6`。
- 最终单一 CAS 提案：`patches-final-v3.json`，SHA-256 `14c46fa893a24005a89773448f2bc86a7cf58fa0d8737b043ec470fb27311341`。
- 最终 diff：`proposed-final-v3.diff`，SHA-256 `b5b4083e802aa428b568f5bfd83bf035b37b38114abab284b12345f5d521254`。
- Notion 私有回读证据：`ef-m02-readback-20261025.json`，SHA-256 `86dd0ffe02cd05a73b7317ebdccfa026a0cb756d7cb78ce7648c33e46e72a9cb`。
- 前次独审：`sync-targeted-review.md`，SHA-256 `ce79b190657369866653be77a5c7a5ed9e9e908eef75c480c5eb57e4b28ea0b3`。
- 结论：**原 B1–B3 已全部关闭；11 条定向 overlay 与 3 条 root 语义精度修正均接受。最终 v3 包无语义残留，可由 root 在当前 source SHA 仍匹配时执行 CAS/原子写入与逐文件回读。** 本报告未写正式文件、Notion 或 Git。

## 1. 叠加重放与最终快照

最终包共 14 个目标、12 个拟修改、2 个已核无增量，按 stage 分为：

- `base82`：82 条；
- `targeted-v2`：11 条；
- `main-semantic-precision`：3 条；
- 合计：96 条顺序操作。

我从当前 14 个正式目标重新读取原文并核验：

1. 当前 14 个 source SHA 均与 v3 登记相同，无基线漂移；
2. `82 → 11 → 3` 分层顺序重放后，14 个结果逐字等于 `proposed-final/` 对应 snapshot；
3. 直接按 v3 的 96 条顺序重放也逐字等于 snapshot；
4. 每个 snapshot 的磁盘 SHA 均等于 v3 的 `proposed_sha256`；
5. 14 条本轮新增操作各自在其所处中间状态中恰好命中一次；没有影响其他基线内容。

v3 中 `targeted-v2` 与 `main-semantic-precision` 的 14 条操作未重复写 `expected_occurrences` 字段，但已独立核为单次命中。最终包的安全边界是**完整 source SHA 比对后写入已登记 snapshot**；不应把它当成忽略 source SHA 的宽松全文替换脚本。

## 2. B1–B3 关闭情况

### B1 · active/excess 两种零基准

课程术语表与知识层级台账现在分别登记：

- `Zero active-return benchmark`：讲义 p.44，主动收益 = 个股 − 本地市场，零表示预期与本地市场持平；
- `Zero excess-return benchmark`：后续数据口径，超额收益 = 总收益 − 同期匹配无风险收益，零表示预期与无风险收益持平；明确不是 p.44 目标，也不升级 M03–M05 教学验收。

LaTeX 分别使用 `\hat a^b_{i,t}=0` 和 `\hat e^b_{i,t}=0`，来源位置分开。原 p.44 合法 active 基准没有被 excess 覆盖。条件均值公式同时改为表格安全的 `$E[r_t\mid x_{t-1}]$`，不改变数学。

状态：`closed`。

### B2 · 数据集卡片

最终 snapshot 已改为：

- `spy_test_predictions_monthly.csv`：60 × 24；
- `weight`：48 个月在市、12 个月空仓；
- 另一个三市场 timing 表的 SPY 45/15 明确为不同结果口径；
- 两个 SPY MSE 写为 `MSE × 10^4`：三市场汇总 20.63、单 SPY 成绩单 20.67；
- 仍保留保存列不等于已取得策略阈值、成交和成本契约。

这些数与实际 CSV 一致。

状态：`closed`。

### B3 · 练习索引与 69 份配套范围

P09、P10、P10a、P10b、P11 及汇总表均明确分层：

- M02 正文对应来源限定解析已核；
- 独立练习精读文件尚未创建、未独审；
- 69 份配套教学范围状态不升级；
- Canvas 是否另发独立练习/书面官答仍待核；
- 旧 p.26/new p.54 的 C 才有课堂确认；新版 D/A 是笔记参考且无对应新录音；P11 课堂未讲、无教授逐项确认。

因此正文通过不再外溢为独立配套题解通过。

状态：`closed`。

## 3. 其余 4 条来源/措辞精度修正

### DDL 课堂提问窗口

“整堂另有 4 次当堂提问给分”已删除。新文只列三个可核题材窗口：相关系数与 R²、国债 ETF 派息、标准化是否改变 R²；不从时间戳数量推断奖励次数，也不把 `25:28/26:01` 同题误算为两次实给分。`might` 原话和制度边界保留。

状态：`accepted`。

### 主动收益与超额收益不是“分母不同”

根术语总表现在写“减去的基准不同”“猜被减去的基准”，并具体列出个股−市场与总收益−无风险收益。两者区别是减数/参照基准，不是收益分母。

状态：`accepted`。

### Data mining 不按课程名绝对定性

原“EF5560 作业/考试一定是贬义”改为：本讲批评“反复试到显著”为贬义；泛指从数据发现模式时仍可中性；按题意和材料说明语境。它保留本讲具体语义，同时不把其他 EF 场景或未审课程永久定性。

状态：`accepted`。

## 4. Notion 与 README 前提

私有回读证据 SHA 与任务提供值一致。我独立比较 `before` 与 `readback`：

- 共 17 个字段；
- 只变化 `卡点/备注` 与 `笔记路径`；
- 其余 15 个字段逐值不变，包括本人通读、自测等字段；
- 新备注与拟写值相符；
- 历史备注 suffix 原样保留；
- 路径已改为正确 code 形式；
- 目标是正确的 `EF5560 Lec02 · Regression and Vibe Coding` 页面。

因此 `README.md::01` 的“五篇对应 Notion 均已写并回读（本人字段未变）”前提已经满足。旧历史备注中仍保留当时“两版 p.25 都错”“缺首 1–3 分钟”等旧文字，但最新前缀已明确纠正当前事实，符合“有日期历史不追改”的规则。

主代理报告 DDL 6 行只读无新增，本包也没有创建新计分任务、DDL、提交或评分事实；`assignment/00-overview/作业总览.md` 保持无增量，接受。

## 5. 最终 14 目标 SHA 绑定

| 目标 | source SHA-256 | proposed SHA-256 | ops |
|---|---|---|---:|
| `EF5560_Fintech_and_AI_in_Finance/00-课程总览.md` | `8d1a3422e366c4ad099c254ff492969e1b9a6cc04fe940aadaf281a73cee97f2` | `bd14535b725847db777a74821514e40e24889f63b2444488be23a803df9b1155` | 7 |
| `EF5560_Fintech_and_AI_in_Finance/_meta/作业与DDL.md` | `fb3e4643b0bb8f84cc83aa76d1f83c559053e29f80c600c526a60771117c830c` | `a36bf93c4c3b60bc2511a8897aafeaa5ac5ddb8349b76d495b8a8ef752c7e3b3` | 6 |
| `EF5560_Fintech_and_AI_in_Finance/_meta/待并入术语总表.md` | `44e26c615b69888dcd9eac699978ca773a93ea12a2cb8646cefda06f3eeb0081` | `a6fd3b05bbd8b538032efb2514230c9cb3bc3ef0121b505b4bf9c9bee4d46542` | 11 |
| `EF5560_Fintech_and_AI_in_Finance/_meta/数据集卡片.md` | `67eacb47b222102a2f22be6af6ac539982334792794aeca827ae9a41d511a256` | `4670034d57b3388bc8aaf02114876c6a5232cc234b2bdf976da09ba00ebdb568` | 10 |
| `EF5560_Fintech_and_AI_in_Finance/_meta/术语表.md` | `e73abecca74f3b54bd1f3fc860b5038f769c9d874554957573d37e62b9980c71` | `eeb06c200dd5bf76ad296960b810589410bd770436d5b3e48f9d2d57a280e117` | 14 |
| `EF5560_Fintech_and_AI_in_Finance/_meta/知识层级台账.md` | `13bcc0eb25fc6faf422ef53ae3d9da4973da7e55165e2f47a97c1ff7303bad38` | `28481cd5fc60a9f9d60d75c15ce4514d3bc8326491fa7ebc5a4ef3d6c82a3bbd` | 13 |
| `EF5560_Fintech_and_AI_in_Finance/_meta/考点库.md` | `947156665b83f575dea2cfb1894862a34a979f71d8829424740422d48682abd6` | `a5a3b71586c591e95d6173a781b8af7c9b37313873dda178ca911adb455e2264` | 11 |
| `EF5560_Fintech_and_AI_in_Finance/assignment/00-overview/作业总览.md` | `7ff281c0fcc913f68ddf42db31a8b44918a3220bd8e33ab59d34d105b4915388` | `7ff281c0fcc913f68ddf42db31a8b44918a3220bd8e33ab59d34d105b4915388` | 0 |
| `EF5560_Fintech_and_AI_in_Finance/assignment/practice/练习索引.md` | `c8bd6e9dd17f25734056e45dbff93aea0fa8a32a0eeb1229d58ec5a0bc17c16d` | `bb5dcfaf7129aafe268bac6490f85d8d724120f3e96fa3c6edd58abeb11055a6` | 8 |
| `README.md` | `8e74633777b9cc10fc3d283d8ded13ec3bfb9086c3c5cafabf961262f55c9270` | `c9cfb71a8da6841c32139e3bb95446fd79620e0e2217607c715c1af7092654dc` | 3 |
| `_meta/Notion进度看板.md` | `e7f16768e29e7662d02b88875709aba15bff95fd533b439a58747b646a8895e5` | `e7f16768e29e7662d02b88875709aba15bff95fd533b439a58747b646a8895e5` | 0 |
| `_meta/术语总表.md` | `6b521fe7a5cb80dcc9912af32f0e519343381480fab5ae0a8a8692e81b15802b` | `82acd94d111be95f0777cb5589d9b9b3cf7ea62c4a1256a259458b299929a0e2` | 8 |
| `_meta/课件题目覆盖台账.md` | `0f0120d5d9c40d275ae6f9d36c73731d38af2e099ab932523a4f9328eb96e5b8` | `a2ab0544bbdd13430795d2383ec78e6d84fce74df496ede4eee101191585a98a` | 3 |
| `_meta/转录处理规则.md` | `b049360cffbb8add86740b035af4323ee61c64706ef97d5253f2ca4308d1c378` | `213e396a40e22b25e4cadcb3432171b910f9de9738af8dfdd93de943d3d69c93` | 2 |

## 6. 最终边界

- 最终包独立定向状态：`accepted`。
- 新增 14 项影响范围：仅 B1–B3、DDL 提问窗口、根术语两处“减去基准”措辞和 Data mining 非绝对化；没有改变正文、其他课程/讲次状态、本人字段或其他基线。
- v3 尚未应用到 vault；root 执行前仍须再次比较 14 个 source SHA，变化者停止并重新合并。
- 应用后须逐文件回读并核 proposed SHA；不能以补丁命令成功代替磁盘回读。
- Git 尚未提交/推送，不得称 Git 或远端保存完成。
- 本报告不授权或声称新的 Notion 写入；它只确认已提供的 EF5560 Lec02 回读证据满足 README 前提。
