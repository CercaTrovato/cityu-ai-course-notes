"""Verify prepared report data/figures. No model fitting; optional saved-model replay."""
from pathlib import Path
import argparse,json,hashlib,subprocess,tempfile
import pandas as pd,numpy as np
from sklearn.metrics import average_precision_score,roc_auc_score
def main():
 a=argparse.ArgumentParser();a.add_argument('--pack',type=Path,required=True);a.add_argument('--output',type=Path,required=True);a.add_argument('--private-dir',type=Path);a.add_argument('--render',action='store_true');args=a.parse_args();P=args.pack;D=P/'data';args.output.mkdir(exist_ok=True,parents=True)
 checks=[]
 for name in ['h04-screening.csv','r3-methods.csv','r3-group-methods.csv','frozen-test-metrics.csv','feature-experiment-results.csv']:
  x=pd.read_csv(D/name);pc='precision_at_10pct' if 'precision_at_10pct' in x else 'precision';rc='recall_at_10pct' if 'recall_at_10pct' in x else 'recall';assert np.allclose(x[pc],x.hits/x.K,rtol=1e-10,atol=1e-12);assert np.allclose(x[rc],x.hits/x.positive_count,rtol=1e-10,atol=1e-12)
  if 'cluster_0_selected' in x:assert (x[[f'cluster_{i}_selected' for i in range(3)]].sum(axis=1)==x.K).all();assert (x[[f'cluster_{i}_hits' for i in range(3)]].sum(axis=1)==x.hits).all()
  checks.append({'table':name,'rows':len(x),'arithmetic':'passed'})
 spec=json.loads((P/'scope-decision.json').read_text(encoding='utf-8'));assert spec['user_choice']=='名单主线＋概率/价值扩展（推荐）'
 plan=json.loads((D/'feature-experiment-plan.json').read_text(encoding='utf-8'));run=json.loads((D/'feature-experiment-verification.json').read_text(encoding='utf-8'));assert run['new_fits']==3 and run['new_frozen_test_scores']==0
 results=pd.read_csv(D/'feature-experiment-results.csv');replay=[]
 if args.private_dir:
  import joblib
  inputs=pd.read_csv(args.private_dir/'january-replay-inputs.csv',dtype={'customer_unique_id':'string'});old=pd.read_csv(args.private_dir/'new-feature-scores.csv',dtype={'customer_unique_id':'string'}).set_index(['customer_unique_id','snapshot_date'])
  assert set(inputs.snapshot_date)=={'2018-01-01'};assert len(inputs)==len(old);k=['customer_unique_id','snapshot_date'];mi=pd.MultiIndex.from_frame(inputs[k]);y=inputs.y.to_numpy(int)
  for name,extra in plan['extras'].items():
   modelpath=args.private_dir/(name+'.joblib');assert hashlib.sha256(modelpath.read_bytes()).hexdigest()==run['model_sha256'][name]
   model=joblib.load(modelpath);score=model.predict_proba(inputs[plan['raw_fields']+extra])[:,1];given=old.loc[mi,name+'_score'].to_numpy();delta=float(abs(score-given).max());assert delta<1e-12
   ranked=pd.DataFrame({'id':inputs.customer_unique_id,'score':score,'y':y}).sort_values(['score','id'],ascending=[False,True])
   for row in results[results.method.eq(name)].itertuples():
    count=int(ranked.iloc[:int(np.ceil(row.fraction*len(ranked)))].y.sum());assert count==row.hits
    assert abs(average_precision_score(y,score)-row.AP)<1e-12 and abs(roc_auc_score(y,score)-row.ROC_AUC)<1e-12
   replay.append({'model':name,'rows':len(inputs),'max_score_difference':delta,'independent_pandas_rank_and_metrics':'passed'})
 figures=json.loads((P/'figure-manifest.json').read_text(encoding='utf-8'))
 for f in figures:
  for ext,want in f['files'].items():assert hashlib.sha256((P/'figures'/(f['figure']+'.'+ext)).read_bytes()).hexdigest()==want
 render_checks=[]
 if args.render:
  # Generate from copied aggregates in the caller's explicitly selected output directory.
  import shutil,sys
  sandbox=args.output/'figure-replay';sandbox.mkdir(exist_ok=True);shutil.copytree(D,sandbox/'data',dirs_exist_ok=True)
  subprocess.run([sys.executable,str(P/'source/plot_report.py'),'--pack',str(sandbox),'--preview-dir',str(args.output/'figure-previews')],check=True)
  for f in figures:
   for ext,want in f['files'].items():
    path=sandbox/'figures'/(f['figure']+'.'+ext);actual=hashlib.sha256(path.read_bytes()).hexdigest();assert actual==want,(f['figure'],ext,'render differs')
   render_checks.append({'figure':f['figure'],'svg_pdf_exact_replay':True})
 outcome={'aggregate_checks':checks,'model_replay':replay,'model_replay_scope':'3 new repair models only;historic member models not re-fitted','figures_checked':len(figures),'figure_replay':render_checks,'fits_in_verifier':0,'private_data_published':False,'scope':'prepared report evidence;not a final submitted manuscript'}
 (args.output/'verification.json').write_text(json.dumps(outcome,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'aggregate_rows':sum(x['rows'] for x in checks),'saved_models_replayed':len(replay),'figures_verified':len(figures),'figure_replays':len(render_checks),'fits':0}))
if __name__=='__main__':main()
