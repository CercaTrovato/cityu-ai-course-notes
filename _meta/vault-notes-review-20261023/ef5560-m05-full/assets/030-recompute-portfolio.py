from pathlib import Path
import json
import numpy as np
import pandas as pd

base = Path(r'D:\上课资料\CityU\EF5560_Fintech_and_AI_in_Finance\course_files_export\class05\class05')
out = Path(r'E:\app-data\codex\scratchpad\ef5560-m05-20261008')
result = {}
pred = pd.read_csv(base/'stock_linear_test_predictions.csv')
saved = pd.read_csv(base/'stock_linear_forecast_spreads.csv').set_index('model')
for model in ['OLS','Ridge','LASSO','Elastic Net','PCR','PLS']:
    d=pred.copy()
    if d[model].nunique()==1:
        result[model]={'constant':True,'value':float(d[model].iloc[0])}
        continue
    d['q']=d.groupby('forecast_week')[model].transform(lambda s: pd.qcut(s.rank(method='first'),5,labels=False)+1)
    means=d.groupby(['forecast_week','q']).stock_return.mean().unstack()
    spread=means[5]-means[1]
    vals={'weeks':len(spread),'mean':float(spread.mean()),'t':float(spread.mean()/spread.std(ddof=1)*np.sqrt(len(spread))),'hit_rate':float((spread>0).mean()),'first_half':float(spread.iloc[:26].mean()),'second_half':float(spread.iloc[26:].mean())}
    vals['saved_mean_difference']=vals['mean']-float(saved.loc[model,'mean_weekly_spread'])
    result[model]=vals
mom=pd.read_csv(base/'weekly_momentum_sort_returns.csv')
result['momentum']={'weeks':len(mom),'start':mom.forecast_week.iloc[0],'end':mom.forecast_week.iloc[-1],'spread_identity_max_error':float((mom['High-Low']-(mom.High-mom.Low)).abs().max()),'terminal_wealth':{c:float((1+mom[c]).prod()) for c in ['Low','Middle','High','High-Low']}}
f=np.array([.008,.004,-.002,-.006]); s=f-f.mean(); w=s/abs(s).sum(); r=np.array([.02,-.01,.01,-.03])
result['p21']={'mean':float(f.mean()),'demeaned':s.tolist(),'weights':w.tolist(),'gross':float(abs(w).sum()),'net':float(w.sum()),'contributions':(w*r).tolist(),'return':float(w@r)}
w27=np.array([.30,.20,-.25,-.25]); r27=np.array([.02,.04,-.02,0])
result['p27']={'gross':float(abs(w27).sum()),'net':float(w27.sum()),'contributions':(w27*r27).tolist(),'return':float(w27@r27)}
result['p25']={'correct':float((.003-.0005)/.018*np.sqrt(52)),'total_return_error':float(.003/.018*np.sqrt(52)),'times52_error':float((.003-.0005)/.018*52)}
result['p26']={'full_r2':1-80/200,'zeroed_r2':1-100/200,'loss':(100-80)/200}
result['p24']={'arithmetic_monthly':0,'wealth':1.1*.9,'cagr_if_two_months_only':(1.1*.9)**6-1,'sample_monthly_vol':float(np.std([.1,-.1],ddof=1))}
result['p20']={'weights':(np.array([.003,.001,-.001,-.003])/.008).tolist(),'return':float(np.array([.375,.125,-.125,-.375])@np.array([.02,.01,-.01,-.02]))}
tilt10=np.maximum(0,.25+10*s); tilt10=tilt10/tilt10.sum()
tilt50raw=np.full(4,.25)+50*s; tilt50=np.maximum(0,tilt50raw); tilt50=tilt50/tilt50.sum()
result['supplement']={'forecast_tilt_eta10':tilt10.tolist(),'forecast_tilt_eta50_raw':tilt50raw.tolist(),'forecast_tilt_eta50':tilt50.tolist(),'vol_k':[.01/.02,.01/.008],'rank_magnitude_mse':float(np.mean((np.array([.10,.20,.30])-np.array([.01,.02,.03]))**2)),'p21_d_changed_return':float(w@np.array([.02,-.01,.01,.03])),'p27_c_changed_return':float(w27@np.array([.02,.04,.02,0])),'two_positive_months_cagr':1.01**12-1,'two_month_sample_ann_vol':float(np.std([.1,-.1],ddof=1)*np.sqrt(12)),'recovery_return':1/1.1-1,'sharpe_rf_010':float((.003-.001)/.018*np.sqrt(52)),'p22_first_two_spread_wealth':float((1+mom['High-Low'].iloc[:2]).prod())}
(out/'recompute-portfolio.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
