from pathlib import Path
import json,hashlib,re,subprocess,sys,shutil
O=Path(__file__).resolve().parent
P=O.parent
V=Path('D:/上课资料/CityU')
NOTE='EF5560_Fintech_and_AI_in_Finance/assignment/practice/practice-exam-a/学习解析.md'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
maintenance=json.loads((O/'status-only-maintenance.json').read_text(encoding='utf8'))
text=(O/'candidate-v3.md').read_text(encoding='utf8')
old=(P/'candidate.md').read_text(encoding='utf8')
assert sha(O/'candidate-v3.md')==maintenance['candidate_sha256']
restore=text
for item in reversed(maintenance['replacements']):
    restore=restore.replace(item['to'],item['from'],1)
assert restore==old,'Unexpected content drift beyond the 3 explicit maintenance replacements.'
math_pattern=r'(?<!\\)\$\$[\s\S]*?(?<!\\)\$\$|(?<![\\$])\$(?!\$)[^\n$]+(?<!\\)\$'
assert re.findall(math_pattern,text)==re.findall(math_pattern,old)
assert re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text)==re.findall(r'!\[[^\]]*\]\(([^)]+)\)',old)
for name in ['b2-loss.svg','b2-loss.png','compute.py','computation-results.json','source-checks.json']:
    assert (O/name).read_bytes()==(P/name).read_bytes(),name
assert 'status: draft' in text and 'official_solution: not_obtained' in text
assert not re.search(r'尚未独立两阶段审查|independent_review: pending|^# .*学习解析候选$',text,re.M)
dump(O/'unchanged-teaching-proof.json',{
    'prior_candidate_sha256':sha(P/'candidate.md'),'candidate_sha256':sha(O/'candidate-v3.md'),
    'inverse_three_replacements_exactly_restores_v2':True,
    'all_math_source_fragments_equal':True,'math_fragment_count':len(re.findall(math_pattern,text)),
    'all_images_links_equal':True,
    'unchanged_files':{n:sha(O/n) for n in ['b2-loss.svg','b2-loss.png','compute.py','computation-results.json','source-checks.json']},
    'new_teaching_review':False,'basis':'Pure administrative status/H1/current workflow maintenance only.'})
cmd=[sys.executable,'-X','utf8',str(V/'_meta/tools/note_quality.py'),str(O/'candidate-v3.md'),
     '--profile','current','--json','--strict','--sections','--readability','--pages','14',
     '--source-checks',str(O/'source-checks.json')]
proc=subprocess.run(cmd,cwd=V,capture_output=True,text=True,encoding='utf8')
(O/'mechanical-v3.txt').write_text(proc.stdout+proc.stderr,encoding='utf8')
data=json.loads(next(x[5:] for x in proc.stdout.splitlines() if x.startswith('JSON:')))
dump(O/'mechanical-v3.json',data)
assert proc.returncode==0 and not data['legacy_problems'] and not data['C']['hard'] and not data['R']['hard']
oldwarn=json.loads((P/'warning-dispositions.json').read_text(encoding='utf8'))
olddata=json.loads((P/'mechanical-current.json').read_text(encoding='utf8'))
dump(O/'warning-dispositions-v3.json',{
    'candidate_sha256':sha(O/'candidate-v3.md'),
    'prior_dispositions':'../warning-dispositions.json',
    'C_warning_objects_exactly_equal':data['C']['warn']==olddata['C']['warn'],
    'R_warning_objects_exactly_equal':data['R']['warn']==olddata['R']['warn'],
    'current_C_warn':data['C']['warn'],'current_R_warn':data['R']['warn'],
    'disposition':'Unchanged warnings inherit exact prior location/context dispositions; maintenance block is administrative only, not a new teaching unit.',
    'counts':{'C_warn':len(data['C']['warn']),'R_warn':len(data['R']['warn']), 'L_C_R_hard':0}})

preview=Path('E:/app-data/codex/scratchpad/cityu-notes-20261118/preview/ef5560-practice-a-dot-v3-status')
binding=json.loads((preview/'binding.json').read_text(encoding='utf8'))
assert binding['sha256']==sha(O/'candidate-v3.md') and binding['math_nodes']==52
html=preview/'index.html';blob=html.read_bytes()
assert hashlib.sha256(blob.replace(b'\r\n',b'\n')).hexdigest()==binding['html_sha256']
shutil.copytree(preview,O/'preview',dirs_exist_ok=True)
dump(O/'preview-binding-actual.json',{
    'candidate_sha256':sha(O/'candidate-v3.md'),'raw_html_sha256':sha(html),
    'LF_normalized_html_sha256':binding['html_sha256'],'CRLF_pairs':blob.count(b'\r\n'),
    'svg_sha256':sha(O/'b2-loss.svg'),'math_nodes':52,
    'url':'http://127.0.0.1:8796/ef5560-practice-a-dot-v3-status/',
    'status':'passed by root actual same-source IAB viewing' if (O/'root-v3-display-confirmation.json').exists() else 'generated; waiting root actual same-source IAB viewing confirmation',
    'actual_observation_file':'root-v3-display-confirmation.json' if (O/'root-v3-display-confirmation.json').exists() else None})
proof=O/'root-v3-display-confirmation.json'
if not proof.exists():
    print(json.dumps({'maintenance':'exact3replacements_verified','machine':'passed',
                      'source_contract':data['C']['source_coverage'],'C_warn':len(data['C']['warn']),
                      'R_warn':len(data['R']['warn']),'waiting':'root actual v3 viewing confirmation'},ensure_ascii=False))
    sys.exit(3)
