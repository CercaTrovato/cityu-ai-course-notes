# 独立定向抽检 · 阶段 2

日期：2026-11-26。审查者：`/root/repair18_independent_review`，未参与候选撰写。阶段 1 记录原样保留于 `review-stage-1.md`。本次是同一次候选优先审查的定向回源与修复复核，不是新一轮全篇审查。

## 结论和边界

**所抽 R13、R11 与补抽 R03 未发现尚未解决的实质阻塞；阶段 1 的 F1/F2 已通过定向复核。可接受为报告写作前的证据准备样本，不可据此称正式报告完成、18 项全部独立认证或任何人已学会。**

封包绑定仍待主代理收尾：本次检查时 core manifest 与 ZIP 仍为上次冻结版本；`RUN-REPORT.md` 已变，新 `source/build_replay_inputs.py` 未纳入该 manifest。主代理已经明确说明这是审查中的补全，未将这种变化伪装成同一冻结字节。最终 manifest/ZIP 更新后，只须核内容指纹绑定，无须因此重跑模型或重审无关正文。

R03 修复的是旧元数据与保存结果不符以及调用模式混淆；R13 是已见开发月上的固定新增对照；R11 是保存名单上的描述性配对比较。三者没有被本报告提升为新的盲测、因果营销收益或完整报告交付。

## 阅读条件与版本

阶段 1 从指定候选入口自行选 R13、R11/R10，视觉看图 03/04/07/10，没有提前读源码或作者自检。阶段 2 由主代理确认后才读取根 `_meta/笔记制作与融合验收流程.md` §3、针对性源码、原字段规格、数据和作者回执。平台上下文此前已经包含全局 AGENTS 规则，因此不冒称完全无上下文盲审。

- 阶段 1 84 文件候选总指纹：`7725fda2661391622ca0c11faff74ae88409ba9be0f07afb052f1ad219499f0c`。
- 阶段 2 87 文件现场总指纹：`06ae37d833ca3448f8995003749e48c50d46bd04f6b1e6d768048bd3e3d293ac`，逐文件见 `review-stage-2-fingerprint.tsv`。算法与阶段 1 相同；包含现场 `source/__pycache__/run_fixed_features.cpython-312.pyc`，并不要求其进入交付包。
- 检查时 core manifest SHA：`bf38c33516c967d62db918e2f91e0e826101a3bb4d032c38a23bf9cfe564e6d6`；旧 ZIP SHA：`2a0a546e1c4ca946aec7a5311543c07d115c71351193a9c70c72140b700385b2`。它们与主代理提供值一致，但不是包含最后适配器的最终封包。
- 独立检查脚本：`reviewer_stage2_check.py`；实际聚合结果与样本 SHA：`reviewer-stage2-check-result.json`，SHA `43de413dc38b93c5811e061423f2ebab45141c0b297decf4cd080f2bb5b4f746`。
- 原始 Git 比较基线 HEAD：`2d2d37cbab726a112f1bd3c2e46f6a26828cbe9e`。

## 实际抽样动作与发现

### R13：处理状态 → 固定实验 → 表 → 图

路径：closure-register 的 `tested_minimal_comparison` → scope-decision 的“新运行、已见开发月” → 原 2 号 v1.1 字段规格 → 新 `run_fixed_features.py` → plan/results/transform-fit → 图 03。

独立读到的机制：脚本先写三配置计划，再从版本 CSV 只解析十月／一月；基线七数值列走 log1p、填补、标准化；新增配送 log 列只做中位数填补和标准化，没有二次 log；星级也不做 log。训练只使用十月，一月 predict_proba 后按分数降序、客户 ID 升序处理并列；三个模型逐一独立 fit。源规格的配送未完成数、配送 log、评分均值和评分覆盖率公式与实现一致，缺失指示没有被省略。

独立核 9 行 5%/10%/20% 结果的 K=ceil(N×比例)、precision、recall；Top10% 为 50/49/48，结果表算术与图一致。plan/code/metrics 实际 SHA 与运行回执对应，原规格 SHA 与计划对应；拟合参数表只标十月学习值。`feature-experiment-verification.json` 的训练人数 21,160/211 与开发 29,368/230、三模型权重 SHA、0 个新增测试评分等是作者执行回执，本审查没有冒称独立再次拟合或重放这三个模型。

