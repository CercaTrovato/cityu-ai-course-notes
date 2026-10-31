import os,pathlib,json,sys,io,contextlib,warnings,shutil
import numpy as np,pandas as pd,scipy,sklearn,statsmodels
import matplotlib; matplotlib.use('Agg')
from matplotlib import pyplot as plt
from scipy.stats import boxcox
from scipy.special import inv_boxcox
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
from sklearn.metrics import root_mean_squared_error
ROOT=pathlib.Path(__file__).resolve().parents[4]; TASK=pathlib.Path(os.environ.get('CITYU_REPRO_OUTPUT','E:/app-data/codex/scratchpad/cityu-t09-reproduction')); TASK.mkdir(parents=True,exist_ok=True); WORK=TASK/'t09-run';WORK.mkdir(exist_ok=True)
source=ROOT/'IS6400_Business_Data_Analytics/course_files_export'
for name in ['heater.csv','weather.csv']: shutil.copy2(source/name,WORK/name)
os.chdir(WORK)
nb=json.loads((source/'Week 9 Time series II_Tutorial.ipynb').read_text(encoding='utf-8')); env={}; rows=[]
for i,c in enumerate(nb['cells'],1):
    if c['cell_type']!='code': continue
    src=''.join(c['source']); src='\n'.join(l for l in src.splitlines() if not l.startswith('%'))
    buf=io.StringIO()
    try:
        with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):exec(compile(src,f'cell-{i}','exec'),env)
        rows.append({'cell':i,'status':'executed','output':buf.getvalue()[-2500:]})
        print(f'cell {i} executed',flush=True)
    except Exception as e:
        rows.append({'cell':i,'status':'failed','error':repr(e)});print(rows[-1],flush=True);break
    finally: plt.close('all')
out={'versions':{'python':sys.version,'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__,'sklearn':sklearn.__version__,'statsmodels':statsmodels.__version__},'original_cells':rows,'original_metrics':{k:float(env[k]) for k in ['rmse_arma','rmse_arima','rmse_sarima','rmse_hw'] if k in env},'original_lambda':float(env['lmbda']) if 'lmbda' in env else None}
(TASK/'t09-execution.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
if any(r['status']=='failed' for r in rows):sys.exit(1)
h=pd.read_csv(WORK/'heater.csv'); h['date']=pd.to_datetime(h.year_month); y=h.demand.to_numpy(dtype=float);n=len(y)-12; tr,te=y[:n],y[n:]
z,lam=boxcox(tr); zte=boxcox(te,lmbda=lam); month=h.date.dt.month.to_numpy(); mm={m:float(np.mean(z[month[:n]==m])) for m in range(1,13)};ds=z-np.array([mm[m] for m in month[:n]])
preds={};diagnostics={}
with warnings.catch_warnings(record=True) as ws:
    warnings.simplefilter('always')
    for name,values,kwargs in [('ARMA',np.diff(ds),{'order':(2,0,1)}),('ARIMA',ds,{'order':(2,1,1)}),('SARIMA',z,{'order':(2,1,1),'seasonal_order':(1,0,3,12)})]:
        fit=ARIMA(values,**kwargs).fit(); p=np.asarray(fit.forecast(12)); diagnostics[name]=getattr(fit,'mle_retvals',{})
        if name=='ARMA':p=ds[-1]+np.cumsum(p)
        if name in ['ARMA','ARIMA']:p=p+np.array([mm[m] for m in month[n:]])
        preds[name]=inv_boxcox(p,lam)
        print(name+' train-only done',flush=True)
    fit=ETSModel(z,trend='add',seasonal='add',seasonal_periods=12).fit(disp=False);preds['ETS']=inv_boxcox(np.asarray(fit.forecast(12)),lam)
    diagnostics['ETS']=getattr(fit,'mle_retvals',{})
    diagnostics['warnings']=list(dict.fromkeys(str(w.message) for w in ws))
out['train_only']={'lambda':float(lam),'train_count':n,'test_count':12,'train_dates':[str(h.date.iloc[0].date()),str(h.date.iloc[n-1].date())],'test_dates':[str(h.date.iloc[n].date()),str(h.date.iloc[-1].date())],'monthly_means':mm,'raw_unit_rmse':{k:float(root_mean_squared_error(te,p)) for k,p in preds.items()},'predictions':{k:p.tolist() for k,p in preds.items()},'actual':te.tolist(),'diagnostics':diagnostics,'point_forecast_limit':'Inverse Box-Cox of conditional transformed forecast is not an unbiased estimate of raw-scale conditional mean.'}
plt.figure(figsize=(10,5));plt.plot(h.date.iloc[n:],te,'ko-',label='Actual')
for k,p in preds.items():plt.plot(h.date.iloc[n:],p,label=k)
plt.ylabel('Heater demand (original units)');plt.legend();plt.tight_layout();plt.savefig(TASK/'t09-forecast.svg');plt.savefig(TASK/'t09-forecast.png',dpi=120);plt.close()
w=pd.read_csv(WORK/'weather.csv'); w['date']=pd.to_datetime(w['Date Time'],format='%d.%m.%Y %H:%M:%S');s=w.set_index('date')['T (degC)'].resample('MS').mean(); wt,wy=s.iloc[:-12],s.iloc[-12:]
wf=ARIMA(wt,order=(1,0,0)).fit();wp=wf.forecast(12);base=s.iloc[-24:-12].to_numpy();out['weather_reference']={'selected_variable':'T (degC)','frequency':'monthly means; available records only, boundary months may be partial','months':len(s),'train_months':len(wt),'test_months':len(wy),'train_dates':[str(wt.index[0].date()),str(wt.index[-1].date())],'test_dates':[str(wy.index[0].date()),str(wy.index[-1].date())],'missing_months':int(s.isna().sum()),'ARIMA100_RMSE_C':float(root_mean_squared_error(wy,wp)),'seasonal_naive_RMSE_C':float(root_mean_squared_error(wy,base)),'actual':wy.tolist(),'ARIMA100':wp.tolist(),'seasonal_naive':base.tolist(),'source_rows':len(w),'monthly_observation_counts':w.set_index('date')['T (degC)'].resample('MS').count().to_dict(),'protocol':'Fixed illustrative ARIMA(1,0,0), no test-driven tuning; seasonal naive uses last observed same month, no fitting.'}
out['weather_reference']['monthly_observation_counts']={str(k.date()):int(v) for k,v in out['weather_reference']['monthly_observation_counts'].items()}
(TASK/'t09-execution.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=lambda x:x.tolist() if hasattr(x,'tolist') else str(x)),encoding='utf-8')
print(json.dumps({'original_metrics':out['original_metrics'],'corrected_metrics':out['train_only']['raw_unit_rmse'],'weather':{k:v for k,v in out['weather_reference'].items() if not isinstance(v,(dict,list))}},ensure_ascii=False),flush=True)
