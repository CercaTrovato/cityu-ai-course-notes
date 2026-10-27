# IS6400 M06 最终实质核对与交接

本报告由 /root/resume_is6400_m06_author_61 汇总真实独审、来源、计算和显示证据，不冒充独立报告。root 确认前任真实作者为 thread:01a1787d-ea2e-7092-b7b4-68d964200cd5；本轮替代作者亦列入 author_ids。独立教学审者 /root/review_is6400_m06_resume_full_61 未参与撰写。/root/visual_is6400_m06_authorized_61 只负责实际显示，不充当教学审者。

## 最终字节与审查范围

正式目标为 IS6400_Business_Data_Analytics/notes/M06-分类-决策树集成SVM与不平衡学习.md。真实原稿 baseline.md.snapshot rawSHA256 为 df7bd2f00896a343542bfcd473a880c19aa729557f201a9d8595da6c89d95a67；当前正式文件仍同字节。

最终 candidate-display-v4.md rawSHA256 为 3a48a68842b47bd780e64c5b5c811b005a38263453e95d4410ed903c8df12928，165041 字节/2501 行。实际受审教学 v3 rawSHA256 为 568b4c466d255798c5730847b1f124c828bd4a641e7fc3a8fd42d27c628bdd4c，165040 字节/2500 行。

完整两阶段独审针对 v2 全篇，随后由同一审者定向关闭 v3 的 B1–B5 及直接依赖；未变全文承接真实原审。v3→v4 只在 §2.8 编号 3 之前补一个空行；display-maintenance-v4.json、display-v3-v4.diff 及本次重新比对均证明非空白序列和 12 个 Mermaid 源码完全相同。显示代理仅对该列表窗重新实际观看关闭 V1。这是非教学显示维护，不能称独审者重新读过 v4 全文。

独审原报告 SHA 为 6d9ec80420c6f6e22fcba03a5890f6ec68be2077023aa0810d393999e415675f。其末尾明确文本语义 accepted，同时保留当时 visual hold；现由后续获得用户明确授权的实际显示报告关闭该 hold，两份报告按真实时间与职责求并集，不追改原报告。

## 来源、原题与重要计算

独审完整报告及 stage-1、stage1-calculations、第二阶段/targeted-v3-results 记录完整 §0–9、§2.1–2.16、全部子节、表、公式、12 图源、折叠答案及自测的顺读、复述和复做。第二阶段实际读 92 页 PDF 全文与必要单页、A 265/B 619 段全文、相关 notebook 23 cells/保存输出、HTML 与 CSV；未将历史 PASS 替代本轮来源核验。

11 组讲义显式任务加 A 四阶段小测，共 12 块题面，完整原英文、必要情境、中文逐问与英文参考保留；Q59/Q68 原题必要图已加入，原点位/线条/文字保持，不发明精确坐标。原题 PNG 不替代可编辑机制图。历史 13 组/18 作答核验单元还含 p.28 理论与 p.85 成本演示，不将计数口径混同、不为凑题数编英文原问。p.85 现标成本演示参考比较。

五项真实阻塞在 v3 由同审定向关闭：

1. 第 10 轮样本改为四个 0.1、两个 0.3、两个 0.8、两个 0.9；算术文件新存 bagging-training-check-v3.json，不覆盖旧错输入回执。真实中点 0.2/0.55/0.85，两侧纯/熵 0。给定常数 +1、原投票/票和不变；“给定 0.05 达到相同熵”不冒充合法非空切分。
2. 校准就地说明“同报 20% 的一组预测与实际正类频率约 20%/50% 比较”，说明有限样本波动及期望成本可能失真；§2.12/2.14 回指，自测不再只背名词。没有假称实际模型已校准。
3. 固定 N 减少 K 时，留出折变大、基模型训练部分变小；100 条 5 折→2 折的 20→50 留出/80→50 训练方向正确，K 至少 2。v4 空行只修列表 2→3 显示，不改教学。
4. SAMME.R 两处明确限于 2026-10-14 scikit-learn 1.5.1 独立复算默认，原 Notebook 不记 sklearn 版本/algorithm，不能认定原授课算法。
5. Q59/Q68 原页图保真、角色与读法补齐；源图内容/语义由同审实看关闭，嵌入实际显示由后续显示代理关闭。

N1 描述长度只补最短含义；N2 成本演示不造原问；ADASYN 原数据未给随机/邻域/预算，不重建精确合成数量。独审同时核 12 行英文参考、§7 整节及 12 图与 v2 的不变关系和摘要/目标/速查依赖，不因哈希换版重开未变全文。

final-source-and-baseline-check.json 现场再次核 7 项 source-manifest、5 项历史输入、17 项 evidence-inheritance 所列依赖的原件及副本 SHA。独审曾另核含 README 的完整 18 文件清单，计数口径保留，不用 17 这个数代替实际文件哈希。

