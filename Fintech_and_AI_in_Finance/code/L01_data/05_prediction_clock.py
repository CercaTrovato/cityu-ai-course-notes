"""
L01_05 · 预测时钟可视化：预测 2026-06 时，15 个特征各自用到了哪些月份的原始数据
=================================================================================
目的      讲义 p.43 用一行公式讲预测时钟（x_t → r_{t+1}），本脚本把它画成甘特图：横轴是原始数据所属的月份，
          纵轴是特征表的 15 个预测变量 + 1 个目标，每行画出它实际引用的时间窗；红线 = 决策时点（2026-05 月末）。
          所有特征的窗口都在红线左边，只有目标 market_return 在右边——这就是"无泄漏"的图像定义。
讲义      Lec01 p.43（预测时钟四条规则）、p.27（三种日期）、p.33（参考月 ≠ 发布日）
笔记      [[M01-金融数据与Vibe-Coding]] §2.5.1、§2.5.4、§2.7.3
输入      spy_monthly_features_240m.csv（用 2026-06 那行做对照）、market_index_prices_240m.csv / market_index_returns_240m.csv
          （US_SPY）、macro_240m.csv
输出      output/L01_05_prediction_clock.png · output/L01_05_prediction_clock.csv
关键决定  · 时间窗不是手写的，是**扰动法**测出来的：把某个月的原始数据改一点点，看 2026-06 那行的哪些特征跟着变。
            变了 = 该特征用到了那个月。这样画出来的窗口就是代码实际的信息依赖，不是想当然
          · 价量类特征的原始数据取"月度对数收益"（价格 = 起点 × exp(Σr)）：动量 / 波动率 / 均线偏离都能表示成
            一段连续的收益月份；ma_gap_k 用 k 个月末价 = k−1 个收益，所以它的窗口比 k 少一格
          · 宏观类特征的原始数据取宏观表的**参考月**（不是发布日——文件里只有参考月，滞后 1/2 个月就是为此留的余量）
          · 重构公式沿用 L01_04 已验证的规则；先断言重构出的 2026-06 那行与文件逐项相等，再做扰动
          · 决策时点 = forecast_month 的前一个月末（2026-05-31）；红线画在 2026-05 与 2026-06 之间
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))   # 让 common 可导入，脚本从哪启动都能跑

import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle, Patch

from common import load, plot

FORECAST = pd.Timestamp("2026-06-30")

# ---------- 1. 读数据，准备"原始数据" ----------
feat = load.spy_features()
px = load.index_prices()["US_SPY"]
ret = load.index_returns()["US_SPY"]
mac = load.macro()[["term_spread", "unemployment_rate", "inflation_yoy"]]
FEATURES = [c for c in feat.columns if c != "market_return"]
assert len(FEATURES) == 15

# 价量类原始数据 = 月度对数收益（含 2006-07 首行的真实收益）；价格由收益重建，起点取反推出的 2006-06 价格
p0 = px.iloc[0] / np.exp(ret.iloc[0])


def build(r: pd.Series, m: pd.DataFrame) -> pd.DataFrame:
    """用 L01_04 验证过的规则，从收益 r 与宏观表 m 重构 15 个特征 + 目标。"""
    p_ext = pd.concat([pd.Series([p0], index=[pd.Timestamp("2006-06-30")]), p0 * np.exp(r.cumsum())]).sort_index()
    out = {"market_return": r}
    for k in (1, 2, 3):
        out[f"return_lag{k}"] = r.shift(k)
    for k in (3, 6, 12):
        out[f"momentum_{k}"] = (p_ext.shift(1) / p_ext.shift(k + 1) - 1).reindex(r.index)
        out[f"volatility_{k}"] = r.shift(1).rolling(k).std(ddof=1) * np.sqrt(12)
    for k in (3, 6, 10):
        out[f"ma_gap_{k}"] = (p_ext.shift(1) / p_ext.shift(1).rolling(k).mean() - 1).reindex(r.index)
    out["term_spread_lag1"] = m["term_spread"].shift(1)
    out["unemployment_lag2"] = m["unemployment_rate"].shift(2)
    out["inflation_yoy_lag2"] = m["inflation_yoy"].shift(2)
    return pd.DataFrame(out)[feat.columns]


base = build(ret, mac)
# 自检：重构出的 2026-06 那行与文件逐项相等（这一步把本脚本与 L01_04 的结论绑在一起）
gap = (base.loc[FORECAST] - feat.loc[FORECAST]).abs()
assert gap.max() < 1e-12, f"重构与文件不一致：\n{gap[gap >= 1e-12]}"

# ---------- 2. 扰动法：逐月改动原始数据，看 2026-06 那行谁变了 ----------
months = pd.date_range("2025-03-31", "2026-06-30", freq="ME")
dep = pd.DataFrame(False, index=feat.columns, columns=months)          # dep[feature, month] = 该特征用到了该月
src = pd.Series("", index=feat.columns)                                # 每个特征的原始数据来源

for m in months:
    r2 = ret.copy(); r2[m] += 0.01                                      # 价量类：改动该月的收益
    changed = (build(r2, mac).loc[FORECAST] - base.loc[FORECAST]).abs() > 1e-12
    dep.loc[changed[changed].index, m] = True
    for col in ("term_spread", "unemployment_rate", "inflation_yoy"):   # 宏观类：改动该月的参考月数值
        m2 = mac.copy(); m2.loc[m, col] = (0 if pd.isna(m2.loc[m, col]) else m2.loc[m, col]) + 1.0
        changed = (build(ret, m2).loc[FORECAST] - base.loc[FORECAST]).abs() > 1e-12
        dep.loc[changed[changed].index, m] = True

for f in feat.columns:
    src[f] = "宏观参考月" if f in ("term_spread_lag1", "unemployment_lag2", "inflation_yoy_lag2") else "SPY 月度收益"

windows = pd.DataFrame({
    "来源": src,
    "窗口起": [dep.loc[f][dep.loc[f]].index.min().strftime("%Y-%m") if dep.loc[f].any() else "" for f in feat.columns],
    "窗口止": [dep.loc[f][dep.loc[f]].index.max().strftime("%Y-%m") if dep.loc[f].any() else "" for f in feat.columns],
    "引用月数": dep.sum(axis=1),
})
windows.to_csv(load.OUTPUT_DIR / "L01_05_prediction_clock.csv", encoding="utf-8-sig")

# ---------- 3. 断言：预测时钟成立 ----------
last_used = {f: dep.loc[f][dep.loc[f]].index.max() for f in feat.columns}
for f in FEATURES:
    assert last_used[f] < FORECAST, f"{f} 用到了 {last_used[f].date()} 的数据——晚于决策时点，存在泄漏！"
assert last_used["market_return"] == FORECAST and dep.loc["market_return"].sum() == 1, "目标只能依赖预测月当月"
expected = {"return_lag1": 1, "return_lag2": 1, "return_lag3": 1, "momentum_3": 3, "momentum_6": 6, "momentum_12": 12,
            "volatility_3": 3, "volatility_6": 6, "volatility_12": 12, "ma_gap_3": 2, "ma_gap_6": 5, "ma_gap_10": 9,
            "term_spread_lag1": 1, "unemployment_lag2": 1, "inflation_yoy_lag2": 1}
for f, n in expected.items():
    assert windows.loc[f, "引用月数"] == n, f"{f} 引用月数 {windows.loc[f, '引用月数']} ≠ 预期 {n}"

print("=" * 80)
print(f"预测 {FORECAST.strftime('%Y-%m')} 时（决策时点 = 2026-05 月末），每个特征实际引用的原始数据月份（扰动法测得）")
print("-" * 80)
print(f"{'列':20s}{'来源':12s}{'窗口':22s}{'月数':>4s}   说明")
notes = {"return_lag1": "r[t−1]", "return_lag2": "r[t−2]", "return_lag3": "r[t−3]",
         "momentum_3": "P[t−1]/P[t−4] − 1 = 3 个收益", "momentum_6": "P[t−1]/P[t−7] − 1 = 6 个收益", "momentum_12": "P[t−1]/P[t−13] − 1 = 12 个收益",
         "volatility_3": "sd(r[t−3..t−1])·√12", "volatility_6": "sd(r[t−6..t−1])·√12", "volatility_12": "sd(r[t−12..t−1])·√12",
         "ma_gap_3": "3 个月末价 = 2 个收益", "ma_gap_6": "6 个月末价 = 5 个收益", "ma_gap_10": "10 个月末价 = 9 个收益",
         "term_spread_lag1": "参考月 t−1（日频均值，发布无滞后）", "unemployment_lag2": "参考月 t−2（次月发布，多留 1 个月）",
         "inflation_yoy_lag2": "参考月 t−2（次月发布，多留 1 个月）", "market_return": "目标：在 t 当月实现 ← 唯一在红线右边"}
for f in feat.columns:
    w = windows.loc[f]
    span = w["窗口起"] if w["窗口起"] == w["窗口止"] else f"{w['窗口起']} → {w['窗口止']}"
    print(f"{f:20s}{w['来源']:12s}{span:22s}{int(w['引用月数']):>4d}   {notes[f]}")
print("-" * 80)
latest = max(last_used[f] for f in FEATURES)
print(f"15 个特征引用的最晚月份 = {latest.strftime('%Y-%m')} < 预测月 {FORECAST.strftime('%Y-%m')}  ✅ 预测时钟成立，无泄漏")
print(f"最长回看 = momentum_12 / volatility_12：{windows.loc['momentum_12', '窗口起']} 起，共 12 个月")
print("=" * 80)

# ---------- 4. 画图：甘特图 ----------
order = list(FEATURES) + ["market_return"]
fig, ax = plot.setup(figsize=(11, 8))
color_of = {"SPY 月度收益": plot.COLORS["US_SPY"], "宏观参考月": plot.COLORS["CN_CSI300"]}
xs = list(months)
for i, f in enumerate(order):
    y = len(order) - 1 - i
    col = plot.COLORS["fitted"] if f == "market_return" else color_of[src[f]]
    for j, m in enumerate(xs):
        if dep.loc[f, m]:
            ax.add_patch(Rectangle((j, y - 0.36), 1, 0.72, facecolor=col, edgecolor="white", lw=0.8, alpha=0.9))
    w = windows.loc[f]
    label = f"{w['窗口起']}" if w["窗口起"] == w["窗口止"] else f"{w['窗口起']} → {w['窗口止']}（{int(w['引用月数'])} 个月）"
    ax.text(len(xs) + 0.2, y, label, va="center", fontsize=8, color="#333")

# 决策时点：2026-05 与 2026-06 之间
cut = xs.index(FORECAST)
ax.axvline(cut, color=plot.COLORS["fitted"], lw=2)
ax.text(cut - 0.15, len(order) + 0.85, "决策时点 2026-05 月末 ◀", ha="right", va="top", fontsize=9, color=plot.COLORS["fitted"], fontweight="bold")
ax.text(cut + 0.15, len(order) + 0.85, "▶ 预测月 2026-06", ha="left", va="top", fontsize=9, color=plot.COLORS["fitted"], fontweight="bold")
ax.axvspan(cut, len(xs), color=plot.COLORS["fitted"], alpha=0.05)

ax.set_xlim(0, len(xs) + 5.2)
ax.set_ylim(-0.6, len(order) + 1.0)
ax.set_xticks(np.arange(len(xs)) + 0.5)
ax.set_xticklabels([m.strftime("%Y-%m") for m in xs], rotation=45, ha="right", fontsize=8)
ax.set_yticks(range(len(order)))
ax.set_yticklabels(order[::-1], fontsize=9)
ax.grid(False)
ax.set_xlabel("原始数据所属的月份（价量类 = SPY 月度收益所在月；宏观类 = 参考月）")
ax.set_title("预测时钟：预测 2026-06 时，15 个特征各自引用了哪些月份的数据（扰动法实测）", fontsize=12.5)
ax.legend(handles=[Patch(color=color_of["SPY 月度收益"], label="价量类：SPY 月度收益 / 月末价"),
                   Patch(color=color_of["宏观参考月"], label="宏观类：参考月（发布日更晚，故多留 1–2 个月）"),
                   Patch(color=plot.COLORS["fitted"], label="目标 market_return：在预测月内实现")],
          loc="lower left", fontsize=8.5)
plot.save(fig, "L01_05_prediction_clock",
          note="数据：spy_monthly_features_240m.csv 的 2026-06 行 · 窗口由扰动法测得（改动某月原始数据，看该行哪些特征跟着变）· 重构规则见 L01_04")
