# EF5560 M02 依赖同步定向修复 v2

## 0. 范围与状态

- 基线补丁包保持原字节：`patches.json` SHA-256 `93f62d27d05798ad113cdbe884d295582a607d8c3d528831721ba6f9ad248276`；`proposed.diff` SHA-256 `993e657916dd8a53e0aaf708ca9262240abc0912198cca84f6195613b9454418`；`sync-audit.md` SHA-256 `726e204e32686b67d7b90f373c5f5ab23eea86af81a6d95d6dbd17f7e9719d74`。
- 原独审报告保持原字节：`sync-targeted-review.md` SHA-256 `ce79b190657369866653be77a5c7a5ed9e9e908eef75c480c5eb57e4b28ea0b3`。
- 正式 M02 已由 root 以 SHA-256 `bbe947f74ccc94a15be7d53174701d5c51d6ace378240f711fb4cb9f15e64064` 完成 full/v2、CAS 写回和回读；本子任务未再读取／重审全篇。
- 本 v2 只修独审 B1–B3，并按 root 补充修正 `作业与DDL.md` 的旧“四次给分”计数。共 5 个目标、11 条相对旧 proposed 状态的 exact old/new。
- `patches-v2.json` 是 overlay，不替换旧 82 条 manifest；`proposed-v2.diff` 的左侧是旧包应用后的 `base-proposed`，右侧是定向修复后的 `revised-proposed`。不能直接对正式 vault 单独应用，应在内存先构造旧 proposed，再叠加 v2，或合并为 root 的最终 CAS 写回内容。
- 本子任务仍未修改正式依赖、Notion 或 Git。

## 1. B1：active／excess 两种零基准与公式显示

### 课程术语表

- 保留讲义 p.44 的 `零主动收益基准（Zero active-return benchmark）`：$\hat a^b_{i,t}=0$，目标是个股收益减本地市场收益，零表示预期与本地市场持平。
- 另列后续数据口径的 `零超额收益基准（Zero excess-return benchmark）`：$\hat e^b_{i,t}=0$，目标是总收益减同期匹配无风险收益，零表示预期与无风险收益持平。
- excess 行明确写“不是 p.44 目标”，来源为后续数据包的口径衔接；只登记差异，不升级 M03–M05 验收状态。
- 本包已触碰的条件均值单元格改为表格安全 LaTeX：$E[r_t\mid x_{t-1}]$。不再使用反引号公式、Unicode 帽子或 Unicode 负号；表格中的条件竖线使用 `\mid`。

### 知识层级台账

原来只有一条混名的 `Zero excess-return benchmark`，v2 拆成 active 与 excess 两行，分别说明减本地市场、减匹配无风险。excess 行显式注明只是与后续数据口径对照，不把后续讲次标成由本次通过。

根 `_meta/术语总表.md` 原 v1 拟稿已让 active/excess 两种分母并存，独审接受，本 v2 不改。

## 2. B2：Class 2 数据卡实值

直接读取当前 `course_files_export/class02/class02/`：

- `spy_test_predictions_monthly.csv`：60 行 × 24 列；
- `weight`：48 个 `1.0`、12 个 `0.0`；
- `spy_regression_scorecard.csv.model_mse = 0.002067413867455998`，乘 $10^4$ 为 20.67413867456；
- `three_market_regression_scorecard.csv` 的 `U.S.: SPY`：`test_mse = 0.0020633589210717856`，乘 $10^4$ 为 20.633589210717856。

因此 v2 精确修为：

- `60 × 23` → `60 × 24`；
- 单 SPY 表 `48 个月在市、12 个月空仓`；
- 三市场 timing 表的 `45/15` 保留为另一结果口径，不能移到单 SPY 表；
- 两表差异写为 `MSE × 10^4：三市场汇总 20.63，单 SPY 成绩单 20.67`。

“保存列不等于已经取得可执行阈值、成交和成本契约”的原限制继续保留。

## 3. B3：练习索引只镜像正文，不升级独立配套教学

P09、P10、P10a、P10b、P11 及汇总表统一改成两层状态：

1. `M02 正文对应来源限定解析已核`；
2. `独立练习精读文件尚未创建、未独审，69 份配套教学范围状态不升级`。

来源地位继续分开：

- 旧 p.26／新 p.54 的 C 有课堂确认；
- 新 p.26／p.27 的 D／A 是笔记参考答案，无对应新录音；
- P11 课堂未讲，无教授逐项确认；
- P09 只写“已核材料未见官方书面答案”，Canvas 是否另发仍待核，不作全局否定。

本修复不新建任何练习文件，也不重审正文或其余 69 份教学范围。

## 4. 补充来源修复：不把三个窗口写成四次实际给分

旧 `作业与DDL.md::03` 的 proposed new 仍写“整堂另有 4 次当堂提问给分”，但时间戳不能支持这个次数：P2 `25:28` 与 `26:01` 属同一道标准化问题，P1 `59:24` 也没有被单独认证为实际给分。

v2 保留 P1 `16:20` 的 `might be the only way you get bonus point` 及其不确定语气，改成可核题材／窗口：

- 相关系数与 $R^2$：P1 `58:53`–`01:00:36`；
- 国债 ETF 派息：P2 `11:15`–`12:31`；
- 标准化是否改变 $R^2$：P2 `25:28`–`26:30`。

不再从时间戳数量推断实际奖励次数；正式参与规则仍以 syllabus 口径为准。

## 5. Notion 与 README 当前前提

root 已对正确页面 `3d58310b2596818a9818c855bf1513c0` 完成只改备注／代码路径后的重新 fetch，四项均为 true：备注拟写一致、旧备注原始 suffix 保持、代码路径补 `EF5560_` 前缀、其他 15 属性全部未变。

私有证据：`E:/app-data/codex/review-evidence/vault-notes-review-20261023/notion/ef-m02-readback-20261025.json`，SHA-256 `86dd0ffe02cd05a73b7317ebdccfa026a0cb756d7cb78ce7648c33e46e72a9cb`。

因此旧包 `README.md::01` 的 `Notion-readback` 前提现在已经满足；Git 仍待，不把 Notion 成功写成 Git 完成。

## 6. CAS 与定向复核清单

- 5 个受影响正式依赖的当前 SHA 均仍等于旧包 `source_sha256`；具体值写入 `patches-v2.json`。
- 每条 v2 old 在旧 `base-proposed` 中唯一出现；v2 JSON 记录 base/revised proposed SHA。
- 正式应用前仍须重新读取 5 个源目标并核 SHA；任一变化即停该文件、重新合并。
- 原独审只需定向复核：两种零基准及 LaTeX 显示、60×24／48/12／MSE 缩放、练习索引两层状态、课堂提问题材窗口与不推次数。
- 其余旧包 78 条未触碰补丁不在本次重开范围；本 v2 不构成 Git 授权执行记录。

