from pathlib import Path
import re,sys,shutil,json,hashlib,html
import markdown
from bs4 import BeautifulSoup
root=Path(r'D:\上课资料\CityU');work=Path(r'E:\app-data\codex\scratchpad\ef5560-final-20261128')
preview=work/'preview-public';preview.mkdir(parents=True,exist_ok=True)
vendor=preview/'vendor';vendor.mkdir(exist_ok=True)
katex=Path(r'E:\app-data\diagram-tools\node_modules\katex\dist')
if not (vendor/'katex').exists():shutil.copytree(katex,vendor/'katex')
mermaid=Path(r'E:\app-data\diagram-tools\node_modules\mermaid\dist\mermaid.min.js')
if mermaid.exists() and not (vendor/'mermaid.min.js').exists():shutil.copy2(mermaid,vendor/'mermaid.min.js')
manifest=[]
for mod in ['m11','m12']:
    candidate=work/mod/'merged.md'
    if not candidate.exists():continue
    text=candidate.read_text(encoding='utf-8');text=re.sub(r'\A---\n.*?\n---\n','',text,flags=re.S)
    def publish_image(rel):
        src=root/rel
        if not src.exists():src=root/'EF5560_Fintech_and_AI_in_Finance'/'notes'/rel
        if not src.exists():return '<strong>Missing image: '+html.escape(rel)+'</strong>'
        name=hashlib.sha256(rel.encode()).hexdigest()[:10]+'-'+src.name
        dst=preview/'images'/name;dst.parent.mkdir(exist_ok=True);shutil.copy2(src,dst)
        manifest.append({'source':rel,'asset':str(dst.relative_to(preview)),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
        return f'<a href="images/{name}" target="_blank"><img src="images/{name}" alt="{html.escape(src.name)}"></a>'
    def image(m):return publish_image(m.group(1).split('|')[0])
    text=re.sub(r'!\[\[([^\]]+)\]\]',image,text)
    text=re.sub(r'!\[[^\]]*\]\(([^)]+)\)',lambda m:publish_image(m.group(1).strip('<>')),text)
    def link(m):
        raw=m.group(1).replace('\\|','|');parts=raw.split('|',1);target=parts[0];label=parts[-1]
        if target.startswith('#'):url=target
        elif '#' in target:
            file,anchor=target.split('#',1);other='m12' if '/M12-' in file else 'm11' if '/M11-' in file else None
            url=(other+'.html#'+anchor) if other else '#'
        else:url='m12.html' if '/M12-' in target else 'm11.html' if '/M11-' in target else '#'
        return '<a href="'+html.escape(url,quote=True)+'">'+html.escape(label)+'</a>'
    text=re.sub(r'\[\[([^\]]+)\]\]',link,text)
    maths=[]
    def hold_math(m):
        idx=len(maths);maths.append(m.group(0));return 'MATHKEEP'+str(idx)+'END'
    text=re.sub(r'(?<!\\)\$\$[\s\S]*?(?<!\\)\$\$',hold_math,text)
    text=re.sub(r'(?<!\\)\$(?!\$)(?:\\.|[^$\n])*?(?<!\\)\$',hold_math,text)
    text=text.replace('\\$','<span class="nomath">$</span>')
    body=markdown.markdown(text,extensions=['tables','fenced_code','toc','md_in_html'])
    for idx,formula in enumerate(maths):body=body.replace('MATHKEEP'+str(idx)+'END',html.escape(formula))
    soup=BeautifulSoup(body,'html.parser')
    for h in soup.find_all(re.compile('^h[1-6]$')):h['id']=h.get_text()
    for code in soup.select('code.language-mermaid'):
        div=soup.new_tag('div');div['class']='mermaid';div.string=code.get_text();code.parent.replace_with(div)
    page='''<!DOCTYPE html><html lang="zh-CN"><meta charset="utf-8"><link rel="stylesheet" href="vendor/katex/katex.min.css"><style>body{max-width:980px;margin:0 auto;padding:32px;font:17px/1.75 "Microsoft YaHei",Arial;color:#20252c;background:#fffdf8}h1,h2,h3,h4{line-height:1.4;scroll-margin-top:24px}h2{margin-top:3em;border-bottom:1px solid #d5d5d5}a{color:#075e85}img{display:block;max-width:100%;height:auto;margin:20px auto}table{border-collapse:collapse;width:100%;display:block;overflow-x:auto;margin:20px 0;font-size:15px}th,td{padding:9px;border:1px solid #ccc;min-width:60px;vertical-align:top}blockquote{border-left:4px solid #5e7b83;padding:8px 16px;background:#edf3f3}pre{white-space:pre-wrap}details{padding:12px;background:#f3f3f0;margin:15px 0}.katex-display{overflow-x:auto;overflow-y:hidden}</style><title>EF5560 融合预览</title>'''+str(soup)+'''<script src="vendor/katex/katex.min.js"></script><script src="vendor/katex/contrib/auto-render.min.js"></script><script src="vendor/mermaid.min.js"></script><script>renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],ignoredClasses:['nomath'],throwOnError:false});mermaid.initialize({startOnLoad:true,securityLevel:'strict'});</script></html>'''
    (preview/(mod+'.html')).write_text(page,encoding='utf-8')
(work/'preview-assets.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('rendered',len(list(preview.glob('m*.html'))),'pages,',len(manifest),'images')