F1 复核：新 PNG 的图 03 已将 `F0 replay` 改为 `F0 new fit`，标题为 `Three new fixed fits (26 Nov)`，脚注写明旧 R3 与三次新拟合是不同实物。可从图单独分清“旧保存 R3”与“新固定开发对照”。F1 关闭。

可复述判断：在已见一月、同一 2,937 名额下，新字段没有提高主命中指标；G2 的 AUC 更高不能替代 Top10% 结果。如果容量改成 5%，G1/G2 命中 34/36 会高于 F0 的 31，所以结论必须限定主容量，不能写“配送/评价信息在任何容量下都无用”。候选保留各容量表，主结论有边界。

### R11：从保存客户分数独立重建配对，而非只检查作者图

working repo 因稀疏检出不存在 `research/frozen-temporal-test-20261125/`；先有一次真实“路径不存在”读取失败，随后主代理提供 source-cache 中的同源历史代码。已实际读 `score_frozen.py` 中独有真实阳性计算及 `binomtest(gain,gain+loss,.5)` 的来源逻辑。

获得明确只读授权后，独立读取私有 `customer-predictions.csv` 的 117,642 行保存分数与选择标记。只在内存按每月的 score↓、ID↑重排，没有重评分、拟合、复制逐客文件或输出客户 ID。九份名单（三个月×三方法）的 Top10% 选择与原选择标记相同，人数、标签正例、K、命中与候选表相同；六组配对的共有、加权独有和对照独有均相同。

| 月份 | K | 共有真实复购者 | 加权独有 | 普通独有 | 加权／普通总命中 | 独立精确 p |
|---|---:|---:|---:|---:|---:|---:|
| 四月 | 3,782 | 56 | 9 | 8 | 65 / 64 | 1.000000 |
| 五月 | 4,003 | 58 | 7 | 9 | 65 / 67 | 0.803619 |
| 六月 | 3,981 | 48 | 11 | 5 | 59 / 53 | 0.210114 |

另三组加权对 recency 的独有计数与 p 值也用独立 Python `math.comb` 二项分布和式复算相符，详见独立结果 JSON；没有调用作者检验函数。上述检验仍以保存模型、已选名单和有方向对称的独有正例假设为条件，不包含重新训练/择模/未来漂移，也不是因果试验。

F2 复核：实际观看的新图 07 已标每月共有数、独有数、加权／普通总命中，中文 `cv-and-uncertainty.md` 直接用 56+9=65、56+8=64 搭桥，并解释 p 不是模型相同或营销盈利的概率。能从总数到独有差异连续读懂，五月净 -2 的不利结果未隐藏。F2 关闭。

可复述判断：四月净多 1 不意味着稳定更强，p=1 不意味着两模型确定相同；即使某个次要 recency 比较 p 小于 0.05，也不能当营销产生新增收益，候选已经保留“次要描述、未校正多重比较、月份相关”边界。

### R03：不同类型的补抽——元数据模式与计算保护

完整读三个当前源码 `metadata_helpers.py`、`run_round3.py`、`run_group_models.py`，并对两驱动的 `git show HEAD:` 原代码做 AST 比较：11 个数据/建模/排序/评价函数不变；两 main 中进入旧元数据段之前的 18／15 条语句不变。原 diff 的变化限于生成元数据及入口分流，未把模型修补混进本次元数据改动。

独立实际执行两驱动各两次 `--metadata-only`，输出仅在本审查 `reviewer-metadata-a/` 和 `reviewer-metadata-b/`。对 `LogisticRegression.fit` 加入禁止调用拦截器，4 次执行没有触发。两次各文件字节相同；保存表指纹真实对应现有 CSV；group 状态为已有结果可用，不再错误写从未运行。输出明示 `metadata_only`、本次没有 fit/predict，环境是再生环境，原训练环境没有被倒填。

另独立构造 base/group 的 metadata_only 与 trained_base_pipeline/trained_group_pipeline 共四种 context：训练路径的元数据明确写驱动此前已完成声明的训练/评分，没有沿用“整个驱动未训练”说法；`new_fits_in_this_regeneration=0` 的字段指序列化动作，配合 execution_scope 不再歧义。只构造 context，没有运行训练驱动。

第一次独立检查在所有上述实质检查后，因最后的 manifest/RUN-REPORT 不匹配断言停止；因此不是一次全绿。已保留现场，第二次只复用已生成的 metadata 文件、记录封包待项并补私有保存分数配对，未再次执行模型训练或重复四次 metadata 命令。

