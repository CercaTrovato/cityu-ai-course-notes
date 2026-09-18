"""
common.load · 统一数据入口
===========================
所有脚本只能从这里读数据。每个 loader 做三件事：
  1. 路径固定相对 code/，脚本从哪启动都能找到
  2. 日期列 → datetime（原文件全是字符串，直接排序会按字典序）
  3. 在 docstring 里写死收益率口径，脚本里不许再猜

八个文件的口径（来自 _meta/数据集卡片.md，全部实跑验证过）：
  周频文件 ①③          → 简单收益  P_t/P_{t-1} - 1
  月频文件 ⑤⑦⑧        → 对数收益  ln(P_t/P_{t-1})
  ②④⑥ 是价格/水平量，没有收益列
"""
from pathlib import Path
import pandas as pd

# code/common/load.py → code/ → EF5560_Fintech_and_AI_in_Finance/ → course_files_export/data/
DATA_DIR = Path(__file__).resolve().parents[2] / "course_files_export" / "data"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def _read(name: str, date_col: str) -> pd.DataFrame:
    """读 csv，日期列转 datetime 并设为索引、按时间排序。"""
    p = DATA_DIR / name
    if not p.exists():
        raise FileNotFoundError(f"找不到数据文件：{p}\n（course_files_export/data/ 是只读原始目录，不要移动它）")
    df = pd.read_csv(p)
    df[date_col] = pd.to_datetime(df[date_col])
    return df.set_index(date_col).sort_index()


# ---------- ① 周频 · AAPL ----------
def aapl_weekly() -> pd.DataFrame:
    """aapl_weekly_prices_returns_156w.csv
    157 行 × 2 列（索引 week_end）。周五收盘。
    列：adjusted_close（复权收盘价）、weekly_return（**简单收益**，首行 NaN）。
    对应讲义 Lec01 p.14 的三行手检清单：157 价格 / 156 收益 / 首行缺失。
    """
    df = _read("aapl_weekly_prices_returns_156w.csv", "week_end")
    return df


# ---------- ② 日频 · PDD / JD 收盘价 ----------
def pdd_jd_daily() -> pd.DataFrame:
    """pdd_jd_daily_close_2023-06-26_2026-06-26.csv
    754 行 × 2 列（索引 date）。纯交易日。列：PDD、JD（收盘价，**未注明是否复权**）。
    """
    return _read("pdd_jd_daily_close_2023-06-26_2026-06-26.csv", "date")


# ---------- ③ 周频 · PDD-JD 配对交易 ----------
def pdd_jd_pair() -> pd.DataFrame:
    """pdd_jd_pair_example_156w.csv
    157 行 × 8 列（索引 week）。**简单收益**。
    列：pdd_close, jd_close, pdd_return, jd_return, pdd_weight, jd_weight（恒为 ±0.5）,
        long_pdd_short_jd_return（组合周收益）, long_pdd_short_jd_wealth（累计净值，从 1 起）。
    讲义 Lec01 p.16 只报了终点 +20.62%；最大回撤 −38.66% 讲义没报。
    """
    return _read("pdd_jd_pair_example_156w.csv", "week")


# ---------- ④ 月频 · 四指数价格 ----------
def index_prices() -> pd.DataFrame:
    """market_index_prices_240m.csv
    240 行 × 4 列（索引 month），2006-07 → 2026-06。
    列：US_S&P500（价格指数，不含股息）、HK_HangSeng、US_SPY（含股息）、CN_CSI300。
    ⚠️ 列名 `US_S&P500` 带 & 符号，用 df["US_S&P500"] 取。
    ⚠️ SP500 与 SPY 的差异就是股息：20 年 5.87× vs 8.44×。
    """
    return _read("market_index_prices_240m.csv", "month")


# ---------- ⑤ 月频 · 四指数收益 ----------
def index_returns() -> pd.DataFrame:
    """market_index_returns_240m.csv
    240 行 × 4 列（索引 month，列名同 ④）。**对数收益** ln(P_t/P_{t-1})，与 ④ 逐月对应（误差 1.6e-15）。
    ⚠️ **首行不是 NaN**：2006-07 那行是 2006-06→07 的真实收益（用了一个价格文件里没有的 2006-06 价格）。
       所以 240 行就是 240 个收益，比价格文件多算一期。要与价格净值 P_t/P_{2006-07} 对齐，
       累加前把第 0 行置 0（L01_01 就是这么做的）；否则 exp(Σr) 会比价格净值高出 exp(r_0)≈0.5%。
    ⚠️ 讲义 p.19 只给了简单收益公式——用它去复利这份数据会算错，见 L01_01。
    """
    return _read("market_index_returns_240m.csv", "month")


# ---------- ⑥ 月频 · 宏观 ----------
def macro() -> pd.DataFrame:
    """macro_240m.csv
    240 行 × 5 列（索引 month）。水平量，无收益列。
    列：dgs10_monthly_mean（10 年期国债）、dff_monthly_mean（联邦基金利率）、unemployment_rate、inflation_yoy、
        term_spread（= dgs10 − dff）。
    ⚠️ 2025-10 有一个月缺失（失业率 + 通胀），文件如实留空，未插值。
    """
    return _read("macro_240m.csv", "month")


# ---------- ⑦ 月频 · SPY 特征表（本课主力） ----------
def spy_features() -> pd.DataFrame:
    """spy_monthly_features_240m.csv
    240 行 × 16 列（索引 forecast_month）。
    目标 y = market_return（SPY 当月**对数收益**）。
    16 个非日期列 = 目标 market_return + 15 个预测变量；15 个预测变量全部只用 forecast_month 之前的信息（L01_04 逐列验算，误差 ≤ 2e-15）：
      return_lag1/2/3 · momentum_3/6/12 · volatility_3/6/12（年化，样本标准差）
      ma_gap_3/6/10 · term_spread_lag1 · unemployment_lag2 · inflation_yoy_lag2
    ⚠️ momentum 用价格算，不是收益连乘；⚠️ 2025-12 那行两个宏观特征缺失。
    """
    return _read("spy_monthly_features_240m.csv", "forecast_month")


