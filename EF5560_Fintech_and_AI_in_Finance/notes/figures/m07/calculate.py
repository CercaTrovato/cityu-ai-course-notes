"""EF5560 M07: reproduce lecture examples and explicitly labelled variants.
Inputs: fixed hypothetical values on Lec07 pp.11,14-16,25-29,38-40,43,47,52,54.
Output: results.json, market-path.svg, pool-prices.svg. No source files changed.
Run with D:/anaconda3/python.exe -X utf8 calculate.py; outputs beside this script.
Charts describe given examples, not observed investment performance.
"""
from pathlib import Path
from math import prod
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'Microsoft YaHei','svg.fonttype':'none','axes.unicode_minus':False,'font.size':12})
results={}
results['issuance']={'first_era_btc':210000*50,'geometric_limit_btc':210000*50/(1-0.5),'daily':[s*144 for s in [50,25,12.5,6.25,3.125,1.5625]]}
path=[100.0]
for r in [-0.237,-0.204,-0.126,0.396]: path.append(path[-1]*(1+r))
results['market']={'index':path,'cumulative_change':path[-1]/100-1}
results['nav']={'common_claim':100-20-10,'premium':150/100-1,'loss_on_premium_collapse':100/150-1,'new_nav':115/11,'old_percentage':1/10,'new_percentage':1/11,'below_nav':108/11,'variant_premium':120/100-1,'variant_loss':100/120-1}
results['mining']={'revenue':0.01*10000000,'profit':0.01*10000000-120000,'halving_drop':1-(80*0.5+20)/100,'variant_drop':1-(60*0.5+40)/100,'hash_share_after_expansion':1/200}
results['staking']={'eth':10*1.04,'usd':10*1.04*1600,'return':1.04*0.8-1,'breakeven_price':2000/1.04,'breakeven_drop':1/1.04-1,'variant_return':1.04*0.9-1}
results['fee']={'dollar_fee':0.001*2000,'small_ratio':2/20,'large_ratio':2/500,'supply_variants':[100+3-2,100+3-4],'rollup_per_transaction':100/100}
def amm(x,y,q):
    assert 0<q<x
    k=x*y; xa=x-q; ya=k/xa; paid=ya-y
    return {'x':x,'y':y,'q':q,'k':k,'x_after':xa,'y_after':ya,'payment':paid,'average':paid/q,'final_marginal':ya/xa}
results['amm']={'shallow':amm(100,200000,10),'deep':amm(1000,2000000,10),'variant_1eth':amm(100,200000,1),'variant_50eth':amm(100,200000,50)}
results['amm']['arbitrage_no_fees']=results['amm']['shallow']['payment']-2000*10
results['lp']={'total_fees':2000000*0.003,'investor_fees':2000000*0.003*0.05,'variant_net':300-500}
results['platform']={'gross_fees':1000000000*0.0003,'after_rebate':1000000000*0.0003-60000}
results['etf']={'cost':10000*0.005+10+10,'ratio':(10000*0.005+20)/10000,'variant_cost':1000*0.005+20,'variant_ratio':(1000*0.005+20)/1000}
results['ml']={'precision':20/100,'false_discovery_share':80/100,'recall_variant':20/(20+30)}
results['drawdown']={'end':100*0.5*1.5,'total':0.5*1.5-1,'recovery':1/0.5-1,'variant_end':100*0.8*1.2,'variant_recovery':1/0.8-1}
assert round(results['staking']['return'],3)==-0.168
assert round(results['amm']['shallow']['payment'],2)==22222.22
assert results['mining']['profit']==-20000
assert round(results['etf']['ratio'],3)==0.007
(out/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
fig,ax=plt.subplots(figsize=(8.6,3.7),layout='constrained')
labels=['起点','2025 Q4','2026 Q1','2026 Q2','2026 Q3']
ax.plot(labels,path,marker='o',linewidth=2.5,color='#1d5368');ax.axhline(100,ls='--',color='#8a5b40')
for i,v in enumerate(path): ax.annotate(f'{v:.2f}',(i,v),xytext=(0,9),textcoords='offset points',ha='center')
ax.set_ylim(40,115);ax.set_ylabel('市值指数（起点 = 100）');ax.set_title('课件给定季度变化的复合路径（非持仓回测）');ax.grid(axis='y',alpha=0.2)
fig.savefig(out/'market-path.svg');fig.savefig(out/'market-path.png',dpi=140);plt.close(fig)
fig,ax=plt.subplots(figsize=(8.6,3.7),layout='constrained')
vals=[results['amm'][p]['average'] for p in ['shallow','deep']]
bars=ax.bar(['100 ETH / 200,000 USDC','1,000 ETH / 2,000,000 USDC'],vals,color=['#1d5368','#509c93'],width=0.5)
ax.axhline(2000,color='#8a5b40',ls='--',label='交易前边际价 2,000')
ax.bar_label(bars,labels=[f'{v:,.2f}' for v in vals],padding=6)
ax.set_ylim(0,2600);ax.set_ylabel('平均成交价（USDC/ETH）');ax.set_title('同样买 10 ETH：深池价格冲击较小（忽略全部费用）');ax.legend(loc='lower right');ax.grid(axis='y',alpha=0.2)
fig.savefig(out/'pool-prices.svg');fig.savefig(out/'pool-prices.png',dpi=140);plt.close(fig)
print(json.dumps(results,ensure_ascii=False,indent=2))
