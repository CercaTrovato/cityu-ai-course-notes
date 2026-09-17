# ASR 专名纠错词典（按课程；执行者每次融合后追加）

> 用法：读转录前先扫一遍本课的表；遇到表里没有的明显错误，**先查讲义确认书面拼写，再追加一行**（转录原文 → 应为，附首次出现的时间戳与讲次）。拿不准的不进表、笔记里标 `[?]`。
> 来源：各笔记 §9.5 的 ASR 样本行（均为真实样本）。中文翻译版一律不用。

## 通用规则

1. 讲义的书面拼写是唯一权威；转录拼写一律服从。
2. 数字、日期、法条编号、百分比以讲义为准；讲义没有的标 `[?]`。
3. 同一个词在一堂课里会被识别成十几种样子（见 AC6761 的 debit / liability），**按语义还原，不按拼写相似度**。
4. ASR 会把教授的中英夹杂转成同音异字；也会把停顿处的半个词接到下一句——引用时用 `[ ]` 补、用 `…` 断。
5. 引用原话时保留转录原词、把纠正放进 `[ ]`：*"we go to the [cash account]"*；整句乱码就不引。

---

## AC6761 · Artificial Intelligence & Accounting（ASR 质量五门课里最差）

| 转录原文 | 应为 | 首见 |
|---|---|---|
| empathy / amplitude / aquaticia / agriculture / average / everything | equity | W2 |
| revenue（在"总资产 − 总负债"语境里） | equity（系统性混淆） | W1 `01:19:14` |
| damage / tennis / David(son) / stereotype / embarrassed / pandem(ic) / MSI / RSI / EBIT | debit(ing) | W2 |
| satisfied / credit tax / Christian | credit（`Christian balance` = equation balance） | W2 |
| test / hash / cache / catch | cash | W2 |
| cash command | cash account | W3 `00:01` |
| fliam / Libra case / livelihood / living space / live nation / likelihood / viabilities | liability / liabilities | W2 |
| tier console / tier count / key account / tea count | T-account | W1 / W2 |
| general letter (of) account / latter count / measure count / leisure | (general) ledger (of accounts) | W1 / W2 |
| Judah entry / June entry / joint entry / children / general entry | journal entry | W2 |
| country receivable / contraceivable / counter receivable / accomplishment level | accounts receivable | W2 |
| counter payable / accountability / account table / accommodate | accounts payable | W2 |
| conception / convection / confection / construction / conduction | transaction | W2 |
| polynomial stomach | common stock | W2 |
| cholesterol parameters | common stock, dividends, revenue and expense | W2 `58:25` |
| crypto account | equipment account | W2 |
| office slides | office supplies | W3 `00:36` |
| Grieving（句首） | [?]（语境为"设备增加"，可能是 "Receiving"） | W3 `00:01` |
| random stems | rent expense | W2 |
| remedies | revenues | W2 |
| splice / spice | supplies | W2 |
| imagery / amateur | inventory | W2 |
| solvent / solo / dissolve | thousand | W2 |
| trial about food | trial balance | W1 |
| counseling | consulting | W2 |
| comf | concepts | W2 |
| hallucinations | illustrations | W2 |
| decar | detailed | W2 |
| less / rate（视频里） | left / right | W2 |
| XPI attacking | XBRL tagging | W1 |
| MBNA | MD&A | W1 |
| Isas / Ifis / IPAS | IFRS | W1 |
| JP / GAHD / DAAB / DAAT / DAHC | GAAP | W1 |
| Rea / RJ / IE / IA / RGM / iron model | REA model | W1 |
| error / Aaron | Enron | W1 |
| lipo / depot | LIFO / FIFO | W1 |
| Lisa | lease | W1 |
| right abuse assets | right-of-use assets | W1 |
| imperative test | impairment test | W1 |
| Pineapple | [?]（某地区名，未还原） | W1 |
| camera（"upload to the camera"） | Canvas | W3 `01:26:11` |
| pancake / 50 UN（选公司的语境） | [?]（可能是 Pinduoduo / S&P 500，需核对） | W3 `01:24:40` |
| “66,000”（库存股回购总额，讲义算法应为 $6×1,000=$6,000） | [?]（数字与算法不符，未还原） | W3 `01:17:09` |
| “800”（少数股东权益例题里 A 的份额） | 80（讲义 p.12 原例：B 净资产 100 的 80%） | W3 `01:19:18` |
| 折旧分录贷方报成 “10,000”（借方已报 1,000） | [?]（按讲义逻辑贷方累计折旧应与借方折旧费用同为 1,000） | W3 `01:03:06` |

## IS5542 · GenAI in Business

| 转录原文 | 应为 | 首见 |
|---|---|---|
| Cloud Code / Cloud Outpost | Claude Code / Claude Opus | L2 |
| Tianwen | Qwen | L2 |
| Tableau E Bench | SWE-bench | L2 |
| Tool (Square) Bench | τ-bench / τ²-bench | L2 |
| Elon style | Elo | L2 |
| Marvel | Marble | L2 |
| PME | Kimi | L2 |
| WorldBench | WildBench | L2 |
| LabBench | LiveBench | L2 |
| artificial generated intelligence | artificial general intelligence | L2 |
| 数字口误：AlexNet "2021"（应 2012）、ImageNet "2012" 启动（讲义 2007）、Mistral "\$1.15"（讲义 \$1.50）、LiveBench "65.96"（讲义 75.96） | 以讲义为准 | L2 |

## IS5113 · AI Ethics and Regulations

| 转录原文 | 应为 | 首见 |
|---|---|---|
| the ontology / dentology | deontology | M02 |
| can / cat / Karen / canteens / Contianism / Cantianism | Kant / Kantianism | M02 |
| beauty | duty | M02 |
| solving / trolling / truest problem | trolley problem | M02 |
| bularity / variety / molarity | morality | M02 |
| polytherm / utilitarism | utilitarianism | M02 |
| Brussels | Russell | M02 |
| quite a dollar calculus | hedonic calculus | M02 |
| peak satisfied | pig satisfied | M02 |
| John's world view | Mill's view | M02 |
| Benthem / Bentam | Bentham | — |
| Colberg / Goldberg | Kohlberg | — |
| categorial imperative | categorical imperative | — |
| Rolls / Ralls | Rawls | — |
| maximum | maxim | — |
| GDP R | GDPR | — |

## IS6400 · Business Data Analytics（技术课：库名 / 指标名易错）

| 转录原文 | 应为 | 首见 |
|---|---|---|
| （待补：pandas / sklearn / R-squared / OLS / multicollinearity 类词以讲义与 notebook 为准） | | W2 |

## EF5560 · Fintech and AI in Finance

| 转录原文 | 应为 | 首见 |
|---|---|---|
| which regression / width regression / weight regression | ridge regression | M03 `44:47`（整堂课反复出现，ASR 几乎没听对过一次） |
| brand | Bryan [Kelly]（教授导师，Gu-Kelly-Xiu 2020 论文作者之一） | M03 `10:23` |
| thumb scrap | term spread | M03 `01:05:54` |
| federal fund way / federal fund[s] way | federal funds rate | M03 `18:12` 起多次 |
| unemployment wave | unemployment rate | M03 `01:05:54` |
| CTO models | [?]（推断为 constant models，未确认） | M03 `36:49` |
| camera（"upload to the camera"） | Canvas | M03 `01:18:56` |
| QP fuel | [?]（未还原，语境为恒指相关指数名） | M03 `01:18:03` |
| funnel three and three | [?]（未还原，语境为"两种不同尺度"） | M03 `01:16:18` |
