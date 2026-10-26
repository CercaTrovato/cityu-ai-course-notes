# IS5542 M02 全篇审修：主验收与交接

2026-10-27（Asia/Shanghai）。本批是 scratch 审修包，不是正式发布。唯一正式写回者仍为原会话 01a17103-659b-7ad2-81ea-dc814266007f；本会话未写 vault、共享快照/台账、Notion、Canvas、Git提交/推送、配置或本人行为字段。

## 版本与真实基线

- 最终候选 candidate-final.md：322002 bytes，SHA256 1b32c675ec29c4ee86a4de39fece94cb2f57d3f16917ef98ef61a7256157eec0。
- 开工真实字节 baseline.md.snapshot：262390 bytes，2e8e43ff24d101f36bed647ec905fbae83dcd58e887481b223d59f3d201761ef。
- 主写者随后只维护M02一处M01 §2.9.1 WikiLink，原显示文字与其他字节可逆验证完全不变。accepted-link-maintenance.json记录真实来源；正式CAS现在必须用baseline-after-link.md.snapshot：262421 bytes，1adffcd3be75c40fd421217318b52d5e9036ddd7288aba8581e5f0de6e61986b，不能被开工旧基线覆盖。
- 冻结v1 e75c…bf5d与冻结v2 89cd…a108均保留。最终与v2只一行差因确定性表述不同，独立字节验证见reviewer/final-F10-binding.json及v2-to-final-F10.diff。
- included-evidence.json实核原classification的included键（69项）包含本篇；不是拿旧inventory或HEAD覆盖当前融合。
- 作者真实会话01a1787d-ea2e-7092-b7b4-68d964200cd5:/root，独审/root/is5542_m02_independent_61。model-check.json与reviewer-provenance.json记录实际gpt-6.1-sol及显式fork_turns:none/high调度；没有回退其他模型或另派审查者。

## 教学审查范围与结论

主作者完整顺读基线4768行，读完全部所供材料，集中作者自查后冻结候选。新独审先只读候选5237行、64学习单元，落盘stage-1；主确认后才给规则/来源/diff，做同一次审查第二阶段。自动带入规则与候选内历史回执已由独审披露，不冒称完全盲审。
独审全篇范围包括全部正文/模型卡/表格/原题/中英答案/公式/代码/图源、折叠答案、速查、词卡、自测和边界。按高中知识起点复述、手工复做和改条件，不由专业常识补桥，不评分，不推定本人掌握。

原报告链真实保留：
- reviewer/stage-1.md，SHA256 e563da9d86e68951d6df797b2f9b323fe1471e205c062c74b2cc30b31fed5e43：64单元全篇顺读、F01–F10，原待修结论不改。
- reviewer/independent-review.md，SHA256 cff6cc77e97fd4c00c60a1aab2a188e75bf90cf4b110c6dd1421cee4a3b3a989：全源回核、F01–F13，原v1待修结论不改。
- reviewer/targeted-review.md，SHA256 8b516032b6999f60bd5e67e6f497a8538041cb11e1f37ebbb61c72760b721902：v2实际定向关闭12组，F10一行仍未闭合，未放行结论不改。
- reviewer/targeted-review-final.md，SHA256 68937e709d9d68ca767ef7f5c609ad4f24ce518af332ca9793a7688a39d3cc0a：只核该句与同类检索/字节继承，最终1b32全次范围passed，未闭合实质教学问题0。
不能仅凭文件存在、字段或机器门槛证明独立身份/教学语义；上述实际工具调度与原代理报告是证据。

集中修复F01–F13见repair-report-v2.md、repair-v2-log.json、candidate-v1-to-v2.diff；最后F10见final-candidate.json/v2-to-final-F10.diff。实质内容为：token/量化/KV/运行词与optimizer/rubric的用途；离线任务对照与随机用户A/B；明确零样本与示范/模糊测试隔离；eligible满足/不满足/未知三态；捆绑提示版本不归因单条；基准推理设置/许可/寿命/DCR/Elo/安全法律短口径；更晚行政记录保护；8.7差值；考试证据图例；时间/差因未知；Muse训练/回答资源分母；图7/9真实语义；46英文整理与逐字原话地位。
最后F10一句当前明确65.7与57为原值、原因未核、版本/模式/条件/来源错误只是可能解释。未变范围按原64单元/来源/数值/图义真实证据承接，没有重开全文盲读或重复训练。

