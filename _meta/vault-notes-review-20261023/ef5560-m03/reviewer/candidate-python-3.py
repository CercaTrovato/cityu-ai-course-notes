from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn.decomposition import PCA
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DATA = Path("EF5560_Fintech_and_AI_in_Finance/course_files_export/class03/class03/hsi_stock_excess_return_panel.csv")
df = pd.read_csv(DATA)
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