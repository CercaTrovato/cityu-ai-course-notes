# Class 4 data

Nonlinear Machine Learning for Return Prediction

Extract the ZIP and open these CSV files in Excel, R, or Python. This folder contains all the data needed for the examples listed below.

## Start here

1. Use the same input panels and date splits as Class 3; fit trees, random forests, or boosting.
2. Choose depth, tree count, and other settings on validation observations.
3. Compare test forecasts and characteristic importance with the saved results.

## Data and definitions

- `market_excess_return_panel.csv`: Three-market monthly excess-return forecasting panel (714 rows; 2006-09-30 to 2026-06-30).
- `hsi_stock_excess_return_panel.csv`: HSI stock-week panel with 30 characteristics and excess returns (12,480 rows; 2023-07-07 to 2026-06-26).
- `technical_characteristics_dictionary.csv`: Definitions for the 30 technical characteristics (30 rows).
- `risk_free_yields_monthly.csv`: Monthly U.S. and Chinese mainland three-month government yields (241 rows; 2006-06-30 to 2026-06-30).
- `hsi_constituents_2023_07.csv`: Fixed July 2023 constituent list, company names, sectors, and membership source (80 rows).

## Classroom results for comparison

- `market_nonlinear_model_summary.csv`: Test evidence for trees, forests, and boosting (15 rows).
- `market_nonlinear_test_predictions.csv`: Monthly nonlinear test predictions for the three markets (180 rows; 2021-07-31 to 2026-06-30).
- `market_nonlinear_feature_importance.csv`: Permutation importance for the selected market models (12 rows).
- `stock_nonlinear_model_summary.csv`: Test evidence for weekly nonlinear stock models (5 rows).
- `stock_nonlinear_test_predictions.csv`: Weekly nonlinear HSI constituent predictions (4,108 rows; 2025-07-04 to 2026-06-26).
- `stock_nonlinear_feature_importance.csv`: Permutation importance for the selected stock model (30 rows).
- `stock_nonlinear_forecast_spreads.csv`: Forecast-sorted weekly high-minus-low portfolio evidence (3 rows).
- `market_nonlinear_validation.csv`: Validation losses across candidate tree-model settings (90 rows).
- `stock_nonlinear_validation.csv`: Validation losses for weekly nonlinear stock models (30 rows).
- `stock_nonlinear_quintiles.csv`: Test-period mean returns by model and forecast quintile, not a weekly time series (15 rows).
- `csi300_recent_window_summary.csv`: CSI 300 July 2023-June 2026 results for the recent-window slide; the original June 2021 model fits are retained (4 rows; 2023-07-31 to 2026-06-30).

## Columns, units, and interpretation

- Start with the same market and stock panels as Class 3. Use the saved validation tables to identify the selected tree, forest, or boosting settings.
- `market_nonlinear_test_predictions.csv` contains 60 test months per market. For the recent CSI 300 slide, select `market` = `Chinese Mainland` and dates July 2023-June 2026. Compare with `csi300_recent_window_summary.csv` (36 months). This is a subperiod of the original test, not a refitted model.
- In prediction files, `actual` is realized excess return and model-name columns are forecasts. In importance files, the recorded permutation diagnostic belongs to the selected model; it is not a regression coefficient or a causal effect.
- Quintile files contain test-period mean returns, not time-series rows. Blank tuning settings indicate settings a model does not use. Neural-network diagrams and loss examples in the lecture are illustrative; no neural-network forecast results are included.

## Forecast panels

| Panel | Row key | Development | Validation | Test |
| --- | --- | --- | --- | --- |
| Monthly markets | forecast_month + market | Sep 2006-Jun 2018 (142) | Jul 2018-Jun 2021 (36) | Jul 2021-Jun 2026 (60) |
| Weekly HSI stocks | forecast_week + ticker | 7 Jul 2023-27 Dec 2024 (78) | 3 Jan-27 Jun 2025 (26) | 4 Jul 2025-26 Jun 2026 (52) |

The `split` column records these periods. All stocks from one week belong to the same split.
The stock grid has 80 July 2023 constituents over 156 weeks (12,480 rows). The stock models use the 12,281 rows with an outcome and all 30 ranked inputs: 6,123 development, 2,050 validation, and 4,108 test rows. Keep unavailable observations blank rather than replacing them with zero.

- Market target: `market_excess_return`; benchmark: `benchmark_ma12_excess_return`. Predictors: `term_spread_lag1`, `fed_funds_lag1`, `unemployment_lag2`, and `inflation_lag2`. Rate and inflation columns are percent; term spread is percentage points.
- Stock target: `excess_return`; benchmark: zero. The 30 columns ending in `_rank` are the model inputs; their raw indicators and formulas are also supplied.
- Weekly stock excess return is simple stock return minus the period-matched risk-free return. In the existing monthly market files, `market_total_return` is a log return and `market_excess_return` subtracts the supplied risk-free return from it. Returns are decimals; annual yields are percent. Dates, IDs, outcomes, and benchmarks are not predictors.

The U.S. and HKSAR use the prior month-end U.S. three-month Treasury yield; the Chinese mainland uses the ChinaBond three-month government yield.
The raw October 2025 U.S. unemployment/inflation gaps were forward-filled before lagging when constructing these shared panels. Model inputs are complete; no future observations were used to fill those gaps.
The monthly market panel starts in September 2006 and ends in June 2026. Its first 12 months have no MA(12) benchmark; the test period is complete.

## Sources

- Common Class 3 market and HSI stock panels.

`manifest.json` is a file inventory for checking the download; you do not need it for the exercises.
