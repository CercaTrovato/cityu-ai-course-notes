import hashlib,json,re,subprocess,sys
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from PIL import Image,ImageDraw
B=Path(__file__).parent; O=B/'main-source';O.mkdir(exist_ok=True)
R=Path('D:/上课资料/CityU');C=R/'EF5560_Fintech_and_AI_in_Finance';data=C/'course_files_export/class02/class02'
sys.path.insert(0,str(R/'_meta/tools'))
from safe_write import atomic_write
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def js(p,x):atomic_write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
src=(B/'recompute_review.py').read_text(encoding='utf-8');old='OUT = Path(r"E:/app-data/codex/scratchpad/vault-notes-revision-20261023/ef5560-m02/recompute-results.json")'
assert src.count(old)==1
clone=O/'recompute-main.py';atomic_write(clone,src.replace(old,'OUT = Path(r"'+(O/'recompute-main-results.json').as_posix()+'")'))
p=subprocess.run([sys.executable,'-X','utf8',str(clone)],capture_output=True,text=True,encoding='utf-8',check=True)
atomic_write(O/'recompute-main.log',p.stdout+p.stderr)
calc=json.loads((O/'recompute-main-results.json').read_text(encoding='utf-8'))
assert all(x['match'] for x in calc['hash_checks'].values())
d=pd.read_csv(data/'market_features.csv',parse_dates=['forecast_month']).sort_values('forecast_month')
predictors=['momentum_12','volatility_12','ma_gap_10'];train=d[d.forecast_month<'2021-07-01'].copy();test=d[d.forecast_month>='2021-07-01'].copy()
mu=train[predictors].mean();sd=train[predictors].std();fit3=sm.OLS(train.market_return,sm.add_constant((train[predictors]-mu)/sd,has_constant='add')).fit()
text=(B/'candidate.md').read_text(encoding='utf-8')
block=next(b for b in re.findall(r'```python\n([\s\S]*?)```',text) if b.startswith('X_test = (test[predictors] - mu) / sd'))
scope={'test':test,'predictors':predictors,'mu':mu,'sd':sd,'sm':sm,'fit3':fit3,'np':np};exec(compile(block,'candidate-exact-forecast-block','exec'),scope)
pred=scope['prediction'];assert len(pred)==60 and np.isfinite(pred).all()
ref=pd.read_csv(data/'spy_test_predictions_monthly.csv')
assert np.allclose(pred,ref['forecast'])
full_fit=sm.OLS(train.market_return,sm.add_constant((train[predictors]-d[predictors].mean())/d[predictors].std(),has_constant='add')).fit()
full_pred=full_fit.predict(sm.add_constant((test[predictors]-d[predictors].mean())/d[predictors].std(),has_constant='add'))
w=ref['timing_weight'] if 'timing_weight' in ref else ref['weight'] if 'weight' in ref else None
if w is None:
 weight_columns=[x for x in ref.columns if 'weight' in x or 'position' in x];assert len(weight_columns)==1,ref.columns;w=ref[weight_columns[0]]
