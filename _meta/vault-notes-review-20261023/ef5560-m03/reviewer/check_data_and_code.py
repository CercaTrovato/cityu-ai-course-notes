from pathlib import Path
import json, hashlib, io, contextlib, re, sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import sklearn

ROOT=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61')
OUT=ROOT/'reviewer'
VAULT=Path('D:/上课资料/CityU')
LOCAL=VAULT/'EF5560_Fintech_and_AI_in_Finance/course_files_export/class03/class03'
ZIP=OUT/'zip-original/class03'
result={'python':sys.version,'sklearn':sklearn.__version__}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
result['zip_comparison']=[]
for p in ZIP.iterdir():
    if p.is_file():
        local=LOCAL/p.name
        result['zip_comparison'].append({'file':p.name,'zip_sha':sha(p),'local_sha':sha(local) if local.exists() else None,'same':local.exists() and sha(local)==sha(p)})
result['manifest_checks']={}
for label,base in [('local',LOCAL),('zip',ZIP)]:
    manifest=json.loads((base/'manifest.json').read_text(encoding='utf-8'))
    checks=[]
    for entry in manifest['files']:
        p=base/entry['file']; df=pd.read_csv(p)
        checks.append({'file':entry['file'],'sha_match':sha(p)==entry['sha256'],'byte_match':p.stat().st_size==entry['bytes'],'rows':len(df),'row_match':len(df)==entry['rows'],'column_match':list(df.columns)==entry['columns']})
    result['manifest_checks'][label]=checks
    mp=pd.read_csv(base/'market_linear_test_predictions.csv'); ms=pd.read_csv(base/'market_linear_model_summary.csv')
    rows=[]
    for market,g in mp.groupby('market'):
        den=np.square(g.actual-g['MA(12)']).sum()
        for model in ['OLS','Ridge','LASSO','Elastic Net']:
            val=1-np.square(g.actual-g[model]).sum()/den
            ref=ms.loc[(ms.market==market)&(ms.model==model),'oos_r2'].iloc[0]
            rows.append({'market':market,'model':model,'n':len(g),'r2':val,'summary':float(ref),'abs_error':abs(val-ref),'benchmark_sse':float(den)})
    result[label+'_market_saved_recalculation']=rows

sp=pd.read_csv(LOCAL/'stock_linear_test_predictions.csv')
ss=pd.read_csv(LOCAL/'stock_linear_model_summary.csv')
result['stock_saved_recalculation']=[]
for model in ['OLS','Ridge','LASSO','Elastic Net','PCR','PLS']:
    r2=1-np.square(sp.actual-sp[model]).sum()/np.square(sp.actual).sum()
    ref=float(ss.loc[ss.model==model,'oos_r2'].iloc[0])
    row={'model':model,'n':len(sp),'r2':float(r2),'summary_abs_error':abs(r2-ref),'nunique':int(sp[model].nunique()),'sd':float(sp[model].std())}
    if sp[model].nunique()>1:
        d=sp.copy()
        d['q']=d.groupby('forecast_week')[model].transform(lambda s:pd.qcut(s.rank(method='first'),5,labels=False)+1)
        w=d.groupby(['forecast_week','q']).actual.mean().unstack()
        s=w[5]-w[1]
        row.update(quintiles=w.mean().to_list(),mean=float(s.mean()),sd_spread=float(s.std()),se=float(s.std()/np.sqrt(len(s))),t=float(s.mean()/s.std()*np.sqrt(len(s))),positive_weeks=int((s>0).sum()),weeks=len(s),first_half=float(s.iloc[:26].mean()),second_half=float(s.iloc[26:].mean()),gross2_growth=float((1+s).prod()),gross1_growth=float((1+s/2).prod()))
        s.to_csv(OUT/f'{model.lower()}-weekly-spread.csv')
    result['stock_saved_recalculation'].append(row)

