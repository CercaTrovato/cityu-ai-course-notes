from pathlib import Path
import sys,json,hashlib,re
sys.dont_write_bytecode=True
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
OUT=Path(__file__).parent
OLD=OUT.parent
VAULT=Path('D:/上课资料/CityU')
COURSE=VAULT/'EF5560_Fintech_and_AI_in_Finance'
SRC=COURSE/'course_files_export/canvas-20261118/practice_exam_A.pdf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj): atomic_write(str(OUT/name),json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
if not (OUT/'baseline.json').exists():
    write('baseline.json',{'source':str(SRC),'source_sha256':sha(SRC),'formal_candidate_created':False,'course_files':{str(p.relative_to(COURSE)):sha(p) for p in COURSE.rglob('*') if p.is_file()},'old_inputs':{str(p):sha(p) for p in [OLD/'exam-a-content.json',OLD/'exam-a-long.json',OLD/'practice_exam_A/pages.json',OLD/'practice_exam_A/source.txt']}})
pages=json.loads((OLD/'practice_exam_A/pages.json').read_text(encoding='utf-8'))
assert len(pages)==14 and isinstance(pages[0],str)
def compact(text):return re.sub(r'\s+',' ',re.sub(r'([A-Za-z])-\n\s*([A-Za-z])',r'\1-\2',text)).strip()
questions={}
for n in range(2,7):
    page=pages[n-1]
    for m in re.finditer(r'(?ms)^(\d+)\.\s+(.*?)(?=^Answer:)',page):
        num=int(m[1]); raw=m[2].strip()
        stem,options=raw.split('\nA.',1)
        opts=re.split(r'(?m)^([B-D])\.\s*',options)
        parsed={'A':compact(opts[0])}
        for i in range(1,len(opts),2): parsed[opts[i]]=compact(opts[i+1])
        assert list(parsed)==list('ABCD')
        questions[f'A{num}']={'section':'A','number':num,'page':n,'marks':2.5,'stem':compact(stem),'options':parsed,'raw_extracted':m[0]}
for i,n in enumerate(range(7,13)):
    id=f'B{i+1}' if i<4 else f'C{i-3}'
    p=pages[n-1]
    p=p[p.index(f'{i+1 if i<4 else i-3}. '):]
    p=p.replace('- END -','').strip()
    stem,rem=p.split('(a)',1)
    a,b=rem.split('(b)',1)
    questions[id]={'section':id[0],'number':int(id[1:]),'page':n,'marks':10,'stem':compact(re.sub(r'^\d+\. ','',stem)),'parts':{'a':compact(a),'b':compact(b)},'raw_extracted':p}
assert len(questions)==22
write('questions-extracted.json',{'source':str(SRC),'source_sha256':sha(SRC),'pages':14,'questions':questions,'visual_confirmation':'Author directly opened all 14 individual PNGs on 2026-11-19; text extraction checked against images; not an official answer.'})
oldA=json.loads((OLD/'exam-a-content.json').read_text(encoding='utf-8'))
oldBC=json.loads((OLD/'exam-a-long.json').read_text(encoding='utf-8'))
def normalize(x):
    if isinstance(x,str):return x.replace('\\\\','\\')
    if isinstance(x,list):return [normalize(y) for y in x]
    if isinstance(x,dict):return {k:normalize(v) for k,v in x.items()}
    return x
answers=normalize(oldA|oldBC)
assert set(answers)==set(questions)
old=answers['B1']['parts'][0]['cn']
assert '约亏15%' in old
answers['B1']['parts'][0]['cn']=old.replace('若 PDD 跌20%、JD只跌5%，简单等金额多空仍约亏15%，空头并未保证对冲。这个20/5例为笔记补充，不是原回测。','以 100 元资本为计算基准，买入 50 元 PDD，做空 50 元 JD。若 PDD 跌 20%、JD 只跌 5%，多头亏 10 元，空头赚 2.5 元，净亏 7.5 元，即相对资本亏 7.5%。若另用每条腿 100 元的基准，差额才是 −15%；必须先声明分母。以上是笔记补充，不是原回测。')
write('working-answers.json',answers)
write('reuse-audit.json',{'old_A_sha256':sha(OLD/'exam-a-content.json'),'old_long_sha256':sha(OLD/'exam-a-long.json'),'verified_against_source':'All 16 selected letters and six multipart outlines were compared with all 14 directly viewed source pages. Core results agree. This is author checking, not independent review.','substantive_change':'B1(a) old equal-money long/short example said approximately −15% without a denominator. Replaced with explicit 100 capital / 50 long / 50 short, profit −7.5, return −7.5%; per-leg spread −15% distinguished.','format_change':'JSON double backslashes in LaTeX normalized to single control backslashes; originals preserved.'})
rows=['# Practice Exam A · 逐页来源证据（待独审）','',f'源：`{SRC}`。SHA-256 `{sha(SRC)}`。本轮实际打开 page-01.png 至 page-14.png，每张 778×1100 左右的完整单页，字和表格可辨。未用联系表或文本冒充视觉。','', '| 物理页/印刷页 | 内容与题目 | 原图/表格与处理 | 视觉证据 | 候选定位 |','|---|---|---|---|---|']
descs={1:'封面：2小时，22题100分，三部分，双面手写A4；不是新期末公告',2:'A1–A3：Ridge、嵌套OLS、PCR/PLS',3:'A4–A6：alpha/beta、双边成本/Sharpe、敞口',4:'A7–A9：托管请求权、分叉、基金收入',5:'A10–A12：NFT三层、CBDC负债、采用',6:'A13–A16：钱包停机、风险能力、筛查、AUM盈亏平衡',7:'B1(a)(b)：相对价值/风险与因果',8:'B2(a)(b)：选30轮、时间组/横截面组',9:'B3(a)(b)：排序校准与定价/回收',10:'B4(a)(b)：融资额度、记录完整和业务信用',11:'C1(a)(b)：4个月真实/模型/MA12表，SSE和OOS R²',12:'C2(a)(b)：BNPL收费、拨款、贡献变动',13:'SCRAP PAPER，纯空白草稿',14:'SCRAP PAPER，纯空白草稿'}
for n in range(1,15):
    path=OLD/f'practice_exam_A/page-{n:02}.png'
    fig='C1 原始三行四个月表逐值转写并保留源页文件；无其他教学图' if n==11 else '文字题/留白，无承载知识的插图；无需复制答题线或空白页'
    rows.append(f'| {n}/{n if n>1 else "封面无印刷号"} | {descs[n]} | {fig} | 实看 {path.name}，SHA `{sha(path)}` | §1（p1）；§2 对应原题 ID；§8逐页表 |')
rows+=['','## 补图必要性','', '- A4/5/6/16、C1/2 用同一量的输入—运算—结果小表，直接回答数额和单位，不另造曲线。', '- B1 多空跨主体用带金额和正负号的小表，B2 数据单位分组用对照表，B4 单笔应收融资用额度/记录/业务验证表。', '- B2(a) 确有训练和验证损失三个候选点的比较：生成同数据英文坐标图及源码供复验；不把点间连线当实际训练轨迹或最优全局证明。', '- 源卷无算法图、流程图或照片遗漏。原始表不是需要保持空间箭头的图，按原数字重排成Markdown，不依赖截图才能学习。', '', '源页视觉≠候选最终显示。禁止UI范围下未使用浏览器或Obsidian，后续仍待实际阅读尺寸与独审。']
atomic_write(str(OUT/'page-evidence.md'),'\n'.join(rows)+'\n')
print('Prepared',len(questions),'questions',sha(SRC))
