"""
L02_02 · 样本外 R² 随窗口怎么变：滚动窗口 vs 扩展窗口
=======================================================
目的      讲义 p.40 列了三种回测设计（固定留出 / 扩展窗口 / 滚动窗口），但只报了固定留出的结果（SPY OOS R² 6.6%）。
          本脚本对同一个三变量模型做逐月再估计：从 60 个月起扩展、或固定长度滚动，看 OOS R² 随时间怎么累积、
          以及讲义那 6.56% 换一种窗口设计还剩多少。
讲义      Lec02 p.37–41（按日期切分、三种设计）、p.46–50（样本外结果）
笔记      [[M02-回归与样本外设计]] §2.6.3、§2.6.4、§2.7.4
输入      spy_monthly_features_240m.csv（对数收益）
输出      output/L02_02_oos_rolling.png · output/L02_02_oos_rolling.csv
关键决定  · 模型 = 讲义的三变量 OLS（momentum_12 / volatility_12 / ma_gap_10），statsmodels.OLS；预测不需要标准化（斜率单位不影响预测）
          · 扩展窗口：第一个预测用前 60 个月（2006-07 → 2011-06）估计，之后每月把新观测加进训练集重估，共 180 个预测（2011-07 → 2026-06）
          · 滚动窗口：训练集固定为最近 60 / 120 / 180 个月，整体向后平移；滚动 60 与扩展窗口从同一个月开始预测，起点相同、之后分叉
          · 固定留出（讲义）：2021-06 冻结系数，60 个测试月一次评分——就是 L02_01 复现的 6.56%
          · 基准始终 = 滞后 MA(12)；累计 OOS R²(t) = 1 − Σ_{s≤t}(r−r̂)² / Σ_{s≤t}(r−r̂ᵇ)²，从各设计的第一个预测起累计
          · 累计曲线的前 12 个预测不画（只有几个观测时比值没有意义，第 1 个月是 +52%）
          · 每个设计都只用预测月之前的信息估计（fit before evaluate，讲义 p.40）；无交易成本
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))   # 让 common 可导入，脚本从哪启动都能跑

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.dates as mdates

from common import load, plot

X3 = ["momentum_12", "volatility_12", "ma_gap_10"]
SPLIT = pd.Timestamp("2021-07-01")
MIN_TRAIN = 60

d = load.spy_features()
r = d["market_return"]
ma12 = r.shift(1).rolling(12).mean()
n = len(d)
assert n == 240 and ma12.notna().sum() == 228


def recursive_forecasts(kind: str, window: int) -> pd.Series:
    """逐月再估计：kind='expanding' 用 [0, t)，kind='rolling' 用 [t−window, t)；返回对每个 t 的预测。"""
    pred = pd.Series(np.nan, index=d.index)
    for t in range(window, n):
        lo = 0 if kind == "expanding" else t - window
        tr = d.iloc[lo:t]
        assert tr.index.max() < d.index[t]                   # 只用预测月之前的行
        fit = sm.OLS(tr["market_return"], sm.add_constant(tr[X3])).fit()
        x_t = sm.add_constant(d.iloc[[t]][X3], has_constant="add")
        pred.iloc[t] = fit.predict(x_t).iloc[0]
    return pred


def oos_r2(pred: pd.Series, start=None) -> float:
    idx = pred.loc[start:].dropna().index if start is not None else pred.dropna().index
    return 1 - ((r[idx] - pred[idx]) ** 2).sum() / ((r[idx] - ma12[idx]) ** 2).sum()


def cum_oos_r2(pred: pd.Series) -> pd.Series:
    idx = pred.dropna().index
    se_m = ((r[idx] - pred[idx]) ** 2).cumsum()
    se_b = ((r[idx] - ma12[idx]) ** 2).cumsum()
    return 1 - se_m / se_b


designs = {
    "扩展窗口（起始 60 月）": recursive_forecasts("expanding", MIN_TRAIN),
    "滚动窗口 60 月": recursive_forecasts("rolling", 60),
    "滚动窗口 120 月": recursive_forecasts("rolling", 120),
    "滚动窗口 180 月": recursive_forecasts("rolling", 180),
}
# 固定留出（讲义）：2021-06 冻结
train, test = d[d.index < SPLIT], d[d.index >= SPLIT]
fit_fixed = sm.OLS(train["market_return"], sm.add_constant(train[X3])).fit()
fixed = pd.Series(np.nan, index=d.index)
fixed.loc[test.index] = fit_fixed.predict(sm.add_constant(test[X3]))
designs["固定留出（讲义，2021-06 冻结）"] = fixed

# ---------- 关键数字 ----------
rows = []
for name, p in designs.items():
    first = p.first_valid_index()
    rows.append({"设计": name, "首个预测月": first.strftime("%Y-%m"), "预测月数": int(p.notna().sum()),
                 "全期累计 OOS R²": oos_r2(p), "讲义测试期 OOS R²(2021-07→)": oos_r2(p, SPLIT),
                 "讲义测试期命中率": float((np.sign(p.loc[SPLIT:]) == np.sign(r.loc[SPLIT:])).mean())})
summary = pd.DataFrame(rows).set_index("设计")
summary.to_csv(load.OUTPUT_DIR / "L02_02_oos_rolling.csv", encoding="utf-8-sig", float_format="%.6f")

oos_fixed = summary.loc["固定留出（讲义，2021-06 冻结）", "讲义测试期 OOS R²(2021-07→)"]
assert abs(oos_fixed - 0.0656) < 5e-4, f"固定留出 OOS R² {oos_fixed:.4%} 应等于讲义的 6.56%"
# 自检：滚动 180 在 2021-07 那个月的训练集就是讲义的 train，所以第一个预测必须与固定留出相同
assert abs(designs["滚动窗口 180 月"].loc[SPLIT:].iloc[0] - fixed.loc[SPLIT:].iloc[0]) < 1e-12
assert abs(designs["扩展窗口（起始 60 月）"].loc[SPLIT:].iloc[0] - fixed.loc[SPLIT:].iloc[0]) < 1e-12

print("=" * 96)
print("SPY 三变量模型 · 样本外 R²（vs 滞后 MA(12)）随窗口设计的变化")
print("-" * 96)
print(f"{'设计':30s}{'首个预测':>10s}{'预测数':>6s}{'全期累计 OOS R²':>16s}{'讲义测试期 OOS R²':>18s}{'测试期命中率':>12s}")
for name, s in summary.iterrows():
    print(f"{name:30s}{s['首个预测月']:>10s}{s['预测月数']:>6d}{s['全期累计 OOS R²']*100:>15.2f}%{s['讲义测试期 OOS R²(2021-07→)']*100:>17.2f}%"
          f"{s['讲义测试期命中率']*100:>11.1f}%")
print("-" * 96)
exp_cum = cum_oos_r2(designs["扩展窗口（起始 60 月）"])
roll60_cum = cum_oos_r2(designs["滚动窗口 60 月"])
print(f"扩展窗口累计 OOS R²：第 1 个月 {exp_cum.iloc[0]*100:+.1f}%（无意义）→ 第 12 个月 {exp_cum.iloc[11]*100:+.2f}% → "
      f"2016-06 {exp_cum.loc['2016-06-30']*100:+.2f}% → 2021-06 {exp_cum.loc['2021-06-30']*100:+.2f}% → 终点 {exp_cum.iloc[-1]*100:+.2f}%")
print(f"滚动 60 月累计 OOS R²：最低 {roll60_cum.iloc[12:].min()*100:+.2f}%（{roll60_cum.iloc[12:].idxmin().strftime('%Y-%m')}）→ 终点 {roll60_cum.iloc[-1]*100:+.2f}%")
print(f"结论：讲义的 6.56% 是固定留出的结果；同一模型逐月重估——扩展窗口在同一测试期得 "
      f"{summary.loc['扩展窗口（起始 60 月）', '讲义测试期 OOS R²(2021-07→)']*100:.2f}%（180 个预测的全期为 "
      f"{summary.loc['扩展窗口（起始 60 月）', '全期累计 OOS R²']*100:.2f}%），滚动 180 得 "
      f"{summary.loc['滚动窗口 180 月', '讲义测试期 OOS R²(2021-07→)']*100:.2f}%，")
print(f"      但滚动 120 只剩 {summary.loc['滚动窗口 120 月', '讲义测试期 OOS R²(2021-07→)']*100:.2f}%、滚动 60 变成 "
      f"{summary.loc['滚动窗口 60 月', '讲义测试期 OOS R²(2021-07→)']*100:.2f}%——窗口越短，系数噪声越大，输给 MA(12)。")
print("=" * 96)

# ---------- 画图 ----------
fig, ax0 = plot.setup(figsize=(11.5, 9))
ax0.remove()
ax_t, ax_b = fig.subplots(2, 1, gridspec_kw={"height_ratios": [1.5, 1]})

style = {"扩展窗口（起始 60 月）": (plot.COLORS["US_S&P500"], "-", 2.0),
         "滚动窗口 60 月": (plot.COLORS["fitted"], "-", 1.4),
         "滚动窗口 120 月": (plot.COLORS["CN_CSI300"], "-", 1.4),
         "滚动窗口 180 月": (plot.COLORS["log"], "-", 1.4),
         "固定留出（讲义，2021-06 冻结）": (plot.COLORS["actual"], "--", 2.0)}
WARM = 12
lo_y, hi_y = 0.0, 0.0
for name, p in designs.items():
    cum = cum_oos_r2(p)
    cum_plot = cum.iloc[WARM:]               # 前 12 个预测为预热期，不画（累计值仍从首个预测起算）
    lo_y, hi_y = min(lo_y, cum_plot.min() * 100), max(hi_y, cum_plot.max() * 100)
    c, ls, lw = style[name]
    ax_t.plot(cum_plot.index, cum_plot * 100, color=c, ls=ls, lw=lw, label=f"{name}  终点 {cum.iloc[-1]*100:+.2f}%")
ax_t.axhline(0, color="#999", lw=0.8)
ax_t.axvspan(SPLIT, d.index[-1], color="#999", alpha=0.10)
Y_FLOOR = -35
ax_t.set_ylim(max(lo_y - 3, Y_FLOOR), hi_y + 5)
ax_t.text(SPLIT, hi_y + 4.5, " 讲义测试期 2021-07 → 2026-06", fontsize=8.5, color="#555", va="top")
r120 = cum_oos_r2(designs["滚动窗口 120 月"]).iloc[WARM:]
if r120.min() * 100 < Y_FLOOR:   # 滚动 120 在 2018 年初的深坑超出画幅，只标注不画
    ax_t.annotate(f"滚动 120 月最低 {r120.min()*100:+.0f}%（{r120.idxmin().strftime('%Y-%m')}，超出画幅）",
                  xy=(r120.idxmin(), Y_FLOOR + 1), xytext=(-230, 12), textcoords="offset points", fontsize=8,
                  color=plot.COLORS["CN_CSI300"], arrowprops=dict(arrowstyle="-", color=plot.COLORS["CN_CSI300"], lw=0.8))
ax_t.set_ylabel("累计 OOS R²（%，vs 滞后 MA(12)，自各设计首个预测起累计）")
ax_t.set_title("同一个三变量模型，逐月重估：样本外 R² 随窗口设计怎么变", fontsize=12.5)
ax_t.legend(loc="lower right", fontsize=8.5)
ax_t.xaxis.set_major_locator(mdates.YearLocator(2)); ax_t.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax_t.annotate(f"讲义 6.56%", xy=(d.index[-1], oos_fixed * 100), xytext=(-70, 22), textcoords="offset points", fontsize=9,
              fontweight="bold", color=plot.COLORS["actual"], arrowprops=dict(arrowstyle="-", color=plot.COLORS["actual"], lw=0.8))

order = ["固定留出（讲义，2021-06 冻结）", "扩展窗口（起始 60 月）", "滚动窗口 180 月", "滚动窗口 120 月", "滚动窗口 60 月"]
vals = [summary.loc[k, "讲义测试期 OOS R²(2021-07→)"] * 100 for k in order]
bars = ax_b.bar(range(len(order)), vals, color=[style[k][0] for k in order], alpha=0.85)
for i, v in enumerate(vals):
    ax_b.text(i, v + (0.4 if v >= 0 else -0.9), f"{v:+.2f}%", ha="center", fontsize=9.5, fontweight="bold")
ax_b.axhline(0, color="#999", lw=0.8)
ax_b.set_xticks(range(len(order)))
ax_b.set_xticklabels([k.replace("（讲义，2021-06 冻结）", "\n（讲义）").replace("（起始 60 月）", "\n（起始 60 月）") for k in order], fontsize=9)
ax_b.set_ylabel("讲义测试期 OOS R²（%）")
ax_b.set_ylim(min(vals) - 3, max(vals) + 3)
ax_b.set_title("同一个 60 月测试期（2021-07 → 2026-06），五种窗口设计的 OOS R²：窗口越短越差", fontsize=11)

plot.save(fig, "L02_02_oos_rolling",
          note="数据：spy_monthly_features_240m.csv（对数收益）· 三变量 OLS 逐月重估，只用预测月之前的行 · 基准 = 滞后 MA(12) · 累计曲线前 12 个预测不画 · 无交易成本")
