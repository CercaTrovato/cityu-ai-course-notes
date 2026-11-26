# IS5542 期末复习框架交接（2026-11-23）

接收：当前总监督「CityU 五课总监督｜剩余任务与期末」，`01a20688-5a1e-7a10-9e18-4ae2d0bcd7bd`。本轮按委派限制只准备 `IS5542_GenAI_in_Business/review/final-2026/`，不改本课 assignment、既有 review 其他文件、根 README 或共享看板，不调用跨会话发送，不向历史总监督发送。本文件供总监督直接读取。

## 可直接使用的结果

- `framework.md`：12 单元、完整课程模块映射、知识依赖图、题型动作、建议顺序、8 项逐题施测的诊断方案，以及最终模拟／补弱方法。
- `sources.json`：44 条稳定来源 ID，含 10 份核心原件、两张历史公告、7 份转录、9 篇笔记参考、考务历史记录、当前官方目录索引，以及待补和外部来源。每条区分 verified／pending、实际可读范围、页码／时间戳、来源类别和限制；本地已存在文件记录字节数与 SHA-256。
- `handover.md`：本回执，记录实际材料、缺口、独立抽检、并发边界及总监督待处理项。
- `progress.json`：`schema_version=1`、`course=IS5542`，12 单元均 `status=not_started`、`mastery=unknown`；`sessions=[]`、`mistakes=[]`。下一步为用户开始后逐题施测 D1，尚未施测或打分。

框架覆盖现有 M01–M09：基础、模型选型、10 类 benchmark、提示／上下文、agent／harness／RAG、三种架构与上线、JTBD／Design Thinking、营销、银行、创作者、法律与 Responsible AI。客座六场均保留；10/17 实际两份资料是 Agentic Era／FDE，不沿用旧 VC 标签造内容。Syllabus 中零售、保险、HR 等尚未取得独立专讲的内容列待范围核实，没有静默删除或编造成已讲。

## 本次实际核了什么

1. 根／本课 AGENTS、前置资料、可读性与制作流程、原题／课堂练习规则、备份与文件安全规则；未启用 Superpowers。使用 PDF 与 PPTX 读取技能，未制作幻灯片或 PDF 成果。
2. 递归枚举本课 `course_files_export` 全部 15 个文件，按文件签名识别了无扩展名的 Google Marketing PDF。10 份核心原件共 **551 个物理页／slide**，均抽取逐页文本；逐页索引、关键正文和范围证据定向读。Syllabus 3 页全文直接读，Lecture 1 p.9／12 原 XML 正文直接核对，M02 后段与 M08 可读正文直接读；详细范围在 sources 中。没有声称 551 页重新全篇教学或全页视觉验收。
3. 实际查看两张 9/11 公告截图；Guest Lecture 原公告确实写客座内容纳入期末。另实际查看五张既有源页图像资产：Design Thinking p.49／50／61、M02 p.45、M03 p.74。不是本轮全页重新渲染；未冒充原生 Obsidian 实验。独立审查者还从原 PDF 渲染查看 Design p.49／50 和 L3 p.24／27／29，范围在报告分列。M02 原图缺件保留，新增框架没有改原件。
4. 读现有 M01–M09 的正文速览／学习目标，M07 开头及 §2.1–§2.9 等详细正文；转录按课程安排、考试信号、银行治理／用途／演示等定位，未本轮逐字通读全部或回听原音。A／B 独立时钟与 partial 边界保留。
5. 重新查金融原件：本课当前源目录（含无扩展名 PDF）和 `C:/Users/BenLi/Downloads` 的 IS5542／GenAI／Financial／bank／Responsible／Guest 文件名过滤，未找到。结论仅限所查本地范围。
6. 当前官方目录、图书馆入口／年份清单、IS5542＋2025／2024／2023 年、mock、外部小红书等实际公开检索。官方当年目录公开索引支持 50%／2 小时；直接读取 PDF、图书馆入口与年份页返回 403。索引可读与认证内完整内容分开。旧 2023/24 同代码属 Outsourcing and Offshoring Management，排除误配。
7. 侧栏检查后实际尝试创建 `iab` Canvas 标签，返回 `Browser is not available: iab`；说明限制后尝试 `chrome`，同样不可用。没有进入 Canvas、AIMS、图书馆认证后的 IS／学期清单，也未站内登录小红书。未绕过安全停止，未购买资料、调用外部按量付费模型 API、发帖／私信或发送邮件。

