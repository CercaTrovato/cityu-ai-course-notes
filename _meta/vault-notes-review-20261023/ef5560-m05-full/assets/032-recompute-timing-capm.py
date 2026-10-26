from pathlib import Path
import json, math
import numpy as np
import pandas as pd
import statsmodels.api as sm

base = Path(r'D:\上课资料\CityU\EF5560_Fintech_and_AI_in_Finance\course_files_export\class05\class05')
out = Path(r'E:\app-data\codex\scratchpad\ef5560-m05-20261008')
res = {}
df = pd.read_csv(base / 'model_portfolios_monthly.csv')
row = df.loc[df.forecast_month.eq('2023-08-31')].iloc[0]
res['aug2023'] = {k:float(row[k]) for k in ['Gradient boosting','volatility_12','Gradient boosting weight','market_total_return','risk_free_return','Gradient boosting portfolio return']}
res['aug2023']['weight_recomputed'] = float(np.clip(row['Gradient boosting']/(5*(row['volatility_12']/math.sqrt(12))**2),0,1))
res['aug2023']['return_recomputed'] = float(row['Gradient boosting weight']*row.market_total_return + (1-row['Gradient boosting weight'])*row.risk_free_return)
for s in ['Buy and hold','LASSO','Gradient boosting']:
    r = df[f'{s} portfolio return'].to_numpy()
    e = df[f'{s} portfolio excess return'].to_numpy()
    w = np.r_[1, np.cumprod(1+r)]
    res[s] = dict(cagr=float(w[-1]**(12/len(r))-1), vol=float(np.std(r,ddof=1)*math.sqrt(12)), sharpe=float(np.mean(e)/np.std(e,ddof=1)*math.sqrt(12)), mdd=float(np.min(w/np.maximum.accumulate(w)-1)), final_wealth=float(w[-1]))
capm = pd.read_csv(base/'three_market_capm_returns_monthly.csv')
res['capm'] = {}
for m, g in capm.groupby('market',sort=False):
    fit = sm.OLS(g.timing_excess_return, sm.add_constant(g.market_excess_return)).fit()
    res['capm'][m] = dict(n=len(g), alpha_monthly=float(fit.params.iloc[0]), alpha_annual=float(12*fit.params.iloc[0]), beta=float(fit.params.iloc[1]), t_ordinary=float(fit.tvalues.iloc[0]), r2=float(fit.rsquared), residual_mean=float(fit.resid.mean()))
res['p43'] = dict(cost=.001*(.3+.3),net_return=.003-.0006,net_excess=.003-.0006-.0005,SRgross=math.sqrt(52)*(.003-.0005)/.018,SRnet=math.sqrt(52)*(.003-.0006-.0005)/.018)
res['p49'] = dict(benchmark=.001+1.1*.01,abnormal=.014-(.001+1.1*.01))
res['p37_rounded'] = dict(weight=.00337/(5*(.1909/math.sqrt(12))**2),return_value=(.00337/(5*(.1909/math.sqrt(12))**2))*(-.0163)+(1-.00337/(5*(.1909/math.sqrt(12))**2))*.0045)
toywealth=np.r_[1,np.cumprod(1+np.array([-.1,.1,.1,-.2]))]
res['toy_drawdown'] = dict(wealth=toywealth.tolist(),drawdown=(toywealth/np.maximum.accumulate(toywealth)-1).tolist())
res['transfer'] = dict(weight=.006/(5*.04**2),clipped_weight=min(1,.006/(5*.04**2)),weight_gamma10=.006/(10*.04**2), SR_weekly_cost=.001*.6, zero_market_variance='must handle explicitly')
res['extra_examples'] = dict(log02_simple=math.expm1(.02),logminus02_simple=math.expm1(-.02),p42_gross=math.sqrt(52)*.002/.02,p42_net=math.sqrt(52)*.0016/.02,p43_cost20bp_sharpe=math.sqrt(52)*(.003-.0012-.0005)/.018,variance4to8_weight=.006/(5*.08**2),hsi_weight_sum=8.91+7.67+7.11+5.47+4.79)
res['extra_examples'].update(assignment_score_sum=sum([10,35,15,15,5,20]),training_rows=78*80,validation_rows=26*80,private_rows=156*80,hsi_annmean_from_held=12*25/60*(-.009463265283173755),csi_annmean_from_held=12*50/60*.001833527609632229,declines_twice=(1-.1)**2-1)
x=np.array([-.01,0,.01]); y=np.array([-.008,.001,.013])
fittoy=sm.OLS(y,sm.add_constant(x)).fit()
res['toy_ols']=dict(alpha=float(fittoy.params[0]),beta=float(fittoy.params[1]),fitted=fittoy.fittedvalues.tolist(),residuals=fittoy.resid.tolist())
stocks=pd.read_csv(base/'hsi_stock_excess_return_panel.csv')
res['stock_capm']={}
for tick in ['0005.HK','0700.HK','9988.HK','0939.HK','1299.HK']:
    g=stocks.loc[stocks.ticker.eq(tick), ['excess_return','market_return','risk_free_return']].dropna()
    fit=sm.OLS(g.excess_return,sm.add_constant(g.market_return-g.risk_free_return)).fit(cov_type='HAC',cov_kwds={'maxlags':4})
    res['stock_capm'][tick]=dict(n=len(g),alpha_annual=float(fit.params.iloc[0]*52),beta=float(fit.params.iloc[1]),t_nw4=float(fit.tvalues.iloc[0]),r2=float(fit.rsquared))
(out/'recompute-timing-capm-results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(res,ensure_ascii=False,indent=2))
