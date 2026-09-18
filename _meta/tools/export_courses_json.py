# -*- coding: utf-8 -*-
"""生成 lecture-transcribe 的 courses.json（课程 → Whisper hotwords / 下次模块 / 转录目录）。

    PYTHONIOENCODING=utf-8 /d/anaconda3/python.exe _meta/tools/export_courses_json.py [--dry-run] [--out <path>] [--max 70]

数据来源（全部按 HANDOFF-cityu-vault.md §6 的规则）：
  · 课程列表：vault 根下 `<课程码>_<课程名>/` 目录；课程全名取根 README「五门课」表
  · hotwords：`<课程>/_meta/术语表.md` 各表的 English 列（按表头定位，不假定列号）
      优先级：① 专名 / 缩写 / 含数字或大写缩写 / 人名   ② ⭐ 段落或 ⭐ 行里的术语
              ③ asr-dictionary.md 本课分节「应为」列（曾被识别错的词的正确写法）   ④ 其余按出现顺序补足
      实际排序：CityU → 专名前 30 → ⭐（≤10）→ asr 词 → 其余专名 → 其余术语；去掉普通英语词、整句、中文；按 ~140 估算 token 截断（默认上限 --max 70 条，宁少勿多）
  · next_module：各 M0N 笔记 frontmatter `date:` —— 今天之后最近一次课的模块；没有则最近一次已上课的模块 + 1
重跑时机：某门课新 module 的术语表写完之后（转录处理规则 §5.1）。输出用 atomic_write。
"""
import io, os, re, sys, glob, json, datetime, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from safe_write import atomic_write
OUT_DEFAULT = r'E:\AIworkspace\lecture-transcribe\courses.json'
ASR = os.path.join(ROOT, '.claude', 'skills', 'transcript-merge', 'reference', 'asr-dictionary.md')
CJK = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
STOP = set('''data model models process method methods analysis system systems value values variable variables feature features
learning training test testing error errors example examples problem problems result results function functions number numbers
level levels type types set sets sample samples record records object objects attribute attributes table tables user users
mind logic ethics morality intelligence consciousness privacy transparency accountability fairness bias risk risks control
return returns price prices cost costs profit loss asset assets income expense expenses cash revenue sales stock equity
weight weights index rate rates time series step steps rule rules class classes group groups score scores mean median mode
range variance deviation distribution frequency count counts label labels token tokens agent agents prompt prompts drift
benchmark benchmarks scale opacity adaptation decoding temperature estimate estimates intercept slope residual deviation
tool tools code coding backup output outputs input inputs permission permissions challenge specification specifications
identifying recording communicating disclosure impairment lease consolidation ledger journal entry entries statement statements
tutorial assignment exam quiz canvas lecture week module course'''.split())
GENERIC_SINGLE = STOP
COMMON = STOP | set('''business understanding preparation building evaluation deployment independent dependent predictor target
response explanatory simple linear regression multiple variable random assumption assumptions curve fitting least squares ordinary
estimate estimation prediction predictive modeling interdisciplinary study engineer scientist stakeholder human machine supervised
unsupervised semi reinforcement representation language large natural processing generative artificial general intelligence
sequential ensemble class attention transformer embedding positional encoding contextual vector generation pretraining
capability evidence mission fit six four vectors paradigms coexist statistical drift expert system systems disruptive technology
workshop cognitive science imitation game test self special pleading golden rule good will duty religious applied moral
relativism consistency theory dilemma philosophy morality metaphysics epistemology thinking acting rationally programme master
financial management tax accounting external internal users general purpose statements ethics auditor opinion clean adverse
qualified unqualified explanatory notes purpose vehicle capitalization expense identifying recording communicating
closing adjusted split dividend total annualized volatility drawdown maximum benchmark treasury yield term spread federal funds
weighted portfolio long short position neutral relative trade pairs rebalance active transaction impact liquidity backtest
forecast clock leakage survivorship point in of and the for to with by on vs a an or per non pre post cross
check procedure step steps specification specifications desktop coding tool permission levels backup output challenge
hold out method closed form solution near zero variance prompt cell time series model column row three row equal count bins
positive return base rate lagged moving average gap stock week panel sectional rank characteristic sorted high minus low
spread archival composite index real world economic value task level protocol open weight chain thought judge zero few shot
inter token latency compound retrieval augmented'''.split())
BRANDS = {'Anaconda', 'Jupyter Notebook', 'Google Colab', 'Vibe Coding', 'Kaggle', 'Python', 'pandas', 'NumPy', 'Matplotlib', 'seaborn',
          'Excel', 'Tableau', 'Power BI', 'Canvas', 'Notion', 'Obsidian', 'ChatGPT', 'Claude', 'Gemini', 'DeepSeek', 'Copilot', 'Cursor'}
