"""
L03_01 · 讲义 Lec03 的全部数字能否复现：真数（class03 五个 CSV）+ 假数算例 + 笔记补充的迷你例子
=====================================================================================
目的      笔记 M03 里出现的每一个数字都要能在这里的输出里找到。三组：
          A) 讲义标 "Illustrative" 的假数算例（p.7/11/16/18/22/34/42/45/54）——按讲义公式重算
          B) 讲义的真数（p.14/21/23/47/49/55）——从 class03 的结果表逐格重算，包括用 180 行月度预测重算 12 个市场 OOS R²、
             用 4,108 行个股预测重算 6 个 OOS R²、Ridge/PCR/PLS/OLS 的五分组均值与价差 t 值、p.49 三只股票
          C) 笔记补充的迷你例子（单输入 Ridge 闭式解、LASSO 软阈值、相关输入下 OLS vs Ridge、中心化排名、无风险折算、
             迷你 OOS R²、两列相关 0.8 的 PC1 占比、动量算例）
讲义      Lec03 p.7–55
笔记      [[M03-线性机器学习与收益预测]] §2.2.2、§2.3、§2.4.1–2.4.6、§2.5.1–2.5.2、§2.6.4–2.6.5、§2.7.2–2.7.3、§2.8.1–2.8.2、§2.9.1–2.9.3
输入      class03/market_linear_model_summary.csv · market_linear_test_predictions.csv · stock_linear_model_summary.csv ·
          stock_linear_test_predictions.csv · stock_linear_forecast_spreads.csv（经 common.load 的 c03_* loader）
输出      stdout（全部关键数字）· output/L03_01_reproduce_lecture.csv（市场 + 个股 OOS R² 重算表）
关键决定  · 五分组用每周 rank(method="first") 再 qcut，与讲义 p.53 "assign five groups using those forecast ranks" 一致；
            79 只股票 → 每周 16/16/15/16/16
          · t 值 = 52 周价差均值 / (标准差/√52)，与 spreads 表的 t_statistic 对照
          · 单输入 Ridge/LASSO 闭式解假设输入已标准化且 Σz² = n（这是"每一个标准差"口径下的自然假设）
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from common import load

def h(s): print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)

# ---------------------------------------------------------------- A 假数算例
h("A. 讲义假数算例（Illustrative，按讲义公式重算）")
print("p.7  OLS 预测 = 0.20% + 0.40%×0.5 − 0.30%×(−1) =", round(0.20 + 0.40 * 0.5 - 0.30 * (-1), 4), "%")
print("p.11 前向选择：验证 MSE 30.00 → 28.70 → 28.20 → 28.40（上升）→ 停，冻结两变量")
print("p.16 LASSO 预测 = 0.10% + 0.48%×0.5 =", round(0.10 + 0.48 * 0.5, 4), "%")
print("p.18 网格最小 26.8 → (penalty 0.001, LASSO share 0.25)")
print("p.22 OOS R² = 1 − 0.018/0.015 =", round(1 - 0.018 / 0.015, 4))
print("p.34 超额 = 2.0% − 0.1% = 1.9%；零预测误差 1.9%（平方 3.61），模型预测 1.7% 误差 0.2%（平方 0.04）")
pc1 = 0.6 * 1 + 0.8 * 0.5; pc2 = -0.5
print("p.42 PCR: PC1 =", pc1, " PC2 =", pc2, " 预测 =", round(0.10 + 0.30 * pc1 - 0.20 * pc2, 4), "%")
c = 0.8 * 0.5 - 0.6 * (-1)
print("p.45 PLS: c =", c, " 预测 =", round(0.10 + 0.30 * c, 4), "%")
A = np.array([0.1, 0.2, 0.3]); mA = np.array([0.2, 0.4, 0.6]); mB = np.array([0.4, 0.8, 1.2])
print("p.54 MSE A =", round(np.mean((A - mA) ** 2), 4), " MSE B =", round(np.mean((A - mB) ** 2), 4), "（×9）；高减低都是", round(0.3 - 0.1, 2), "%")

# ---------------------------------------------------------------- B 真数
h("B1. 市场任务（p.14 / p.21 / p.23）：结果表 + 用 180 行预测逐月重算 OOS R²")
ms = load.c03_market_summary()
ms["val_x1e4"] = (ms.validation_mse * 1e4).round(2); ms["oos_pct"] = (ms.oos_r2 * 100).round(1)
print(ms[["market", "model", "val_x1e4", "alpha", "l1_ratio", "oos_pct", "nonzero_coefficients"]].to_string(index=False))
mp = load.c03_market_predictions()
rows = []
for mk, g in mp.groupby("market"):
    sse_b = ((g.actual - g["MA(12)"]) ** 2).sum()
    for m in ["OLS", "Ridge", "LASSO", "Elastic Net"]:
        r2 = 100 * (1 - ((g.actual - g[m]) ** 2).sum() / sse_b)
        rows.append(dict(task="market", group=mk, model=m, oos_r2_pct=round(r2, 1), n=len(g)))
    print(f"  {mk:17s} SSE_MA12 = {sse_b:.5f}  月数 = {len(g)}  重算 OOS R²: " +
          ", ".join(f"{r['model']} {r['oos_r2_pct']}%" for r in rows if r['group'] == mk))

h("B2. 个股任务（p.47）：结果表 + 用 4,108 行预测重算 OOS R²（对零）")
ss = load.c03_stock_summary()
ss["val_x1e4"] = (ss.validation_mse * 1e4).round(2); ss["oos_pct"] = (ss.oos_r2 * 100).round(2)
print(ss[["model", "val_x1e4", "alpha", "l1_ratio", "oos_pct", "nonzero_coefficients"]].to_string(index=False))
sp = load.c03_stock_predictions()
assert len(sp) == 4108, f"stock_linear_test_predictions.csv 只有 {len(sp)} 行（manifest 4,108 行）——本地文件已截断，请从 Canvas 重新下载 class03.zip"  # ASSERT_4108 2026-09-21
print("行数", len(sp), " 周数", sp.forecast_week.nunique(), " 股票数", sp.ticker.nunique(),
      " 实现超额收益标准差", round(sp.actual.std() * 100, 2), "%")
sse0 = (sp.actual ** 2).sum()
for m in ["OLS", "Ridge", "LASSO", "Elastic Net", "PCR", "PLS"]:
    r2 = 100 * (1 - ((sp.actual - sp[m]) ** 2).sum() / sse0)
    rows.append(dict(task="stock", group="HSI", model=m, oos_r2_pct=round(r2, 3), n=len(sp)))
    print(f"  {m:12s} OOS R² = {r2:+.3f}%   预测标准差 = {sp[m].std() * 100:.3f}%   取值个数 = {sp[m].nunique()}")
print("  LASSO / Elastic Net 常数预测值 =", round(sp.LASSO.iloc[0] * 100, 4), "%（= 截距）")

h("B3. p.49 一周三只股票（2025-07-04，PCR）")
wk = sp[sp.forecast_week == "2025-07-04"]
for tk, name in [("0939.HK", "CCB"), ("3690.HK", "Meituan"), ("0968.HK", "Xinyi Solar")]:
    r = wk[wk.ticker == tk].iloc[0]
    print(f"  {name:12s} 预测 {r.PCR * 100:+.2f}%  实现 {r.actual * 100:+.2f}%  无风险 {r.risk_free_return * 100:.3f}%")

h("B4. p.55 按预测分五组（每周 rank → qcut(5)），52 周均值与价差")
def quint(df, col):
    d = df.dropna(subset=[col]).copy()
    d["q"] = d.groupby("forecast_week")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False) + 1)
    wkm = d.groupby(["forecast_week", "q"]).actual.mean().unstack()
    spread = wkm[5] - wkm[1]
    t = spread.mean() / spread.std() * np.sqrt(len(spread))
    return (wkm.mean() * 100).round(2).tolist(), round(spread.mean() * 100, 3), round(t, 2), round((spread > 0).mean(), 3), \
           round(spread.iloc[:26].mean() * 100, 2), round(spread.iloc[26:].mean() * 100, 2)
fs = load.c03_stock_spreads().set_index("model")
for m in ["Ridge", "PCR", "PLS", "OLS"]:
    q, sprd, t, hit, h1, h2 = quint(sp, m)
    ref = fs.loc[m]
    print(f"  {m:6s} Q1..Q5 = {q}  Q5−Q1 = {sprd:+.3f}%/周  t = {t}  命中率 {hit}  前半 {h1:+.2f}% 后半 {h2:+.2f}%   "
          f"| spreads 表: {ref.mean_weekly_spread * 100:+.3f}%  t = {ref.t_statistic:.2f}")
print("  Ridge 年化价差 ≈ 0.48% × 52 =", round(0.004805 * 52 * 100, 1), "%；LASSO / EN sortable =", fs.loc['LASSO', 'sortable'], fs.loc['Elastic Net', 'sortable'])

# ---------------------------------------------------------------- C 笔记补充的迷你例子
h("C. 笔记补充的迷你例子")
n, sxy = 100, 40.0
for lam in [0, 25, 100, 400]:
    print(f"  C1 单输入 Ridge（n=100, Σzr=40）：λ = {lam:3d} → β = {sxy / (n + lam):.2f} = 0.40 × n/(n+λ)")
for lam in [0, 0.1, 0.3, 0.4, 0.5]:
    print(f"  C1 单输入 LASSO 软阈值：λ = {lam} → β = {np.sign(0.4) * max(0.4 - lam, 0):.2f}")
x_dec = np.array([0.02, 0.03, 0.04, 0.05, 0.01])
z1 = (x_dec - x_dec.mean()) / x_dec.std(ddof=1); z2 = (x_dec * 100 - (x_dec * 100).mean()) / (x_dec * 100).std(ddof=1)
print("  C2 标准化消单位：z(小数) =", z1.round(3), " z(百分数) =", z2.round(3), " 相同:", np.allclose(z1, z2))
rng = np.random.default_rng(0)
x1 = rng.normal(size=200); x2 = x1 + 0.05 * rng.normal(size=200); y = 0.5 * x1 + 0.5 * x2 + rng.normal(size=200)
X = np.column_stack([x1, x2]); Xs = (X - X.mean(0)) / X.std(0, ddof=1); yc = y - y.mean(); n = len(y)
rho = Xs[:, 0] @ Xs[:, 1] / (n - 1); c1 = Xs[:, 0] @ yc / (n - 1); c2 = Xs[:, 1] @ yc / (n - 1)
print(f"  C3 两列标准化输入：ρ = {rho:.4f}  c1 = {c1:.4f}  c2 = {c2:.4f}（笔记 §2.4.2 闭式解的输入）")
for lam in [0, 10, 100]:
    k = lam / (n - 1); det = (1 + k) ** 2 - rho ** 2
    b_closed = np.array([((1 + k) * c1 - rho * c2) / det, ((1 + k) * c2 - rho * c1) / det])
    b = np.linalg.solve(Xs.T @ Xs + lam * np.eye(2), Xs.T @ yc)
    print(f"  C3 λ = {lam:3d}  k = {k:.4f}  分母 = {det:.5f} → 闭式解 β = {b_closed.round(2)}  矩阵解 = {b.round(2)}  和 = {b.sum():.2f}")
mom = pd.Series({"A": 0.05, "B": -0.02, "C": 0.10, "D": 0.01, "E": -0.07}); pr = mom.rank(pct=True)
print("  C4 百分位:", pr.round(2).to_dict(), " 中心化:", (pr - 0.5).round(2).to_dict())
print("  C5 无风险：年化 4.2% → 周 ", round(0.042 / 52 * 100, 4), "%，月", round(0.042 / 12 * 100, 3), "%")
act = np.array([0.019, -0.005, 0.010, -0.020, 0.004]); pred = np.array([0.017, 0.001, 0.003, -0.004, 0.002])
print("  C6 迷你 OOS R²（对零）：SSE_model =", round(((act - pred) ** 2).sum(), 6), " SSE_zero =", round((act ** 2).sum(), 6),
      " R² =", round(1 - ((act - pred) ** 2).sum() / (act ** 2).sum(), 4))
print("  C7 两列相关 0.8：PC1 方差占比 = (1+0.8)/2 =", (1 + 0.8) / 2)
print("  C8 由 t = 1.459、价差 0.4805% 反推 52 周价差标准差 =", round(0.4805 / 1.459 * np.sqrt(52), 2), "%")
print("  C9 动量：110/100 − 1 =", round(110 / 100 - 1, 2))

out = load.OUTPUT_DIR / "L03_01_reproduce_lecture.csv"
pd.DataFrame(rows).to_csv(out, index=False)
print(f"\n[saved] {out}")
