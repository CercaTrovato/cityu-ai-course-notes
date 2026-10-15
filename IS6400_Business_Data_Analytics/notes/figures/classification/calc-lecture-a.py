import json
import math
from pathlib import Path


def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))


out = {}

# Lecture p.28: 25 independent classifiers, each with error 0.35.
eps = 0.35
out["p28_majority_error"] = sum(
    math.comb(25, i) * eps**i * (1 - eps) ** (25 - i)
    for i in range(13, 26)
)

# Lecture p.18: root (3 Yes, 7 No) and Home Owner split.
def gini(counts):
    total = sum(counts)
    return 1 - sum((count / total) ** 2 for count in counts) if total else 0.0


def entropy(counts):
    total = sum(counts)
    return -sum((count / total) * math.log2(count / total) for count in counts if count) if total else 0.0


root_counts = [3, 7]
owner_yes = [0, 3]
owner_no = [3, 4]
weighted_gini = 3 / 10 * gini(owner_yes) + 7 / 10 * gini(owner_no)
weighted_entropy = 3 / 10 * entropy(owner_yes) + 7 / 10 * entropy(owner_no)
out["p18_home_owner_split"] = {
    "root_gini": gini(root_counts),
    "weighted_child_gini": weighted_gini,
    "gini_gain": gini(root_counts) - weighted_gini,
    "root_entropy_bits": entropy(root_counts),
    "weighted_child_entropy_bits": weighted_entropy,
    "information_gain_bits": entropy(root_counts) - weighted_entropy,
}

# Lecture p.37-p.39: ten stump outputs on the original x grid.
xs = [i / 10 for i in range(1, 11)]
stumps = [
    (0.35, 1, -1),
    (0.70, 1, 1),
    (0.35, 1, -1),
    (0.30, 1, -1),
    (0.35, 1, -1),
    (0.75, -1, 1),
    (0.75, -1, 1),
    (0.75, -1, 1),
    (0.75, -1, 1),
    (0.05, 1, 1),
]
votes = [[left if x <= k else right for x in xs] for k, left, right in stumps]
vote_sums = [sum(row[j] for row in votes) for j in range(len(xs))]
pred = [1 if value > 0 else -1 if value < 0 else 0 for value in vote_sums]
original_y = [1, 1, 1, -1, -1, -1, -1, 1, 1, 1]
out["p39"] = {
    "x_0_9_votes": [row[8] for row in votes],
    "x_0_9_sum": vote_sums[8],
    "x_0_9_prediction": pred[8],
    "all_vote_sums": vote_sums,
    "all_predictions": pred,
    "matches_original_grid": pred == original_y,
}

# Lecture p.47 weighted vote, using the three displayed alpha values.
slide_alpha = [1.738, 2.7784, 4.1195]
slide_predictions = [
    [-1] * 7 + [1] * 3,
    [1] * 10,
    [1] * 3 + [-1] * 7,
]
slide_scores = [
    sum(slide_alpha[t] * slide_predictions[t][j] for t in range(3))
    for j in range(10)
]
out["p47_weighted_vote"] = slide_scores

# Supplementary, exact three-round AdaBoost example.
y = [-1, -1, 1, 1]
h = [
    [-1, -1, 1, -1],
    [-1, 1, 1, 1],
    [-1, -1, -1, 1],
]
w = [0.25] * 4
ada_rounds = []
alphas = []
for t, ht in enumerate(h, start=1):
    error = sum(wi for wi, yi, hi in zip(w, y, ht) if yi != hi)
    alpha = 0.5 * math.log((1 - error) / error)
    raw = [wi * math.exp(-alpha * yi * hi) for wi, yi, hi in zip(w, y, ht)]
    z = sum(raw)
    new_w = [value / z for value in raw]
    alphas.append(alpha)
    scores = [sum(alphas[k] * h[k][j] for k in range(t)) for j in range(4)]
    ada_rounds.append({
        "round": t,
        "weights_before": w,
        "error": error,
        "alpha": alpha,
        "normalizer": z,
        "weights_after": new_w,
        "ensemble_scores": scores,
    })
    w = new_w
out["supplementary_adaboost"] = {
    "y": y,
    "base_predictions": h,
    "rounds": ada_rounds,
    "final_prediction": [1 if s > 0 else -1 for s in ada_rounds[-1]["ensemble_scores"]],
}

# Lecture p.53 stacking inference and the A-logit typo check.
stack_inputs = {
    "A": (0.25, 0.10),
    "B": (0.70, 0.85),
    "C": (0.60, 0.80),
}
stack = {}
for name, (lr, tree) in stack_inputs.items():
    logit = -4 + 3 * lr + 2 * tree
    stack[name] = {"logit": logit, "probability": sigmoid(logit), "prediction_at_0_5": int(sigmoid(logit) >= 0.5)}
out["p53_stacking"] = stack
out["p53_a_table_logit_minus_0_35_probability"] = sigmoid(-0.35)

target = Path(__file__).with_name("results.json")
target.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
