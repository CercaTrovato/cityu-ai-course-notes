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