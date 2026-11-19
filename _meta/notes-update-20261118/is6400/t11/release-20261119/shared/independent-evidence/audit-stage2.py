from pathlib import Path
from datetime import datetime,timezone
import json,re,hashlib,base64,ast,difflib,sys
from PIL import Image
R=Path('D:/上课资料/CityU');W=Path(__file__).parent.parent;O=Path(__file__).parent;P=R/'_meta/notes-update-20261118/is6400/t11'
sys.path.insert(0,str(R/'_meta/tools'));from safe_write import atomic_write
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def js(name,v):
    p=O/name;assert not p.exists();atomic_write(str(p),json.dumps(v,ensure_ascii=False,indent=2)+'\n')
nbpath=R/'IS6400_Business_Data_Analytics/course_files_export/canvas-20261118/Week 11 selection.ipynb'
assert sha(nbpath)=='a1b85cb3d817cf64e5fbe2ccc7fbdbf86c99f3bf76834f2e09269e10dd0c17a2'
nb=json.loads(nbpath.read_text(encoding='utf-8'));text=(W/'candidate.md').read_text(encoding='utf-8');a12=(W/'a12-learning-candidate.md').read_text(encoding='utf-8')
assert sha(W/'candidate.md')=='5c3b876cc27a1951b7eca79d32bc13da1ef84e88173530b9320ddfbf056312be'
assert sha(W/'a12-learning-candidate.md')=='13f1a87de7503d84135de9f4709fbe0b4e3ba3a6423f3754d7cfae2ac3ead7bd'
heads=list(re.finditer(r'(?m)^### 2\.\d+ cell (\d+) · (.+)$',text));sections={int(m[1]):text[m.start():heads[i+1].start() if i+1<len(heads) else text.index('\n## 3.',m.end())] for i,m in enumerate(heads)}
assert len(sections)==len(nb['cells'])==63
run=json.loads((P/'source-run.json').read_text(encoding='utf-8'));bycell={x['cell']:x for x in run['results']}
rows=[];original_pngs=[]
for i,c in enumerate(nb['cells'],1):
    src=''.join(c['source']);sec=sections[i];r={'cell':i,'type':c['cell_type'],'source_sha256':hashlib.sha256(src.encode()).hexdigest(),'candidate_heading':heads[i-1][0].strip(),'candidate_section_present':True,'source_markdown_read_directly':c['cell_type']=='markdown'}
    if c['cell_type']=='code':
        codes=re.findall(r'```python\n(.*?)\n```',sec,re.S);r['code_exact']=len(codes)==1 and codes[0].strip()==src.strip();assert r['code_exact'],i
        r['recorded_source_run_code_hash_matches']=bycell[i]['source_sha256']==r['source_sha256'];assert r['recorded_source_run_code_hash_matches']
        outs=[]
        for oi,out in enumerate(c.get('outputs',[]),1):
            if 'text' in out:outs.append(''.join(out['text']))
            if 'text/plain' in out.get('data',{}):outs.append(''.join(out['data']['text/plain']))
            if 'image/png' in out.get('data',{}):
                b=base64.b64decode(''.join(out['data']['image/png']));h=hashlib.sha256(b).hexdigest();p=R/f'IS6400_Business_Data_Analytics/notes/figures/t11-source/cell-{i:02d}-out-{oi:02d}.png';assert sha(p)==h
                original_pngs.append({'cell':i,'output':oi,'formal_path':str(p),'source_decoded_sha256':h,'formal_exact':True})
        r['saved_text_outputs_count']=len(outs);r['saved_text_outputs_fully_present']=all(o.strip() in sec for o in outs)
        if not r['saved_text_outputs_fully_present']:assert i==44
        r['output_treatment']='cell44 repetitive CV log transparently excerpted, full log persistent in source Notebook/source-saved-outputs.txt' if i==44 else 'complete saved text output present'
        r['recorded_source_run_error']=bycell[i]['error'];assert bycell[i]['error'] is None
    rows.append(r)
