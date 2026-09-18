"""
L01_04 · 逐列验算特征表没有泄漏：15 个预测变量能否只用"更早的"原始数据重构出来
=====================================================================================
目的      数据集卡片 §7 说 spy_monthly_features_240m.csv 的 4 类滞后规则误差全为 0。本脚本用代码证明：
          对 15 个预测变量逐列用价格表 / 收益表 / 宏观表按"只用 t−1 及更早"的规则重构，报每列的最大绝对误差；
          （⚠️ 卡片与 load.py 说"16 个特征"，实为 16 个非日期列 = 1 个目标 market_return + 15 个预测变量）
          再故意按 7 种错误方式重构（不滞后、居中窗口、ddof=0、收益连乘……），证明这套验算真的抓得到泄漏。
讲义      Lec01 p.43（预测时钟四条规则）、p.46（shift(1) 的代码）、p.47（三行手检）、p.48（五种泄漏路径）
笔记      [[M01-金融数据与Vibe-Coding]] §2.7.3、§9.4 ②；数据集卡片 §7
输入      spy_monthly_features_240m.csv（被审计对象）；market_index_prices_240m.csv / market_index_returns_240m.csv /
          macro_240m.csv（重构用的原料，US_SPY 列）
输出      output/L01_04_leakage_audit.png · output/L01_04_leakage_audit.csv
关键决定  · 重构规则（t = forecast_month，所有窗口止于 t−1）：
              return_lag_k[t]   = r[t−k]
              momentum_k[t]     = P[t−1] / P[t−k−1] − 1        ← 用价格算；收益是对数收益，∏(1+r) 会算错、exp(Σr) 才对
              volatility_k[t]   = sd(r[t−k…t−1], ddof=1) × √12  ← 样本标准差，年化
              ma_gap_k[t]       = P[t−1] / mean(P[t−k…t−1]) − 1
              term_spread_lag1  = macro.term_spread[t−1]；unemployment_lag2 / inflation_yoy_lag2 = macro[t−2]
          · 审计窗口 = 2007-07-31 起的 228 行（跳过前 12 行：它们的 12 月窗口用了样本前的数据，文件里看不到）
          · momentum_12 在 2007-07 那行要用 2006-06 的价格，价格表没有——但收益表首行是 2006-06→07 的真实对数收益，
            所以 P_{2006-06} = P_{2006-07} / exp(r_{2006-07}) 可以反推出来（88.13），这样 15 列都能从 2007-07 起验
          · 误差阈值 1e-12：浮点重算的误差量级是 1e-16，任何真实的构造差异都在 1e-3 以上，中间没有灰色地带
          · 缺失处理：2025-12 行的两个宏观特征本来就是 NaN（来自宏观表 2025-10 的缺口），比较时跳过 NaN，不填补
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))   # 让 common 可导入，脚本从哪启动都能跑

import numpy as np
import pandas as pd

from common import load, plot

TOL = 1e-12
AUDIT_START = "2007-07-31"     # 跳过前 12 行

# ---------- 1. 读数据 ----------
feat = load.spy_features()
px = load.index_prices()["US_SPY"]
ret = load.index_returns()["US_SPY"]
mac = load.macro()
assert (feat["market_return"] - ret).abs().max() == 0, "目标列应与收益表的 US_SPY 完全同源"

# 反推价格表里没有的 2006-06 价格：收益表首行 = ln(P_{2006-07}/P_{2006-06})
p_2006_06 = px.iloc[0] / np.exp(ret.iloc[0])
px_ext = pd.concat([pd.Series([p_2006_06], index=[pd.Timestamp("2006-06-30")]), px]).sort_index()
assert abs(np.log(px_ext.iloc[1] / px_ext.iloc[0]) - ret.iloc[0]) < 1e-15

# ---------- 2. 按"只用 t−1 及更早"的规则重构 15 列 ----------
def rebuild():
    r = ret; p = px_ext
    out = {}
    for k in (1, 2, 3):
        out[f"return_lag{k}"] = r.shift(k)
    for k in (3, 6, 12):
        out[f"momentum_{k}"] = (p.shift(1) / p.shift(k + 1) - 1).reindex(feat.index)
        out[f"volatility_{k}"] = r.shift(1).rolling(k).std(ddof=1) * np.sqrt(12)
    for k in (3, 6, 10):
        out[f"ma_gap_{k}"] = (p.shift(1) / p.shift(1).rolling(k).mean() - 1).reindex(feat.index)
    out["term_spread_lag1"] = mac["term_spread"].shift(1)
    out["unemployment_lag2"] = mac["unemployment_rate"].shift(2)
    out["inflation_yoy_lag2"] = mac["inflation_yoy"].shift(2)
    return pd.DataFrame(out)

rebuilt = rebuild()
cols = [c for c in feat.columns if c != "market_return"]
assert len(cols) == 15 and set(cols) == set(rebuilt.columns), "特征表应为 1 个目标 + 15 个预测变量"

# ---------- 3. 反例：故意做错的 7 种构造（前 5 种是泄漏，后 2 种是口径错） ----------
wrong = {   # 名称: (对照的文件列, 错误构造)
    "momentum_12 不滞后 P_t/P_{t−12}−1（泄漏：用了当月价）": ("momentum_12", px / px.shift(12) - 1),
    "return_lag1 不滞后（泄漏：= 当月收益）": ("return_lag1", ret),
    "volatility_12 居中窗口 center=True（泄漏路径②）": ("volatility_12", ret.rolling(12, center=True).std(ddof=1) * np.sqrt(12)),
    "unemployment_lag2 只滞后 1 个月（泄漏：参考月≠发布日）": ("unemployment_lag2", mac["unemployment_rate"].shift(1)),
    "term_spread_lag1 不滞后（泄漏：用了当月利差）": ("term_spread_lag1", mac["term_spread"]),
    "volatility_12 用总体标准差 ddof=0（口径错）": ("volatility_12", ret.shift(1).rolling(12).std(ddof=0) * np.sqrt(12)),
    "momentum_12 用 ∏(1+r)−1 收益连乘（口径错：r 是对数收益）": ("momentum_12", (1 + ret.shift(1)).rolling(12).apply(np.prod, raw=True) - 1),
}
# 附加一条"看似不同、其实等价"的构造：对数收益累加 exp(Σr)−1 与价格法相同
alt_ok = np.exp(ret.shift(1).rolling(12).sum()) - 1

# ---------- 4. 逐列误差 ----------
rows = []
for c in cols:
    a = feat[c].loc[AUDIT_START:]
    b = rebuilt[c].loc[AUDIT_START:]
    both = a.notna() & b.notna()
    err = (a[both] - b[both]).abs()
    first_ok = rebuilt[c].first_valid_index()
    rows.append({"列": c, "类型": "正确规则", "比较行数": int(both.sum()), "最大绝对误差": float(err.max()),
                 "文件NaN": int(a.isna().sum()), "无需反推即可验的首行": str(first_ok.date()), "结论": "✅ 无泄漏" if err.max() < TOL else "❌"})
for name, (tgt, series) in wrong.items():
    a = feat[tgt].loc[AUDIT_START:]; b = series.reindex(feat.index).loc[AUDIT_START:]
    both = a.notna() & b.notna()
    err = (a[both] - b[both]).abs()
    rows.append({"列": name, "类型": "反例（故意做错）", "比较行数": int(both.sum()), "最大绝对误差": float(err.max()),
                 "文件NaN": int(a.isna().sum()), "无需反推即可验的首行": "", "结论": "抓到 ✔" if err.max() > TOL else "❌ 没抓到"})
a = feat["momentum_12"].loc[AUDIT_START:]; b = alt_ok.loc[AUDIT_START:]
rows.append({"列": "momentum_12 用 exp(Σr)−1 对数收益累加（等价写法）", "类型": "等价构造", "比较行数": int(len(a)),
             "最大绝对误差": float((a - b).abs().max()), "文件NaN": 0, "无需反推即可验的首行": "", "结论": "✅ 与价格法相同"})
table = pd.DataFrame(rows)
table.to_csv(load.OUTPUT_DIR / "L01_04_leakage_audit.csv", encoding="utf-8-sig", index=False)

good = table[table["类型"] == "正确规则"]
bad = table[table["类型"] == "反例（故意做错）"]
# 断言：15 列全部在浮点误差内；7 个反例全部被抓到
assert (good["最大绝对误差"] < TOL).all(), "有特征列不能用 t−1 及更早的数据重构——可能存在泄漏或口径差异"
assert (bad["最大绝对误差"] > 1e-3).all(), "反例没有被抓到，说明验算没有区分力"
assert (good["比较行数"] >= 227).all()      # 228 行；两个宏观列少 1 行（2025-12 缺失）

print("=" * 96)
print(f"审计对象 spy_monthly_features_240m.csv · 15 个预测变量（+1 个目标列 market_return，与收益表误差 0）")
print(f"审计窗口 {AUDIT_START} → 2026-06-30（228 行，跳过前 12 行）")
print(f"反推出的 2006-06 SPY 价格 = {p_2006_06:.4f}（用收益表首行 {ret.iloc[0]:+.6f} 反推，使 momentum_12 从 2007-07 起可验）")
print("-" * 96)
print(f"{'列':22s}{'比较行数':>6s}{'最大绝对误差':>14s}{'文件NaN':>8s}{'不反推可验首行':>16s}  结论")
for _, r in good.iterrows():
    print(f"{r['列']:22s}{r['比较行数']:>8d}{r['最大绝对误差']:>16.2e}{r['文件NaN']:>8d}{r['无需反推即可验的首行']:>16s}  {r['结论']}")
print("-" * 96)
print("反例（故意做错的构造）——同一套验算必须能抓到：")
for _, r in bad.iterrows():
    print(f"  {r['最大绝对误差']:>10.2e}  {r['列']}  → {r['结论']}")
eq = table[table["类型"] == "等价构造"].iloc[0]
print(f"等价构造：{eq['列']}  误差 {eq['最大绝对误差']:.2e}")
print("-" * 96)
print(f"结论：15 列最大误差 {good['最大绝对误差'].max():.2e}（浮点量级），7 个反例最小误差 {bad['最大绝对误差'].min():.2e}——")
print("      正确规则与任何一种错误构造之间差 13 个数量级，'误差为 0' 不是巧合，是构造规则被精确复现。")
print(f"      2025-12 行的 unemployment_lag2 / inflation_yoy_lag2 为 NaN（宏观表 2025-10 缺口 + 2 个月滞后），未填补。")
print("=" * 96)

# ---------- 5. 画图：每列最大绝对误差（对数坐标），正确规则 vs 反例 ----------
fig, ax = plot.setup(figsize=(11, 8))
plot_tbl = pd.concat([good, table[table["类型"] == "等价构造"], bad]).reset_index(drop=True)
floor = 1e-17
vals = plot_tbl["最大绝对误差"].clip(lower=floor)
colors = {"正确规则": plot.COLORS["simple"], "等价构造": plot.COLORS["log"], "反例（故意做错）": plot.COLORS["fitted"]}
ypos = np.arange(len(plot_tbl))[::-1]
ax.barh(ypos, vals, color=[colors[t] for t in plot_tbl["类型"]], alpha=0.85, height=0.7)
ax.set_xscale("log")
ax.set_xlim(floor, 1e3)
ax.axvline(TOL, color="#333", ls="--", lw=1)
ax.text(TOL, len(plot_tbl) - 0.2, f" 判定阈值 {TOL:.0e}", fontsize=8.5, va="bottom", ha="left", color="#333")
ax.set_yticks(ypos)
ax.set_yticklabels(plot_tbl["列"], fontsize=8.5)
for y, v, raw in zip(ypos, vals, plot_tbl["最大绝对误差"]):
    ax.text(v * 1.6, y, "0（精确相等）" if raw == 0 else f"{raw:.1e}", va="center", fontsize=8, color="#333")
ax.set_xlabel("与文件列的最大绝对误差（对数坐标；审计窗口 2007-07 → 2026-06，228 行）")
ax.set_title("特征表逐列重构：15 个预测变量按正确规则误差 ≈ 0，7 种错误构造全部被抓到", fontsize=12.5)
ax.grid(True, axis="x", alpha=0.3); ax.grid(False, axis="y")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=colors["正确规则"], label="正确规则：只用 t−1 及更早的数据重构"),
                   Patch(color=colors["等价构造"], label="等价构造：对数收益累加 = 价格比"),
                   Patch(color=colors["反例（故意做错）"], label="反例：不滞后 / 居中窗口 / 错口径")],
          loc="upper right", fontsize=8.5)
plot.save(fig, "L01_04_leakage_audit",
          note="数据：spy_monthly_features_240m.csv 对照 market_index_prices/returns_240m.csv（US_SPY）与 macro_240m.csv · 2006-06 价格由收益表首行反推 · 前 12 行未审计")
