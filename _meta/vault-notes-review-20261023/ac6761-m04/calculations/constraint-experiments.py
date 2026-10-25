from __future__ import annotations

import json
import sqlite3
from pathlib import Path

OUT = Path(__file__).with_name("constraint-results.json")


def expect_error(conn, sql, params=()):
    try:
        conn.execute(sql, params)
        conn.commit()
        return None
    except sqlite3.IntegrityError as exc:
        conn.rollback()
        return str(exc)


evidence = {}

# Independent simplified as-of receivables example; not the note's Sale/SaleLine schema.
db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys = ON")
db.executescript(
    """
    CREATE TABLE Sale(
      saleID TEXT PRIMARY KEY,
      saleDate TEXT NOT NULL,
      amount NUMERIC NOT NULL CHECK(amount >= 0)
    );
    CREATE TABLE CashReceipt(
      receiptID TEXT PRIMARY KEY,
      receiptDate TEXT NOT NULL,
      amount NUMERIC NOT NULL CHECK(amount >= 0)
    );
    CREATE TABLE Duality(
      saleID TEXT NOT NULL REFERENCES Sale(saleID),
      receiptID TEXT NOT NULL REFERENCES CashReceipt(receiptID),
      amountApplied NUMERIC NOT NULL CHECK(amountApplied > 0),
      PRIMARY KEY(saleID, receiptID)
    );
    """
)
db.executemany("INSERT INTO Sale VALUES(?,?,?)", [("S1", "2013-01-01", 100), ("S2", "2013-01-02", 200)])
db.executemany(
    "INSERT INTO CashReceipt VALUES(?,?,?)",
    [("R1", "2013-01-03", 40), ("R2", "2013-01-04", 30), ("R3", "2013-02-01", 250), ("R4", "2013-01-04", 1000)],
)
db.executemany(
    "INSERT INTO Duality VALUES(?,?,?)",
    [("S1", "R1", 40), ("S1", "R2", 30), ("S1", "R3", 30), ("S2", "R3", 200)],
)
query = """
SELECT s.saleID, s.amount, COALESCE(a.applied,0) AS applied,
       s.amount-COALESCE(a.applied,0) AS AR
FROM Sale AS s
LEFT JOIN (
  SELECT d.saleID, SUM(d.amountApplied) AS applied
  FROM Duality AS d JOIN CashReceipt AS r ON d.receiptID=r.receiptID
  WHERE r.receiptDate<=:asof
  GROUP BY d.saleID
) AS a ON s.saleID=a.saleID
WHERE s.saleDate<=:asof
ORDER BY s.saleID;
"""
jan = db.execute(query, {"asof": "2013-01-31"}).fetchall()
feb = db.execute(query, {"asof": "2013-02-28"}).fetchall()
receipt_balances = db.execute(
    """
    SELECT r.receiptID, r.amount, COALESCE(SUM(d.amountApplied),0),
           r.amount-COALESCE(SUM(d.amountApplied),0)
    FROM CashReceipt r LEFT JOIN Duality d ON d.receiptID=r.receiptID
    GROUP BY r.receiptID, r.amount ORDER BY r.receiptID
    """
).fetchall()
evidence["asof_receivables"] = {
    "jan_rows": jan,
    "jan_total_ar": sum(row[3] for row in jan),
    "feb_rows": feb,
    "feb_total_ar": sum(row[3] for row in feb),
    "receipt_balances": receipt_balances,
}

