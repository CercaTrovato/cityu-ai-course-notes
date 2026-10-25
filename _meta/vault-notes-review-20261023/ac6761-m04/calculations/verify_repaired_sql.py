import pathlib,re,sqlite3,json,hashlib,subprocess,sys
P=pathlib.Path(__file__).parent;c=P/'candidate-repaired-v1.md';t=c.read_text(encoding='utf-8');s=t.split('#### 2.9.9 ',1)[1].split('### 2.10 ',1)[0]
blocks=re.findall(r'```sql\n(.*?)```',s,re.S);assert len(blocks)==5
db=sqlite3.connect(':memory:');db.executescript(blocks[0]);db.executescript(blocks[1])
cookie=db.execute(blocks[2]).fetchall();ar={date:db.execute(blocks[3],{'asof':date}).fetchall() for date in ['2013-01-31','2013-02-28']};bal=db.execute(blocks[4]).fetchall()
probes=[]
for table in ['Inventory','Employee','Customer','CashAccount','Sale','CashReceipt']:
 values=list(db.execute('SELECT * FROM '+table+' LIMIT 1').fetchone());values[0]=None
 try:db.execute('INSERT INTO '+table+' VALUES('+','.join('?' for x in values)+')',values);probes.append({'table':table,'null_rejected':False})
 except sqlite3.IntegrityError as e:probes.append({'table':table,'null_rejected':True,'error':str(e)})
assert cookie==[('S001','Cookie','Paul','Joe',1,10,8)]
assert sum(x[3] for x in ar['2013-01-31'])==230 and sum(x[3] for x in ar['2013-02-28'])==0
assert [x[3] for x in bal]==[0,0,20,1000] and all(x['null_rejected'] for x in probes)
result={'candidate_sha256':hashlib.sha256(c.read_bytes()).hexdigest(),'sqlite_version':sqlite3.sqlite_version,'exact_printed_sql_blocks':5,'cookie':cookie,'AR':ar,'balances':bal,'six_null_pk_probes':probes,'limits':'Teaching input, not live course database; does not certify Access or cross-row money constraints'}
(P/'repaired-sql-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
