from pathlib import Path
import json
import numpy as np,pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import StackingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
sp=Path(__file__).parent
df=pd.read_csv('D:/上课资料/CityU/IS6400_Business_Data_Analytics/course_files_export/Credit_approval.csv')
Xtr,Xte,ytr,yte=train_test_split(df.drop(columns='Approved'),df.Approved,test_size=0.4,random_state=1)
clf=StackingClassifier(estimators=[('dt',DecisionTreeClassifier(max_depth=3,random_state=1)),('knn',make_pipeline(StandardScaler(),KNeighborsClassifier(n_neighbors=7))),('svm',make_pipeline(StandardScaler(),SVC(probability=True,C=1,kernel='rbf',random_state=1)))],final_estimator=LogisticRegression(max_iter=2000,random_state=1),cv=5,stack_method='auto',passthrough=False).fit(Xtr,ytr)
Z=clf.transform(Xte)
result={'classes':clf.classes_.tolist(),'stack_method':clf.stack_method_,'shape':list(Z.shape),'first_row_meta_features':Z[0].tolist(),'first_row_base_second_probabilities':[float(e.predict_proba(Xte.iloc[:1])[0,1]) for e in clf.estimators_],'retained_class':str(clf.classes_[1]),'warning':'transform is fitted full-training base model output for inference, not stored OOF training features'}
assert np.allclose(result['first_row_meta_features'],result['first_row_base_second_probabilities'])
(sp/'stacking-shape.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
