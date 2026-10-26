from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import t

base=Path(r'D:\上课资料\CityU\EF5560_Fintech_and_AI_in_Finance\course_files_export\class05\class05')
out=Path(r'E:\app-data\codex\scratchpad\ef5560-readable-20261008')
d=pd.read_csv(base/'stock_linear_test_predictions.csv')
d['q']=d.groupby('forecast_week').OLS.transform(lambda s: pd.qcut(s.rank(method='first'),5,labels=False)+1)
g=d.groupby(['forecast_week','q']).stock_return.mean().unstack()
x=g[5]-g[1]
mean=float(x.mean()); sd=float(x.std(ddof=1)); se=sd/np.sqrt(len(x)); statistic=mean/se
r={'n':len(x),'mean_decimal':mean,'mean_percent':100*mean,'sample_sd_decimal':sd,'sample_sd_percent':100*sd,'mean_se_decimal':se,'mean_se_percent':100*se,'sqrt_n':float(np.sqrt(len(x))),'t_statistic':float(statistic),'degrees_freedom':len(x)-1,'two_sided_5pct_critical':float(t.ppf(.975,len(x)-1)),'two_sided_p_if_iid_normal':float(2*t.sf(abs(statistic),len(x)-1)),'positive_weeks':int((x>0).sum()),'positive_fraction':float((x>0).mean()),'first_half_mean_percent':100*float(x.iloc[:26].mean()),'second_half_mean_percent':100*float(x.iloc[26:].mean()),'mean_difference_hkd_per_million':1e6*mean}
(out/'portfolio-t-recompute.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(r,ensure_ascii=False,indent=2))
