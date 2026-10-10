from pathlib import Path
import sys,json,io,hashlib
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage,dendrogram
from sklearn.cluster import DBSCAN
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
import argparse
_parser=argparse.ArgumentParser(description='只读图源与独立输出目录；SVG保留可检索文字')
_parser.add_argument('--output-dir',type=Path,default=Path(__file__).parent)
_args=_parser.parse_args()
HERE=_args.output_dir.resolve()
HERE.mkdir(parents=True,exist_ok=True)
SRC=Path('D:/上课资料/CityU/IS6400_Business_Data_Analytics/course_files_export')
plt.rcParams['svg.fonttype']='none'
results={'purpose':'仅新增图定向复算；不重跑原Notebook全部实验','versions':{}}
import scipy,sklearn
results['versions']={'numpy':np.__version__,'scipy':scipy.__version__,'sklearn':sklearn.__version__}
def output(fig,name):
 b=io.StringIO();fig.savefig(b,format='svg');atomic_write(str(HERE/(name+'.svg')),b.getvalue());plt.close(fig)
animals=pd.read_csv(SRC/'vertebrate.csv');X=animals.drop(columns=['Name','Class']).to_numpy()
results['vertebrate_sha256']=hashlib.sha256((SRC/'vertebrate.csv').read_bytes()).hexdigest()
fig,axes=plt.subplots(1,4,figsize=(18,7),layout='constrained')
results['linkage']={}
for ax,method in zip(axes,['single','complete','average','ward']):
 Z=linkage(X,method);results['linkage'][method]=Z.tolist()
 dendrogram(Z,labels=animals.Name.to_list(),orientation='right',ax=ax,color_threshold=0,above_threshold_color='black')
 ax.set(title=method,xlabel='merge height (Ward scale differs)')
output(fig,'animal-linkage')
points=pd.read_csv(SRC/'chameleon.data',sep=' ',names=['x','y']).to_numpy()
db=DBSCAN(eps=15.5,min_samples=5).fit(points);labels=db.labels_;core=np.zeros(len(points),bool);core[db.core_sample_indices_]=True
results['chameleon_sha256']=hashlib.sha256((SRC/'chameleon.data').read_bytes()).hexdigest()
results['dbscan']={'eps':15.5,'min_samples':5,'noise':int((labels==-1).sum()),'core':int(core.sum()),'border':int(((labels>=0)&~core).sum()),'counts':{str(k):int((labels==k).sum()) for k in np.unique(labels)},'first_point':{'xy':points[0].tolist(),'label':int(labels[0]),'core':bool(core[0])}}
atomic_write(str(HERE/'dbscan-points.json'),json.dumps({'points':points.tolist(),'labels':labels.tolist(),'core':core.tolist()},indent=2)+'\n')
fig,ax=plt.subplots(figsize=(10,6),layout='constrained')
for k in np.unique(labels):
 if k==-1:continue
 color=plt.get_cmap('tab10')(int(k)%10)
 for mask,marker,size in [(core,'o',9),(~core,'^',25)]:
  ids=(labels==k)&mask;ax.scatter(points[ids,0],points[ids,1],s=size,marker=marker,color=color,label=f'cluster {k}' if marker=='o' else None)
noise=labels==-1;ax.scatter(points[noise,0],points[noise,1],marker='x',s=16,color='black',label='noise -1')
ax.scatter([],[],marker='o',color='gray',label='core');ax.scatter([],[],marker='^',color='gray',label='border')
ax.annotate('row 1',points[0],xytext=(12,12),textcoords='offset points',arrowprops={'arrowstyle':'->'})
ax.set(xlabel='x (source coordinate unit)',ylabel='y (source coordinate unit)',title='DBSCAN: eps=15.5, min_samples=5 (includes self)');ax.legend(fontsize=8,ncol=2)
output(fig,'dbscan-roles')
W=np.array([[0,1,.1,0],[1,0,0,.1],[.1,0,0,1],[0,.1,1,0]],float);deg=W.sum(1);L=np.eye(4)-W/1.1
v1=np.ones(4)/2;v2=np.array([1,1,-1,-1])/2;U=np.column_stack((v1,v2));T=U/np.linalg.norm(U,axis=1)[:,None]
results['spectral']={'W':W.tolist(),'degree':deg.tolist(),'eigenvalues':np.linalg.eigvalsh(L).tolist(),'U':U.tolist(),'normalized_rows':T.tolist(),'eigen_residual':float(np.abs(L@v2-2/11*v2).max()),'initial_SSE':float(((T-np.array([[0,1],[0,1],[0,-1],[0,-1]]))**2).sum()),'updated_SSE':0}
fig,ax=plt.subplots(figsize=(7,4),layout='constrained')
ax.scatter(T[:2,0],T[:2,1],marker='o',s=100,label='points 1,2');ax.scatter(T[2:,0],T[2:,1],marker='^',s=100,label='points 3,4')
ax.annotate('1,2 overlap',T[0],xytext=(15,0),textcoords='offset points');ax.annotate('3,4 overlap',T[2],xytext=(15,0),textcoords='offset points')
ax.scatter([0,0],[1,-1],marker='x',color='black',label='initial centers')
for start,end in zip([(0,1),(0,-1)],[T[0],T[2]]):ax.annotate('',end,xytext=start,arrowprops={'arrowstyle':'->'})
ax.set(xlim=(-.3,1.7),ylim=(-1.3,1.3),xlabel='normalized eigenvector 1',ylabel='normalized eigenvector 2',title='Teaching graph embedding; center update arrows');ax.legend(fontsize=9)
output(fig,'spectral-embedding')
atomic_write(str(HERE/'results.json'),json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'first_merge':results['linkage']['single'][0],'dbscan':results['dbscan'],'spectral':results['spectral']},ensure_ascii=False))
