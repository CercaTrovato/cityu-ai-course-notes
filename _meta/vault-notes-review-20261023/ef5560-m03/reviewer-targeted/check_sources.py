from pathlib import Path
import hashlib, io, json, subprocess, zipfile
import numpy as np
import pandas as pd

root=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61')
out=root/'reviewer-targeted'
course=Path('D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance')
raw=course/'course_files_export/class03/class03'
zip_path=course/'course_files_export/class03.zip'
with zipfile.ZipFile(zip_path) as z:
    panel_name=next(n for n in z.namelist() if n.endswith('/market_excess_return_panel.csv'))
    readme_name=next(n for n in z.namelist() if n.endswith('/README.md'))
    new=pd.read_csv(io.BytesIO(z.read(panel_name)))
    (out/'zip-readme.txt').write_bytes(z.read(readme_name))
old=pd.read_csv(raw/'market_excess_return_panel.csv')

def rf_errors(df):
    y=df['risk_free_yield_lag1_pct']/100
    return {'n':len(df),'simple_max_abs':float(np.max(np.abs(df.risk_free_return-((1+y)**(1/12)-1)))),
            'log_max_abs':float(np.max(np.abs(df.risk_free_return-np.log1p(y)/12)))}

pred=pd.read_csv(raw/'stock_linear_test_predictions.csv')
quintiles=pd.read_csv(raw/'stock_linear_quintiles.csv')
weekly=[]
for week, frame in pred.groupby('forecast_week'):
    frame=frame.copy()
    frame['q']=pd.qcut(frame['Ridge'].rank(method='first'),5,labels=False)+1
    grouped=frame.groupby('q')['actual'].mean()
    weekly.append(float(grouped.loc[5]-grouped.loc[1]))
d=np.array(weekly)
market=pd.read_csv(raw/'market_linear_test_predictions.csv')
us=market.loc[market.market=='U.S.']
stock=pd.read_csv(raw/'hsi_stock_excess_return_panel.csv')
usable=stock.loc[stock.usable_for_ml]
rank_basis=stock.loc[stock.complete_characteristics]
rank_error={c:float((rank_basis.groupby('forecast_week')[c[:-5]].rank(method='average',pct=True)-0.5-rank_basis[c]).abs().max())
            for c in stock.columns if c.endswith('_rank')}
feature_groups={}
dev=usable.loc[usable.split=='development']
for c in ['mom20d_rank','close_vs_sma20d_rank','rv20d_rank','illiq20d_rank']:
    rows=[]
    for _,f in dev.groupby('forecast_week'):
        q=pd.qcut(f[c].rank(method='first'),5,labels=False)+1
        rows.append(f.groupby(q)['excess_return'].mean().to_numpy())
    feature_groups[c]=(np.mean(rows,axis=0)*100).tolist()
summary={'rf_old_extracted':rf_errors(old),'rf_new_zip':rf_errors(new),
 'us_lasso':{'min':float(us['LASSO'].min()),'max':float(us['LASSO'].max()),'min_month':str(us.loc[us['LASSO'].idxmin(),'forecast_month'])},
 'ridge_weekly':{'n':len(d),'mean':float(d.mean()),'sd':float(d.std(ddof=1)),
 'se':float(d.std(ddof=1)/np.sqrt(len(d))),'t':float(d.mean()/(d.std(ddof=1)/np.sqrt(len(d)))),
 'positive':int((d>0).sum()),'first_half':float(d[:26].mean()),'second_half':float(d[26:].mean()),
 'full_equity_end':float(np.prod(1+d)),'half_equity_end':float(np.prod(1+d/2))},
 'rank_max_error':max(rank_error.values()),'feature_groups_percent':feature_groups,
 'constant_prediction_counts':{c:int(pred[c].nunique()) for c in ['LASSO','Elastic Net']},
 'rsi_fields':[x for x in pd.read_csv(raw/'technical_characteristics_dictionary.csv').name if 'rsi' in x.lower()]}
first=stock.loc[stock.forecast_week=='2023-07-07'].copy()
first['all_nonmissing_rank']=first.mom20d.rank(method='average',pct=True)-0.5
first['usable_only_rank']=(first.loc[first.usable_for_ml,'mom20d'].rank(method='average',pct=True)-0.5)
summary['rank_membership_first_week']={'all_rows':len(first),'valid_mom20d':int(first.mom20d.notna().sum()),
 'complete_features':int(first.complete_characteristics.sum()),'usable_for_ml':int(first.usable_for_ml.sum()),
 'CCB':first.loc[first.ticker=='0939.HK',['ticker','mom20d','mom20d_rank','complete_characteristics','usable_for_ml','all_nonmissing_rank','usable_only_rank']].to_dict(orient='records'),
 'raw_nonmissing_but_incomplete':first.loc[first.mom20d.notna() & ~first.complete_characteristics,['ticker','mom20d','mom20d_rank','complete_characteristics','usable_for_ml']].to_dict(orient='records')}
all_errors={c:float((stock.groupby('forecast_week')[c[:-5]].rank(method='average',pct=True)-0.5-stock[c]).abs().max()) for c in rank_error}
rank_col=max(all_errors,key=all_errors.get)
raw_col=rank_col[:-5]
all_rank=stock.groupby('forecast_week')[raw_col].rank(method='average',pct=True)-0.5
worst=(all_rank-stock[rank_col]).abs().idxmax()
w=stock.loc[worst,'forecast_week']
summary['rank_membership_difference']={'week':w,'feature':raw_col,'max_error':all_errors[rank_col],'row':stock.loc[worst,['ticker',raw_col,rank_col,'complete_characteristics','usable_for_ml']].to_dict(),
 'all_feature_valid_recalculation':float(all_rank.loc[worst]),
 'excluded_with_valid_raw_feature':stock.loc[(stock.forecast_week==w)&stock[raw_col].notna()&~stock.complete_characteristics,['ticker',raw_col,rank_col,'complete_characteristics','usable_for_ml']].to_dict(orient='records')}
(out/'independent-targeted-calculations.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
for name,pdf in [('old56',course/'course_files_export/Lec03_Linear_Machine_Learning.pdf'),
                 ('new54',course/'course_files_export/canvas-20261020/Lec03_Linear_Machine_Learning.pdf')]:
    subprocess.run(['pdftotext','-layout',str(pdf),str(out/f'{name}-source-layout.txt')],check=True,capture_output=True)
print(json.dumps(summary,ensure_ascii=False,indent=2))
