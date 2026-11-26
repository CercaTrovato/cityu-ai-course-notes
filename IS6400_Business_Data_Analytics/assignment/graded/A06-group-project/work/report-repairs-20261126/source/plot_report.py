"""Report figures from saved aggregate CSVs only. No customer rows and no fitting."""
from pathlib import Path
import argparse,json,hashlib
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator,PercentFormatter
a=argparse.ArgumentParser();a.add_argument('--pack',type=Path,required=True);a.add_argument('--preview-dir',type=Path,required=True);args=a.parse_args();P=args.pack;D=P/'data';F=P/'figures';F.mkdir(exist_ok=True);args.preview_dir.mkdir(exist_ok=True,parents=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.titlesize':13,'axes.labelsize':12,'svg.fonttype':'none','svg.hashsalt':'IS6400-report-repairs-20261126','axes.spines.top':False,'axes.spines.right':False})
COL={'weighted':'#167d8d','ordinary':'#647c92','recency':'#8b6a3e','new':'#8b4b85'};saved=[]
def rd(n):return pd.read_csv(D/n)
def save(fig,name,source,note):
 for ext in ['svg','pdf']:fig.savefig(F/(name+'.'+ext),bbox_inches='tight',metadata={'Date':None} if ext=='svg' else {'CreationDate':None,'ModDate':None})
 fig.savefig(args.preview_dir/(name+'.png'),dpi=120,bbox_inches='tight');plt.close(fig)
 saved.append({'figure':name,'source_tables':source,'caption':note,'files':{ext:hashlib.sha256((F/(name+'.'+ext)).read_bytes()).hexdigest() for ext in ['svg','pdf']}})
def bars(ax,names,vals,colors):
 xx=np.arange(len(vals));ax.bar(xx,vals,color=colors);ax.set_xticks(xx,names);ax.set_ylim(0,max(vals)*1.24);ax.yaxis.set_major_locator(MaxNLocator(integer=True));ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
 for x,y in zip(xx,vals):ax.annotate(str(int(y)),(x,y),xytext=(0,5),textcoords='offset points',ha='center',fontsize=11)
flow=rd('dataset-flow.csv');fig,ax=plt.subplots(figsize=(12.5,5.8),layout='constrained')
for i,x in flow.iterrows():
 start=pd.Timestamp(x.history_start);snap=pd.Timestamp(x.snapshot);end=pd.Timestamp(x.label_end_exclusive)
 ax.barh(i,(snap-start).days,left=mdates.date2num(start),height=.44,color='#647c92',label='Historical predictors' if i==0 else None)
 ax.barh(i,(end-snap).days,left=mdates.date2num(snap),height=.44,color='#d78c31',label='90-day outcomes' if i==0 else None)
 ax.plot(mdates.date2num(snap),i,'k|',markersize=16)
ax.set_yticks(range(len(flow)),[f'{x.snapshot} | N={x.customers:,}; buyers={x.positive_customers:,}' for x in flow.itertuples()]);ax.invert_yaxis();ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3));ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'));ax.legend(loc='upper center',bbox_to_anchor=(.5,-.08),ncol=2);ax.grid(axis='x',alpha=.2);ax.set_title('Predictors precede each snapshot; outcomes follow it\nCalendar windows overlap; repeated customers are not independent new samples')
save(fig,'01-time-windows',['dataset-flow.csv'],'All intervals left-closed/right-open. October training, January development, April–June saved-model evaluation; calendar coverage is not source-system completeness.')
screen=rd('h04-screening.csv');fig,ax=plt.subplots(figsize=(11.8,5),layout='constrained');names=['LR','Weighted\nLR','Forest','Weighted\nforest','CatBoost','Weighted\nCatBoost','Recency'];bars(ax,names,screen.hits.tolist(),[COL['ordinary'],COL['weighted'],COL['ordinary'],COL['weighted'],COL['ordinary'],COL['weighted'],COL['recency']]);ax.set_ylabel('Observed repeat buyers in the list');ax.set_title('H04 screening: 7 methods, same January N=29,368 and K=2,937');fig.text(.5,-.035,'Three model families × two class-weight configurations + one rule. Ranking counts, not marketing uplift.',ha='center',fontsize=10)
save(fig,'02-initial-screening',['h04-screening.csv'],'Separate H04 saved stage. Weighted LR leads Top10% hits/AP; CatBoost leads ROC-AUC; not all metrics have the same winner.')
r3=rd('r3-methods.csv').query('top_fraction == 0.1');g=rd('r3-group-methods.csv').query('top_fraction == 0.1');new=rd('feature-experiment-results.csv').query('fraction == 0.1');fig,axs=plt.subplots(1,2,figsize=(14,5.2),layout='constrained')
oldvals=r3.hits.tolist()+g.loc[~g.method.eq('F0_global_weighted'),'hits'].tolist();bars(axs[0],['Base\nU','Base\nW','Delivery\nU','Delivery\nW','Review\nU','Review\nW','+Group','Separate\ngroups'],oldvals,[COL['ordinary'],COL['weighted']]*3+[COL['new']]*2);axs[0].set_title('Saved member R3 configurations');axs[0].set_ylabel('Observed repeat buyers')
bars(axs[1],['F0 new fit','New G1','New G2'],new.hits.tolist(),[COL['weighted'],COL['new'],COL['new']]);axs[1].set_title('Three new fixed fits (26 Nov)');fig.suptitle('January, N=29,368; K=2,937 in every comparison');fig.text(.5,-.045,'Saved R3 and the three new fits are separate artifacts. New field definitions are not the earlier delivery/review groups.',ha='center',fontsize=10)
save(fig,'03-feature-comparisons',['r3-methods.csv','r3-group-methods.csv','feature-experiment-results.csv'],'New fixed run: F0=50,G1=49,G2=48. Only October/January used for fitting/evaluation; tests not used for reselection. G2 AUC improves while primary hits/AP do not.')
test=rd('frozen-test-metrics.csv');top=test.query('fraction == 0.1');methods=[('frozen_weighted_lr8','Weighted LR',COL['weighted']),('frozen_unweighted_lr8','Ordinary LR',COL['ordinary']),('recency_rule','Recency',COL['recency'])];dates=sorted(top.snapshot_date.unique());labels=['Apr','May','Jun'];fig,axs=plt.subplots(1,3,figsize=(14.4,4.8),layout='constrained')
for j,(method,label,color) in enumerate(methods):
 q=top[top.method.eq(method)].sort_values('snapshot_date');xx=np.arange(3)+(j-1)*.23;axs[0].bar(xx,q.hits,width=.22,label=label,color=color)
 for x,y in zip(xx,q.hits):axs[0].annotate(str(int(y)),(x,y),xytext=(0,4),textcoords='offset points',ha='center',fontsize=9)
 for ax,metric in zip(axs[1:],['precision','recall']):
  y=q[metric].to_numpy();lo=q[metric+'_wilson95_low'].to_numpy();hi=q[metric+'_wilson95_high'].to_numpy();ax.errorbar(xx,y,yerr=np.vstack([y-lo,hi-y]),fmt='o',color=color,capsize=3,label=label);ax.yaxis.set_major_formatter(PercentFormatter(1));ax.set_ylim(bottom=0)
