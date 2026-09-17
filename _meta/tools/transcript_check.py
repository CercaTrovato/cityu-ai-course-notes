# -*- coding: utf-8 -*-
"""
transcript_check.py — 转录融合的机器验收（配合 .claude/skills/transcript-merge/SKILL.md 使用）。

用法（在 vault 根目录）：
    PYTHONIOENCODING=utf-8 /d/anaconda3/python.exe _meta/tools/transcript_check.py scan  <转录.txt> [<part2.txt> ...]
    PYTHONIOENCODING=utf-8 /d/anaconda3/python.exe _meta/tools/transcript_check.py audit <笔记.md> --transcript <转录.txt> [<更多转录.txt> ...] [--json] [--no-red]

scan  ：融合前跑。解析时间戳 → 段数、起止、时长、时序倒退、≥120 秒空档（附前后原文）、
        首尾各 3 段原文（判断"内容上"是否缺开头/缺结尾——脚本判断不了，必须人读）、
        考试/作业/行政信号词命中清单（带时间戳，供 §9.2 / 考点库 / 作业与DDL 用）。
audit ：融合后跑。逐项检查笔记是否达到 AC6761 M02 v1.0 的融合形态：
        A1  frontmatter transcript: merged 且 status: v1.0
        A2  「待转录补充」计数 = 0
        A3  每个「🎙️ 课堂补充」格：含时间戳，或 ❓/⏭️ 标记 + ≥20 字理由
        A4  笔记里出现的每个 `时间戳` 都能在转录里找到对应段（防编造）
        A5  带时间戳/🎙️ 行里的斜体英文引文 *"..."* 能在转录里模糊匹配到（<40% FAIL，40–60% WARN；防编造原话）
        A6  §8 表「课堂覆盖」列：非封面/分隔页行不得为空或 —
        A7  §9.1、§9.2 有表且 §9.2 ≥3 行带时间戳；§9.5 含「反方视角」
        A8  §6.2 至少 1 条 🔴 且带时间戳与引文（转录里确实没有任何考试信号时加 --no-red 降为 WARN）
        A9  §0 有 🎙️ 课堂实况块；文首提示块提到 merged（WARN）
        A10 出现"教授说/教授强调/教授明确…"的行没有时间戳（WARN，列出行号）
        A11 §9.6（或 9.7）变更记录有本次合并行（含"转录"二字）
        A12 §8 里所有 `a`–`b` 区间的并集覆盖录音时长的比例 ≥ 75%（WARN；低于此值说明没有全程对齐）
        FAIL = 任一 A1–A8、A11 不过；WARN 不影响判定，但要在 §9.5 说明或修掉。
时间戳写法：`MM:SS`（<1h）或 `HH:MM:SS`，必须加反引号；多段录音写 `part2 12:34`，脚本按 --transcript 文件名里的 partN 分别查。
引文写法：*"原话"*（斜体+直引号）；对 ASR 的改写/补词放在方括号 [ ] 里，脚本会跳过方括号只核对原文部分。
"""
import re, io, sys, os, json

TS = re.compile(r'(?<![\d:])(\d{1,2}):(\d{2})(?::(\d{2}))?(?![\d:])')
CJK = re.compile(r'[一-鿿]')
SIGNAL = ['exam', 'midterm', 'final', 'quiz', 'test', 'assignment', 'homework', 'submit', 'canvas', 'deadline',
          'due', 'group', 'presentation', 'project', 'remember', 'important', 'careful', 'memorize', 'mark',
          'grade', 'score', 'next week', 'break', 'skip', "don't have to", 'do not have to', 'not required',
          'upload', 'email', 'by yourself', 'practice', 'exercise']

def to_sec(h, m, s):
    if s is None:  # MM:SS
        return int(h) * 60 + int(m)
    return int(h) * 3600 + int(m) * 60 + int(s)

def fmt(sec):
    h, r = divmod(sec, 3600); m, s = divmod(r, 60)
    return '%d:%02d:%02d' % (h, m, s) if h else '%02d:%02d' % (m, s)

