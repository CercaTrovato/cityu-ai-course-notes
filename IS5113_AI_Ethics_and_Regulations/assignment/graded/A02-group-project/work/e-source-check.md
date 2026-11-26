# IS5113 Group 17｜E 来源核查与组内交接稿

2026-11-07 · 对照 37 页组稿及演讲备注。以下是本人可审阅的核查与英文改句候选。组内采纳、报告合稿和本人实际核验贡献待分别登记。

## 逐项核查

PPT 页码与论文 PDF 页码分别列出。T1/T2/R2/R3 是组稿引用编号。论文中的实验结果可以为行业政策提供理由，具体措施和效果需另行验证。

| 引用与 PPT 页 | 原文位置与实际观察 | 核查结论与建议 |
| --- | --- | --- |
| **T1** · 第 13–15、24、27、35 页 | Mall 等，ICCV 2019。§3.1，PDF p.3／印刷 p.413。研究把基于 Instagram 的 StreetStyle 与 Flickr 100M 的照片结合，按六大洲 44 个主要城市归类并做人物检测、裁切，共约 770 万张人物图片。§3.2，PDF pp.3–4／印刷 pp.413–414，使用带长期变化与周期项的模型拟合趋势。属性序列是各城市各周样本的校准后属性概率均值，详见 §3.1 末段。§4.1 表 2，PDF p.6／印刷 p.416，分别比较属性趋势未来 1 周与 26 周，风格组合表列 26 周。§4.4–5，PDF p.8／印刷 p.418，另在 Barcelona 的 Flickr 样本检验，作者仍把识别和缓解社交媒体影像偏差列为未来问题。 | 预测方法有依据。第 13 页及备注把 “street images” 精确为 “Instagram and Flickr photos grouped by city”。第 27、35 页补 §3.1、§4.1 表 2 和 §5。第 14 页保留“可能覆盖不足”，第 15 页先查覆盖与标注误差，再比较预测误差。样本中估计的属性流行程度、实际人口穿着和商品销量是三个不同量。此研究未测 Nike 预测或某文化已被系统性忽视。[T1 ICCV 原文](https://openaccess.thecvf.com/content_ICCV_2019/papers/Mall_GeoStyle_Discovering_Fashion_Trends_and_Events_ICCV_2019_paper.pdf) |
| **T2** · 第 15、24、28（备注）、35 页 | Carlini 等，USENIX Security 2023。摘要 PDF p.2／印刷 p.5253。§4.1–4.2，PDF pp.4–6／印刷 pp.5255–5257，定义并检验近似复现。Stable Diffusion v1.4 的定向实验使用重复度高的训练图对应描述，反复生成并筛查近似输出。§4.2.2 和图 3，PDF p.6／印刷 p.5257，94 张达预设距离阈值，另人工确认 13 张，合计 107 张近似副本。 | 第 15 页“原创性审查”有风险依据。第 28 页正文未列 T2，可补一行，或仅把 §4.2.1–2 与图 3 加到现有备注。摘要跨实验的数量与 v1.4 这一项结果口径不同。定向抽取没有给出普通使用时的复现概率。输出复现、训练授权、是否侵权及作品可版权性需要分别判断。[T2 USENIX 原文](https://www.usenix.org/system/files/usenixsecurity23-carlini.pdf) |
| **R2** · 第 11、29、37 页 | Wadinambiarachchi 等，CHI 2024。§3.1–3.2，PDF pp.4–5。60 人限时 20 分钟，先看头像示例，三个条件分别为无额外工具、Google 图片搜索、Midjourney V4。研究以草图中沿用示例的 14 种显著特征的比例来操作化固着。§4.2 图 6，PDF p.8，可用生成式 AI 条件比无额外支持的基线固着更高。§5.4，PDF p.16，讨论工具熟练程度、等待时间等限制。 | 第 11、29 页方向正确。补上共同示例、工具与测量，避免把“无额外支持”读成未看示例。图 6 的预测比例与表 1 的模型系数不同，别把 .32 写成固着增加 32 个百分点。头像任务无法给 Nike 鞋履原创性打分，也无法说明所有设计流程都会受同样影响。[R2 作者原文](https://qiushi-zhou.github.io/PDF/CHI-2024-AI.pdf) |
| **R3** · 第 32、37 页，第 11、15 页答问可引用第 32 页 | Doshi 与 Hauser，arXiv v3，2024-03-14。PDF pp.2–3，293 人随机分到人写、可用 1 条或至多 5 条 GPT-4 点子三种条件，写八句英文故事，600 名另行招募的读者评分。Results PDF pp.4–6 图 2 比较单篇评价。PDF pp.9–10 图 5 用文本嵌入比较每篇故事与本组其他故事的平均内容表示。 | 第 32 页“评价更好，同时组内更像”可保留。将 “AI-assisted stories” 改成 “stories written with access to GPT-4 ideas”，因为实验比较的是可使用点子的条件，有人可选择不用。将 “became” 改成与无 AI 点子组的横向比较。第 37 页保留 v3，补图 2、图 5 定位。备注注明相似度以同组其余故事的平均内容表示为参照。该结果用于提出分别评估单件质量和整批多样性的建议。[R3 v3 原文](https://arxiv.org/pdf/2312.00506v3) |

## 公司自述与研究分开

- **第 11、27 页，K1。** Nike 官方特写 Phase Two 开头第 2–3 个正文段提到有些早期呈现 Air 的 AI 图采用相近的流动风格，设计师从中挑选能让概念走向不同方向的灵感。这里可把第 11 页的 “similar concept aesthetics” 精确成 “a similar fluid aesthetic in many early AI images interpreting Air”。此来源是 Nike 的流程自述，描述早期探索，未测量最终系列整体原创性。[Nike A.I.R. 特写](https://about.nike.com/en/magazine/nike-design-athlete-imagined-revolution)
- **第 13、27 页，K3。** Nike 2019 年 8 月 6 日公告首段及介绍 Celect 平台的第三段，支持收购与以细分地区需求预测帮助库存优化的用途。A.I.R. 介绍概念设计。现有引用没有建立 Nike 当前潮流预测模型、GeoStyle 部署或与 A.I.R. 的集成。[Nike Celect 公告](https://investors.nike.com/news-events/press-releases/detail/103/nike-inc-acquires-data-science-and-demand-sensing-expert-celect)
- **第 14–15 页，组内分析与建议。** 数据覆盖不足、预测误差影响生产、相似性疑点和审批责任是风险推理及控制建议。第 15 页现写“按地区和人口组测试误差”，落实时先明确预测目标和参考结果，按有足够样本的目标市场检查覆盖和误差。只在有适用依据、可靠标签及足够样本时做人口分组。缺可靠分组数据时记录缺口，必要时补充合适的数据或限制用途。设计审查分两道：明显相似的图查来源与权限，整批概念再看是否过度集中于一种设计路线。第 15 页口播把 “The existing design review” 改为 “Our proposed design review”，以免被理解成 Nike 已有的制度。文化授权、法律和生产影响由对应分工核对后合稿。

## 英文改句候选

| 页码 | 建议给统筹的句子 |
| --- | --- |
| 11 与 29 | “In a 60-participant chatbot-avatar study, sketches made with access to Midjourney V4 repeated more features of a shared example on average than sketches made without an additional inspiration tool.” 第 11 页可用短版，完整方法留第 29 页或备注。 |
| 13 | “GeoStyle used computer vision to estimate the prevalence of clothing attributes from Instagram and Flickr photos and forecast how it changed by city over time.” |
| 14 | “Image-based forecasts may miss styles from locations or communities that are sparsely represented in the data.” |
| 15，替换误差测试句 | “Before ordering, check coverage and forecast errors by intended market. Use demographic breakdowns only where lawful, reliable data support them.” |
| 15，补充原创性备注 | “Check strong similarities to identifiable sources before release. Compare distinct design directions and record why the reviewer selected the final concept.” |
| 28，补充证据行 | “Training-image reproduction risk · Carlini et al., §4.2 and Fig. 3 · targeted extraction in a tested model.” |
| 32 | “Compared with writers without access to GPT-4 ideas, writers offered these ideas earned higher ratings on some measures. Their stories were also more similar to the average content of the other stories in their group.” |

## Q&A 候选

**Did Nike use GeoStyle in A.I.R.?** The sources we reviewed document three separate activities. Celect concerns local demand and inventory. GeoStyle forecasts changes in observed clothing features. A.I.R. is Nike’s public account of concept design. We have no source connecting GeoStyle to Nike’s workflow.

**Can an accurate forecast still overlook a community?** Yes. A model can accurately predict what appears in the available photos while missing people who rarely appear in them. We would check coverage and compare forecasts with an appropriate reference for the intended market before using them to place orders.

**Does similar-looking output prove copying or infringement?** Similarity is a signal to investigate. The extraction study found near-copies under targeted testing. A release reviewer should trace the specific image and its sources, then check the relevant permissions and context.

**Do the fixation and creativity studies contradict each other?** They measure different outcomes. One counts features repeated from an example avatar. The other compares reader ratings of individual stories and similarity within each group. Individual quality and group diversity should be evaluated separately.

**What would you ask a fashion brand to do differently?** We would assign an owner to review data coverage before production and require design teams to compare genuinely different concepts before release. A flagged similarity would trigger source review. The approval record would name the person making the decision and give the reasons.

## 本人的选择与交接顺序

1. 两项事实修正可先读：第 13 页的数据来源、第 32 页的“可使用 AI 点子”的实验条件。第 11、29 页补比较基线，第 15、28 页补 T2 证据与政策边界。
2. 建议采用「生产前查预测数据，发布前查设计」作为 E 的主线。它能把 T1 与其他三篇研究放进实际业务动作。备选是「单款质量和整批多样性分开评估」作为主讲与答问重心，预测仍留在第 13–15 页。
3. 由本人选定重心并用自己的话复述后，把逐页改句和英文问答交统筹。请统筹将 E 的 T2 备注与 G 的第 28 页、E 的第 13 页与 D 的公司核查对齐。A 可从英文问答中选用适合排练的版本。
4. 报告部分记录自己读了哪些原文、发现哪处措辞问题、最终采纳哪些建议，并如实记录本轮用 Codex 辅助提取、对照和起草。本人是否已逐项复核、统筹是否已合稿，均待各自的实际记录。下载的 PDF 是报告格式样稿。

## 核查版本

组稿 SHA-256 为 `711671637ca56458f571aa67fefb4246129b057a83329c3d23c704224589fc0d`。2026-11-07 实际查看分工图和 PowerPoint 导出的第 11、13–15、24、27–29、32、35、37 页，读取对应备注，查四篇原文的方法、结果和限制及 Nike 两份官方来源。页定位采用本次所读版本。样稿只核报告用途与结构。
