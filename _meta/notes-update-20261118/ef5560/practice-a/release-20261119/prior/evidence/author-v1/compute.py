from pathlib import Path
from decimal import Decimal as D
from fractions import Fraction as F
import json,sys,hashlib
sys.dont_write_bytecode=True
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
OUT=Path(__file__).parent
r={}
r['A4']={'start_pct':str(D('.20')+D('1.50')*D(0)),'end_pct':str(D('.20')+D('1.50')*D('2.00')),'increase_pp':str(D('1.50')*D('2.00'))}
cost=(D('.30')+D('.30'))*D('.0010')
net=D('.0030')-cost
r['A5']={'cost_decimal':str(cost),'net_mean_decimal':str(net),'weekly_volatility_decimal':'0.0300','net_weekly_sharpe':str(net/D('.0300'))}
r['A6']={'gross_pct':60+40,'net_pct':60-40,'long_on_100':60,'short_on_100':40}
aum=D('600000')/(D('.004')-D('.001'))
r['A16']={'annual_fee_rate':'.004','annual_variable_cost_rate':'.001','annual_fixed_cost_USD':600000,'break_even_AUM_USD':str(aum),'profit_at_options_USD':{str(a):str(D(a)*(D('.004')-D('.001'))-D('600000')) for a in [150000000,200000000,120000000,600000000]}}
r['B1_supplement']={'basis_capital':100,'long':50,'short':50,'PDD_return':'-.20','JD_return':'-.05','long_profit':str(D(50)*D('-.20')),'short_profit':str(-D(50)*D('-.05')),'profit':str(D(50)*(D('-.20')-D('-.05'))),'return_on_capital':str(D('.5')*(D('-.20')-D('-.05'))),'return_spread_not_capital_return':'-.15'}
r['B2']={'epochs':[10,30,60],'training_loss':['.0030','.0020','.0015'],'validation_loss':['.0032','.0024','.0028'],'minimum_validation_loss':'.0024','selected_epoch':30}
r['B3']={'underprediction_percentage_points':[3-1,7-4],'supplement_EL_PD1pct_EAD1000_LGD50pct':str(D('.01')*D('1000')*D('.5')),'supplement_EL_PD3pct_EAD1000_LGD50pct':str(D('.03')*D('1000')*D('.5'))}
r['B4']={'receivable_RMB':2000000,'cap_fraction':'.80','cap_RMB':str(D('2000000')*D('.80')),'existing_RMB':1300000,'remaining_RMB':str(D('2000000')*D('.80')-D('1300000')),'assumption':'Same receivable, complete and current outstanding financing; capacity is not approval.'}
actual=list(map(F,['.03','-.01','.02','-.02']))
model=list(map(F,['.02','0','.01','-.01']))
benchmark=[F('.01')]*4
err_model=[a-m for a,m in zip(actual,model)]
err_ma=[a-b for a,b in zip(actual,benchmark)]
sse_model=sum((x*x for x in err_model),F(0));sse_ma=sum((x*x for x in err_ma),F(0))
oos=1-sse_model/sse_ma
r['C1']={'model_errors':[str(float(x)) for x in err_model],'model_squared_errors':[str(float(x*x)) for x in err_model],'MA12_errors':[str(float(x)) for x in err_ma],'MA12_squared_errors':[str(float(x*x)) for x in err_ma],'SSE_model_exact':str(sse_model),'SSE_model_decimal':str(float(sse_model)),'SSE_MA12_exact':str(sse_ma),'SSE_MA12_decimal':str(float(sse_ma)),'OOS_R2_exact':str(oos),'OOS_R2_percent':float(oos)*100,'unit':'Squared decimal returns; R2 dimensionless; same four test months.'}
fee=D('2000')*D('.04'); payout=D('2000')-fee
r['C2']={'purchase_HKD':2000,'fee_HKD':str(fee),'payout_HKD':str(payout),'contribution_a_HKD':str(fee-D(18)-D(30)-D(12)),'contribution_b_HKD':str(fee-D(18)-D(55)-D(12)),'change_HKD':str(-(D(55)-D(30))),'supplement_break_even_ECL_HKD':str(fee-D(18)-D(12)),'overhead_tax_ignored':True}
assert sse_model==F(1,2500) and sse_ma==F(9,5000) and oos==F(7,9)
assert cost==D('.0006') and net/D('.03')==D('.08') and aum==D('200000000')
atomic_write(str(OUT/'computation-results.json'),json.dumps(r,ensure_ascii=False,indent=2)+'\n')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(7,3.7),layout='constrained')
epochs=r['B2']['epochs']
ax.plot(epochs,[.003,.002,.0015],marker='o',label='Training loss',color='#31688e')
ax.plot(epochs,[.0032,.0024,.0028],marker='s',label='Validation loss',color='#b85b34')
ax.scatter([30],[.0024],s=95,facecolors='none',edgecolors='black',zorder=4)
ax.annotate('Lowest of 3 candidates\n30 epochs, loss 0.0024',xy=(30,.0024),xytext=(34,.00305),arrowprops={'arrowstyle':'->'},fontsize=9)
ax.set(xlabel='Training duration (epochs)',ylabel='Loss (as provided)',title='Practice Exam A — B2(a): choose on validation, not training')
ax.set_xticks(epochs);ax.set_ylim(.0012,.0035);ax.grid(alpha=.2);ax.legend(loc='lower left')
fig.savefig(OUT/'b2-loss.svg');fig.savefig(OUT/'b2-loss.png',dpi=150);plt.close(fig)
print(json.dumps(r,ensure_ascii=False,indent=2))
