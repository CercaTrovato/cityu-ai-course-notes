import json,math
from pathlib import Path
def entropy(pos,neg):
    n=pos+neg
    return -sum(p*math.log2(p) for p in [pos/n,neg/n] if p)
def gini(pos,neg):
    n=pos+neg
    return 1-(pos/n)**2-(neg/n)**2
root=gini(3,7)
result={'home_gain':root-7/10*gini(3,4),'married_gain':root-6/10*gini(3,3),'home_entropy_gain':entropy(3,7)-7/10*entropy(3,4),'married_entropy_gain':entropy(3,7)-6/10*entropy(3,3)}
# Independent four-record CART and regression-tree miniature.
x=[1,2,3,4];yc=[0,0,1,1];yr=[2,4,8,10]
reg=[]
for k in [1.5,2.5,3.5]:
    groups=[[yi for xi,yi in zip(x,yr) if (xi<=k)==side] for side in [True,False]]
    means=[sum(g)/len(g) for g in groups]
    sse=sum(sum((yi-m)**2 for yi in g) for g,m in zip(groups,means))
    reg.append({'threshold':k,'means':means,'SSE':sse})
result['regression_splits']=reg
result['regression_root_SSE']=sum((v-6)**2 for v in yr)
grow=[('s1',1,0,0,1),('s2',1,1,0,1),('s3',0,1,0,1),('n1',1,0,1,0),('n2',1,1,1,0),('n3',0,1,1,0),('n4',0,0,1,0),('n5',0,0,0,0)]
prior=3/8
gains={}
for name,ix,val in [('free',1,1),('win',2,1),('known',3,0)]:
    subset=[r for r in grow if r[ix]==val];p=sum(r[-1] for r in subset);n=len(subset)-p
    gains[name]={'p':p,'n':n,'foil_gain':p*(math.log2(p/(p+n))-math.log2(prior))}
result['rule_first_candidates']=gains
result['rule_predictions']={r[0]:int((r[3]==0 and r[1]==1) or (r[3]==0 and r[2]==1)) for r in grow}
result['toy_rule_accuracy']=sum(result['rule_predictions'][r[0]]==r[-1] for r in grow)/8
result['ADASYN']={'r':[0,0.5,1],'normalized':[0,1/3,2/3],'budget':6,'allocated':[0,2,4],'SMOTE_point':[2+0.25*2,2+0.25*1]}
result['kernel_example']={'w':-2/3,'b':5/3,'scores':{str(x):5/3-2*x*x/3 for x in [0,1.5,3]}}
result['knn_example']={'mean':3,'std':math.sqrt(5),'query':(3.8-3)/math.sqrt(5),'distances':[abs(3.8-x)/math.sqrt(5) for x in [0,2,4,6]]}
sigmoid=lambda z:1/(1+math.exp(-z))
result['logistic_one_step']={'prob1':sigmoid(0.25),'newloss':(-math.log(0.5)-math.log(sigmoid(0.25)))/2,'queryprob':sigmoid(0.2)}
(Path(__file__).parent/'extra-results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