actual=json.loads(proof.read_text(encoding='utf8'))
assert actual['observer']=='/root' and actual['candidate_sha256']==sha(O/'candidate-v3.md')
assert actual['status']=='passed'
summary='''# Practice A · v3 status-only rebind

This receipt carries the accepted v2 teaching/source review to a purely administrative v3. No new independent review is claimed or performed. The original full Stage1/2 and directed acceptance remain unchanged in ../evidence/independent-review. Actual old candidate716… was accepted by /root/ef_m11_review; actual current candidate hash is in the bound JSON.

Exactly three changes: independent_review frontmatter pending→independently-reviewed, H1 removes 候选, and §9.4 replaces a literally false current-not-reviewed workflow paragraph with the completed-review status and the distinction from the student's own learning/submission. status:draft, reference/official-source/legal boundaries and historical author viewing statements remain.

The exact inverse of these three replacements restores accepted v2. All question/option/teaching/math/calculation/image bytes outside those replacements remain identical. The source contract, SVG15editabletext d402808a…, PNG and calculation JSON are byte-identical. Their real v2 rerun and original source/visual semantics evidence carry forward. This is not a new training run or a new full review.

Current14-page22-question machine/source-contract checks are freshly rerun with L/C/R hard0. All current warnings are stored beside the prior exact dispositions; any newly found discrepancy would block rather than be hidden. Root actually views the new unique v3 URL, recorded in root-v3-display-confirmation.json. Same-source raw preview, LF-normalized original binding and exact current asset hashes are bound. No native Obsidian claim.

New formal destination stays EF5560_Fintech_and_AI_in_Finance/assignment/practice/practice-exam-a/学习解析.md with adjacent b2-loss.svg. This is scratch staging only, not formal write/sync or an update of student's own learning state.
'''
(O/'review-v3.md').write_text(summary,encoding='utf8')
assets=[{'path':p.relative_to(O).as_posix(),'sha256':sha(p)} for p in sorted(O.rglob('*'))
        if p.is_file() and p.name not in ['review-v3.json','gate-v3.txt','staging-manifest-v3.json']]
assets += [{'path':'../review-final.json','sha256':sha(P/'review-final.json')},
           {'path':'../warning-dispositions.json','sha256':sha(P/'warning-dispositions.json')},
           {'path':'../computation-rerun-proof.json','sha256':sha(P/'computation-rerun-proof.json')}]
for p in sorted((P/'evidence').rglob('*')):
    if p.is_file():assets.append({'path':'../'+p.relative_to(P).as_posix(),'sha256':sha(p)})
review={'schema':'note-review-v2','note':NOTE,'scope':'full','source_sha256':None,
        'candidate_sha256':sha(O/'candidate-v3.md'),'review_file':'review-v3.md','review_sha256':sha(O/'review-v3.md'),
        'checks':{
          'understanding':{'status':'passed','evidence':'Accepted v2 full review + exact3-administrative-diff maintenance carryforward; no new independent review claimed.'},
          'sources':{'status':'passed','evidence':'Original14page/full22question/28unit source review unchanged; current22question contract freshly passed.'},
          'warnings':{'status':'passed','evidence':'mechanical-v3 and all exact current warning dispositions/carryforward.'},
          'visuals':{'status':'passed','evidence':'root-v3-display-confirmation actual unique-url exact v3; original math/PNG/SVG semantic evidence unchanged.'}},
        'independent_review':{
          'author_ids':['/root/cityu_legal_resume','/root'],'reviewer_id':'/root/ef_m11_review',
          'perspective':'high-school-beginner','status':'passed',
          'candidate_sha256':sha(O/'candidate-v3.md'),
          'original_reviewed_candidate_sha256':maintenance['prior_candidate_sha256'],
          'evidence_mode':'pure_administrative_maintenance_carryforward_not_new_review',
          'maintenance_file':'status-only-maintenance.json',
          'report_file':'../evidence/independent-review/directed-review-v2.md',
          'report_sha256':sha(P/'evidence/independent-review/directed-review-v2.md')},
        'assets':assets,'unresolved':[]}
dump(O/'review-v3.json',review)
cmd=[sys.executable,'-X','utf8',str(V/'_meta/tools/note_release_gate.py'),str(O/'candidate-v3.md'),
     '--note',NOTE,'--scope','full','--pages','14','--source-checks',str(O/'source-checks.json'),
     '--review',str(O/'review-v3.json')]
proc=subprocess.run(cmd,cwd=V,capture_output=True,text=True,encoding='utf8')
(O/'gate-v3.txt').write_text(proc.stdout+proc.stderr,encoding='utf8')
assert proc.returncode==0,(proc.stdout+proc.stderr)[-3000:]
dump(O/'staging-manifest-v3.json',{
    'candidate':'candidate-v3.md','candidate_sha256':sha(O/'candidate-v3.md'),
    'note':NOTE,'new_target_verified_absent':not(V/NOTE).exists(),
    'svg':'b2-loss.svg','svg_sha256':sha(O/'b2-loss.svg'),
    'review_file':'review-v3.json','review_sha256':sha(O/'review-v3.json'),
    'gate':'passed','formal_write_or_sync':False,
    'acceptance':'prior accepted v2 + explicit administrative status-only maintenance; no new review'})
print((O/'staging-manifest-v3.json').read_text(encoding='utf8'))
