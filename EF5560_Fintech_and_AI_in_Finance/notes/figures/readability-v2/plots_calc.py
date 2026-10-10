from pathlib import Path
import argparse,sys,json,hashlib
sys.dont_write_bytecode=True
ap=argparse.ArgumentParser()
ap.add_argument('--vault-root',required=True)
ap.add_argument('--output',required=True)
a=ap.parse_args(); ROOT=Path(a.vault_root); WORK=Path(a.output)
sys.path.insert(0,str(ROOT/'_meta/tools'))
from safe_write import atomic_write
def put(p,s):
    p.parent.mkdir(parents=True,exist_ok=True);atomic_write(str(p),s)
def jput(p,o):put(p,json.dumps(o,ensure_ascii=False,indent=2)+'\n')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import StringIO,BytesIO
plt.rcParams.update({'font.family':'Microsoft YaHei','axes.unicode_minus':False,'svg.fonttype':'none','font.size':12})
ASSET='EF5560_Fintech_and_AI_in_Finance/notes/figures/readability-v2/'
def save(fig,name):
    svg=StringIO();fig.savefig(svg,format='svg',bbox_inches='tight');put(WORK/'candidate'/ASSET/(name+'.svg'),svg.getvalue())
    png=BytesIO();fig.savefig(png,format='png',dpi=150,bbox_inches='tight')
    p=WORK/'preview'/(name+'.png');p.parent.mkdir(parents=True,exist_ok=True)
    atomic_write(str(p),png.getvalue().decode('latin-1'),encoding='latin-1')
    plt.close(fig)
x=np.array([-1.,0.,1.]);y=np.array([-.8,.1,1.3]);beta=np.sum((x-x.mean())*(y-y.mean()))/np.sum((x-x.mean())**2);alpha=y.mean()-beta*x.mean();fit=alpha+beta*x
fig,ax=plt.subplots(figsize=(8,5));ax.scatter(x,y,label='三个已实现月（教学数据）');xx=np.linspace(-1.2,1.2,80);ax.plot(xx,alpha+beta*xx,label='OLS：alpha=0.2%，beta=1.05');ax.plot([0,0],[0,alpha],lw=4,label='截距：市场超额为零时的高度');ax.plot([0,0],[y[1],fit[1]],ls='--',lw=3,label='中间点残差 −0.1 个百分点');ax.axhline(0,color='grey',lw=.8);ax.axvline(0,color='grey',lw=.8);ax.set_xlabel('市场月超额收益（%）');ax.set_ylabel('组合月超额收益（%）');ax.set_title('同一月的偏离不是跨月截距（M05 §2.32 教学补充）');ax.legend(fontsize=10);save(fig,'capm-example')
X=np.array([[2,1],[1,2],[-1,-2],[-2,-1]],float);target=np.array([1,-1,1,-1],float);sd=X.std(axis=0,ddof=1);Z=X/sd;wp=np.array([1,1])/np.sqrt(2);wm=np.array([1,-1])/np.sqrt(2);t1=Z@wp;t2=Z@wm
fig,ax=plt.subplots(figsize=(7,6));ax.scatter(Z[:,0],Z[:,1],s=90,c=['#245b88' if v>0 else '#b94d3e' for v in target]);
for i,(u,v) in enumerate(Z):ax.annotate(f'行{i+1}；y={target[i]:+.0f}',(u,v),xytext=(8,6),textcoords='offset points',fontsize=10)
for w,name in [(wp,'PC1 高方差方向 1.8'),(wm,'低方差 / 本例 PLS 方向 0.2')]:
    ax.plot([-1.5*w[0],1.5*w[0]],[-1.5*w[1],1.5*w[1]],label=name)
ax.set_aspect('equal');ax.set_xlabel('训练标准化 z1（无单位）');ax.set_ylabel('训练标准化 z2（无单位）');ax.set_title('输入变化最大，未必与 y 有关（M03 教学补充）');ax.legend(fontsize=10,loc='upper left',bbox_to_anchor=(1.02,1));save(fig,'pcr-pls-directions')
q=t2@target/(t2@t2); newz=np.array([3.,1.])/sd
calc={'source':'笔记中明确标注的教学小数据；未重跑原课程模型','capm':{'x_percent':x.tolist(),'y_percent':y.tolist(),'alpha_percent':alpha,'beta':beta,'fit_percent':fit.tolist(),'residual_percent':(y-fit).tolist()},'pcr_pls':{'X':X.tolist(),'y':target.tolist(),'sample_sd':sd.tolist(),'cov':np.cov(Z,rowvar=False).tolist(),'T1':t1.tolist(),'T2':t2.tolist(),'PCR_K1':float((t1@target)/(t1@t1)),'PLS_q':float(q),'new_raw':[3,1],'new_PLS':float(newz@wm*q)},'fees':{'capital':1000000,'buy':200000,'sell':200000,'fee_rate':.001,'fee':400},'rank_all_equal':{'average_ranks':[3]*5,'centered':[.1]*5}}
bx=np.array([4,1,1,3,2,5,2,6],float);by=np.array([8,1,-1,3,2,6,0,9],float)
order=np.argsort(bx,kind='stable');groups=[order[i:i+2] for i in range(0,8,2)];means=np.array([[bx[g].mean(),by[g].mean()] for g in groups])
fig,axs=plt.subplots(1,2,figsize=(10,4));axs[0].scatter(bx,by)
for i,(u,v) in enumerate(zip(bx,by)):axs[0].annotate(str(i+1),(u,v),xytext=(5,5),textcoords='offset points')
axs[1].plot(means[:,0],means[:,1],marker='o');axs[0].set_title('原8行（标签是原ID）');axs[1].set_title('每箱2行后的4个均值点')
for ax in axs:ax.set_xlabel('教学输入 x');ax.set_ylabel('教学输出 y')
fig.subplots_adjust(top=.78,wspace=.28)
save(fig,'binning-example')
calc['binning']={'x':bx.tolist(),'y':by.tolist(),'groups_original_ID':[[int(i+1) for i in g] for g in groups],'mean_points':means.tolist(),'tie_rule':'原行顺序打破并列，四箱每箱2行，教学例非官方10箱'}
jput(WORK/'important-calculations.json',calc)
print(json.dumps(calc,ensure_ascii=False))
