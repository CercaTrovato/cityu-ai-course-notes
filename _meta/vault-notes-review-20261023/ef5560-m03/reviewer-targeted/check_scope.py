from pathlib import Path
import json, hashlib, difflib, collections

root = Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61')
out = root / 'reviewer-targeted'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
files = ['formal-baseline.md.snapshot', 'candidate.md', 'candidate-repaired-v3.md']
doc = {name: (root/name).read_text(encoding='utf-8') for name in files}
original = doc['candidate.md'].splitlines()
repaired = doc['candidate-repaired-v3.md'].splitlines()

def heading(lines, end):
    h = [line for line in lines[:end+1] if line.startswith(('## ', '### ', '#### '))]
    return h[-1] if h else '(frontmatter/intro)'

changes = []
for tag, a, b, c, d in difflib.SequenceMatcher(None, original, repaired, autojunk=False).get_opcodes():
    if tag != 'equal':
        changes.append({'tag':tag,'original_lines':[a+1,b],'v3_lines':[c+1,d],
            'heading':heading(repaired,c),'old':original[a:b],'new':repaired[c:d]})
(out/'initial-to-v3-diff.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'initial-to-v3.diff').write_text(''.join(difflib.unified_diff(
    doc['candidate.md'].splitlines(True),doc['candidate-repaired-v3.md'].splitlines(True),fromfile='candidate.md',tofile='candidate-repaired-v3.md')),encoding='utf-8')

patches = {}
for f in ['repairs-v1.json','repairs-v2.json','v3-fixes.json']:
    obj=json.loads((root/f).read_text(encoding='utf-8-sig'))
    items=obj if isinstance(obj,list) else obj.get('replacements',obj.get('operations',[]))
    patches[f]={'type':type(obj).__name__,'keys':list(obj) if isinstance(obj,dict) else [],'count':len(items),
        'issues':dict(collections.Counter(x.get('issue','(none)') for x in items)),
        'no_ops':[i+1 for i,x in enumerate(items) if x.get('old')==x.get('new')]}
sources=json.loads((root/'source-map.json').read_text(encoding='utf-8-sig'))
hashes=[{'path':x['path'],'actual':sha(Path(x['path'])),'expected':x['sha256']} for x in sources['originals']]
summary={'candidate_hashes':{f:sha(root/f) for f in files},
 'full_review_hash':sha(root/'reviewer/independent-review.md'),'patches':patches,'diff_change_count':len(changes),
 'diff_section_counts':dict(collections.Counter(x['heading'] for x in changes)),
 'sources':hashes,'source_mismatches':[x['path'] for x in hashes if x['actual']!=x['expected']]}
(out/'scope-and-hash-audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='sources'},ensure_ascii=False,indent=2))