### R14 最后补全：只做限定静态阅读

主代理在审查中新增 `source/build_replay_inputs.py` 和 RUN-REPORT 的调用说明。实际读适配器：复用有 main guard 的字段脚本定义，合并一月已有输入、重算六个派生字段，输出到配置中的 private_output；已有文件内容不同就拒绝覆盖，生成时先 partial 后替换。没有 fit 或 predict 调用。未执行该适配器，不把作者所述“字节一致”作为独立复算结论；此处只确认文档补全与无拟合路径未引入明显误导，不扩大为全 R14 复审。

## 实物绑定与剩余建议

核心样本最终 SHA 全表已写独立 JSON，这里列直接承载 F1/F2 修复的实物：

| 文件 | SHA256 |
|---|---|
| figures/03-feature-comparisons.svg | fd95b0a51f33f29bb9805d10aabd5d25baf586fcbca3a3e530f0800b34fcf47f |
| figures/03-feature-comparisons.pdf | 1fa511470a5429bbc964c3197e6902bfa3ad21bdd4b0234827bc0ab591ef4872 |
| figures/07-paired-evidence.svg | 9ca9f8f36e506ac75c17f481b3dd306ab6c9f7a966fa6fb6431487b0de9fa122 |
| figures/07-paired-evidence.pdf | d0b8c0f51ed1960b9c89cc67d4f4afd2ca2cef9ffca1bb0c877f039d247b8175 |
| cv-and-uncertainty.md | 2f105f4235faaf012270a1ff9eae68fb7117d7f23158fb7ab617701fcdef4f56 |
| source/build_replay_inputs.py | b0cca465f3a7da1847090d255d93cc0e903ec9a9940ca06265b09301d7bf884c |
| RUN-REPORT.md | 620007d53454b7ea3d807df10c32421a58d38e13ac8381461974d7c42a051d89 |

视觉载体为内部 PNG 图 03/07，SHA 见独立 JSON；没有实际视觉查看 PDF 正式导出。作者的 `replay-reviewfix/verification.json` 声称最终 10 图 SVG/PDF 可同源重画，现已读作作者证据；不据此替代独立视觉记录。

阶段 1 的 O1（缩略语／U-W／p×F×M 释义）保留为后续写报告时的非阻塞建议。本包用途是写作准备，尚未成文；不要求把全部写作速记扩成教学课本。正式正文首次出现这些指标和符号时应给对象、分母和含义。

## 未抽范围

未对其余 R 项作完整独立认证；未全读业务试验/章节/贡献内容；未核原始数据库的漏采、状态回写、时间戳完整性；未重新拟合或独立回放新增三模型；未重新评分冻结模型；未证明旧训练环境、严格嵌套聚类 CV 或任一盲测；未将 10 图全部重新视觉审查；未核真实客户触达/成本/利润；未核 GitHub、CityU 正文、本地／线上看板或最终提交状态。

下一步仅由主代理完成最终封包指纹与实际写回绑定；本审查不改候选、不作课程写回、不提交或推送。

## 最终封包机械追加 · 原待项已关闭

本节记录主代理完成封包后的最终状态，取代前文“封包绑定待收尾”的时点状态；不扩展上述实质抽样结论，也没有重新训练或重审正文。

独立执行 `reviewer_final_package_check.py`，结果保存在 `reviewer-final-package-check.json`：

- 最终 core manifest SHA256：`fe9078e2f616ff5f1e8d828103df6731230019ab50b5b43b42b007880820d16b`。
- 最终 core ZIP SHA256：`5c138facb23b8396bb9f340e31040d29c250a5fab4bf3e94447ea936940f0933`。
- manifest 的 **84 个文件**逐一核实际 SHA，全部相符；ZIP 的 **85 个成员**恰好为上述 84 文件加 `package-manifest.json`，无重复成员。逐成员 SHA 与清单/manifest 相符，完整 CRC 校验无误。
- RUN-REPORT 和 `source/build_replay_inputs.py` 均已纳入最终绑定。适配器从前次已读字节只新增 `sys` 导入与 `sys.dont_write_bytecode=True`；去掉这两处缓存控制后，SHA 恢复为前次已读的 `b0cca465f3a7da1847090d255d93cc0e903ec9a9940ca06265b09301d7bf884c`。最终适配器 SHA 为 `317d919329215593dc33d8afd865a48854c671b6c74b86557ba721784395a2b4`，没有额外行为改动。
- 最终包没有 `__pycache__`/`.pyc` 或私有模型扩展文件；没有已知逐客预测、分数、回放输入或候选逐客表文件名。37 份 CSV 的实际表头均不含 `customer_unique_id`、`customer_id`、`order_id` 逐行键，结合成员白名单，未发现客户行表混入。本检查不等于对任意文本进行身份隐私认证。
- README 与 closure-register SHA 分别仍为 `35ef30308ef61be7255fa8ef114d85dd4cb591e27e968bda7423ba556a188fcb`、`2294ff77ced7b34e58d13c4fdcff3dd663d583409cd21110b75f1e2fc9cc3359`，未变。

