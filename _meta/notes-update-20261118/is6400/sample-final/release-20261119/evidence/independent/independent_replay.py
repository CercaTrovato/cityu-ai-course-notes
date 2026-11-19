from pathlib import Path
import sys,json,hashlib,subprocess,importlib.util,itertools,math,re
import numpy as np,pandas as pd,sklearn,statsmodels,openpyxl
S=Path(__file__).resolve().parent;A=S.parent/'dot-author';R=Path('D:/上课资料/CityU')
# Independently transcribed after actually viewing the three images extracted from archived DOCX.
train=[(0,0,0,0,4,0),(0,0,0,1,0,1),(0,0,1,0,0,1),(0,1,0,1,0,1),(1,0,1,0,3,0),(1,1,0,1,0,5)]
valid=[(0,0,0,1,4,0),(0,0,1,1,3,0),(0,1,0,0,0,1),(0,1,1,0,0,2),(1,0,0,0,2,0),(1,0,0,1,3,0)]
tree=(0,(1,(2,(3,'+','-'),'-'),'-'),(1,'+','-'))
def variants(t,rows):
    if isinstance(t,str):return [t]
    f,l,r=t;p=sum(x[4] for x in rows);n=sum(x[5] for x in rows);assert p!=n
    out=['+' if p>n else '-']
    for x,y in itertools.product(variants(l,[a for a in rows if a[f]==0]),variants(r,[a for a in rows if a[f]==1])):out.append((f,x,y))
    return out
def pred(t,r):return t if isinstance(t,str) else pred(t[1+int(r[t[0]])],r)
def leaves(t):return 1 if isinstance(t,str) else leaves(t[1])+leaves(t[2])
models=[]
for t in variants(tree,train):
    tr=[r[5] if pred(t,r)=='+' else r[4] for r in train];va=[r[5] if pred(t,r)=='+' else r[4] for r in valid]
    L=leaves(t);e=sum(tr);v=sum(va);models.append({'tree':t,'leaves':L,'train_errors':e,'validation_errors':v,'pessimistic_percent':100*(e+L)/15,'train_row_errors':tr,'validation_row_errors':va})
assert len(models)==9
expected={(6,0,7),(5,1,3),(4,2,0),(3,3,3),(5,3,12),(4,4,8),(3,5,5),(2,6,8),(1,7,12)}
assert {(x['leaves'],x['train_errors'],x['validation_errors']) for x in models}==expected
(S/'tree-independent.json').write_text(json.dumps({'source':'actual archivedDOCX image1/2/3 visually read; manually entered by reviewer','training':train,'validation':valid,'models':models,'count':len(models)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
replay=S/'author-replay';replay.mkdir(exist_ok=True)
logs=[]
for label,args in [('tree',['--output',str(replay)]),('missing-q1',['--q1',str(S/'ORIGINAL_Q1_NOT_PRESENT.xlsx'),'--output',str(replay)]),('missing-btc',['--btc',str(S/'ORIGINAL_BTC_NOT_PRESENT.csv'),'--output',str(replay)])]:
    p=subprocess.run([sys.executable,'-B','-X','utf8',str(A/'reproduce.py'),*args],capture_output=True,text=True,encoding='utf-8');(S/(label+'-replay.txt')).write_text(p.stdout+p.stderr,encoding='utf-8');logs.append({'label':label,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
assert [x['exit'] for x in logs]==[0,2,2]
author=json.loads((replay/'tree-recalculated.json').read_text(encoding='utf-8'))
assert {(x['leaves'],x['train_errors'],x['validation_errors']) for x in author['models']}==expected
spec=importlib.util.spec_from_file_location('author_sample_reproduce_readonly',A/'reproduce.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
toy=S/'synthetic-tests';toy.mkdir(exist_ok=True)
q=toy/'synthetic-Q1-not-course-data.xlsx';pd.DataFrame({'Churn':['Yes',' ','No',None],'LastTransaction':[10,20,30,40]}).to_excel(q,index=False)
qres=mod.q1_summary(q);assert qres['missing_churn']==2 and qres['valid_LastTransaction']==4 and qres['IQR']==15
badq=toy/'synthetic-invalid-money.xlsx';pd.DataFrame({'Churn':['Yes'],'LastTransaction':['oops']}).to_excel(badq,index=False)
try:mod.q1_summary(badq);raise AssertionError('invalid value accepted')
except ValueError as e:badq_error=str(e)
dates=pd.date_range('2013-04-30','2018-04-30',freq='D');deltas=[2.0]
for i in range(1,len(dates)):deltas.append(.3+.7*deltas[-1]+.2*math.sin(i*.3))
prices=100+np.cumsum(deltas);btc=toy/'synthetic-BTC-not-course-data.csv';pd.DataFrame({'Date':dates,'Close':prices}).to_csv(btc,index=False)
forecast,meta=mod.btc_forecast(btc);c,phi=meta['parameters'];d=float(prices[-1]-prices[-2]);manual=[];v=float(prices[-1])
for i in range(5):d=c+phi*d;v+=d;manual.append(v)
assert np.allclose(forecast['Forecast'],manual) and list(forecast['Trading date'])==['2018-05-01','2018-05-02','2018-05-03','2018-05-04','2018-05-05']
badbtc=toy/'synthetic-missing-day.csv';pd.DataFrame({'Date':dates,'Close':prices}).drop(index=40).to_csv(badbtc,index=False)
try:mod.btc_forecast(badbtc);raise AssertionError('missing date accepted')
except ValueError as e:badbtc_error=str(e)
from sklearn.tree import DecisionTreeClassifier
models8=[DecisionTreeClassifier(max_depth=n,random_state=42) for n in [7,8]]
assert [m.get_params()['max_depth'] for m in models8]==[7,8]
hits=[]
roots=[R/'IS6400_Business_Data_Analytics',S.parent]
for root in roots:
    for p in root.rglob('*'):
        if p.is_file() and (re.fullmatch('Q1\\.xlsx',p.name,re.I) or re.fullmatch('Q4[ _-]*BTC.*\\.csv',p.name,re.I)):hits.append(str(p))
result={'executor':'/root/cityu_closeout_inventory','independent_tree_count':9,'matches_candidate_and_actual_author_tree_run':True,'actual_author_replay_exit_codes':[{'label':x['label'],'exit':x['exit']} for x in logs],'synthetic_only_not_original_Q1':qres,'invalid_money_rejected':badq_error,'synthetic_only_not_original_BTC':{'n_prices':meta['n_prices'],'dates':list(forecast['Trading date']),'actual_statsmodels_forecast_matches_manual_recursion':True,'no_original_BTC_answer_claim':True},'missing_day_rejected':badbtc_error,'sklearn_parameters_instantiated':[7,8],'versions':{'numpy':np.__version__,'pandas':pd.__version__,'sklearn':sklearn.__version__,'statsmodels':statsmodels.__version__,'openpyxl':openpyxl.__version__},'bounded_original_input_search':{'roots':[str(x) for x in roots],'filename_matches':hits,'limit':'No claim for unchecked OS locations/cloud; original DOCX package has no embeddeddata objects'},'source_candidate_hash':hashlib.sha256((A/'sample-final-learning.md').read_bytes()).hexdigest()}
(S/'execution-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
