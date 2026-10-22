# AC6761 M01 材料 audit 疑点定向复核

- 审查者：`/root/review_ac6761_m01`
- 作者：`/root`
- 候选：`candidate.md`
- 候选 SHA-256：`1cc9fe0b429730dc700cbc9e9675d76584d7b7f7190094cf101760b614fcde14`
- `material-audit.txt` SHA-256：`2be5a5cb6a499bef7f7618a8aad7c87e0118cb14d99c486f1ba20ccea0b18322`
- 复核范围：只核 A5、A10、A13、A14；没有重开全篇教学审查，没有修改候选或 vault。
- 来源：`M01-transcript.txt`、`M02-transcript.txt` 的相邻时间窗口，`AC6761 Outline 2627.docx` 的原句，以及候选对应行。

## 结论

`material-audit.txt` 的整体机器判定为 PASS，但其中不是所有警告都能作为误报关闭。A5 有 1 处把损坏 ASR 改写成未加方括号的逐字引文；A10 有 1 处跨出本小节已声明的转录范围而未就地给时间戳；A13 有 6 处把 ASR 校正词留在引号内而未完整标明校正，其中 XBRL 原音仍未重听；A14 的 2 个位置把上下文推得的 `2 million` 放进受损句的逐字引文。以上属于来源/引文地位阻塞，当前候选不能据此判材料疑点全部关闭。

其余 A10 7 项有相邻引文、答案内时间戳、精确回链或明确“不是教授说的”；A13 的官方及格线来自 Outline/官方目录，不应拿课堂转录窗口匹配，属于 audit 来源并集误报。

## A5：低匹配引文

| 候选位置 | 候选写法 | 实际来源窗口 | 判断 | 最小修复 |
|---|---|---|---|---|
| 181 | `The schedule… if we have any change, I will let you know immediately.`（`14:48`） | M01 `14:48` 原 ASR：`A temporary plan for this course. The schedule is in the future. If we have any change, I will actually know immediately.` | **真实修文**。候选的 `let you know` 很可能是合理还原，但原音未听，不能冒充逐字引文；`The schedule…` 也重排了损坏句 | 改为中文转述：“教授说明这是暂定安排，如有变化会及时通知（M01 `14:48`；ASR 句法损坏，未保留逐字引文）。”不要把 `actually know` 乱码写回正文 |

## A10：教授说/强调但本行无时间戳

| 候选行 | 实际定位 | 判断 | 最小处理 |
|---:|---|---|---|
| 195 | M01 `06:18` 开始问 AI accounting 从 producer 还是 user perspective；本小节开头已声明全部来自 `06:18–12:20` | **误报**：本行是小节内转述，不是逐字引文，范围已覆盖 | 不必改；如想增强定位，可加 `(M01 06:18)`，不是阻塞 |
| 283 | “quality filter”来自 M01 `17:16`：ASR 为 `So you become the quality theater`，上下文是 AI hallucinate ratios/trends/footnotes | **真实定位缺口**：本行在 §2.2.1，而该小节声明范围只到 `12:20`；实际来源在 §2.2.2 的 `17:16` | 加 `(M01 17:16；见 §2.2.2)`，或将这句只放 §2.2.2；不必把 `quality theater` 乱码引回正文 |
| 2010 | 下一块 2012–2016 立即给 M01 `01:53:06` 和 `01:54:08–01:54:55` 两段原话，明确考试使用简化三列格式 | **相邻来源，误报** | 不改 |
| 3493 | §4.4 是速查；§2.6.1 已在 1072–1099 给 `51:43–53:05` 与 `58:24`，其中 `just for your information` 与原转录一致 | **精确回链，误报** | 不改；速查无需重复所有时间戳 |
| 3741 | 这是“🔴 教授明示”的等级定义，不是在声称某个具体教授说法 | **规则行误报** | 不改 |
| 3952 | 题干问教授为何以货币计量引入 REA；答案 3970–3976 就地给 M01 `01:13:05` 原话与第二处证据 | **答案内有来源，误报** | 不改 |
| 4065 | “正负号 requirement”已由 §2.8.3 的 M01 `01:54:30` 原话支撑；余额行也在 `01:55:16` 及 W2 `40:49–41:10` 说明 | **回链证据充分，误报** | 不改 |
| 4423 | 本行明确写 `⚪ ... 推断，不是教授说的`，只是字符串命中“教授说” | **否定语境误报** | 不改 |

## A13：方括号外出现转录窗口未匹配词

