---
course: EF5560
module: 1
week: 1
date: 2026-09-03
source: "Lec01_Data_and_Vibe_Coding.pdf（58 页）"
transcript: merged
prerequisites: []
new_concepts: [Vibe Coding, 六步循环, 六项规格, 桌面编码工具, 代码留痕, 简单收益, 对数收益, 复权价, 拆股, 现金股利, 价格指数, 波动率, 回撤, 基准, 期限利差, 组合权重, 多空组合, 美元中性, 配对交易, 主动收益, 交易成本, 另类数据, 预测时钟, 数据泄漏, 前视偏差, 生存者偏差, 冻结样本池, 时点数据, 参考期vs发布日, 归档日, 数据修订, 发布滞后, 五种泄漏路径, 三行手检, 预测变量, 特征表, 横截面, 面板数据, 动量, 均线偏离, 技术指标, 财务比率四件套, 市值加权, 收益预测R2量级, 市场有效性, 随机游走, 反转, 上证综指vs沪深300, 恒生科技指数]
tags: [EF5560, fintech, 金融数据, vibe-coding, 数据泄漏, 时点数据]
status: v1.0
updated: 2026-10-23
mechanism_spec: v1
mechanism_review: passed
mechanism_review_mode: full-independent-20261023
mechanism_content: repaired

readability_rules: v2
teaching_standard: novice-v1

readability_review: passed
teaching_review_run: vault-notes-review-20261023
teaching_review_receipt: _meta/vault-notes-review-20261023/ef5560-m01/review.json
administrative_maintenance: 2026-10-23
administrative_maintenance_receipt: _meta/vault-notes-review-20261023/batch1-sync/admin-ef5560-m01.json
---

# M01 · 金融数据与 Vibe Coding

> **本讲一句话**：这一讲不教你写代码，也不教你建模型——它教你在**让 AI 替你写代码之前**必须先说清楚的那些事，而其中最要命的一件是：**这个数字，在那一天，投资者到底看不看得见？**
> ✅ **既有转录合并材料已于 2026-10-23 重审**：`M01-transcript.txt` 当前 scan 为 `00:01`→`02:15:21`、671 段；无 ≥120 秒时间戳空档。首句像讲课中段残句，故开头可能缺失；结尾有明确下课语。此次未新增音源，也不把文本连续写成音频完整。
> **原始材料**：`Lec01_Data_and_Vibe_Coding.pdf`（58 页）｜**状态**：v1.0（既有讲义 × 转录合并；材料接口重审，教学验收另行）

---

## 0. 三分钟速览

**这一讲讲了什么**

讲义表面上讲"怎么用 Codex 下载金融数据"，但真正的主题只有一个：**信息的时间戳**。金融数据里到处埋着"文件上写的日期"和"投资者真正能看到它的日期"之间的落差——宏观数据发布晚一两周、公司财报晚一到三个月、指数成分股名单是事后才知道的。**只要把这两个日期搞混，回测就会做出漂亮但完全不存在的收益。**

AI 辅助编码（Vibe Coding）在这里的角色是：它把"写代码"这件事的成本降到几乎为零，于是**唯一还需要人做的事，就变成了定义问题和检查证据**。教授对这点毫不含糊——课上说了至少四遍"我不教编程、也不考编程"。

配套的第三条线是**数感**：知道 S&P 500 长期年化 8%、收益预测的 R² 只有 1%、CSI 300 曾经回撤 70%。有了这些量级参照，你才有能力在 AI 吐出一个数字时说"这不对劲"。

**学完你应该能**

1. **写出**一条合格的数据指令：语言与包、数据范围、价格口径、预测时钟、变量公式、输出与检查，六项一个不缺
2. **区分**同一个数字上的三种日期——参考期 / 发布（归档）日 / 可用于预测的日期——并说出为什么财务预测变量在归档日之前必须保持缺失
3. **判断**一个回测有没有前视偏差、生存者偏差，并说出"冻结样本池"具体保护了什么
4. **复述**收益率、复权价、波动率、回撤、基准这几个概念，且每个都能报出一个量级参照数字
5. **看懂**讲义里的 6 段 Python 代码在做什么（不要求会写），并说出每一步的输出应该长什么样

**如果只记三件事**

1. **日期 ≠ 可知日期。** 文件里的 `2026-06-01` 是那个月的"参考期"，不是投资者知道这个数的日子。教授原话：「the mistake I see… 99.9%… that's missing the date.」（🎙️`02:00:05`）
2. **数据比模型重要。** 「Data and data and data. **The predictor[s] are way more useful than model[s].**」（🎙️`24:41`）
3. **AI 写完代码要留痕。** Vibe Coding 最大的隐患不是写错，是错了以后**没有代码可查**（🎙️`01:06:31`，讲义完全没提这条）

**🎙️ 课堂实况**

录音从课程由来与安排开始，前约 20 分钟集中讲课程结构、考试与作业；随后以 AI 工具现场演示串联数据下载、收益口径、基准、时点和泄漏。`01:13:50` 宣布休息，后半段继续讲复权、冻结样本池、宏观/财报发布时间、预测变量和图诊断，`02:13:16` 后布置课后练习与分组，`02:15:21` 明确下课。p.8/11/15/16 等讲义页在现有转录中无可确认对应，状态只能写“未知/无对应”，不能据关键词 0 命中判定教授明确略过并降权。

---

## 1. 开始之前 · 知识衔接

### 1.1 你已经有的

