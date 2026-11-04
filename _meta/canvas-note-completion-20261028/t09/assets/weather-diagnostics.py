import pathlib,json,warnings,pandas as pd,numpy as np
import matplotlib;matplotlib.use('Agg')
from matplotlib import pyplot as plt
from statsmodels.tsa.stattools import kpss,acf,pacf
T=pathlib.Path('E:/app-data/codex/scratchpad/cityu-notes-20261028');p=pathlib.Path('D:/上课资料/CityU/IS6400_Business_Data_Analytics/course_files_export/weather.csv')
d=pd.read_csv(p);dt=pd.to_datetime(d['Date Time'],format='%d.%m.%Y %H:%M:%S');s=pd.Series(d['T (degC)'].to_numpy(),index=dt).resample('MS').mean();train=s.iloc[:-12]
with warnings.catch_warnings(record=True) as ws:
    warnings.simplefilter('always');stat,pval,lags,crit=kpss(train,regression='c',nlags='auto')
out={'KPSS_train':{'statistic':float(stat),'pvalue':float(pval),'lags':int(lags),'critical_values':crit},'ACF_train':acf(train,nlags=24).tolist(),'PACF_train':pacf(train,nlags=24).tolist(),'warnings':[str(w.message) for w in ws],'negative_values':int((train<0).sum()),'zero_values':int((train==0).sum())}
(T/'weather-diagnostics.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
r=json.loads((T/'t09-execution.json').read_text(encoding='utf-8'))['weather_reference'];dates=s.iloc[-12:].index
plt.figure(figsize=(10,5));plt.plot(dates,r['actual'],'ko-',label='Actual');plt.plot(dates,r['ARIMA100'],label='ARIMA(1,0,0)');plt.plot(dates,r['seasonal_naive'],label='Seasonal naive');plt.ylabel('Monthly temperature (degrees C)');plt.legend();plt.tight_layout();plt.savefig(T/'t09-weather.svg');plt.savefig(T/'t09-weather.png',dpi=120)
print(json.dumps({'KPSS':out['KPSS_train'],'ACF12':out['ACF_train'][12],'PACF1':out['PACF_train'][1],'negative_months':out['negative_values']},ensure_ascii=False))
