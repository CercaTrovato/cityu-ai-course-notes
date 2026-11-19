from pathlib import Path
import sys,json,hashlib,shutil,re,difflib
sys.dont_write_bytecode=True
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
P=Path(__file__).parent
V5=P.parent/'dot-package-v5-20261119'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):
    p=P/name;p.parent.mkdir(parents=True,exist_ok=True)
    atomic_write(str(p),json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def write(name,text):
    p=P/name;p.parent.mkdir(parents=True,exist_ok=True);atomic_write(str(p),text)
def copy(src,dst):
    p=P/dst;p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():assert sha(src)==sha(p)
    else:shutil.copy2(src,p)
    assert sha(src)==sha(p)
assert sha(V5/'candidate.md')=='affad4efa641eaa9d287285460873ab36d33eef5298f18e1bf3cfe4cff3b65d3'
for dirname in ['evidence','figures','history']:
    for f in (V5/dirname).rglob('*'):
        if f.is_file():copy(f,str(f.relative_to(V5)))
for name in ['candidate.md','review.md','review.json','gate-output-final.txt','root-final-display-v5.json','mechanical-final.json','mechanical-final.txt','warning-dispositions.json','warning-version-map.json','maintenance-binding.json','maintenance-exact.diff','staging-manifest.json']:
    copy(V5/name,'history/v5-'+name)
text=(V5/'candidate.md').read_text(encoding='utf-8')
old1='本篇已形成逐页候选，仍待独立高中知识起点两阶段审查、来源问题定向核验、Mermaid 与原图在最终阅读尺寸的实际显示、机械疑点处理及正式发布门槛。65 页源页实际视觉已看，不等于最终笔记显示已看。'
new1='本篇65页源页已实际视觉跟读，并完成本篇讲义学习范围的独立审查与定向复核。源页阅读、最终笔记显示和发布回执分别留证；不把来源保真等同为现行法律核查。'
old2='未写入正式笔记、课程元文件、Notion 或 Git；未改变本人通读、自测、复习、出席、提交或评分状态。此候选未被接受，不能据其存在宣称 M09 已完成。'
new2='本篇是讲义版学习材料；不代表本人通读、自测、复习、出席、提交或评分状态发生变化。'
assert text.count(old1)==text.count(old2)==1
v6=text.replace(old1,new1).replace(old2,new2)
marker='重点待核：'
mid5=next(l for l in text.splitlines() if l.startswith(marker))
mid6=next(l for l in v6.splitlines() if l.startswith(marker))
assert mid5.encode('utf-8')==mid6.encode('utf-8')
write('candidate.md',v6)
write('maintenance-v5-v6.diff',''.join(difflib.unified_diff(text.splitlines(True),v6.splitlines(True),fromfile='v5-affad4',tofile='v6-status-only')))
parent_binding=json.loads((V5/'maintenance-binding.json').read_text(encoding='utf-8'))
oldlines=(P/'history/candidate-v2.md').read_text(encoding='utf-8').splitlines();newlines=v6.splitlines()
mapping={}
for block in difflib.SequenceMatcher(None,oldlines,newlines,autojunk=False).get_matching_blocks():
    for o in range(block.size):mapping[block.b+o+1]=block.a+o+1
put('maintenance-binding.json',{'reviewed_candidate_sha256':parent_binding['reviewed_candidate_sha256'],'prepared_candidate_sha256':sha(P/'candidate.md'),'intermediate_v5_sha256':sha(V5/'candidate.md'),'v2_v5_exact_reconstruction_evidence':'history/v5-maintenance-binding.json','v5_v6_actual_changes':[[old1,new1],[old2,new2]],'current_law_middle_paragraph_byte_identical':True,'other_v5_text_unchanged':True,'unchanged_line_map_v6_to_v2':mapping,'independent_reviewer_did_not_read_v5_or_v6':True,'basis':'Parent requested manufacturing-status correction only. No change to lesson, legal conditions/numbers, figures, original questions, source limits or personal state.'})
put('root-final-display-v6-pending.json',{'candidate_sha256':sha(P/'candidate.md'),'status':'pending root exact-v6 IAB observations','v5_result':'history/v5-root-final-display-v5.json retained only as old-version evidence; not claimed to cover exact-v6 rendering','root_instruction':'Keep current law middle paragraph byte-identical; final UI only after actual v6 check.'})
print(json.dumps({'candidate_sha256':sha(P/'candidate.md'),'bytes':(P/'candidate.md').stat().st_size,'changes':2,'current_law_paragraph_identical':True},ensure_ascii=False))