| 候选行 | 词 | 实际原文/归属 | 判断 | 最小修复 |
|---:|---|---|---|---|
| 158 | `Failing either component may lead...` | `AC6761 Outline 2627.docx` P45 原文：`Students are required to pass both coursework and examination components to guarantee to pass the course. Failing either component may lead to failure in the course.`；候选明确标“官方课程目录”，不是课堂话语 | **来源并集误报**。这句不应匹配 M01/M02 转录 | 不改引文；材料 audit 若支持来源类型，应将 Outline/目录引文与 transcript 引文分开核 |
| 735 | `capitalized` | M01 `47:46` 原 ASR：`Instead it is the so-called characterized into the balance sheet.`；上下文与 p.24 书面内容都指费用被转成资产，但 ASR 没有逐字出现 `capitalized` | **真实修文**：会计术语校正合理，逐字引文地位不准确 | 引文内写 `Instead it is [capitalized] into the balance sheet.`，并保留时间戳；或把 `capitalized` 移到引文外作笔记术语，不写 `characterized` 乱码 |
| 1508 | `million` | M01 `01:21:09` 原 ASR：`the revenue would be that too many so-called revenue`。相邻 `01:20:00–01:20:43` 明确给资产 3 million、负债 1 million，因此权益应为 2 million；但该受损句没有可核的字面 `2 million` | **真实修文，同时触发 A14** | 不在引号中写 `the revenue would be that 2 million`。改为：“`01:21:09` 把 equity 识别成 revenue；同段由 3 million assets − 1 million liabilities 可算出 2 million equity。数额来自相邻句和等式，不是该受损句的逐字引文。” |
| 1557 | `sale` | M01 `01:23:02` 原 ASR：`credit care... Credit fair... the seller owned credit, no cash.`；稳定信息是卖方、赊销、no cash，术语词本身损坏 | **真实修文** | 改为转述：“教授用卖方赊销说明 on credit，并明确说 `no cash`（M01 `01:23:02`；术语前半句 ASR 损坏）。”如保留整句，引文中将校正术语写 `[credit sale]` |
| 2397 | `affect~` | M02 `06:10` 原 ASR：`liability is not effective. So the number even the same.`；语义是 liability not affected | **真实修文** | 引文写 `liability is not [affected], so the number [is] even the same`，把整个校正词放方括号；或直接中文转述“负债不变” |
| 2772 | `account~` | M02 `44:29–44:50` 原 ASR：`on credit... no cash receipt... count receivable increase... asset increase... revenue increase` | **真实修文** | 将引文校正为 `"[on credit] means no cash receipt from customer. So it's [accounts receivable] increase—[that's an] asset increase. And the revenue increase[s]"`；核心金额/处理由 DOCX 与答案表另证，不依赖 ASR 拼写 |
| 4411 | `XBRL tagging` | M01 `07:32` 原 ASR：`some XPI attacking ... related to IDEA model`；`XBRL tagging` 是强语境校正，但本轮未重听原音 | **真实来源限制** | 不把 `XBRL tagging` 放成无标记逐字引文。写“转录 `07:32` 为 `XPI attacking`；结合会计信息化语境，笔记暂按 `[XBRL tagging?]` 理解，原音未核”，或只保留外部定义并把课堂词标待核 |

## A14：引文数字在窗口中找不到

| 候选行 | 判断 | 实际依据 | 最小修复 |
|---:|---|---|---|
| 1508 | **真实修文**，与 A13 同一问题 | `2 million` 可由相邻 3 million assets − 1 million liabilities 推出，也在前一个损坏句中疑似被 ASR 写作 `2,000,000`；但 `01:21:09` 引号内只有 `too many` | 按 A13 1508 方案，把数字移出逐字引文，明确是上下文/等式结果 |
| 4440 | **真实修文**，是 1508 在待核表的重复 | 此行再次在引号中写 `the revenue would be that 2 million` | 同步改成“`01:21:09` 将 equity 误识为 revenue；2 million 是由同段 3−1 推得，原句 ASR 损坏”，不要保留伪精确引文 |

## 最小修复清单

1. 181 改为带时间戳的中文转述，明确 ASR 损坏，不保留修复后的逐字英文。
2. 283 补 `M01 17:16` 或回链 §2.2.2。
3. 735 的 `capitalized` 整词加方括号，或移出引号。
4. 1508 与 4440 删除引号内的 `2 million` 重构；把数额写成相邻句/等式推得，并只说明 equity→revenue 的 ASR 错。
5. 1557 改为仅引用稳定的 `no cash`，或把 `[credit sale]` 整体标为校正。
6. 2397 把 `[affected]` 整词放入方括号，或改中文转述。
7. 2772 把 `[on credit]`、`[accounts receivable]` 等校正部分完整放入方括号。
8. 4411 将 XBRL 课堂词标为语境校正且原音未核，不再作无标记逐字引文。

## 当前状态

候选的教学机制与数字不因这些警告被推翻；问题集中在“转述/校正”被排成逐字引文，以及跨来源 audit 的误报。上述 8 个位置完成最小修复并同步重复处后，才可关闭本次材料警告。当前材料疑点状态为**待修，不通过**。

