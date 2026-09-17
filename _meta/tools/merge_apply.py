# -*- coding: utf-8 -*-
"""
merge_apply.py — 转录融合「分片模式」的合并器：收齐各分片的 patch.json / findings.json，在副本上应用、渲染结构块、
跑验收；通过后**一次** atomic_write 进 vault。分片代理不写 vault，主代理只跑这一条命令。
配合 .claude/skills/transcript-merge/SKILL.md §「分片并行模式」与 reference/formats.md §10（patch / findings 格式）。

用法（vault 根）：
    PYTHONIOENCODING=utf-8 /d/anaconda3/python.exe _meta/tools/merge_apply.py <工作目录> --note <笔记相对路径> --transcript <转录…> [--pages N] [--dry-run] [--partial] [--src <原稿副本>]
        --partial：分片自验（只含自己的 shard_k）——隐含 --dry-run，A1/A2/A3/A6/A7/A8/A9/A11 的 FAIL 不计（那是别的分片 / 主代理的事），A4/A5/A13/A14 与 note_quality 必须过
    PYTHONIOENCODING=utf-8 /d/anaconda3/python.exe _meta/tools/merge_apply.py extract <笔记相对路径> <输出 patch.json>     # 把已合并笔记的 🎙️ 格与 §8 覆盖列导成 patch（回放 / 自测用）

工作目录结构：
    <工作目录>/shard_*/patch.json      分片的 🎙️ 格与 §8 覆盖列（整格替换，按小节标题定位）
    <工作目录>/shard_*/findings.json   分片的结构化发现（🔴 行、§9.x 行、时间分配、元文件追加行……）
    <工作目录>/main.json               主代理的补充：replacements（任意精确替换）、merge_row（§9.6）、head（文首提示块）
    <工作目录>/merged.md               输出：应用后的副本（--dry-run 只到这里）
    <工作目录>/merge_report.txt        输出：验收结果

退出码：0 = 副本通过验收（非 dry-run 时已写入 vault）；1 = 有 FAIL，未写入。
"""
import os, sys, io, re, json, glob, shutil, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from safe_write import atomic_write
PY = sys.executable
LABEL = re.compile(r'^(\*\*(⚠️|💡|📄|🔗|🧪|所以呢|🎯|📌|📝|🔴|🟡|⚪|🎙️)|#{2,6} |---|\*\*[^*]{1,12}\*\*$)')
CELL = re.compile(r'^\*\*🎙️ ?课堂(补充|实况|练习)')

def die(msg): print('✗', msg); sys.exit(1)

# ------------------------------------------------------------------ 定位工具
def find_heading(lines, heading):
    """heading 可以是完整标题行，或 '#### 2.4.3' 这样的前缀；必须唯一。"""
    h = heading.strip()
    hits = [i for i, l in enumerate(lines) if l.strip() == h or re.match(re.escape(h) + r'[ .（]', l)]
    if len(hits) != 1: die('小节标题定位到 %d 处（需唯一）：%s' % (len(hits), heading))
    return hits[0]

def section_range(lines, start):
    lvl = len(lines[start]) - len(lines[start].lstrip('#'))
    j = start + 1
    while j < len(lines) and not (lines[j].startswith('#') and (len(lines[j]) - len(lines[j].lstrip('#'))) <= lvl): j += 1
    return start, j

def own_range(lines, start):
    """标题直属的正文范围：到下一个任意级别的标题为止（不含子小节）。"""
    j = start + 1
    while j < len(lines) and not re.match(r'^#{1,6} ', lines[j]): j += 1
    return start, j

def cell_range(lines, a, b):
    """小节 [a,b) 内唯一的 🎙️ 格：从 **🎙️ 课堂补充** 行到下一个格标签 / 标题 / --- 之前（保留其后的空行归下一格）。"""
    starts = [i for i in range(a, b) if CELL.match(lines[i])]
    if len(starts) != 1: return None
    i = starts[0]; j = i + 1
    while j < b and not LABEL.match(lines[j]): j += 1
    while j - 1 > i and lines[j - 1].strip() == '': j -= 1        # 结尾空行不算格内容
    return i, j

