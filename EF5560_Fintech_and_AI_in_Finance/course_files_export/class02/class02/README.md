# Class 2 data

Regression and Return Predictability

Extract the ZIP and open these CSV files in Excel, R, or Python. This folder contains all the data needed for the examples listed below.

## Start here

1. Use market_features.csv for the SPY regression example and csi300_macro_panel_monthly_240m.csv for the China-macro example.
2. Estimate coefficients on pre-test observations and interpret their signs and significance.
3. Evaluate July 2021-June 2026 forecasts against lagged MA(12); use the saved result tables to compare your calculations.

## Data and definitions

- `market_features.csv`: SPY returns and predictors; use this filename for the Class 2 code example (240 rows; 2006-07-31 to 2026-06-30).
- `macro_monthly_240m.csv`: Monthly macro inputs for the three-market comparison (240 rows; 2006-07-31 to 2026-06-30).
- `market_index_returns_monthly_240m.csv`: Monthly market returns for the three-market comparison (240 rows; 2006-07-31 to 2026-06-30).
- `csi300_macro_panel_monthly_240m.csv`: CSI 300 returns and lagged Chinese macro predictors (240 rows; 2006-07-31 to 2026-06-30).

## Classroom results for comparison

- `spy_regression_scorecard.csv`: SPY test-period regression and timing statistics (1 rows).
- `spy_test_predictions_monthly.csv`: SPY test-period forecasts, benchmark, and realized returns (60 rows; 2021-07-31 to 2026-06-30).
- `csi300_macro_scorecard.csv`: CSI 300 test-period forecast statistics (1 rows).
- `csi300_macro_test_predictions.csv`: CSI 300 test forecasts, benchmark, and realized returns (60 rows; 2021-07-31 to 2026-06-30).
- `spy_single_predictor_regressions.csv`: Individual-predictor OLS coefficients and significance (4 rows).
- `spy_momentum_bins.csv`: Training-sample binned momentum and next-month returns (10 rows).
- `three_market_regression_scorecard.csv`: Regression evidence for the U.S., HKSAR, and Chinese mainland (3 rows).
- `three_market_timing_scorecard.csv`: Timing-strategy evidence for the three markets (3 rows).

## Columns, units, and interpretation

- Start with `market_features.csv`. It is the same SPY input supplied in Class 1 under `spy_features_monthly_240m.csv`; this package keeps only the filename used in the Class 2 slide.
- For the saved SPY multiple regression, predict `market_return` using `momentum_12`, `volatility_12`, and `ma_gap_10`. The single-predictor table also includes `return_lag1`.
- For CSI 300, use `exports_yoy_lag2`, `imports_yoy_lag2`, `cli_gap_lag2`, and `reer_12m_lag2`. These are already lagged. The first, second, and fourth are percent changes; CLI is measured relative to 100.
- The input covers July 2006-June 2026. Development is July 2006-June 2018, validation July 2018-June 2021, and test July 2021-June 2026. The saved final OLS fits use all 180 pre-test months.
- Monthly `market_return` is a log return before risk-free adjustment. SPY's `benchmark` and CSI 300's `benchmark_ma12` are the previous 12 monthly returns averaged. OOS R-squared is 1 minus model squared-error sum divided by benchmark squared-error sum.
- The October 2025 macro blanks and December 2025 lagged macro blanks are retained from Class 1. They are not among the saved SPY regression's three predictors. CSI 300's first 12 MA(12) values are blank; its 60 test benchmarks are complete.
- The saved timing results set the cash return and trading costs to zero. Monthly wealth calculations should be reviewed for the log-versus-simple return convention before being treated as investment-performance evidence.

## Return definition

The Class 2 forecasting target is monthly log market return before subtracting a risk-free return. Its MA(12) benchmark uses the preceding 12 monthly returns.
Classes 3-5 use separate excess-return panels; do not substitute those targets into the Class 2 result comparison.

## Sources

- Class 1 market and macro data, plus the Chinese macro panel documented in the lecture.

`manifest.json` is a file inventory for checking the download; you do not need it for the exercises.
