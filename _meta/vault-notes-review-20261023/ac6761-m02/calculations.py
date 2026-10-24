import json
from collections import defaultdict
from pathlib import Path


OUT = Path(__file__).resolve().parent / "recompute-results.json"


def run(name, entries):
    ledger = defaultdict(lambda: {"debit": [], "credit": []})
    for tx, debits, credits in entries:
        assert sum(v for _, v in debits) == sum(v for _, v in credits), tx
        for account, amount in debits:
            ledger[account]["debit"].append([tx, amount])
        for account, amount in credits:
            ledger[account]["credit"].append([tx, amount])
    balances = {}
    for account, sides in ledger.items():
        dr = sum(v for _, v in sides["debit"])
        cr = sum(v for _, v in sides["credit"])
        balances[account] = {
            **sides,
            "debit_total": dr,
            "credit_total": cr,
            "signed_dr_minus_cr": dr - cr,
            "side": "Dr" if dr > cr else "Cr" if cr > dr else "zero",
            "amount": abs(dr - cr),
        }
    tb_dr = sum(v["amount"] for v in balances.values() if v["side"] == "Dr")
    tb_cr = sum(v["amount"] for v in balances.values() if v["side"] == "Cr")
    assert tb_dr == tb_cr
    return {"name": name, "entries": entries, "ledger": balances, "trial_balance": {"debit": tb_dr, "credit": tb_cr}}


ff = [
    (1, [("Cash", 30000)], [("Common Stock", 30000)]),
    (2, [("Supplies", 2500)], [("Cash", 2500)]),
    (3, [("Equipment", 26000)], [("Cash", 26000)]),
    (4, [("Supplies", 7100)], [("Accounts Payable", 7100)]),
    (5, [("Cash", 4200)], [("Consulting Revenue", 4200)]),
    (6, [("Rent Expense", 1000)], [("Cash", 1000)]),
    (7, [("Salaries Expense", 700)], [("Cash", 700)]),
    (8, [("Accounts Receivable", 1900)], [("Consulting Revenue", 1600), ("Rental Revenue", 300)]),
    (9, [("Cash", 1900)], [("Accounts Receivable", 1900)]),
    (10, [("Accounts Payable", 900)], [("Cash", 900)]),
    (11, [("Dividends", 200)], [("Cash", 200)]),
    (12, [("Cash", 3000)], [("Unearned Consulting Revenue", 3000)]),
    (13, [("Prepaid Insurance", 2400)], [("Cash", 2400)]),
    (14, [("Supplies", 120)], [("Cash", 120)]),
    (15, [("Utilities Expense", 305)], [("Cash", 305)]),
    (16, [("Salaries Expense", 700)], [("Cash", 700)]),
]

gtech = [
    (1, [("Cash", 40000)], [("Owner's Capital", 40000)]),
    (2, [("Prepaid Rent", 24000)], [("Cash", 24000)]),
    (3, [("Equipment", 8000)], [("Cash", 8000)]),
    (4, [("Office Supplies", 1500)], [("Accounts Payable", 1500)]),
    (5, [("Cash", 9000)], [("Service Revenue", 9000)]),
    (6, [("Accounts Receivable", 6000)], [("Service Revenue", 6000)]),
    (7, [("Utilities Expense", 800)], [("Cash", 800)]),
    (8, [("Accounts Payable", 1000)], [("Cash", 1000)]),
    (9, [("Owner's Withdraw", 2000)], [("Cash", 2000)]),
    (10, [("Cash", 4000)], [("Accounts Receivable", 4000)]),
    (11, [("Rent Expense", 2000)], [("Prepaid Rent", 2000)]),
    (12, [("Supplies Expense", 1100)], [("Office Supplies", 1100)]),
]

quiz1 = [
    (1, [("Cash", 8000)], [("Owner's Capital", 8000)]),
    (2, [("Prepaid Rent", 1800)], [("Cash", 1800)]),
    (3, [("Equipment", 1200)], [("Cash", 1200)]),
    (4, [("Supplies", 350)], [("Accounts Payable", 350)]),
    (5, [("Cash", 1500)], [("Service Revenue", 1500)]),
    (6, [("Accounts Receivable", 700)], [("Service Revenue", 700)]),
    (7, [("Advertising Expense", 150)], [("Cash", 150)]),
    (8, [("Accounts Payable", 350)], [("Cash", 350)]),
    (9, [("Owner's Withdraw", 400)], [("Cash", 400)]),
    (10, [("Cash", 700)], [("Accounts Receivable", 700)]),
    (11, [("Rent Expense", 600)], [("Prepaid Rent", 600)]),
    (12, [("Supplies Expense", 230)], [("Supplies", 230)]),
]


result = {
    "FastForward": run("FastForward", ff),
    "GTech": run("GTech", gtech),
    "Quiz1": run("Quiz1", quiz1),
}

ffb = result["FastForward"]["ledger"]
result["FastForward"]["statements"] = {
    "assets": sum(ffb[a]["amount"] for a in ["Cash", "Accounts Receivable", "Supplies", "Prepaid Insurance", "Equipment"]),
    "liabilities": sum(ffb[a]["amount"] for a in ["Accounts Payable", "Unearned Consulting Revenue"]),
    "revenue": ffb["Consulting Revenue"]["amount"] + ffb["Rental Revenue"]["amount"],
    "expenses": ffb["Rent Expense"]["amount"] + ffb["Salaries Expense"]["amount"] + ffb["Utilities Expense"]["amount"],
    "dividends": ffb["Dividends"]["amount"],
}
result["FastForward"]["statements"]["net_income"] = result["FastForward"]["statements"]["revenue"] - result["FastForward"]["statements"]["expenses"]
result["FastForward"]["cash_flows"] = {"CFO": 9100 - 3520 - 2400 - 1000 - 1400 - 305, "CFI": -26000, "CFF": 30000 - 200}

gtb = result["GTech"]["ledger"]
result["GTech"]["statements"] = {
    "assets": sum(gtb[a]["amount"] for a in ["Cash", "Accounts Receivable", "Prepaid Rent", "Office Supplies", "Equipment"]),
    "liabilities": gtb["Accounts Payable"]["amount"],
    "revenue": gtb["Service Revenue"]["amount"],
    "expenses": gtb["Rent Expense"]["amount"] + gtb["Utilities Expense"]["amount"] + gtb["Supplies Expense"]["amount"],
    "withdraw": gtb["Owner's Withdraw"]["amount"],
}
result["GTech"]["statements"]["net_income"] = result["GTech"]["statements"]["revenue"] - result["GTech"]["statements"]["expenses"]
result["GTech"]["cash_flows"] = {"CFO": 13000 - 24000 - 800 - 1000, "CFI": -8000, "CFF": 40000 - 2000}

assert result["FastForward"]["statements"] == {"assets": 42395, "liabilities": 9200, "revenue": 6100, "expenses": 2705, "dividends": 200, "net_income": 3395}
assert result["FastForward"]["cash_flows"] == {"CFO": 475, "CFI": -26000, "CFF": 29800}
assert result["GTech"]["statements"] == {"assets": 49600, "liabilities": 500, "revenue": 15000, "expenses": 3900, "withdraw": 2000, "net_income": 11100}
assert result["GTech"]["cash_flows"] == {"CFO": -12800, "CFI": -8000, "CFF": 38000}
assert result["Quiz1"]["trial_balance"] == {"debit": 10200, "credit": 10200}

OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k: {"trial_balance": v["trial_balance"], "balances": {a: {"side": b["side"], "amount": b["amount"]} for a, b in v["ledger"].items()}} for k, v in result.items()}, ensure_ascii=False, indent=2))
