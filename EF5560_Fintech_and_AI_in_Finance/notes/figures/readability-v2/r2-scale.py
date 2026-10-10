"""M01 §2.9.3：真实样本内关系与明确合成关系的同尺度比较。

计算链来自课程 code/L02_regression/03_r2_scale.py；不调用其 vault 写入入口。
运行参数 --data 指向 spy_monthly_features_240m.csv，--output 指向本脚本所在候选目录。
真实月对数收益；同一240个输入；合成关系 seed=5560、R2=0.5。
图不能证明样本外准确性、因果关系或投资价值。
"""
from pathlib import Path
import argparse,io,json,hashlib,sys
sys.dont_write_bytecode=True
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);ap.add_argument('--output',required=True)
a=ap.parse_args();src=Path(a.data);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(src);x=d.volatility_12;y=d.market_return
assert len(d)==240 and x.notna().all() and y.notna().all()
real=sm.OLS(y,sm.add_constant(x)).fit()
z=(x-x.mean())/x.std(ddof=1)
e=pd.Series(np.random.default_rng(5560).standard_normal(len(z)),index=z.index)
e-=e.mean();e-=(e@z)/(z@z)*z;e/=e.std(ddof=1);z/=z.std(ddof=1)
ystar=np.sqrt(0.5)*z+np.sqrt(0.5)*e
ysyn=y.mean()+y.std(ddof=1)*ystar/ystar.std(ddof=1)
syn=sm.OLS(ysyn,sm.add_constant(x)).fit()
assert abs(syn.rsquared-0.5)<1e-12
assert abs(ysyn.mean()-y.mean())<1e-12 and abs(ysyn.std(ddof=1)-y.std(ddof=1))<1e-12
plt.rcParams.update({'font.family':'Microsoft YaHei','axes.unicode_minus':False,'svg.fonttype':'none','font.size':13})
# 纵向排列保证 768px 阅读栏仍能读到坐标、单位和底部边界说明。
fig,axes=plt.subplots(2,1,figsize=(10.2,13.2),sharex=True,sharey=True)
xx=np.linspace(x.min(),x.max(),100)
for ax,yy,fit,title in zip(axes,[y,ysyn],[real,syn],['真实 SPY 月对数收益','合成收益：指定样本内关系']):
    ax.scatter(x,yy*100,s=26,alpha=.55,color='#527f9f',edgecolors='none')
    ax.plot(xx,(fit.params.iloc[0]+fit.params.iloc[1]*xx)*100,color='#c65134',lw=2.5,label='样本内 OLS 拟合线')
    ax.axhline(0,color='#aaaaaa',lw=.8);ax.grid(alpha=.16)
    ax.set_title(title+f'\n样本内 R² = {fit.rsquared*100:.2f}%（240 点）',fontsize=15,pad=10)
    ax.set_xlabel('滞后 12 个月年化波动率（小数；0.20 = 20%）',fontsize=13)
    ax.legend(loc='upper right',fontsize=12,framealpha=.9)
    ratio=fit.fittedvalues.std(ddof=1)/fit.resid.std(ddof=1)
    ax.text(.02,.04,f'拟合值标准差 / 残差标准差 = {ratio:.2f}',transform=ax.transAxes,fontsize=12)
axes[0].set_ylabel('月对数收益（%；百分数表示）',fontsize=13)
axes[1].set_ylabel('月对数收益（%；百分数表示）',fontsize=13)
fig.suptitle('同一输入、同一坐标：样本内拟合强弱怎样改变散点外观',fontsize=18,y=.995)
fig.text(.5,.012,'上：2006-07 至 2026-06 真实数据。下：seed 5560 的合成教学对照，保持收益均值与标准差。\n两图均无样本外检验；R² 的量级不能自动转成投资价值。',ha='center',fontsize=13)
fig.tight_layout(rect=[.05,.06,.98,.97],h_pad=2.2)
buf=io.StringIO();fig.savefig(buf,format='svg',metadata={'Date':None});atomic_write(str(out/'r2-scale.svg'),buf.getvalue())
result={'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'n':len(d),'start':d.forecast_month.iloc[0],'end':d.forecast_month.iloc[-1],'seed':5560,'real_r2':real.rsquared,'synthetic_r2':syn.rsquared,'real_fitted_residual_sd_ratio':real.fittedvalues.std(ddof=1)/real.resid.std(ddof=1),'same_mean':bool(np.isclose(y.mean(),ysyn.mean())),'same_sample_sd':bool(np.isclose(y.std(ddof=1),ysyn.std(ddof=1))),'claim_boundary':'in-sample visualization only; synthetic comparison is not empirical evidence'}
atomic_write(str(out/'r2-scale-results.json'),json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False));plt.close(fig)
