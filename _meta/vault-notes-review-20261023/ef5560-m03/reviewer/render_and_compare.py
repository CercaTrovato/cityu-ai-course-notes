from pathlib import Path
import json,re,difflib,subprocess
from PIL import Image,ImageOps,ImageDraw
OUT=Path('E:/app-data/codex/scratchpad/cityu-review-resume-20261025/ef5560-m03-review-61/reviewer')
MAP=json.loads((OUT.parent/'source-map.json').read_text(encoding='utf-8'))
old=json.loads((OUT/'old56-pages.json').read_text(encoding='utf-8'))
new=json.loads((OUT/'new54-pages.json').read_text(encoding='utf-8'))
def norm(s):return re.sub(r'\s+',' ',re.sub(r'\b\d+/(54|56)\b','',s)).strip()
mapping=[]
changed=[]
for j,np in enumerate(new,1):
    oi=j if j<=32 else j+2
    op=old[oi-1]
    same=norm(op)==norm(np)
    mapping.append({'old':oi,'new':j,'same_text_without_footer':same})
    if not same: changed.append({'old':oi,'new':j,'old_text':op,'new_text':np})
(OUT/'new54-comparison.json').write_text(json.dumps({'mapping':mapping,'deleted_old':[33,34],'changed':changed},ensure_ascii=False,indent=2),encoding='utf-8')
pages=[4,6,10,12,13,15,17,19,20,22,24,26,27,32,35,36,38,40,41,43,44,47,48,50,54,55,56]
RENDER=OUT/'fresh-pdf-render'; RENDER.mkdir(exist_ok=True)
for label,idx in [('old56',0),('new54',1)]:
    selected=pages if label=='old56' else [p if p<=32 else p-2 for p in pages]
    for p in selected:
        dest=RENDER/f'{label}-p{p:02}'
        subprocess.run(['D:/poppler/Library/bin/pdftoppm.exe','-f',str(p),'-l',str(p),'-r','135','-singlefile','-png',MAP['originals'][idx]['path'],str(dest)],check=True,capture_output=True)
    for k in range(0,len(selected),4):
        subset=selected[k:k+4]
        thumbw=1152; thumbh=690
        sheet=Image.new('RGB',(thumbw*2,thumbh*2),'white')
        draw=ImageDraw.Draw(sheet)
        for q,p in enumerate(subset):
            im=Image.open(RENDER/f'{label}-p{p:02}.png').convert('RGB')
            im.thumbnail((thumbw,thumbh-26))
            x=(q%2)*thumbw;y=(q//2)*thumbh
            sheet.paste(im,(x,y+26)); draw.text((x+8,y+5),f'{label} page {p}',fill='black')
        sheet.save(RENDER/f'{label}-sheet-{k//4+1:02}.png')
print('changed_new_pages',[(x['old'],x['new']) for x in changed])
print('text_identical_pages',sum(x['same_text_without_footer'] for x in mapping),'of54')
print('rendered',len(pages)*2,'source pages','contact sheets',len(list(RENDER.glob('*sheet*'))))
