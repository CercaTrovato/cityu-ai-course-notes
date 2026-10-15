from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.datasets import make_classification
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier, RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


ROOT = Path(r"D:\上课资料\CityU")
SRC = ROOT / "IS6400_Business_Data_Analytics" / "course_files_export"
OUT = Path(r"E:\app-data\codex\scratchpad\is6400-classification-20261014\tutorial")
OUT.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def scalar(v):
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return float(v)
    return v


nb_path = SRC / "Week 7 Classification_Tutorial.ipynb"
credit_path = SRC / "Credit_approval.csv"
fraud_path = SRC / "creditcard-reduced.csv"

nb = json.loads(nb_path.read_text(encoding="utf-8"))
cell_inventory = []
for i, cell in enumerate(nb["cells"]):
    outputs = cell.get("outputs", [])
    cell_inventory.append({
        "cell": i,
        "type": cell["cell_type"],
        "execution_count": cell.get("execution_count"),
        "saved_output_count": len(outputs),
        "source_lines": len(cell.get("source", [])),
    })

credit = pd.read_csv(credit_path)
fraud = pd.read_csv(fraud_path)

credit_summary = {
    "shape": list(credit.shape),
    "file_size_bytes": credit_path.stat().st_size,
    "columns_exact": list(credit.columns),
    "dtypes": {k: str(v) for k, v in credit.dtypes.items()},
    "missing_count": {k: int(v) for k, v in credit.isna().sum().items()},
    "duplicates": int(credit.duplicated().sum()),
    "target_counts": {str(k): int(v) for k, v in credit["Approved"].value_counts().items()},
    "target_share": {str(k): float(v) for k, v in credit["Approved"].value_counts(normalize=True).items()},
    "numeric_min": {k: scalar(v) for k, v in credit.select_dtypes("number").min().items()},
    "numeric_max": {k: scalar(v) for k, v in credit.select_dtypes("number").max().items()},
    "numeric_mean": {k: scalar(v) for k, v in credit.select_dtypes("number").mean().items()},
}

fraud_summary = {
    "shape": list(fraud.shape),
    "file_size_bytes": fraud_path.stat().st_size,
    "columns": list(fraud.columns),
    "dtypes": {k: str(v) for k, v in fraud.dtypes.items()},
    "missing_count": {k: int(v) for k, v in fraud.isna().sum().items()},
    "duplicates": int(fraud.duplicated().sum()),
    "target_counts": {str(k): int(v) for k, v in fraud["Class"].value_counts().items()},
    "target_share": {str(k): float(v) for k, v in fraud["Class"].value_counts(normalize=True).items()},
    "time_min_max": [scalar(fraud["Time"].min()), scalar(fraud["Time"].max())],
    "amount_min_max_mean_median": [
        scalar(fraud["Amount"].min()), scalar(fraud["Amount"].max()),
        scalar(fraud["Amount"].mean()), scalar(fraud["Amount"].median())
    ],
}

Y = credit["Approved"]
X = credit.drop(columns=["Approved"])
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=1)

models = {
    "decision_tree": DecisionTreeClassifier(max_depth=2),
    "random_forest": RandomForestClassifier(max_depth=2, n_estimators=500, random_state=1),
    "bagging": BaggingClassifier(estimator=DecisionTreeClassifier(max_depth=2), n_estimators=50, random_state=1),
    "adaboost": AdaBoostClassifier(estimator=DecisionTreeClassifier(max_depth=2), n_estimators=5, random_state=1),
    "stacking": StackingClassifier(
        estimators=[
            ("dt", DecisionTreeClassifier(max_depth=3, random_state=1)),
            ("knn", make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=7))),
            ("svm", make_pipeline(StandardScaler(), SVC(probability=True, C=1.0, kernel="rbf", random_state=1))),
        ],
        final_estimator=LogisticRegression(max_iter=2000, random_state=1),
        cv=5,
        stack_method="auto",
        passthrough=False,
    ),
}
model_results = {}
for name, model in models.items():
    model.fit(X_train, Y_train)
    pred_train = model.predict(X_train)
    pred_test = model.predict(X_test)
    model_results[name] = {
        "train_accuracy": float(accuracy_score(Y_train, pred_train)),
        "validation_accuracy": float(accuracy_score(Y_test, pred_test)),
        "confusion_labels": ["+", "-"],
        "confusion_matrix": confusion_matrix(Y_test, pred_test, labels=["+", "-"]).tolist(),
    }

