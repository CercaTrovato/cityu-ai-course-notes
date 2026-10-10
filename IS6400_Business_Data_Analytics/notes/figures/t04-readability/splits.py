from pathlib import Path
import argparse,sys,io,json,hashlib
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,default=Path(__file__).parent);args=p.parse_args();out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
src=Path('D:/上课资料/CityU/IS6400_Business_Data_Analytics/course_files_export/iris.txt')
df=pd.read_csv(src,header=None,names=['sepal-L','sepal-W','petal-L','petal-W','class']);df['is_setosa']=df['class'].eq('Iris-setosa')
plt.rcParams['svg.fonttype']='none';fig,axes=plt.subplots(2,1,figsize=(8,9),layout='constrained');counts={}
for ax,(col,cut) in zip(axes,[('petal-W',.8),('sepal-L',6.)]):
 for is_setosa,marker,color,label in [(True,'o','tab:blue','Setosa'),(False,'^','tab:orange','Non-Setosa')]:
  sub=df[df.is_setosa==is_setosa];ax.scatter(sub[col],sub['sepal-W'],marker=marker,color=color,label=label,alpha=.7,s=28)
 ax.axvline(cut,color='black',linestyle='--',label=f'{col} <= {cut:g} goes left');ax.set(xlabel=col+' (cm)',ylabel='sepal-W (cm)',title=f'Given split: {col} <= {cut:g}');ax.legend(fontsize=10)
 counts[col]={'left_setosa':int(((df[col]<=cut)&df.is_setosa).sum()),'left_non':int(((df[col]<=cut)&~df.is_setosa).sum()),'right_setosa':int(((df[col]>cut)&df.is_setosa).sum()),'right_non':int(((df[col]>cut)&~df.is_setosa).sum())}
b=io.StringIO();fig.savefig(b,format='svg');atomic_write(str(out/'iris-splits.svg'),b.getvalue());atomic_write(str(out/'splits-results.json'),json.dumps({'source':'T04 current43-cell classroom cell16; marker shapes supplemented','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'counts':counts},ensure_ascii=False,indent=2)+'\n');print(counts)
