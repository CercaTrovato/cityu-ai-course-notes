# IS6400 T02 两处残留关闭记录

审查者 `/root/is6400_t01_t02_review`。复核 `t02-residual-closed-candidate.md`，SHA-256 `de6f010a466c41085e82e544c217dee2c3532e0319a055d89e61356e16af373a`。比较 `t02-second-frozen.md`，SHA-256 `04328d2eeac3147a5b719339c01ba427e6c3e4ed4e0649b9ad19fe04c40029a3`。两版各 2,658 行。按原始字节逐行对照，仅第 743、744、2052、2054、2057 行变化。

**两处残留已关闭。**

- §3.1 现说明列尺度差与强相关可能使求解敏感，并指向 §3.4 的多因素诊断。原 Notebook 第 22 格的保存警告确实列出 `linalg.solve(A, Xy, assume_a="pos", overwrite_a=True)`。新版表述与原输出及 §3.5 的精确求解限定一致。
- §7.4 的总领、表头和 solver 行已限定为所供教程片段。原 Summary 中 `Ridge(alpha=1, solver="cholesky")` 仍保留，课堂 alpha 原话和转录尾部限制未变。新版不再从片段未见推断整堂课没讲。

其他行完全一致，承接 `t02-independent-review.md`、`t02-targeted-recheck.md` 和 `t02-targeted-recheck-2.md` 的原代码、五张源图、原题和复算证据。独立审查的教学缺陷已关闭。正式 Obsidian 显示仍待核验。
