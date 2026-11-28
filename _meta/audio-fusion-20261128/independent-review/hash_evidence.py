from pathlib import Path
from PIL import Image
import hashlib,json
out=Path('E:/app-data/codex/scratchpad/ef5560-final-20261128/independent-review')
course=Path('D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance')
paths=[out/p for p in ['m11-stage-1.md','m12-stage-1.md','m11-transcript-windows.txt','m12-transcript-windows.txt','m11-sample-diff.txt','m12-sample-diff.txt']]
paths+=list(out.glob('*-source-sheet-*.png'))
paths += [course/'notes/figures'/p for p in ['m11/source-p45.png','m11/source-p50.png','m12/lec12-p30.png','m12/lec12-p33.png','m12/lec12-p36.png']]
rows=[]
for p in paths:
    row={'path':str(p).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    if p.suffix=='.png': row['dimensions']=list(Image.open(p).size)
    rows.append(row)
(out/'evidence-hashes.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for row in rows:
    if 'notes/figures' in row['path']: print(row)
for n in ['m11-independent-review.md','m12-independent-review.md']:
    p=out/n; print(n,hashlib.sha256(p.read_bytes()).hexdigest())
