# M12 最终文字定向核查

日期：2026-11-28。审查者 `/root/independent_fusion_review`；作者/合并者 `/root`、`/root/m12_fusion_author`。本次仅核最终两篇中的M12一处引入词，不重开全篇，不改候选。

承接报告 `m12-independent-review.md`（SHA256 `97a5cbdb9b315f1c5e3d3f9f6fcb440156e1ecf0ef397abb818012c922b3be25`）及原stage-1，均保留。原候选SHA256 `365c481e9bdc9604d74f8d94e6ef1ca74e83ee138054d2865760ecc964bd5f7a`。

最终候选 `../m12/merged.md` 实际SHA256 `991e1632e4bcf6ed1ca73ef682acbfb0b2c16d65800b033ef46b00797120971b`。

实际查看 `../final-wording-fixes.md`、候选p38课堂块及上下文（候选第705行）：将“教授把‘抽取数字’扩为‘读懂条件’，问”中的引入词改为“说明”。该改动关闭原报告非阻塞措辞建议：LLM is not only for extracting news在已核S35 02:01:09是陈述，后面才问资格/银行资金可得。英文引文、时间戳、两问参考地位、限定词和答案不变。

用只读逆替换核实：将最终字节中该新引入词唯一一次替回旧词，得到的SHA256与原独审候选完全一致；无其他字节变化。执行结果保存于 `final-wording-hash-mapping.json`，脚本 `check_final_wording.py`。不是仅接受作者自述或只更新哈希。

本处无需重跑教学样本/源图，无新增阻塞；原抽检结论及全部未抽/显示限制可映射到上述最终候选。供最终note-review-v2连同原独审报告、stage-1及本定向核查绑定。不得据此宣称全篇独审或最终发布/同步完成。