**封包绑定待项已关闭。** 当前可接受结论仍只覆盖 R13/R11/R03 抽样、R14 适配器的限定静态阅读和本节机械封包；不升级为全 18 项独立认证。审查报告作为独立附属证据保存，不要求进入被签的 core ZIP，不将报告自身纳入其绑定对象。

## R07 来源标题定向修复与更新封包追加

主代理在发布前自行发现：原 `research/round3/data/features/field-dictionary.csv` 是 10 项服务字段定义，不能称为“完整 141 字段字典”。本次追加只复核这一已修正文案／来源问题和新封包，不重审其他项、不运行模型。

独立通过 `git show HEAD:research/final-validation-20261112/data/data-manifest.json` 读取原冻结记录，原件 SHA 为 `eff3c84937bd123ae5ec89a8e1ff7d7ba0bdc1014751e80696d208fe4f1df937`。逐行对比当前 `data/extension-141-field-dictionary.csv`：141 个名字唯一，顺序与原 raw_fields 完全相同；8 个 categorical/string、133 个 numeric 的类型与原 categorical_fields 完全一致，序号和 base8_member 也逐项一致。类型在这里指冻结建模输入角色，不是新证明的物理数据类型。

原 10 项服务定义另存 `data/service-field-definitions.csv`，与 `git show HEAD:research/round3/data/features/field-dictionary.csv` **逐字节相同**，SHA 为 `89e2425c7afcf2e4e7e4dfd831127965b2453c21f51fc81b09cd0e3a5307c932`。当前 141 清单中有 6 项能直接对应这些已提供定义，它们的 definition 和 availability_assumption 与原表逐项相同；余下 135 项明确写只列纳入／类型、公式仍查原来源，没有据字段名推造公式。

已实际读修订 `methods-and-data.md` 的链接和末段：名称为“冻结 141 输入列清单及类型”，并明确不是由 10 项表推定的完整公式字典。原文件名仍保留 field-dictionary 以兼容入口，但当前文案和逐行 definition_scope 没有扩大证据。因此本次定向 R07 标题／来源缺陷已关闭；不表示本审查逐一核实了 141 项特征构造、历史可得性或全部公式。

独立机械检查脚本为 `reviewer_r07_package_check.py`，结果保存在 `reviewer-r07-package-check.json`。新 manifest 的 **85 个文件**实际 SHA 均相符；ZIP 的 **86 个成员**恰好为它们加 manifest，无重复、逐成员 SHA 相符、完整 CRC 正常；38 份 CSV 表头没有逐客 ID 键，未发现 pyc、模型文件或已知逐客预测／分数／回放行表。README/closure 的 SHA 与此前记录不变。

本次最终封包绑定更新为：

- core manifest SHA256：`84fb12f468abc0ddc0a97ef33804a05ec2c710918ba44ecd2ea5394e4500279e`。
- core ZIP SHA256：`153e3d3243a4bf755f87e99ea1f57acee6b914987d622cc00b9fb6adce576eaa`。
- `methods-and-data.md` SHA256：`dddb5a3b79f15f6bab672f50006588823694862aeead7f204de51fcb6bf17133`。
- `data/extension-141-field-dictionary.csv` SHA256：`572fe97ad625cc3e2944825ea1cda837199dc316460f731a67b985d0318093ad`。

上一节 84 文件封包为本次来源修复前的真实历史记录，继续保留；以上 85 文件封包是当前绑定。实质结论新增的范围仅为 R07 这处来源／措辞定向修复，其余未抽范围不变。
