"""EF5560 M05 图源；只读 Class05 CSV。用 --data 和 --output 指定输入/输出。"""
from pathlib import Path
import argparse, json, hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);ap.add_argument('--output',required=True)
a=ap.parse_args(); data=Path(a.data); out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'Microsoft YaHei','axes.unicode_minus':False,'font.size':11,'svg.fonttype':'none'})
hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(data.iterdir()) if f.is_file()}
manifest=json.loads((data/'manifest.json').read_text())
checks=[{'file':x['file'],'hash_ok':hashes[x['file']]==x['sha256'],'bytes_ok':(data/x['file']).stat().st_size==x['bytes']} for x in manifest['files']]
assert all(x['hash_ok'] and x['bytes_ok'] for x in checks)
results={'manifest':checks,'source_hashes':hashes,'metrics':{},'figure_sources':{}}
def save(fig,name,source):
    fig.tight_layout();fig.savefig(out/(name+'.svg'),bbox_inches='tight');fig.savefig(out/(name+'.png'),dpi=130,bbox_inches='tight');plt.close(fig)
    results['figure_sources'][name]=source
d=pd.read_csv(data/'stock_drop_zero_importance.csv').head(8).iloc[::-1]
fig,ax=plt.subplots(figsize=(9,4));ax.barh(d.characteristic,d.delta_r2*100,color='#24618a');ax.set_xlabel('训练 R² 的下降（百分点）');ax.set_title('逐列置零，保持原模型和观测固定（讲义 p.9）');save(fig,'importance','stock_drop_zero_importance.csv; delta_r2 * 100, not normalized shares')
panel=pd.read_csv(data/'hsi_stock_excess_return_panel.csv')
d=panel.loc[panel.forecast_week=='2026-06-26'].dropna(subset=['mom60d_rank']).sort_values('mom60d_rank')
ranks=pd.concat([d.head(5),d.tail(5)])
fig,ax=plt.subplots(figsize=(9,4));ax.barh(ranks.ticker,ranks.mom60d_rank,color=['#24618a']*5+['#b03036']*5);ax.axvline(0,color='gray');ax.set_xlabel('周开始前已知的中心化 60 日动量排名');ax.set_title('2026-06-26：79 个可用排名（讲义 p.6）');save(fig,'momentum-ranks','hsi_stock_excess_return_panel.csv, forecast_week=2026-06-26, mom60d_rank; not forecast')
m=np.linspace(-.5,.5,101);fig,ax=plt.subplots(figsize=(7,3.6));ax.plot(m,.10+.40*np.maximum(0,m),label='v=0');ax.plot(m,.10+.40*np.maximum(0,m-.25),label='v=0.25（笔记补充）',linestyle='--');ax.set_xlabel('中心化动量排名 m');ax.set_ylabel('预测周超额收益（%）');ax.set_title('讲义 p.11 给定规则的条件响应曲线');ax.legend();save(fig,'response-example','Lecture p.11 toy rule; supplemental reference v=.25; NOT empirical p.12 curve')
d=pd.read_csv(data/'weekly_momentum_sort_returns.csv');date=pd.to_datetime(d.forecast_week)
fig,ax=plt.subplots(figsize=(10,4))
for c in ['Low','Middle','High','High-Low']:
    w=np.r_[1,np.cumprod(1+d[c].to_numpy())];ax.plot(pd.Index([date.iloc[0]-pd.Timedelta(weeks=1),*date]),w,label=c)
    results['metrics']['momentum_'+c+'_terminal']=float(w[-1])
ax.set_ylabel('初始资本为 1 的累计财富');ax.set_title('动量三分组：156 周；High−Low 每边单位敞口（讲义 p.22）');ax.legend(ncol=4);save(fig,'momentum-wealth','weekly_momentum_sort_returns.csv; cumprod(1+r), unit per side spread')
d=pd.read_csv(data/'three_market_capm_returns_monthly.csv');score=pd.read_csv(data/'three_market_timing_scorecard.csv')
fig,axs=plt.subplots(1,3,figsize=(13,4),sharey=False)
for ax,(market,g) in zip(axs,d.groupby('market',sort=False)):
    g=g.sort_values('forecast_month');dt=pd.to_datetime(g.forecast_month)
    for c,label in [('market_total_return','买入持有'),('timing_total_return','OLS 择时')]:
        w=np.cumprod(1+g[c]);ax.plot(dt,w,label=label)
    ax.set_title(market);ax.set_ylabel('累计财富');ax.legend(fontsize=9)
    results['metrics'][market]={'BH_terminal':float(np.prod(1+g.market_total_return)),'timing_terminal':float(np.prod(1+g.timing_total_return)),'held':int(g.weight.sum())}
save(fig,'timing-wealth','three_market_capm_returns_monthly.csv; simple returns, cash earns zero; p33–35')
d=pd.read_csv(data/'model_portfolios_monthly.csv');summary=pd.read_csv(data/'model_portfolio_summary.csv');dt=pd.to_datetime(d.forecast_month)
fig,axs=plt.subplots(2,1,figsize=(10,7),sharex=True)
for name in ['Buy and hold','LASSO','Gradient boosting']:
    r=d[name+' portfolio return'];ex=d[name+' portfolio excess return']; w=np.r_[1,np.cumprod(1+r)];dd=w/np.maximum.accumulate(w)-1
    xs=pd.Index([dt.iloc[0]-pd.offsets.MonthEnd(1),*dt]);axs[0].plot(xs,w,label=name);axs[1].plot(xs,dd*100,label=name)
    met={'cagr':float(w[-1]**(12/len(r))-1),'vol':float(r.std(ddof=1)*np.sqrt(12)),'sharpe':float(ex.mean()/ex.std(ddof=1)*np.sqrt(12)),'mdd':float(dd.min()),'wealth':float(w[-1])}
    ref=summary[summary.strategy==name].iloc[0]
    for k,col in [('cagr','compound_annual_return'),('vol','annualized_volatility'),('sharpe','sharpe'),('mdd','maximum_drawdown')]:assert np.isclose(met[k],ref[col],atol=1e-10),(name,k,met[k],ref[col])
    results['metrics'][name]=met
axs[0].set_ylabel('累计财富（初始为 1）');axs[1].set_ylabel('距历史高点回撤（%）');axs[0].set_title('连续权重：现金赚同期无风险收益，未扣成本（讲义 p.39 / p.44）');axs[0].legend();save(fig,'continuous-performance','model_portfolios_monthly.csv; simple total wealth, excess Sharpe; initial wealth included in drawdown')
fig,ax=plt.subplots(figsize=(10,4))
for name in ['LASSO','Gradient boosting']:ax.plot(dt,d[name+' weight']*100,label=name)
ax.set_ylabel('市场仓位（%）');ax.set_title('连续权重由当时预测和滞后风险共同决定（讲义 p.40）');ax.legend();save(fig,'continuous-weights','model_portfolios_monthly.csv; supplied weight columns, zero to one')
(out/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results['metrics'],ensure_ascii=False,indent=2));print('manifest matches:',len(checks),'figures:',len(results['figure_sources']))