for ax,title in zip(axs,['Top10% hits','Precision (Wilson 95%)','Recall (Wilson 95%)']):ax.set_xticks(range(3),labels);ax.set_title(title);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
for ax,metric in zip(axs[1:],['precision','recall']):ax.set_ylim(0,float(top[metric+'_wilson95_high'].max())*1.1)
axs[0].set_ylim(0,80);axs[0].legend(fontsize=9);fig.suptitle('Saved H04-spec pipelines, no refit; May favors ordinary LR');fig.text(.5,-.04,'Within-month capacities: Apr 3,782; May 4,003; Jun 3,981. Windows/customers overlap. Intervals exclude training/time drift.',ha='center',fontsize=10)
save(fig,'04-frozen-months',['frozen-test-metrics.csv','frozen-test-windows.csv'],'All methods and adverse month retained. Wilson intervals are conditional reference intervals, not evidence from three independent blind tests.')
fig,axs=plt.subplots(1,3,figsize=(12.8,4.5),layout='constrained')
for ax,date,title in zip(axs,dates,['April','May','June']):
 for method,label,color in methods:
  q=test[test.snapshot_date.eq(date)&test.method.eq(method)].sort_values('fraction');ax.plot(q.fraction*100,q.hits,'o-',label=label,color=color)
 ax.set_title(title);ax.set_xticks([5,10,20]);ax.set_xlabel('Customers selected (%)');ax.grid(alpha=.2);ax.yaxis.set_major_locator(MaxNLocator(integer=True));ax.set_ylim(bottom=0)
