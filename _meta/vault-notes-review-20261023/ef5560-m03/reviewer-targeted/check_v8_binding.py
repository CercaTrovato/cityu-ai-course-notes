from pathlib import Path
import hashlib, json, re, difflib

root=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61')
old=(root/'candidate-repaired-v7.md').read_text(encoding='utf-8')
new=(root/'candidate-final-v8.md').read_text(encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changes=[]
for op,a,b,c,d in difflib.SequenceMatcher(None,old.splitlines(),new.splitlines(),autojunk=False).get_opcodes():
    if op!='equal':changes.append({'op':op,'v7_lines':[a+1,b],'v8_lines':[c+1,d],
        'old':old.splitlines()[a:b],'new':new.splitlines()[c:d]})
code=lambda text:re.findall(r'```python\n(.*?)```',text,re.S)
graph=lambda text:re.findall(r'```mermaid\n(.*?)```',text,re.S)
summary={'v7_sha256':sha(root/'candidate-repaired-v7.md'),'v8_sha256':sha(root/'candidate-final-v8.md'),
 'v8_bytes':(root/'candidate-final-v8.md').stat().st_size,
 'independent_review_sha256':sha(root/'reviewer-targeted/independent-review.md'),
 'full_review_sha256':sha(root/'reviewer/independent-review.md'),
 'section_0_through_end_identical':old[old.index('## 0.'):] == new[new.index('## 0.'):],
 'section_0_through_end_bytes_identical':(root/'candidate-repaired-v7.md').read_bytes().split(b'## 0.',1)[1] == (root/'candidate-final-v8.md').read_bytes().split(b'## 0.',1)[1],
 'python_block_count':len(code(new)),'python_blocks_identical':code(old)==code(new),
 'mermaid_count':len(graph(new)),'mermaid_identical':graph(old)==graph(new),
 'changes':changes}
(root/'reviewer-targeted/final-v8-binding-evidence.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
