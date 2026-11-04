## Notebook cell 25

# Q1. Five classifiers and their performance

## Data and comparison setup

I use `creditcard-reduced.csv`, with `Class` as the target and the other 30 columns as predictors. Class 1 is the minority class. I remove records that match in all columns before splitting, then use a stratified 60% training / 40% test split with `random_state=42`.

All five classifiers use the same training rows, test rows and predictors. Logistic regression uses a scaler fitted within its training pipeline. The tree models use the supplied numeric features directly.

## Cell 26 output

Python 3.12.3 ; pandas 2.3.3 ; scikit-learn 1.5.1
Original rows: 32764 ; identical records removed: 177 ; retained: 32587
Predictors: 30 ; missing cells: 0


## Cell 26 table


 All Train Test 
 Class 
 0 32114 19268 12846 
 1 473 284 189

## Cell 26 output

Positive-class share: 1.451499%


## Notebook cell 27

## Metrics

The confusion matrices use actual classes as rows and predicted classes as columns, in the order 0, 1. A true positive (TP) is a class-1 record predicted as 1. A false negative (FN) is a class-1 record predicted as 0. False positives (FP) are class-0 records predicted as 1; true negatives (TN) are class-0 records predicted as 0.

I report accuracy and the class-1 precision, recall and F1-score:

$$
\mathrm{Accuracy}=\frac{TP+TN}{TP+TN+FP+FN},\qquad
\mathrm{Precision}=\frac{TP}{TP+FP}.
$$

$$
\mathrm{Recall}=\frac{TP}{TP+FN},\qquad
F_1=\frac{2\,\mathrm{Precision}\,\mathrm{Recall}}{\mathrm{Precision}+\mathrm{Recall}}.
$$

For example, TP=8, FP=2 and FN=4 give precision $8/10=0.8$, recall $8/12\approx0.666667$ and F1 $16/22\approx0.727273$. Accuracy counts all correct predictions; precision and recall describe different errors on the positive class.

## Cell 28 table


 Accuracy Precision Recall F1 
 Model 
 Logistic regression 0.999386 0.989189 0.968254 0.978610 
 Decision tree 0.999540 0.974093 0.994709 0.984293 
 Random forest 0.999540 0.984127 0.984127 0.984127 
 Bagging 0.999616 0.979167 0.994709 0.986877 
 AdaBoost 0.999770 0.989474 0.994709 0.992084

## Cell 28 table


 TN FP FN TP 
 Model 
 Logistic regression 12844 2 6 183 
 Decision tree 12841 5 1 188 
 Random forest 12843 3 3 186 
 Bagging 12842 4 1 188 
 AdaBoost 12844 2 1 188

## Notebook cell 29

# Q2. Differences between the classifiers

Logistic regression fits a linear boundary after scaling the inputs. The decision tree splits individual features into regions; I limit it to depth 5 with at least 5 training records per leaf. Random forest averages 200 trees fitted with bootstrap samples and random feature subsets. Bagging averages 100 depth-5 trees fitted to bootstrap samples. AdaBoost fits 100 small depth-2 trees sequentially, giving more influence to previously misclassified training records; I use SAMME with a learning rate of 0.5.

The models therefore differ in the boundaries they can fit and how they combine trees. A single tree is easy to follow but depends on its chosen splits. Forest and bagging average several fitted trees. AdaBoost adjusts the training emphasis at each stage, while logistic regression estimates one set of coefficients.

## Cell 30 result

AdaBoost has the highest test F1-score, 0.992084, with precision 0.989474 and recall 0.994709. It detects 188 of the 189 positive records and produces 2 false positives. The highest recall, 0.994709, is shared by Decision tree, Bagging, AdaBoost; while AdaBoost has the highest precision (0.989474).

## Cell 30 result

Predicting every record as class 0 gives accuracy 0.985501, but recall and F1 are both 0.000000 because every positive record is missed. The confusion matrices and positive-class metrics are therefore more informative than accuracy alone. For a balance between positive detections and false alarms in this comparison, I would choose AdaBoost.

## Notebook cell 31

# Q3. Classification with and without class weights

I compare two depth-5 decision trees with the same minimum leaf size, random seed, predictors and data split. The second tree gives class 1 more weight. I calculate the weight from training counts:

$$
w_0=1,\qquad w_1=\frac{n_0}{n_1},
$$

where $n_0$ and $n_1$ count the class-0 and class-1 training records. This gives the two classes equal total weight when choosing splits. The weights change the fitting criterion rather than adding records or changing their labels.

## Cell 32 output

Training class weights: class 0 = 1.000000; class 1 = 67.845070


## Cell 32 table


 Accuracy Precision Recall F1 
 Model 
 Without class weights 0.999540 0.974093 0.994709 0.984293 
 With class weights 0.999386 0.964103 0.994709 0.979167

## Cell 32 table


 TN FP FN TP 
 Model 
 Without class weights 12841 5 1 188 
 With class weights 12839 7 1 188

## Cell 33 result

Both trees detect 188 of the 189 positive records, giving recall 0.994709. Weighting changes precision from 0.974093 to 0.964103, and F1 from 0.984293 to 0.979167. False positives increase from 5 to 7, while each tree misses 1 positive record. The higher class-1 training weight changes which splits the tree selects.

## Notebook cell 34

## Additional analysis: the cost of the two error types

The preferred class-weight setting depends on the relative cost of a false positive and a missed positive. To compare the observed counts, let one false positive cost one unit and one false negative cost $r$ units:

$$
\mathrm{Cost}(r)=FP+r\,FN.
$$

The table uses assumed ratios $r=1,10,50,100$; these are scenarios, not measured business costs. For example, FP=10 and FN=3 give $10+10\times3=40$ units when $r=10$.

## Cell 35 table


 FN/FP cost ratio Without weights With weights 
 1 6 8 
 10 15 17 
 50 55 57 
 100 105 107

## Cell 35 result

Both trees miss 1 positive record. Weighting increases false positives from 5 to 7, so its error cost is 2 units higher at every listed ratio. I would keep the unweighted tree for this split.

## Notebook cell 36

## Training-data check: the role of Time

The training classes occupy different ranges of `Time`. I examine this using a separate stratified 70%/30% split of the training rows and a fixed depth-5 tree using only `Time`. This check leaves the outer test set and the five-model comparison unchanged.

## Cell 37 table


 min max median count 
 Class 
 0 155839 172792 163279.500000 19268 
 1 406 170348 70249.500000 284

## Cell 37 output

Internal validation confusion matrix (Time only):
[[5781    0]
 [   7   78]]
Internal validation F1 (Time only): 0.957055
Fitted Q1 tree importance assigned to Time: 0.954175


## Cell 37 result

Class 0 training records have Time values from 155839 to 172792, while class 1 ranges from 406 to 170348. A tree using Time alone reaches internal validation F1 0.957055. Time also accounts for 95.417488% of the Q1 tree's fitted impurity reduction. The high random-split scores partly reflect this strong class separation within the supplied sample. They should be read as a comparison on that sample rather than as a forecast of later records.

## Notebook cell 38

## Sources

IS6400, “Week 7 Classification_Tutorial.ipynb,” assignment Questions 1–3; supplied `creditcard-reduced.csv`. The model implementations are from scikit-learn; their settings are shown in the code.

I used OpenAI Codex to assist with this assignment.