## 仍缺的优先级资料与入口

| 优先级 | 待补项 | 当前真实状态／下一步 |
|---|---|---|
| 1 | 最后一节复习课课件、录音／转录、考试说明 | 既有 tentative 安排为 11/28；11/23 尚未到。仍须回读最新公告确认日期；到位后先更新范围和练习顺序 |
| 1 | 当学期教师参考卷／mock、官方答案或 rubric | 本地没有取得独立卷，当前 Canvas 未访问，不能写“未发布”；先核 Files／Modules／Announcements／考试相关页面 |
| 1 | 11/21 Responsible AI 专属材料 | M10 原件／转录未在本课本地找到；不以 M01 概览替代其覆盖 |
| 2 | M07 金融原讲义、完整演示与缺失录音边界 | 重新查后仍仅部分录音／笔记；取得后定向补单元，不重做全课笔记 |
| 2 | 正式考务／允许材料 | 12/18 18:30–20:30、LI 3508 只是 11/5 AIMS 历史基线；本轮未重登。开闭卷／材料／计算器／选答规则未知 |
| 3 | 图书馆 2025–2026、2024–2025 等 IS5542 往年卷 | 仅公开年份清单与检索，未进入 IS 部门／学期清单。先核课程名称、年份、学期，避免旧代码错课 |
| 4 | 小红书外部线索 | 公开搜索未得可核题面；站内未查。即使取得，仍为外部资料，不能升级成教师明示或真题 |

Canvas 入口：<https://canvas.cityu.edu.hk/courses/71410>。图书馆：<https://www.cityu.edu.hk/lib/digital/exampaper/index.htm>；年份：<https://www.cityu.edu.hk/lib/digital/exampaper/ftlist.htm>。本轮没有向用户索取凭据；浏览器可用后若确需认证，仅让用户接手确实必要的登录一步。当前不因这项阻塞暂停可用部分的复习。

## 总监督汇总时可读取的字段

- `framework_status=usable_with_source_gaps` 表示路线可用且仍有来源缺口；与独立抽检状态、学生掌握程度分开。
- 各单元稳定 `id`、`title`、`source_ids`、`prerequisite_ids`、`question_types`、`status`；`suggested_order` 为本课建议顺序。
- 学习证据采用 `explanation_seen`／`solved_with_hints`／`independently_correct`／`retest_passed` 分层，当前均无证据。未来须保留用户关键原问题、原作答、提示和纠错，不按文件数／聊天数计算掌握。
- `exam_conditions` 中 `schedule_live_verified=false`、`format_final_confirmed=false`；比例只放 `provisional_format`。不要据此把 20／30／50 或场地标为本轮已正式复核。
- 需要在本课 `review/README.md` 加入口、共享五课看板登记／发布，以及根仓库提交推送的动作，均交总监督统一串行完成。本会话不操作这些共享文件，不并发 `git add/commit/push`。

## 文件安全、验证与本轮边界

隔离基线：`E:/app-data/codex/scratchpad/is5542-final-20261123/integrity-baseline.json`（59 篇 Markdown，开工 errors=0），未覆盖共享 manifest。四个目标在开工时均不存在。原文件 SHA-256、文本索引、候选与脚本均留本任务 scratch。

