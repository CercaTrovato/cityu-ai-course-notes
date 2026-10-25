from pathlib import Path
import hashlib,re,json,difflib
root=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61')
old=(root/'candidate-final-v11.md').read_bytes();new=(root/'candidate-final-v12.md').read_bytes()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
blocks=lambda data,kind:re.findall(rb'```'+kind+rb'\r?\n(.*?)```',data,re.S)
display=lambda data:re.findall(rb'\$\$.*?\$\$',data,re.S)
a=old.decode('utf-8').splitlines();b=new.decode('utf-8').splitlines();changes=[]
for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
    if tag!='equal':changes.append({'type':tag,'before':[i+1,j],'after':[k+1,l],'old':a[i:j],'new':b[k:l]})
test_pp=[1,1];cases=[]
for c in [-1,0,1]:
    errors=[y-c for y in test_pp];squares=[e*e for e in errors]
    cases.append({'c_percent':c,'errors_pp':errors,'squares_pp_squared':squares,'SSE_pp_squared':sum(squares),'R2_against_zero':1-sum(squares)/2})
result={'v11_sha256':sha(root/'candidate-final-v11.md'),'v12_sha256':sha(root/'candidate-final-v12.md'),
 'v12_bytes':len(new),'changes':changes,'constant_forecast_example':cases,
 'coefficient_conditional_example':{'z_spread_old':0.5,'z_spread_new':1.5,'other_z_rate':-1,'old_prediction_pct':0.2+0.4*0.5-0.3*(-1),'new_prediction_pct':0.2+0.4*1.5-0.3*(-1),'change_pp':0.4},
 'mermaid_count':len(blocks(new,b'mermaid')),'mermaid_bytes_equal':blocks(old,b'mermaid')==blocks(new,b'mermaid'),
 'python_count':len(blocks(new,b'python')),'python_bytes_equal':blocks(old,b'python')==blocks(new,b'python'),
 'display_math_count':len(display(new)),'display_math_bytes_equal':display(old)==display(new)}
(root/'reviewer-targeted/final-v12-binding-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='changes'},ensure_ascii=False,indent=2))
