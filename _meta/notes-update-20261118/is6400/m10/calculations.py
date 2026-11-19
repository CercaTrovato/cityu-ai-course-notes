from pathlib import Path
import numpy as np,json,sys
from scipy.stats import ttest_ind
R=Path('D:/上课资料/CityU');P=R/'_meta/notes-update-20261118/is6400/m10';sys.path.insert(0,str(R/'_meta/tools'));from safe_write import atomic_write
x=np.array([1,2.9,3.3,4.9,5.6,6.3,7.2,8.3,9.7,10.5,11.5,12.8,13,14.7,15.7,16.2,17.5,18.6,19.4,20.2]);y=np.array([3.3,9.8,10.3,14.8,16.8,19.8,21.8,25.2,29.6,31.8,35.1,38.7,39.9,44.2,47.8,49,52.9,56.7,58.5,61.2]);valid=np.array([3,5,6,11]);train=np.array([i for i in range(20) if i not in valid]);coef=np.linalg.lstsq(np.c_[np.ones(len(train)),x[train]],y[train],rcond=None)[0];pred=np.c_[np.ones(len(valid)),x[valid]]@coef;err=y[valid]-pred
leaves_l=[(3,1),(2,1),(0,2),(1,2),(3,0),(3,1),(0,5)];leaves_r=[(5,2),(1,4),(3,0),(3,6)]
folds=[]
xq=np.array([2.9,3.3,4.9,5.6,6.3,7.2,8.3,9.7,10.5]);yq=np.array([9.8,10.3,14.8,16.8,19.8,21.8,25.2,29.6,31.8])
for v in [[0,1,2],[3,4,5],[6,7,8]]:
 tr=[k for k in range(9) if k not in v];c=np.linalg.lstsq(np.c_[np.ones(6),xq[tr]],yq[tr],rcond=None)[0];e=yq[v]-np.c_[np.ones(3),xq[v]]@c;folds.append(dict(train_rid=[k+1 for k in tr],valid_rid=[k+1 for k in v],intercept=c[0],slope=c[1],mae=float(np.abs(e).mean())))
ab=ttest_ind([10,11,12,13,14],[8,9,10,11,12],equal_var=False)
out=dict(holdout=dict(intercept=coef[0],slope=coef[1],validation_rid=(valid+1).tolist(),predictions=pred.tolist(),errors=err.tolist(),mae=float(np.abs(err).mean()),rmse=float(np.sqrt((err**2).mean()))),quiz_3fold=folds,metrics=dict(errors=[-2,4],mae=3,average=1,mape=.2,sse=20,rmse=np.sqrt(10)),cv=dict(mean=3,sample_std=float(np.std([2,3,4,3,3],ddof=1))),tree61=dict(n_l=sum(a+b for a,b in leaves_l),n_r=sum(a+b for a,b in leaves_r),errors_l=sum(min(a,b) for a,b in leaves_l),errors_r=sum(min(a,b) for a,b in leaves_r),penalty_l=(4+7)/24,penalty_r=(6+4)/24,omega_tie=2/3),tree64=dict(before=(10+.5)/30,after=(9+4*.5)/30),wss_bss=dict(points=[0,2,8,10],centers=[1,9],global_mean=5,wss=4,bss=64,tss=68),ab=dict(mean_a=10,mean_b=12,var_a=2.5,var_b=2.5,n_a=5,n_b=5,se=1,t=float(ab.statistic),two_sided_p=float(ab.pvalue),df=8))
atomic_write(str(P/'calculations.json'),json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
