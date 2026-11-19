from pathlib import Path
import json,hashlib,re,shutil
root=Path(__file__).resolve().parent
src=root.parent/'practice_exam_B'
vault=Path('D:/上课资料/CityU')
pdf=vault/'EF5560_Fintech_and_AI_in_Finance/course_files_export/canvas-20261118/practice_exam_B.pdf'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,s:p.write_text(s if isinstance(s,str) else json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
pages=json.loads((src/'pages.json').read_text('utf-8-sig'))
raw_sections=(root/'analysis-sections.json').read_text('utf-8')
# The author input uses literal LaTeX backslashes; JSON newlines remain escaped.
raw_sections=re.sub(r'(?<!\\)\\(?!n)',lambda m:'\\\\',raw_sections)
sections=json.loads(raw_sections)
assert len(pages)==14
(root/'figures/practice-exam-b').mkdir(parents=True,exist_ok=True)
head='''---
course: EF5560
type: practice-exam-learning-analysis
status: draft
learning_status: author-checked-independent-review-pending
official_solution: not_verified
date: 2026-11-19
---

# Practice Examination B · 完整题面与中英学习解析

## 阅读入口与状态

这份卷子给出预测、风险、支付与代币化的情境，要你辨别证据、解释业务流程并复算数字。全卷22题：A区16道选择题（每题2.5分，共40分）；B区4道简答、各含(a)(b)（共40分）；C区2道计算、各含(a)(b)（共20分）。实际作答单元为16+8+4=28。以下逐页保留英文题面及全部选项，再给中文题意、各选项/各小问解析与英文参考作答。

**这是学习解析，不是官方答案、正式提交稿或本人已完成考试的记录。** 所有答案均为题面推理的参考作答；尚未逐项核到官方解答或当前Canvas考试安排。源封面为Semester A 2026/27、两小时、闭卷但允许一张双面A4手写笔记；要求答全部题、A区填字母、C区展示步骤、交整卷及写有座位号/学号的手写参考纸。这是该练习卷的原文要求，不自动推定实际考试日期、当次允许材料或提交入口。不得把本电子解析当作封面所准许的手写参考纸。

来源：`EF5560_Fintech_and_AI_in_Finance/course_files_export/canvas-20261118/practice_exam_B.pdf`，14物理页；1为封面，2–6为A，7–10为B，11–12为C，13–14为草稿纸。全部14页已实际看图，题面用同版本文本排版保留，原图在对应页可核。源PDF SHA-256：SOURCE_SHA。

读法：首次顺读各页；练习时先关解析自己做；复习先用末尾答案索引定位，再重做改条件题。未假定你懂金融或大学统计，必要定义在题旁补足。以下金融讨论只针对假设题面与学习概念，不认证任何产品现行条款、储备或个人投资建议。

## 按页对照
'''.replace('SOURCE_SHA',sha(pdf))
parts=[head]; evidence=[]
for i,page in enumerate(pages,1):
 image=f'figures/practice-exam-b/page-{i:02}.png'; shutil.copy2(src/f'page-{i:02}.png',root/image)
 parts.append(f'\n## p.{i} · '+('封面与卷面规则' if i==1 else '草稿纸' if i>=13 else '题面与解析')+'\n')
 parts.append(f'\n![练习卷B物理p.{i}]({image})\n\n[打开原页大图]({image})\n')
 parts.append('\n<details><summary>英文原题全文（按原页；仅统一换行展示）</summary>\n\n```text\n'+page.rstrip()+'\n```\n\n</details>\n')
 if str(i) in sections: parts.append('\n'+sections[str(i)]+'\n')
 elif i==1:parts.append('\n本页行政要求已在阅读入口逐项解释；座位号/Student ID字段保持空白，不填写或提交。\n')
 else:parts.append('\n本页只写 SCRAP PAPER，无新增题目、选项或答案；保留页身份，不虚构额外两题。\n')
 evidence.append({'physical_page':i,'source_image':image,'sha256':sha(root/image),'viewed':'Actual page PNG viewed by /root/cityu_review_probe at native tool display; all labels/questions legible','content':'cover' if i==1 else 'scrap paper; no questions' if i>=13 else {2:'A1–3',3:'A4–6',4:'A7–9',5:'A10–12',6:'A13–16',7:'B1(a)(b)',8:'B2(a)(b)',9:'B3(a)(b)',10:'B4(a)(b)',11:'C1(a)(b)',12:'C2(a)(b)'}[i],'candidate_heading':f'p.{i}'})
parts.append('''
## 复习索引与最容易错的桥梁

A区参考字母依次：**A、B、B、D、D、B、C、C、A、C、A、C、D、D、A、B**。字母只是索引，不代替题旁理由。

- A1/A3/A4：显著、样本内拟合、测试预测、因果与利润是不同问题，不能互相充当证明。
- A2/A5/A7/A11/A15：先确定减谁、除谁、总上限还是单机构、总损失还是分配；数字算对但对象错仍会选错。
- A8/A10/A12/A13、B4：账本记录、底层资产、契约权利、银行资金完成分别核验。
- B1/C1：只能用决策时已经可得的信息；开发样本定义的尺度不能由未来数据偷偷重写。
- B2：改变截距只平移，条件关系翻转需要交互/非线性；灵活不保证泛化。
- B3/C2：收入不等于利润；总资产增加不等于每股增加，必须同时跟踪分母。

## 改条件自测（笔记自拟，非原卷题）

1. A5的路径改为100→120→114→130，最大回撤是多少？
2. A7已有融资变为85万元、合计上限仍80万元，B还能新借多少？
3. C1新动量改为0、其余条件不变，预测超额收益是多少？
4. C2按每股10美元增发200万股，NAV每股怎样变？
5. B1年报在周五收市后公布，可否把数据用于当天收市前的预测？

<details><summary>自测参考答案与理由</summary>

1. (120−114)/120=5%；最后130创高不抹掉此前回撤。
2. 新增空间为0；已有融资还超过上限5万元，不能把负5万元当可放款金额。须查记录/风险并处理超限，不代表自动获准继续放贷。
3. 新动量z=(0−2)/2=−1，所以0.10%+0.20%×(−1)=−0.10%。标准化波动率仍0.5，零系数贡献仍0。预测负超额不等于已实现亏损。
4. (80+2×10)/(8+2)=10美元/股。不计成本/价格变化时按原NAV发行不改变平均每股资产。
5. 不可。收市后才公开不满足决策前已知；应按实际可用时点和交易规则对齐下一次合资格决策。

</details>

## 核对范围与待补

题面全部22题、28作答单元、64选择项均保留；无另外的题面数据表或需重画的试题曲线。原题p.13/14为空白草稿纸。表格、决策树、时间流程、备份流程均为解析补充，不是官方图或给定数字。尤其B2树叶+2%/−2%/0%是演示，不能当原卷数据。

作者已复算算术并检查题面/页图；独立教学审查、最终Markdown/公式/Mermaid实际显示尚待完成。官方答案、Canvas当前考试/提交安排未核，不称未发布；未修改个人出席、学习、自测、提交或评分状态。没有执行交易、提交答案、修改备份权限或操作金融账户。
''')
text='\n'.join(parts)
write(root/'candidate.md',text)
write(root/'page-evidence.json',{'source_path':str(pdf),'source_sha256':sha(pdf),'physical_pages':14,'visual_pages_read':14,'pages':evidence})
questions=[]
for p in range(2,7):
 for m in re.finditer(r'(?ms)^(\d+)\. (.*?)(?=^\d+\. |\Z)',pages[p-1]):
  original=m.group(0).strip(); num=int(m.group(1)); opts=re.findall(r'(?m)^([ABCD])\. ',original)[-4:]
  assert opts==list('ABCD'),(num,opts)
  questions.append({'id':f'A{num}','page':p,'original':original,'option_letters':opts,'analysis_anchor':f'A{num}','status':'author-checked-reference-not-official'})
for section,start,end in [('B',7,10),('C',11,12)]:
 for i in range(start,end+1):
  num=i-start+1
  for sub in ['a','b']:questions.append({'id':f'{section}{num}({sub})','page':i,'original_page_text_retained':True,'analysis_anchor':f'{section}{num}({sub})','status':'author-checked-reference-not-official'})
assert len(questions)==28
write(root/'question-ledger.json',{'candidate_sha256':sha(root/'candidate.md'),'source_sha256':sha(pdf),'questions':questions,'units':28,'multiple_choice_options':64,'official_solution':'not_verified'})
checks={'A2_excess_percent':-.60-.04,'A5_drawdown':(120-90)/120,'A7_RMB_headroom':1000000*.8-600000,'A9_time_reduction':(40-25)/40,'A11_HKD_proceeds':500*99.7,'A11_discount':(100-99.7)/100,'A15_USD_investor_loss':1000-600-100,'B3_USD_retained':1000*(.03-.018-.004),'C1_zm':(4-2)/2,'C1_zv':(5-4)/2,'C1_excess_percent':.1+.2*1,'C2_before_NAV':80/8,'C2_a_NAV':(80+2*12)/(8+2),'C2_b_NAV':(80+2*8)/(8+2),'C2_par_NAV':(80+2*10)/(8+2)}
write(root/'arithmetic-checks.json',checks)
write(root/'author-evidence.md',f'''# Practice B author evidence

Author /root/cityu_review_probe; not an official solution. Candidate SHA {sha(root/'candidate.md')}.

Read all 14 actual page PNGs, not just contact sheets; source text/pages checked against visuals. p1 administrative boundaries and p13/14 scrap identity preserved. p2–6 16 MC questions each four options; p7–10 eight B subparts; p11–12 four C subparts. All English source page text is embedded verbatim as extracted (newline layout only), with page originals. Separate Chinese per-option reasoning, each B/C subpart and English reference answers are provided. Generated examples and diagrams are labelled.

No official answer file was provided with the source intake; current Canvas not opened in this author task. Therefore official solution and current administrative state remain unverified, not asserted absent. No current bank/product/legal terms were inferred from hypothetical questions. Source files read-only; all output scratch only.

Arithmetic independently evaluated in arithmetic-checks.json using raw inputs; units and denominator assumptions explained locally. This author check is not an independent review or final rendered visual acceptance. Full independent review remains pending and must be performed by a different agent.
''')
write(root/'freeze.json',{'candidate_sha256':sha(root/'candidate.md'),'source_sha256':sha(pdf),'author_id':'/root/cityu_review_probe','independent_review':'pending','final_UI':'pending','question_units':28,'source_pages':14,'assets':[{'path':str(p.relative_to(root)).replace('\\','/'),'sha256':sha(p)} for p in root.rglob('*') if p.is_file() and p.name!='freeze.json']})
print(json.dumps({'candidate_sha256':sha(root/'candidate.md'),'source_sha256':sha(pdf),'units':28,'options':64,'pages':14},ensure_ascii=False))
