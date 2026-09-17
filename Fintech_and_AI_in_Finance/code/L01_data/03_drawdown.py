"""
L01_03 · PDD-JD 配对交易的完整路径：终点 +20.62% 的路上跌了多少
=================================================================
目的      讲义 p.16 只报了终点 +20.62%。本脚本画出全程净值与回撤，回答"路径长什么样"：
          最大回撤 −38.66%（峰 2024-01-19 → 谷 2025-04-11），至 2026-06 仍未收复（终点仍在 −32% 的回撤里）。
讲义      Lec01 p.15（权重与收益公式）、p.16（历史结果 +20.6%）
笔记      [[M01-金融数据与Vibe-Coding]] §2.10.2、§2.10.3
输入      pdd_jd_pair_example_156w.csv（周频，**简单收益**；权重恒为 +0.5 / −0.5，每周五再平衡）
输出      output/L01_03_drawdown.png · output/L01_03_drawdown.csv
关键决定  · 净值直接用文件的 long_pdd_short_jd_wealth（起点 100），并用 ∏(1+r) 从组合周收益重算一遍做口径自检
          · 组合周收益按讲义 p.15 的公式 0.5·r_PDD − 0.5·r_JD 复核（简单收益可跨资产相加，对数收益不行）
          · 回撤 = 当前净值 / 历史最高净值 − 1，按周五收盘净值算；周内的真实回撤只会更深
          · 最大回撤的"峰"取谷底之前的历史最高点；"收复"= 净值回到峰值以上
          · 不含股息、交易成本、融券费、融资成本（讲义 p.16 图注已声明）
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))   # 让 common 可导入，脚本从哪启动都能跑

import numpy as np
import pandas as pd
import matplotlib.dates as mdates

from common import load, plot

# ---------- 1. 读数据 ----------
d = load.pdd_jd_pair()
wealth = d["long_pdd_short_jd_wealth"]
r_ls = d["long_pdd_short_jd_return"]

# 口径自检 ①：组合收益 = 0.5·r_PDD − 0.5·r_JD（讲义 p.15）
formula = 0.5 * d["pdd_return"] - 0.5 * d["jd_return"]
assert np.nanmax(np.abs(formula - r_ls)) < 1e-12, "组合周收益与讲义 p.15 公式不符"
# 口径自检 ②：权重恒为 ±0.5（每周再平衡回等额美元）
assert (d["pdd_weight"] == 0.5).all() and (d["jd_weight"] == -0.5).all()
# 口径自检 ③：净值 = 100·∏(1+r)，说明 r 是**简单收益**（对数收益应当用 exp(Σr)）
rebuilt = 100 * (1 + r_ls.fillna(0)).cumprod()
assert np.allclose(rebuilt, wealth, atol=1e-9), "净值不是简单收益的复利——口径与假设不符"
assert wealth.iloc[0] == 100 and len(d) == 157 and r_ls.isna().sum() == 1, "应为 157 行、首行收益缺失、净值从 100 起"

# ---------- 2. 回撤 ----------
peak_so_far = wealth.cummax()
dd = wealth / peak_so_far - 1
trough = dd.idxmin()
peak = wealth.loc[:trough].idxmax()
recovered = wealth.loc[trough:][wealth.loc[trough:] >= wealth[peak]]
recover_date = recovered.index[0] if len(recovered) else None
weeks_peak_to_trough = int(((d.index > peak) & (d.index <= trough)).sum())
weeks_under_water = int((dd < 0).sum())
weeks_below_20 = int((dd <= -0.20).sum())

total_return = wealth.iloc[-1] / wealth.iloc[0] - 1
n_weeks = int(r_ls.notna().sum())
ann_vol = r_ls.std(ddof=1) * np.sqrt(52)
ann_ret = (wealth.iloc[-1] / wealth.iloc[0]) ** (52 / n_weeks) - 1

# 数值自检：终点必须等于讲义 p.16 的 +20.62%（讲义写 +20.6%）
assert abs(total_return - 0.2062) < 5e-5, f"终点收益 {total_return:.4%} ≠ 讲义 +20.62%"
assert abs(dd.min() - (-0.3866)) < 5e-5 and trough.strftime("%Y-%m-%d") == "2025-04-11"

out = pd.DataFrame({"净值": wealth, "历史最高": peak_so_far, "回撤": dd, "组合周收益": r_ls,
                    "PDD归一化": d["pdd_close"] / d["pdd_close"].iloc[0] * 100,
                    "JD归一化": d["jd_close"] / d["jd_close"].iloc[0] * 100})
out.to_csv(load.OUTPUT_DIR / "L01_03_drawdown.csv", encoding="utf-8-sig", float_format="%.6f")

print("=" * 70)
print("PDD-JD 美元中性配对（多 PDD 0.5 / 空 JD 0.5，每周五再平衡）  2023-06-30 → 2026-06-26")
print(f"  周数                    : {n_weeks} 个周收益（157 个周五价格）")
print(f"  终点净值                : {wealth.iloc[-1]:.2f}（起点 100）→ 累计 {total_return*100:+.2f}%   ← 讲义 p.16 只报了这个数")
print(f"  归一化终值              : PDD {out['PDD归一化'].iloc[-1]:.1f} / JD {out['JD归一化'].iloc[-1]:.1f}（讲义 p.11：110.7 / 74.4）")
print(f"  年化收益 / 年化波动     : {ann_ret*100:.1f}% / {ann_vol*100:.1f}%")
print(f"  最大回撤                : {dd.min()*100:.2f}%   ← 讲义没报")
print(f"    峰                    : {peak.date()}  净值 {wealth[peak]:.2f}（全程最高）")
print(f"    谷                    : {trough.date()}  净值 {wealth[trough]:.2f}（峰后 {weeks_peak_to_trough} 周）")
print(f"    是否收复              : {'是，' + str(recover_date.date()) if recover_date is not None else '否——至 2026-06-26 终点仍在回撤 ' + f'{dd.iloc[-1]*100:.1f}%'}")
print(f"  处于回撤中的周数        : {weeks_under_water}/{len(dd)}；回撤 ≤ −20% 的周数：{weeks_below_20}")
worst = r_ls.idxmin(); best = r_ls.idxmax()
print(f"  最差 / 最好单周         : {r_ls.min()*100:.2f}%（{worst.date()}） / {r_ls.max()*100:+.2f}%（{best.date()}）")
w0924 = d.loc["2024-09-27"]
print(f"  2024-09-27 那周         : PDD {w0924['pdd_return']*100:+.1f}%、JD {w0924['jd_return']*100:+.1f}% 同涨，"
      f"组合 {w0924['long_pdd_short_jd_return']*100:+.1f}% —— 美元中性 ≠ 风险中性")
print("=" * 70)

# ---------- 3. 画图：上净值 + 峰谷标注，下回撤 ----------
fig, ax0 = plot.setup(figsize=(11, 8))
ax0.remove()
ax_w, ax_dd = fig.subplots(2, 1, sharex=True, gridspec_kw={"height_ratios": [1.5, 1]})

ax_w.plot(out.index, out["PDD归一化"], color=plot.COLORS["PDD"], lw=1.0, alpha=0.6, label=f"PDD 归一化价  终点 {out['PDD归一化'].iloc[-1]:.1f}")
ax_w.plot(out.index, out["JD归一化"], color=plot.COLORS["JD"], lw=1.0, alpha=0.6, label=f"JD 归一化价  终点 {out['JD归一化'].iloc[-1]:.1f}")
ax_w.plot(wealth.index, wealth, color=plot.COLORS["pair"], lw=2.2, label=f"多 PDD / 空 JD 组合净值  终点 {wealth.iloc[-1]:.2f}（{total_return*100:+.2f}%）")
ax_w.plot(peak_so_far.index, peak_so_far, color=plot.COLORS["pair"], lw=0.8, ls=":", alpha=0.6, label="历史最高净值")
ax_w.axhline(100, color="#999", lw=0.8)
ax_w.scatter([peak, trough], [wealth[peak], wealth[trough]], color=plot.COLORS["fitted"], zorder=5, s=36)
ax_w.annotate(f"峰 {peak.date()}\n{wealth[peak]:.2f}", xy=(peak, wealth[peak]), xytext=(10, 6), textcoords="offset points",
              fontsize=9, color=plot.COLORS["fitted"], fontweight="bold")
ax_w.annotate(f"谷 {trough.date()}\n{wealth[trough]:.2f}（较峰 {dd.min()*100:.2f}%）", xy=(trough, wealth[trough]), xytext=(-150, -34),
              textcoords="offset points", fontsize=9, color=plot.COLORS["fitted"], fontweight="bold",
              arrowprops=dict(arrowstyle="-", color=plot.COLORS["fitted"], lw=0.8))
ax_w.annotate(f"{wealth.iloc[-1]:.2f}", xy=(wealth.index[-1], wealth.iloc[-1]), xytext=(6, -4), textcoords="offset points",
              fontsize=10, color=plot.COLORS["pair"], fontweight="bold")
ax_w.set_ylabel("净值（2023-06-30 = 100）")
ax_w.set_title("PDD-JD 美元中性配对：讲义只报了终点 +20.62%，路径里有一段 −38.66% 的回撤", fontsize=12.5)
ax_w.legend(loc="upper left", fontsize=8.5)

ax_dd.fill_between(dd.index, dd * 100, 0, color=plot.COLORS["fitted"], alpha=0.25)
ax_dd.plot(dd.index, dd * 100, color=plot.COLORS["fitted"], lw=1.2)
ax_dd.axhline(0, color="#999", lw=0.8)
ax_dd.axvline(trough, color=plot.COLORS["fitted"], lw=0.8, ls="--")
ax_dd.annotate(f"最大回撤 {dd.min()*100:.2f}%\n{trough.date()}", xy=(trough, dd.min() * 100), xytext=(12, -2), textcoords="offset points",
               fontsize=9.5, color=plot.COLORS["fitted"], fontweight="bold")
ax_dd.annotate(f"终点仍在回撤 {dd.iloc[-1]*100:.1f}%\n（高点未收复）", xy=(dd.index[-1], dd.iloc[-1] * 100), xytext=(-150, 60),
               textcoords="offset points", fontsize=8.5, color=plot.COLORS["actual"],
               arrowprops=dict(arrowstyle="-", color=plot.COLORS["actual"], lw=0.8))
ax_dd.set_ylabel("回撤（相对历史最高净值，%）")
ax_dd.set_ylim(-45, 3)
ax_dd.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
ax_dd.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

plot.save(fig, "L01_03_drawdown",
          note="数据：pdd_jd_pair_example_156w.csv（周五收盘，简单收益，权重 +0.5/−0.5 每周再平衡）· 回撤按周五净值计 · 不含股息、交易成本、融券费、融资成本")