def parse_transcript(path):
    """返回 [(sec, ts_str, text)]，按文件顺序。兼容 Notta 导出：时间戳单独一行，下一行为文本。"""
    lines = io.open(path, encoding='utf-8').read().splitlines()
    segs = []; cur = None
    for ln in lines:
        s = ln.strip()
        m = re.fullmatch(r'(\d{1,2}):(\d{2})(?::(\d{2}))?', s)
        if m:
            if cur: segs.append(cur)
            cur = [to_sec(*m.groups()), s, '']
        elif cur is not None and s:
            cur[2] += (' ' if cur[2] else '') + s
    if cur: segs.append(cur)
    return [tuple(x) for x in segs]

FILLERS = {'um', 'uh', 'er', 'ah', 'hmm', 'mm', 'mhm', 'eh'}
def words(t):
    return [w for w in re.findall(r"[a-z0-9]+", t.lower().replace("'", '')) if w not in FILLERS]

# ---------------------------------------------------------------- scan
def scan(paths):
    total_segs = 0; total_dur = 0
    for p in paths:
        segs = parse_transcript(p)
        if not segs:
            print('!! 没有解析到任何时间戳段：', p); continue
        print('=' * 90); print('文件:', p); print('段数:', len(segs), ' 起:', segs[0][1], ' 止:', segs[-1][1],
              ' 时长(按时间戳):', fmt(segs[-1][0] - segs[0][0]), ' 大小:', os.path.getsize(p), 'B')
        total_segs += len(segs); total_dur += segs[-1][0] - segs[0][0]
        back = [(a[1], b[1]) for a, b in zip(segs, segs[1:]) if b[0] < a[0]]
        print('时序倒退:', back if back else '无')
        gaps = [(a, b) for a, b in zip(segs, segs[1:]) if b[0] - a[0] >= 120]
        print('≥120 秒空档: %d 处' % len(gaps))
        for a, b in gaps:
            print('   %s → %s (%s)' % (a[1], b[1], fmt(b[0] - a[0])))
            print('      前: ' + a[2][:160]); print('      后: ' + b[2][:160])
        print('-- 首 3 段（判断是否缺开头：第一句应是问候/议程/上节回顾，若已在讲课中段 = 缺开头）')
        for s in segs[:3]: print('   %s  %s' % (s[1], s[2][:200]))
        print('-- 末 3 段（判断是否缺结尾：应有下课语/布置作业；若是半句或噪声 = 缺结尾）')
        for s in segs[-3:]: print('   %s  %s' % (s[1], s[2][:200]))
        print('-- 信号词命中（供 §9.2 / 考点库 / 作业与DDL；每词最多列 12 处）')
        for kw in SIGNAL:
            pat = re.compile(r'\b' + re.escape(kw) + r'\b'); hits = [s for s in segs if pat.search(s[2].lower())]
            if hits:
                print('   %-16s %2d 处: %s' % (kw, len(hits), ', '.join(h[1] for h in hits[:12]) + (' …' if len(hits) > 12 else '')))
    if len(paths) > 1:
        print('=' * 90); print('合计段数 %d，合计时长 %s（各段各自从 0 计时，接缝需按内容判断）' % (total_segs, fmt(total_dur)))

# ---------------------------------------------------------------- audit
def section(text, num):
    """返回 '## N.' 一节的正文（到下一个 '## ' 为止）。"""
    m = re.search(r'^## %s\..*?$' % num, text, re.M)
    if not m: return ''
    rest = text[m.end():]
    n = re.search(r'^## ', rest, re.M)
    return rest[:n.start()] if n else rest

def subsection(text, num):
    m = re.search(r'^### %s\b.*?$' % re.escape(num), text, re.M)
    if not m: return ''
    rest = text[m.end():]
    n = re.search(r'^##', rest, re.M)
    return rest[:n.start()] if n else rest

