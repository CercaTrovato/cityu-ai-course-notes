"""AC6761 supplementary learning code, not instructor-provided code.

Read the original CSV without modifying it. Fit the specified pooled OLS with
an intercept: stockprice ~ bmratio + roe + size. No dropping, winsorisation,
extra predictors, lags, fixed effects or train/test split is performed.
All derived files go only to the explicitly supplied output directory.
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import sys

import numpy as np
import pandas as pd
import scipy
import statsmodels
import statsmodels.api as sm


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def analyse(data_path, output_dir):
    data_path = Path(data_path).resolve()
    output_dir = Path(output_dir).resolve()
    if output_dir.is_relative_to(data_path.parent):
        raise ValueError("Choose a separate derived-output directory, outside the source directory.")
    before = sha256(data_path)
    df = pd.read_csv(data_path, dtype={"GVKEY": "string"})
    required = ["GVKEY", "FYEAR", "stockprice", "bmratio", "roe", "size", "mom", "agratio"]
    if list(df.columns) != required:
        raise ValueError(f"Unexpected columns: {list(df.columns)}")
    if df.isna().any().any():
        raise ValueError("Missing values found; decide a documented sample rule before estimation.")
    numeric = df.drop(columns="GVKEY").to_numpy(dtype=float)
    if not np.isfinite(numeric).all():
        raise ValueError("Non-finite numeric values found; do not silently replace them.")
    if df.duplicated(["GVKEY", "FYEAR"]).any():
        raise ValueError("Duplicate firm-year keys found; inspect before estimation.")

    y = df["stockprice"]
    X = sm.add_constant(df[["bmratio", "roe", "size"]], has_constant="add")
    fit = sm.OLS(y, X, missing="raise").fit()
    # Independent numerical check: NumPy least-squares solver on the same X/y.
    beta_np, _, rank, singular_values = np.linalg.lstsq(X.to_numpy(), y.to_numpy(), rcond=None)
    np.testing.assert_allclose(fit.params.to_numpy(), beta_np, rtol=1e-9, atol=1e-9)
    residual = y.to_numpy() - X.to_numpy() @ beta_np
    sse = float(residual @ residual)
    centered_y = y.to_numpy() - y.mean()
    sst = float(centered_y @ centered_y)
    np.testing.assert_allclose(sse, fit.ssr, rtol=1e-10)
    np.testing.assert_allclose(1 - sse / sst, fit.rsquared, rtol=1e-10)
    np.testing.assert_allclose(residual.mean(), 0, atol=1e-9)

    # Sensitivity of uncertainty only: same coefficients, alternative covariance.
    hc1 = fit.get_robustcov_results(cov_type="HC1", use_t=True)
    cluster = fit.get_robustcov_results(
        cov_type="cluster", groups=df["GVKEY"], use_correction=True,
        df_correction=True, use_t=True,
    )
    ci = fit.conf_int(alpha=0.05)
    coeff = pd.DataFrame({
        "term": X.columns, "coefficient": fit.params.to_numpy(),
        "standard_error_conventional": fit.bse.to_numpy(),
        "t_conventional": fit.tvalues.to_numpy(),
        "p_conventional": fit.pvalues.to_numpy(),
        "ci95_low_conventional": ci[0].to_numpy(),
        "ci95_high_conventional": ci[1].to_numpy(),
        "standard_error_HC1": hc1.bse,
        "standard_error_firm_cluster": cluster.bse,
        "p_firm_cluster": cluster.pvalues,
    })
    preview = df.head(5).copy()
    preview["fitted_stockprice"] = fit.predict(X.iloc[:5]).to_numpy()
    preview["residual_actual_minus_fitted"] = preview.stockprice - preview.fitted_stockprice
    sizes = df.groupby("GVKEY").size()
    stats = {c: {k: float(v) for k, v in df[c].describe(percentiles=[.01,.25,.5,.75,.99]).items()}
             for c in required[2:]}
    summary = {
        "source_path_at_run": str(data_path), "source_sha256": before,
        "script_sha256": sha256(__file__),
        "source_bytes_unchanged": sha256(data_path) == before,
        "rows": len(df), "columns": required,
        "companies": int(df.GVKEY.nunique()),
        "years": sorted(int(v) for v in df.FYEAR.unique()),
        "company_year_duplicate_count": int(df.duplicated(["GVKEY","FYEAR"]).sum()),
        "missing_counts": {k:int(v) for k,v in df.isna().sum().items()},
        "firm_observation_count_distribution": {str(k):int(v) for k,v in sizes.value_counts().sort_index().items()},
        "model": "pooled OLS with intercept; stockprice ~ bmratio + roe + size",
        "parameter_count_including_intercept": len(fit.params),
        "df_resid": float(fit.df_resid), "rank": int(rank),
        "r_squared": float(fit.rsquared), "adjusted_r_squared": float(fit.rsquared_adj),
        "SSE": sse, "SST": sst, "RMSE_in_sample": float(np.sqrt(sse/len(df))),
        "residual_standard_error": float(np.sqrt(sse/fit.df_resid)),
        "mean_stockprice": float(y.mean()), "residual_mean": float(residual.mean()),
        "condition_number": float(fit.condition_number),
        "negative_fitted_count": int((fit.fittedvalues < 0).sum()),
        "fitted_min": float(fit.fittedvalues.min()), "fitted_max": float(fit.fittedvalues.max()),
        "numpy_coefficient_max_abs_difference": float(np.max(np.abs(beta_np-fit.params.to_numpy()))),
        "data_summary": stats,
        "sensitivity": {
            "HC1": "heteroskedasticity-robust covariance; same point estimates",
            "firm_cluster": "same point estimates; finite-sample correction, t reference with G-1 degrees of freedom",
            "cluster_count": int(df.GVKEY.nunique()),
            "cluster_inference_df": int(df.GVKEY.nunique()-1),
            "limits": "Does not remove omitted variables, selection, reverse causality or common year shocks."
        },
        "environment": {"python":sys.version.split()[0],"platform":platform.platform(),
            "numpy":np.__version__,"pandas":pd.__version__,"scipy":scipy.__version__,"statsmodels":statsmodels.__version__},
        "not_performed": ["no causal identification","no future-return prediction","no train/test split",
            "no stock-specific fixed effects","no data cleaning beyond fail-fast validation",
            "no automatic inference of undocumented units or field construction"],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    coeff.to_csv(output_dir/"ols-coefficients.csv", index=False, float_format="%.12g")
    preview.to_csv(output_dir/"first-five-fitted.csv", index=False, float_format="%.12g")
    (output_dir/"ols-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    (output_dir/"statsmodels-summary.txt").write_text(str(fit.summary()),encoding="utf-8")
    print(f"Rows={len(df)}, companies={df.GVKEY.nunique()}, years={df.FYEAR.min()}-{df.FYEAR.max()}")
    print(coeff.to_string(index=False))
    print(f"R2={fit.rsquared:.12g}; adjusted R2={fit.rsquared_adj:.12g}; RMSE={summary['RMSE_in_sample']:.12g}")
    print(f"NumPy coefficient max difference={summary['numpy_coefficient_max_abs_difference']:.3g}")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, help="Original read-only data1.csv")
    parser.add_argument("--output-dir", required=True, help="Separate directory for derived files")
    args = parser.parse_args()
    analyse(args.data,args.output_dir)
