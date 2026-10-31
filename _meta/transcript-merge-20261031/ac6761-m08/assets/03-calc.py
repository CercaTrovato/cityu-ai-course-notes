from pathlib import Path
import json, hashlib
from fractions import Fraction as F
from collections import defaultdict
from datetime import datetime

ROOT=Path('E:/app-data/codex/scratchpad/cityu-audio-batch-20261031')
OUT=ROOT/'author-ac6761'
d=json.loads((ROOT/'sources/ac6761-example-tables.json').read_text(encoding='utf-8-sig'))
sales={x['SaleNumber']:x for x in d['Sale']}
cust={x['CustomerNumber']:x for x in d['Customer']}
inv={x['ItemID']:x for x in d['Inventory']}
cash={x['RemittanceAdviceNumber']:x for x in d['CashReceipt']}
links=d['Sale-CashRecDuality']; sf=d['Inventory-SaleStockflow']
lag=[]
for l in links:
 s=sales[l['SaleNumber']]; r=cash[l['RemittanceAdviceNumber']]
 lag.append(dict(customer=s['CustomerNumber'],name=cust[s['CustomerNumber']]['Name'],sale=s['SaleNumber'],receipt=r['RemittanceAdviceNumber'],sale_date=s['Date'][:10],receipt_date=r['Date'][:10],lag_days=(datetime.fromisoformat(r['Date'])-datetime.fromisoformat(s['Date'])).days,applied=l['Applied']))
ct=defaultdict(float); pt=defaultdict(float); qty=defaultdict(int); st=defaultdict(float)
for s in sales.values():ct[s['CustomerNumber']]+=s['Amount']
for l in sf:
 amount=l['Quantity']*l['ActualPrice'];pt[l['InventoryItemID']]+=amount;qty[l['InventoryItemID']]+=l['Quantity'];st[l['SaleNumber']]+=amount
assert all(st[k]==v['Amount'] for k,v in sales.items())
applied={k:sum(l['Applied'] for l in links if l['SaleNumber']==k) for k in sales}
assert sum(ct.values())==sum(pt.values())==117800
assert sum(applied.values())==sum(r['Amount'] for r in cash.values())==53132
minrows=[]
for item in inv:
 rows=[l for l in sf if l['InventoryItemID']==item];m=min(l['ActualPrice'] for l in rows)
 for l in rows:
  if l['ActualPrice']==m:
   s=sales[l['SaleNumber']];minrows.append(dict(item=item,price=m,sale=s['SaleNumber'],salesperson=s['SalesRepNumber'],customer=s['CustomerNumber'],name=cust[s['CustomerNumber']]['Name']))
raw=json.loads((ROOT/'sources/ac6761-predict-auditfee.json').read_text(encoding='utf-8-sig'))
rows=raw['cells']['xl/worksheets/sheet1.xml'][1:]
data=[(int(r[0]['value']),F(r[1]['value']),F(r[2]['value'])) for r in rows]
n=len(data);x=[r[1] for r in data];y=[r[2] for r in data]
sx=sum(x);sy=sum(y);sxx=sum(v*v for v in x);sxy=sum(a*b for a,b in zip(x,y))
b=(n*sxy-sx*sy)/(n*sxx-sx*sx);a=(sy-b*sx)/n
pred=a+b*5;sse=sum((yy-a-b*xx)**2 for xx,yy in zip(x,y))
assert n==25
expanded=json.loads((ROOT/'sources/ac6761-example-tables2.json').read_text(encoding='utf-8-sig'))
result={'basic_tables':{k:len(v) for k,v in d.items()},'q1':[dict(link=l,receipt=cash[l['RemittanceAdviceNumber']],sale=sales['S-5']) for l in links if l['SaleNumber']=='S-5'], 'q2':[dict(stockflow=l,inventory=inv[l['InventoryItemID']],customer=cust[sales['S-2']['CustomerNumber']]) for l in sf if l['SaleNumber']=='S-2'], 'q3':lag,'applied_by_sale':applied,'unpaid_by_sale':{k:sales[k]['Amount']-applied[k] for k in sales},'q4_per_item_minima':minrows,'q4_global_minimum':min(l['ActualPrice'] for l in sf),'q5_totals':dict(ct),'q6_amounts':dict(pt),'q6_quantities':dict(qty),'sale_reconciliation':dict(st),'ols':{'n':n,'sum_x':str(sx),'sum_y':str(sy),'sum_xx':str(sxx),'sum_xy':str(sxy),'a_fraction':str(a),'b_fraction':str(b),'a':float(a),'b':float(b),'cgi5':float(pred),'sse':float(sse),'data':[[yr,float(xx),float(yy)] for yr,xx,yy in data]},'expanded_schema':{k:{'rows':len(v),'fields':list(v[0]) if v else []} for k,v in expanded.items()}}
def seconds(t):
 parts=list(map(int,t.split(':')))
 if len(parts)==2:parts=[0]+parts
 return parts[0]*3600+parts[1]*60+parts[2]
segments=[('S22','00:00','04:12'),('S22','04:12','11:48'),('S22','11:48','22:39'),('S23-M06','00:00','15:55'),('S23-M06','15:55','20:27'),('S23-M08','20:27','29:56'),('S23-M08','29:56','36:18'),('S23-M08','36:18','01:05:41'),('S23-M08','01:05:41','01:13:06'),('S23-M08','01:13:06','01:29:54'),('S23-M08','01:29:54','01:46:24'),('S23-Excel-increment','01:13:06','01:29:34'),('S23-two-pros','51:51','52:12'),('S23-NLP','01:34:13','01:38:27')]
result['time_segments']=[{'source':src,'start':aa,'end':bb,'seconds':seconds(bb)-seconds(aa)} for src,aa,bb in segments]
(OUT/'calculation-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k in ['q3','q4_per_item_minima','q5_totals','q6_amounts','q6_quantities','ols','expanded_schema']},ensure_ascii=False,indent=2))
