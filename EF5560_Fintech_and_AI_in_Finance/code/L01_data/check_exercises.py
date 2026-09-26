"""EF5560 M01 p.16（M02）、p.31、p.54 课堂题目的只读数据核对。

从课程原始 CSV 读取；不下载、不改写数据，也不把测试目标用于构造预测变量。
运行：D:\\anaconda3\\python.exe -X utf8 L01_data/check_exercises.py（工作目录 code/）
"""

import csv
from pathlib import Path


DATA = Path(__file__).resolve().parents[2] / "course_files_export" / "data"


def rows(name):
    with (DATA / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


spy = rows("spy_monthly_features_240m.csv")
top_five = sorted(spy, key=lambda row: abs(float(row["market_return"])), reverse=True)[:5]
print("M02 p.16 SPY 月度 market_return 绝对值前五（数据列为对数收益）：")
for row in top_five:
    print(row["forecast_month"], f'{float(row["market_return"]):+.3%}')

macro = rows("macro_240m.csv")
print("M01 p.31 课程宏观表中失业率或通胀缺失的月份：")
for row in macro:
    if not row["unemployment_rate"] or not row["inflation_yoy"]:
        print(row["month"], "UNRATE=", row["unemployment_rate"] or "缺失", "CPI_YOY=", row["inflation_yoy"] or "缺失")

aapl = {row["week_end"]: row for row in rows("aapl_weekly_prices_returns_156w.csv")}
known_price = float(aapl["2026-06-19"]["adjusted_close"])
lagged_price = float(aapl["2026-05-22"]["adjusted_close"])
momentum = known_price / lagged_price - 1
target = float(aapl["2026-06-26"]["weekly_return"])
print("M01 p.54 AAPL 4 周滞后动量示例：")
print("2026-06-19 / 2026-05-22 复权价：", known_price, lagged_price)
print("预测 2026-06-26 时已知的 4 周动量：", f"{momentum:+.3%}")
print("2026-06-26 后来实现的周收益（仅作事后核对）：", f"{target:+.3%}")
