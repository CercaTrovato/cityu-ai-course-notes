"""
L01_02 · 四个指数 20 年累计净值与回撤：恒生的高点为什么还没收复
=================================================================
目的      讲义 p.20 只画了三市场归一化价格、p.51 只画了回撤，两张图分开且没给数字。
          本脚本把净值与回撤放在同一张图里，回答三件事：
            ① 20 年终点倍数（S&P500 5.87× / SPY 8.44× / 恒生 1.35× / CSI300 3.85×）——SP500 与 SPY 的差就是股息
            ② 最大回撤有多深、发生在哪个月（CSI300 −70.8% @2008-10，恒生 −59.1%、S&P500 −52.6% @2009-02）
            ③ 谁的历史高点至今没收复：恒生 2018-01 高点差 30%；CSI300 2007-10 高点 19 年未收复（差 12.5%）
讲义      Lec01 p.17–21（下载与归一化价格）、p.51（回撤图）
笔记      [[M01-金融数据与Vibe-Coding]] §2.3.4、§2.9.2
输入      market_index_prices_240m.csv（月末价格）、market_index_returns_240m.csv（对数收益，只用来算年化波动率）
输出      output/L01_02_index_20y.png · output/L01_02_index_20y.csv
关键决定  · 净值 = P_t / P_{2006-07}，起点 1.0；上图用对数坐标，否则 8.44× 的 SPY 会把 1.35× 的恒生压成一条直线
          · 回撤 = 当前净值 / 历史最高净值 − 1，用**月末价**算——日内/日频的真实回撤只会更深
          · "未收复"= 样本终点 2026-06 的价格仍低于历史最高月末价；差距 = P_end / P_peak − 1
          · 年化收益 = 终点倍数^(12/240) − 1（几何年化，简单收益口径）；年化波动 = 对数收益样本标准差 × √12
          · 四个指数口径不同：US_S&P500 / HK_HangSeng / CN_CSI300 是**价格指数**（不含股息），US_SPY 是**含股息**复权价
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))   # 让 common 可导入，脚本从哪启动都能跑

import numpy as np
import pandas as pd
import matplotlib.dates as mdates

from common import load, plot

LABELS = {"US_S&P500": "S&P 500（价格指数）", "US_SPY": "SPY（含股息）",
          "HK_HangSeng": "恒生指数", "CN_CSI300": "沪深 300"}

# ---------- 1. 读数据 ----------
prices = load.index_prices()
logret = load.index_returns()
assert len(prices) == 240 and prices.isna().sum().sum() == 0, "价格表应为 240 行且无缺失（讲义 p.18：missing months zero）"

# ---------- 2. 净值与回撤 ----------
nav = prices / prices.iloc[0]                 # 2006-07 = 1.0
dd = nav / nav.cummax() - 1                   # 相对历史最高净值的回撤（≤ 0）

# 口径自检：回撤必须 ≤ 0，且在创新高的月份恰好为 0
assert (dd <= 1e-12).all().all(), "回撤不能为正"
assert (dd.iloc[0] == 0).all(), "首月净值 = 历史最高，回撤应为 0"
# 口径自检：SPY 含股息，累计一定高于同市场的价格指数
assert nav["US_SPY"].iloc[-1] > nav["US_S&P500"].iloc[-1], "SPY 含股息，20 年累计应高于 S&P 500 价格指数"

# ---------- 3. 关键数字 ----------
rows = []
for c in prices.columns:
    peak_month = prices[c].idxmax()
    trough_month = dd[c].idxmin()
    rows.append({
        "指数": c,
        "终点倍数": nav[c].iloc[-1],
        "年化收益(几何)": nav[c].iloc[-1] ** (12 / len(prices)) - 1,
        "年化波动(对数收益)": logret[c].std(ddof=1) * np.sqrt(12),
        "最大回撤": dd[c].min(),
        "最大回撤月": trough_month.strftime("%Y-%m"),
        "历史最高月": peak_month.strftime("%Y-%m"),
        "终点距高点": prices[c].iloc[-1] / prices[c].max() - 1,
        "高点至今年数": (prices.index[-1] - peak_month).days / 365.25,   # 0 = 终点就是新高
    })
summary = pd.DataFrame(rows).set_index("指数")
summary.to_csv(load.OUTPUT_DIR / "L01_02_index_20y.csv", encoding="utf-8-sig", float_format="%.6f")

dividend_gap = nav["US_SPY"].iloc[-1] - nav["US_S&P500"].iloc[-1]

print("=" * 78)
print("四个指数  2006-07-31 → 2026-06-30（240 个月，起点 = 1.0）")
print("-" * 78)
print(f"{'指数':14s}{'终点倍数':>9s}{'年化收益':>9s}{'年化波动':>9s}{'最大回撤':>9s}{'发生月':>9s}{'历史高点':>9s}{'距高点':>8s}{'高点距今':>9s}")
for c, r in summary.iterrows():
    print(f"{c:14s}{r['终点倍数']:>8.2f}×{r['年化收益(几何)']*100:>8.2f}%{r['年化波动(对数收益)']*100:>8.2f}%"
          f"{r['最大回撤']*100:>8.1f}%{r['最大回撤月']:>9s}{r['历史最高月']:>9s}{r['终点距高点']*100:>7.1f}%{r['高点至今年数']:>7.1f} 年")
print("-" * 78)
print(f"SP500 vs SPY 的差 = 股息：{nav['US_S&P500'].iloc[-1]:.2f}× vs {nav['US_SPY'].iloc[-1]:.2f}×，差 {dividend_gap:.2f}×")
print(f"恒生：历史最高 {summary.loc['HK_HangSeng', '历史最高月']}（{prices['HK_HangSeng'].max():.0f}），"
      f"2026-06 只有 {prices['HK_HangSeng'].iloc[-1]:.0f}，还差 {-summary.loc['HK_HangSeng', '终点距高点']*100:.1f}%"
      f"（{summary.loc['HK_HangSeng', '高点至今年数']:.1f} 年未收复）")
print(f"CSI300：历史最高 {summary.loc['CN_CSI300', '历史最高月']}（{prices['CN_CSI300'].max():.0f}），"
      f"2026-06 只有 {prices['CN_CSI300'].iloc[-1]:.0f}，还差 {-summary.loc['CN_CSI300', '终点距高点']*100:.1f}%"
      f"（{summary.loc['CN_CSI300', '高点至今年数']:.1f} 年未收复）")
print(f"投 100 元的 20 年终值：S&P500 {nav['US_S&P500'].iloc[-1]*100:.0f} / CSI300 {nav['CN_CSI300'].iloc[-1]*100:.0f} / 恒生 {nav['HK_HangSeng'].iloc[-1]*100:.0f}")
print(f"单月最差（对数收益）：" + " / ".join(f"{c} {logret[c].min()*100:.2f}%（{logret[c].idxmin().strftime('%Y-%m')}）" for c in logret.columns))
print(f"⚠️ 年化收益若把对数收益误当简单收益复利再年化，S&P500 会算成 {((1 + logret['US_S&P500']).prod()) ** (12 / 240) * 100 - 100:.2f}%（正确的几何年化是 {summary.loc['US_S&P500', '年化收益(几何)']*100:.2f}%）")
print("=" * 78)

# 数值自检：对准数据集卡片 §4 / §5 的数字
assert abs(nav["US_S&P500"].iloc[-1] - 5.87) < 0.01 and abs(nav["US_SPY"].iloc[-1] - 8.44) < 0.01
assert summary.loc["HK_HangSeng", "历史最高月"] == "2018-01" and summary.loc["CN_CSI300", "历史最高月"] == "2007-10"
assert abs(summary.loc["CN_CSI300", "最大回撤"] - (-0.708)) < 0.001 and summary.loc["CN_CSI300", "最大回撤月"] == "2008-10"
assert abs(summary.loc["HK_HangSeng", "最大回撤"] - (-0.591)) < 0.001 and abs(summary.loc["US_S&P500", "最大回撤"] - (-0.526)) < 0.001
assert summary.loc["HK_HangSeng", "高点至今年数"] > 8 and summary.loc["CN_CSI300", "高点至今年数"] > 18, "恒生 / CSI300 的高点应在多年前且至今未收复"

# ---------- 4. 画图：上净值（对数坐标）、下回撤 ----------
fig, ax0 = plot.setup(figsize=(11, 8.5))
ax0.remove()
ax_nav, ax_dd = fig.subplots(2, 1, sharex=True, gridspec_kw={"height_ratios": [1.6, 1]})

for c in prices.columns:
    ax_nav.plot(nav.index, nav[c], color=plot.COLORS[c], lw=1.6 if c != "US_S&P500" else 2.0,
                ls="--" if c == "US_SPY" else "-", label=f"{LABELS[c]}  {nav[c].iloc[-1]:.2f}×")
    ax_dd.plot(dd.index, dd[c] * 100, color=plot.COLORS[c], lw=1.3, ls="--" if c == "US_SPY" else "-")
    ax_dd.fill_between(dd.index, dd[c] * 100, 0, color=plot.COLORS[c], alpha=0.06)

ax_nav.set_yscale("log")
ax_nav.set_yticks([0.5, 1, 2, 4, 8])
ax_nav.set_yticklabels(["0.5×", "1×", "2×", "4×", "8×"])
ax_nav.axhline(1, color="#999", lw=0.8)
ax_nav.set_ylabel("累计净值（2006-07 = 1，对数坐标）")
ax_nav.set_title("四个指数 20 年：累计净值与回撤（月末价）", fontsize=13)
ax_nav.legend(loc="upper left", fontsize=9, ncol=2)

# 标注两个"未收复"的高点（文字放在空白区，细线指向高点；xytext 用数据坐标）
for c, txt_xy in (("HK_HangSeng", (pd.Timestamp("2012-09-30"), 4.6)), ("CN_CSI300", (pd.Timestamp("2008-03-31"), 6.0))):
    pk = prices[c].idxmax()
    ax_nav.annotate(f"{LABELS[c]}高点 {pk.strftime('%Y-%m')}\n至今未收复，差 {-summary.loc[c, '终点距高点']*100:.0f}%（{summary.loc[c, '高点至今年数']:.0f} 年）",
                    xy=(pk, nav.loc[pk, c]), xytext=txt_xy, textcoords="data", fontsize=8.5,
                    color=plot.COLORS[c], arrowprops=dict(arrowstyle="-", color=plot.COLORS[c], lw=0.8))
ax_nav.annotate(f"SPY − S&P500 = 股息\n{nav['US_SPY'].iloc[-1]:.2f}× vs {nav['US_S&P500'].iloc[-1]:.2f}×",
                xy=(nav.index[-1], nav["US_SPY"].iloc[-1]), xytext=(pd.Timestamp("2020-06-30"), 7.6), textcoords="data",
                fontsize=8.5, color=plot.COLORS["US_SPY"], arrowprops=dict(arrowstyle="-", color=plot.COLORS["US_SPY"], lw=0.8))

ax_dd.set_ylabel("回撤（相对历史最高，%）")
ax_dd.set_ylim(-80, 3)
ax_dd.axhline(0, color="#999", lw=0.8)
for c in ("CN_CSI300", "HK_HangSeng", "US_S&P500"):
    tm = dd[c].idxmin()
    ax_dd.annotate(f"{dd[c].min()*100:.1f}%  {tm.strftime('%Y-%m')}", xy=(tm, dd[c].min() * 100),
                   xytext=(8, -4 if c != "US_S&P500" else 6), textcoords="offset points", fontsize=8.5, color=plot.COLORS[c])
ax_dd.annotate(f"恒生 2026-06 仍处于 {dd['HK_HangSeng'].iloc[-1]*100:.0f}% 的回撤中", xy=(dd.index[-1], dd["HK_HangSeng"].iloc[-1] * 100),
               xytext=(pd.Timestamp("2018-06-30"), -70), textcoords="data", fontsize=8.5, color=plot.COLORS["HK_HangSeng"],
               arrowprops=dict(arrowstyle="-", color=plot.COLORS["HK_HangSeng"], lw=0.8))
ax_dd.xaxis.set_major_locator(mdates.YearLocator(2))
ax_dd.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

plot.save(fig, "L01_02_index_20y",
          note="数据：market_index_prices_240m.csv（月末价；S&P500 / 恒生 / 沪深 300 为价格指数不含股息，SPY 为含股息复权价）· 回撤按月末价计，日频回撤只会更深 · 无交易成本")