重要树 Gini/熵、四阶段准确率、回归 SSE、25 模型尾概率、原票、AdaBoost 状态、Stacking 明式、硬/软间隔、二次映射、p.83 指标、p.85 成本/阈值、FOIL/剪枝和 SMOTE 数值分别有独审实际复做、作者算术或同输入/脚本/结果的历史承接证据。未重训、未执行原 notebook、未重抽样、未运行优化器、未新核音；历史 SLSQP success 不当成最优性证明，旧 calc-extra additional_checks 生成限制保留。

## 当前机器模式与全部软项

正式文件名 M06，检查为实际 M 模式，不因 scratch 名称猜成 T，不加 --tutorial。v3 预检 L/C.hard/R.hard 为 0/0/0，C.warn 3、R.warn 210；v4 一空行映射保存在 warnings-final-m-mode.json。最终同字节 full gate 的 current 原始 JSON/分组/退出码由 final-gate-result.json 和 final-quality.json 记录，不能把下述判断替代实际运行。

三处 C.warn 是父单元/表达式识别疑点：§2.4 紧随 §2.4.1 有均值 6/SSE 40、叶均值 3/9/SSE 4；§2.5 给 25/.35/13 尾和、三模型组合数与独立条件，实际尾概率 0.0604449；§2.16 同节直接代入 SMOTE (2,2)+0.25(2,1)=(2.5,2.25)。均为同机制真实数字路径，不拿不相关 API 输出豁免。

R.warn 全部类别与实际位置见 warnings-final-m-mode.json；author-review-v2.md 和独审报告的机器疑点段已实核全部组：表头/单位和原题图表计数、并列短句、同机制成对公式、嵌套完整小例、英文原题与来源时间、算法对象/长段分步、名单背景/术语复用、文字误解而非图标。校准、K 方向和版本等真实缺陷已修，未被同类套话豁免。v4 只移动空行后的行号，实际模式不变；历史 G/E FAIL 保留，不为字数/固定标签凑 PASS。

## 实际显示与证据元数据

authorized-visual-20261027/visual-review.md rawSHA 为 1af43a2cd211b0763743145dff9aabcf8bff3bcb25835a4ae1c0f841a44e9c30，visual-review.json rawSHA 为 9b6af6216b99963e4c971736444ab7b8d63dcdfbeca1b6d79adaed2d7e31c67e。用户明确允许从内置浏览器恢复已确认本机 URL 的只读显示，代理在 IAB 读取同源 8866；本次作者只读文件，没有 UI 操作。

实际显示闭合并集：12 张 Mermaid 的正常尺寸上/中/下/回路窗口、Q59/Q68 590×443 原题图和中英邻接、§2.6 三表与熵代入、K/校准/成本输入/IHT/SAMME.R 受影响段。v3 唯一 V1 列表空行缺陷由 root 制 v4 后，同显示代理只重看 v4 对应窗关闭。56 张截图逐文件哈希再核，source-assets/http-byte-check 绑定实际 HTML/候选/依赖。原 Windows 不可靠 URL 的安全停止及后续明确授权恢复分开保留，不绕过或追改旧失败；原生 Obsidian 未看。

原 screenshots.json 的 width/height 按错误头偏移解码 JPEG，被写成 65536/4292542531。此处已用现有 PIL 对原字节解码，56 图格式均为 JPEG，真实尺寸为 1280×720 或 1265×712，完整对应见 screenshot-dimensions-verified.json。原清单与原显示报告/哈希保持不变；补充只是元数据纠正，不冒称新截图/新观看，不用 DOM/尺寸代替实际看图。

## 正式门槛与 root 剩余执行

当前适用教学、来源、警告与必要实际显示无剩余实质阻塞，可作一次正式 full gate。review.json 将最终 v4 candidate_sha 绑定原独审报告，同时用 reviewed_teaching_sha256 明示实际 v3 教学字节、引用空行维护映射及 v4 实看回执。程序仅验证记录/哈希，不认证身份或语义；没有伪造新独审者或冒称全文重新阅读。

publication-operations-final.json 为 cityu-exact-operations-v1：当前 beforeSHA/原始快照、唯一 replace_exact、模拟 proposed/hash，只追加本 M06 精确增量，不覆盖 root 已写其他 62 篇的共享工作；漂移须重新合并本增量。两原题图 create_if_absent+SHA 先落地并回读，同名异 SHA 即停，不覆盖，再对主正文 CAS/atomic_write/精确 rawSHA 回读。T07/数据卡/行政/作业无相应语义增量，不借 M06 升级。

README/69篇当前计数与进度只由 root 按实际写回/适用各端闭合更新；本篇没有新增库存。Notion 仅精确更新既有正确行备注/材料事实，保留个人通读/自测/复习/已提交/评分；共享、Notion、Git fetch/精确暂存/远端核验分别报告。此作者只写 scratch，不写正式库/Notion/Git或个人字段。

冻结 v4 的 pending 和“候选待验收”保留制作时点，最终本次验收结论由真实回执承载。root 若落地前仅维护审核状态字段/该提示，需另列精确 non-teaching 映射，不能据此改教学、伪造新全文阅读或扩大原授权。
