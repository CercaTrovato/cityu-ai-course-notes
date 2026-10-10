from pathlib import Path
import sys,io,json,argparse
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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ap=argparse.ArgumentParser(description='Reproduce registered teaching SVG assets')
ap.add_argument('--output-dir',type=Path,default=BASE,help='Default: directory beside this generator')
ap.add_argument('--only',choices=['all','lloyd-states','link-distances','dbscan-neighborhood'],default='all')
args=ap.parse_args()
out=args.output_dir.resolve()
out.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'svg.fonttype':'none','font.size':11})
evidence={}
def export(fig,name):
    buf=io.StringIO();fig.savefig(buf,format='svg',bbox_inches='tight');save(out/(name+'.svg'),buf.getvalue());plt.close(fig)
if args.only in ['all','lloyd-states']:
    x=np.array([0.,2.,3.,9.,10.])
    states=[([0,3],[0,1,1,1,1],'Initial assignment: J = 86'),([0,6],[0,1,1,1,1],'Update centers: J = 50'),([0,6],[0,0,0,1,1],'Reassign: J = 38'),([5/3,9.5],[0,0,0,1,1],'Update: J = 31/6')]
    fig,axs=plt.subplots(4,1,figsize=(10,7),sharex=True)
    vals=[]
    for ax,(centers,labels,title) in zip(axs,states):
        c=np.array(centers);z=np.array(labels);j=float(((x-c[z])**2).sum());vals.append(j)
        for cluster,marker,color in [(0,'o','#26769e'),(1,'s','#ab5b28')]:
            mask=z==cluster
            ax.scatter(x[mask],np.zeros(mask.sum()),color=color,marker=marker,s=70,
                       label='Cluster '+str(cluster+1)+' ('+('circle' if cluster==0 else 'square')+')')
        ax.scatter(c,np.ones(2)*0.22,c=['#26769e','#ab5b28'],marker='X',s=120)
        for k,p in enumerate(x):ax.text(p,-0.13,str(int(p))+' [G'+str(z[k]+1)+']',ha='center',fontsize=10)
        for k,p in enumerate(c):ax.annotate('C'+str(k+1)+'='+format(p,'.3g'),(p,.22),xytext=(p,.4),ha='center')
        ax.set_ylim(-.32,.58);ax.set_yticks([]);ax.set_title(title,loc='left');ax.grid(axis='x',alpha=.25)
    axs[0].legend(loc='upper right',fontsize=9,ncol=2)
    axs[-1].set_xlabel('Position (teaching coordinate); X markers are centers C1/C2')
    fig.tight_layout();export(fig,'lloyd-states')
    assert np.allclose(vals,[86,50,38,31/6]);evidence['lloyd']={'x':x.tolist(),'states':states,'J':vals,'labels_after_next_assignment':np.argmin((x[:,None]-np.array([5/3,9.5])[None,:])**2,axis=1).tolist()}
