import json
from pathlib import Path

OUT=Path(__file__).parent

def run(transactions):
    a=l=e=0; rows=[]
    for i,(da,dl,de,label) in enumerate(transactions,1):
        a+=da;l+=dl;e+=de
        rows.append({'transaction':i,'label':label,'delta':[da,dl,de],'after':[a,l,e],'balanced':a==l+e})
    return rows

fast=[(30000,0,30000,'owner investment'),(0,0,0,'cash to supplies'),(0,0,0,'cash to equipment'),(7100,7100,0,'supplies on credit'),(4200,0,4200,'cash consulting revenue'),(-1000,0,-1000,'rent expense'),(-700,0,-700,'salary expense'),(1900,0,1900,'credit consulting and rental revenue'),(0,0,0,'cash collection of receivable'),(-900,-900,0,'partial AP payment'),(-200,0,-200,'cash dividend')]
swift=[(20000,0,20000,'owner investment'),(0,0,0,'cash to van'),(0,0,0,'cash to supplies'),(1000,1000,0,'fuel on credit'),(3000,0,3000,'cash service revenue'),(-800,0,-800,'rent expense'),(2500,0,2500,'credit service revenue'),(-500,-500,0,'partial AP payment')]
fast_rows=run(fast); swift_rows=run(swift)
statements={'revenue':4200+1600+300,'expenses':1000+700,'net_income':4200+1600+300-1000-700,'ending_equity':30000+(4200+1600+300-1000-700)-200,'assets':4800+0+9600+26000,'liabilities':6200,'cfo':6100-3400-1000-700,'cfi':-26000,'cff':30000-200,'ending_cash':(6100-3400-1000-700)-26000+(30000-200)}
checks={'fast_all_balanced':all(x['balanced'] for x in fast_rows),'swift_all_balanced':all(x['balanced'] for x in swift_rows),'fast_final':fast_rows[-1]['after'],'swift_final':swift_rows[-1]['after'],'balance_sheet_balanced':statements['assets']==statements['liabilities']+statements['ending_equity'],'cash_flow_ties':statements['ending_cash']==4800,'income_to_equity_ties':statements['ending_equity']==34200}
payload={'fastforward_11':fast_rows,'swift_8':swift_rows,'financial_statements':statements,'checks':checks}
(OUT/'calculation-results.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False,indent=2))
