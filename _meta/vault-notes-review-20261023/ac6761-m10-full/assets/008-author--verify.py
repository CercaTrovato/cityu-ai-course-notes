from pathlib import Path
from decimal import Decimal as D, getcontext
from zipfile import ZipFile
import hashlib, json, posixpath, re, sys
import xml.etree.ElementTree as ET

getcontext().prec=40
OUT=Path(__file__).parent
ROOT=Path(r'D:\上课资料\CityU')
sys.path.insert(0,str(ROOT/'_meta/tools'))
from safe_write import atomic_write
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s): return re.sub(r'\s+',' ',s.replace('\u200b','').replace('\ufeff','')).strip()
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
candidate=OUT/'candidate-v1.md'
v1=candidate.read_text(encoding='utf-8')
v0=(OUT.parent/'candidate-v0.md').read_text(encoding='utf-8')
manifest={'candidate':{'path':str(candidate),'sha256':sha(candidate)},'baseline':{'path':str(OUT.parent/'baseline.md.snapshot'),'sha256':sha(OUT.parent/'baseline.md.snapshot')},'v0':{'path':str(OUT.parent/'candidate-v0.md'),'sha256':sha(OUT.parent/'candidate-v0.md')},'sources':[],'rules':[],'viewed_source_renders':[]}
questions=[]
texts=[]
for label,name in [('main','Week 10 PPT.pptx'),('ratio','Week 10 PPT Ratio Analysis.pptx')]:
    p=ROOT/'AC6761_Artificial_Intelligence_Accounting/course_files_export'/name
    with ZipFile(p) as z:
        rels={n.attrib['Id']:n.attrib['Target'] for n in ET.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
        pres=ET.fromstring(z.read('ppt/presentation.xml'))
        order=[posixpath.normpath('ppt/'+rels[s.attrib['{'+NS['r']+'}id']]) for s in pres.findall('p:sldIdLst/p:sldId',NS)]
        for page,member in enumerate(order,1):
            root=ET.fromstring(z.read(member))
            paras=[norm(''.join(t.text or '' for t in el.findall('.//a:t',NS))) for el in root.findall('.//a:p',NS)]
            paras=[x for x in paras if x]
            texts.extend([f'## {label} p.{page}',*paras,''])
            for q in paras:
                if '?' in q:
                    questions.append({'number':len(questions)+1,'deck':label,'page':page,'text':q,'v0':norm(q) in norm(v0),'v1':norm(q) in norm(v1)})
        manifest['sources'].append({'path':str(p),'sha256':sha(p),'slide_count':len(order),'real_slide_order':order})
assert len(questions)==87 and all(q['v0'] and q['v1'] for q in questions)
assert re.findall(r'\*\*原题 (\d+)',v0)==re.findall(r'\*\*原题 (\d+)',v1)
blocks=lambda s: re.findall(r'```mermaid\n(.*?)```',s,re.S)
assert blocks(v0)==blocks(v1)
manifest['unchanged_mermaid_blocks']=[hashlib.sha256(x.encode()).hexdigest() for x in blocks(v1)]
for rel in ['AGENTS.md','_meta/可读性总规则.md','AC6761_Artificial_Intelligence_Accounting/_meta/AC6761可读性细则.md','_meta/机制理解与可读性标准.md','_meta/笔记制作与融合验收流程.md','_meta/课件题目处理规则.md','_meta/教学图示规范.md','_meta/教学图示工具流程.md']:
    p=ROOT/rel; manifest['rules'].append({'path':str(p),'sha256':sha(p)})
old=Path(r'E:\app-data\codex\scratchpad\ac6761-canvas-20261022')
for directory,page in [('render-Week-10-PPT',39),('render-Week-10-PPT-Ratio-Analysis',16),('render-Week-10-PPT-Ratio-Analysis',15)]:
    p=old/directory/f'幻灯片{page}.PNG'
    manifest['viewed_source_renders'].append({'path':str(p),'sha256':sha(p),'origin':'historical rendering; current original source SHA matched reviewer extraction; viewed by author this turn'})

inputs={'revenue':D(1000),'cogs':D(600),'ni':D(80),'ca':D(300),'cl':D(150),'inventory_begin':D(90),'inventory_end':D(110),'prepaid':D(20),'cash_end':D(110),'ar_begin':D(40),'ar_end':D(60),'assets_begin':D(800),'assets_end':D(1000),'equity_begin':D(450),'equity_end':D(550),'liabilities_begin':D(350),'liabilities_end':D(450),'debt_end':D(400),'ebit':D(120),'interest':D(20),'tax':D(20),'shares_avg':D(40),'shares_end':D(40),'price':D(30)}
i=inputs
assert i['ca']==i['cash_end']+i['ar_end']+i['inventory_end']+i['prepaid']
assert i['assets_end']==i['liabilities_end']+i['equity_end']
assert i['assets_begin']==i['liabilities_begin']+i['equity_begin']
assert i['ni']==i['ebit']-i['interest']-i['tax']
avg_inv=(i['inventory_begin']+i['inventory_end'])/2
avg_ar=(i['ar_begin']+i['ar_end'])/2
avg_a=(i['assets_begin']+i['assets_end'])/2
avg_e=(i['equity_begin']+i['equity_end'])/2
ratios={'average_inventory':avg_inv,'average_ar':avg_ar,'average_assets':avg_a,'average_equity':avg_e,'current':i['ca']/i['cl'],'quick':(i['ca']-i['inventory_end']-i['prepaid'])/i['cl'],'gross_margin':(i['revenue']-i['cogs'])/i['revenue'],'roe':i['ni']/avg_e,'roa':i['ni']/avg_a,'debt_equity_report_date':i['debt_end']/i['equity_end'],'interest_coverage':i['ebit']/i['interest'],'inventory_turnover':i['cogs']/avg_inv,'inventory_days':D(365)/(i['cogs']/avg_inv),'receivables_turnover_revenue_proxy':i['revenue']/avg_ar,'dso_revenue_proxy':D(365)/(i['revenue']/avg_ar),'basic_eps':i['ni']/i['shares_avg'],'book_value_per_share':i['equity_end']/i['shares_end']}
ratios['pe']=i['price']/ratios['basic_eps']
ratios['pb']=i['price']/ratios['book_value_per_share']
ratios['market_equity']=i['price']*i['shares_end']
ratios['pb_total_check']=ratios['market_equity']/i['equity_end']
assert ratios['pb']==ratios['pb_total_check']
ratios['dupont']=(i['ni']/i['revenue'])*(i['revenue']/avg_a)*(avg_a/avg_e)
assert abs(ratios['dupont']-ratios['roe'])<D('1e-35')
z_inputs={'assets':D(1000),'liabilities':D(500),'book_equity':D(500),'ca':D(300),'cl':D(150),'retained':D(200),'ebit':D(120),'price':D(15),'shares':D(50),'sales':D(1000)}
z=z_inputs
assert z['assets']==z['liabilities']+z['book_equity']
xs=[(z['ca']-z['cl'])/z['assets'],z['retained']/z['assets'],z['ebit']/z['assets'],z['price']*z['shares']/z['liabilities'],z['sales']/z['assets']]
contributions=[a*b for a,b in zip(xs,map(D,['1.2','1.4','3.3','0.6','1']))]
zscore=sum(contributions)
assert zscore==D('2.756')
scenario={}
for name,volume,raw_multiplier in [('base',D('1.05'),D(1)),('bull',D('1.15'),D(1)),('bear',D('.9'),D('1.2'))]:
    sales=D(1000)*volume; cost=D(300)*volume*(1+raw_multiplier); gross=sales-cost
    scenario[name]={'revenue':sales,'cost':cost,'gross':gross,'gross_margin':gross/sales,'cash_receipts':sales*D('.9'),'closing_ar':sales*D('.1'),'cash_proxy':sales*D('.9')-cost}
result={'shared_inputs':inputs,'balance_checks':'begin/end balance sheets and CA composition agree; total debt 400 is subset of liabilities 450; not a full cash-flow statement','ratios':ratios,'independent_z_inputs':z_inputs,'z_components':xs,'z_contributions':contributions,'z':zscore,'z_ebit_200':zscore+D('3.3')*(D(200)/1000-D(120)/1000),'scenario_assumptions':'price and product mix constant, all costs proportional to volume, raw materials half baseline cost','scenarios':scenario,'bear_price_cut_only':{'revenue':900,'cogs':660,'gross':240,'gross_margin':D(240)/900},'self_test':{'average_ar':50,'turnover':D(900)/50,'dso':D(365)/(D(900)/50),'changed_average_ar':70,'changed_turnover':D(900)/70,'changed_dso':D(365)/(D(900)/70),'wrong_rounded_dso':D(365)/D('12.86')},'cash_bridges':{'old_inventory_paid':D(40)-100+60,'current_inventory_cash':D(40)-100,'current_inventory_credit':D(40)-100+60,'immediate_customer_cash_old_inventory':D(40)+60},'inventory_end_130_days':D(365)/(D(600)/((D(90)+130)/2)),'supplier_cost_example':{'initial_margin':D(400)/1000,'increased_component_margin':D(300)/1000},'regression_given_model':{'x20':2*20+10,'x25':2*25+10}}
manifest['question_check']={'count':len(questions),'exact_after_whitespace_normalization':sum(q['v1'] for q in questions),'numbers_unchanged':True,'questions':questions}
for fn,data in [('calculation-results-v1.json',result),('sourcehash.json',manifest)]:
    atomic_write(OUT/fn,json.dumps(data,ensure_ascii=False,indent=2,default=str)+'\n')
atomic_write(OUT/'current-source-text.txt','\n'.join(texts))
print(json.dumps({'candidate_sha256':sha(candidate),'questions_matched':len(questions),'mermaid_unchanged':len(blocks(v1)),'quick':str(ratios['quick']),'de':str(ratios['debt_equity_report_date']),'pb':str(ratios['pb']),'z':str(zscore),'self_test_dso':str(result['self_test']['changed_dso'])},ensure_ascii=False))