axs[0].set_ylabel('Observed repeat buyers');axs[0].legend(fontsize=9);fig.suptitle('Capacity sensitivity from the same fixed scores; no capacity-specific refit')
save(fig,'05-frozen-capacity',['frozen-test-metrics.csv'],'More contacts can increase counts while lowering list concentration;10% is a comparison capacity, not a proven operating optimum.')
names=['Global\nbase','Add group\nlabel','Separate\ngroups'];fx=rd('fixed-long79.csv');model_names=fx.Model.str.strip();equal79=[int(fx.loc[model_names.eq(key),'Hits'].iloc[0]) for key in ['F0 Weighted (Main)','B +Cluster_id','C Segmented Fallback']];fig,axs=plt.subplots(1,3,figsize=(12.5,4.8),layout='constrained');bars(axs[0],names,g.cluster_1_selected.tolist(),[COL['weighted'],COL['new'],COL['new']]);bars(axs[1],names,g.cluster_1_hits.tolist(),[COL['weighted'],COL['new'],COL['new']]);bars(axs[2],names,equal79,[COL['weighted'],COL['new'],COL['new']]);axs[0].set_title('Group places inside global K=2,937');axs[1].set_title('Group hits inside that global list');axs[2].set_title('Separate equal group capacity K=79');fig.suptitle('Long-inactive group: more places do not establish better within-group ranking');fig.text(.5,-.05,'R3 total hits: 50/50/49. Group pool: 12,330 with 90 observed buyers. The 79-place quota is diagnostic, not an optimum.',ha='center',fontsize=10)
save(fig,'06-group-coverage',['r3-group-methods.csv','fixed-long79.csv','current-profiles.csv'],'73/181/518 are group places inside a global list;79 is a separate same-size within-group comparison.')
paired=rd('frozen-test-paired.csv');p=paired[paired.comparator.eq('frozen_unweighted_lr8')].sort_values('snapshot_date');fig,ax=plt.subplots(figsize=(11.5,5.4),layout='constrained');xx=np.arange(3);ax.bar(xx-.18,p.gained_positive_customers,width=.35,color=COL['weighted'],label='Weighted-only buyers');ax.bar(xx+.18,p.lost_positive_customers,width=.35,color=COL['ordinary'],label='Ordinary-only buyers');pairlabels=[]
for i,x in enumerate(p.itertuples()):
 w=int(top.loc[top.snapshot_date.eq(x.snapshot_date)&top.method.eq('frozen_weighted_lr8'),'hits'].iloc[0]);u=int(top.loc[top.snapshot_date.eq(x.snapshot_date)&top.method.eq('frozen_unweighted_lr8'),'hits'].iloc[0]);shared=w-int(x.gained_positive_customers);assert shared==u-int(x.lost_positive_customers)
 pairlabels.append(f'{labels[i]}: {shared} found by both\nTotal weighted/ordinary: {w}/{u}')
 ax.text(i,max(x.gained_positive_customers,x.lost_positive_customers)+.7,f'Net {x.net_hits:+d}; p={x.exact_paired_positive_discordance_p:.3f}',ha='center',fontsize=11)
 for offset,y in [(-.18,x.gained_positive_customers),(.18,x.lost_positive_customers)]:ax.annotate(str(int(y)),(i+offset,y),xytext=(0,4),textcoords='offset points',ha='center',fontsize=10)
