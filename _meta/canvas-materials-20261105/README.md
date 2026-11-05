---
type: Canvas材料与笔记增量
date: 2026-11-05
status: delivered-with-source-limitations
---

# Canvas 新材料归档与笔记增量 · 2026-11-05

> 2026-11-06 GitHub 发布范围见[发布说明](../publication/canvas-20261106.md)。下文“未提交／未推送”描述 11 月 5 日本地制作结束时的状态。

本地教学范围、课程同步及根共享索引已完成。Notion 本批13个唯一目标已由root写入并实际回读：5学习进度＋8DDL，6新建＋7既有更新；本次忠实rows回读学习53行、DDL65行，5科考试起止与用户来源/HKT零差异，个人字段及既有学习高状态/提交评分零变动。详 [notion-sync-final.json](notion-sync-final.json)。用户已确认电脑/手机 Remotely Save 自动同步关闭；本批无 Git 提交/推送、发邮件或上传作业。

## 原件与真实库存

12 份原件已归档并逐项 SHA-256 回读，旧版未替换；共享收尾重新核12项仍同hash。PDF共302页，DOCX元数据3+2页与AC作者实际5页视觉记录一致，两Excel工作表、Notebook86cell。源版本及路径见 [source-manifest.json](source-manifest.json)，共享实盘清单见 [inventory.json](shared-closeout/inventory.json)。

| 课程 | 本批原件 | 当前核心M/T入口 | 本批教学与维护范围 |
|---|---:|---:|---|
| AC6761 | 4 | 10 | Case6/Quiz3两学习解析全篇；M10两Excel附件§2.11局部；M09主体仅导航维护 |
| EF5560 | 3 | 9 | M09新54页笔记；A02新学习导览，依据现行3页brief与3页syllabus；行政新版要求 |
| IS5113 | 2 | 8 | M08新92页笔记；4页报告样稿只作A02格式/来源维护 |
| IS6400 | 3 | 18 | M09新版L10 137页全文跟读；T10新86-cell笔记及9页Colab PDF；旧98页L11只必要对照 |
| IS5542 | 0 | 6 | 无新Files/Modules文件；仅据用户考试快照维护日期，不扩M06反思或M07缺讲义范围 |

现有51核心入口=38 v1.0+12 v0.9+1既有draft/partial（IS5542 M07），转录TXT55个且本批无新增。本批新增3核心M/T，不把其余48全部说成本批新审。Case6、Quiz3、EF A02是另列的配套学习入口，不混入51。

## 教学、来源、显示与写回

四课共8个具体教学包：AC三包（其中M10局部）、EF两包、IS5113一包、IS6400两包。每包按其真实范围独立两阶段审查，实质缺陷一次批修/定向关闭；来源、重要计算、必要真实同源IAB显示、正式门槛及CAS原子写/精确字节回读分别留证。原生Obsidian本批未直接核；未沿用上批界面豁免。

- [AC6761结果](ac6761/course-result.json)：Case6/Quiz3仍draft，真实公司、年报、双工具输出未做；M10只核新增附件，不称全篇新审。机器原题契约未提供的限制保留，人源/独审已核。
- [EF5560结果](ef5560/course-result.json)：M09 54页/16原图、A02 6源页/3页英文全文/24名称URI；A02仍draft，24网站并未逐站核实时内容；旧大纲与历史来源保留。
- [IS5113结果](is5113/course-result.json)：M08 92页/14原图/2机制图/12组22回答分量；无本讲转录，部分历史/法域完整调查未做；样稿不替本组分配。
- [IS6400结果](is6400/course-result.json)：M09主源137页、T10 86cell；旧L11只核5留用原图和7个必要旧引页，未重看全98页；无TensorFlow安装/训练或付费调用。

M09/M08/T10新增讲义稿仍v0.9/pending，实际授课日和周次未核；笔记生成不等于本人已读、自测通过或作业完成。既有冻结审稿与换行字节映射分别保留，未为统一hash改历史报告。

## 行政、本地共享与远端同步

AC6761 PPT11/11前邮件（具体小时未给）、报告11/29前；EF5560 A02 11/29 12:00 HKT，只交含Zoom链接的PDF，TA2为12/6；IS5113报告12/1 12:00 HKT，样稿没有新截止/页数豁免。本批没有代发、代交或填写真实Worksheet。

五课期末日期已同步本地，来源 [exam-schedule-source.json](exam-schedule-source.json) 是用户计划所记11/5 12:56 AIMS已读快照，root本轮未重登；允许材料11/30起公布。本人出席、学习、复习、提交、评分均保持；旧11/2真实Submitted回执仅承接不新造。

根README当前全部库存/入口/待办/表/目录、术语总表四课增量、作业练习索引及各课本次术语队列由唯一共享收尾者串行CAS写回并回读，详 [shared-result.json](shared-closeout/shared-result.json)。课程已做各自完整性与链接核对；最终检查结果见 [checks-final.json](shared-closeout/checks-final.json)，此处不提前认证脚本结果或用户掌握。已有旧is07冻结candidate-v0六条表格别名问题未改历史。

## 保护与剩余边界

开工root自有完整性基线903个Markdown未被覆盖。所有旧课件、旧版本、原音与其他既有dirty改动保留。源文件公开仍须保留既有第三方隐私边界，不把本地归档等同已经GitHub发布。

本批按上述来源和真实范围交付；Notion最终回执已闭合，最终检查结果见 [checks-final.json](shared-closeout/checks-final.json)。Git保持未提交/未推送。没有新转录登记，不改根转录规则。

Notion旧备注的可见内容均保留；IS5113项目一处本地.md路径及本次触及的AC两材料路径改为原生inline code以避免工具误当域名，可见路径不变，不能声称所有序列化逐字符未动。新增 [Quiz3 Worksheet行](https://app.notion.com/p/40f8310b259681b1bc21dcdffca5170b) 只跟踪原件明确的邮件交付要求，类型其他，截止/分值未知、本人状态空缺；不视作新确认评分任务或已提交。既有PPT行未重复创建。

13个本批目标的完成不延伸为旧11/4待追加的16条备注全部补齐，也不填补IS5542 M07讲义或扩大M06旧Google反思范围。
