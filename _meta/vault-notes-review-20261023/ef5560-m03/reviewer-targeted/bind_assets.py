from pathlib import Path
import json, hashlib

root=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61')
out=root/'reviewer-targeted'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=[p for p in out.iterdir() if p.is_file() and p.name not in ['assets-sha256.json','independent-review.md']]
mapping=json.loads((root/'source-map.json').read_text(encoding='utf-8-sig'))
paths += [Path(x['path']) for x in mapping['originals']]
paths += [Path(x) for x in mapping['rules']]
paths += [Path('D:/上课资料/CityU/.agents/skills/transcript-merge/SKILL.md'),
          Path('D:/上课资料/CityU/_meta/转录处理规则.md'),Path('D:/上课资料/CityU/_meta/笔记质量规范.md')]
paths += [root/f for f in ['source-map.json','formal-baseline.md.snapshot','candidate.md',
 'candidate-repaired-v3.md','candidate-repaired-v4.md','candidate-repaired-v5.md','candidate-repaired-v6.md','candidate-repaired-v7.md',
 'repairs-v1.json','repairs-v1.diff','repairs-v2.json','repairs-v1-v2.diff','v3-fixes.json','v2-v3.diff',
 'v4-fixes.json','v3-v4.diff','v5-fixes.json','v4-v5.diff','v6-fixes.json','v5-v6.diff','v7-fixes.json','v6-v7.diff',
 'targeted-reading-scope.md','identity-operations-disclosure.json','reviewer/independent-review.md',
 'new-assets/03_train_market.py','new-assets/04_train_weekly_and_trace.py']]
paths += list((root/'main-source-checks').glob('*'))
paths += [root/'reviewer/fresh-pdf-render'/f for f in ['old56-p19.png','old56-p20.png','old56-p24.png','old56-p35.png',
 'old56-p36.png','old56-p43.png','old56-p48.png','new54-p39.png']]
paths += [root/'main-visual-v3'/f for f in ['graph-3-v5.png','graph-5-v5.png','graph-6-v5-top.png','graph-6-v5-bottom.png','graph-4-v5-top.png','graph-4-v5-bottom.png']]
assets=[]
for p in sorted(set(paths)):
    if p.is_file():assets.append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size})
payload={'schema':'targeted-review-assets-v1','final_candidate_sha256':sha(root/'candidate-repaired-v7.md'),
 'reviewer_id':'/root/review_ef_m03_repairs_61','assets':assets}
(out/'assets-sha256.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'asset_count':len(assets),'manifest_sha256':sha(out/'assets-sha256.json'),
 'report_sha256':sha(out/'independent-review.md'),'final_candidate_sha256':sha(root/'candidate-repaired-v7.md')},indent=2))
