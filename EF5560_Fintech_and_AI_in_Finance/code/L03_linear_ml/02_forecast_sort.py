"""
L03_02 · 预测精度 vs 排序：六个线性模型的 OOS R² 与按预测分五组的实现收益
=======================================================================
目的      把讲义 p.47（OOS R² 对零）与 p.55（Ridge 五分组价差）画在同一张图上，让"MSE 看水平、分组看次序"一眼可见：
          左图六个模型的 OOS R² 都在 ±0.6% 内；右图四个可排序模型的五组均值都从负到正单调上升，
          常数预测（LASSO / Elastic Net）在右图没有线——它们排不了序。
讲义      Lec03 p.47–48、p.51、p.53–55
笔记      [[M03-线性机器学习与收益预测]] §2.8.1、§2.8.4、§2.9.1–2.9.3
输入      class03/stock_linear_test_predictions.csv · stock_linear_forecast_spreads.csv（经 common.load）
输出      output/L03_02_forecast_sort.png · output/L03_02_forecast_sort.csv（各模型五组均值 + 价差 + t）
关键决定  · 分组：每个测试周内按该模型预测 rank(method="first") 后 qcut(5)；等权
          · 常数预测模型不画分组线，只在图注说明（与讲义 p.51 "no stock ranking" 一致）
          · 全部数字与 spreads 表逐格对照，差异应 < 0.001 个百分点
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from common import load, plot

sp = load.c03_stock_predictions()
assert len(sp) == 4108, f"stock_linear_test_predictions.csv 只有 {len(sp)} 行（manifest 4,108 行）——本地文件已截断，请从 Canvas 重新下载 class03.zip"  # ASSERT_4108 2026-09-21
fs = load.c03_stock_spreads().set_index("model")
models = ["OLS", "Ridge", "LASSO", "Elastic Net", "PCR", "PLS"]
sse0 = (sp.actual ** 2).sum()
oos = {m: 100 * (1 - ((sp.actual - sp[m]) ** 2).sum() / sse0) for m in models}

rows = []
curves = {}
for m in models:
    if sp[m].nunique() == 1:
        rows.append(dict(model=m, oos_r2_pct=round(oos[m], 3), sortable=False))
        continue
    d = sp.copy()
    d["q"] = d.groupby("forecast_week")[m].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False) + 1)
    wkm = d.groupby(["forecast_week", "q"]).actual.mean().unstack()
    spread = wkm[5] - wkm[1]
    t = spread.mean() / spread.std() * np.sqrt(len(spread))
    means = (wkm.mean() * 100)
    curves[m] = means
    rows.append(dict(model=m, oos_r2_pct=round(oos[m], 3), sortable=True,
                     **{f"Q{k}": round(means[k], 3) for k in range(1, 6)},
                     spread_pct=round(spread.mean() * 100, 3), t=round(t, 2),
                     spread_ref_pct=round(fs.loc[m, "mean_weekly_spread"] * 100, 3), t_ref=round(fs.loc[m, "t_statistic"], 2)))
tab = pd.DataFrame(rows)
print(tab.to_string(index=False))

fig, ax = plot.setup(figsize=(11, 4.6))
fig.clf()
ax1, ax2 = fig.subplots(1, 2)
colors = {"OLS": "#7f7f7f", "Ridge": "#1f77b4", "LASSO": "#d62728", "Elastic Net": "#ff7f0e", "PCR": "#2ca02c", "PLS": "#9467bd"}
ax1.bar(models, [oos[m] for m in models], color=[colors[m] for m in models])
ax1.axhline(0, color="k", lw=0.8)
ax1.set_title("测试 OOS R²（对零超额收益，4,108 股-周）")
ax1.set_ylabel("%")
for i, m in enumerate(models):
    ax1.text(i, max(oos[m], 0) + 0.02, f"{oos[m]:+.2f}%", ha="center", fontsize=8)
for m, means in curves.items():
    ax2.plot(range(1, 6), means.values, marker="o", label=f"{m}（Q5−Q1 {tab.set_index('model').loc[m, 'spread_pct']:+.2f}%，t {tab.set_index('model').loc[m, 't']:.2f}）", color=colors[m])
ax2.axhline(0, color="k", lw=0.8)
ax2.set_xticks(range(1, 6)); ax2.set_xlabel("预测五分组（1 = 预测最低，5 = 最高）"); ax2.set_ylabel("平均周超额收益 %")
ax2.set_title("按预测分五组后的实现收益（52 周均值）")
ax2.legend(fontsize=7)
plot.save(fig, "L03_02_forecast_sort", note="数据：class03/stock_linear_test_predictions.csv；LASSO / Elastic Net 为常数预测，无法分组（讲义 p.51）；未扣交易成本")
tab.to_csv(load.OUTPUT_DIR / "L03_02_forecast_sort.csv", index=False)
print(f"[saved] {load.OUTPUT_DIR / 'L03_02_forecast_sort.csv'}")
