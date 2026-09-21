"""
L04_01 · 讲义 Lec04 的全部数字能否复现：真数（class04 结果表 + 共享面板）+ 假数算例 + 笔记补充的迷你例子
==========================================================================================
目的      笔记 M04 里出现的每一个数字都要能在这里的输出里找到。三组：
          A) 讲义标 "Illustrative" 的假数算例（p.11/14/15/19/23/27/32/33/46/53）——按讲义公式重算
          B) 讲义的真数（p.9/10/34/36/37/38/41/44/45/47/48/49/50/51）——从 class04 的结果表逐格重算，
             并用两个共享面板核对树的叶子人数（p.9/10/44）与可用行数（p.34/41）
          C) 笔记补充的迷你例子（bagging 方差公式代入、boosting 第二步、OOS R² 与价差可以同时正负）
讲义      Lec04 p.9–51
笔记      [[M04-非线性机器学习与收益预测]] §2.2–2.9
输入      class04/ 的 16 个文件（经 common.load 的 c04_* loader）+ class03/market_linear_model_summary.csv（p.38 线性列）
输出      stdout（全部关键数字）· output/L04_01_reproduce_lecture.csv（市场 + 个股 OOS R² 重算表）
关键决定  · 五分组用每周 rank(method="first") 再 qcut（与 L03_01 相同），79 只股票 → 每周 16/16/15/16/16
          · t 值 = 52 周价差均值 / (标准差/√52)，与 spreads 表的 t_statistic 对照
          · p.9/10/44 的叶子人数按讲义给出的阈值在"development + validation"行上直接数（不重训，重训见 L04_02）
          · ⚠️ class03/stock_linear_test_predictions.csv 已损坏（358/4,108 行），本脚本不读它；p.50 的 PCR 行取 class03 汇总表
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from common import load

def h(s): print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)
def oos(actual, pred, bench): return 100 * (1 - ((actual - pred) ** 2).sum() / ((actual - bench) ** 2).sum())

# ---------------------------------------------------------------- A 假数算例
h("A. 讲义假数算例（Illustrative，按讲义公式重算）")
low = [3, 1, 2]; high = [0, -1, -2]
print(f"p.14 两片叶子：r_low = ({'+'.join(map(str, low))})/3 = {np.mean(low):.0f}% ; r_high = ({'+'.join(map(str, high))})/3 = {np.mean(high):.0f}%")
print(f"p.14 新月份通胀 2.0% → 走左枝 → 预测 {np.mean(low):.0f}%；3.5% → 右枝 → {np.mean(high):.0f}%")
val = {1: 28, 2: 26, 4: 29, 8: 35}; tr = {1: 24, 2: 21, 4: 16, 8: 9}
print(f"p.11 验证 MSE ×1e4 {val} → 最小在深度 {min(val, key=val.get)}；训练 MSE 单调下降 {tr}")
print(f"p.15 动量效应：低波动 +0.6% − 0.0% = +0.6%；高波动 −0.2% − 0.0% = −0.2% → 符号随波动率翻转")
bag = [0.8, -0.2, 0.3]
print(f"p.19 bagging：({' '.join(f'{x:+}' for x in bag)})/3 = {np.mean(bag):.1f}%")
ret = np.array([3, 1, 2, 0, -1, -2]); F0 = ret.mean(); res = ret - F0
print(f"p.23 boosting：F0 = 均值 = {F0}；残差 = {res.tolist()}；树桩在 2.5% 切开：左叶均值 {res[:3].mean():+.1f}、右叶 {res[3:].mean():+.1f}")
print(f"     ν = 0.1 → F1 = {F0} + 0.1×(±1.5) = {F0 + 0.15:.2f} 或 {F0 - 0.15:.2f}")
print(f"p.27 MCQ：波动率 1.5% ≤ 2% 且动量 −0.4% ≤ 0 → 第三行 → −0.2%（选 C）")
for s, m, v in [("A", 1.0, 0.5), ("B", 1.0, 1.5)]:
    hh = max(0.0, m - v); print(f"p.32 隐藏单元 {s}：h = max(0, {m}−{v}) = {hh} → 预测 = 0.10% + 0.40%×{hh} = {0.10 + 0.40 * hh:.2f}%")
ep = {10: 0.0027, 30: 0.0023, 60: 0.0026}
print(f"p.33 早停：验证 MSE {ep} → 最小在 epoch {min(ep, key=ep.get)}")
print("p.46 MCQ：验证 MSE 最小 = Random forest 0.0021 → 选 B（不能看测试期 MSE 挑模型）")
print("p.53 简答：OOS R² −1%（量级误差比猜零大）与价差 +0.08%（排序略有信息）可以同时成立——两个指标量的不是一回事")

# ---------------------------------------------------------------- C 笔记补充
h("C. 笔记补充的迷你例子")
for rho in (0.0, 0.5, 0.9):
    for B in (1, 10, 100):
        v = rho + (1 - rho) / B
        print(f"  bagging 方差/σ²：ρ={rho} B={B:3d} → {v:.3f}", end="")
    print()
F1 = F0 + 0.1 * np.where(np.arange(6) < 3, 1.5, -1.5)
res2 = ret - F1
print(f"  boosting 第二步：F1 = {F1.round(2).tolist()}；新残差 = {res2.round(2).tolist()}；同一树桩再切一次 → 左叶 {res2[:3].mean():+.2f}、右叶 {res2[3:].mean():+.2f} → F2 = F1 + 0.1×(±{abs(res2[:3].mean()):.2f})")
infl = np.array([1.0, 1.8, 2.2, 3.0, 3.6, 4.4])
for s in [1.4, 2.0, 2.6, 3.3, 4.0]:
    L = ret[infl <= s]; R = ret[infl > s]; sse = ((L - L.mean()) ** 2).sum() + ((R - R.mean()) ** 2).sum()
    print(f"  p.6 分裂准则（六个月例子）：阈值 {s} → 左 {L.tolist()} 均值 {L.mean():.2f} / 右 {R.tolist()} 均值 {R.mean():.2f} → 两叶 SSE 之和 {sse:.2f}")
a = np.array([1.9, -0.5, 1.0, -2.0, 0.4]); p_ = np.array([0.4, 0.3, 0.2, 0.1, 0.0])
print(f"  OOS R² 为负但排序对：实现 {a.tolist()} 预测 {p_.tolist()} → OOS R²(对零) = {oos(a, p_, 0*a):.1f}%；预测最高两只均值 {a[:2].mean():+.2f}% vs 最低两只 {a[-2:].mean():+.2f}% → 高减低 {a[:2].mean()-a[-2:].mean():+.2f}%")

# ---------------------------------------------------------------- B 真数
h("B1. 共享面板核对（p.34 / p.41）：行数、拆分、可用观测")
mp = load.c04_market_panel(); spn = load.c04_stock_panel()
print("市场面板", mp.shape, "市场 =", sorted(mp.market_label.unique()), "拆分 =", mp[mp.market == 'US_SPY'].split.value_counts().to_dict())
print("  每市场月数 =", mp.groupby('market').size().to_dict(), "→ 238 个月（2006-09 → 2026-06）；MA(12) 基准缺失月数 =", int(mp[mp.market == 'US_SPY'].benchmark_ma12_excess_return.isna().sum()))
rank_cols = [c for c in spn.columns if c.endswith('_rank')]
usable = spn.dropna(subset=['excess_return'] + rank_cols)
print("股票面板", spn.shape, "股票数 =", spn.ticker.nunique(), "周数 =", spn.forecast_week.nunique(), "rank 列 =", len(rank_cols))
print("  可用行（目标 + 30 个 rank 齐全）=", len(usable), "按拆分 =", usable.split.value_counts().to_dict(), "周数按拆分 =", usable.groupby('split').forecast_week.nunique().to_dict())
assert len(mp) == 714 and len(usable) == 12281, "面板行数与 README 不符"

h("B2. 讲义 p.9 / p.10 的根节点（按讲义阈值在 development+validation 行上直接数）")
pre = mp[mp.split.isin(['development', 'validation'])]
for lab, thr in [("U.S.", 2.482), ("HKSAR", 2.456)]:
    g = pre[pre.market_label == lab]
    lo = g[g.inflation_lag2 <= thr]; hi = g[g.inflation_lag2 > thr]
    print(f"  {lab:6s} 训练月 {len(g)}：通胀_lag2 ≤ {thr}% → {len(lo)} 个月，均值超额 {100*lo.market_excess_return.mean():+.1f}%（{100*len(lo)/len(g):.1f}%）；> {thr}% → {len(hi)} 个月，均值 {100*hi.market_excess_return.mean():+.1f}%（{100*len(hi)/len(g):.1f}%）；总体均值 {100*g.market_excess_return.mean():+.1f}%")

h("B3. 讲义 p.44 的个股树桩（dolvol_trend_rank ≤ 0.150，在 development+validation 可用行上直接数）")
pre_s = usable[usable.split.isin(['development', 'validation'])]
lo = pre_s[pre_s.dolvol_trend_rank <= 0.150]; hi = pre_s[pre_s.dolvol_trend_rank > 0.150]
print(f"  训练行 {len(pre_s)}：≤0.150 → {100*len(lo)/len(pre_s):.1f}% 行，均值超额 {100*lo.excess_return.mean():+.2f}%；>0.150 → {100*len(hi)/len(pre_s):.1f}%，均值 {100*hi.excess_return.mean():+.2f}%；总体 {100*pre_s.excess_return.mean():+.3f}%")
print(f"  0.150 在训练行 dolvol_trend_rank 分布中的分位 = {100*(pre_s.dolvol_trend_rank <= 0.150).mean():.1f}%（讲义说约第 65 百分位）")

h("B4. 市场任务（p.10 / p.36 / p.38）：结果表 + 用 180 行预测逐月重算 12 个 OOS R²")
ms = load.c04_market_summary(); ms['val_x1e4'] = (ms.validation_mse * 1e4).round(2); ms['test_x1e4'] = (ms.test_mse * 1e4).round(2); ms['oos_pct'] = (ms.oos_r2 * 100).round(1)
print(ms[['market', 'model', 'val_x1e4', 'max_depth', 'min_samples_leaf', 'learning_rate', 'test_x1e4', 'oos_pct']].to_string(index=False))
mpred = load.c04_market_predictions(); rows = []
for mk, g in mpred.groupby('market'):
    for m in ['OLS', 'Decision tree', 'Random forest', 'Gradient boosting']:
        r2 = oos(g.actual, g[m], g['MA(12)']); tab = float(ms[(ms.market == mk) & (ms.model == m)].oos_r2) * 100
        rows.append(dict(task='market', group=mk, model=m, oos_r2_pct=round(r2, 1), table_pct=round(tab, 1), n=len(g), match=abs(r2 - tab) < 0.05))
    print(f"  {mk:17s} 月数 {len(g)}  重算: " + ", ".join(f"{r['model']} {r['oos_r2_pct']:+.1f}%{'✅' if r['match'] else '❌'}" for r in rows if r['group'] == mk))
c03 = load.c03_market_summary()
print("\n  p.38 线性列（class03 汇总表）：", {mk: f"{m} {100*float(c03[(c03.market == mk) & (c03.model == m)].oos_r2):+.1f}%" for mk, m in [('U.S.', 'LASSO'), ('HKSAR', 'Elastic Net'), ('Chinese Mainland', 'LASSO')]})
print("  p.38 非线性列（class04 汇总表，验证选中）：", {mk: f"{m} {100*float(ms[(ms.market == mk) & (ms.model == m)].oos_r2):+.1f}%" for mk, m in [('U.S.', 'Gradient boosting'), ('HKSAR', 'Decision tree'), ('Chinese Mainland', 'Random forest')]})
mv = load.c04_market_validation()
best = mv.loc[mv.groupby(['market', 'model']).validation_mse.idxmin()]
print("  验证表里各族最小验证 MSE 的设置：")
print(best[['market', 'model', 'max_depth', 'min_samples_leaf', 'learning_rate', 'n_estimators', 'validation_mse']].assign(validation_mse=lambda d: (d.validation_mse * 1e4).round(2)).to_string(index=False))

h("B5. p.37 CSI 300 最近 36 个月子窗口（2023-07 → 2026-06，模型仍用 2021-06 拟合）")
cn = mpred[(mpred.market == 'Chinese Mainland') & (mpred.forecast_month >= '2023-07-01')]
rec = load.c04_csi300_recent()
for m in ['OLS', 'Decision tree', 'Random forest', 'Gradient boosting']:
    r2 = oos(cn.actual, cn[m], cn['MA(12)']); tab = 100 * float(rec[rec.model == m].oos_r2)
    print(f"  {m:18s} 子窗口 {len(cn)} 个月 OOS R² 重算 {r2:+.1f}%  表 {tab:+.1f}%  {'✅' if abs(r2-tab) < 0.05 else '❌'}")
print(f"  子窗口里 MA(12) 的 MSE ×1e4 = {1e4*((cn.actual-cn['MA(12)'])**2).mean():.2f}；实现超额收益最大月 = {cn.loc[cn.actual.idxmax(), 'forecast_month'].date()} {100*cn.actual.max():+.1f}%（2024-09-24 政策公告后的那个月）")

h("B6. p.36 美国 Gradient boosting 的置换重要性（×1e6）")
mi = load.c04_market_importance()
print(mi.assign(imp_x1e6=lambda d: (d.permutation_importance * 1e6).round(1), sd_x1e6=lambda d: (d.importance_sd * 1e6).round(1))[['market', 'selected_model', 'feature', 'imp_x1e6', 'sd_x1e6']].to_string(index=False))

h("B7. 个股任务（p.45 / p.47 / p.50）：验证表、结果表 + 用 4,108 行预测重算 OOS R²（对零）")
ss = load.c04_stock_summary(); ss['val_x1e4'] = (ss.validation_mse * 1e4).round(2); ss['test_x1e4'] = (ss.test_mse * 1e4).round(2); ss['oos_pct'] = (ss.oos_r2 * 100).round(3)
print(ss[['model', 'val_x1e4', 'max_depth', 'min_samples_leaf', 'learning_rate', 'test_x1e4', 'oos_pct', 'forecast_correlation']].to_string(index=False))
sv = load.c04_stock_validation()
print("  验证表各族最小："); print(sv.loc[sv.groupby('model').validation_mse.idxmin()][['model', 'max_depth', 'min_samples_leaf', 'learning_rate', 'n_estimators', 'validation_mse']].assign(validation_mse=lambda d: (d.validation_mse * 1e4).round(2)).to_string(index=False))
sp = load.c04_stock_predictions()
print("  预测表行数", len(sp), "周数", sp.forecast_week.nunique(), "股票数", sp.ticker.nunique())
assert len(sp) == 4108, "stock_nonlinear_test_predictions.csv 行数不对——检查文件是否被截断"
for m in ['OLS', 'Decision tree', 'Random forest', 'Gradient boosting']:
    r2 = oos(sp.actual, sp[m], sp['Zero']); tab = 100 * float(ss[ss.model == m].oos_r2)
    rows.append(dict(task='stock', group='HSI', model=m, oos_r2_pct=round(r2, 3), table_pct=round(tab, 3), n=len(sp), match=abs(r2 - tab) < 0.005))
    print(f"  {m:18s} OOS R² 重算 {r2:+.3f}%  表 {tab:+.3f}%  测试 MSE ×1e4 {1e4*((sp.actual-sp[m])**2).mean():.2f}  预测标准差 {100*sp[m].std():.2f}%  {'✅' if abs(r2-tab) < 0.005 else '❌'}")
pcr = load.c03_stock_summary(); pcr = pcr[pcr.model == 'PCR'].iloc[0]
print(f"  实现超额收益标准差 {100*sp.actual.std():.2f}%；PCR（class03 汇总表）OOS R² = {100*pcr.oos_r2:+.3f}%、测试 MSE ×1e4 {1e4*pcr.test_mse:.2f}")
print("  ⚠️ p.47 把 +0.01% / +0.04% / −0.14% 显示为 +0.0% / +0.0% / −0.1%，p.50 显示为 +0.01% / +0.04%：同一数字两种舍入")

h("B8. p.49 Techtronic 0669.HK，2025-10-31 那一周")
r = sp[(sp.ticker == '0669.HK') & (sp.forecast_week == '2025-10-31')].iloc[0]
print(f"  股票收益 {100*r.stock_return:+.2f}%  无风险 {100*r.risk_free_return:+.2f}%  实现超额 {100*r.actual:+.2f}%  RF 预测 {100*r['Random forest']:+.2f}%  GB {100*r['Gradient boosting']:+.2f}%  DT {100*r['Decision tree']:+.2f}%  分组 Q{int(r.forecast_quintile)}")

h("B9. p.48 / p.51 分组价差：结果表 + 用 4,108 行预测按周分五组重算")
sq = load.c04_stock_quintiles(); ssp = load.c04_stock_spreads()
print(sq.pivot(index='model', columns='forecast_quintile', values='mean_excess_return').mul(100).round(3).to_string())
print(ssp.assign(spread_pct=lambda d: (d.mean_weekly_spread * 100).round(3), t=lambda d: d.t_statistic.round(2), hit=lambda d: d.hit_rate.round(3))[['model', 'spread_pct', 't', 'annualized_sharpe', 'hit', 'first_half_mean', 'second_half_mean']].to_string(index=False))
for m in ['Decision tree', 'Random forest', 'Gradient boosting']:
    d = sp.copy(); d['q'] = d.groupby('forecast_week')[m].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False) + 1)
    wk = d.groupby(['forecast_week', 'q']).actual.mean().unstack(); spread = wk[5] - wk[1]
    t = spread.mean() / (spread.std(ddof=1) / np.sqrt(len(spread)))
    tab = ssp[ssp.model == m].iloc[0]
    print(f"  {m:18s} 五组均值 % = {[round(100*wk[q].mean(), 3) for q in range(1, 6)]}  价差 {100*spread.mean():+.3f}%（表 {100*tab.mean_weekly_spread:+.3f}%）  t {t:.2f}（表 {tab.t_statistic:.2f}）  命中 {(spread > 0).mean():.3f}")
    if m == 'Decision tree':
        print(f"     决策树预测只有 {d[m].nunique()} 个取值 → 每周分组靠 rank(method='first') 硬切，'排序'其实是按行序，价差无意义")
si = load.c04_stock_importance().sort_values('permutation_importance', ascending=False)
print("  RF 置换重要性前 5（×1e6）：", [(f, round(v * 1e6, 2)) for f, v in zip(si.feature.head(5), si.permutation_importance.head(5))])
print("  重要性 ≤ 0 的特征数：", int((si.permutation_importance <= 0).sum()), "/ 30")

out = pd.DataFrame(rows); out.to_csv(load.OUTPUT_DIR / 'L04_01_reproduce_lecture.csv', index=False, encoding='utf-8-sig')
print("\n写出", load.OUTPUT_DIR / 'L04_01_reproduce_lecture.csv', "；全部对上？", bool(out.match.all()))
assert out.match.all(), "有 OOS R² 与结果表对不上"
