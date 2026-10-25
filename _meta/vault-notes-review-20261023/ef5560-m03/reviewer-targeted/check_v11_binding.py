from pathlib import Path
import hashlib,re,json,difflib
root=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61')
old=(root/'candidate-final-v10.md').read_bytes();new=(root/'candidate-final-v11.md').read_bytes()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
blocks=lambda data,kind:re.findall(rb'```'+kind+rb'\r?\n(.*?)```',data,re.S)
display=lambda data:re.findall(rb'\$\$.*?\$\$',data,re.S)
stdout=(root/'main-source-checks/04_train_weekly_and_trace.py.stdout.txt').read_text(encoding='utf-8')
scores=[]
for line in stdout.splitlines():
    if 'validation MSE=' in line and 'test OOS R2=' in line:
        model=line.split(' {',1)[0]
        vm=float(line.split('validation MSE=',1)[1].split('test OOS R2=',1)[0])
        score=float(line.split('test OOS R2=',1)[1])
        scores.append({'model':model,'validation_mse':vm,'test_oos_r2_percent':score*100,'rounded_percent':f'{score*100:+.3f}%'})
changes=[]
a=old.decode('utf-8').splitlines();b=new.decode('utf-8').splitlines()
for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
    if tag!='equal':changes.append({'type':tag,'before':[i+1,j],'after':[k+1,l],'old':a[i:j],'new':b[k:l]})
result={'candidate_v10_sha256':sha(root/'candidate-final-v10.md'),'candidate_v11_sha256':sha(root/'candidate-final-v11.md'),
 'v11_bytes':len(new),'changes':changes,'scores_from_existing_stdout':scores,
 'validation_selected':min(scores,key=lambda x:x['validation_mse'])['model'],
 'mermaid_equal':blocks(old,b'mermaid')==blocks(new,b'mermaid'),'mermaid_count':len(blocks(new,b'mermaid')),
 'python_equal':blocks(old,b'python')==blocks(new,b'python'),'python_count':len(blocks(new,b'python')),
 'display_math_equal':display(old)==display(new),'display_math_count':len(display(new)),
 'stdout_sha256':sha(root/'main-source-checks/04_train_weekly_and_trace.py.stdout.txt'),
 'v10_observation_sha256':sha(root/'reviewer-targeted/final-v10-binding.md')}
(root/'reviewer-targeted/final-v11-binding-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='changes'},ensure_ascii=False,indent=2))