ax.set_xticks(xx,pairlabels);ax.set_ylim(0,15);ax.set_ylabel('Repeat buyers found by only one list');ax.legend();ax.set_title('Paired fixed-capacity comparison: unique and shared buyers');fig.text(.5,-.055,'Large p-values here do not support a directional advantage; they are not the probability that models are equal.\nExact secondary comparisons, no multiplicity adjustment; overlapping months; no causal marketing claim.',ha='center',fontsize=10)
save(fig,'07-paired-evidence',['frozen-test-paired.csv','frozen-test-metrics.csv'],'April shared56 plus9/8 unique gives totals65/64,net+1,p1.0. A large p-value does not prove equivalence;months are not independent replications.')
trial=rd('trial-plan.csv');fig,ax=plt.subplots(figsize=(9.5,4.8),layout='constrained');bars(ax,['Relative +25%','Relative +50%','Relative +100%'],trial.total_required.tolist(),[COL['ordinary']]*3);ax.axhline(12330,color=COL['new'],linestyle='--',label='Historical group pool12,330');ax.set_ylabel('Total customers across both arms');ax.set_title('Proposed content test: required sample versus historical pool');ax.legend();fig.text(.5,-.045,'Baseline0.730%;two-sided alpha5%;power80%;1:1 allocation;90-day repurchase. Reachability/consent unknown;not run.',ha='center',fontsize=10)
save(fig,'08-trial-feasibility',['trial-plan.csv'],'Both groups contacted:home-goods versus generic guide. Sample plan is not evidence of treatment effectiveness.')
prob=rd('extension-calibrated-probabilities.csv');prob[['date','strategy']]=prob.cell.str.split('__',expand=True);families=['weightedLR','unweightedLR',next(x for x in prob.family.unique() if 'cat' in x.lower())];fig,axs=plt.subplots(1,3,figsize=(12.8,4.5),layout='constrained')
for ax,fam,display in zip(axs,families,['Weighted LR','Ordinary LR','Native CatBoost (3 seeds)']):
 for strategy,color in [('single',COL['weighted']),('pooled','#d78c31')]:
  q=prob[prob.family.eq(fam)&prob.strategy.eq(strategy)].sort_values('date');ax.plot(range(3),q.logloss,'o-',label=strategy,color=color)
 ax.set_title(display);ax.set_xticks(range(3),['Nov17','Dec17','Jan18']);ax.grid(alpha=.2)
axs[0].set_ylabel('All-customer log loss (lower is better)');axs[0].legend();fig.suptitle('Separate calibrated extension: pooled history did not consistently improve quality');fig.text(.5,-.04,'80% fit/20% calibration protocol;overlapping historical evaluations. This is not the full-October R3 ranking artifact.',ha='center',fontsize=10)
save(fig,'09-probability-extension',['extension-calibrated-probabilities.csv'],'Compare single/pooled within a family/date;do not read falling loss across dates as isolated model improvement because prevalence changes.')
v=rd('extension-value-capacity.csv');q=v[v.evaluation_date.eq('2018-01-01')&v.strategy.eq('single')&v.family.eq('p_wlr')&v.scope.eq('global')&v.capacity.eq(.1)&v.rule.isin(['p','purchase_F_M','expected_G'])];fig,ax=plt.subplots(figsize=(9.2,5),layout='constrained')
for row,label,color in [('p','Probability ranking',COL['weighted']),('purchase_F_M','p × historical F × M','#d78c31'),('expected_G','Expected goods amount',COL['new'])]:
 x=q[q.rule.eq(row)].iloc[0];ax.scatter(x.hits,x.captured_G,s=110,label=label,color=color);ax.annotate(f'{int(x.hits)} buyers; {x.captured_G:,.2f}',(x.hits,x.captured_G),xytext=(7,7),textcoords='offset points',fontsize=10)
ax.set_xlim(26,47);ax.set_ylim(4000,7100);ax.grid(alpha=.2);ax.set_xlabel('Observed repeat buyers captured');ax.set_ylabel('Future goods amount captured (BRL)');ax.legend(loc='lower left');ax.set_title('Separate value extension: amount and buyer counts can trade off');fig.text(.5,-.04,'January single weighted LR,80/20 calibrated protocol,K=2,937.43 buyers is not the R3 full-October50. Goods amount is not profit or uplift.',ha='center',fontsize=10)
save(fig,'10-value-extension',['extension-value-capacity.csv'],'Same calibrated p,only ranking formula changes;43/4598.15 vs37/6557.40 vs30/5857.29. Never attach these amounts to the R3 50-buyer list.')
(P/'figure-manifest.json').write_text(json.dumps(saved,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'figures':len(saved),'vector_files':len(saved)*2,'fits':0},ensure_ascii=False))
