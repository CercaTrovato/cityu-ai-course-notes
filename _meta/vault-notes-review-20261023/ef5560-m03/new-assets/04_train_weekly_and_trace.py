"""L03_04 · 六模型周度训练及具名股票PCR追踪。
目的      同一周度切分比较六模型，再追踪一只具名股票的冻结PCR预测。
讲义      旧56页版 Lec03 p.50（新版p.48）。
笔记      M03 §2.8.3。
输入      旧解压 hsi_stock_excess_return_panel.csv；个股周simple总收益减7/365有效simple rf。
输出      stdout验证设置/测试OOS R²和CCB追踪；不生成PNG/CSV或改原数据/output/。
关键决定  dev拟合候选、validation选设置、pre-test重估、test只评一次；CCB不参与选择/拟合。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import load
import numpy as np
from sklearn.cross_decomposition import PLSRegression
from sklearn.decomposition import PCA
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

df = load.c03_stock_panel()
df = df.loc[df["usable_for_ml"].astype(str).str.lower().eq("true")].copy()
features = [c for c in df.columns if c.endswith("_rank")]
assert len(features) == 30
dev = df.loc[df.split == "development"]
val = df.loc[df.split == "validation"]
pretest = df.loc[df.split.isin(["development", "validation"])]
test = df.loc[df.split == "test"]
assert (len(dev), len(val), len(pretest), len(test)) == (6123, 2050, 8173, 4108)

def candidates():
    yield "OLS", {}, make_pipeline(StandardScaler(), LinearRegression())
    for a in [0.1, 1, 10, 100, 1000]:
        yield "Ridge", {"alpha": a}, make_pipeline(StandardScaler(), Ridge(alpha=a))
    for a in [0.0001, 0.001, 0.003, 0.01]:
        yield "LASSO", {"alpha": a}, make_pipeline(StandardScaler(), Lasso(alpha=a, max_iter=100000))
    for a in [0.001, 0.003, 0.01]:
        for rho in [0.25, 0.5, 0.75]:
            yield "Elastic Net", {"alpha": a, "rho": rho}, make_pipeline(
                StandardScaler(), ElasticNet(alpha=a, l1_ratio=rho, max_iter=100000))
    for k in [1, 3, 5, 10, 15, 20]:
        yield "PCR", {"K": k}, make_pipeline(StandardScaler(), PCA(k), LinearRegression())
    for k in [1, 3, 5, 10]:
        yield "PLS", {"K": k}, make_pipeline(StandardScaler(), PLSRegression(n_components=k, scale=False))

best = {}
for name, setting, model in candidates():
    model.fit(dev[features], dev["excess_return"])
    mse = mean_squared_error(val["excess_return"], np.ravel(model.predict(val[features])))
    if name not in best or mse < best[name][0]:
        best[name] = (mse, setting)

def frozen_model(name, setting):
    if name == "OLS": return make_pipeline(StandardScaler(), LinearRegression())
    if name == "Ridge": return make_pipeline(StandardScaler(), Ridge(alpha=setting["alpha"]))
    if name == "LASSO": return make_pipeline(StandardScaler(), Lasso(alpha=setting["alpha"], max_iter=100000))
    if name == "Elastic Net": return make_pipeline(StandardScaler(), ElasticNet(
        alpha=setting["alpha"], l1_ratio=setting["rho"], max_iter=100000))
    if name == "PCR": return make_pipeline(StandardScaler(), PCA(setting["K"]), LinearRegression())
    return make_pipeline(StandardScaler(), PLSRegression(n_components=setting["K"], scale=False))

sse0 = np.square(test["excess_return"]).sum()
for name, (val_mse, setting) in best.items():
    model = frozen_model(name, setting)
    model.fit(pretest[features], pretest["excess_return"])
    pred = np.ravel(model.predict(test[features]))
    oos_r2 = 1 - np.square(test["excess_return"].to_numpy() - pred).sum() / sse0
    print(name, setting, "validation MSE=", val_mse, "test OOS R2=", oos_r2)

pcr_setting = best["PCR"][1]
assert pcr_setting == {"K": 5}
pcr_frozen = frozen_model("PCR", pcr_setting)
pcr_frozen.fit(pretest[features], pretest["excess_return"])

ccb = test.loc[(test["ticker"] == "0939.HK") &
               (test["forecast_week"] == "2025-07-04")].copy()
assert len(ccb) == 1

scaler = pcr_frozen.named_steps["standardscaler"]
pca = pcr_frozen.named_steps["pca"]
return_ols = pcr_frozen.named_steps["linearregression"]

raw_rank = ccb[features].iloc[0].to_numpy(float)
z = (raw_rank - scaler.mean_) / scaler.scale_
scores = (z - pca.mean_) @ pca.components_.T
terms = scores * return_ols.coef_
manual = float(return_ols.intercept_ + terms.sum())
pipeline = float(pcr_frozen.predict(ccb[features])[0])

print("raw rank input =", raw_rank)
print("pre-test scaler mean =", scaler.mean_)
print("pre-test scaler scale =", scaler.scale_)
print("standardized input =", z)
print("PCR K=5 scores =", scores)
print("return intercept =", return_ols.intercept_)
print("return coefficients =", return_ols.coef_)
print("score × coefficient terms =", terms)
print("manual / pipeline / actual =",
      manual, pipeline, float(ccb["excess_return"].iloc[0]))
assert abs(manual - pipeline) < 1e-14
