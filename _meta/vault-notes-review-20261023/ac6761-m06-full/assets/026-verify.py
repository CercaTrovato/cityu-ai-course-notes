from pathlib import Path
import hashlib,json,re,sqlite3,decimal,subprocess,sys,zipfile,xml.etree.ElementTree as ET,io,contextlib
ROOT=Path('D:/上课资料/CityU')
OUT=Path('E:/app-data/codex/scratchpad/cityu-workflow-rollout-20261026/dispatch-m06-repair')
OLD=OUT.parent/'ac6761-m06-full'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
source_rows=json.loads((OLD/'reviewer/current-source-hashes.json').read_text(encoding='utf-8-sig'))
source_checks=[dict(x,current_sha256=sha(Path(x['path'])),unchanged=sha(Path(x['path']))==x['sha256']) for x in source_rows]
assert all(x['unchanged'] for x in source_checks)
(OUT/'source-hash-verification.json').write_text(json.dumps(source_checks,ensure_ascii=False,indent=2),encoding='utf-8')

# Re-read exact source XML only for the newly introduced original Quiz text and changed QBE titles.
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(source_rows[1]['path']) as z:
    root=ET.fromstring(z.read('word/document.xml'))
    paragraphs=[''.join(p.itertext()) for p in []] # actual visible text below, excluding structural values
    paragraphs=[''.join(p.itertext()) for p in root.findall('.//w:p',ns)]
    # use only w:t runs: itertext can repeat namespace text in some producers
    paragraphs=[''.join(p.findtext('.',default='') for p in [])] if False else [''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in root.findall('.//w:p',ns)]
quiz=[x for x in paragraphs if x.strip()]
candidate=(OUT/'candidate-v1.md').read_text(encoding='utf-8')
assert all(x in candidate for x in quiz)
with zipfile.ZipFile(source_rows[0]['path']) as z:
    slide_text={str(n):'\n'.join(t.text or '' for t in ET.fromstring(z.read(f'ppt/slides/slide{n}.xml')).findall('.//a:t',ns)) for n in [9,10,11,13,16,19,21,23,24,25,27,34,35,37,38,41,42,43,44,46,47,49,50,51,73,74,76,77,79,80,86,87,88,89,90,91,92]}
(OUT/'changed-source-excerpts.json').write_text(json.dumps({'quiz_paragraphs':quiz,'ppt_slide_text':slide_text,'basis':'newly read current source XML; image content inherited by exact media hashes from original reviewer'},ensure_ascii=False,indent=2),encoding='utf-8')

# SQLite only: no access to the original database, no file writes by SQLite.
db=json.loads((OLD/'reviewer/db-current-dotnet-read.json').read_text(encoding='utf-8-sig'))
data={x['name']:x for x in db}
con=sqlite3.connect(':memory:')
con.executescript('CREATE TABLE Sale(id TEXT,amt NUMERIC,dt TEXT); CREATE TABLE CR(id TEXT,dt TEXT); CREATE TABLE Applied(sale TEXT,ra TEXT,amt NUMERIC);')
con.executemany('INSERT INTO Sale VALUES(?,?,?)',[(r[0],r[1],r[2][:10]) for r in data['Sale']['rows']])
con.executemany('INSERT INTO CR VALUES(?,?)',[(r[0],r[3][:10]) for r in data['CashReceipt']['rows']])
con.executemany('INSERT INTO Applied VALUES(?,?,?)',data['Duality']['rows'])
query=re.search(r'```sql\n(SELECT s.id, s.amt, COALESCE.*?;)\n```',candidate,re.S).group(1)
results={}
for t,expected in [('2014-07-31',48134),('2014-08-31',64668)]:
    rows=con.execute(query,{'asof':t}).fetchall()
    total=sum(r[3] for r in rows)
    assert total==expected,(t,total)
    results[t]={'rows':rows,'total':total}
