from pathlib import Path
import json,sqlite3,hashlib
work=Path(__file__).parent;root=work/('recheck-'+__import__('datetime').datetime.now().strftime('%Y%m%d-%H%M%S'))
root.mkdir(parents=True,exist_ok=True)
data=json.loads((work/'Case4-source-data.json').read_text(encoding='utf-8'))
schema='''PRAGMA foreign_keys=ON;
CREATE TABLE Cashier(CashierNo TEXT PRIMARY KEY NOT NULL CHECK(length(trim(CashierNo))>0), Name TEXT NOT NULL);
CREATE TABLE CashReceipt(CashRNo TEXT PRIMARY KEY NOT NULL CHECK(length(trim(CashRNo))>0), Amount INTEGER NOT NULL, CashierNo TEXT NOT NULL REFERENCES Cashier(CashierNo));
CREATE TABLE Customer(CustomerID TEXT PRIMARY KEY NOT NULL CHECK(length(trim(CustomerID))>0), CustomerName TEXT NOT NULL, CustomerAge INTEGER NOT NULL);
CREATE TABLE Sale(SaleID TEXT PRIMARY KEY NOT NULL CHECK(length(trim(SaleID))>0), CustomerID TEXT NOT NULL REFERENCES Customer(CustomerID));
CREATE TABLE CustomerA(CustomerID TEXT PRIMARY KEY NOT NULL CHECK(length(trim(CustomerID))>0), CustomerName TEXT NOT NULL, CustomerAddress TEXT NOT NULL);
-- The following three tables are Q2 teaching examples, not supplied rows.
CREATE TABLE Purchase(PurchaseID TEXT PRIMARY KEY NOT NULL, SupplierID TEXT NOT NULL);
CREATE TABLE PurchaseReturn(ReturnID TEXT PRIMARY KEY NOT NULL);
CREATE TABLE ReturnLink(PurchaseID TEXT NOT NULL REFERENCES Purchase(PurchaseID), ReturnID TEXT NOT NULL REFERENCES PurchaseReturn(ReturnID), PRIMARY KEY(PurchaseID,ReturnID));
'''
dbpath=root/'Case4-关系模型核验.sqlite';assert not dbpath.exists(),dbpath
db=sqlite3.connect(dbpath);db.executescript(schema)
db.executemany('INSERT INTO Cashier VALUES(?,?)',data['cashiers'])
db.executemany('INSERT INTO CashReceipt VALUES(?,?,?)',data['cash_receipts'])
db.executemany('INSERT INTO Customer VALUES(?,?,?)',[(x[1],x[2],x[3]) for x in data['sales_raw']])
db.executemany('INSERT INTO Sale VALUES(?,?)',[(x[0],x[1]) for x in data['sales_raw']])
db.executemany('INSERT INTO CustomerA VALUES(?,?,?)',[r for r in data['customer_a'] if r[0] is not None])
db.executemany('INSERT INTO Purchase VALUES(?,?)',data['extra_q2_examples']['purchases'])
db.executemany('INSERT INTO PurchaseReturn VALUES(?)',data['extra_q2_examples']['returns'])
db.executemany('INSERT INTO ReturnLink VALUES(?,?)',data['extra_q2_examples']['links']);db.commit()
results=[]
def record(name,actual,expected):
    passed=actual==expected;results.append({'check':name,'actual':actual,'expected':expected,'passed':passed});assert passed,name
joined=db.execute('SELECT SaleID,s.CustomerID,CustomerName,CustomerAge FROM Sale s JOIN Customer c ON c.CustomerID=s.CustomerID ORDER BY s.rowid').fetchall()
record('Q3b拆分JOIN无损还原，保留两个Andy编号',[list(r) for r in joined],data['sales_raw'])
summary=db.execute('SELECT c.CashierNo,c.Name,COUNT(r.CashRNo),COALESCE(SUM(r.Amount),0) FROM Cashier c LEFT JOIN CashReceipt r ON r.CashierNo=c.CashierNo GROUP BY c.CashierNo,c.Name ORDER BY c.CashierNo').fetchall()
record('Q4五个收银员保留及分组汇总',[list(r) for r in summary],[['C1','F',2,500],['C2','G',0,0],['C3','H',0,0],['C4','I',0,0],['C5','J',2,500]])
record('Q4金额总数',db.execute('SELECT SUM(Amount) FROM CashReceipt').fetchone()[0],1000)
record('Q3a编号前导零保留',[r[0] for r in db.execute('SELECT CustomerID FROM CustomerA ORDER BY rowid')],['05233','05234','05235'])
def must_reject(name,sql,args):
    db.execute('SAVEPOINT negative_case')
    try:
        db.execute(sql,args)
    except sqlite3.IntegrityError:
        rejected=True
    else:rejected=False
    finally:
        db.execute('ROLLBACK TO negative_case');db.execute('RELEASE negative_case')
    record(name,rejected,True)
must_reject('Q3a Stephen主键NULL拒绝','INSERT INTO CustomerA VALUES(?,?,?)',[None,'Stephen','318 C street'])
must_reject('Q3a空字符串主键拒绝','INSERT INTO CustomerA VALUES(?,?,?)',['','Stephen','318 C street'])
must_reject('Q4悬空Cashier外键拒绝','INSERT INTO CashReceipt VALUES(?,?,?)',['R-X',1,'C-UNKNOWN'])
must_reject('Q4收款缺Cashier拒绝','INSERT INTO CashReceipt VALUES(?,?,?)',['R-X',1,None])
must_reject('Q4重复CashR主键拒绝','INSERT INTO CashReceipt VALUES(?,?,?)',['1',1,'C1'])
record('同名同龄可保留为不同客户',db.execute("SELECT COUNT(*) FROM Customer WHERE CustomerName='Andy' AND CustomerAge=21").fetchone()[0],2)
record('PK/FK整体检查',db.execute('PRAGMA foreign_key_check').fetchall(),[])
# Demonstrate why parent minimum participation is not guaranteed by ordinary FKs.
db.execute('SAVEPOINT orphan_demo');db.execute("INSERT INTO PurchaseReturn VALUES('R-EMPTY')")
orphans=[r[0] for r in db.execute('SELECT h.ReturnID FROM PurchaseReturn h LEFT JOIN ReturnLink l ON l.ReturnID=h.ReturnID GROUP BY h.ReturnID HAVING COUNT(l.PurchaseID)=0')]
record('Q2无关联退货头需业务核对（FK不自动防止）',orphans,['R-EMPTY'])
db.execute('ROLLBACK TO orphan_demo');db.execute('RELEASE orphan_demo')
db.commit();db.close()
(root/'Case4-schema.sql').write_text(schema,encoding='utf-8')
out={'checks':results,'cashier_summary':[list(r) for r in summary],'checks_passed':len(results),'currency':'not specified by question','q2_example_is_supplement':True,'official_solution_verified':False}
(root/'Case4-核验结果.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
# All rebuilt results are written to the new recheck folder.
(root/'Case4-source-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'checks_passed':len(results),'cashier_summary':out['cashier_summary'],'amount_total':1000},ensure_ascii=False))
