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
| FAPIT (principle) | FATP | M03 `00:01` |
| Thousand Year（剧名，未还原） | [?]（语境为报应正义相关的影视作品，无法确认原名） | M03 `45:33` |
| master of power | master's programme（不确定） | M03 `01:40:16` |
| one dollar out of the fifty-nine or one hundred | 数字疑似错误，未还原（不确定） | M03 `01:17:02` |
| categoric imperative | categorical imperative | M03 `01:54:07` |
| CHET test / CHET-GPT | ChatGPT | M04 `42:44` |
| human noise | [?]（语境"with … and with agentic AI, it can actually do what a physical person can do"，疑似 humanoid 一类误听，拿不准） | M04 `05:26` |
| Boon trust | [?]（语境是复述"信任三要素"总结句，拿不准原词） | M04 `28:17` |
| a bioeconomist | [?]（指代论文作者身份的用词，可能是 behavioral economist 之类，拿不准） | M04 `36:45` |
| employer models | [?]（语境"engage employer models and AI applications"，可能是对 AI/ML models 一类术语的误听，拿不准） | M04 `19:51` |
| Compass / Qantas case / caucus case / accomplished case | COMPAS（Correctional Offender Management Profiling for Alternative Sanctions） | M04 `01:14:50` 起反复出现 |
| Applecart case | Apple Card case | M04 `01:31:02`（shard_3 案例名，本片段边界内发现） |
| Chameleon Airlines | Air Canada | M04 `01:31:02`（shard_3 案例名，本片段边界内发现） |
| CVE / CVEs | CV / CVs（简历） | M04 `59:23` 起反复出现 |
| system tree | [?]（未还原，语境为"算法/决策树"，不确定） | M04 `59:28` |
| soft-based | [?]（未还原，语境疑似 "shortlisted"，不确定） | M04 `59:33` |
| welcomed（"a person who could have been released has now been welcomed"） | [?]（未还原，语境为"被继续拘押"，与 welcomed 字面矛盾，疑似 detained/confined，不确定） | M04 `01:23:51` |
| Freelance Night 2014 | [?]（未还原，语境为 Amazon 2014 案总结句，疑似专名误识别） | M04 `01:05:18` |
| reprimand（"fairness and discriminating in reprimand"） | [?]（未还原，语境为 Amazon 招聘案，疑似 recruitment，未确认） | M04 `01:22:46` |
| re-authentic（"unlikely to be re-authentic"） | reoffend | M04 `01:16:36` |
| re-attempt（"high probability of re-attempt"） | reoffending / recidivism | M04 `01:17:17` |
| political review（"rated as high for political review"） | parole review | M04 `01:18:09` |
| advocates（"Recruiters, advocates, managers and regulators"） | [?]（未还原，语境疑似 candidates，未确认） | M04 `01:07:13` |
| AI Canada | Air Canada | M04（同一堂课内 ASR 时对时错，`01:40:28` 处正确，`01:44:14` 处误作 "AI Canada"） |
| Richmond fare | bereavement fare | M04 `01:42:02` |
| checkbox / check board(s) / tech board(s) | chatbot(s) | M04 `01:47:06`、`01:49:57`、`01:50:14`、`01:50:25` |
| Chez GVD | ChatGPT | M04 `02:08:25` |
| AdvoCard | Apple Card | M04 `02:02:58` |
| entropic | Anthropic | M04 `02:06:14`（教授自我纠正 "Open AI or entropic? Entropic, you know"） |
| expandability | explainability | M04 `01:52:40`、`02:09:38`（全讲反复出现） |
| IT photography firm | IT consulting / consultancy firm | M04 `02:11:13` |
| David Hanson | [?]（疑似知名科技企业家，未核实拼写，不作断言） | M04 `01:33:42` |
| Mofat / Moffat | [?]（Air Canada 案当事人姓名，前后拼写不一致） | M04 `01:40:37` |

## IS6400 · Business Data Analytics（技术课：库名 / 指标名易错；M03 起为本地 Whisper，错法是按发音写成常见词）

| 转录原文 | 应为 | 首见 |
|---|---|---|
| （待补：pandas / sklearn / R-squared / OLS / multicollinearity 类词以讲义与 notebook 为准） | | W2 |
| CPU | CityU（Whisper 按发音） | M03 `00:49` |
| SKU (value/type) | scale (value/type)（不确定，见 s95） | M03 `07:12` 起反复出现 |
| X field | attribute（不确定） | M03 `22:28` |
| quotation analysis | association analysis | M03 `16:19` |
| estimation nominal attributes | asymmetric nominal attributes | M03 `16:19` |
| racial equity | ratio attribute | M03 `22:20` |
| VGA | BDA（Business Data Analytics，不确定） | M03 `05:32` |
| infrastructure data | unstructured data（不确定） | M03 `28:16` |
| SKU needs | skewness | M03 `49:49` |
| channel phase | Chernoff faces | M03 `01:43:53` |
| tennis break | 疑似 ten[?]-minute break | M03 `01:32:50` |
| cross-line experiment | [?]（未还原，语境为准实验/实验方法名） | M03 `55:44` |
| read SZV | read_csv | T03 `01:47:10` |
| PP-DOS | pd（pandas） | T03 `01:47:32` |
| SKU needs / school needs | skewness | T03 `01:46:09`、`01:49:09`、`01:52:40` |
| KUDOS list / QNAS / quotasys | kurtosis | T03 `01:49:54`、`01:52:16`、`01:52:45` |
| LBNB / LVM / LWB | Airbnb | T03 `01:59:19` |
| costiller | scikit-learn（sklearn） | T03 `02:01:47` |
| board transactions | fraud transactions[?] | T03 `01:54:07` |
| Stata Airbnb | so today[,] Airbnb[?] | T03 `02:10:40` |
| capitation | classification[?] | T03 `01:53:43` |
| the 19th percentile | the 90th percentile[?] | T03 `01:57:02` |

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
