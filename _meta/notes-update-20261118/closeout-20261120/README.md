# 11 月 18 日笔记批次 · 三端收尾回执

完成日期：2026-11-20。本批发布收尾已完成，缺源部分保持待补。

| 环节 | 已核结果 | 证据 |
|---|---|---|
| GitHub | `main` 内容提交 `b7a095b8453a9b3d812f3827153a7c1fefd092fa`；835 个发布清单文件逐字节核对 | [远端回读](github-readback.json)、[发布清单](publication-manifest.json) |
| 本地看板 | 24 条记录，0 schema／来源错误；五课补充资料已接入，五课管理解释有效 | [最终检查](final-checks.json) |
| 线上看板 | 五课均发布成功，active_release 与 content_hash 独立回读一致 | [线上回读](online-board-readback.json)、[发布器回执](publisher-receipt.json) |

[本地看板](http://127.0.0.1:8766/) · [线上看板](https://cityu-board-online.vercel.app/) · [GitHub](https://github.com/CercaTrovato/cityu-ai-course-notes)。线上课程页面继续要求 GitHub 登录，本次侧栏未登录课程页；实际发布数据与附件完整性以授权发布接口的版本／内容哈希及服务端字节校验为据。

## 当前材料与版本

全库 59 个核心入口：41 v1.0、17 v0.9、1 draft。本批 8 个核心＋4 份学习参考，共 12 份导航维护；IS6400 M10 与 Sample Final 的局部深化另有独立审查。[当前版本链](current-version-manifest.json)保留原发布、导航维护及局部教学深化，旧报告按实际版本承接。原有 51 核心和本批 12 文档在本次收尾中均未改教学字节。

README 五课表和目录库存一致，readme_check 为 0；完整性检查为 0。link_check 的 6 项均位于未改的 2026-10-28 冻结候选，不改历史证据来刷绿。没有新增全库教学审查或冒称本人已学会。

## 五课线上版本

| 课程 | 发布版本 | 内容指纹前缀 | 附件数 |
|---|---|---|---:|
| AC6761 | `b50f0bd6-65e2-4447-934a-9f36cea3f66d` | `cd9807f50f43ff67` | 16 |
| IS6400 | `14b74e0c-da8b-48aa-a62f-bb2b17ab6ce6` | `1ab5a19597a442f7` | 250 |
| IS5113 | `a30446de-d0ba-4fd9-ad48-0879c847d05c` | `06921199a2e098fe` | 22 |
| IS5542 | `54ea288a-af36-4b4f-9e68-ba967ed9da3a` | `3429ba32bd34364e` | 36 |
| EF5560 | `a360ba64-eec4-4c79-9a13-6726361072f3` | `a86533e58bdf5998` | 16 |

四课以精确白名单增加补充 Markdown 资料；IS6400 既有索引已达 250 项，保留 250 个原附件并全部复用，本批从来源区链接已核 GitHub 资料。[容量处置](is6400-capacity-disposition.json)。未改容量、访问权限或线上代码，无需代码部署。

资料是课程学习补充，不计小组项目新交件或成员验收。A12 参考学习项 done，截止 2026-11-27 23:59 HKT，个人作答及提交仍 unknown；其余既有提交事实保持。旧 `board-metadata-preparation.json` 是写入阶段回执，当前版本以 final-checks 与线上回读为准。

## 保留的待补项

- IS5542 M07 金融讲义：录音先行 draft 不升级。
- IS6400 Sample Final 的 Q1.xlsx 与原始 Q4 BTC-USD.csv：未知数值不填，教学模拟数据不冒充 BTC 实测。

本次未提交课程作业、发送邮件或开启 Remotely Save 自动同步。原始课件只读，主工作区其他修改保持；Git 使用隔离分支正常提交与 fast-forward 推送，无 AI 署名、无 force push、无跳过 hooks。此回执记录已核内容提交，后续文档提交只保存三端结果，不为自身 SHA 无限追加提交。