# Step 4: one Sale may have multiple receipts; each receipt must have one Sale.
db2 = sqlite3.connect(":memory:")
db2.execute("PRAGMA foreign_keys = ON")
db2.executescript(
    """
    CREATE TABLE Sale(saleID TEXT PRIMARY KEY);
    CREATE TABLE CashReceipt(
      receiptID TEXT PRIMARY KEY,
      saleID TEXT NOT NULL REFERENCES Sale(saleID)
    );
    INSERT INTO Sale VALUES('S1');
    INSERT INTO CashReceipt VALUES('R1','S1');
    INSERT INTO CashReceipt VALUES('R2','S1');
    """
)
evidence["one_to_many"] = {
    "two_receipts_same_sale": db2.execute("SELECT * FROM CashReceipt ORDER BY receiptID").fetchall(),
    "null_sale_error": expect_error(db2, "INSERT INTO CashReceipt VALUES('R3',NULL)"),
    "orphan_sale_error": expect_error(db2, "INSERT INTO CashReceipt VALUES('R4','S9')"),
}

# One-to-one local constraints still do not force each parent to have a child.
db3 = sqlite3.connect(":memory:")
db3.execute("PRAGMA foreign_keys = ON")
db3.executescript(
    """
    CREATE TABLE Parent(id TEXT PRIMARY KEY);
    CREATE TABLE Child(
      id TEXT PRIMARY KEY,
      parentID TEXT NOT NULL UNIQUE REFERENCES Parent(id)
    );
    INSERT INTO Parent VALUES('P1');
    INSERT INTO Parent VALUES('P2');
    INSERT INTO Child VALUES('C1','P1');
    """
)
evidence["one_to_one"] = {
    "parent_without_child_is_allowed": db3.execute(
        "SELECT p.id FROM Parent p LEFT JOIN Child c ON c.parentID=p.id WHERE c.id IS NULL"
    ).fetchall(),
    "second_child_same_parent_error": expect_error(db3, "INSERT INTO Child VALUES('C2','P1')"),
}

# Composite PK/FK/positive amount does not enforce allocation totals.
db4 = sqlite3.connect(":memory:")
db4.execute("PRAGMA foreign_keys = ON")
db4.executescript(
    """
    CREATE TABLE Sale(id TEXT PRIMARY KEY, amount NUMERIC NOT NULL);
    CREATE TABLE Receipt(id TEXT PRIMARY KEY, amount NUMERIC NOT NULL);
    CREATE TABLE Allocation(
      saleID TEXT NOT NULL REFERENCES Sale(id),
      receiptID TEXT NOT NULL REFERENCES Receipt(id),
      amountApplied NUMERIC NOT NULL CHECK(amountApplied > 0),
      PRIMARY KEY(saleID, receiptID)
    );
    INSERT INTO Sale VALUES('S1',10);
    INSERT INTO Receipt VALUES('R1',1);
    INSERT INTO Allocation VALUES('S1','R1',5);
    """
)
evidence["over_allocation"] = {
    "rows_allowed_by_local_constraints": db4.execute("SELECT * FROM Allocation").fetchall(),
    "receipt_overallocated_by": db4.execute(
        "SELECT SUM(a.amountApplied)-r.amount FROM Receipt r JOIN Allocation a ON a.receiptID=r.id GROUP BY r.id"
    ).fetchone()[0],
}

evidence["load"] = {"950_of_1000": 950 / 1000, "30_of_1000": 30 / 1000}

# Current targeted clarification: a declared SQLite FK must also be enabled.
foreign_key_modes = []
for enabled in [False, True]:
    probe = sqlite3.connect(":memory:")
    probe.execute("PRAGMA foreign_keys=" + ("ON" if enabled else "OFF"))
    probe.executescript("CREATE TABLE P(id TEXT PRIMARY KEY); CREATE TABLE C(id TEXT PRIMARY KEY, pid TEXT REFERENCES P(id));")
    error = expect_error(probe, "INSERT INTO C VALUES('C1','missing-parent')")
    foreign_key_modes.append({"foreign_keys": enabled, "rejected_orphan": error is not None, "error": error})
    probe.close()
evidence["current_fk_mode_clarification"] = foreign_key_modes
evidence["engine"] = sqlite3.sqlite_version
evidence["rounding"] = {"two_of_three_pct": 2/3*100, "display_about_67": round(2/3*100), "three_of_four_pct":3/4*100}

OUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(evidence, ensure_ascii=False, indent=2))
