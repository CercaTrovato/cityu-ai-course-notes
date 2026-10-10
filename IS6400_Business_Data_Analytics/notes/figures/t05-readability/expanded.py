from pathlib import Path
import argparse,sys,io,json,hashlib,itertools
import numpy as np,pandas as pd,scipy,sklearn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.cluster.hierarchy import linkage,dendrogram
from sklearn import cluster,datasets
from sklearn.preprocessing import StandardScaler
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
p=argparse.ArgumentParser(description='T05定向图/机制复算，原件只读');p.add_argument('--output-dir',type=Path,default=Path(__file__).parent);a=p.parse_args();OUT=a.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
SRC=Path('D:/上课资料/CityU/IS6400_Business_Data_Analytics/course_files_export')
plt.rcParams.update({'svg.fonttype':'none','font.size':12})
R={'versions':{'numpy':np.__version__,'scipy':scipy.__version__,'sklearn':sklearn.__version__},'source_hashes':{},'linkage':{},'grid':{},'non_spherical':{}}
def source(name):
 path=SRC/name;R['source_hashes'][name]=hashlib.sha256(path.read_bytes()).hexdigest();return path
def output(fig,name):
 b=io.StringIO();fig.savefig(b,format='svg');atomic_write(str(OUT/(name+'.svg')),b.getvalue());plt.close(fig)
animals=pd.read_csv(source('vertebrate.csv'));AX=animals.drop(columns=['Name','Class']).to_numpy()
for method in ['single','complete','average','ward']:
 Z=linkage(AX,method);fig,ax=plt.subplots(figsize=(8,6.5),layout='constrained');dendrogram(Z,labels=animals.Name.to_list(),orientation='right',ax=ax,color_threshold=0,above_threshold_color='black',leaf_font_size=12);ax.set(title=method+' linkage — same 15 animals',xlabel='merge height (Ward: sqrt(2 * SSE increase))');output(fig,'animal-'+method)
 members={i:[str(animals.Name.iloc[i])] for i in range(15)};example=None
 for i,row in enumerate(Z):
  left,right=members[int(row[0])],members[int(row[1])]
  if example is None and row[2]>0:example={'row_0_based':i,'new_id':15+i,'left':left,'right':right,'height':float(row[2]),'count':int(row[3])}
  members[15+i]=left+right
 R['linkage'][method]={'Z':Z.tolist(),'nonzero_example':example}
# Original cell23 input protocols, separate four readable 2x2 method figures.
moons=datasets.make_moons(n_samples=1000,noise=.05,random_state=170)[0]
blobs=datasets.make_blobs(n_samples=1000,random_state=170)[0]
varied=datasets.make_blobs(n_samples=1000,cluster_std=[1.,2.5,.5],random_state=170)[0]
aniso=blobs@np.array([[.6,-.6],[-.4,.8]])
for name,raw,k in [('moons',moons,2),('blobs',blobs,3),('varied',varied,3),('aniso',aniso,3)]:
 X=StandardScaler().fit_transform(raw);fig,axes=plt.subplots(2,2,figsize=(9,8),layout='constrained');rows={}
 for ax,method in zip(axes.flat,['single','average','complete','ward']):
  model=cluster.AgglomerativeClustering(n_clusters=k,linkage=method).fit(X);labels=model.labels_;rows[method]={'labels':labels.tolist(),'counts':np.bincount(labels).tolist(),'row1_label':int(labels[0])}
  ax.scatter(X[:,0],X[:,1],c=labels,cmap=ListedColormap(['#377eb8','#ff7f00','#4daf4a']),vmin=0,vmax=2,s=8);ax.set(title=method,xlabel='standardized x',ylabel='standardized y');ax.set_aspect('equal',adjustable='box')
 fig.suptitle(name+' — same rows, k='+str(k)+', fit scale once per dataset');output(fig,'linkage-'+name)
 R['grid'][name]={'input_rows':raw.tolist(),'scaled_rows':X.tolist(),'k':k,'methods':rows}
