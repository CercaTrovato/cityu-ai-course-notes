from pathlib import Path
import json,sys,hashlib,re
sys.dont_write_bytecode=True
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
P=Path(__file__).parent
V5=P.parent/'dot-package-v5-20261119'
SHA='a96bf9a2b4acdee09c4c8cde1b9e9d5f3d05fbdb3a8a041f67dbf77747ec5e47'
NOTE='IS5542_GenAI_in_Business/notes/M09-AI法律问题-版权责任与客户资料.md'
VAULT=Path('D:/上课资料/CityU')
SOURCE=VAULT/'IS5542_GenAI_in_Business/course_files_export/canvas-20261118/IS5542-Guest Lecture6.pdf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,t):atomic_write(str(P/name),t.rstrip()+'\n')
def put(name,o):write(name,json.dumps(o,ensure_ascii=False,indent=2))
assert sha(P/'candidate.md')==SHA
binding=json.loads((P/'preview/binding.json').read_text(encoding='utf-8'))
assert binding['sha256']==SHA
put('root-final-display-v6.json',{'candidate_sha256':SHA,'verified_by':'/root','reported_to':'/root/cityu_legal_resume','basis':'Parent actual IAB observations on 2026-11-19, recorded after exact-v6 URL; packaging author did not claim own browser view','surface':'IAB full source-bound preview','observed':{'banner_sha256':SHA,'images_loaded':9,'images_expected':9,'mermaid_rendered':1,'p46_mermaid_width':713,'p46_labels':'Actual screenshot viewed; labels legible','details':7,'interaction':'Clicked fifth answer; correct human oversight vs mechanical confirmation and Mak objective/other-element conditions visible','nonempty_internal_broken_anchors':0,'errors':0,'scroll_width':1265,'client_width':1265,'overflow':False,'section9_5':'Corrected sentence 不把来源保真等同为现行法律核查 visible; Tesla and other limits remain'},'prior_unchanged_p61_evidence':'history/v5-root-final-display-v5.json contains root actual p61 caption/quotation/image-label readability. No new v6 p61 screenshot is asserted. Nine image bytes and stylesheet/source HTML remain bound.','preview_binding_file':'preview/binding.json','preview_binding_sha256':sha(P/'preview/binding.json'),'html_raw_sha256':sha(P/'preview/index.html'),'html_normalized_utf8_sha256':hashlib.sha256((P/'preview/index.html').read_text(encoding='utf-8').encode('utf-8')).hexdigest(),'binding_html_sha256':binding['html_sha256'],'raw_vs_normalized':'Both hashes preserved; no pretending Windows newline-normalized hash is raw file hash.','status':'verified exact-v6 source-bound IAB; native Obsidian not directly viewed'})
report='''# IS5542 M09 · v6 主准备与范围核对

## 1. 当前候选及边界

准备者 `/root/cityu_legal_resume`，教学修订/最终显示核验 `/root`，独审 `/root/legal_stage_review`。本报告是准备者的主报告，不冒充独审者新写报告。

候选 `candidate.md` 为90,357 bytes，SHA `a96bf9a2b4acdee09c4c8cde1b9e9d5f3d05fbdb3a8a041f67dbf77747ec5e47`。正式拟定目标 `IS5542_GenAI_in_Business/notes/M09-AI法律问题-版权责任与客户资料.md`，准备时不存在。原65页PDF的SHA仍为 `1c1a107695d0236055ca898b801e0dcd459b207e84572d3e8abd3c88f2444ec0`。

这里只制作新scratch包，没有正文/图/元数据/Notion/Git正式写回。最终gate的实际结果在 `gate-output-final.txt`；工具通过不等于已经发布或全部当前法律核实。

## 2. 独审及维护版本承接

独审先仅按原187b3a候选进行完整高中起点顺读，阶段1冻结后再读规则/原件/作者证据，从全部65源页反查候选。阶段2的原始待修结论原样保留，不改历史。root修订为36818后，原审查者实际读变化及依赖，并定向关闭B1–B3、Q1–Q4、S1：公平使用最小整体因素、重大性区别、程序地图、漏原问/译解及原页条件。S2家庭岗位误译指控经官方用语核验撤回，非作者纠错。

该独审报告严格绑定36818，不声称审查者读过v5/v6。本包保留原阶段1、阶段2和定向报告，作者/修订者/审查者身份真实。

36818→v5 affad4由七项精确重建证明只是两处来源标签/错字、真实教学状态/前言、两处圈号转编号、一处段间空行。v5→v6仅按root要求把§9.5首尾两段过时制造状态改为真实现状；中间重点待核法律段UTF-8字节完全相同，其余v5文本不变。没有改变案例、法理条件、数值、原题、图义、答案或个人状态。

证据为 `maintenance-binding.json`、`maintenance-v5-v6.diff` 和 `history/v5-maintenance-binding.json`；旧原稿、v4失败和v5gate/报告均留存。继承实质审查的理由是实际维护差异已核，不是只更新SHA或伪造新审查。

## 3. 来源、原题及计算

作者和独审分别实际看过全部65源页；正文65页级入口、§8每页精确链接。9张图8/15/18/26/31/37/39/58/61逐图与旧渲染和原资产SHA相同，正文旁有具体中文读法。二维码/联系名片按源页非教学理由不复刻、不扫描、不联络。source/page证据、独审逐源列表、9图绑定和法律文件原副本均保存。

原题/选项/语境、逐项中文及参考英答由独审对源核；36818又补p29/p56/p60/p61原问、p35/45/53/55/59中文读题，以及p38定义简述、p42近65mph、p48拒绝解释。question-inventory不是note-source-checks-v1，机械明确未用清单认证题面；人工逐源证据不与机器能力混淆。

Tesla算术可由已取两页判决复做：已分配补偿11.55m+7.92m+23.10m=42.57m美元，加200m惩罚性赔偿=242.57m，不再乘33%。新增公平使用桥梁据§107整体因素并以Bartz/ROSS有限用途/市场事实解释；刑事重大程度据四元素和法改会2021报告§6.69、成对假例，均由独审定向核来源和迁移，不向真实个案作定罪意见。

sources的通过仅指此讲义有限学习范围的来源可追踪、原问和必要新增解释有依据、未知明确保留。香港合订法/生效注释、s33现时状态、TDM完整当前状态、Bartz批准全文、Uber刑事原件、Re A全文与引句、Tesla上诉终局、付费SAE全文等未核队列不因此变完成。官方摘要/新闻稿/镜像/当事人文件不伪称原判全文。

## 4. 当前v6全部实际警告

v6已真实重跑current/strict。C.hard=0、R.hard=0，C.warn9、R.warn139。逐项比较实际code/line/message及每条R所在完整行，与v5已实质处置的一条一条匹配；不是照搬数量。两处§9.5制造状态变更在这些警告之后。当前逐条理由、标题、旧审行位、原独审依据在 `warning-dispositions.json`，完整旧清单保留历史。

具体处置涵盖监管比较与有依据非内容页、图标签/机构/法庭引注、p25整体因素与案例因果桥梁、p54四编号/空段/成对例而非真正无结构、§8的p./标题点号误触发句数、匿名/同意/组织权力等分别必要的否定条件。所有疑点依据具体内容处置，不为凑阈值删除条件。V4 FAIL原输出及维护差异保留，没有追改失败历史。

## 5. 精确v6最终显示，归属root

root在收到新v6 URL后实际IAB核验并报告PASS：a96bf9完整banner、9/9原图、1渲染Mermaid、7折叠、0非空断链/错误/溢出，scroll/client宽均1265。p46实际截图图宽713、标签可读；实际点第五答案，人工干预与机械确认、Mak客观标准及其他门槛内容可见。§9.5修正句“不把来源保真等同为现行法律核查”与Tesla等限制仍在。

这是root实际观察，不是准备者或独审者冒称亲看v6。`root-final-display-v6.json`保存归属与raw/换行规范化哈希，原预览HTML/binding/图都保存。v5的p61实际图注/引句/图标签证据只按不变资产承接，不称新增v6截图。原生Obsidian未直接查看。

## 6. 三场景及剩余状态

预习：阶段1全篇顺读与阶段2/定向迁移闭合教学断点；后续仅制造状态/版式维护。课中：65源页反向定位、漏原问/独有元素已修，9图与锚点有实际核验。复习：§3–§7与补充机制/词卡/自测一致，root实际展开第五答案检查关键条件。未推断本人已学会。

适用实质教学阻塞已由独审定向关闭，当前维护、警告、root同源最终显示已实核；最终门槛以gate实际输出为准。法律当前性/完整原判等是明确限制，不是本稿当前合规意见。transcript仍pending/v0.9，不造课堂内容。正式CAS写回/回读、课程元数据、Notion、Git/远端均尚未在本包执行，不能称发布或同步完成。
'''
write('review.md',report)
manifest=json.loads((P/'staging-manifest.json').read_text(encoding='utf-8'))
manifest['release_status']='exact-v6 root IAB verified; scratch only; formal gate result separate, no formal writes'
put('staging-manifest.json',manifest)
assert not (VAULT/NOTE).exists(),'Target appeared; coordinate before formal action'
assets=[]
for f in P.rglob('*'):
    if f.is_file() and f.name not in ['review.json','gate-output-final.txt','gate-summary.json']:
        assets.append({'path':str(f.relative_to(P)).replace('\\','/'),'sha256':sha(f)})