def apply_cells(lines, cells, log):
    for c in cells:
        i = find_heading(lines, c['section']); a, b = own_range(lines, i)
        r = cell_range(lines, a, b)
        if not r: die('小节内 🎙️ 格不是恰好 1 个：%s' % c['section'])
        block = c['block'].rstrip('\n').split('\n')
        if not CELL.match(block[0]): die('patch block 必须以 **🎙️ 课堂补充** 开头：%s' % c['section'])
        lines[r[0]:r[1]] = block; log.append('格 %s：%d 行 → %d 行' % (c['section'][:40], r[1] - r[0], len(block)))
    return lines

def apply_s8(lines, rows, log):
    s8 = find_heading(lines, '## 8'); a, b = section_range(lines, s8)
    hdr = next((i for i in range(a, b) if lines[i].startswith('|') and '课堂覆盖' in lines[i]), None)
    if hdr is None: die('§8 没有带「课堂覆盖」列的表')
    ci = [c.strip() for c in lines[hdr].strip().strip('|').split('|')].index(next(c for c in [x.strip() for x in lines[hdr].strip().strip('|').split('|')] if '课堂覆盖' in c))
    for r in rows:
        key = r['page'].strip()
        idx = [i for i in range(hdr + 2, b) if lines[i].startswith('|') and re.match(r'^\|\s*\**%s\**\s*\|' % re.escape(key), lines[i])]
        if len(idx) != 1: die('§8 行定位到 %d 处：%s' % (len(idx), key))
        cells = [c.strip() for c in lines[idx[0]].strip().strip('|').split('|')]
        while len(cells) <= ci: cells.append('')
        cells[ci] = r['coverage']
        lines[idx[0]] = '| ' + ' | '.join(cells) + ' |'
    log.append('§8 覆盖列：%d 行' % len(rows))
    return lines

# ------------------------------------------------------------------ 渲染 findings
def sub_range(lines, num):
    i = next((k for k, l in enumerate(lines) if re.match(r'^### %s\b' % re.escape(num), l)), None)
    if i is None: return None
    j = i + 1
    while j < len(lines) and not lines[j].startswith('##'): j += 1
    return i, j

def last_table_end(lines, a, b):
    """[a,b) 内最后一张表的结束行（不含）；没有表返回 None。"""
    end = None; i = a
    while i < b:
        if lines[i].startswith('|'):
            j = i
            while j < b and lines[j].startswith('|'): j += 1
            end = j; i = j
        else: i += 1
    return end

def append_rows(lines, num, rows, header, placeholder_re, log):
    """往 §num 的表追加行；若该节还是"无转录"占位，就用 header 新建表替换占位段落。"""
    if not rows: return lines
    r = sub_range(lines, num)
    if r is None: die('找不到 §%s' % num)
    a, b = r; body = '\n'.join(lines[a + 1:b])
    if placeholder_re and re.search(placeholder_re, body):
        keep = [l for l in lines[a + 1:b] if l.startswith('>') and '转录到手后' not in l]   # 保留与转录无关的引用块（通常没有）
        new = [''] + header + rows + ['']
        lines[a + 1:b] = new; log.append('§%s：替换占位 → 新表 %d 行' % (num, len(rows)))
        return lines
    end = last_table_end(lines, a, b)
    if end is None:
        lines[b:b] = [''] + header + rows + ['']; log.append('§%s：新建表 %d 行' % (num, len(rows)))
    else:
        lines[end:end] = rows; log.append('§%s：追加 %d 行' % (num, len(rows)))
    return lines

def renumber(rows, start=1):
    out = []
    for k, r in enumerate(rows, start):
        cells = r.strip().strip('|').split('|')
        if cells and cells[0].strip().isdigit(): cells[0] = ' %d ' % k
        out.append('|' + '|'.join(cells) + '|')
    return out

