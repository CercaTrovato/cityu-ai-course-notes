# W7 主代理完成核查：2026-11-02

## 本次范围与来源

用户要求寻找正确 W7 分类稿；现成稿搜索覆盖 CityU（含 anaconda_projects）、Downloads、Desktop、既有 outputs，仅命中教师教程，因此从教师副本完成三问。用户本聊天已确认电脑/手机 Remotely Save 自动同步关闭。开始快照 is6400-week7-build-20261102，599 Markdown；旧 dirty 文件保留。只制作并交付本地文件，由本人手动提交。未上传、提交、撤回或改 Canvas；不处理 10/21 Quiz、小组事项或 Git。

定稿前实际只读核 Assignments / Announcements / Files / Modules。W7 337924 为 10 points、2026-10-23 23:59 HKT，页面仍显示 New Attempt；旧 10/21 13:02 附件为 Bitcoin，已下载并与 A09 SHA 672b72e19019cf07d6cd7139e4fd666d9d11ee99c6ad329dc1e5dbdd38643de8 完全一致。337924 是分类三问入口，不是 Bitcoin 主作业。教师 Notebook 23 格及两个 CSV 哈希见 sources.json。分类数据本轮从 module 666019 / file 15905852 下载并与库内全字节相同。Files 总入口重定向课程首页，已从 Modules 发布附件核源；公告 5 条、10/1 提交说明 637007 已读，没有 W7 新追加题面。截止已过；未试提交、未确认迟交许可或可得分数，不把 New Attempt 当作教师同意补交。

## 计算、原题与文字

最终 Notebook 39 格，19 代码格 execution_count 连续 1–19，error 0。原教师 23 格 source/type 与成品 cells 2–24 逐格一致，原件只读。学生三问用 creditcard-reduced.csv，保留全英文题面（50/30/20）；原题 credictcard 拼写按真实附件在代码中纠正。Q1 五模型同一 stratified 60/40、seed42；Q2 机制与真实比较；Q3 同一树固定其余参数，只变 class_weight。完整实现、独立拆分/指标复做和四点修复见 independent-review.md / stage-1.md。去重 177 后 32,587，训练 19,552、测试 13,035；测试正类 189。AdaBoost TN12844/FP2/FN1/TP188：F1=376/379=0.992084；权重后树 FP5→7、FN均1，不编造改善。成本 FP+rFN 的 8 项、Time 训练内验证和类别分布已复核，明确是当前随机切分结果。Time 重要性不是因果。

正式新增英文 Markdown、动态生成文字、表格与标准 HTML 均按全库 §4b 全文核对。没有新增内部审核/待上传提醒、非数字段内手动加粗、多余自我保证和泛泛防御语。必要数据分布/评价范围限定只在其影响解释处保留。真实工具声明保留。A10/A11 承接本日正文独审与运行证据，exact SHA 锁定，不再改词、重训或重复全篇审查。

## 机器警告的具体处理

当前 guide：L=0、C.hard=0、C.warn=0、R.hard=0；R.warn=11，历史 G/E PASS（不等同教学）。没有机器源题清单，因此机器 source_coverage 为 unverified_without_manifest；人工逐源与独审已核 3 问完整，不改写成机器已认证。

- L14 R1a/R1c 两项：一个完整段落按 Q1/2/3 列实际交付，分号分隔三问，前后有文件入口；独审逐问顺读无缺桥。
- L60/62/128/140/152/154 R7a 六项：sigmoid 概率、指标、权重、内部 F1 与实际结果按课程六位精度展示，旁有符号、分母和小例；不为警告删正确数值。
- L86 R5a 一项：五个行内式属于 AdaBoost 同一个 5 记录归一化数值链，已补 ln/exp 反运算、2/6 与 1/6，独审亲算关闭。
- L94/96 R6b 两项：四术语对应矩阵四格，紧邻给中文定义、行列方向及 AdaBoost 实数，随后四式逐项解释；不是未解释术语堆积。

## 实际显示证据与范围

root 与独审实际观看最终 cell-28.png、cell-32.png，5+2 混淆矩阵数值/坐标/标签清晰，图与表一致。正式 HTML 从同版本 Notebook 标准 HTMLExporter 导出，不手改。浏览器预览连接超时后断开，改用标准 nbconvert WebPDFExporter + 现存 Chromium 做私人打印核验；没有安装、下载软件、禁用 sandbox 或使用用户登录 profile。

week7-render.pdf 共 21 页、guide-render.pdf 共 6 页。实际看 week7 页13/17 公式、页14/18 数值表及权重图；guide 页2/3/4/5 的标准化、sigmoid、Gini、ln/exp、归一化、四指标与权重/成本均真正渲染，无裸 LaTeX、缺字或公式溢出。PDF 的长代码行按标准导出打印会水平裁切，提交 HTML 原样保留可横向滚动；PDF 仅内部核验，不作为提交文件。未声称原生 Obsidian 侧栏或 Jupyter 桌面 GUI 已看；实际显示证据载体及范围明确。本轮没有 M/T 教学版本升级。学习 guide 保留 draft 标签，不替本人确认学习及原生 Obsidian 导航验收。

## 完成条件与状态

独审者 /root/w7_review 未参与写作，完整首读后回源核规则，再定向关闭 4 点。最终教学阻塞 0。机器门槛和报告 SHA 绑定只验证版本，不认证语义；本报告给出实际证据。提交文件本地完成，行政补交接受情况与本人手动提交另列。旧 A09 字节及历史已提交状态保持，新 W7 分类件尚未上传；A10/A11 新稿也尚未提交。Notion 与本地入口只更新准备摘要，不修改个人已提交/学习/评分字段。
