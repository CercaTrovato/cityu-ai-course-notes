from pathlib import Path
import csv, difflib, hashlib, io, json, re, subprocess, zipfile
import pandas as pd
import numpy as np

root = Path('D:/上课资料/CityU')
scratch = Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61')
dep = scratch / 'dependency-sync'
out = dep / 'reviewer-sync'
sha = lambda b: hashlib.sha256(b).hexdigest()
read = lambda p: Path(p).read_text(encoding='utf-8-sig')
e = {'stage1_sha256_before': sha((out/'stage-1.md').read_bytes())}
for version in ('v1','v3'):
    spec = json.loads(read(dep/f'sync-proposals-{version}.json'))
    records = []
    for t in spec['targets']:
        bpath = Path(t['baseline'])
        bbytes = bpath.read_bytes()
        cpath = Path(t['candidate']) if t.get('candidate') else bpath
        cbytes = cpath.read_bytes()
        bt, ct = read(bpath), read(cpath)
        own = ''.join(difflib.unified_diff(bt.splitlines(True),ct.splitlines(True),fromfile=t['path'],tofile=f"{t['id']} proposal"))
        supplied = dep/f'proposals-{version}'/f"{t['id']}.diff"
        supplied_text = read(supplied) if supplied.exists() else ''
        # Line endings are normalized by read_text; compare every actual diff line.
        rec = {'id':t['id'],'formal_path':t['path'],'baseline_sha256':sha(bbytes),'baseline_matches_manifest':sha(bbytes)==t['baseline_sha256'],'candidate_sha256':sha(cbytes),'candidate_matches_manifest':sha(cbytes)==t['candidate_sha256'],'no_increment': bbytes==cbytes,'operations':len(t['operations']),'independent_diff_sha256':sha(own.encode()),'supplied_diff_exists':supplied.exists(),'supplied_diff_matches':own==supplied_text}
        if own and own != supplied_text:
            rec['diff_headers'] = [own.splitlines()[:2],supplied_text.splitlines()[:2]]
            rec['diff_body_matches'] = own.splitlines()[2:]==supplied_text.splitlines()[2:]
        records.append(rec)
    e[version] = records
    e[f'{version}_operation_count'] = sum(r['operations'] for r in records)

sm = json.loads(read(scratch/'source-map.json'))
e['originals'] = [{'path':o['path'],'sha256':sha(Path(o['path']).read_bytes()),'matches_source_map':sha(Path(o['path']).read_bytes())==o['sha256']} for o in sm['originals']]
course = root/'EF5560_Fintech_and_AI_in_Finance'
old = course/'course_files_export/class03/class03'
zpath = course/'course_files_export/class03.zip'
with zipfile.ZipFile(zpath) as z:
    files = {Path(n).name:z.read(n) for n in z.namelist() if not n.endswith('/')}
    e['zip_difference'] = [{'name':n,'equal':(old/n).read_bytes()==b,'old_sha256':sha((old/n).read_bytes()),'zip_sha256':sha(b)} for n,b in sorted(files.items())]
    e['manifests'] = []
    for label, payload, getbytes in [('old',(old/'manifest.json').read_bytes(),lambda n:(old/n).read_bytes()),('zip',files['manifest.json'],lambda n:files[n])]:
        manifest = json.loads(payload)
        checks=[]
        for item in manifest['files']:
            b = getbytes(item['file'])
            rows=list(csv.reader(io.StringIO(b.decode('utf-8-sig'))))
            checks.append({'file':item['file'],'rows':len(rows)-1,'hash_ok':sha(b)==item['sha256'],'bytes_ok':len(b)==item['bytes'],'rows_ok':len(rows)-1==item['rows'],'columns_ok':rows[0]==item['columns']})
        e['manifests'].append({'version':label,'files':checks})
    m=pd.read_csv(old/'market_excess_return_panel.csv')
    mz=pd.read_csv(io.BytesIO(files['market_excess_return_panel.csv']))
    s=pd.read_csv(old/'hsi_stock_excess_return_panel.csv')
    usable=s.loc[s.usable_for_ml.astype(str).str.lower().eq('true')]
    y=m.risk_free_yield_lag1_pct/100
    yz=mz.risk_free_yield_lag1_pct/100
    ys=s.risk_free_yield_pct/100
    e['data']={'market_shape':list(m.shape),'stock_shape':list(s.shape),'market_us_splits':m.loc[m.market.eq('US_SPY')].groupby('split').size().to_dict(),'stock_usable_splits':usable.groupby('split').size().to_dict(),'stock_weeks':usable.groupby('split').forecast_week.nunique().to_dict(),'rank_columns':sum(c.endswith('_rank') for c in s.columns),'old_rf_simple_maxerror':float(np.abs(m.risk_free_return-((1+y)**(1/12)-1)).max()),'zip_rf_log_maxerror':float(np.abs(mz.risk_free_return-np.log1p(yz)/12).max()),'weekly_rf_maxerror':float(np.abs(s.risk_free_return-((1+ys)**(7/365)-1)).max()),'old_zip_total_return_maxdifference':float(np.abs(m.market_total_return-mz.market_total_return).max())}

