"""Reference for the Cell 82 pipeline. Run from its final notes/figures folder.
Outputs stay outside the course vault. This file is not a submitted assignment.
"""
import os,pathlib,json,warnings
import pandas as pd
import matplotlib;matplotlib.use('Agg')
from matplotlib import pyplot as plt
from statsmodels.tsa.stattools import kpss,acf,pacf
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import root_mean_squared_error
if '__file__' in globals():
    course=pathlib.Path(__file__).resolve().parents[3]
else:
    # Notebook users on this verified machine: adjust this explicit course path if relocated.
    course=pathlib.Path('D:/上课资料/CityU/IS6400_Business_Data_Analytics')
assert (course/'course_files_export/weather.csv').is_file(), 'Set course to the directory containing course_files_export'
out=pathlib.Path(os.environ.get('CITYU_WEATHER_OUTPUT','E:/app-data/codex/scratchpad/cityu-weather-reference'));out.mkdir(parents=True,exist_ok=True)
weather=pd.read_csv(course/'course_files_export/weather.csv')
weather['date']=pd.to_datetime(weather['Date Time'],format='%d.%m.%Y %H:%M:%S')
monthly=weather.set_index('date')['T (degC)'].resample('MS').mean()
assert not monthly.isna().any(), 'Monthly gaps require explicit handling'
train,test=monthly.iloc[:-12],monthly.iloc[-12:]
# Temperature has negative values: no unshifted Box-Cox. Diagnose only the training period.
with warnings.catch_warnings(record=True) as ws:
    warnings.simplefilter('always');stat,pval,lags,critical=kpss(train,regression='c',nlags='auto')
acf_values=acf(train,nlags=24);pacf_values=pacf(train,nlags=24)
# This fixed non-seasonal model is an illustrative candidate, not test-selected best order.
fit=ARIMA(train,order=(1,0,0)).fit();pred=fit.forecast(12)
seasonal_naive=monthly.iloc[-24:-12].to_numpy()
results={'training_KPSS':{'stat':float(stat),'p':float(pval),'lags':int(lags)},'acf12':float(acf_values[12]),'pacf1':float(pacf_values[1]),'warnings':[str(w.message) for w in ws],'ARIMA100_RMSE_C':float(root_mean_squared_error(test,pred)),'seasonal_naive_RMSE_C':float(root_mean_squared_error(test,seasonal_naive))}
plt.figure(figsize=(10,5));plt.plot(test.index,test,'ko-',label='Actual');plt.plot(test.index,pred,label='ARIMA(1,0,0)');plt.plot(test.index,seasonal_naive,label='Seasonal naive');plt.ylabel('Monthly temperature (degrees C)');plt.legend();plt.tight_layout();plt.savefig(out/'weather-comparison.svg')
(out/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
