"""IS6400 sample-final learning calculations. No external substitute datasets.

Run with no arguments: source-image decision tree calculations only.
Run --q1 PATH: actual Q1 workbook summary.
Run --btc PATH: actual BTC file, fixed AR(1) on first differences.
All output stays in this scratch directory unless --output is supplied.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
TRAIN = [(0,0,0,0,4,0), (0,0,0,1,0,1), (0,0,1,0,0,1),
         (0,1,0,1,0,1), (1,0,1,0,3,0), (1,1,0,1,0,5)]
VALID = [(0,0,0,1,4,0), (0,0,1,1,3,0), (0,1,0,0,0,1),
         (0,1,1,0,0,2), (1,0,0,0,2,0), (1,0,0,1,3,0)]


def prediction(row, left=0, right=False, root=False):
    a,b,c,d,_,_ = row
    if root:
        return '-'
    if a == 1:
        return '-' if right else ('+' if b == 0 else '-')
    if left == 3:
        return '+'
    if b == 1:
        return '-'
    if left == 2:
        return '+'
    if c == 1:
        return '-'
    if left == 1:
        return '+'
    return '+' if d == 0 else '-'


def evaluate(rows, left=0, right=False, root=False):
    details = []
    for i,row in enumerate(rows, 1):
        pred = prediction(row, left, right, root)
        wrong = row[5] if pred == '+' else row[4]
        details.append({'row': i, 'prediction': pred, 'errors': wrong})
    return {'n': sum(r[4]+r[5] for r in rows),
            'errors': sum(r['errors'] for r in details), 'rows': details}


def tree_results():
    models = []
    for right in (False, True):
        for left in range(4):
            tr = evaluate(TRAIN, left, right)
            va = evaluate(VALID, left, right)
            leaves = 6-left-int(right)
            models.append({'model': f'L{left}-R{int(right)}',
                           'leaves': leaves, 'train_errors': tr['errors'],
                           'validation_errors': va['errors'],
                           'training_error_percent': 100*tr['errors']/15,
                           'pessimistic_percent': 100*(tr['errors']+leaves)/15,
                           'validation_error_percent': 100*va['errors']/15,
                           'training_rows': tr['rows'], 'validation_rows': va['rows']})
    tr = evaluate(TRAIN, root=True)
    va = evaluate(VALID, root=True)
    models.append({'model': 'root-only', 'leaves': 1,
                   'train_errors': tr['errors'], 'validation_errors': va['errors'],
                   'training_error_percent': 100*tr['errors']/15,
                   'pessimistic_percent': 100*(tr['errors']+1)/15,
                   'validation_error_percent': 100*va['errors']/15,
                   'training_rows': tr['rows'], 'validation_rows': va['rows']})
    assert evaluate(TRAIN)['errors'] == 0
    assert evaluate(VALID)['errors'] == 7
    assert next(m for m in models if m['model']=='L2-R0')['validation_errors'] == 0
    return {'training': TRAIN, 'validation': VALID, 'models': models}


def require_file(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f'Original course data missing: {path}. No proxy data used.')
    return path


def q1_summary(path):
    path = require_file(path)
    df = pd.read_excel(path)
    needed = {'Churn','LastTransaction'}
    if not needed.issubset(df.columns):
        raise ValueError(f'Required columns absent. Actual columns: {list(df.columns)}')
    churn = df['Churn'].replace(r'^\s*$', pd.NA, regex=True)
    amount = pd.to_numeric(df['LastTransaction'], errors='coerce')
    invalid = df['LastTransaction'].notna() & amount.isna()
    if invalid.any():
        raise ValueError('Non-numeric non-empty LastTransaction entries: inspect before computing IQR.')
    valid = amount.dropna()
    if valid.empty or not np.isfinite(valid).all():
        raise ValueError('No valid finite LastTransaction values, or infinity encountered.')
    q1 = valid.quantile(.25, interpolation='linear')
    q3 = valid.quantile(.75, interpolation='linear')
    return {'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'rows': len(df), 'missing_churn': int(churn.isna().sum()),
            'valid_LastTransaction': len(valid),
            'missing_LastTransaction': int(amount.isna().sum()),
            'quartile_method': 'linear interpolation / Excel QUARTILE.INC',
            'Q1': float(q1), 'Q3': float(q3), 'IQR': float(q3-q1)}


def btc_forecast(path):
    from statsmodels.tsa.ar_model import AutoReg
    path = require_file(path)
    df = pd.read_csv(path)
    if not {'Date','Close'}.issubset(df.columns):
        raise ValueError(f'Expected Date and Close columns. Actual: {list(df.columns)}')
    # D/M/Y is the question's displayed convention; ISO dates also parse.
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True, errors='raise')
    df['Close'] = pd.to_numeric(df['Close'], errors='raise')
    df = df.sort_values('Date').set_index('Date')
    if df.index.has_duplicates:
        raise ValueError('Duplicate dates: resolve against the original file; do not silently drop.')
    start, end = pd.Timestamp('2013-04-30'), pd.Timestamp('2018-04-30')
    history = df.loc[start:end, 'Close']
    expected = pd.date_range(start, end, freq='D')
    if not history.index.equals(expected):
        raise ValueError('History is not the full consecutive 2013-04-30 to 2018-04-30 period.')
    if history.isna().any() or not np.isfinite(history).all():
        raise ValueError('Close contains missing/non-finite values: inspect rather than invent.')
    delta = history.diff().dropna()
    # Fix AR(1) before seeing forecasts. This is an explicit teaching specification.
    model = AutoReg(delta.to_numpy(), lags=1, trend='c', old_names=False).fit()
    next_delta = np.asarray(model.predict(start=len(delta), end=len(delta)+4, dynamic=False))
    next_close = float(history.iloc[-1]) + np.cumsum(next_delta)
    dates = pd.date_range('2018-05-01', periods=5, freq='D')
    result = pd.DataFrame({'Trading date': dates.strftime('%Y-%m-%d'),
                           'Forecast': next_close})
    metadata = {'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'training_start': str(history.index[0].date()),
                'training_end': str(history.index[-1].date()),
                'n_prices': len(history), 'n_differences': len(delta),
                'model': 'AutoReg on first difference, lags=1, intercept',
                'parameters': model.params.tolist(),
                'last_actual_close': float(history.iloc[-1])}
    return result, metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--q1', type=Path)
    parser.add_argument('--btc', type=Path)
    parser.add_argument('--output', type=Path, default=HERE)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.q1:
        print(json.dumps(q1_summary(args.q1), ensure_ascii=False, indent=2))
    elif args.btc:
        result, metadata = btc_forecast(args.btc)
        print(json.dumps(metadata, ensure_ascii=False, indent=2))
        print(result.to_string(index=False, float_format=lambda x: f'{x:.2f}'))
        result.to_csv(args.output/'btc-forecast.csv', index=False, float_format='%.2f')
        (args.output/'btc-metadata.json').write_text(json.dumps(metadata, indent=2)+'\n', encoding='utf-8')
    else:
        result = tree_results()
        (args.output/'tree-recalculated.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        print(pd.DataFrame(result['models']).drop(columns=['training_rows','validation_rows']).to_string(index=False, float_format=lambda x: f'{x:.2f}'))


if __name__ == '__main__':
    try:
        main()
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