assets.append({'path':str(SOURCE),'sha256':sha(SOURCE)})
put('review.json',{'schema':'note-review-v2','note':NOTE,'scope':'full','source_sha256':None,'candidate_sha256':SHA,'review_file':'review.md','review_sha256':sha(P/'review.md'),'checks':{'understanding':{'status':'passed','evidence':'Actual full stage1/stage2 then directed-recheck-v2 at36818; v6 inherits only via exact v2-v5 and v5-v6 maintenance binding, not fabricated new reviewer reading'},'sources':{'status':'passed','evidence':'Scoped lecture traceability and all65 source-page/original-question human checks,9asset binding; targeted107/Mak-degree basis. Current-law/full-original-judgment limits unchanged in§9.5 and scope-and-limits; not legal opinion'},'warnings':{'status':'passed','evidence':'Actual v6current/strict hard0, every9C+139R actual warning and full R line compared and specifically disposed; prior failure history preserved'},'visuals':{'status':'passed','evidence':'root-final-display-v6.json: exact source-bound IAB,9/9images/1Mermaid/7details/no errors, anchors or overflow; actualp46 screenshot/fifthanswer/§9.5. Root observations, no nativeObsidian claim'}},'independent_review':{'author_ids':['/root/cityu_legal_resume','/root'],'reviewer_id':'/root/legal_stage_review','perspective':'high-school-beginner','status':'passed','candidate_sha256':SHA,'actually_reviewed_candidate_sha256':'36818bf6c69bc0d3f892db5a05eb050b4b233d9f6438fef50d0339ad28cfd866','report_file':'evidence/independent/directed-recheck-v2.md','report_sha256':sha(P/'evidence/independent/directed-recheck-v2.md'),'carry_forward':'maintenance-binding.json','binding_basis':'Report actually binds36818. No new v6 independent reading claimed; exact maintenance audit preserves reviewed teaching scope.'},'assets':assets,'unresolved':[],'nonblocking_scope_limits_file':'scope-and-limits.json','operational_release':'scratch package only; no official files, Notion or Git written'})
print('v6 review binding',sha(P/'review.json'),'assets',len(assets))
