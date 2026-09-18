# Class 3 data

Linear Machine Learning for Return Prediction

## Files

- `market_linear_model_summary.csv`: Validation settings and test evidence for the monthly linear models.
- `market_linear_test_predictions.csv`: Monthly test predictions for the three markets.
- `stock_linear_model_summary.csv`: Validation settings and test evidence for the weekly stock models.
- `stock_linear_test_predictions.csv`: Weekly HSI constituent test predictions.
- `stock_linear_forecast_spreads.csv`: Forecast-sorted weekly high-minus-low portfolio evidence.

## Shared files

- `../shared/market_excess_return_panel.csv`: Three-market monthly excess-return forecasting panel.
- `../shared/hsi_stock_excess_return_panel.csv`: HSI stock-week panel with 30 characteristics and excess returns.
- `../shared/technical_characteristics_dictionary.csv`: Definitions for the 30 technical characteristics.
- `../shared/risk_free_yields_monthly.csv`: Monthly U.S. and Chinese mainland three-month government yields.

## Notes

- The market target is monthly excess return; the OOS benchmark is lagged MA(12) excess return.
- The stock target is weekly excess return; the OOS benchmark is zero.
- The obsolete active-return field is excluded from the student panel.

## Sources

- U.S. and HKSAR risk-free proxy: U.S. three-month Treasury yield.
- Chinese mainland risk-free proxy: ChinaBond three-month government yield.
