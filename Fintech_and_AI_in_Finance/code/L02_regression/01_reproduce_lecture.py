"""
L02_01 · 复现 Lec02 讲义上每一个已发布的数字
=============================================
目的      讲义 p.9–51 报了 40 多个数字（相关系数、斜率、标准误、p 值、R²、样本外 R²、命中率……）。本脚本用课程给的
          两个 CSV 与 statsmodels.OLS 逐个复现，每个数字都 assert 到讲义的小数位，并输出"讲义值 / 复现值 / 差"对照表。
          结论：全部对上——这份讲义是完全可复现的。
讲义      Lec02 p.15（相关）、p.21–24（简单回归）、p.29（相关矩阵）、p.32–33（标准化多元回归）、p.35（CSI 宏观训练样本）、
          p.47/49（SPY 样本外）、p.51（CSI 宏观样本外）
笔记      [[M02-回归与样本外设计]] §2.3.4、§2.4.2–2.4.5、§2.5.2–2.5.4、§2.7.4、§2.8、§2.9
输入      spy_monthly_features_240m.csv、csi300_macro_panel.csv（目标都是**对数收益**）
输出      output/L02_01_reproduce_lecture.png · output/L02_01_reproduce_lecture.csv
关键决定  · 切分按讲义 p.41：train = forecast_month < 2021-07-01（180 个月），test = 其余 60 个月；行序按日期，绝不打乱
          · 三变量模型 = momentum_12 / volatility_12 / ma_gap_10（讲义 p.10 点名的三个）；用 statsmodels.OLS（助教明说项目要用它）
          · 标准化只用 train 的均值与标准差（ddof=1），test 用同一组 mu/sd 变换（讲义 p.31/45）
          · 基准 = 滞后 MA(12) = r[t−12..t−1] 的均值（SPY 自己算；CSI 用文件的 benchmark_ma12，两者定义相同）
          · OOS R² = 1 − Σ(r−r̂)² / Σ(r−r̂ᵇ)²（讲义 p.43 的定义，分母是基准误差，不是 sklearn 的 r2_score）
          · 命中率 = sign(r̂) == sign(r) 的比例；基准命中率 = 正收益月占比
          · 容差 = 讲义显示位数的半个单位（例如讲义写 0.74 → |差| ≤ 0.005）；讲义写 "≈" 的 R²=0.1% 按一位小数判
          · 目标是对数收益，讲义 p.10/16 文字写的是简单收益——用对数收益能精确复现每一个数，说明讲义实际用的就是对数收益
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))   # 让 common 可导入，脚本从哪启动都能跑

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.dates as mdates

from common import load, plot

SPLIT = "2021-07-01"
X3 = ["momentum_12", "volatility_12", "ma_gap_10"]
SHORT = {"momentum_12": "动量", "volatility_12": "波动率", "ma_gap_10": "均线偏离"}

# ---------- 1. 读数据、切分 ----------
d = load.spy_features()
train, test = d[d.index < SPLIT], d[d.index >= SPLIT]
assert len(d) == 240 and len(train) == 180 and len(test) == 60, "切分应为 180 / 60（讲义 p.39）"
assert d.index.is_monotonic_increasing, "行序必须按日期"
y_tr, y_te = train["market_return"], test["market_return"]

checks = []   # (讲义页, 项目, 讲义值, 复现值, 小数位)


def check(page, item, lecture, repro, decimals):
    checks.append({"讲义页": page, "项目": item, "讲义值": lecture, "复现值": repro, "小数位": decimals})


# ---------- 2. p.15 相关系数；p.29 相关矩阵（训练 180 月） ----------
corr3 = {c: train[c].corr(y_tr) for c in X3}
for c, lec in zip(X3, (0.02, 0.12, 0.05)):
    check("p.15", f"corr({SHORT[c]}, 下月收益)", lec, corr3[c], 2)
cm_cols = ["return_lag1", "momentum_12", "volatility_12", "ma_gap_10", "term_spread_lag1"]
cm = train[cm_cols].corr()
lecture_cm = {("return_lag1", "momentum_12"): 0.29, ("return_lag1", "volatility_12"): 0.06, ("return_lag1", "ma_gap_10"): 0.54,
              ("return_lag1", "term_spread_lag1"): -0.00, ("momentum_12", "volatility_12"): -0.44, ("momentum_12", "ma_gap_10"): 0.74,
              ("momentum_12", "term_spread_lag1"): -0.03, ("volatility_12", "ma_gap_10"): -0.13, ("volatility_12", "term_spread_lag1"): 0.30,
              ("ma_gap_10", "term_spread_lag1"): 0.00}
for (a, b), lec in lecture_cm.items():
    check("p.29", f"corr({a}, {b})", lec, cm.loc[a, b], 2)

# ---------- 3. p.21–24 三个简单回归 ----------
simple = {}
for c in X3:
    m = sm.OLS(y_tr, sm.add_constant(train[[c]])).fit()
    simple[c] = m
lec_simple = {"momentum_12": (0.6, 2.1, 0.76, 0.1), "volatility_12": (8.5, 5.2, 0.11, 1.5), "ma_gap_10": (3.0, 4.2, 0.48, 0.3)}
for c, (b, se, p, r2) in lec_simple.items():
    m = simple[c]
    check("p.24", f"{SHORT[c]} 斜率 (pp)", b, m.params[c] * 100, 1)
    check("p.24", f"{SHORT[c]} 标准误 (pp)", se, m.bse[c] * 100, 1)
    check("p.24", f"{SHORT[c]} p 值", p, m.pvalues[c], 2)
    check("p.24", f"{SHORT[c]} R² (%)", r2, m.rsquared * 100, 1)
mom = simple["momentum_12"]
check("p.21", "r̂(%) 截距 0.8", 0.8, mom.params["const"] * 100, 1)
check("p.21", "r̂(%) 斜率 0.6", 0.6, mom.params["momentum_12"] * 100, 1)
check("p.21", "动量 +0.10 → 拟合收益变化 (bp)", 6.3, mom.params["momentum_12"] * 0.10 * 1e4, 1)
check("p.22", "动量 t 统计量", 0.31, mom.tvalues["momentum_12"], 2)

# ---------- 4. p.32–33 标准化多元回归（只用 train 的 mu/sd） ----------
mu, sd = train[X3].mean(), train[X3].std(ddof=1)
Z_tr = (train[X3] - mu) / sd
Z_te = (test[X3] - mu) / sd                       # test 用 train 的 mu/sd，不重算
fit3 = sm.OLS(y_tr, sm.add_constant(Z_tr)).fit()
lec_multi = {"momentum_12": (0.4, 0.6, 0.50), "volatility_12": (0.7, 0.4, 0.07), "ma_gap_10": (0.0, 0.5, 0.95)}
for c, (b, se, p) in lec_multi.items():
    check("p.33", f"标准化 {SHORT[c]} 斜率 (%)", b, fit3.params[c] * 100, 1)
    check("p.33", f"标准化 {SHORT[c]} 标准误 (%)", se, fit3.bse[c] * 100, 1)
    check("p.33", f"标准化 {SHORT[c]} p 值", p, fit3.pvalues[c], 2)
check("p.33", "R²_train (%)", 2.2, fit3.rsquared * 100, 1)
# 自检：标准化不改变预测（只改变斜率的单位）
fit3_raw = sm.OLS(y_tr, sm.add_constant(train[X3])).fit()
assert np.allclose(fit3.predict(sm.add_constant(Z_te)), fit3_raw.predict(sm.add_constant(test[X3])), atol=1e-12)

# ---------- 5. p.47/49 SPY 样本外：冻结的规格 vs 滞后 MA(12) ----------
r_all = d["market_return"]
ma12 = r_all.shift(1).rolling(12).mean()          # 只用 t−12..t−1，本身无泄漏
bench = ma12.loc[test.index]
pred = fit3.predict(sm.add_constant(Z_te))
oos_r2 = 1 - ((y_te - pred) ** 2).sum() / ((y_te - bench) ** 2).sum()
hit_model = (np.sign(pred) == np.sign(y_te)).mean()
hit_ma12 = (np.sign(bench) == np.sign(y_te)).mean()
pos_months = int((y_te > 0).sum())
check("p.46/49", "SPY OOS R² vs MA(12) (%)", 6.6, oos_r2 * 100, 1)
check("p.47", "SPY 三变量回归 命中率 (%)", 63.3, hit_model * 100, 1)
check("p.47", "SPY MA(12) 命中率 (%)", 61.7, hit_ma12 * 100, 1)
check("p.47", "SPY 测试期正收益月数 (/60)", 38, pos_months, 0)
check("p.47", "SPY 永远猜涨命中率 (%)", 63.3, pos_months / 60 * 100, 1)

# ---------- 6. p.35 / p.51 CSI 300 宏观模型 ----------
c = load.csi300_panel()
ctr, cte = c[c.index < SPLIT], c[c.index >= SPLIT]
XC = ["exports_yoy_lag2", "imports_yoy_lag2", "cli_gap_lag2", "reer_12m_lag2"]
assert (c["benchmark_ma12"] - c["market_return"].shift(1).rolling(12).mean()).abs().max() < 1e-12, "benchmark_ma12 应 = 滞后 MA(12)"
fitc = sm.OLS(ctr["market_return"], sm.add_constant(ctr[XC])).fit()
check("p.35", "CSI 进口增长 β (pp / 1pp)", -0.15, fitc.params["imports_yoy_lag2"] * 100, 2)
check("p.35", "CSI 进口增长 p 值", 0.001, fitc.pvalues["imports_yoy_lag2"], 3)
check("p.35", "CSI 联合 F 检验 p 值", 0.026, fitc.f_pvalue, 3)
check("p.35", "CSI R²_train (%)", 6.1, fitc.rsquared * 100, 1)
predc = fitc.predict(sm.add_constant(cte[XC]))
yc, bc = cte["market_return"], cte["benchmark_ma12"]
oos_c = 1 - ((yc - predc) ** 2).sum() / ((yc - bc) ** 2).sum()
hit_c, hit_cb = (np.sign(predc) == np.sign(yc)).mean(), (np.sign(bc) == np.sign(yc)).mean()
check("p.51", "CSI 宏观模型 OOS R² (%)", -13.2, oos_c * 100, 1)
check("p.51", "CSI 宏观模型 命中率 (%)", 48.3, hit_c * 100, 1)
check("p.51", "CSI MA(12) 命中率 (%)", 56.7, hit_cb * 100, 1)
check("p.51", "CSI 宏观模型 MSE ×1e4", 31.65, ((yc - predc) ** 2).mean() * 1e4, 2)
check("p.51", "CSI MA(12) MSE ×1e4", 27.97, ((yc - bc) ** 2).mean() * 1e4, 2)
check("p.48", "CSI 测试期正收益月基准率 (%)", 48.3, (yc > 0).mean() * 100, 1)

# ---------- 7. 对照表 + 断言 ----------
tbl = pd.DataFrame(checks)
tbl["差"] = tbl["复现值"] - tbl["讲义值"]
tbl["容差(半个显示单位)"] = 0.5 * 10.0 ** (-tbl["小数位"]) + 1e-9
tbl["复现值(按讲义位数舍入)"] = [round(v, int(k)) for v, k in zip(tbl["复现值"], tbl["小数位"])]
tbl["对上?"] = np.where(tbl["差"].abs() <= tbl["容差(半个显示单位)"], "✅", "❌")
tbl.to_csv(load.OUTPUT_DIR / "L02_01_reproduce_lecture.csv", encoding="utf-8-sig", index=False, float_format="%.6g")

print("=" * 100)
print(f"Lec02 讲义数字复现（train 180 / test 60，statsmodels {sm.__version__}）")
print("-" * 100)
print(f"{'页':8s}{'项目':34s}{'讲义值':>10s}{'复现值':>12s}{'差':>12s}  结论")
for _, r in tbl.iterrows():
    k = int(r["小数位"])
    print(f"{r['讲义页']:8s}{r['项目']:34s}{r['讲义值']:>10.{k}f}{r['复现值']:>12.{k + 2}f}{r['差']:>+12.{k + 2}f}  {r['对上?']}")
print("-" * 100)
n_ok = int((tbl["对上?"] == "✅").sum())
print(f"共 {len(tbl)} 个数字，对上 {n_ok} 个，对不上 {len(tbl) - n_ok} 个")
print(f"精确值：corr 0.0229/0.1206/0.0533 · 简单回归斜率 {mom.params['momentum_12']*100:.3f}/{simple['volatility_12'].params['volatility_12']*100:.3f}/"
      f"{simple['ma_gap_10'].params['ma_gap_10']*100:.3f} pp · 动量 R² {mom.rsquared*100:.3f}%（讲义写 ≈0.1%，一位小数确实进到 0.1）")
print(f"      r̂(%) = {mom.params['const']*100:.3f} + {mom.params['momentum_12']*100:.3f}·mom · 标准化斜率 {fit3.params['momentum_12']*100:.2f}/"
      f"{fit3.params['volatility_12']*100:.2f}/{fit3.params['ma_gap_10']*100:.2f}% · R²_train {fit3.rsquared*100:.2f}%")
print(f"      SPY OOS R² {oos_r2*100:.2f}% · 命中率 {hit_model*100:.1f}% = 永远猜涨 {pos_months}/60 · MA(12) {hit_ma12*100:.1f}%"
      f" · 模型预测全部为正（{int((pred > 0).sum())}/60），所以命中率与'永远猜涨'完全相同")
print(f"      CSI 进口 β {fitc.params['imports_yoy_lag2']*100:.3f} pp，p={fitc.pvalues['imports_yoy_lag2']:.4f}，R²_train {fitc.rsquared*100:.2f}%"
      f" · OOS R² {oos_c*100:.2f}% · 命中率 {hit_c*100:.1f}% vs MA(12) {hit_cb*100:.1f}%（正收益基准率 {(yc>0).mean()*100:.1f}%）")
print("=" * 100)
assert (tbl["对上?"] == "✅").all(), "有讲义数字没有复现出来：\n" + tbl[tbl["对上?"] != "✅"].to_string()

# ---------- 8. 画图：四格，各对应一页讲义 ----------
fig, ax0 = plot.setup(figsize=(12.5, 9))
ax0.remove()
(ax1, ax2), (ax3, ax4) = fig.subplots(2, 2)

# (1) p.18/21：动量散点 + 拟合线
ax1.scatter(train["momentum_12"], y_tr * 100, s=16, alpha=0.5, color=plot.COLORS["actual"])
xx = np.linspace(train["momentum_12"].min(), train["momentum_12"].max(), 50)
ax1.plot(xx, (mom.params["const"] + mom.params["momentum_12"] * xx) * 100, color=plot.COLORS["fitted"], lw=2)
ax1.set_title(f"p.18/21  r̂(%) = {mom.params['const']*100:.2f} + {mom.params['momentum_12']*100:.2f}·mom，R² = {mom.rsquared*100:.2f}%", fontsize=10)
ax1.set_xlabel("滞后 12 个月动量（train 180 月）"); ax1.set_ylabel("下月 SPY 收益（%）")

# (2) p.33：标准化斜率 ± 1 se
ax2.bar(range(3), fit3.params[X3] * 100, yerr=fit3.bse[X3] * 100, color=[plot.COLORS["US_SPY"], plot.COLORS["CN_CSI300"], plot.COLORS["log"]],
        capsize=4, alpha=0.85)
for i, cc in enumerate(X3):
    ax2.text(i, fit3.params[cc] * 100 + fit3.bse[cc] * 100 + 0.05, f"p = {fit3.pvalues[cc]:.2f}", ha="center", fontsize=9)
ax2.set_xticks(range(3)); ax2.set_xticklabels([SHORT[cc] for cc in X3])
ax2.axhline(0, color="#999", lw=0.8)
ax2.set_ylabel("标准化斜率（% / 1 个训练 sd），误差线 ±1 se")
ax2.set_title(f"p.33  三变量标准化回归，R²_train = {fit3.rsquared*100:.1f}%", fontsize=10)

# (3) p.49：SPY 测试期 实现 vs 预测 vs MA(12)
ax3.plot(test.index, y_te * 100, color=plot.COLORS["actual"], lw=1.4, label="已实现收益")
ax3.plot(test.index, pred * 100, color=plot.COLORS["fitted"], lw=1.8, label="三变量回归预测")
ax3.plot(test.index, bench * 100, color=plot.COLORS["US_S&P500"], lw=1.4, ls="--", label="滞后 MA(12) 基准")
ax3.axhline(0, color="#999", lw=0.8)
ax3.set_title(f"p.49  SPY 样本外 60 月：OOS R² = {oos_r2*100:.2f}%，命中率 {hit_model*100:.1f}% = 永远猜涨 {pos_months}/60", fontsize=10)
ax3.set_ylabel("月收益（%）"); ax3.set_ylim(y_te.min() * 100 - 5, y_te.max() * 100 + 1); ax3.legend(fontsize=8, loc="lower right", ncol=3)
ax3.xaxis.set_major_locator(mdates.YearLocator()); ax3.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

# (4) p.51：CSI 300 宏观模型样本外
ax4.plot(cte.index, yc * 100, color=plot.COLORS["actual"], lw=1.4, label="已实现收益")
ax4.plot(cte.index, predc * 100, color=plot.COLORS["fitted"], lw=1.8, label="四宏观变量回归预测")
ax4.plot(cte.index, bc * 100, color=plot.COLORS["US_S&P500"], lw=1.4, ls="--", label="滞后 MA(12) 基准")
ax4.axhline(0, color="#999", lw=0.8)
ax4.set_title(f"p.51  CSI 300 宏观模型样本外：OOS R² = {oos_c*100:.2f}%（训练期 p = {fitc.pvalues['imports_yoy_lag2']:.4f}）", fontsize=10)
ax4.set_ylabel("月收益（%）"); ax4.set_ylim(yc.min() * 100 - 5, yc.max() * 100 + 1); ax4.legend(fontsize=8, loc="lower right", ncol=3)
ax4.xaxis.set_major_locator(mdates.YearLocator()); ax4.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

fig.suptitle(f"Lec02 讲义数字复现：{len(tbl)} 个已发布数字全部对上（对照表见 L02_01_reproduce_lecture.csv）", fontsize=13)
plot.save(fig, "L02_01_reproduce_lecture",
          note="数据：spy_monthly_features_240m.csv / csi300_macro_panel.csv（对数收益）· train < 2021-07 (180) / test (60) · statsmodels.OLS · 标准化只用 train 的 mu/sd · 基准 = 滞后 MA(12)")
