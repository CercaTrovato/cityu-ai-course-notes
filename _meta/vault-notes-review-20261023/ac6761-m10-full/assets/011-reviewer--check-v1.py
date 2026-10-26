from pathlib import Path
from decimal import Decimal as D, getcontext
import difflib, hashlib, json, re
getcontext().prec=40
out=Path(__file__).parent
v0p=out.parent/'candidate-v0.md'
v1p=out.parent/'author/candidate-v1.md'
v0=v0p.read_text(encoding='utf-8'); v1=v1p.read_text(encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
norm=lambda s:re.sub(r'\s+',' ',s.replace('\u200b','').replace('\ufeff','')).strip()
old=json.loads((out/'source-evidence.json').read_text(encoding='utf-8'))
source_states=[{'path':s['path'],'sha256':sha(Path(s['path'])),'unchanged':sha(Path(s['path']))==s['sha256']} for s in old['sources']]
question_states=[{'number':q['source_question'],'page':q['page'],'preserved':norm(q['text']) in norm(v1)} for q in old['source_questions']]
blocks=lambda s:re.findall(r'```mermaid\n(.*?)```',s,re.S)
numbered=lambda s:re.findall(r'\*\*原题 (\d+)',s)
def units(s):
    starts=list(re.finditer(r'\*\*原题 (\d+)',s))
    return {int(m.group(1)):s[m.start():starts[i+1].start() if i+1<len(starts) else s.index('#### 2.10.9',m.start())]
            for i,m in enumerate(starts)}
u0=units(v0);u1=units(v1)
changed_questions=[n for n in u0 if norm(u0[n])!=norm(u1[n])]
reference_counts={str(n):{'has_chinese':bool(re.search(r'中文',u1[n])),
                        'has_english_reference':bool(re.search(r'英文参考',u1[n]))} for n in u1}
actual_diff=''.join(difflib.unified_diff(v0.splitlines(True),v1.splitlines(True),fromfile='candidate-v0.md',tofile='author/candidate-v1.md'))
given_diff=(out.parent/'author/candidate-v0-to-v1.diff').read_text(encoding='utf-8')
navigation={}
for start,end,key in [('### 8.1','### 8.2','main'),('### 8.2','## 9.','ratio')]:
    text=v1.split(start,1)[1].split(end,1)[0]
    navigation[key]=[int(x) for x in re.findall(r'^\|\s*(\d+)\s*\|',text,re.M)]
numeric_positions=[]
for tag,a,b,c,d in difflib.SequenceMatcher(a=v0.splitlines(),b=v1.splitlines()).get_opcodes():
    if tag not in ('equal','delete'):
        numeric_positions += [{'line':i+1,'text':v1.splitlines()[i]} for i in range(c,d) if re.search(r'\d',v1.splitlines()[i])]
stale_patterns=[r'300-100-20',r'400/500',r'30/10',r'每股账面值\s*\|\s*30 / 2 / 10',r'速动比率[^\n]*1\.2',r'P/B[^\n]*3 倍',r'365/12\.86']
stale=[{'pattern':p,'matches':re.findall(p,v1)} for p in stale_patterns]
calc={
 'ca':D(110)+60+110+20,'assets_begin':D(350)+450,'assets_end':D(450)+550,
 'ni':D(120)-20-20,'avg_inventory':(D(90)+110)/2,'avg_equity':(D(450)+550)/2,
 'quick':(D(300)-110-20)/150,'de':D(400)/550,'eps':D(80)/40,'bvps':D(550)/40,
 'pb_per_share':D(30)/(D(550)/40),'pb_total':(D(30)*40)/550,
 'dupont':(D(80)/1000)*(D(1000)/900)*(D(900)/500),
 'z':D('1.2')*D('.15')+D('1.4')*D('.2')+D('3.3')*D('.12')+D('.6')*D('1.5')+1,
 'z_ebit_200':D('1.2')*D('.15')+D('1.4')*D('.2')+D('3.3')*D('.20')+D('.6')*D('1.5')+1,
 'retained':D(150)+80-30,'bearing_volume_cost':D(300)*D('.9')*(1+D('1.2')),
 'bearing_price_cost':D(300)+D(300)*D('1.2'),'bearing_price_margin':D(240)/900,
 'cash_old_stock':D(40)-100+60,'cash_current_cash_stock':D(40)-100,
 'cash_current_credit_stock':D(40)-100+60,'cash_immediate':D(40)+60,
 'selftest_dso':D(365)/(D(900)/70),'sgna_ratio':D(11)/120,
 'supplier_margin_1':(D(1000)-D(100)*(4+2))/1000,
 'supplier_margin_2':(D(1000)-D(100)*(5+2))/1000,
 'regression_x20':D(2)*20+10,'regression_x25':D(2)*25+10,
}
scenario={}
for name,m,raw in [('base',D('1.05'),D(1)),('bull',D('1.15'),D(1)),('bear',D('.9'),D('1.2'))]:
    revenue=D(1000)*m;cost=D(300)*m*(1+raw)
    scenario[name]={'revenue':revenue,'cost':cost,'gross':revenue-cost,'gross_margin':(revenue-cost)/revenue,
                   'cash_receipts':revenue*D('.9'),'ar':revenue*D('.1'),'cash_proxy':revenue*D('.9')-cost}
evidence={'candidate':{'sha256':sha(v1p),'bytes':v1p.stat().st_size,'lines':len(v1.splitlines())},
 'sources':source_states,'real_diff_matches_given':actual_diff==given_diff,'questions':question_states,
 'question_numbers_unchanged':numbered(v0)==numbered(v1),'mermaid_count':len(blocks(v1)),
 'changed_question_units':changed_questions,'reference_presence':reference_counts,
 'mermaid_blocks_unchanged':blocks(v0)==blocks(v1),'navigation':navigation,
 'stale_formula_checks':stale,'independent_calculations':calc,'scenarios':scenario,
 'changed_numeric_positions':numeric_positions}
assert evidence['candidate']['sha256']=='bd561a195951599515d74b03314004145f55f12920e25411e3b6539731daa757'
assert evidence['real_diff_matches_given'] and all(s['unchanged'] for s in source_states)
assert len(question_states)==87 and all(q['preserved'] for q in question_states)
assert evidence['question_numbers_unchanged'] and evidence['mermaid_blocks_unchanged']
assert all(x['has_chinese'] and x['has_english_reference'] for x in reference_counts.values())
assert navigation['main']==list(range(1,43)) and navigation['ratio']==list(range(1,17))
assert not any(x['matches'] for x in stale)
(out/'v1-targeted-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
print(json.dumps({'candidate':evidence['candidate'],'diff_verified':True,'source_hashes_unchanged':True,
 'question_match':len(question_states),'mermaid_unchanged':len(blocks(v1)),'navigation':[len(navigation['main']),len(navigation['ratio'])],
 'changed_question_units':changed_questions,
 'stale_formula_matches':0,'numeric_positions_to_read':len(numeric_positions),
 'calculations':calc,'scenarios':scenario},ensure_ascii=False,indent=2,default=str))
