"""显式无时间戳来源核验；不修改或替代 timestamp audit。

public manifest: {schema:untimed-source-v1, source_mode:untimed,
 sources:[{id:U1,text:relative.txt,text_sha256:...,pages:19,
 page_line_counts:{"1":45},redacted_lines:[{page:1,line:2,category:export_metadata}]}]}
text line: U1 p.01 L003: verbatim source line
note locator: `U1 p.01 L003–L010` (single line allowed)
"""
import argparse, hashlib, json, re, sys
from pathlib import Path

LOC=re.compile(r'(?P<id>U\d+) p\.(?P<page>\d{2,}) L(?P<start>\d{3,})(?:[–-]L(?P<end>\d{3,}))?')
ROW=re.compile(r'^(U\d+) p\.(\d{2,}) L(\d{3,}): ?(.*)$')
QUOTES=re.compile(r'(?<!\*)\*["“]([^"“”\n]+)["”]\*(?!\*)')
CLAIM=re.compile(r'教授(?:说|强调|明确|指出|认为|要求|提到|举例)|转录(?:提到|指出|显示|记载)(?!的)|课堂(?:上|中)(?:提到|讨论|给出|认为)')
PAGE_ONLY=re.compile(r'(U\d+) p\.(\d+)(?:[–-](\d+))?')

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def normalize(s): return re.findall(r"[a-z]+(?:'[a-z]+)?|\d+(?:[.,]\d+)*",s.casefold().replace('’',"'"))

