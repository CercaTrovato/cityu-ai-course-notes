# Class 1 data

Financial Data and Vibe Coding

Extract the whole ZIP, then open the CSV files in this folder. No separate shared-data download is needed.

## Using the data

1. Open the AAPL and market tables; check dates, missing values, and return units.
2. Plot prices and returns, then compare the PDD/JD long-short example.
3. Inspect the lagged predictors in spy_features_monthly_240m.csv before using them to forecast.

## Data and definitions

- `macro_monthly_240m.csv`: Monthly U.S. macro variables and the term spread.
- `market_index_prices_monthly_240m.csv`: Monthly price levels for the market examples.
- `market_index_returns_monthly_240m.csv`: Monthly market returns in decimal units.
- `aapl_prices_returns_weekly_156w.csv`: Three years of weekly AAPL prices and returns.
- `pdd_jd_pair_weekly_156w.csv`: Weekly PDD and JD returns and a long-short illustration.
- `spy_features_monthly_240m.csv`: SPY returns and lagged monthly predictors.

## Notes

- Returns are in decimal units unless a column name states otherwise.
- Monthly observations run through June 2026; individual-stock examples use the three-year weekly contract.
- The AAPL financial-statement and filing-date demonstration requires a live download. No saved quarterly-statement CSV is available in this course snapshot.

## Sources

- Yahoo Finance market and stock histories.
- Federal Reserve Economic Data (FRED): https://fred.stlouisfed.org/

`manifest.json` lists column names, row counts, date ranges, and SHA-256 checksums.
