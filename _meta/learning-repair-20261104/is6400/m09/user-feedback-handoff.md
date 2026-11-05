# IS6400 M09 用户反馈与交付断点

2026-11-04T19:48:20+08:00。M09 单篇优先；其他篇不重审。正式文件、原件、冻结候选和原独审回执未改。

- 2026-11-04 15:12:28.794（北京时间）：mcp__cua_repl.js 调用 let iab = await cua.getBrowser({id:'iab'}); 返回 “Browser is not available: iab”（call_5ab4696ad7a840e0ab9fcb0d8f20886b，会话记录第 306 行）。
- 2026-11-04 15:14:03.440（北京时间）：mcp__cua_repl.js 调用 let chromeLauncher = await cua.getApp({windowId:460952});（绑定 Chrome 以新建专用预览窗口；call_0c52aa689d424c4bbd1aeae5a8282306，会话记录第 359–360 行）失败。工具原文：

> Computer Use has been stopped for this turn because it could not determine the current browser URL on Windows with enough confidence to enforce policy. Stop your work and send a final message noting why Computer Use ended.

工具原文说 Computer Use 在当轮被停止，原因是 Windows 上不能以足够置信度确定当前浏览器 URL 来执行策略；接着要求停止工作并在最终消息说明原因。原文没有说永久禁用某个 App，也没有授权切换通道。统筹后续要求不重试受限操作或改渠道绕过；此次只读本地文件与静态源图，没有 Computer Use 调用。

正式路径：D:\上课资料\CityU\IS6400_Business_Data_Analytics\notes\M09-深度学习-神经网络与文本分析.md。仍是 2026-10-28 旧稿，SHA addb8b49623ef0bbc7d4092e5c3a0bf4dcd0b49df8203db54ebf2b82d162d14a。正文 0 个图片引用，正式 notes/figures/m09-source 不存在；§2 按主题并页（如 p.16–17、21–30），§8 为区间或多页映射。用户反馈对日常入口成立。冻结稿：E:\app-data\codex\scratchpad\learning-repair-is6400-20261104\m09-revised-layout.md，SHA 05c969c6aa9867e26134d196b9410759dfaa5cbdda8c7e72d9b90e5aafe9d798。§2 有 98 个页级入口，§8 逐物理页精确定位，83 个图引用有 83 个暂存图。独立 HTML 有自己的资产，未与正式入口相连。上述数字不是教学深度证据。

实际打开六张 PDF 源页 PNG，对照现有候选：

| 页 | 现有解释和判断 | 最小修补 |
|---|---|---|
| p.10 | L105–129 已解释 a_j、W_ji、in_i、g、a_i，有二输入和偏置数字例。 | 补三段原标注：右边三个箭头把同一个 a_i 送往不同单元；原图无单列偏置，补充算例才加入 b。 |
| p.16 | L182–186 有 5→3→4 和前馈方向，缺一条可跟的原图线路、节点计算和非线性的条件。 | 沿最上输入→最上隐藏→最上输出；最上输出另接中间隐藏节点，图中并非全连接。节点按 p.10 乘加再激活；若各层只做乘加，整体仍可合成一次仿射变换。 |
| p.24 | L257–261 能对准 x₁→a₃⁽²⁾ 的红边、起始层及终点／起点下标，保留中英原问与答法。 | 补 θ⁽¹⁾₃,₁x₁ 是第 3 行第 1 特征列的贡献，与该行其余特征及偏置相加，再激活得到第 3 个橙圈结果。 |
| p.30 | L333–337 有三输入和猫图的特征层级，未逐层对应左图及右图结果。 | 左图按 3→3→2→1 走一条原连线到 hΘ(x)；右图另沿照片→隐藏表示→CAT? YES，边缘到物体是图示直觉，不将两张网络按节点硬配。 |
| p.69 | L841–845 主要点数黄色框。p.70–75 分拆讲解完整运算，p.69 自身还不能跟中间块的一条完整流路。 | 标三个时间块、蓝 x 紫 h、上下跨时点线；沿 C 的 ×／＋ 到下一时点，再沿粉色 tanh 与输出门的 × 得 h_t。区别三个 σ、黄色候选 tanh 和粉色输出 tanh；给两条短式，回指 p.70–75 的分步。 |
| p.72 | L859–863 已能定位黑色输入线和第一个 σ，有门公式及 0／1 两端；尚未示范门值怎样实际改动旧 C。 | 补 W_f、b_f、σ 各做什么，沿 f_t 竖线上行与顶部旧 C 相乘，示算 2×0.25=0.5；这是保留下来的旧部分，新内容尚未相加。 |

下一步另起候选，只改六处，重点补 p.16、30、69、72；原题、其他 92 页及既有审查证据保留。由原审定向核六处，实际显示和正式写回仍待统筹确定。未调用 GUI，未改变正式正文和图片目录。

建议的 Obsidian 用户入口（方案，未执行）：在本课程 review/m09-preview/M09-待验逐页学习稿.md 放同库待验副本，图放 review/m09-preview/figures/m09-source/，Markdown 相对图链可直接复用；同页外链保持原 vault 目标。候选页在首部明显写“待验预览，不是正式稿”，不更新用户个人字段；review/README.md 可列临时入口。待统筹确认后，正式 M09 只在 frontmatter 后加一个纯导航说明，写清“下方为旧稿，新稿待验”，用全 vault 路径双链指到候选，保留旧正文其余字节。先静态逐图核 83 项 SHA、98 个页锚与全部回指、校验候选的教学正文差异及外链目标；用户从 Obsidian 实际打开，检查六页图与公式、Mermaid 和 §8 跳转。验收结论按实际显示证据记录，候选不作正式发布或同步。
