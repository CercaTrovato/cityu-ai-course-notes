# M04 逐源题面核对

## 旧 p.26 → §2.3.6

**Short-Answer Question: Is This Threshold Investable?**

A tree splits at inflation = 2.5%. Pre-test diagnostics:

| Diagnostic | Evidence |
|---|---|
| Leaf support | Only four months support the high-inflation leaf. |
| Leaf-size sensitivity | Minimum leaf size 12 removes the split. |
| Time stability | A later pre-test refit gives a different split. |

1. Identify two warning signs in the diagnostics.
2. Explain whether the threshold is credible enough to guide a financial decision.
3. Propose one additional validation check without looking at the frozen test.

Interpretability alone does not establish a stable regime.

原文、全部选项、中文逐问、英文参考答案已对照 PDF 全页核验；无官方标准答案者保留笔记参考地位。

## 旧 p.27 → §2.3.6

**Multiple-Choice Question: Reading a Regression Tree**

Suppose a fitted tree uses the following weekly forecasting rule:

| Condition | Forecast return |
|---|---:|
| Volatility > 2% | −0.8% |
| Volatility ≤ 2%, momentum > 0 | +0.6% |
| Volatility ≤ 2%, momentum ≤ 0 | −0.2% |

A stock has volatility 1.5% and momentum −0.4%. What is its forecast?

A) −0.8%  
B) −0.4%  
C) −0.2%  
D) +0.6%

原文、全部选项、中文逐问、英文参考答案已对照 PDF 全页核验；无官方标准答案者保留笔记参考地位。

## 旧 p.28 → §2.3.6

**Multiple-Choice Question: Why Randomize Predictor Selection?**

An analyst averages many trees fitted to bootstrap samples. Nearly every tree uses the same dominant predictor for its first split, and their forecast errors are strongly correlated. Why might random predictor subsets improve the ensemble?

A) They ensure that each individual tree has a lower training error.  
B) They can reduce correlation among tree forecasts, making averaging more effective.  
C) They ensure that the strongest predictor appears at the root of every tree.  
D) They remove the need to choose complexity on validation data.

原文、全部选项、中文逐问、英文参考答案已对照 PDF 全页核验；无官方标准答案者保留笔记参考地位。

## 旧 p.35 → §2.4.5

**Short-Answer Question: How Should We Split a Stock Panel?**

An analyst has 30 stocks observed over 156 weeks: 4,680 stock-week rows. She randomly splits the rows into training and test sets, then argues that the large sample justifies a large neural network.

1. Why do 4,680 rows not represent 4,680 independent market episodes?
2. Why is this random split unsuitable for evaluating forecasts of future returns?
3. Describe a better sample split and how you would choose the network size.

原文、全部选项、中文逐问、英文参考答案已对照 PDF 全页核验；无官方标准答案者保留笔记参考地位。

## 旧 p.46 → §2.6.4

**Multiple-Choice Question: Which Nonlinear Model Was Selected?**

Three models are tuned before the frozen test period. Their mean squared errors are:

| Model | Validation MSE | Test MSE |
|---|---:|---:|
| Shallow tree | 0.0024 | 0.0019 |
| Random forest | 0.0021 | 0.0023 |
| Boosting | 0.0022 | 0.0018 |

Which model should be reported as the preselected evaluation model?

A. Shallow tree, because it has the lowest test MSE among the trees.  
B. Random forest, because it has the lowest validation MSE.  
C. Boosting, because it has the lowest test MSE.  
D. Average the tree and boosting after observing the test results.  

**Discuss:** Separate model selection from final evaluation. Why cannot the test-period winner replace the model frozen after validation?

原文、全部选项、中文逐问、英文参考答案已对照 PDF 全页核验；无官方标准答案者保留笔记参考地位。

## 旧 p.53 → §2.7.5

**Short-Answer Question: Forecast Accuracy and Stock Ranking**

Suppose a stock excess-return model has a test OOS $R^2$ of −1% against a zero forecast. Its top-minus-bottom portfolio has a mean weekly return of +0.08% before costs over the same test period.

1. Explain how negative OOS $R^2$ and a positive mean portfolio return can coexist.
2. Is the positive mean return enough to recommend investing? Give two additional checks and explain what each would tell you.

原文、全部选项、中文逐问、英文参考答案已对照 PDF 全页核验；无官方标准答案者保留笔记参考地位。

新版 p.28、p.48 保留问句，分别对应旧 p.26、p.46；新版 p.29、p.30、p.38、p.55 是给定演示或说明，不编新教授问句。
