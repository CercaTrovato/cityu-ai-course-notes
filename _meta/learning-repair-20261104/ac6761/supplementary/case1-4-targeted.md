# AC6761 配套教学｜Case 1–4 定向复核

独立审查者 /root/ac6761_review。按 [阶段 1](case1-4-stage-1.md)、[独立回源报告](case1-4-independent.md) 和 [冻结绑定](targeted-candidate-bindings.json) 只核 C1-01、C1-02、C2-01、C4-01。四份候选和各自的基线实测 SHA-256 均与绑定一致。

| ID | 结果 | 最终候选 SHA-256 与证据 |
|---|---|---|
| C1-01 | 关闭 | M01 `a63bf78b43014bfa4b9f2f355e691032c8d7ce02ea28cf1e62334a6aa15bb8f7`。唯一差异是 SWIFT 读题入口，沿原题符号 `$`，标原件未给币种代码。阶段 2 原题和 After 数字均可承接。 |
| C1-02 | 关闭 | Case 1 `b6d353acefafa1fd85dbf72abd01a8661cc7240708e8d499ae658697b4ce8f8a`。§8 改成打开本地 Case 1 原件第 1 页，只读八笔英文，再从零做账；官解在后两页。相对链接按正式配套文档所在目录解码后，确指向已回核的 DOCX，实测原件 SHA `af790f648a4a0e11e76cb3a7428749f140a00be727c30fffc63a99350cd3bab4`。 |
| C2-01 | 关闭 | M02 `2a27c80df6cb5904ee5932a1f1bae5cd2e5d4f02c2b5a825124d44c5d89da9cc`。Case 2 英文余额答和试算总额沿原 `$`，表前说明原件未写币种代码；两处历史录音缺口描述的推定美元也已去掉。数值、原题与其他交易组未改。 |
| C4-01 | 关闭 | Case 4 `cf39764bc4585030a6d99978eb5de40629198bcf796d2df24cde546f0eee1911`。§6.1 已区分保留全部人员、数匹配编号、求和及补值。对正式 SQLite 同 SHA 文件用 mode=ro、immutable=1 再核，G/H/I 为 COUNT 0、裸 SUM NULL、COALESCE 0，F/J 各 2 笔共 500。工作簿同 SHA 的 Q4 C/D 列实核 COUNTIF 按收银员编号数收款行、SUMIF 按收银员汇总金额，缓存对五人依次为 2/500、0/0、0/0、0/0、2/500。正文限定表完整且确无收款才补零，工作簿及数据库未变。 |

Case 2、Case 3 配套正文仍与基线逐字节相同。四项全部关闭，其他证据承接阶段 2。此次只核本地差异、源码链接和现行附件，未操作原生 Excel、Obsidian 或外部系统。