本讲是全课起点。读者只需会四则运算、简单代数和百分数；本篇不假定会金融、统计、机器学习或 Python。[[EF5560_Fintech_and_AI_in_Finance/_meta/知识层级台账#L0 · 入场基线|L0 台账]]只用于登记依赖，不能代替正文解释。

为读懂后面的任务，先认三个角色：**预测变量（predictor）**是决策前已经知道的输入，**目标（target）**是之后才发生、要预测的结果；**训练集（training set）**用来定规则，**测试集（test set）**留到最后，只检验一次。例：用前 8 个月的动量定规则，再用后 2 个月检验；若看完后 2 个月再换变量，它们就不再是独立测试。

统计和代码也从当前任务所需的最小动作讲起：均值是平均水平，标准差描述一组数围绕均值的起伏；R²、散点图和箱线图在首次承担判断时再就地展开。Python 代码只要求能追踪“输入表 → 选列 → 调函数 → 得到新表/序列”，不要求自己从空白写程序。

### 1.2 本讲全新引入的概念

| 概念 | English | 展开于 |
|---|---|---|
| Vibe Coding · 六步循环 · 六项规格 | Vibe Coding / Six-Step Procedure / Six Specifications | §2.2 |
| 桌面编码工具 · 权限分级 · 代码留痕 | Desktop coding tool / Permission levels / Code backup | §2.2 |
| 简单收益 · 对数收益 | Simple return / Log return | §2.3 |
| 复权价 · 拆股 · 现金股利 · 价格指数 | Adjusted close / Stock split / Cash dividend / Price index | §2.3 |
| 波动率 · 回撤 · 基准 · 期限利差 | Volatility / Drawdown / Benchmark / Term spread | §2.3、§2.6、§2.9 |
| 预测时钟 · 数据泄漏 · 前视偏差 | Forecast clock / Data leakage / Look-ahead bias | §2.5 |
| 参考期 vs 发布日 · 归档日 · 数据修订 · 发布滞后 | Reference period vs release date / Filing date / Revision / Release lag | §2.5、§2.6 |
| 生存者偏差 · 冻结样本池 | Survivorship bias / Frozen universe | §2.8 |
| 预测变量 · 特征表 · 横截面 · 面板数据 | Predictor / Feature table / Cross-section / Panel | §2.7 |
| 动量 · 均线偏离 · 技术指标 · 财务比率四件套 | Momentum / MA gap / Technical indicator / Accounting ratios | §2.7 |
| 五种泄漏路径 · 三行手检 | Five leakage channels / Three-row check | §2.7 |
| 市场有效性 · 随机游走 · 反转 · R² 量级 | Market efficiency / Random walk / Reversal / R² magnitude | §2.9 |
| 多空组合 · 美元中性 · 配对交易 | Long-short / Dollar-neutral / Pairs trade | §2.10（❓ 现有转录无可确认对应） |

### 1.3 为什么这一讲放在这里 · 重排说明

这是第 1 讲，没有"承接"，只有"铺路"。它铺的路极其具体：

- **§2.5–2.7（时点纪律与特征表）→ 直接是 M02 的输入。** M02 要问"这个变量能不能改善预测"，前提是这个变量本身没作弊。讲义 p.44 明说：「Write both down now, **because Class 3 re-estimates them and the definitions must not move.**」
- **§2.3（数感）→ 是整个 ML 板块的验收标准。** M02 的样本外 R²、M05 的组合业绩，全靠"这个数合不合理"来判断。
- **§2.9（用图诊断）→ 是 M02 第一页的起点。** 讲义 p.58：「We move from constructing and checking data to asking whether a variable improves a return forecast.」

**重排说明**

讲义原顺序是六段拼接：

> A 课程定位与考核（p.1–7）→ **B PDD-JD 配对交易案例 + 六步法（p.8–16）** → C 市场数据下载与检查（p.17–25）→ D 宏观与公司财务（p.26–41）→ E 无泄漏构造预测变量（p.42–48）→ F 用图诊断与收尾（p.49–58）

本笔记调整为：

> §2.1 定位（A）→ §2.2 Vibe Coding 方法论（从 B 里抽出 p.9/10/12，将配对案例后移至 §2.10）→ §2.3 金融词汇与数感（从 C、F 里抽出）→ §2.4 下载与检查（C）→ **§2.5 预测时钟（把散在 D、E 里的时点内容合并）** → §2.6 宏观与财务的三种时点（D）→ §2.7 造预测变量（E）→ §2.8 冻结样本池（把 p.24–25 从 C 里抽出来单独成节）→ §2.9 用图诊断（F）→ **§2.10 配对交易（B，先补足收益与时点依赖，再读案例）** → §2.11 工作坊与失败诊断表（p.54 转课后尝试；p.55 无逐页课堂对应）→ §2.12 收尾

**三个调整的理由**：

1. **把 PDD-JD 配对交易（p.8、11、15、16 共 4 页）后移到 §2.10。** 先学收益、预测时钟和组合权重，再把这些动作合到案例中，初学者才容易复做。现有转录没有可确认对应；关键词未命中不能证明教授明确略过，因此不据此降低复习优先级。
2. **把"预测时钟"提取成独立的 §2.5，放在所有数据类型之前。** 讲义把时点问题拆散在 p.27、33、39–40、43、47、48，读者要读到第 43 页才看到统一的图示。但这是本讲**唯一真正的主题**，先讲清楚，后面每种数据只是它的一个实例。
3. **把 p.24–25（冻结样本池 + 选择题）单独成 §2.8。** 因为教授在这里明说了「**this is one of the exam questions I design**」（🎙️`01:27:47`）——这是全讲可信度最高的考点，不能埋在"市场数据检查"里。

小节 ↔ 页码的完整对应见 [[#8. 讲义页码映射|§8]]。

---

## 2. 正文

### 2.1 这门课要你学什么（讲义 p.2–7）

#### 2.1.1 两块内容，一个学期

讲义 p.2 给了一张分层表，说明"AI 在金融里能干什么"以及本课各块讲到哪：

| 层 | 典型 AI 应用 | EF5560 讲在哪 |
|---|---|---|
| **信息与文本** | 行情、会计、宏观、交易、申报、新闻、规则数据 | Class 1 的数据纪律；Class 12 的 LLM 文本应用 |
| **预测** | 收益、风险、违约、欺诈、需求、客户行为 | **核心**：Classes 2–4 的回归与线性/非线性 ML |
| **决策与产品** | 组合、定价、额度、支付、借贷、投顾、保险 | Class 5 的投资决策；Classes 10–12 的产品案例 |
| **基础设施与控制** | API、云、区块链、网络安全、RegTech、模型治理 | Classes 6–12 的机制与控制 |

> **Part I：ML in Finance（Classes 1–5）** ｜ **Part II：FinTech（Classes 6–12）**
> 讲义原话：「The two parts share a financial setting but address different questions.」（p.2）

**🎙️ 课堂补充**：教授解释了为什么今年把两部分**调换了顺序**——去年先讲 FinTech 公司案例，学生下课后普遍问"我到底学到了什么"，因为案例课没有"做完一道题"的踏实感；今年改成先讲有明确操作的投资部分（`06:37`）。

他还说明本课的由来：**AIB 项目 2025 年成立，请 EF 系为其新开一门课，他去年才开始建，今年幻灯片全部推倒重做，而且是用 AI 重做的**（`00:03`–`00:38`）。

→ 边界：这支持今年课件重做，不能推出所有往届资料都不存在，也不能据此预测明年的安排。

**所以呢**：知道了这门课讲什么、怎么分两部分，接下来三节继续把"这门课"本身的背景交代完——一个金融 AI 产品还需要哪些层面、两条建造 AI 的路线、以及最终怎么给你打分。

#### 2.1.2 一个金融 AI 产品需要的不只是模型（讲义 p.3）

上一节的分层表说的是"这门课讲什么"；讲义 p.3 换了一个角度，说的是"做成一个真正能上线的金融 AI 产品，除了模型准不准，还要想清楚哪几件事"——很多学生（以及很多真实项目）只顾着调模型，结果模型很好用却从没改变过任何一个实际决策。讲义把一个产品拆成四层，每层配一个该问的问题，以及不问会有什么后果：

| 层 | 设计问题 | 忽略它会怎样 |
|---|---|---|
| 数据与获取 | 信息是否及时、时点正确、被许可、模型可用？ | 泄漏、输入过期、或数据根本没法上线 |
| 模型与基准 | 任务是预测还是生成？必须打败哪个简单替代方案？ | 输出看着合理，但没有可衡量的决策价值 |
| 决策流程与分发 | 用户拿到的是 API、副驾、自动规则、还是人工复核建议？ | 模型很强，却从没改变过任何一个金融决策 |
| 控制与问责 | 谁验证、谁监控、谁保障安全、谁能覆盖、谁审计？ | 模型风险、责任不清、代价高昂的运营事故 |

> **Keep in mind（讲义 p.3）**：「Financial value comes from the full system: data, model, decision process, distribution, and controls.」

**❓ 课堂覆盖未知**：现有转录无可确认对应，不能由此判定明确略过。这张表仍须完整学习；它可作为第二板块 FinTech 公司案例的分析骨架（案例报告占 30%）。

**所以呢**：知道了"一个产品需要哪几层"，下一个自然的问题是——**由谁来控制这些层**？这决定了两条建造 AI 路线（下一节）的分野。

#### 2.1.3 两种建造与分发 AI 的路线（讲义 p.4）

讲义用两个人做对照（**肖像是 AI 生成的编辑插图，不是照片**，讲义自己标注了）：

| | **Sam Altman**（CEO, OpenAI） | **梁文锋 Liang Wenfeng**（DeepSeek 创始人；幻方 High-Flyer 联合创始人） |
|---|---|---|
| 路线 | 把前沿研究接到消费产品、开发者 API、企业部署上，跑在自建的中心化基础设施上 | 从量化研究转向基础模型，把 DeepSeek-R1 的代码与权重以 **MIT License** 开源 |
| 金融用户该问 | 模型质量与分发能带来多少价值？产品对算力、定价、访问权、治理的依赖有多深？ | 开放权重与工程效率能带来多少价值？谁来管商业化、运营和模型风险？ |

> **Keep in mind（讲义 p.4）**：「**Which layer a firm controls decides what it can charge for.** Ask that before asking whose model is better.」

**🎙️ 课堂补充（转录 `32:24`–`34:19`、`01:03:33`）**——这段讲义只给了框架，教授给了实操结论：

- **对本课的作业来说，中国 AI 和美国 AI 没有区别**：「we are really working on very simple problems… the [question] is which one is cheaper.」
- **成本**：ChatGPT Pro **\$200/月**、Claude Max **\$200/月**（教授自己两个都买了，走科研经费）。**建议学生用便宜的**：DeepSeek、通义千问（Qwen）、Kimi 等开源系；豆包（Doubao）是闭源。
- **CityU 已为全校订阅 ChatGPT**，可以直接用（`01:03:33`）。
- 教授对"中国厂商为什么开源"的解读：**芯片短缺**。开源后模型可以部署在腾讯、阿里等平台上，把自家有限的算力留给 AGI 研发（`37:04`）。⚪ 这是他的个人判断，不是课程内容。

**所以呢**：无论选哪条路线，对本课的作业来说结论是一样的——重要的不是哪个模型更强，而是**哪个更便宜、你能不能用**（§2.2.1 还会回到这一点）。

#### 2.1.4 考核（讲义 p.5）

这门课怎么打分，直接决定你该把时间花在哪。讲义 p.5 给出五项加总到 100% 的成绩构成，其中光是期末考试就占了将近一半：

| 考核项 | 权重 |
|---|---|
| FinTech 公司案例报告 | 10% |
| 录像展示 | 20% |
| ML 投资作业 | 20% |
| 参与与课堂表现 | 10% |
| **两小时期末考** | **40%** |

完整规则、DDL、以及官方目录补充的 GenAI 政策见 [[EF5560_Fintech_and_AI_in_Finance/_meta/作业与DDL|作业与DDL]] 和 [[EF5560_Fintech_and_AI_in_Finance/_prep/课程前置资料|课程前置资料]]。

**🎙️ 三条讲义没写的关键信息**：
1. **期末是闭卷手写、禁用一切电子设备**，「I might allow you for **one page for hand written cheat sheet**」（`10:20`）——单页手写小抄可能被允许，待 Canvas 确认。
2. **点名是真的会扣分**：每人起始 5/10 分；答对或推理合理 +1；答错不扣；**被点到人不在 −1**；提前一天请假不扣（`14:43`–`15:37`）。
3. **教授取消了传统作业**，因为「if I give you assignment, everyone [will] get 100」——他女儿用豆包做作业让他意识到这点（`09:37`）。所以分数集中在考试和小组产出上。

**所以呢**：了解了这门课教什么、怎么打分，接下来正式进入本讲的第一项技能——怎么让 AI 帮你写代码，同时不让它替你做本该由你自己做的判断，也就是 Vibe Coding。

---

### 2.2 Vibe Coding：把"写代码"外包，把"定义问题"留下

#### 2.2.1 是什么

以前想下载一份股票数据，你得自己会写 Python：知道去哪装包、怎么调用下载函数、报错了怎么查文档。现在你只需要用一句人话把要求说清楚——"帮我下载苹果最近三年的周收盘价"——AI 就能把代码写出来、跑给你看。**这种"用自然语言指挥 AI 写代码、而不是自己动手敲"的工作方式，就是 Vibe Coding（氛围编码 / AI 辅助编码）。** 严谨地说：

**Vibe Coding（AI 辅助编码）** = 用自然语言把任务描述清楚 → 让 AI 助手写并**运行**一段小 Python 程序 → 检查结果 → 修改指令 → 直到输出通过你事先写好的检查项。

讲义 p.7 把分工写死了：

| **AI 能帮你** | **你仍然要自己决定** |
|---|---|
| 把金融任务翻译成可执行的 Python | 目标、样本、变量、时点 |
| 解释你看不懂的语法 | 每个日期上**什么是可观测的** |
| 报错后修改代码 | 输出在经济上**说不说得通** |

> **Keep in mind（讲义 p.7）**：「Give an instruction → run Python → inspect → revise → save.」

**为什么需要它**

因为编程技能会**折旧**，而金融判断不会。

**🎙️ 教授的原话最有说服力（`39:22`–`41:36`）**：
> 「In the past I spent two or three lectures teaching Python… **Right now I want to spend zero.** Many of you [will] forget [it] after your master study, because you don't use [it]. And I can tell you, I also forget… I'm 48 years old now.
> **If you believe that you are the top 10%, 5% of the student[s], I highly suggest you to master coding. If you believe you are an average student, I would suggest you learn vibe coding**, because you might not use this every day.」

**💡 换个说法（笔记补充）**：Vibe Coding 相当于把程序员从"打字员"变成"审稿人"。你不再需要记住 `df.resample("W-FRI").last()` 这串字符，但你必须知道**"按周五重采样"这个决定本身对不对**——因为 AI 不会替你判断该用周五还是周三。

**所以呢**：知道了 Vibe Coding 是"你审稿、AI 打字"，下一个问题是这个"审稿"具体分几步走——讲义把它画成了一个循环。

#### 2.2.2 六步循环（讲义 p.9）

2.2.1 把 Vibe Coding 概括成"给指令→跑→查→改→存"五个动作，讲义 p.9 把它拆成更具体的六步，而且画成一个**循环**而不是一条直线——因为第 6 步"修正保存"之后，往往会带着新发现的问题回到第 1 步重新定义，一次任务经常要转好几圈这个环：

```mermaid
flowchart LR
    A["1. 定义<br/>样本与变量"] --> B["2. 给出<br/>精确指令"]
    B --> C["3. 先原样跑<br/>不要急着改代码"]
    C --> D["4. 检查<br/>数据行与图"]
    D --> E["5. 挑战<br/>时点与逻辑"]
    E --> F["6. 修正、保存<br/>并记录"]
    F --> A
```

六步依次是：

①先把样本、变量定义清楚，

②翻译成一条精确指令（六项规格见 §2.2.3），

③先让 AI**原样跑一次、不要手痒去改代码**，

④检查跑出来的数据行和图，

⑤专挑时点和逻辑的毛病（本讲后半的重点），

⑥确认没问题后修正、保存、并记录这次改了什么。

> 讲义 p.9：「The loop is complete only when the output passes **explicit checks**.」
> ◑ **课堂一句带过**：转录 `46:02` 只有一句「This is the six[-]step for [vibe] coding」，随后就切到实操演示了。但这个环里的第 3 步（**先不要动手改代码**）是有讲究的：先原样运行，你才能知道 AI 的原始理解是什么。

**所以呢**：六步循环的第 2 步是"给出精确指令"，但"精确"到底要写清哪几件事？讲义把它拆成了六项规格。

#### 2.2.3 六项规格：一条合格指令必须写清什么（讲义 p.10）★

2.2.1 说"你仍然要自己决定目标、样本、变量、时点"，但这句话太抽象——具体要写清哪几件事，AI 才不会自作主张地帮你做决定？讲义 p.10 给出一张清单，把一条合格指令拆成六项，每项写漏了会出什么问题都列在最后一列，其中第 4 项（预测时钟）是全讲最容易被忽视、也最致命的一项：

| # | 规格 | 具体要写什么 | 写漏了会怎样 |
|---|---|---|---|
| 1 | **语言与包** | R + `quantmod`，或 Python + `yfinance` + `pandas` | AI 换一个包，结果口径就变了 |
| 2 | **数据** | 代码（ticker）、来源、起始日、结束日、频率 | 拿到的样本区间和你想的不一样 |
| 3 | **价格口径** | 复权（adjusted）还是不复权 | 拆股会被当成暴跌（见 §2.3.3） |
| 4 | **预测时钟** | 信号在什么时候形成、目标是哪一期的收益 | **最致命**——直接产生数据泄漏 |
| 5 | **预测变量** | 精确公式 + 滚动窗口长度 | 同名不同算法，M03 复现不出来 |
| 6 | **输出与检查** | CSV 文件、图、维度、缺失计数、样本行 | 你没有可核对的证据 |

**⚠️ 常见误解**
- ❌「指令写得越详细越啰嗦」→ 恰恰相反。第 6 项（**要求 AI 自己报告行数、首末日期、缺失数**）是成本最低、收益最高的一条。讲义 p.14 的例子就是把它写进指令里的：要求返回「157 weekly prices；156 non-missing returns；a saved, date-sorted file」。
- ❌「AI 报了错才需要检查」→ **最危险的失败是不报错的**。讲义 p.55 把它列成第 6 类失败：「**Logic：it runs, but computes something you did not specify.**」

**所以呢**：六项规格是纸面清单；下面三条是教授在课堂上才补的、清单里没写但动手时立刻用得上的操作细节。

#### 2.2.4 🎙️ 三条只有课堂上才有的操作要点

这三条讲义**完全没有**，但对实际动手非常关键。

**① 必须用"桌面编码工具"，不是聊天机器人（`43:06`–`43:48`）**
> 「**I'm not asking you to use the chatbot.** You are going to download the desktop coding tool… like the Codex I have here, like the Claude Code I have here… **then they can access the local computer.**」

区别在于：聊天机器人只能把代码"打印"给你，桌面工具能**读写你的本地文件、真的执行代码、看到真实报错**。这才使得"运行 → 检查 → 修正"的循环成立。教授还提到豆包也有类似工具。

**② 权限要分级给，从最保守的开始（`43:48`–`45:15`）**
> 「for [Claude], they will have like auto / manual / accept edits / plan / bypass everything… **My suggestion is you try the simple one first. Don't [give] everything to AI**, because… they might send email [on] behalf of you. They might send your money to someone else.」

**③ ★ 每次都要把代码存下来（`01:06:31`–`01:07:31`）**
> 「every time you ask your AI to use the vibe coding for you, **please also save the file for the code**. This is very different [from] manual coding… for vibe coding, if you don't really have the code, then **you don't know where to find the mistake**. So please have a backup for the code… every time you create a figure, have a backup to save all the codes.」

**💡 换个说法（笔记补充）**：手工编程时代码天然留在你的工程里；Vibe Coding 时代码是"一次性"的对话产物，跑完就没了。于是你手上只剩一张图和一个数字，**却无法回答"这个数是怎么算出来的"**——而这恰恰是本课要求的可复现性（syllabus：「Empirical work must preserve the data timing and transformation steps needed to reproduce the reported result.」）。
**操作建议**：给每张进入报告的图配一个 `.py` 文件同名保存。ML 投资作业明确要求交「reproducible code package」，这条不是可选项。

**⚠️ 常见误解**：❌「AI 生成的代码不用管，反正能跑」→ ML 投资作业的评分里**明确包含可复现的代码包**，没有代码等于交不了。

**所以呢**：Vibe Coding 的流程讲完了。但六项规格里第 2、3、5 项（数据、价格口径、预测变量）全都要用到金融词汇——收益率、复权价、指数——下一节从零开始把它们讲清楚。

---

### 2.3 金融数据的最小词汇表（读者零基础，本节从头讲）

讲义把这些概念散在 p.13、19、22 和图注里，本节合并讲清。**每个概念都配一个量级参照**——这是教授说的本课第一优先级（🎙️`02:12:27`）。

#### 2.3.1 收益率：简单收益与对数收益

**是什么**

讲义和课程数据里的"收益率"其实有两种算法，数值上很接近，但混着用会导致后面的累计收益算错（真实踩坑案例见 §9.3 ①）。最直觉的一种：上周五收盘价 100 元，这周五涨到 110 元，"涨了 10%"——这是**简单收益**。金融里还有另一种写法，同一个例子算出来是 9.53%，不完全一样但很接近，叫**对数收益**。两者的差距只有在涨跌幅很大时才会明显拉开。

严谨地说：

- **简单收益（simple return）**：$r_t = P_t / P_{t-1} - 1$
- **对数收益（log return）**：$g_t = \ln(P_t / P_{t-1}) = \ln(1+r_t)$

| 符号 | 是什么 | 已知/待求 |
|---|---|---|
| $P_t$ | 第 $t$ 期（如某一周）的价格 | 已知：下载到的价格序列 |
| $P_{t-1}$ | 上一期的价格 | 已知 |
| $r_t$ | 第 $t$ 期的收益率 | 待求 |

**代入数字**：价格从 100 涨到 110——简单收益 $r_t = 110/100 - 1 = 10\%$；对数收益 $g_t = \ln(1.1) \approx 9.53\%$。

**先把 $\ln$ 和 $\exp$ 当作一对记账工具**

输入对象是正的资金倍数 $u$。

自然对数 $g=\ln u$ 是满足 $e^g=u$ 的指数，其中 $e\approx2.718$。

反向运算 $\exp(g)=e^g$ 把指数还原成资金倍数。

比如 $\ln(1.1)\approx0.09531$，再算 $\exp(0.09531)\approx1.1$。

因此，正数相乘时，$\ln(1.10\times0.90)=\ln(1.10)+\ln(0.90)$；$\exp$ 再把相加后的结果还原。这里不需要微积分，只需认清输入是正资金倍数、输出是指数记账值。

**为什么需要两个**
- **简单收益能跨资产相加**：组合收益 $= \sum_i w_i \times r_i$（$w_i$ 是第 $i$ 个资产的权重，$r_i$ 是它的简单收益）。§2.10 的多空组合就必须用它。
- **对数收益能跨时间相加**：累计对数收益 $G=\sum_t g_t$；累计简单收益 $R=\exp(G)-1$，净值倍数 $\exp(G)$。$N$ 个价格只有 $N-1$ 个相邻收益。画长期走势图、算波动率时用它更方便。
- 收益小的时候两者几乎相等（1% 时差 0.005%）；收益大的时候差很多（+50% 时简单 0.50 vs 对数 0.405）。

**课件原例**（讲义 p.19）
> 「From the checked weekly adjusted prices, calculate **r_t = P_t / P_{t−1} − 1**.」——讲义**明文只给了简单收益的公式**。

**🎙️ 课堂补充（`46:42`）**
> 「Probably you don't know that there are **many types of price**, [and] many types of returns. If you don't know those names… if you just type price and return, they will use the [standard] one.」
> → 教授承认这是个坑，并给了实用建议：**不确定时就说"简单收益"，AI 默认给的也是它**。

**⚠️ 常见误解（★ 本讲最容易被坑的一条）**
❌「课程数据集里的收益都是简单收益」——**错**。实测课程给的 8 个 CSV：

| 文件 | 频率 | 实际口径 |
|---|---|---|
| `aapl_weekly_prices_returns_156w.csv` | 周 | **简单收益** ✅ 与 p.19 公式一致 |
| `pdd_jd_pair_example_156w.csv` | 周 | **简单收益** ✅ |
| `market_index_returns_240m.csv` | 月 | **对数收益** ⚠️ |
| `spy_monthly_features_240m.csv` | 月 | **对数收益** ⚠️ |
| `csi300_macro_panel.csv` | 月 | **对数收益** ⚠️ |

（数值验证见 [[EF5560_Fintech_and_AI_in_Finance/_meta/数据集卡片|数据集卡片]]。复算差异约为 $10^{-15}$，属于浮点表示容差内一致，不应理解为机器输出了数学上的精确零；`L01_01` 用 $\exp(\sum r)$ 与价格净值核对，`L01_03` 用 $\prod(1+r)$ 与周频净值核对，两种口径分别验过。）
讲义 p.20/21 的图注确实写了 "monthly **log** returns"，所以图是自洽的；但**唯一给出的公式（p.19）是简单收益**。**做作业时必须自己确认口径**，尤其是把月度收益复利加总成累计业绩的时候。

**与其他概念的关系**：收益率是 §2.7 特征表里的目标变量（`y`），也是 §2.3.4 波动率的输入。

> 📁 **代码**：[`code/L01_data/01_return_conventions.py`](../code/L01_data/01_return_conventions.py) —— 同一份 S&P 500 月度数据，对数收益正确累加 = 价格净值 5.87×；误当简单收益复利只剩 4.59×（`L01_01`）
> 💡 原辅助图证据文件保留；本轮正文用可编辑表格与流程图解释机制。

**所以呢**：算收益率要用哪个价格，本身还有讲究——公司拆股、发股利都会让报价"跳一下"，下一节看这个跳动该怎么处理。

#### 2.3.1a 把收益、复利、年化、风险与回撤走成一条线（💡 笔记补充）

这里有两条不同的计算链。第一条逐期更新钱和高点；第二条在读完全部收益以后求平均、波动与年化。

| 量 | 是什么 | 单位/频率 | 何时得到 | 三月例 |
|---|---|---|---|---|
| $V_t$ | 当前账户金额 | 元/月末 | 本月结算后 | 108.9 |
| $H_t$ | 到本月为止最高金额 | 元/月末 | 更新当前财富后 | 110 |
| $D_t$ | 当前金额相对高点的变化 | 无单位比例 | 当前财富/峰值后 | −1% |
| $s$ | 三个月简单收益起伏 | 月收益标准差 | 三期读完后 | 0.115470054 |
| $\bar d$ | 平均超出现金的收益 | 月收益 | 同期扣现金后 | 0.023333333 |

下方控制图的回边只更新下一期金额。月1用100元乘1.1得到110，并更新峰值110；月2用110乘0.9得到99，峰值仍110，所以回撤−10%；月3到108.9，仍没越过峰值。读完三期才输出终值、最大回撤和其他统计。

箭头是时间/控制推进，不代表财富上涨；“更新峰值”取旧峰值与当前财富的较大者。文字替代：钱逐期连乘，峰值只升不降，回撤按当前峰值作分母。年化只换口径，不让三个月变成长期可靠预测。

<details><summary>读图自测：末期回撤−1%，为何最大回撤仍为−10%？</summary>

最大回撤要记住所有状态中最负的值。月2曾跌到99/110−1=−10%；最后恢复一些，不会把那次经历从路径删除。

</details>

现在要回答一个具体问题：同一笔钱涨、跌、再涨，期末到底剩多少？只报平均收益会遗漏资金路径。本例无外部现金流、无税费，初始权益 100 元，三个完整月末为 110、99、108.9 元。输入是 4 个价格，输出是 3 个收益、累计增长、年化增长和路径风险。

| 状态 | 价格/净值 | 简单收益 $r$ | 对数收益 $g$ | 至今峰值 $H$ | 回撤 $D=P/H-1$ |
|---|---:|---:|---:|---:|---:|
| 基期 | 100 | — | — | 100 | 0 |
| 月 1 | 110 | 10% | 0.095310180 | 110 | 0 |
| 月 2 | 99 | −10% | −0.105360516 | 110 | −10% |
| 月 3 | 108.9 | 10% | 0.095310180 | 110 | −1% |

**复利、峰值与回撤**

步骤 1 从相邻价作比，得到每期资金乘数 $1+r$；步骤 2 逐期更新 $V_t=V_{t-1}(1+r_t)$，到 108.9 即读完三期、停止；步骤 3 每期更新峰值 $H_t=max(H_{t-1},V_t)$，再算回撤。最大回撤取所有 $D_t$ 中最小值，故为 −10%，而不是期末的 −1%。回撤归 0 是当前恢复历史峰值，不要求过去 12 个月每期盈利。

复利依据是相邻比值约分：$\prod_{t=1}^n(P_t/P_{t-1})=P_n/P_0$。取 log 后乘法变加法，所以 $G=\sum g_t=0.085259844$，$R=\exp(G)-1=8.9\%$。简单收益直接相加是 10%，没有反映第二个月在 110 元上损失 11 元。

几何平均每月收益 $\bar r_{\rm geo}=(1.089)^{1/3}-1$，意思是找一个固定月增长率，连乘三次恰好到同一终点。年化复合增长率（CAGR）因此为 $1.089^{12/3}-1=40.640862\%$；这里三个完整月的数值很短，只是演算，不能当稳定年回报预测。算术平均 $\bar r=(0.1-0.1+0.1)/3=3.333333\%$，线性年化为 40%，与 CAGR 不同。

**样本波动与风险年化**

风险计算使用同一组三个月的简单收益，按以下步骤求样本波动：

1. 每项减去均值，偏差为 $0.0666667,-0.1333333,0.0666667$。
2. 平方后相加，得到 $0.0266667$。
3. 除以 $n-1$，得到样本方差 $s^2=0.0133333$。
4. 开方，得到样本标准差 $s=0.115470054$。

这里计算的是收益的标准差。三期偏差相加必须等于 0；知道前两项后，最后一项已被均值约束决定，所以只有 $n-1$ 个可自由变化的偏差，分母用 $n-1$。这就是本例“少一个自由度”的具体含义。

月频平均收益若只换成一年口径，常写成“月均值 × 12”；复利路径则从 $1.089=(1+m)^3$ 解每月固定增长率 $m$，再把同一倍数延长到 12 个月。风险不同：独立月份的**方差**相加为 12 倍，标准差才变成 $s\sqrt{12}=40\%$。若各月常一起涨跌，就存在协方差，不能只把风险简单相加；因此根号年化要求零自相关、方差稳定。

Sharpe 先扣掉同月无风险收益，再比较平均与起伏。本例假设现金每月收益为 1%。

1. 定义超额收益 $d_t=r_t-r_{f,t}$，得到 $[0.09,-0.11,0.09]$。
2. 计算平均，得到 $\bar d=0.023333333$；样本标准差为 $s_d=0.115470054$。
3. 相除得到月 Sharpe：$\bar d/s_d=0.202072594$。
4. 在无自相关等年化条件下乘 $\sqrt{12}$，得到年化 Sharpe $0.7$。

平均与标准差都用月收益单位，比例无单位。只有年化条件成立，最后一步才可使用根号规则。

无风险在分子被扣除；当它变化时，也会通过差额序列影响分母，但不能“在波动分母扣 rf”。CAGR 减一个年利率再除波动是另一口径，不能冒称上述标准计算。

🔗 [Sharpe 1994 原文](https://web.stanford.edu/~wfsharpe/art/sr/SR.htm)，获取日 2026-10-01。

```mermaid
flowchart TD
 A["输入正价格与期间、收益口径"] --> B{"相邻价完整且同口径？"}
 B -->|否| Z["停止并回查公司行动/缺失"]
 B -->|是| C["算相邻收益，初始化净值与峰值"]
 C --> D["乘本期资金乘数，更新峰值与回撤"]
 D --> E{"还有下一期？"}
 E -->|有| D
 E -->|无| F["输出终值/CAGR/样本波动/最大回撤"]
```

边界：零/负价格不能这样取 log；$r\le-1$ 中断正权益复利链；$n<2$ 无样本标准差，$s_d=0$ 夏普未定义；申购赎回会让终点比夹杂外部现金流。缺失不能用未来价格向前填，拆股和股利须按可比口径处理。异常值会因平方显著影响波动，应先回查原事件，不能只为降低风险数字删掉。

**迁移题**：① 只保留 100→110→99，为何简单收益和为 0 却亏钱？② 若这三期改成周，其终点与年化公式哪里变化？
<details><summary>答案（笔记补充）</summary>
① 先赚 10 元，后在 110 元上亏 11 元，累计 −1%，累计 log 为 $\ln(0.99)=-0.010050336$。② 终点 108.9 不变，CAGR 改用 $1.089^{52/3}-1$，波动乘 $\sqrt{52}$；不能继续用 12。短样本年化仍不是稳定预测。
</details>

**所以呢**：收益、风险和回撤必须共享明确的基期与收益个数。课程 240 个价格的 July 2006→June 2026 净值路径只有 239 个间隔；本轮同基期核对 S&P CAGR 9.297018%、波动 15.461784%，不是把 240 条含额外首月收益与 239 间隔混报。

#### 2.3.2 复权价 vs 未复权价（讲义 p.22）

**是什么**

同一只股票，只因为公司做了一次"1 股拆 2 股"或者派了一次现金，报价本身就会在某一天突然跳动——但这个跳动跟你到底赚不赚钱毫无关系。比如一只股票从 200 元"跌"到 100 元，可能根本不是亏钱，只是拆股了。金融数据把这类"跳动"分成三种情况处理：

- **拆股（stock split）**：公司把 1 股拆成 2 股，报价从 200 变成 100。**投资者没有任何损失**——你手上从 1 股变成 2 股。
- **现金股利（cash dividend）**：公司发现金，除息日价格会下跌，**投资者同时拿到现金；总收益须合并价格变化和股利，未必为正**。
- **复权价（adjusted close）**：把上述两类事件的影响回填进历史价格，使得不同时点的价格在经济意义上可比。

<details><summary>讲义 p.22 英文原题与必要情境（课堂讨论；无选项）</summary>

**Adjusted and Unadjusted Prices Answer Different Questions**

- A stock split changes the quoted price without creating an investor loss.
- A cash dividend creates a return even though the ex-dividend price falls.
- An adjusted series tries to place prices on a comparable economic basis.
- Package defaults and vendor conventions can change; make the choice explicit.

**Class discussion:** What would a 2-for-1 split do to a return computed from unadjusted closing prices?

</details>

中文限定词：`unadjusted` 是未复权收盘价；问题问“计算出来的收益会怎样”，不是投资者真实财富一定怎样。讲义无书面官方答案；中英参考答案为：**It would show an apparent return of about −50%, even though the investor's total value is unchanged because one share becomes two shares.**

**课件原例**（讲义 p.22 的四条 + 课堂讨论题）
> - 拆股改变报价但不造成投资者损失
> - 现金股利产生收益，即使除息价下跌
> - 复权序列试图把价格放在可比的经济基础上
> - **包默认值和数据商约定会变；口径要显式写出来**
>
> **Class discussion**：「What would a 2-for-1 split do to a return computed from **unadjusted** closing prices?」
> **答案**：会记录成约 **−50%** 的暴跌。这是纯粹的记账假象。

**🎙️ 课堂补充（`27:28`–`27:46`、`01:21:07`）**
> 「For most stocks, the close price and adjusted close price, they are the same. But for some small[-]cap stocks… **if you don't know the difference, always use the adjusted close price.**」
> 「if you see a price dropped by 4[9]%, there [is] probably a two[-]for[-]one split for the stock.」
> 还有一条讲义没有的具体例子：**债券 ETF（exchange-traded fund，交易所交易基金）每月初派息**。ETF 是可在交易所买卖的一篮子资产基金，基金份额价格与所跟踪资产的价值一起变动；派息会把一部分价值从份额价格转成现金。因此每月可能看到"净值涨了但显示负收益"，若不用复权价就难以把价格变化和派息放在同一口径下读懂（`01:21:33`）。

**💡 换个说法（笔记补充）**：未复权价像标价牌，复权序列则把公司行动影响调整到可比基础；它不是你的真实账户净值。账户还涉及持股数量、现金、税费、再投资和交易成本。拆股时 1 股 × 100 元变成 2 股 × 50 元，价值仍 100 元；除息时 100→98 且每股收到 2 元，总收益 $(98+2)/100-1=0$，不是保证盈利。

**⚠️ 常见误解**
❌「复权价就是历史真实成交价」→ **不是**。复权价是被反复重算的：每次新的分红或拆股发生，整段历史都会被重新调整。所以**今天下载的复权价，和一年前下载的同一段历史，数值可能不同**。这与 §2.5.4 的"数据修订"是同一类问题。

**所以呢**：价格口径搞对了，下一步是"用什么去比较不同市场的整体表现"——这就要用到指数和基准。

#### 2.3.3 指数、基准、以及"上证综指"这个坑

**是什么**

如果有人告诉你"我今年赚了 5%"，这句话本身没法判断好坏——5% 算好算差，要看跟什么比、以及这笔钱当初买的是一个多大的公司组合。这里有两个概念决定"跟什么比"：

- **市值加权指数（capitalization-weighted index）**：大公司权重大。🎙️`01:31:29`：「if you [own] Alibaba, you take 8%[；]if [it's] others, you take 0.0[X]%.」
- **基准（benchmark）**：判断一个策略好坏的参照物。没有基准，"我赚了 5%"这句话没有意义。

**🎙️ 课堂补充（`30:19`–`31:52`）——这段完整替代了讲义没讲的部分**
> 「It is not okay [to] just tell you that I'm making money 5% a year. **If you can simply just buy the treasury bond with 4.8% for [the] 10-year… then 5% a year seems [poor]**, because you are taking huge risk investing in the stock market but you're only earning 0.2% more than the treasury bond.」

于是基准是**分市场的**：美股比 S&P 500 和美债；A 股比 CSI 300 和中债。

**🎙️ ★ 一条讲义完全没有、但极其实用的知识（`01:10:59`–`01:11:26`）**
> 「If you read the… financial media, most of them keep [talking about the] **Shanghai Stock Exchange index**… **Th[at] is something not tradable.** …**This is [a] really common mistake for evaluating returns.** But the CSI [300], this is something you can buy [as an] ETF.」

**💡 换个说法（笔记补充）**：指数点位是统计量，本身不能直接买卖；ETF 是可以在交易所买卖、并试图跟踪该指数的一篮子基金份额，所以“指数不可交易”与“有可交易跟踪产品”并不矛盾。统计业绩可用合适的指数作基准；若比较可执行投资机会，须说明跟踪产品、费用、股息和追踪差异。

🔗 [富国上证综指 ETF（510210）官方产品页](https://www.fullgoal.com.cn/fundDetail/510210/index.html) 明确标的为上证综合指数，[SSE 2026-02-04 公告](https://www.sse.com.cn/disclosure/announcement/general/jjzssgg/c/c_20260204_10808440.shtml) 已列该产品；获取日 2026-10-01。这是对课堂口述范围的纠正，不是投资推荐。

**所以呢**：口径和参照物都讲清楚了，下一节直接给出几个必须记住的具体数字——没有这些量级参照，你没法判断 AI 吐出来的数字对不对。

#### 2.3.4 数感：必须记住的量级参照 ★★

这一小节是"笔记补充 + 转录"的合成，讲义里没有任何一页集中给这些数字。**教授把这件事列为本课第一优先级**：

> 🎙️`02:12:27`「**Develop a sense for numbers. That's the top priority [thing] I want [you] to learn from the course.**」

下表给出价格、收益和风险的数感参照。每行先标量的名称，再列参照值及其来源，避免把不同单位的数字混比。

| 量 | 参照值 | 来源 |
|---|---|---|
| S&P 500 长期年化收益 | **≈ 8%/年**（过去一个世纪） | 见下方「S&P 500 长期年化收益 · 来源」 |
| 美国 10 年期国债收益率（2026-09） | **≈ 4.8%**；30 年期约 5.03% | 🎙️`31:01`、`01:47:55` |
| 中国 10 年期国债收益率 | **≈ 1.8%** | 🎙️`31:24` |
| "年化 50% 的策略" | **教授的经验性警示**：「they will disappear very, very soon」；不是数学上不可能，须核时点、杠杆、成本、风险与样本外稳定性 | 🎙️`51:34` |
| 中国科技股的合理预期 | 比 8% 高，**10% 出头**，不是 50% | 🎙️`52:15` |
| **股票收益预测的 R²** | 见下方「股票收益预测的 R² · 参照值」 | 🎙️`01:44:05`、`02:09:06` ★ |
| 对比：营销领域的数据挖掘 | R² 能从 **50% 提到 60%**；收益预测只能从 **1% 到 1.2%** | 🎙️`01:44:49` ★ |
| 20 年累计（投 100 元，2006-07→2026-06） | 见下方「20 年累计（投 100 元，2006-07→2026-06） · 参照值」 | 🎙️`01:09:28`。💡 实测：587 / 385 / 135（`L01_02`） |
| 最大回撤 | 见下方「最大回撤 · 参照值」 | 🎙️`02:10:16` 说 CSI「more than 70%」、S&P「about 50%」。💡 实测数字见左（`L01_02`） |
| 年化波动率 | 见下方「年化波动率 · 参照值」 | 💡 用 `market_index_returns_240m.csv` 实测（`L01_02`：同一路径 239 个对应收益：15.461784% / 21.800951% / 27.276111%） |
| 单月最差 | 见下方「单月最差 · 参照值」 | 见下方「单月最差 · 来源」 |

**S&P 500 长期年化收益 · 来源**

🎙️`49:53`。

💡 用课程数据实测：2006-07→2026-06 S&P 500 价格指数（不含股息）几何年化 9.297018%（240 个价格仅有 239 个间隔，$5.874202734^{12/239}-1$），与"≈ 8%"同一量级。

课堂 `49:53` 给的是 S&P 过去百年约 8% 的经验量级，未说明股息口径。本例采用课程样本和价格指数，时期及口径与课堂概数并不相同，不能把二者的差额归因于已确认的股息再投资。

⚠️ 本行曾误写为 7.95%——那是把对数收益当简单收益复利到 4.59× 再年化的结果，正是 §9.3 ① 的坑，2026-09-10 按脚本改正

**股票收益预测的 R² · 先知道它在比较什么**

先用四个月的人为小例。实际收益的平均值是 0.5%，所以“只报平均值”的基准每月都预测 0.5%。每个月的“实际 − 预测”叫**残差（residual）**；把残差平方后相加，是模型没解释掉的误差。普通最小二乘（OLS）就是选择一条线，使训练样本的残差平方和尽量小。

| 月 | 实际收益 | 模型预测 | 模型残差 | 基准预测 | 基准残差 |
|---|---:|---:|---:|---:|---:|
| 1 | 1.0% | 0.8% | 0.2 个百分点 | 0.5% | 0.5 个百分点 |
| 2 | −1.0% | −0.6% | −0.4 个百分点 | 0.5% | −1.5 个百分点 |
| 3 | 2.0% | 1.4% | 0.6 个百分点 | 0.5% | 1.5 个百分点 |
| 4 | 0.0% | 0.4% | −0.4 个百分点 | 0.5% | −0.5 个百分点 |

基准残差平方和是 $0.5^2+(-1.5)^2+1.5^2+(-0.5)^2=5$ 个百分点平方；模型残差平方和是 $0.2^2+(-0.4)^2+0.6^2+(-0.4)^2=0.72$ 个百分点平方。

$R^2$ 比较模型残差平方和与基准残差平方和：

$$
R^2=1-\frac{0.72}{5}=0.856=85.6\%.
$$

这个 85.6% 是刻意构造的高拟合教学例，只用来演示算法；它不是本课市场数据的真实预测力，更不是收益率 85.6%。一般地，$R^2=1\%$ 表示样本内平方误差相对基准少约 1%，不能与收益率比较单位。在训练样本上算叫样本内；在未参与选变量或定参数的后来样本上算叫样本外，后者更接近真实预测检验。

**课堂参照：平均 ≈ 1%**。

到 2–3% 被教授视为潜在优势。

是否成本后盈利须单独验证

**20 年累计（投 100 元，2006-07→2026-06） · 参照值**

S&P 500 → ≈ 600。

CSI 300 → ≈ 400。

恒生 → ≈ 130

同一 class01 价格表的恒生起终倍数为 1.348215270；240 个价格形成 239 个间隔，故 CAGR 为 $1.348215270^{12/239}-1=0.01511468$，即约 **1.511468%/年**。这是本讲数据与期间的复算值，不写成近似 1.7%。

**最大回撤 · 参照值**

CSI 300 −70.8%（2008-10）。

恒生 −59.1%（2009-02）。

S&P 500 −52.6%（2009-02）

**年化波动率 · 参照值**

S&P 500 ≈ 15%。

恒生 ≈ 22%。

CSI 300 ≈ 27%

**单月最差 · 参照值**

CSI 300 −29.9%。

恒生 −25.5%。

S&P 500 −18.6%

**单月最差 · 来源**

💡 原列为对数收益，2008-10 为 −29.91% / −25.45% / −18.56%。

转换成真实比例损失 $\exp(g)-1$ 为 −25.851% / −22.466% / −16.942%。

不可把 log 百分数直接当账户损失比例

**⚠️ 常见误解**
❌「R² 只有 1%，那这门课的模型全是废的」→ 教授的原话恰恰相反：「if you can get R² above two or three percent, **many hedge funds can make huge profits on that**」（`02:09:06`）。**在金融里，1% 的 R² 不是"没用"，而是"这个领域的正常水平"**——因为市场里有无数人在抢同样的信息。用做营销预测的直觉（R² 要 0.5 以上）来评价收益预测，是初学者最典型的误判。

**所以呢**：记住这些量级参照，是为了在下一步真正动手下载、计算数据时，一眼看出"这个数不对劲"。§2.4 开始真正动手。

> 📁 **代码**：[`code/L01_data/02_index_20y.py`](../code/L01_data/02_index_20y.py) —— 四个指数 20 年净值 + 回撤，跑一遍即可复现本表的累计倍数、最大回撤、年化波动、单月最差；另有恒生 2018-01 高点至今差 30%、CSI 300 2007-10 高点 19 年未收复（`L01_02`）
> 💡 原辅助图证据文件保留；本轮正文用可编辑表格与流程图解释机制。
> 📁 R² = 1% 的散点图长什么样，见 [`code/L02_regression/03_r2_scale.py`](../code/L02_regression/03_r2_scale.py)（`L02_03`，图在 [[M02-回归与样本外设计|M02]] §2.9）

---

### 2.4 把数据下下来，并且检查它

#### 2.4.1 样本、变量、日期：本讲的三个数据集（讲义 p.13）

本讲后面会同时用到好几份数据，如果不先弄清楚"谁是月频、谁是周频、各自从哪年到哪年"，很容易在合并数据时把日期对错。讲义 p.13 用一张时间线说清这件事：三个月度指数（标普 500、恒生、沪深 300）和美国宏观数据共用同一条 **240 个月**（2006-07 至 2026-06）的日历；另外恒生科技 30 只个股用的是更密的 **156 周**周频数据（2023-07 至 2026-06）。

```mermaid
flowchart TD
    A["月频：2006-07 → 2026-06<br/>240 个月，共用同一日历"] --> A1["S&P 500"]
    A --> A2["Hang Seng"]
    A --> A3["CSI 300"]
    A --> A4["美国宏观"]
    B["周频：2023-07 → 2026-06<br/>156 周"] --> B1["HSTECH 30 只个股"]
```

> **Keep in mind（讲义 p.13）**：「Markets and macro share **one 240-month calendar**. The later HSTECH 30 exercise uses denser weekly observations, and **every forecasting row uses only information known before its return is realized**.」
> 讲义脚注还有一句诚实的免责：「Free data support teaching. **Research needs point-in-time data with documented revisions and historical constituents.**」

**所以呢**：知道了"谁是月频、谁是周频、各自什么区间"，下一步是先把工具装好，才能真正跑代码。

#### 2.4.2 让 Codex 装环境（讲义 p.12）

Vibe Coding 的第一步甚至不是分析数据，而是让 AI 把开发环境装好——如果这步图省事整个交给 AI 处理，轻则装错版本的包，重则被要求交出不该给的权限（§2.2.4 的"权限分级"就是防这个）。讲义给的示例指令值得照抄：

> 「I use [Windows 11 / macOS]. Check whether Python 3 and R already work. If either is missing, use the official VS Code or RStudio installer. **Before any installation, show the package, destination, and command; then wait for approval.** Install `yfinance`, `pandas`, `matplotlib`, `akshare`, `quantmod`, and `TTR`, and report the installed versions.」

四步：

① 先看现有环境

② 检查来源与安装位置

③ 批准安装

④ 验证版本与 import。
**Pause if the scope changes**：不要提供凭据或无关的个人文件。

**🎙️ 课堂补充**：教授现场演示了这一段（`53:29`–`55:48`），问 Codex「Can you tell me whether Python is installed locally?」「Is this the latest version?」「Please help me update」。他还坦承课上网速受 VPN 影响（`54:14`），这在转录里留下了两处内容重复的段落——不是教学内容。

**所以呢**：环境装好之后，才轮到讲义 p.14 那个具体的下载任务——构造 156 周的收益。

#### 2.4.3 构造 156 周的收益（讲义 p.14）

六项规格（§2.2.3）讲的是六条抽象要求；讲义 p.14 给了一个具体样例，把六项规格套在一只真实股票（AAPL，苹果）上——要几年数据、用什么价格口径、日期怎么标，全部写进了下面这条英文指令里：

**示例指令**（讲义原文）
> 「Using Python and **adjusted** AAPL prices, build **Friday-labelled** weekly prices from **30 June 2023** through **26 June 2026** and **simple weekly returns** from 7 July 2023 through 26 June 2026. **Download enough earlier data to calculate the first return.** Run the job, save the table, and report the first date, last date, row count, and missing values.」

把下载任务写成可执行规格时，逐行确定对象、频率和交付检查。表中每项规格都对应一个接受标准。

| 跑之前先定死 | 只有满足这些才接受结果 |
|---|---|
| 复权价口径 | **157** 个周价格 |
| 周五作为周标签 | **156** 个非缺失收益 |
| 精确的起止日期 | 一个已保存、按日期排序的文件 |

**🎙️ 课堂补充（`47:50`）**——教授把这个检查抽象成一条通用的"挑战式检验"：
> 「if I download… 200 prices there… then I [should] have **199 returns**, because you need to calculate the [difference] between two [prices]. So you need to challenge the output from time to time, **because you understand the logic of the data**.」

他在演示时也确认了「157 prices with 156 returns」（`01:07:31`）。

**💡 验证（笔记补充）**：课程给的 `aapl_weekly_prices_returns_156w.csv` 实测确实是 **157 行价格、156 个非缺失收益、第一个收益为空**，且 `weekly_return` 与 `adjusted_close` 的简单收益公式吻合到 3e-16。**这个数据集是本讲唯一一个可以逐项对上讲义检查清单的样本，值得拿来练手。**

**所以呢**：单一股票、单一数据源的下载练完了；真正的数感表（§2.3.4）需要三个指数、两个数据源拼在一起，下一节看这怎么做。

#### 2.4.4 从两个数据源拼一张表（讲义 p.17–18）

§2.3.4 数感表里标普 500、恒生、沪深 300 三个指数 20 年的表现数字是怎么来的？三个市场分散在两个不同的数据源：美股和港股在 Yahoo Finance 能查到完整历史，沪深 300 只能从 AKShare 拿（原因见下表第 3 行）。下面这段代码示范怎么把它们拼到同一张表上。

**只为读代码的最小表模型**：DataFrame 是一张二维表；`index` 是每行标签（这里是日期），`columns` 是列名。选一列如 `df["Close"]` 后得到 Series，可把它想成“带日期标签的一列”。`=` 把右边结果命名；`f(x, option=True)` 是调用函数，括号里先放输入、再放命名参数；点号方法链 `daily.resample("ME").last()` 是把上一步结果继续交给下一个动作。

| index 日期 | Close | Volume |
|---|---:|---:|
| 2026-06-01 | 100 | 20 |
| 2026-06-02 | 102 | 25 |

读 `close = df["Close"]`：从表 `df` 选出 Close 列，把这列 Series 命名为 `close`。`dtype` 是一列的存储类型；`float64` 可做小数运算，`object` 常意味着数字被当成文本，需先停下核对。

```python
import akshare as ak
import pandas as pd
import yfinance as yf

global_px = yf.download(
    ["^GSPC", "^HSI"],
    start="2006-06-01", end="2026-07-01",
    auto_adjust=True, progress=False
)["Close"]
csi = ak.stock_zh_index_daily_em(
    symbol="sh000300", start_date="20060601", end_date="20260630"
)
csi["date"] = pd.to_datetime(csi["date"])
csi_px = csi.set_index("date")["close"]
csi_px.name = "CSI300"
daily = global_px.join(csi_px, how="outer")
```

**逐行说明（不要求会写，要求会读）**

| 行 | 在干什么 | 关键参数为什么这么取 |
|---|---|---|
| `yf.download([...])` | 从 Yahoo Finance 一次下两个指数：`^GSPC` = S&P 500，`^HSI` = 恒生 | `start` 定在 **2006-06**，比目标区间 2006-07 早一个月——就是 p.14 说的「download enough earlier data」，为了能算出第一个收益 |
| `auto_adjust=True` | 返回**复权**价 | 对应六项规格的第 3 项 |
| `ak.stock_zh_index_daily_em(symbol="sh000300")` | 用 AKShare 取沪深 300 | 🎙️`01:07:45`：「the Yahoo Finance ha[s] **[no] full history**」for 中国数据，所以换源 |
| `.join(..., how="outer")` | 按日期对齐三条序列 | `outer` 表示**保留任一市场的交易日**，不强行取交集 |

三条序列现在还按各自市场的原始交易日历堆在一张表里（港股、A股、美股的假期都不一样），下一步要把它们压缩成统一的月度频率，才能对上 §2.4.1 说的那条 240 个月共用日历：

```python
monthly = daily.resample("ME").last()
monthly = monthly.loc["2006-07":"2026-06"]
print(monthly.index.min()); print(monthly.index.max())
print(monthly.shape); print(monthly.isna().sum())
```

**Verified output（讲义 p.18）**：first month `2006-07-31`；last month `2026-06-30`；shape `(240, 3)`；missing months **zero**。

| 行 | 在干什么 |
|---|---|
| `.resample("ME").last()` | 按**月末**（Month End）分组，并对每一列取该月最后一个非缺失值；pandas `Resampler.last` 默认 `skipna=True`（[官方文档](https://pandas.pydata.org/docs/reference/api/pandas.api.typing.Resampler.last.html)，获取日 2026-10-23） |
| `.loc["2006-07":"2026-06"]` | 裁到目标的 240 个月 |
| 四个 `print` | 就是六项规格第 6 项要求的"自报维度与缺失" |

> **Keep in mind（讲义 p.18）**：「The shared calendar lines up the dates. **Holidays, trading hours, and index construction rules still differ across the three markets.**」
> 讲义还提醒：「These are **price-index** returns; **dividends are not included**.」

**🎙️ 课堂补充（`01:24:10`–`01:24:34`）**——教授给了跨市场对齐的具体例子：
> 「for the National [Day] break… in mainland China you have seven day[s] break, but in Hong Kong you only have one day break… **for Christmas, there's [no holiday] in mainland China, but there's a break in Hong Kong.**」
> 因此**日频 outer join 表**会因各市场假日不同而在某些日期出现 NA；但这不等于月频表必然缺月。只要某市场在该月仍有至少一个有效交易日，逐列 `.last()` 跳过 NA 后，本例月频 `(240,3)` 可以是 0 个缺月。教授在 `01:23:36`–`01:23:58` 强调缺失是现实常态，而本例“日频有空格、月频无缺月”说的是两个不同阶段。这个区别也意味着：若整列整月都缺，`.last()` 仍会得到 NA，不能静默补值。
>
> 原课堂表述：跨市场日历会出现缺失值，而这正是他坚持不给学生"洗干净的数据集"的原因：「Other faculties, they will just give you a well[-]clean[ed] data set… But in real world data… you exactly [see] what I show you: **data missing value everywhere.**」（`01:23:47`）

**所以呢**：数据拼好了、也知道了缺失值是常态，但还不能直接拿去算收益——算之前，讲义要求先做四项检查。

#### 2.4.5 算之前先做四项检查（讲义 p.23）

数据拼好了（§2.4.4），还不能马上算收益。讲义坚持要先看一眼数据本身长什么样——列名对不对、有没有缺失、数量级合不合理——这样才能在错误的收益被算出来**之前**发现问题，而不是算完一堆漂亮数字之后才回头怀疑。讲义 p.23 给了一条检查指令，要求 AI 在动手计算前先交出四样东西。中文读题关键词是“计算前、精确列名和类型、首尾三行、缺失与描述统计”；描述统计至少要看计数、均值、最小/最大值是否符合该市场量级。

<details><summary>讲义 p.23 英文原题（无选项）</summary>

**Data-checking instruction**

Before calculating returns, run Python and show: (1) table dimensions, (2) exact column names and types, (3) the first and last three dated rows, and (4) missing-value and descriptive-statistic summaries.

Reading the output is the part that cannot be delegated. Two questions decide whether to continue: which column is the adjusted economic price, and are the missing observations and magnitudes plausible for this market?

</details>

原题没有官方答案；下文是依据讲义检查要求的中文参考解释：

> **Data-checking instruction**：「Before calculating returns, run Python and show: **(1)** table dimensions, **(2)** exact column names and types, **(3)** the first and last three dated rows, and **(4)** missing-value and descriptive-statistic summaries.」

讲义接着写了本讲最重要的一句方法论：

> 「**Reading the output is the part that cannot be delegated.**」

两个问题决定要不要继续：**哪一列是复权后的经济价格？缺失值和数量级对这个市场来说合理吗？**

**English reference answer（⚪ 条件性答案）**: Use the explicitly adjusted-price column only after checking the vendor convention. Continue only when missing observations match the market calendar or a documented source gap and when prices, returns, and dates have plausible magnitudes; otherwise stop and inspect the raw rows. 本讲 AAPL 样本应核 adjusted_close、157 个周价与首行收益缺失；三市场日表允许假日 NA，月表本例为 240×3 且零缺月。

**⚠️ 常见误解**：❌「AI 说没问题就没问题」→ 🎙️`47:16`：「They are numbers[; ] might be everything might be fake. You don't know.」教授明确说 AI 会编造数字，且 AI 自己也在免责声明里承认这点。

**所以呢**：数据检查完，本讲真正的主题才正式登场——预测时钟，也是全篇最重要的一节。

---

### 2.5 ★ 预测时钟：本讲真正的主题

这是全讲最重要的一节。讲义把它拆散在 p.27、33、39–40、43、47–48，本笔记合并。

#### 2.5.1 预测时钟（Forecast clock）

先固定一个决策时点，再判断每个量在哪边。以2026-06-19周五收盘后作预测为例：价格和过去窗口已知，2026-06-26的价格与下一周收益未知。

| 对象 | 何时可知 | 在本次决策中的角色 |
|---|---|---|
| 截至6/19的动量 | 6/19收盘后可算 | 输入 |
| 6/26收盘价 | 6/26收盘后 | 未来结果端点 |
| 6/19–6/26收益 | 两端点均已实现后 | 目标，不能作输入 |

下方 $x_t\to r_{t+1}$ 的箭头只表示先形成输入、后观察结果，不表示输入造成了收益。若数据行按目标周 $t+1$ 标注，该行输入仍来自 $t$；后文改用目标周$t$时，输入止于$t-1$。两套记号只换标签，真实顺序不能换。

**是什么**

§2.2.3 六项规格的第 4 项提到过"预测时钟"，说它写漏了后果最致命，但没细讲它到底是什么。它其实是给数据表的每一行做一次"时间戳公证"：这一行里，凡是当**预测变量**用的数字，必须证明自己在"公证时刻"**之前**就已经存在；凡是当**目标**（要预测的收益）用的数字，则必须证明自己是公证时刻**之后**才发生的。用讲义的话说，一条明文规定，说清两件事：**预测变量在什么时刻已经可知；目标收益在什么时刻才实现。** 讲义 p.43 的图示：

$$\underbrace{x_t}_{\text{第 } t \text{ 周收盘后可知}} \quad\longrightarrow\quad \underbrace{r_{t+1} = P_{t+1}/P_t - 1}_{\text{在第 } t+1 \text{ 周内实现}}$$

先按下面的预测时钟区分目标期、输入时点与可用信息。每行说明一个符号如何限制取数。

| 符号 | 是什么 |
|---|---|
| $x_t$ | 预测变量：第 $t$ 周收盘后就已经知道的数（动量、波动率……） |
| $r_{t+1}$ | 目标：下一周（第 $t+1$ 周）内实现的收益，用第 $t+1$ 周末与第 $t$ 周末的价格算 |
| $P_t$ | 第 $t$ 周末的价格 |

**代入一个具体例子**：用 §2.4.1 提到的恒生科技 30 只个股周频数据，假设 $t$ = 2026-06-19 那一周（周五收盘）。$x_t$ 可以是"截至 2026-06-19 收盘算出的过去 4 周动量"——这个数当天收盘后就能算出来，属于**已知**。

$r_{t+1}$ 则是下一周的收益 $P_{t+1}/P_t - 1$，要用 2026-06-26 和 2026-06-19 两个周五的收盘价，这笔收益**要等到 2026-06-26 收盘才真正发生**。如果有人在 2026-06-19 当天就已经用上了 2026-06-26 才会出现的信息（哪怕只早一天），这一行数据就已经泄漏——这正是下一节要讲的"数据泄漏"。

配套四条规则（讲义 p.43）：
1. 保存下来的那一行，用**预测周 t+1** 来标注
2. 个股特征只能用**不晚于第 t 周**的价格和成交量
3. 已归档的会计数据可以向后延续；**尚未归档的值必须保持不可用**
4. 多下载一些样本前的数据来构造滚动信号，然后**只保留恰好 156 个预测周**

**为什么需要它**

因为不写清楚，AI 生成的代码有很大概率把方向搞反，而且**不会报错**。

> **Common failure（讲义 p.47）**：「An AI assistant may produce **syntactically valid code with the target shifted in the wrong direction**.」

**🎙️ 课堂补充（`29:01`–`29:59`、`02:00:05`）**
> 「At the time point, for example, 2015, if you want to predict return for Hang Seng index [in] 2015 January, **you can only use predictors up to 2014 December**. The rule seems simple. But when you see the data… you'll find that it is **very, very easy to mix up**.」
> 「**the mistake I see… 99.9%… that's missing the date.** It is not the functional form.」

**💡 换个说法（笔记补充）**：把每一行数据想象成一封信，信封上写着"第 t+1 周才准拆"。里面装的所有预测变量，都必须是在封信那一刻（第 t 周末）就已经写好的。**任何一个在第 t+1 周才知道的数字被塞进信封，整封信就作废了。**

**所以呢**：预测时钟定义了"谁在前、谁在后"这条抽象规则；下一节看这条规则被违反时，具体表现是什么——数据泄漏。

#### 2.5.2 数据泄漏、前视偏差与"漂亮的假业绩"

**是什么**
- **数据泄漏（data leakage）**：用了在那个时点还不可能知道的信息。
- **前视偏差（look-ahead bias）**：数据泄漏在回测里的具体表现——用未来信息去评价历史策略。

**🎙️ 课堂补充（`30:06`、`01:35:06`、`01:43:57`）**——教授给了一条**可直接用来自查的经验法则**：
> 「anytime I see students get **crazy returns**, they are [almost] all… data leakage. **This is the [most common] mistake.**」
> 「My tip [is]: **if you see very good prediction, then you must [be] us[ing] future information.**」

**⚠️ 常见误解**
❌「泄漏是个技术 bug，跑通了就没有」→ 泄漏的典型症状恰恰是"跑得特别顺、结果特别好"。**它不会报错，只会让你自我感觉良好。**

**所以呢**：知道了"数据泄漏"这个统称，下一节列出它最常发生的五种具体写法——光知道定义防不住，知道套路才防得住。

#### 2.5.3 五种泄漏路径（讲义 p.48）★

上一节说"数据泄漏"是用了当时不可能知道的信息，但这句话很抽象——具体会在哪些操作里不知不觉发生？讲义 p.48 列出五种最常见的写法，**每一种单独看代码都完全合法、不会报错**，这也是它们危险的原因：

| # | 路径 | 为什么是泄漏 |
|---|---|---|
| 1 | 在划分训练/测试集**之前**用全样本做中心化或标准化 | 测试期的均值和标准差混进了训练期 |
| 2 | 用**居中的**滚动窗口（centered rolling window） | 窗口一半落在未来 |
| 3 | 按**财季期末**对齐会计数据，而不是按发布日 | 见 §2.6.3 |
| 4 | 用**后来才观测到**的值去填补缺失 | 未来值倒灌进历史 |
| 5 | 看完最终测试集表现之后再**回头挑选**预测变量 | 测试集被你用作了选择依据 |

**把 1、2、5 走成能追踪的小例**

- 全样本标准化：训练期数值 `[1,2,3]`，测试期极端值 `100`。若先用四个数求均值 `26.5`，训练期已经“知道”未来有 100；正确做法只用训练期均值 `2` 和训练期标准差变换训练/测试。
- 居中窗口：假设在 3 月 31 日形成信号，用它预测 4 月收益。若给 3 月计算“三个月居中均值”，窗口可能包含 2 月、3 月和 4 月；4 月在信号时刻尚未发生，已经泄漏。正确的三个月尾部窗口只用 1 月、2 月、3 月，并在 4 月目标实现前冻结。
- 测试集选变量：前 8 月训练，后 2 月测试。看完后 2 月后在 20 个变量里挑“测试成绩最好”的那个，相当于用答案选题；应在训练/验证期定变量，只对冻结方案使用测试集一次。

路径 3 的财报归档例见 §2.6.3；路径 4 的发布时间/修订例见 §2.6.1。五条的共同检查是：每个处理参数和选择决定由哪一段数据决定？若答案包含最终测试期，它就不再是独立测试。

> **Keep in mind（讲义 p.48）**：「**A predictor formula is not complete until its information date is specified.**」

**所以呢**：第三至第五种泄漏路径都直接与日期有关。

下一节把所有和日期相关的坑，归纳成三种必须分开记的日期。

#### 2.5.4 三类日期与四个节点，永远分开记（讲义 p.27）★

这张链帮助回答：文件上写3月末，为何4月不能使用报表？箭头表示从所描述期间到公开/可用的时间顺序，不是数值计算或因果关系。

用讲义日期例走一次：2025Q1经营到3/31结束，报表到5/2才归档。4月的预测在“公开”节点之前，因此新值不可用；5/2当天也要比较真实公开时刻与本次决策cutoff。只有公开时刻不晚于cutoff，才走到“可用于预测”。

简短替代读法：先看报告讲哪个期间，再看什么时候公开，最后看决策当时是否已经公开。图没有精确时刻时不能推出5/2开盘就可交易。

<details><summary>读图自测：公司5/2晚间公开，5/2下午决策能用新值吗？</summary>

不能。虽是同一个日历日，公开节点仍晚于决策cutoff；用旧合法值或保留缺失。

</details>

这里说“三类日期”是：

1. 数据描述的参考期或交易期；
2. 文件标签日；
3. 真实公开日或归档日。

实际决策还要增加第 4 个比较节点——决策 cutoff。“可用于预测”不是新的数据日期，而是公开时刻与 cutoff 比较后的判断结果。

讲义把"从经济事件到可用信息"画成一条链：

```mermaid
flowchart LR
    A[经济事件发生的时期<br/>Economic period] --> B[文件上标注的日期<br/>File date]
    B --> C[公开发布 / 归档<br/>Release or filing]
    C --> D[可用于预测<br/>Usable to forecast]
```

四类输入都必须在下单前可得。逐行比较它的标签日期与真实可用时刻，标签相同不代表发布时间相同。

| 数据 | 文件上可见的日期是什么意思 | 什么时候才能用 |
|---|---|---|
| 市场指数 | 交易月或交易日 | 决策只用**更早的**收盘价 |
| 日频利率 | 交易日 | 先**聚合成月频、再滞后**，才能用于该预测月 |
| 月频宏观 | **参考月**（reference month） | **发布公开之后** |
| 公司财务 | **财季期末**（fiscal period end） | **10-Q / 10-K 归档之后** |

> **Keep in mind（讲义 p.27）**：「**A date in a file is not automatically a date when investors could have known the value.**」

**所以呢**：抽象规则、失败案例、日期分类都讲完了；接下来两节看这条规则在宏观数据和公司财务里分别是什么样子的具体坑。

> 📁 **代码**：[`code/L01_data/05_prediction_clock.py`](../code/L01_data/05_prediction_clock.py) —— 预测时钟画成甘特图：预测 2026-06 时，特征表 15 个预测变量各自引用了哪些月份的原始数据（用扰动法实测，不是手写）；全部止于 2026-05，只有目标在红线右边（`L01_05`）
> 💡 原辅助图证据文件保留；本轮正文用可编辑表格与流程图解释机制。

---

### 2.6 宏观数据与公司财务：三种时点的具体实例

#### 2.6.1 宏观数据：参考月 ≠ 发布日（讲义 p.28、p.30–33）

§2.5 讲的是抽象规则；宏观数据是这条规则最常踩坑的一类实例。一份标注"2026-06"的失业率数字，那个日期指的是**统计的是哪个月**，不是**投资者哪天能看到这个数**——失业率通常要到下个月中才公布（具体节奏见下文教授的现场演示）。讲义 p.28 给的下载指令，明确要求不要把这两个日期搞混：

**课件原例**——讲义 p.28 的宏观指令：
> 「Download FRED series **DGS10, DFF, UNRATE, CPIAUCSL**. Convert daily rates to **monthly means** and keep monthly series at monthly frequency. Return exactly 240 month rows from 2006-07 through 2026-06, **preserve published missing values**, and plot each series. **Do not treat a reference-month date as its public release date.**」

（`DGS10` = 10 年期美债收益率；`DFF` = 联邦基金利率；`UNRATE` = 失业率；`CPIAUCSL` = CPI 价格指数水平。CPI 是一篮子消费品和服务的价格水平；若把它转成同比，才是在问“相对去年同月上涨了多少百分比”，两者不能混用。）

讲义 p.30 先要求对一条 UNRATE 序列保存两份文件：raw 保留下载原貌和来源证据，cleaned 只做已声明的解析或整理，不能覆盖 raw。预期对象是 2006-07 至 2026-06 的 240 个 observation-month 行，含 observation date 和 UNRATE 值，并保留发布的缺失；这一步不能把参考月当发布日期、把当前 vintage 当实时 vintage，或把缺失当 0。

讲义 p.33 把这条讲透了：

> 一行标注 `2026-06-01` 的数据，**标的是参考月，不是投资者得知失业率的那一天**。
> - 月度宏观序列通常在参考期**之后**才发布
> - 已发布的值**会被修订**
> - 今天从 FRED 下载到的历史，可能是**修订后**的版本，而不是当年实时看到的版本（vintage）
> - 因此预测练习需要**发布日历**；修订重要时还需要 **ALFRED** 这类实时版本数据
>
> **Do not do this（讲义 p.33）**：「Do not forward-fill a monthly series from the first day of its reference month and call it a real-time predictor.」

<details><summary>讲义 p.31 英文原题（四问，无选项）</summary>

**Plot FRED, Then Check the Timing**

**Follow-up instruction**

Run Python to plot UNRATE against its observation month. Then repeat for DGS10, DFF, and CPIAUCSL, using monthly means for the daily rate series. Return the chart, the aggregation rule, and a table of missing months.

1. Does the chart use the requested variable and units?
2. Did daily rates become monthly means rather than month-end values?
3. Are gaps visible rather than silently filled?
4. What extra release lag is required before using each series for prediction?

</details>

中文限定词：`observation month` 是参考月；日频利率必须取月均；缺口必须显示；用于预测还要补实际发布滞后。原题无官方答案，以下为课程数据与 p.28–33 支持的参考作答。

**讲义 p.31 的四个检查问题，逐问回答**（✅ 来自课程数据与 p.28–33；发布时间的精确日期未在数据包里，不能编造）：

**1. 变量与单位。** UNRATE 是失业率百分比；DGS10 / DFF 是以百分比表示的年化利率；CPIAUCSL 是价格指数水平。若画派生的 inflation_yoy，纵轴必须写“CPI 同比 %”。图例、数据列名和来源元数据要互相对上。

**2. 日频转月频。** 对 DGS10 / DFF 应按月份取日观察值均值，并检查有效日数。课程 CSV 只提供月均列，没有原始日频行；因此能确认交付列名，不能独立重算每个月均值。

**3. 缺口。** 不静默插值或前填。课程宏观表 2025-10 的失业率与通胀为空，图和缺月表应保留；缺口原因仍须回数据源核查。

**4. 发布滞后。** UNRATE 和 CPI 的标签是参考月，月均利率也要等当月观察值收齐。逐个预测日查实际发布日和 vintage；没有发布日历时采用并披露保守滞后，不能把 2026-06-01 当成 6 月 1 日可用。

**🎙️ 课堂补充（`01:32:10`–`01:34:38`）——教授现场做了一次演示**

他先冷不丁问全班：「**Can anyone tell me what is the CPI for China in August?**」然后自答：

> 「CPI [is] usually released **in the second week of the month**. There's [a lag] to collect the data, to calculate [the] data, to publish the data… So that's the reason **we will not see the CPI of August at the end of August or the first [week] of September**.」
> 「For… GDP, [it's] released in the end of [the] second week or the beginning of the third week, **after the quarter**.」

**🎙️ ★ 教授个人的"保守滞后"做法（`01:41:10`–`01:43:00`、`01:55:59`）——讲义完全没有**
> 「Researchers, they are very conservative — so like me. **I will not use CPI of August until… I will wait till the end of this month to predict the [next] month.** …So I will take a **one[-]month lag**. For [earnings announcements], I will wait for **three months**… Because I guess that most companies, they need one to three months to release their financial information.」

**💡 换个说法（笔记补充）**：讲义按实际公开时间匹配；教授另给参考期加保守滞后的近似。财季 3/31 加 3 个月是 6 月末，而不是 5/2 归档后再加 3 个月到 8 月。固定 lag 仍可能遇迟发或历史修订；采用何种规则必须写清，并检查实际公开时间不晚于 cutoff。

**💡 一个绝佳的真实例子（笔记补充，来自课程数据集）**：`macro_240m.csv` 里 240 个月**只有一个月缺失**——**2025-10**，`unemployment_rate` 和 `inflation_yoy` 同时为空。这正是讲义 p.28 说的「**preserve published missing values**」的实物：文件当月两字段确实为空；没有发布日期或缺失原因，不能据此断言官方未发布。

这个缺口按 2 个月滞后传导到 `spy_monthly_features_240m.csv` 的 **2025-12** 行。**如果当初"顺手填一下"，你就永远看不到这个信号。**

**English reference answers（逐问）**

1. Verify each chart's series ID and units against source metadata; UNRATE is a percent, DGS10/DFF are annualized rates in percent, and CPIAUCSL is an index level.
2. Aggregate daily rate observations by calendar month using the monthly mean, not the month-end observation.
3. Keep and report missing months; do not silently interpolate or forward-fill them.
4. Use the actual release calendar and vintage available before each forecast cutoff. If those records are unavailable, apply and disclose a conservative lag rather than treating the reference month as the release date.

**所以呢**：美国的宏观数据讲完了；中国的宏观数据不在同一个数据源里，下一节换一个接口继续讲同一条规则。

#### 2.6.2 AKShare 与中国宏观（讲义 p.29）

上一节讲的是美国的宏观数据源 FRED；中国的宏观数据不在 FRED 里，要换一个接口，叫 AKShare（§2.4.4 拼沪深 300 数据时已经用过）。讲义 p.29 给了一条对应的下载指令，取的是中国的 CPI 同比（和去年同月比的物价涨幅）和官方 PMI（采购经理人指数，一个反映制造业景气度的指数，50 是荣枯线）：

> **示例指令**：「Using AKShare, download China CPI year-on-year and official PMI. Keep 2006-07 through 2026-06, create a 240-month calendar, preserve missing months, and **print the exact column names before selecting fields**. Explain the units and release timing. **Stop if the interface has changed.**」

两条附注（讲义 p.29）：
- **CPI 和 PMI 是月频；GDP 是季频，不能把它"抻"成 240 个假月度观测**
- 做研究要用官方或授权数据源核对

```python
import akshare as ak
import matplotlib.pyplot as plt
cpi = ak.macro_china_cpi_yearly()
pmi = ak.macro_china_pmi()
print(cpi.columns.tolist())     # ← 先打印列名，再选字段
print(pmi.tail())
```

**逐行说明**

| 行 | 在干什么 | 关键参数为什么这么取 |
|---|---|---|
| `ak.macro_china_cpi_yearly()` | 取中国 CPI **同比**数据 | 函数名自带 "yearly"，对应的是同比（与去年同月比），不是环比（与上月比） |
| `ak.macro_china_pmi()` | 取官方 PMI | PMI 是扩散指数，50 是荣枯线：高于 50 表示制造业在扩张 |
| `print(cpi.columns.tolist())` | **先打印列名，再选字段** | 讲义 p.35：「**Package output is not a stable database schema.**」——第三方包的列名会随版本改变，先看清楚再选，才不会静默拿错列 |
| `print(pmi.tail())` | 打印最后几行 | 快速确认数据取到了最新月份，且格式正常 |

**所以呢**：宏观数据的时点坑讲完了；公司财务是另一类更隐蔽的坑，因为财报上印的日期本身就容易让人误以为"到点就能用"。

#### 2.6.3 公司财务：用归档日，不用财季期末（讲义 p.34–41）★

**是什么**

一份"截至 2025-03-31 的季度报表"，并不是 3 月 31 日就能用。它要等到公司把 10-Q 提交给监管机构那天（例如 **2025-05-02**）才成为公开信息。

```
2025-03-31   ──→   2025-05-02   ──→   财务预测变量可用
（财季期末）        （10-Q 归档）        （实际公开时刻不晚于决策 cutoff）
```

**课件原例**（讲义 p.39）
> - 这些数值描述的是 3 月结束的那个季度
> - **如果报表 5 月才归档，投资者在 3 月不可能用到里面的字段**
> - **该预测变量在归档日之前必须保持缺失，之后一直沿用到下一次归档**

**日期匹配规则的自然语言写法**（讲义 p.40，可直接抄给 AI）
> 「For each trading date, attach only the **latest** financial statement **whose filing date is on or before that trading date**. Keep both the fiscal period end and filing date in the output. **Do not match on the fiscal period end.** Show three rows around every filing date so I can check when the values change.」

**🎙️ ★ 课堂补充：教授现场打开 Yahoo Finance 演示了这个坑（`01:37:12`–`01:38:40`）**
> 「from Yahoo Finance… **you will only see June 30, March 31, September 30, December 31. This is only [the reference date].** But they did **not** tell you when do they [announce] the June 30 results.」
> 他随即查了腾讯（`0700.HK`）：「**So August 12th.** …This is the reference quarter end… **This is the actual publication date.**」

他还给了同期的三个真实归档日（`01:43:15`）：**腾讯 8 月 12 日；阿里巴巴 8 月 20 日；另一家公司 8 月 21 日**——用来说明**不同公司的发布日各不相同，不能一刀切**。

**🎙️ 一段讲义没有的制度史（`01:38:40`–`01:39:23`）**
> 「before 2000, the SEC [still received] **mails** for the financial report… so once they do the earnings announcement, it still takes **a few weeks**… Right now, when they finish the earnings announcement, you will see the report to the SEC **the other day**.」
> 课堂口述在这里把美国 SEC 与香港 SFC 并列。监管机构名称属于课堂事实，但**提交/发布机制不能直接类比**：美国 10-Q/10-K 走 SEC filing；香港上市公司的公告和文件按 HKEX Listing Rules 经电子呈交系统（ESS）提交，并在 HKEXnews 发布。HKEX 明确说明 HKEXnews 是监管信息的首个发布点，ESS 用于提交待发布文件（[HKEX ESS FAQ](https://www.hkex.com.hk/Global/Exchange/FAQ/ESS-All-FAQs/Access-to-eSubmission-System-ESS?sc_lang=en)、[HKEX 投资者 FAQ](https://www.hkex.com.hk/-/media/HKEX-Market/Listing/Rules-and-Guidance/eSubmission-System/Listed-Company-Information-Dissemination-and-Related-Trading-Arrangements/faqinv.pdf)，获取日 2026-10-23）。因此腾讯等港股的可用时点应核实际 HKEXnews 公告发布时间，不能套用美国“向 SEC 归档”的同款规则。
> → **含义**：做长历史回测（课堂 `01:38:40`–`01:39:23` 提到长期美股研究）时，2000 年前后的"归档滞后"长度完全不同，不能用同一个假设。

**⚠️ 常见误解（★ 教授反复强调）**
❌「财报里的日期就是可以用的日期」→ 🎙️`01:39:37`：「**Most people I see when they do stock prediction, they mismatch the day**… You cannot use [information] which [is] released in August to predict return in July.」

**所以呢**：知道了"用归档日、不用财季期末"，下一步是怎么把归档之后拿到的会计数字，变成能跨公司比较的预测变量。

#### 2.6.3a 从财报接口到可知时点（讲义 p.35–40；💡 机制补充）

接口取值和时点匹配是两条流程，不能因为画出收入柱就把该收入当历史可用输入。

| 步 | 输入 | 动作 | 输出 |
|---|---|---|---|
| 1 | AAPL代码 | 取得季度表 | 科目×财季表 |
| 2 | 原表 | 查看index/columns | 已确认科目与报告期 |
| 3 | 已确认收入行 | 选取并按报告期排序 | 收入Series |
| 4 | 排序收入 | 画柱、核币种/单位 | 收入图 |
| 5 | 公开/版本事件 | 与每个cutoff比较 | 合法预测输入 |

一行是一种操作状态，最后一步不由前四步自动产生。下面匹配图的箭头表示筛选与循环；5/2 16:00只允许旧18%，5/5可用20%，5/9才用修订21%。每次都从事件表按该cutoff筛，不能把今天最新版本倒灌。

文字替代：报告期用于说明收入所属期间，公开时刻与版本用于决定它何时能预测。原季度表与历史事件文件未保存，本节例子为明确假设，不声称重新下载了课堂数据。

想画苹果季度收入，先得知道返回表怎样摆放；想用收入预测，更要知道投资者何时拿到它。这是两个独立任务。

p.35/36 过程是 `Ticker("AAPL")`→`quarterly_income_stmt`，返回 DataFrame，通常行是科目、列是财季期末；先打印 `index`/`columns`，确认收入字段存在，再用 `.loc["Total Revenue"]` 选成 Series。`.sort_index()` 将报告期升序排列，`.plot(kind="bar")` 生成柱图 Axes，再核标题、日期和货币单位。

显示 5 季度时输出应为 5 根收入柱；期末是横轴，不是公开日。原始季度表未保存，不能拿今天接口替换课堂截图并称重现。

每一步保存的状态依次是 ticker→原返回表→确认过的科目和报告期→一列收入→升序收入→图。缺字段、单位未知、季度与 YTD 流量混杂、空返回时停止并打印原表，不能用另一个会计科目静默替换；画收入不会自动生成资产、权益、现金流或 filing metadata。

时点匹配另用一个完整教学例。假设旧报告 2/14 公开，利润率 18%；新报告参考期 3/31、5/2 **18:00** 公开、利润率 20%；5/8 修订为 21%。决策 cutoff 5/2 **16:00**。输入事件记录至少有参考期、公开时刻、版本时刻、值；先筛公开/版本时刻均不晚于 cutoff，再选合格记录中最新报告及当时版本。

| 历史决策时刻 | 合格最新值 | 不允许的动作 |
|---|---:|---|
| 5/2 16:00 | 18% | 使用当天 18:00 才公开的 20% |
| 5/5 | 20% | 把 5/8 修订 21% 前填 |
| 5/9 | 21% | 以此重写 5/5 的历史输入 |

每个 cutoff 处理一次，到最后一个日期停止，输出带 reference/public/version/cutoff 的匹配表。首次公开前没有旧值则 NA；公开后可以向后持有到下一合法事件。讲义 p.39 只给日期，不能据此断言 5/2 开盘可交易；跨时区更不能只比较日历字符串。

```mermaid
flowchart TD
 A["保留事件参考期/公开时刻/版本时刻"] --> B["逐个决策 cutoff 筛公开且当时已有版本"]
 B --> C{"有合法记录？"}
 C -->|无| D["输出 NA 或资料受阻"]
 C -->|有| E["取最新公开记录的当时版本"]
 E --> F["输出值与来源时刻，核不晚于 cutoff"]
 D --> G{"还有日期？"}
 F --> G
 G -->|有| B
 G -->|无| H["保存时点匹配表"]
```

失败机制：只匹配期末等于提前看到报告；使用当前修订快照则将过去不存在的版本回填。前者要补实际发布时刻，后者要历史版本；固定三个月滞后不能修复这两项数据缺口。宏观数据一样，参考月、公开时间和 vintage 必须分别保留。

**迁移题**：若新报告延期到 7/5，财季 3/31 加 3 个月能否在 6/30 使用？若没有旧报告，5/2 16:00 取什么？
<details><summary>答案（笔记补充）</summary>
不能，6/30 仍早于实际公开；没有旧报告则 NA，不能向前填 20%。所需历史发布/vintage 原表不在当前课包，故本例只演示流程。
</details>

**所以呢**：画出报表与合法预测是两种输出；必须先把数据单位与时点各自核清，再算财会比率。

#### 2.6.4 把会计水平量变成可比的预测变量（讲义 p.38）

苹果一个季度能赚几百亿美元，一家初创公司一个季度可能只赚几百万——利润的绝对金额没法直接比较两家公司谁更会赚钱，因为体量根本不在一个量级。**把绝对金额换成比率**，才能让不同规模的公司放到同一张表里比较，这也是下一节"横截面"分析的前提。讲义 p.38 给了四个候选的会计比率：

| 预测变量 | 公式 | 含义 |
|---|---|---|
| **利润率** Profit margin | 净利润 / 营业收入 | 每一元销售产生多少利润 |
| **账面杠杆** Book leverage | 1 − 股东权益 / 总资产 | 资产中由非股权索取权融资的比例 |
| **资产增长** Asset growth | 总资产 / 上期总资产 − 1 | 会计资产规模的扩张速度 |
| **现金流/资产** Cash flow to assets | 经营活动现金流 / 总资产 | 相对规模的经营现金创造能力 |

**代入数字（假设）**：某公司一个季度营业收入 1 亿元、净利润 2000 万元，利润率 $= 2000/10000 = 20\%$；若总资产 5 亿元、股东权益 2 亿元，账面杠杆 $= 1 - 2/5 = 60\%$（讲义未给具体公司的真实财务数字，这里用整数假设只演示怎么代入）。

> **Keep in mind（讲义 p.38）**：「These are **candidate features for teaching**, not a claim that each one predicts AAPL's next-week active return.」

**🎙️ 课堂补充（`01:51:42`–`01:54:28`）**：教授把这一段直接接到了**案例作业**上：
> 「in the second half of this course you are going to investigate a lot of fintech companies… many of them are **public companies**. …you can [pull] a lot of [their] financials… **The [analysis] I expect from you: you should have some number analysis for the company you introduce.**」
> 他举的例子是 **MicroStrategy（现更名 Strategy）**——那家大量持有比特币的公司：「What will happen to Strategy if there's a bull market for Bitcoin next year?」
> 还回答了学生的提问：**CityU 有 Bloomberg / Wind 终端，但要去机房，本课不需要**（`01:54:28`）。

**所以呢**：价格、宏观、财务三类数据的时点规则都讲完了；下一节把它们真正合并成一张能拿去建模的特征表。

---

#### 2.6.4a 四个比率与四幅图怎样核对（讲义 p.37–38；💡 完整补例）

先把输入与分母摆清楚。下面金额是本节同币种“万元”的假设例，收入/净利/现金流为期间流量；资产/权益为期末存量。

| 项目 | 万元 | 角色 |
|---|---:|---|
| 收入 | 10000 | 利润率分母 |
| 净利 | 2000 | 利润率分子 |
| 本期资产 | 50000 | 杠杆/现金比率分母 |
| 权益 | 20000 | 资产中权益部分 |
| 上期资产 | 40000 | 增长比较起点 |
| 经营现金流 | 2500 | 现金流比率分子 |

1. 利润率：2000/10000=20%，读“每100元收入留下20元净利”。
2. 账面杠杆：(50000−20000)/50000=60%，读非权益索取权占资产60%；不只指有息债。
3. 资产增长：50000/40000−1=25%，比较两期资产，不比较两期收入。
4. 经营现金流/资产：2500/50000=5%，读期间经营现金相对期末资产规模。

单位相除抵消，分母为零时该项不可算；季度与YTD、跨公司会计口径必须确认。讲义四图没有资产增长图，不能把四个比率硬配四幅图；缺原季度表只保留原图近似量级，不画假真实曲线。

同币种单位“万元”，假设收入 10000、净利 2000、资产 50000、权益 20000、上期资产 40000、经营现金流 2500。先确认每列是同一公司同一期，收入/净利/现金流是期间流量，资产/权益是期末存量；再核季度与 YTD 不能混用，最后按各分母计算。

利润率 $2000/10000=0.2$；由资产=负债+权益，账面杠杆 $(50000-20000)/50000=0.6$，含非权益索取权而不只计有息债；资产增长 $50000/40000-1=0.25$；现金流/资产 $2500/50000=0.05$。单位抵消后分别为 20%、60%、25%、5%。输入 6 个水平量输出 4 比率，分母为 0 则该项 NA 并报告；负权益可能让杠杆大于 1，是业务含义而非必然软件错误。跨公司会计口径不同或季节性强，会使同样比率难以直接比较。

p.37 四图横轴均为 **2025Q1→2026Q1**：左上收入/净利柱的纵轴 USD billions，区分金额与比例；右上利润率约 0.25–0.29，即每美元收入约产生 0.25–0.29 美元净利；左下账面杠杆约 0.71–0.80，不能误读为“股价风险 80%”；右下经营现金流/资产约 0.07–0.14。第四季度收入/利润与现金流比例较高，后续回落。这是源审读图的**近似量级**，没有原季度表，不声称精确财务数复算。四图并没有资产增长图，不能将四个公式与四幅图一一强配。

**迁移题**：净利不变、收入变为 20000，利润率是多少？权益降到 −1000、资产仍 50000，账面杠杆为何超过 1？
<details><summary>答案（笔记补充）</summary>
利润率降为 10%；杠杆 $1-(-1000/50000)=1.02$，表示负权益对应的非权益索取权超过账面资产，并不等于公式算错。应回查亏损累积和会计口径。
</details>

**所以呢**：先确认图在量金额还是比率，再问这些候选变量有没有样本外预测价值；图上升不等于下周股价必涨。

---

### 2.7 无泄漏地造预测变量

讲义 p.42 是本节标题分隔页 **“Construct Predictors without Leakage”**，不含独立公式或题目；它给 p.43–48 的预测时钟、变量公式、代码、三行手检和五种泄漏路径划定主题。以下从 p.43 的具体时钟开始。

#### 2.7.1 一行数据可以装三类信息（讲义 p.41）

前面几节分别讲了价格类、宏观类、财务类数据各自的时点规则；真正要拿去建模时，这些数据要合并成一张**特征表（feature table）**——一行代表"一个预测期"，列是各个预测变量加上目标收益。麻烦在于：同一行里的几列，"新鲜度"完全不同——价格几乎实时可知，财务滞后一个季度，而目标收益压根还没发生。讲义 p.41 用一行示例，列出这一行里装的五类列各自的时点规则：

| 列 | 来源 | 时点规则 |
|---|---|---|
| `mom20d_rank` | 日频复权价 | 只用到**上一周为止**的数据 |
| `rv20d_rank` | 日频收益 | 窗口**结束于预测周之前** |
| `profit_margin` | 财务报表 | **归档日之后**才可用 |
| `market_return` | SPY 或市场指数 | **在预测周 t 内实现** |
| `active_return` | 个股收益 − 市场收益 | 个股减市场 |

> **Keep in mind（讲义 p.41）**：「The row is labelled by the **forecast week**; every predictor must already be known **before that week's return begins**.」

**💡 换个说法（笔记补充）**：这张表的三类信息各有各的"可知时刻"——价格类几乎是实时的，财务类落后一个季度，而目标收益是**唯一一个属于未来的东西**。把它们放进同一行的唯一合法方式，就是让前三类全部停在同一条线之前。

**所以呢**：知道了特征表里各列的"新鲜度"不同，下一节给出三个具体会写进代码的预测变量，看这条规则怎么落到公式上。

#### 2.7.2 三个周频预测变量（讲义 p.44）

§2.5.1 的预测时钟说的是抽象规则；这一节给出三个具体的、真正会写进代码的预测变量，全部只用**第 t 周之前**的价格算出来（记号沿用 §2.5.1：$P_t$ 是第 $t$ 周的价格，$r_t$ 是第 $t$ 周的收益）：

| 变量 | 在第 t 周之前就已知的公式 | 图上应该看到什么 |
|---|---|---|
| **4 周动量** | $P_{t-1} / P_{t-5} - 1$ | 短周期的趋势与反转 |
| **4 周波动率** | $\sqrt{52} \cdot \operatorname{sd}(r_{t-4}, \dots, r_{t-1})$ | 变化中的周度风险 |
| **4 周均线偏离** | $P_{t-1} / \bar P_{t-1,4} - 1$ | 距离近期趋势有多远 |
| （目标）**周收益** | $P_t / P_{t-1} - 1$ | 噪声很大的结果，以及方向对不对 |

**代入数字**：假设第 $t-1$ 周（上周）收盘价是 105 元，第 $t-5$ 周（4 周前）收盘价是 100 元，4 周动量 $= 105/100 - 1 = 5\%$。注意最新只用到 $t-1$（上周），**不含第 $t$ 周**——因为第 $t$ 周的价格要到本周收盘才知道，提前用了就是下一节说的"数据泄漏"。

> **Keep in mind（讲义 p.44）**：「Each of the three has a formula and a window. **Write both down now, because Class 3 re-estimates them and the definitions must not move.**」

**⚠️ 注意讲义内部的一处记号切换**：p.43 用的是「x_t → r_{t+1}」（行按 t+1 标注），p.44/46/47 用的是「预测变量停在 t−1 → 目标 = P_t/P_{t−1}−1」（行按预测周 t 标注）。**两套记号描述的是同一件事，但容易看晕。** 建议统一记成一句话：**"这一行的目标收益是哪一期，这一行所有预测变量就必须停在那一期开始之前"**。

**所以呢**：公式定下来了，下一节看它们怎么变成真正能跑的 Python 代码——这一步最容易在"挪一格"这个细节上出错。

#### 2.7.3 代码怎么落地（讲义 p.46）

§2.7.2 给了三个预测变量的公式；这里看它们怎么变成五行真正能跑的 Python 代码——**关键不在语法本身，在每一行有没有把"只用 t 之前的信息"这条规则真正落实**：

```python
price        = aapl["Close"].resample("W-FRI").last()
return_1w    = price.pct_change()
momentum_4   = price.pct_change(4).shift(1)
volatility_4 = return_1w.rolling(4).std().shift(1) * 52**0.5
target       = return_1w
print(momentum_4.head())
```

**逐行说明**

| 行 | 在干什么 | 时点上为什么这么写 |
|---|---|---|
| `.resample("W-FRI").last()` | 把日频价格压成**周五标注**的周频价 | 对应六项规格第 2 项的"频率" |
| `.pct_change()` | 相邻两期的**简单收益** | 与 p.19 的定义一致 |
| `.pct_change(4)` | 跨 4 期的涨幅 $P_t/P_{t-4}-1$ | 这是**未滞后**的原始动量 |
| **`.shift(1)`** ★ | **整列往后挪一格** | 这一格落实目标行的尾窗映射，但不能替代公开时点、版本和样本池检查：挪完之后，第 t 周那行拿到的是 $P_{t-1}/P_{t-5}-1$，**不含第 t 周的价格** |
| `.rolling(4).std()` | 4 期滚动标准差 | 注意是**尾部**窗口，不是居中窗口（对应 p.48 泄漏路径 ②） |
| `* 52**0.5` | 乘 √52 **年化** | 周频 → 年化。月频要乘 √12 |

> **Keep in mind（讲义 p.46）**：「Codex may create **one object per line** so that the calculation is easy to check. In class, inspect the returned columns and timing rather than typing the syntax.」

**💡 验证（笔记补充）**：课程给的 `spy_monthly_features_240m.csv` 完全遵守了这套规则，且**可以逐项验算**：
- `volatility_3/6/12` = $\operatorname{sd}(r_{t-k},\dots,r_{t-1}) \times \sqrt{12}$（样本标准差，`ddof=1`）——与复算在浮点容差内一致（`L01_04`：≤ 2.1e-15）
- `momentum_3/6/12` = $P_{t-1}/P_{t-k-1} - 1$（用 SPY 价格）——与复算在浮点容差内一致（`L01_04`：≤ 4.7e-16）
- `ma_gap_3` = $P_{t-1}/\text{mean}(P_{t-3..t-1}) - 1$——与复算在浮点容差内一致（`L01_04`：≤ 3.7e-16，`ma_gap_6/10` 同）
- `term_spread_lag1` = 宏观表的 `term_spread` 恰好滞后 1 个月；`unemployment_lag2` 恰好滞后 2 个月——索引对齐复核为精确匹配（`L01_04`；其余浮点列仍按容差读）。

**这些核对证明当前快照的计算窗口与所述公式一致，不认证历史发布时点与 vintage。** 包中没有宏观发布日期和历史版本，不能据此称所有 15 列都通过 point-in-time 验收。

**所以呢**：代码写对了不代表结果对了；下一节给出验证窗口方向最直接的方式：拿三行数字出来用手核对；它不能代替发布时点、历史版本与样本池核查。

> 📁 **代码**：[`code/L01_data/04_leakage_audit.py`](../code/L01_data/04_leakage_audit.py) —— 15 个预测变量逐列按"只用 t−1 及更早"的规则重构，最大误差 2.1e-15；同一套验算对 7 种故意做错的构造（不滞后、居中窗口、ddof=0、收益连乘……）全部报出 ≥ 1.3e-2 的误差，说明"误差为 0"不是巧合（`L01_04`）
> 💡 原辅助图证据文件保留；本轮正文用可编辑表格与流程图解释机制。
> 📁 每个特征的时间窗画成甘特图：[`code/L01_data/05_prediction_clock.py`](../code/L01_data/05_prediction_clock.py)（`L01_05`，图见 §2.5.4）

#### 2.7.4 三行手检：验证窗口方向的最后一道防线（讲义 p.47）★

挑三个连续的预测周，**用手核对**：

| 预测周 | 预测变量里允许出现的信息 | 存为目标的收益 |
|---|---|---|
| $t-1$ | 截至第 $t-2$ 周收盘且决策 cutoff 前已公开的值 | $P_{t-1}/P_{t-2} - 1$ |
| $t$ | 截至第 $t-1$ 周收盘且决策 cutoff 前已公开的值 | $P_t/P_{t-1} - 1$ |
| $t+1$ | 截至第 $t$ 周收盘且决策 cutoff 前已公开的值 | $P_{t+1}/P_t - 1$ |

讲义 p.45 把它写进了指令模板：「show **three consecutive rows with every source price used in the calculation**」。

**⚠️ 常见误解**：❌「我看了代码，`shift(1)` 写了，所以没问题」→ 讲义的整节存在意义就是反对这一点。`shift` 的方向、`pct_change` 的期数、`rolling` 是否居中——三者任一处错，代码都照跑不误。对 `shift`、`pct_change` 和 `rolling` 的窗口方向，**把三行数字摆出来对着价格算一遍是最直接的确认**。它不能认证宏观发布日、财报 vintage 或历史成分股；那些仍要查事件时间和点时数据。

**所以呢**：窗口手检是验证窗口方向的最后一道防线；发布、版本与样本池仍须另查。如果一开始就只用自己算得出来的价量指标，是不是就能完全避开"发布滞后"的问题？下一节教授给了答案。

#### 2.7.4a 三行从输入窗口到最终特征（💡 笔记补充）

三行核对要分两张表：先看过去窗口，再看模型拿到的特征与未来目标。两张都按目标周5/6/7连接，不能只按行序猜对应。

| 目标周 | 动量两端源价 | 波动源收益 | 目标是否已知 |
|---|---|---|---|
| 5 | $P_4/P_0$ | $r_1\ldots r_4$ | 未知 |
| 6 | $P_5/P_1$ | $r_2\ldots r_5$ | 未知 |
| 7 | $P_6/P_2$ | $r_3\ldots r_6$ | 未知 |

周5→6时移出最老$r_1$，加入刚实现的$r_5$，重新求均值和样本方差。$r_6$不进入输入。4周动量的两端相隔4个区间，所以需要5个周价格，波动则需要4个已经实现的收益。

图的箭头是从价格对象到合法预测行的控制/数据推进。“完整窗口”否分支保留NA；cutoff不合法则停止。用目标周5走是分支时，最终输出过去窗口算出的三特征，以及只用于事后核对的−5%目标。

文字替代：尾窗计算→后移绑定目标周→检查源时刻→输出核对行。图增加的公开时点停止出口是笔记补充检查；`shift`本身只挪行，不会执行公开时刻审核。

<details><summary>读图自测：只改未来P5，目标周5的动量会变吗？</summary>

不会，周5动量只用了P4/P0；会变的是周5实现收益，周6以后输入才可能吸收新P5。

</details>

要预测周 $t$，必须先列出截至 $t-1$ 已完成的价格和收益。本例周价 $P_0\ldots P_7=[100,110,99,108.9,119.79,113.8005,125.18055,137.698605]$；由相邻比值得 $r_1\ldots r_7=[0.1,-0.1,0.1,0.1,-0.05,0.1,0.1]$。单位是任意一致货币，收益为 decimal。为了避免把金额和比例挤在同一格，先按目标周列来源窗口，再单独列计算结果：

| 目标周 | 动量来源价格 | 波动来源收益 | 均价来源价格 |
|---|---|---|---|
| 5 | $P_0,P_4$ | $r_1,r_2,r_3,r_4$ | $P_1\ldots P_4$ |
| 6 | $P_1,P_5$ | $r_2,r_3,r_4,r_5$ | $P_2\ldots P_5$ |
| 7 | $P_2,P_6$ | $r_3,r_4,r_5,r_6$ | $P_3\ldots P_6$ |

再读计算结果与事后目标：

| 目标周 | 动量 | 年化样本 sd | 均价 | 偏离率 | 实现目标 |
|---|---:|---:|---:|---:|---:|
| 5 | 19.790% | 72.111026% | 109.4225 | 9.474742% | −5% |
| 6 | 3.455% | 74.330344% | 110.372625 | 3.105729% | 10% |
| 7 | 26.445% | 54.083269% | 116.9177625 | 7.067179% | 10% |

以第 5 周决策为例，先用已实现的前四周收益求风险：

1. 平均为 $0.05$，偏差为 $[0.05,-0.15,0.05,0.05]$。
2. 平方后相加，得到 $0.03$。
3. 除以 $4-1$，样本方差为 $0.01$；再开方，周波动为 $0.1$。
4. 按周频年化假设乘 $\sqrt{52}$，得到年化波动。

从第 5 周向第 6 周滚动时，移出最早的 $r_1$，加入已实现的 $r_5=-0.05$。此时 $r_6$ 还未知，不能进入输入。

MA gap 比较的是价格与均价。四周动量则要用相隔四周的价格，因此需要 5 个价格点；不能将这两种窗口混为一谈。

代码状态对应为：日价→`resample("W-FRI").last()` 的周价 Series→`pct_change(fill_method=None)` 的相邻简单收益→各尾窗计算→`shift(1)` 后按目标周标行→四列特征/目标表。`shift` 只是挪行，既不核公开时间也不补暖机历史；开始不足 4 个完整已知收益时波动 NA，动量没有第五个端点也 NA。

不能以未来值前填。周五是假日时 `.last()` 取周内最后可见值，标签周五不等于真实交易在周五发生；须保留源交易日。

outer join 按日期并集拼市场会产生跨市场假日 NA，不能默认为同时交易或静默插值。

```mermaid
flowchart TD
 A["排序唯一日价，保存源日与口径"] --> B["周末标签取周内最后已知价"]
 B --> C["相邻收益与尾窗三特征"]
 C --> D{"完整窗口？"}
 D -->|否| E["保留 NA，等待更多过去数据"]
 D -->|是| F["后移一行，绑定目标周"]
 F --> G{"各源日均在 cutoff 前？"}
 G -->|否| H["停止并更正窗口/日期"]
 G -->|是| I["输出三行源价、特征与目标"]
```

信号在周末收盘后才算出，真实交易只能用随后可成交价；若用刚刚结束的同一收盘价成交，应披露理想化收盘撮合假设。表中 $P_t/P_{t-1}-1$ 是教学 close-to-close 目标，换成下一开盘入场必须重定义持有期收益，不能拿旧收益回报真实成交业绩。

失败：居中窗包含未来；删 shift 使特征偷用目标端价；缺失前填可能制造假零收益；四期很短使异常值主导波动。对应修正分别是尾窗、核行标签、保留缺失并回源、比较预先设定长窗（代价是响应慢）。这些不是由模型调参补救。

**迁移题**：① 仅改未来 $P_5$ 为 120，行 5 哪些特征变化？② 把 `.shift(1)` 删除，坏状态从哪一步开始？
<details><summary>答案（笔记补充）</summary>
① 行 5 所有特征不变，只有该行实现目标改变；行 6 将重新吸收 $P_5/r_5$。② 未后移的动量在目标行使用 $P_t$；程序语法可合法，但源日核对不通过，停止在目标周映射。
</details>

**所以呢**：三行算例检验窗口，发布/vintage 检验可知时点；两种证据缺一不可。


#### 2.7.5 🎙️ 自己造技术指标：一条讲义没写透的策略（01:56:14–02:00:19）

教授给了一条实操上非常重要的判断：

> 「For macro variables, macro predictors, financial predictors — yes, **we need to wait a few more weeks** to use the data. **But can we construct predictors ourselves? Yes, we can.** …you can calculate a lot [of] technical indicators… **And in this way there will be [no] data leakage, because you can [compute] everything [on] your own.**」

**💡 换个说法（笔记补充）**：宏观和财务数据的时点风险来自**外部发布流程**——你无法控制别人什么时候发布。而价量派生的技术指标（动量、波动、均线偏离）**完全由你自己从历史价格算出来**，只要窗口不越界，就天然不存在"发布滞后"问题。这解释了为什么本讲的三个示范变量全是价量类的。

他还演示了怎么用 AI 扩充变量池：直接问「Can you list commonly used technical predictors, top 30?」并坦承「for those top 30 predictors, **I don't know 20 of them**. But it is okay, because you are going to use a high[-]dimension model」（`01:57:55`）。→ **这就是 ML 板块的动机：变量多到人读不完，才需要机器去挑。**

**⚠️ 常见误解**：❌「自己算就一定没泄漏」→ 讲义 p.48 的路径 ②（居中滚动窗口）和 ④（用未来值填缺失）恰恰是"自己算"时最容易犯的。**自己算只是免疫了"发布滞后"这一类泄漏，不是免疫全部。**

**所以呢**：怎么造无泄漏的预测变量讲完了；下一节回到样本本身一个更根本的问题——如果连"当时有哪些股票"都是用今天的名单去凑的，特征造得再对也没用。

---

### 2.8 ★★ 冻结样本池与生存者偏差（讲义 p.24–25）——教授明示的考题

#### 2.8.1 课件原例：156 周的横截面（讲义 p.24）

讲义 p.24 是一张热力图：**每一行是一只股票，每一列是一个预测周，颜色表示该周收益**（色阶在 ±15% 处截断）。样本是 **2023 年 7 月的恒生科技指数（HSTECH 30）成分股**，且**这份名单在 156 周里始终不变**。

**🎙️ 课堂补充（`01:25:43`–`01:27:28`）**：教授点了成分股名字——**腾讯（0700.HK）、阿里巴巴、美团、京东、小米**——并说明为什么要冻结：
> 「if you happen to know those index[es], they change their stock list from time to time. Some stocks can [be] included, some stocks get excluded… **You will not have the same 30 stocks all the time.**」
他还教了怎么读这张图：整列偏红 = 港股大涨的一周；整列偏蓝 = 大跌的一周。

**所以呢**：这张热力图用的是冻结不变的名单；讲义马上拿它出了一道单选题，专门考"如果不冻结会怎样"。

#### 2.8.2 🔴 讲义 p.25 的选择题——教授明说这是他设计的考题

上一节的热力图用的是冻结不变的 30 只成分股；讲义 p.25 接着这张图出了一道单选题，考的是“如果不冻结、退市了就找新公司来替补，会出什么问题”。教授当堂明说这道题就是他为考试设计的原题。

<details><summary>讲义 p.25 完整英文原题、全部选项与 Discuss</summary>

**Multiple-Choice Question: What Does a Frozen Universe Protect?**

A researcher starts with the July 2023 HSTECH 30 constituents. When one stock delists, it is replaced by a company that joined the index in 2025 so that every week still has 30 stocks. What is the main problem?

A) Future membership information changes the historical investment universe.

B) Weekly returns can no longer be computed for any surviving stock.

C) The replacement automatically removes all extreme returns.

D) The market index must become equally weighted.

**Discuss:** What should the frozen panel record after the original constituent delists, and why?

</details>

中文限定词：`starts with` 固定 2023-07 起点名单，`joined in 2025` 是未来信息，`main problem` 只选最核心问题。来源地位：A 由课堂讲评确认；Discuss 的具体退市收益处理仍须按可验证来源，不能猜 0 或 −100%。

中文题意与选项如下：

> 一位研究者以 **2023 年 7 月**的 HSTECH 30 成分股为起点。当其中一只股票退市时，他用一家**2025 年才加入指数**的公司替补，好让每一周都还是 30 只股票。**主要问题是什么？**
>
> **A) 未来的成分股信息改变了历史投资范围**
> B) 存续股票的周收益再也算不出来了
> C) 替补会自动剔除所有极端收益
> D) 市场指数必须变成等权重
>
> **Discuss**：原始成分股退市之后，这个冻结面板应该记录什么？为什么？

**✅ 正确答案：A**

**English reference answer**: A is correct because 2025 membership was not known in July 2023, so the replacement changes the historical investable universe with future information. B, C, and D do not follow. After a constituent delists, keep its verified terminal return or liquidation treatment, record the exit, and leave later panel entries missing rather than replacing it with a future member. If the terminal value is unavailable, mark the result unresolved instead of inventing zero or −100%.

**🔴 教授的原话（`01:27:47`）**——这是本讲可信度最高的一条：
> 「if someone asked me **what might be the question you see in the exam, this is one of the exam questions I design.**」

**教授对每个选项的讲评（`01:30:24`–`01:31:40`）**：
- **A 对。** 课堂 `01:29:47` 说明不能用未来信息改变历史投资范围，因为当时不知道谁会在 2025 年加入。IPO（首次公开发行上市）例子只说明 2026 年才上市的股票不能被后来塞进 2023 年可交易池；它不表示公司当时不存在或无人知道。
- **B 错**：任何在指数里（甚至被剔除的）股票，收益都照样算得出来。
- **C 错**：「The replacement will [not] remove extreme returns… they simply just change the stock list.」他还举了反例——2025 年涨了几十倍的股票进了 CSI 300 成分，替换恰恰会**引入**极端收益。
- **D 错**：「**most index[es], they are [value]-weighted** — bigger companies take higher weight, smaller compan[ies] take lower weight. If you [own] Alibaba, you take 8%; [others] 0.0X%.」

**💡 "Discuss" 那问的参考答案（笔记补充）**：冻结面板应当**如实记录该股票退市这件事本身**——保留它直到退市日，退市当期给出退市收益（或按规则处理），之后该行**留空而不是替补**。用后来的成分股填坑，等于把"2023 年我不可能知道的信息"塞回了 2023 年。

**所以呢**：这道题的正确答案（A）背后是一个比"选择题"更大的原则——生存者偏差，下一节把它说清楚。

**💡 冻结面板的可执行补例**：初始名单 A/B/C，三周历 1/2/3。周 2 B 退市，周 3 D 加入指数。状态始终保留 A/B/C 三个 ID；周 2 B 的退市损益必须查可验证的最后可交易价/清算款，未知则标待核，不填 0；周 3 B 不可交易则留 NA、保存退出事件，不让 D 填进 B 的历史格。输出 3×3 历史面板及退市事件/缺失原因表，处理完最后周停止。若想研究动态成分池，那是另一个预先定义、按当时公告更新名单的研究目标，不能悄悄替换冻结任务。

流程为“保存期初名单→建立固定股票×周历→合并当时价格→遇退出查终止损益→退出后 NA→输出固定面板”，不以活到今天筛选 ID。失败一是删掉 B 使损失消失，二是事后把 D 前填进历史。**变式题**：若 B 周 2 最后价值从 10 变 2，能删掉它避免极端值吗？
<details><summary>答案（笔记补充）</summary>
不能；经来源确认的 −80% 是真实退出风险，应保留并说明。未知清算款则明确资料受阻，不能猜 −100% 或 0。
</details>

#### 2.8.3 生存者偏差是什么、为什么它是同一件事

**是什么**：只保留"活到今天"的样本，导致历史业绩被系统性高估。因为死掉的（退市、破产、被剔除）恰恰是表现最差的那批。

**与前视偏差的关系**：**生存者偏差是前视偏差的一个特例**——"谁活下来了"这件事本身，就是一条未来信息。

**⚠️ 常见误解**：❌「我用的是真实历史数据，所以没问题」→ 只要**成分股名单**是今天下载的，你的历史数据就已经被未来污染了。讲义 p.13 的脚注说得很清楚：「Research needs point-in-time data with documented revisions and **historical constituents**.」

**所以呢**：数据本身的两个陷阱（预测时钟、冻结样本池）都讲完了；下一节换一种完全不同的排查方式——不看公式，只看图。

---

### 2.9 用图诊断数据（讲义 p.49–53）

#### 2.9.1 四张图，四个不同的问题（讲义 p.49）

前面几节都在讲"怎么把数据做对"。先保留讲义的完整英文四问，再用中文逐图回答。

<details><summary>讲义 p.49 英文原题（四图四问，无选项）</summary>

**Four Plots, Four Different Questions**

1. **Price through time:** Did the download cover the intended sample? Are adjustments plausible?
2. **Returns through time:** Are there extreme observations, gaps, or suspicious zeros?
3. **Rolling volatility:** Does risk vary through time as expected?
4. **Predictor versus target:** Is the relation visible, nonlinear, dominated by outliers, or simply weak?

</details>

中文限定词：`plausible` 是“看起来合理但仍须回源”，`rolling` 要写窗口终点，`dominated by outliers` 是少数极端点主导图形。原题没有官方答案，下文是基于本讲图的参考判断。

这一节换个角度——数据做完之后，**用眼睛看**是发现问题最快的方法，比等模型跑完再排查要快得多。讲义 p.49 给了四种图，每种回答一个不同的问题，画错了图就等于问错了问题：

| 图 | 它回答的问题 |
|---|---|
| **价格随时间** | 下载覆盖了想要的样本吗？复权看起来合理吗？ |
| **收益随时间** | 有没有极端观测、缺口、或可疑的零值？ |
| **滚动波动率** | 风险是否如预期般随时间变化？ |
| **预测变量 vs 目标** | 关系可见吗？是非线性、被离群点主导、还是干脆就很弱？ |

**四问的示例判断（讲义 p.49；以本讲现有图为证，不把“图上没看到”写成统计检验）**：① 价格图先查 2006-07 至 2026-06 是否覆盖目标 240 个月，再回原始价格和公司行动核对复权；曲线平滑不等于复权正确。② 收益图上 CSI 300 的 2008 年危机月明显极端（§2.9.2），应查是否真实事件，并逐月检查缺口 / 可疑零值，而非直接删点。

③ 滚动波动率应在危机期抬高、平静期回落；若用来预测下月，窗口必须截止于预测日之前。④ 预测变量与下月收益的散点云很散（§2.9.3），肉眼看不出强关系；不能因为分箱后线略上升就断言样本外可预测。

**English reference answers（逐图）**: (1) Check start/end dates and corporate-action adjustments against raw data. (2) Investigate extreme returns, calendar gaps, and suspicious zeros before deleting anything. (3) Confirm that rolling risk rises and falls over time and that its window ends before the forecast period. (4) Treat a weak or outlier-driven scatter as diagnostic evidence only; it does not establish out-of-sample predictability.

> **Keep in mind（讲义 p.49）**：「Each plot answers one question. **Decide which question you are asking before you request the chart.**」

**🎙️ 课堂补充**：教授的版本更直白——「plot, plot and plot」（`02:06:31`），且他反复演示了同一个动作：**画出来之后，先问"这个形状合不合理"**（`01:12:22`、`01:22:11`）。

**所以呢**：知道了四种图各自回答什么问题，下一节直接看讲义已经画好的六页成品图，练习怎么读它们。

#### 2.9.2 讲义的六页成品图在讲什么

上一节讲的是"该画哪种图、每种图回答什么问题"；这一节直接看讲义已经画好的六页图，每张图对应哪个市场、哪段数据、要看出什么结论：

| 讲义页 | 图 | 要点 |
|---|---|---|
| p.20 | 三市场归一化价格（2006-07 = 100）＋ 12 个月滚动波动率 | 20 年后 S&P 500 ≈ 590、CSI 300 ≈ 385、恒生 ≈ 135 |
| p.21 | 三市场月度**对数**收益箱线图 | CSI 300 的离群点最多、箱体最宽；S&P 500 最集中 |
| p.32 | 四张宏观图：失业率、CPI 同比、10Y 美债月均、**期限利差** | 共用同一条 240 个月日历；缺失值**保留可见** |
| p.50 | 240 个月美股预测面板：月收益 / 滞后 12 月波动率 / 滞后 12 月动量 / 动量 vs 下月收益散点 | 「compare the predictor's timing and scale with the return target **before treating any visible pattern as forecast evidence**」 |
| p.51 | 三市场**回撤**曲线 | 同样的累计收益，路径可以完全不同 |
| p.52 | 同一套预测变量配方在三个市场的不同表现 | 「Always inspect before modeling」 |

**把 p.20、p.50、p.52 的独有图义补齐**

- p.20 上图把三个市场 2006-07 都归一为 100，只能比较价格指数路径；下图是滞后 12 月滚动年化波动率。2008–2009 三者风险同时抬高，CSI 300 超过 50%；2015–2016 CSI 再现约 40% 高峰，2022–2023 恒生接近 40%。共同危机与各市场独有阶段都存在，不能用一个静态年化波动数替代整条风险路径。
- p.50 左上月收益围绕 0 高频跳动，右上滞后波动率和左下滞后动量具有连续阶段；右下动量与下月收益仍像散点云。读图要横向比较“预测变量较平滑、目标很噪”，也要纵向核单位：动量和收益是百分比，波动率是年化百分比。持续的 predictor 不等于能预测噪声目标。
- p.52 同一动量/波动配方在三市场给出不同范围与阶段：S&P 动量大致在 −40% 到 +40%，恒生约 −60% 到 +60%，CSI 300 早期动量接近 +300%；三者波动峰值时点也不同。统一代码只保证公式相同，不保证尺度、分布或模型参数可直接搬用。

**🎙️ 课堂补充：几张图的解读，教授给得比讲义细得多**

**先学会读箱线图**：中间的线是中位数。箱体下边是第一四分位数 $Q_1$，上边是第三四分位数 $Q_3$，覆盖中间 50% 的月份；四分位距为 $IQR=Q_3-Q_1$。常见默认画法先设下围栏 $Q_1-1.5IQR$ 和上围栏 $Q_3+1.5IQR$，再把两根“须”画到围栏范围内最远的实际观测，范围外的点单独标为离群点。讲义只给成图、没有保存绘图参数；这里说明的是常见默认读法，精确须端点仍须查生成代码，不能冒充课件设置已核。离群点先回查事件与数据，不能自动删除。

**① 箱线图（p.21，转录 `01:19:11`–`01:20:33`）**
> 「there are a lot of outliers for the CSI 300… you have like one, two, three, four, five **20% drop[s] in one month**… The S&P 500, it is more stable, most of them from **negative 10% to 10% per month**.」
> 他给了一条实用推论：「if you invest in a stock, **how much you can lose in a month**? …if you buy the stock market in total, then this is the maximum you might lose in the past 20 years… **So it is still manageable.** But if you buy some tiny small cap stocks, then of course it is possible to **lose 99% in one week**.」

**② 回撤（p.51，转录 `02:09:27`–`02:11:22`）**——他先讲了个笑话再讲概念：
> 「my wife would look at my account… **she never asked me how much I [make]. She only asked me how much I lose.** …So she [cares] about **drawdown**.」
> 「the CSI 300 lose more than 70%… **about 70% in 2007–2008**… for [2015] they lose like 60%… The S&P 500 during the financial crisis, they lose about **50%**, but they come back… **most of the time the drawdown is about zero**, which means that [in] the past 12 months they don't lose any money.」
>
> **就地纠正课堂口述**：按本篇 $D_t=V_t/H_t-1$ 的 running-peak 定义，`drawdown = 0` 只表示当前净值回到截至当时的历史峰值；它不能推出过去 12 个月每一期都没亏钱，也不能推出任意 12 个月区间收益非负。保留原话是为了忠实记录，计算与答题按严格定义。

**💡 实测核对（笔记补充）**：用课程数据算最大回撤 → **CSI 300 −70.8%（2008-10）、恒生 −59.1%（2009-02）、S&P 500 −52.6%（2009-02）**（`L01_02`）。教授口述的数字与数据完全对得上。

**③ 期限利差（p.32 右下，转录 `01:48:20`–`01:49:40`）**——讲义只画了图、没给解释，这段全部来自课堂：
> 「the 10-year treasury yield **minus the federal fund rate**. The federal fund rate [is] the interbank rate of commercial banks… this is the long[-]term yield, this is the short[-]term yield. **The difference [reflects] people's expectations [about] the future.** …if you [lend] your money longer term, you require higher compensation. …**We expect this guy to be always positive. But there [were] some period[s] it was negative** — that means that there might be a financial crisis, there might be an economic crisis coming.」

中文读法：期限利差就是“10 年期国债收益率 − 联邦基金利率”。例如前者 4.5%、后者 5.0%，利差为 $-0.5$ 个百分点，表示长期利率低于短期利率。课堂把负值解释为对未来增长或风险的警示信号；它不是“危机必然发生”的保证，仍需结合样本时期、其他指标和发布时点判断。

**④ 失业率的尖峰（p.32 左上，转录 `01:45:19`）**——教授把它做成了一道随堂点名题：
> 「Can anyone tell me [why] there's a spike here?」……答案：**疫情**。「we see 14% [unemployment] because people [couldn't work].」（数据实测：`UNRATE` 峰值 **14.8%**。）

**所以呢**：六页成品图看完，最后一张（p.50 的散点图）留了一个悬念——它跟前面几张不一样，几乎"什么都看不出来"。下一节专门讲这件事。

> 📁 **代码**：[`code/L01_data/02_index_20y.py`](../code/L01_data/02_index_20y.py) —— 讲义 p.20 的归一化价格与 p.51 的回撤画在同一张图里（上净值对数坐标、下回撤），三个最大回撤的数字与月份都在 stdout（`L01_02`，图见 §2.3.4）。补一句图上能看到、教授没说的：「most of the time the drawdown is about zero」只对 S&P 500 成立——恒生 2018-01 的高点到 2026-06 仍差 30%（8 年未收复），CSI 300 2007-10 的高点 19 年未收复（`L01_02`）

#### 2.9.3 ★ 散点图上"看不出规律"才是正常的（讲义 p.50 右下，转录 02:07:24–02:09:06）

讲义 p.50 右下角是"动量 vs 下月收益"的散点图，讲义只写了一句克制的提示。教授把它讲成了本讲的收官思想：

> 「can anyone tell me what patterns you have seen for this figure? **My answer is [no] pattern.** Because the signal is too small… the signal is usually **lower than 1% R²**. If you tell me you find [a pattern] in this plot, then **you are [fooling] yourself**. It is hard to recognize by your eyes.」
> 「**this makes sense to me because I know stock returns are very hard to predict.** If something [is] easy to predict, the traders will [take] all [the] profits and then it become[s] harder to predict. …**this is the market efficiency.**」
> 「But once you accumulate more predictors, **it is possible the black box machine learning can pick up a little bit.** …if you can get R² above two or three percent, many hedge funds can make huge profits.」

**🎙️ 配套的市场有效性小课（`01:01:24`–`01:02:49`）**
> 「the stock price looks like a **martingale or random walk**… **the best predictor for the stock price tomorrow is today's price.** …because I graduated from U Chicago, [in the] Chicago finance school they believe [in] market efficiency… **Eugene Fama** — this is a Nobel prize winner from Chicago… everything [known] up to today [is] already incorporated into the price. …But in reality, you always find some **[slightly] negative** [autocorrelation], so we call it **reversal**.」

**💡 换个说法（笔记补充）**：如果收益率的规律是肉眼可见的，它早就被套利抹平了。**"图上看不出东西"不是你的分析失败，而是与弱信号现象相容，但不足以证实市场有效性；小样本、噪声、非线性或错位也能造成散点很散。** 本课强调弱预测信号也值得检验；但从样本内 R² 1% 提到 2%，仍需经过样本外评价与投资约束检查。

**⚠️ 常见误解**：❌「散点图看着有点趋势，说明变量有用」→ 讲义 p.53 虽写“Ask four questions”，实际列了**五个**反问：**哪几个观测在驱动这条趋势？单位和年化对不对？滚动统计量有没有偷看未来？散点该用原始值、排序值还是缩尾值？结论有没有说清尺度、基准和预测期限？**

<details><summary>讲义 p.53 英文原题（标题写 four，实际五问；无选项）</summary>

**Read an Explanation against the Evidence**

1. Which observations drive the axes and apparent pattern?
2. Are the units and annualization correct?
3. Did the rolling statistic use only past and current data?
4. Should the scatter use raw, ranked, or winsorized variables?
5. Does the conclusion identify a scale, benchmark, and forecast horizon?

</details>

中文题意：逐项核观测、单位/年化、窗口时点、变量表示和结论范围。讲义没有给待批改的具体解释或官方答案，以下是参考判断标准。

**讲义 p.53 实为五个核对问句，逐问给判断标准**（⚪ 笔记参考解读；讲义没有提供一份待批改的具体解释文本）：

1. **哪些观测在驱动图形？** 标出极端月及样本两端，例如课程 SPY 的 2008-10、2020-03 / 04（`code/L01_data/check_exercises.py`）；比较有 / 无这些点的散点和斜率，不能看见危机点就自动删掉。
2. **单位和年化对吗？** 本课 `market_return` 是月收益，`volatility_12` 是年化的过去一年波动率；图题、轴单位及解释都要写清，不把“月收益 1%”与“年化波动率 20%”当同一时间尺度。
3. **滚动统计量有没有偷看未来？** 用于预测 $t$ 月的波动率、动量和均线差只能用 $t-1$ 及更早的价格；抽一行手算并对照生成代码的窗口边界，**仅凭成品图不能确认无泄漏**。
4. **原始、排序还是缩尾变量？** 先用未加工点诊断，再只在开发 / 验证期比较预先说明的排序或缩尾规则，报告改变了哪些极端点与斜率；不因测试图不好看才换表示法。
5. **结论有尺度、基准、期限吗？** 完整表述应指明“用截至上月底的信号预测下月 SPY 收益；图上关系弱；后续样本外成绩相对滞后 MA(12) 评价”，不能只写“散点略向上，所以值得投资”。

**English reference answers（五问）**: Identify influential observations and axis ranges; verify units and annualization; reconstruct one rolling window to exclude future data; compare raw/ranked/winsorized representations only under a predeclared development rule; and state the scale, benchmark, and forecast horizon in the conclusion. The slide supplies questions, not an official worked answer.

**所以呢**：用图诊断数据讲完了，本讲关于"怎么正确处理数据"的内容也讲完了。接下来两节看两个课上完全没讲、但仍要掌握的案例——先是一个具体的多空组合案例。

> 📁 **计算与图源**：当前纵向 SVG 的可编辑脚本是 [r2-scale.py](figures/readability-v2/r2-scale.py)，计算链另见 [`code/L02_regression/03_r2_scale.py`](../code/L02_regression/03_r2_scale.py)。图的排布为上、下两幅： 上图是真实的 SPY 月收益 vs 滞后 12 月波动率（240 个月，R² = 1.01%），下图用同一个 x 合成一个 R² = 50% 的关系，同样点数、同样坐标：R² = 1% 时拟合值的波动只有噪声的 0.10 倍，肉眼确实看不出斜率（`L02_03`）
**同尺度散点图要回答的问题**：输入和坐标不变时，样本内关系强弱会怎样改变散点的外观？

![[EF5560_Fintech_and_AI_in_Finance/notes/figures/readability-v2/r2-scale.svg]]

横轴是滞后 12 月年化波动率。散点图每个点是一对“输入 x、结果 y”；自相关则比较同一收益序列与自身滞后值，问过去收益和后来收益是否一起变化。非线性表示关系不是一条直线，OLS 直线可能看不见它。样本内只描述用于拟合的这些点；样本外是在冻结规则后用新时期检验。

横轴具体是滞后 12 月年化波动率，小数 0.20 表示 20%。纵轴是月对数收益的百分数表示；每点对应一个月，红线为样本内 OLS 拟合线，即选择一条使训练样本竖直残差平方和最小的直线。本图没有流程箭头。

**走一个点的读法**：先在横轴找到 0.20，再向上读红线的高度，这是该输入下的拟合收益。附近散点高于或低于红线的垂直距离，表示实际值与拟合值的误差。

向下看合成图：同一个输入位置的拟合趋势更陡，散点相对拟合线更集中。下图由 seed 5560 的教学构造形成，保持上图目标的均值与标准差；它不是第二份真实金融样本。

**边界与文字替代**：上图使用 2006-07 至 2026-06 的全部 240 月，样本内 $R^2$ 约 1.01%；下图构造为 50%。图只解释同尺度下关系强弱的外观，不能推导样本外表现、因果或投资价值，也不设“金融 1% 即好”的通用门槛。

**读图自测**：如果把上图的样本内 $R^2$ 提到 2%，能直接说策略赚钱吗？不能，还需独立测试、交易规则、成本与风险证据。可编辑图源为 `notes/figures/readability-v2/r2-scale.py`，输入与计算结果记录在同目录 JSON。


---

### 2.10 PDD-JD 相对价值交易（讲义 p.8、11、15、16）

**❓ 材料边界**：现有转录没有可确认的 PDD-JD 对应段。关键词 0 命中可能来自未录到、ASR 漏词或课堂没有逐页讲解，不能证明明确跳过。以下按讲义完整自学，不据此降低优先级；多空组合概念还会用于 M05。

#### 2.10.1 案例设定（讲义 p.8）

本节开始的三个小节按讲义展开一个课堂对应状态未知的案例。讲义用两家中国电商公司做了一个"押注谁更强"的具体例子：拼多多母公司 PDD Holdings 和京东 JD.com。两家公司当时都面临同一个变量——外卖业务——但处境不同：

| PDD Holdings（PDD） | JD.com（JD） |
|---|---|
| 旗下平台是拼多多和 Temu。投资论点把 PDD 视作**不在外卖竞争之内** | JD 于 **2025 年 2 月**正式上线外卖业务。新业务带来投资与执行风险，但也可能提升客流与交叉销售 |

<details><summary>讲义 p.8 英文原题与必要情境（无选项）</summary>

**PDD-JD: A Relative-Value Trade**

PDD Holdings' reported platforms are Pinduoduo and Temu. The investment thesis treats PDD as outside the food-delivery competition. JD.com officially launched Food Delivery in February 2025. The new business adds investment and execution risk, but could also raise customer traffic and cross-selling.

**The question:** Can a dollar-neutral long PDD / short JD position benefit if investors price the new food-delivery exposure more heavily into JD?

</details>

中文限定词：`dollar-neutral` 是多空名义金额相等，`benefit if` 是条件性问题，不保证盈利或因果。讲义无官方答案；下文给中英参考答案和算术条件。

> **中文题意（讲义 p.8）**：如果投资者把新增的外卖敞口更多地计入 JD 的定价，一个美元中性的“做多 PDD / 做空 JD”头寸能否受益？
>
> **English reference answer（⚪ 笔记推断）**: It may benefit only if PDD outperforms JD by more than trading and shorting costs over the holding period. Dollar neutrality does not remove every shared risk, and the historical comparison does not prove that food delivery caused the return spread.

**直接回答（⚪ 依据讲义案例的条件性结论）**：**可能受益，但不是“京东跌就一定赚”。** 等额美元头寸的下一周收益为 $0.5r_{\rm PDD}-0.5r_{\rm JD}$；只有当 PDD 的收益**高于** JD（扣交易成本和做空成本后仍高）才盈利。即使两股都上涨，只要 PDD 涨得更多也能赚；两股都下跌时也同理。讲义给出的历史回报只能演示这种相对收益的算术，不能证明“外卖业务导致了价差”或未来继续有效，因为样本窗口从 JD 上线外卖**之前**就开始（p.16）。
> **Keep in mind**：「**The position direction comes from a business hypothesis, not a price z-score.** Historical data must test the hypothesis.」

**所以呢**：设定讲完了，下一节看这个"押注谁更强"的想法具体怎么变成一个可以计算收益的组合。

#### 2.10.2 多空组合怎么算（讲义 p.15）

**做空（short selling）**先借入 JD 股票并卖出，以后买回归还；价格下跌时买回更便宜，空头盈利，价格上涨时空头亏损。因此公式里的负权重不是随意的减号，而是“JD 上涨会拖累组合、JD 下跌会帮助组合”。

只做多 PDD，你没法知道赚的钱是因为"PDD 真的比 JD 强"，还是单纯因为"中国电商这几年整体在涨"——要把后一种共同因素剔除，就得同时做空等额美元的 JD：净美元敞口为 0，但两股对共同因素的敏感度可能不同，不能保证大盘风险被完全剔除。

组合押相对表现，仍有共同风险。

讲义把这个操作写成公式，在每个周五收盘时，设等额美元权重：

$$w_t^\text{PDD} = +0.5, \quad w_t^\text{JD} = -0.5, \qquad r_{t+1}^\text{LS} = 0.5 \cdot r_{t+1}^\text{PDD} - 0.5 \cdot r_{t+1}^\text{JD}$$

多空组合先定两腿权重，再等待下一期收益实现。下表逐个说明权重和收益符号。

| 符号 | 是什么 | 已知/待求 |
|---|---|---|
| $w_t^\text{PDD}$、$w_t^\text{JD}$ | 第 $t$ 周收盘时分配给 PDD、JD 的美元权重 | 已知：固定为 +0.5 / −0.5 |
| $r_{t+1}^\text{PDD}$、$r_{t+1}^\text{JD}$ | 下一周（第 $t+1$ 周）PDD、JD 各自的收益 | 待观测 |
| $r_{t+1}^\text{LS}$ | 多空组合（long-short）在第 $t+1$ 周的收益 | 待求 |

**代入课程数据里的真实两周**（`pdd_jd_pair_example_156w.csv` 前两行，`L01_03` 用的就是这张表）：

| 周 | PDD 周收益 | JD 周收益 | 组合收益 $r^{\text{LS}}$ | 读法 |
|---|---|---|---|---|
| 2023-07-07 | +1.24% | +4.78% | $0.5\times1.24\% - 0.5\times4.78\% = \mathbf{-1.77\%}$ | **两家都涨，组合却亏**——因为 JD 涨得更多；组合赚的不是"涨不涨"，是"PDD 是否比 JD 强" |
| 2023-07-14 | +13.56% | +6.66% | $0.5\times13.56\% - 0.5\times6.66\% = \mathbf{+3.45\%}$ | 两家又都涨，这次 PDD 强得多，组合赚 |

两周都是"中国电商一起涨"，组合公式取两者的**差**；共同因素只有在两腿加载相同的条件下才完全抵消——这就是"美元中性"（dollar neutral）要达到的效果，也是"相对价值"三个字的字面意思。

每周五**再平衡**回同样的权重。

> **Keep in mind（讲义 p.15）**：「The position is **dollar neutral**, but it does **not** neutralize all China-consumer, currency, regulatory, or business risk.」

**为什么需要它（笔记补充）**：单独做多 PDD，你同时押注了"中国消费好"和"PDD 比 JD 好"。加上做空 JD 之后，第一项大致被对冲掉，剩下的主要是**相对判断**。这就是"相对价值"的含义。

**所以呢**：知道了多空组合怎么算，下一节看这个具体案例在讲义给的历史区间里，实际算出来的收益和回撤是多少。

#### 2.10.2a 两周资金账与再平衡终点（💡 笔记补充，课程真实收益）

把两腿金额放在同一张账里，才能知道为什么“两股都涨”仍会亏。初始权益100，预定每周按新权益设两腿±0.5；收益为simple，无成本教学口径。

| 状态 | 多头名义 | 空头名义 | 结算后权益 |
|---|---:|---:|---:|
| 首周期初 | +50 | −50 | 待结算 |
| 首周结算 | 多赚0.621926526 | 空亏2.387928509 | 98.233998017 |
| 第二周期初 | +49.116999009 | −49.116999009 | 待结算 |
| 第二周结算 | 按各股实现收益计算 | 保留空头负号 | 101.623887211 |

金额单位与初始100相同，名义不是收入；结算后权益成为下一次再平衡的分母。下方箭头表示持有期推进：收益实现→计算两腿损益→更新权益→再设下一期两腿，不是拿旧50永远不变。

文字替代：先借股票卖出的一腿，遇JD上涨要花更多钱买回，所以亏；每次从新权益继续，直到最后预定期间或借券条件不满足。图是含执行边界的补充版本，不说原CSV已验证真实可借券。

<details><summary>读图自测：首周亏后，第二周仍拿±50计算，可继续称固定±0.5吗？</summary>

不能。±0.5的分母是新权益98.233998017，两腿要重设成±49.116999009；仍拿50已经换了规模。

</details>

初始账户权益 100，long 名义 50、short 名义 50，净名义 0、总名义 100；这是教学资本归一化，保证金/现金安排另行假定，绝非零本金套利。第一周 PDD 0.01243853052、JD 0.04775857017：多头赚 0.621926526，空头亏 2.387928509，净损益 −1.766001983，权益 98.233998017。第一周结束重设两腿名义 $98.233998017/2=49.116999009$。

第二周 PDD 0.13557142857、JD 0.06655480984：净损益 $49.116999009\times(0.13557142857-0.06655480984)$，组合收益 0.03450830936；更新权益 $98.233998017(1+0.03450830936)=101.623887211$。读完第二周就停止，输出权益与损益账；若延长到全部 156 周，重复“旧权益定两腿→收益实现→更新权益→再平衡”，源审终值 120.622015697。不能将单次持股而不再平衡的漂移权重继续写成固定 ±0.5。

```mermaid
flowchart TD
 A["期初权益 V，设名义 ±V/2"] --> B["下一持有期收益实现"]
 B --> C["损益=V/2 乘两股收益差"]
 C --> D["更新权益与回撤"]
 D --> E{"还有期间且可借券？"}
 E -->|有| A
 E -->|无| F["输出终值/路径风险/成本假设"]
```

beta 是对市场变动的敏感度；假设 PDD beta 1.4、JD 0.8，净 beta 为 $0.5(1.4)-0.5(0.8)=0.3$，美元中性仍带市场风险。借券失败、融券费、保证金追加、不同 beta 或汇率加载都会改变可执行结果；本例 gross 收益没有认证成本后可投资性。主动收益 $r_{stock}-r_{market}$ 与超额收益 $r_{stock}-r_f$ 用不同基准：同周股票 8%、市场 6%、现金 1%，分别为 2% 与 7%，不能互换。

**迁移题**：PDD 跌 5%、JD 跌 8%，±0.5 组合赚多少？若只剩 0.3 净 beta，是否能称无市场风险？
<details><summary>答案（笔记补充）</summary>
收益 $0.5(-0.05)-0.5(-0.08)=1.5\%$，仍须扣成本；净 beta 0.3 不为 0，市场上涨 1% 的共同加载部分约贡献 0.3%，不是纯粹消除市场风险。
</details>

**所以呢**：多空组合有资金分母、有路径与执行条件；仅报终点无法说明投资者经历。


#### 2.10.3 历史结果（讲义 p.11、16）

讲义 p.11 不只给终点。两条线都从 2023-06-30 的 100 开始：PDD 在 2024 年多次冲到约 200–225，随后大幅回落再反弹；JD 先跌到约 65–80，2024 年末短暂冲到约 140，之后又走低。相对路径多次改变，不能把起终点差解释成稳定价差。原页明确这是 closing-price comparison，不含股利等 total-return 成分。

本案例的终点收益须与归一化起点、期间数和成本假设一起读；下表报讲义原结果，随后解释路径风险。

| | 数字 |
|---|---|
| 区间 | 2023-07-07 → 2026-06-26，**156 个周收益** |
| 归一化价格（2023-06-30 = 100） | **PDD 110.7｜JD 74.4** |
| 多空组合**累计收益** | **+20.6%** |
| 不含 | 股息、交易成本、融券费、融资成本 |

> **Keep in mind（讲义 p.16）**：「**The window starts before JD Food Delivery launched.** It illustrates long-short return arithmetic, but **cannot establish that food delivery caused the result.**」

**💡 讲义没告诉你的一个数字（笔记补充）**：用课程数据集 `pdd_jd_pair_example_156w.csv` 实测，这个"美元中性"组合的**最大回撤是 −38.7%**（发生在 2025-04-11；`L01_03`：−38.66%，峰 2024-01-19 净值 178.47 → 谷 109.47，峰后 64 周）。**+20.6% 的累计收益背后，是一段接近腰斩的净值曲线**，而且到 2026-06-26 终点仍处于 −32.4% 的回撤中、高点从未收复（`L01_03`）。

讲义只报了终点，没报路径——这恰好是 §2.9.2 讲的"回撤才是客户真正经历的东西"。**做作业报告业绩时，只给累计收益是不合格的。**

**所以呢**：这个案例把多空组合、美元中性与收益路径合在一起；这些概念在 M05（从预测到组合）会重新出现，课堂覆盖未知不影响本节的自学要求。

> 📁 **代码**：[`code/L01_data/03_drawdown.py`](../code/L01_data/03_drawdown.py) —— 跑一遍即可复现本节全部数字：终点 +20.62%（断言 = 讲义 p.16）、归一化终值 110.7 / 74.4（= 讲义 p.11）、最大回撤 −38.66% 与发生日期（`L01_03`）
> 💡 原辅助图证据文件保留；本轮正文用可编辑表格与流程图解释机制。

---

### 2.11 现场工作坊与失败诊断表（讲义 p.54–55）

> p.54 的工作坊可按收尾布置转为课后尝试（🎙️ `02:13:16` 后让学生自行找股票、下载和画图）；p.55 的失败诊断表没有可核的逐页课堂对应。这两种状态分开记录，均不降低自学要求。后者可帮助定位自己运行代码时遇到的失败。

#### 2.11.1 现场工作坊：三道自练题（讲义 p.54）

讲义原设计是**全班从三项中选一道**，教授现场贴 prompt、跑一遍、一起看证据；原页第 3 项后悬空 `or` 是版式缺口，不能据此编出第 4 项，也不能写成三题都要求现场运行。

<details><summary>讲义 p.54 英文原题（三选一；无选项字母）</summary>

**Live Prompt Workshop: Change One Element**

The class chooses one task for a live run:

1. compare the weekly returns of two HSTECH 30 constituents while retaining the same 156 forecast weeks;
2. add one FRED series to the 240-month macro calendar and state its release-time problem;
3. construct one additional price-based predictor from the AAPL weekly series; or

Keep in mind: First agree on the sample, variable definition, dates, and checks. I then paste the prompt, run it, and we inspect the evidence together. You do not need to type Python in class.

</details>

中文限定词：`chooses one task` 是三选一，`same 156 forecast weeks` 要保持同一预测周，新增 FRED 序列必须说明发布时点。原件无官方结果；任务 1/2 需要指定股票/序列并实际运行，以下只给可执行 prompt、验收条件和条件性答案，不编造现场输出。

三道题各对应本讲前面的一节：

| # | 题目（讲义 p.54） | 练的是哪一节 | 做的时候要卡住什么 |
|---|---|---|---|
| 1 | 比较 **HSTECH 30 成分股里任意两只**的周收益，**保留同样的 156 个预测周** | §2.4.3（156 周收益）、§2.8（冻结样本池） | 成分股名单要用**期初冻结**的那份，不能用今天的；两只股票的周历必须对齐到同一条 156 周日历 |
| 2 | 往 240 个月的宏观日历里**加一条 FRED 序列**，并**说明它的发布时间问题** | §2.6.1（参考月 ≠ 发布日） | 写清这条序列的参考期、发布滞后、是否有修订；月度序列不能前填成"实时预测变量" |
| 3 | 从 AAPL 周频序列里**再造一个基于价格的预测变量** | §2.7.2（三个周频预测变量）、§2.7.5（🎙️ 自己造技术指标） | 只能用 `t` 及之前的价格；造完用 §2.7.4 的三行手检验一次 |

**English reference answer (Task 1, conditional)**: The comparison is valid only after selecting two historical constituents, freezing the July-2023 universe, aligning adjusted Friday prices to the same 156 forecast weeks, and hand-checking sample returns. No unique numeric answer exists until the two tickers are specified.

**任务 1 可执行 prompt（未运行）**：`Using the frozen July-2023 HSTECH 30 universe, choose [ticker A] and [ticker B], build adjusted Friday prices and simple weekly returns for the same 156 forecast weeks, print first/last dates, row counts, missing weeks, and three hand-checked returns.` 条件性答案：只有冻结名单、复权口径、共同周历和三行复算都通过，才可比较；缺具体两只股票时没有唯一数值答案。

**English reference answer (Task 2, conditional)**: Preserve the 240-month calendar and missing values, but attach the selected FRED series only after its actual release time and historical vintage are known. The required lag depends on the chosen series, so no unique lag can be stated before the series ID and release calendar are specified.

**任务 2 可执行 prompt（未运行）**：`Add [FRED series ID] to the 2006-07–2026-06 240-month calendar. Preserve missing months; return the observation frequency, aggregation rule, release calendar/vintage requirement, and the first forecast month when each value is usable.` 条件性答案：具体 lag 取决于所选序列的实际发布时间与修订规则；未指定 series ID 时不能给唯一 lag。

**English reference answer (Task 3)**: Define two-week momentum for forecast week t as P(t-1)/P(t-3)-1, so every source price is known before the target week ends. Print three rows with both source dates and recompute them by hand.

**任务 3 中英参考答案：新增 2 周动量的可复算示例**（⚪ 笔记补充，参数变式；不是教授现场产物）。已讲的 4 周动量不是新指标，这里改为 $m_{2,t}=P_{t-1}/P_{t-3}-1$。一行仍按目标周标注，所用源价都早于目标结束。

| 目标周 | 最新已知价（源日） | 更早价（源日） | 2 周动量 |
|---|---:|---:|---:|
| 2026-06-12 | 307.339996338（6/5） | 308.820007324（5/22） | −0.479247118% |
| 2026-06-19 | 291.130004883（6/12） | 312.059997559（5/29） | −6.707041223% |
| 2026-06-26 | 298.010009766（6/19） | 307.339996338（6/5） | −3.035721573% |

这是课程 CSV 真实数，复算见源审 `ef-m01-source-audit/final_check.py`；显示位数经过舍入。第一行用 $307.339996338/308.820007324-1$，不能把 6/12 实现价放进去。此处只交造变量与三行时点核对，不证明预测力。选第 1/2 题还须指定股票/新增 FRED 序列；未有冻结名单或发布日期原表时不编唯一结果。

**讲义 p.54 的 Keep in mind**（原文大意）：先把**样本、变量定义、日期、检查项**四件事定下来，然后才贴 prompt、跑代码、一起看证据；「**You do not need to type Python in class.**」

💡 **这页真正在教什么**：不是三道题本身，而是**做题的顺序**——先定规格（p.10 的六项规格）再跑代码。三道题都刻意要求"保留同样的 156 周 / 同一条 240 月日历"，就是在逼你把 §2.8 的冻结样本池和 §2.5 的预测时钟当成**前置条件**而不是事后检查。

**所以呢**：知道了"先定规格、再跑代码"的顺序，下一节看真正动手时最常见的失败长什么样、以及怎么在不猜语法的情况下诊断它。

📁 **代码**：题 2 的"发布时间问题"可以直接对照 [`code/L01_data/05_prediction_clock.py`](../code/L01_data/05_prediction_clock.py) 的预测时钟图（`L01_05`）——加进去的新序列应该和图上现有的 15 个特征一样，全部落在决策线左侧。

#### 2.11.2 失败诊断表：报错时先打印什么（讲义 p.55）★

讲义 p.55 的标题是 **"If the Live Run Fails, Read the Evidence"**——现场跑失败时，**先打印证据，再猜原因**。六类失败按讲义原表整理：

| 失败类型 | 猜原因之前先打印什么 | 通常的原因 |
|---|---|---|
| **Network 网络** | 原始响应，或者那个空的 DataFrame | 数据源拒绝、限流，或什么都没返回 |
| **Ticker 代码** | 你请求的代码 vs 返回的代码 | 退市、改名，或代码补零补错（💡 如港股 `0700.HK` 少写成 `700`） |
| **Column 列** | `df.columns` | 字段改名了，或返回的是多级列（multi-level frame） |
| **Date 日期** | 首尾两个索引值**和它们的类型** | 日期还是没解析的字符串，或两套日历被拼到了一起 |
| **Type 类型** | `df.dtypes` | 数值列以文本形式到达，算术运算被静默阻断 |
| **Logic 逻辑** | 出错那一行**之前**的那个对象 | **代码跑通了，但算的不是你要的东西** |

**正常/异常输出的最小样子**

- df.columns 正常可为 Close / Volume；若出现多个 ticker 层级，先确认多级列。
- 日期 index 应像 2026-06-01 且类型为 datetime；若仍是字符串，不能可靠排序。
- 价格 dtype 应是 float64 等数值类型；若是 object，先查逗号或文字。
- 空 DataFrame 会显示 0 行，不能继续计算。方法链每一步都应保留可打印的中间对象。

**讲义 p.55 的收尾句**：「**Change one input, rerun from the top, and record the fix.** The task is to diagnose the evidence, not to guess Python syntax.」——每次只改**一个**输入、从头重跑、把修复记下来；任务是诊断证据，不是猜 Python 语法。

**⚠️ 常见误解**：❌「没报错 = 没问题」→ 表里最后一类 **Logic** 就是为此设的：它**不报错**。§2.2.4 里教授反复强调的"检查日期"、§2.7.4 的三行手检，都是在对付这一类。

💡 **本库代码库里的一次真实案例**（`L01_01`）：写 [`01_return_conventions.py`](../code/L01_data/01_return_conventions.py) 时，断言 `exp(Σr) == P_T/P_0` **失败**了。按 p.55 的做法——不猜、先打印收益文件的前两行——发现 `market_index_returns_240m.csv` 的**第一行不是 NaN 而是一个真实收益**（用了价格文件里没有的 2006-06 价格），属于表里的 **Date/Logic** 混合型：两份文件的"第 0 期"定义不同。

修复只改一个输入（首行置 0 作基期），从头重跑，断言通过；修复记录写在脚本的"关键决定"栏。

> 🔗 与 IS6400 的对照：IS6400 的 Tutorial 1 也在教同一件事的初级版（Jupyter 的执行顺序 ≠ 排列顺序，见 [[T01-Jupyter入门与Pandas基础]] §7.2）。两门课都在说：**AI 生成的代码，出错的形态和人写的不一样——最危险的是跑通了但算错了。**

---

**💡 完整失败诊断演练**：要核 July=100 的价格路径，价格只有 July/August/September 为 100/110/99，收益表 July 0.02、August 0.1、September −0.1。坏中间态将三条收益都乘入：$100(1.02)(1.1)(0.9)=100.98$，与真实终价 99 不符。

先打印日期发现 July 收益来自未保存 June 基价；只改这一项，把 July 设为基期、不计入此路径，再从头生成 $100\to110\to99$，断言终值=终价、收益个数=价格数−1。保存原输入、基期排除理由与修复；不是删除一个“不好看”的坏收益。

若目的是 June 起的投资，则须补 June 基价并另定义路径，不能用 July 基期套 June 收益。

Vibe 六步循环的停止条件是已预先写下的单位/日期/行数/关键恒等式全部核对、输出与代码已保存；不以“AI 说成功”停止。缺源数据/响应空/无法确认版本时以受阻收尾，不偷偷改 ticker 或分析目标。上述三价例的迁移：若 July 收益为 −2%，仍应按 July 基期排除它；原因是时钟，绝非收益方向。

**所以呢**：只改一个输入，是为了让修复原因可解释；重跑应能得到完整可检查输出。



### 2.12 收尾：讲义版与教授版的"记住三件事"

这一讲讲了课程结构、Vibe Coding、金融词汇、下载与检查数据、预测时钟、冻结样本池、用图诊断——内容很多，但收尾的"记住三件事"其实有**两份**，讲义写的和教授现场说的侧重点并不一样：讲义偏"操作清单"，教授偏"这门课到底想让你学会什么"。两份都要记，原因见下文。

**讲义 p.57 的版本**
1. 在用代码之前，先定义样本、变量和**信息日期**
2. 把交易日、宏观发布日、财报归档日**分开记**；用手核对一个 lead 或 lag
3. **在拟合模型之前，先用图诊断数据**

<details><summary>讲义 p.56 英文原题（四问，无选项）</summary>

**Whole-Class Check: Four Questions**

1. What does one row represent, and which date belongs to the predictor and target?
2. Are the prices adjusted, and how was that choice verified?
3. Does each macro or accounting value use its release or filing date?
4. Can the code regenerate the table and plot from a clean environment?

</details>

中文限定词：一行的粒度、输入/目标日期、复权证据、真实公开时点和从空环境复现。讲义无官方答案，以下为本库数据的条件性参考作答。

**讲义 p.56 的四个自查问题**（现场检查表，可直接用于作业）
1. 一行代表什么？哪个日期属于预测变量、哪个属于目标？
2. 价格是复权的吗？这个选择是怎么验证的？
3. 每个宏观或会计数值，用的是它的**发布日 / 归档日**吗？
4. 这段代码能从一个**干净环境**重新生成这张表和这张图吗？

**把四问用于本库数据的参考作答**（⚪ 笔记核查；课堂现场输出未保存，不能冒充教授当堂答案）：① `spy_monthly_features_240m.csv` 一行是一个**预测月**，滞后特征来自该月之前，`market_return` 是该月实现的目标；必须在代码里逐列核对窗口，不只看列名。② AAPL 文件提供 `adjusted_close`，可用来计算跨拆股 / 派息可比的收益；但仅凭这个列名还**不能证明**数据商每次公司行动都处理正确，需与原始收盘价和公司行动记录抽样对照。

③ `macro_240m.csv` 的月份标签是参考期，不是发布日；文件不含逐条实际发布日期或财报归档日，故**不能凭这张表证明所有宏观 / 会计值当时可用**，应补发布日历 / 原始归档日再核。④ “能否从干净环境重跑”需要在新环境实际安装依赖、运行代码并比对输出行数、日期、图和关键数字；存在脚本并不等于已完成这个独立验证，课堂现场产物缺失时结论应写“尚未验证”。

**English reference answers（四问）**: One row must have a declared grain and separate predictor/target dates. Adjusted prices require a named vendor convention plus sample checks against raw prices and corporate actions. Macro/accounting values require actual release/filing publication times before the cutoff. Reproducibility requires a fresh environment to rerun the code and match row counts, dates, tables, and plots; the existence of a script alone is insufficient.

**🎙️ 教授版的收尾（`02:12:27`–`02:13:41`）**——重点完全不同：
> 「**Develop a sense for numbers. That's the top priority [thing] I want [you] to learn from the course.** …**This is not the course to teach you which model is most powerful, because my answer [is] that most of them are garbage** when [applied to] stock return prediction tests.
> So it is hard to find [something] useful, but **it is important to remember some historical events and what [happened]**… all those [events] cannot be picked up by machine learning. Machine learning statistical models, **they cannot [predict a] financial crisis**.」

**🎙️ 第一周的"作业"（`02:13:16`）**——不计分，但教授明说了：
> 「after class, you can try yourself: find some stock[s] in the Hang Seng index, in the Hang Seng Tech index, in CSI 300, in S&P 500, and then **vibe cod[e]**… plot the data, see what happens, download the financial[s], see what happens. …**Take home assignment: just play with [it] yourself and then try to see if you like this kind of thing[s] or not.**」

**讲义 p.58 预告 M02**
> 「We move from constructing and checking data to asking whether a variable **improves a return forecast**. …**The next question is not whether a pattern exists, but whether it improves a decision.**」
> 三条具体目标：读散点图与拟合线而不混淆相关与预测；把简单回归、多元回归和 **12 个月移动平均基准**作比较；解读预测误差、样本外表现和跨时间的稳定性。
> → 见 [[M02-回归与样本外设计]]，以及跨课对照 [[M02-预测分析-线性回归]]（IS6400 W02，同周同主题）。

---

## 3. 一图看懂

### 3.1 本讲的骨架：三条线

```mermaid
flowchart TD
    subgraph L1["① 工具线：Vibe Coding"]
        direction TB
        A1["六项规格<br/>把任务说清楚"] --> A2["六步循环<br/>指令→跑→查→改→存"]
        A2 --> A3["🎙️ 桌面工具 + 权限分级 + 代码留痕"]
    end
    subgraph L2["② 纪律线：预测时钟 ★核心"]
        direction TB
        B1["参考期 / 发布日 / 归档日<br/>三种日期分开记"] --> B2["数据泄漏<br/>五种路径"]
        B2 --> B3["三行手检"]
        B1 --> B4["生存者偏差<br/>→ 冻结样本池 🔴考点"]
    end
    subgraph L3["③ 判断线：数感"]
        direction TB
        C1["S&P 500 ≈ 8%/年<br/>R² ≈ 1%<br/>CSI300 回撤 −70%"] --> C2["用图诊断<br/>四张图四个问题"]
        C2 --> C3["🎙️ 看不出规律<br/>不能据此证明市场有效性"]
    end
    A3 ~~~ B1
    B3 ~~~ C1
    L1 --> D["合格的特征表<br/>x_t → r_(t+1)"]
    L2 --> D
    L3 --> D
    D --> E["M02：这个变量<br/>能不能改善预测？"]
```

**这张图在说**：Vibe Coding 只是把"打字"这件事拿走了，它没有拿走任何判断。剩下的两条线——时点纪律和数感——才是本讲真正要交付的能力，也是 M02 之后所有内容的地基。

### 3.2 一个数字的一生：从事件到可用

```mermaid
flowchart TD
    A["经济事件<br/>2025 Q1 的经营"] -->|"财季结束"| B["2025-03-31<br/>文件上的日期"]
    B -->|"公司编报"| C["2025-05-02<br/>示例归档日"]
    C -->|"与决策 cutoff 比较"| D["实际公开后首个合法决策<br/>预测变量才取值"]
    B -.->|"🎙️ 参考期加 3 个月近似"| E["2025-06 月末<br/>仍须核实际公开时间与历史版本"]
    B -.->|"❌ 常见错误"| F["按 2025-03-31 匹配<br/>= 数据泄漏"]
    style F fill:#fdd,stroke:#c00
    style E fill:#ffd
```

**这张图在说**：讲义 p.39 的例子。同一份财报有四个可能的日期，参考期不能作公开日；归档须早于实际决策 cutoff，固定 lag 只是一种另行声明的近似，不自动认证合法可用。

---

## 4. 速查表

### 4.1 六项规格（写指令前对照）

| # | 规格 | 一句话检查 |
|---|---|---|
| 1 | 语言与包 | R+`quantmod` / Python+`yfinance`+`pandas`？ |
| 2 | 数据 | ticker、来源、起、止、频率，五项齐了吗？ |
| 3 | 价格口径 | 复权还是不复权？**写出来** |
| 4 | 预测时钟 | 信号何时形成？目标是哪一期？ |
| 5 | 预测变量 | 公式 + 窗口，两样都写 |
| 6 | 输出与检查 | 让它自报：维度、首末日期、行数、缺失数 |

### 4.2 三种日期 · 四类数据

| 数据 | 文件上的日期 | 合法可用时点 | 教授的保守做法 |
|---|---|---|---|
| 市场指数 | 交易日/月 | 只用更早的收盘价 | — |
| 日频利率 | 交易日 | 先聚合月均、再滞后 | — |
| 月频宏观 | 参考月 | 公开发布后 | 参考月加约 1 个月并核公开日 |
| 公司财务 | 财季期末 | 10-Q/10-K 归档后 | 参考期加约 3 个月并核公开日 |

### 4.3 五种泄漏路径 + 一条检验

| # | 路径 | 关键词 |
|---|---|---|
| 1 | 全样本标准化 | 划分前不能用全样本统计量 |
| 2 | 居中滚动窗口 | 只能用**尾部**窗口 |
| 3 | 按财季期末对齐 | 必须按**归档日** |
| 4 | 用后来的值填缺失 | 缺失就让它缺着 |
| 5 | 看完测试集再选变量 | 测试集只能用一次 |
| ✅ | **三行手检** | 挑连续三期，手工核对预测变量与目标 |

### 4.4 数感速查（考前必背）

| 量 | 数字 |
|---|---|
| S&P 500 长期年化 | **≈ 8%** |
| 美债 10Y / 中债 10Y（2026-09） | **≈ 4.8% / 1.8%** |
| 收益预测 R² | 见下方「收益预测 R² · 数字」 |
| 20 年累计（100 起投） | S&P≈600｜CSI300≈400｜恒生≈130 |
| 年化波动率 | S&P≈15%｜恒生≈22%｜CSI300≈27% |
| 最大回撤 | CSI300 **−71%**｜恒生 **−59%**｜S&P **−53%** |
| "年化 50% 的策略" | 教授的高风险警示；不能单凭数字断言欺诈 |

**收益预测 R² · 数字**

**≈ 1%**。

2–3% 是教授口述的潜在优势。

是否盈利还须验证成本、稳定性与决策规则

### 4.5 收益率口径速查

| | 公式 | 能沿什么相加 | 课程数据里谁用它 |
|---|---|---|---|
| 简单收益 | `P_t/P_{t−1} − 1` | **跨资产**（组合） | 周频文件（AAPL、PDD-JD） |
| 对数收益 | `ln(P_t/P_{t−1})` | **跨时间**（累计） | **月频文件（三个）** |

---

## 5. 双语术语卡

| 中文 | English | 考试可用的英文定义 | 首现 |
|---|---|---|---|
| AI 辅助编码 / 氛围编码 | Vibe Coding / AI-assisted coding | Describe the task in plain language, let an AI assistant write and run a small Python job, inspect the result, and revise until the output passes explicit checks. | §2.2 |
| 预测时钟 | Forecast clock | The stated rule for when a signal is formed and which future return is the target. | §2.5.1 |
| 数据泄漏 | Data leakage | Using information in a predictor that was not observable at the time the forecast was made. | §2.5.2 |
| 前视偏差 | Look-ahead bias | Evaluating a historical strategy with information that only became available later. | §2.5.2 |
| 生存者偏差 | Survivorship bias | Keeping only the assets that survived to today, which systematically overstates historical performance. | §2.8.3 |
| 冻结样本池 | Frozen universe | Fixing the index membership as of a historical date so that later membership changes cannot enter the historical sample. | §2.8 |
| 时点数据 | Point-in-time data | Data recorded as it stood on each date, rather than the currently revised series. | §2.5.4 |
| 参考期 | Reference period / observation month | The period a statistic describes — not the day investors could see it. | §2.5.4 |
| 发布日 / 归档日 | Release date / Filing date | The actual public timestamp: US 10-Q/10-K filing uses SEC records; Hong Kong listed-company announcements use HKEX ESS/HKEXnews publication rather than an assumed SFC-equivalent filing. | §2.6.3 |
| 数据修订 / 实时版本 | Revision / Vintage (ALFRED) | A current download may contain revised history rather than the vintage seen in real time. | §2.6.1 |
| 复权收盘价 | Adjusted close | A vendor-adjusted series for splits and dividends; cash dividends can offset part of an ex-dividend price fall, but do not guarantee a positive total return. | §2.3.2 |
| 拆股 | Stock split | A split changes the quoted price without creating an investor loss. | §2.3.2 |
| 简单收益 | Simple return | `r_t = P_t / P_{t−1} − 1` | §2.3.1 |
| 对数收益 | Log return | `r_t = ln(P_t / P_{t−1})` | §2.3.1 |
| 波动率（年化） | Annualized volatility | Standard deviation of returns scaled by the square root of the number of periods per year. | §2.3.4 |
| 回撤 / 最大回撤 | Drawdown / Maximum drawdown | The cumulative loss from the running peak; the part a client actually lives through. | §2.9.2 |
| 基准 | Benchmark | The reference return a strategy must beat before its performance means anything. | §2.3.3 |
| 期限利差 | Term spread | Long-term yield minus short-term rate; a negative spread is often treated as a risk warning, not a guarantee of recession. | §2.9.2 |
| 市值加权 | Capitalization-weighted | Bigger companies take higher weight in the index. | §2.8.2 |
| 动量 | Momentum | `P_{t−1}/P_{t−k−1} − 1`, the cumulative price change known before the forecast period. | §2.7.2 |
| 均线偏离 | Moving-average gap | `P_{t−1} / mean(P_{t−k..t−1}) − 1`, distance from the recent trend. | §2.7.2 |
| 主动收益 | Active return | Stock return minus market return. | §2.7.1 |
| 特征表 | Feature table | One row per forecast period (and asset), with predictors known before the period and the realized return as target. | §2.7.1 |
| 横截面 | Cross-section | The set of assets observed at one point in time. | §2.8.1 |
| 多空组合 / 美元中性 | Long-short / Dollar-neutral | Equal dollar weights long and short, so the net dollar exposure is zero. | §2.10.2 |
| 相对价值交易 | Relative-value trade | A position whose payoff depends on the relative performance of two related assets. | §2.10.1 |
| 再平衡 | Rebalance | Resetting portfolio weights to their targets each period. | §2.10.2 |
| 市场有效性 | Market efficiency | The market-efficiency hypothesis says available information is incorporated into prices; it is a testable hypothesis, not a fact proved by one scatter plot. | §2.9.3 |
| 随机游走 / 鞅 | Random walk / Martingale | A martingale has conditional expected next value equal to its current value; a random walk adds assumptions about increments. This is a model distinction, not a proven property of every asset. | §2.9.3 |
| 反转 | Reversal | The slight negative autocorrelation found in realized returns. | §2.9.3 |
| 另类数据 | Alternative data | Non-public datasets bought by investors to obtain information beyond public sources. | §2.7.5 |
| 买卖价差 | Bid-ask spread | A simple proxy for transaction cost. | §2.3 / 🎙️ 问答 |

---

## 6. 考点预判与答题框架

### 6.1 可信度分级

| 级别 | 含义 |
|---|---|
| 🔴 教授明示 | 转录中直接出现考试、题型、优先级或明确要求，并保留可核英文原话与原始时间戳 |
| 🟡 ILO 反推 | 对应 syllabus ILO / 官方 CILO，但教授没有在本段直接明示会考 |
| ⚪ 笔记推断 | 根据内容重要性、数据或题型作出的笔记判断 |

### 6.2 考点清单

| 可信度 | 考点 | 直接证据 | 对应小节 |
|---|---|---|---|
| 🔴 | 何时使用模型，而非硬核统计推导 | *"I'm the one [who is] trying to teach you when to use those model[s]… And of course you will see this in the exam."*（`04:24`） | M02–M04 |
| 🔴（M01 当堂历史；后续已更新） | M01 当堂只说手写考试与小抄待定，后续规则见表后行政更新 | *"Handwritten exam… I might allow you [to bring] one page for [a] hand written cheat sheet… I will tell you later."*（`10:20`） | §9.5 |
| 🔴 | 无编码题 | *"First of all[,] there's no coding test… Coding is not [a] [part] [of] my course at all."*（`01:15:10`） | 全篇 |
| 🔴 | MCQ 上限 60%，另有投资计算与 FinTech 简答 | *"In CTU, we are only allowed to give 60% for multiple questions."*（`01:15:22`）；*"I'll also give you some simple calculation question[s] for the investment part or some… short question[s] for the fintech part."*（`01:15:42`） | 全篇 |
| 🔴 | 冻结样本池选择题 | *"This is one of the exam questions I design."*（`01:27:47`） | §2.8.2 |
| 🔴 | 预测变量最常见错误是日期错配 | *"The mistake I see… 99.9%… that's missing the date."*（`02:00:05`） | §2.5–§2.7 |
| 🔴 | 培养数感是最高优先级 | *"Develop a sense for numbers. That's the top priority [thing] I want [you] to learn from the course."*（`02:12:27`） | §2.3.4、§4.4 |
| 🟡 | 六项数据规格、复权口径、五种泄漏路径 | syllabus ILO 1 与讲义题面 | §2.2–§2.5 |
| ⚪ | 对数/简单收益、期限利差、多空组合 | 讲义和数据的教学价值推断 | §2.3、§2.9、§2.10 |

**行政更新（后续课堂，不是 M01 当堂已定）**：M01 当堂只说手写考试与小抄待定；后续 M03 `02:53`–`03:17` 确认一张 A4、双面手写，内容不限，不许打印或用 iPad；最终执行仍以 Canvas 为准。

红级只保留上表中可直接回源的明示；合理推断不升级为教授明示。

### 6.3 答题框架

**框架 A · "这个回测有没有问题？"（最可能的题型）**

按四问顺序检查，每问一句话，能拿满结构分：

1. **样本池**：成分股名单是哪一天的？退市的怎么处理？（→ 生存者偏差）
2. **时点**：每个预测变量在目标收益开始之前就可知吗？宏观用发布日了吗？财务用归档日了吗？（→ 前视偏差）
3. **口径**：价格复权了吗？收益是简单还是对数？年化用对系数了吗？
4. **基准**：跟什么比？指数统计基准与成本后可交易产品是否区分？比较目标、期间和收益口径是否一致？

**框架 B · "给你一个数字，判断合不合理"**

1. 先确认它是什么量：收益、波动、回撤、Sharpe，还是预测 $R^2$；不同单位的百分数不互相比大小。
2. 投资业绩只与同口径的长期年化收益、波动、回撤、杠杆和成本比较；算术平均乘 52/12、路径增长用 $\prod(1+r)^{h/n}-1$、波动在适用条件下乘 $\sqrt h$。
3. 模型预测力另与基准误差和样本外 $R^2$ 比较；$R^2=1\%$ 不是收益 1%。
4. 若同类指标明显偏高 → 优先排查数据泄漏，但数值偏高本身不能证明泄漏（🎙️「if you see very good prediction, then you must [be] us[ing] future information」）
5. 若明显偏低 → 检查口径（是不是把对数当简单、是不是漏了股息）

**框架 C · "简答：这家 FinTech 公司的商业模式"（第二板块的题型）**

用讲义 p.3 的四层：**数据与获取 → 模型与基准 → 决策流程与分发 → 控制与问责**，再加一句"谁付钱、收入怎么来"。🎙️`01:16:00`：「What kind of business model they rely on? What might be the expected revenue? **Which part of the customer[s] are they earning their money [from]?**」

---

## 7. 自测

### 概念题

**1.** 一份季度报表的期末是 2025-03-31，10-Q 在 2025-05-02 归档。若你在特征表里把这份报表的利润率匹配到 2025 年 4 月的交易日上，犯了什么错？会造成什么后果？

<details><summary>答案</summary>

犯的是**按财季期末对齐会计数据**的错误——讲义 p.48 五种泄漏路径的第 3 条，属于**数据泄漏 / 前视偏差**。

**后果**：4 月的每一天，模型都在使用一份要到 5 月 2 日才存在的公开信息。回测会显示出"财务变量很有预测力"，但这个预测力完全来自于偷看未来。真实交易时这个变量根本不存在。

**正确做法（讲义 p.39–40）**：该变量在 2025-05-02 之前保持**缺失**，从实际公开时刻不晚于决策 cutoff 的那次决策开始取值，并**一直沿用到下一次归档**。
</details>

**2.** 为什么"看到一个策略年化 50%"应该先怀疑数据，而不是先高兴？给出两个量级参照。

<details><summary>答案</summary>

因为它远超任何合理的量级参照：

- **S&P 500 长期年化约 8%**（课堂百年经验量级，未说明股息口径）；
- **本讲恒生价格指数 2006-07 至 2026-06 的 CAGR 约 1.511%/年**（不含股息，239 个间隔）。

两者都是年化收益参照，但期间不同，课堂股息口径未说明，不能直接排名市场优劣。50% 连续多年明显高于这两组同单位参照，应查杠杆、回撤、成本、样本期和泄漏。

$R^2$ 约 1% 属于另一类“预测误差改善”尺度，只能用来检查模型预测力，不能与年化收益直接比较。

教授的两句原话可以直接引用：
- 「if those people can make 50 a year for multiple years, **they will not be your friend. They will disappear very, very soon**」（`51:45`）
- 「**if you see very good prediction, then you must [be] us[ing] future information**」（`01:43:57`）

**第一嫌疑：数据泄漏。** 其次才是过拟合、幸存样本、忽略交易成本。
</details>

**3.** 简单收益和对数收益各自"能沿什么方向相加"？为什么这件事在本课的数据集上特别要小心？

<details><summary>答案</summary>

- **简单收益能跨资产相加**：组合收益 = Σ(权重 × 各资产简单收益)。多空组合公式 `0.5·r^PDD − 0.5·r^JD` 必须用简单收益。
- **对数收益能跨时间相加**：`ln(P_T/P_0) = Σ ln(P_t/P_{t−1})`。算 20 年累计、画长期走势、算波动率用它更方便。

**为什么要小心**：课程 8 个数据集**两种口径混用**——三个月频文件（`market_index_returns_240m`、`spy_monthly_features_240m`、`csi300_macro_panel`）是**对数收益**，两个周频文件（AAPL、PDD-JD）是**简单收益**。而讲义 p.19 唯一给出的公式是简单收益。

**如果把对数收益当简单收益去复利累乘**，20 年下来 S&P 500 会算出 4.59 倍而不是正确的 5.87 倍——差了一大截。
</details>

**4.** `momentum_4 = price.pct_change(4).shift(1)` 里的 `.shift(1)` 删掉会怎样？为什么代码不会报错？

<details><summary>答案</summary>

删掉 `.shift(1)` 之后，第 t 周那一行的动量变成 `P_t / P_{t−4} − 1`——**它包含了第 t 周的收盘价**。而这一行的目标恰恰是 `P_t/P_{t−1} − 1`，也用到了 `P_t`。

于是预测变量和目标共享同一个价格，回归会显示出很强的"预测力"，**但那只是同一个数字在等号两边出现**。

**为什么不报错**：语法完全合法，维度也对得上。这正是讲义 p.47 说的 **Common failure**——「An AI assistant may produce **syntactically valid code with the target shifted in the wrong direction**」，以及 p.55 的第 6 类失败「**Logic: it runs, but computes something you did not specify**」。

**发现窗口错位的直接方法**：三行手检（§2.7.4）——把连续三周的预测变量、用到的原始价格、目标收益全部打印出来对一遍。
</details>

**5.** 课堂 `02:07:24`–`02:09:06` 说明散点图上“看不出规律”是正常现象。用一句话解释为什么，并说明这对 ML 板块意味着什么。

<details><summary>答案</summary>

**为什么**：教授从市场有效性的直觉解释弱信号；散点很散也可能来自噪声、少量样本或非线性，不能由图证明效率——**R² 低于 1% 时，人眼根本分辨不出来**（🎙️`02:07:58`）。

**对 ML 板块的含义**：
1. **不要用"R² 要 0.5 以上"的直觉来评价收益预测模型**。金融和营销不是一回事——营销领域数据挖掘能把 R² 从 50% 提到 60%，收益预测只能从 1% 提到 1.2%（🎙️`01:44:49`）。
2. **单个变量看不出来，不代表一堆变量组合起来看不出来**：「once you accumulate more predictors, it is possible the black box machine learning can pick up a little bit」（`02:09:06`）。这就是 M03/M04 存在的理由。
3. **评价标准必须是"相对基准的改进"，而不是绝对拟合优度**——这正是 M02 的样本外 R² 和 MA(12) 基准要解决的问题。
</details>

### 案例分析题

**6.**（讲义 p.25 原题，🔴 教授明示这是他设计的考题）一位研究者以 2023 年 7 月的 HSTECH 30 成分股为起点。当其中一只股票退市时，他用一家 2025 年才加入指数的公司替补，好让每一周都还是 30 只。**主要问题是什么？** 并回答讲义的追问：**原始成分股退市之后，这个冻结面板应该记录什么？为什么？**

<details><summary>参考思路</summary>

**选 A：未来的成分股信息改变了历史投资范围。**

**为什么是 A**：2023 年 7 月做决策的投资者**不可能知道**哪家公司会在 2025 年加入指数——那家公司当时可能还没上市、或者规模还不够。把它塞进 2023 年的样本，等于用未来信息重新定义了历史的可投资范围。这是**前视偏差**，而且它的特例形式是**生存者偏差**：能在 2025 年被选入指数的公司，通常是这两年表现好的公司。

🔴 教授原话：「you cannot use future information to predict the historical investment universe, because **you don't know [which] stock will be added in 2025**… future information cannot be used if you want to backtest your strategy.」（`01:29:47`）

**为什么排除其余三项**（教授逐条讲评过）：
- **B（收益算不出来了）**：错。任何股票——包括被剔除的——收益照样算得出来，"仍在指数内"不是计算收益的前提。
- **C（自动剔除极端收益）**：错，而且方向反了。教授举了反例：2025 年涨了几十倍的股票才会被选进指数，**替换恰恰会引入极端收益**。
- **D（指数必须变成等权）**：错。「most index[es] are [value]-weighted」——市值加权，大公司权重大（阿里 8%，小公司 0.0X%）。成分股变动与加权方式无关。

**追问的答案**：冻结面板应当**如实记录退市这件事本身**——
1. 保留该股票到它的**最后一个可交易周**，给出最终收益（或按退市清算规则处理）；
2. 之后该行**留空**，让面板在那一周变成 29 只股票，**不要替补**；
3. 记录下退市日期与原因，作为面板的元数据。

**为什么**：留空是**诚实的**——它反映了当时投资者真实面对的处境（手上这只股票没了）。替补则是在伪造一个"永远有 30 只好股票"的历史，把最坏的结果从样本里抹掉了。**你的策略在真实世界里会承受退市带来的损失，回测就必须也承受。**

**加分点**：指出这和讲义 p.13 脚注的呼应——「Research needs point-in-time data with documented revisions and **historical constituents**」。免费数据只有"今天的成分股名单"，做严肃研究必须买历史成分股数据。
</details>

**7.**（综合题）你的组员交来一个周频选股回测：用"4 周动量 + 最新一期的利润率 + 上月 CPI 同比"预测下周主动收益，2023-07 至 2026-06，样本是今天从 Yahoo Finance 下载的 HSTECH 30 名单，年化收益 42%，夏普 2.1。**你要在提交前问哪些问题？**

<details><summary>参考思路</summary>

**先用框架 B 判断量级**：年化 42% 应与同口径长期收益、波动、回撤、杠杆和成本比较；夏普 2.1 应与同频差额收益的均值/标准差口径比较。本文没有给出可独立复算的“港股 20 年年化 1.7%”链条，因此不把它当参照。两项都异常强时，**首要核查数据泄漏**，但异常不等于已经证明泄漏。 不是"我们很厉害"。

**然后用框架 A 逐项排查，四类问题：**

**① 样本池（→ 生存者偏差）★ 最可疑**
- 名单是**今天下载**的 HSTECH 30 → 这就是第 6 题的错误。2023-07 时的成分股与今天不同。
- 这三年退市或被剔除的公司完全不在样本里，而它们通常是表现最差的。
- **要做的**：换成 2023-07 的历史成分股名单并冻结；退市的留空而非替补。

**② 时点（→ 前视偏差）**
- **“最新一期的利润率”**：美国样本是否按 SEC filing 的真实时刻匹配？香港样本是否按 HKEXnews 公告发布时间匹配？不能把 10-Q/10-K、SFC 和 HKEX 公告机制混写成一种“归档日”。若只按财季期末匹配，就是泄漏路径 ③。
- **"上月 CPI 同比"**：CPI 大约在次月第二周发布（🎙️`01:32:53`）。若在 t 月直接用了 t−1 月的 CPI，在 t 月上旬就已经泄漏。教授的做法是**再多滞后一个月**。
- **"4 周动量"**：有没有 `.shift(1)`？做三行手检。

**③ 口径**
- 价格复权了吗？港股同样有拆股和分红。
- 收益是简单还是对数？算术平均收益的年化可按频率乘 52；波动率按年化因子乘 $\sqrt{52}$。若把多期收益连成财富路径，需按复利计算（如对数收益先求和再取指数，或简单收益连乘），不能把 CAGR 一律写成“平均收益 ×52”。
- **主动收益的市场基准用的是什么？** 恒生指数还是恒生科技指数？用错基准，主动收益整体会有系统性偏移。

**④ 基准与成本**
- 夏普 2.1 是否先用同期同币种无风险收益构造差额收益，再取差额均值/差额标准差？港元还是美元？
- **交易成本一分没扣**：周度调仓 156 次，30 只股票。🎙️`02:03:48` 教授说过，本课默认"小土豆投资者"、忽略交易成本，**但写报告时必须说明这个假设**。
- **只报了收益，没报回撤。** 参照 §2.10.3：PDD-JD 那个"美元中性"组合累计 +20.6%，最大回撤却是 −38.7%。**必须报最大回撤。**

**⑤ 可复现性**
- 代码存了吗？（🎙️`01:06:31`）ML 投资作业明确要求交可复现代码包。
- 能从干净环境重跑出同一张表吗？（讲义 p.56 第 4 问）

**结论怎么写**：不要说"结果是假的"，要说"**在排除 ① ② 之前，这个结果不可采信**"，并给出具体的重跑方案。syllabus 明确要求：「report weak results as weak」。
</details>

---

## 8. 讲义页码映射

| 笔记小节 | 讲义页 | 课堂覆盖 | 转录时间 |
|---|---|---|---|
| §2.1.1 两块内容 | p.2 | ✅ 详讲 + 🎙️ 大量课外展开（课程由来、顺序调换） | `00:03`–`06:56` |
| §2.1.2 金融 AI 产品四层 | p.3 | ❓ 现有转录无明确对应；不能判定略过或降权 | — |
| §2.1.3 两种 AI 路线 | p.4 | ✅ 详讲 + 🎙️ 成本、开源动因、CityU 订阅 | `32:24`–`38:17`、`01:03:33` |
| §2.1.4 考核 | p.5 | ✅ 详讲 + 🎙️ 手写小抄、点名规则、取消传统作业 | `09:21`–`16:37` |
| §2.2.1 Vibe Coding 是什么 | p.6, 7 | ✅ 详讲 + 🎙️ "top 10% 学编程，其余学 vibe coding" | `08:22`、`39:22`–`41:55` |
| §2.2.2 六步循环 | p.9 | ✅ 一句带过 | `46:02` |
| §2.2.3 六项规格 | p.10 | 🎙️ 用现场演示替代（腾讯数据的例子） | `46:02`–`47:10` |
| §2.2.4 桌面工具/权限/留痕 | **讲义无** | 🎙️ **课外展开** ★ | `43:06`–`45:15`、`01:06:31`–`01:07:31` |
| §2.3.1 收益率口径 | p.19（部分） | 🎙️ 课外补充"有很多种收益" | `46:42` |
| §2.3.2 复权价 | p.22 | ✅ 详讲 + 🎙️ 小盘股、债券 ETF 派息例子 | `27:28`、`01:20:47`–`01:21:33` |
| §2.3.3 指数与基准 | **讲义无独立页** | 🎙️ **课外展开** ★ 上证综指不可交易 | `30:19`–`31:52`、`01:10:59` |
| §2.3.4 数感量级表 | **讲义无** | 🎙️ **课外展开** ★★ | `49:40`–`52:26`、`01:44:05` |
| §2.4.1 样本与日期 | p.13 | ❓ 无逐页对应时间；课堂概念有涉及，不可降权 | — |
| §2.4.2 装环境 | p.12 | ✅ 现场演示 | `53:29`–`55:48` |
| §2.4.3 156 周收益 | p.14 | ✅ 详讲 + 🎙️ "200 价格→199 收益"检验 | `47:50`–`48:21`、`01:07:31` |
| §2.4.4 两个数据源 | p.17, 18 | ✅ 详讲 + 🎙️ 跨市场假期差异 | `01:07:45`–`01:09:17`、`01:24:10` |
| §2.4.5 四项检查 | p.23 | ✅ 详讲 | `01:23:00`–`01:23:36` |
| §2.5.1 预测时钟 | p.43 | ✅ 详讲 | `29:01`–`29:59`、`01:59:44` |
| §2.5.2 泄漏与前视偏差 | p.19（部分） | ✅ 详讲 + 🎙️ "crazy returns = leakage" | `30:06`、`01:35:06`、`01:43:57` |
| §2.5.3 五种泄漏路径 | p.48 | ◑ 只确认日期错配；其余四条无逐项课堂对应 | `02:00:05` |
| §2.5.4 三种日期 | p.27 | ✅ 详讲 | `01:32:10`–`01:34:38` |
| §2.6.1 宏观时点 | p.28, 30, 31, 32, 33 | ✅ 详讲 + 🎙️ 中国 CPI/GDP 发布节奏、+1 月保守滞后 | `01:32:53`–`01:50:14` |
| §2.6.2 AKShare | p.29 | ✅ 讲了 | `01:40:04`–`01:40:40` |
| §2.6.3 归档日 | p.34, 35, 36, 39, 40 | ✅ **详讲，现场演示 Yahoo Finance** ★ + 🎙️ 腾讯 8/12、阿里 8/20、SEC 2000 年前后 | `01:36:59`–`01:39:37`、`01:55:19` |
| §2.6.4 财务比率 | p.37, 38 | ✅ 详讲 + 🎙️ 接到案例作业、MicroStrategy | `01:51:42`–`01:54:28` |
| §2.7.1 三类信息 | p.41 | ✅ 讲了（XT→YT+1 表格） | `01:23:13`、`02:00:35` |
| §2.7.2 三个预测变量 | p.44 | ✅ 讲了 | `01:57:23` |
| §2.7.3 代码落地 | p.45, 46 | ✅ 讲了 | `01:58:11`–`02:00:19` |
| §2.7.4 三行手检 | p.47 | ❓ 未逐条对齐；课堂强调日期检查，不能判明确略过 | `02:00:05` |
| §2.7.5 自造技术指标 | p.44（延伸） | 🎙️ **课外展开** ★ 自己算=无发布滞后 | `01:56:14`–`01:58:11` |
| §2.8.1 HSTECH 热力图 | p.24 | ✅ **详讲** + 🎙️ 成分股名字、怎么读图 | `01:25:43`–`01:27:28` |
| §2.8.2 冻结样本池选择题 | p.25 | 🔴 **详讲 + 明示是考题 + 逐项讲评** | `01:27:47`–`01:31:48` |
| §2.9.1 四张图 | p.49 | ✅ 讲了（"plot, plot and plot"） | `02:06:31` |
| §2.9.2 六页成品图 | p.20, 21, 32, 50, 51, 52 | ✅ **详讲** + 🎙️ 箱线图解读、回撤故事、期限利差、疫情尖峰 | `01:09:28`–`01:13:50`、`01:19:11`、`01:45:19`、`01:48:20`、`02:09:27` |
| §2.9.3 无模式散点 | p.50（右下）, p.53 | ✅ **详讲** + 🎙️ 市场有效性、Fama、反转 | `01:01:24`–`01:02:49`、`02:07:24`–`02:09:06` |
| §2.10 PDD-JD 配对交易 | **p.8, 11, 15, 16** | ❓ 现有转录无可确认对应；关键词 0 命中不证明明确略过，不可降权 | — |
| §2.12 收尾 | p.56, 57, 58 | 🔀 教授给了**不同的**三条（数感 / 历史事件 / 模型多为 garbage） | `02:12:27`–`02:13:41` |
| — | p.26, 42（章节分隔页） | 无内容 | — |
| §2.11 工作坊与失败诊断表 | p.54、55 | p.54 ↪️ 课后尝试；p.55 ❓ 无逐页课堂对应，不可降权 | `02:13:16` 后 |
| — | p.1（封面） | ⚪ 封面 | — |
| **全程材料对齐** | 讲义讲解、行政、AI 工具演示、休息、问答与跑题均纳入 align | ✅ 671 段逐段归入连续块；不等于音频完整 | `00:01`–`02:15:21` |

**页面统计**：讲义共 **58 页**。下列主题按讲解单元列出，部分页面跨主题重复计入，不能把这些数字当作不相交分解：课程行政与定位 6 页（10%）｜Vibe Coding 方法论 5 页｜数据下载与检查 12 页｜宏观与公司财务 15 页｜无泄漏构造变量 7 页｜诊断图与收尾 9 页｜配对交易案例 4 页｜章节分隔与封面 3 页。原材料总页数仍以 58 页为准。

**✅ 覆盖率声明：58 页全部已读并纳入。**
- 无纯图片页被跳过。**全部 58 页已用 Read 工具按页视觉复核**（3 批：1–20、21–40、41–58），文本提取字符数偏低的图表页（p.11、13、16、20、21、24、32、37、50、51、52）均已逐张读图并在正文或本映射表中转写为文字/表格。
- **明确未纳入正文的只有 3 页**：p.1（封面）、p.26 与 p.42（章节分隔页，各只有一行标题），三页均无实质内容。

**「课堂覆盖」判读边界**：只有明确 skip/翻页证据才标 ⏭️。关键词未命中或没有逐页时间戳只标 ❓/无对应，不能据此降权。当前转录按 14 个连续块覆盖全部 671 段。

**课堂时间分配（按转录 10–15 分钟连续块）**

| 区间 | 主要内容 | 约时长 | 录音占比 |
|---|---|---:|---:|
| `00:01`–`09:51` | 课程由来、结构与行政 | 约 10 分钟 | 7.3% |
| `10:05`–`19:45` | 考试、作业、参与和课程目标 | 约 10 分钟 | 7.1% |
| `20:01`–`29:59` | 金融 AI 定位、价格收益与预测时钟 | 约 10 分钟 | 7.4% |
| `30:06`–`39:56` | 基准、模型选择、AI 工具路线与成本 | 约 10 分钟 | 7.3% |
| `40:10`–`49:53` | Vibe Coding、桌面工具/权限、规格与下载演示 | 约 10 分钟 | 7.2% |
| `50:07`–`59:51` | 数感量级、环境安装与现场演示 | 约 10 分钟 | 7.2% |
| `01:00:01`–`01:09:45` | 市场有效性、收益构造、代码留痕和跨源下载 | 约 10 分钟 | 7.2% |
| `01:10:01`–`01:19:59` | 三市场图、指数基准、休息与考试形式 | 约 10 分钟 | 7.4% |
| `01:20:13`–`01:29:57` | 复权、数据检查、热力图和冻结样本池 | 约 10 分钟 | 7.2% |
| `01:30:12`–`01:39:53` | 冻结样本讲评、宏观参考期与财报日期 | 约 10 分钟 | 7.2% |
| `01:40:04`–`01:49:51` | FRED/AKShare、归档、保守滞后和宏观图 | 约 10 分钟 | 7.2% |
| `01:50:03`–`01:59:56` | 期限利差、财务比率和预测变量 | 约 10 分钟 | 7.3% |
| `02:00:05`–`02:09:53` | 日期错配、另类数据、成本和图诊断 | 约 10 分钟 | 7.2% |
| `02:10:05`–`02:15:21` | 回撤、数感收尾、课后练习与分组 | 约 5 分钟 | 3.9% |

全量对齐证据由本次正式审查包保存。该表的占比按每块首末文本时间戳估算，合计约 98.1%，约 1.9% 段间空隙没有分配；连续材料定位区间覆盖 8,120 秒是另一种索引口径，不能混为逐秒内容覆盖，也不认证原音完整。

---

## 9. 延伸与勘误

### 9.1 课件与课堂覆盖的不确定项

| 讲义页 | 内容 | 判定 | 依据 | 建议 |
|---|---|---|---|---|
| p.3 | 金融 AI 产品四层 | ❓ 转录无明确对应 | 没有逐页时间戳；关键词缺失不足以证明 skip | 保留完整自学，不降权 |
| p.8, 11, 15, 16 | PDD-JD 案例 | ❓ 转录无可确认对应 | 未找到可靠对应话题，但未录到/ASR 漏词/现场翻页均无法排除 | 保留完整题解，M05 还会使用 |
| p.9 | 六步循环 | ✅ 一句带过 | `46:02` 出现 six-step 后转入演示 | 记流程，并用演示理解 |
| p.10 | 六项规格 | ✅ 演示替代逐条讲页 | `46:02`–`47:10` | 仍按讲义六项完整学习 |
| p.47 | 三行手检 | ❓ 无逐页讲解证据 | `02:00:05` 强调日期错误，但未逐项走 p.47 | 不可降权 |
| p.53、p.56 | 解释核对/全班四问 | ❓ 无逐页对应 | 现有转录无法确认是否照页讲 | 作为作业自查保留 |
| p.54、55 | 工作坊与诊断 | p.54 ↪️；p.55 ❓ | `02:13:16` 后布置课后尝试只支持 p.54；p.55 无逐页证据 | 两页完整自学 |

本次没有找到足以认定课堂明确跳过的页，因此不设置降权型 ⏭️。

### 9.2 课上讲了但课件没有 🎙️

| # | 纯课堂增量 | 区间/时长 | 原始时间戳 | 对应小节 | 为什么值钱 |
|---:|---|---|---|---|---|
| 1 | 何时用模型会进考试 | 约 30 秒 | *"I'm the one [who is] trying to teach you when to use those model[s]… And of course you will see this in the exam."*（`04:24`） | §6.2 | 🔴 直接考试明示 |
| 2 | 桌面编码工具而非聊天框 | 约 2 分钟 | *"You are going to download the desktop coding tool."*（`43:06`） | §2.2.4 | 决定实际工作方式 |
| 3 | 每次保存代码 | 约 1 分钟 | *"Every time you ask your AI to create it… please also save the file for the code."*（`01:06:31`） | §2.2.4 | 可追错与复现 |
| 4 | 指数业绩必须有基准 | 约 2 分钟 | *"The benchmark is also quite important."*（`30:19`） | §2.3.3 | 防止孤立报 5% |
| 5 | 收益预测最常见错误是日期错配 | 约 1 分钟 | *"The mistake I see… 99.9%… that's missing the date."*（`02:00:05`） | §2.5–§2.7 | 🔴 直接错误模式 |
| 6 | SEC 归档历史滞后 | 约 1 分钟 | `01:38:40`–`01:39:23` | §2.6.3 | 回测不能跨年代套固定 lag；香港机制另据 HKEX 纠正 |
| 7 | 宏观 +1 月、财务 +3 月的保守近似 | 约 2 分钟 | `01:41:10`–`01:43:00` | §2.6.1 | 缺发布日历时的课堂近似，不冒充精确规则 |
| 8 | 上证综指点位不可直接交易 | 约 30 秒 | `01:10:59`–`01:11:26` | §2.3.3 | 区分统计基准与可交易产品 |
| 9 | 另类数据、交易成本与市场冲击 | 约 4 分钟 | `02:01:14`–`02:05:20` | §2.7.5 | 把教学价量指标放回真实机构边界 |
| 10 | 数感是最高优先级 | 约 1 分钟 | *"Develop a sense for numbers. That's the top priority [thing] I want [you] to learn from the course."*（`02:12:27`） | §2.3.4、§4.4 | 🔴 直接学习优先级 |
| 11 | 课程安排的课堂说明 | 约 1 分钟 | `01:17` 无教材；`14:01`、`14:31` 本年 12 讲、因公共假期改录制展示 | §2.1 | 课堂行政说明，当前执行以 Canvas 最新通知为准；不从转录补造具体假期日期 |

这里的引文只保留转录可确认词；ASR 损坏处不用猜测补正文。

### 9.3 课件自身的问题

**① ⚠️ 收益率口径：讲义与数据集不一致**
讲义 p.19 唯一给出的公式是**简单收益** `r_t = P_t/P_{t−1} − 1`，但三个月频数据集（`market_index_returns_240m.csv`、`spy_monthly_features_240m.csv`、`csi300_macro_panel.csv`）里的收益**全部是对数收益**（实测误差 1e-15，精确匹配）。讲义 p.20/p.21 的**图注**确实写了 "monthly log returns"，所以图是自洽的——**但正文从未定义过对数收益，也从未说明为什么月频改口径**。
**影响**：直接把月频收益当简单收益复利累乘，20 年会算错约 22%（S&P 500：4.59 倍 vs 正确的 5.87 倍；`L01_01`：终点低估 21.8%）。**做 ML 作业时必须先确认口径。**

> 📁 **代码**：[`code/L01_data/01_return_conventions.py`](../code/L01_data/01_return_conventions.py) —— 三条净值曲线并排：价格净值 / 对数收益正确累加（重合）/ 误当简单收益复利（4.59×），断言前两者一致到 1e-10（`L01_01`，图见 §2.3.1）

**② ⚠️ p.44 的记号与 p.43 不一致**
p.43 用「x_t → r_{t+1}」，且明说「The saved row is labelled by forecast week **t+1**」；p.44/46/47 改用「预测变量停在 t−1、目标 = P_t/P_{t−1}−1」，行按预测周 **t** 标注。两者描述同一件事，但**同一份讲义里切换了行的标注约定**，初学者极易读错。见 §2.7.2 的提醒。

**③ ⚠️ p.54 的列表被版式截断**
"Live Prompt Workshop" 列出三项候选任务，第 3 项以「**or**」结尾，提示列表可能存在排版/编辑问题；可见材料不足以断言一定有第四项，更不能猜其内容。

**p.53 的计数文字与实际列表不符**：标题下写 *"Ask four questions"*，下面却有 **五个**独立检查问句（观测、单位、滚动窗口、变量表示、结论范围）。本笔记 §2.9.3 按五问逐项作答，不漏最后一个。

**④ p.44 的标题与表格行数对不上**
标题是 "**Three** Weekly Stock Predictors"，表里却有四行。第四行 "Weekly target" 是目标不是预测变量，所以严格说标题没错，但表格没有把目标行与三个预测变量视觉分开，容易数错。

**⑤ p.4 的肖像是 AI 生成的**
讲义自己在脚注标明：「Portraits are **AI-generated editorial illustrations, not photographs**.」这条本身没问题，但值得记一笔——**一门讲"检查证据"的课，在自己的讲义里演示了这种披露习惯**，案例报告里引用图片时应当照做（案例 brief 也明确要求「Cite every… borrowed chart or image」）。

**⑥ p.2 与 p.3 的表格在 `pdftotext` 下会行错位**
两张表的首列标签跨行，纯文本提取后标签与内容会串行。**做笔记时必须视觉复核**，否则会把 "Prediction" 的应用写到 "Information and text" 行上。本笔记的表格已按图像校正。

**⑦ 官方课程目录与本讲内容脱节**
官方 CILO 里**没有任何一条**对应本讲的"AI 辅助编码 + 数据时点纪律"，而官方 Keyword Syllabus 里的「Unsupervised Learning and Clustering」在 2026/27 的 12 讲主题里根本不存在。详见 [[EF5560_Fintech_and_AI_in_Finance/_prep/课程前置资料|课程前置资料]] §3.3。

**⑧ ⚠️ 课堂 drawdown 口述不等于正式定义**

转录 `02:11:31` 把“回撤约为 0”说成“过去 12 个月没有亏钱”。按本篇和讲义图使用的 running-peak 定义，0 只表示当前净值达到截至当时的历史峰值；过去 12 个月仍可能出现过亏损月份或先跌后涨。正文 §2.9.2 已保留原话并就地纠正，答题按严格定义。

**⑨ ⚠️ 美国与香港的披露机制不能只换监管机构名称**

课堂把 SEC 与 SFC 并列，但美国 10-Q/10-K filing 与香港上市公司经 ESS/HKEXnews 发布公告不是同一机制。港股特征可用时点须查实际 HKEXnews 公告发布时间，不能套用美国 filing 规则；正文 §2.6.3 已按 HKEX 官方资料纠正。

### 9.4 课外补充

**① 🔗 关于 R² ≈ 1% 这个数字的出处（笔记补充，⚪ 我的推断）**
教授说的"收益预测 R² 平均 1%"与资产定价文献中的常见量级一致（月度收益预测的样本外 R² 通常在 0.5%–1% 量级）。他本人的研究方向正是这一领域，且他在课上多次提到自己做"return prediction for equities, bonds, currency"（`01:38`）。
⚪ **这是我根据领域常识做的对照，教授没有给具体文献。** 若考试要求引用，只引用他的口头量级即可。

**② 💡 一个可以自己跑的验证练习（笔记补充）**
`spy_monthly_features_240m.csv` 是一张**计算窗口可重构、历史可得性仍待核**的特征表。建议自己写十行代码验一遍：
```
volatility_12[t] == std(market_return[t-12:t], ddof=1) * sqrt(12)   # 应该完全相等
momentum_12[t]  == US_SPY_price[t-1] / US_SPY_price[t-13] - 1        # 应该完全相等
term_spread_lag1[t] == macro.term_spread[t-1]                        # 应该完全相等
unemployment_lag2[t] == macro.unemployment_rate[t-2]                 # 应该完全相等
```
四条我都验过，误差均为 0。**验一遍你就真的懂了"滞后"是什么意思**，比读十遍讲义有用。

> 📁 **代码**：这四条（以及其余 11 列）已写成 [`code/L01_data/04_leakage_audit.py`](../code/L01_data/04_leakage_audit.py)，15 列最大误差 2.1e-15（`L01_04`）。两个只有跑过才知道的细节：① `momentum_12[t]` 在 2007-07 那行要用 2006-06 的价格，价格表里没有，但可以用收益表首行反推（P = 88.13）；② `momentum_12` 用 $\exp(\sum g) - 1$（$g$ 已是对数收益；不能再次取 log） 也能精确复现（误差 1.6e-15）——对不上的只是 `∏(1+r) − 1`，因为收益是对数的

**③ 💡 `macro_240m.csv` 里那个唯一的缺失月**
240 个月里只有 **2025-10** 的失业率和通胀为空。这是"保留已发布的缺失值、不做静默插值"（讲义 p.28、p.32 图注）的实物证据，也顺带演示了缺失如何按 2 个月滞后传导到特征表的 2025-12 行（`L01_04`：两个宏观列各只能比较 227 行，缺的就是 2025-12）。**做作业时不要顺手 `fillna()`。**

**④ 🔗 ALFRED（讲义 p.33 提到但没展开）**
FRED 的"实时版本"数据库（ALFRED = **A**rchival FRED）。FRED 给你的是**修订后的当前版本**，ALFRED 给你的是**每个历史日期上当时可见的版本**。做严肃的宏观预测回测必须用后者。讲义只提了一个名字，没说是什么。
（🔗 圣路易斯联储公开数据库，常识性补充，非课程材料）

**⑤ 变更记录：2026-09-11 按预习可读性规则重写 §2**
按 [[笔记模板]]「★ 预习可读性」六条硬要求，对 §2 全部 42 个 `###`/`####` 小节做了逐节零基础试读，并做了以下改写（不改标题、不删事实，只增补写法）：
- §2.3.2（复权价）、§2.3.3（指数与基准）：原来"是什么"后直接跳进术语列表，补了一句不含新术语的人话开头再进入定义
- §2.10.2（多空组合怎么算）：原来公式后没有符号表、没有代入数字，现在补齐符号表 + 一组标注"假设"的代入数字（讲义未给某一具体周的真实涨跌数字）
- §2.6.4（会计比率表）：补一组标注"假设"的代入数字（利润率、账面杠杆各一例）
- §2.4.2（让 Codex 装环境）、§2.12（收尾）：原来开头过薄，补了一句说明"为什么这一步/这一节存在"
- 其余全部小节：补齐小节结尾"所以呢"（这个概念在漏斗里的位置、为什么接下一节），共新增 40 处；已经合格的小节（如 §2.3.1、§2.11.1、§2.11.2 已有等价的收尾句）未动
详见任务对话记录；本次改写未发现新的事实错误。

**2026-10-02 本轮修订范围与证据**：利用既有全源审报告一次修复公式、间隔计数、时点边界和核心机制；新增数字例均为笔记补充，计算记录在 `C:/Users/BenLi/.codex/scratchpad/cityu-depth-20260930/ef-draft-medium/calc-results.json`，原课程复算在 `ef-m01-source-audit/recompute-results.json`。未新增转录引文，未读/写个人作业，未更新原材料。完整季度财报、实际发布时刻、宏观 vintage 和原冻结 HSTECH30 面板仍缺，不能以教学补例称原结果已重现。`mechanism_review: passed` 是 2026-10-02 的历史字段，不代表本次全篇独立审查已通过；当时按简化流程验收，新增 6 张流程图已实际查看，图 5 已定向改为纵向分层并复看可读；未做独立全量 Q/R 盲读，不补造评分。


### 9.5 待核对

| # | 事项 | 说明 |
|---:|---|---|
| 1 | 转录登记 | `M01-transcript.txt`，SHA-256 `025a51821af5f2cf53fb9793900f62e7f9d65953a24fd86e014b93f11beaee33`；671 条带时间戳的段记录、670 个唯一时间戳，`42:28` 连续出现两段（首段中断，次段重复开头后继续）。scan 与 audit 的差值可定位到这一处，不代表少读一段；原转录不改。范围 `00:01`–`02:15:21`、2:15:20，无倒退或 ≥120 秒空档；这些只说明文本时序 |
| 2 | 开头完整性 | 首句 *"Discourse last year. Okay."*（`00:01`）像中段残句；可能缺问候/开场，不因时间戳从 00:01 开始就认证完整 |
| 3 | 结尾完整性 | `02:15:21` 有 *"Okay, that's all. See you next week."*，文本结尾完整；仍未逐字核原音 |
| 4 | 期末小抄 | M01 `10:20` 当时说一页手写小抄仍待定；后续 M03 `02:53`–`03:17` 已确认一张 A4、双面手写、内容不限、不许打印或用 iPad。最终执行仍以 Canvas 为准 |
| 5 | 学生问答 ASR | `02:05:20` 附近多句损坏，只保留能确认的主题，不还原乱码 |
| 6 | 第三家公司名 | `01:37:56` ASR 作 “Zihu”，无法确认，正文回避名称 |
| 7 | MSF/MS[?]E | `02:22` 名称不清且不影响本讲内容，保留 `[?]` |
| 8 | 未核材料 | 未逐字重听原音；讲义 p.37 精确季度底表、宏观 vintage、完整冻结成分股面板仍缺，不升级为已验证 |

**反方视角**

1. 最薄弱处：现有转录开头可能缺失，且现场屏幕操作不能由 ASR 完整恢复；因此安装/运行细节仍主要靠讲义和保存代码。
2. 若考试直接问课堂原句：最可能答不稳的是 `02:05:20` 学生问答、`01:37:56` 公司名和 `02:22` 项目名；这些均未强行还原。
3. 本次推断及其风险：按文本把无对应页标 ❓，而非 ⏭️；若原音实际明确跳页，复习优先级可能偏高，但不会漏学。宏观/财务固定 lag 是课堂近似，不是跨数据源的现实保证。

### 9.6 变更记录

| 日期 | 变更 |
|---|---|
| 2026-09-11 | 链接修复：本文件 1 处 Markdown 形式的同文件锚点（`[§x](#slug)` 写法）改为 Obsidian 双链 `[[#标题原文\|§x]]`——Obsidian 按标题原文匹配，GitHub 式小写连字符 slug 一律点不开（对抗自检清单 9b）。只改链接写法，标题与正文未动 |
| 2026-10-23 | **重审既有转录合并结果，未新增音源**：重新 scan 原 `M01-transcript.txt`（671 段，`00:01`–`02:15:21`），建立全程 align，复核教授明示与直接引文格式，修正“无对应=略过”的过度判断，并更新 §0、§6、§8、§9.1/9.2/9.5。材料机器结果与教学/视觉验收分开记录 |

---

## 相关

- [[EF5560_Fintech_and_AI_in_Finance/00-课程总览|00-课程总览]]
- [[EF5560_Fintech_and_AI_in_Finance/_meta/知识层级台账|知识层级台账]] · [[EF5560_Fintech_and_AI_in_Finance/_meta/术语表|术语表]] · [[EF5560_Fintech_and_AI_in_Finance/_meta/考点库|考点库]]
- [[EF5560_Fintech_and_AI_in_Finance/_meta/数据集卡片|数据集卡片]] —— 本讲用到的 8 个 CSV 的完整统计
- [[EF5560_Fintech_and_AI_in_Finance/_meta/作业与DDL|作业与DDL]]
- [[EF5560_Fintech_and_AI_in_Finance/_prep/课程前置资料|课程前置资料]]
- 下一讲：[[M02-回归与样本外设计]]
- 跨课：[[M02-预测分析-线性回归]]（IS6400 W02）—— 与本课 [[M02-回归与样本外设计]] 同周同主题，且同样在教"用 GenAI 写代码"；课程口径见 [[IS6400_Business_Data_Analytics/_prep/课程前置资料|IS6400 课程前置资料]]
