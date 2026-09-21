# Class 3 data

Linear Machine Learning for Return Prediction

Extract the whole ZIP, then open the CSV files in this folder. No separate shared-data download is needed.

## Using the data

1. Start with market_excess_return_panel.csv; compare linear models using the four lagged macro predictors and the supplied split.
2. Use hsi_stock_excess_return_panel.csv and the characteristic dictionary for the weekly stock exercise.
3. Choose model settings on validation observations, then compare test errors and forecast-sorted portfolio returns with the reference results.

## Data and definitions

- `market_excess_return_panel.csv`: Three-market monthly excess-return forecasting panel.
- `hsi_stock_excess_return_panel.csv`: HSI stock-week panel with 30 characteristics and excess returns.
- `technical_characteristics_dictionary.csv`: Definitions for the 30 technical characteristics.
- `risk_free_yields_monthly.csv`: Monthly U.S. and Chinese mainland three-month government yields.
- `hsi_constituents_2023_07.csv`: Fixed July 2023 constituent list, company names, sectors, and membership source.

## Classroom results for comparison

- `market_linear_model_summary.csv`: Validation settings and test evidence for the monthly linear models.
- `market_linear_test_predictions.csv`: Monthly test predictions for the three markets.
- `stock_linear_model_summary.csv`: Validation settings and test evidence for the weekly stock models.
- `stock_linear_test_predictions.csv`: Weekly HSI constituent test predictions.
- `stock_linear_forecast_spreads.csv`: Forecast-sorted weekly high-minus-low portfolio evidence.
- `market_linear_validation.csv`: Validation losses across candidate model settings.
- `market_linear_coefficients.csv`: Fitted standardized coefficients for the market models.
- `stock_linear_validation.csv`: Validation losses for the weekly stock models.
- `stock_linear_coefficients.csv`: Fitted standardized coefficients for the linear stock models.
- `stock_linear_quintiles.csv`: Weekly realized returns for forecast-sorted stock portfolios.

## Forecast panels

| Panel | Row key | Development | Validation | Test |
| --- | --- | --- | --- | --- |
| Monthly markets | forecast_month + market | 142 months per market | 36 months per market | 60 months per market |
| Weekly HSI stocks | forecast_week + ticker | 78 weeks | 26 weeks | 52 weeks |

The `split` column records these periods. All stocks from one week belong to the same split.
The stock grid has 80 July 2023 constituents over 156 weeks (12,480 rows). Blank cells denote unavailable observations, not zeros.

- Market target: `market_excess_return`; benchmark: `benchmark_ma12_excess_return`. Use the four lagged macro columns as predictors.
- Stock target: `excess_return`; benchmark: zero. The 30 columns ending in `_rank` are the model inputs; their raw indicators and formulas are also supplied.
- Excess return is total return minus the period-matched risk-free return. Returns are decimals (0.01 = 1%); annual yields are percent. Dates, IDs, targets, contemporaneous returns, and benchmark outcomes are not predictors.

The U.S. and HKSAR use the prior month-end U.S. three-month Treasury yield; the Chinese mainland uses the ChinaBond three-month government yield.
The monthly market panel starts in September 2006 and ends in June 2026. Its first 12 months have no MA(12) benchmark; the test period is complete.

## Notes

- The four market predictors are U.S. macro variables in all three markets. Class 2's CSI 300 example uses a different, China-macro specification.

## Sources

- U.S. and HKSAR risk-free proxy: U.S. three-month Treasury yield.
- Chinese mainland risk-free proxy: ChinaBond three-month government yield.

`manifest.json` lists column names, row counts, date ranges, and SHA-256 checksums.