def render(lines, F, main, log):
    today = main.get('date') or datetime.date.today().isoformat()
    # frontmatter
    fm_end = next((i for i in range(1, min(40, len(lines))) if lines[i].strip() == '---'), None)
    if fm_end is None: die('没有 frontmatter')
    fm = lines[:fm_end]
    def setfm(k, v):
        for i, l in enumerate(fm):
            if l.startswith(k + ':'): fm[i] = '%s: %s' % (k, v); return
        fm.append('%s: %s' % (k, v))
    setfm('transcript', 'merged'); setfm('status', 'v1.0'); setfm('updated', today)
    lines[:fm_end] = fm
    # §0 课堂实况
    if F.get('class_summary'):
        r = sub_range(lines, '0.') or None
        s0 = find_heading(lines, '## 0'); a, b = section_range(lines, s0)
        blk = ['', '> 🎙️ **课堂实况**（%s）：%s' % (main.get('class_date', today), ' '.join(F['class_summary'])), '']
        lines[b:b] = blk; log.append('§0：课堂实况块')
    # §6.2 🔴 行：插在第一条非 🔴 行之前（🔴 在表首）
    if F.get('red'):
        r = sub_range(lines, '6.2'); a, b = r
        end = last_table_end(lines, a, b)
        if end is None: die('§6.2 没有表')
        hdr = next(i for i in range(a, b) if lines[i].startswith('|'))
        first_non_red = next((i for i in range(hdr + 2, end) if not lines[i].startswith('| 🔴')), end)
        lines[first_non_red:first_non_red] = F['red']; log.append('§6.2：🔴 %d 行' % len(F['red']))
    # §8 时间分配表
    if F.get('time_alloc'):
        s8 = find_heading(lines, '## 8'); a, b = section_range(lines, s8)
        tot = sum(float(x['min']) for x in F['time_alloc']) or 1
        rows = ['| %s | %s | ~%.1f min | %.1f%% |' % (x['label'], x['range'], float(x['min']), 100 * float(x['min']) / tot) for x in F['time_alloc']]
        blk = ['', '**课堂时间分配**（%s，按时间戳）：' % main.get('span', '按转录'), '', '| 内容块 | 时间戳 | 用时 | 占比 |', '|---|---|---|---|'] + rows + ['']
        while b > a and lines[b - 1].strip() in ('', '---'): b -= 1
        lines[b:b] = blk; log.append('§8：时间分配表 %d 行' % len(rows))
    # §9.1 / 9.2 / 9.5
    lines = append_rows(lines, '9.1', F.get('s91', []), ['| 讲义页 | 内容 | 课上处理 | 笔记处理 |', '|---|---|---|---|'], r'无转录', log)
    lines = append_rows(lines, '9.2', renumber(F.get('s92', [])), ['| # | 内容 | 时长 | 时间戳 | 小节 | 为什么值钱 |', '|---|---|---|---|---|---|'], r'无转录', log)
    if F.get('s95'):
        r = sub_range(lines, '9.5'); a, b = r; existing = [l for l in lines[a:b] if re.match(r'^\|\s*\d+\s*\|', l)]
        lines = append_rows(lines, '9.5', renumber(F['s95'], len(existing) + 1), ['| # | 事项 | 说明 |', '|---|---|---|'], None, log)
    # §9.6
    row = main.get('merge_row')
    if row:
        r = sub_range(lines, '9.6') or sub_range(lines, '9.7'); a, b = r
        end = last_table_end(lines, a, b)
        if end is None: die('§9.6 没有表')
        lines[end:end] = [row if row.startswith('|') else '| %s | %s |' % (today, row)]; log.append('§9.6：合并行')
    # 主代理的任意精确替换（文首提示块、§6.1 计数等）
    text = '\n'.join(lines)
    for rp in main.get('replacements', []):
        if text.count(rp['old']) != 1: die('replacements 定位到 %d 处：%s' % (text.count(rp['old']), rp['old'][:60]))
        text = text.replace(rp['old'], rp['new'])
    if main.get('replacements'): log.append('replacements：%d 处' % len(main['replacements']))
    return text.split('\n')

# ------------------------------------------------------------------ 元文件追加
META_TARGETS = {   # findings 键 → (文件相对课程 _meta 的路径 或 vault 相对路径, 块标题, 表头)
    'kb_rows':     ('_meta/考点库.md',        '🔴 教授明示（转录追加）', ['| 可信度 | # | 考点 | 依据 | 对应小节 |', '|---|---|---|---|---|']),
    'ddl_rows':    ('_meta/作业与DDL.md',     '课堂口头信息（转录追加）', ['| 事项 | 内容 | 来源 |', '|---|---|---|']),
    'term_rows':   ('_meta/术语表.md',        '课堂口头术语 / 例子（转录追加）', ['| 中文 | English | 课上说法 | 出处 |', '|---|---|---|---|']),
    'ledger_rows': ('_meta/知识层级台账.md',  '来源回填（转录追加）', ['| 概念 | 来源 | 出处 |', '|---|---|---|']),
    'cross_rows':  ('_meta/待并入术语总表.md', '跨课有价值的条目（转录追加）', ['| 优先级 | 中文 | English | 一句话定义 | 首现 | 可能冲突的课 |', '|---|---|---|---|---|---|']),
    'asr_rows':    ('.claude/skills/transcript-merge/reference/asr-dictionary.md', None, None),
}

