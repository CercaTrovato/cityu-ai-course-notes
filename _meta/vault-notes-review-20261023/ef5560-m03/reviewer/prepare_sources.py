from pathlib import Path
import json, hashlib, zipfile, difflib, subprocess, re

ROOT=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61')
OUT=ROOT/'reviewer'
MAP=json.loads((ROOT/'source-map.json').read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
hashes=[]
for item in MAP['originals']:
    path=Path(item['path'])
    actual=sha(path) if path.exists() else None
    hashes.append({'path':str(path),'expected':item['sha256'],'actual':actual,'match':actual==item['sha256']})
for p in MAP['rules']:
    hashes.append({'path':p,'actual':sha(p),'role':'current rule'})
(OUT/'source-hashes.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2),encoding='utf-8')
base=Path(MAP['formal_baseline']['path']).read_text(encoding='utf-8-sig')
cand=Path(MAP['candidate']['path']).read_text(encoding='utf-8-sig')
diff=''.join(difflib.unified_diff(base.splitlines(True),cand.splitlines(True),fromfile='formal-baseline',tofile='candidate',n=3))
(OUT/'baseline-candidate.diff').write_text(diff,encoding='utf-8')
with zipfile.ZipFile(MAP['originals'][2]['path']) as z:
    files=[]
    for info in z.infolist():
        if info.is_dir(): continue
        dest=(OUT/'zip-original'/info.filename).resolve()
        if not dest.is_relative_to((OUT/'zip-original').resolve()): raise ValueError(info.filename)
        dest.parent.mkdir(parents=True,exist_ok=True)
        data=z.read(info)
        dest.write_bytes(data)
        files.append({'name':info.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(OUT/'zip-inventory.json').write_text(json.dumps(files,ensure_ascii=False,indent=2),encoding='utf-8')
for name,idx in [('old56',0),('new54',1),('syllabus',3)]:
    subprocess.run(['D:/poppler/Library/bin/pdftotext.exe','-layout',MAP['originals'][idx]['path'],str(OUT/(name+'-layout.txt'))],check=True)
    text=(OUT/(name+'-layout.txt')).read_text(encoding='utf-8')
    pages=text.split('\f')
    if not pages[-1].strip(): pages.pop()
    (OUT/(name+'-pages.json')).write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
    print(name,'pages=',len(pages),'chars=',len(text))
blocks=[]
for i,m in enumerate(re.finditer(r'```python\s*\n(.*?)\n```',cand,re.S),1):
    p=OUT/f'candidate-python-{i}.py'
    p.write_text(m.group(1),encoding='utf-8')
    blocks.append({'id':i,'candidate_line':cand[:m.start()].count('\n')+1,'path':str(p),'lines':len(m.group(1).splitlines())})
(OUT/'candidate-python-blocks.json').write_text(json.dumps(blocks,ensure_ascii=False,indent=2),encoding='utf-8')
print('mapped_hashes_all_match=',all(x.get('match',True) for x in hashes))
print('diff_lines=',len(diff.splitlines()),'plus=',sum(x.startswith('+') and not x.startswith('+++') for x in diff.splitlines()),'minus=',sum(x.startswith('-') and not x.startswith('---') for x in diff.splitlines()))
print('zip_files=',len(files),'blocks=',blocks)
