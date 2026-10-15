from pathlib import Path
import hashlib,json,argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
parser=argparse.ArgumentParser(description='M06 teaching calculations; generate in an explicit scratch directory.')
parser.add_argument('--output',required=True,help='Explicit output directory outside the vault')
OUT=Path(parser.parse_args().output).resolve()
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'Microsoft YaHei','axes.unicode_minus':False,'font.size':12,'svg.fonttype':'none'})
res={
 'volume_usd_month':100000*40,'revenue_usd_month':100000*40*.005,
 'average_cost_usd_per_tx':{str(n):10000/n+.05 for n in [10000,50000,100000]},
 'combined_partial_margin_usd_month':20000-(10000+.05*100000),
 'advance_cap_rmb':1000000*.8,'bank_b_capacity_rmb':1000000*.8-600000,
 'interest_rmb_60_days':600000*.06*60/360,'interest_rmb_30_days':600000*.06*30/360,
 'duplicate_payment_avoided_rmb':800,'treasury_topup_usd':1000000-700000,
 'released_cash_usd':2000000-1200000,'annual_opportunity_saving_usd':800000*.04,
 'net_annual_saving_usd':180000-60000,'payback_years':300000/(180000-60000),
 'handling_minutes_saved':40-25,'handling_relative_reduction':(40-25)/40,
 'reconciliation_change_pp':4-12,'default_change_pp':2.1-2,
 'loan_profit_rmb_before':8000-4000-2000-1500,'loan_profit_rmb_after':8000-4000-2000-1000,
 'variants':{'half_fee_revenue':4000000*.0025,'half_fee_margin':10000-15000,'bank_b_after_repayment':800000-500000,'opportunity_at_2pct':800000*.02,'payback_higher_run_cost':300000/(180000-120000)},
 'hash_original':hashlib.sha256(b'Invoice amount USD 10000').hexdigest(),
 'hash_altered':hashlib.sha256(b'Invoice amount USD 90000').hexdigest(),
 'hash_same_input_equal':hashlib.sha256(b'Invoice amount USD 10000').digest()==hashlib.sha256(b'Invoice amount USD 10000').digest(),
 'source':'Lec06 p.10–11,p.20,p.37–40,p.44–45,p.49,p.52–53; teaching assumptions, not observed business outcomes'
}
assert res['volume_usd_month']==4000000 and res['payback_years']==2.5
assert res['hash_original']!=res['hash_altered']
trials=[]
for nonce in range(10000):
    digest=hashlib.sha256(('block101|prev100|Alice pays Bob 1|'+str(nonce)).encode()).hexdigest()
    hit=digest.startswith('0')
    trials.append({'nonce':nonce,'digest':digest,'hit':hit})
    if hit:break
res['pow_toy']={'input_prefix':'block101|prev100|Alice pays Bob 1|','target':'hex digest starts with 0','max_attempts':10000,'trials':trials,'stop_nonce':nonce}
res['pos_weight_toy']={'total_stake':100,'group_weights':[40,35,25],'first_support':40,'second_support':75,'checkpoint_threshold':'at least two thirds; not a full Ethereum state machine'}
assert nonce==3
(OUT/'results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
def save(fig,name):
    fig.tight_layout();fig.savefig(OUT/f'{name}.svg');fig.savefig(OUT/f'{name}.png',dpi=140);plt.close(fig)
fig,ax=plt.subplots(figsize=(7,4));x=['1 万笔','5 万笔','10 万笔'];y=[1.05,.25,.15]
ax.bar(x,y,color='#146585');ax.set_ylabel('平均成本（美元/笔）');ax.set_xlabel('每月交易笔数');ax.set_title('固定成本分摊：讲义 p.11 教学假设')
for i,v in enumerate(y):ax.text(i,v+.025,f'{v:.2f}',ha='center')
ax.set_ylim(0,1.25);save(fig,'average-cost')
fig,ax=plt.subplots(figsize=(7,4));ax.bar([0,1],[.6,.6],label='A 已贷',color='#146585');ax.bar([0,1],[.6,.2],bottom=[.6,.6],label='B 新贷',color='#84c5ad')
ax.axhline(.8,color='#b0476e',linestyle='--',label='80% 合计上限（假设）');ax.set_xticks([0,1],['B 贷 60 万','B 贷 20 万']);ax.set_ylabel('融资合计（人民币百万元）');ax.set_title('同一应收款 100 万元：讲义 p.37');ax.legend(fontsize=10,loc='upper right');ax.set_ylim(0,1.5);save(fig,'financing-capacity')
fig,ax=plt.subplots(figsize=(7,4));ax.bar(['采用前','采用后'],[2,1.2],color='#146585');ax.set_ylabel('平均闲置现金（美元百万元）');ax.set_ylim(0,2.5);ax.set_title('现金释放 0.8 百万美元：讲义 p.45 教学假设')
for i,v in enumerate([2,1.2]):ax.text(i,v+.05,str(v),ha='center')
save(fig,'idle-cash')
fig,ax=plt.subplots(figsize=(7,4));ax.bar(['年节省','年运行费'],[180,60],color=['#146585','#84c5ad']);ax.set_ylabel('美元千元/年');ax.set_ylim(0,220);ax.set_title('净年节省 120 千美元：讲义 p.49 教学假设')
for i,v in enumerate([180,60]):ax.text(i,v+4,str(v),ha='center')
save(fig,'adoption-cost')
print(json.dumps(res,ensure_ascii=False,indent=2))
