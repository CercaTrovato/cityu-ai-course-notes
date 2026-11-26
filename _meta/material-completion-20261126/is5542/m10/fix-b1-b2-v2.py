from pathlib import Path
import sys,hashlib,json,difflib,subprocess
from fractions import Fraction
o=Path(__file__).parent; root=Path('D:/上课资料/CityU')
sys.path.insert(0,str(root/'_meta/tools'))
from safe_write import atomic_write
original=o/'M10-责任AI-公平解释与治理落地.md'
assert hashlib.sha256(original.read_bytes()).hexdigest()=='e2e5dcfe7c70e78ec3cffb5717ddb8c143e3ebe0556e9fd14d6f5a9bb25af83c'
t=original.read_text(encoding='utf-8'); changes=[]
def replace(id,old,new):
    global t
    assert t.count(old)==1,(id,t.count(old))
    t=t.replace(old,new);changes.append(id)
anchor='原图称不同基础率下人口统计均等与均等赔率不能同时优化。'
accuracy='''#### 准确率均等：把两类正确决定一起数

左图的另一项是准确率均等（Accuracy Parity），原文为 “The protected and unprotected groups should have equal accuracy.” 中文是：受保护群体与比较群体的总体准确率应相同。准确率的分子是判断正确的人数：合格者获批，加上不合格者被正确拒绝；分母是该组全部人数。它既计算批得对，也计算拒得对，和只数获批人数的获批率不同。

💡 沿用 p.25 的笔记补充数据，逐组核正确决定：

1. A 的不合格者有 40 人，其中误批 8 人，故正确拒绝 $40-8=32$ 人。加上合格且获批的 48 人，总体准确率为 $(48+32)/100=80\\%$。
2. B 的不合格者有 70 人，其中误批 14 人，故正确拒绝 $70-14=56$ 人。加上合格且获批的 24 人，总体准确率为 $(24+56)/100=80\\%$。

本例准确率同为 80%，但获批率仍为 56%／38%。准确率把两类正确决定合并，相同准确率本身不保证真阳性率、假阳性率或获批率都相同。English reference（笔记自拟）：Accuracy parity requires equal overall accuracy across groups. Accuracy counts correct approvals and correct rejections, whereas the acceptance rate counts all approvals.

'''
replace('B2-p26',anchor,accuracy+'#### 不同公平要求何时会冲突\n\n'+anchor)
old='''右侧两张图把红黄热区叠在医学影像和道路场景上。显著性图（saliency map）显示输入某些部分对指定输出的敏感程度。梯度加权类激活映射（Gradient-weighted Class Activation Mapping, Grad-CAM）用目标输出对卷积特征图的梯度形成权重，再组合特征图，产生重要区域热图。

按一条路径读：指定模型输出类别→找与类别相关的特征变化→加权合成区域→叠回原图供人检查。较亮区域提示模型对这个输出使用了哪里的信息；不是“此处一定有病”或“已证明刹车由行人造成”。原论文明确是 coarse localization，原页“exact pixels”与“visual proof”说法过强。'''
new='''右侧两张图把红黄热区叠在医学影像和道路场景上。显著性图（saliency map）显示输入某些部分对指定输出的敏感程度。梯度加权类激活映射（Gradient-weighted Class Activation Mapping, Grad-CAM）则把网络中间的区域响应，组合成与一个目标输出有关的粗热区。

先认清被组合的对象：网络处理图像时，中间会形成多张特征图（feature maps）。每张可看成一个小网格，各格记录图像相应区域对某种模式的响应强弱，例如边缘或纹理。它们是网络内部的数值记录，不是人工已经标好的病灶图。

💡 机制桥梁（笔记补充）：以想检查的“异常”类别分数为目标，梯度（gradient）描述这个分数对某个区域响应的小幅变化有多敏感。若该响应稍增，目标分数明显上升，就说明它在当前输入附近有正向影响；若分数下降，影响方向相反。这里解释的是模型分数对内部数值的局部敏感性，不是改变现实物体后的因果效应。

再按顺序把这些记录变成可看的图：

1. 对每张特征图，把不同空间位置的目标分数敏感性作平均，形成这张图的权重。权重表示这类模式对当前目标分数的局部影响方向和程度。
2. 各张特征图乘上自己的权重后相加，保留对目标起正向支持的部分，得到粗粒度区域图。某区域在重要模式上的响应强，组合后可能更亮。
3. 把小区域图放大并叠回原图，供人定位模型关注的区域。放大不会补出原来没有的精确像素证据。

较亮区域提示模型对这个输出使用了哪里的信息；不是“此处一定有病”或“已证明刹车由行人造成”。原论文明确是 coarse localization，原页“exact pixels”与“visual proof”说法过强。'''
replace('B1-p42',old,new)
replace('B2-term-card','| 机会均等 | Equality of opportunity |','| 准确率均等 | Accuracy parity | Equal overall accuracy across groups, counting correct approvals and correct rejections. | p.26 |\n| 机会均等 | Equality of opportunity |')
replace('B1-term-card','A gradient-based method producing coarse regions relevant to a chosen model output.','A method that weights internal feature maps by their sensitivity to a target score and combines them into a coarse region map.')
replace('B2-selftest-heading','### 7.1 三种公平比例','### 7.1 公平比例与总体准确率')
replace('B2-selftest-prompt','计算两组获批率、TPR、FPR；满足哪些公平定义？','计算两组获批率、TPR、FPR 和总体准确率；满足哪些公平定义？')
replace('B2-selftest-answer','B 误批改 7 后，B 获批率变 31%，FPR 变 10%，TPR 仍是 $24/30=80\\%$。机会均等仍成立，均等赔率不再成立。不是所有指标跟着一项同时变化。',
'''A 正确拒绝 32 人，总体准确率为 $(48+32)/100=80\\%$；B 正确拒绝 56 人，总体准确率为 $(24+56)/100=80\\%$。两组也满足准确率均等，但这不使获批率自动相同。

B 误批改 7 后，B 获批率变 31%，FPR 变 10%，TPR 仍是 $24/30=80\\%$。B 正确拒绝变为 $70-7=63$ 人，总体准确率升为 $(24+63)/100=87\\%$。机会均等仍成立，均等赔率与准确率均等不再成立。不是所有指标跟着一项同时变化。准确率的读法见 [[#讲义 p.26 · Optimizing Every Fairness Metric Simultaneously is Mathematically Impossible|p.26]]。''')
target=o/'M10-责任AI-公平解释与治理落地-v2.md'
atomic_write(target,t)
sha=hashlib.sha256(target.read_bytes()).hexdigest()
diff=''.join(difflib.unified_diff(original.read_text(encoding='utf-8').splitlines(True),t.splitlines(True),fromfile=original.name,tofile=target.name))
atomic_write(o/'b1-b2-v2.diff',diff)
assert Fraction(48+32,100)==Fraction(24+56,100)==Fraction(4,5)
assert Fraction(24+70-7,100)==Fraction(87,100)
atomic_write(o/'calculation-check-v2.json',json.dumps({'scope':'B2 only; original calculations retained in calculation-check.json','A_true_negative':32,'B_true_negative':56,'A_accuracy':0.8,'B_accuracy':0.8,'B_changed_false_positive':7,'B_changed_true_negative':63,'B_changed_accuracy':0.87,'verification':'Fraction arithmetic assertions executed'},ensure_ascii=False,indent=2)+'\n')
meta=json.loads((o/'course-updates-draft.json').read_text(encoding='utf-8'))
for entry in meta:
    if entry['kind']=='append' and ('术语表.md' in entry['target'] or '知识层级台账.md' in entry['target']):
        entry['text']=entry['text'].replace('| 机会均等 | Equality of opportunity |','| 准确率均等 | Accuracy parity | Equal overall accuracy across groups, counting correct approvals and correct rejections. | p.26 |\n| 机会均等 | Equality of opportunity |').replace('A gradient-based method producing coarse regions relevant to a chosen model output.','A method that weights internal feature maps by their sensitivity to a target score and combines them into a coarse region map.')
