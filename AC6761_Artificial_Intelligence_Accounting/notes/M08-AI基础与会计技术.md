---
course: AC6761
module: M08
week: 8
date: null
source: ["AC6761_Artificial_Intelligence_Accounting/course_files_export/Week 8 PPT.pptx（45 页）"]
transcript: pending
prerequisites: [高中四则运算与一次函数]
new_concepts: [Narrow AI, AGI, 半监督学习, 强化学习, 线性回归, 最小二乘法, OCR, RPA, NLP]
tags: [AC6761, AI, machine-learning]
status: v0.9
readability_rules: v2
mechanism_spec: v1
mechanism_review: passed
mechanism_review_mode: full-independent-gpt6.1-20261025
mechanism_content: repaired
readability_review: passed
teaching_standard: novice-v1
updated: 2026-10-25
---

# M08 · AI 基础与会计技术

## 0. 三分钟速览

本讲从 AI 的范围出发，区分四种机器学习训练方式，用线性回归展示模型如何拟合预测线，最后把 OCR、RPA、NLP 和生成式 AI 放进会计工作流。

学完你能：

- 区分窄人工智能与人工通用智能的能力范围。
- 根据标签和反馈类型判断监督、无监督、半监督或强化学习。
- 解释会计分类模型的输入、标签、输出与漂移风险。
- 手算最小二乘回归并区分预测值、残差和平方误差。
- 说明 OCR、RPA、NLP、生成式 AI 的输入输出、失败方式和控制点。

课程前置材料将 W8 对应 CILO 2：识别会计中的 AI 技术与模型。课程没有为 CILO 分配权重，不能据此推断考试比重。

## 1. 开始之前 · 知识衔接

### 1.1 你已有的

| 概念 | 一句话唤醒 | 回链 |
|---|---|---|
| AI 与 ML 直觉 | AI 是计算系统承担感知、学习、判断或语言任务；ML 从数据学习预测或结构。 | [[AC6761_Artificial_Intelligence_Accounting/_meta/知识层级台账\|知识层级台账]] |
| 标注数据 | 标签是训练样本中已知的正确答案。 | [[AC6761_Artificial_Intelligence_Accounting/_meta/知识层级台账\|知识层级台账]] |
| 生成式 AI 与幻觉 | 模型会按提示生成内容，但流畅文字仍可能错误。 | [[AC6761_Artificial_Intelligence_Accounting/notes/M01-会计与商业\|M01：会计与商业]] |

### 1.2 本讲全新引入的概念

Narrow AI 和 AGI 在 §2.1。四类学习在 §2.2–§2.5。线性回归和最小二乘在 §2.6。深度学习、会计应用与 OCR、RPA、NLP、生成式 AI 在 §2.7–§2.10。

### 1.3 为什么这一讲放在这里 · 重排说明

前七周以会计基础为主，W8 才正式引入 AI。笔记先讲概念和训练信号，再讲回归计算，最后讨论会计工具链。这样读者先理解模型怎样工作，再判断案例数字和工具输出能否采信。课件历史、生活应用等顺序相应后移；映射表保留原页位置。

## 2. 正文

讲义 p.1 只有课程标题，是封面页而非教学内容页；按规则不展开。正文从内容页 p.2 开始，p.1 不计作讲解遗漏。

### 2.1 AI、Narrow AI 与 AGI（讲义 p.2–7）

**是什么**

人工智能（Artificial Intelligence, AI）是被设计来模拟学习、解决问题、决策和语言理解等认知功能的计算系统（讲义 p.2）。窄人工智能（Narrow AI）在特定领域表现好，但不能自动把能力迁移到其他任务；人工通用智能（Artificial General Intelligence, AGI）指能适应广泛任务的类人能力（讲义 p.3）。

讲义 p.2 的标题问题原文是 **“What is Artificial Intelligence?”**，没有选项或独立编号练习。下面保留原定义，避免把笔记英语改写当作原句。

**讲义英文原文（p.2）**：

> Artificial Intelligence (AI) refers to computer systems engineered to simulate human cognitive functions—including learning, problem-solving, decision-making, and language understanding—enabling autonomous task execution without explicit programming.

**中文读题与边界**：问题要求解释 AI 是什么；原文说系统模拟学习、解决问题、决策和语言理解。末尾“without explicit programming”若读成所有 AI 都没有显式程序，会过宽：本讲自己也列了规则式 ELIZA/专家系统。这里应区分按规则编写的系统与从数据学习的系统，二者都可能承担 AI 任务。

**English reference answer（笔记自拟）**: Artificial intelligence refers to computer systems designed to perform tasks involving learning, problem-solving, decision-making or language understanding. Some systems use explicit rules, while machine-learning systems learn patterns from data.

讲义 p.3 对 AGI 写“currently unrealized and debated among researchers”；这是课件时点的说法，不作为本次已核实的 2026 实时发展判断。

**为什么需要它**

发票科目分类模型能提出类别，不等于它理解全部会计，也不等于能处理从未见过的合同。先说清任务范围，才不会夸大能力。

**课件原例**

p.3 用 Deep Blue 下棋说明窄 AI：它专门搜索棋局并选择走法，不能因此处理其他领域。p.4–6 的时间线是讲义的简化回顾，逐项读法如下。

