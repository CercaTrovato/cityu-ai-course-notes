---
course: AC6761
module: M09
type: practice
status: draft
learning_status: 本次独立教学审查完成（真实 Worksheet 待实作）
official_solution: 未取得官方解答
source: "Case 6.docx（2026-11-05 下载，Word 只读渲染 3 页）"
transcript: none
updated: 2026-11-05
readability_rules: v2
teaching_standard: novice-v1
---

# Case 6 · 从两个利益相关者视角比较 AI 财报分析

本题要你拿一家上市公司的同一份最新年报，选两个关心不同问题的人，再把每个问题交给两个 AI 工具。最后比较四份真实回答，判断数字有没有依据、回答有没有切中对象、哪些地方不能相信。

这是一份学习解析和作答方法示例。公司、报告、工具及真实输出尚未由本人选择或提供，因此下文的提示词与条件式英文答案是参考写法。不能把它们当成已经完成的 Worksheet，也不能把“可能出错”写成“本次已发现错误”。本题原件没有给截止、分值或发送要求；本轮 Canvas 行政核查以任务回执为准。

## 1. 按源页找到任务

预习先读 §2 的两类决策，再走 §3–§5；课中可从下表按页定位；复习用 §6 自测，先说出核查理由再看答案。M09 的相关背景是[[AC6761_Artificial_Intelligence_Accounting/notes/M09-AI财报分析与利益相关者|利益相关者视角]]：同一份报表可以服务不同决策，不能给所有人同一段泛泛的“公司表现良好”。

下表一行对应只读 Word 渲染的一页，页码是本次渲染物理页，不冒称原 DOCX 的固定分页。

