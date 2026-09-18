"""
L02_03 · R² = 1% 的散点图长什么样：为什么金融 1% 算好、IS6400 0.5 算正常
========================================================================
目的      跨课最大的口径冲突：EF5560 说收益预测 R² ≈ 1% 是常态、2–3% 对冲基金就能赚大钱（🎙️ M01 02:09:06），
          IS6400 那类通用课把 R² = 0.5 当"正常"。本脚本把两者画在一起：左边是真实的 SPY 月收益 vs 滞后 12 月波动率
          （R² ≈ 1%），右边用**同一个 x、同样的点数、同样的坐标比例**合成一个 R² = 0.5 的关系。让读者一眼看到
          "金融的可预测性有多低"——以及教授说的"图上看不出规律才正常"是什么意思（讲义 L1 p.50、L2 p.11–12）。
讲义      Lec02 p.11–16（先画图再拟合）、p.23（R² 是方差摘要，低 R² 正常）；Lec01 p.50（散点图）
笔记      [[M02-回归与样本外设计]] §2.4.4、§2.9；[[M01-金融数据与Vibe-Coding]] §2.3.4、§2.9.3；术语总表 §2.2
输入      spy_monthly_features_240m.csv（全部 240 个月，对数收益）
输出      output/L02_03_r2_scale.png · output/L02_03_r2_scale.csv
关键决定  · 左图用全样本 240 个月（不是训练 180 月）：volatility_12 的全样本 R² = 1.01%，正好是"1%"的实物；
            训练 180 月的 R² 是 1.45%（讲义 p.24），这里要的是"1% 长什么样"，所以取全样本
          · 右图的合成 y：z = 标准化的同一个 x；噪声 e ~ N(0,1)（seed 5560）先对 z 正交化再标准化，
            y* = √0.5·z + √0.5·e，于是样本 R² **精确等于 0.5**（不是近似）；再把 y* 缩放到与真实 y 相同的均值和标准差，
            两图 y 轴量程相同——唯一的差别是"信号占方差的比例"
          · 两图共用 x/y 轴范围、点数、点的大小与透明度；拟合线用 statsmodels.OLS
          · 额外打印"拟合值标准差 / 残差标准差"——R² = 1% 意味着预测值的波动只有噪声的十分之一
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))   # 让 common 可导入，脚本从哪启动都能跑

import numpy as np
import pandas as pd
import statsmodels.api as sm

from common import load, plot

XCOL = "volatility_12"
TARGET_R2 = 0.5
SEED = 5560

# ---------- 1. 真实数据：SPY 月收益 vs 滞后 12 月波动率 ----------
d = load.spy_features()
x = d[XCOL]
y = d["market_return"]
assert len(d) == 240 and x.notna().all() and y.notna().all()
fit_real = sm.OLS(y, sm.add_constant(x)).fit()
r2_real = fit_real.rsquared

# ---------- 2. 合成数据：同一个 x，R² 精确 = 0.5 ----------
rng = np.random.default_rng(SEED)
z = (x - x.mean()) / x.std(ddof=1)
e = pd.Series(rng.standard_normal(len(z)), index=z.index)
e = e - e.mean()
e = e - (e @ z) / (z @ z) * z                     # 对 z 正交化：样本相关恰为 0
e = e / e.std(ddof=1)
z = z / z.std(ddof=1)
y_star = np.sqrt(TARGET_R2) * z + np.sqrt(1 - TARGET_R2) * e
y_syn = y.mean() + y.std(ddof=1) * y_star / y_star.std(ddof=1)   # 与真实 y 同均值、同标准差
fit_syn = sm.OLS(y_syn, sm.add_constant(x)).fit()
r2_syn = fit_syn.rsquared
assert abs(r2_syn - TARGET_R2) < 1e-9, f"合成 R² = {r2_syn}，应精确等于 {TARGET_R2}"
assert abs(y_syn.std(ddof=1) - y.std(ddof=1)) < 1e-12 and abs(y_syn.mean() - y.mean()) < 1e-12
assert fit_syn.params[XCOL] > 0

# ---------- 3. 关键数字 ----------
def describe(fit, yy, tag):
    fitted = fit.fittedvalues
    return {"数据": tag, "R²": fit.rsquared, "相关系数": np.sign(fit.params[XCOL]) * np.sqrt(fit.rsquared),
            "斜率": fit.params[XCOL], "p值": fit.pvalues[XCOL], "y标准差": yy.std(ddof=1),
            "拟合值标准差": fitted.std(ddof=1), "残差标准差": fit.resid.std(ddof=1),
            "拟合值sd/残差sd": fitted.std(ddof=1) / fit.resid.std(ddof=1)}

tbl = pd.DataFrame([describe(fit_real, y, f"真实 SPY 月收益 vs {XCOL}"), describe(fit_syn, y_syn, "合成 y（同一个 x）")]).set_index("数据")
tbl.to_csv(load.OUTPUT_DIR / "L02_03_r2_scale.csv", encoding="utf-8-sig", float_format="%.6f")

print("=" * 88)
print(f"同样 240 个点、同一个 x = {XCOL}、同样的 y 均值与标准差，只改变信号占方差的比例")
print("-" * 88)
for tag, r in tbl.iterrows():
    print(f"{tag}")
    print(f"    R² = {r['R²']*100:.2f}%   corr = {r['相关系数']:+.3f}   斜率 = {r['斜率']:+.4f}   p = {r['p值']:.3g}")
    print(f"    y 标准差 {r['y标准差']*100:.2f}%   拟合值标准差 {r['拟合值标准差']*100:.2f}%   残差标准差 {r['残差标准差']*100:.2f}%"
          f"   拟合值 sd / 残差 sd = {r['拟合值sd/残差sd']:.2f}")
print("-" * 88)
print(f"读法：R² = 1% 时预测值的波动只有噪声的 {tbl.iloc[0]['拟合值sd/残差sd']:.2f} 倍（约 1/10），肉眼在散点里看不出斜率——")
print(f"      这就是教授说的'图上看不出规律才正常'；R² = 0.5 时预测值与噪声一样大（{tbl.iloc[1]['拟合值sd/残差sd']:.2f} 倍），趋势一眼可见。")
print(f"      金融里 R² 从 1% 提到 2–3% 就有对冲基金级别的价值；营销/通用数据挖掘的 R² 参照系是 0.5 以上（IS6400）。")
print("=" * 88)

# ---------- 4. 画图：并排两图，同轴同点数 ----------
fig, ax0 = plot.setup(figsize=(12.5, 5.8))
ax0.remove()
ax_l, ax_r = fig.subplots(1, 2, sharex=True, sharey=True)
xx = np.linspace(x.min(), x.max(), 100)
for ax, yy, fit, title, col in ((ax_l, y, fit_real, f"真实：SPY 月收益 vs 滞后 12 月波动率\nR² = {r2_real*100:.2f}%（240 个月）", plot.COLORS["US_SPY"]),
                                 (ax_r, y_syn, fit_syn, f"合成：同一个 x，噪声换成信号\nR² = {r2_syn*100:.1f}%（同样 240 个点）", plot.COLORS["simple"])):
    ax.scatter(x, yy * 100, s=18, alpha=0.55, color=plot.COLORS["actual"], edgecolor="none")
    ax.plot(xx, (fit.params["const"] + fit.params[XCOL] * xx) * 100, color=plot.COLORS["fitted"], lw=2.2, label="OLS 拟合线")
    ax.axhline(0, color="#999", lw=0.8)
    ax.set_title(title, fontsize=11, color=col)
    ax.set_xlabel("滞后 12 个月年化波动率（volatility_12）")
    ax.legend(loc="upper right", fontsize=9)
    ax.text(0.02, 0.03, f"拟合值 sd / 残差 sd = {fit.fittedvalues.std(ddof=1) / fit.resid.std(ddof=1):.2f}",
            transform=ax.transAxes, fontsize=9, color="#333", va="bottom")
ax_l.set_ylabel("月收益（%）")
ax_l.set_ylim(min(y.min(), y_syn.min()) * 100 - 1, max(y.max(), y_syn.max()) * 100 + 1)
fig.suptitle("R² = 1% 与 R² = 50% 的散点图：金融里 1% 算好（EF5560），通用数据挖掘里 0.5 才算正常（IS6400）", fontsize=12.5)
plot.save(fig, "L02_03_r2_scale",
          note=f"数据：spy_monthly_features_240m.csv（对数收益，240 个月）· 右图 y 为合成（seed {SEED}，噪声对 x 正交化，样本 R² 精确 = 0.5，均值与标准差同左图）· statsmodels.OLS")
