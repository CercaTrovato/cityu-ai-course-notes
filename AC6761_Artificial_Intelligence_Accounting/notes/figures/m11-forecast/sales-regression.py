"""Week 11 pp.19-20 teaching correction; original 10 rows, no real sales claim."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['svg.fonttype'] = 'none'

out = Path(__file__).resolve().parent
data = {
    'advertising_expenditure': [1000,1500,2000,2500,3000,3500,4000,4500,5000,5500],
    'sales': [2000,2500,3000,4000,4500,5000,6000,6500,7000,8000],
}
df = pd.DataFrame(data)
X, y = df[['advertising_expenditure']], df['sales']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
model = LinearRegression().fit(X_train,y_train)
pred = model.predict(X_test)
baseline = np.repeat(y_train.mean(), len(y_test))
x = X_train.iloc[:,0].to_numpy(dtype=float)
yt = y_train.to_numpy(dtype=float)
b = np.sum((x-x.mean())*(yt-yt.mean())) / np.sum((x-x.mean())**2)
a = yt.mean() - b*x.mean()
assert np.allclose([a,b],[model.intercept_,model.coef_[0]])
results = {
 'training_rows': X_train.index.tolist(), 'test_rows':X_test.index.tolist(),
 'x_mean':x.mean(), 'y_mean':yt.mean(), 'Sxx':float(np.sum((x-x.mean())**2)),
 'Sxy':float(np.sum((x-x.mean())*(yt-yt.mean()))),
 'coefficient':b, 'intercept':a,
 'test':[{'advertising_expenditure':float(xx),'actual':float(yy),'predicted':float(pp),'residual':float(yy-pp)} for xx,yy,pp in zip(X_test.iloc[:,0],y_test,pred)],
 'MAE':float(mean_absolute_error(y_test,pred)),
 'MSE':float(mean_squared_error(y_test,pred)),
 'baseline_MAE':float(mean_absolute_error(y_test,baseline)),
 'p17_price_check':150*(1+0.082),
 'scope':'classroom toy data; random split reproduces slide design, not a time-series forecast',
}
(out/'sales-regression-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
fig,ax=plt.subplots(figsize=(8,4.8))
ax.scatter(X_train.iloc[:,0],y_train,label='Training observations',marker='o')
ax.scatter(X_test.iloc[:,0],y_test,label='Held-out actual',marker='s',s=70)
grid=np.linspace(1000,5500,100).reshape(-1,1)
ax.plot(grid[:,0],a+b*grid[:,0],label='Fitted line (training only)',color='#cf6b35')
ax.scatter(X_test.iloc[:,0],pred,label='Held-out prediction',marker='x',s=80,color='#9e2525')
ax.set(xlabel='Advertising expenditure (source units)',ylabel='Sales (source units)',title='Week 11: corrected toy-data regression')
ax.legend(fontsize=9); ax.grid(alpha=0.2); fig.tight_layout()
fig.savefig(out/'sales-regression.svg'); fig.savefig(out/'sales-regression.png',dpi=150)
svg = out/'sales-regression.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
print(json.dumps(results,indent=2))
