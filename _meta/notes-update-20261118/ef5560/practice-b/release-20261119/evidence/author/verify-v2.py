from pathlib import Path
import json,re,hashlib
d=Path(__file__).resolve().parent
s=(d/'mechanical-v2.txt').read_text('utf-8-sig'); j=next(json.loads(x[5:]) for x in s.splitlines() if x.startswith('JSON:'))
v=(d/'candidate-v2.md').read_text('utf-8'); old=(d/'candidate.md').read_text('utf-8')
a=re.findall(r'```text\n(.*?)\n```',old,re.S); b=re.findall(r'```text\n(.*?)\n```',v,re.S)
assert a==b and len(b)==14
assert re.findall(r'!\[[^\]]*\]\(([^)]+)\)',old)==re.findall(r'!\[[^\]]*\]\(([^)]+)\)',v)
assert v.count('English reference:')==28
summary={'candidate_sha256':hashlib.sha256((d/'candidate-v2.md').read_bytes()).hexdigest(),'exit_code':0,'L':j['legacy_problems'],'C_hard':j['C']['hard'],'C_warn':j['C']['warn'],'R_hard':j['R']['hard'],'R_warn':j['R']['warn'],'exact_source_blocks_unchanged':len(b),'English_reference_count':v.count('English reference:'),'source_contract':'Manual exact14 source blocks retained; original reviewer full source pass unchanged, directed v2 pending; no machine source manifest supplied'}
(d/'mechanical-v2-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not j['legacy_problems'] and not j['C']['hard'] and not j['R']['hard']
print(json.dumps({k:len(summary[k]) for k in ['L','C_hard','C_warn','R_hard','R_warn']},ensure_ascii=False))
