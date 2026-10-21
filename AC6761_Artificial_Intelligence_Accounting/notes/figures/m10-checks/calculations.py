from decimal import Decimal, getcontext
import json

getcontext().prec = 18
D = Decimal
data = {
    "revenue": D("1000"), "cogs": D("600"), "net_income": D("80"),
    "current_assets": D("300"), "inventory": D("100"),
    "prepaids": D("20"), "current_liabilities": D("150"),
    "total_debt": D("400"), "total_equity": D("500"),
    "ebit": D("120"), "interest": D("20"),
    "inventory_begin": D("90"), "inventory_end": D("110"),
    "ar_begin": D("40"), "ar_end": D("60"),
    "total_assets_begin": D("800"), "total_assets_end": D("1000"),
    "equity_begin": D("450"), "equity_end": D("550"),
    "working_capital": D("150"), "retained_earnings": D("200"),
    "market_equity": D("750"), "total_liabilities": D("500"),
    "share_price": D("30"), "eps": D("2"), "book_value_per_share": D("10"),
}
avg_inv = (data["inventory_begin"] + data["inventory_end"]) / 2
avg_ar = (data["ar_begin"] + data["ar_end"]) / 2
avg_assets = (data["total_assets_begin"] + data["total_assets_end"]) / 2
avg_equity = (data["equity_begin"] + data["equity_end"]) / 2
ratios = {
    "current_ratio_x": data["current_assets"] / data["current_liabilities"],
    "quick_ratio_x": (data["current_assets"] - data["inventory"] - data["prepaids"]) / data["current_liabilities"],
    "gross_margin_pct": (data["revenue"] - data["cogs"]) / data["revenue"] * 100,
    "roe_avg_pct": data["net_income"] / avg_equity * 100,
    "roa_avg_pct": data["net_income"] / avg_assets * 100,
    "debt_to_equity_x": data["total_debt"] / data["total_equity"],
    "interest_coverage_x": data["ebit"] / data["interest"],
    "inventory_turnover_x": data["cogs"] / avg_inv,
    "inventory_days_days": D(365) / (data["cogs"] / avg_inv),
    "receivables_turnover_x": data["revenue"] / avg_ar,
    "dso_days": D(365) / (data["revenue"] / avg_ar),
    "pe_x": data["share_price"] / data["eps"],
    "pb_x": data["share_price"] / data["book_value_per_share"],
    "dupont_margin": data["net_income"] / data["revenue"],
    "dupont_turnover": data["revenue"] / avg_assets,
    "dupont_equity_multiplier": avg_assets / avg_equity,
}
ratios["dupont_roe_pct"] = ratios["dupont_margin"] * ratios["dupont_turnover"] * ratios["dupont_equity_multiplier"] * 100
ratios["traditional_roe_pct"] = data["net_income"] / avg_equity * 100
ratios["z_score_classic"] = D("1.2") * (data["working_capital"] / data["total_assets_end"]) + D("1.4") * (data["retained_earnings"] / data["total_assets_end"]) + D("3.3") * (data["ebit"] / data["total_assets_end"]) + D("0.6") * (data["market_equity"] / data["total_liabilities"]) + (data["revenue"] / data["total_assets_end"])
z_parts = {
    "X1": data["working_capital"] / data["total_assets_end"],
    "X2": data["retained_earnings"] / data["total_assets_end"],
    "X3": data["ebit"] / data["total_assets_end"],
    "X4": data["market_equity"] / data["total_liabilities"],
    "X5": data["revenue"] / data["total_assets_end"],
}
z_weights = {"X1": D("1.2"), "X2": D("1.4"), "X3": D("3.3"), "X4": D("0.6"), "X5": D("1.0")}
z_contributions = {k: z_weights[k] * z_parts[k] for k in z_parts}
z_one_factor_shift = dict(z_parts)
z_one_factor_shift["X3"] = D("0.20")
z_shifted_score = sum(z_weights[k] * z_one_factor_shift[k] for k in z_parts)

# Scenario assumptions: 1,000 base revenue; 600 baseline COGS. The base case
# holds unit costs / COGS-to-sales constant. In the bear case, half of COGS is
# raw-material-sensitive; its price rises 20% while volume falls 10%.
scenario = {}
for name, growth in (("base", D("0.05")), ("bull", D("0.15")), ("bear", D("-0.10"))):
    revenue = D("1000") * (D("1") + growth)
    if name != "bear":
        cogs = D("600") * (D("1") + growth)
    else:
        volume_factor = D("0.90")
        non_material_cost = D("300") * volume_factor
        raw_material_cost = D("300") * volume_factor * D("1.20")
        cogs = non_material_cost + raw_material_cost
    gross_profit = revenue - cogs
    gross_margin_pct = gross_profit / revenue * 100
    cash_collections = revenue * D("0.90")
    ending_receivables = revenue * D("0.10")
    operating_cash_proxy = cash_collections - cogs
    scenario[name] = {
        "revenue": revenue, "cogs": cogs, "gross_profit": gross_profit,
        "gross_margin_pct": gross_margin_pct, "cash_collections": cash_collections,
        "ending_receivables": ending_receivables,
        "operating_cash_proxy_before_other_items": operating_cash_proxy,
    }
print(json.dumps({"input": {k: str(v) for k, v in data.items()}, "averages": {"inventory": str(avg_inv), "receivables": str(avg_ar), "assets": str(avg_assets), "equity": str(avg_equity)}, "outputs": {k: str(v) for k, v in ratios.items()}, "z_score_parts": {k: str(v) for k, v in z_parts.items()}, "z_score_contributions": {k: str(v) for k, v in z_contributions.items()}, "z_score_x3_changed_from_0_12_to_0_20": str(z_shifted_score), "scenarios": {name: {k: str(v) for k, v in values.items()} for name, values in scenario.items()}, "label": "笔记补充示例，虚构货币单位；仅用于复算，不是 Apple 数据"}, ensure_ascii=False, indent=2))