def audit(note,manifest):
    errors=[]; stats={'locators':0,'quotes':0,'classroom_cells':0,'claims':0}
    mp=Path(manifest); meta=json.loads(mp.read_text(encoding='utf-8'))
    if meta.get('schema')!='untimed-source-v1' or meta.get('source_mode')!='untimed':
        return {'schema':'untimed-source-audit-v1','passed':False,'errors':['explicit untimed manifest required'],'stats':stats}
    sources={}
    for src in meta.get('sources',[]):
        ident=src['id']; rel=Path(src['text'])
        if ident in sources or not re.fullmatch(r'U\d+',ident): errors.append('invalid or duplicate source '+ident)
        if rel.is_absolute() or '..' in rel.parts: errors.append('source text must use portable relative path'); continue
        p=mp.parent/rel
        if digest(p)!=src['text_sha256']: errors.append('source hash changed: '+ident)
        pages={}; removed={(x['page'],x['line']) for x in src.get('redacted_lines',[])}
        counts=src.get('page_line_counts',{})
        if set(counts)!=set(str(i) for i in range(1,src['pages']+1)) or any(not isinstance(v,int) or v<1 for v in counts.values()):
            errors.append(ident+' missing/invalid original page line counts')
        for ln,row in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
            if not row.strip(): continue
            m=ROW.fullmatch(row)
            if not m: errors.append(f'{ident} malformed public text line {ln}'); continue
            sid,pg,num,txt=m.groups(); pg,num=int(pg),int(num)
            if sid!=ident or not 1<=pg<=src['pages'] or num<1: errors.append(f'{ident} invalid source coordinate line {ln}')
            pool=pages.setdefault(pg,{})
            if num in pool or (pg,num) in removed: errors.append(f'{ident} duplicate/redacted coordinate {pg}:{num}')
            pool[num]=txt
        if set(pages)!=set(range(1,src['pages']+1)): errors.append(ident+' missing physical page')
        for pg,rows in pages.items():
            expected=counts.get(str(pg),max(rows))
            if set(rows)|{num for page,num in removed if page==pg} != set(range(1,expected+1)):
                errors.append(f'{ident} original line extent changed on page {pg}')
            for num in range(1,expected+1):
                if num not in rows and (pg,num) not in removed: errors.append(f'{ident} unexplained omitted line {pg}:{num}')
        sources[ident]=(pages,removed)
    text=Path(note).read_text(encoding='utf-8'); lines=text.splitlines(); resolved={}
    for n,line in enumerate(lines,1):
        for m in LOC.finditer(line):
            stats['locators']+=1; ident=m['id']; pg=int(m['page']); a=int(m['start']); b=int(m['end'] or a)
            if ident not in sources or a>b or a<1: errors.append(f'note:{n} invalid/wrong source locator {m[0]}'); continue
            pages,removed=sources[ident]; pool=pages.get(pg,{})
            if not pool or b>max(pool) or not any(k in pool for k in range(a,b+1)) or any(k not in pool and (pg,k) not in removed for k in range(a,b+1)):
                errors.append(f'note:{n} out of range/redacted locator {m[0]}'); continue
            resolved.setdefault(n,[]).append(' '.join(pool[k] for k in range(a,b+1) if k in pool))
        # Malformed locators cannot silently escape the real locator enumerator.
        remnants=LOC.sub('',line)
        for coarse in PAGE_ONLY.finditer(remnants):
            ident,pg,last=coarse.groups(); pg=int(pg); last=int(last or pg)
            if ident not in sources or pg>last or any(x not in sources[ident][0] for x in range(pg,last+1)):
                errors.append(f'note:{n} invalid coarse page reference')
        # Titles and scope notes may name a physical page without claiming a line citation.
        # Such coarse references are never added to the resolved quote windows.
        remnants=PAGE_ONLY.sub('',remnants)
        if re.search(r'U\d+\s+p\.|U\d+\s+L\d',remnants): errors.append(f'note:{n} malformed locator')
    for n,line in enumerate(lines,1):
        quotes=QUOTES.findall(line)
        # English block quotes are source quotations too, even without italic markers.
        if re.match(r'^>\s*[A-Za-z"“]',line) and not quotes:
            q=LOC.sub('',re.sub(r'^>\s*','',line)).strip('"“” `（）() ')
            if len(normalize(q))>=4: quotes=[q]
        for q in quotes:
            stats['quotes']+=1
            windows=resolved.get(n,[])
            if not windows: errors.append(f'note:{n} quote missing same-line locator'); continue
            # Remove explicitly marked changes, preserve every remaining fragment in order.
            frags=[normalize(x) for x in re.split(r'\[[^\]]*\]|…|\.\.\.',q) if normalize(x)]
            matched=False
            for win in windows:
                pool=normalize(win); pos=0; good=True
                # Brackets mark editorial wording, never an automatic numeric exemption.
                numbers=re.findall(r'\d+(?:[.,]\d+)*',q)
                source_numbers=re.findall(r'\d+(?:[.,]\d+)*',win)
                if any(num not in source_numbers for num in numbers): continue
                for frag in frags:
                    found=next((i for i in range(pos,len(pool)-len(frag)+1) if pool[i:i+len(frag)]==frag),None)
                    if found is None: good=False; break
                    pos=found+len(frag)
                if good and frags: matched=True; break
            if not matched: errors.append(f'note:{n} quote/number differs from cited local source')
        claim=CLAIM.search(line)
        negated=claim and re.search(r'(?:不等于已确认|不能写成|不能当作|未确认)[“"\s]*$',line[:claim.start()])
        if claim and not negated:
            stats['claims']+=1
            if n not in resolved: errors.append(f'note:{n} classroom assertion missing same-line locator')
        if re.match(r'^\*\*🎙️\s*课堂(?:补充|实况|练习)',line):
            stats['classroom_cells']+=1
            end=n
            while end<len(lines) and not re.match(r'^#{2,6} |^\*\*(?:💡|⚠️|所以呢|🎙️)',lines[end]): end+=1
            if not any(k in resolved for k in range(n,end+1)): errors.append(f'note:{n} classroom cell missing locator')
    if not stats['locators']: errors.append('no source locators found')
    return {'schema':'untimed-source-audit-v1','passed':not errors,'errors':errors,'stats':stats,
            'note_sha256':digest(Path(note)),'manifest_sha256':digest(mp),
            'limits':['not a timed transcript audit','no audio/speaker verification','only prescribed italic or English block quotations are parsed; other attributions require substantive review','semantic attribution and complete source coverage require substantive review']}

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('note'); p.add_argument('--manifest',required=True); args=p.parse_args()
    try: result=audit(args.note,args.manifest)
    except (OSError,ValueError,KeyError,TypeError) as exc: result={'schema':'untimed-source-audit-v1','passed':False,'errors':[str(exc)]}
    print(json.dumps(result,ensure_ascii=False,indent=2)); sys.exit(0 if result['passed'] else 1)
