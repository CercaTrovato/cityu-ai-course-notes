from pathlib import Path
import hashlib, re, difflib, json
root=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61')
old=(root/'candidate-final-v9.md').read_bytes();new=(root/'candidate-final-v10.md').read_bytes()
blocks=lambda data,kind:re.findall(rb'```'+kind+rb'\r?\n(.*?)```',data,re.S)
displaymath=lambda data:re.findall(rb'\$\$.*?\$\$',data,re.S)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changes=[]
a=old.decode('utf-8').splitlines();b=new.decode('utf-8').splitlines()
for op,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
    if op!='equal':changes.append({'op':op,'v9_lines':[i+1,j],'v10_lines':[k+1,l],
        'before':a[i:j],'after':b[k:l]})
result={'v9_sha256':sha(root/'candidate-final-v9.md'),'v10_sha256':sha(root/'candidate-final-v10.md'),
 'v10_bytes':len(new),'changes':changes,'mermaid_count':len(blocks(new,b'mermaid')),
 'mermaid_bytes_equal':blocks(old,b'mermaid')==blocks(new,b'mermaid'),
 'python_count':len(blocks(new,b'python')),'python_bytes_equal':blocks(old,b'python')==blocks(new,b'python'),
 'display_math_count':len(displaymath(new)),'display_math_bytes_equal':displaymath(old)==displaymath(new),
 'source_page50_last_sentence':'Read the model comparison first, then trace the named stock through the fitted rule.',
 'initial_residual':'English answer omits the requested test OOS R2 numerical output; sent targeted fix request. No retraining needed.'}
(root/'reviewer-targeted/final-v10-binding-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='changes'},ensure_ascii=False,indent=2))
