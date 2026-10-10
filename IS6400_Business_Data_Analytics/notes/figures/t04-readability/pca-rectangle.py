from pathlib import Path
import sys,json,io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
import argparse
_parser=argparse.ArgumentParser(description='只读图源与独立输出目录；SVG保留可检索文字')
_parser.add_argument('--output-dir',type=Path,default=Path(__file__).parent)
_args=_parser.parse_args()
HERE=_args.output_dir.resolve()
HERE.mkdir(parents=True,exist_ok=True)
X=np.array([[0.,0.],[4.,0.],[0.,2.],[4.,2.]])
mu=X.mean(axis=0); D=X-mu; S=D.T@D/3
z=D[:,0]; reconstructed=np.column_stack((z+mu[0],np.full(4,mu[1])))
data={'source':'T04 §4.1 笔记补充四行表，非Iris','X':X.tolist(),'classes':[0,0,1,1],'mu':mu.tolist(),'covariance':S.tolist(),'axis':[1,0],'z':z.tolist(),'reconstructed':reconstructed.tolist(),'retained_variance':.8,'squared_error':float(((X-reconstructed)**2).sum())}
atomic_write(str(HERE/'pca-rectangle.json'),json.dumps(data,ensure_ascii=False,indent=2)+'\n')
plt.rcParams['svg.fonttype']='none'
fig,axes=plt.subplots(1,2,figsize=(11,4.6),layout='constrained')
for c,marker in [(0,'o'),(1,'^')]:
 ids=[i for i in range(4) if data['classes'][i]==c]
 axes[0].scatter(X[ids,0],X[ids,1],marker=marker,label=f'class {c}',s=75)
for i,p in enumerate(X):
 axes[0].annotate(f'ID{i+1}',p,xytext=(8,8),textcoords='offset points')
 axes[0].plot([p[0],p[0]],[p[1],1],':',color='gray')
axes[0].axhline(1,color='black',linestyle='--',label='retained axis through mean')
axes[0].scatter([2],[1],marker='x',color='black',s=80,label='mean (2,1)')
axes[0].set(xlim=(-.7,5.3),ylim=(-.5,3.1),xlabel='measurement 1 (teaching unit)',ylabel='measurement 2 (teaching unit)',title='Original rows and projection')
axes[0].legend(fontsize=8,loc='upper center')
for i in range(4):
 axes[1].scatter(z[i],i+1,marker='o' if i<2 else '^',s=75,color='tab:blue' if i<2 else 'tab:orange')
 axes[1].annotate(f'ID{i+1}: z={z[i]:g}',(z[i],i+1),xytext=(7,0),textcoords='offset points',va='center')
axes[1].set(xlim=(-3,4),ylim=(.5,4.6),xlabel='z along retained unit axis',ylabel='row ID (display separation only)',title='Same z across different classes')
axes[1].set_yticks([1,2,3,4])
buff=io.StringIO();fig.savefig(buff,format='svg');atomic_write(str(HERE/'pca-rectangle.svg'),buff.getvalue())

print(json.dumps(data,ensure_ascii=False))
