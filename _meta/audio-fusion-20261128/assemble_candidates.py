from pathlib import Path
import sys,json,hashlib,re,subprocess,difflib
root=Path(r'D:\上课资料\CityU');work=Path(r'E:\app-data\codex\scratchpad\ef5560-final-20261128')
sys.path.insert(0,str(root/'_meta/tools'))
from safe_write import atomic_write
from merge_apply import apply_cells,render
from note_release_gate import quality_gate
course='EF5560_Fintech_and_AI_in_Finance'
names={'m11':'M11-数字信贷与众筹.md','m12':'M12-智能投顾网络安全与监管科技.md'}
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def columns(line):return [x.strip() for x in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
def safe_s8(text, rows, log):
    lines=text.split('\n');start=next(i for i,l in enumerate(lines) if l.startswith('## 8.'))
    stop=next((i for i in range(start+1,len(lines)) if lines[i].startswith('## ')),len(lines))
    header=next(i for i in range(start,stop) if lines[i].startswith('|') and '课堂覆盖' in lines[i])
    cells=columns(lines[header]);ci=next(i for i,c in enumerate(cells) if '课堂覆盖' in c)
    for item in rows:
        key=str(item['page']).strip('* ')
        hits=[i for i in range(header+2,stop) if lines[i].startswith('|') and columns(lines[i])[0].strip('* ')==key]
        assert len(hits)==1,(key,len(hits))
        i=hits[0];parts=columns(lines[i]);assert len(parts)==len(cells),(key,len(parts),len(cells))
        parts[ci]=item['coverage'];lines[i]='| '+' | '.join(parts)+' |'
    log.append('§8: split only unescaped pipes; exact row replacements='+str(len(rows)))
    return '\n'.join(lines)
for mod in sys.argv[1:] or names:
    folder=work/mod;name=names[mod];note=f'{course}/notes/{name}';baseline=work/('baseline-'+name)
    source=baseline.read_text(encoding='utf-8');assert digest(root/note)==digest(baseline),'正式基线变化，停止'
    patch=json.loads((folder/'patch.json').read_text(encoding='utf-8'))
    findings=json.loads((folder/'findings.json').read_text(encoding='utf-8'))
    main=json.loads((folder/'main.json').read_text(encoding='utf-8'))
    for field in [patch.get('status',''),findings.get('status',''),main.get('status','')]:
        assert 'draft' not in field.lower() and 'pending' not in field.lower(),field
    text=source;log=[]
    pre=folder/'pre-replacements.json'
    if pre.exists():
        data=json.loads(pre.read_text(encoding='utf-8'))
        for rp in data.get('replacements',data if isinstance(data,list) else []):
            assert text.count(rp['old'])==1,(mod,'pre',rp['old'][:100],text.count(rp['old']))
            text=text.replace(rp['old'],rp['new']);log.append('pre structure exact replacement')
    text='\n'.join(apply_cells(text.split('\n'),patch.get('cells',[]),log))
    text=safe_s8(text,patch.get('s8',[]),log)
    text='\n'.join(render(text.split('\n'),findings,main,log))
    text=text.rstrip('\n')+'\n';atomic_write(str(folder/'merged.md'),text)
    assert source==baseline.read_text(encoding='utf-8')
    diff=''.join(difflib.unified_diff(source.splitlines(True),text.splitlines(True),fromfile=note,tofile=note))
    atomic_write(str(folder/'candidate.diff'),diff)
    report={'module':mod,'note':note,'scope':'changed','source_sha256':digest(baseline),'candidate_sha256':digest(folder/'merged.md'),'cells_in_patch':len(patch.get('cells',[])),'s8_rows':len(patch.get('s8',[])),'log':log,'compatibility':'Scratch assembler reuses merge_apply apply_cells/render; stock CLI cannot add §6.2/§9.5/coverage header before applying rows and split(|) mishandles escaped wiki aliases. Baseline never replaced by preprocessed copy; official audit and note_release_gate still required.'}
    atomic_write(str(folder/'assembly.json'),json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(mod,report['candidate_sha256'],report['cells_in_patch'],report['s8_rows'])
