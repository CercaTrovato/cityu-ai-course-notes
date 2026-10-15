from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_classification
HERE=Path(__file__).parent
OUT=HERE/'figures/classification'
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.size':14,'svg.fonttype':'none'})
X,y=make_classification(n_samples=10000,n_features=2,n_redundant=0,n_clusters_per_class=1,weights=[0.1],flip_y=0,random_state=2)
fig=plt.figure(figsize=(10,9),layout='constrained')
gs=fig.add_gridspec(2,2,height_ratios=[1,1])
scatter=fig.add_subplot(gs[0,:])
for label in [0,1]:
    sel=y==label
    scatter.scatter(X[sel,0],X[sel,1],s=7,alpha=0.35,label=f'Class {label}')
scatter.set(xlabel='Synthetic feature 1 (unitless)',ylabel='Synthetic feature 2 (unitless)',title='Synthetic samples: 1,000 Class 0 / 9,000 Class 1')
scatter.legend(markerscale=3)
for j,(title,cm) in enumerate([('No class weight',np.array([[262,124],[8,3606]])),('class_weight = {0: 10, 1: 1}',np.array([[376,10],[532,3082]]))]):
    ax=fig.add_subplot(gs[1,j]);ax.imshow(cm,cmap='Blues',vmin=0,vmax=3614)
    for (i,k),v in np.ndenumerate(cm):ax.text(k,i,str(v),ha='center',va='center',fontsize=18,color='white' if v>1807 else 'black')
    ax.set(xticks=[0,1],yticks=[0,1],xlabel='Predicted class',ylabel='Actual class',title=title)
fig.savefig(OUT/'class-weight-effect.svg')
fig.savefig(OUT/'class-weight-effect.png',dpi=150)
print(OUT/'class-weight-effect.svg')
