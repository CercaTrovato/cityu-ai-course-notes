from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats


ROOT = Path(r"D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance")
DATA = ROOT / "course_files_export/class02/class02"
OUT = Path(r"E:/app-data/codex/scratchpad/vault-notes-revision-20261023/ef5560-m02/recompute-results.json")
SPLIT = pd.Timestamp("2021-07-01")
X3 = ["momentum_12", "volatility_12", "ma_gap_10"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = json.loads((DATA / "manifest.json").read_text(encoding="utf-8"))
hash_checks = {}
for item in manifest["files"]:
    p = DATA / item["file"]
    hash_checks[item["file"]] = {
        "manifest": item["sha256"],
        "actual": sha256(p),
        "match": sha256(p) == item["sha256"],
    }


d = pd.read_csv(DATA / "market_features.csv", parse_dates=["forecast_month"]).sort_values("forecast_month")
d = d.set_index("forecast_month")
train, test = d.loc[d.index < SPLIT], d.loc[d.index >= SPLIT]
assert (len(d), len(train), len(test)) == (240, 180, 60)

simple = {}
for x in X3:
    fit = sm.OLS(train["market_return"], sm.add_constant(train[[x]])).fit()
    simple[x] = {
        "intercept_pct": float(fit.params["const"] * 100),
        "slope_pct_per_decimal": float(fit.params[x] * 100),
        "se_pct_per_decimal": float(fit.bse[x] * 100),
        "t": float(fit.tvalues[x]),
        "p": float(fit.pvalues[x]),
        "r2_pct": float(fit.rsquared * 100),
    }

mu = train[X3].mean()
sd = train[X3].std(ddof=1)
ztr = (train[X3] - mu) / sd
zte = (test[X3] - mu) / sd
fit3 = sm.OLS(train["market_return"], sm.add_constant(ztr)).fit()
pred = fit3.predict(sm.add_constant(zte))
ma12 = d["market_return"].shift(1).rolling(12).mean().loc[test.index]
spy_model_sse = float(((test["market_return"] - pred) ** 2).sum())
spy_bench_sse = float(((test["market_return"] - ma12) ** 2).sum())
spy_oos = 1 - spy_model_sse / spy_bench_sse
spy_hits = int((np.sign(pred) == np.sign(test["market_return"])).sum())
spy_pos = int((test["market_return"] > 0).sum())
spy_neg_pred = int((pred < 0).sum())


csi = pd.read_csv(DATA / "csi300_macro_panel_monthly_240m.csv", parse_dates=["forecast_month"]).sort_values("forecast_month")
csi = csi.set_index("forecast_month")
ctr, cte = csi.loc[csi.index < SPLIT], csi.loc[csi.index >= SPLIT]
xc = ["exports_yoy_lag2", "imports_yoy_lag2", "cli_gap_lag2", "reer_12m_lag2"]
fitc = sm.OLS(ctr["market_return"], sm.add_constant(ctr[xc])).fit()
predc = fitc.predict(sm.add_constant(cte[xc]))
yc = cte["market_return"]
bc = cte["benchmark_ma12"]
csi_model_sse = float(((yc - predc) ** 2).sum())
csi_bench_sse = float(((yc - bc) ** 2).sum())
csi_pos = int((yc > 0).sum())
csi_hits = int((np.sign(predc) == np.sign(yc)).sum())
csi_always_down_hits = int((yc < 0).sum())


# Candidate §2.4.1a three-row calculation.
x = np.array([0.0, 1.0, 2.0])
y = np.array([1.0, 2.0, 2.0])
fit_small = sm.OLS(y, sm.add_constant(x)).fit()
tcrit = float(stats.t.ppf(0.975, df=1))


# Candidate §2.5.1a four-row matrix calculation.
xm = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
ym = np.array([1.0, 2.0, 3.0, 5.0])
fit_matrix = sm.OLS(ym, sm.add_constant(xm)).fit()


# Candidate §2.9a two-period account example and fractional-weight variant.
v0 = 100.0
v1 = v0 * math.exp(0.1)
v2 = v1 * 1.01
half_simple = 0.5 * (math.exp(0.1) - 1)
half_log = math.log1p(half_simple)


# Verify the exact slide snippet's predict contract against a statsmodels fit.
test_z_full = test.copy()
test_z_full[["momentum_z", "volatility_z", "ma_gap_z"]] = (test[X3] - mu) / sd
predict_full_frame = {"worked": True, "error": None}
try:
    fit3.predict(test_z_full)
except Exception as exc:
    predict_full_frame = {"worked": False, "error": f"{type(exc).__name__}: {exc}"}


official_spy = pd.read_csv(DATA / "spy_regression_scorecard.csv").iloc[0]
official_three = pd.read_csv(DATA / "three_market_regression_scorecard.csv")
official_timing = pd.read_csv(DATA / "three_market_timing_scorecard.csv")
official_spy_predictions = pd.read_csv(DATA / "spy_test_predictions_monthly.csv")


def recursive_forecast(kind: str, window: int) -> pd.Series:
    out = pd.Series(np.nan, index=d.index)
    for i in range(window, len(d)):
        lo = 0 if kind == "expanding" else i - window
        tr = d.iloc[lo:i]
        fit = sm.OLS(tr["market_return"], sm.add_constant(tr[X3])).fit()
        out.iloc[i] = fit.predict(sm.add_constant(d.iloc[[i]][X3], has_constant="add")).iloc[0]
    return out


rolling_results = {}
for label, series in {
    "expanding60": recursive_forecast("expanding", 60),
    "rolling60": recursive_forecast("rolling", 60),
    "rolling120": recursive_forecast("rolling", 120),
    "rolling180": recursive_forecast("rolling", 180),
}.items():
    idx = series.loc[SPLIT:].dropna().index
    rolling_results[label] = float(
        (1 - ((d.loc[idx, "market_return"] - series.loc[idx]) ** 2).sum()
         / ((d.loc[idx, "market_return"] - d["market_return"].shift(1).rolling(12).mean().loc[idx]) ** 2).sum())
        * 100
    )

result = {
    "hash_checks": hash_checks,
    "spy": {
        "simple": simple,
        "multi_params_pct": {k: float(v * 100) for k, v in fit3.params.items()},
        "multi_se_pct": {k: float(v * 100) for k, v in fit3.bse.items()},
        "multi_p": {k: float(v) for k, v in fit3.pvalues.items()},
        "multi_r2_pct": float(fit3.rsquared * 100),
        "model_mse": spy_model_sse / 60,
        "benchmark_mse": spy_bench_sse / 60,
        "oos_r2_pct": float(spy_oos * 100),
        "hits": spy_hits,
        "positive_months": spy_pos,
        "negative_predictions": spy_neg_pred,
        "official_single_scorecard_oos_pct": float(official_spy.oos_r_squared * 100),
        "official_three_market_oos_pct": float(official_three.loc[official_three.market.str.contains("SPY"), "oos_r2"].iloc[0] * 100),
        "official_prediction_rows_match_recomputed": bool(np.allclose(official_spy_predictions["forecast"], pred.to_numpy())),
    },
    "csi_macro": {
        "import_beta_target_decimal_per_input_pp": float(fitc.params["imports_yoy_lag2"]),
        "import_beta_target_pp_per_input_pp": float(fitc.params["imports_yoy_lag2"] * 100),
        "import_p": float(fitc.pvalues["imports_yoy_lag2"]),
        "f_p": float(fitc.f_pvalue),
        "train_r2_pct": float(fitc.rsquared * 100),
        "model_mse_x1e4": csi_model_sse / 60 * 1e4,
        "benchmark_mse_x1e4": csi_bench_sse / 60 * 1e4,
        "oos_r2_pct": float((1 - csi_model_sse / csi_bench_sse) * 100),
        "model_hits": csi_hits,
        "positive_months": csi_pos,
        "always_down_hits": csi_always_down_hits,
    },
    "small_ols": {
        "params": fit_small.params.tolist(),
        "sse": float(np.sum(fit_small.resid ** 2)),
        "se_slope": float(fit_small.bse[1]),
        "t_slope": float(fit_small.tvalues[1]),
        "p_slope": float(fit_small.pvalues[1]),
        "tcrit_95_df1": tcrit,
        "ci_slope": [float(fit_small.params[1] - tcrit * fit_small.bse[1]), float(fit_small.params[1] + tcrit * fit_small.bse[1])],
        "r2": float(fit_small.rsquared),
        "f": float(fit_small.fvalue),
    },
    "matrix_ols": {
        "params": fit_matrix.params.tolist(),
        "resid": fit_matrix.resid.tolist(),
        "sse": float(np.sum(fit_matrix.resid ** 2)),
        "bse": fit_matrix.bse.tolist(),
        "tvalues": fit_matrix.tvalues.tolist(),
        "r2": float(fit_matrix.rsquared),
        "f": float(fit_matrix.fvalue),
        "f_p": float(fit_matrix.f_pvalue),
    },
    "strategy_example": {"v1": v1, "v2": v2, "half_simple": half_simple, "half_log": half_log},
    "slide_predict_full_dataframe": predict_full_frame,
    "rolling_oos_r2_pct_2021_07_onward": rolling_results,
    "official_timing": official_timing.to_dict(orient="records"),
}

OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