| 源页 | 本页新增要求 | 本文位置 |
|---|---|---|
| p.1 | 一家公司、最新年报、五选二的利益相关者、两个 AI | [[#2. p.1 · 先选要作什么决定的人\|§2]] |
| p.2 | 第一人的提示词及两份回答；第二人的提示词开头 | [[#3. p.2 · 一个对象配一个分析问题\|§3]] |
| p.3 | 第二人的两份回答；比较、对象适配、局限三问 | [[#4. p.3 · 保存四份回答再核证据\|§4]]、[[#5. p.3 · 三个讨论问题怎样作答\|§5]] |

### 完整英文原题

下方保留原件所有有字内容及填答字段，去掉不可见零宽字符并统一空白行。自动项目编号按实际页面恢复，原文的单复数和题序保留。

<details><summary>展开 Case 6 完整英文原题与填答字段</summary>
<p>Case 6</p>
<p>Instructions: </p>
<ol>
<li>
<p>Choose a Company &amp; Report:  Select one listed company. Download its
    most recent Annual Report (Form 10-K).</p>
</li>
<li>
<p>Complete the Worksheet:  Follow the steps outlined in the worksheet
    below. You will select stakeholders, formulate prompts, and use AI
    tools to find answers.</p>
</li>
</ol>
<p>Student Worksheet: AI-Powered Stakeholder Analysis</p>
<h4>Step 1: Stakeholder Selection</h4>
<p>Choose two stakeholders from the list below. You will analyze the
company from their unique perspectives.</p>
<ul>
<li>
<p>Investors</p>
</li>
<li>
<p>Creditors</p>
</li>
<li>
<p>Auditors</p>
</li>
<li>
<p>Suppliers</p>
</li>
<li>
<p>Regulators</p>
</li>
</ul>
<p>The Chosen Stakeholders: </p>
<ol>
<li>
<p>_________________________</p>
</li>
<li>
<p>_________________________</p>
</li>
</ol>
<h4>Step 2: AI Tool Selection</h4>
<p>Choose any two AI tools. You will use these to generate insights.</p>
<p>The Chosen AI Tools: </p>
<ol>
<li>
<p>_________________________</p>
</li>
<li>
<p>_________________________</p>
</li>
</ol>
<h4>Step 3: Prompt Formulation &amp; AI Analysis</h4>
<p>For each stakeholder, design one specific, analytical prompt. The
prompts should be based on the company's financial health and require
analysis, not just a simple fact.</p>
<p>Stakeholder 1:  _________________________</p>
<p>Your Prompt: </p>
<p>_________________________</p>
<p>Now, ask your prompt to both of your chosen AI tools.  Copy and Paste
the AI responses below. </p>
<p>AI Tool 1:  _________________________</p>
<p>Response: </p>
<p>_________________________</p>
<p>AI Tool 2:  _________________________</p>
<p>Response: </p>
<p>_________________________</p>
<p>Stakeholder 2:  _________________________</p>
<p>Your Prompt: </p>
<p>_________________________</p>
<p>Now, ask this prompt to both of your chosen AI tools.  Copy and Paste
the AI responses below. </p>
<p>AI Tool 1:  _________________________</p>
<p>Response: </p>
<p>_________________________</p>
<p>AI Tool 2: _________________________</p>
<p>Response: </p>
<p>_________________________</p>
<h4>Step 4: Critical Analysis &amp; Discussion</h4>
<p>Discuss the following questions:</p>
<ol>
<li>
<p>Comparison:  What were the main similarities in the answers provided
    by the two different AI tools? Were they consistent in their data
    and conclusions?</p>
</li>
<li>
<p>Stakeholder Focus:  Did the AI responses adequately address the
    specific concerns of your chosen stakeholders? For example, did the
    answer for a <em>creditor</em> focus on risk and solvency, while the answer
    for an <em>investor</em> focused on growth and profitability?</p>
</li>
<li>
<p>Limitations:  What are the potential limitations of using these AI
    tools for financial analysis? Did you notice any hallucinations,
    outdated information, or superficial analysis?</p>
</li>
</ol>
</details>

## 2. p.1 · 先选要作什么决定的人

### 2.1 选身份时要写出决策

利益相关者（Stakeholder）是会因公司的经营或财务状况受到影响的人。这里不是只写两个身份名称，而是要说清他们准备用年报作什么决定。投资者（Investor）拥有或考虑购买权益，关心投入能否得到回报；债权人（Creditor）已借钱或考虑放贷，先关心到期能否收回本金和利息。

以下是原题五个可选身份的中文读法及参考关注点。原题只要求选两个，后列是笔记补充的分析方向，并非另外五问。

| 原题身份 | 中文 | 一个可分析的决策 |
|---|---|---|
| Investors | 投资者 | 利润增长是否有现金支持，回报能否持续 |
| Creditors | 债权人 | 现金、还款时间和债务是否匹配 |
| Auditors | 审计师 | 哪项报表判断容易出现重大错误、需要什么证据 |
| Suppliers | 供应商 | 是否给公司赊账，付款能力与客户集中风险怎样 |
| Regulators | 监管者 | 披露是否充分、哪些疑点需进一步核查 |

例如，供应商赊销是“先给货、以后收钱”；它会关心客户能否按合同付款。供应商不一定已向公司发放银行贷款，不能把身份直接换成银行。审计师与监管者也不能凭 AI 回答认定公司存在违法或舞弊。

**参考选择：Investor + Creditor。** 这是便于演示的组合，不是替本人选定答案。报告先登记公司全名、财年、报告发布日期、下载日期、官网或法定披露入口、报告页码、币种与单位。题面同时写 listed company 和 Form 10-K；选用其他格式年报时，应先确认教师是否接受，不能默默把两者视为所有上市公司的同一种文件。“最新”按实际作答日核，不把下载较晚的旧财年当最新。

英文参考写法：

> My proposed stakeholders are investors and creditors. Investors need to assess sustainable returns, while creditors need to assess repayment capacity. The final company and report must be identified before the analysis is performed.

## 3. p.2 · 一个对象配一个分析问题

分析性提示词（Analytical prompt）要求从证据作比较或判断。“公司收入是多少？”只提取一个事实；“收入增长时，利润率与经营现金流是否同步改善？”则需要把几个证据连起来。经营现金流（Cash flow from operating activities）是经营活动实际流入减流出的现金，不等于利润。

下面两条是笔记补充的英文提示词模板。方括号必须用真实公司、报告及财年替换，并把相同报告交给两个工具；不要在没有附件时保留“attached report”而假装工具看过文件。

**投资者提示词：**

> Using only [company]'s [fiscal year] annual report [file or official URL], assess whether its reported profit growth appears sustainable. Compare revenue growth, net profit margin and operating cash flow over the comparable years available in the report. Show each source page, input, formula and unit. Explain possible drivers using the report's disclosures, distinguish evidence from hypotheses, and identify missing information. Do not invent unavailable figures.


收入增长率（Revenue growth rate）先求本期比上期多多少，再以上期为比较基准。两期必须属于同一主体、可比期间、同一币种和单位。

$$
g=\frac{R_1-R_0}{R_0}\times100\%
$$

这里 $R_0$ 是上期收入，$R_1$ 是本期收入，$g$ 是相对上期的百分比变化。💡 换个说法（笔记补充）：上期收入 100、本期 120，先算增加 $120-100=20$；再问新增的 20 相当于原来 100 的多少，所以 $g=20/100\times100\%=20\%$。若除以 120，就变成“增量占本期收入多少”，回答了不同问题。

增长率跨两期比较收入；净利润率在同一期把净利润除以收入。若本期收入 120、净利润 12，本期净利润率为 $12/120=10\%$，不是上述 20%。若上期收入为 0，增长率公式会除以零，应报告绝对变化与基期为零，不能硬填百分比；非正基期也不能直接按通常的正基期增长解释。

净利润率（Net profit margin）是净利润除以收入：每 100 元收入最后留下多少利润。收入增长、利润增长和收进现金是三个问题，须分别核，再解释它们的联系。报告没有足够可比年度时让工具列缺口，不补造年份。

**债权人提示词：**

> Using the same report, assess [company]'s ability to meet short-term obligations and service debt. Examine current assets and current liabilities, cash, operating cash flow, interest expense and disclosed debt maturities. State ratio definitions, periods, source pages and units. Identify constraints on cash and distinguish accounting profit from cash available for repayment. Give a conditional conclusion and the further evidence a creditor would need.

流动资产（Current assets）通常是一个营业周期或一年内预计变成现金、出售或耗用的资产；流动负债（Current liabilities）是相应短期内要履行的债务。流动比率（Current ratio）把前者除以后者，但资产中的存货未必能立即卖出收钱，所以不能把一个高比率当成到期还款保证。两人可以看同一个指标，但后续决策不同。


债权人问题里的利息费用（Interest expense）是这段期间为借款等负债承担的利息代价，帮助判断利润对利息的覆盖；现金何时实际付出，还须看现金流和附注。债务到期安排（Debt maturities）列哪些本金何时到期，决定要在哪个日期筹到钱。受限现金（Restricted cash）是用途或提取受到限制的现金；不能把受限部分直接当成可自由还债的钱。

查证据时先在年报目录或全文搜索以下英文，再实际打开对应表与附注。报告名称可能不同，搜索只是定位，AI 给的页码仍须亲自核对。

| 要核的量 | 优先查找位置 | 对当前判断的用途 |
|---|---|---|
| Revenue、Net income | 利润表（Income statement / Statement of operations） | 分别核两期收入与本期净利，重算增长率和利润率 |
| Current assets、Current liabilities、Cash | 资产负债表（Balance sheet / Statement of financial position） | 核同一报告日的短期资产、负债与现金总额 |
| Operating cash flow | 现金流量表（Statement of cash flows）的 Operating activities | 核这段期间经营活动实际净收付现金 |
| Interest expense | 利润表或利息、借款附注（Notes） | 核利息代价及期间，不把所有财务费用自动视为利息 |
| Debt maturities、Restricted cash | 借款、流动性、现金等相关附注（Notes） | 核还款日、受限金额与限制条件 |

同时核报表标题的主体范围。合并报表（Consolidated statements）包括母公司及纳入合并的子公司；母公司单体只列母公司，分子分母不能混用两种范围。金额标为“千元”就先按千元读，不与另一表的“元”直接相除。

💡 证据核验小例（完全虚构，不是某家公司的年报）：假设手里的合并报表注明“2023 年度、单位千元”。资产负债表的现金行是 150；现金附注又写其中 40 仅限指定用途。借款附注说本金 120 在明天到期。先确认三项同一主体、币种与单位，再算自由使用现金至多 $150-40=110$ 千元。

在不计其他收付与融资的假设下，110 比明天到期的 120 少 10 千元。这支持“现有可用现金本身不足以覆盖这笔到期本金”，不能直接推出公司一定违约，因为还没查明天以前的收款和可用融资。即使利润表有净利润，也不能把利润数直接加到这 110 上；若 AI 写“现金 150 足以还 120”，证据链就找到了漏查限制的具体一步。真实作答须填实际表名、页码、原行和附注，不能借用这个虚构例的年份或数字。

两工具比较时保留同一问题、报告版本和资料范围，并记录工具名、模型名（界面确实显示时）、运行日期、是否联网、输入附件和原始回答。记录这些条件有助于判断差异来自数字口径还是输入不同，不保证模型每次回答相同。

## 4. p.3 · 保存四份回答再核证据

先固定一个利益相关者，再分别收集工具 A 和 B；第二位再重复。因此原题总共需要 **2 条提示词、4 份回答**。同一工具换两次对话不能自动算作“两种 AI 工具”。工具实际选择尚未确定，下表是记录结构，空缺应保留“未运行”。

| 回答编号 | 角色与输入 | 当前状态 |
|---|---|---|
| I-A | 投资者问题 → 工具 A | 未运行，无真实回答 |
| I-B | 同一投资者问题 → 工具 B | 未运行，无真实回答 |
| C-A | 债权人问题 → 工具 A | 未运行，无真实回答 |
| C-B | 同一债权人问题 → 工具 B | 未运行，无真实回答 |

核查时从每份回答挑出会改变结论的数字和断言，回年报找到原行。把输入、单位、期间、公式与复算结果写到相邻位置。例如利润率声称 12%，就找同口径净利润和收入，实际做除法。引用存在也不代表引用页支持这句话。

💡 换个说法（笔记补充）：假设收入 100、净利润 12，净利润率是 $12/100=12\%$。两个工具都报 12%，但若它们共同把不同公司的一行当成输入，二者一致仍是同一个错误。正确性来自回原件核对，不来自投票。

原年报和工具原文单独保存。若 AI 写“现金足以还债”，还要查现金是否受限、债务何时到期；年末现金多不等于每个到期日都有钱。只有实际看过相关披露才能写“未见该限制”，不能从工具没有提到推断限制不存在。

## 5. p.3 · 三个讨论问题怎样作答

### 5.1 Comparison：数字与结论分别比较

先答两个工具在哪些数字、计算或结论上一致，再列差异并说明核对结果。不能只写“答案很相似”，也不能用篇幅长短判断质量。

英文参考框架（尚未填真实结果）：

> Both tools reported [verified result] using [matching inputs and definition]. They differed on [specific figure or conclusion]. Rechecking [report page and calculation] supports [finding]. Agreement alone does not establish accuracy.

方括号不能直接交付。没有实际输出时，当前只能回答“相似性与一致性待运行后比较”，不能编一句“两个工具都准确”。

### 5.2 Stakeholder Focus：看回答是否帮助这个人的决定

投资者回答应把利润、增长和可持续回报连起来；债权人回答应把偿债资源、到期时间与风险连起来。若两个角色都只收到“收入增加，前景很好”，它们都没有充分回答各自的问题。

💡 换个说法（笔记补充）：一家公司的收入和利润上涨，但贷款明天到期而现金下月才收回。这个时点差对债权人很关键；利润增长不能直接消除缺口。投资者也不能因此就忽略短期融资风险，只是其问题还包括长期回报。

英文参考：

> The investor response should connect growth and profitability to sustainable returns. The creditor response should connect liquidity, cash restrictions and debt maturities to repayment risk. Whether the actual responses achieved this remains to be checked against the saved outputs.

### 5.3 Limitations：潜在风险与本次发现分开

幻觉（Hallucination）是生成了没有证据支持的数字、引用或断言。过时信息是资料属于较早期间却被当成当前状况。表层分析则是列出比率，未说明它怎样回答当前决策。三者是待检查风险；本次尚无真实工具输出，不能说已经观察到其中任何一项。

英文参考：

> Potential limitations include unsupported figures or citations, outdated information, inconsistent definitions and superficial interpretation. Each claimed error must be tied to a saved response and checked against the report. No tool-specific error has yet been established in this exercise.

作答时用“原回答短摘录 → 报告证据或计算 → 影响哪个结论 → 修改后的有条件结论”的顺序。若只缺资料，写“证据不足”，不把未知写成已证明的错误。

## 6. 下次怎样独立做

本题的顺序是：固定公司和报告 → 选两种决策 → 各写一条分析问题 → 同题问两个工具 → 保存四份原文 → 回报表核数字 → 逐问讨论。最新报告、工具输出、具体比较结论仍待实际作答；本解析不改变本人学习或提交状态。

**改条件自测（笔记补充）：** 两个工具的流动比率分别为 2.0 和 2.5，就能判其中一个算错吗？

<details><summary>参考答案</summary>
<p>不能直接判断。先核它们的公司、报告日、流动资产与流动负债行、币种单位及合并范围是否一致。若同一输入为 800 和 400，正确除法是 2.0；若另一个用了 320 作分母，先追问 320 来自哪里，再判它是不同口径、引用错误还是计算错误。差异提示需要核证据，并不自动告诉你哪一个工具可靠。</p>
<p>English: A disagreement requires checking the inputs and definitions first. With identical inputs of 800 and 400, the current ratio is 2.0; a different denominator must be traced to its source.</p>
</details>

原件：[[AC6761_Artificial_Intelligence_Accounting/course_files_export/Case 6.docx|Case 6.docx]]。答案地位：⚪ 参考作答（笔记推断）；未取得官方解答。本任务暂无正式提交稿。
