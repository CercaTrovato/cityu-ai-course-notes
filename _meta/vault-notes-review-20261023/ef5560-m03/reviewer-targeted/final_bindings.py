from pathlib import Path
import json, hashlib, difflib, re
import numpy as np

root=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61')
out=root/'reviewer-targeted'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
candidate=root/'candidate-repaired-v7.md'
text=candidate.read_text(encoding='utf-8')
bound={name:sha(root/name) for name in ['formal-baseline.md.snapshot','candidate.md','candidate-repaired-v3.md','candidate-repaired-v4.md','candidate-repaired-v5.md','candidate-repaired-v6.md','candidate-repaired-v7.md','reviewer/independent-review.md','reviewer-targeted/stage-1.md']}
blocks={}
for version in ['v3','v4','v5','v6','v7']:
    blocks[version]=re.findall(r'```mermaid\n(.*?)```',(root/f'candidate-repaired-{version}.md').read_text(encoding='utf-8'),re.S)
v4=(root/'candidate-repaired-v4.md').read_text(encoding='utf-8').splitlines(True)
v5=(root/'candidate-repaired-v5.md').read_text(encoding='utf-8').splitlines(True)
(out/'v4-v5-independent.diff').write_text(''.join(difflib.unified_diff(v4,v5,fromfile='v4',tofile='v5')),encoding='utf-8')
pairs=[]
for version_a,version_b in [('v3','v4'),('v4','v5'),('v5','v6'),('v6','v7')]:
    a=(root/f'candidate-repaired-{version_a}.md').read_text(encoding='utf-8').splitlines()
    b=(root/f'candidate-repaired-{version_b}.md').read_text(encoding='utf-8').splitlines()
    changes=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag!='equal':changes.append({'type':tag,'before':[i+1,j],'after':[k+1,l]})
    pairs.append({'from':version_a,'to':version_b,'change_blocks':changes})
    (out/f'{version_a}-{version_b}-independent.diff').write_text(''.join(difflib.unified_diff(
        (root/f'candidate-repaired-{version_a}.md').read_text(encoding='utf-8').splitlines(True),
        (root/f'candidate-repaired-{version_b}.md').read_text(encoding='utf-8').splitlines(True),
        fromfile=version_a,tofile=version_b)),encoding='utf-8')
a=np.array([1.5,1.5,3.0]); b=np.array([1.0,2.0,3.0]);ad=a-a.mean();bd=b-b.mean()
summary={'bound_hashes':bound,'final_lines':len(text.splitlines()),'mermaid_counts':{k:len(v) for k,v in blocks.items()},
 'mermaid_v3_v4_unchanged':blocks['v3']==blocks['v4'],'mermaid_v4_v5_unchanged':blocks['v4']==blocks['v5'],
 'mermaid_v5_v6_unchanged':blocks['v5']==blocks['v6'],'mermaid_v6_v7_unchanged':blocks['v6']==blocks['v7'],
 'differences':pairs,'ties':{'means':[float(a.mean()),float(b.mean())],'product_sum':float(ad@bd),
  'squares':[float(ad@ad),float(bd@bd)],'correlation':float((ad@bd)/np.sqrt((ad@ad)*(bd@bd)))}}
(out/'final-bindings.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
