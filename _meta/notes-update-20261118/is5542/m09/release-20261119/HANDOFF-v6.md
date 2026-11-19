# M09 v6 最终准备包 · 未正式写回

- 候选：`candidate.md`，90,357 bytes。
- SHA-256：`a96bf9a2b4acdee09c4c8cde1b9e9d5f3d05fbdb3a8a041f67dbf77747ec5e47`。
- 正式拟定目标：`IS5542_GenAI_in_Business/notes/M09-AI法律问题-版权责任与客户资料.md`。准备时不存在。
- 9张图：`figures/m09/page-08.png`、15、18、26、31、37、39、58、61；字节与旧源渲染/原资产清单逐一一致。
- 源PDF：`course_files_export/canvas-20261118/IS5542-Guest Lecture6.pdf`，65页，SHA `1c1a107695d0236055ca898b801e0dcd459b207e84572d3e8abd3c88f2444ec0`。

## 最后两段维护

仅按root要求修§9.5首尾过时制造状态。中间重点待核法律段UTF-8字节与v5完全一致，其他v5教学/题面/数字/图义都不变。`maintenance-v5-v6.diff` 和 `maintenance-binding.json` 有实际比对，不假称独审者读过v6。

## 门槛与证据

最终 `note_release_gate.py --scope full --review review.json` 已实际执行，输出：机器门槛PASS、记录完整且版本一致。完整输出 `gate-output-final.txt`。这是准备阶段的真实工具结果，不是正式写回或同步完成。

当前 C.hard/R.hard均0，C.warn9/R.warn139；本轮每条实际警告及所在文字与v5逐一核对且保留具体处置。源题未由机器清单认证，原题全范围证据来自真正独立逐源审查。

root已另在精确v6 IAB实际核：9/9图、1Mermaid、7折叠、第五答案交互、§9.5修正句及法律限制，0断链/错误/横向溢出。原始/规范化HTML哈希及实际观察归属root，见 `root-final-display-v6.json`。

独立审查通过的是36818实质范围，经实际维护映射继承到当前候选；原阶段1/2/定向报告全部保留，未造新报告。v4 FAIL与v5 gate/history都留存。

## 未完成但不得夸大的部分

本包没有正式文件、图片、元文件、Notion或Git写入。root发布前应重读 `staging-manifest.json` 的目标基线，按CAS/原子写及精确回读执行。

全部现行法律/完整原判缺口仍按§9.5与 `scope-and-limits.json` 保留：香港现行合订法与生效注释/s33/TDM当前完整状态、Bartz批准全文、Uber刑事原件、Re A原判及引句、Tesla上诉终局、付费SAE全文等。它们不是“已核完”，本篇也不是当前法律意见。transcript仍pending/v0.9，原生Obsidian未直接查看，不改变本人学习/提交状态。

无剩余已知实质教学阻塞；接下来是root正式写回及各端同步，不应因此重做全篇独审。
