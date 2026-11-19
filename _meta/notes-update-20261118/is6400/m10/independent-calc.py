from pathlib import Path
import json, hashlib, math, statistics
from scipy.stats import t
root=Path('D:/上课资料/CityU')
e=root/'_meta/notes-update-20261118/is6400/m10'
sx=[1.0,2.9,3.3,4.9,5.6,6.3,7.2,8.3,9.7,10.5,11.5,12.8,13.0,14.7,15.7,16.2,17.5,18.6,19.4,20.2]
sy=[3.3,9.8,10.3,14.8,16.8,19.8,21.8,25.2,29.6,31.8,35.1,38.7,39.9,44.2,47.8,49.0,52.9,56.7,58.5,61.2]
def fitcheck(x,y,ids):
    tr=[i for i in range(len(x)) if i+1 not in ids]
    mx=statistics.mean(x[i] for i in tr); my=statistics.mean(y[i] for i in tr)
    slope=sum((x[i]-mx)*(y[i]-my) for i in tr)/sum((x[i]-mx)**2 for i in tr)
    intercept=my-slope*mx
    errs=[y[i-1]-(intercept+slope*x[i-1]) for i in ids]
    return dict(intercept=intercept,slope=slope,validation_rid=ids,errors=errs,mae=statistics.mean(abs(v) for v in errs),rmse=math.sqrt(statistics.mean(v*v for v in errs)))
left=[(3,1),(2,1),(0,2),(1,2),(3,0),(3,1),(0,5)]
right=[(5,2),(1,4),(3,0),(3,6)]
A=[8,9,10,11,12]; B=[10,11,12,13,14]
va=statistics.variance(A);vb=statistics.variance(B);na=len(A);nb=len(B)
se=math.sqrt(va/na+vb/nb); df=(va/na+vb/nb)**2/((va/na)**2/(na-1)+(vb/nb)**2/(nb-1));tt=(statistics.mean(B)-statistics.mean(A))/se
figs=json.loads((e/'source-figures.json').read_text(encoding='utf-8'))
bad=[]
for f in figs:
    p=root/f['path']
    if hashlib.sha256(p.read_bytes()).hexdigest()!=f['sha256']: bad.append(f['page'])
result={
 'method':'Independent literal transcription from viewed source table; closed-form scalar least squares; scipy t survival function. No author calculation code executed.',
 'source_inputs':dict(x=sx,y=sy),
 'holdout':fitcheck(sx,sy,[4,6,7,12]),
 'quiz_3fold':[fitcheck(sx[1:10],sy[1:10],ids) for ids in [[1,2,3],[4,5,6],[7,8,9]]],
 'metrics':dict(mae=3,mean_error=1,mape=.2,sse=20,rmse=math.sqrt(10),precision=8/12,recall=8/10,f1=16/22,auc=sum(p>n for p in [.9,.4] for n in [.6,.1])/4),
 'cv':dict(mean=statistics.mean([2,3,4,3,3]),sample_std=statistics.stdev([2,3,4,3,3])),
 'tree61':dict(n_left=sum(sum(v) for v in left),n_right=sum(sum(v) for v in right),errors_left=sum(min(v) for v in left),errors_right=sum(min(v) for v in right),penalty_left=(4+7)/24,penalty_right=(6+4)/24,half_penalty_left=(4+.5*7)/24,half_penalty_right=(6+.5*4)/24,tie=2/3),
 'tree64':dict(before=(10+.5)/30,after=(4+3+1+1+4*.5)/30),
 'clusters':dict(wss=sum((v-c)**2 for v,c in [(0,1),(2,1),(8,9),(10,9)]),bss=2*(1-5)**2+2*(9-5)**2,tss=sum((v-5)**2 for v in [0,2,8,10])),
 'ab':dict(mean_a=statistics.mean(A),mean_b=statistics.mean(B),var_a=va,var_b=vb,se=se,t=tt,df=df,p=2*t.sf(abs(tt),df),p_reversed=2*t.sf(abs(-tt),df)),
 'weighted_mae':(90*1+10*9)/100,
 'figure_manifest':dict(entries=len(figs),sha_mismatch_pages=bad),
 'page_manifest':dict(entries=len(json.loads((e/'page-evidence.json').read_text(encoding='utf-8'))['pages']))
}
out=Path('E:/app-data/codex/scratchpad/cityu-notes-20261118/is6400/m10/independent-calculations.json')
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
