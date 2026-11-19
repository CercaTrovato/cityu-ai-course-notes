# Practice B · P1与结构定向修复

作者 `/root/cityu_review_probe`。原全篇独审 `/root/legal_stage_review` 的 stage-1.md / stage-2-combined.md 保留原字节。本轮不覆写旧candidate.md或原freeze/verification历史。

新候选 `candidate-v2.md` SHA-256：`3ad3cc324dbff2e2b04bb525e2d087014d86db8ee7a0bade19b029d5fcb1f68d`。

## 实质修复P1

B1(b)现为§2.7.2：绝对金额录错为原百万分之一；比例分子分母若同比缩小，比率相消不变；仅分子错、分母原单位时比率才缩小百万倍。英文原答一般性要求核单位/含义，无错误倍数断言，保持不变。题面、数值和其他选择项/小问未修改。

## 结构与纯显示修复

为让标准门槛实际读取正文，不再以standalone为由豁免：

- 标为practice-guide并加作业身份、可读性标准元数据。
- 原阅读说明置§1；原14页置§2，页级标题2.1–2.14，原逐题标题置相应下级标题，保留原A/B/C编号。
- 原复习索引、自测、核对边界分别归§4/7/9。
- 增加§0速览、§3四层证据表、§5词表、§6英文作答框架、§8页级精确映射，全部是已有解释的导航/回忆；不增加官方答案或现行产品事实。
- A6的CAPM公式/符号解释，以及B1(b)的检查/金额例/后果，按原语序分段，降低单段公式或列表长度；除P1外不改原回答措辞。

完整精确diff为candidate-v1-to-v2.diff，类别及旧/新哈希为revision-v2.json。新布局有新增回忆内容，已请原独审定向核其含义与保留关系，不把整份布局都声称只是空白变更。

## 真实核对结果

verify-v2.py确认：14个text原题全文块与原稿逐字相同；14个嵌图路径不变；28个English reference仍在。源PDF和64选项的原全篇独审证据不变。

本轮current checker实际exit0，L=0、C.hard=0、R.hard=0；C.warn20、R.warn108原样保存mechanical-v2.txt和mechanical-v2-summary.json。没有用zero hard证明教学或最终显示通过。C提示主要含原页/子单元层级及行政/草稿页，真实解释在其后子题；完整疑点仍留给复核，不抹除。无机器源题清单契约PASS；原题保真靠14原文块相等、源图与既有独立逐源检查，不伪造机器未做的认证。

新同源预览：`http://127.0.0.1:8796/ef5560-practice-b-dot-v2/`，22数学节点、3 Mermaid、14原页图。此为源码预览生成，不是实际最终UI已看。原始binding为LF内存哈希，Windows写盘CRLF的差异应按原方法同时绑定，不能只照抄旧HTML哈希。

已把新候选及精确diff交原审查者定向复核。独审定向结果与最终UI尚未在本作者报告中自行标通过。仅scratch修改，正式库/个人学习/提交/评分字段未改。
