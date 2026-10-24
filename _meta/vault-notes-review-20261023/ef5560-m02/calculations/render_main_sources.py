import json,subprocess
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
B=Path(__file__).parent;O=B/'main-source';C=Path('D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance/course_files_export');P=Path('C:/Users/BenLi/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe')
new=O/'render-new';new.mkdir(exist_ok=True)
subprocess.run([str(P),'-r','120','-png',str(C/'canvas-20261020/Lec02_Regression_Vibe_Coding.pdf'),str(new/'new')],check=True,capture_output=True)
diffs=[]
for a in range(1,55):
 b=a if a<=25 else 54 if a==26 else a+1 if a<=52 else a+2
 oldim=Image.open(B/f'source-review/render/old-{a:02d}.png').convert('RGB');newim=Image.open(new/f'new-{b:02d}.png').convert('RGB');assert oldim.size==newim.size
 box=(0,0,oldim.width,oldim.height-24);d=ImageChops.difference(oldim.crop(box),newim.crop(box));bbox=d.getbbox()
 if bbox:diffs.append({'old':a,'new':b,'difference_bbox_excluding_bottom_24_pixels':bbox})
high=O/'render-critical';high.mkdir(exist_ok=True)
pages=[3,5,12,19,25,29,34,36,37,38,39,40,44,46,47,48,49,50,51]
for ver,pp in [('old',pages),('new',[26,27])]:
 pdf=C/('Lec02_Regression_Vibe_Coding.pdf' if ver=='old' else 'canvas-20261020/Lec02_Regression_Vibe_Coding.pdf')
 for n in pp:subprocess.run([str(P),'-r','230','-f',str(n),'-l',str(n),'-singlefile','-png',str(pdf),str(high/f'{ver}-{n:02d}')],check=True,capture_output=True)
record={'new_pages_rendered':56,'old_source_rendered_page_count':54,'matched_page_images_excluding_bottom_footer':54-len(diffs),'differences':diffs,'critical_230dpi_pages':{'old':pages,'new':[26,27]},'not_visual_acceptance_until_root_views':True}
(O/'page-pixel-comparison.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(record,ensure_ascii=False))
