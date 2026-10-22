"""M07 readability repair: balance tracking and small-trade marginal-price examples.
Lecture pp.38-40; added quantities explicitly marked as note supplements.
Output beside script. Does not fetch market data or touch original materials.
"""
from pathlib import Path
from decimal import Decimal, getcontext
import json
getcontext().prec=40
D=Decimal
def trade(x,y,q):
 x,y,q=map(D,map(str,[x,y,q]));k=x*y;xa=x-q;ya=k/xa;pay=ya-y
 return dict(eth_before=str(x),usdc_before=str(y),buy_eth=str(q),eth_after=str(xa),usdc_after=str(ya),payment=str(pay),average=str(pay/q),start_marginal=str(y/x),end_marginal=str(ya/xa))
main=trade(100,200000,10)
newy=D(main['usdc_after'])
r={'main':main,'small_trades':[trade(100,200000,q) for q in [1,0.1,0.01,0.001]],'after_trade_small':trade(90,newy,'0.01'),'deep':trade(1000,2000000,10),'lp_share_2pct':str(D(2000000)*D('0.003')*D('0.02')),'staking_original_usd':str(D(10)*D(1600)),'staking_reward_usd':str(D('0.4')*D(1600)),'leverage_1pct_change':str(D(1000)*D('0.01')),'supply_era_amounts':[str(D(10500000)/(D(2)**i)) for i in range(4)],'premia':{'pool_value_external_fixed_before':str(D(100)*D(2000)+D(200000)),'pool_value_external_fixed_after':str(D(90)*D(2000)+newy)}}
assert D(main['eth_after'])+D(main['buy_eth'])==100
assert abs(newy-D(200000)-D(main['payment']))<D('1e-30')
assert D(r['small_trades'][-1]['average'])<D(r['small_trades'][0]['average'])
out=Path(__file__).resolve().parent
(out/'amm-readability-results.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps(r,ensure_ascii=False,indent=2))