## 来源、附件与题目

source-manifest.json及final-binding-check.json对六个原件给真实完整SHA/字节并最终重核未变：88页Lecture2 PDF；552条M02转录；9页Project Template；syllabus；两张9/11公告。
全部88页文字、8张联系表覆盖的全部页和必要p2/45/61/71/73/74/75/77/78/79单页已由主/独审按各自真实记录核对。p2信息图确有内容；p3–5为视频入口；页脚不是物理页。PDF实际3860468 bytes，不照pdfinfo的错误0字节显示当空文件；pdfdetach记录0嵌入。
模板9页全文及notes/XML读取，0 notes XML/0非空备注、0嵌入、6个media实际看为logo，无附加题面。不安装python-pptx；当前解释器ModuleNotFoundError后改ZIP/XML读取，未改依赖。不是从“有备注字段”推定内容。
syllabus与当前课程前置/台账供教学背景；官方目录CILO沿既有历史核验记录，不冒称本轮取得官网PDF。9/11两公告原图实际读，承接DDL/作业总览中10/10/10/18更晚已核行政/HKT及本人已提交记录，未登录Canvas，不因未登录降级这些事实。

现有转录552记录/552唯一时点，00:00→末段首02:07:20跨度7640秒=2:07:20，倒退0，相邻段首>=120秒gap0。末段本身很长且有收束，真实末段结束和媒体总长未知。两次宣布休息后文本时钟只前进21/63秒，不证实际暂停方式或休息长度。p6无对应、开头范围待核，不降权。没有认出明确学生提问不等现场无互动。没有核原音/墙钟/外部完整视频。
模型/榜单均为2026-09历史材料；厂商、自报/未独立验证、教师职业观点、视频内李飞飞/主持人与笔记补充分开。源内安装/登录/上传/发送/订房/接口演示没有真实执行；用户代码/成果/元数据未运行或更改。

source-checks-v2.json最终42记录组：34PDF（10标题/导引+24教学任务组，部分组含两问）+8口头任务组。题面、选项、中文限定/逐项解释、英文参考及来源地位已逐源核；42不等于42道独立PDF题或都可独立求解。
p45两图确实缺失，原钥匙B/C不当验证；RULER原为占位模板；GDPval原本截断且缺公司/数据；赛事、NIH/作者履历原记录未取得，不造论文/注册号或报告。化学题保留原键与缺机理证明边界，不为AI基准课编有机机理。DCR无估计器、AA差因及细评分未知继续保留。
46普通口头英文块全部明确“要点整理、非逐字”，45教师/1视频内李飞飞；原题、讲义p8原句、笔记英文卡与规范原句另列。规范引文有实际时间定位/校正，不靠低匹配绿灯代替其他英文块的来源地位。

## 数值与代码

inherited-evidence三文件为旧真实执行的M02相同输入数例，所含别讲数据不冒称本轮M02实做；主/独审核其当前适用性。量化/KV、请求成本、ECE、组合/宏平均/异质、AIME等未变输入承接。
calculation-current.json是本批一次纯教学数值/参考函数检查：softmax更新、BT两模型、Elo、时间估计、酒店假设、has_close_elements边界；不是LLM训练、真实预订、模型调用或业务实验。F08只把65.7−57正确写8.7；参考函数没有运行用户项目。代码任务/输入输出/索引/循环/停止及失败边界已在正文解释。

## 机械、全部警告与绑定

最终current/full/88/source-checks对candidate-final实际运行，quality-gate-result.json显式绑定1b32及after-link源1adff。L0、C.hard0、R.hard0；R.warn404、C.warn3；字面contract42记录passed。最终源句新增的R1a保留完整未知条件，不删条件凑指标。
warning-disposition-final.json列齐404条原code/行号/上下文、18类共用实质依据；原389警告和v2新增/变化23条由原审实读承接，净增不冒称新增数。C三处为行政总引言、六卡总引言、Grok卡，实际日程/卡片/轮次与来源解释在相邻正文，不给空泛引言复制一遍过程。
历史G诊断8/9项通过；E有48组提示，历史总判定FAIL，原始结果保留，不假称旧配额全部PASS。门槛不认证教学。

