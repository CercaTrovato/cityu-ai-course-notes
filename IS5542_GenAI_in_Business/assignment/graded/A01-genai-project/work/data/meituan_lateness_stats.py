"""Summarise real lateness in the Meituan INFORMS TSL waybill data (local copy, not redistributed).

Lateness = arrive_time - estimate_arrived_time, per order, in minutes.
Only orders that were grabbed and delivered (arrive_time > 0) and have a promised time are used.
Pre-booked orders are reported separately because their promised time works differently.
Output: a small JSON of aggregate statistics only (no order-level rows).
"""
import json
import sys
import zipfile

import pandas as pd

zip_path, out_path = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(zip_path) as z:
    with z.open("all_waybill_info_meituan_0322.csv") as f:
        df = pd.read_csv(f, usecols=[
            "dt", "order_id", "waybill_id", "is_courier_grabbed", "is_weekend", "is_prebook",
            "estimate_arrived_time", "arrive_time", "platform_order_time",
        ])

stats = {"waybill_rows": int(len(df)), "unique_orders": int(df["order_id"].nunique()),
         "dates": sorted(df["dt"].unique().tolist())}

# one row per order: keep the waybill that was grabbed and delivered
done = df[(df["is_courier_grabbed"] == 1) & (df["arrive_time"] > 0) & (df["estimate_arrived_time"] > 0)]
done = done.sort_values("arrive_time").drop_duplicates("order_id", keep="last")
stats["delivered_orders_with_promise"] = int(len(done))

def summarise(d):
    late_min = (d["arrive_time"] - d["estimate_arrived_time"]) / 60
    dur_min = (d["arrive_time"] - d["platform_order_time"]) / 60
    late = late_min[late_min > 0]
    return {
        "orders": int(len(d)),
        "share_late_any": round(float((late_min > 0).mean()), 4),
        "share_late_over_10min": round(float((late_min > 10).mean()), 4),
        "share_late_over_20min": round(float((late_min > 20).mean()), 4),
        "share_late_over_30min": round(float((late_min > 30).mean()), 4),
        "share_late_over_60min": round(float((late_min > 60).mean()), 4),
        "late_minutes_quantiles_among_late": {q: round(float(late.quantile(q)), 1) for q in (0.25, 0.5, 0.75, 0.9, 0.99)},
        "early_minutes_median_among_on_time": round(float((-late_min[late_min <= 0]).median()), 1),
        "order_to_arrival_minutes_quantiles": {q: round(float(dur_min.quantile(q)), 1) for q in (0.1, 0.5, 0.9)},
    }

stats["non_prebook"] = summarise(done[done["is_prebook"] == 0])
stats["prebook"] = summarise(done[done["is_prebook"] == 1])

np_ = done[done["is_prebook"] == 0].copy()
np_["hour"] = pd.to_datetime(np_["platform_order_time"], unit="s", utc=True).dt.tz_convert("Asia/Shanghai").dt.hour
np_["late30"] = (np_["arrive_time"] - np_["estimate_arrived_time"]) > 30 * 60
by_hour = np_.groupby("hour").agg(orders=("order_id", "size"), share_late_over_30min=("late30", "mean"))
stats["non_prebook_by_order_hour_beijing"] = {int(h): {"orders": int(r.orders), "share_late_over_30min": round(float(r.share_late_over_30min), 4)}
                                             for h, r in by_hour.iterrows()}
by_wk = np_.groupby("is_weekend")["late30"].mean()
stats["non_prebook_share_late_over_30min_by_weekend_flag"] = {int(k): round(float(v), 4) for k, v in by_wk.items()}

json.dump(stats, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps({k: v for k, v in stats.items() if k != "non_prebook_by_order_hour_beijing"}, ensure_ascii=False, indent=2))