if args.only in ['all','link-distances']:
    A=np.array([[0.,0.],[0.,2.]]);B=np.array([[3.,0.],[3.,4.]])
    dist=np.linalg.norm(A[:,None,:]-B[None,:,:],axis=2)
    fig,axs=plt.subplots(1,3,figsize=(12,4))
    for ax in axs:
        ax.scatter(*A.T,marker='o',s=65,label='A');ax.scatter(*B.T,marker='s',s=65,label='B')
        for group,points in [('A',A),('B',B)]:
            for i,point in enumerate(points):ax.annotate(group+str(i+1),point,xytext=(5,5),textcoords='offset points')
        ax.set_aspect('equal');ax.set_xlim(-.7,3.7);ax.set_ylim(-.7,4.7);ax.set_xlabel('x');ax.set_ylabel('y');ax.grid(alpha=.25)
    for i in range(2):
        for j in range(2):axs[0].plot([A[i,0],B[j,0]],[A[i,1],B[j,1]],color='#777',alpha=.65)
    axs[0].set_title('4 cross-cluster pairs\nMIN=3; MAX=5; mean=3.8028')
    ca=A.mean(axis=0);cb=B.mean(axis=0);cc=np.vstack([A,B]).mean(axis=0)
    axs[1].scatter(*ca,marker='X',s=110);axs[1].scatter(*cb,marker='X',s=110)
    axs[1].plot([ca[0],cb[0]],[ca[1],cb[1]],color='#333');axs[1].set_title('Centroids: (0,1), (3,2)\ndistance = sqrt(10)')
    axs[2].scatter(*cc,marker='X',s=130,color='#222',label='Merged center')
    for point in np.vstack([A,B]):axs[2].plot([point[0],cc[0]],[point[1],cc[1]],color='#777',alpha=.7)
    axs[2].set_title('Ward: SSE 10 -> 20\nincrease = 10')
    fig.tight_layout();export(fig,'link-distances')
    old=float(((A-ca)**2).sum()+((B-cb)**2).sum());new=float(((np.vstack([A,B])-cc)**2).sum());assert np.isclose(new-old,10)
    evidence['links']={'A':A.tolist(),'B':B.tolist(),'cross_distances':dist.tolist(),'min':float(dist.min()),'max':float(dist.max()),'average':float(dist.mean()),'centroid_distance':float(np.linalg.norm(ca-cb)),'SSE_before':old,'SSE_after':new,'ward_delta':new-old}
if args.only in ['all','dbscan-neighborhood']:
    x=np.array([0,.1,.2,.4,1.]);eps=.21;neigh=np.abs(x[:,None]-x[None,:])<=eps;core=neigh.sum(axis=1)>=3
    border=(neigh[:,core].any(axis=1))&~core;noise=~core&~border
    fig,ax=plt.subplots(figsize=(11,3.8))
    for mask,marker,label,color in [(core,'o','Core','#26769e'),(border,'s','Border','#ab5b28'),(noise,'x','Noise','#333')]:ax.scatter(x[mask],np.zeros(mask.sum()),marker=marker,label=label,color=color,s=100)
    for i,point in enumerate(x):ax.text(point,-.12,str(point)+' (n='+str(neigh[i].sum())+')',ha='center',rotation=35)
    ax.plot([.2-eps,.2+eps],[.32,.32],color='#26769e',linewidth=3);ax.text(.2,.38,'Neighborhood of 0.2: [ -0.01, 0.41 ]',ha='center')
    for i,j in [(0,1),(1,2)]:ax.annotate('',(x[j],.05),(x[i],.05),arrowprops={'arrowstyle':'-','color':'#26769e','linewidth':2})
    ax.annotate('Attach border; do not expand',(.4,.03),(.6,.58),arrowprops={'arrowstyle':'->','color':'#ab5b28'},ha='center')
    ax.set_ylim(-.32,.73);ax.set_xlim(-.25,1.2);ax.set_yticks([]);ax.set_xlabel('Position; eps=0.21; MinPts=3 (self included)');ax.legend(loc='upper left');ax.grid(axis='x',alpha=.25);fig.tight_layout();export(fig,'dbscan-neighborhood')
    assert neigh.sum(axis=1).tolist()==[3,3,4,2,1]
    evidence['dbscan']={'x':x.tolist(),'eps':eps,'MinPts':3,'counts':neigh.sum(axis=1).tolist(),'core':x[core].tolist(),'border':x[border].tolist(),'noise':x[noise].tolist()}
save(out/'calculation-evidence.json',json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
if args.only=='all':
    save(out/'figure-inputs.json',json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
else:
    # A partial run must not overwrite inputs of unaffected diagrams.
    save(out/(args.only+'-inputs.json'),json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'only':args.only,'output_dir':str(out),'calculations':evidence,'visual_review':'pending'},ensure_ascii=False))