runs=json.loads(read(root/'_meta/vault-notes-review-20261023/ef5560-m03/formal-code-runs.json'))
e['formal_runs_identity']=[]
for run in runs:
    name=Path(run['script']).name
    stdout=scratch/f'formal-{name}.stdout.txt'
    stderr=scratch/f'formal-{name}.stderr.txt'
    e['formal_runs_identity'].append({'script':run['script'],'script_sha256':sha((root/run['script']).read_bytes()),'script_matches':sha((root/run['script']).read_bytes())==run['script_sha256'],'stdout_sha256':sha(stdout.read_bytes()),'stdout_matches':sha(stdout.read_bytes())==run['stdout_sha256'],'stderr_sha256':sha(stderr.read_bytes()),'stderr_matches':sha(stderr.read_bytes())==run['stderr_sha256'],'recorded_exit':run['exit'],'execution_this_stage':False})

transcript=read(course/'transcripts/M03-transcript.txt')
stamps=re.findall(r'^\s*((?:\d{2}:)?\d{2}:\d{2})\s*$',transcript,re.M)
e['transcript']={'records':len(stamps),'unique':len(set(stamps)),'first':stamps[0],'last':stamps[-1],'duplicates':sorted({x for x in stamps if stamps.count(x)>1})}
sections=re.split(r'^\s*((?:\d{2}:)?\d{2}:\d{2})\s*$',transcript,flags=re.M)
wanted={'05:35','05:48','06:01','01:05:54','01:06:15','01:09:55','01:10:54','01:12:16','01:15:01','01:15:16','01:16:18','01:16:59','01:38:49','01:41:00','01:42:16','01:51:47','01:51:59','01:54:11','01:55:31','01:59:10','02:17:41','02:18:48','02:19:00','02:21:28','02:23:49','02:24:04'}
e['transcript_excerpt']=[{'time':sections[i],'text':sections[i+1].strip()} for i in range(1,len(sections)-1,2) if sections[i] in wanted]

pdf_pages={}
for label,pdf in [('old56',sm['originals'][0]['path']),('new54',sm['originals'][1]['path'])]:
    p=subprocess.run(['D:/poppler/Library/bin/pdftotext.exe','-layout',pdf,'-'],check=True,capture_output=True)
    pages=p.stdout.decode('utf-8').split('\f')
    if not pages[-1].strip(): pages.pop()
    selected=[5,8,12,13,14,15,17,19,20,22,25,26,27,30,32,37,38,41,44,47,50,51,54,55,56] if label=='old56' else [22,25,26,27,36,39,43,45,48,49,52,53,54]
    pdf_pages[label]={'pages':len(pages),'selected':{str(i):pages[i-1] for i in selected}}
e['pdf_page_counts']={k:v['pages'] for k,v in pdf_pages.items()}
(out/'stage2-fresh-pdf-text.json').write_text(json.dumps(pdf_pages,ensure_ascii=False,indent=2),encoding='utf-8')
e['stage1_sha256_after']=sha((out/'stage-1.md').read_bytes())
(out/'stage2-evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:e[k] for k in ['v1_operation_count','v3_operation_count','data','transcript','formal_runs_identity','stage1_sha256_before','stage1_sha256_after']},ensure_ascii=False,indent=2))
print('originals all match:',all(o['matches_source_map'] for o in e['originals']))
print('zip differences:',[x['name'] for x in e['zip_difference'] if not x['equal']])
print('manifest all checks:',all(all(r[k] for k in ['hash_ok','bytes_ok','rows_ok','columns_ok']) for m in e['manifests'] for r in m['files']))
print('diff mismatches:',[(version,r['id'],r.get('diff_body_matches')) for version in ['v1','v3'] for r in e[version] if r['supplied_diff_exists'] and not r['supplied_diff_matches']])
