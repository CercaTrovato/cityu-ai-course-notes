# Author handoff: IS6400 Sample Final

Author: `/root/is6400_sample_author`.

This is the author's one consolidated self-check, not independent teaching review. Candidate frozen SHA-256: `fd09c3685802b2f7dde0e4a41a91d09f441fe99f25db7db5a3a1676582afaf1f`.

## Scope and source

- 9 subquestions: Q1(1–2), Problem 3(1–4), Q5(1–3).
- Read the actual archived DOCX XML in addition to parent `source.md`. Actual source has one native date/forecast table, three PNG media members, and no embedded workbook/CSV.
- Opened each of the three PNGs with `view_image`; manually verified each A/B/C/D/positive/negative table entry, branch and label. `freeze_evidence.py` also checks extracted media bytes against the DOCX members.
- `source-text-compare.json`: every nontrivial DOCX paragraph, including OMML text, appears in candidate under alphanumeric normalization. Unmatched paragraphs: 0. This check cannot replace the manual reading of notation, enumeration and images.
- Retained original English question words and (a)/(b), all 9 subparts, 6 variable definitions, five forecast dates, source figure/table captions including conflicting image captions. Source spelling `foresting` and numbering defects are disclosed rather than silently repaired.

## Main decisions and checks

- Missing Churn count is not guessed. Deletion and mode imputation are explained with their limitations for a target label. Unknown category and recovering actual labels are distinguished from made-up supervised labels.
- IQR uses all valid numeric LastTransaction observations irrespective of Churn presence. Convention explicitly fixed to linear / QUARTILE.INC. Both odd- and even-length deterministic teaching examples checked by hand.
- Source training and validation denominators both 15, not 6 table rows. Original training error 0/15; leaf penalty 6/15; validation 7/15.
- All 9 majority-class pruning subtrees calculated. Recursive independent enumeration of an explicit tuple tree agrees with the separate if/else reproduction code, and with the earlier manual result file. A complete row-contribution table supports every model.
- Leaf penalty fixed to source's 1, not a generic textbook's 0.5. Pessimistic ties are not presented as uniquely selecting the validation-best tree.
- Root-at-depth-zero versus source level-one is disclosed for the 8-layers parameter. No empirical training accuracy is claimed from just constructing a classifier.
- Price difference versus percentage return distinguished. AR(1) with intercept is an explicitly chosen reference specification, not official/best-order inference. Recursive five-step differences are cumulatively restored to prices.
- Q5(3) defines a full, temporally ordered expanding-window method and 365 shared daily targets, with pre-specified candidates, naive baseline, MAE primary/RMSE secondary, true-price scoring, and limits of validation-based model selection.
- Code reads only original required files. Missing-data runs both exit 2 with a truthful message. No artificial, alternative-site, random or other-period price dataset has been substituted. Therefore no data-dependent Q1 numbers, five BTC prices, p-values, fitted coefficients or fake results screenshot are present.

## Mechanical checks and warning disposition

`quality-current.txt`: current / strict / sections / readability PASS; L hard 0, C hard 0, R hard 0. Source manifest not supplied to that script, therefore it truthfully says `unverified_without_manifest`; manual 9-item coverage is in candidate §8 and the source comparison is separate.

R warnings total 78. Locations are preserved in the tool log. Group disposition for independent semantic review:

- R8a (14): DOCX has no stable rendered source page identifiers in this author workflow. Candidate uses original question/subquestion and source-image references instead, expressly stated in §8. Do not invent PDF page numbers.
- R4a (2): the two transcribed original tables retain row ID, four binary features and two class counts (7 columns). Original images are also present. These are short numeric cells, not 7 prose columns; final display must still be checked.
- R4c (14), R1c (5), R2b (5), R3a (1): short compound cells/list explanations. Main objects and meanings are spelled out beside the tables and named sequence. These are warning candidates, not machine-verified teaching sufficiency.
- R4f (13): A/B/C/D input roles and lack of business semantics explained in §2.2.1; table IDs T/V explained there. Error denominators/formulas defined before summary table; row-contribution sequence order defined immediately before its table. Native Trading date/Forecast table is identified in a new adjacent reading sentence.
- R6b (3), R6d (14), R6a (1): several hits are source labels and IDs. L0–L3/R0–R1 are exhaustively defined before model comparison; T/V and A0/B1 defined before trace tables. AR/MAE/RMSE have adjacent Chinese/full-English definitions. Word-format and date-format abbreviations are incidental; no hidden algorithm step depends on knowing their expansion.
- R1e (3): necessary distinctions include row versus instance count, label versus amount, difference versus return, depth versus layers. These affect the answer rather than merely adding defensive prose.
- R5a (1), R5b (2): paired recursive expressions and the fully worked teaching example share one derivation; symbol purposes and changed quantities are explicit. Final formula readability remains to be actually viewed.

`link-check.txt`: 0 problems, scans 1 candidate markdown. This script checks vault-style links, not Markdown image existence. Media existence and byte identity are separately asserted in `freeze_evidence.py`.

## Explicit remaining gates

1. Independent novice-perspective review has not been performed by the author. Parent must arrange it without presenting this author score summary in stage 1.
2. Final rendered candidate (especially formulas, 7-column numeric tables and source image sizes) has not been visually inspected by this author. Actual source images have been inspected; these are different claims.
3. Missing Q1.xlsx and Q4 BTC-USD.csv block only the real data-dependent outputs. Rechecked local known source/user-document roots with no matching files. Unchecked cloud/current Canvas availability remains unknown.
4. Current Canvas four-entry status and official solutions were not checked by this author. No claim that an official answer has not been published.
5. Only new `dot-author` scratch files written. No formal vault, original source, Git, dashboard, submission, or user message change.
