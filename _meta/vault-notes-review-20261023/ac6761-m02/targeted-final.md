# AC6761 M02 第二次定向复核（B2 / B6 / B7 / B8）

## 1. 身份与对象

- 原作者／主代理：`/root`
- 修文作者：`/root/scope_classification`
- 原独立审查者／本次定向复核者：`/root/review_ac6761_m02`
- 本次候选：`candidate.md`
- 本次候选 SHA-256：`BC6DE9539606E975E3BE0586B0735DE247D2364F506A4F5FB7CF21B13607DAD9`
- `candidate.md`、`author/proposed.md`、`author/proposed-v2.md` 三者 SHA 一致。
- 本次只复核 B2、B6、B7、B8 及直接受影响入口；B1/B3/B4/B5 未改，不重复审查。旧 `stage-1.md`、`independent-review.md`、`targeted-recheck.md` 均保留未覆盖。

作者提供 `changes-v2.json` 17 个补丁、`source-dispositions-v2.md`、`verification-v2.json` 等定位材料；以下关闭结论来自候选逐行核对、原 DOCX/转录对照和独立 transcript audit，不以作者自查或机器 PASS 代替。

## 2. 逐项结果

### B2｜缩写首用、现金流与 Closing 桥

**状态：仍有 1 个最小残余，未完全关闭。**

已关闭部分：

- §1.2 第 123 行直接展开 `A = Assets（资产） / L = Liabilities（负债） / E = Equity（权益）`。
- 第 124 行直接展开 `AR = Accounts Receivable（应收账款） / AP = Accounts Payable（应付账款）`。
- 第 125 行直接展开 `NI = Net Income（净利润） / TB = Trial Balance（试算表）`，因此后续 881、886、1237–1252、1345、1797–1806 的缩写已有前置。
- §2.8 第 2039 行已改成“统一沿用 §1.2 已定义的缩写”，不再误称这里首次出现。
- §2.8 2043–2049 正确区分 CFO/CFI/CFF 的业务对象，并说明现金流分类不等于收入费用分类；Closing 被限定为报表之后的后续步骤。
- `FF` 的首个正文使用已改回 `FastForward`，后续 `FF16笔` 有完整名称上下文。

仍缺：

- §1.2 第 126 行是三个缩写的真正首次出现，却只写 `CFO = 经营活动现金流 / CFI = 投资活动现金流 / CFF = 筹资活动现金流`，没有写英文全称。现行规则要求缩写首次写全称；§2.8 到 2043–2045 才补 `Cash Flow from Operating / Investing / Financing Activities`，位置仍晚于首次出现和 1806 的首次正文计算。
- 最小修复：第 126 行直接改为：
  - `CFO = Cash Flow from Operating Activities（经营活动现金流）`
  - `CFI = Cash Flow from Investing Activities（投资活动现金流）`
  - `CFF = Cash Flow from Financing Activities（筹资活动现金流）`

### B6｜Quiz 1 原题与课堂行政状态

**状态：已关闭。**

- Quiz T1 已按官方原文改为 `Owner invests $8,000...`，删除静默增加的 `The`。
- 1817–1840 的英文题面与官方 `Quiz 1 with solution.docx` P3/P5–P51 顺序、金额一致。
- 广告费采用官方 150，应付偿还采用官方 350；官方重复的 Service Revenue 表只保留一次并披露。
- 1857–1872 的 12 个 POST 账户余额与官方表一致。
- 1878–1880 已登记 W3 `20:29`–`21:08`：另需 ending balance、答卷会收取作为 participation 证据、本次不评分、首页写姓名和学号；同时明确不能推断用户已经完成或提交，也不能推成 participation 不计分。
- §9.5 第 3250 行同步行政边界，不再声称转录中没有个人作业／提交要求，并保留 W1/W2 未录范围的不确定性。

### B7｜Case 1 的 1,000／4,000 冲突

**状态：已关闭。**

- 第 3243 行明确：作答采用官方 `Case 1 with solution.docx` 的燃油 1,000；后续 21,000、24,000、23,200 的余额链也与 1,000 一致。
- 同行保留 `M02-transcript.txt` `40:23` 文本为 4,000 的事实，并明确本轮未听原音，不能在 ASR 错误、教授口误或其他声学问题之间作选择。
- 3258 的反方视角也沿用同一边界，没有再认证错误成因。

### B8｜拼接式引文、notes payable 低匹配与空档边界

**状态：已关闭。**

- 自测第 7 题原低匹配的 Notes Payable 合并引文已改为中文转述，保留 `51:43`–`51:57` 和 §2.2.2 回链。
- §9.5 课堂练习 2 已删除 `chapter [four?]`、`purchase[d] supplies` 等拼接式直引，只列可确认对象、无法拼成题面的边界和官方 DOCX 后续补齐状态。
- 三处空档已改为“定位活动”，明确空档本身不能证明录音完整；结尾缺失判断不再用课程总时长猜出“至少丢 20 分钟”。
- ASR 样本改为“高风险词映射”，明确未逐处核听原音；`01:16:37` 冲突也不再冒充已确认教授原话。
- 对当前候选重新运行六源 transcript audit：414 个时间戳 0 未匹配、59 条引文 0 未匹配、`quotes_low=0`、`A13=0`、`A14=0`。5 条 A10 均为相邻标题/段落已经给出时间范围的上下文提示，不是无来源课堂主张。

## 3. 同类残余搜索

全文搜索并人工核对以下旧措辞：`purchase[d]`、`chapter [four?]`、`The owner invests`、`这里首次使用`、`空档均已查明`、`没有内容丢失`、`4,000 是 ASR 错误`、`115/315 是 ASR 错误`。候选中已无这些过强或旧版表述。

目前与音频边界相关的保留语句均写成“转录文本与官方书面源冲突；原音未核，不判断错误成因”。Quiz 1、Case 1、`01:16:37` 三处口径一致。

## 4. 未决与下一步

唯一未决是 B2 第 126 行没有在 CFO/CFI/CFF 首次出现时写英文全称。该修复只影响 §1.2 一行；修后检查该行和候选 SHA 即可，无需再次复核其他单元或重新运行完整盲审。

当前候选 SHA-256：`BC6DE9539606E975E3BE0586B0735DE247D2364F506A4F5FB7CF21B13607DAD9`。

独立审查状态：`pending_one_targeted_fix`。

未修改 candidate、vault、Notion 或 Git。
