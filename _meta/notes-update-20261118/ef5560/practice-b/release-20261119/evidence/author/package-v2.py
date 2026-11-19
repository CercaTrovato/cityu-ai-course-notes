from pathlib import Path
import json,hashlib,re,shutil
d=Path(__file__).resolve().parent; out=d/'release-v2-20261119'; reviewer=d.parent/'practice-exam-b-dot-review'; vault=Path('D:/上课资料/CityU'); preview=d.parents[1]/'preview/ef5560-practice-b-dot-v2'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,v:p.write_text(v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
expected='3ad3cc324dbff2e2b04bb525e2d087014d86db8ee7a0bade19b029d5fcb1f68d'
assert sha(d/'candidate-v2.md')==expected
target='EF5560_Fintech_and_AI_in_Finance/assignment/practice/practice-exam-b/学习解析.md'
assert not (vault/target).exists()
out.mkdir(exist_ok=True); (out/'evidence/author').mkdir(parents=True,exist_ok=True)
for p in d.iterdir():
 if p.is_file():shutil.copy2(p,out/'evidence/author'/p.name)
shutil.copytree(reviewer,out/'evidence/reviewer',dirs_exist_ok=True)
shutil.copytree(d/'figures',out/'figures',dirs_exist_ok=True)
shutil.copytree(preview,out/'preview',dirs_exist_ok=True)
shutil.copy2(d/'candidate-v2.md',out/'candidate.md')
assert sha(out/'evidence/reviewer/directed-recheck-v2.md')=='73ffa79783b7768ffe69ae898cea9ee031714247c8b86cf89165de7679c37dac'
for p in reviewer.rglob('*'):
 if p.is_file():assert sha(p)==sha(out/'evidence/reviewer'/p.relative_to(reviewer))
raw=(d/'mechanical-v2.txt').read_text('utf-8-sig'); machine=next(json.loads(x[5:]) for x in raw.splitlines() if x.startswith('JSON:'))
assert not machine['legacy_problems'] and not machine['C']['hard'] and not machine['R']['hard']
write(out/'mechanical-final.json',machine)
text=(d/'candidate-v2.md').read_text('utf-8'); lines=text.splitlines()
items=[]
for w in machine['C']['warn']:
 section=w['section']
 if section.startswith('0.'):reason='Roadmap summarizes assessed units; it is not an extra calculation needing proof.'
 elif section.startswith('2.1 '):reason='Cover administrative instructions fully retained and interpreted in §1; no algorithm to invent.'
 elif section.startswith('2.13 ') or section.startswith('2.14 '):reason='Actual SCRAP PAPER pages with no questions; candidate explicitly preserves this non-content identity.'
 elif section.startswith('2.2.2'):reason='A2 locally gives excess-return definition, exact −.60%−.04%=−.64% and exclusion of other denominators; reviewer independently reproduced.'
 elif section.startswith('2.4.1'):reason='A7 explicitly computes aggregate cap800k minus existing600k =200k and distinguishes credit approval.'
 elif section.startswith('2.5.1'):reason='A10 directly distinguishes short-term underlying asset income less expenses from transfer counts/fee revenue; all four choices explained.'
 elif section.startswith('2.6.3'):reason='A15 locally computes total400, platform100, investor300 and rejects double counting; independently reproduced.'
 elif section.startswith('6.'):reason='Answer-organization framework, not another exam question; all28 actual English answers retained locally.'
 else:reason='Page-level source container preceding its numbered child questions. Exact original question page is retained as text/image; substantive explanations are the immediate child A/B/C units, independently checked in original stages and preserved in v2. Container is not a missing solution.'
 items.append({**w,'disposition':reason})
for code,line,message in machine['R']['warn']:
 actual=lines[line-1]
 if code=='R8a':reason='Four-level question heading retains original A/B/C unit beneath a unique §2 page entry. Maximum depth4; deliberate page+question navigation rather than a fifth-level fragment. Original reviewer checked all28 units and v2 heading mappings.'
 elif code=='R8b':reason='First paragraph gives answer and needed definitions/boundary of one question. Sentence count does not remove an input or require new proof; full learner redoing evidence supports it.'
 elif code=='R5b':reason='Parallel equations share defined quantities: A7 cap/headroom or C1 two standardized inputs. Each substituted value, denominator and final interpretation is given nearby; independent arithmetic rechecked both, so no unexplained equality jump.'
 elif code=='R5a':reason='B2(b) introduces one hidden-unit formula, named inputs/parameters and combined output in one mechanism. max rule and concrete m2/v1 versus v3 example explain transformation; original full learner review found no need for professional knowledge to fill it.'
 elif code=='R2b':reason='Numbered check/action is one coherent decision with concrete why: B1(b)security/target alignment; B3(b)total cost or completion. No steps are elided. List length is a warning, and original full stage1 reconstructed these exact tasks.'
 elif code=='R2a':reason='Single local inference/example with explicit conditions, not a bare jargon paragraph: A14 calibration/loss distinction, B2 tree/hidden-unit transfer, C1 fixed scaling or zero-coefficient limits. Source and learner reviews cover unchanged wording.'
 elif code=='R1c':reason='Semicolons enumerate linked objects in the same question: custody/evidence/rights, hidden-unit example states, or standardized-input/scaling values. Their distinct roles are locally explained, no condition is removed.'
 elif code=='R1e':reason='Separate necessary distinctions (retained revenue/profit; excess/raw realized return) prevent materially wrong answers; positive numeric result is already given, not only denials.'
 elif code=='R4c':reason='Short recap/term table cell, not the location of full reasoning; corresponding local question retains detailed calculations.'
 elif code=='R4f':reason='B3(a) table states all percentages use USD1000 and computes each retained amount; C2 table introduced as assets/shares in millions and USD/share with numerator/denominator defined. Table cells show formulas and adjoining prose reads the result.'
 elif code=='R7a':reason='Single source SHA in source identification is traceability metadata, not a quantity the learner must decode or calculate.'
 elif code=='R3a':reason='§1 groups source identity, original cover constraints, learning status and three reading routes; these are explicit separate paragraphs, not an unexplained core algorithm. Original reviewer examined retained cover and final navigation, no missing condition.'
 elif code in ('R6d','R6b','R6a'):
  if any(x in actual for x in ['USD','HKD','RMB','NAV10']):reason='Currency amount tokenization (USD/HKD/RMB plus digits) or repeated NAV is not a new technical acronym. Local Chinese uses exact dollars/yuan and reproduces each computation.'
  elif 'SCRAP' in actual or 'PAPER' in actual:reason='Original source label immediately explained as blank scrap paper, not two unexplained technical concepts.'
  elif any(x in actual for x in ['A1/','A2/','A8/']):reason='Question IDs in review index are navigation labels, not a cluster of new concepts.'
  else:reason='Local definition/meaning is already supplied: A1 significance/p-value, A2 excess=stock−risk-free, A3 SSE/SST meanings, A5 peak-to-trough, A6 CAPM and market exposure, A11 NAV, A13 price gap, A14 PD/LGD/EAD Chinese names and calibration role. Later occurrences recall the same object; no extra numeric loss model is required by A14. Full independent review reconstructed current tasks.'
 else:raise RuntimeError('Unhandled R '+code)
 items.append({'code':code,'line':line,'message':message,'actual_text':actual,'disposition':reason})
write(out/'warning-dispositions.json',{'candidate_sha256':expected,'C_warn':len(machine['C']['warn']),'R_warn':len(machine['R']['warn']),'items':items})
original=(d/'candidate.md').read_text('utf-8'); sourceblocks=lambda t:re.findall(r'```text\n(.*?)\n```',t,re.S)
assert sourceblocks(original)==sourceblocks(text) and len(sourceblocks(text))==14
write(out/'manual-source-contract.json',{'candidate_sha256':expected,'source_pdf_sha256':'2e748c176ac2632536b00818e6b2a898aa0ffad28e4d689b7598533b63ac1dd5','source_pages':14,'exact_source_text_blocks':14,'questions':22,'answer_units':28,'MC_options':64,'English_reference_answers':text.count('English reference:'),'basis':'Author direct PDF reextraction + independent actual14-page visual/text comparison in stage2-source-binding.json; directed final review independently proved source blocks/14images/28English answers unchanged.','machine_source_contract':'unverified_without_manifest: source questions retained in literal text fences, which checker strip_code excludes. No fake machine source PASS; manual and independent actual source evidence supplied instead.'})
binding=json.loads((preview/'binding.json').read_text('utf-8-sig')); rawhtml=(preview/'index.html').read_bytes(); lfsha=hashlib.sha256(rawhtml.replace(b'\r\n',b'\n')).hexdigest(); assert binding['sha256']==expected and binding['html_sha256']==lfsha
images=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text);assert len(images)==14
for p in images:assert sha(d/p)==sha(preview/p)
write(out/'preview-binding.json',{'candidate_sha256':expected,'raw_html_sha256':hashlib.sha256(rawhtml).hexdigest(),'LF_html_sha256':lfsha,'CRLF_pairs':rawhtml.count(b'\r\n'),'binding_original':binding,'source_image_hashes':14,'explanation':'Windows generator hashes in-memory LF before write_text CRLF; raw and normalized hashes recorded, no semantic HTML rewrite.'})
write(out/'root-final-display.json',{'observer':'/root','candidate_sha256':expected,'status':'passed','received':'2026-11-19','preview':'http://127.0.0.1:8796/ef5560-practice-b-dot-v2/','evidence':'Actual IAB banner3ad3…;14/14 images,22math,3Mermaid,15folds; no errors/broken internal anchors/overflow1265=1265. p11 source table readable. Root clicked selftest and saw5% max drawdown, nonnegative new capacity, standardization.','boundary':'Actual root observation attributed, not author independent review or source-only visual proof.'})
write(out/'target-guard.json',{'note':target,'target_exists':False,'current_target_sha256':None,'structure_basis':'Existing course assignment/practice/练习索引.md confirms practice root; substantial stand-alone exam gets practice-exam-b/学习解析.md rather than lecture or graded submission. New descriptive folder, not a claim that it already exists.','root_action':'recheck absence before atomic new-file write; stop if concurrent target appears. Figures relative to new analysis file directory.'})
report='''# Practice B v2 release package

Author/packager: /root/cityu_review_probe. Independent reviewer: /root/legal_stage_review. Candidate SHA: '''+expected+'''.

Original full stage1 then14-page stage2 and directed final closure are preserved exactly under evidence/reviewer. Original P1 was fixed in actual candidate-v2; source/answers unchanged evidence and metadata-only final hash closure are explicit in directed report. This packaging is not an author self-review.

## Original failure and real repair

Old candidate and mechanical-precheck.txt preserve exit2 找不到 §2 正文. It was not waived. v2 has §§0–9, page-level §2 units and original question subheads; actual current L/C.hard/R.hard all0. Original reviewer separately examined the new recap/navigation, P1 ratio condition, retained sources/answers and final metadata change. Exact v1-to-v2 diff, response and original snapshots remain evidence/author. Candidate's frozen pending statements are historical author-state, superseded by this receipt's independent/visual evidence, not altered to fake events.

## Source and solutions

14 source pages,22 questions,28 answer units,64 choices. All14 original text blocks,14 source-page images and28 English answers retained. Source PDF hash, direct reextraction, original independent14-page actual visuals and final preservation comparison are bound. manual-source-contract.json openly distinguishes real source verification from machine strip_code limitations; no machine source-manifest PASS claimed. Reference answers are not official answers; current Canvas/administrative unknowns remain. No actual exam submission or personal-learning status changed.

## Warnings

Current20 C and108 R warnings each listed at actual line with disposition. Page containers, cover and scrap identities are not unsolved questions; A2/A7/A10/A15 have specific local definition/calculation/option reasoning. Four-level headings preserve page+question indexing; metrics, paired formulas, lists, currency tokenization and table-column flags are individually mapped to source/learning evidence. All raw results remain, no hard item is dismissed. §§0/3/5/6/8 recap additions were independently examined.

## Final display

Exact candidate/banner and source-image hashes bound in preview-binding.json; LF memory vs raw Windows CRLF HTML difference explicitly proved. Root actual IAB22math/3diagrams/14images/15folds and interaction evidence attributed in root-final-display.json. Original reviewer source visuals and root final display remain distinct. No author pretend-browser claim.

## Publication boundary

New target under existing course assignment/practice structure, absence guard required. Only scratch package; no formal vault, Notion, Git or personal state changes. Root must recheck target absence and atomically write candidate plus figures, preserve source/independent evidence, then read back exact SHA. This draft learning analysis is not an officially graded answer or actual exam-rule confirmation.
'''
write(out/'review.md',report)
source=vault/'EF5560_Fintech_and_AI_in_Finance/course_files_export/canvas-20261118/practice_exam_B.pdf'; assert sha(source)=='2e748c176ac2632536b00818e6b2a898aa0ffad28e4d689b7598533b63ac1dd5'
files=[p for p in out.rglob('*') if p.is_file() and p.name not in ('review.json','staging-manifest.json','gate-output.txt')]
assets=[{'path':str(p.relative_to(out)).replace('\\','/'),'sha256':sha(p)} for p in files]+[{'path':str(source),'sha256':sha(source)}]
write(out/'review.json',{'schema':'note-review-v2','note':target,'scope':'full','source_sha256':None,'candidate_sha256':expected,'review_file':'review.md','review_sha256':sha(out/'review.md'),'checks':{'understanding':{'status':'passed','evidence':'evidence/reviewer/stage-1.md + stage-2-combined.md + directed-recheck-v2.md; exact independent chain'},'sources':{'status':'passed','evidence':'manual-source-contract.json + independent stage2-source-binding.json; all14 original source pages and final preservation check'},'warnings':{'status':'passed','evidence':'mechanical-final.json + warning-dispositions.json;20C/108R all listed; old exit2 and real v2 structure fix preserved'},'visuals':{'status':'passed','evidence':'root-final-display.json + preview-binding.json; root actual exact-v2 IAB, not reviewer source images'}},'independent_review':{'author_ids':['/root/cityu_review_probe'],'reviewer_id':'/root/legal_stage_review','perspective':'high-school-beginner','status':'passed','candidate_sha256':expected,'report_file':'evidence/reviewer/directed-recheck-v2.md','report_sha256':sha(out/'evidence/reviewer/directed-recheck-v2.md')},'assets':assets,'unresolved':[]})
write(out/'staging-manifest.json',{'candidate_sha256':expected,'target':target,'target_absence_required':True,'files':[{'path':str(p.relative_to(out)).replace('\\','/'),'sha256':sha(p)} for p in out.rglob('*') if p.is_file() and p.name!='staging-manifest.json']})
print(json.dumps({'out':str(out),'review_sha256':sha(out/'review.json'),'candidate_sha256':expected,'warnings':len(items),'images':len(images)},ensure_ascii=False))
