from pathlib import Path
import sys,re,json,hashlib,shutil
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
o=Path(__file__).parent
root=Path('D:/上课资料/CityU')
course='IS5542_GenAI_in_Business'
name='M10-责任AI-公平解释与治理落地.md'
source=f'{course}/course_files_export/canvas-20261126/IS5542 - Lecture 10.pdf'
sha=hashlib.sha256((root/source).read_bytes()).hexdigest()
parts=(o/'pages-01-32.md').read_text(encoding='utf-8')+'\n'+(o/'pages-33-71.md').read_text(encoding='utf-8')
pages=[]
for match in re.finditer(r'^@@(\d+)\|([^\n|]+)\|([^\n]+)\n(.*?)(?=^@@|\Z)',parts,re.M|re.S):
    n,title,kind,body=match.groups()
    pages.append({'page':int(n),'title':title,'kind':kind,'body':body.strip(),'heading':f'讲义 p.{n} · {title}'})
assert [p['page'] for p in pages]==list(range(1,72))
(o/'figures'/'m10-lecture-10').mkdir(parents=True,exist_ok=True)
asset_manifest=[]
texts=[]
for p in pages:
    n=p['page']
    t=f"### {p['heading']}\n\n{p['body']}\n"
    if p['kind']=='原图':
        dest=o/'figures'/'m10-lecture-10'/f'p{n:03}.png'
        shutil.copyfile(o/'pages'/f'p-{n:02}.png',dest)
        target=f'{course}/notes/figures/m10-lecture-10/p{n:03}.png'
        t+=f'\n![[{target}]]\n\n[[{target}|打开本页清晰原图]]。来源：Lecture 10，物理 p.{n}；整页渲染保留图中文字和关系。\n'
        asset_manifest.append({'figure_id':f'm10-p{n:03}','source':source,'source_sha256':sha,'physical_page':n,'method':'pdftoppm -r 110 -png; full page; no crop','scratch_file':str(dest),'target':target,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'explanation_heading':p['heading']})
    texts.append(t)
mapping='\n'.join(f"| L10／{p['page']} | {p['title']} | [[#{p['heading']}\\|定位]] | "+(f"原图 m10-p{p['page']:03}" if p['kind']=='原图' else p['kind'])+' |' for p in pages)
ending=(o/'ending.md').read_text(encoding='utf-8').replace('{{PAGE_MAP}}',mapping)
candidate=(o/'intro.md').read_text(encoding='utf-8')+'\n\n'.join(texts)+'\n'+ending
atomic_write(o/name,candidate)
atomic_write(o/'asset-manifest.json',json.dumps(asset_manifest,ensure_ascii=False,indent=2)+'\n')
atomic_write(o/'page-content.json',json.dumps(pages,ensure_ascii=False,indent=2)+'\n')
evidence=f'# M10 逐页来源与视觉证据\n\n来源 `{source}`，SHA-256 `{sha}`，71 页。\n\n作者实际打开 `sheets/sheet01.png` 至 `sheet35.png`（每张两页）及 `pages/p-71.png`；页内主要文字、箭头和图例可辨认。源图渲染 110 DPI，2200×1238 像素。图密页 p.6 与小字控件以单页复核记录为准。不能以此声称视频已观看。\n\n| 物理页 | 原标题 | 实际视觉载体 | 独有要素／增量 | 正文标题 | 原图处置／补图判断 | 结果与边界 |\n|---|---|---|---|---|---|---|\n'
for p in pages:
    n=p['page']; carrier=f'sheets/sheet{(n+1)//2:02}.png' if n<71 else 'pages/p-71.png'
    first=p['body'].split('\n\n')[0].replace('|','／')
    if len(first)>170:first=first[:170]+'…（完整要素见页内容记录）'
    disposition=f"m10-p{n:03} 全页原图及就地解释" if p['kind']=='原图' else {'文字':'无教学结构图；文字页已解释，装饰不取','行政':'行政要求原值保留，不执行外部动作','封面':'装饰封面省略，保留讲次入口','分隔':'非内容入口，已链接后续范围','结束':'无新知识，保留复习回指'}[p['kind']]
    supplement='p.63 补真实失败分支／有限重试 Mermaid' if n==63 else ('完整原图已承载所讲关系；不重复重绘' if p['kind']=='原图' else '单事实／行政／文字分类不需另造流程')
    evidence+=f"| {n} | {p['title']} | {carrier} 已实际看 | {first} | {p['heading']} | {disposition}；{supplement} | 作者据源成稿；无转录／独立抽检另记 |\n"
atomic_write(o/'page-evidence.md',evidence)
questions=[{'page':15,'units':1,'source':'What is Responsible AI?','status':'完整保留题意和中英参考，非官方原答'}, {'page':27,'units':1,'source':'Would this individual have received the same prediction if their sensitive attribute had been different?','status':'完整问句与因果条件中英参考'}, {'page':28,'units':4,'source':'Did I get the loan? / Was the decision process fair and transparent?；3 pillars questions','status':'过程／结果情境与三支柱逐问参考'}, {'page':51,'units':12,'source':'System purpose 2 questions; stakeholder; mitigation and oversight tasks; 7 Accountability Yes/No checks','status':'原题/任务原文完整保留，逐项中文与英文参考；不伪填真实系统Yes/No'}, {'page':58,'units':1,'source':'What do we review our products for, and why?','status':'标题问句中英参考'}]
atomic_write(o/'question-evidence.json',json.dumps({'source':source,'source_sha256':sha,'scope':'all 71 physical pages visually read; explicit prompts below; rhetorical titles explained in corresponding body','questions':questions,'video_gaps':[13,14,17]},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'candidate':str(o/name),'candidate_sha256':hashlib.sha256((o/name).read_bytes()).hexdigest(),'bytes':(o/name).stat().st_size,'pages':len(pages),'figures':len(asset_manifest)},ensure_ascii=False))
