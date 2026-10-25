from pathlib import Path
import re,json,subprocess,html
OUT=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61/reviewer')
CAND=(OUT.parent/'candidate.md').read_text(encoding='utf-8')
code=re.findall(r'```mermaid\s*\n(.*?)\n```',CAND,re.S)
mermaid=Path('E:/app-data/diagram-tools/node_modules/mermaid/dist/mermaid.min.js')
script=mermaid.read_text(encoding='utf-8')
svg=Path('D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance/notes/figures/readability-v2/pcr-pls-directions.svg')
for i,block in enumerate(code,1):
    doc='<!doctype html><html><meta charset="utf-8"><style>body{font-family:Arial,"Microsoft YaHei";margin:28px} .mermaid{max-width:1160px} svg{max-height:950px;max-width:1160px}</style><h2>Candidate exact Mermaid '+str(i)+'</h2><pre class="mermaid">'+html.escape(block)+'</pre><script>'+script+'</script><script>mermaid.initialize({startOnLoad:true,securityLevel:"strict",theme:"default",flowchart:{useMaxWidth:true}});</script></html>'
    (OUT/f'candidate-graph-{i}.html').write_text(doc,encoding='utf-8')
(OUT/'candidate-svg.html').write_text('<!doctype html><html><meta charset="utf-8"><style>body{margin:24px} img{max-width:1200px}</style><img src="'+svg.as_uri()+'"></html>',encoding='utf-8')
edge='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
profile=OUT/'edge-review-profile'
records=[]
for name in [f'candidate-graph-{i}' for i in range(1,7)]+['candidate-svg']:
    p=OUT/(name+'.html'); shot=OUT/(name+'.png')
    args=[edge,'--headless','--no-first-run','--disable-gpu','--allow-file-access-from-files','--no-default-browser-check','--virtual-time-budget=5000','--hide-scrollbars','--window-size=1300,1100','--user-data-dir='+str(profile),'--screenshot='+str(shot),p.as_uri()]
    r=subprocess.run(args,capture_output=True,text=True,timeout=40)
    records.append({'name':name,'exit':r.returncode,'image_exists':shot.exists(),'stderr_tail':r.stderr[-400:]})
(OUT/'browser-render-records.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(records)
