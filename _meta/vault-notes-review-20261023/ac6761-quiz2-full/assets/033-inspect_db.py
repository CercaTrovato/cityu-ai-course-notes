from pathlib import Path
import pyodbc,json,hashlib,shutil
root=Path('E:/app-data/codex/scratchpad/ac6761-canvas-20261022')
src=root/'originals/ExampleTables1.accdb'
copy=root/'database-inspection.accdb'
shutil.copy2(src,copy)
con=pyodbc.connect(f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={copy};READONLY=1;',autocommit=True)
cur=con.cursor(); tables=[r.table_name for r in cur.tables(tableType='TABLE') if not r.table_name.startswith('MSys')]
report={'original_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'tables':{}}
for t in tables:
    cols=[{'name':r.column_name,'type':r.type_name} for r in cur.columns(table=t)]
    rows=cur.execute('SELECT * FROM ['+t.replace(']',']]')+']').fetchall()
    report['tables'][t]={'columns':cols,'count':len(rows),'sample':[[str(x) for x in r] for r in rows[:4]]}
if 'Sale' in tables:
    cols=[r['name'] for r in report['tables']['Sale']['columns']]
    report['sale_columns']=cols
    q='SELECT [Sale Number], [Amount], [SalesRepNumber] FROM [Sale] WHERE [SalesRepNumber] = ?'
    try: report['query_sql']=q; report['query_result']=[[str(x) for x in r] for r in cur.execute(q,'E-10').fetchall()]
    except Exception as e: report['query_error']=str(e)
con.close()
(root/'database-inspection.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
