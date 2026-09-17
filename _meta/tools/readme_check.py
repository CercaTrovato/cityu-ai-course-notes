# -*- coding: utf-8 -*-
"""README 状态同步检查：根 README「五门课」表必须与各笔记 frontmatter 一致。

    PYTHONIOENCODING=utf-8 /d/anaconda3/python.exe _meta/tools/readme_check.py          # 有不一致 → 逐条列出，exit 1

规则（每条都对应一次真实漏改）：
  R1 「笔记」列必须出现每篇 M0N / T0N 笔记的 `M0N vX.Y`（与 frontmatter status 一致；同一模块不能同时出现两个版本号）
  R2 frontmatter `transcript: merged` 的模块，「转录」列必须有 `M0N ✅` 或 `W0N ✅`，且不能再写该模块「待导出 / 待录 / 未导出」
  R3 frontmatter `transcript: pending` 的模块，「转录」列不能写成 ✅
  R4 「待办 / 最近完成」表里不能有已完成事项仍是 🟡 / 🔴 的行：同一行同时含「待导出」与已 merged 模块的课程码+模块号
  R5 目录树 / 五门课表里不能再出现 `pending` 字样指向已 merged 的模块（粗查：README 全文里 "M0N" 同行含 "pending" 且该模块已 merged）
"""
import io, os, re, sys, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
COURSES = {'IS5113': 'AI_Ethics_and_Regulations', 'IS5542': 'GenAI_in_Business', 'EF5560': 'Fintech_and_AI_in_Finance',
           'AC6761': 'Artificial_Intelligence_Accounting', 'IS6400': 'Business_Data_Analytics'}

def in_range(mod, status, col):
    """接受 `M04–M06 v0.9` 这种区间写法。"""
    for m in re.finditer(r'([MT])(\d\d)[–-][MT]?(\d\d) (v\d\.\d)', col):
        if m.group(1) == mod[0] and int(m.group(2)) <= int(mod[1:]) <= int(m.group(3)) and m.group(4) == status: return True
    return False

def fm(path):
    t = io.open(path, encoding='utf-8').read(2000)
    g = lambda k: (re.search(r'^%s:\s*(\S+)' % k, t, re.M) or [None, ''])[1]
    return g('status'), g('transcript')

def main():
    readme = io.open(os.path.join(ROOT, 'README.md'), encoding='utf-8').read()
    lines = readme.split('\n')
    probs = []
    rows = {}
    for l in lines:
        m = re.match(r'^\|\s*\**[^|]+?\**\s*\|\s*(IS\d{4}|EF\d{4}|AC\d{4})\s*\|', l)
        if m:
            cells = [c.strip() for c in l.strip().strip('|').split('|')]
            if len(cells) >= 5: rows[m.group(1)] = (cells[3], cells[4], l)
    for code, cdir in COURSES.items():
        if code not in rows: probs.append('五门课表缺 %s 行' % code); continue
        notes_col, tr_col, raw = rows[code]
        for p in sorted(glob.glob(os.path.join(ROOT, cdir, 'notes', '[MT]0*.md'))):
            mod = os.path.basename(p)[:3]; status, tr = fm(p)
            if not status: continue
            if ('%s %s' % (mod, status)) not in notes_col and not in_range(mod, status, notes_col):
                probs.append('R1 %s 行「笔记」列没有 %s %s（frontmatter status）' % (code, mod, status))
            others = [v for v in re.findall(r'\b%s (v\d\.\d)' % mod, notes_col) if v != status]
            if others: probs.append('R1 %s 行「笔记」列 %s 同时出现 %s' % (code, mod, others))
            wmod = 'W' + mod[1:]                                  # IS6400 的「转录」列按周写：W0N ✅ 同时覆盖 M0N 与 T0N
            if tr.startswith('merged'):
                if not re.search(r'(%s|%s|M%s) ✅' % (mod, wmod, mod[1:]), tr_col):
                    probs.append('R2 %s 行「转录」列没有 %s ✅（frontmatter transcript: merged）' % (code, mod))
                if re.search(r'(%s|%s) ?(待导出|待录|未导出|未合并)' % (mod, wmod), tr_col):
                    probs.append('R2 %s 行「转录」列仍写 %s 待导出，但已 merged' % (code, mod))
                for i, l in enumerate(lines):
                    if re.search(r'\b%s\b' % mod, l) and code in l and re.search(r'待导出', l) and not re.search(r'~~|✅', l):
                        probs.append('R4 待办表第 %d 行仍是待导出：%s' % (i + 1, l[:80]))
                    if code in l and re.search(r'\b%s\b' % mod, l) and re.search(r'`pending`', l) and '00-课程总览' not in l:
                        probs.append('R5 第 %d 行 %s %s 仍写 pending' % (i + 1, code, mod))
            elif tr.startswith('pending') or tr == 'none':
                if re.search(r'(%s|%s) ✅' % (mod, wmod), tr_col):
                    probs.append('R3 %s 行「转录」列写了 %s ✅，但 frontmatter 是 %s' % (code, mod, tr))
    for p in probs: print('✗', p)
    print('readme_check 问题数: %d' % len(probs))
    sys.exit(1 if probs else 0)

if __name__ == '__main__':
    main()