atomic_write(o/'course-updates-draft-v2.json',json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
evidence=(o/'page-evidence.md').read_text(encoding='utf-8')
lines=[]
for line in evidence.splitlines():
    if line.startswith('| 26 |'):line=line.replace('作者据源成稿；无转录／独立抽检另记','B2已补原图Accuracy Parity原句、分母与同例80%/80%；定向复核待执行')
    if line.startswith('| 42 |'):line=line.replace('作者据源成稿；无转录／独立抽检另记','B1已补特征图、目标梯度、空间平均权重与粗图组合；定向复核待执行')
    lines.append(line)
atomic_write(o/'page-evidence-v2.md','\n'.join(lines)+'\n')
args=[sys.executable,'-X','utf8',str(root/'_meta/tools/note_quality.py'),str(target),'--pages','71','--strict','--sections','--readability','--source-checks',str(o/'source-checks.json'),'--json']
r=subprocess.run(args,cwd=root,capture_output=True,text=True,encoding='utf-8')
atomic_write(o/'quality-v2.txt',r.stdout+r.stderr)
d=json.loads(r.stdout.split('JSON:',1)[1]);atomic_write(o/'quality-v2.json',json.dumps(d,ensure_ascii=False,indent=2)+'\n')
result={'baseline_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'candidate':str(target),'candidate_sha256':sha,'bytes':target.stat().st_size,'changed_units':changes,'quality_exit':r.returncode,'C_hard':d['C']['hard'],'R_hard':d['R']['hard'],'source_contract':d['C']['source_coverage']['status'],'independent_review':'pending_original_reviewer_targeted_B1_B2','display':'pending_root_targeted_B1_B2','unchanged_evidence':'71 source pages,60 figures,other17 question contracts and original independent samples retained'}
atomic_write(o/'b1-b2-v2-result.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
