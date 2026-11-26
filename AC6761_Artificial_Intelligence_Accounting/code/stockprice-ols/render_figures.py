"""Editable author source for the two learning figures (local computation only)."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--data',required=True)
parser.add_argument('--output-dir',required=True)
args=parser.parse_args()
DATA=Path(args.data).resolve();OUT=Path(args.output_dir).resolve()
if OUT.is_relative_to(DATA.parent):raise ValueError('Derived figures must remain outside the original source directory.')
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','pdf.fonttype':42,'font.size':10})
def save(fig,name):
 for ext in ['svg','pdf']:fig.savefig(OUT/(name+'.'+ext),bbox_inches='tight')
 fig.savefig(OUT/(name+'.png'),bbox_inches='tight',dpi=720)
 plt.close(fig)
x=np.array([1,2,3]); y=np.array([2,2,5]);fig,ax=plt.subplots(figsize=(6.2,3.8))
xx=np.linspace(.7,3.3,100);ax.plot(xx,1.5*xx,label='Fitted line: y = 1.5 x',color='#2168a6')
ax.scatter(x,y,color='#202c35',zorder=5,label='Illustrative observations')
for xi,yi in zip(x,y):ax.plot([xi,xi],[1.5*xi,yi],color='#b34b35',ls='--',lw=1.6)
ax.annotate('At x = 2: actual 2 - fitted 3 = residual -1',xy=(2,2.5),xytext=(.8,4.6),arrowprops={'arrowstyle':'->','color':'#b34b35'},fontsize=9)
ax.set(xlabel='Illustrative x (arbitrary units)',ylabel='Illustrative y (arbitrary units)',xlim=(.6,3.4),ylim=(.5,5.8));ax.grid(alpha=.2);ax.legend(loc='lower right',fontsize=8);fig.tight_layout();save(fig,'ols-residual-example')
df=pd.read_csv(DATA);X=np.column_stack([np.ones(len(df)),df[['bmratio','roe','size']].to_numpy()]);beta=np.linalg.lstsq(X,df.stockprice.to_numpy(),rcond=None)[0];fitted=X@beta
fig,ax=plt.subplots(figsize=(6.2,3.8));ax.scatter(fitted,df.stockprice,s=3,alpha=.18,color='#2168a6',edgecolors='none');lo=min(fitted.min(),df.stockprice.min());hi=max(fitted.max(),df.stockprice.max());ax.plot([lo,hi],[lo,hi],ls='--',color='#b34b35',label='actual = fitted')
ax.set(xlabel='In-sample fitted stockprice (file units)',ylabel='Observed stockprice (file units)',title='All 36,103 observations; no axis trimming');ax.grid(alpha=.2);ax.legend(fontsize=8);fig.tight_layout();save(fig,'observed-vs-fitted')
print('source',len(df),'negative_fitted',int((fitted<0).sum()),'fitted_range',float(fitted.min()),float(fitted.max()))
