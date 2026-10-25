from pathlib import Path
import hashlib,re,json,difflib
root=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
blocks=lambda data,kind:re.findall(rb'```'+kind+rb'\r?\n(.*?)```',data,re.S)
display=lambda data:re.findall(rb'\$\$.*?\$\$',data,re.S)
docs={v:(root/f'candidate-final-v{v}.md').read_bytes() for v in [11,12,13,14,15]}
pairs=[]
for prev,nxt in [(11,12),(12,13),(13,14),(14,15)]:
    a=docs[prev].decode('utf-8').splitlines();b=docs[nxt].decode('utf-8').splitlines();changes=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag!='equal':changes.append({'type':tag,'before':[i+1,j],'after':[k+1,l],'old':a[i:j],'new':b[k:l]})
    pairs.append({'from':prev,'to':nxt,'changes':changes})
result={'hashes':{f'v{v}':sha(root/f'candidate-final-v{v}.md') for v in docs},'v15_bytes':len(docs[15]),
 'pairs':pairs,'mermaid_counts':{str(v):len(blocks(docs[v],b'mermaid')) for v in docs},
 'python_counts':{str(v):len(blocks(docs[v],b'python')) for v in docs},
 'display_math_counts':{str(v):len(display(docs[v])) for v in docs},
 'v11_to_v15_mermaid_bytes_equal':blocks(docs[11],b'mermaid')==blocks(docs[15],b'mermaid'),
 'v11_to_v15_python_bytes_equal':blocks(docs[11],b'python')==blocks(docs[15],b'python'),
 'v11_to_v15_display_math_bytes_equal':display(docs[11])==display(docs[15]),
 'constant_counterexample_labeled': '**💡 数字反例（笔记补充）**：两只股票测试收益都为 +1%' in docs[15].decode('utf-8')}
(root/'reviewer-targeted/final-v15-binding-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='pairs'},ensure_ascii=False,indent=2))