def all_common(t):
    toks = [w for w in re.findall(r"[a-z]+", t.lower())]
    return bool(toks) and all(w in COMMON for w in toks)

def clean_cell(c):
    c = re.sub(r'<br\s*/?>', ' / ', c)
    c = re.sub(r'\[\[[^\]]*\|([^\]]*)\]\]', r'\1', c); c = re.sub(r'\[\[([^\]]*)\]\]', r'\1', c)
    c = c.replace('**', '').replace('`', '')
    c = re.sub(r'\$[^$]*\$', ' ', c)
    return c.strip()

def split_terms(cell):
    """一个 English 单元格 → 若干候选短语（括号里的缩写单独成项）。"""
    out = []
    for m in re.finditer(r'\(([A-Z][A-Za-z0-9&\-]{1,12})\)', cell): out.append(m.group(1))
    base = re.sub(r'（[^）]*）|\([^)]*\)', ' ', cell)
    for part in re.split(r'\s*(?:/|、|;|；|,|，| vs\.? | = |→|⇒|=)\s*', base):
        p = re.sub(r'\s+', ' ', part).strip(' .:：-–—').strip()
        if not p or CJK.search(p): continue
        if len(p.split()) > 4 or len(p) < 2: continue
        if not re.search(r'[A-Za-z]', p): continue
        out.append(p)
    return out

def is_proper(t):
    toks = t.split()
    if re.search(r'\d', t): return True
    if any(re.fullmatch(r'[A-Z][A-Z0-9&\-]{1,}', w) for w in toks): return True           # 缩写
    if any(re.search(r'[a-z][A-Z]', w) for w in toks): return True                        # CamelCase
    if any('-' in w and w[0].isupper() for w in toks): return True                        # T-account / Fama-French / CRISP-DM
    if re.search(r"'s\b", t): return True                                                 # Kohlberg's
    return False

def generic(t):
    toks = t.lower().split()
    if len(toks) == 1 and toks[0] in GENERIC_SINGLE: return True
    if len(toks) == 1 and len(toks[0]) <= 3 and not t.isupper(): return True
    if re.fullmatch(r'[A-Z][A-Z0-9&\-]+', t): return False                             # 缩写永远保留
    if all_common(t) and not re.search(r'[A-Z][a-z]*[A-Z]|\d|-', t): return True        # 全是常用词、又没有缩写 / 数字 / 连字符
    return False

def est_tokens(t): return int(len(t.split()) * 1.4 + 1)

def read_terms(path):
    """→ [(term, priority)]，priority 1 专名 / 2 ⭐ / 4 其余；按出现顺序。"""
    out = []; ei = None; star_sec = False
    for ln in io.open(path, encoding='utf-8'):
        s = ln.rstrip('\n')
        if s.startswith('#'): star_sec = ('⭐' in s or '★' in s); ei = None; continue
        if not s.startswith('|'): continue
        cells = [c.strip() for c in s.strip().strip('|').split('|')]
        if any(c.lower() == 'english' for c in cells):
            ei = next(k for k, c in enumerate(cells) if c.lower() == 'english'); continue
        if ei is None or len(cells) <= ei or set(cells[0]) <= set('-: '): continue
        star = star_sec or '⭐' in s or '★' in s
        zh = re.sub(r'[⭐★]', '', clean_cell(cells[0])).strip()
        if ei != 0 and zh and not CJK.search(zh):                                       # 中文列本身是 ASCII 专名 / 缩写（CRISP-DM、LASSO、Jupyter Notebook）
            for t in split_terms(zh):
                if is_proper(t) or t in BRANDS: out.append((t, 1))
        for t in split_terms(clean_cell(cells[ei])):
            if generic(t): continue
            out.append((t, 1 if is_proper(t) else (2 if star else 4)))
    return out

def read_asr(code):
    if not os.path.exists(ASR): return []
    t = io.open(ASR, encoding='utf-8').read()
    m = re.search(r'^## %s[^\n]*\n(.*?)(?=^## |\Z)' % code, t, re.M | re.S)
    if not m: return []
    out = []
    for ln in m.group(1).split('\n'):
        if not ln.startswith('| ') or ln.startswith('| 转录原文'): continue
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        if len(cells) < 2 or cells[1].startswith('[?]'): continue
        for x in split_terms(clean_cell(cells[1])):
            x = re.sub(r'\[|\]', '', x)
            if x.lower() in ('unemployment rate', 'canvas', 'so today', 'the 90th percentile', 'thinking', 'duty', "master's programme") or x.startswith('[') or len(x.split()) > 3: continue
            if re.fullmatch(r'[A-Za-z][A-Za-z0-9&\-\' ]*', x) and len(x.split()) <= 4: out.append(x)
    return out

