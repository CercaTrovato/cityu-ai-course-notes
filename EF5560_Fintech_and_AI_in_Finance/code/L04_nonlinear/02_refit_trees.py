"""
L04_02 · 用共享面板把讲义的树重新长一遍：阈值、叶子、验证 MSE、测试 OOS R² 能否复现
==========================================================================================
目的      讲义 p.8/9/10/43/44 只给了"拟合好的树长什么样"；本脚本按 class04 汇总表里记录的设置（深度 / 最小叶大小 / 学习率 / 树数），
          在 development 行上拟合 → 算 validation MSE（对照汇总表）→ 在 development+validation 行上重拟合 → 读根节点阈值与叶子（对照讲义）
          → 在 test 行上算 OOS R²（对照汇总表）。树是确定性算法，应逐位对上；森林 / 提升有随机数与实现差异，只能近似。
讲义      Lec04 p.6、p.8–10、p.21–22、p.36、p.43–45、p.47
笔记      [[M04-非线性机器学习与收益预测]] §2.2.3、§2.3.1–2.3.2、§2.5.2、§2.7.1–2.7.3、§2.8.1
输入      class04/market_excess_return_panel.csv · hsi_stock_excess_return_panel.csv · 两张汇总表（经 common.load）
输出      stdout · output/L04_02_refit_trees.csv（每个市场 / 面板 × 模型：验证 MSE 与测试 OOS R² 的重算值 vs 表值）
关键决定  · sklearn DecisionTreeRegressor(criterion="squared_error")，阈值取相邻观测中点，与讲义 p.6 的最小化式一致
          · 市场任务：三个市场各自拟合（预测变量相同，目标不同）；基准 MA(12) 超额收益；OOS R² = 1 − SSE_model / SSE_MA12
          · 股票任务：只用 12,281 个完整行；随机森林 max_features=5（⌊√30⌋，p.21）、验证期 300 棵、重拟合 500 棵；random_state=0
          · 提升：sklearn GradientBoostingRegressor(learning_rate, n_estimators, max_depth, min_samples_leaf)，无子采样
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor, export_text
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from common import load

def h(s): print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)
def oos(a, p, b): return 100 * (1 - ((a - p) ** 2).sum() / ((a - b) ** 2).sum())
rows = []

# ---------------------------------------------------------------- 市场任务
h("1. 市场任务：三个市场 × {树, 森林, 提升}，按汇总表的设置重拟合")
mp = load.c04_market_panel(); ms = load.c04_market_summary()
X = ['term_spread_lag1', 'fed_funds_lag1', 'unemployment_lag2', 'inflation_lag2']
for lab in ['U.S.', 'HKSAR', 'Chinese Mainland']:
    g = mp[mp.market_label == lab.replace('Chinese Mainland', 'Chinese mainland')]
    dev, val, tst = (g[g.split == s] for s in ['development', 'validation', 'test'])
    pre = pd.concat([dev, val])
    for model in ['Decision tree', 'Random forest', 'Gradient boosting']:
        r = ms[(ms.market == lab) & (ms.model == model)].iloc[0]
        d, leaf = int(r.max_depth), int(r.min_samples_leaf)
        def make(n_est):
            if model == 'Decision tree': return DecisionTreeRegressor(max_depth=d, min_samples_leaf=leaf, random_state=0)
            if model == 'Random forest': return RandomForestRegressor(n_estimators=n_est, max_depth=d, min_samples_leaf=leaf, max_features=2, random_state=0, n_jobs=-1)
            return GradientBoostingRegressor(learning_rate=float(r.learning_rate), n_estimators=200, max_depth=d, min_samples_leaf=leaf, random_state=0)
        m = make(300).fit(dev[X], dev.market_excess_return)
        vmse = 1e4 * ((val.market_excess_return - m.predict(val[X])) ** 2).mean()
        m2 = make(500).fit(pre[X], pre.market_excess_return)
        r2 = oos(tst.market_excess_return, m2.predict(tst[X]), tst.benchmark_ma12_excess_return)
        rows.append(dict(task='market', group=lab, model=model, val_mse_x1e4=round(vmse, 2), val_table=round(1e4 * r.validation_mse, 2), oos_pct=round(r2, 1), oos_table=round(100 * r.oos_r2, 1)))
        print(f"  {lab:17s} {model:18s} depth {d} leaf {leaf:2d}  验证 MSE 重算 {vmse:.2f} / 表 {1e4*r.validation_mse:.2f}   测试 OOS R² 重算 {r2:+.1f}% / 表 {100*r.oos_r2:+.1f}%")
        if model == 'Decision tree':
            print("     重拟合（178 个月）的树：")
            for line in export_text(m2, feature_names=X, decimals=3).splitlines(): print("       " + line)
            n = m2.tree_.n_node_samples; v = m2.tree_.value.ravel()
            print(f"     根节点：{X[m2.tree_.feature[0]]} ≤ {m2.tree_.threshold[0]:.3f}；左子 {n[1]} 个月 均值 {100*v[1]:+.1f}% ({100*n[1]/n[0]:.1f}%)；右子 {n[m2.tree_.children_right[0]]} 个月 均值 {100*v[m2.tree_.children_right[0]]:+.1f}%")

# ---------------------------------------------------------------- 股票任务
h("2. 个股任务：恒指周度面板 × {树, 森林, 提升}")
sp = load.c04_stock_panel(); ss = load.c04_stock_summary()
rank_cols = [c for c in sp.columns if c.endswith('_rank')]
u = sp.dropna(subset=['excess_return'] + rank_cols)
dev, val, tst = (u[u.split == s] for s in ['development', 'validation', 'test'])
pre = pd.concat([dev, val])
print(f"  行数：development {len(dev)} / validation {len(val)} / test {len(tst)}；特征 {len(rank_cols)} 个 rank 列")
for model in ['Decision tree', 'Random forest', 'Gradient boosting']:
    r = ss[ss.model == model].iloc[0]; d, leaf = int(r.max_depth), int(r.min_samples_leaf)
    def make(n_est):
        if model == 'Decision tree': return DecisionTreeRegressor(max_depth=d, min_samples_leaf=leaf, random_state=0)
        if model == 'Random forest': return RandomForestRegressor(n_estimators=n_est, max_depth=d, min_samples_leaf=leaf, max_features=5, random_state=0, n_jobs=-1)
        return GradientBoostingRegressor(learning_rate=float(r.learning_rate), n_estimators=150, max_depth=d, min_samples_leaf=leaf, random_state=0)
    m = make(300).fit(dev[rank_cols], dev.excess_return)
    vmse = 1e4 * ((val.excess_return - m.predict(val[rank_cols])) ** 2).mean()
    m2 = make(500).fit(pre[rank_cols], pre.excess_return)
    pred = m2.predict(tst[rank_cols]); r2 = oos(tst.excess_return, pred, 0 * tst.excess_return)
    rows.append(dict(task='stock', group='HSI', model=model, val_mse_x1e4=round(vmse, 2), val_table=round(1e4 * r.validation_mse, 2), oos_pct=round(r2, 3), oos_table=round(100 * r.oos_r2, 3)))
    print(f"  {model:18s} depth {d} leaf {leaf:3d}  验证 MSE 重算 {vmse:.2f} / 表 {1e4*r.validation_mse:.2f}   测试 OOS R² 重算 {r2:+.3f}% / 表 {100*r.oos_r2:+.3f}%   测试 MSE ×1e4 {1e4*((tst.excess_return-pred)**2).mean():.2f}")
    if model == 'Decision tree':
        t_ = m2.tree_; n = t_.n_node_samples; v = t_.value.ravel()
        print(f"     重拟合（8,173 行）树桩：{rank_cols[t_.feature[0]]} ≤ {t_.threshold[0]:.4f}；左 {100*n[1]/n[0]:.1f}% 行 均值 {100*v[1]:+.2f}%；右 {100*n[2]/n[0]:.1f}% 行 均值 {100*v[2]:+.2f}%")
        wk = pre.assign(side=pre.dolvol_trend_rank > t_.threshold[0]).groupby('side').forecast_week.nunique()
        print(f"     两片叶子各自覆盖的周数：≤ 阈值 {wk[False]} 周，> 阈值 {wk[True]} 周（共 {pre.forecast_week.nunique()} 周）——p.42 说的'数支持规则的独立周数'")

out = pd.DataFrame(rows); out.to_csv(load.OUTPUT_DIR / 'L04_02_refit_trees.csv', index=False, encoding='utf-8-sig')
tree_ok = out[out.model == 'Decision tree']
print("\n决策树（确定性）全部逐位对上？", bool(((tree_ok.val_mse_x1e4 - tree_ok.val_table).abs() < 0.02).all() and ((tree_ok.oos_pct - tree_ok.oos_table).abs() < 0.2).all()))
print("写出", load.OUTPUT_DIR / 'L04_02_refit_trees.csv')