X_syn, y_syn = make_classification(
    n_samples=10000, n_features=2, n_redundant=0,
    n_clusters_per_class=1, weights=[0.1], flip_y=0, random_state=2
)
Xs_train, Xs_test, ys_train, ys_test = train_test_split(
    X_syn, y_syn, test_size=0.4, random_state=1
)
weighted_results = {}
for name, weights in [("unweighted", None), ("class_weight_0_10", {0: 10.0, 1: 1.0})]:
    model = DecisionTreeClassifier(max_depth=2, class_weight=weights)
    model.fit(Xs_train, ys_train)
    pred = model.predict(Xs_test)
    weighted_results[name] = {
        "confusion_labels": [0, 1],
        "confusion_matrix": confusion_matrix(ys_test, pred, labels=[0, 1]).tolist(),
        "accuracy": float(accuracy_score(ys_test, pred)),
        "minority_0_precision": float(precision_score(ys_test, pred, pos_label=0)),
        "minority_0_recall": float(recall_score(ys_test, pred, pos_label=0)),
        "minority_0_f1": float(f1_score(ys_test, pred, pos_label=0)),
    }

fig, axes = plt.subplots(1, 3, figsize=(13, 4))
for label in [0, 1]:
    idx = y_syn == label
    axes[0].scatter(X_syn[idx, 0], X_syn[idx, 1], s=4, alpha=0.35, label=str(label))
axes[0].set_title("Synthetic imbalanced data")
axes[0].set_xlabel("feature 1")
axes[0].set_ylabel("feature 2")
axes[0].legend(title="class")
for ax, (title, key) in zip(axes[1:], [("No class weight", "unweighted"), ("class_weight={0:10,1:1}", "class_weight_0_10")]):
    cm = np.array(weighted_results[key]["confusion_matrix"])
    im = ax.imshow(cm, cmap="Blues")
    for (i, j), val in np.ndenumerate(cm):
        ax.text(j, i, str(val), ha="center", va="center")
    ax.set_title(title)
    ax.set_xlabel("predicted")
    ax.set_ylabel("actual")
    ax.set_xticks([0, 1], ["0", "1"])
    ax.set_yticks([0, 1], ["0", "1"])
fig.tight_layout()
fig.savefig(OUT / "class-weight-effect.svg", format="svg", bbox_inches="tight")
fig.savefig(OUT / "class-weight-effect.png", dpi=160, bbox_inches="tight")
plt.close(fig)

results = {
    "environment": {
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "scikit_learn": sklearn.__version__,
        "matplotlib": matplotlib.__version__,
        "notebook_kernelspec": nb.get("metadata", {}).get("kernelspec"),
        "notebook_language_info": nb.get("metadata", {}).get("language_info"),
    },
    "source_hashes_sha256": {
        nb_path.name: sha256(nb_path),
        credit_path.name: sha256(credit_path),
        fraud_path.name: sha256(fraud_path),
    },
    "cell_inventory": cell_inventory,
    "credit_approval": credit_summary,
    "fraud_dataset": fraud_summary,
    "split": {
        "train_shape": [int(X_train.shape[0]), int(X_train.shape[1])],
        "test_shape": [int(X_test.shape[0]), int(X_test.shape[1])],
        "train_target_counts": {str(k): int(v) for k, v in Y_train.value_counts().items()},
        "test_target_counts": {str(k): int(v) for k, v in Y_test.value_counts().items()},
    },
    "credit_models_recomputed": model_results,
    "synthetic_counts": {str(k): int(v) for k, v in zip(*np.unique(y_syn, return_counts=True))},
    "class_weight_recomputed": weighted_results,
    "scope_note": "评分任务使用 fraud 数据的五模型训练未执行；仅做数据概况。教学 cells 在 scratch 中用当前 API 复算。",
}
(OUT / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(results, ensure_ascii=False, indent=2))