def course_name(code):
    rd = io.open(os.path.join(ROOT, 'README.md'), encoding='utf-8').read()
    m = re.search(r'^\|\s*\**([^|*]+?)\**\s*\|\s*%s\s*\|' % code, rd, re.M)
    return m.group(1).strip() if m else None

def next_module(cdir, today):
    dates = {}
    for p in glob.glob(os.path.join(cdir, 'notes', 'M0*.md')):
        t = io.open(p, encoding='utf-8').read(1500)
        m = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', t, re.M)
        if m: dates[int(os.path.basename(p)[1:3])] = datetime.date.fromisoformat(m.group(1))
    if not dates: return 'M01', '没有笔记'
    future = [(d, n) for n, d in dates.items() if d > today]
    if future:
        d, n = min(future); return 'M%02d' % n, '笔记 M%02d 的 date %s 在今天之后（课前建稿）' % (n, d)
    n, d = max(dates.items(), key=lambda kv: kv[1])
    return 'M%02d' % (n + 1), '最近一次已上课 M%02d（%s，笔记 date）+ 1；每周一次' % (n, d)

def build(max_n):
    today = datetime.date.today(); courses = []
    for cdir in sorted(glob.glob(os.path.join(ROOT, '[A-Z][A-Z][0-9][0-9][0-9][0-9]_*'))):
        code = os.path.basename(cdir)[:6]
        terms = read_terms(os.path.join(cdir, '_meta', '术语表.md'))
        asr = read_asr(code)
        stars = [(t, 2) for t, p in terms if p == 2][:10]                                # ⭐ 段落术语多为普通词，最多 10 条
        proper = [(t, 1) for t, p in terms if p == 1]
        asr = [x for x in asr if len(x) >= 3 and x.lower() not in ('scale', 'attribute', 'pd')]
        # 专名前 30 → ⭐ → 曾听错的词（asr）→ 其余专名 → 其余术语；asr 词是实测失败案例，不能被长长的专名尾巴挤掉
        ranked = [('CityU', 0)] + proper[:30] + stars + [(t, 3) for t in asr] + proper[30:] + [(t, 4) for t, p in terms if p == 4]
        seen = set(); hot = []; budget = 140                                             # ≈ 估算 token；faster-whisper 约 100 真实 token 后截断，排序即优先级
        for t, p in ranked:
            k = t.lower()
            if k in seen: continue
            if generic(t) and p not in (0, 3): continue
            if budget - est_tokens(t) < 0 or len(hot) >= max_n: break
            seen.add(k); hot.append(t); budget -= est_tokens(t)
        nm, why = next_module(cdir, today)
        courses.append({'code': code, 'name': course_name(code) or os.path.basename(cdir)[7:].replace('_', ' '),
                        'dir': cdir.replace('/', '\\'), 'transcripts_dir': os.path.join(cdir, 'transcripts').replace('/', '\\'),
                        'next_module': nm, 'hotwords': hot,
                        'notes': '转录放 transcripts/M0N-transcript.txt；next_module 依据：%s' % why,
                        '_stats': {'terms_total': len(terms), 'proper': sum(1 for _, p in terms if p == 1), 'star': sum(1 for _, p in terms if p == 2), 'asr': len(asr)}})
    return {'generated': datetime.datetime.now().isoformat(timespec='seconds'), 'vault': ROOT.replace('/', '\\'),
            'source': '_meta/tools/export_courses_json.py（术语表 English 列 + asr-dictionary + 笔记 date）', 'courses': courses}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dry-run', action='store_true'); ap.add_argument('--out', default=OUT_DEFAULT); ap.add_argument('--max', type=int, default=70)
    a = ap.parse_args()
    data = build(a.max)
    for c in data['courses']:
        st = c.pop('_stats')
        print('%s %-40s next=%s hotwords=%2d  (术语 %d：专名 %d / ⭐ %d；asr %d)  | %s' % (c['code'], c['name'][:40], c['next_module'], len(c['hotwords']), st['terms_total'], st['proper'], st['star'], st['asr'], c['notes'].split('依据：')[1]))
        if a.dry_run: print('   ', ', '.join(c['hotwords']))
    if a.dry_run: return
    text = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    atomic_write(a.out, text, min_ratio=0); print('✓ 写入', a.out, len(text.encode()), '字节')

if __name__ == '__main__':
    main()
