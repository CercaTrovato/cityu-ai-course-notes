from pathlib import Path
import re,json,hashlib,runpy
import markdown
O=Path(__file__).parent
v1=(O/'candidate-v1.md').read_text(encoding='utf-8');v2=(O/'candidate-v2.md').read_text(encoding='utf-8')
H1='ef8dd59794d5eba4b0a52a545c9db589775cf3ca536208e31d798af57763d8c4';H2='d9d556997ffb6ba936d8aabbb610242a45f24eb7a463fca90bad68d7086c4a5c'
assert hashlib.sha256((O/'candidate-v1.md').read_bytes()).hexdigest()==H1
assert hashlib.sha256((O/'candidate-v2.md').read_bytes()).hexdigest()==H2
basehtml=(O/'visual-completion-preview.html').read_text(encoding='utf-8')
(O/'visual-full-v1.html').write_text(basehtml,encoding='utf-8')
head=basehtml.split('<main>')[0];tail=basehtml.split('</main>',1)[1]
def span(t,a,b):
 i=t.index(a);j=t.index(b,i+len(a));return t[i:j]
def section(t,prefix):
 m=re.search(r'^(#{2,4}) '+re.escape(prefix)+r'.*$',t,re.M);assert m,prefix
 n=re.search(r'^#{1,'+str(len(m[1]))+r'} ',t[m.end():],re.M)
 return t[m.start():m.end()+n.start()] if n else t[m.start():]
panels=[
('01-cutoff',span(v1,'<details><summary>可选的 SQLite','**所以呢**：JOIN用于'),'v1'),
('02-permatch',span(v1,'**例 3：逐匹配行减法','**在 Access 里怎么写横向计算**'),'v1'),
('03-sql',section(v1,'2.17.3 ')+section(v1,'2.17.4 '),'v1'),
('04-two-three-columns',span(v1,'**结果**（讲义 p.72 截图）','**所以呢**'),'v1'),
('05-quiz',section(v1,'2.23.9 '),'v1'),
('06-wauc',span(v1,'**那么这件商品“一件平均多少钱”？**','**⚠️⚠️ 标题里')+'\n\n'+span(v1,'💡 **先读函数，再看安全分母**','**⚠️ 结果只有三个商品')+'\n\n'+span(v1,'**安全除法与Access边界**','**图旁边界**：原查询标not'),'v1'),
('07-order-grain',span(v1,'💡 **按客户计算之前','**⚠️ 2.5 天这个数字'),'v1'),
('08-antijoin',span(v1,'**截图：查询设计视图**（窗口标题 `InventoryWithout','**⭐ 这一页把 W6 接回了 M05'),'v1'),
('09-quick-join',section(v1,'4.3 '),'v1'),
('10-quick-queries-v2',section(v2,'4.8 '),'v2'),
('11-definitions',span(v1,'**字段类型兼容与显示属性**','**强制参照完整性**')+'\n\n'+span(v1,'**空值替代函数**','**行项目金额**'),'v1'),
('12-framework',section(v1,'框架 C '),'v1'),
('13-source-errors',span(v1,'### 9.3 课件自身的问题','#### C. 命名与拼写不一致'),'v1'),
('18-v2-question-table',span(v2,'⚠️ **仅凭总账分录无法读出客户对产品的反应。**','**💡 换个说法（笔记补充）**'),'v2')
]
answerdict={}
for m in re.finditer(r'\*\*英文参考答案（笔记自拟，(U\d{2})）\*\*[^\n]*\n\n> ([^\n]+)',v1):
 answerdict[m[1]]=m.group(0)
answerdict['U22']=next(l for l in v1.splitlines() if '**English reference answer（笔记参考答案）**' in l)
oral=next(l for l in v1.splitlines() if 'For the reconstructed not-equal-to-C-2 condition' in l)
answerdict['U23']='**U23 · 英文参考（原口述与重建边界）**\n\n'+oral
assert len(answerdict)==34,len(answerdict)
for k,lo in enumerate((1,10,19,28),14):
 keys=[f'U{i:02d}' for i in range(lo,min(lo+9,35))]
 panels.append((f'{k:02d}-english-'+keys[0]+'-'+keys[-1],'\n\n---\n\n'.join(answerdict[x] for x in keys),'v1'))
manifest=[]
for name,raw,version in panels:
 bodyraw=raw.replace('<details>','<details open markdown="1">')
 bodyraw=re.sub(r'\[\[([^\]]+)\]\]',lambda m:m[1].replace('\\|','|').split('|')[-1],bodyraw)
 body=markdown.markdown(bodyraw,extensions=['tables','fenced_code','md_in_html','toc','sane_lists'],tab_length=2)
 body=re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>',r'<pre class="mermaid">\1</pre>',body,flags=re.S)
 h=H2 if version=='v2' else H1
 currenthead=re.sub('冻结候选 '+H1,'冻结候选 '+h,head)
 page=currenthead+'<main><h1>'+name+'</h1>'+body+'</main>'+tail
 path=O/f'visual-panel-{name}.html';path.write_text(page,encoding='utf-8')
 manifest.append({'name':name,'version':version,'candidate_sha256':h,'html':str(path),'html_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_excerpt_sha256':hashlib.sha256(raw.encode()).hexdigest()})
(O/'visual-panel-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(O/'visual-completion-preview.html').write_bytes(Path(manifest[0]['html']).read_bytes())
print(json.dumps({'panels':len(manifest),'names':[x['name'] for x in manifest]},ensure_ascii=False))
