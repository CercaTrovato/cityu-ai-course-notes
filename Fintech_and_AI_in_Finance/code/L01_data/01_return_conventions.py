"""
L01_01 · 简单收益 vs 对数收益：同一份数据两种口径差多少
=========================================================
目的      讲义 Lec01 p.19 只给了简单收益公式 P_t/P_{t-1} − 1，但月频 csv 里存的全是对数收益。
          本脚本用同一份 S&P 500 数据算三条净值曲线，量化"用错口径会差多少"。
讲义      Lec01 p.19（公式）、p.20–21（图注里才出现 "log returns"）
笔记      [[M01-金融数据与Vibe-Coding]] §2.3.1、§9.3
输入      market_index_prices_240m.csv（价格）、market_index_returns_240m.csv（对数收益）
输出      output/L01_01_return_conventions.png · output/L01_01_return_conventions.csv
关键决定  · ⚠️ 收益文件首行是真实收益（非 NaN），须置 0 作基期才能与价格净值对齐
          · 三条曲线：① 价格直接算的真实净值 P_t/P_0（基准真相）
                      ② 对数收益按正确方式累加再取 exp —— 应与 ① 完全重合
                      ③ 把对数收益**误当简单收益**逐月复利 ∏(1+r) —— 讲义公式套错数据的后果
          · 起点 2006-07-31 = 1.0；用 US_S&P500（价格指数，不含股息）
          · 差异用"终点倍数"和"最大偏离百分点"两种方式报，前者好记，后者说明差异是累积的
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))   # 让 common 可导入，脚本从哪启动都能跑

import numpy as np
import pandas as pd

from common import load, plot

# ---------- 1. 读数据 ----------
prices = load.index_prices()["US_S&P500"]
logret = load.index_returns()["US_S&P500"].copy()
# ⚠️ 收益文件首行不是 NaN：它是 2006-06→2006-07 的真实收益（用了价格文件里没有的 2006-06 价格）。
#    要与"价格净值 P_t/P_{2006-07}"对齐，第 0 行必须置 0 作为基期。见 common.load.index_returns 的说明。
logret.iloc[0] = 0.0

# ---------- 2. 三条净值曲线（都从 2006-07 = 1.0 起算） ----------
truth = prices / prices.iloc[0]                       # ① 真实净值
correct = np.exp(logret.cumsum())                     # ② 对数收益的正确用法：累加后取 exp
wrong = (1 + logret).cumprod()                        # ③ 把对数收益当简单收益复利 —— 错误用法

# 口径自检：② 必须与 ① 重合
assert np.allclose(truth.values, correct.values, rtol=1e-10), "对数收益累加与价格净值不一致——数据口径与假设不符"

# ---------- 3. 关键数字 ----------
end_truth, end_wrong = truth.iloc[-1], wrong.iloc[-1]
gap_pct = (wrong / truth - 1) * 100                   # 每月的相对偏离（百分点）
worst_month = gap_pct.idxmin()
summary = pd.DataFrame({
    "真实净值(价格)": truth, "对数收益正确累加": correct, "误当简单收益复利": wrong, "偏离%": gap_pct
})
summary.to_csv(load.OUTPUT_DIR / "L01_01_return_conventions.csv", encoding="utf-8-sig")

print("=" * 60)
print("S&P 500 价格指数  2006-07-31 → 2026-06-30（240 个月）")
print(f"  真实累计倍数（价格 P_T/P_0）         : {end_truth:.2f}×")
print(f"  对数收益正确累加 exp(Σr)             : {correct.iloc[-1]:.2f}×   ← 与真实重合 ✅")
print(f"  误当简单收益复利 ∏(1+r)              : {end_wrong:.2f}×   ← 讲义 p.19 公式套错数据")
print(f"  终点低估                              : {(1 - end_wrong / end_truth) * 100:.1f}%")
print(f"  最大偏离                              : {gap_pct.min():.1f}%（{worst_month.date()}）")
print(f"  20 年年化（真实）                     : {(end_truth ** (12 / len(prices)) - 1) * 100:.2f}%")
print("=" * 60)
print("为什么错在这里：对数收益 r=ln(P_t/P_{t-1}) 满足 Σr = ln(P_T/P_0)，")
print("  所以正确做法是 exp(Σr)；而 ∏(1+r) 是简单收益的复利公式，")
print("  两者在 |r| 小时接近（ln(1+x)≈x），但 240 个月累积后差 %.0f 个百分点。" % (gap_pct.min()))

# ---------- 4. 画图 ----------
fig, ax = plot.setup(figsize=(11, 5.5))
ax.plot(truth.index, truth, color=plot.COLORS["actual"], lw=2.2, label="真实净值  P_t / P_0")
ax.plot(correct.index, correct, color=plot.COLORS["log"], lw=1.2, ls="--", label="对数收益正确累加  exp(Σr)  ← 与真实重合")
ax.plot(wrong.index, wrong, color=plot.COLORS["simple"], lw=2, label="⚠️ 对数收益误当简单收益复利  ∏(1+r)")
ax.axhline(1, color="#999", lw=0.8)
ax.set_title("同一份 S&P 500 月度数据，两种收益口径的累计净值差多少", fontsize=13)
ax.set_ylabel("净值（2006-07 = 1.0）")
ax.set_xlabel("")
ax.legend(loc="upper left", fontsize=9)
ax.annotate(f"{end_truth:.2f}×", xy=(truth.index[-1], end_truth), xytext=(-40, 8), textcoords="offset points",
            fontsize=10, color=plot.COLORS["actual"], fontweight="bold")
ax.annotate(f"{end_wrong:.2f}×", xy=(wrong.index[-1], end_wrong), xytext=(-40, -16), textcoords="offset points",
            fontsize=10, color=plot.COLORS["simple"], fontweight="bold")
plot.save(fig, "L01_01_return_conventions",
          note="数据：market_index_prices_240m.csv / market_index_returns_240m.csv（US_S&P500，价格指数不含股息）· 对数收益口径 · 无交易成本")
