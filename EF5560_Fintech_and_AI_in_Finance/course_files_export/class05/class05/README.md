# Class 5 data

Interpretable Machine Learning and Portfolio Decisions

Extract the ZIP and open these CSV files in Excel, R, or Python. This folder contains all the data needed for the examples listed below.

## Start here

1. Use the stock panel and characteristic dictionary to interpret model inputs and the saved importance scores.
2. Use stock_linear_test_predictions.csv for forecast sorts, or weekly_momentum_sort_returns.csv for the separate momentum sort. Compare the six-model results with stock_linear_forecast_spreads.csv.
3. Use the CAPM return files and weekly HSI panel to estimate alpha and beta; compare with the saved regressions.

## Data and definitions

- `model_portfolios_monthly.csv`: Monthly forecasts, positions, total returns, and excess returns (60 rows; 2021-07-31 to 2026-06-30).
- `three_market_capm_returns_monthly.csv`: Monthly total and excess returns used in the CAPM regressions (180 rows; 2021-07-31 to 2026-06-30).
- `capm_market_data_monthly.csv`: Matched market total returns, risk-free returns, and excess returns for CAPM (180 rows; 2021-07-31 to 2026-06-30).
- `hsi_top5_weights_2026_08.csv`: August 2026 index weights identifying the five CAPM examples (5 rows).
- `weekly_momentum_sort_returns.csv`: Realized total returns for the course's weekly momentum-sorted portfolios (156 rows; 2023-07-07 to 2026-06-26).
- `stock_linear_test_predictions.csv`: Stock-week forecasts and realized returns for comparing the six linear-model portfolio sorts (4,108 rows; 2025-07-04 to 2026-06-26).
- `market_excess_return_panel.csv`: Three-market monthly excess-return forecasting panel (714 rows; 2006-09-30 to 2026-06-30).
- `hsi_stock_excess_return_panel.csv`: HSI stock-week panel with 30 characteristics and excess returns (12,480 rows; 2023-07-07 to 2026-06-26).
- `technical_characteristics_dictionary.csv`: Definitions for the 30 technical characteristics (30 rows).
- `risk_free_yields_monthly.csv`: Monthly U.S. and Chinese mainland three-month government yields (241 rows; 2006-06-30 to 2026-06-30).
- `hsi_constituents_2023_07.csv`: Fixed July 2023 constituent list, company names, sectors, and membership source (80 rows).

## Classroom results for comparison

- `model_portfolio_summary.csv`: Return, risk, drawdown, Sharpe ratio, and turnover statistics (3 rows).
- `stock_drop_zero_importance.csv`: Drop-to-zero characteristic importance for the stock model (30 rows).
- `three_market_capm_regressions.csv`: CAPM alpha and beta for the three market-timing examples (3 rows).
- `hsi_large_constituent_capm.csv`: Weekly CAPM evidence for selected large HSI constituents (5 rows).
- `three_market_timing_scorecard.csv`: Three-market OLS timing results calculated with simple portfolio returns (3 rows).
- `stock_linear_coefficients.csv`: Fitted standardized stock coefficients for the interpretation examples (180 rows).
- `stock_linear_forecast_spreads.csv`: Summary of the six linear-model sorts shown in Class 5, including the models with constant forecasts (6 rows).
- `stock_linear_model_summary.csv`: Selected linear settings and stock-model test evidence (7 rows).
- `stock_nonlinear_model_summary.csv`: Selected nonlinear settings and stock-model test evidence (5 rows).

## Columns, units, and interpretation

