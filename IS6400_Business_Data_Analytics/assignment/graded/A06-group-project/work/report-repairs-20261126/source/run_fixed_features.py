"""Three predeclared October/January LR configurations; no test-month selection.
Explicit --fit is required. Customer-level inputs, scores and models stay private.
"""
from pathlib import Path
import argparse,io,csv,json,zipfile,hashlib,importlib.util,platform,warnings
import numpy as np,pandas as pd,joblib,sklearn
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer,StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score,roc_auc_score
from threadpoolctl import threadpool_limits
KEY=['customer_unique_id','snapshot_date'];DATES={'2017-10-01','2018-01-01'}
BASE=['R','F','M','average_item_rows','freight_share','recent30_orders','recent30_spend'];EXTRA={'F0':[],'G1':['delivery_pending_n','delivery_days_log','delivery_days_mean_missing'],'G2':['review_score_mean','known_review_ratio','review_score_mean_missing']}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def bounded(data):
 lines=data.decode('utf-8-sig').splitlines(keepends=True);header=next(csv.reader([lines[0]]));col=header.index('snapshot_date');kept=[lines[0]];excluded={}
 for line in lines[1:]:
  # These versioned CSVs have comma-free IDs/ISO date columns. Filter dates before pandas parses predictors/labels.
  date=line.split(',')[col].strip('"\r\n')
  if date in DATES:kept.append(line)
  else:excluded[date]=excluded.get(date,0)+1
 return pd.read_csv(io.StringIO(''.join(kept)),dtype={'customer_unique_id':'string'}),excluded
def make(extra):
 blocks=[('base',Pipeline([('log1p',FunctionTransformer(np.log1p,feature_names_out='one-to-one')),('impute',SimpleImputer(strategy='median',add_indicator=True)),('scale',StandardScaler())]),BASE),('state',Pipeline([('impute',SimpleImputer(strategy='most_frequent')),('onehot',OneHotEncoder(handle_unknown='ignore',sparse_output=False))]),['state'])]
 if extra:blocks.append(('extra',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())]),extra))
 return Pipeline([('preprocess',ColumnTransformer(blocks,remainder='drop')),('model',LogisticRegression(C=1.,penalty='l2',solver='lbfgs',class_weight='balanced',max_iter=2000,tol=1e-4,random_state=2026))])
def select(scores,ids,fraction):
 k=int(np.ceil(len(scores)*fraction));order=np.lexsort((ids.astype(str).to_numpy(),-scores));mask=np.zeros(len(scores),bool);mask[order[:k]]=True;return mask
def measure(frame,scores,fraction):
 y=frame.y.to_numpy(int);m=select(scores,frame.customer_unique_id,fraction);h=int(y[m].sum());k=int(m.sum());p=int(y.sum())
 return {'fraction':fraction,'N':len(y),'positive_count':p,'K':k,'hits':h,'precision':h/k,'recall':h/p,'AP':float(average_precision_score(y,scores)),'ROC_AUC':float(roc_auc_score(y,scores))},m
