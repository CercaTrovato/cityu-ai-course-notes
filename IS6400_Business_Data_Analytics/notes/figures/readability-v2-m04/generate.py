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
plt.rcParams.update({'svg.fonttype':'none','font.size':11})
ap=argparse.ArgumentParser(description='Reproduce registered teaching SVG assets')
ap.add_argument('--output-dir',type=Path,default=BASE,help='Default: directory beside this generator')
args=ap.parse_args()
out=args.output_dir.resolve()
out.mkdir(parents=True,exist_ok=True)
x=np.array([[1.,1.],[2.,1.],[3.,2.],[4.,3.],[5.,3.]])
mu=x.mean(axis=0);d=x-mu;s=d.T@d/(len(x)-1)
eig,u=np.linalg.eigh(s);order=np.argsort(eig)[::-1];eig=eig[order];u=u[:,order]
if u[0,0]<0:u[:,0]*=-1
z=d@u[:,0];rec=z[:,None]*u[:,0]+mu;res=x-rec
assert np.allclose(s,[[2.5,1.5],[1.5,1]])
assert np.allclose(res@u[:,0],0,atol=1e-12)
assert np.isclose((res**2).sum(),(len(x)-1)*eig[1])
fig,axs=plt.subplots(1,2,figsize=(12,5))
axs[0].scatter(*x.T,label='Original point',marker='o',s=60)
axs[0].scatter(*rec.T,label='Reconstruction',marker='s',facecolors='none',edgecolors='#ab5b28',s=75)
line=mu+np.array([-3.,3.])[:,None]*u[:,0];axs[0].plot(*line.T,color='#333',label='First axis through mean')
for a,b in zip(x,rec):axs[0].plot([a[0],b[0]],[a[1],b[1]],'--',color='#777')
axs[0].scatter(*mu,marker='X',s=110,color='#333');axs[0].annotate('mean=(3,2)',mu,xytext=(12,-22),textcoords='offset points')
axs[0].annotate('x=(1,1)',x[0],xytext=(-5,-25),textcoords='offset points')
axs[0].annotate('x_hat=(1.106,0.829)',rec[0],xytext=(20,-2),textcoords='offset points')
axs[0].set_title('Keep axis; discard perpendicular residual')
for i,value in enumerate(z):axs[1].scatter(value,0,marker='o',s=60);axs[1].annotate('row '+str(i+1)+'\nz='+format(value,'.3f'),(value,0),xytext=(0,15 if i%2==0 else -40),textcoords='offset points',ha='center')
axs[1].axhline(0,color='#777');axs[1].set_title('Same 5 objects, now one coordinate each');axs[1].set_xlabel('z: coordinate along first unit axis');axs[1].set_yticks([]);axs[1].set_ylim(-.5,.5)
axs[0].set_aspect('equal');axs[0].set_xlabel('Original x1');axs[0].set_ylabel('Original x2');axs[0].legend(loc='upper left',fontsize=9)
for ax in axs:ax.grid(alpha=.25)
fig.tight_layout();buf=io.StringIO();fig.savefig(buf,format='svg',bbox_inches='tight');save(out/'pca-projection.svg',buf.getvalue());plt.close(fig)
result={'source':'M04 §2.13.3/2.14.2 existing explicit teaching data','x':x.tolist(),'mu':mu.tolist(),'sample_covariance':s.tolist(),'eigenvalues':eig.tolist(),'unit_axis':u[:,0].tolist(),'z':z.tolist(),'reconstructed':rec.tolist(),'SSE':float((res**2).sum()),'variance_ratio':float(eig[0]/eig.sum()),'visual_review':'pending'}
save(out/'calculation-evidence.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n');save(out/'figure-inputs.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
