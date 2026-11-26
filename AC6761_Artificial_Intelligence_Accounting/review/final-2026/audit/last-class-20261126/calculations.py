from fractions import Fraction
from pathlib import Path
import json,sqlite3
R=Path(__file__).resolve().parent
A=[2000000,1000000,500000,1500000,1000000]
B=[25000000,10000000,3000000,12000000,20000000]
out={'common_size':{'A_total_assets':sum(A[:2]),'B_total_assets':sum(B[:2]),'A':[round(float(Fraction(v,sum(A[:2]))*100),1) for v in A],'B':[round(float(Fraction(v,sum(B[:2]))*100),1) for v in B]},'nike_margin':{'2014':float(Fraction(2693,27799)*100),'2016':float(Fraction(3760,32376)*100)},'supplement_margin':[10,8]}
db=sqlite3.connect(':memory:')
db.execute('create table cash_receipt(id text,amount integer,bank text,date text,customer text,cashier text)')
db.executemany('insert into cash_receipt values(?,?,?,?,?,?)',[('RA-1',1666,'BA-6','25 July','C-2','E-39'),('RA-2',10000,'BA-7','26 July','C-2','E-39'),('RA-3',7200,'BA-7','15 Aug','C-1','E-39'),('RA-4',32600,'BA-7','15 Aug','C-5','E-39'),('RA-5',1666,'BA-6','25 Aug','C-2','E-39')])
out['customer_C2']=db.execute("select * from cash_receipt where customer='C-2'").fetchall()
db.execute('create table sale(id text,amount integer,month integer,day integer,rep text)')
db.executemany('insert into sale values(?,?,?,?,?)',[('S-1',7200,7,1,'E-12'),('S-2',10000,7,21,'E-10'),('S-3',16000,7,22,'E-10'),('S-4',10000,7,26,'E-10'),('S-5',16600,7,31,'E-10'),('S-6',35000,8,15,'E-10'),('S-7',23000,8,21,'E-99')])
out['not_E10']=db.execute("select id,amount from sale where rep<>'E-10'").fetchall()
out['variant_AND']=db.execute("select id,amount from sale where rep<>'E-10' AND amount>=10000").fetchall()
out['July']=db.execute('select id,amount,day from sale where month=7 and day between 1 and 31').fetchall()
out['limits']='Computed using exact fractions and SQLite in-memory semantic checks, not a live Access database run. Given Access syntax corrections are separately sourced.'
(R/'calculations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