def meta_blocks(F, course_dir, module, today):
    out = {}
    for key, (rel, title, header) in META_TARGETS.items():
        rows = F.get(key) or []
        if not rows: continue
        path = os.path.join(ROOT, rel) if rel.startswith('.claude') else os.path.join(course_dir, rel)
        if title is None:                       # asr-dictionary：直接追加行（表在文件末尾）
            out[path] = '\n'.join(rows) + '\n'
        else:
            out[path] = '\n\n## 🎙️ %s 转录追加（%s）· %s\n\n' % (module, today, title) + '\n'.join(header + rows) + '\n'
    return out

# ------------------------------------------------------------------ 验收
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    return r.returncode, (r.stdout or '') + (r.stderr or '')

PARTIAL_OK = ('A1 ', 'A2 ', 'A3 ', 'A6 ', 'A7 ', 'A8 ', 'A9 ', 'A11 ')   # 分片自验时允许的 FAIL（其它分片 / 主代理负责的部分）

def verify(merged, transcripts, pages, strict, baseline_L, partial=False):
    rc1, out1 = run([PY, os.path.join(HERE, 'transcript_check.py'), 'audit', merged, '--transcript'] + transcripts)
    if partial and rc1 != 0:
        left = [l for l in out1.splitlines() if l.strip().startswith('✗') and not any(c in l for c in PARTIAL_OK)]
        rc1 = 1 if left else 0
    cmd = [PY, os.path.join(HERE, 'note_quality.py'), merged, '--pages', str(pages)] + (['--strict'] if strict else [])
    rc2, out2 = run(cmd)
    L = re.search(r'L 合规问题 (\d+) 条', out2); L = int(L.group(1)) if L else 0
    ok2 = ('【判定】 PASS' in out2) if strict else (L <= baseline_L)
    return rc1 == 0, ok2, out1, out2, L

# ------------------------------------------------------------------ extract（回放 / 自测）
def extract(note_rel, out):
    lines = io.open(os.path.join(ROOT, note_rel), encoding='utf-8').read().split('\n')
    cells = []; cur_head = None
    for i, l in enumerate(lines):
        if re.match(r'^#{2,5} ', l): cur_head = l.strip()
        if CELL.match(l) and cur_head and cur_head.startswith('###'):
            a, b = own_range(lines, find_heading(lines, cur_head)); r = cell_range(lines, a, b)
            if r and r[0] == i: cells.append({'section': cur_head, 'block': '\n'.join(lines[r[0]:r[1]])})
    s8 = find_heading(lines, '## 8'); a, b = section_range(lines, s8); rows = []
    hdr = next((i for i in range(a, b) if lines[i].startswith('|') and '课堂覆盖' in lines[i]), None)
    if hdr is not None:
        cols = [c.strip() for c in lines[hdr].strip().strip('|').split('|')]; ci = next(k for k, c in enumerate(cols) if '课堂覆盖' in c)
        for i in range(hdr + 2, b):
            if not lines[i].startswith('|'): break
            cs = [c.strip() for c in lines[i].strip().strip('|').split('|')]
            m = re.match(r'\**(p\.[\d–\-]+)\**', cs[0])
            if m and len(cs) > ci: rows.append({'page': m.group(1), 'coverage': cs[ci]})
    io.open(out, 'w', encoding='utf-8', newline='\n').write(json.dumps({'note': note_rel, 'cells': cells, 's8': rows}, ensure_ascii=False, indent=1))
    print('extract：%d 个 🎙️ 格，%d 行 §8 覆盖列 → %s' % (len(cells), len(rows), out))

