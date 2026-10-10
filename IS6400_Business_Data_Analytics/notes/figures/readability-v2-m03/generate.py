from pathlib import Path
import sys,io,json,argparse,hashlib
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parent))
ROOT=Path('D:/上课资料/CityU')
sys.path.insert(0,str(ROOT/'_meta/tools'))
from safe_write import atomic_write
BASE=Path(__file__).parent
def save(p,t):
    p.parent.mkdir(parents=True,exist_ok=True)
    atomic_write(str(p),t)
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'svg.fonttype':'none','font.size':11})
ap=argparse.ArgumentParser(description='Reproduce registered teaching SVG assets')
ap.add_argument('--output-dir',type=Path,default=BASE,help='Default: directory beside this generator')
args=ap.parse_args()
out=args.output_dir.resolve()
out.mkdir(parents=True,exist_ok=True)
base=np.array([63,64,64,70,72,76,77,81,81.]);alter=base.copy();alter[-1]=181
fig,axs=plt.subplots(1,2,figsize=(11,5),sharey=True);ev=[]
for ax,data,title in zip(axs,[base,alter],['Original nine values','Only last 81 replaced by 181']):
    ordered=np.sort(data);q1=np.median(ordered[:4]);q3=np.median(ordered[5:]);med=ordered[4];iqr=q3-q1;lo=q1-1.5*iqr;hi=q3+1.5*iqr;inside=data[(data>=lo)&(data<=hi)]
    p10,p90=np.quantile(data,[.1,.9],method='linear')
    stats=[{'label':'Tukey','q1':q1,'q3':q3,'med':med,'whislo':inside.min(),'whishi':inside.max(),'fliers':data[(data<lo)|(data>hi)].tolist()},{'label':'10/90','q1':q1,'q3':q3,'med':med,'whislo':p10,'whishi':p90,'fliers':data[(data<p10)|(data>p90)].tolist()}]
    ax.bxp(stats,showfliers=True,widths=.45);ax.axhline(lo,linestyle='--',color='#777');ax.axhline(hi,linestyle='--',color='#777');ax.set_title(title);ax.set_ylabel('Original teaching value');ax.grid(axis='y',alpha=.25)
    ev.append({'data':data.tolist(),'quartile_method':'exclude median, median of lower/upper half','Q1':q1,'median':med,'Q3':q3,'IQR':iqr,'fences':[lo,hi],'Tukey_whiskers':[float(inside.min()),float(inside.max())],'linear_p10_p90':[float(p10),float(p90)],'Tukey_outliers':stats[0]['fliers']})
fig.tight_layout();buf=io.StringIO();fig.savefig(buf,format='svg',bbox_inches='tight');save(out/'box-policies.svg',buf.getvalue());plt.close(fig)
assert ev[0]['Q1']==64 and ev[0]['Q3']==79 and ev[0]['Tukey_whiskers']==[63.,81.]
assert ev[1]['Tukey_outliers']==[181.]
x=np.array([80.,90.,70.,100.]);y=np.array([1200.,1300.,1100.,1350.]);cov=np.cov(x,y,ddof=1)[0,1];corr=np.corrcoef(x,y)[0,1]
fig,ax=plt.subplots(figsize=(7,5));ax.scatter(x,y,s=70)
for name,xx,yy in zip('ABCD',x,y):ax.annotate(name,(xx,yy),xytext=(5,5),textcoords='offset points')
ax.axvline(x.mean(),color='#777',linestyle='--');ax.axhline(y.mean(),color='#777',linestyle='--');ax.set_xlabel('Graduation rate (%)');ax.set_ylabel('SAT score');ax.set_title('Four invented schools; paired deviations');ax.grid(alpha=.25);fig.tight_layout();buf=io.StringIO();fig.savefig(buf,format='svg',bbox_inches='tight');save(out/'paired-covariance.svg',buf.getvalue());plt.close(fig)
cov_data={'source':'M03 §2.11 existing invented four-school example, not the 49-school source','graduation_percent':x.tolist(),'SAT':y.tolist(),'mean_x':float(x.mean()),'mean_y':float(y.mean()),'paired_products':((x-x.mean())*(y-y.mean())).tolist(),'covariance':float(cov),'correlation':float(corr),'covariance_after_x_div100':float(np.cov(x/100,y,ddof=1)[0,1])}
csv=ROOT/'IS6400_Business_Data_Analytics/course_files_export/Airbnb.csv';price=np.exp(pd.read_csv(csv,usecols=['log_price'])['log_price'].to_numpy());mean=float(price.mean());q75=float(np.quantile(price,.75));count=int((price<mean).sum())
correction={'source':str(csv),'source_sha256':hashlib.sha256(csv.read_bytes()).hexdigest(),'purpose':'定向核原句均价比四分之三房源贵，与Q3约180矛盾；非全实验重跑','N':len(price),'price_mean':mean,'Q75':q75,'strict_below_mean_count':count,'strict_below_mean_fraction':count/len(price),'old_claim':'158美元比四分之三的房源都贵','finding':'mean<Q75且低于均价的观察比例不是75%，旧句不成立'}
result={'boxes':ev,'covariance':cov_data,'directed_correction':correction,'visual_review':'pending'}
save(out/'calculation-evidence.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n');save(out/'figure-inputs.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
