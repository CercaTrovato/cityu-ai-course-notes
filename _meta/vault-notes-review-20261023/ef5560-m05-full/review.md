# EF5560 M05 全篇重审主报告

本任务仅制作 scratch 候选与可复查交接包。正式主写者是原笔记重审会话，本会话没有写 vault、共享完整性 manifest、全库进度、README、Notion、Canvas、Git 或配置。

## 版本、范围与实际模型

- 作者 `/root`，chat `01a17880-ce9e-7390-876c-f980eae405af`；当前请求模型从本机实际 `turn_context` 核为 `gpt-6.1-sol`，证据 `model-check.json`。未按默认配置推测，也未修改provider/模型/历史。
- 原稿实际字节 `baseline.md`：SHA-256 `278688109be29ba9c4cc1531e66ddfecc12252f00c9364eb77a8d809e33bcb7b`，与派单期望一致。最终候选 `candidate.md`：SHA-256 `365c6086f9f03d173b1ecbcfbf9c9a4020fb36c309c9bd10c81e3478e25d44a3`。真实全差异 `candidate.diff`；修复差异 `repair-v1.diff`。
- 完整§0–§9、37正文学习单元、全部折叠/公式/10 Mermaid/8 SVG嵌入上下文、6页14作答单元与5自测均完整读。54页讲义全部抽读，53页在正文有对应（其中4章节标题有衔接说明），p1封面；纯图重点承接同源真实显示证据并实际查看p12。

## 来源与计算

真实讲义54页：`Lec05_Interpretable_Machine_Learning_and_Portfolio_Decisions.pdf`，SHA `02eb0d14e1ada91fe73d3c1f933aa7d1e4c96b17297e0c855f33b8ef675f731f`。Class05的20CSV、README和manifest共22个输入逐项hash与旧已执行记录一致；完整字段/形状/缺失概览为data-inspection.json，哈希承接为inherited-evidence.json。没有重新训练/重复跑未变模型；12个历史脚本/结果快照已复制入本任务inherited/并核hash，重要数字及精度按其真实范围承接，不把结果一致当教学认证。

原转录M05-transcript-partial.txt SHA `91597aa604ff8a56d77f7f05c80dd0ebbb242b33e1ea7f4afa32f2f59ec7b819`，与source.json一致；867保留段/865唯一秒值，00:00–02:26:51，无≥120秒时钟空档。全文读完，完整去向align.md；末尾有结束语，不能沿用“止于02:26:27/缺尾”结论。dropped.json的5段保留为历史过滤候选，未核音，不把“重复幻觉”标签当本次已听校证明；其中重复名/过渡短句未转为教学遗漏或私人姓名公开。开头直接进入作业提醒，课堂完整起点仍未知。

p21/25/26/27/43/49的完整题面、数据、全部选项和小问已回源，中文逐问/逐项解析保留，补齐独立英文参考答案；source-checks.json列6题14个作答单元。p25接近1、p26为10%有课堂确认，p27数值ASR不清不认证为教师答案，p49概念讲解不升级全部数字官方确认。

本次新增实际运算仅为配平方/四行误差/时间分区和理想化单期ETF倍数，见new-calculations.json及repair-calculations.json：交叉项抵消后全目标与两单列平方目标一致，负斜率跨零两半轴最小均为0；8811秒分区相加正确。这些是明确标注的笔记补充，不是新实证指标。

## 一次自查、独审与集中修复

完稿冻结candidate-frozen-v1.md（c6e08c…）后才派独审。独审 `/root/ef05_independent`，agent `01a17892-4bbb-7171-8fbf-3e8b2ba1182e`，显式model=gpt-6.1-sol、fork_turns=none；实际请求模型也由其model-check.json核实。先只候选初读stage-1.md落盘，作者读取确认后才follow-up提供规则/源/diff/疑点。平台自动带入规则与候选历史记录已披露，不假称完全盲审。

原全篇独审与第二阶段核查在reviewer/independent-review.md，37单元实际复做清单在stage-1.md。三组阻塞集中修复一次：B1四行正交数据、目标展开、两半轴与零端点；B2规模/价值特征买空例与未核网页边界；B3杠杆/反向ETF、基金费用及单股CAPM同期解释/事前预测。S1–S3只简短澄清NATR背景范围、切点只识名、指数值工具计算，不拓宽任务。

同一原审查者只定向复核真实修复及直接依赖，亲自写targeted-recheck.md，绑定最终SHA，B1–B3全部关闭，实质教学/材料阻塞0。原报告与stage1保留，未让作者换身份，未另派多轮全文评分。独审没有实看图像；视觉由主代理单列负责。

## 机械疑点与实际显示

冻结版current L/C/R PASS（R硬0/C硬0），6题清单契约通过；443警告已列齐位置并由作者warnings-disposition.md及独审warning-audit.md实质分类。真实LASSO缺桥梁没有被机器0硬错掩盖，已按独审修文。最终门槛输出以release-gate.txt为准；historical G/E仍保存原始FAIL，不冒称旧strict通过。

最终transcript audit PASS：37标准课堂补充格、364时戳/73机器识别引文，未匹配0、A13/A14为0；另新增3课堂应用段。A10紧邻时间/原话，A12逐页引用并集73%与行政/课间/离题区间的区别已在align.md及独审报告解释，不虚填覆盖。候选49个wiki链接定向检查见links.json，最终若只是行号移动不改链接目标则承接；不运行全库评分。

新增/受影响显示用自己8814同源HTML+MathJax/Mermaid在IAB后台自建标签逐窗口实看，6页英文题面、英文答案、新LASSO表/配平方/边界、均值方差说明、3课堂段均可读。截图和精确载体见visual-review.md。未变10 Mermaid与8嵌入逐字符串相同，7张m05数据图及CAPM教学图源/输入按真实hash与已有显示记录承接。新旧视觉不能混称；未逐式查看950个MathJax容器，未直接打开原生Obsidian。没有关键新图显示阻塞。

## 保留限制与交接边界

实际授课日期未证，candidate date/week为null；下载日不推成上课日。原森林及p12网格缺失、网页行情/股名/ETF具体条款/外部论文与网站当前状态未重新联网核、原音未全听校，全部保留范围限制。课程书面与口头的SSE必增/推断/零现金/mean与CAGR/交易比例差异已明确，未把课堂简化当恒等式。8/15页及附件行政冲突仍待当前官网核定，不标作业可提交或本人已提交。

sync-draft.md包含每个§6适用目标、真实本地基线hash与Notion目标/拟写备注，不写共享文件或外部状态。Notion本次未实时读取，因此没有伪造实时写前值/回读；主写者需重读、精确合并并回读。保护本人通读/自测/复习/提交/评分字段。最终完整性与CAS候选/source复核以handoff.json记录，正式写回与同步/Git均未执行。


最终纯维护映射：独审实际复核版本 SHA 为 `2a4dd1bd8af1f995093802fbd88e16ccd5120e73999407d5fdadd8b5a59e46d9`；其后仅按 `format-only.diff` 分段及将 `<` 改为等价 LaTeX `\lt`。主代理核差异不改变教学含义，并在 IAB 实看 `visual-format-lasso.png`、`visual-format-natr.png`，950个容器中无mjx-merror。最终 SHA 为 `365c6086f9f03d173b1ecbcfbf9c9a4020fb36c309c9bd10c81e3478e25d44a3`，映射保存在 maintenance-mapping.json。未声称原独审者读过此格式版哈希，不因无语义变化重开全文审查。
