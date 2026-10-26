# IS5113 M04 全篇主验收记录（仅交接准备，未发布）

作者/主验收：`/root`。独立审查者：`/root/review_is5113_m04_full_61`。本任务只写 scratch；正式主写者为会话 `01a17103-659b-7ad2-81ea-dc814266007f`。本记录不把准备完成写成正式写回、同步或推送完成。

## 范围、版本与独立审查

真实基线 `baseline.md.snapshot`：SHA256 `ee9f0ae7bc90252ffe6b3266c72f99c1ea9bf97c5c57c392dca1b0695b5a4e2b`，367839 bytes。审查范围是整篇，包括前置、41 个教学单元、图/公式/原题/术语/摘要/自测/来源说明及受影响依赖。不是仅审新增四案。

唯一独立代理的模型与实际执行见 `reviewer/model-check.json`。审查者先顺读候选，首读 5999 行、41 单元并将真实发现写入 `reviewer/stage-1.md`；随后同次阶段二回源，报告 `reviewer/independent-review.md`。B01–B13、S01–S04 集中修复；原审定向 v2/v3 关闭全部实质教学阻塞。各阶段原报告不覆盖、不由作者冒写。

原审最终接受的 v3 SHA256 为 `7a3e8ca26a09548481b9f0af7863289b4c40d342c9fb9cdd3131fca78a8fbbfa`；`targeted-review-v3.md` SHA256 为 `dad771c764f1c4157d10f513299f1fb07ee1e47b11d0ffbdbd2957712e885756`。

实际显示发现论文分组标题与节点重叠，因此最终 `candidate-final.md` 只在第一张 Mermaid 增加一行 `subGraphTitleMargin` 配置。精确差异为 `v3-to-final-visual.diff`；`visual-maintenance.json` 绑定原受审版与最终版。节点、边、文字、公式、方向、条件与解释次序均未改变。此为制作流程 §2.1(4)、§3.4 的排版维护，主代理核差异后承接原独审，不声称审查者另读过这个排版版本，也不增加全篇审查。

材料保留既有 `v1.0 / transcript: merged`、date；updated 为 2026-10-27。保留的旧 frontmatter 审查字段仅是历史记录。本人通读、自测、复习、提交与评分均未升级。

## 来源、逐页和逐题

`source-index.json` 绑定旧版 50 页 PDF（SHA `abf92042caca6887e981f4b53736de44507e1bc89830c090fa56be191a809e94`）、新版 79 页 PDF（SHA `7180a25a7f4581e9258163fc03d14eab7afbe452caf48daf44bd07af21040ab2`）及原转录（SHA `8423e6b36461cfcb644ac9485c09b25d365194df7b21a8333b390448da93b797`）。课程 Outline 2 页另见 sources 证据。旧页码继续定位旧版，新页码显式标新版，§8 保留对应。

主代理通读两版文本、整篇与转录，实际查看 28 个不同来源页，相关图片留在 `source-images/`。共享 50 对原嵌图解码像素哈希相同；文字例外为 p.19 标题单复数及旧 p.24／新 p.53 过渡标题。旧 p.26／新 p.55 有审查元数据、图例与五饼图，不能作标题例外。旧版当前分类为 43 内容页、7 非内容页；历史 42/8 不追改为新执行。

论文模型严格保留可辨五路径：Disclosure→Helpfulness/Reliability，Clarity→Functionality，Accuracy→Functionality/Reliability，控制项指三种信任信念。箭头为研究假设关系，不补系数、因果或九条全连接。p.18 原问为 `Does disclosing the usage of AI compromise trust in the user?`。新 p.31 Applicant A92/B74/C61 原表不附口述 cutoff80 为资格规则。

`source-checks.json` 保存 34 项原问/条目契约：旧 p.27–29 的 21 项隐私原题、新 p.44 四问、新 p.50/51 共八问及 p.18 研究问句。原问、必要语境、中文读法与实质英文参考答案分开；同案四段中英可共同回答两页不同问法，英文注明笔记自拟。34 项字面锚点初查无缺失；最终 gate 的 source_coverage 是当前机器核对结果，不能代替上述回源。

转录计数为 969 条记录、968 个唯一时刻，`01:46:32` 两条，不删重复秒值。`00:00–02:11:34` 是文本跨度，时间连续/课间公告不证明原音完整。41 个课堂补充标签保留，audit 的 40 格是格式识别口径；`transcript-audit-v1.json` 检查 153 引文/682 时间引用，无字面不匹配及 A13/A14。告警涉及无红级、无固定实况标签与六行邻近引用定位，不为凑标签或红条编考试通知。

