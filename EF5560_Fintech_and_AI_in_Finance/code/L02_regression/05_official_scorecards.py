"""
L02_05 · class02 官方结果表 vs 本库 9/10 的复现（L02_01–L02_04）
=====================================================================
目的      2026-09-21 教授补发 class02 数据包，里面有 8 张"课堂结果表"。本脚本把它们与 M02 笔记里已写的数字逐格对照，
          并从 60 行测试预测表重算 OOS R² 与方向命中率，确认 M02 v1.0 的数字全部站得住；顺带把择时策略表（Class 5 预告）打印出来。
讲义      Lec02 p.24、p.33、p.46–48、p.51
笔记      [[M02-回归与样本外设计]] §2.5、§2.7.4、§2.8.3、§9.5；[[EF5560_Fintech_and_AI_in_Finance/_meta/数据集卡片]] §12
输入      class02/ 的 8 张结果表（经 common.load 的 c02_* loader）
输出      stdout · output/L02_05_official_scorecards.csv（对照表）
关键决定  · 4 张输入表与 data/ 逐字节相同（sha256），不再重复检查
          · 对照容差：OOS R² 0.05 个百分点、命中率 0.1 个百分点、回归系数按讲义显示位数
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from common import load

def h(s): print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)
rows = []
def cmp(item, note_val, official, tol):
    ok = abs(note_val - official) <= tol; rows.append(dict(item=item, note=note_val, official=round(official, 4), ok=ok))
    print(f"  {'✅' if ok else '❌'} {item:44s} 笔记 {note_val:>9}  官方 {official:>10.4f}")

h("1. SPY 三变量回归成绩单（p.47 / p.49）")
sc = load.c02_spy_scorecard().iloc[0]
cmp("OOS R² (%)", 6.56, 100 * sc.oos_r_squared, 0.05)
cmp("模型方向命中率 (%)", 63.3, 100 * sc.model_directional_accuracy, 0.1)
cmp("MA(12) 方向命中率 (%)", 61.7, 100 * sc.benchmark_directional_accuracy, 0.1)
sp = load.c02_spy_predictions()
r2 = 100 * (1 - (sp.model_error ** 2).sum() / (sp.benchmark_error ** 2).sum())
print(f"  用 60 行预测表重算 OOS R² = {r2:.3f}%；模型预测全部为正？ {bool((sp.forecast > 0).all())}（M02 §2.7.4 的结论）；正收益月 {int((sp.market_return > 0).sum())}/60")
print(f"  择时策略（Class 5 预告）：年化收益 {100*sc.timing_annual_return:.2f}% / 波动 {100*sc.timing_annual_volatility:.2f}% / 夏普 {sc.timing_sharpe:.3f}  vs 买入持有 {100*sc.buy_hold_annual_return:.2f}% / {100*sc.buy_hold_annual_volatility:.2f}% / {sc.buy_hold_sharpe:.3f}")

h("2. CSI 300 宏观回归成绩单（p.35 / p.51）")
cs = load.c02_csi300_scorecard().iloc[0]
cmp("训练 R² (%)", 6.08, 100 * cs.train_r_squared, 0.05)
cmp("OOS R² (%)", -13.17, 100 * cs.oos_r_squared, 0.05)
cmp("模型命中率 (%)", 48.3, 100 * cs.model_directional_accuracy, 0.1)
cmp("MA(12) 命中率 (%)", 56.7, 100 * cs.benchmark_directional_accuracy, 0.1)
cmp("模型 MSE ×1e4", 31.65, 1e4 * cs.model_mse, 0.05)
cmp("基准 MSE ×1e4", 27.97, 1e4 * cs.benchmark_mse, 0.05)

h("3. 单变量回归（p.24）")
sg = load.c02_single_predictor().set_index('predictor')
for k, slope, se, p in [('momentum_12', 0.6, 2.1, 0.76), ('volatility_12', 8.5, 5.2, 0.11), ('ma_gap_10', 3.0, 4.2, 0.48)]:
    cmp(f"{k} 斜率 (pp)", slope, 100 * sg.loc[k, 'slope'], 0.05); cmp(f"{k} 标准误 (pp)", se, 100 * sg.loc[k, 'standard_error'], 0.05); cmp(f"{k} p 值", p, sg.loc[k, 'p_value'], 0.005)
print(f"  return_lag1（讲义未单列）：斜率 {100*sg.loc['return_lag1','slope']:.2f} pp，p = {sg.loc['return_lag1','p_value']:.3f}，R² {100*sg.loc['return_lag1','r_squared']:.2f}%")

h("4. 三市场回归与择时（p.46–48；择时表是 Class 5 预告）")
tr = load.c02_three_market_regression()
for _, r in tr.iterrows():
    print(f"  {r.market:28s} OOS R² {100*r.oos_r2:+.2f}%  命中率 {100*r.directional_accuracy:.1f}%  正收益基准率 {100*r.positive_return_base_rate:.1f}%  ({int(r.directional_hits)}/60 命中, {int(r.positive_months)} 个正收益月)")
cmp("恒生 OOS R² (%)", 4.4, 100 * tr.iloc[1].oos_r2, 0.05); cmp("CSI 300 OOS R² (%)", 4.3, 100 * tr.iloc[2].oos_r2, 0.05)
cmp("恒生命中率 (%)", 41.7, 100 * tr.iloc[1].directional_accuracy, 0.1); cmp("CSI 300 命中率 (%)", 51.7, 100 * tr.iloc[2].directional_accuracy, 0.1)
print(f"  ⚠️ 三市场表里 SPY 的 OOS R² = {100*tr.iloc[0].oos_r2:.2f}%，与 SPY 成绩单的 {100*sc.oos_r_squared:.2f}% 不同（测试 MSE {1e4*tr.iloc[0].test_mse:.2f} vs {1e4*sc.model_mse:.2f}）——⚪ 三市场表可能用了另一组预测变量（文件未说明），笔记 p.46 写的'≈ 6.6%' 两个都覆盖")
tt = load.c02_three_market_timing()
print(tt.assign(**{c: (tt[c] * 100).round(2) for c in ['buy_hold_ann_return', 'timing_ann_return', 'buy_hold_ann_volatility', 'timing_ann_volatility']})[['market', 'buy_hold_ann_return', 'timing_ann_return', 'buy_hold_sharpe', 'timing_sharpe', 'timing_market_exposure', 'months_in_market', 'months_in_cash']].round(3).to_string(index=False))

h("5. 动量十箱（p.15 的分箱图数据）")
mb = load.c02_momentum_bins()
print(mb.assign(mean_momentum=lambda d: (d.mean_momentum * 100).round(1), mean_return=lambda d: (d.mean_return * 100).round(2)).to_string(index=False))
print(f"  十箱均值收益与均值动量的相关 = {np.corrcoef(mb.mean_momentum, mb.mean_return)[0,1]:+.2f}（M02 §2.3.3 说的'看不出趋势'）")

out = pd.DataFrame(rows); out.to_csv(load.OUTPUT_DIR / 'L02_05_official_scorecards.csv', index=False, encoding='utf-8-sig')
print("\n对照", len(out), "项，全部一致？", bool(out.ok.all()))
assert out.ok.all()
