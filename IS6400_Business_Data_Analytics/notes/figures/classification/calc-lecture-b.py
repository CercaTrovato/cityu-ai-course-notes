import json
import math
from pathlib import Path
from scipy.optimize import minimize

root = Path(__file__).resolve().parent


def metrics(tp, fn, fp, tn):
    accuracy = (tp + tn) / (tp + fn + fp + tn)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "tp": tp,
        "fn": fn,
        "fp": fp,
        "tn": tn,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def soft_svm_objective(w, b, xs, ys, c):
    slacks = [max(0.0, 1.0 - y * (w * x + b)) for x, y in zip(xs, ys)]
    return 0.5 * w * w + c * sum(slacks), slacks


lecture_cost = {
    "M1": -1 * 150 + 100 * 40 + 1 * 60 + 0 * 250,
    "M2": -1 * 250 + 100 * 45 + 1 * 5 + 0 * 200,
}

lecture_cost_audit = {
    "M1_actual_positive": 150 + 40,
    "M1_actual_negative": 60 + 250,
    "M2_actual_positive": 250 + 45,
    "M2_actual_negative": 5 + 200,
    "same_actual_class_distribution": False,
    "comparison_note": "The two matrices do not describe the same true-class distribution, so their model quality is not directly comparable.",
}

q_threshold = 1 / 102

hard_margin = {
    "points": [[-2, -1], [-1, -1], [1, 1], [2, 1]],
    "w": 1,
    "b": 0,
    "functional_margins": [2, 1, 1, 2],
    "full_margin": 2,
}

soft_points_x = [-2, -1, 1, 2, 1]
soft_points_y = [-1, -1, 1, 1, -1]
soft_candidates = {}
soft_optima = {}
for c in [0.1, 1.0, 10.0]:
    rows = []
    for w, b in [(1.0, 0.0), (0.8, -0.4), (0.0, -1.0)]:
        objective, slacks = soft_svm_objective(w, b, soft_points_x, soft_points_y, c)
        rows.append({"w": w, "b": b, "objective": objective, "slacks": slacks})
    soft_candidates[str(c)] = rows
    def objective(v):
        return 0.5 * v[0] * v[0] + c * sum(v[2:])

    constraints = []
    for idx, (x, y) in enumerate(zip(soft_points_x, soft_points_y)):
        constraints.append({
            "type": "ineq",
            "fun": lambda v, x=x, y=y, idx=idx: y * (v[0] * x + v[1]) + v[2 + idx] - 1.0,
        })
    solved = minimize(
        objective,
        x0=[0.5, 0.0] + [1.0] * len(soft_points_x),
        method="SLSQP",
        bounds=[(None, None), (None, None)] + [(0.0, None)] * len(soft_points_x),
        constraints=constraints,
        options={"ftol": 1e-12, "maxiter": 2000},
    )
    soft_optima[str(c)] = {
        "success": bool(solved.success),
        "message": solved.message,
        "w": solved.x[0],
        "b": solved.x[1],
        "slacks": solved.x[2:].tolist(),
        "objective": solved.fun,
        "constraint_values": [y * (solved.x[0] * x + solved.x[1]) + solved.x[2 + idx] - 1.0 for idx, (x, y) in enumerate(zip(soft_points_x, soft_points_y))],
    }

rbf = []
gamma = 0.5
for a, b in [([0, 0], [0, 0]), ([0, 0], [1, 0]), ([0, 0], [2, 0])]:
    sq_dist = sum((u - v) ** 2 for u, v in zip(a, b))
    rbf.append({"a": a, "b": b, "squared_distance": sq_dist, "gamma": gamma, "kernel": math.exp(-gamma * sq_dist)})

results = {
    "lecture_page_83_metrics": metrics(10, 20, 50, 10000),
    "all_negative_1000": metrics(0, 1, 0, 999),
    "all_class0_10000": metrics(0, 10, 0, 9990),
    "lecture_page_85_costs": lecture_cost,
    "lecture_page_85_audit": lecture_cost_audit,
    "cost_sensitive_threshold": {
        "cost_matrix": {"C(+,+)": -1, "C(+,-)": 100, "C(-,+)": 1, "C(-,-)": 0},
        "predict_positive_if_p_positive_gt": q_threshold,
    },
    "hard_margin_example": hard_margin,
    "soft_margin_candidate_comparison": soft_candidates,
    "soft_margin_slsqp_optima": soft_optima,
    "rbf_example": rbf,
}

(root / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(results, ensure_ascii=False, indent=2))
