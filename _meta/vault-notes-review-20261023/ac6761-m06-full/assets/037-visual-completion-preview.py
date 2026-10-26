from pathlib import Path
import runpy,re,hashlib,json,markdown
O=Path(__file__).parent
EXPECTED='ef8dd59794d5eba4b0a52a545c9db589775cf3ca536208e31d798af57763d8c4'
p=O/'candidate-v1.md'
assert hashlib.sha256(p.read_bytes()).hexdigest()==EXPECTED
runpy.run_path(str(O/'preview.py'))
t=p.read_text(encoding='utf-8')
t=re.sub(r'^---\n.*?\n---\n','',t,count=1,flags=re.S)
t=t.replace('<details>','<details open markdown="1">')
# Convert Obsidian link labels only for same-source reading, without navigating.
t=re.sub(r'\[\[([^\]]+)\]\]',lambda m:m[1].replace('\\|','|').split('|')[-1],t)
body=markdown.markdown(t,extensions=['tables','fenced_code','md_in_html','toc','sane_lists'],tab_length=2)
body=re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>',r'<pre class="mermaid">\1</pre>',body,flags=re.S)
css='''body{margin:0;background:#f2f2f2;color:#202020;font:18px/1.65 "Microsoft YaHei",sans-serif}header{position:sticky;top:0;background:#fff;border-bottom:1px solid #aaa;padding:8px 20px;z-index:2;font-size:13px}main{max-width:1040px;margin:auto;background:#fff;padding:24px 42px}p,li{overflow-wrap:anywhere}table{border-collapse:collapse;font-size:16px;width:100%;table-layout:auto}td,th{border:1px solid #bbb;padding:8px;text-align:left}blockquote{border-left:4px solid #789;padding-left:18px;margin:20px 0;background:#f7f9fb}pre{background:#f1f3f5;padding:15px;overflow:auto;font-size:15px;line-height:1.5}code{font-family:Consolas,monospace}h1,h2,h3,h4{line-height:1.4;scroll-margin-top:55px}summary{font-weight:bold;cursor:pointer}.mermaid{background:white;text-align:center;white-space:normal;overflow:visible}.mermaid svg{max-width:100%;height:auto}.katex-display{overflow-x:auto;overflow-y:hidden}details{padding:8px;border-left:2px solid #ddd}'''
script='''window.visualReady=false;window.visualErrors=[];
mermaid.initialize({startOnLoad:false,securityLevel:'strict',theme:'default',fontFamily:'Microsoft YaHei'});
(async()=>{try{await mermaid.run({querySelector:'.mermaid'});}catch(e){window.visualErrors.push(String(e));}
try{renderMathInElement(document.querySelector('main'),{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false,ignoredTags:['script','noscript','style','textarea','pre','code']});}catch(e){window.visualErrors.push(String(e));}
window.visualReady=true;document.querySelector('#render-state').textContent='render complete; '+window.visualErrors.join('; ');})();'''
page='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>M06 frozen candidate visual completion</title><link rel="stylesheet" href="/deps/katex/katex.min.css"><style>'+css+'</style></head><body><header>冻结候选 '+EXPECTED+' · 同源浏览器显示，非 Obsidian/Access UI · <span id="render-state">rendering</span></header><main>'+body+'</main><script src="/deps/mermaid.min.js"></script><script src="/deps/katex/katex.min.js"></script><script src="/deps/katex/contrib/auto-render.min.js"></script><script>'+script+'</script></body></html>'
(O/'visual-completion-preview.html').write_text(page,encoding='utf-8')
(O/'visual-completion-source.json').write_text(json.dumps({'candidate_sha256':EXPECTED,'preview_sha256':hashlib.sha256(page.encode()).hexdigest(),'renderer':'existing preview.py plus full same-source markdown/tables/folds/wikilink labels; local Mermaid/KaTeX','port':8814,'port_requested':8813,'port_change_reason':'8813 occupied by EF04 pid69680; not stopped or modified'},ensure_ascii=False,indent=2),encoding='utf-8')
print('full same-source preview ready')
