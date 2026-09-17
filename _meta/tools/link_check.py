# -*- coding: utf-8 -*-
"""
link_check.py — 全库链接检查（对抗自检清单第 9b 项），原 scratchpad/check9b.py 整理版。

用法（任意目录）：
    PYTHONIOENCODING=utf-8 /d/anaconda3/python.exe _meta/tools/link_check.py [vault根目录]
    省略参数时以本脚本所在位置推算 vault 根（_meta/tools/ 的上两级）。

查四类静默失效的链接（期望：除最后一行外无输出；有问题 exit 1）：
    ① 重名裸链接      [[术语表]] 这类五门课各有一份的文件名，没带目录
    ② 锚点失效        [[文件#锚点]] / [[#锚点]] 的锚点与目标文件的标题逐字比不上（GitHub 式 slug 一律失效）
    ③ Markdown 式锚点  [x](#slug) —— Obsidian 不认
    ④ 表格行里的双链别名竖线没转义（[[a|b]] 在表格里必须写 [[a\\|b]]）
    另：无锚点双链的目标文件是否存在
"""
import re, io, glob, os, collections, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
os.chdir(ROOT)
files = [f for f in glob.glob('**/*.md', recursive=True) if 'course_files_export' not in f]
byname = collections.defaultdict(list)
for f in files: byname[os.path.splitext(os.path.basename(f))[0]].append(f)
dups = {n for n, v in byname.items() if len(v) > 1}

def body(f):
    t = re.sub(r'```.*?```', '', io.open(f, encoding='utf-8').read(), flags=re.S)
    spans = [m.span() for m in re.finditer(r'`[^`\n]*`', t)]
    return t, spans
def in_code(pos, spans): return any(s <= pos < e for s, e in spans)
def clean(h): return re.sub(r'\s+', ' ', re.sub(r'[#|^\[\]`]', '', h)).strip()
HEADS = {}
def heads(tgt):
    if tgt not in HEADS:
        HEADS[tgt] = [clean(h) for h in re.findall(r'^#{1,6}\s+(.+?)\s*$', re.sub(r'```.*?```', '', io.open(tgt, encoding='utf-8').read(), flags=re.S), re.M)]
    return HEADS[tgt]

bad = 0
for f in files:
    t, spans = body(f)
    for m in re.finditer(r'\[\[([^\]\|#/]+)(#[^\]\|]*)?(\|[^\]]*)?\]\]', t):
        if in_code(m.start(), spans): continue
        name = m.group(1).strip()
        if name in dups and not os.path.exists(name + '.md'):
            print('重名裸链接', f, m.group(0)); bad += 1
    for m in re.finditer(r'\[\[([^\]\|#]*)#([^\]\|]+?)(\\)?(\|[^\]]*)?\]\]', t):
        if in_code(m.start(), spans): continue
        name = m.group(1).strip(); base = name.split('/')[-1]
        tgt = f if not name else (name + '.md' if os.path.exists(name + '.md') else (byname.get(base) or [None])[0])
        if not tgt: print('目标缺失', f, m.group(0)); bad += 1; continue
        anchor = clean(m.group(2).replace('\\|', ' |'))
        if anchor not in heads(tgt): print('锚点失效', f, m.group(0)); bad += 1
    for m in re.finditer(r'\[\[([^\]\|#]+)(\|[^\]]*)?\]\]', t):
        if in_code(m.start(), spans): continue
        name = m.group(1).strip().rstrip('\\'); base = name.split('/')[-1]
        if name.startswith('http') or re.search(r'\.(png|jpg|jpeg|svg|gif|pdf)$', name, re.I): continue
        if not (os.path.exists(name + '.md') or byname.get(base)):
            print('目标缺失(无锚点)', f, m.group(0)); bad += 1
    for m in re.finditer(r'\[[^\]]*\]\(#([^)]*)\)', t):
        if in_code(m.start(), spans): continue
        if clean(m.group(1)) not in heads(f): print('锚点失效(md)', f, m.group(0)); bad += 1
    for k, line in enumerate(io.open(f, encoding='utf-8').read().split('\n'), 1):
        if line.startswith('|') and '对抗自检清单' not in f:
            for m in re.finditer(r'\[\[[^\]]*?\|[^\]]*\]\]', line):
                if '\\|' not in m.group(0): print('表格双链别名未转义', f, k, m.group(0)); bad += 1
print('link_check 问题数:', bad, '（扫描文件数 %d）' % len(files))
sys.exit(1 if bad else 0)
