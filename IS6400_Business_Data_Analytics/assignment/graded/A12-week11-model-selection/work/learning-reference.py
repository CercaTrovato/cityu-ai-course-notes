"""Local learning-reference experiment for source cell 63; not a submission notebook."""
from pathlib import Path
import json,sys,hashlib,time,warnings
import numpy as np,sklearn
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split,StratifiedKFold,GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest,f_classif
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score,recall_score
R=Path(__file__).resolve().parents[5];S=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'_meta/tools'));from safe_write import atomic_write
start=time.time();data=load_breast_cancer();X,y=data.data,data.target
Xd,Xh,yd,yh=train_test_split(X,y,random_state=0)
baseline=[]
for name,model in [('DT',DecisionTreeClassifier()),('RF',RandomForestClassifier()),('SVC',SVC())]:
 np.random.seed(20261118);model.fit(Xd,yd);pred=model.predict(Xh);baseline.append(dict(model=name,accuracy=float(accuracy_score(yh,pred)),error=float(1-accuracy_score(yh,pred)),malignant_recall=float(recall_score(yh,pred,pos_label=0)),params=model.get_params()))
outer=list(StratifiedKFold(3,shuffle=True,random_state=11).split(X,y));inner=StratifiedKFold(3,shuffle=True,random_state=22)
configs=[('DT',DecisionTreeClassifier(random_state=0),{'model__max_depth':[3,None],'model__min_samples_leaf':[1,3]}),('RF',RandomForestClassifier(random_state=0),{'model__max_depth':[5,None],'model__min_samples_leaf':[1,3]}),('SVC',SVC(),{'model__C':[1,10],'model__gamma':['scale',.0001]})]
results=[]
for feature_select in [False,True]:
 for name,model,grid in configs:
  steps=([('select',SelectKBest(f_classif)),('scale',StandardScaler())] if feature_select else [])+[('model',model)]
  candidates=dict(grid)
  if feature_select:candidates['select__k']=[10,20,'all']
  folds=[]
  for k,(tr,te) in enumerate(outer,1):
   pipe=Pipeline(steps);search=GridSearchCV(pipe,candidates,cv=inner,scoring='accuracy',refit=True,n_jobs=1,error_score='raise')
   with warnings.catch_warnings(record=True) as ws:
    warnings.simplefilter('always');search.fit(X[tr],y[tr]);pred=search.predict(X[te])
   folds.append(dict(fold=k,n_train=len(tr),n_test=len(te),correct=int((pred==y[te]).sum()),accuracy=float(accuracy_score(y[te],pred)),error=float(1-accuracy_score(y[te],pred)),malignant_recall=float(recall_score(y[te],pred,pos_label=0)),inner_best_score=float(search.best_score_),best_params=search.best_params_,warnings=list({str(w.message) for w in ws})))
  scores=[f['accuracy'] for f in folds];results.append(dict(model=name,preprocessing='SelectKBest then StandardScaler, each fitted inside every training fold' if feature_select else 'raw input; no learned preprocessing',folds=folds,mean_accuracy=float(np.mean(scores)),sample_std_accuracy=float(np.std(scores,ddof=1)),mean_error=float(1-np.mean(scores))))
  # Intermediate progress omitted in the persistent replay copy.
out=dict(scope='source cell63 Q1-Q3 local learning reference; no official answer or personal submission claim',dataset=dict(name='Breast Cancer Wisconsin Diagnostic',shape=list(X.shape),target_names=data.target_names.tolist(),class_counts=np.bincount(y).tolist()),environment=dict(python=sys.version,sklearn=sklearn.__version__,numpy=np.__version__),q1=dict(split='same random_state0 holdout as source cell27, 426 train /143 test; no stratify',default_estimators=True,global_rng_seed=20261118,models=baseline,interpretation='heldout scores used to choose among models; selected score is not an untouched final estimate'),q2_q3=dict(outer='StratifiedKFold3 shuffle seed11 on all569; inner StratifiedKFold3 shuffle seed22',metric='accuracy; error=1-accuracy; malignant recall pos_label0 also reported',grids='small fixed educational grids, no claim of global hyperparameter optimum',results=results,interpretation='same outer partitions reused for exploratory comparison of families and preprocessing; within each fit test fold excluded; choosing a final winning family/preprocessing after outer scores makes it another selection step, so do not call its outer mean an untouched final performance guarantee'),elapsed_seconds=time.time()-start)
atomic_write(str(S/'learning-reference-results.json'),json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(dict(q1=[dict(model=b['model'],error=b['error']) for b in baseline],nested=[dict(model=x['model'],preprocessing=x['preprocessing'],mean_accuracy=x['mean_accuracy'],sample_std=x['sample_std_accuracy']) for x in results],elapsed=out['elapsed_seconds']),ensure_ascii=False,indent=2))
