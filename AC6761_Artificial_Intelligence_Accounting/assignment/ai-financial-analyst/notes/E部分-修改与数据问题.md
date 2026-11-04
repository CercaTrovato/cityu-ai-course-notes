# E 部分修改与数据问题 · 2026-10-25

当前任务由用户明确：以 PPT 为主，先把本人负责的 E 部分改清楚；发现数据问题及时提出。报告正文是否收到不阻塞本次 PPT 修改。

## 最新文件

[E 部分修订稿](../work/section-e/output.pptx) 是独立的五页文件，页脚对应总稿第 18–22 页。英文页面，保留演讲者备注及中文排练提示；英文讲稿约 621 词，文本估计加停顿约 6 分钟，未实际朗读计时。尚未合并到 24 页总稿或在线 PPT，也没有更改其他组员的页面。

第 18 页将全部三种情境放进同一张表，解释 annual sustainable EPS 和 P/E；第 19 页对照两家 HOLD 的不同理由；第 20 页把 AI 辅助步骤和团队判断分开；第 21 页将错误风险与核对办法配对；第 22 页总结公司质量与买入价格是两个问题。

## 需要向组员提出的显示问题

原稿第 8 页：`US$141.1m + US$327.5m = US$468.5m`。按照页面上的一位小数相加应为 468.6，因此展示等式不一致。

已从 Celsius FY2025 官方业绩公告回源：经营利润 141,062，渠道终止费用 327,461，原表单位均为 US$ thousand。换成百万后，141.062 + 327.461 = 468.523，保留一位小数为 468.5。因此底层加总正确，是舍入显示问题，不应将它报告成财务数据错误。

建议负责该页的组员将文字改为 “US$468.5m after adding back the termination fee, calculated using unrounded inputs”，或展示更多位数的输入。此处只是待团队采用的改法，本轮没有修改第 8 页，也没有向群里发送消息。

来源：[Celsius FY2025 官方业绩公告](https://ir.celsiusholdingsinc.com/news/news-details/2026/Celsius-Holdings-Reports-Full-Year-2025-and-Fourth-Quarter-Financial-Results/default.aspx)，2026-10-25 浏览器现场读取财务表。

## 本轮已核的 E 部分关键口径

- Monster 2025 年报 diluted EPS 为 US$1.94；[2026 Q2 官方公告](https://investors.monsterbevcorp.com/news-releases/news-release-details/monster-beverage-reports-2026-second-quarter-financial-results) 的 Stock Split 段确认二拆一，派发计划为 2026-08-10 收盘后、预计 8 月 11 日按拆股价交易。换算 EPS 为 US$0.97，不再减半。
- [Monster 历史行情](https://stockanalysis.com/stocks/mnst/history/)及 [Celsius 历史行情](https://stockanalysis.com/stocks/celh/history/)的 2026-10-19 收盘参考价分别为 US$46.80 和 US$29.72，与原稿一致；没有把它们称为实时股价。
- Celsius FY2025 官方业绩公告列示 GAAP diluted EPS US$0.25 与 adjusted diluted EPS US$1.34，保留两种口径。情境中的 US$1.20 是未验证的团队持续盈利假设，不是公司预测、GAAP 调节表或已实现恢复。
- 六组 EPS × P/E 乘法正确；中心情境相对上述参考价的差额分别为 −5.9829% 和 +0.9421%，页面展示 −6.0% 和 +0.9%。这些不是保证投资回报率。

40 倍、25 倍等精确估值倍数尚无独立模型验证；用更强已报告利润率和现金创造能力解释 Monster 较高倍数，只能支持团队相对判断，不能证明精确数值正确。两家 HOLD 仍为可讨论的条件评级。

## AI 说明与审查边界

AI 历史操作以 “described/reported in the group draft” 归因。具体工具名、Hayward 误源过程、原始计算程序及日志仍须与初稿作者确认，没有冒称用户本人执行全部检查。其他组员的完整财务比率不在本轮全面审计范围。

独立审查由未参与撰写的 gpt-6.1-sol 子代理完成，先读候选；修复一个术语解释断点后做定向复核，内容问题已关闭。主代理实际查看五页初次渲染图，并重新查看有改动的第 18 页；未见溢出、遮挡或缺字。该内容/视觉检查不等于团队确认或可提交。

原始群 PPT 和年报保持字节不变；本轮没有写入在线 PPT、提交作业、发送消息或 Git 提交/推送。完整性检查以最后回执为准。

返回 [工作区首页](../README.md)。