# ------------------------------------------------------------------ main
def main():
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(2)
    if a[0] == 'extract': extract(a[1], a[2]); return
    work = os.path.abspath(a[0]); dry = '--dry-run' in a; partial = '--partial' in a
    if partial: dry = True
    def opt(k, d=None):
        return a[a.index(k) + 1] if k in a else d
    note_rel = opt('--note'); pages = int(opt('--pages', 0) or 0)
    transcripts = []
    if '--transcript' in a:
        k = a.index('--transcript') + 1
        while k < len(a) and not a[k].startswith('--'): transcripts.append(a[k]); k += 1
    if not (note_rel and transcripts): die('需要 --note 与 --transcript')
    src = os.path.join(ROOT, note_rel); course_dir = os.path.dirname(os.path.dirname(src))
    src_read = opt('--src', src)          # 回放 / 自测：从别的文件读原稿，写入目标仍是 --note
    module = re.match(r'([MT]\d+)', os.path.basename(note_rel)).group(1)
    text0 = io.open(src_read, encoding='utf-8').read()
    strict = bool(re.search(r'^quality_spec:\s*v1', text0[:800], re.M))
    if not pages:
        m = re.search(r'（(\d+) 页）', text0[:800]); pages = int(m.group(1)) if m else die('给 --pages')
    # 基线（legacy 模式看 L 数不变差）
    baseline_L = 0
    if not strict:
        _, out = run([PY, os.path.join(HERE, 'note_quality.py'), src_read, '--pages', str(pages)])
        m = re.search(r'L 合规问题 (\d+) 条', out); baseline_L = int(m.group(1)) if m else 0
    # 收集分片
    shards = sorted(glob.glob(os.path.join(work, 'shard_*')))
    if not shards: die('工作目录下没有 shard_* 子目录')
    F = {}; cells = []; s8 = []; log = []
    for sd in shards:
        p = os.path.join(sd, 'patch.json')
        if os.path.exists(p):
            P = json.load(io.open(p, encoding='utf-8')); cells += P.get('cells', []); s8 += P.get('s8', [])
        f = os.path.join(sd, 'findings.json')
        if os.path.exists(f):
            for k, v in json.load(io.open(f, encoding='utf-8')).items():
                if isinstance(v, list): F.setdefault(k, []).extend(v)
                else: F[k] = v
    mp = os.path.join(work, 'main.json'); main_ = json.load(io.open(mp, encoding='utf-8')) if os.path.exists(mp) else {}
    # 应用
    lines = text0.split('\n')
    lines = apply_cells(lines, cells, log)
    if s8: lines = apply_s8(lines, s8, log)
    lines = render(lines, F, main_, log)
    merged = os.path.join(work, 'merged.md')
    io.open(merged, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    today = main_.get('date') or datetime.date.today().isoformat()
    blocks = meta_blocks(F, course_dir, module, today)
    # 验收
    ok1, ok2, out1, out2, L = verify(merged, transcripts, pages, strict, baseline_L, partial)
    rep = ['merge_apply %s  %s%s' % (datetime.datetime.now().isoformat(timespec='seconds'), note_rel, '  [partial：分片自验，A1/2/3/6/7/8/9/11 的 FAIL 不计]' if partial else ''), '分片 %d 个，🎙️ 格 %d，§8 行 %d' % (len(shards), len(cells), len(s8))] + ['  · ' + l for l in log] + \
          ['', '--- transcript_check audit', out1.strip(), '', '--- note_quality %s' % ('strict' if strict else 'legacy（基线 L=%d）' % baseline_L), out2.strip()[-1500:],
           '', '元文件追加：' + (', '.join(os.path.relpath(p, ROOT) for p in blocks) if blocks else '无'),
           '', '【结果】 audit %s · note_quality %s%s' % ('PASS' if ok1 else 'FAIL', 'PASS' if ok2 else 'FAIL', '' if strict else '（L=%d）' % L)]
    io.open(os.path.join(work, 'merge_report.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(rep))
    print('\n'.join(rep[:2 + len(log)])); print('   audit: %s   note_quality: %s%s' % ('PASS' if ok1 else 'FAIL', 'PASS' if ok2 else 'FAIL', '' if strict else '（L=%d，基线 %d）' % (L, baseline_L)))
    if not ok1: print(out1.strip()[-1200:])
    if not ok2: print(out2.strip()[-1200:])
    print('   报告：', os.path.join(work, 'merge_report.txt'))
    if not (ok1 and ok2): sys.exit(1)
    if dry: print('   --dry-run：未写入 vault（副本在 %s）' % merged); return
    n = atomic_write(src, '\n'.join(lines)); print('   ✓ 写入', note_rel, n, '字节')
    for path, blk in blocks.items():
        old = io.open(path, encoding='utf-8').read() if os.path.exists(path) else ''
        atomic_write(path, old.rstrip('\n') + '\n' + blk, min_ratio=0.0); print('   ✓ 追加', os.path.relpath(path, ROOT))

if __name__ == '__main__':
    main()
