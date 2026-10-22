import json
from pathlib import Path
# Given illustrative labels/predictions from the note, not a trained deployed model.
truth=['finance','emergency','course','finance'];pred=['finance','emergency','finance','finance']
accuracy=sum(a==b for a,b in zip(truth,pred))/len(truth)
def confusion(y,p):
 return {'TP':sum(a and b for a,b in zip(y,p)),'FP':sum(not a and b for a,b in zip(y,p)),'FN':sum(a and not b for a,b in zip(y,p)),'TN':sum(not a and not b for a,b in zip(y,p))}
final=confusion([x=='emergency' for x in truth],[x=='emergency' for x in pred])
validation_truth=[True,False,True,False];scores=[.85,.65,.55,.35]
thresholds={str(t):confusion(validation_truth,[v>=t for v in scores]) for t in [.70,.50]}
result={'scope':'synthetic instructional given-output arithmetic; no real system training or deployment evidence','test_accuracy':accuracy,'test_emergency':final,'validation_thresholds':thresholds,'validation_ids':{'0.70':[13],'0.50':[13,14,15]},'checks':{'accuracy_75pct':accuracy==.75,'test_confusion':final=={'TP':1,'FP':0,'FN':0,'TN':3},'threshold_070':thresholds['0.7']=={'TP':1,'FP':0,'FN':1,'TN':2},'threshold_050':thresholds['0.5']=={'TP':2,'FP':1,'FN':0,'TN':1}}}
assert all(result['checks'].values())
(Path(__file__).parent/'main-calculation-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
