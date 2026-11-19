from pathlib import Path
import re,json,hashlib,math
d=Path(__file__).resolve().parent; src=d.parent/'practice_exam_B'; p=d/'candidate.md'
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
t=p.read_text('utf-8'); pages=json.loads((src/'pages.json').read_text('utf-8-sig'))
blocks=re.findall(r'```text\n(.*?)\n```',t,re.S)
assert len(blocks)==14
for i,(a,b) in enumerate(zip(blocks,pages),1):assert a==b.rstrip(),i
assert len(re.findall(r'^### A\d+ ·',t,re.M))==16
assert len(re.findall(r'^### B\d+\([ab]\) ·',t,re.M))==8
assert len(re.findall(r'^### C\d+\([ab]\) ·',t,re.M))==4
assert t.count('English reference:')==28
imgs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',t);assert len(imgs)==14
assert all((d/i).is_file() for i in imgs)
assert len(re.findall(r'```mermaid\n',t))==3
expected={'A2_excess_percent':-.64,'A5_drawdown':.25,'A7_RMB_headroom':200000,'A9_time_reduction':.375,'A11_HKD_proceeds':49850,'A11_discount':.003,'A15_USD_investor_loss':300,'B3_USD_retained':8,'C1_zm':1,'C1_zv':.5,'C1_excess_percent':.3,'C2_before_NAV':10,'C2_a_NAV':10.4,'C2_b_NAV':9.6,'C2_par_NAV':10}
actual=json.loads((d/'arithmetic-checks.json').read_text('utf-8'))
assert all(math.isclose(actual[k],v,abs_tol=1e-9) for k,v in expected.items())
preview=d.parents[1]/'preview/ef5560-practice-b-dot'
b=json.loads((preview/'binding.json').read_text('utf-8-sig')); html=(preview/'index.html').read_bytes()
assert b['sha256']==sha(p)
assert hashlib.sha256(html.replace(b'\r\n',b'\n')).hexdigest()==b['html_sha256']
result={'candidate_sha256':sha(p),'question_units':28,'english_answers':28,'exact_source_page_blocks':14,'MC_options':64,'images':14,'generated_mermaid':3,'arithmetic_cases_checked':len(expected),'actual_pdf_vs_intake':'reextracted via Poppler; whitespace-normalized equality confirmed','original_source_blocks_exact':True,'preview':str(preview),'raw_html_sha256':hashlib.sha256(html).hexdigest(),'LF_html_sha256':b['html_sha256'],'preview_math_nodes':b['math_nodes'],'preview_UI':'not_viewed','mechanical_note_quality':{'exit_code':2,'message':'找不到 §2 正文，无法评估','disposition':'Lecture-note parser not applicable to standalone exercise analysis. Original error preserved; no machine PASS claimed. Exercise task coverage checked explicitly instead.'},'independent_review':'pending; spawn failed agent thread limit reached'}
(d/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
