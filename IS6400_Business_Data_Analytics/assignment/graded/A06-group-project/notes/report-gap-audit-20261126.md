# IS6400 最终报告前审计与第一批分工建议

截至2026-11-26 HKT。本人已确认11/25展示完成、没有老师反馈、最终报告未开始；W4/W5个人作业由总监督记录，本会话只维护A06。下面是审计与分工建议，不是报告正文，也不是成员已认领任务。

## 先给可以直接执行的判断

当前主要问题不是完全没有实验，而是报告目标/模型身份尚未统一、少量记录会在复跑时自相矛盾、现成证据未整理成报告图文。已有数据和图不能因为旧待办而重做；未执行业务试验也不能被当成漏跑算法。本轮没有拟合模型、扫参数、重建标签、付费调用或触达客户。

最先做：6号协调报告范围单；3号修元数据生成并做实验身份表；1号整理时间/字段来源图；5号从现成27行整合三期报告表，推荐派生面板并建立图表白名单；2/4号交已有修正版特征/画像/试验解释。具体名单及日期均为建议，待本人/成员确认。

## 1. 本次真实审计范围与核验结果

- 协作仓库基线：`4a61991ad2c0a1e70deaa691078a6aff5f6dfec6`，共1283个已跟踪文件；枚举了全部路径/大小/Git blob，读取并缓存了939个相关文本。仓库共有363份CSV、92个SVG、151个PNG；这是文件数，不能当作独立实验/图数。
- 8份公开发布manifest合计362个条目逐一核SHA：0缺失、0不匹配。这证明本批对应字节可取，不证明全部科学结论正确。
- 重新核算R3基础18行、群模型9行、5号补全容量12行、冻结测试27行，共66行的适用Precision/Recall、群加总和混淆计数：0算术不一致。没有重新生成分数。
- 检查6个关键运行脚本的AST与路径/拟合调用；11/25冻结评分脚本没有fit/fit_transform/partial_fit/set_params调用；R3元数据生成矛盾在源码中仍存在。未执行这些训练脚本。
- 当前课堂PPTX与Git版本SHA一致；核对第3/6/7/8/9/10/11/12/13/14/15页文本和对应表，三期9个Top10%计数、R3容量75、参数未发现新数字冲突。原15页及经理版三页不修改，也未从“展示完成”推定使用了哪个投影文件。
- 实际看Guideline p2；6张跨批次现有图的风险样本（R3模型/79、5号配对、滚动概率、人数/价值、校准、AE删块）已看，未发现这6张的轴/图例与其限定结论明显矛盾。未逐张重审全部92个SVG或全部PNG。
- 两份本机私有manifest中的14条绝对路径当前14/14存在；冻结测试私有逐客户评分表存在，可用于派生图而无需重训。本轮只核存在，不重核这些私有表全部字节/每行，也不将其公开。
- 原件只读，选定PPT/PDF/指南与两份权重记录了当前SHA；本批用独立course_integrity基线，不覆盖共享manifest。电脑/手机Remotely Save关闭要求沿用既有确认，未观察手机。
- 本轮没有重新登录Canvas核新公告，正式截止沿已存Canvas证据为12/6 23:59 HKT；Guideline p2的May1是旧模板日期。定稿前需核最新格式/附件要求。

## 2. 逐项缺口：证据、最小动作和验收

P0为先纠错/定口径；P1为报告补齐证据和表达。下列open指报告准备仍需执行相应动作，不等于相关研究没有做过。

### R01 · P0 · 展示完成与报告未开始必须进入当前入口

- 分类：必须澄清的现行记录
- 现状与证据：本人11/26在总监督确认：11/25展示完成、没有老师反馈、最终报告未开始。现assignment的presentation=todo、report=in_progress；submission说明仍写展示待完成；timeline的date-presentation=planned。
- 影响：旧排练/展示待办会继续抢占报告安排；报告in_progress可能被误读为正文已有。
- 最小修补动作：只更正本课A06当前事实；展示实际日期记11/25，不补具体钟点；报告正文改待开始。历史准备记录不删除。
- 交付图表/数据：当前assignment/timeline；本次事实回执。
- 验收办法：当前不再催排练；报告仍未提交；W4/W5 A05/A07由总监督处理，本会话未改。
- 依赖：本人新事实已给出。
- 建议岗位：6号协调；课程会话写A06；总监督收尾共享端