沿用委派所承接的 Remotely Save 自动同步关闭要求和已有确认，本轮没有启动同步；当前电脑配置仅暴露封装键，未直接核出自动同步开关值，不声称观察到手机状态。正式写回仅使用 `safe_write.atomic_write`、写前原目标状态核对和写后字节回读。

独立抽检由未参与撰写的 `/root/is5542_framework_review` 执行，显式模型 `gpt-6.1-sol`、推理强度 `high`，`fork_turns=none`。第一阶段先读候选，抽 U07、U05 及 D5→补依赖→变式→隔后复测路径；第二阶段才给规则和原件，独立重抽 Design p.34／39／49–63、L3 p.14／15／20–33／38–40 并看必要原图，另核客座公告与 L1 p.12。报告没有认证其余单元全部来源、551 页全覆盖、当前线上材料、法律现行性或本人学习效果。

第二阶段发现 U07 未显式列五阶段的完整路线缺口，已补“同理理解→定义问题→构思→原型→测试”的任务、产物与反馈，以及问题／方案的发散收敛；另补 JTBD／job story／HMW、harness／RAG 的中文用途入口，D3 区分术语陌生与业务推理，D5 可普通文字描述。JSON 同步这些目标；其余补充只有评测口径、科学 AI 应用边界和笔记链接。集中修改后由原审查者定向复核，最终结果写在下方回执。第一／第二阶段报告路径为 `E:/app-data/codex/scratchpad/is5542-final-20261123/independent-review/stage-1.md`、`stage-2.md`，保留真实旧候选 SHA，不把新版本倒写成首轮已经通过。

`note_quality.py` 的 M／T §0–§9 门槛不用于冒充本次复习规划通过；本轮没有新写或改写 M／T 正文，不制作虚假的 `note-review-v2` 正文发布回执。实际核 JSON 结构、ID 引用、依赖、页数、链接和隔离完整性。当前没有授课、正式模拟、作业提交、外部写入或 Git 推送完成声明。

写回前完整性回读发现本课 assignment 内另有 3 处并发变动：新增 `A01-genai-project/notes/final-closeout-20261123.md`、`final-ppt-fill-20261123.md`，修改 `work/presentation/draft-20261123/missing-materials.md`。均未由本会话修改、覆盖或纳入提交；本会话保持只写 final-2026，交总监督分别核对。


## 交付前定向复核结果

原审查者的 `final-review.md` 已实际回读：U07 五阶段覆盖缺口、术语入口与 D3／D5 分流均关闭；样本及修改范围没有剩余阻塞，可交付为带来源缺口的复习框架。未独立重审全部 pass 指标细节或全部科学 AI 事实，不扩大为全课教学验收。

- 复核报告 SHA-256：`de30f6b218395a7dd82aa394bf96f625fb91f863a6bd1f6eb6bcb3c02a71ca7d`。
- 最终实质框架 SHA-256：`1fdb9b1be8fb70b3400c4b6232f74baab5265316518db7a9c44ca74a738753ca`。
- 原审查 progress SHA-256：`870f309e9e3c896e87899e9db5bfd9ceb0d4bc36798a2fac488c4032381c7436`；之后只补审查状态／证据字段，单元、考试条件与学习记录未改。
- 来源清单：34 条 verified（只按各自 verification_scope 解读），10 条 pending；44 个来源 ID 和 12 个单元 ID 无重复。
- 候选 JSON 结构、来源引用、先修顺序、全单元路线、现有笔记回链、源文件哈希核对均 errors=0；没有新增学习会话或错题记录。
- 四文件正式写回和隔离完整性的实际回执位于本任务 scratch 的 `publish-result.json`、`integrity-final.json`；四文件已原子写回并逐字节回读一致，初次写后隔离完整性 errors=0。

最终写回范围为本目录四文件。初次写后完整性统计 63 篇 Markdown、errors=0；相对开工基线的其他并发变动与本目录新增分列在回执中。没有 Git 提交／推送或共享看板发布；这些仍由当前总监督统一收尾。
