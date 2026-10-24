import hashlib,json,re,sys,subprocess
from pathlib import Path
B=Path(__file__).parent;R=Path('D:/上课资料/CityU');sys.path.insert(0,str(R/'_meta/tools'))
from safe_write import atomic_write
source=B/'author/main-proposed-v2.md';before=source.read_text(encoding='utf-8');text=before;changes=[]
assert hashlib.sha256(source.read_bytes()).hexdigest()=='2cb1787ecf4f58438114c9b341ca3d8615c13285926696816ce3a3de918d5689'
def edit(old,new,reason):
 global text
 assert text.count(old)==1,(reason,text.count(old))
 changes.append({'old':old,'new':new,'reason':reason});text=text.replace(old,new,1)
edit('$mathrm{SST}=',r'$\mathrm{SST}=', '恢复作者新增SST公式缺失的LaTeX反斜杠；数学不变。')
edit('L0 层面另需：最小二乘、R²、标准误、p 值的基本含义（见 [[EF5560_Fintech_and_AI_in_Finance/_meta/知识层级台账|台账]] L0）。**但"金融里怎么读它们"不在 L0**，本讲展开。','本讲会就地解释最小二乘、R²、标准误和 p 值，不要求先从 [[EF5560_Fintech_and_AI_in_Finance/_meta/知识层级台账|台账]] L0 掌握大学统计。台账用于定位历史依赖；当前需要的计算和金融读法仍在正文展开。','取消以大学统计L0为读者已有掌握的前提，与实际高中起点正文一致。')
edit('不能仅靠该信息集系统性获得异常收益。','不能仅靠该信息集系统性获得异常收益（超过所声明风险调整基准的收益）。','就地解释新增EMH定义实际依赖的异常收益。')
edit('- **为什么大多数人认为收益根本不可预测**：先给基准定义。','先给有效市场假说的基准定义。','在已有EMH小标题下直接解释定义，避免把定义、信息集和现实判断塞进单个超长列表项。')
edit('说明常数真值预测的基准分数为 0，并列出有限样本等边界。','说明在非恒定目标上，始终预测该评估样本均值的常数模型得分为 0，并列出有限样本等边界。','官方文档指预测样本均值的常数模型，不能误写为目标为常数的情况。')
line=next(x for x in text.splitlines() if x.startswith('**English reference answer（笔记自拟）**: The momentum plots'))
prefix,body=line.split(': ',1);sentences=re.split(r'(?<=\.)\s+(?=[A-Z])',body);assert len(sentences)==4
edit(line,prefix+':\n\n'+'\n\n'.join(sentences)+'\n','四句英文答题过程按图/联合模型归因/经济价值/改判证据分段；原词、数字、标点和顺序全部保留，分开随后的中文说明。')
out=B/'author/main-final-proposed.md'
for prior in [out,B/'author/main-final-changes.json',B/'main-source/mechanical-final-precheck.txt']:
 if prior.exists():
  hist=B/'main-source/history';hist.mkdir(exist_ok=True)
  atomic_write(hist/(prior.name+'.'+hashlib.sha256(prior.read_bytes()).hexdigest()[:12]+'.snapshot'),prior.read_bytes().decode('utf-8'))
atomic_write(out,text)
record={'schema':'exact-root-targeted-replacements-v1','author_id':'/root','source_file':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'changes':changes,'status':'pending_independent_targeted_recheck'}
atomic_write(B/'author/main-final-changes.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
p=subprocess.run([sys.executable,'-X','utf8',str(R/'_meta/tools/note_quality.py'),str(out),'--profile','current','--strict','--sections','--readability'],cwd=R,capture_output=True,text=True,encoding='utf-8')
atomic_write(B/'main-source/mechanical-final-precheck.txt',p.stdout+p.stderr)
print(json.dumps({'candidate_sha256':record['candidate_sha256'],'root_exact_changes':len(changes),'current_exit':p.returncode,'tail':(p.stdout+p.stderr)[-1000:]},ensure_ascii=False))
