from pathlib import Path
import hashlib, re, difflib, json

root=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61')
old_b=(root/'candidate-final-v8.md').read_bytes()
new_b=(root/'candidate-final-v9.md').read_bytes()
old=old_b.decode('utf-8');new=new_b.decode('utf-8')
normal=lambda s:re.sub(r'\s+','',re.sub(r'(?m)^> ?','',s))
changes=[]
for op,a,b,c,d in difflib.SequenceMatcher(None,old.splitlines(),new.splitlines(),autojunk=False).get_opcodes():
    if op!='equal':
        before='\n'.join(old.splitlines()[a:b]);after='\n'.join(new.splitlines()[c:d])
        changes.append({'op':op,'v8_lines':[a+1,b],'v9_lines':[c+1,d],
          'same_nonwhitespace_after_removing_quote_prefix':normal(before)==normal(after),
          'before':before,'after':after})
blocks=lambda data,kind:re.findall(rb'```'+kind+rb'\r?\n(.*?)```',data,re.S)
math=lambda data:re.findall(rb'\$\$.*?\$\$|(?<!\$)\$(?!\$)[^\r\n$]*?\$(?!\$)',data,re.S)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
result={'v8_sha256':sha(root/'candidate-final-v8.md'),'v9_sha256':sha(root/'candidate-final-v9.md'),
 'v9_bytes':len(new_b),'diff_blocks':changes,
 'first_10_blocks_only_quote_prefix_and_whitespace':len(changes)==11 and all(x['same_nonwhitespace_after_removing_quote_prefix'] for x in changes[:10]),
 'mermaid_count':len(blocks(new_b,b'mermaid')),'mermaid_bytes_equal':blocks(old_b,b'mermaid')==blocks(new_b,b'mermaid'),
 'python_count':len(blocks(new_b,b'python')),'python_bytes_equal':blocks(old_b,b'python')==blocks(new_b,b'python'),
 'math_fragments_count':len(math(new_b)),'math_bytes_equal':math(old_b)==math(new_b),
 'v8_binding_sha256':sha(root/'reviewer-targeted/final-v8-binding.md'),
 'v7_closure_report_sha256':sha(root/'reviewer-targeted/independent-review.md')}
(root/'reviewer-targeted/final-v9-binding-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='diff_blocks'},ensure_ascii=False,indent=2))
