PRAGMA foreign_keys=ON;
CREATE TABLE Cashier(CashierNo TEXT PRIMARY KEY NOT NULL CHECK(length(trim(CashierNo))>0), Name TEXT NOT NULL);
CREATE TABLE CashReceipt(CashRNo TEXT PRIMARY KEY NOT NULL CHECK(length(trim(CashRNo))>0), Amount INTEGER NOT NULL, CashierNo TEXT NOT NULL REFERENCES Cashier(CashierNo));
CREATE TABLE Customer(CustomerID TEXT PRIMARY KEY NOT NULL CHECK(length(trim(CustomerID))>0), CustomerName TEXT NOT NULL, CustomerAge INTEGER NOT NULL);
CREATE TABLE Sale(SaleID TEXT PRIMARY KEY NOT NULL CHECK(length(trim(SaleID))>0), CustomerID TEXT NOT NULL REFERENCES Customer(CustomerID));
CREATE TABLE CustomerA(CustomerID TEXT PRIMARY KEY NOT NULL CHECK(length(trim(CustomerID))>0), CustomerName TEXT NOT NULL, CustomerAddress TEXT NOT NULL);
-- The following three tables are Q2 teaching examples, not supplied rows.
CREATE TABLE Purchase(PurchaseID TEXT PRIMARY KEY NOT NULL, SupplierID TEXT NOT NULL);
CREATE TABLE PurchaseReturn(ReturnID TEXT PRIMARY KEY NOT NULL);
CREATE TABLE ReturnLink(PurchaseID TEXT NOT NULL REFERENCES Purchase(PurchaseID), ReturnID TEXT NOT NULL REFERENCES PurchaseReturn(ReturnID), PRIMARY KEY(PurchaseID,ReturnID));