assert [x for x in results['2014-07-31']['rows'] if x[0]=='S-2'][0][3]==8334
assert [x for x in results['2014-08-31']['rows'] if x[0]=='S-2'][0][3]==6668
daily=con.execute("SELECT dt,SUM(amt) FROM Sale WHERE dt BETWEEN '2014-07-15' AND '2014-07-31' GROUP BY dt").fetchall()
monthly=con.execute("SELECT substr(dt,1,4),substr(dt,6,2),SUM(amt) FROM Sale WHERE dt BETWEEN '2014-07-15' AND '2014-07-31' GROUP BY substr(dt,1,4),substr(dt,6,2)").fetchall()
assert len(daily)==4 and monthly==[('2014','07',52600)]
fulljuly=con.execute("SELECT SUM(amt) FROM Sale WHERE dt>='2014-07-01' AND dt<'2014-08-01'").fetchone()[0]
assert fulljuly==59800
D=decimal.Decimal
cost=D(40)*D(18)+D(30)*D(22)+D(30)*D('20.67')
assert cost==D('2000.10') and cost/D(100)==D('20.001')
numeric={'execution':'SQLite in-memory plus Decimal; not ACE or Access UI','source_data_evidence':str(OLD/'reviewer/db-current-dotnet-read.json'),'source_data_evidence_sha256':sha(OLD/'reviewer/db-current-dotnet-read.json'),'candidate_sql_exact':query,'cutoff_results':results,'daily':daily,'monthly':monthly,'full_july':fulljuly,'S2_wrong_per_match':[8334,8334],'S2_right_balance':6668,'WAUC':{'cost':str(cost),'quantity':100,'unit_cost':str(cost/D(100))},'screenshot_ar':8455-0-140,'screenshot_ap':35270-28450-480,'access_ace_evidence_inherited':str(OLD/'reviewer/ace-targeted-results.json'),'access_ui_executed':False}
(OUT/'numeric-verification.json').write_text(json.dumps(numeric,ensure_ascii=False,indent=2),encoding='utf-8')

# Structural mapping only; semantic acceptance remains with the original independent reviewer.
units=json.loads((OLD/'reviewer/question-coverage.json').read_text(encoding='utf-8-sig'))['units']
coverage=[]
clines=candidate.splitlines()
for i,u in enumerate(units,1):
    token=f'U{i:02d}'
    positions=[j+1 for j,l in enumerate(clines) if token in l]
    assert positions,(token,u)
    u=dict(u,id=token,candidate_lines=positions,repair_status='author_repaired_pending_targeted_independent_recheck')
    if i==22: u['english_reference_lines']=[next(j+1 for j,l in enumerate(clines) if '**English reference answer（笔记参考答案）**' in l)]
    if i==23: u['english_reference_lines']=[next(j+1 for j,l in enumerate(clines) if 'For the reconstructed not-equal-to-C-2 condition' in l)]
    coverage.append(u)
(OUT/'question-coverage-v1.json').write_text(json.dumps({'count':len(coverage),'units':coverage,'not_a_semantic_pass':True},ensure_ascii=False,indent=2),encoding='utf-8')

# Run the stock link checker logic against only the candidate in its real vault context.
target=next(ROOT.glob('AC6761*/notes/M06-*.md'))
relative=str(target.relative_to(ROOT))
source=(ROOT/'_meta/tools/link_check.py').read_text(encoding='utf-8')
source=source.replace('for f in files:\n    t, spans = body(f)','for f in [TARGET]:\n    t, spans = body(f)')
realopen=io.open
def redirected_open(f,*args,**kwargs):
    p=Path(f)
    if (p if p.is_absolute() else ROOT/p).resolve()==target.resolve(): return realopen(OUT/'candidate-v1.md',*args,**kwargs)
    return realopen(f,*args,**kwargs)
stream=io.StringIO()
io.open=redirected_open
try:
    with contextlib.redirect_stdout(stream):
        try: exec(compile(source,str(ROOT/'_meta/tools/link_check.py'),'exec'),{'__file__':str(ROOT/'_meta/tools/link_check.py'),'TARGET':relative,'__name__':'__main__'})
        except SystemExit as e: linkcode=e.code
finally: io.open=realopen
(OUT/'link-check.log').write_text(stream.getvalue(),encoding='utf-8')

cmd=[sys.executable,'-X','utf8',str(ROOT/'_meta/tools/note_release_gate.py'),str(OUT/'candidate-v1.md'),'--note',str(target.relative_to(ROOT)),'--source',str(OUT/'candidate-v0.snapshot.md'),'--scope','changed','--pages','92','--check-only']
p=subprocess.run(cmd,cwd=ROOT,capture_output=True,encoding='utf-8',errors='replace')
(OUT/'mechanical-precheck.log').write_text(p.stdout+p.stderr,encoding='utf-8')
(OUT/'verification-summary.json').write_text(json.dumps({'source_hashes_verified':len(source_checks),'source_hashes_unchanged':True,'quiz_complete_original_retained':True,'question_units_with_locations':34,'numeric_assertions':'passed within explicitly limited example','link_check_exit':linkcode,'mechanical_precheck_exit':p.returncode,'command':cmd,'independent_targeted_review':'pending; not executed in this thread','formal_note':str(target),'formal_note_sha256':sha(target),'candidate_sha256':sha(OUT/'candidate-v1.md')},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'sources_unchanged':True,'quiz_original_retained':True,'units':34,'link_exit':linkcode,'gate_exit':p.returncode,'gate_tail':(p.stdout+p.stderr)[-2500:]},ensure_ascii=False))
