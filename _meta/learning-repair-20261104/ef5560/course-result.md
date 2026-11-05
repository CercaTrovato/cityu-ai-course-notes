# EF5560 逐页修补结果 · 2026-11-04

本批完成 8 篇核心笔记。按版本实际查看 604 张源页，共保留 121 张课件原图。每篇通过两阶段独审、定向复核、正式发布门槛及正文精确回读，预习、课中逐页跟读、课后复做各有证据。

| 笔记 | 实际源页范围 | 课件原图 | 本轮修补 | 写回、独审与 Notion |
|---|---|---:|---|---|
| M01 | 58 页 | 15 | PDD/JD 案例、复权和数据时钟按物理页定位，修正逐页原题和四类诊断图读法。 | [正文回读](m01/writeback.json) · [独审](m01/independent-review.md) · [Notion](m01/notion-readback.json) |
| M02 | 课堂旧 54／Canvas 新 56 | 12 | 分开旧 p.25 错轴与新日期轴、两道新增选择题、SPY 单表与三市场汇总。 | [正文回读](m02/writeback.json) · [独审](m02/independent-review.md) · [Notion](m02/notion-readback.json) |
| M03 | 课堂旧 56／Canvas 新 54 | 12 | 旧版专属页、PCR 新四格和旧推导分开。Ridge 52 周价差 +0.48052 个百分点。 | [正文回读](m03/writeback.json) · [独审](m03/independent-review.md) · [Notion](m03/notion-readback.json) |
| M04 | 课堂旧 54／Canvas 新 56 | 14 | 保留旧题与新版演示，纠正完整树图及两次局部裁切，分列美国提升 +6.3%／+6.1%。 | [正文回读](m04/writeback.json) · [独审](m04/independent-review.md) · [Notion](m04/notion-readback.json) |
| M05 | 54 页 | 11 | 六题 14 作答单元。分开 0／1、连续仓位及 CAPM 三种现金处理，按已有公告记录厘清 8＋1 页。 | [正文回读](m05/writeback.json) · [独审](m05/independent-review.md) · [Notion](m05/notion-readback.json) |
| M06 | 54 页 | 18 | 四轨转录。修正双花候选分支与首次确认，回核 p.39 报销和 p.49 回收期。 | [正文回读](m06/writeback.json) · [独审](m06/independent-review.md) · [Notion](m06/notion-readback.json) |
| M07 | 54 页 | 27 | 补 p.03 英文比较指令，18 个题面／演示源页，核拍卖锁款、AMM 三种价格和分类分母。 | [正文回读](m07/writeback.json) · [独审](m07/independent-review.md) · [Notion](m07/notion-readback.json) |
| M08 | 54 页 | 12 | 区分二级成交、一级赎回、Aave 借款与清算。p.47–54 顺延的完整计算保留。 | [正文回读](m08/writeback.json) · [独审](m08/independent-review.md) · [Notion](m08/notion-readback.json) |

## 配套范围

- A01 的教学 Notebook 原 SHA 与 2026-10-27 独审版相同。本批在隔离输入和空内核重跑 36 个代码格。17 份结果有 16 份逐字节相同，包括权重 CSV、五张图和三张表。结果 JSON 的差异为路径与两项低位浮点值。
- A01 导览、知识地图和课堂复现 README 已核并修正链接或说明。现有源码 ZIP 的 36 个代码格与 Notebook 相同，20 个讲解格保留旧版。历史回执和正式作业材料按库存中列出的排除范围处理。
- 练习索引将已经审过的原题链接至相应页，独立练习文件及本人课程状态按其各自记录。复习目录及其他纯导航按库存核链接。详见 [配套回执](supplementary/evidence.json) 和 [范围清单](inventory.json)。

## 检查和交接

- 隔离完整性核对 49 个文件，0 个异常，16 个预期改动。所有课件原图的文件散列与发布回执一致。本课正文与本批证据链接 0 个问题；全库检查另有其他课程或历史候选的告警，已按归属隔离。link_check 问题数: 21 （扫描文件数 790）。
- 显示在本地 Chrome 用同源课件资产、KaTeX 与 Mermaid 核验。原生 Obsidian 显示没有直接验收。四轨或双轨材料的缺录、原音未逐声听校和后续未取得课堂证据按各篇记录。外部行情、产品及政策描述以相应的历史材料范围为准。
- 课程 Notion 八篇已读回；M06 的历史文件名经 Notion 自动生成链接，按显示文字规范化后与拟写内容逐字一致。其余属性逐值比较。Git 状态为本地工作区改动。
- 根 README、跨课术语和转录登记的增量已交 [共享增量清单](shared-updates.json)，由统筹指定的收尾者合并。
