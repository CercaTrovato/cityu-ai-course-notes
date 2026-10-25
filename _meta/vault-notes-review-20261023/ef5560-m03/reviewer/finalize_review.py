from pathlib import Path
import hashlib,json
OUT=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61/reviewer')
M=json.loads((OUT.parent/'source-map.json').read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
checks=[]
for item in M['originals']:
    actual=sha(item['path'])
    checks.append({'path':item['path'],'actual_sha256':actual,'expected_sha256':item['sha256'],'unchanged':actual==item['sha256']})
checks.extend({'path':M[key]['path'],'actual_sha256':sha(M[key]['path']),'expected_sha256':M[key]['sha256'],'unchanged':sha(M[key]['path'])==M[key]['sha256']} for key in ['candidate','formal_baseline'])
(OUT/'final-readonly-verification.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
assets=[]
for p in sorted(OUT.rglob('*')):
    if not p.is_file() or 'edge-review-profile' in p.parts or p.name=='assets-sha256.json':continue
    assets.append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)})
for p in [OUT.parent/'source-map.json',OUT.parent/'candidate.md',OUT.parent/'formal-baseline.md.snapshot',Path('D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance/notes/figures/readability-v2/pcr-pls-directions.svg'),Path('D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance/notes/figures/readability-v2/plots_calc.py')]:
    assets.append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p),'role':'read-only external evidence'})
(OUT/'assets-sha256.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2),encoding='utf-8')
print('original_count',len(M['originals']),'final_unchanged',all(x['unchanged'] for x in checks))
print('stage1_sha256',sha(OUT/'stage-1.md'))
print('independent_review_sha256',sha(OUT/'independent-review.md'))
print('assets_count',len(assets))
print('report_lines',len((OUT/'independent-review.md').read_text(encoding='utf-8').splitlines()))