g=ref['market_return'] if 'market_return' in ref else ref['actual_return'] if 'actual_return' in ref else test.market_return.reset_index(drop=True)
correct_wealth=float(np.prod(1+w*np.expm1(g)));bad_wealth=float(np.prod(1+w*g));bh=float(np.exp(g.sum()))
assert np.isclose(correct_wealth,1.645882222,atol=1e-9)
develop=np.array([[1,0],[1,1],[1,2]],float);dy=np.array([1,2,2],float)
beta=np.linalg.lstsq(develop,dy,rcond=None)[0];valid_pred=float(np.array([1,3])@beta);mean_pred=float(dy.mean())
allx=np.array([[1,0],[1,1],[1,2],[1,3]],float);ally=np.array([1,2,2,4],float);refit=np.linalg.lstsq(allx,ally,rcond=None)[0]
fp=np.array([[1,4],[1,5]])@refit;actual=np.array([3,5]);bench=np.array([8/3,3]);sse=float(np.sum((fp-actual)**2));bsse=float(np.sum((bench-actual)**2))
assert np.allclose(refit,[.9,.9]) and np.isclose(sse,2.41)
smallx=np.array([4,1,1,3,2,5,2,6]);smally=np.array([8,1,-1,3,2,6,0,9]);ids=pd.qcut(pd.Series(smallx).rank(method='first'),4,labels=False)
binmeans=pd.DataFrame({'x':smallx,'y':smally,'bin':ids}).groupby('bin')[['x','y']].mean().values.tolist()
assert np.allclose(binmeans,[[1,0],[2,1],[3.5,5.5],[5.5,7.5]])
oldtxt=(B/'source-review/lecture-old-54.txt').read_text(encoding='utf-8').split('\f');newtxt=(B/'source-review/lecture-new-56.txt').read_text(encoding='utf-8').split('\f')
def norm(x):return re.sub(r'\s+',' ',re.sub(r'\b\d+/(?:54|56)\b','',x)).strip()
mapping=[(i,i if i<=25 else 54 if i==26 else i+1 if i<=52 else i+2) for i in range(1,55)]
pagechecks=[{'old':a,'new':b,'normalized_extracted_text_identical':norm(oldtxt[a-1])==norm(newtxt[b-1])} for a,b in mapping]
checks={'source_candidate_sha256':sha(B/'candidate.md'),'read_scope':'Root actual complete candidate 1-end, old lecture54 text, P1 379 +P2 260 records; new version equivalence below; visual inspection separate pending.', 'forecast_block_sha256':hashlib.sha256(block.encode()).hexdigest(),'forecast_contract':{'input_shape':list(scope['X_test'].shape),'output_shape':list(pred.shape),'finite':bool(np.isfinite(pred).all()),'matches_saved_60_rows':bool(np.allclose(pred,ref.forecast))},'full_scaling_prediction_max_difference':float(np.max(np.abs(pred-full_pred))),'strategy':{'weight_counts':w.value_counts().to_dict(),'correct_simple_terminal':correct_wealth,'correct_simple_cagr':correct_wealth**.2-1,'incorrect_log_chain_terminal':bad_wealth,'buy_hold_terminal':bh,'buy_hold_cagr':bh**.2-1},'teaching_six_rows':{'validation_ols_se':(valid_pred-4)**2,'validation_mean_se':(mean_pred-4)**2,'refit_coefficients':refit.tolist(),'test_predictions':fp.tolist(),'model_sse':sse,'benchmark_sse':bsse,'oos_pct':(1-sse/bsse)*100},'binmeans':binmeans,'page_text_equivalence':pagechecks,'new_pages':[26,27],'original_main_calculations_sha256':sha(O/'recompute-main-results.json')}
inputs=[C/'course_files_export/Lec02_Regression_Vibe_Coding.pdf',C/'course_files_export/canvas-20261020/Lec02_Regression_Vibe_Coding.pdf',*[C/'transcripts'/f for f in ['M01-transcript.txt','M02-transcript-part1.txt','M02-transcript-part2.txt']],*sorted(p for p in data.iterdir() if p.is_file())]
checks['source_inputs']=[{'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in inputs]
js(O/'main-source-calculations.json',checks)
renders=B/'source-review/render';items=[(f'old-{i:02d}',renders/f'old-{i:02d}.png') for i in range(1,55)]+[(f'new-{i}',renders/f'new-{i}.png') for i in [26,27]]
for start in range(0,len(items),9):
 group=items[start:start+9];sheet=Image.new('RGB',(2400,1440),'white');dr=ImageDraw.Draw(sheet)
 for j,(label,pth) in enumerate(group):
  im=Image.open(pth).convert('RGB');im.thumbnail((792,440));x=(j%3)*800;y=(j//3)*480;sheet.paste(im,(x,y+30));dr.text((x+8,y+5),label,fill='black')
 sheet.save(O/f'source-contact-{start//9+1:02d}.png')
print(json.dumps({'manifest_matches':len(calc['hash_checks']),'forecast':checks['forecast_contract'],'strategy':checks['strategy'],'text_equivalent':sum(x['normalized_extracted_text_identical'] for x in pagechecks),'text_differences':[x for x in pagechecks if not x['normalized_extracted_text_identical']],'contact_sheets':7,'source_dimensions':Image.open(renders/'old-03.png').size},ensure_ascii=False))