def tables(block):
    """把一节里的多张表分开（连续的 | 行为一张表）；每张表是 [行→单元格列表]，不含分隔行。"""
    out = []; cur = []
    for ln in block.splitlines():
        if ln.startswith('|'):
            if not re.match(r'^\|\s*-', ln): cur.append([c.strip() for c in ln.strip().strip('|').split('|')])
        elif cur:
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out

def table_rows(block):
    return [r for tb in tables(block) for r in tb]

def audit(note, tpaths, want_json=False, no_red=False):
    text = io.open(note, encoding='utf-8').read()
    body = re.sub(r'```.*?```', '', text, flags=re.S)
    # 行号按原文件报；围栏代码内的行置空，不参与逐行检查
    lines = []; fence = False
    for ln in text.splitlines():
        if ln.strip().startswith('```'): fence = not fence; lines.append(''); continue
        lines.append('' if fence else ln)
    fails = []; warns = []; info = {}

    # 转录：时间戳集合 + 词序列
    ts_all = set(); ts_part = {}; twords = []; span = 0
    for p in tpaths:
        segs = parse_transcript(p)
        secs = {s[0] for s in segs}
        if segs and p == tpaths[0]: span = segs[-1][0] - segs[0][0]   # 只按第一份（本讲）转录算时长
        ts_all |= secs
        mp = re.search(r'part(\d+)', os.path.basename(p))
        if mp: ts_part[int(mp.group(1))] = secs
        twords += [w for s in segs for w in words(s[2])]
    shingles = set(zip(twords, twords[1:], twords[2:]))
    bigrams = set(zip(twords, twords[1:]))
    info['transcript_segments'] = len(ts_all)

    # A1
    fm = re.match(r'^---\n(.*?)\n---', text, re.S)
    fmt_ = fm.group(1) if fm else ''
    if not re.search(r'^transcript:\s*merged', fmt_, re.M): fails.append('A1 frontmatter transcript 不是 merged')
    if not re.search(r'^status:\s*v1\.0', fmt_, re.M): fails.append('A1 frontmatter status 不是 v1.0')

    # A2
    n_pending = len(re.findall(r'待转录补充', body))
    info['待转录补充'] = n_pending
    if n_pending: fails.append('A2 仍有 %d 处「待转录补充」' % n_pending)

    # A3 🎙️ 格
    cell_starts = [i for i, ln in enumerate(lines) if re.match(r'^\*\*🎙️ ?课堂(补充|实况|练习)|^🎙️ \*\*课堂', ln)]
    LABEL = re.compile(r'^(\*\*(⚠️|💡|📄|🔗|🧪|所以呢|🎯|📌|📝|🔴|🟡|⚪|🎙️)|#{2,6} |---|\*\*[^*]{1,12}\*\*$)')
    bad_cells = []
    for i in cell_starts:
        j = i + 1
        while j < len(lines) and not LABEL.match(lines[j]): j += 1
        blk = '\n'.join(lines[i:j])
        has_ts = bool(TS.search(blk)); has_mark = ('❓' in blk or '⏭️' in blk) and len(CJK.findall(blk)) >= 20
        if not (has_ts or has_mark): bad_cells.append(i + 1)
    info['🎙️_cells'] = len(cell_starts)
    if bad_cells: fails.append('A3 %d 个 🎙️ 格既无时间戳也无 ❓/⏭️+理由（行 %s）' % (len(bad_cells), bad_cells[:15]))
    if not cell_starts: fails.append('A3 没找到任何「**🎙️ 课堂补充**」格')

    # A4 时间戳可回溯
    unmatched = []; n_ts = 0
    for i, ln in enumerate(lines):
        for m in re.finditer(r'`(?:part(\d+) )?(\d{1,2}):(\d{2})(?::(\d{2}))?`', ln):
            n_ts += 1
            part, h, mm, s = m.groups(); sec = to_sec(h, mm, s)
            pool = ts_part.get(int(part), ts_all) if part else ts_all
            if sec not in pool: unmatched.append((i + 1, m.group(0)))
    info['timestamps_cited'] = n_ts; info['timestamps_unmatched'] = len(unmatched)
    if unmatched: fails.append('A4 %d/%d 个时间戳在转录里找不到对应段：%s' % (len(unmatched), n_ts, unmatched[:12]))

    # A5 引文可回溯（只查带时间戳或 🎙️ 的行；只认 *"…"* 斜体纯英文引文，**"…"** 是讲义引文不查）
    bad_q = []; low_q = []; n_q = 0
    for i, ln in enumerate(lines):
        if not (TS.search(ln) or '🎙️' in ln): continue
        for q in re.findall(r'(?<!\*)\*["“]([^"“”*|一-鿿]+?)["”]\*(?!\*)', ln):
            core = re.sub(r'\[[^\]]*\]', ' | ', q)              # 方括号补词 = 转录里没有，作为断点
            frags = [f for f in re.split(r'\||…|\.\.\.|—', core) if len(words(f)) >= 4]
            if not frags: continue
            n_q += 1
            tot = hit = 0
            for f in frags:
                w = words(f)
                sh = list(zip(w, w[1:], w[2:])) if len(w) >= 6 else list(zip(w, w[1:]))   # 短句用二元组
                for g in sh:
                    tot += 1
                    hit += (g in shingles) if len(g) == 3 else (g in bigrams)
            if tot:
                r = round(hit / tot, 2)
                if r < 0.4: bad_q.append((i + 1, r, q[:70]))
                elif r < 0.6: low_q.append((i + 1, r, q[:50]))
    info['quotes_checked'] = n_q; info['quotes_unmatched'] = len(bad_q); info['quotes_low'] = len(low_q)
    if bad_q: fails.append('A5 %d/%d 条引文与转录匹配率 <40%%（可能编造，或改写未加方括号）：%s' % (len(bad_q), n_q, bad_q[:8]))
    if low_q: warns.append('A5 %d 条引文匹配率 40–60%%（多半是改写了 ASR 却没加 [ ]，请核对）：%s' % (len(low_q), low_q[:6]))

    # A6 §8 课堂覆盖列（只看带「课堂覆盖」列的那张映射表）
    s8 = section(body, 8)
    rows = next((tb for tb in tables(s8) if any('课堂覆盖' in c for c in tb[0])), None); missing = 0; checked = 0
    if rows:
        hdr = rows[0]; ci = next(k for k, c in enumerate(hdr) if '课堂覆盖' in c)
        for r in rows[1:]:
            if len(r) <= ci: continue
            rowtxt = ' '.join(r)
            if any(k in rowtxt for k in ('封面', '分隔', '⚪', '标题页')): continue
            if not re.search(r'p\.\d', rowtxt): continue
            checked += 1
            if r[ci] in ('', '—', '-', '–'): missing += 1
        if missing: fails.append('A6 §8 有 %d/%d 个内容页行的「课堂覆盖」为空或 —' % (missing, checked))
    else:
        fails.append('A6 找不到 §8 带「课堂覆盖」列的页码映射表')
    info['§8_rows_checked'] = checked
    if '时间分配' not in s8 and '用时' not in s8: warns.append('A6 §8 没有「课堂时间分配」表')

    # A7 §9.1 / 9.2 / 9.5
    s91 = subsection(body, '9.1'); s92 = subsection(body, '9.2'); s95 = subsection(body, '9.5')
    if not table_rows(s91): fails.append('A7 §9.1 没有表格（略过/缺失清单）')
    r92 = [r for r in table_rows(s92)[1:] if TS.search(' '.join(r))]
    if len(r92) < 3: fails.append('A7 §9.2 带时间戳的行只有 %d（需 ≥3）' % len(r92))
    if '反方视角' not in s95: fails.append('A7 §9.5 缺「反方视角」')
    if '无转录' in s92 and '无法判断' in s92: fails.append('A7 §9.2 仍写着"本讲无转录，无法判断"')

    # A8 §6.2 🔴
    s6 = section(body, 6)
    red = [r for r in table_rows(s6) if r and r[0].startswith('🔴')]
    red_ok = [r for r in red if TS.search(' '.join(r)) and re.search(r'\*["“]', ' '.join(r))]
    info['🔴_rows'] = len(red); info['🔴_rows_with_quote'] = len(red_ok)
    if not red_ok:
        (warns if no_red else fails).append('A8 §6.2 没有带时间戳+引文的 🔴 行（%d 条 🔴）' % len(red))
    if re.search(r'0 条.*无转录|无转录.*无法产生', s6): fails.append('A8 §6.1 仍写着"本讲无转录，无法产生 🔴"')

    # A9
    s0 = section(body, 0)
    if '课堂实况' not in s0: warns.append('A9 §0 没有「🎙️ 课堂实况」块')
    if 'merged' not in text[:3000]: warns.append('A9 文首提示块没提到 merged / 转录特殊之处')

    # A10 无证据的"教授说"
    noev = [i + 1 for i, ln in enumerate(lines) if re.search(r'教授(说|强调|明确|指出|提到|补充)', ln) and not TS.search(ln)
            and not re.search(r'见 §|见 \[\[|§9\.|转录 `', ln)]
    if noev: warns.append('A10 %d 行有"教授说/强调…"但本行无时间戳：%s' % (len(noev), noev[:20]))

    # A11
    s96 = subsection(body, '9.6') or subsection(body, '9.7')
    if not re.search(r'\|\s*20\d\d-\d\d-\d\d.*转录', s96): fails.append('A11 §9.6/9.7 变更记录没有含"转录"的合并行')

    # A12 §8 区间并集覆盖率
    iv = []
    for m in re.finditer(r'`(?:part\d+ )?(\d{1,2}):(\d{2})(?::(\d{2}))?`\s*[–\-—~]\s*`(?:part\d+ )?(\d{1,2}):(\d{2})(?::(\d{2}))?`', s8):
        a = to_sec(*m.groups()[:3]); b = to_sec(*m.groups()[3:])
        if b > a: iv.append((a, b))
    iv.sort(); cov = 0; cur = None
    for a, b in iv:
        if cur and a <= cur[1]: cur = (cur[0], max(cur[1], b))
        else:
            if cur: cov += cur[1] - cur[0]
            cur = (a, b)
    if cur: cov += cur[1] - cur[0]
    ratio = round(cov / span, 2) if span else 0
    info['§8_time_coverage'] = ratio
    if span and ratio < 0.75: warns.append('A12 §8 的转录区间只覆盖录音的 %d%%（并集 %s / 录音 %s）——检查是否全程对齐' % (ratio * 100, fmt(cov), fmt(span)))

    verdict = 'PASS' if not fails else 'FAIL'
    if want_json:
        print(json.dumps({'note': note, 'verdict': verdict, 'fails': fails, 'warns': warns, 'info': info}, ensure_ascii=False, indent=1))
    else:
        print('=' * 90); print('转录融合验收  ', os.path.basename(note)); print('-' * 90)
        for k, v in info.items(): print('   %-24s %s' % (k, v))
        for f in fails: print('   ✗', f)
        for w in warns: print('   △', w)
        print('【判定】', verdict)
    return verdict == 'PASS'

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] not in ('scan', 'audit'):
        print(__doc__); sys.exit(2)
    if a[0] == 'scan':
        scan(a[1:]); sys.exit(0)
    note = a[1]; want_json = '--json' in a; no_red = '--no-red' in a
    tp = []
    if '--transcript' in a:
        k = a.index('--transcript') + 1
        while k < len(a) and not a[k].startswith('--'): tp.append(a[k]); k += 1
    if not tp: print('audit 需要 --transcript <转录文件>'); sys.exit(2)
    sys.exit(0 if audit(note, tp, want_json, no_red) else 1)
