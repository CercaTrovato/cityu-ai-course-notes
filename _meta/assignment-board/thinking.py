"""Local-only project reasoning, with explicit source files and revision checks."""
import csv
import hashlib
import html
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
import bleach
import markdown

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def location(root, assignment_id):
    if not re.fullmatch(r'[A-Z]{2}\d{4}-A\d{2}',assignment_id): raise ValueError('作业编号无效')
    course,aid=assignment_id.split('-')
    found=list(root.glob(f'{course}_*/assignment/graded/{aid}-*/thinking.json'))
    if len(found)>1: raise ValueError('发现重复的思路记录')
    return found[0] if found else None

def source_path(root,manifest,source):
    p=Path(source['path']).resolve()
    course_root=manifest.parents[3].resolve()
    config=root/'_meta/assignment-board/thinking-sources.local.json'
    permitted=json.loads(config.read_text('utf-8')) if config.exists() else {}
    allowed=[course_root]+[Path(x).resolve() for x in permitted.get('roots',{}).get(manifest.parent.name,[])]
    if not any(p.is_relative_to(r) for r in allowed) or p.suffix.lower() not in ('.md','.csv','.json','.py'):
        raise ValueError('该资料不在本课程的本地阅读清单内')
    if not p.is_file(): raise ValueError('来源文件当前缺失')
    if p.stat().st_size>2_000_000: raise ValueError('来源过大，请使用摘要和原始数据索引')
    return p

def load(root,assignment_id):
    manifest=location(root,assignment_id)
    if not manifest: return None
    d=json.loads(manifest.read_text('utf-8'))
    if d.get('schema_version')!=1 or d.get('assignment_id')!=assignment_id: raise ValueError('思路记录的版本或归属不匹配')
    if d.get('publication')!='local_review': raise ValueError('本地思路预览须保留待验收状态')
    nodes=d.get('nodes',[]);ids=[n['id'] for n in nodes];sources=[s['id'] for s in d['sources']]
    if not nodes or len(ids)!=len(set(ids)) or len(sources)!=len(set(sources)): raise ValueError('节点或来源编号缺失／重复')
    for n in nodes:
        if not re.fullmatch(r'[a-z0-9-]+',n['id']): raise ValueError('节点编号无效')
        for key in ('question','choice','result','meaning','next','owner','date','status','summary','title'):
            if not isinstance(n.get(key),str) or not n[key].strip(): raise ValueError(f'{n["id"]} 缺少 {key}')
        if n['status'] not in ('team','decision','local','pending','idea'): raise ValueError('节点状态无效')
        if not set(n['evidence']).issubset(sources): raise ValueError('节点引用了未登记来源')
        if not isinstance(n['stage'],int) or not 0<=n['stage']<=12: raise ValueError('节点层级无效')
    for e in d['edges']:
        if e['from'] not in ids or e['to'] not in ids: raise ValueError('连线引用缺失节点')
    warnings=[]
    if digest(manifest.parent/'assignment.json')!=d.get('assignment_revision'): warnings.append('课程进度台账已有新版本；本页仍保留注明日期的思路记录，请复核新增进展。')
    for s in d['sources']:
        try:
            p=source_path(root,manifest,s);s['current_sha256']=digest(p);s['changed']=s['current_sha256']!=s['sha256'];s['available']=True
            if s['changed']: warnings.append(s['title']+' 已更新，节点解释需复核。')
        except (OSError,ValueError) as exc: s['available']=False;s['error']=str(exc);warnings.append(s['title']+'：'+str(exc))
        s.pop('path',None)
    d['latest_progress']=json.loads((manifest.parent/'assignment.json').read_text('utf-8-sig')).get('summary','') if digest(manifest.parent/'assignment.json')!=d.get('assignment_revision') else ''
    d['warnings']=warnings;d['revision']=digest(manifest)
    return d

class Links(HTMLParser):
    def __init__(self,source,paths): super().__init__(convert_charrefs=False);self.source=source;self.paths=paths;self.out=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='a':
            href=attrs.get('href','');split=urlsplit(href)
            if split.scheme in ('https','http'): attrs.update(target='_blank',rel='noopener noreferrer')
            elif href.startswith('#'): pass
            else:
                target=(self.source.parent/unquote(href.split('#')[0])).resolve()
                found=self.paths.get(str(target).casefold())
                attrs={'href':'#','data-thinking-source':found} if found else {'title':'此引用未纳入本页阅读清单'}
        self.out.append('<'+tag+''.join(' '+k+'="'+html.escape(v or '',quote=True)+'"' for k,v in attrs.items())+'>')
    def handle_endtag(self,tag): self.out.append('</'+tag+'>')
    def handle_data(self,value): self.out.append(value)
    def handle_entityref(self,name): self.out.append('&'+name+';')
    def handle_charref(self,name): self.out.append('&#'+name+';')

def source_content(root,assignment_id,source_id):
    manifest=location(root,assignment_id)
    if not manifest: raise ValueError('本课程还没有登记思路资料')
    d=json.loads(manifest.read_text('utf-8'));source=next((s for s in d['sources'] if s['id']==source_id),None)
    if not source: raise ValueError('资料编号未登记')
    p=source_path(root,manifest,source);text=p.read_text('utf-8-sig');kind=p.suffix.lower()
    rows=None
    if kind=='.md':
        rendered=markdown.markdown(text,extensions=['tables','fenced_code','sane_lists'])
        paths={}
        for s in d['sources']:
            try: paths[str(source_path(root,manifest,s)).casefold()]=s['id']
            except ValueError: pass
        parser=Links(p,paths);parser.feed(rendered);rendered=''.join(parser.out)
        rendered=bleach.clean(rendered,tags=['h1','h2','h3','h4','h5','h6','p','br','hr','strong','em','ul','ol','li','blockquote','pre','code','table','thead','tbody','tr','th','td','a'],attributes={'a':['href','title','target','rel','data-thinking-source'],'code':['class']},protocols=['https','http'],strip=True)
    elif kind=='.csv':
        rows=list(csv.DictReader(io.StringIO(text)));fields=list(rows[0]) if rows else []
        rendered='<p>显示前 500 行，共 '+str(len(rows))+' 行。</p><table><thead><tr>'+''.join('<th>'+html.escape(k)+'</th>' for k in fields)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(row[k])+'</td>' for k in fields)+'</tr>' for row in rows[:500])+'</tbody></table>'
    else: rendered='<pre>'+html.escape(text)+'</pre>'
    return {'title':source['title'],'html':rendered,'rows':rows,'sha256':digest(p),'changed':digest(p)!=source['sha256'],'kind':kind,'path':str(p)}