transcript-audit-final.txt对最终candidate-final真实PASS：36课堂块、488时码/0未匹配、41规范引文/0未匹配/0低匹配，A13/A14均0。A8图例红符号不是会考条；A10三处数字冲突/NOT提醒/M01历史预告按相邻来源/跨讲地位解释，不造本讲时间。显式区间并集7039/7640≈92%，不是媒体完整率，不造末段结束到100%。
旧61b7/89cd门槛/audit保留各自真实版本，未改hash冒称实跑。本篇具体缺陷修复后才复验；没有重训/核音/全库评分。

## 实际显示与图示

9 Mermaid均有可编辑块及figures/源；只有图7/9在v1→v2发生语义变化。原7图按同源图块/文件哈希与v1实际观看证据承接，未称最后一步又重看全部。图7分前三训练与第四使用，图9明确校验失败且真实返回P；新两图top/bottom截图已主/独审实看。
visual/v2-*相关截图覆盖token、softmax记号/优化器、评分准则、三态酒店/捆绑版本、随机用户A/B、Muse原句、p8原格及邻近限定。最终仅F10一句变化，final-F10-unknown-cause.png已主实际看，原独审不冒称看过新图，只核实际最终文本。
final-display-metrics.json为最终可观察DOM：9SVG、136数学节点、错误0、显示式溢出0、无页面横向溢出，fonts=loaded，1280×720/正文900px/16px。最终页面全局ready未由工具返回，不以其为证据。
曾发现预览器把LaTeX内<当HTML，已仅修预览载体，组合条件完整显示；空帽子/列表间距已修。实际载体为本地IAB，未核原生Obsidian。解析成功/尺寸绿不代替图义或教学；原音/外部完整视频/当前平台/法律未核边界保持。

## 精确写回计划与执行边界

publication-plan.json有11个fresh基线目标及17项no_increment。每目标有path/before_sha256/原字节快照/append或replace_exact，只镜像已审M02。根术语总表先合并并精确回读后才能写课程队列“已合”。README仅本篇入口/说明，不猜全库总数，不改别课；根规则不加进度。
M02 §2.3标题纠正导致M03一条入链须随同纯WikiLink维护，计划保留显示文字和所有其他字节，不改M03教学/状态。M03亦fresh基线/CAS，由root处理；不覆盖其前序融合。
既有更晚一页/Canvas/两周、HKT、提交/评分不降级；模板时长不等分值的旧推断只在适用处精确纠正。Notion仅字段草稿，未定位/读取row，不触用户个人行为/DDL状态。无新增原件/录音/用户项目或数据要迁移。
links-final.json按原link_check.py语义在内存投影中定向检查最终候选+11目标（12文件），全vault建目标索引但不做全库评分，结果0；没有应用任何正式增量。
integrity-final.json使用本任务开工自有snapshot而非共享manifest，verify通过；观察到56处并发变化完整列盘，非本会话编辑。正式M02当前仍精确等after-link基线，原件六源哈希未变。共享目标最终fresh比对见final-binding-check.json，若此后变化只重基精确增量，不用整文件snapshot覆盖。
资源已关闭：自有tab3及8821/session46156，8821不再监听；未碰其他端口/标签。

冻结正文保留pending字段/候选提示以维持原审绑定，另交可选metadata-maintenance-plan.json，只在正式主写者接收并实际写回/回读后按非教学维护流程改状态和提示，保存新diff/hash，不把1b32冒称维护后字节。
本包教学/视觉/机械完成不等于正式正文、跨文件应用/回读、Notion、Git或线上发布完成。后者本次均未执行；没有普通会话创建/跨线程消息。root接收后fresh-read/CAS/原子写/精确回读并逐端报告。


## 收尾的README并发重基与链接证据

README在根级并发发布中再次变化，最终提案只从最新正文提取唯一IS5542课程入口句并追加本篇同一后缀；所有最新全库计数和其他行保留，未写正式README。具体新基线/快照在readme-final-refresh.json及publication-plan.json。原12文件定向链接结果0与最新README单目标定向结果0合并覆盖最终12文件，其余11项输入/候选未变，见final-link-union.json；不是把旧README扫描重标成新执行。根主写者应用时仍须fresh-read/CAS，任何后续变化只重基精确增量。
