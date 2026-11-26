"""Rebuild the new repair models' January private inputs; no model fitting."""
from pathlib import Path
import argparse,json,zipfile,hashlib,sys
sys.dont_write_bytecode=True
import numpy as np
from run_fixed_features import bounded,BASE,KEY
def main():
 a=argparse.ArgumentParser();a.add_argument('--config',type=Path,required=True);args=a.parse_args();cfg=json.loads(args.config.read_text(encoding='utf-8'))
 with zipfile.ZipFile(cfg['h02_archive']) as z:
  def rd(name):return bounded(z.read(next(n for n in z.namelist() if n.endswith('/'+name))))[0]
  f=rd('snapshot_features.csv');y=rd('snapshot_labels.csv')
 asof=bounded(Path(cfg['asof_features']).read_bytes())[0]
 v=f[f.snapshot_date.eq('2018-01-01')].merge(y.loc[y.snapshot_date.eq('2018-01-01'),KEY+['y']],on=KEY,validate='one_to_one').merge(asof.loc[asof.snapshot_date.eq('2018-01-01'),KEY+['delivered_known_n','delivery_days_mean','review_known_n','review_score_mean']],on=KEY,validate='one_to_one')
 v['delivery_pending_n']=v.F-v.delivered_known_n;v['delivery_days_log']=np.log1p(v.delivery_days_mean.clip(lower=0));v['delivery_days_mean_missing']=v.delivery_days_mean.isna().astype(float);v['known_review_ratio']=v.review_known_n/v.F;v['review_score_mean_missing']=v.review_score_mean.isna().astype(float)
 cols=KEY+['y']+BASE+['state','delivery_pending_n','delivery_days_log','delivery_days_mean_missing','review_score_mean','known_review_ratio','review_score_mean_missing'];b=v[cols].to_csv(index=False,lineterminator='\n').encode('utf-8')
 private=Path(cfg['private_output']);private.mkdir(parents=True,exist_ok=True);target=private/'january-replay-inputs.csv'
 if target.exists():assert target.read_bytes()==b,'Existing private inputs differ; preserve and investigate.'
 else:
  temp=private/'january-replay-inputs.partial';assert not temp.exists();temp.write_bytes(b);temp.replace(target)
 print(json.dumps({'rows':len(v),'snapshot':'2018-01-01','sha256':hashlib.sha256(b).hexdigest(),'fits':0,'published':False}))
if __name__=='__main__':main()
