from pathlib import Path
import sys,json,hashlib,shutil,re,collections
sys.dont_write_bytecode=True
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
P=Path(__file__).parent
V5=P.parent/'dot-package-v5-20261119'
PREVIEW=P.parents[2]/'preview/is5542-m09-dot-v6'
VAULT=Path('D:/上课资料/CityU')
NOTE='IS5542_GenAI_in_Business/notes/M09-AI法律问题-版权责任与客户资料.md'
SOURCE=VAULT/'IS5542_GenAI_in_Business/course_files_export/canvas-20261118/IS5542-Guest Lecture6.pdf'
EXPECTED='a96bf9a2b4acdee09c4c8cde1b9e9d5f3d05fbdb3a8a041f67dbf77747ec5e47'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,text):
    p=P/name;p.parent.mkdir(parents=True,exist_ok=True);atomic_write(str(p),text.rstrip()+'\n')
def put(name,obj):write(name,json.dumps(obj,ensure_ascii=False,indent=2))
def copy(src,dst):
    p=P/dst;p.parent.mkdir(parents=True,exist_ok=True)
    if not p.exists():shutil.copy2(src,p)
    assert sha(p)==sha(src),str(p)
assert sha(P/'candidate.md')==EXPECTED
assert sha(SOURCE)=='1c1a107695d0236055ca898b801e0dcd459b207e84572d3e8abd3c88f2444ec0'
raw=(P/'mechanical-final.txt').read_text(encoding='utf-8-sig')
q=json.loads(raw[raw.index('JSON:')+5:])
put('mechanical-final.json',q)
assert not q['C']['hard'] and not q['R']['hard']
before=json.loads((V5/'warning-dispositions.json').read_text(encoding='utf-8'))
v5lines=(V5/'candidate.md').read_text(encoding='utf-8').splitlines()
lines=(P/'candidate.md').read_text(encoding='utf-8').splitlines()
olditems={(i['layer'],i['code'],i['line'],i['message']):i for i in before['items']}
items=[]
for code,line,message in q['R']['warn']:
    key=('R',code,line,message);assert key in olditems,('new warning requires actual disposition',key)
    assert lines[line-1]==v5lines[line-1],('changed warned line',line)
    item=dict(olditems[key]);item['actual_line']=lines[line-1]
    item['v6_carry_forward']='Actual v6 warning and entire warned line match v5; two changed §9.5 status paragraphs occur later. Reason/independent teaching evidence unchanged.'
    items.append(item)
for w in q['C']['warn']:
    key=('C',w['code'],w['line'],w['message']);assert key in olditems,key
    item=dict(olditems[key]);item['v6_carry_forward']='Actual v6 code/section/line/message unchanged, source identity and teaching unchanged.';items.append(item)
put('warning-dispositions.json',{'candidate_sha256':EXPECTED,'mechanical_sha256':sha(P/'mechanical-final.json'),'R_actual':len(q['R']['warn']),'C_actual':len(q['C']['warn']),'every_actual_warning_has_disposition':len(items)==len(q['R']['warn'])+len(q['C']['warn']),'items':items,'no_new_current_warning_unchecked':True,'v5_dispositions_preserved':'history/v5-warning-dispositions.json'})
write('warning-dispositions.md',f'''# M09 v6 实际警告继承核对

候选 `{EXPECTED}`。v6实际重跑current/strict：C.hard=0、R.hard=0，C.warn={len(q['C']['warn'])}、R.warn={len(q['R']['warn'])}。

逐条核了当前code/line/message，全部与v5同条一致；每条R警告的实际完整行也与v5相同。两处§9.5制造状态修正均在这些警告之后，没有以旧数量代替当前运行。每条具体处置理由、上下文、独审依据保留在JSON，不以“未变”代替原有实质核对。

v5警告清单与v4 FAIL均保留历史。这里仅处理可读性启发式和非内容页，不升级法律当前状态。''')
put('warning-version-map.json',[{'layer':i['layer'],'code':i['code'],'v6_line':i['line'],'v5_line':i['line'],'reviewed_v2_line':i.get('v2_line'),'actual_warning_unchanged':True,'actual_R_line_unchanged':i['layer']=='R'} for i in items])
for f in PREVIEW.rglob('*'):
    if f.is_file():copy(f,'preview/'+str(f.relative_to(PREVIEW)))
copy(V5/'image-binding.json','image-binding.json')
imgs=json.loads((P/'image-binding.json').read_text(encoding='utf-8'))
for im in imgs:assert sha(P/im['file'])==im['sha256']
oldmanifest=json.loads((V5/'staging-manifest.json').read_text(encoding='utf-8'))
for a in oldmanifest['actions']:
    path=Path(a['target']);a['target_exists']=path.exists();a['target_sha256']=sha(path) if path.exists() else None
    if a['source'].endswith('candidate.md'):a['source']=str(P/'candidate.md');a['sha256']=EXPECTED
    else:a['source']=str(P/Path(a['source']).relative_to(V5))
    assert not path.exists() or a['target_sha256']==a['sha256'],'Unexpected conflicting formal target'
oldmanifest.update({'candidate_sha256':EXPECTED,'candidate_bytes':(P/'candidate.md').stat().st_size,'release_status':'scratch only; exact-v6 UI/root observations pending until separate verified receipt','scope':'scratch v6 prepared; no formal writes'})
put('staging-manifest.json',oldmanifest)
limits=json.loads((V5/'scope-and-limits.json').read_text(encoding='utf-8'))
limits['candidate_sha256']=EXPECTED
limits['deferred_nonblocking_source_limits'][-1]='§9.5首尾已只修真实制造状态，完整中间重点待核法律段UTF-8字节与v5相同；无新增Git/Notion/个人学习完成断言。'
put('scope-and-limits.json',limits)
put('mechanical-summary-final.json',{'candidate_sha256':EXPECTED,'bytes':(P/'candidate.md').stat().st_size,'C_hard':q['C']['hard'],'R_hard':q['R']['hard'],'C_warn':len(q['C']['warn']),'R_warn':len(q['R']['warn']),'warning_codes':dict(collections.Counter(x[0] for x in q['R']['warn'])),'actual_current_warnings_disposed':True,'source_pages':65,'images':9,'section9_5_middle_identical':True,'source_contract':q['C']['source_coverage']})
print(json.dumps({'candidate_sha256':EXPECTED,'C_warn':len(q['C']['warn']),'R_warn':len(q['R']['warn']),'hard':0,'preview':str(P/'preview/binding.json')},ensure_ascii=False))