### R02 · P0 · 锁定报告的目标、版本和素材范围，不能沿用相互冲突的采用文案

- 分类：报告采用前必须定口径
- 现状与证据：[research/role05-mainline-20261113/README.md:L7](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/role05-mainline-20261113/README.md#L7)；[docs/team/final-research-closeout.md:L3](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/docs/team/final-research-closeout.md#L3)；现report-brief-20261123.md §3记录11/15仅确定展示A、报告范围未逐项重定。
- 影响：同容量命中、校准概率、价值排序是不同任务，混成一条冠军榜会产生假结论。
- 最小修补动作：6号提出一页范围单：要解决的经理决定、主指标、采用模型/拟合文件、比较人群、正文与附录材料、真实成员贡献；交本人/团队确认。这里不替团队选择A/B或具体模型。
- 交付图表/数据：report-scope-and-provenance.csv及建议章节清单。
- 验收办法：每个主表具训练/校准/评价日期、客户池、输入、模型指纹、容量和指标；本人/团队采用另有真实记录。
- 依赖：先看已完成材料目录；不依赖新训练。
- 建议岗位：6号主责，3/5号核版本，各岗确认本人成果

### R03 · P0 · R3重跑脚本会把已跑群模型的元数据覆盖为Not run

- 分类：可直接验证的记录生成错误
- 现状与证据：[research/team-round3-20261112/members/role03/run_round3.py:L238](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/members/role03/run_round3.py#L238) 对照 [research/team-round3-20261112/members/role03/run-metadata.json:L43](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/members/role03/run-metadata.json#L43)；[research/team-round3-20261112/members/role03/group-model-metadata.json:L16](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/members/role03/group-model-metadata.json#L16)
- 影响：正常重跑不生成已交元数据；候选比较是否用过一月的表述会自相矛盾。不是命中结果被本轮发现算错。
- 最小修补动作：3号修记录生成器和运行顺序，明确一月是开发比较、B/C CV以固定全十月H05映射为条件；先用无训练的元数据生成/比对验收，不改参数。
- 交付图表/数据：可独立生成的run-metadata、环境清单、优化诊断及日志。
- 验收办法：相同输入生成同配置；不再写群模型未跑；声明与run_group_models.py及CSV一致；后续真复跑单独授权和记录。
- 依赖：R02的版本命名；输入文件就位。
- 建议岗位：3号修，5号检查

### R04 · P0 · 5号原CI图和群内收益归因不能进入报告；已有课程修正版可直接用

- 分类：错误材料使用禁令及最小修补
- 现状与证据：[research/role05-mainline-20261113/README.md:L31](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/role05-mainline-20261113/README.md#L31)；[research/role05-mainline-20261113/README.md:L37](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/role05-mainline-20261113/README.md#L37)；[research/role05-mainline-20261113/README.md:L35](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/role05-mainline-20261113/README.md#L35)
- 影响：原公式把比例/命中数单位混用；全局2937相同不代表群席位相同，不能唯一归因为群内变准。
- 最小修补动作：报告素材白名单排除原错误图；采用已补四模型容量、配对换入换出、群席位图。5号改文案，不要求重新做已正确的配对算术。
- 交付图表/数据：素材准用/禁用表；更正后的独立验收说明。
- 验收办法：50/46净增4仍保持；明确席位重分配；无错误CI、无相同hits即相同名单的表述。
- 依赖：R02与现有role05/audit表。
- 建议岗位：5号主责，3号给版本，6号合稿

### R05 · P1 · H04、R3与概率/价值线必须分栏，不能拼成同一模型的结果

- 分类：报告必需的版本证据
- 现状与证据：[research/team-round3-20261112/audit/h04-v02-vs-round3-F0.csv:L3](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/audit/h04-v02-vs-round3-F0.csv#L3)；[research/final-validation-20261112/README.md:L58](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/final-validation-20261112/README.md#L58)；[research/frozen-temporal-test-20261125/test-plan.json:L9](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/frozen-temporal-test-20261125/test-plan.json#L9)
- 影响：H04/R3加权均命中50，却各换17人、久单79/73；校准线43采用80/20切分，不能据50对43评算法。
- 最小修补动作：从现有产物做实验身份总表，分开筛选H04、成员R3、校准/价值、11/25加载权重测试；保留每张图的原协议。
- 交付图表/数据：experiment-registry.csv，至少含run_id/model_sha/preprocess/split/seed/cohort/K/metric/source。
- 验收办法：50/46、50/48/46/50/49、43及65/64各能追到独立run；数值不跨行拼接。
- 依赖：R02；现有权重、CSV和manifest。
- 建议岗位：3号整理，5号核对，6号选入报告

### R06 · P1 · 已有覆盖与成熟性表，报告仍缺一张统一客户流和时间图

- 分类：报告必需的可读数据证据
- 现状与证据：[research/final-validation-20261112/data/README.md:L9](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/final-validation-20261112/data/README.md#L9)；[research/team-round3-20261112/members/role01/field-time-audit.csv:L1](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/members/role01/field-time-audit.csv#L1)；[research/frozen-temporal-test-20261125/test-windows.csv:L1](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/frozen-temporal-test-20261125/test-windows.csv#L1)
- 影响：读者无法从多个目录知道哪些是历史字段、哪些是未来标签，或把滚动行数当独立人数。
- 最小修补动作：复用七历史快照、三期新测试窗口、既有原表核验；整理原始表→合格订单→客户快照→训练/校准/评价的漏斗和时间线，不重造已一致的快照。
- 交付图表/数据：dataset-flow.csv、time-window.svg/PDF、字段时点字典。
- 验收办法：起止均说明含/不含；一月29368/230、四月37813/299等对表；pooled重复客户/订单和测试窗口重叠明确；总数不相加冒称独立样本。
- 依赖：R02；1号现有daily/monthly/source-tail/field-time表。
- 建议岗位：1号主责，3号核split，5号验算

### R07 · P1 · 静态导出与预计送达的历史版本不能包装为已证明无泄漏

- 分类：报告必须披露的来源边界
- 现状与证据：[research/team-round3-20261112/acceptance.json:L11](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/acceptance.json#L11)；[research/final-validation-20261112/data/README.md:L27](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/final-validation-20261112/data/README.md#L27)；[research/team-round3-20261112/members/role01/build_audit.py:L134](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/members/role01/build_audit.py#L134)
- 影响：按事件截止能拦未来送达/评价，不证明支付、状态、州或承诺日期的历史版本无回写；这是未证假设，不是本轮证实泄漏。
- 最小修补动作：写信息可得性表和限制；对采用的具体字段逐项标已核事件截断/静态假设/不入模型。若要因果解释配送作用，再讨论剔除依赖承诺日期字段的敏感性，非本轮默认训练。
- 交付图表/数据：feature-availability.csv及数据限制段落。
- 验收办法：不以列名无future或每日有订单证明完全无泄漏；标签和未来金额不进X；不无依据声称源系统漏采。
- 依赖：R06字段定义。
- 建议岗位：1号主责，2/3号配合

### R08 · P1 · 预处理、类别不平衡与模型比较已做，需放进同条件方法表

- 分类：报告必须说明的比较条件
- 现状与证据：[research/team-round3-20261112/members/role03/run_round3.py:L67](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/members/role03/run_round3.py#L67)；[research/team-round3-20261112/members/role03/january-comparison.csv:L1](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/members/role03/january-comparison.csv#L1)；[slides/classroom-20261125/QA-20261125.md:L17](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/slides/classroom-20261125/QA-20261125.md#L17)
- 影响：不能把7种方法说成7种算法家族，也不能把加权分数当自然复购概率或accuracy约99%当有效。
- 最小修补动作：复用主筛选3家族6配置+recency、R3六特征/权重配置及两新增群模型；列训练期填补/缩放/编码、class_weight、容量和AP等。
- 交付图表/数据：method-comparison.csv、参数/预处理表、类别支持数小表。
- 验收办法：固定客户/标签/K；模型配置与第15页一致；1%正例下有hits/Precision/Recall/AP，说明ROC-AUC取舍。无需为了形式补SMOTE。
- 依赖：R05。
- 建议岗位：3号模型表，1号支持数，5号核

### R09 · P1 · 群模型CV以全十月群映射为条件，不能称完整折内独立验证

- 分类：报告解释必修，重跑有条件
- 现状与证据：[research/team-round3-20261112/acceptance.json:L44](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/acceptance.json#L44)；[research/team-round3-20261112/members/role03/build_training_clusters.py:L36](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/members/role03/build_training_clusters.py#L36)；[research/team-round3-20261112/members/role03/run_group_models.py:L169](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/members/role03/run_group_models.py#L169)
- 影响：普通管道折内填补/缩放正确，不代表聚类中心也每折重学。五折是在十月客户中轮流留出一份核对；F0未加权/加权平均每折命中7.0/6.8人，不是准确率，也不是未来窗口验证。
- 最小修补动作：先改报告口径、显示真实CV8配置均值/样本SD；只有团队要主张完整端到端CV比较时，才另定每折重拟合聚类及标签映射的有限复跑。
- 交付图表/数据：CV表及条件说明；严格CV复跑列可选条件任务。
- 验收办法：五折shuffle=True、seed2026；每折留出4232位客户，从中选424人；F0未加权/加权平均命中7.0/6.8人，±为5折样本SD、不叫CI；不拿7与一月50直接比。
- 依赖：R03/R05；严格复跑需先确认用途。
- 建议岗位：3号主责，4号群映射，5号核

### R10 · P1 · 三期冻结测试已有27行数据，先整合报告表，再按需要派生同源图

- 分类：必须完整呈现；新绘图为推荐交付，不需重训
- 现状与证据：库存research/frozen-temporal-test-20261125有11文件/3CSV/1py，SVG=0、PNG=0；[research/frozen-temporal-test-20261125/metrics.csv:L1](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/frozen-temporal-test-20261125/metrics.csv#L1)；课堂PPT第14页已有完整表格；私有逐客户评分表当前存在。本轮未找到直接绑定11/25该run的三期独立图，不据目录无图断言全库没有可复用图。
- 影响：报告必须完整交代三期结果，不能只呈现四月而隐藏五月普通LR更高；这不要求每项结果都新增图，清楚的表格也可满足呈现。
- 最小修补动作：先把第14页/已存CSV整理成带run、样本数、K和指标的报告表；推荐再从CSV画三期hits及Precision/Recall和容量面板；若需PR曲线，从现存分数读，不fit。
- 交付图表/数据：必交三期报告表；推荐frozen-test-panels.svg/PDF、绘图.py、graph-data.csv及source/run标签。
- 验收办法：每月三方法同K；四月K3782时WLR/ULR/recency命中65/64/45人，五月K4003时65/67/57人，六月K3981时59/53/48人；表可验收，图须同源；区间定义清楚且不合并作独立样本。
- 依赖：R05；不依赖新模型。
- 建议岗位：3号给数据，5号表/推荐绘图及核数，6号解释

### R11 · P1 · 同名单配对比较和不确定性已有部分结果，不能错借版本或过度显著化

- 分类：已有统计证据的正确应用
- 现状与证据：[research/frozen-temporal-test-20261125/paired-comparisons.csv:L1](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/frozen-temporal-test-20261125/paired-comparisons.csv#L1)；[research/role05-mainline-20261113/audit/paired-list-recomputed.csv:L1](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/role05-mainline-20261113/audit/paired-list-recomputed.csv#L1)；[research/final-validation-20261112/README.md:L66](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/final-validation-20261112/README.md#L66)
- 影响：四月净+1没有稳定优势证据；金额/概率线的2000次条件重抽样不涵盖重新训练/模型搜索，不能迁给R3。
- 最小修补动作：逐主结论选对应的已有配对表/区间；四月共同56、独有9/8的检验已存在，不再列为未做。若报告不作显著优越主张，无需为每张图追加检验。
- 交付图表/数据：claim-uncertainty.csv；对应方法和限制。
- 验收办法：区分样本SD、Wilson比例区间、固定分数客户配对区间；说明窗口重复、多比较及训练不确定性。
- 依赖：R02/R05。
- 建议岗位：5号主责，3号核score身份

### R12 · P1 · 当前群画像与固定79诊断已齐，需用新名单而非旧46命中画像

- 分类：可直接复用的分群解释
- 现状与证据：[research/team-round3-20261112/audit/current-profile-summary.csv:L1](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/audit/current-profile-summary.csv#L1)；[research/role05-mainline-20261113/audit/fixed-long79.csv:L1](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/role05-mainline-20261113/audit/fixed-long79.csv#L1)；[slides/classroom-20261125/QA-20261125.md:L63](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/slides/classroom-20261125/QA-20261125.md#L63)
- 影响：旧79席和当前73席不能混；518席命中4并不证明等容量群内识别更准；画像差异不是原因。
- 最小修补动作：直接采用当前R3三卡、全局席位/命中与另固定79对照；说明群名来自画像，不是手设R阈值。
- 交付图表/数据：群画像表、coverage-vs-ranking图、群稳定性配置脚注。
- 验收办法：16335/12330/703；当前2190/73/674及21/2/27加总；固定79各模型2/2/1对上。
- 依赖：R05，4号既有H05及当前卡。
- 建议岗位：4号主责，5号核，2号辅助解释

### R13 · P1 · 2号新G1/G2组合与3号已测F1/F2不同，不应泛称配送/评价无效

- 分类：必须保留未测边界；补实验可选
- 现状与证据：[research/role02-v11-20261113/README.md:L12](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/role02-v11-20261113/README.md#L12)；[slides/classroom-20261125/Speaker-Guide-20261125.md:L92](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/slides/classroom-20261125/Speaker-Guide-20261125.md#L92)；课堂第13页左右分栏。
- 影响：已测F1/F2的48/46不能当作新组合成绩；delivery_days_log再次log会偷换定义。
- 最小修补动作：报告先写清已测/未测字段规格；若确认新组合进入报告验证范围，最小只比F0/G1/G2，冻结字段/参数/人群/K，不扫网格；已见测试不可重标盲测。
- 交付图表/数据：tested-vs-proposed.csv；可选F0/G1/G2匹配实验方案。
- 验收办法：2号v1.1的20行CI修复保持关闭；不因未模型化就丢弃描述性证据，也不把相关性称预测增益。
- 依赖：R02采用范围与2/3号接口确认，实验须另定。
- 建议岗位：2号字段、3号可选执行、5号验收

### R14 · P1 · 已有脚本和本机私有输入，不等于报告读者一条命令可复跑

- 分类：报告复现交付确需补
- 现状与证据：[research/frozen-temporal-test-20261125/score_frozen.py:L13](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/frozen-temporal-test-20261125/score_frozen.py#L13)；[research/team-round3-20261112/members/role03/README.md:L59](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/members/role03/README.md#L59)；14项私有manifest指向的本机产物本次存在14/14。
- 影响：脚本依赖本机E盘目录、H02/时点字段/模型私有文件，公开目录故意不含逐客户输入；缺面向合稿的统一运行入口/环境证据。
- 最小修补动作：先补config+inputs manifest+环境锁定+报告数据/图只读replay入口；提供聚合绘图复跑和本机授权路径说明。干净环境执行验证另排，不在本轮声称已跑。
- 交付图表/数据：RUN-REPORT.md、config示例、environment、verify-only日志、run-to-figure清单。
- 验收办法：在隔离输出目录只加载保存模型/数据可再生主表/图；缺输入明确报错；不改原件/静默fit；私有逐客户表不公开。
- 依赖：R05/R03与1号原始数据清单。
- 建议岗位：3号运行包，1号输入，5号隔离验收

### R15 · P1 · 概率/价值/AE/时间与消融已完成，缺的是按报告问题选择兼容证据

- 分类：不应重做的深化材料整合
- 现状与证据：[research/final-validation-20261112/README.md:L13](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/final-validation-20261112/README.md#L13)；[research/common-comparison-20261112/README.md:L1](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/common-comparison-20261112/README.md#L1)；[research/ae-ablation-20261112/README.md:L1](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/ae-ablation-20261112/README.md#L1)；[research/final-validation-20261112/probability/README.md:L35](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/final-validation-20261112/probability/README.md#L35)
- 影响：“缺很多实验”不能直接变成补跑AE/多期/校准；同协议图已有，但不允许跨协议抢最好数值或把优化success当严格收敛。
- 最小修补动作：6号按R02选入概率/价值或方法扩展时，复用已有同口径矩阵、校准、预算、删块、滚动图及实际终止诊断；整理排除理由。
- 交付图表/数据：report-evidence-map.csv，正文8–10个图位建议；其余保留附录导航。
- 验收办法：训练/校准80/20与全十月模型分开；概率、金额、命中目标分开；负结果和跨期偏移一起保留。
- 依赖：R02；无需新拟合。
- 建议岗位：6号取舍，3号技术、5号核，保留本地研究贡献来源

### R16 · P1 · 内容试验规划已算，尚无触达和营销效果数据，不能列为漏跑的模型实验

- 分类：业务建议与可执行性写清
- 现状与证据：[research/team-round3-20261112/README.md:L88](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/README.md#L88)；课堂第8页；[slides/classroom-20261125/mobile/manager/Manager-Script.md:L31](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/slides/classroom-20261125/mobile/manager/Manager-Script.md#L31)
- 影响：12,330历史池不是同意且可触达人群；相对+50%需要21,308样本，现有数据不识别利润或联系增量。
- 最小修补动作：复用1:1主题/通用指南、90天全随机客户分母、alpha5%/power80%及三种效应规划；列渠道/同意/成本/样本可行性待业务输入。不真实发消息或开展试验。
- 交付图表/数据：业务试验设计表及可行性/成本数据需求清单。
- 验收办法：两组都联系；+50%不是+50个百分点；明确未执行；没有随机结果就不写营销收益已证明。
- 依赖：4号现有样本量表；业务输入由真人提供。
- 建议岗位：4号方案，6号经理建议，5号核

### R17 · P1 · 报告正文、章节归属和图文引用尚未制作，不能由PPT/材料数量代替

- 分类：正式报告实际缺件
- 现状与证据：本人11/26确认报告未开始；原Guideline.pdf p2要求20–25页、11号、双倍行距、图表在正文、引用计页；现report-brief-20261123.md已有23页建议但无正式正文。
- 影响：缺封面/一页摘要/业务问题/数据/分析结果/结论/引用的完整交付；通用AI模板或纯指标不能满足经理读者。
- 最小修补动作：按现有23页建议提出分工；先交结果包和段落要点，确认范围后再写报告正文；数据/方法/结论来源逐段绑定。
- 交付图表/数据：章节-负责人-图表-来源-验收表；正式正文留下一阶段。
- 验收办法：封面成员和贡献准确，引用含数据与方法，图表靠近对应结论；定稿核Canvas允许附件/公告和12/6 23:59 HKT，不沿用PDF旧May1。
- 依赖：R02及R06–R16证据整理。
- 建议岗位：六岗分工，6号合稿；正式提交由本人确认代表

### R18 · P1 · 成员回件、课程复算与本地深化成果分开署实

- 分类：必须区分的真实贡献与验收
- 现状与证据：[research/team-round3-20261112/acceptance.json:L4](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/team-round3-20261112/acceptance.json#L4)；[research/role05-mainline-20261113/README.md:L3](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/role05-mainline-20261113/README.md#L3)；[research/role02-v11-20261113/README.md:L14](https://github.com/CercaTrovato/olist-repurchase-analysis/blob/4a61991ad2c0a1e70deaa691078a6aff5f6dfec6/research/role02-v11-20261113/README.md#L14)
- 影响：旧acceptance的5号未收/2号待修是快照，后续已补；不能抹去成员贡献，也不能把代理研究写成组员亲跑。
- 最小修补动作：做当前交件/修订矩阵，继承后续role05回件和role02-v1.1验收；未闭合的3/5记录性问题据实保留；六岗建议待认领。
- 交付图表/数据：contribution-and-acceptance.csv；当前报告采用记录。
- 验收办法：每一段有来源/作者与核验边界；正式认领需真人记录；不重催已交的2号CI或5号意见。
- 依赖：R02与当前三个批次记录。
- 建议岗位：6号协调，各岗核自己贡献，5号验收

## 3. 已完成、不要再派成欠账的项目

|项目|当前证据与可用边界|处理|
|---|---|---|
|R3数据时点、键/标签核验|1号88341行、十月/一月14字段比较已在交付核验；本轮manifest完整|复用；历史版本/入库假设继续披露|
|主模型/类别加权/容量比较|初筛7方法；R3六特征权重配置与两分群扩展；18+9行当前结果齐|不因为报告未写就再跑一轮|
|2号v1.1的20行CI修复|96校验项已核，d标准误/区间与课程修正版吻合，点值不变|这项已关闭；不再催同一补件|
|5号验收意见和课程修正版|已收到，配对表/四模型容量/席位图存在；原错误图不采用|修记录性表述，不说5号从未交|
|全量概率/校准/价值排序|30模型位置、25新拟合+5复用，6条件金额、18组合容量等已有；同协议结果可复用|不是漏跑研究；采用范围待确认|
|复杂模型、预算、删块、历史时间检查|common-comparison、AE-ablation、validation等均有源表/代码/图|按问题挑兼容证据，不把GAT/完整MVSIB等明确未实现者伪称已做|
|四月/五月/六月冻结测试|3方法×3期×3容量=27行；指标、Wilson参考区间、配对比较已存；本轮算术核对通过|不再说没有测试结果；不能改参后仍称原测试未参与选择|
|内容随机试验的规划|1:1、90天、同渠道/格式/时间和样本量已算|未实施是数据/业务阶段边界，不伪造结果|

## 4. 只有满足用途才值得做的加分实验

1. 2号完整G1/G2的同条件LR对照：仅在确认它属于报告问题、字段规格和评价方案后运行；不是用四月/五月/六月重新挑赢家。
2. 完整折内重拟合聚类的CV：只有要作严格端到端泛化主张才需要；当前可保留条件CV并准确写限定。
3. 剔除预计承诺/静态时点假设字段的敏感性：若报告把服务信息作为关键结论，先确定目的再定最小对照。
4. 更长未来、真实触达、成本/利润/CLV：现有数据不能凭算法补出；要新业务数据与真人授权，不列成本周必跑模型。

不建议在报告前临时开启大规模SMOTE、GAT、更多AE结构、超参网格或新日期搜索；已有弱/负结果本身是报告证据。新增试验必须先说明要检验的哪条结论及失败时如何写。

## 5. 第一批可直接评审的六岗分工建议

以下按已有能力和贡献分配，不代表已发给成员、已认领或承诺交期。建议11/26先认领、11/27晚交最小证据包；原11/28段落、12/2合稿、12/4定稿、12/5建议交件均仍只是建议，正式截止12/6 23:59 HKT。

|岗位|第一交件，不先写大段正文|主要依赖|验收/下一交接|
|---|---|---|---|
|1号 数据与时点|R06/R07：客户流、训练/标签时间图、字段可得性及输入清单，复用现有CSV|6号范围单|5号核总数/边界；交2/3号方法表|
|2号 EDA与特征|R13：已测F1/F2 vs新G1/G2规格、v1.1修正效应图及白话解释；列未测而非许诺提升|1号字段；不需新训练|3号确认可接入规格，5号核CI来源|
|3号 模型与复现|R03/R05/R08/R09/R14：实验身份表、元数据修复、参数/预处理/环境及只读复跑入口|1号输入，6号采用范围|5号核同条件和保存权重；不改模型重选|
|4号 分群与业务|R12/R16：当前R3群卡、73/79/518对照及内容试验可行性/数据需求|3号run身份，1/2号数据解释|5号核群总数/样本量；交6号经理建议|
|5号 评估与图表核验|R04/R10/R11：图表准用表、三期报告表（推荐同源派生图）、逐结论数值和不确定性检查|1–4号表/图；测试27行已可直接用|给6号“可用/禁用/待证”的明确验收，不用常量PASS|
|6号 本人协调与合稿|R02/R15/R17/R18：一页范围/证据取舍、章节-图表-来源-成员矩阵、收件清单及最终经理故事|先汇总现有包，不要求别人重跑证明材料存在|本人/团队确认范围与认领后开正文；先不替成员承诺|

建议先留8–10个正文图位：数据/时间1–2、主模型/容量2、三期测试1–2、群覆盖/排序1、业务试验1；若采用概率/价值扩展，再用兼容图替换部分图位。不是强制塞入所有92图。

## 6. 本次没有做与阶段边界

没有新训练/调参、没有重建全部源数据、没有新的未来盲测、没有正式报告正文或正式交作业。没有改W4/W5 A05/A07、他课/共享management/根README、线上发布配置或旧root_thread_id校验器；本批CityU根Git和管理/线上收尾交总监督。本人新事实不等于全员接受某报告路线或已分配到具体段落。

课程元数据写回、独立抽检、GitHub远端和总监督待收尾状态分别见 supervision-update-20261126.md；当前审计通过不预填报告可提交。
