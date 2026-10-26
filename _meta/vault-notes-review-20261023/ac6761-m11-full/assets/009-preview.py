from pathlib import Path
import http.server, urllib.parse, re, mistune, html, json, sys
OUT=Path(__file__).resolve().parent
ROOT=Path(r'D:\上课资料\CityU')
RUNTIME=Path(r'E:\app-data\diagram-tools\node_modules')
SOURCE=Path(r'E:\app-data\codex\scratchpad\ac6761-canvas-20261022\render-Week-11-PPT')
text=(OUT/'candidate.md').read_text(encoding='utf-8')
text=re.sub(r'^---\n.*?\n---\n','',text,count=1,flags=re.S)
blocks=[]; maths=[]
def block(m):
 blocks.append(m[0]); return f'CODEPLACEHOLDER{len(blocks)-1}END'
text=re.sub(r'```.*?```',block,text,flags=re.S)
text=re.sub(r'!\[\[([^\]]+)\]\]',lambda m:f'<img src="/vault/{urllib.parse.quote(m[1])}" alt="教学回归图">',text)
text=re.sub(r'\[\[([^\]|]+)(?:\\?\|([^\]]+))?\]\]',lambda m:f'[{m[2] or m[1]}](/vault/{urllib.parse.quote(m[1])})',text)
def math(m,display=False):
 maths.append((m[1],display)); return f'MATHPLACEHOLDER{len(maths)-1}END'
text=re.sub(r'\$\$\s*\n(.*?)\n\s*\$\$',lambda m:math(m,True),text,flags=re.S)
text=re.sub(r'(?<!\\)\$([^$\n]+?)(?<!\\)\$',math,text)
for i,b in enumerate(blocks): text=text.replace(f'CODEPLACEHOLDER{i}END',b)
body=mistune.create_markdown(escape=False,plugins=['table','strikethrough'])(text)
for i,(tex,display) in enumerate(maths):
 tag='div' if display else 'span'; el=f'<{tag} class="math'+(' math-block' if display else '')+'">'+html.escape(tex)+f'</{tag}>'
 body=body.replace(f'<p>MATHPLACEHOLDER{i}END</p>',el).replace(f'MATHPLACEHOLDER{i}END',el)
body=re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>',r'<pre class="mermaid">\1</pre>',body,flags=re.S)
heading_index=iter(range(100))
body=re.sub(r'<(h[234])>',lambda m:f'<{m[1]} id="heading-{next(heading_index)}">',body)
for key,needle in [('returns','💡 换个说法（笔记补充）：同一起点，两种收益口径。'),('entry','安全运行入口（笔记补充）'),('statistics-tail','改一个条件便能检验这条逻辑')]:
 body=re.sub(r'<p>(?=(?:(?!</p>).)*'+re.escape(needle)+r')',f'<p id="{key}">',body,count=1,flags=re.S)
diagram_index=iter(range(1,4))
body=re.sub(r'<pre class="mermaid">',lambda m:f'<pre class="mermaid" id="diagram-{next(diagram_index)}">',body)
HEAD='''<!DOCTYPE html><html lang="zh-CN"><meta charset="utf-8"><title>M11 最终同源检查</title><link rel="stylesheet" href="/runtime/katex/dist/katex.min.css"><style>
body{font:17px/1.85 "Microsoft YaHei",sans-serif;color:#243348;background:#f4f6f9;margin:0}main{max-width:940px;margin:32px auto;background:white;padding:42px 54px}h1,h2,h3,h4{line-height:1.4;color:#113654}h2{margin-top:2.5em;border-bottom:1px solid #ccd8e4;padding-bottom:12px}p{margin:1em 0}table{border-collapse:collapse;width:100%;font-size:15px;margin:1em 0}th,td{border:1px solid #ccd6df;padding:7px 10px;text-align:left;vertical-align:top}th{background:#eef3f7}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f5f7;padding:18px;font:14px/1.5 Consolas,monospace}blockquote{border-left:4px solid #7c9bb6;padding-left:18px;color:#405366}img,svg{max-width:100%;height:auto}a{color:#1a6396}details{background:#f8fafc;padding:12px;margin:1em 0}summary{cursor:pointer}nav{position:fixed;top:8px;right:8px;background:white;padding:8px;font-size:12px}.katex-display{overflow-x:auto}.mermaid{background:white;text-align:center;padding:0}
</style><style>nav{display:none}</style><nav>当前候选同源预览 · Obsidian 未直接查看</nav><main>'''
TAIL='''</main><script src="/runtime/katex/dist/katex.min.js"></script><script>
window.mathErrors=[];document.querySelectorAll('.math').forEach(el=>{try{katex.render(el.textContent,el,{displayMode:el.classList.contains('math-block'),throwOnError:true,strict:false})}catch(e){window.mathErrors.push(String(e))}});
</script><script type="module">import mermaid from '/runtime/mermaid/dist/mermaid.esm.min.mjs';mermaid.initialize({startOnLoad:false,securityLevel:'strict',theme:'neutral',flowchart:{htmlLabels:true}});window.diagramErrors=[];try{await mermaid.run({querySelector:'.mermaid'})}catch(e){window.diagramErrors.push(String(e))}window.previewReady=true;</script></html>'''
(OUT/'preview.html').write_text(HEAD+body+TAIL,encoding='utf-8')
diagrams=re.findall(r'<pre class="mermaid"[^>]*>.*?</pre>',body,re.S)
(OUT/'diagrams.html').write_text(HEAD+'<h1>M11 三张同源图</h1>'+''.join(f'<h2>图 {i}</h2>'+d for i,d in enumerate(diagrams,1))+TAIL,encoding='utf-8')
if '--build-only' in sys.argv: sys.exit(0)
class Handler(http.server.SimpleHTTPRequestHandler):
 def translate_path(self,path):
  path=urllib.parse.unquote(urllib.parse.urlparse(path).path); base=OUT
  for prefix,target in [('/runtime/',RUNTIME),('/vault/',ROOT),('/source/',SOURCE)]:
   if path.startswith(prefix): base=target;path=path[len(prefix):];break
  else:path=path.lstrip('/')
  dest=(base/path).resolve()
  return str(dest if dest.is_relative_to(base.resolve()) else OUT/'invalid')
 def log_message(self,*args):pass
http.server.ThreadingHTTPServer(('127.0.0.1',8812),Handler).serve_forever()
