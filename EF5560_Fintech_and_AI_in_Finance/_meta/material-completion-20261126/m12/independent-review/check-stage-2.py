from pathlib import Path
import csv, hashlib, json, zipfile
from collections import Counter
import subprocess, re

vault = Path(r'D:\上课资料\CityU')
task = Path(r'E:\app-data\codex\scratchpad\cityu-material-completion-20261126\ef5560')
source = vault / 'EF5560_Fintech_and_AI_in_Finance/course_files_export/canvas-20261126-review/Lec12_Robo_Cybersecurity_and_RegTech.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
pages = [5,10,21,24,26,27,29,30,34,35,36,37,38]
pdfinfo = subprocess.check_output([r'D:\poppler\Library\bin\pdfinfo.exe',str(source)],encoding='utf-8',errors='replace')
page_count = int(re.search(r'Pages:\s+(\d+)',pdfinfo).group(1))
sample_text = {str(p):subprocess.check_output([r'D:\poppler\Library\bin\pdftotext.exe','-f',str(p),'-l',str(p),'-layout',str(source),'-'],encoding='utf-8') for p in pages}
evidence = {'source': str(source), 'source_sha256': sha(source), 'page_count': page_count, 'sample_text': sample_text}
assets = json.loads((task / 'asset-manifest.json').read_text(encoding='utf-8'))
evidence['sample_assets'] = []
for a in assets:
    if a['page'] in [5,10,21,36]:
        observed = sha(Path(a['scratch']))
        evidence['sample_assets'].append({'page':a['page'], 'observed_sha256':observed, 'manifest_sha256':a['sha256'], 'matches':observed==a['sha256'], 'same_as_source_page_png':observed==sha(task/f"p-{a['page']:02d}.png")})
base = vault / 'EF5560_Fintech_and_AI_in_Finance/course_files_export/class03'
evidence['tables'] = []
with zipfile.ZipFile(base.parent/'class03.zip') as z:
    for name in ['stock_linear_quintiles.csv','stock_linear_validation.csv']:
        path = base/'class03'/name
        rows = list(csv.DictReader(path.open(encoding='utf-8-sig',newline='')))
        member = next(n for n in z.namelist() if n.endswith('/'+name) or n==name)
        item = {'name':name, 'sha256':sha(path), 'bytes':path.stat().st_size, 'rows':len(rows), 'columns':list(rows[0]), 'nulls':{k:sum(r[k]=='' for r in rows) for k in rows[0]}, 'models':dict(Counter(r['model'] for r in rows)), 'matches_zip':sha(path)==hashlib.sha256(z.read(member)).hexdigest()}
        if name.startswith('stock_linear_quintiles'):
            rr = {r['forecast_quintile']:float(r['mean_excess_return']) for r in rows if r['model']=='Ridge'}
            item['ridge_q1_q5_spread_pct']=[rr['1']*100,rr['5']*100,(rr['5']-rr['1'])*100]
            item['observations_by_model']={m:sum(int(r['observations']) for r in rows if r['model']==m) for m in item['models']}
        else:
            item['pcr_min'] = min((r for r in rows if r['model']=='PCR'),key=lambda r:float(r['validation_mse']))
        evidence['tables'].append(item)
pred=list(csv.DictReader((base/'class03/stock_linear_test_predictions.csv').open(encoding='utf-8-sig',newline='')))
weeks=Counter(r['forecast_week'] for r in pred)
evidence['test_calendar']={'rows':len(pred),'weeks':len(weeks),'first':min(weeks),'last':max(weeks),'stocks_per_week':sorted(set(weeks.values())), 'lasso_unique':len(set(r['LASSO'] for r in pred)), 'en_unique':len(set(r['Elastic Net'] for r in pred))}
(task/'independent-review/stage-2-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in evidence.items() if k!='sample_text'},ensure_ascii=False,indent=2))
for p in pages:
    print(f'\nPAGE {p}\n{evidence["sample_text"][str(p)]}')