- For interpretation, begin with `stock_linear_coefficients.csv` and `stock_drop_zero_importance.csv`. In the latter, `delta_r2` is the loss of training R-squared when one ranked input is set to zero while keeping the fitted model fixed. It is not OOS R-squared. Multiply by 100 to express it in percentage points.
- The momentum file contains weekly simple returns for the Low/Middle/High groups and `High-Low`. The six-model forecast sorts instead use `stock_linear_test_predictions.csv`; do not treat the two sorts as the same strategy. LASSO and Elastic Net have constant forecasts and no reported long-short sort.
- Monthly model portfolios cover the U.S. market only, July 2021-June 2026. Columns ending in `weight`, `portfolio return`, and `portfolio excess return` distinguish positions, before-risk-free-adjustment returns, and excess returns.
- Monthly model forecasts remain in log excess-return units. Market, risk-free, portfolio-return, and portfolio-excess-return fields used for wealth and performance are converted to simple returns before portfolio arithmetic and compounding. Weekly stock returns are simple returns.
- The three-market timing scorecard uses 167 complete pre-test months per market (Aug 2007-Jun 2021) after lag construction, then a common 60-month test (Jul 2021-Jun 2026). Forecasts and OOS losses use monthly log returns; strategy returns, annualized means, Sharpe ratios, and compounded wealth use simple returns converted from realized log returns. Cash earns zero in that classroom exercise.
- CAPM uses the local market: adjusted SPY for the U.S., Hang Seng for HKSAR, and CSI 300 for the Chinese mainland. `hsi_top5_weights_2026_08.csv` selects the five stock examples using August 2026 weights; it does not define a July 2023 trading universe.

## Forecast panels

| Panel | Row key | Development | Validation | Test |
| --- | --- | --- | --- | --- |
| Monthly markets | forecast_month + market | Sep 2006-Jun 2018 (142) | Jul 2018-Jun 2021 (36) | Jul 2021-Jun 2026 (60) |
| Weekly HSI stocks | forecast_week + ticker | 7 Jul 2023-27 Dec 2024 (78) | 3 Jan-27 Jun 2025 (26) | 4 Jul 2025-26 Jun 2026 (52) |

The `split` column records these periods. All stocks from one week belong to the same split.
The stock grid has 80 July 2023 constituents over 156 weeks (12,480 rows). The stock models use the 12,281 rows with an outcome and all 30 ranked inputs: 6,123 development, 2,050 validation, and 4,108 test rows. Keep unavailable observations blank rather than replacing them with zero.

- Market target: `market_excess_return`; benchmark: `benchmark_ma12_excess_return`. Predictors: `term_spread_lag1`, `fed_funds_lag1`, `unemployment_lag2`, and `inflation_lag2`. Rate and inflation columns are percent; term spread is percentage points.
- Stock target: `excess_return`; benchmark: zero. The 30 columns ending in `_rank` are the model inputs; their raw indicators and formulas are also supplied.
- Monthly market total, risk-free, excess, benchmark, and forecast fields are log returns. Weekly stock total, risk-free, excess, and forecast fields are simple returns. Returns are decimals; annual yields are percent. Dates, IDs, outcomes, and benchmarks are not predictors.

The U.S. and HKSAR use the prior month-end U.S. three-month Treasury yield; the Chinese mainland uses the ChinaBond three-month government yield.
The raw October 2025 U.S. unemployment/inflation gaps were forward-filled before lagging when constructing these shared panels. Model inputs are complete; no future observations were used to fill those gaps.
The monthly market panel starts in September 2006 and ends in June 2026. Its first 12 months have no MA(12) benchmark; the test period is complete.

## Notes

- The three-market timing scorecard uses 167 complete pre-test months per market (Aug 2007-Jun 2021) after lag construction, then a common 60-month test (Jul 2021-Jun 2026). Forecasts and OOS loss use monthly log returns; portfolio performance converts realized log returns to simple returns. Cash earns zero in this timing exercise.
- The saved empirical portfolio results are before transaction costs. The separate 10 bp cost and Sharpe-ratio examples in the slides are hypothetical and need no additional CSV.
- The ML investment assignment remains in its separate student-release folder.

## Sources

- Current Class 3 and Class 4 forecasts and the common risk-free-rate file.
- Hang Seng Index factsheet for constituent weights.

`manifest.json` is a file inventory for checking the download; you do not need it for the exercises.
