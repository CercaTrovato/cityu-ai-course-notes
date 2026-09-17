# -*- coding: utf-8 -*-
"""
integrity_check.py — 全库 Markdown 完整性快照与比对。任何 agent 任务**开工前 snapshot、收工后 verify**；发现问题停下报告，不许"凭记忆重建"。

用法（vault 根目录）：
    PYTHONIOENCODING=utf-8 /d/anaconda3/python.exe _meta/tools/integrity_check.py snapshot [标签]
        → 记录所有 .md（不含 course_files_export）的字节数 / 行数 / sha256 / 最后一个标题 到 _meta/tools/integrity_manifest.json
    PYTHONIOENCODING=utf-8 /d/anaconda3/python.exe _meta/tools/integrity_check.py verify [--allow <文件路径片段> ...]
        → 与最近一次快照比对：
             ✗ 任何文件 utf-8 解码失败
             ✗ 笔记（*/notes/*.md）最后一个标题不是 §9 / 变更记录 / 相关
             ✗ 文件缩短超过 20%（--allow 指定的路径除外——例如你本来就要整篇重写的那篇）
             △ 列出所有变动过的文件（供核对"我没打算改的文件为什么变了"）
        退出码：0 = 全部通过，1 = 有 ✗
    PYTHONIOENCODING=utf-8 /d/anaconda3/python.exe _meta/tools/integrity_check.py scan
        → 不比对快照，只查解码与结尾（随时可跑）
"""
import os, sys, io, re, json, glob, hashlib, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
MANIFEST = os.path.join(ROOT, '_meta', 'tools', 'integrity_manifest.json')

def files():
    out = []
    for f in glob.glob(os.path.join(ROOT, '**', '*.md'), recursive=True):
        rel = os.path.relpath(f, ROOT).replace('\\', '/')
        if 'course_files_export' in rel or rel.startswith('.obsidian/'): continue
        out.append(rel)
    return sorted(out)

def info(rel):
    b = open(os.path.join(ROOT, rel), 'rb').read()
    d = {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()[:16]}
    try:
        t = b.decode('utf-8'); d['utf8'] = True; d['lines'] = t.count('\n') + 1
        heads = re.findall(r'^#{2,4} .*$', t, re.M); d['last_head'] = heads[-1][:60] if heads else ''
    except UnicodeDecodeError as e:
        d['utf8'] = False; d['lines'] = 0; d['last_head'] = ''; d['err_at'] = e.start
    return d

def tail_ok(rel, d):
    if '/notes/' not in rel: return True
    h = d['last_head']
    return h.startswith('## 相关') or '9.' in h or '变更' in h

def snapshot(tag=''):
    m = {'time': datetime.datetime.now().isoformat(timespec='seconds'), 'tag': tag, 'files': {r: info(r) for r in files()}}
    io.open(MANIFEST, 'w', encoding='utf-8', newline='\n').write(json.dumps(m, ensure_ascii=False, indent=1))
    print('snapshot: %d 个文件，%s，标签「%s」→ %s' % (len(m['files']), m['time'], tag, os.path.relpath(MANIFEST, ROOT)))

def scan():
    bad = 0
    for r in files():
        d = info(r)
        if not d['utf8']: print('✗ utf-8 断裂', r, '字节', d.get('err_at')); bad += 1
        elif not tail_ok(r, d): print('✗ 结尾异常', r, '最后标题：', d['last_head'], '|', d['bytes'], '字节'); bad += 1
    print('scan：%d 个文件，问题 %d' % (len(files()), bad))
    return bad == 0

def verify(allow):
    if not os.path.exists(MANIFEST): print('没有快照，先跑 snapshot'); return False
    m = json.load(io.open(MANIFEST, encoding='utf-8'))
    old = m['files']; bad = 0; changed = []
    for r in files():
        d = info(r)
        if not d['utf8']: print('✗ utf-8 断裂', r); bad += 1; continue
        if not tail_ok(r, d): print('✗ 结尾异常', r, '最后标题：', d['last_head']); bad += 1
        o = old.get(r)
        if o is None: changed.append(('新增', r, d['bytes'])); continue
        if o['sha256'] != d['sha256']:
            changed.append(('改动', r, '%d → %d 字节' % (o['bytes'], d['bytes'])))
            if d['bytes'] < o['bytes'] * 0.8 and not any(a in r for a in allow):
                print('✗ 缩短超过 20%%：%s  %d → %d 字节（若是有意重写，用 --allow）' % (r, o['bytes'], d['bytes'])); bad += 1
    for r in old:
        if r not in set(files()): changed.append(('删除', r, old[r]['bytes']))
    print('--- 相对快照「%s」（%s）的变动 %d 处：' % (m.get('tag', ''), m['time'], len(changed)))
    for c in changed: print('   △', *c)
    print('verify：问题 %d' % bad)
    return bad == 0

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(2)
    if a[0] == 'snapshot': snapshot(' '.join(a[1:])); sys.exit(0)
    if a[0] == 'scan': sys.exit(0 if scan() else 1)
    if a[0] == 'verify':
        allow = []
        if '--allow' in a: allow = a[a.index('--allow') + 1:]
        sys.exit(0 if verify(allow) else 1)
    print(__doc__); sys.exit(2)
