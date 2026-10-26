import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.DataFrame({
    'advertising_expenditure': [1000,1500,2000,2500,3000,3500,4000,4500,5000,5500],
    'sales': [2000,2500,3000,4000,4500,5000,6000,6500,7000,8000]
})
X = df[['advertising_expenditure']]
y = df['sales']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
result = X_test.copy()
result['actual_sales'] = y_test
result['predicted_sales'] = y_pred
result['residual'] = result['actual_sales'] - result['predicted_sales']
mae = result['residual'].abs().mean()
baseline = y_train.mean()
baseline_mae = (y_test - baseline).abs().mean()

print(result.round(6).to_string())
print('slope:', model.coef_[0], 'intercept:', model.intercept_)
print('MAE:', mae)
print('baseline prediction:', baseline, 'baseline MAE:', baseline_mae)
