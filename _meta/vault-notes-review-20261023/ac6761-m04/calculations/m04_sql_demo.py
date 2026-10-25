import sqlite3

# 输入：以下完整自拟教学表；内存库每次运行从空库开始。
db = sqlite3.connect(':memory:')
schema_sql = r"""PRAGMA foreign_keys = ON;
CREATE TABLE Inventory(itemID TEXT NOT NULL PRIMARY KEY, description TEXT NOT NULL, currentReferenceCost NUMERIC NOT NULL);
CREATE TABLE Employee(empID TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE Customer(custID TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE CashAccount(cashAccountID TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE Sale(
  saleID TEXT NOT NULL PRIMARY KEY, saleDate TEXT NOT NULL, location TEXT NOT NULL,
  empID TEXT NOT NULL REFERENCES Employee(empID),
  custID TEXT NOT NULL REFERENCES Customer(custID)
);
CREATE TABLE SaleLine(
  saleID TEXT NOT NULL REFERENCES Sale(saleID), lineNo INTEGER NOT NULL,
  itemID TEXT NOT NULL REFERENCES Inventory(itemID), quantity NUMERIC NOT NULL CHECK(quantity>0),
  unitPrice NUMERIC NOT NULL CHECK(unitPrice>=0), unitCost NUMERIC NOT NULL CHECK(unitCost>=0),
  PRIMARY KEY(saleID,lineNo)
);
CREATE TABLE CashReceipt(
  receiptID TEXT NOT NULL PRIMARY KEY, receiptDate TEXT NOT NULL, amount NUMERIC NOT NULL CHECK(amount>=0),
  cashAccountID TEXT NOT NULL REFERENCES CashAccount(cashAccountID),
  empID TEXT NOT NULL REFERENCES Employee(empID), custID TEXT NOT NULL REFERENCES Customer(custID)
);
CREATE TABLE Duality(
  saleID TEXT NOT NULL REFERENCES Sale(saleID),
  receiptID TEXT NOT NULL REFERENCES CashReceipt(receiptID),
  amountApplied NUMERIC NOT NULL CHECK(amountApplied>0),
  PRIMARY KEY(saleID,receiptID)
);"""
input_sql = r"""INSERT INTO Inventory VALUES ('C01','Cookie',8),('X01','Example item',0);
INSERT INTO Employee VALUES ('E01','Paul');
INSERT INTO Customer VALUES ('U01','Joe');
INSERT INTO CashAccount VALUES ('CA01','Store cash');
INSERT INTO Sale VALUES
 ('S001','2013-01-01','Festival Walk 7-11','E01','U01'),
 ('S1','2013-01-02','Example','E01','U01'),
 ('S2','2013-01-03','Example','E01','U01');
INSERT INTO SaleLine VALUES
 ('S001',1,'C01',1,10,8),('S1',1,'X01',1,100,0),('S2',1,'X01',1,200,0);
INSERT INTO CashReceipt VALUES
 ('R001','2013-01-01',10,'CA01','E01','U01'),
 ('R1','2013-01-03',40,'CA01','E01','U01'),
 ('R2','2013-01-04',30,'CA01','E01','U01'),
 ('R3','2013-02-01',250,'CA01','E01','U01'),
 ('R4','2013-01-04',1000,'CA01','E01','U01');
INSERT INTO Duality VALUES
 ('S001','R001',10),('S1','R1',40),('S1','R2',30),('S1','R3',30),('S2','R3',200);"""
cookie_sql = r"""SELECT s.saleID, i.description, e.name AS employee, c.name AS customer,
       sl.quantity,
       sl.quantity*sl.unitPrice AS revenue,
       sl.quantity*sl.unitCost AS cost
FROM Sale AS s
JOIN SaleLine AS sl ON sl.saleID=s.saleID
JOIN Inventory AS i ON i.itemID=sl.itemID
JOIN Employee AS e ON e.empID=s.empID
JOIN Customer AS c ON c.custID=s.custID
WHERE s.saleID='S001';"""
ar_sql = r"""WITH sale_total AS (
  SELECT s.saleID, s.saleDate, SUM(sl.quantity*sl.unitPrice) AS saleAmount
  FROM Sale AS s JOIN SaleLine AS sl ON sl.saleID=s.saleID
  WHERE s.saleDate<=:asof
    AND s.saleID IN ('S1','S2')
  GROUP BY s.saleID, s.saleDate
), applied AS (
  SELECT d.saleID, SUM(d.amountApplied) AS appliedAmount
  FROM Duality AS d
  JOIN CashReceipt AS r ON r.receiptID=d.receiptID
  WHERE r.receiptDate<=:asof
  GROUP BY d.saleID
)
SELECT st.saleID, st.saleAmount, COALESCE(a.appliedAmount,0) AS applied,
       st.saleAmount-COALESCE(a.appliedAmount,0) AS accountsReceivable
FROM sale_total AS st
LEFT JOIN applied AS a ON a.saleID=st.saleID
ORDER BY st.saleID;"""
balance_sql = r"""SELECT r.receiptID, r.amount, COALESCE(SUM(d.amountApplied),0) AS applied,
       r.amount-COALESCE(SUM(d.amountApplied),0) AS unapplied
FROM CashReceipt AS r
LEFT JOIN Duality AS d ON d.receiptID=r.receiptID
WHERE r.receiptID IN ('R1','R2','R3','R4')
GROUP BY r.receiptID, r.amount
ORDER BY r.receiptID;"""
db.executescript(schema_sql)
db.executescript(input_sql)
print('cookie:', db.execute(cookie_sql).fetchall())
for cutoff in ['2013-01-31', '2013-02-28']:
    rows = db.execute(ar_sql, {'asof': cutoff}).fetchall()
    print(cutoff, rows, 'total AR:', sum(row[3] for row in rows))
print('receipt balances:', db.execute(balance_sql).fetchall())
db.close()
