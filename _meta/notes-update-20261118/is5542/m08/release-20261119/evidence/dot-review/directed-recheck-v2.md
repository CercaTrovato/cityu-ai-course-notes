# M08 Directed Recheck v2

Reviewer: `/root/cityu_review_probe`, original independent reviewer; no participation in candidate authoring or editing.

Frozen candidate: `E:/app-data/codex/scratchpad/cityu-notes-20261118/is5542/m08/dot-author/candidate-v2.md`

Verified SHA-256: `b39dba598a7ea1ff89476ca660f03755273b4ef30faaaf1104d7dba08bee9332`.

## Scope and evidence

Read m08-directed-fix.diff and actual frozen §2.17, §2.18, §7.5. This is the requested targeted closure, not another full review. Stage 1 and Stage 2 reports remain unchanged and applicable to unchanged material under their stated limits.

## S1-01: CLOSED

§2.17 now explicitly distinguishes diagnostic/development tasks from tasks excluded from all improvement decisions. It states that consulting diagnostic results to choose data/training changes makes those tasks part of development even when their answers never directly enter training. The loop node D now says diagnostic evaluation rather than independent held-out evaluation. Passing the diagnostic threshold leads to fixing the solution, then checking on unused tasks, then reporting results/boundaries. It also states that changing the solution after inspecting final results removes the same set's final-independent status.

Retried the original counterexample: first inspect a same-name-channel error in D, change training samples, and evaluate again on D. Under revised text this is legitimate diagnosis but not independent final evidence; final evidence must come from the separate F step. Thus the prior wrong conclusion is no longer supported.

§7.5 agrees exactly: continue using known tasks diagnostically but retain separate tasks untouched by decisions. §2.18 still gives a conditional interpretation of recursive and requires independent checking; its following paragraph explicitly requires materials not used for improvement decisions. Read alongside the clarified §2.17, this does not instruct reuse of the diagnostic set as independent evidence. Its general wording need not be expanded into a new experiment-design lesson.

The fix remains labelled supplemental, with source p.17 restricted to Data/Train/Eval. No new claim about actual yes&/ByteDance training procedures or performance is introduced.

## Status

**Independent semantic/learning blocker S1-01 closed for the verified v2 hash.** The earlier independent report's pending targeted-correction status is superseded on this item by this dated-version closure; original observations are preserved. No other substantive blocker was identified in the prior full review.

Final rendered note UI, Mermaid display and actual link operation were not examined in this directed check. This report does not grant final UI/visual-publication approval, does not verify writeback/sync, and does not assert user learning.

Only this new report was written. Candidate and vault were not changed.
