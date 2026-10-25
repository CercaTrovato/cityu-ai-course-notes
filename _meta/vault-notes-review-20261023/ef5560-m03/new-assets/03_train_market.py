"""L03_03 · 美国市场 Ridge/LASSO 冻结训练入口。
目的      从指定保存面板验证选参，再重估并输出测试评价。
讲义      旧56页版 Lec03 p.25（新版同p.25）。
笔记      M03 §2.5.3。
输入      旧解压 market_excess_return_panel.csv；月度log总收益减旧simple月rf的保存超额列。
输出      stdout参数/测试OOS R²；不生成PNG/CSV，不改原数据或output/。
关键决定  验证选参，178月pre-test重估整链；不切换新版ZIP或重建行情/vintage。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import load
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

df = load.c03_market_panel()
df = df.loc[df["market"] == "US_SPY"].copy()
x_names = ["term_spread_lag1", "fed_funds_lag1",
           "unemployment_lag2", "inflation_lag2"]
target = "market_excess_return"

development = df.loc[df["split"] == "development"].copy()
validation = df.loc[df["split"] == "validation"].copy()
pretest = df.loc[df["split"].isin(["development", "validation"])].copy()
test = df.loc[df["split"] == "test"].copy()
assert (len(development), len(validation), len(pretest), len(test)) == (142, 36, 178, 60)

grids = {
    "ridge": [0.01, 0.1, 1, 10, 100, 1000],
    "lasso": [0.00001, 0.0001, 0.001, 0.01, 0.1],
}

def estimator(name, alpha):
    if name == "ridge":
        return Ridge(alpha=alpha)
    return Lasso(alpha=alpha, max_iter=100000)

chosen = {}
for name, alphas in grids.items():
    scored = []
    for alpha in alphas:
        pipe = make_pipeline(StandardScaler(), estimator(name, alpha))
        pipe.fit(development[x_names], development[target])
        pred = pipe.predict(validation[x_names])
        scored.append((mean_squared_error(validation[target], pred), alpha))
    chosen[name] = min(scored)[1]

forecast = {}
for name, alpha in chosen.items():
    frozen = make_pipeline(StandardScaler(), estimator(name, alpha))
    frozen.fit(pretest[x_names], pretest[target])
    forecast[name] = frozen.predict(test[x_names])

sse_benchmark = ((test[target] - test["benchmark_ma12_excess_return"]) ** 2).sum()
for name, pred in forecast.items():
    oos_r2 = 1 - ((test[target] - pred) ** 2).sum() / sse_benchmark
    print(name, "alpha=", chosen[name], "test OOS R2=", oos_r2)