def main():
 a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--config',type=Path,required=True);a.add_argument('--output',type=Path,required=True);a.add_argument('--fit',action='store_true');args=a.parse_args()
 if not args.fit:raise SystemExit('Training disabled: pass --fit only for the three authorized predeclared configurations.')
 cfg=json.loads(args.config.read_text(encoding='utf-8'));out=args.output;out.mkdir(parents=True,exist_ok=True);private=Path(cfg['private_output']);private.mkdir(parents=True,exist_ok=True)
 if (out/'feature-experiment-plan.json').exists():raise FileExistsError('Preserve the prior run; choose a new output directory.')
 source_spec=args.repo/'research/role02-v11-20261113/member/feature-spec.json'
 if not source_spec.exists():
  source_spec=Path('E:/app-data/codex/scratchpad/is6400-report-gap-audit-20261126/source-cache/research/role02-v11-20261113/member/feature-spec.json')
 original={k:sha(cfg[k]) for k in ['h02_archive','asof_features','stored_r3_predictions','stored_group_predictions']}
 assert original['h02_archive']=='3b58f4e493e825a76ccc569f205cfa0db5d27e22b13389c3c00ff958a316419a'
 assert original['asof_features']=='549f0502199291466a42e674e2f9f746462de57953974ff06b5b66dc409b0628'
 plan={'scope':'3 fixed development configurations; report repair R13','train':'2017-10-01','development':'2018-01-01','raw_fields':BASE+['state'],'extras':EXTRA,'classifier':{'C':1,'penalty':'l2','solver':'lbfgs','class_weight':'balanced','max_iter':2000,'tol':.0001,'random_state':2026},'capacities':[.05,.1,.2],'new_extra_preprocessing':'Explicit formulas then median imputation and standardization fitted on October; no extra log1p on delivery_days_log or review stars. Base seven numeric fields retain their log1p pipeline.','purpose':'Test the delivered Role02 field formulas, not recreate unavailable private candidate table bytes. Existing field screening and all prior outcomes have been seen.','no_test_scoring':True,'no_model_reselection_using_test':True,'no_grid_search':True,'source_spec_sha256':sha(source_spec),'input_sha256':original}
 (out/'feature-experiment-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 with zipfile.ZipFile(cfg['h02_archive']) as z:
  def rd(name):return bounded(z.read(next(n for n in z.namelist() if n.endswith('/'+name))))
  features,exf=rd('snapshot_features.csv');labels,exl=rd('snapshot_labels.csv')
 asof,exa=bounded(Path(cfg['asof_features']).read_bytes());needed=['delivered_known_n','delivery_days_mean','review_known_n','review_score_mean']
 data=features.merge(labels[KEY+['y']],on=KEY,validate='one_to_one').merge(asof[KEY+needed],on=KEY,how='left',validate='one_to_one')
 assert set(data.snapshot_date)==DATES and data[KEY].duplicated().sum()==0
 data['delivery_pending_n']=data.F-data.delivered_known_n;assert data.delivery_pending_n.ge(0).all()
 data['delivery_days_log']=np.log1p(data.delivery_days_mean.clip(lower=0));data['delivery_days_mean_missing']=data.delivery_days_mean.isna().astype(float)
 data['known_review_ratio']=data.review_known_n/data.F;data['review_score_mean_missing']=data.review_score_mean.isna().astype(float)
 train=data.loc[data.snapshot_date.eq('2017-10-01')].copy();val=data.loc[data.snapshot_date.eq('2018-01-01')].copy()
 scores={};rows=[];diagnostics=[];transforms=[];model_hashes={}
 for name,extra in EXTRA.items():
  model=make(extra)
  with warnings.catch_warnings(record=True) as caught,threadpool_limits(limits=2):
   warnings.simplefilter('always');model.fit(train[BASE+['state']+extra],train.y)
  score=model.predict_proba(val[BASE+['state']+extra])[:,1];assert np.isfinite(score).all();scores[name]=score
  checkpoint=private/(name+'.joblib');assert not checkpoint.exists();joblib.dump(model,checkpoint);model_hashes[name]=sha(checkpoint)
  diagnostics.append({'method':name,'n_iter':int(model.named_steps['model'].n_iter_[0]),'iteration_limit':2000,'warnings':' | '.join(str(x.message) for x in caught),'input_fields':len(BASE)+1+len(extra),'transformed_columns':int(model.named_steps['model'].n_features_in_),'model_sha256':model_hashes[name],'old_original_training_environment_claimed':False})
  if extra:
   block=model.named_steps['preprocess'].named_transformers_['extra']
   for i,col in enumerate(extra):transforms.append({'method':name,'field':col,'median':float(block.named_steps['impute'].statistics_[i]),'mean_after_imputation':float(block.named_steps['scale'].mean_[i]),'std_after_imputation':float(block.named_steps['scale'].scale_[i]),'fit_snapshot':'2017-10-01'})
  for f in [.05,.1,.2]:m,_=measure(val,score,f);rows.append({'run_id':'repair-G1G2-20261126','method':name,**m})
 result=pd.DataFrame(rows);result.to_csv(out/'feature-experiment-results.csv',index=False,lineterminator='\n');pd.DataFrame(diagnostics).to_csv(out/'feature-optimization.csv',index=False,lineterminator='\n');pd.DataFrame(transforms).to_csv(out/'feature-transform-fit.csv',index=False,lineterminator='\n')
 detail=val[KEY+['y']].copy()
 for name,s in scores.items():detail[name+'_score']=s
 detail.to_csv(private/'new-feature-scores.csv',index=False,lineterminator='\n')
 old=pd.read_csv(cfg['stored_r3_predictions'],dtype={'customer_unique_id':'string'});aligned=val[KEY].merge(old[KEY+['F0_base_weighted_score']],on=KEY,validate='one_to_one');s=aligned.F0_base_weighted_score.to_numpy();new=select(scores['F0'],val.customer_unique_id,.1);prior=select(s,val.customer_unique_id,.1)
 pairs=[]
 for name in ['G1','G2']:
  own=select(scores[name],val.customer_unique_id,.1);y=val.y.to_numpy(int);pairs.append({'method':name,'reference':'F0_new_replay','common_selected':int((own&new).sum()),'added_hits':int(y[own&~new].sum()),'removed_hits':int(y[new&~own].sum()),'net_hits':int(y[own].sum()-y[new].sum()),'scope':'January development; not a test result'})
 pd.DataFrame(pairs).to_csv(out/'feature-paired-comparison.csv',index=False,lineterminator='\n')
 after={k:sha(cfg[k]) for k in original};assert after==original
 receipt={'new_fits':3,'grid_searches':0,'train_N':len(train),'train_positives':int(train.y.sum()),'development_N':len(val),'development_positives':int(val.y.sum()),'parsed_dates':sorted(DATES),'excluded_dates_before_predictor_label_parsing':{'features':exf,'labels':exl,'asof':exa},'new_frozen_test_scores':0,'input_hashes_unchanged':True,'base_replay_vs_saved_R3':{'max_absolute_score_difference':float(abs(scores['F0']-s).max()),'same_selected_customers':int((new&prior).sum()),'K':int(new.sum())},'environment':{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'sklearn':sklearn.__version__},'model_sha256':model_hashes,'plan_sha256':sha(out/'feature-experiment-plan.json'),'script_sha256':sha(__file__),'metrics_sha256':sha(out/'feature-experiment-results.csv'),'reading_scope':'Input archive/file bytes scanned and hashed; only October/January predictors and labels parsed into model frames. No April/May/June model evaluation or selection.'}
 (out/'feature-experiment-verification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(result.loc[result.fraction.eq(.1)].to_string(index=False));print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