- **1943：** McCulloch 与 Pitts 提出人工神经元的数学模型，尝试用简化单元表达神经活动。
- **1950：** 图灵提出用对话行为测试机器是否表现得像人；测试的是可观察表现，不直接证明机器有人的意识。
- **1956：** 达特茅斯会议将 Artificial Intelligence 作为研究领域名称。
- **1966：** ELIZA 用脚本规则模拟心理治疗对话，说明自然的对话表象也可能来自固定回应。
- **1969：** Shakey 将感知、规划与行动结合，在受控环境中导航和操作物体。
- **1973–1980：** 课件称为第一轮 AI winter，并把资金收缩与 Lighthill Report 对未兑现承诺的批评相连。
- **1980 年代：** 专家系统（如 XCON）用规则支持技术配置决策，重新带来商业兴趣。
- **1986：** 课件把反向传播归于 Geoffrey Hinton，属于简化归因。反向传播由多位研究者发展；Rumelhart、Hinton、Williams 共同署名的 1986 年论文讨论以反向传播学习内部表示（Nature 323, 533–536，[论文 DOI](https://doi.org/10.1038/323533a0)），不能写成 Hinton 独创。🔗 论文作者及书目信息已于 2026-10-22 核 Nature 记录，未据此重建整段 AI 史。
- **1997：** Deep Blue 击败 Kasparov，展示专门搜索系统的棋类能力。
- **2012：** AlexNet 在 ImageNet 推动深度学习图像识别。讲义 p.6 另声称“slashing image recognition errors by 41%”；未给错误率基准、分母或原研究，保留为课件数字，不据此说本次已证实。
- **2020–2025：** 课件列 GPT-3（2020）、ChatGPT（2022）、GPT-4/Gemini 多模态模型和 MCP（2024–2025）。这些时间与“革命性”“标准化”等评价仍是课件声称；MCP 的起始时间和“标准化”说法待核。

p.7 原 SmartArt 是三个套叠圆：AI 包含 ML，ML 包含 DL；p.8 文字也说明这一关系。下图按原包含语义重画，框的空间大小不是市场份额或性能比较。

```mermaid
flowchart TB
 subgraph AI["人工智能 AI"]
  subgraph ML["机器学习 ML"]
   DL["深度学习 DL"]
  end
 end
```

从外向内读：一个 DL 方法属于 ML，因而也属于 AI；反过来，规则式专家系统可以属于 AI，却不必属于 DL。这个变式只检验集合包含，不由“更里面”推出更强。

**🎙️ 课堂补充**

待转录补充。讲者备注全空，没有可用课堂转录，因此不能断言教授是否讲过或略过。

**💡 换个说法（笔记补充）**

计算器能算总账，不代表会判断收入确认；模型能处理一类任务，也不自动拥有通用判断力。

**常见误解**

AI 不是单一算法。ML 是 AI 的方法家族之一；Narrow / General 则是能力范围分类，两者不是同一分类轴。

**与其他概念的关系**

本节先限定 AI 的能力范围，下一节按训练信号解释 ML 模型怎样学习。

**所以呢**

识别范围能帮助会计人员把模型输出限制在它实际承担的任务内。

### 2.2 监督学习（讲义 p.8–13）

**是什么**

监督学习（Supervised Learning）用带标签样本训练：每条样本有输入和已知正确输出。模型学习输入到标签的映射，再预测新样本（讲义 p.10）。

**讲义英文原文（p.10）**：

> Supervised learning is a type of machine learning in which the model is trained on labeled data. Each training example consists of an input and a known correct output (the label). The algorithm learns the mapping from inputs to outputs so that it can predict the correct label for new, unseen data.


**为什么需要它**

当业务类别预先定义，且历史记录有人工确认答案时，可用这些记录训练并用已知答案检查预测。

**课件原例**

p.12：会计人员已为历史发票和信用卡交易编码，模型读取供应商、描述、金额、部门、日期等特征。讲义举例 “Uber or taxi receipts → Travel” 和 “Adobe subscription → Software / IT”。新发票由模型提出科目。课件未给出真实数据、精度或上线结果。

p.10 水果图中的监督者（Supervisor）提供训练数据集和期望输出（Desired Output），算法据此学习；后面的 Processing 表示使用学得的规则处理输入，并输出水果类别。训练时知道答案，使用时正要预测新记录的答案。下面把这两个阶段展开为同一流程，水果只作原图对象，不假称讲义给了分类算法。

```mermaid
flowchart LR
 T["训练水果的特征"] --> L["学习输入与标签的关系"]
 S["监督者给期望类别"] --> L
 L --> M["已训练模型"]
 N["新水果特征"] --> P["Processing 使用模型"]
 M --> P
 P --> O["苹果 / 梨 / 黄色果实等预测类别"]
```

沿发票例迁移：历史出租车单及核准 Travel 供学习；新出租车单只有字段，模型提出 Travel 再供复核。改变新单金额并不能唯一推出会分到哪类：特征、训练方式和模型尚未具体给定，不能凭三条示例保证分类规则。

**完整小例（笔记补充）**

构造三条教学数据：出租车 28 元→差旅；酒店 120 元→差旅；设计软件订阅 40 元→软件服务。输入是描述、金额等字段，标签是经核准科目。简化规则可学到“出租车/酒店→差旅”“软件订阅→软件服务”。给新单据预测后，应由人复核低置信、新供应商和重大金额。小样本只能解释流程，不能证明真实准确率。

**机制、失败与边界**

训练输入是历史单据和特征，目标是核准标签，输出是新记录的类别或类别分数。若旧编码错误，模型会复制错误；政策或供应商变化会产生数据漂移。应在未参与训练的样本上评估，并监测错分类型。准确率相同，重大错分的会计后果仍可能不同。

课件称监督学习可直接比较预测和标签、标签良好时有效、相对容易解释；缺点是标签成本高、未来分布变化时退化，且不善于发现未定义的新模式（p.11、13）。

**🎙️ 课堂补充**

待转录补充。

**💡 换个说法（笔记补充）**

像新员工参考已复核凭证学习编码；遇到新供应商仍需请教和复核。

**常见误解**

有标签不等于标签正确；指标好也不代表业务后果可接受。

**与其他概念的关系**

监督学习回答预先定义的类别/数值；无监督学习寻找没有答案标签的数据结构。

**所以呢**

标签质量、评估样本和人工复核共同决定自动建议是否能进入账务流程。

### 2.3 无监督学习（讲义 p.14–17）

**是什么**

无监督学习（Unsupervised Learning）面对没有正确答案标签的数据，寻找群组、规律或异常（p.14）。

**讲义英文原文（p.14）**：

> Unsupervised learning works with unlabeled data. The algorithm is not told what the “correct” answer is. Instead, it searches for hidden patterns, groupings, or structures within the data itself.


**为什么需要它**

大组织可能有大量分录，逐笔标“正常/错误”很贵；分析人员也未必预先知道所有异常类型。

**课件原例与完整小例**

p.14 原图把未标类别的水果输入 Model，输出相似果实的不同组：红苹果一组、黄色果实一组、西瓜切片一组。模型没有事先收到“正确组别”；分出的组还须人解释。它和 p.10 的区别是有没有期望输出参与训练，而不是有没有输出结果。

```mermaid
flowchart LR
 A["未标注水果或分录特征"] --> B["按所选相似标准找结构"]
 B --> C["不同群组 / 离群线索"]
 C --> D["人解释组别或调查原因"]
```

沿图读分录：金额相近、相似科目/时点/用户的记录可能在一组；不同相似标准会改变分组。图只解释结构发现，不指定距离算法或保证任何异常都能找到。讲义 p.16 的固定规则例是“amounts over \$10,000”：它只按金额截断，会放过小额但不寻常的记录。

讲义 p.16 说模型观察金额、科目组合、时间、用户和摘要，学习“正常”模式并标出离群项。

构造例子：同类耗材分录通常为 80、90、95 元，另有一笔 9,800 元记录。模型可能把后者标成异常。

调查者再核发票、采购、审批和业务背景。若它是年度批量采购，异常不代表舞弊。小额拆分也可能不突出。此例不保证特定算法一定发现这笔记录。

课件称其不需标签、适合发现隐藏模式和新型异常；但客观评估难、群组需人工解释，对预定义类别未必精确（p.15、17）。

**🎙️ 课堂补充**

待转录补充。

**💡 换个说法（笔记补充）**

算法先指出“这笔和同类差很多”，会计人员再查清原因。

**常见误解**

异常分数不是舞弊结论。算法受变量尺度、距离定义和样本范围影响。

**与其他概念的关系**

它常用于筛查线索；监督模型可在已有调查结论后学习预定义类别。

**所以呢**

无监督输出应进入调查队列，不能直接形成会计定性。

### 2.4 半监督学习（讲义 p.18–21）

**是什么**

半监督学习（Semi-supervised Learning）用少量标注数据和大量未标注数据共同学习（p.18）。

**讲义英文原文（p.18）**：

> Semi-supervised learning sits between supervised and unsupervised approaches. It uses a small amount of labeled data together with a large amount of unlabeled data.


**为什么需要它**

合同专家的时间有限，给数千份合同逐一标注可能不可行。

**课件原例与完整小例**

讲义 p.20 设企业有数千份合同，只能仔细标注几百份；特征可有条款、交易方、付款条件、期限和关键词。模型结合两类数据分类剩余合同。

**可追踪的方法示例（笔记补充，非讲义指定算法或实测）**：仍设专家标注 100 份合同，40 份含自动续约、60 份不含，另有 900 份未标。为说明 900 份怎样参与学习，选一种自训练（self-training）办法：先用人工标签训练初始模型，再把部分预测暂作伪标签（pseudo-label）加入训练；伪标签是模型猜测，不能升级成人工真答案。

1. 先留 20 份人工标签合同作检查集（含/不含续约各 8/12 份），不参与拟合；初始模型只用其余 80 份（32/48 份）学习。特征可为原文条款、关键词及期限，目标是“是否含自动续约条款”，不是决定合同实际上是否续约。
2. 初始模型处理 900 份未标合同。为追踪流程，**设定**其中 60 份的类别分数为 0.95，其余 840 份分数不超过 0.60；这些是示意中间输出，没有运行一个真实分类器。分数是模型对类别的倾向，不是已经校准的真实正确概率。
3. 本示例临时选分数至少 0.90 的 60 份，把模型预测类别记作伪标签，并单独记录其身份；0.90 只为演示筛选，不是行业或课程阈值。
4. 用 80 份人工标签加 60 份伪标签重新训练，共 140 份参与拟合。**900 份正是在第 2–4 步提供候选及新增训练样本**；若移除这 900 份，就没有这 60 个伪标签，训练仍只用 80 份。剩下 840 份此轮不并入。
5. 再用始终留出的 20 份人工标签比较重训前后错误。若错误增加，就撤销这一轮伪标签或调整方法，不能因数据多就宣布改善。真实评估还要有更充分的独立数据，本小例不证明精度。

```mermaid
flowchart TD
 A["100人工标签：80训练 + 20留出"] --> B["80训练初始模型"]
 U["900未标合同"] --> C["模型给候选类别与分数"]
 B --> C
 C --> D["本例筛60伪标签；保留来源身份"]
 D --> E["80人工 + 60伪标签重训"]
 A --> F["20留出合同只评估"]
 E --> F
 F --> G{错误是否改善且风险可接受?}
 G -->|否| H["撤回本轮 / 改方法"]
 G -->|是| I["继续人工抽查；不当真实上线证明"]
```

伪标签若错，重训可能强化自己的错误；跨业务线/法域时，100 份也可能不具代表性。合同判断仍须回原文复核。讲义只要求联合利用两类数据，没有规定必须用伪标签；其他半监督方法也存在。

课件称其可减少标注量，适合文档分类；仍依赖高质量、具代表性的少量标签，无标签噪声也会影响结果（p.19、21）。

**🎙️ 课堂补充**

待转录补充。

**💡 换个说法（笔记补充）**

专家批改少量练习后，模型利用所有材料寻找相似写法；未批改材料提供结构，不会自动提供真答案。

**常见误解**

数据多不能补救标签偏差；样本分布不一致时模型会把错误推广到更大范围。

**与其他概念的关系**

它介于监督与无监督思路之间：有少量正确答案锚定分类，又利用无标签数据。

**所以呢**

先评估标签代表性和人工抽查方案，再判断半监督能否降低工作量。

### 2.5 强化学习（讲义 p.22–25）

**是什么**

强化学习（Reinforcement Learning, RL）让智能体（agent）在环境中行动，根据奖励/惩罚学习策略，以提高长期累计奖励（p.22）。状态是当前信息，动作是选择，环境反馈改变下一状态。

**讲义英文原文（p.22）**：

> Reinforcement learning (RL) is a type of machine learning in which an agent learns to make decisions by interacting with an environment. The agent receives rewards or penalties based on its actions and learns a policy that maximizes cumulative reward over time.

p.22 原图以狗作 agent、训练者作 environment：actions 箭头由 agent 指向环境；rewards 和 observations 从环境返回 agent。会计类比中，这三方向对应选择下一项检查、返回检查结果/奖励、更新剩余时间与风险信息。

```mermaid
flowchart LR
 A["Agent：抽样策略，按当前状态选动作"] -->|"actions：检查哪项或停止"| E["Environment：交易总体 / 模拟审计"]
 E -->|"observations：结果、剩余时间"| A
 E -->|"rewards：预先定义的评价"| A
```

箭头是行动与反馈回路，不是把狗的训练当作审计实证。下一段只用自拟数值解释多次反馈。

**为什么需要它**

审计抽样顺序会影响剩余时间、已知风险和下一步行动，属于连续决策，而非对静态记录单次分类。

**课件原例与完整小例**

讲义 p.24 将抽样策略设为 agent，交易总体设为 environment，下一项检查设为 action。奖励可按错误发现率、高风险覆盖或每小时发现数定义。

**两回合可复做模拟（笔记补充）**：每回合重新开始，审计员有 2 小时，A 为普通费用，B 为新供应商，C 为期末手工分录。同一项每回合最多查一次，也允许停止。状态至少含剩余时间、已检查集合和已观察结果；动作不能超过剩余时间。

下表每行是一项检查；耗时为小时，重大错误/高风险覆盖为本次模拟设定的实际反馈，不是事先知道的真实审计结论。奖励把三部分**相加**：发现重大错误给 5，覆盖高风险给 2，每耗时半小时扣 1。

| 项目 | 耗时 | 模拟反馈：重大错误 | 模拟反馈：高风险覆盖 | 本次奖励 |
|---|---:|---:|---:|---:|
| A 普通费用 | 0.5 | 0 | 0 | 0+0−1=−1 |
| B 新供应商 | 1 | 1 | 1 | 5+2−2=5 |
| C 期末手工 | 1 | 1 | 1 | 5+2−2=5 |

第一回合先探索 A：用 0.5 小时得−1，剩 1.5 小时、已查集合为 A。再查 C，用 1 小时得 5，累计奖励 4，剩 0.5 小时；B 需 1 小时不可选，停止。第二回合改为探索 B：用 1 小时得 5，剩 1 小时，再查 C 得 5，累计 10，时间用完。

学习步骤是把“状态—动作—收到的反馈”记下来，比较从相似起点取得的累计奖励，再调整以后动作选择的倾向。本示例只比较两条已试路径：在所设反馈下，B→C 比 A→C 好，C→B 也能得到 10；不是已证明真实最优策略，更不是声称两次就学会全部审计。真实反馈有不确定性，须多次审计或模拟和足够探索。讲义 p.24 明确写“Over successive audits or simulations”。

**改条件**：若 C 改需 1.5 小时，B→C 共 2.5 小时已不可行。C 自身奖励变为 5+2−3=4；B 独查仍得 5，之后可停止，不能照搬旧路径。若只奖小错数量而不管重大性/耗时，目标会改变，策略可能偏向容易的小错。所有数值、简化比较和停止动作均属笔记补充，不是课程标准或实测。

如果只奖励“发现数量”，策略可能总查容易发现的小错而忽略重大风险；模拟环境不代表真实总体时，策略也会失效。课件列出优点为适合序列决策和反馈优化；缺点是奖励和环境难定义、计算成本与解释/审计困难（p.23、25）。

**🎙️ 课堂补充**

待转录补充。

**💡 换个说法（笔记补充）**

它像不断调整巡检顺序的排班员：每次行动后看结果，再决定下一步。奖励设计决定它追求什么。

**常见误解**

奖励高不等于审计质量高；目标设计遗漏约束时，策略可能优化错目标。

**与其他概念的关系**

监督学习用固定标签学预测；强化学习（Reinforcement Learning, RL）根据行动和环境反馈学策略。

**所以呢**

RL 在此是优化思路示例；实际审计要约束目标、权限、解释和复核。

### 2.6 线性回归与最小二乘（讲义 p.27–30）

**是什么**

**讲义英文原文（p.27）**：

> Linear regression is a statistical method used to model the relationship between a dependent variable (target) and one or more independent variables (features) by fitting a linear equation to observed data.

如果要根据订单批次估计对账工时，可以用直线描述输入与目标的关系。课件给出的观测关系是 $Y=a+bX+e$（p.27）。符号含义如下。

| 符号 | 含义 | 本例读法 |
|---|---|---|
| $X$ | 输入变量；订单批次数 | 一周有 2 个订单批次 |
| $Y$ | 目标变量；实际对账工时 | 该周实际 3 小时 |
| $a$ | 截距；输入为零时的基线预测 | 拟合后为 $1/3$ 小时 |
| $b$ | 斜率；输入每增加 1 单位时预测变化量 | 拟合后每批次增加 $1.5$ 小时 |
| $e$ | 观测误差项 | 实际值与总体关系的差异 |
| $\hat{Y}$ | 模型给出的预测值 | $\hat{Y}=a+bX$ |
| $e_i$ | 第 $i$ 条数据的残差 | 实际工时减预测工时 |

符号表中的 $a$ 和 $b$ 来自下方教学数据，不是课件给出的参数。残差按 $e_i=y_i-\hat{y}_i$ 计算。

**为什么需要它**

回归把“业务量变化时工时如何变化”的问题转为可复算的关系。残差还能显示每条记录的预测差异。

**课件原例**

**讲义英文原文（p.29）**：

> The most common method for fitting a regression line is the method of least squares.

**讲义英文原文（p.29）**：

> It calculates the best-fit line for the observed data by minimizing the sum of the squares of the vertical deviations from each data point to the line.

p.28 图示 X 是输入变量，Y 是待预测的因变量，散点周围画有上升直线。p.29 说明最小二乘法（Least Squares）使观测点到拟合线的竖直偏差平方和最小。p.30 的示意线为 $\hat{Y}=X+4$，箭头表示竖直残差。讲义没有提供绘图数据，因此不能从该图复算参数。p.28、p.30 图已通过原件渲染检查。

**可复算小例（笔记补充）**

假设订单批次 $x$ 与对账工时 $y$ 的教学数据是 $(1,2)$、$(2,3)$、$(3,5)$。每对数字依次表示订单批次和小时数；这组数据仅为笔记示例。

最小二乘选择 $a$ 和 $b$，使平方误差和最小：
$$
SSE=\sum_i(y_i-a-bx_i)^2
$$

先读记号。下表将“索引/相加/平均”的操作分开，每行保留同一三点例的读法。

| 记号 | 怎样读与怎样做 | 本例 |
|---|---|---|
| $i$ | 记录的行号 | 依次为 1、2、3 |
| $\sum_i$ | 把各行所指定的结果相加 | 例如把三个平方残差相加 |
| $\bar{x}$ | 输入的平均数，三批次值先相加再除行数 | $\bar{x}=(1+2+3)/3=2$ |
| $\bar{y}$ | 工时的平均数，三工时值先相加再除行数 | $\bar{y}=(2+3+5)/3=10/3$ |

SSE 是三行残差平方相加，单位为小时²；平方防止正负误差互相抵消，也使大误差的代价更高。

下面的斜率/截距公式适用于有截距的一元最小二乘，并要求$x$不全相同；算完小例后再用高中配方说明公式为何使 SSE 最小。

第一步，计算均值：$\bar{x}=2$，$\bar{y}=10/3$。

第二步，计算斜率。分子逐项计算为 $(-1)(-4/3)+0(-1/3)+(1)(5/3)=3$。分母逐项计算为 $(-1)^2+0^2+1^2=2$。因此：
$$
b=\frac{\sum_i(x_i-\bar{x})(y_i-\bar{y})}{\sum_i(x_i-\bar{x})^2}
=\frac{3}{2}=1.5
$$

第三步，计算截距：$a=\bar{y}-b\bar{x}=10/3-1.5\times2=1/3$。因此拟合式为 $\hat{y}=1/3+1.5x$。

第四步，对每个样本代入拟合式。以第一行为例，$x=1$ 时 $\hat{y}=1/3+1.5=11/6$，残差是 $2-11/6=1/6$，平方残差是 $1/36$。

| $x$（订单批次） | 实际 $y$（小时） | 预测 $\hat{y}$（小时） | 残差 $y-\hat{y}$（小时） | 平方残差（小时²） |
|---:|---:|---:|---:|---:|
| 1 | 2 | 11/6 | 1/6 | 1/36 |
| 2 | 3 | 10/3 | −1/3 | 1/9 |
| 3 | 5 | 29/6 | 1/6 | 1/36 |
| 合计 | 10 | 10 | 0 | 1/6 |

以第二行说明读法：$x=2$ 表示 2 个订单批次，实际工时为 3 小时，预测工时为 $10/3$ 小时。实际减预测得到残差 $3-10/3=-1/3$ 小时，再平方得到 $1/9$ 小时²。

三行预测值合计为 10 小时，与实际值合计相同。残差合计为 0。平方残差相加得到 $SSE=1/36+1/9+1/36=1/6$ 小时²。

**为什么这条线使 SSE 最小：只用平方非负与配方（笔记补充）**

先把每条数据减去各自平均数：$d_i=x_i-\bar{x}$、$q_i=y_i-\bar{y}$。这些“离平均数多少”的数相加都是 0。再把$c=a+b\bar{x}-\bar{y}$定义为平均输入处的预测减平均实际。于是每行残差可改写成$q_i-bd_i-c$。

展开平方后，含$c$的一次项为$-2c\sum_i(q_i-bd_i)=0$，所以：

$$
SSE=\sum_i(q_i-bd_i)^2+n c^2.
$$

这里$n$是数据行数，本例为 3。固定$b$时，前一项不随$a$变化，后一项是非负的平方；选$c=0$能使它最小。这就给出$a=\bar{y}-b\bar{x}$。这一步没有用偏导或“正交”作前置。

再把三种加总记短一点。每项把对象、加总式及本例数值放在一起：

1. 输入偏差平方和：$V=\sum_i d_i^2=2$。
2. 输入/目标偏差乘积和：$S=\sum_i d_iq_i=3$。
3. 目标偏差平方和：$T=\sum_i q_i^2=(16+1+25)/9=14/3$。

当$c=0$时，展开再配方：

$$
SSE=T-2bS+b^2V
=V\left(b-\frac{S}{V}\right)^2+T-\frac{S^2}{V}.
$$

下表把配方中暂用的记号对回同一三点例。每行只给一个量的意义、单位和数值；它们是计算中间量，不是又一组原始数据。

| 记号 | 对象与单位 | 本例 |
|---|---|---|
| $d_i$ | 每行输入减平均输入，单位批 | $-1,0,1$ |
| $q_i$ | 每行工时减平均工时，单位小时 | $-4/3,-1/3,5/3$ |
| $c$ | 平均输入处预测减平均实际，单位小时 | 待选；为最小时取 0 |
| $V$ | 输入偏差平方相加，单位批² | 2 |
| $S$ | 输入/工时偏差乘积相加，单位批×小时 | 3 |
| $T$ | 工时偏差平方相加，单位小时² | $14/3$ |

因为输入不全相同，至少有一个输入偏差非 0，所以输入偏差平方和为正，即$V>0$。配方后最后两项只由数据决定，调整斜率只改变前面的平方项。

取$b=S/V$时，平方项恰为 0；其他斜率使该项为正，所以这正是最小值。再代回截距式，就得到上面使用的两个公式。

本例的最小值为$14/3-9/2=1/6$，与逐行残差平方相加一致。

**零分母边界**：若所有$x$都为 2，每个$d_i$为 0，$V=0$，不能除以它。此时数据只能确定在$x=2$处的预测水平，不能独自确定斜率。

将全部$y$加 1 而$x$不变，则各$q_i$不变，斜率仍 1.5，截距加 1 变为 4/3。拟合的代数性质不证明订单批次导致工时变化。

**图形怎样读（笔记补充）**：下图仅用上述三个自拟点，横轴批次、纵轴小时，实线为拟合值，竖线为同一$x$处的实际减预测。$x=2$的点在线下，残差为−1/3；$x=1$和 3 在线上方，各为 1/6。空心点$x=4$只表示预测 19/3，没有真实工时，因此没有可知的实际残差。

![[AC6761_Artificial_Intelligence_Accounting/notes/figures/m08-novice-review-20261025/regression-three-points.svg]]

图源/数据见[[AC6761_Artificial_Intelligence_Accounting/notes/figures/m08-novice-review-20261025/plot-regression.py|可编辑绘图脚本]]。原 p.28 是上升散点/直线；p.30 左图点落在给定$\hat{Y}=X+4$线上，右图点偏离并用竖直箭头表示差。原图未给完整样本表，不从像素反推精确坐标；本图不冒称复刻了那组未知数据。

**计算流程（笔记补充）**：按刚才的三点例先整理数据，确认输入有变化，才依次求均值、斜率与截距，再逐行计算预测/残差/SSE。若改成所有输入都为 2，图在求斜率前暂停；不能先除以 0 再检查未来适用性。

```mermaid
flowchart TD
 A[整理 x,y] --> CheckX{至少有两个不同的 x?}
 CheckX -->|是| B[计算均值]
 CheckX -->|否| StopFit[暂停斜率拟合：核数据或另选模型]
 B --> C[求斜率 b]
 C --> D[求截距 a]
 D --> E[计算预测值]
 E --> F[计算残差和平方]
 F --> G[合计 SSE 并核对]
 G --> H{新数据仍适用?}
 H -->|是| I[谨慎预测]
 H -->|否或外推| J[重估或换模型]
```

**机制与边界**

平方使大残差权重更高，极端值会影响拟合。SSE 最小只说明样本内按该目标拟合较好，不证明因果，也不保证未来准确。小样本、弯曲关系、结构变化和超范围外推都可能误导；应看散点、残差模式和留出数据，并限定预测范围。

**🎙️ 课堂补充**

待转录补充。

**💡 换个说法（笔记补充）**

直线像一根按规则摆放的尺；点到线的竖直差是残差。最小二乘让差值平方后总和最小，而不是让每个点都在线上。

**常见误解**

总体误差项 $e$ 与拟合后样本残差不是同一对象。回归残差是竖直距离，不是点到直线的斜向最短距离。

**与其他概念的关系**

回归是监督学习的数值预测方法。费用编码是类别预测；两者都需已知结果评估。

**所以呢**

能复算拟合值仍需判断样本是否适合未来业务，不能把预测当承诺。

### 2.7 ML 应用与 DL（讲义 p.8、26、37）

**是什么**

机器学习（Machine Learning, ML）从数据学习预测关系（p.8）。深度学习（Deep Learning, DL）是使用多层神经网络的 ML 分支，适合处理大量图像、音频和文本（p.8、37）。p.7 套叠圆已从渲染图确认 AI ⊃ ML ⊃ DL。

**讲义英文原文（p.8）**：

> Definition: ML is a subset of AI that focuses on the development of algorithms that allow computers to learn from and make predictions based on data.

**讲义英文原文（p.8）**：

> Definition: DL is a specialized area within ML that uses neural networks with many layers (hence "deep"). These networks are particularly effective for handling large amounts of unstructured data, such as images, audio, and text.

**“层”怎样理解（笔记补充）**：输入先变成数值，例如图像的像素；一层中的相连计算单元把前一层的数值作组合，再传给下一层，多次组合后给出类别分数或数值输出。神经网络（neural network）是这种相连处理单元的结构，“深”指多个处理层。早层可能组合局部线索，后层再组合较大模式；这只是理解多阶段处理，不保证某一层必学会人的某种概念。本讲不要求训练权重或反向传播运算。

**为什么需要它**

理解包含关系可避免把 DL 当成独立于 ML 的算法类别，也提醒复杂模型需更多数据和检查。

**课件原例**

p.26 列的是用途目录：推荐把历史互动变成候选排序；语音处理把声音变成文字/指令；图像诊断寻找影像模式供专业复核；目标识别/跟踪寻找图像中的对象及其随帧变化；大数据分析从历史特征找预测线索；分类输出已定义类别、聚类输出待解释群组。名称与产品是讲义示例，具体实现和成效未核。p.37 称 DL 持续胜过早期系统，但没有比较对象、任务或指标，不能推广为普遍结论。

**🎙️ 课堂补充**

待转录补充。

**💡 换个说法（笔记补充）**

AI 是大集合，ML 是其中一类，DL 又在 ML 之内。集合位置说明分类关系，不表示里面的每个系统表现都更好。

**常见误解**

DL 的“深”指多层结构，不代表更懂会计或更可信。

**与其他概念的关系**

监督信号分类与模型结构分类是两条轴；DL 也可以在不同监督设置中使用。

**所以呢**

按任务需要选方法，不能仅因模型名称新或复杂就优先采用。

### 2.8 生活、商业与会计应用（讲义 p.31–35）

**是什么**

AI 应用把数据、方法和具体工作相连。会计例子包括录入记账、异常检测、现金流预测、合规监控和趋势分析（p.35）。

**为什么需要它**

场景说明技术要解决什么问题，但效果需要数据、指标和对照才能确认。

**课件原例**

p.31–34 的数字都是课件声称。讲义未附来源、时期、样本、指标定义或比较基准，因此逐项保留但不作事实认定。

**p.31 · 智能家居与健康**
- Nest：优化供暖/制冷，节省能源账单 12–15%。
- Ring：人脸识别并对可疑活动发出即时提醒。
- iRobot Genius：地图精度 99%。
- Fitbit / Apple Watch：监测健康指标，以 92% 准确率检测问题。
- Babylon Health：简化症状分析，急诊等待时间减少 30%。

**p.32 · 娱乐与交通**
- Netflix：按观看历史推荐内容，每月节省 10 亿小时。
- TikTok：按用户互动个性化 feed，用户留存提高 47%。
- Google Maps：预测交通堵塞，平均通勤时间减少 18%。
- Tesla：用实时物体检测和避撞降低事故率 40%。

**p.33 · 客服与金融**
- Zendesk / Intercom 聊天机器人：解决 85% 常规咨询，响应时间从 10 分钟降至 10 秒，人工成本减少 30%。
- 情感分析：以 90% 准确率识别邮件/社交媒体中的客户不满，以便主动服务补救。
- PayPal：通过实时交易模式分析，每年预防 40 亿美元欺诈。
- Kensho 算法交易：依据市场情绪以微秒级交易，取得比人类交易者高 20% 的回报。

**p.34 · 零售与制造**
- Amazon：按购买历史和浏览行为提供超个性化推荐，产生 35% 销售。
- Walmart：库存 AI 预测需求激增，准确率 98%，缺货和浪费减少 25%。
- Siemens：预测维护传感器提前 48 小时发现设备问题，停机减少 45%，每厂每年节省 170 万美元。
- 计算机视觉：每分钟检查 200 件，原文是 99.9% **precision**，对比人类 95%；讲义未定义其分母/评估协议，不把 precision 静默当成 accuracy，也不据此认定数字可比。

p.35 的五项会计用途没有效果数字，下面逐项读它们解决什么问题。

- **例行任务自动化**：单据字段进入系统，规则/模型提出编码，核验与授权后才记账；减少重复输入，不免除错误检查，具体流程见§2.9。
- **异常检测**：在分录中找不同寻常的金额/时点/科目组合，输出调查线索，再核业务证据，不能把线索直接当舞弊。
- **现金流预测与规划**：已知期初现金、预计收款与付款时间，可以逐期算余额，找可能短缺的时点。自拟一周例为期初 100、预计收 80、付 150，预测期末 30；若 80 延期未收，当周期变成−50，应核融资或支付安排。这里是预测情景，不是已经收到钱；ML 可帮助估计金额/时点，仍要核假设。
- **风险/合规监控**：把交易与适用规则比对，提出异常和待查依据，负责人确认主体、法域、时点与原规则后采取行动。大量数据扫描不等于自动保证守法。
- **趋势分析**：按一致期间和口径比较历史数据，定位变化并进一步查原因；看到趋势不证明原因、也不保证它持续。

教学工作流：发票进入系统→OCR 提取→规则/ML 校验→低置信或不匹配时人工复核→获授权后 RPA 录入→保存凭证与审批日志。此为笔记补充，不代表课件报告的部署。

**🎙️ 课堂补充**

待转录补充。

**💡 换个说法（笔记补充）**

模型可以产生线索或草稿；会计人员核实证据后才形成账务判断。

**常见误解**

案例和公司名称不能证明宣称数字。效果需可追溯的原始来源及清楚的分母和比较基准。

**与其他概念的关系**

ML 提供预测/聚类，OCR/NLP 处理输入，RPA 执行规则化动作；错误可沿链条传播。

**所以呢**

把自动化流程按输入、校验、审批和日志拆开，才看得见控制点。

### 2.9 OCR 与 RPA（讲义 p.36、40–41）

**是什么**

**讲义英文原文（p.41）**：

> Optical Character Recognition (OCR) is a technology that converts text from scanned or digital documents into machine-readable text.

**讲义英文原文（p.40）**：

> Robotic Process Automation (RPA) primarily handles structured data and is best for rules-based transactions.

光学字符识别（Optical Character Recognition, OCR）把扫描或数字文档文字转换为机器可读文本（p.41）。机器人流程自动化（Robotic Process Automation, RPA）按规则处理结构化数据和系统操作（p.40）。

**为什么需要它**

OCR 将图像内容转成候选字段；RPA 可将核准字段用于订单匹配、报销检查、对账或应收发票录入。

**课件原例与输入输出**

课件 p.40 的应付账款（Accounts Payable, AP）流程会匹配供应商发票与采购订单、核差旅政策、对账；应收账款（Accounts Receivable, AR）流程先检查客户发票授权与价格，再过账到收入账户。这是源中的自动化例，不能推出所有发票均已满足收入确认条件。企业资源规划（Enterprise Resource Planning, ERP）在这里指保存业务/账务记录的系统，不要求先学它的架构。OCR 可减少输入并使文档可搜索，讲义未给误差率。

表中幂等（idempotency）指同一获批发票即使因断线重试，也只产生一次应有录入结果。例如先查“供应商+发票编号+期间”等可靠身份是否已处理，成功后记录状态；重试不能无条件再插一笔。具体去重键、事务和故障恢复实现仍须另行验证，此处只解释控制目标。

| 阶段 | 输入 | 中间输出 | 失败与控制 |
|---|---|---|---|
| OCR | 扫描发票 | 供应商、日期、金额候选字段 | 模糊/错位/小数点误读；低置信转人工并与订单核对 |
| 校验 | 字段、订单、政策 | 匹配状态和异常项 | 重复/币种不符；暂停处理并留痕 |
| RPA | 已通过校验的字段 | ERP 草稿或匹配结果 | 页面变化/权限错误/重复操作；授权、幂等检查、日志 |


下面把发票从读取走到入账，箭头表示处理顺序。每行阶段表说明谁接收什么，流程图补出不通过时的去向。

```mermaid
flowchart TD
 A[扫描发票] --> B[OCR候选字段]
 B --> C[核订单与币种并查重复]
 C --> D{校验及授权通过?}
 D -->|是| E[RPA录入并留日志]
 D -->|否| F[人工复核并暂停自动录入]
```

**走图例（笔记补充）**：订单是 100 元，OCR 错读成 1,000 元。金额不匹配使流程走向人工复核；复核后重新校验并获批，才允许 RPA 录入 100 元。未经批准时，终点是暂停，不是自动修成某个数。

看不到图时，主线是“读出候选、核验、审批、再录入”。这些控制属于笔记补充方案，原课件没有提供系统实现。

**读图自测**：金额正确但没有录入权限，应走哪条路？

<details><summary>答案</summary>

走否分支，暂停自动录入并交人工处理。金额正确只通过数据核验，仍未通过授权。

</details>

**🎙️ 课堂补充**

待转录补充。

**💡 换个说法（笔记补充）**

OCR 像把纸表转成可搜索文本；RPA 像按清单搬运信息。前者可能读错，后者可能忠实执行错误输入。

**常见误解**

OCR 不等于理解语义；RPA 不必然使用 AI。自动操作需要异常队列和审批边界。

**与其他概念的关系**

OCR 输出可供 ML/NLP 校验，RPA 执行已确认的规则动作；任何环节出错都可能污染后续记录。

**所以呢**

在自动过账前验证关键字段并控制权限，避免错误被高速复制。

### 2.10 NLP、GenAI 与会计控制（讲义 p.36、38–45）

**是什么**

自然语言处理（Natural Language Processing, NLP）分析文本；可做摘要、合同信息提取和监管文本审阅（p.38）。生成式 AI（Generative AI）根据提示生成内容，可用于报告或财报草稿（p.39）。

**为什么需要它**

合同、评论和法规是文本。NLP 可整理内容，GenAI 可组织草稿；二者都需把输出追溯到原文。

**课件原例**

p.38 说评论可辅助退货准备估计/库存短缺判断。机制是先从评论抽取退货原因、缺货投诉等线索，再与实际销售、退货和库存数据核对；情绪文本本身不能给出应计准备金额或证明实际缺货。合同字段与监管原文也须回源，不能由一句摘要直接形成会计结论。

**讲义英文原文（p.38）**：

> Natural Language Processing (NLP) interprets words rather than numerical data.

原句“rather than numerical data”是本页的文字任务对照，不表示 NLP 系统不会使用数值表示或不能处理文本中的金额。

**讲义英文原文（p.39）**：

> Generative AI refers to the ability of certain deep-learning models to rapidly create content in response to text prompts. This technology marks a significant advancement in AI, as it can understand and generate natural language.

中文要点：本页说某些深度学习模型按文本提示生成内容；“understand”在此是任务表现描述，不据此认定它拥有人的理解或会计责任。

#### 2.10.1 工具名单怎样分类（讲义p.42）

p.42 列 ChatGPT、Claude、Copilot、Excel、Python、Vic.ai、Truewind、Karbon 等。前几项可作为助手/应用名称，Excel 是表格平台，Python 是编程语言；后面几个是会计相关工具名称。Excel/Python 可以承载或调用 AI 工作，但仅有名称不等于每项自身都是 AI 模型。讲义未给版本、权限、功能测试和排名，不能从名单推当前能力或推荐顺序。

#### 2.10.2 会计工具的六阶段变化（讲义p.43）

每行是一段课件概述；“新增能力”说明输入怎样更容易进入后续处理，不表示后一阶段完全替代前一阶段，年份和采用范围均未独立历史核验。

| 课件阶段 | 新增处理能力与仍需保留的检查 |
|---|---|
| 手工记账时期 | 人逐笔准备记录/报表，资料整理和核算依赖人的细致工作 |
| 1980 年代电子表格 | VisiCalc、Lotus 1-2-3、Excel 帮助输入/费用管理与公式计算；公式和引用错误仍会传播 |
| 1980 年代 OCR 采用 | 从发票图像提取文字，减少重录；错字、版面和金额仍要校验 |
| 1990 年代早期 AI | 人工神经网络用于舞弊检测、财务预测的尝试；讲义称复杂性限制采用，未给采用率 |
| 2000 年代 ML 增长 | 更好的算法支持预测、分析和风险评估；数据/标签/评估决定是否适用 |
| 2010 年代及以后 NLP 工具 | 处理语言、报告草稿及实时数据，支持预测线索；及时不等于正确，生成句仍须回原文 |

例如同一发票经历“手工重录→表格求和→OCR 提字段→模型建议编码”，每一步改变处理方式，却都要核金额、分类、权限与凭证。课件给演变概述，不证明某公司已完成这条路线。

#### 2.10.3 五项潜在优势怎样产生（讲义p.44）

课件把这些列为 advantages；下面补出条件链，而不是宣称已达到收益。

1. **Automation 自动化**：输入/编码/对账/开票的重复动作减少，可腾出时间给策略、客户和学习；若异常队列很大，节时未必兑现。
2. **Accuracy 准确性**：一致规则或模型可处理重复数据、提示人漏掉的模式；错误输入/规则也会一致地错，必须看具体指标与复核结果。
3. **Cost Savings 节约成本**：重复工时下降才可能降低成本或承接更多客户；还需扣软件、培训、复核和迁移成本，不能把节省分钟直接当利润。
4. **Real-Time Insights 实时洞察**：最新交易进入一致口径的报表，管理者更早看到变化；数据晚到、未核或口径不同会让“实时”失真。
5. **Enhanced Security 增强安全**：识别异常模式、通知合适负责人能更早调查/阻断；它不是不会泄露或不会舞弊的保证，权限与响应仍必要。

#### 2.10.4 四项成本与质量控制（讲义p.45）

- **Learning 学习新软件**：离开熟悉平台要重新学操作，原熟练速度会暂时下降；不是用户不会会计。
- **Training 培训**：员工和整个事务所需要时间与专门培训，费用可能增加；须安排负责人与练习/求助渠道，不能只采购软件。
- **Switching Costs 转换成本**：调整流程与迁移期间可能先掉产能，回报不立即出现。课件说“typically follows quickly”，但没有时长/样本，不能承诺快速回本。
- **Quality Control 质量控制**：过度采信自动建议会记错科目/金额，应复核建议。课件提 find-and-recode，是寻找符合条件的已录项目并重新编码；改之前要核筛选范围和授权，避免把一条错建议批量改成另一种错，并留变更记录。这是功能含义，未实际验证某产品按钮。

**输入—中间输出—失败—控制（笔记补充）**

合同原文进入系统后，NLP 分段并提出金额、期限、续约和付款字段；模型输出候选字段与原文位置；GenAI 可据此生成摘要草稿。若扫描不清、附录遗漏或把“不得续约”读成“可续约”，摘要会误导。会计人员需逐条打开原文，核实政策并签核。无法回到原文的句子不应采纳。保存版本、访问记录和审批证据。

**🎙️ 课堂补充**

待转录补充。

**💡 换个说法（笔记补充）**

摘要像合同的索引卡，不是合同本身。流畅表达不能替代原文证据。

**常见误解**

文本抽取准确不等于会计判断正确；生成内容可能虚构条款。深度学习、NLP 和 GenAI 有交叉，不是互斥技术名单。

**与其他概念的关系**

OCR 先把图像转成文本，NLP 处理文本，GenAI 生成草稿，RPA 执行获批动作。每一步需保留可追溯来源。

**所以呢**

专业判断与签核责任仍需落在人，模型输出必须可核、可退回、可记录。

## 3. 一图看懂

下图按可用反馈区分学习类型，箭头表示分类对应，不表示训练先后。OCR 入账的局部流程另见 §2.9。

```mermaid
flowchart LR
 A[有标签] --> B[监督学习]
 C[无标签] --> D[无监督学习]
 E[少量标签和大量无标签] --> F[半监督学习]
 G[行动与环境反馈] --> H[强化学习]
```

图只按训练时实际利用的反馈分类，没有画单据工作流。半监督须同时利用人工标签与未标数据，不是只看数量；OCR 到 RPA 的工作流在§2.9，仍须校验和授权。

## 4. 速查表

| 方法 | 训练或处理时的输入 | 输出 | 会计用途 | 限制 |
|---|---|---|---|---|
| 监督学习 | 已标注样本 | 类别/数值预测 | 费用科目分类 | 标签偏差、漂移 |
| 无监督学习 | 无标签样本 | 群组/异常分数 | 分录筛查 | 异常不等于舞弊 |
| 半监督学习 | 少量标签+大量无标签 | 分类结果 | 合同分类 | 代表性与噪声 |
| 强化学习 | 状态、动作、反馈、奖励 | 决策策略 | 抽样优化设想 | 奖励设计、解释性 |
| 线性回归 | 拟合需特征及实际目标；预测时只给新特征 | 预测值；实际目标已知后才算残差 | 工时/现金流估计 | 输入须有变化，线性假设/外推另核 |
| OCR | 图像/扫描件 | 候选文本字段 | 发票读取 | 模糊、版面错误 |
| NLP | 文本 | 摘要/抽取 | 合同与法规 | 上下文遗漏 |
| GenAI | 提示与上下文 | 新文本草稿 | 报告辅助 | 幻觉、来源断链 |
| RPA | 结构化输入和规则 | 系统动作与日志 | 匹配、录入 | 规则或权限错误 |

例如“监督学习的训练输入是已标注样本”描述模型训练阶段；上线新发票尚无标签，模型正要预测它的科目。

## 5. 双语术语卡

下表英语为**笔记自拟参考定义**，不是整表逐字讲义原文；原句及过宽口径见正文对应节。

| 中文 | English | 笔记自拟英文参考定义 | 首现位置 |
|---|---|---|---|
| 人工智能 | Artificial Intelligence | AI systems simulate functions such as learning, problem-solving, decision-making, and language understanding. | §2.1 / p.2 |
| 窄人工智能 | Narrow AI | Narrow AI performs specific tasks but does not automatically transfer knowledge to unrelated tasks. | §2.1 / p.3 |
| 人工通用智能 | Artificial General Intelligence | AGI refers to human-like adaptability across a broad range of tasks. | §2.1 / p.3 |
| 机器学习 | Machine Learning | ML develops algorithms that learn from data and make predictions. | §2.7 / p.8 |
| 深度学习 | Deep Learning | DL is a specialized area of ML using neural networks with many layers. | §2.7 / p.8 |
| 监督学习 | Supervised Learning | It learns a mapping from inputs to known outputs using labeled examples. | §2.2 / p.10 |
| 无监督学习 | Unsupervised Learning | It searches for patterns or structure in unlabeled data. | §2.3 / p.14 |
| 半监督学习 | Semi-supervised Learning | It combines a small labeled dataset with a larger unlabeled dataset. | §2.4 / p.18 |
| 强化学习 | Reinforcement Learning | It learns a policy through interaction with an environment and reward feedback. | §2.5 / p.22 |
| 线性回归 | Linear Regression | It models a target as a linear function of one or more features. | §2.6 / p.27 |
| 最小二乘法 | Least Squares | It fits a line by minimizing the sum of squared vertical residuals. | §2.6 / p.29 |
| 残差 | Residual | A residual is the observed value minus its fitted value. | §2.6 / p.27–30 |
| NLP | Natural Language Processing | NLP processes human language, for example by summarizing text or extracting contract information. | §2.10 / p.38 |
| 生成式 AI | Generative AI | Generative AI creates content in response to prompts. | §2.10 / p.39 |
| RPA | Robotic Process Automation | RPA automates rule-based tasks involving structured data. | §2.9 / p.40 |
| OCR | Optical Character Recognition | OCR converts document text into machine-readable text. | §2.9 / p.41 |

## 6. 考点预判与答题框架

### 6.1 可信度分级

- 🟡 ILO 反推：CILO 2 要求识别会计中的 AI 技术和模型；课程前置资料没有权重，不能推算考试概率。
- ⚪ 笔记推断：学习方式比较、回归拟合步骤、OCR/RPA 流程控制适合检验理解。
- 无转录，当前没有教授明示考点。

### 6.2 考点清单

1. 根据训练信号判断四种学习方式，说明会计用途和限制。
2. 说明异常检测结果为何需要人工调查。
3. 复做最小二乘计算，并用平方非负/配方解释为何 SSE 最小；不要求未经教学的偏导或正交。
4. 描述 OCR 到 RPA 的输入、输出、失败点和审批控制。

### 6.3 答题框架

分类题写“反馈/标签→学习目标→输出→会计例→风险”。回归题写“变量→斜率→截距→预测与残差→SSE→适用边界”。工具题写“原始材料→转换→校验→动作→人工例外→日志”。

**完整英文作答示范（笔记自拟）**

- **Learning method**: Use supervised learning when historical invoices have verified account labels. Unlabeled contracts contribute to semi-supervised training only if the method actually uses them; pseudo-labels are predictions, so they require separate evaluation.
- **Regression**: Fit a line by minimizing squared vertical residuals. The slope formula requires variation in the inputs. For a future input, the model predicts a value; its actual residual is unknown until the outcome is observed.
- **Control**: OCR extracts candidate fields, while RPA performs authorized rule-based actions. Validate the amount, currency and invoice identity, review exceptions, and prevent a retry from creating a duplicate entry.
- **AI adoption**: Automation may reduce repetitive work, but migration, training and review have costs. Check the original evidence before accepting a generated report or an automatic coding suggestion.

这些完整句帮助把中文机制转为英文作答，不是教授规定句式或得分保证。

## 7. 自测

1. 手上有一批历史发票及各自核准科目，想预测一张新发票的科目，优先用什么学习方式？历史标签属于哪批数据？
2. 异常模型标记大额耗材分录，能否直接断言舞弊？
3. OCR 与 RPA 的工作分别是什么？小数点误读应如何拦截？
4. 数据 (1,2)、(2,3)、(3,5) 的最小二乘预测式是什么？X=4 的预测为何谨慎？

<details><summary>答案</summary>

1. 监督学习。标签是历史发票的已核准科目；新发票正等待预测，不能说它已经有正确答案。英文参考：Use supervised learning with verified historical invoice labels, then predict an account for the new invoice.
2. 不能。应核原始发票、采购订单、审批、供应商及业务背景。英文参考：An anomaly is an investigation lead, not proof of fraud.
3. OCR 提出机器可读字段，RPA 按规则操作系统。金额应与订单、总额和审批交叉核对；不一致转人工。英文参考：Validate the candidate amount and authorization before RPA posts the invoice.
4. $\hat{y}=1/3+1.5x$；$x=4$得$19/3\approx6.33$小时。它超出样本范围，且只有三个教学点，需先验证关系和代表性；没有实际$y$，不能给该新点真实残差。英文参考：The prediction is approximately 6.33 hours, but it is an extrapolation from only three teaching observations.

</details>

## 8. 讲义页码映射

| 小节 | 页码 | 覆盖内容 | 课堂状态 |
|---|---:|---|---|
| §2.1 | 2–7 | AI 定义、类型、发展史、SmartArt | 待转录 |
| §2.7 | 8、26、37 | ML/DL、ML 应用、DL | 待转录 |
| §2.2–§2.5 | 9–25 | 四类学习、特点、例子和优缺点 | 待转录 |
| §2.6 | 27–30 | 线性回归、拟合/竖直残差原图说明及三点补图 | 待转录；图像核对不证明已讲授 |
| §2.8 | 31–35 | 生活/商业/会计案例 | 待转录；数字未核源 |
| §2.9–§2.10 | 36、38–45 | 技术输入输出、工具类别、六阶段演变、五优势与四成本/控制 | 待转录 |

p.1 是封面，且 §2 开头明确说明不属内容页；p.2–45 均有正文覆盖。

复算附件：[[AC6761_Artificial_Intelligence_Accounting/notes/figures/m08-checks/regression_recalc.py|三点回归脚本]] 与 [[AC6761_Artificial_Intelligence_Accounting/notes/figures/m08-checks/regression_recalc_result.txt|精确分数结果]]。

## 9. 延伸与勘误

### 9.1 课件有但课上略过

转录缺失，待核，不能判断哪些内容略过。

### 9.2 课上讲了但课件没有

转录缺失，待核；speaker notes 全空。

### 9.3 课件自身的问题

- p.7 渲染图确认 AI ⊃ ML ⊃ DL 的套叠关系；p.8 文本也支持该关系。
- p.27 的 $Y=a+bX+e$ 是含误差项的观测关系；预测拟合式应区分写成 $\hat{Y}=a+bX$。
- p.30 的 $\hat{Y}=X+4$ 未给生成数据，只能读作示意线。
- p.31–34 的产品效果数字没有来源/口径；不当作已核实事实。
- p.37 的“持续优于”无比较对象或指标，不能推广。
- p.42 工具名单没有版本或测试依据；不表示推荐排名。

### 9.4 课外补充

回归三点手算、监督分类、异常筛查、半监督合同、RL 奖励与 OCR→RPA 流程均为笔记补充例，不是课件实测。

### 9.5 待核对

- 转录到位后核验课堂讲授、略过和新增内容，并填课堂状态。
- 课件历史、公司效果、产品数字需回源核口径后才能引用。
- Week 8 PPT 现已在 course_files_export 归档，本次只读核 SHA 与 45 页/图/SmartArt；没有待归档缺口。实际授课日期、课堂是否讲过/略过及转录仍未知。