panel=pd.read_csv(LOCAL/'hsi_stock_excess_return_panel.csv')
features=[c for c in panel.columns if c.endswith('_rank')]
usable=panel['usable_for_ml'].astype(str).str.lower().eq('true')
result['stock_panel']={'rows':len(panel),'features':len(features),'tickers_grid':int(panel.ticker.nunique()),'usable':int(usable.sum()),'per_split':panel.loc[usable].groupby('split').size().to_dict(),'one_split_per_week':bool(panel.groupby('forecast_week').split.nunique().eq(1).all())}
rank_errors=[]
for feature in features:
    raw=feature[:-5]
    calc=panel.groupby('forecast_week')[raw].rank(pct=True,method='average')-0.5
    rank_errors.append(float((calc-panel[feature]).abs().max()))
result['rank_max_error']=max(rank_errors)
refit=panel.loc[usable & panel.split.isin(['development','validation'])]
z=StandardScaler().fit_transform(refit[features])
pca=PCA().fit(z)
corr=np.corrcoef(z,rowvar=False)
result['pca']={'mean_abs_offdiag':float(np.abs(corr[np.triu_indices(30,1)]).mean()),'cum_3_5_10':np.cumsum(pca.explained_variance_ratio_)[[2,4,9]].tolist(),'pc1':dict(zip(features,pca.components_[0].tolist())),'pc2':dict(zip(features,pca.components_[1].tolist()))}
y=panel.loc[panel.risk_free_yield_pct.notna(),'risk_free_yield_pct']/100
rf=panel.loc[panel.risk_free_yield_pct.notna(),'risk_free_return']
result['weekly_rf_effective7d_error']=float((rf-((1+y)**(7/365)-1)).abs().max())
for label,base in [('local',LOCAL),('zip',ZIP)]:
    p=pd.read_csv(base/'market_excess_return_panel.csv'); y=p.risk_free_yield_lag1_pct/100
    result[label+'_monthly_rf_errors']={'simple_effective':float((p.risk_free_return-((1+y)**(1/12)-1)).abs().max()),'log_effective':float((p.risk_free_return-np.log1p(y)/12).abs().max())}

for label,ids in [('market',[2]),('weekly',[3,4])]:
    ns={'__name__':'__main__'}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf):
        for i in ids: exec(compile((OUT/f'candidate-python-{i}.py').read_text(encoding='utf-8'),str(OUT/f'candidate-python-{i}.py'),'exec'),ns)
    (OUT/f'candidate-{label}-execution.txt').write_text(buf.getvalue(),encoding='utf-8')
    if label=='market': result['candidate_market_execution']={'chosen':ns['chosen'],'stdout':buf.getvalue()}
    else:
        result['candidate_weekly_execution']={'best':ns['best'],'stdout':buf.getvalue(),'ccb_prediction':ns['pipeline'],'ccb_manual':ns['manual'],'ccb_actual':float(ns['ccb'].excess_return.iloc[0]),'pca_scores':ns['scores'].tolist(),'return_intercept':float(ns['return_ols'].intercept_),'return_coefs':ns['return_ols'].coef_.tolist()}

def default(o):
    if isinstance(o,np.generic): return o.item()
    raise TypeError(type(o).__name__)
(OUT/'independent-calculations.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=default),encoding='utf-8')
print('versions',result['python'],result['sklearn'])
print('different_zip_vs_local',[r['file'] for r in result['zip_comparison'] if not r['same']])
print('manifest_all_valid',{k:all(x['sha_match'] and x['byte_match'] and x['row_match'] and x['column_match'] for x in v) for k,v in result['manifest_checks'].items()})
print('candidate-market',result['candidate_market_execution'])
print('candidate-weekly',result['candidate_weekly_execution'])
print('PCA',result['pca']['mean_abs_offdiag'],result['pca']['cum_3_5_10'])
print('rank-error',result['rank_max_error'],'rf',result['weekly_rf_effective7d_error'],result['local_monthly_rf_errors'],result['zip_monthly_rf_errors'])
print('saved_metrics_max_abs_error',max(x['abs_error'] for x in result['local_market_saved_recalculation']),max(x['summary_abs_error'] for x in result['stock_saved_recalculation']))
print('Ridge_spread',next(x for x in result['stock_saved_recalculation'] if x['model']=='Ridge'))