欧委会 Article3/6/50/113 与 Omnibus 本轮保存网页响应；法律角色、两类高风险路线与分期不混同 Article50，完整附录、具体系统与过渡个案仍待核。NYDFS 原链接重定向取得 19 页原 PDF，SHA `3508fb05240c10cf10a30094a2e4e1d8bc0ace1cbc169f3fda4e928ddd579162`，未发现特定违法证据不等于全面公平认证。CanLII/CRT 本轮 403，Air Canada 裁决事实沿旧引用保留，不能冒称本轮重读裁决全文。未重取完整 GDPR/香港法规、FAQ/Article111、FMTI 原报告、论文微观数据，未实测产品/SDK、未逐声核音。

## 重要计算与边界

`calculations.json` 保存九格、最小值/并列最优、派生比例、金额与量表计数。`v2-directed-calculations.json` 只针对变化的停止目标承接旧九格并收集完整 tie，未重复训练。找到一个达到下界的解可证明最小值，但不证明已找全同值解；本例完整集合须遍历九格。

FPR 的分母是实际未再犯者，FNR 的分母是实际再犯者。30 人自拟微例：4/20=20%，3/10=30%，总体高风险 11/30≈36.7%；三者问题不同，不能用作口述 9/10 或 1/10 的实证来源。21 项审查按截图为 18 满足/3 部分，三个部分为 GEN1/DCQ5/SHRQ5，不能将五域饼图扇区作 21 项总分。Air Canada 各金额加总是算术核对，不扩为裁决全文重新确认。

透明六构件按功能区分，受众不排他；信息 Accuracy 与预测准确率分开；透明不自动带来信任、公平或问责，授权、纠错与救济须另建立。公司 ensure/default 等引文保留来源地位，摘要/速查/自测改为主张或可能作用。旧“必考/不考/7红级”不能由课堂总结、自读安排和不完整 ASR 推出。

## R/C 疑点的实际处置

最终门槛结果与全部位置分别存 `gate-output.txt`、`quality-current.json`、`warning-locations-final.json`。分类依据与真实相邻说明见 `warnings-review.md`；不将警告数改成零，不以字数、标签或脚本 PASS 认证教学。原 v2 的 C.warn 7 均为父节短引言，实际解释在随后子节；R.warn 保留全部机器原文。原唯一 R1a 硬长句已拆为两段，v3 两处 `\text` 命令的 TAB 损坏已修，最终实际显示另核。

独审发现的问题先修正文，原审定向闭合；不能以“这是误报”覆盖 B01–B13。C.hard、L 与本次全篇 R.hard 必须为零；若最终门槛另报真实硬项，本包不能放行。旧 G/E strict 结果单独保存，不能称其 PASS。

## 实际图文观看

载体为本机 IAB 同源浏览器预览，viewport 1280×720、正文宽 768px；不是原生 Obsidian。`preview.py` 只负责转换与渲染。曾因 display math 正则从单行公式的尾部跨段吞入下一公式，生成仅 4 图/16 数学的错误 HTML；修为逐对 `$$…$$` 后生成 5 图/38 数学，无占位符遗留、0 KaTeX 错误，未靠修改教学内容掩盖转换问题。

实际查看并保存：论文五路径图（651.65×630.99）、搜索停止图上/下（541×1246）、错误率中文标签/分母公式、法律分类桥、四案中英收束、隐私审查概览与展开原题/GEN1 中英答案。SVG 保存为 `diagram-final-1.svg` 至 `diagram-final-5.svg`，尺寸见 `browser-display-final.json`。三张未变概览的语义图源哈希和 768px 同源 v1 实际截图由 `diagram-version-map.json` 承接；不把承接说成本轮重新逐图观看。第一张图通过仅增标题留白消除实际重叠，第二张图确认“九格全部检查”才停止收集完整 tie。

误命名的 `research-model-final.png` 实际是旧转换异常时的反事实入口，明确排除作为论文图证明；应看 `research-model-final-fixed.png`。不声称完整笔记每个滚动窗口、原生 Obsidian 或全部原音已经实际查看。

## 发布与同步边界

`publication-plan.json` 含正式正文指针和 10 个共享文件的实际最新基线 SHA、原字节快照、29 个 append/replace_exact 操作及预期输出哈希。根术语先合并并回读，课程队列才可执行完成记录；README 仅本篇精确行更新，不计算全库进度，根 AGENTS/CLAUDE 不追加进度。所有草稿只镜像受审内容，不加入新教学。

正式主写者必须重新核 main_note 基线，CAS/原子写/精确回读；共享文件逐项 CAS，冲突停该项并重合并。计划中的“已并入”等文字只有对应依赖真实完成后才可应用。Notion 本任务未访问/写入，须由正式主写者读取既有 M04 行、保护本人学习字段，写后逐字段回读；Canvas/Git 同样未写入。独审/视觉/机械通过、正式写回、同步和远端分别报告。
