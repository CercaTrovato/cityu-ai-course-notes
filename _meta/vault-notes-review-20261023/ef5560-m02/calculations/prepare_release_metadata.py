import hashlib,json,sys,subprocess
from pathlib import Path
B=Path(__file__).parent;R=Path('D:/上课资料/CityU');sys.path.insert(0,str(R/'_meta/tools'))
from safe_write import atomic_write
src=B/'candidate.md';text=src.read_text(encoding='utf-8');assert hashlib.sha256(src.read_bytes()).hexdigest()=='2fd0501e90f9892a07604b896e13f3d52f7db17eadf83bb8edbd05ebd5235102'
changes=[]
for old,new in [('updated: 2026-10-23','updated: 2026-10-25'),('mechanism_review: pending','mechanism_review: passed'),('mechanism_review_mode: efficient-20261002','mechanism_review_mode: full-independent-20261023'),('readability_review: pending\n---','readability_review: passed\n---'),('该历史状态不覆盖本次 frontmatter 的 `mechanism_review/readability_review: pending`。','该历史状态不作为本次全篇审查的依据；现行结论由本任务 full/v2 回执与当前 frontmatter 共同记录。')]:
 assert text.count(old)==1,(old,text.count(old));changes.append({'old':old,'new':new});text=text.replace(old,new,1)
out=B/'author/release-metadata-proposed.md';atomic_write(out,text)
rec={'schema':'nonteaching-release-metadata-v1','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'changes':changes,'condition':'Independent full plus targeted understanding/sources accepted; formal publication still requires current gate, CAS writeback and sync separately.'}
atomic_write(B/'author/release-metadata-changes.json',json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
course=R/'EF5560_Fintech_and_AI_in_Finance';args=[sys.executable,'-X','utf8',str(R/'_meta/tools/transcript_check.py'),'audit',str(out),'--transcript',*[str(course/'transcripts'/n) for n in ['M02-transcript-part1.txt','M02-transcript-part2.txt','M01-transcript.txt']],'--json']
p=subprocess.run(args,cwd=R,capture_output=True,text=True,encoding='utf-8');atomic_write(B/'main-source/material-final.json',p.stdout);data=json.loads(p.stdout);print(json.dumps({'sha256':rec['candidate_sha256'],'metadata_changes':5,'audit_exit':p.returncode,'verdict':data['verdict'],'fails':data['fails'],'warns':data['warns'],'info':data['info']},ensure_ascii=False))
