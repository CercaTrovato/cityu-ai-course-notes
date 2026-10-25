from pathlib import Path
import difflib, hashlib, json, re

p=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61/dependency-sync')
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda f:Path(f).read_text(encoding='utf-8-sig')
spec=json.loads(read(p/'sync-proposals-v4.json'))
repairs=json.loads(read(p/'v3-v4-repairs.json'))
rows=[]
for t in spec['targets']:
    bp=Path(t['baseline']);cp=Path(t['candidate']) if t.get('candidate') else bp
    b,c=bp.read_bytes(),cp.read_bytes()
    own=list(difflib.unified_diff(read(bp).splitlines(True),read(cp).splitlines(True),fromfile=t['path'],tofile=t['id']+' proposal'))
    supplied=p/'proposals-v4'/f"{t['id']}.diff"
    d=read(supplied).splitlines(True) if supplied.exists() else []
    rec={'id':t['id'],'formal_path':t['path'],'baseline_sha256':sha(b),'candidate_sha256':sha(c),'baseline_match':sha(b)==t['baseline_sha256'],'candidate_match':sha(c)==t['candidate_sha256'],'no_increment':b==c,'diff_body_match':own[2:]==d[2:]}
    if t.get('candidate'):
        prev=read(p/'proposals-v3'/f"{t['id']}.md")
        transformed=prev
        for r in repairs:
            if r['id']==t['id']:
                assert transformed.count(r['old'])==1,(t['id'],r['old'])
                transformed=transformed.replace(r['old'],r['new'],1)
        rec['v3_v4_exact_logged_repair_only']=transformed==read(cp)
    rows.append(rec)
tables={}
for fid,line,expected in [('f02',35,5),('f02',245,3),('f03',245,6)]+[('f07',i,5) for i in range(629,641)]:
    text=read(p/'proposals-v4'/f'{fid}.md').splitlines()[line-1]
    count=len(re.findall(r'(?<!\\)\|',text))
    tables[f'{fid}:{line}']={'delimiters':count,'expected':expected,'ok':count==expected}
e={'reviewer_id':'/root/review_ef_m03_sync_61','scope':'all 30 original operations plus same-review local repairs and affected context; 14 targets','targets':rows,'v3_v4_repairs_exact':all(r.get('v3_v4_exact_logged_repair_only',True) for r in rows),'tables':tables,'stage1_sha256':sha((p/'reviewer-sync/stage-1.md').read_bytes())}
(p/'reviewer-sync/final-v4-evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'all_baseline_candidate_hashes_match':all(r['baseline_match'] and r['candidate_match'] for r in rows),'all_full_diff_bodies_match':all(r['diff_body_match'] for r in rows),'v3_v4_repairs_exact':e['v3_v4_repairs_exact'],'all_15_affected_rows_have_expected_columns':all(v['ok'] for v in tables.values()),'stage1_sha256':e['stage1_sha256']},ensure_ascii=False,indent=2))
