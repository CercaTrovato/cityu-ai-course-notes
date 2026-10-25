from pathlib import Path
import json,re,hashlib,difflib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression,Lasso
OUT=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61/reviewer')
DATA=Path('D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance/course_files_export/class03/class03')
r={}
dev=np.array([[0,0],[1,1],[2,0],[3,1]],float); y=np.arange(4.)
val=np.array([[4,0],[5,1]],float); vy=np.array([3,4.])
r['forward_selection']={'empty_validation_mse':float(np.mean((vy-y.mean())**2)),'candidates':{}}
for cols,name in [([0],'x1'),([1],'x2'),([0,1],'both')]:
    model=LinearRegression().fit(dev[:,cols],y)
    r['forward_selection']['candidates'][name]={'coef':model.coef_.tolist(),'validation_pred':model.predict(val[:,cols]).tolist(),'mse':float(np.mean((vy-model.predict(val[:,cols]))**2))}
refit=LinearRegression().fit(np.r_[dev[:,[0]],val[:,[0]]],np.r_[y,vy])
r['forward_selection']['refit_new6']=float(refit.predict([[6]])[0])
G=np.array([[1,.5],[.5,1]]);c=np.array([.4,.4]);b=np.zeros(2);log=[]
for k in range(1,31):
    previous=b.copy()
    for j in range(2):
        u=c[j]-(G[j]@b-G[j,j]*b[j]);b[j]=np.sign(u)*max(abs(u)-.1,0)/G[j,j]
    gradient=G@b-c; kkt=np.max(np.abs(gradient+.1*np.sign(b)));change=np.max(abs(b-previous))
    log.append({'round':k,'beta':b.tolist(),'change':float(change),'kkt':float(kkt)})
    if change<=1e-5 and kkt<=1e-5:break
r['lasso_coordinate']=log
r['ridge_two_columns']={str(lam):np.linalg.solve(G+lam*np.eye(2),c).tolist() for lam in [0,.1,.5]}
X=np.array([[2,1],[1,2],[-1,-2],[-2,-1]],float);target=np.array([1,-1,1,-1.]);sd=X.std(0,ddof=1);Z=X/sd
wp=np.array([1,1])/np.sqrt(2);wm=np.array([1,-1])/np.sqrt(2);tp=Z@wp;tm=Z@wm;q=tm@target/(tm@tm)
r['pcr_pls']={'sample_sd':sd.tolist(),'t_plus':tp.tolist(),'t_minus':tm.tolist(),'variances':[float(tp.var(ddof=1)),float(tm.var(ddof=1))],'pcr_sse':float(np.square(target).sum()),'pls_q':float(q),'pls_new3_1':float(np.array([3,1])/sd@wm*q)}
r['unit_change_counterexample']={}
for scale in [1,100]:
    model=Lasso(alpha=.5,fit_intercept=False,max_iter=100000).fit(np.array([[-1.],[1.]])*scale,[-1.,1.])
    r['unit_change_counterexample'][str(scale)]={'coef':float(model.coef_[0]),'pred_for_raw_x1':float(model.predict([[scale]])[0])}
panel=pd.read_csv(DATA/'hsi_stock_excess_return_panel.csv')
d=panel.loc[panel.split.eq('development') & panel.usable_for_ml].copy()
r['characteristic_sorts_week_equal_mean_percent']={}
for col in ['mom20d_rank','close_vs_sma20d_rank','rv20d_rank','illiq20d_rank']:
    temp=d.dropna(subset=[col,'excess_return']).copy()
    temp['q']=temp.groupby('forecast_week')[col].transform(lambda s:pd.qcut(s.rank(method='first'),5,labels=False)+1)
    w=temp.groupby(['forecast_week','q']).excess_return.mean().unstack()
    r['characteristic_sorts_week_equal_mean_percent'][col]=(w.mean()*100).tolist()
mp=pd.read_csv(DATA/'market_linear_test_predictions.csv');us=mp.loc[mp.market.eq('U.S.')]
r['US_saved_lasso_range']={'min':float(us.LASSO.min()),'max':float(us.LASSO.max()),'min_month':us.loc[us.LASSO.idxmin(),'forecast_month']}
asr=Path('D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance/transcripts/M03-transcript.txt').read_text(encoding='utf-8-sig')
stamps=re.findall(r'(?m)^\s*((?:\d+:)?\d{2}:\d{2})\s*$',asr)
r['M03_timestamps']={'records':len(stamps),'unique':len(set(stamps)),'duplicate_stamps':sorted(set(x for x in stamps if stamps.count(x)>1))}
cand=(OUT.parent/'candidate.md').read_text(encoding='utf-8-sig');base=(OUT.parent/'formal-baseline.md.snapshot').read_text(encoding='utf-8-sig')
r['issue_origins']={}
needles={'B3':'最终的斜率会比 OLS 小','B4':'否（方向内全非零）','B5':'输入矩阵的行空间','B6':'把模型 B 改成','B8':'百分数版的斜率是小数版的 1/100','B9':'那一列在那周对预测无贡献','B10':'再把这些值套到验证和测试数据上','B11':'所有模型都会被比成负数'}
for key,needle in needles.items():
    r['issue_origins'][key]={'needle':needle,'in_baseline':needle in base,'in_candidate':needle in cand}
(OUT/'additional-calculations.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(r,ensure_ascii=False,indent=2))
