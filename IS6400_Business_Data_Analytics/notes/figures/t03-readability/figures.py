from pathlib import Path
import sys,io,json,hashlib
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
import argparse
_parser=argparse.ArgumentParser(description='只读图源与独立输出目录；SVG保留可检索文字')
_parser.add_argument('--output-dir',type=Path,default=Path(__file__).parent)
_args=_parser.parse_args()
HERE=_args.output_dir.resolve()
HERE.mkdir(parents=True,exist_ok=True)
SRC=Path('D:/上课资料/CityU/IS6400_Business_Data_Analytics/course_files_export/iris.txt')
data=pd.read_csv(SRC,header=None)
data.columns=['sepal length','sepal width','petal length','petal width','class']
plt.rcParams['svg.fonttype']='none'
def output(fig,name):
 s=io.StringIO();fig.savefig(s,format='svg');atomic_write(str(HERE/(name+'.svg')),s.getvalue());plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
counts,bins,_=ax.hist(data['petal width'],bins=20)
ax.set(title='Iris petal width: 20 bins',xlabel='petal width (cm)',ylabel='number of flowers')
output(fig,'iris-hist')
fig,ax=plt.subplots(figsize=(8,4),layout='constrained');data.boxplot(ax=ax)
ax.set(title='Iris: default 1.5 IQR whiskers',ylabel='measurement (cm)');output(fig,'iris-box')
fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
for marker,(name,g) in zip(['o','^','s'],data.groupby('class')):
 ax.scatter(g['petal length'],g['petal width'],alpha=.7,marker=marker,label=name)
ax.set(title='Iris: original row pairs',xlabel='petal length (cm)',ylabel='petal width (cm)');ax.legend();output(fig,'iris-scatter')
fig,ax=plt.subplots(figsize=(9,4),layout='constrained');parallel_coordinates(data,'class',ax=ax)
ax.set(title='Iris: one polyline per row; raw cm',ylabel='measurement (cm)');output(fig,'iris-parallel')
toy=pd.DataFrame({'a':[1,2,3],'b':[2,4,6],'c':[3,2,1]});corr=toy.corr()
fig,ax=plt.subplots(figsize=(5,4),layout='constrained')
im=ax.imshow(corr,vmin=-1,vmax=1,cmap='coolwarm');fig.colorbar(im,ax=ax,label='Pearson r')
ax.set_xticks(range(3),corr.columns);ax.set_yticks(range(3),corr.index)
for i in range(3):
 for j in range(3):ax.text(j,i,f'{corr.iloc[i,j]:.0f}',ha='center',va='center')
ax.set_title('Teaching a/b/c; 3 paired rows per cell');output(fig,'toy-correlation')
results={'iris_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'source':'T03 cells14/17/20/23同源机制，新散点额外配点形；非旧像素','iris_rows':len(data),'hist_counts':counts.tolist(),'hist_edges':bins.tolist(),'first_row':data.iloc[0].to_list(),'box_quantiles':data.iloc[:,:4].quantile([.25,.5,.75]).to_dict(),'toy_input':toy.to_dict('list'),'toy_cov':toy.cov().to_numpy().tolist(),'toy_corr':corr.to_numpy().tolist(),'paired_count':3}
atomic_write(str(HERE/'results.json'),json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'hist_total':counts.sum(),'first_row':results['first_row'],'toy_corr':results['toy_corr']},ensure_ascii=False))
