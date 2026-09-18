"""
L02_04 · 方向命中率 63.3% 到底强不强：与多数类基线对比
=======================================================
目的      讲义 p.47 说三变量回归的方向命中率 63.3%，而测试期 60 个月里 38 个月是正的（也是 63.3%）。本脚本算清楚：
          ① 多数类基线（永远猜涨）是多少 ② 模型到底在哪些月份预测了下跌（答案：一次都没有——60 个预测全为正，
          所以它的方向判断与"永远猜涨"逐月完全相同）③ 用二项检验看 38/60 相对 50% 和相对多数类基线各是什么 p 值。
讲义      Lec02 p.43（命中率定义）、p.44（基准必须匹配目标）、p.47–48（三市场方向结果）
笔记      [[M02-回归与样本外设计]] §2.7.2、§2.7.4、§4.3
输入      spy_monthly_features_240m.csv（对数收益）
输出      output/L02_04_hit_rate.png · output/L02_04_hit_rate.csv
关键决定  · 模型 = L02_01 的冻结规格（三变量 OLS，train 180 月，2021-06 冻结），预测 = 同一组系数
          · 方向 = sign(·)；测试期没有恰好为 0 的收益，不需要处理平局
          · 多数类基线有两种：事后的（测试期正收益占比 38/60 = 63.3%，讲义用的）和事前的（训练期正收益占比 67.8%，
            2021-06 时就已知）——两者都报，后者才是真正"决策时可用"的基线
          · 二项检验用 scipy.stats.binomtest，单侧 greater：H0 = 命中率 ≤ 基线；对 50% 和对多数类基线各做一次
          · 模型 vs 永远猜涨的配对比较（McNemar）在这里退化：两者 60 个月的方向判断逐月相同，没有任何不一致的月份
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))   # 让 common 可导入，脚本从哪启动都能跑

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from matplotlib.patches import Rectangle, Patch

from common import load, plot

SPLIT = "2021-07-01"
X3 = ["momentum_12", "volatility_12", "ma_gap_10"]

# ---------- 1. 冻结规格的预测 ----------
d = load.spy_features()
train, test = d[d.index < SPLIT], d[d.index >= SPLIT]
assert len(train) == 180 and len(test) == 60
fit = sm.OLS(train["market_return"], sm.add_constant(train[X3])).fit()
pred = fit.predict(sm.add_constant(test[X3]))
y = test["market_return"]
ma12 = d["market_return"].shift(1).rolling(12).mean().loc[test.index]
assert (y != 0).all(), "测试期有收益恰为 0 的月份，需要定义平局规则"

sign_y, sign_m, sign_b = np.sign(y), np.sign(pred), np.sign(ma12)
always_up = pd.Series(1.0, index=test.index)

n = len(y)
k_model = int((sign_m == sign_y).sum())
k_ma12 = int((sign_b == sign_y).sum())
k_up = int((always_up == sign_y).sum())
pos_test = int((y > 0).sum())
pos_train = float((train["market_return"] > 0).mean())
n_pred_neg = int((pred < 0).sum())

# 断言：对准讲义 p.47
assert k_model == 38 and k_up == 38 and k_ma12 == 37 and pos_test == 38
assert n_pred_neg == 0, "模型在测试期有负的预测——与 60/60 全正的记录不符"
assert (sign_m == always_up).all(), "模型方向与永远猜涨应逐月完全相同"

# ---------- 2. 二项检验 ----------
p_vs_50 = stats.binomtest(k_model, n, 0.5, alternative="greater").pvalue
p_vs_majority = stats.binomtest(k_model, n, pos_test / n, alternative="greater").pvalue
p_vs_train_base = stats.binomtest(k_model, n, pos_train, alternative="greater").pvalue
n_disagree = int((sign_m != always_up).sum())
# 混淆矩阵：模型对下跌月的识别
down_months = int((y < 0).sum())
down_caught = int(((pred < 0) & (y < 0)).sum())

rows = [
    {"预测": "三变量回归（冻结规格）", "命中": k_model, "命中率": k_model / n, "预测为负的月数": n_pred_neg},
    {"预测": "永远猜涨（事后多数类）", "命中": k_up, "命中率": k_up / n, "预测为负的月数": 0},
    {"预测": "滞后 MA(12)", "命中": k_ma12, "命中率": k_ma12 / n, "预测为负的月数": int((ma12 < 0).sum())},
    {"预测": "抛硬币（期望）", "命中": n / 2, "命中率": 0.5, "预测为负的月数": n / 2},
]
tbl = pd.DataFrame(rows).set_index("预测")
tbl.to_csv(load.OUTPUT_DIR / "L02_04_hit_rate.csv", encoding="utf-8-sig", float_format="%.6f")
monthly = pd.DataFrame({"实际收益": y, "模型预测": pred, "MA12": ma12, "实际方向": sign_y, "模型方向": sign_m, "MA12方向": sign_b,
                        "模型命中": (sign_m == sign_y).astype(int)})
monthly.to_csv(load.OUTPUT_DIR / "L02_04_hit_rate_monthly.csv", encoding="utf-8-sig", float_format="%.6f")

print("=" * 84)
print(f"SPY 测试期 2021-07 → 2026-06（{n} 个月）：方向命中率与基线")
print("-" * 84)
for name, r in tbl.iterrows():
    print(f"  {name:22s} 命中 {r['命中']:>4.0f}/{n}  = {r['命中率']*100:5.1f}%   预测为负的月数 {r['预测为负的月数']:.0f}")
print("-" * 84)
print(f"  测试期正收益月：{pos_test}/{n} = {pos_test/n*100:.1f}%（事后多数类基线）；训练期正收益占比 {pos_train*100:.1f}%（事前基线，2021-06 已知）")
print(f"  模型预测范围：{pred.min()*100:+.2f}% ~ {pred.max()*100:+.2f}%，全部为正 → 方向判断与'永远猜涨'逐月相同（不一致月数 = {n_disagree}）")
print(f"  {down_months} 个下跌月里模型识别出 {down_caught} 个（召回率 {down_caught/down_months*100:.0f}%）")
print(f"  二项检验（单侧，H0：命中率 ≤ 基线）：")
print(f"    vs 50%（抛硬币）        p = {p_vs_50:.4f}   ← 看起来'显著'，但 50% 是错误的基线")
print(f"    vs 63.3%（事后多数类）   p = {p_vs_majority:.4f}   ← 与永远猜涨没有区别")
print(f"    vs 67.8%（训练期基线）   p = {p_vs_train_base:.4f}   ← 相对事前可知的基线甚至偏低")
print(f"  结论：63.3% 不是模型的功劳，是这 60 个月里牛市月份占比的复读；'跟 50% 比'会把一个从不预测下跌的模型误判为有方向能力。")
print("=" * 84)

# ---------- 3. 画图：条纹图（每月实际 / 模型 / MA(12) 方向）+ 命中率对比 ----------
fig, ax0 = plot.setup(figsize=(12.5, 7.2))
ax0.remove()
ax_s, ax_b = fig.subplots(2, 1, gridspec_kw={"height_ratios": [1.15, 1]})

UP, DOWN = plot.COLORS["simple"], plot.COLORS["fitted"]
rows_stripe = [("实际方向", sign_y, None), ("模型预测方向", sign_m, sign_y), ("永远猜涨", always_up, sign_y), ("滞后 MA(12) 方向", sign_b, sign_y)]
for i, (name, s, truth) in enumerate(rows_stripe):
    yy = len(rows_stripe) - 1 - i
    for j, m in enumerate(test.index):
        ax_s.add_patch(Rectangle((j, yy - 0.4), 1, 0.8, facecolor=UP if s.iloc[j] > 0 else DOWN, edgecolor="white", lw=0.6, alpha=0.9))
        if truth is not None and s.iloc[j] != truth.iloc[j]:
            ax_s.text(j + 0.5, yy, "×", ha="center", va="center", fontsize=9, color="white", fontweight="bold")
    if truth is not None:
        hits = int((s == truth).sum())
        ax_s.text(n + 0.4, yy, f"{hits}/{n} = {hits/n*100:.1f}%", va="center", fontsize=9.5, fontweight="bold")
    else:
        ax_s.text(n + 0.4, yy, f"{pos_test} 涨 / {n - pos_test} 跌", va="center", fontsize=9.5)
ax_s.set_xlim(0, n + 9)
ax_s.set_ylim(-1.5, len(rows_stripe) - 0.4)   # 底部留一条空带放图例
ax_s.set_yticks(range(len(rows_stripe)))
ax_s.set_yticklabels([r[0] for r in rows_stripe][::-1], fontsize=9.5)
ticks = [j for j, m in enumerate(test.index) if m.month in (1, 7)]
ax_s.set_xticks([t + 0.5 for t in ticks])
ax_s.set_xticklabels([test.index[t].strftime("%Y-%m") for t in ticks], fontsize=8.5)
ax_s.grid(False)
ax_s.set_title("每月方向：模型 60 个月全部预测上涨，与'永远猜涨'逐月相同（× = 判错）", fontsize=11)
ax_s.legend(handles=[Patch(color=UP, label="涨 / 预测涨"), Patch(color=DOWN, label="跌 / 预测跌")], loc="lower left", fontsize=8.5, ncol=2, frameon=False)

names = ["三变量回归", "永远猜涨\n（事后多数类）", "滞后 MA(12)", "训练期正收益占比\n（事前基线）", "抛硬币"]
vals = [k_model / n, k_up / n, k_ma12 / n, pos_train, 0.5]
cols = [plot.COLORS["fitted"], plot.COLORS["baseline"], plot.COLORS["US_S&P500"], plot.COLORS["baseline"], "#bbbbbb"]
ax_b.bar(range(len(names)), [v * 100 for v in vals], color=cols, alpha=0.85)
for i, v in enumerate(vals):
    ax_b.text(i, v * 100 + 0.8, f"{v*100:.1f}%", ha="center", fontsize=10, fontweight="bold")
ax_b.axhline(pos_test / n * 100, color=plot.COLORS["baseline"], ls="--", lw=1)
ax_b.text(len(names) - 0.5, pos_test / n * 100 + 0.8, "多数类基线 63.3%", ha="right", fontsize=8.5, color="#555")
ax_b.set_xticks(range(len(names))); ax_b.set_xticklabels(names, fontsize=9)
ax_b.set_ylim(0, 80)
ax_b.set_ylabel("方向命中率（%）")
ax_b.set_title(f"二项检验（38/60）：vs 50% p = {p_vs_50:.3f}（错误基线）｜vs 63.3% 多数类 p = {p_vs_majority:.2f}｜vs 67.8% 训练期基线 p = {p_vs_train_base:.2f}",
               fontsize=10)

plot.save(fig, "L02_04_hit_rate",
          note="数据：spy_monthly_features_240m.csv（对数收益）· 三变量 OLS，train < 2021-07 冻结 · 命中 = sign(预测) == sign(实际) · 二项检验单侧 greater（scipy.stats.binomtest）")