assert len(original_pngs)==9
questions=[line.strip() for line in ''.join(nb['cells'][62]['source']).splitlines() if re.match(r'^\d\.',line)]
assert len(questions)==3
for q in questions:assert q in text and q in a12
figs=json.loads((P/'all-figures.json').read_text(encoding='utf-8'));assert len(figs)==13
observations={5:'Black observed points; X about1-5 radians, Y about+1 to-1; no prediction legend.',8:'Power15 title; predicted blue and real orange; mostly near-fit on scaled x0-1.',12:'Power15 validation; at right x about1 predicted blue differs substantially from orange, as described.',14:'lambda0.1 title, no legend; blue smooth prediction and orange observations, source plotting order supplies identities.',17:'Ridge validation blue/orange right-end discrepancy remains; same scaled x.',33:'Original full tree small; large persistent image read root x[7]<=0.049, gini0.468, samples426, value159/267; True subtree x[23]<=952.9 and False subtree x[23]<=785.8; deeper leaves including value0/4 and1/0 visible in large carrier.',34:'Pruned index5 tree; root426 and159/267, True260 value13/247; x[13]<=42.19; left247 value4/243; False166 value146/20, x[10]<=0.192; title still5-th, candidate explicitly corrects zero-index count.',35:'Only one root, gini0.468, samples426, value159/267, no feature rule; majority benign.',37:'Top nodes from31 to3, bottom depth8 to1 as alpha increases to~0.034; depth plateaus while nodes still reduce.',48:'Official StratifiedKFold image has sample index0-100, CV0-4, red test / blue train; class/group rows differ and group not isolated.',29:'Prior-run step curve total impurity0 to~0.14 over alpha0 to~0.034; root-only last alpha omitted.'}
figure_rows=[]
for f in figs:
    p=R/f['formal_path'];assert sha(p)==f['sha256'];assert sha(Path(f['path']))==f['sha256'];im=Image.open(p)
    assert str(Path(f['formal_path']).relative_to('IS6400_Business_Data_Analytics/notes')).replace('\\','/') in text
    figure_rows.append({'cell':f['cell'],'formal_path':f['formal_path'],'sha256':sha(p),'pixels':list(im.size),'matching_manifest_and_source_carrier':True,'actual_current_reviewer_view':'view_image tool opened formal image directly during Stage2; not final browser display','actual_observation':observations[f['cell']]})

formal_t11=R/'IS6400_Business_Data_Analytics/notes/T11-模型选择实战-Ridge剪枝与交叉验证.md'
formal_a12=R/'IS6400_Business_Data_Analytics/assignment/graded/A12-week11-model-selection/notes/学习参考.md'
link_rows=[]
for formal,txt in [(formal_t11,text),(formal_a12,a12)]:
    for match in re.finditer(r'!?\[[^\]]*\]\(([^)]+)\)',txt):
        s=match[1]
        if s.startswith(('http','mailto','#')):continue
        p=(formal.parent/s).resolve();link_rows.append({'from':str(formal),'link':s,'resolved':str(p),'exists':p.exists(),'sha256':sha(p) if p.is_file() else None})
assert all(x['exists'] for x in link_rows)
script=formal_a12.parent.parent/'work/learning-reference.py';assert script.resolve().parents[5]==R
executed=(P/'reference-protocol-executed.py').read_text(encoding='utf-8');persistent=script.read_text(encoding='utf-8')
logicdiff=list(difflib.unified_diff(executed.splitlines(),persistent.splitlines(),n=1));assert len(logicdiff)<35
js('stage-2-script-path-diff.json',{'executed_original':str(P/'reference-protocol-executed.py'),'executed_sha256':sha(P/'reference-protocol-executed.py'),'persistent_script':str(script),'persistent_sha256':sha(script),'diff_lines':logicdiff,'observed_scope':'only root/output paths, progress suppression and output file name; model/data/split code unchanged','actual_root_discovery':str(script.resolve().parents[5]),'powerShell_command_interpreter_exists':Path('D:/anaconda3/python.exe').exists(),'linked_output_exists':(script.parent/'learning-reference-results.json').exists()})
prechecks=[]
for name in ['candidate.md.precheck.txt','a12-learning-candidate.md.precheck.txt']:
    s=(W/name).read_text(encoding='utf-8');q=json.loads(next(line[5:] for line in s.splitlines() if line.startswith('JSON:')))
    prechecks.append({'file':name,'log_sha256':sha(W/name),'L':q['legacy_problems'],'C_hard':q['C']['hard'],'R_hard':q['R']['hard'],'C_warn':q['C']['warn'],'R_warn':q['R']['warn'],'source_coverage':q['C']['source_coverage'],'limits':'existing author precheck only; not new run; no source contract supplied, source fidelity separately audited here'})
