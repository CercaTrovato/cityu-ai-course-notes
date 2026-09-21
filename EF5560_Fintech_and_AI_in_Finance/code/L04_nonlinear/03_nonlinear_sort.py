"""
L04_03 · 线性 vs 非线性：市场 OOS R² 对照、美国测试期预测曲线、个股五分组曲线、随机森林特征重要性
==========================================================================================
目的      把讲义 p.36 / p.38 / p.48 四块信息画成两张图：
          图 1（市场）：三个市场 × {OLS, LASSO, Elastic Net, 决策树, 随机森林, 梯度提升} 的测试 OOS R²（对 MA(12)）柱状 + 美国测试期实现 vs 梯度提升预测
          图 2（个股）：三族非线性模型的 OOS R²（对零）+ 按预测分五组的实现周超额收益曲线 + 随机森林置换重要性前 15
讲义      Lec04 p.36、p.38、p.47–48、p.50–51
笔记      [[M04-非线性机器学习与收益预测]] §2.5.2、§2.8.2、§2.9.1–2.9.3
输入      class04/market_nonlinear_test_predictions.csv · stock_nonlinear_test_predictions.csv · stock_nonlinear_feature_importance.csv ·
          class03/market_linear_model_summary.csv（线性列）（经 common.load）
输出      output/L04_03_market.png · output/L04_03_stock.png · output/L04_03_nonlinear_sort.csv（各模型五组均值 + 价差 + t）
关键决定  · 分组：每个测试周内按该模型预测 rank(method="first") 后 qcut(5)；等权；与 L03_02 / L04_01 一致
          · 市场图截去 CSI 300 的 OLS / 决策树（−148% / −176%），用文字标注，否则其他柱子看不见
          · 重要性 ×1e6 显示（表里是测试 MSE 的增量，小数）
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from common import load, plot

def oos(a, p, b): return 100 * (1 - ((a - p) ** 2).sum() / ((a - b) ** 2).sum())

# ---------------------------------------------------------------- 图 1 市场
mp = load.c04_market_predictions(); c03 = load.c03_market_summary(); c04 = load.c04_market_summary()
markets = ['U.S.', 'HKSAR', 'Chinese Mainland']
lin = {m: {mk: 100 * float(c03[(c03.market == mk) & (c03.model == m)].oos_r2.iloc[0]) for mk in markets} for m in ['OLS', 'LASSO', 'Elastic Net']}
non = {m: {mk: 100 * float(c04[(c04.market == mk) & (c04.model == m)].oos_r2.iloc[0]) for mk in markets} for m in ['Decision tree', 'Random forest', 'Gradient boosting']}
allm = {**lin, **non}
plot.setup(); plt.close('all')
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5))
w = 0.13; x = np.arange(3)
for i, (m, d) in enumerate(allm.items()):
    vals = [max(d[mk], -45) for mk in markets]
    bars = a1.bar(x + (i - 2.5) * w, vals, w, label=m)
    for j, mk in enumerate(markets):
        if d[mk] < -45: a1.text(x[j] + (i - 2.5) * w, -44, f'{d[mk]:.0f}%', rotation=90, ha='center', va='bottom', fontsize=7, color='white')
a1.axhline(0, color='k', lw=0.8); a1.set_xticks(x); a1.set_xticklabels(['美国', '香港', '中国内地'])
a1.set_ylabel('测试 OOS R²（对滞后 MA(12)，%）'); a1.set_title('六个模型 × 三个市场（2021-07 → 2026-06，60 个月）'); a1.legend(fontsize=7, ncol=2)
a1.set_ylim(-46, 12)
us = mp[mp.market == 'U.S.']
a2.plot(us.forecast_month, 100 * us.actual, color=plot.COLORS['actual'], lw=0.9, label='实现超额收益')
a2.plot(us.forecast_month, 100 * us['Gradient boosting'], color=plot.COLORS['fitted'], lw=1.6, label=f'梯度提升预测（OOS R² {non["Gradient boosting"]["U.S."]:+.1f}%）')
a2.plot(us.forecast_month, 100 * us['MA(12)'], color=plot.COLORS['baseline'], lw=1.2, ls='--', label='MA(12) 基准')
a2.axhline(0, color='k', lw=0.6); a2.set_ylabel('月度超额收益（%）'); a2.set_title('美国：验证选中的梯度提升 vs 实现'); a2.legend(fontsize=8)
fig.suptitle('市场任务：多一层灵活性并没有让三个市场都变好（讲义 p.36 / p.38）', fontsize=11)
plot.save(fig, 'L04_03_market')

# ---------------------------------------------------------------- 图 2 个股
sp = load.c04_stock_predictions(); fs = load.c04_stock_spreads().set_index('model'); imp = load.c04_stock_importance()
models = ['Decision tree', 'Random forest', 'Gradient boosting']; zh = {'Decision tree': '决策树', 'Random forest': '随机森林', 'Gradient boosting': '梯度提升'}
rows = []; curves = {}
for m in models:
    d = sp.copy(); d['q'] = d.groupby('forecast_week')[m].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False) + 1)
    wk = d.groupby(['forecast_week', 'q']).actual.mean().unstack(); spread = wk[5] - wk[1]
    t = spread.mean() / spread.std(ddof=1) * np.sqrt(len(spread)); curves[m] = wk.mean() * 100
    rows.append(dict(model=m, oos_r2_pct=round(oos(sp.actual, sp[m], sp['Zero']), 3), n_unique_pred=int(sp[m].nunique()),
                     **{f'q{q}': round(100 * wk[q].mean(), 3) for q in range(1, 6)}, spread_pct=round(100 * spread.mean(), 3), t=round(t, 2),
                     spread_table=round(100 * fs.loc[m, 'mean_weekly_spread'], 3), t_table=round(fs.loc[m, 't_statistic'], 2)))
out = pd.DataFrame(rows); out.to_csv(load.OUTPUT_DIR / 'L04_03_nonlinear_sort.csv', index=False, encoding='utf-8-sig')
print(out.to_string(index=False))
fig, (b1, b2, b3) = plt.subplots(1, 3, figsize=(15, 4.8))
b1.bar([zh[m] for m in models], out.oos_r2_pct, color=['#7f7f7f', '#1f77b4', '#2ca02c']); b1.axhline(0, color='k', lw=0.8)
for i, v in enumerate(out.oos_r2_pct): b1.text(i, v + (0.005 if v >= 0 else -0.02), f'{v:+.3f}%', ha='center', fontsize=9)
b1.set_ylabel('测试 OOS R²（对零，%）'); b1.set_title('预测精度：三族都在 ±0.15% 内'); b1.set_ylim(-0.2, 0.1)
for m, c in zip(models, ['#7f7f7f', '#1f77b4', '#2ca02c']):
    b2.plot(range(1, 6), curves[m].values, marker='o', color=c, label=f'{zh[m]}（Q5−Q1 {out.set_index("model").loc[m, "spread_pct"]:+.2f}%，t {out.set_index("model").loc[m, "t"]:.2f}）')
b2.axhline(0, color='k', lw=0.6); b2.set_xticks(range(1, 6)); b2.set_xlabel('按预测分组：低 → 高'); b2.set_ylabel('组内均值周超额收益（%）')
b2.set_title('排序：森林 / 提升的 Q5 > Q1，但 t < 1.1'); b2.legend(fontsize=7)
top = imp.sort_values('permutation_importance', ascending=True).tail(15)
b3.barh(top.feature.str.replace('_rank', ''), top.permutation_importance * 1e6, color='#1f77b4')
b3.set_xlabel('置换重要性（测试 MSE 增量 ×1e6）'); b3.set_title('随机森林：dolvol_trend 一枝独秀，10 个特征 ≤ 0')
fig.suptitle('个股任务：精度几乎为零、排序略有信号、重要性集中在成交额趋势（讲义 p.47–51）', fontsize=11)
fig.tight_layout()
plot.save(fig, 'L04_03_stock')
print('两张图已写出：L04_03_market.png · L04_03_stock.png')