for name,file,gamma in [('two-d','2d_data.txt',5000),('elliptical','elliptical.txt',500)]:
 X=pd.read_csv(source(file),delimiter=' ',names=['x','y']).to_numpy();km=cluster.KMeans(n_clusters=2,max_iter=50,random_state=1);sp=cluster.SpectralClustering(n_clusters=2,random_state=1,affinity='rbf',gamma=gamma);kl=km.fit_predict(X);sl=sp.fit_predict(X)
 fig,axes=plt.subplots(3,1,figsize=(8,12),layout='constrained')
 for ax,label,lab in zip(axes,['Original input','K-means: k=2, max_iter=50','Spectral: k=2, gamma='+str(gamma)],[None,kl,sl]):
  if lab is None:ax.scatter(X[:,0],X[:,1],s=8,color='gray')
  else:ax.scatter(X[:,0],X[:,1],s=8,c=lab,cmap=ListedColormap(['#377eb8','#ff7f00']),vmin=-.5,vmax=1.5)
  ax.set(title=label,xlabel='x (source coordinate unit)',ylabel='y (source coordinate unit)');ax.set_aspect('equal',adjustable='box')
 output(fig,'comparison-'+name)
 R['non_spherical'][name]={'input_file':file,'gamma':gamma,'kmeans_params':km.get_params(),'spectral_params':{k:v for k,v in sp.get_params().items() if not callable(v)},'kmeans_labels':kl.tolist(),'spectral_labels':sl.tolist(),'row1':{'xy':X[0].tolist(),'kmeans':int(kl[0]),'spectral':int(sl[0])},'counts':{'kmeans':np.bincount(kl).tolist(),'spectral':np.bincount(sl).tolist()}}
# Complete local Lloyd example: fixed original ratings, explicit teaching initialization.
ratings=np.array([[5,5,2,1],[4,5,3,2],[4,4,4,3],[2,2,4,5],[1,2,3,4],[2,1,5,5]],float);centers=ratings[[0,1]].copy();states=[]
for it in range(1,21):
 distances=((ratings[:,None,:]-centers[None,:,:])**2).sum(2);lab=distances.argmin(1);new=np.vstack([ratings[lab==j].mean(0) for j in [0,1]])
 states.append({'iteration':it,'centers_before':centers.tolist(),'labels':lab.tolist(),'sse_before_update':float(distances[np.arange(6),lab].sum()),'centers_after':new.tolist(),'sse_after_update':float(((ratings-new[lab])**2).sum()),'stop':bool(np.array_equal(new,centers))})
 centers=new
 if states[-1]['stop']:break
R['lloyd_teaching']={'input':ratings.tolist(),'initial_center_rows_1_based':[1,2],'tie_policy':'smaller center index','stop_policy':'centers unchanged; maximum20; reject empty cluster','states':states}
# Small linkage example, explicit tie-break lexicographic member IDs.
pts=np.array([0.,2.,5.,9.]);R['small_linkage']={}
for method in ['single','complete','average','ward']:
 cs=[(i,) for i in range(4)];steps=[]
 while len(cs)>1:
  cand=[]
  for c1,c2 in itertools.combinations(cs,2):
   dd=np.abs(pts[list(c1),None]-pts[list(c2)][None,:]);delta=len(c1)*len(c2)/(len(c1)+len(c2))*(pts[list(c1)].mean()-pts[list(c2)].mean())**2
   score={'single':dd.min(),'complete':dd.max(),'average':dd.mean(),'ward':delta}[method];cand.append((float(score),c1,c2))
  score,c1,c2=min(cand);new=tuple(sorted(c1+c2));steps.append({'candidates':[{'score':v,'left':list(l),'right':list(r)} for v,l,r in cand],'chosen':[list(c1),list(c2)],'score':score,'merged':list(new)});cs=sorted([c for c in cs if c not in [c1,c2]]+[new])
 R['small_linkage'][method]=steps
P=pd.read_csv(source('chameleon.data'),delimiter=' ',names=['x','y']).to_numpy();db=cluster.DBSCAN(eps=15.5,min_samples=5).fit(P);dist=np.linalg.norm(P-P[0],axis=1);ids=np.flatnonzero(dist<=15.5);core=set(db.core_sample_indices_.tolist());R['dbscan_row1']={'neighbors_1_based':(ids+1).tolist(),'distances':dist[ids].tolist(),'core_neighbors_1_based':[int(i+1) for i in ids if int(i) in core],'core_neighbor784_count':int((np.linalg.norm(P-P[783],axis=1)<=15.5).sum()),'label':int(db.labels_[0])}
atomic_write(str(OUT/'expanded-results.json'),json.dumps(R,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'linkage_examples':{k:v['nonzero_example'] for k,v in R['linkage'].items()},'lloyd':states,'small_linkage':{k:[s['score'] for s in v] for k,v in R['small_linkage'].items()},'dbscan_row1':R['dbscan_row1'],'grid_counts':{k:{m:v['counts'] for m,v in r['methods'].items()} for k,r in R['grid'].items()}},ensure_ascii=False,indent=2))
