from pathlib import Path
import re, difflib,hashlib
root=Path('E:/app-data/codex/scratchpad/ef5560-final-20261128')
src=Path('E:/app-data/codex/outputs/ef5560-final-20261128/public-source/M11-M12-transcript-source35-redacted.txt')
txt=src.read_text(encoding='utf-8')
def sec(t):
    v=list(map(int,t.split(':'))); return sum(n*60**i for i,n in enumerate(reversed(v)))
parts=re.split(r'(?m)^(\d{1,2}:\d\d(?::\d\d)?)\s*$',txt)
segments=[(parts[i],parts[i+1].strip()) for i in range(1,len(parts),2)]
windows={'m11':[('04:19','08:49'),('20:37','28:08'),('31:46','40:54')],'m12':[('01:33:17','01:38:58'),('01:40:33','01:41:36'),('01:43:47','02:03:34')]}
print('source SHA',hashlib.sha256(src.read_bytes()).hexdigest())
for name,ranges in windows.items():
    output=[]
    for a,b in ranges:
        output.append(f'WINDOW {a}--{b}')
        output.extend(t+' '+s for t,s in segments if sec(a)<=sec(t)<sec(b))
    (root/'independent-review'/f'{name}-transcript-windows.txt').write_text('\n\n'.join(output),encoding='utf-8')
for name,baseline in [('m11','baseline-M11-数字信贷与众筹.md'),('m12','baseline-M12-智能投顾网络安全与监管科技.md')]:
    p=root/baseline; data=p.read_text(encoding='utf-8')
    print(name,'baseline SHA',hashlib.sha256(p.read_bytes()).hexdigest())
    pages=([39,45,46,47,49,50,52] if name=='m11' else [24,26,27,29,30,31,32,33,34,35,36,37,38])
    cand=(root/name/'merged.md').read_text(encoding='utf-8')
    output=[]
    for pg in pages:
        pattern=rf'(?ms)^### 2\.{pg:02d} p\.0?{pg}\b.*?(?=^### |^## |\Z)'
        old=re.search(pattern,data); new=re.search(pattern,cand)
        if old and new:
            output.extend(difflib.unified_diff(old.group().splitlines(),new.group().splitlines(),fromfile=f'baseline-p{pg}',tofile=f'candidate-p{pg}'))
        else: output.append(f'pattern absent {pg}')
    (root/'independent-review'/f'{name}-sample-diff.txt').write_text('\n'.join(output),encoding='utf-8')
