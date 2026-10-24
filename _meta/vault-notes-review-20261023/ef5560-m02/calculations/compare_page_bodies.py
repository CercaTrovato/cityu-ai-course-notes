import json
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
B=Path(__file__).parent;O=B/'main-source';rows=[]
for a in range(1,55):
 b=a if a<=25 else 54 if a==26 else a+1 if a<=52 else a+2
 p=Image.open(B/f'source-review/render/old-{a:02d}.png').convert('RGB');q=Image.open(O/f'render-new/new-{b:02d}.png').convert('RGB')
 dif=ImageChops.difference(p,q)
 # Mask only the visible slide-progress rule and page-count footer, not body content.
 draw=ImageDraw.Draw(dif);draw.rectangle((0,45,755,49),fill='black');draw.rectangle((700,388,755,425),fill='black')
 bbox=dif.getbbox();count=sum(1 for v in dif.getdata() if v!=(0,0,0))
 rows.append({'old':a,'new':b,'changed_pixels':count,'body_difference_bbox':bbox})
 if bbox:dif.save(O/f'body-diff-{a:02d}.png')
out={'masked_regions_at_756x426':'slide progress rule y45-49; page count x700-755,y388-425','exact_body_matches':sum(x['changed_pixels']==0 for x in rows),'remaining_differences':[x for x in rows if x['changed_pixels']],'not_substitute_for_reading':True}
(O/'page-body-comparison.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