js('stage-2-existing-mechanical-warnings.json',prechecks)
rules=['_meta/笔记制作与融合验收流程.md','_meta/可读性总规则.md','_meta/逐页学习与课件图示规范.md','_meta/机制理解与可读性标准.md','_meta/课件题目处理规则.md','_meta/课堂练习完成与解析规范.md','_meta/材料处理规则.md','IS6400_Business_Data_Analytics/AGENTS.md','IS6400_Business_Data_Analytics/_meta/IS6400可读性细则.md','IS6400_Business_Data_Analytics/_meta/IS6400作业制作规范.md']
receipt={'schema':'cityu-independent-source-audit-stage2-v1','created_utc':datetime.now(timezone.utc).isoformat(),'reviewer_id':'/root/cityu_is5113_package','source':str(nbpath),'source_sha256':sha(nbpath),'candidate_sha256':sha(W/'candidate.md'),'a12_candidate_sha256':sha(W/'a12-learning-candidate.md'),'source_cells':63,'source_markdown_cells':30,'source_code_cells':33,'code_exact_count':sum(x.get('code_exact',False) for x in rows),'source_run_code_hash_matches':sum(x.get('recorded_source_run_code_hash_matches',False) for x in rows),'new_execution_of_classroom33cells':False,'source_run_recorded_errors':len(run['errors']),'source_saved_text_full_count':sum(x.get('saved_text_outputs_fully_present',False) for x in rows),'cell44_excerpt_explicit':True,'all_three_assignment_questions_exact_in_both_candidates':True,'rows':rows,'original_png_byte_audit':original_pngs,'figures':figure_rows,'reader_links':link_rows,'rules_consulted':[{'path':x,'sha256':sha(R/x)} for x in rules],'previous_reports_and_closure_records':[{'path':str(P/x),'sha256':sha(P/x)} for x in ['stage-1.md','stage-2.md','independent-review.md','independent-replay-results.json','directed-revision.json','candidate-directed.diff','a12-learning-candidate-directed.diff','all-figures.json','cell-evidence.json','source-run.json','run_source.py','reference-protocol-executed.py','canvas-admin.json']],'bound_new_replay':'stage-2-new-replay-verification.json','new_replay_status':json.loads((O/'stage-2-new-replay-verification.json').read_text(encoding='utf-8')),'final_browser_ui':'not performed by this reviewer','formal_or_old_evidence_writes':'none'}
js('stage-2-source-receipt.json',receipt)
print(json.dumps({'cells':len(rows),'code_exact':sum(x.get('code_exact',False) for x in rows),'saved_text_fully_present':sum(x.get('saved_text_outputs_fully_present',False) for x in rows),'original_pngs':len(original_pngs),'all_figures_currently_viewed':len(figs),'reader_links_verified':len(link_rows),'receipt':str(O/'stage-2-source-receipt.json'),'precheck_counts':[{'file':q['file'],'L':len(q['L']),'C_hard':len(q['C_hard']),'R_hard':len(q['R_hard']),'C_warn':len(q['C_warn']),'R_warn':len(q['R_warn'])} for q in prechecks]},ensure_ascii=False,indent=2))
