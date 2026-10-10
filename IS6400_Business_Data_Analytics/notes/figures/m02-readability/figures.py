from pathlib import Path
import sys,io,json
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
plt.rcParams['svg.fonttype']='none'
def output(fig,name):
 buff=io.StringIO();fig.savefig(buff,format='svg');atomic_write(str(HERE/(name+'.svg')),buff.getvalue());plt.close(fig)
x=np.array([0.,1.,2.]);y=np.array([1.,2.,2.]);X=np.column_stack([np.ones(3),x-1]);theta=np.zeros(2);states=[]
for k in range(21):
 error=X@theta-y;J=error@error/6;g=X.T@error/3
 states.append({'step':k,'a_c':float(theta[0]),'b':float(theta[1]),'J':float(J),'gradient':g.tolist()})
 if np.max(np.abs(g))<.001:break
 theta=theta-g
assert len(states)==7
fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
axes[0].plot([s['step'] for s in states],[s['b'] for s in states],'o-',label='b (eta=1, centered X)');axes[0].axhline(.5,ls='--',color='black',label='OLS b=0.5');axes[0].set(xlabel='completed updates',ylabel='slope b',title='State read before next update');axes[0].legend(fontsize=9)
axes[1].plot([s['step'] for s in states],[s['J'] for s in states],'o-',label='centered, eta=1');axes[1].set(xlabel='completed updates',ylabel='J=SSE/(2n)',title='Stops at step 6: max |gradient| < 0.001');axes[1].legend(fontsize=9)
output(fig,'gd-states')
lams=np.linspace(0,1,301);b_r=1/(2+3*lams);b_l=np.maximum(1/3-lams,0)/(2/3)
fig,ax=plt.subplots(figsize=(9,4),layout='constrained');ax.plot(lams,b_r,label='Ridge: u/(v+lambda)',lw=2);ax.plot(lams,b_l,label='Lasso: max(u-lambda,0)/v',lw=2);ax.axvline(1/3,ls='--',color='black',label='Lasso threshold 1/3');ax.scatter([.1],[1/2.3],marker='o');ax.scatter([.1],[.35],marker='s');ax.set(xlabel='lambda in declared teaching objective',ylabel='slope b',title='Same centered input: u=1/3, v=2/3; intercept not penalized');ax.legend(fontsize=9);output(fig,'regularization-paths')
results={'source':'M02 §2.8.4与§2.10.3原三点教学例；非原鸡蛋/15阶曲线','training_x':x.tolist(),'training_y':y.tolist(),'GD':{'design':'[1,x-1]','eta':1,'max_updates':20,'gradient_tolerance':.001,'states':states,'stop_reason':'gradient_tolerance','raw_intercept':float(theta[0]-theta[1]),'slope':float(theta[1])},'paths':{'u':1/3,'v':2/3,'lambda':lams.tolist(),'ridge':b_r.tolist(),'lasso':b_l.tolist(),'ridge_objective':'SSE/(2n)+lambda*b^2/2','lasso_objective':'SSE/(2n)+lambda*abs(b)','threshold':1/3,'lambda_0_1':{'ridge':1/2.3,'lasso':.35}},'versions':{'numpy':np.__version__,'matplotlib':matplotlib.__version__}}
atomic_write(str(HERE/'results.json'),json.dumps(results,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'GD':results['GD'],'path_example':results['paths']['lambda_0_1']},ensure_ascii=False))