# ---------- ⑧ 月频 · CSI300 宏观面板 ----------
def csi300_panel() -> pd.DataFrame:
    """csi300_macro_panel.csv
    240 行 × 6 列（索引 forecast_month）。**对数收益**。
    目标 market_return；benchmark_ma12 = market_return.shift(1).rolling(12).mean()（前 12 行 NaN）；
    cli_gap_lag2 含义文件未说明。
    """
    return _read("csi300_macro_panel.csv", "forecast_month")


# ---------- ⑨–⑬ class03 数据包（Lec03，2026-09-17） ----------
# course_files_export/class03/class03/：五个"结果表"，不是原始面板。原始面板在 README 引用的 ../shared/（导出包缺失）。
CLASS03_DIR = Path(__file__).resolve().parents[2] / "course_files_export" / "class03" / "class03"


def _read03(name: str, date_col=None) -> pd.DataFrame:
    p = CLASS03_DIR / name
    if not p.exists():
        raise FileNotFoundError(f"找不到 class03 文件：{p}")
    df = pd.read_csv(p)
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
    return df


def c03_market_summary() -> pd.DataFrame:
    """market_linear_model_summary.csv · 15 行 × 9 列。三个市场 × {MA(12), OLS, Ridge, LASSO, Elastic Net}。
    validation_mse / test_mse 为小数平方（讲义 ×10⁴ 显示）；oos_r2 对滞后 MA(12)（小数，讲义显示 %）；
    alpha = 软件惩罚参数（scikit-learn 尺度，= n·λ）；MA(12) 行的 validation_mse / alpha 为 NaN。"""
    return _read03("market_linear_model_summary.csv")


def c03_market_predictions() -> pd.DataFrame:
    """market_linear_test_predictions.csv · 180 行 × 8 列 = 60 个测试月 × 3 市场（2021-07-31 → 2026-06-30）。
    actual = 月度**超额**收益（小数）；MA(12) = 滞后 12 月超额收益均值（基准）；OLS/Ridge/LASSO/Elastic Net = 各模型预测。"""
    return _read03("market_linear_test_predictions.csv", "forecast_month")


def c03_stock_summary() -> pd.DataFrame:
    """stock_linear_model_summary.csv · 7 行 × 9 列。恒指面板 {Zero, OLS, Ridge, LASSO, Elastic Net, PCR, PLS}。
    oos_r2 对零超额收益；PCR/PLS 的 alpha 列存的是成分数 K；LASSO/EN 的 nonzero_coefficients = 0（常数预测）。"""
    return _read03("stock_linear_model_summary.csv")


def c03_stock_predictions() -> pd.DataFrame:
    """stock_linear_test_predictions.csv · 4,108 行 × 17 列 = 52 个测试周 × 79 只恒指成分股（2025-07-04 → 2026-06-26）。
    actual = stock_return − risk_free_return（周**超额**收益，小数）；risk_free_return ≈ risk_free_yield_pct/100/52；
    Zero…PLS = 各模型预测；predicted_excess_return = 验证选中模型（PCR）的预测；forecast_quintile = 按它分的五组。"""
    return _read03("stock_linear_test_predictions.csv", "forecast_week")


def c03_stock_spreads() -> pd.DataFrame:
    """stock_linear_forecast_spreads.csv · 6 行 × 11 列。每个模型按预测分五组后的 Q5−Q1 周价差、t 值、年化夏普、命中率、前后半段均值。
    sortable = False 的行（LASSO、Elastic Net）是常数预测，无法分组。"""
    return _read03("stock_linear_forecast_spreads.csv")


# ---------- 汇总 ----------
ALL = {
    "aapl_weekly": aapl_weekly,
    "pdd_jd_daily": pdd_jd_daily,
    "pdd_jd_pair": pdd_jd_pair,
    "index_prices": index_prices,
    "index_returns": index_returns,
    "macro": macro,
    "spy_features": spy_features,
    "csi300_panel": csi300_panel,
    "c03_market_summary": c03_market_summary,
    "c03_market_predictions": c03_market_predictions,
    "c03_stock_summary": c03_stock_summary,
    "c03_stock_predictions": c03_stock_predictions,
    "c03_stock_spreads": c03_stock_spreads,
}

if __name__ == "__main__":
    # 自检：八个文件都能读、日期都是 datetime、行数与数据集卡片一致
    expect = {"aapl_weekly": 157, "pdd_jd_daily": 754, "pdd_jd_pair": 157, "index_prices": 240,
              "index_returns": 240, "macro": 240, "spy_features": 240, "csi300_panel": 240,
              "c03_market_summary": 15, "c03_market_predictions": 180, "c03_stock_summary": 7,
              "c03_stock_predictions": 4108, "c03_stock_spreads": 6}
    for k, fn in ALL.items():
        df = fn()
        if k.startswith("c03_"):
            ok = "✅" if len(df) == expect[k] else "❌"
            print(f"{ok} {k:22s} {len(df):4d} 行 × {df.shape[1]:2d} 列  (class03 结果表)")
            continue
        ok = "✅" if len(df) == expect[k] and str(df.index.dtype).startswith("datetime") else "❌"
        print(f"{ok} {k:22s} {len(df):4d} 行 × {df.shape[1]:2d} 列  {df.index.min().date()} → {df.index.max().date()}")
