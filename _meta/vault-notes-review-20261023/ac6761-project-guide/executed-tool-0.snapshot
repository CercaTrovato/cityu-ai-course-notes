# -*- coding: utf-8 -*-
"""
note_quality.py — CityU 笔记机器检查（现行规则 2026-10-21）

用法：python note_quality.py <笔记> [--pages N] [--tut] [--strict] [--json] [--sections]
      [--readability] [--readability-strict] [--profile current|historical]
      [--source-checks 原题清单.json]

默认 current：L格式、R硬项、有证据的内容缺失/纯数字算式/源题清单错误参与机器判定。
固定标签、中文字数、页/小节比和类比数量只保存在 historical 字段，不决定当前FAIL。
historical：重放旧G/E配额判定；--strict使旧E参与，--legacy使旧E仅警告。
小节a后缀与代码语言正则边界修复同时适用于两种profile；历史输出不声称逐字重现旧版bug。
--source-checks：显式提供人工回源建立的note-source-checks-v1清单，
核源文件哈希、原题全文/选项字母与全文、每问中英答案锚点；不自动认证清单抄写和答案语义。
未提供清单时，源题完整性明确未验证；页码引述不等于实质逐页覆盖。
计算只核可安全识别的纯数字四则/幂/开方等式及显示精度，不执行代码或猜符号/单位。
所有profile都保留L/R检查；机器PASS不等于教学、计算运行或原题保真已验收。
JSON有profile、C、historical、legacy_problems、R等字段；旧诊断和回执不可追改为新结果。
退出码：0=机器可验证项通过（仍须实质核对），1=阻塞，2=参数/文件/结构错误。
"""
import re, io, sys, os, json, collections, argparse, glob, ast, math, hashlib, unicodedata
from pathlib import Path

SPEC_DATE = '2026-09-16'

# ---------------------------------------------------------------- 基础工具
CJK = re.compile(r'[一-鿿]')
def cjk(s): return len(CJK.findall(s))
def nonws(s): return len(re.sub(r'\s', '', s))

def classify(lines):
    """给每行打类型：code / bq / table / head / formula / text / blank"""
    out = []; fence = False; math = False
    for l in lines:
        s = l.strip()
        if s.startswith('```'):
            fence = not fence; out.append('code'); continue
        if fence: out.append('code'); continue
        if s.count('$$') % 2 == 1:
            math = not math; out.append('formula'); continue
        if math: out.append('formula'); continue
        if s.startswith('$$'): out.append('formula'); continue
        if not s: out.append('blank'); continue
        if s.startswith('#'): out.append('head'); continue
        if s.startswith('>'): out.append('bq'); continue
        if s.startswith('|'): out.append('table'); continue
        out.append('text')
    return out

PAGE_RE = re.compile(r'p\.\s*(\d+)(?:\s*[–\-~]\s*(\d+))?')
def pages_in(s, total=9999):
    cov = set()
    for x in PAGE_RE.finditer(s):
        a = int(x.group(1)); b = int(x.group(2)) if x.group(2) else a
        if b < a: b = a
        cov.update(range(a, min(b, total) + 1))
    return cov

def strip_code(t):
    t = re.sub(r'```.*?```', '', t, flags=re.S)
    return re.sub(r'`[^`\n]*`', '', t)

# ---------------------------------------------------------------- 标签与类型
LABELS = collections.OrderedDict([
    ('what', r'是什么|这块在干什么|在干什么'), ('why', r'为什么需要它|为什么这么写'),
    ('orig', r'课件原例|课件原文|notebook 原'), ('mic', r'🎙️'),
    ('alt', r'换个说法'), ('misc', r'常见误解|易错点'), ('rel', r'与其他概念的关系'),
    ('so', r'所以呢'), ('whyf', r'为什么公式长这样'), ('edge', r'极端情况|边界情况|极端 / 边界'),
    ('line', r'^逐行'), ('out', r'^输出'),
])
LABEL_LINE = re.compile(r'^\s*\*\*([^*\n]{1,40})\*\*')
def label_of(line):
    m = LABEL_LINE.match(line)
    if not m: return None
    txt = m.group(1)
    for k, pat in LABELS.items():
        if re.search(pat, txt): return k
    return 'other'

TYPE_TAG = re.compile(r'<!--\s*(?:类型|型)\s*[:：]\s*([^\s>]+)\s*-->')
ADMIN = re.compile(r'评分|作业|日程|行政|课程怎么运作|课后资源|教材与平台|小组项目|Take ?Away|课程表|安装|上手路径|截图|联系方式|考试安排|收尾|复核|反方|承接页|议程')
def section_type(head, lines, kinds, tag):
    if tag: return tag
    h = head
    if ADMIN.search(h): return '行政型'
    if re.search(r'勘误|写错|错误|讲义在这里|讲义把', h): return '勘误型'
    if 'code' in kinds and sum(1 for k in kinds if k == 'code') >= 3: return '代码型'
    if 'formula' in kinds: return '公式型'
    if re.search(r'算法|流程|步骤|怎么算|怎么做|手算|递归|迭代|梯度下降|五步|四步|三步', h): return '算法流程型'
    if re.search(r'\bvs\.?\b|对比|≠|区别|还是|两条路|两种|三种|四种|哪个', h, re.I): return '对比型'
    if re.search(r'图|plot|可视化|曲线|散点|直方|箱线|热力', h, re.I): return '图表读法型'
    if re.search(r'案例|例子|算例|数据集|实战|小测|场景|Iris|Airbnb', h, re.I): return '案例数据型'
    return '定义型'

# ---------------------------------------------------------------- 先修概念（L0-唤醒清单）
PREREQ = [
    ('中位数', r'中位数'), ('众数', r'众数'), ('方差', r'(?<!协)方差(?!分析)'), ('标准差', r'标准差'),
    ('标准误', r'标准误'), ('正态分布', r'正态分布'), ('分位数', r'分位数|百分位'), ('对数', r'对数|\blog\b'), ('概率密度', r'概率密度|密度函数'),
    ('期望', r'期望值|数学期望|\bE\['), ('相关系数', r'相关系数'), ('协方差', r'协方差'), ('矩阵', r'矩阵'), ('向量', r'向量'),
    ('转置', r'转置'), ('逆矩阵', r'逆矩阵|求逆|矩阵的逆'), ('特征值', r'特征值'), ('特征向量', r'特征向量'), ('导数', r'导数'),
    ('梯度', r'梯度'), ('假设检验', r'假设检验'), ('p 值', r'p ?值'), ('t 值', r't ?值|t 统计量'), ('置信区间', r'置信区间'),
    ('显著性', r'显著性|统计显著'), ('方差分析', r'方差分析|ANOVA'), ('卡方', r'卡方'), ('似然', r'似然'), ('线性组合', r'线性组合'),
    ('内积', r'内积|点积'), ('欧氏距离', r'欧氏距离|欧几里得距离'), ('熵', r'(?<![a-z])熵'), ('自由度', r'自由度'), ('残差', r'残差'),
    ('R²', r'R\^2|R²|判定系数'), ('标准化', r'标准化|z 分数|Z 分数|z-score'), ('指数', r'指数函数|\bexp\b'), ('偏度', r'偏度'), ('峰度', r'峰度'),
    ('条件概率', r'条件概率'), ('贝叶斯', r'贝叶斯'),
]

# ---------------------------------------------------------------- 原 notecheck 七项
def legacy_checks(t, TOTAL, tut):
    probs = []; info = {}
    lines = t.split('\n')
    if TOTAL > 0 and not tut:
        m = re.search(r'## 2\. .*?(?=\n## 3\.)', t, re.S)
        body = strip_code(m.group(0)) if m else ''
        cov = pages_in(body, TOTAL)
        info['L1_未讲解页'] = [i for i in range(1, TOTAL + 1) if i not in cov]
        info['L1_省略前缀连写'] = re.findall(r'p\.\d+[、,]\s*\d+', body)[:10]
    MATHY = re.compile(r'[Σ∑√∈≈≠≤≥×÷∂∞αβγδεθλμσπρτφω]|[̂̄̅]|²|³|ᵀ|⁻¹|\bargmin|[a-zA-Z]_\{')
    for lang, b in re.findall(r'```([a-zA-Z]*)\n(.*?)```', t, re.S):
        if lang in ('', 'text', 'math') and MATHY.search(b) and not re.search(r'\b(import|def |print\(|pd\.|np\.|plt\.|SELECT|FROM)', b):
            probs.append('L2 代码块里的伪公式: ' + b.strip().splitlines()[0][:80])
    for s in re.findall(r'`([^`\n]{3,120})`', re.sub(r'```.*?```', '', t, flags=re.S)):
        if MATHY.search(s) and not re.search(r'\.(py|csv|md|txt|pdf|ipynb)|/|\(\)|\bdf\b|pd\.|np\.|^\d+\s*[—–-]+\s*[∞\d]+$', s):
            probs.append('L2 行内代码里的伪公式: ' + s)
    def pipes(s): return len([k for k, ch in enumerate(s) if ch == '|' and (k == 0 or s[k - 1] != '\\')])
    in_fence = False; i = 0
    while i < len(lines):
        l = lines[i]
        if l.lstrip().startswith('```'): in_fence = not in_fence
        if not in_fence and l.startswith('|'):
            head = pipes(l); j = i
            while j < len(lines) and lines[j].startswith('|'):
                if pipes(lines[j]) != head: probs.append('L3 管道数不一致 行%d: %s' % (j + 1, lines[j][:60]))
                for m in re.finditer(r'(?<!\\)\$([^$\n]+?)(?<!\\)\$', lines[j]):
                    if '|' in m.group(1) and '\\|' not in m.group(1): probs.append('L3 表格公式含裸竖线 行%d' % (j + 1))
                for m in re.finditer(r'\[\[[^\]]*?\|[^\]]*\]\]', lines[j]):
                    if '\\|' not in m.group(0): probs.append('L3 表格里双链别名未转义 行%d %s' % (j + 1, m.group(0)))
                j += 1
            i = j; continue
        i += 1
    def is_currency(line):
        for m in re.finditer(r'(?<!\\)\$(\d)', line):
            rest = line[m.end():]; j = rest.find('$')
            seg = rest[:j] if j >= 0 else None
            if seg is not None and re.match(r'^\s*[−\-]?[\d.,]*\s*$', seg): continue      # $5$ / $-10$ / $0.5$ 是 LaTeX 数字，不是货币
            if seg is None or not re.search(r'[\\^_=+\-×/]', seg): return True
        return False
    fence = False
    for k, line in enumerate(lines, 1):
        if line.lstrip().startswith('```'): fence = not fence; continue
        if not fence and is_currency(line): probs.append('L3 未转义货币 $ 行%d: %s' % (k, line[:70]))
    fence = False
    for k, line in enumerate(lines, 1):
        if line.lstrip().startswith('```'): fence = not fence; continue
        if not fence and re.match(r'^#{1,6} ', line) and re.search(r'[|\[\]^*`]', line): probs.append('L4 标题含特殊字符 行%d: %s' % (k, line[:60]))
    fences = len(re.findall(r'^\s*```', t, re.M)); info['L5_围栏数'] = fences
    if fences % 2: probs.append('L5 代码围栏数为奇数: %d' % fences)
    c2 = strip_code(t)
    o, c = len(re.findall(r'<details', c2)), len(re.findall(r'</details>', c2)); info['L5_details'] = (o, c)
    if o != c: probs.append('L5 details 开/闭不配对: %d/%d' % (o, c))
    heads = set()
    for line in re.sub(r'```.*?```', '', t, flags=re.S).split('\n'):
        m = re.match(r'^#{1,6}\s+(.*?)\s*$', line)
        if m: heads.add(re.sub(r'\s+', ' ', re.sub(r'[#|^\[\]`]', '', m.group(1))).strip())
    for m in re.finditer(r'\[\[#([^\]|]+?)\s*(?:\\?\|[^\]]*)?\]\]', c2):
        a = re.sub(r'\s+', ' ', re.sub(r'[#|^\[\]`]', '', m.group(1))).strip()
        if a not in heads: probs.append('L6 同文件锚点失效: ' + m.group(0))
    return probs, info

# ---------------------------------------------------------------- 解析
def frontmatter(t):
    m = re.match(r'---\n(.*?)\n---', t, re.S)
    fm = {}
    if m:
        for line in m.group(1).split('\n'):
            k, _, v = line.partition(':')
            if _: fm[k.strip()] = v.strip()
    return fm

def body_M(t):
    m = re.search(r'\n## 2\..*?(?=\n## 3\.)', t, re.S)
    return m.group(0) if m else ''

def body_T(t):
    m = re.search(r'\n## 2\..*?(?=\n## \d+\.\s*(?:完整流程串讲|自己动手|完整流程))', t, re.S)
    if not m: m = re.search(r'\n## 2\..*?(?=\n## [4-9]\.)', t, re.S)
    return m.group(0) if m else ''

def split_sections(body):
    lines = body.split('\n'); secs = []; cur = None; fence = False
    for l in lines:
        if l.strip().startswith('```'): fence = not fence
        if not fence and re.match(r'^#{3,4} ', l):
            cur = [l]; secs.append(cur); continue
        if cur is None: cur = ['(intro)']; secs.append(cur)
        cur.append(l)
    return secs

def terms_sec5(t):
    """§5 术语卡 → [(中文, English, 首现节号)]"""
    sec5 = re.search(r'\n## 5\..*?(?=\n## 6\.)', t, re.S)
    out = []
    if not sec5: return out
    for line in sec5.group(0).split('\n'):
        if not line.startswith('|') or '---' in line or re.match(r'\|\s*中文', line): continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) < 4: continue
        m = re.search(r'§\s*(\d+(?:\.\d+)*[a-z]?)', cells[-1])
        out.append((cells[0], cells[1], m.group(1) if m else ''))
    return out

NONCONTENT = re.compile(r'封面|标题页|目标页|学习目标|分隔页|空白页|章节页|过渡页|行政页|安装截图页|截图页')
def noncontent_pages(t, total):
    sec8 = re.search(r'\n## 8\..*?(?=\n## 9\.)', t, re.S)
    non = set()
    if not sec8: return non
    for line in sec8.group(0).split('\n'):
        if not line.startswith('|') or not NONCONTENT.search(line): continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        pg = pages_in(line, total)
        first_is_dash = cells[0].startswith('—') or cells[0].startswith('（') or cells[0].startswith('(')
        if first_is_dash or NONCONTENT.search(cells[0]) or (len(cells) > 2 and NONCONTENT.search(cells[2]) and len(pg) <= 2):
            non |= pg
    return non

# ---------------------------------------------------------------- 小节指标
LATEX_CMDS = set('textbf textit arg hat bar xrightarrow xleftarrow mathcal boxed Longrightarrow Leftrightarrow longrightarrow implies frac tfrac dfrac sum prod text mathrm operatorname left right min max argmin argmax cdot cdots ldots times div hat bar tilde vec sqrt exp log ln quad qquad big Big bigl bigr mid underbrace overbrace approx ne neq le ge leq geq in infty to rightarrow Rightarrow partial nabla mathbf boldsymbol top T over displaystyle limits int lim sin cos tan begin end aligned pmatrix bmatrix cases dots vdots ddots mathbb mathcal mathit langle rangle lvert rvert lVert rVert Vert vert star ast pm mp equiv propto sim implies iff forall exists subset supset cup cap setminus emptyset therefore because circ bullet colon'.split())
def formula_tokens(tex):
    """公式里的「符号」：希腊字母命令 + 单个拉丁字母（含下标），忽略 \\text{…} 内容与 LaTeX 排版命令"""
    tex = re.sub(r'\\(?:text|mathrm|operatorname)\{[^}]*\}', ' ', tex)
    toks = set()
    for mm in re.finditer(r'\\([a-zA-Z]+)', tex):
        if mm.group(1) not in LATEX_CMDS: toks.add('\\' + mm.group(1))
    tex2 = re.sub(r'\\[a-zA-Z]+', ' ', tex)
    tex2 = re.sub(r'[_^]\{[^}]*\}|[_^][A-Za-z0-9]', ' ', tex2)      # 上下标不算新符号
    for mm in re.finditer(r'(?<![a-zA-Z])([A-Za-z])(?![a-zA-Z])', tex2):
        if mm.group(1) not in INDEX_LETTERS: toks.add(mm.group(1))
    return toks
INDEX_LETTERS = set('i j k n N t T m d e')          # 求和下标 / 样本量 / 时间 / 自然常数：默认已知
def selfdesc_formula(tex):
    return ('\\underbrace' in tex) or len(re.findall(r'\\text\{[^}]*[\u4e00-\u9fff]', tex)) >= 2
def numeric_formula(tex):
    return len(re.findall(r'\d+(?:\.\d+)?', re.sub(r'_\{?\d+\}?|\^\{?\d+\}?|\\[a-zA-Z]+', '', tex))) >= 3

NUM_STEP = re.compile(r'\d[\d,\.]*\s*[×x\*/÷+−\-]\s*[\d(]|\(\s*[\d,\.]+\s*[−\-+]\s*[\d,\.]+\s*\)|[=≈]\s*\**\s*[−\-]?\d[\d,\.]*.*[=≈]\s*\**\s*[−\-]?\d|\\frac\{[\d\.]+\}\{[\d\.]+\}')
NUM_ANY = re.compile(r'[=≈×+−]\s*\**\s*[−\-]?\d|\d+\.\d+|\d{1,3}(?:,\d{3})+')
REASON = re.compile(r'→|——|—|因为|其实|实际上|正确|应该|不是|才是|只有|而是|但')
SUBJ = re.compile(r'^\d+(?:\.\d+)*[a-z]?')

def section_metrics(sec, sec_type_override=None):
    head = sec[0]; lines = sec; kinds = classify(lines)
    m = collections.OrderedDict()
    m['sec'] = re.sub(r'^#+\s*', '', head)
    m['num'] = (SUBJ.match(m['sec']) or [None])[0] if SUBJ.match(m['sec']) else ''
    m['level'] = len(head) - len(head.lstrip('#')) if head.startswith('#') else 0
    tag = None
    for l in lines[:3]:
        mm = TYPE_TAG.search(l)
        if mm: tag = mm.group(1)
    m['cjk'] = sum(cjk(l) for l, k in zip(lines, kinds) if k not in ('code', 'head'))
    m['chars'] = sum(nonws(l) for l, k in zip(lines, kinds) if k not in ('code', 'head'))
    m['own_cjk'] = sum(cjk(l) for l, k in zip(lines, kinds) if k == 'text')
    bq = sum(nonws(l) for l, k in zip(lines, kinds) if k == 'bq')
    m['bq_ratio'] = round(bq / m['chars'], 2) if m['chars'] else 0
    m['code_blocks'] = sum(1 for l, k in zip(lines, kinds) if k == 'code' and l.strip().startswith('```')) // 2
    m['pages'] = sorted(pages_in(head))
    # 标签块
    blocks = collections.defaultdict(list); cur = 'pre'; order = []
    for l, k in zip(lines, kinds):
        if k == 'head': continue
        lab = label_of(l) if k == 'text' else None
        if lab and lab != 'other': cur = lab; order.append(lab)
        blocks[cur].append(l)
    m['labels'] = [k for k in LABELS if k in blocks]
    m['type'] = section_type(m['sec'], lines, kinds, tag)
    what = [l for l in blocks.get('what', []) if not re.match(r'^\s*\*\*[^*]+\*\*\s*$', l)]
    m['what_cjk'] = sum(cjk(l) for l in what if not l.strip().startswith('>'))
    m['why_cjk'] = sum(cjk(l) for l in blocks.get('why', []))
    # 换个说法角度
    alt = blocks.get('alt', [])
    alt_body = []
    for l in alt:
        if LABEL_LINE.match(l) and re.search(r'换个说法', l):
            rest = re.sub(r'^\s*\*\*[^*]+\*\*[：:]?\s*', '', l)
            if rest.strip(): alt_body.append(rest)
        else: alt_body.append(l)
    paras = [p for p in re.split(r'\n\s*\n', '\n'.join(alt_body).strip()) if cjk(p) >= 40]
    bullets = [l for l in alt_body if re.match(r'^\s*[-*•]\s', l) and cjk(l) >= 40]
    angles = bullets if len(bullets) > len(paras) else paras
    m['alt_angles'] = len(angles)
    # 「不靠数字的角度」：段落里没有行内公式 $…$、没有 ≈，且数字串少于 6 个（类比 / 比喻 / 换一种说法，而不是又一个算例）
    m['alt_nodigit'] = sum(1 for p in angles if not re.search(r'\$[^$]+\$|≈', p) and len(re.findall(r'\d+', p)) < 6)
    m['alt_cjk'] = sum(cjk(l) for l in alt_body)
    # 常见误解
    misc = blocks.get('misc', [])
    items = [l for l in misc if '❌' in l] or [l for l, k in zip(lines, kinds) if '❌' in l and k == 'text']
    m['misc_n'] = len(items)
    m['misc_reason'] = sum(1 for l in items if REASON.search(l.split('❌', 1)[1]))
    # 公式三件套
    fstarts = []; inmath = False
    for i, (l, k) in enumerate(zip(lines, kinds)):
        if k != 'formula': inmath = False; continue
        if not inmath: fstarts.append(i)
        inmath = True
    m['formula_n'] = len(fstarts)
    symtab = [i for i, (l, k) in enumerate(zip(lines, kinds)) if k == 'table' and re.search(r'符号|记号|含义|是什么|意思', l) and i + 1 < len(lines) and lines[i + 1].strip().startswith('|')]
    # 符号表里登记过的符号（表格行第一格里的 $…$）
    syms = set()
    for s0 in symtab:
        j = s0 + 2
        while j < len(lines) and lines[j].strip().startswith('|'):
            cell = lines[j].strip('|').split('|')[0]
            for mm in re.finditer(r'\$([^$]+)\$', cell): syms |= formula_tokens(mm.group(1))
            j += 1
    m['symtab_syms'] = syms
    # 正文散文里用 $…$ 点名过的符号（如「似然函数 $L(\theta)$」）也算已解释
    m['prose_syms'] = set()
    for l, k in zip(lines, kinds):
        if k == 'text':
            for mm in re.finditer(r'(?<!\$)\$(?!\$)([^$\n]+)\$', l): m['prose_syms'] |= formula_tokens(mm.group(1))
    m['formulas'] = []
    for f in fstarts:
        blk = []; j = f
        while j < len(lines) and kinds[j] == 'formula': blk.append(lines[j]); j += 1
        near = any(f - 30 <= s <= f + 30 for s in symtab)
        if not near:
            # 散文式符号说明：公式后 8 行文字里用 $…$ 逐个点到了全部符号（如「其中 $\lambda$ 是…」）
            after = [l for l, k in zip(lines[j:j + 8], kinds[j:j + 8]) if k in ('text', 'table')]
            inline = set()
            for l in after:
                for mm in re.finditer(r'\$([^$\n]+)\$', l): inline |= formula_tokens(mm.group(1))
            ftoks = formula_tokens(' '.join(blk))
            near = bool(ftoks) and ftoks <= inline
        m['formulas'].append((f, ' '.join(blk).strip(), near))
    txt = [l for l, k in zip(lines, kinds) if k in ('text', 'table')]
    m['numex_step'] = sum(1 for l in txt if NUM_STEP.search(l))
    m['numex_any'] = sum(1 for l in txt if NUM_ANY.search(l))
    # 代码三件套
    bad_code = 0
    idx = [i for i, (l, k) in enumerate(zip(lines, kinds)) if l.strip().startswith('```') and k == 'code']
    for a, b in zip(idx[0::2], idx[1::2]):
        if not re.match(r'^\s*```(python|py|sql|bash|sh|r|R)\b', lines[a]): continue
        before = [kinds[j] for j in range(max(0, a - 3), a)]
        after_lines = lines[b + 1:b + 9]; after_kinds = kinds[b + 1:b + 9]
        ok_before = 'text' in before
        ok_after = any(k in ('table',) for k in after_kinds) or any(re.match(r'^\s*[-*]\s', l) or re.search(r'逐行|这几行|关键', l) for l in after_lines)
        if not (ok_before and ok_after): bad_code += 1
    m['code_bad'] = bad_code
    # 首元素
    body = [(l, k) for l, k in zip(lines, kinds) if k not in ('head', 'blank') and not re.match(r'^\s*\*\*[^*]+\*\*\s*$', l) and not TYPE_TAG.search(l)]
    m['first_kind'] = body[0][1] if body else 'none'
    m['first_bad'] = int(m['first_kind'] in ('table', 'formula', 'code'))
    fp = []
    src = what if what else [x for x, k in zip(lines, kinds) if k not in ('head',)]
    for l in src:
        if re.match(r'^\s*\*\*[^*]+\*\*\s*$', l) or TYPE_TAG.search(l): continue
        if not l.strip():
            if fp: break
            continue
        fp.append(l)
        if len(fp) >= 3: break
    m['first_para'] = ' '.join(fp)
    m['has_so'] = int('so' in blocks)
    m['has_whyf'] = int('whyf' in blocks or bool(re.search(r'为什么(公式|要除以|要平方|是 ?n ?[−-] ?1|要乘|要开根|要取对数|长这样)', '\n'.join(txt))))
    m['has_edge'] = int('edge' in blocks or bool(re.search(r'极端|边界|退化|当 .{0,12}(为 0|等于 0|趋于|=0|= 0)|最大值|最小值', '\n'.join(txt))))
    m['has_step_table'] = int(any(re.match(r'^\s*\d+[\.、)]\s', l) for l in txt) or any(re.search(r'步骤|第 ?[一二三1-3] ?步|Step', l) for l in txt))
    m['has_cmp_table'] = int(any(k == 'table' for k in kinds))
    m['has_script'] = int(bool(re.search(r'脚本|\.py\b|verify_|复算|复核|实跑', '\n'.join(txt))))
    m['orig_cjk'] = sum(cjk(l) for l in blocks.get('orig', []))
    return m

# ---------------------------------------------------------------- 术语首现 / 先修唤醒
EXPL_AFTER = re.compile(r'^.{0,40}?[（(][^）)]*[A-Za-z]')
DEF_WORD = re.compile(r'^\s*(?:\*\*)?\s*(是|指|即|：|:|=|——|，就是|就是|，即|叫做|称为|的意思是|的定义)')

def explained_here(term, english, lines, kinds, i, after):
    """就地解释：术语后 ≤40 字内有括号（含英文）/ 定义词；或 4 行窗口内出现 §5 的英文名"""
    if EXPL_AFTER.match(after) or DEF_WORD.match(after): return True
    if re.match(r'^[^。]{0,60}?(就是|指的是|意思是|即|也就是|说的是)', after): return True
    if english:
        en = re.sub(r'\(.*?\)', '', english.split('/')[0]).strip()[:25]
        if len(en) >= 3:
            win = ' '.join(l for l, k in zip(lines[i:i + 4], kinds[i:i + 4]) if k != 'code')
            if re.search(re.escape(en), win, re.I): return True
    return False

def term_checks(t, body, sec5):
    """G4：每个 §5 术语在其「首现」小节里被就地解释；G5：先修概念的唤醒。"""
    lines = body.split('\n'); kinds = classify(lines)
    sec_of = {}; cur = ''
    for i, (l, k) in enumerate(zip(lines, kinds)):
        if k == 'head':
            mm = re.match(r'^#+\s*(\d+(?:\.\d+)*[a-z]?)', l); cur = mm.group(1) if mm else cur
        sec_of[i] = cur
    heads_by_sec = {}
    for i, (l, k) in enumerate(zip(lines, kinds)):
        if k == 'head':
            mm = re.match(r'^#+\s*(\d+(?:\.\d+)*[a-z]?)', l)
            if mm: heads_by_sec[mm.group(1)] = l
    unexplained = []; checked = 0; early = 0
    for zh, en, first in sec5:
        primary = re.split(r'\s*/\s*|（|\(|、|\s*·\s*', zh)[0].strip().strip('*')
        if len(primary) < 2 or not first: continue
        checked += 1
        # 候选写法：全称 + 去掉「属性/变量/回归/…」后缀的核心词（≥2 字）
        core = re.sub(r'(属性|变量|回归|模型|分析|方法|系数|参数|指数|函数|矩阵|数据|规则|评分|问题)$', '', primary)
        cands = [primary] + ([core] if len(core) >= 2 and core != primary else [])
        cand_re = re.compile('|'.join(re.escape(c) for c in cands))
        # 本节及祖先节标题里出现该术语 → 本节负责定义
        anc = [first[:j] for j in range(len(first), 0, -1) if first[:j] in heads_by_sec and (j == len(first) or first[j] == '.')]
        heads_txt = ' '.join(heads_by_sec.get(a, '') for a in anc)
        en_core = re.sub(r'\(.*?\)', '', en.split('/')[0]).strip()[:20] if en else ''
        if cand_re.search(heads_txt) or (len(en_core) >= 3 and re.search(re.escape(en_core), heads_txt, re.I)):
            continue
        found = False; ok = False; first_line = None
        for i, (l, k) in enumerate(zip(lines, kinds)):
            if k in ('code',): continue
            insec = sec_of[i] == first or sec_of[i].startswith(first + '.')
            mm = cand_re.search(l)
            if not mm: continue
            if not insec:
                if not found and first_line is None: first_line = i
                continue
            found = True
            if k == 'head': ok = True; break
            if explained_here(primary, en, lines, kinds, i, l[mm.end():]): ok = True; break
            break
        if first_line is not None and first_line < (i if found else 10**9): early += 1
        if not found: unexplained.append((primary, '§%s 内未出现' % first))
        elif not ok: unexplained.append((primary, '§%s 行 %d 未就地解释' % (first, i + 1)))
    # ---- 先修概念唤醒
    sec11 = re.search(r'### 1\.1.*?(?=\n### 1\.2)', t, re.S)
    sec11_txt = sec11.group(0) if sec11 else ''
    sec5_txt = ' '.join(zh for zh, en, f in sec5)
    prereq_bad = []; prereq_seen = 0
    for name, pat in PREREQ:
        rx = re.compile(pat)
        if rx.search(sec5_txt) or rx.search(sec11_txt): continue       # 本讲术语 / §1.1 已唤醒
        for i, (l, k) in enumerate(zip(lines, kinds)):
            if k in ('code', 'bq', 'formula'): continue
            mm = rx.search(l)
            if not mm: continue
            prereq_seen += 1
            head = heads_by_sec.get(sec_of[i], '')
            after = l[mm.end():]
            if k == 'head' or rx.search(head): break
            if re.match(r'^.{0,25}?[（(]', after) or re.search(r'\[\[|§\s*\d', l) or DEF_WORD.match(after): break
            prev = lines[i - 1] if i > 0 else ''
            if rx.search(prev) and re.search(r'[（(]', prev): break
            prereq_bad.append((name, i + 1)); break
    return unexplained, checked, prereq_bad, early

# ---------------------------------------------------------------- R 可读性层（《可读性总规则》，2026-10-08）
# 口径：阅读单元 = 1 个汉字 / 可见标点计 1；连续英文单词或数字串计 1；行内公式、行内代码各计 2；Markdown 标记不计。
# 切句：每行单独切（列表项、段落行天然断开），行内按 。！？ 切；引用块、表格、代码、公式、标题不参与句长统计。
R_TH = dict(sent_hard=120, sent_warn=80, sent_p90=60, long_share=0.03, para_hard=200, para_warn=150, para_sent_hard=7, para_sent_warn=6,
            li_hard=150, li_warn=80, run_hard=800, run_warn=500, circ_hard=3, neg_hard=4, neg_warn=3, bold_warn=4,
            cols_hard=9, cols_warn=7, cell_hard=80, cell_warn=40, cell_sent_hard=3, cell_sent_warn=2, row_warn=200,
            math_hard=6, math_warn=4, inline_tex_warn=60, code_lines_warn=30, paren_warn=30, gloss_warn=3, first_para_sent_warn=4)
R_CODE = collections.OrderedDict([
    ('R1a', '单句长度'), ('R1b', '全篇句长分布'), ('R1c', '一句多个分号'), ('R1d', '括号插入语过长'), ('R1e', '否定澄清堆叠'),
    ('R2a', '段落长度 / 句数'), ('R2b', '列表项长度'), ('R2c', '段内圈号编号'), ('R2d', '段内加粗过多'),
    ('R3a', '连续正文块过长'), ('R3b', '标题层级过深'), ('R3c', '表格前缺空行'),
    ('R4a', '表格列数'), ('R4b', '单元格字数'), ('R4c', '单元格句数'), ('R4d', '表格前无引导文字'), ('R4e', '表格行总长'),
    ('R5a', '一段行内公式过多'), ('R5b', '一个公式块多个等式'), ('R5c', '行内公式过长'), ('R5d', '代码块过长'), ('R5e', '小数省略前导 0'),
    ('R6a', '一段术语注释过密'), ('R7a', '主线混入核验细节'), ('R7b', '长原话未放引用块'),
    ('R8a', '§2 标题缺页码'), ('R8b', '小节首段过长'), ('R0', '豁免数量超限'),
    ('R4f', '表头说明线索待核'), ('R4g', '统计量计算判断待核'), ('R6b', '句内术语密度待核'), ('R6c', '压缩表达待核'),
    ('R6d', '术语首用解释待核'), ('R8c', '误解解释待核'),
])
R_EXEMPT = re.compile(r'<!--\s*可读性豁免\s*[:：]\s*([^>]*?)\s*-->')
R_LABEL = re.compile(r'^\s*\*\*[^*\n]{1,30}\*\*\s*[：:]?')
R_NEG = re.compile(r'不是|不能|不代表|不等于|不意味着|并不|并非|不保证|不说明')
R_CIRC = re.compile(r'[①②③④⑤⑥⑦⑧⑨⑩]')
R_TS = re.compile(r'\b\d{1,2}:\d{2}(?::\d{2})?\b')
R_ZONE_MAP = re.compile(r'^##\s+\d+\.\s*.*(映射)')
R_ZONE_LOG = re.compile(r'^##\s+\d+\.\s*.*(延伸与勘误|勘误|复核记录|验收记录)')
R_LOG_DETAILS = re.compile(r'复算|来源|核验|日志|验证|审查|脚本')

def r_strip_md(s):
    s = re.sub(r'\[\[([^\]|]*?)\\?\|([^\]]*)\]\]', r'\2', s)
    s = re.sub(r'\[\[([^\]]*)\]\]', r'\1', s)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = s.replace('**', '').replace('__', '')
    return re.sub(r'<[^>]+>', '', s)

R_WORD = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.,%\-+/]*')
def r_units(s):
    """阅读单元数（见上方口径）"""
    s = r_strip_md(s)
    n = [0]
    def rep(m): n[0] += 1; return ' '
    s = re.sub(r'(?<!\$)\$(?!\$)[^$\n]+\$', rep, s)
    s = re.sub(r'`[^`\n]+`', rep, s)
    lat = len(R_WORD.findall(s))
    rest = R_WORD.sub('', s)
    return len(re.findall(r'[^\s\-*#>|]', rest)) + lat + 2 * n[0]

def r_sentences(text):
    out = []
    # Markdown 段落内的软换行不是句号，不能靠折行规避检查。
    for line in [re.sub(r'\s*\n\s*', ' ', text)]:
        line = re.sub(r'^\s*([-*+]|\d+[.)])\s+', '', line.strip())
        prot = re.sub(r'\$[^$]+\$', lambda m: m.group(0).replace('。', '.').replace('？', '?').replace('！', '!'), line)
        for s in re.split(r'(?<=[。！？])', prot):
            if r_units(s) >= 3: out.append(s.strip())
    return out

def r_blocks(t):
    """把笔记切成块：(kind, text, 起始行号, zone, ctx)。kind ∈ para/li/label/table/bq/code/formula/head/html；
    zone ∈ main（§0–§7 及 T 笔记主体）/ map（页码映射）/ log（§9 延伸与勘误）；ctx = dict(mic, logdet, exempt, sec)"""
    lines = t.split('\n')
    m = re.match(r'---\n.*?\n---\n', t, re.S)
    i = t[:m.end()].count('\n') if m else 0
    out = []; zone = 'main'; sec = ''; fence = False; math = False; mic = False; logdet = 0; exempt = None; lab = ''; labno = 0
    details_stack = []
    cur = []; curk = None; curl = 0; curctx = None
    def flush():
        nonlocal cur, curk, curctx
        if cur: out.append((curk, '\n'.join(cur), curl, zone, curctx))
        cur = []; curk = None; curctx = None
    while i < len(lines):
        raw = lines[i]; s = raw.strip()
        if fence:
            cur.append(raw)
            if s.startswith('```'): fence = False; flush()
            i += 1; continue
        if math:
            cur.append(raw)
            if s.count('$$') % 2 == 1: math = False; flush()
            i += 1; continue
        if s.startswith('```'):
            flush(); curk = 'code'; curl = i + 1; curctx = dict(mic=mic, logdet=logdet > 0, exempt=exempt, sec=sec); exempt = None
            cur.append(raw); fence = True; i += 1; continue
        if s.startswith('$$'):
            flush(); curk = 'formula'; curl = i + 1; curctx = dict(mic=mic, logdet=logdet > 0, exempt=exempt, sec=sec); exempt = None
            cur.append(raw)
            if s.count('$$') % 2 == 1: math = True
            else: flush()
            i += 1; continue
        mm = R_EXEMPT.search(s)
        if mm: flush(); exempt = mm.group(1) or '未写理由'; i += 1; continue
        if not s: flush(); i += 1; continue
        if s.startswith('#'):
            flush()
            if s.startswith('## '):
                zone = 'map' if R_ZONE_MAP.match(s) else ('log' if R_ZONE_LOG.match(s) else 'main')
            hm = re.match(r'^#+\s*(\d+(?:\.\d+)*[a-z]?)', s); sec = hm.group(1) if hm else sec
            mic = False; lab = ''
            out.append(('head', s, i + 1, zone, dict(mic=False, logdet=logdet > 0, exempt=None, sec=sec, label='')))
            i += 1; continue
        if re.search(r'<details\b', s):
            flush()
            details_stack.append(bool(logdet or (re.search(r'<summary\b', s) and R_LOG_DETAILS.search(s))))
        if re.search(r'<summary\b', s) and details_stack and R_LOG_DETAILS.search(s):
            details_stack[-1] = True
        if '</details>' in s and details_stack:
            flush()
            details_stack.pop()
        logdet = int(any(details_stack))
        if s.startswith('>'): k = 'bq'
        elif s.startswith('|'): k = 'table'
        elif re.match(r'^([-*+]|\d+[.)])\s', s): k = 'li'
        elif s.startswith('<'): k = 'html'
        elif R_LABEL.match(s) and r_units(R_LABEL.sub('', s)) < 3: k = 'label'
        else: k = 'para'
        if k in ('para', 'label') and R_LABEL.match(s):
            mic = '🎙️' in R_LABEL.match(s).group(0)
            lab = re.sub(r'[*：:\s]', '', R_LABEL.match(s).group(0)); labno += 1
        if k in ('li', 'html', 'label') or k != curk:
            flush(); curk = k; curl = i + 1; curctx = dict(mic=mic, logdet=logdet > 0, exempt=exempt, sec=sec, label=lab, labno=labno); exempt = None
        cur.append(s); i += 1
    flush()
    return out, lines

def r_cells(row):
    return [c.strip() for c in re.split(r'(?<!\\)\|', row.strip().strip('|'))]

def r_cell_sentence_count(cell):
    """R4c：句末标点终结最后一句，不额外制造一句；连续句末标点只作一个边界。"""
    text = re.sub(r'\$[^$]*\$', '', cell).rstrip('。；！？')
    return len(re.findall(r'[。；！？]+', text)) + (1 if r_units(cell) > 0 else 0)

# ---------------------------------------------------------------- R v2：说人话与表头完整性（2026-10-08 用户截图反馈）
# R4f 表头缺专门说明  R4g 统计量列缺计算或判断  R6b 一句术语过多  R6c 压缩表达  R6d 高风险术语在本节首用未展开  R8c 常见误解未用 ❌ 格式
R_VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R_COURSES = ('AC6761', 'EF5560', 'IS5113', 'IS5542', 'IS6400')
R_ACR_STOP = set('AI ML API CSV PDF HTML URL OK ID PPT PPTX CEO US USA HK UK EU QA FAQ PS NB TV PC IT UI DDL GB MB KB'.split())
R_GENERIC_HEAD = re.compile(r'^(项目|内容|字段|说明|含义|是什么|例子|示例|备注|步骤|动作|页|讲义页|页码|来源|中文|English|英文|术语|首现|首现位置|读法|作用|行|行号|代码片段|代码|列|编号|序号|类型|问题|答案|结论|理由|维度|场景|情况|改法|症状|层|名称|对象|模型|学校|公司|账户|日期|时间|标记|组成部分|注|原文|翻译|本例取值|本节取值|单位|已知还是要算|何时已知|读作|判断|结果|数值|脚本|格|阶段|方法|做法|字段名|操作|界面|位置|人物|机构|观点|阶段|例|英文定义|考试可用的英文定义)$', re.I)
R_METRIC_HEAD = re.compile(r'均值|平均|比例|率|价差|收益|误差|统计量|标准|权重|分数|得分|系数|重要性|贡献|回撤|换手|占|差|MSE|RMSE|MAE|R\^?2|R²|Beta|Alpha|SSE|距离|概率|余额|金额|利润|成本', re.I)
R_STAT_HEAD = re.compile(r'^(t|p|z|F|t\(.*\)|t_\{?\\?mathrm\{?stat\}?\}?|tstat)$|统计量|p值|t值|显著|置信', re.I)   # 检验统计量：必须有计算和判断线
R_CN_NUM = '零一二三四五六七八九十'
R_CALC = re.compile(r'\d[\d.,%]*\s*(?:[=÷×/]|\\frac|\\div|\\times)|(?:=|÷|\\frac|\\approx|≈)\s*[{\\]?\s*[\d−\-]')
R_JUDGE = re.compile(r'临界|阈值|判断线|大于|小于|超过|低于|高于|约 ?2|拒绝|显著|怎么判断|判断')
R_EXPL_AFTER = re.compile(r'^[\s*”"」]{0,3}(?:[（(][^）)]*[\u4e00-\u9fff][^）)]*[）)]|[：:]|，?\s*(?:即|也就是|就是|是指|指的是|指|意思是|叫做?|称为|表示|是(?!否)))')
R_EXPL_BEFORE = re.compile(r'(?:叫做?|称为|这叫|叫作|记作|简称|即|所谓)\s*[“"「*]*\s*$')

def r_explanation_clue(plain, start, end):
    """检测先解释后命名、括号命名等线索；不认证语义正确性。"""
    before, after = plain[max(0, start - 100):start], plain[end:end + 100]
    if R_EXPL_AFTER.match(after) or R_EXPL_BEFORE.search(before):
        return True
    if re.search(r'[（(]\s*$', before) and re.match(r'\s*[）)]', after):
        return cjk(re.split(r'[。！？]', before)[-1]) >= 4
    return False
R_COMPRESS = re.compile(r'口径|层面|意义上|稳定性|有效性|一致性|可比性|稳健性|显著性结论|证据强度|时间依赖|常见近似|一定条件下|仍需检查|掩盖了?|体现了|体现出|反映了|支持.{0,6}结论|提供了?.{0,6}证据|存在.{0,4}问题|具有.{0,4}意义')

def r_course_of(t, path):
    c = frontmatter(t).get('course', '').strip()
    if c in R_COURSES: return c
    for part in re.split(r'[\\/]', os.path.abspath(path or '')):
        for cc in R_COURSES:
            if part.startswith(cc + '_'): return cc
    return ''

def r_variants(cell):
    cell = re.sub(r'\*\*|`|\$', '', cell)
    return [w.strip(' “”"') for w in re.split(r'\s*[/／、]\s*|[（(]|[）)]', cell) if len(w.strip(' “”"')) >= 2]

def r_risk_terms(course):
    """课程可读性细则「高风险术语」表 → [(变体列表, 人话)]"""
    out = []
    if not course: return out
    for p in glob.glob(os.path.join(R_VAULT, course + '_*', '_meta', course + '可读性细则.md')):
        with io.open(p, encoding='utf-8') as source:
            txt = source.read()
        m = re.search(r'\n#+ [^\n]*高风险术语[^\n]*\n(.*?)(?=\n#+ |\Z)', txt, re.S)
        if not m: continue
        for line in m.group(1).split('\n'):
            if not line.startswith('|') or re.match(r'^\|[\s:|-]+\|?$', line): continue
            cells = r_cells(line)
            if len(cells) < 2 or cells[0] in ('术语', '词', '本课术语'): continue
            out.append((r_variants(cells[0]), cells[1]))
    return out

def r_term_index(t, course):
    idx = []
    for i, (vs, gloss) in enumerate(r_risk_terms(course)):
        for v in vs: idx.append((v, 'K%d' % i, 'risk'))
    for j, (zh, en, first) in enumerate(terms_sec5(t)):
        vs = r_variants(zh) + [e.strip() for e in re.split(r'\s*/\s*', re.sub(r'\(.*?\)', '', en or '')) if len(e.strip()) >= 4]
        for v in vs: idx.append((v, 'S%d' % j, 'sec5'))
    idx.sort(key=lambda x: -len(x[0]))
    out = []
    for v, cid, kind in idx:
        pat = re.compile(r'(?<![A-Za-z])' + re.escape(v) + r'(?![A-Za-z])', re.I) if v.isascii() else re.compile(re.escape(v))
        out.append((pat, v, cid, kind))
    return out

def r_find_terms(s, idx):
    """一行里的术语命中 [(start, end, 原文, cid, kind)]：高风险表 / §5 术语卡 / 大写缩写，不重叠"""
    clean = re.sub(r'\$[^$]*\$|`[^`]*`|\[\[[^\]]*\]\]|https?://\S+|p\.\s*\d+', lambda m: ' ' * len(m.group(0)), s)
    taken = [False] * len(clean); hits = []
    for pat, v, cid, kind in idx:
        for m in pat.finditer(clean):
            if any(taken[m.start():m.end()]): continue
            for k in range(m.start(), m.end()): taken[k] = True
            hits.append((m.start(), m.end(), m.group(0), cid, kind))
    for m in re.finditer(r'(?<![A-Za-z0-9])[A-Z][A-Z0-9]{1,}(?![A-Za-z0-9])', clean):
        w = m.group(0)
        if any(taken[m.start():m.end()]) or w in R_ACR_STOP or re.match(r'^[MTWSQ]\d+$|^[A-Z]{2}\d{4}$', w): continue
        hits.append((m.start(), m.end(), w, 'A:' + w, 'acr'))
    hits.sort()
    return hits

def r_norm_head(h):
    # 保留 t(alpha) 等角色，只剥离明确的单位括号。
    h = re.sub(r'[（(](?:%|％|元|万元|秒|周|月|年)[）)]', '', h)
    h = re.sub(r'\\mathrm\{([^}]*)\}|\\text\{([^}]*)\}', lambda m: m.group(1) or m.group(2), h)
    return re.sub(r'[\s*$`\\{}]', '', h)

R_T_TOKEN = r'\$t[\$_(]|\|t\||t ?统计量|t_\{?\\mathrm\{stat\}|(?<![A-Za-z])t\s*[=≈(]|t_\{?stat'
def r_stat_token(core):
    if core.lower() in ('t', 'tstat', 't_stat'): return re.compile(R_T_TOKEN)
    if re.match(r'^t[(_]', core): return re.compile(re.escape(core) + '|' + R_T_TOKEN)
    return re.compile(re.escape(core), re.I)

def r_v2_checks(t, blocks, lines, path, tut, add, hard, warn, cut):
    course = r_course_of(t, path)
    idx = r_term_index(t, course)
    heads = [(ln, x) for k, x, ln, zone, ctx in blocks if k == 'head']
    # ---- 节单元：### 及其 #### 子节；只查 §2（T 笔记查全部主体）
    def in_body(ctx):
        return tut or re.match(r'^2(\.|$)', (ctx or {}).get('sec') or '') is not None
    unit_of = {}; unit_head = collections.defaultdict(str); unit = None
    for k, x, ln, zone, ctx in blocks:
        if k == 'head':
            lvl = len(x) - len(x.lstrip('#'))
            if lvl <= 3: unit = ln
            unit_head[unit] += ' ' + x
        unit_of[ln] = unit
    vocab = collections.defaultdict(set)
    for k, x, ln, zone, ctx in blocks:
        if k in ('li', 'para') and ctx and '本节用词' in (ctx.get('label') or ''):
            for line in x.split('\n'):
                head_part = re.split(r'[：:]', r_strip_md(line), 1)[0]
                for h in r_find_terms(head_part, idx): vocab[unit_of[ln]].add(h[3])
    seen = collections.defaultdict(set)
    misc = collections.OrderedDict()
    for k, x, ln, zone, ctx in blocks:
        if zone != 'main' or not ctx or ctx.get('exempt') or ctx.get('logdet'): continue
        lab = ctx.get('label') or ''
        if k in ('para', 'li') and '常见误解' in lab and in_body(ctx):
            key = (unit_of[ln], ctx.get('labno'))
            misc.setdefault(key, [ln, False])
            if '❌' in x: misc[key][1] = True
        if k not in ('para', 'li'): continue
        for line in x.split('\n'):
            plain = r_strip_md(line)
            # R6c 压缩表达（一句 ≥2 处）
            for s in r_sentences(line):
                cs = R_COMPRESS.findall(r_strip_md(s))
                if len(cs) >= 2: add(warn, 'R6c', ln, '“%s”：%s' % ('、'.join(cs[:3]), cut(s)))
                hs = r_find_terms(r_strip_md(s), idx)
                n = len({h[3] for h in hs})
                if n >= 6: add(warn, 'R6b', ln, '一句 %d 个术语，核对是否需要拆解（%s）：%s' % (n, '、'.join(dict.fromkeys(h[2] for h in hs)), cut(s)))
                elif n >= 4: add(warn, 'R6b', ln, '一句 %d 个术语（%s）：%s' % (n, '、'.join(dict.fromkeys(h[2] for h in hs)), cut(s)))
            # R6d 高风险术语在本节第一次出现时要展开（前文定义过不豁免）
            if not in_body(ctx) or '本节用词' in lab: continue
            u = unit_of[ln]
            for st, en, w, cid, kind in r_find_terms(plain, idx):
                if cid in seen[u]: continue
                seen[u].add(cid)
                if kind == 'sec5' or cid in vocab[u]: continue
                if r_explanation_clue(plain, st, en): continue
                nearby = r_strip_md(x)
                if any(h[3] == cid and r_explanation_clue(nearby, h[0], h[1])
                       for h in r_find_terms(nearby, idx)): continue
                if kind == 'risk': add(warn, 'R6d', ln, '“%s”本节首用未识别到解释线索；人工核对附近的动作说明或唤醒' % w)
                else: add(warn, 'R6d', ln, '缩写“%s”首用未识别到中文说明；人工核对' % w)
    for (u, _), (ln, ok) in misc.items():
        if not ok: add(warn, 'R8c', ln, '未发现 ❌ 标记；核对是否已用文字写清错误理解及理由，标记本身不是要求')
    # ---- R4f / R4g 表头完整性：表头里的指标、符号、缩写在同一小节要有专门说明；统计量列还要有计算和判断线
    hlines = [ln for ln, x in heads if len(x) - len(x.lstrip('#')) <= 4]
    for k, x, ln, zone, ctx in blocks:
        if k != 'table' or zone != 'main' or not in_body(ctx) or (ctx and (ctx.get('exempt') or ctx.get('logdet'))): continue
        rows = [r for r in x.split('\n') if r.startswith('|')]
        hdr = r_cells(rows[0])
        if len(hdr) < 2 or any(re.search(r'符号|记号|表头|列名|字段|术语', h) for h in hdr): continue
        lo = max([h for h in hlines if h < ln] or [1]); hi = min([h for h in hlines if h > ln] or [len(lines) + 1])
        tab_end = ln + len(rows) - 1
        eligible = set()
        for bk, bx, bl, bz, bc in blocks:
            if bz == 'main' and bk in ('para', 'li', 'formula', 'table') and not (bc or {}).get('logdet'):
                eligible.update(range(bl, bl + len(bx.split('\n'))))
        rng = [(i, lines[i - 1]) for i in range(lo + 1, hi)
               if i in eligible and not (ln <= i <= tab_end)]
        for col, h in enumerate(hdr, start=1):
            core = r_norm_head(h)
            if not core or R_GENERIC_HEAD.match(core): continue
            needs = '$' in h or re.search(r'[A-Za-z]', core) or R_METRIC_HEAD.search(core) or r_find_terms(core, idx)
            if not needs: continue
            pos = re.compile(r'第\s*(?:%d|%s)\s*列' % (col, R_CN_NUM[col] if col <= 10 else 'X'))
            def dedicated(line):
                s0 = re.sub(r'^\s*(?:[-*+]|\d+[.)])\s+', '', line.strip())
                nl = r_norm_head(re.sub(r'^\|', '', s0))
                if nl.startswith(core) or nl.startswith('“' + core) or nl.startswith('「' + core): return True
                if pos.search(line) or re.search(r'[“「]?' + re.escape(core) + r'[”」]?(?:这一?|一)?列|列[的“「]' + re.escape(core), r_norm_head(line)): return True
                if re.search(r'[“「]' + re.escape(core) + r'[”」].{0,3}(?:是|表示|指|：|:)', r_norm_head(line)): return True
                return any(r_norm_head(b).startswith(core) or core in [r_norm_head(p) for p in re.split(r'[/／、]', b)] for b in re.findall(r'\*\*(.+?)\*\*', line))
            if not any(dedicated(l) for i, l in rng if l.strip()):
                add(warn, 'R4f', ln, '表头“%s”未识别到专门说明；核对含义、算法或来源、单位和一行读法' % core)
                continue
            if R_STAT_HEAD.search(core):
                tok = r_stat_token(core)
                hit = lambda l: tok.search(l) or tok.search(r_norm_head(l))
                has_calc = any(hit(l) and R_CALC.search(l) for i, l in rng)
                has_judge = any(hit(l) and R_JUDGE.search(l) for i, l in rng)
                if not (has_calc and has_judge):
                    add(warn, 'R4g', ln, '统计量列“%s”未识别到%s；核对本列代入过程、判断规则和条件' % (core, '、'.join(n for n, ok in (('计算', has_calc), ('判断线', has_judge)) if not ok)))

def readability_checks(t, tut=False, path=None):
    blocks, lines = r_blocks(t)
    hard = []; warn = []; exempt_n = 0; sent_all = []
    cell_max = 0; cell_max_line = 0; cols_max = 0
    def add(lst, code, ln, detail): lst.append((code, ln, detail))
    def cut(s, n=36):
        s = re.sub(r'\s+', ' ', r_strip_md(s)); return s[:n] + ('…' if len(s) > n else '')
    run = 0; run_start = None; prev_kind = None; first_para_pending = None
    for idx, (k, x, ln, zone, ctx) in enumerate(blocks):
        if ctx and ctx.get('exempt'):
            exempt_n += 1; prev_kind = k; continue
        # ---- 版面与连续正文块
        if k in ('head', 'label', 'table', 'code', 'formula', 'html') or (k == 'para' and R_LABEL.match(x)):
            if run > R_TH['run_hard'] and zone == 'main': add(hard, 'R3a', run_start, '%d 单元无标题 / 标签 / 表格 / 公式隔断' % run)
            elif run > R_TH['run_warn'] and zone == 'main': add(warn, 'R3a', run_start, '%d 单元无隔断' % run)
            run = 0; run_start = None
        if k == 'head':
            lvl = len(x) - len(x.lstrip('#'))
            if lvl >= 5: add(hard, 'R3b', ln, '%d 级标题；改为 #### 或加粗标签' % lvl)
            if zone == 'main' and not tut and lvl in (3, 4) and re.match(r'^#+\s*2\.', x) and not re.search(r'p\.\s*\d|cell|Cell', x):
                add(warn, 'R8a', ln, cut(x, 40))
            first_para_pending = ln if lvl in (3, 4) and zone == 'main' else None
            prev_kind = k; continue
        if zone == 'log' or (ctx and ctx.get('logdet')):
            if k == 'table' and ln >= 2 and lines[ln - 2].strip() and not lines[ln - 2].strip().startswith('|'):
                add(hard, 'R3c', ln, '表格紧接上一行文字，Obsidian 不渲染')
            prev_kind = k; continue
        logdet = ctx.get('logdet') if ctx else False
        if k in ('para', 'li', 'bq'):
            if run_start is None: run_start = ln
            run += r_units(x)
        # ---- 句子与段落
        if k in ('para', 'li') and not logdet and zone == 'main':
            u = r_units(x); ss = r_sentences(x)
            for s in ss:
                su = r_units(s); sent_all.append(su)
                if su > R_TH['sent_hard']: add(hard, 'R1a', ln, '%d 单元：%s' % (su, cut(s)))
                elif su > R_TH['sent_warn']: add(warn, 'R1a', ln, '%d 单元：%s' % (su, cut(s)))
                if s.count('；') >= 2: add(warn, 'R1c', ln, '%d 个分号：%s' % (s.count('；'), cut(s)))
            for p in re.findall(r'[（(]([^（）()]*)[）)]', re.sub(r'\$[^$]*\$', '', x)):
                if r_units(p) > R_TH['paren_warn']: add(warn, 'R1d', ln, '括号内 %d 单元：%s' % (r_units(p), cut(p)))
            ng = len(R_NEG.findall(x))
            if ng >= R_TH['neg_hard']: add(hard, 'R1e', ln, '一段 %d 处“不是 / 不能…”澄清' % ng)
            elif ng >= R_TH['neg_warn']: add(warn, 'R1e', ln, '一段 %d 处否定澄清' % ng)
            if k == 'para':
                if u > R_TH['para_hard'] or len(ss) >= R_TH['para_sent_hard']: add(hard, 'R2a', ln, '%d 单元 / %d 句：%s' % (u, len(ss), cut(x)))
                elif u > R_TH['para_warn'] or len(ss) >= R_TH['para_sent_warn']: add(warn, 'R2a', ln, '%d 单元 / %d 句：%s' % (u, len(ss), cut(x)))
                if len(R_CIRC.findall(x)) >= R_TH['circ_hard']: add(hard, 'R2c', ln, '段内 %d 个圈号编号，改为编号列表' % len(R_CIRC.findall(x)))
            else:
                if u > R_TH['li_hard']: add(hard, 'R2b', ln, '%d 单元：%s' % (u, cut(x)))
                elif u > R_TH['li_warn']: add(warn, 'R2b', ln, '%d 单元：%s' % (u, cut(x)))
                if len(R_CIRC.findall(x)) >= R_TH['circ_hard']: add(hard, 'R2c', ln, '列表项内 %d 个圈号编号，拆成子列表' % len(R_CIRC.findall(x)))
            nb = len(re.findall(r'\*\*[^*\n]+\*\*', R_LABEL.sub('', x, count=1)))
            if nb >= R_TH['bold_warn']: add(warn, 'R2d', ln, '段内 %d 处加粗' % nb)
            nm_ = len(set(re.findall(r'(?<!\$)\$(?!\$)([^$\n]+)\$', x)))
            if nm_ >= R_TH['math_hard']: add(hard, 'R5a', ln, '一段 %d 个不同行内公式，改符号表或逐项列表' % nm_)
            elif nm_ >= R_TH['math_warn']: add(warn, 'R5a', ln, '一段 %d 个不同行内公式' % nm_)
            for f in re.findall(r'(?<!\$)\$(?!\$)([^$\n]+)\$', x):
                if len(f) > R_TH['inline_tex_warn']: add(warn, 'R5c', ln, '行内公式 %d 字符，改独立公式：%s' % (len(f), f[:30]))
            gl = len(re.findall(r'[（(][^（）()]*[A-Za-z]{3,}[^（）()]*[）)]', x))
            if gl >= R_TH['gloss_warn']: add(warn, 'R6a', ln, '一段 %d 处括号英文注释（约等于 %d 个新术语）' % (gl, gl))
            if not (ctx and ctx.get('mic')):
                ev = []
                if re.search(r'\d+\.\d{6,}', re.sub(r'\$[^$]*\$', '', x)) or re.search(r'\$[^$]*\d+\.\d{7,}[^$]*\$', x): ev.append('6 位以上小数')
                if re.search(r'[A-Za-z]:\\\\|[A-Za-z]:\\[^\s]|(?<![\w/])/d/|scratchpad', x): ev.append('绝对路径')
                if re.search(r'\b[0-9a-f]{16,}\b', x): ev.append('哈希')
                if len(R_TS.findall(x)) >= 3: ev.append('%d 个时间戳' % len(R_TS.findall(x)))
                if re.search(r'10\^\{?[−-]\d{2,}|\de-\d{2,}', x): ev.append('浮点级误差')
                if re.search(r'\.(csv|py|ipynb|xlsx|json)\b', x) and re.search(r'复算|核验|保存表|\d[\d,]* 行|rank\(|qcut\(|groupby\(', x): ev.append('复算记录')
                if ev: add(warn, 'R7a', ln, '、'.join(ev) + '；移到 §9 或折叠「复算与来源」')
            for q in re.findall(r'\*["“]([^"”*]{20,})["”]\*', x):
                if len(re.findall(r'[A-Za-z]+', q)) >= 25: add(warn, 'R7b', ln, '段内英文原话 %d 词，放引用块并配中文' % len(re.findall(r'[A-Za-z]+', q)))
            if re.search(r'(?<![\w.\d])\.\d', re.sub(r'\$[^$]*\$|`[^`]*`|\[\[[^\]]*\]\]|https?://\S+', '', x)):
                add(hard, 'R5e', ln, '“.5” 写成 “0.5”')
            if first_para_pending and k == 'para':
                if len(ss) >= R_TH['first_para_sent_warn']: add(warn, 'R8b', ln, '小节首段 %d 句；首段 ≤ 3 句，先给问题或结论' % len(ss))
                first_para_pending = None
        # ---- 表格
        if k == 'table':
            if ln >= 2 and lines[ln - 2].strip() and not lines[ln - 2].strip().startswith('|'):
                add(hard, 'R3c', ln, '表格紧接上一行文字，Obsidian 不渲染')
            rows = [r for r in x.split('\n') if r.startswith('|')]
            hdr = r_cells(rows[0]) if rows else []
            body = [r_cells(r) for r in rows[2:]]
            ncol = len(hdr)
            if zone == 'main':
                cols_max = max(cols_max, ncol)
                for offset, row in enumerate(rows):
                    if offset == 1: continue
                    for cell in r_cells(row):
                        size = r_units(cell)
                        if size > cell_max: cell_max, cell_max_line = size, ln + offset
                if ncol >= R_TH['cols_hard']: add(hard, 'R4a', ln, '%d 列；拆表或转置' % ncol)
                elif ncol >= R_TH['cols_warn']: add(warn, 'R4a', ln, '%d 列' % ncol)
            for j, r in enumerate(body):
                tot = 0
                for c in r:
                    cu = r_units(c); tot += cu
                    ns = r_cell_sentence_count(c)
                    tgt_h = hard if zone == 'main' else warn
                    if cu > R_TH['cell_hard']: add(tgt_h, 'R4b', ln + 2 + j, '单元格 %d 单元：%s' % (cu, cut(c)))
                    elif cu > R_TH['cell_warn']: add(warn, 'R4b', ln + 2 + j, '单元格 %d 单元：%s' % (cu, cut(c)))
                    if ns >= R_TH['cell_sent_hard']: add(tgt_h, 'R4c', ln + 2 + j, '单元格 %d 句：%s' % (ns, cut(c)))
                    elif ns >= R_TH['cell_sent_warn']: add(warn, 'R4c', ln + 2 + j, '单元格 %d 句' % ns)
                if tot > R_TH['row_warn'] and zone == 'main': add(warn, 'R4e', ln + 2 + j, '一行合计 %d 单元' % tot)
            if zone == 'main' and not tut and ctx and re.match(r'^2(\.|$)', ctx.get('sec') or '') and prev_kind not in ('para', 'li', 'label', 'html'):
                add(hard, 'R4d', ln, '表格前一块是 %s；先用一段话说明一行是什么、各列回答什么' % {'table': '另一张表', 'formula': '公式', 'code': '代码', 'head': '标题', 'bq': '引用'}.get(prev_kind, prev_kind))
        if k == 'formula' and zone == 'main':
            body_tex = re.sub(r'\\text\{[^}]*\}', '', x)
            if re.search(r'\\qquad|,\s*\\quad', body_tex) and body_tex.count('=') >= 2:
                add(warn, 'R5b', ln, '一个 $$ 块放了多个等式；拆开并在中间加一句话')
        if k == 'code' and zone == 'main':
            n_lines = len(x.split('\n')) - 2
            if n_lines > R_TH['code_lines_warn'] and not re.match(r'^\s*```(mermaid|dot|text)', x):
                add(warn, 'R5d', ln, '代码块 %d 行；按功能拆块并分别说明' % n_lines)
        prev_kind = k
    # 最后一块也要结算，不能靠文末没有标题漏过连续正文限制。
    if run > R_TH['run_hard'] and blocks and blocks[-1][3] == 'main':
        add(hard, 'R3a', run_start, '%d 单元无隔断（文末）' % run)
    elif run > R_TH['run_warn'] and blocks and blocks[-1][3] == 'main':
        add(warn, 'R3a', run_start, '%d 单元无隔断（文末）' % run)
    # ---- 全篇句长分布
    stats = {}
    if sent_all:
        xs = sorted(sent_all)
        p = lambda q: xs[int(round((len(xs) - 1) * q))]
        o80 = sum(1 for v in xs if v > R_TH['sent_warn'])
        stats = dict(sentences=len(xs), mean=round(sum(xs) / len(xs), 1), p50=p(.5), p90=p(.9), max=xs[-1],
                     over80=o80, over120=sum(1 for v in xs if v > R_TH['sent_hard']), long_share=round(o80 / len(xs), 3))
        if stats['p90'] > R_TH['sent_p90']: add(hard, 'R1b', 0, '句长 p90 = %d > %d' % (stats['p90'], R_TH['sent_p90']))
        if stats['long_share'] > R_TH['long_share']: add(hard, 'R1b', 0, '>80 单元长句占 %.1f%% > %.0f%%' % (100 * stats['long_share'], 100 * R_TH['long_share']))
    r_v2_checks(t, blocks, lines, path, tut, add, hard, warn, cut)
    stats['exempt'] = exempt_n
    stats.update(table_max_columns=cols_max, table_max_cell_units=cell_max,
                 table_max_cell_line=cell_max_line, measurement_version='v2')
    if exempt_n > 5: add(hard, 'R0', 0, '%d 个豁免块超过上限 5；人工检查是否误藏核心讲解' % exempt_n)
    return dict(hard=hard, warn=warn, stats=stats)

# ---------------------------------------------------------------- 判定
REQ_CELLS = {
    '定义型': ['what', 'why', 'alt', 'misc', 'so'],
    '公式型': ['what', 'why', 'alt', 'misc', 'so'],
    '算法流程型': ['what', 'why', 'alt', 'misc', 'so'],
    '对比型': ['what', 'why', 'alt', 'misc', 'so'],
    '案例数据型': ['what', 'why', 'misc', 'so'],
    '图表读法型': ['what', 'why', 'misc', 'so'],
    '勘误型': ['what', 'so'],
    '代码型': ['what', 'so'],
    '行政型': [],
}
CELL_NAME = {'what': '是什么', 'why': '为什么需要它', 'alt': '💡 换个说法', 'misc': '⚠️ 常见误解', 'so': '所以呢', 'orig': '课件原例', 'mic': '🎙️ 课堂补充', 'rel': '与其他概念的关系'}

TH = dict(cjk_per_page=250, terms_per_leaf=1.6, pages_per_leaf=2.5, sec_min_cjk=150, term_explain_rate=0.90,
          prereq_max_bad=3, so_rate=0.80, tut_cjk_per_cell=350, tut_code_bad_rate=0.20)

def nm(r): return r['num'] or r['sec'][:16]

def evaluate_M(t, fn, TOTAL, strict):
    body = body_M(t)
    if not body: return None
    secs = split_sections(body)
    rows = [section_metrics(s) for s in secs if s[0] != '(intro)']
    leaf = [r for r in rows if r['cjk'] >= 60]
    sec5 = terms_sec5(t)
    # 术语归节（容器节平摊）
    leafnums = {r['num'] for r in leaf}
    per_sec_terms = collections.Counter()
    for zh, en, first in sec5:
        if not first: continue
        if first in leafnums: per_sec_terms[first] += 1
        else:
            kids = [r['num'] for r in leaf if r['num'].startswith(first + '.')]
            for k in kids: per_sec_terms[k] += 1.0 / len(kids)
    for r in leaf:
        r['terms'] = round(per_sec_terms.get(r['num'], 0), 2)
        r['need_cjk'] = max(0, TH['cjk_per_page'] * len(r['pages']) - r['cjk'])
    non = noncontent_pages(t, TOTAL)
    content = TOTAL - len(non) if TOTAL else 0
    blines = body.split('\n'); bk = classify(blines)
    sec2_cjk = sum(cjk(l) for l, k in zip(blines, bk) if k not in ('code', 'head'))
    unexpl, nterms, prereq_bad, early = term_checks(t, body, sec5)
    concept = [r for r in leaf if r['type'] != '行政型']
    # ---- G 硬门槛
    G = collections.OrderedDict()
    G['G1 密度 §2 字/内容页 ≥ %d' % TH['cjk_per_page']] = (round(sec2_cjk / content) if content else None, (sec2_cjk / content >= TH['cjk_per_page']) if content else None)
    tpl = round(len(sec5) / len(leaf), 2) if leaf else 0
    G['G2a 粒度 术语数/leaf 小节 ≤ %.1f' % TH['terms_per_leaf']] = (tpl, tpl <= TH['terms_per_leaf'])
    ppl = round(content / len(leaf), 2) if leaf and content else 0
    G['G2b 粒度 内容页/leaf 小节 ≤ %.1f' % TH['pages_per_leaf']] = (ppl, (ppl <= TH['pages_per_leaf']) if content else None)
    thin = [nm(r) for r in leaf if r['terms'] >= 1 and r['cjk'] < TH['sec_min_cjk']]
    G['G2c 承载术语的小节 ≥ %d 字' % TH['sec_min_cjk']] = (thin, not thin)
    bad_first = [nm(r) for r in leaf if r['first_bad']]
    G['G3a 小节首元素为段落'] = (bad_first, not bad_first)
    # G3b：公式的符号表——同节 ±30 行有符号表 / 公式自注释 / 全是数字代入 / 符号都在前面带符号表的公式里出现过
    explained_syms = set(); bad_f = []
    for r in leaf:
        explained_syms |= r['symtab_syms'] | r['prose_syms']
        for idx, text, near in r['formulas']:
            toks = formula_tokens(text)
            if near or selfdesc_formula(text) or numeric_formula(text):
                explained_syms |= toks; continue
            if toks - explained_syms: bad_f.append((nm(r), text[:40], sorted(toks - explained_syms)[:6]))
            explained_syms |= toks
    bad_fn = [nm(r) for r in leaf if r['formula_n'] and not r['numex_any']]
    G['G3b 公式有符号表（或符号已在前文解释）'] = (bad_f, not bad_f)
    G['G3c 有公式的小节有数字例子'] = (bad_fn, not bad_fn)
    bad_c = [nm(r) for r in leaf if r['code_bad']]
    G['G3d 代码三件套'] = (bad_c, not bad_c)
    # G6：「所以呢」按 ### 单元算（#### 子节任一有即可）
    units = collections.OrderedDict()
    for r in concept:
        u = '.'.join(r['num'].split('.')[:2]) if r['num'] else r['sec']
        units.setdefault(u, []).append(r)
    so_units = [(u, any(x['has_so'] for x in rs)) for u, rs in units.items()]
    so_rate = round(sum(1 for u, ok in so_units if ok) / len(so_units), 2) if so_units else 1
    G['G6 ### 单元「所以呢」覆盖率 ≥ %.2f' % TH['so_rate']] = ((so_rate, [u for u, ok in so_units if not ok]), so_rate >= TH['so_rate'])
    # ---- E 元素清单（新规则，strict 才计入）
    rate = round(1 - len(unexpl) / nterms, 2) if nterms else 1
    E = []
    if rate < TH['term_explain_rate']: E.append(('全篇', '术语首现', ['§5 术语在首现小节就地解释率 %.2f < %.2f：%s' % (rate, TH['term_explain_rate'], '；'.join('%s（%s）' % u for u in unexpl[:8]))]))
    if prereq_bad: E.append(('全篇', '先修唤醒', ['先修概念首次使用无一句话唤醒：%s' % '、'.join('%s（行 %d）' % p for p in prereq_bad[:10])]))
    for r in concept:
        miss = []
        for c in REQ_CELLS.get(r['type'], []):
            if c not in r['labels']: miss.append('缺 ' + CELL_NAME[c])
        if 'alt' in REQ_CELLS.get(r['type'], []) and 'alt' in r['labels']:
            if r['alt_angles'] < 2: miss.append('换个说法角度 %d < 2' % r['alt_angles'])
            elif r['alt_nodigit'] == 0: miss.append('换个说法没有一个不靠数字的角度')
        if 'misc' in REQ_CELLS.get(r['type'], []) and 'misc' in r['labels']:
            if r['misc_n'] < 2: miss.append('常见误解 %d 条 < 2' % r['misc_n'])
            elif r['misc_reason'] < r['misc_n']: miss.append('常见误解 %d/%d 条缺理由' % (r['misc_n'] - r['misc_reason'], r['misc_n']))
        if r['type'] == '公式型':
            if not r['numex_step']: miss.append('数字例子没有算式（只给结果不算手把手）')
            if not r['has_whyf']: miss.append('缺「为什么公式长这样」')
            if not r['has_edge']: miss.append('缺 极端/边界情况')
        if r['type'] == '算法流程型':
            if not r['has_step_table']: miss.append('缺 编号步骤')
            if not r['numex_any']: miss.append('缺 手算一遍的数字例子')
        if r['type'] == '对比型' and not r['has_cmp_table']: miss.append('缺 对比表')
        if r['type'] == '案例数据型' and r['numex_any'] and not r['has_script']: miss.append('数字例子未标脚本来源')
        if r['type'] == '勘误型' and r['bq_ratio'] == 0: miss.append('勘误型缺讲义原文引用')
        if r['terms'] >= 1 and r['what_cjk'] < 80: miss.append('「是什么」自己的话 < 80 字')
        r['E_miss'] = miss
        if miss: E.append((nm(r), r['type'], miss))
    ok_G = all(v[1] is not False for v in G.values())
    ok_E = not E
    verdict = 'PASS' if ok_G and (ok_E or not strict) else 'FAIL'
    if verdict == 'PASS' and not ok_E: verdict = 'PASS（存量宽限：E 有 %d 个小节缺元素）' % len(E)
    summary = dict(file=fn, total_pages=TOTAL, noncontent=sorted(non), content_pages=content, sec2_cjk=sec2_cjk, note_cjk=cjk(t),
                   leaf_n=len(leaf), concept_n=len(concept), terms_n=len(sec5), strict=strict)
    return dict(summary=summary, G=G, E=E, rows=leaf, verdict=verdict)

def evaluate_T(t, fn, strict):
    body = body_T(t)
    if not body: return None
    secs = split_sections(body)
    rows = [section_metrics(s) for s in secs if s[0] != '(intro)']
    leaf = [r for r in rows if r['cjk'] >= 40]
    fm = frontmatter(t)
    mm = re.search(r'(\d+)\s*code', fm.get('source', ''))
    ncode = int(mm.group(1)) if mm else sum(r['code_blocks'] for r in leaf)
    blines = body.split('\n'); bk = classify(blines)
    cjk_body = sum(cjk(l) for l, k in zip(blines, bk) if k not in ('code', 'head'))
    G = collections.OrderedDict()
    per = round(cjk_body / ncode) if ncode else None
    G['G1t 逐块讲解 字/code cell ≥ %d' % TH['tut_cjk_per_cell']] = (per, (per >= TH['tut_cjk_per_cell']) if per is not None else None)
    nblocks = sum(r['code_blocks'] for r in leaf); nbad = sum(r['code_bad'] for r in leaf)
    rate = round(nbad / nblocks, 2) if nblocks else 0
    G['G3d 代码三件套缺失率 ≤ %.2f' % TH['tut_code_bad_rate']] = ((nbad, nblocks), rate <= TH['tut_code_bad_rate'])
    bad_first = [nm(r) for r in leaf if r['first_bad']]
    G['G3a 小节首元素为段落'] = (bad_first, not bad_first)
    E = []
    for r in leaf:
        miss = []
        for c, cname in (('what', '这块在干什么'), ('line', '逐行'), ('why', '为什么这么写'), ('misc', '易错点')):
            if c not in r['labels'] and not (c == 'line' and r['code_blocks'] == 0): miss.append('缺 ' + cname)
        if 'out' not in r['labels'] and r['code_blocks']: miss.append('缺 输出')
        r['E_miss'] = miss
        if miss: E.append((nm(r), 'cell 块', miss))
    ok_G = all(v[1] is not False for v in G.values()); ok_E = not E
    verdict = 'PASS' if ok_G and (ok_E or not strict) else 'FAIL'
    if verdict == 'PASS' and not ok_E: verdict = 'PASS（存量宽限：E 有 %d 个小节缺元素）' % len(E)
    summary = dict(file=fn, code_cells=ncode, body_cjk=cjk_body, note_cjk=cjk(t), leaf_n=len(leaf), strict=strict)
    return dict(summary=summary, G=G, E=E, rows=leaf, verdict=verdict)

# ---------------------------------------------------------------- 现行内容线索：不以标签/字数/类比配额代替实质核对
CURRENT_SPEC = '2026-10-21'
SECTION_NUMBER = r'\d+(?:\.\d+)*[a-z]?'
PLACEHOLDER = re.compile(r'^(?:待补(?:充)?|待完善|略|同理|见(?:讲义|课件|上文)|TODO|TBD|N/?A)[。.!！\s]*$', re.I)


def content_sections(body, include_level2=False):
    """保留真实标题、a后缀和全局行号；父节包含子节，空容器不算缺正文。"""
    lines = body.splitlines()
    kinds = classify(lines)
    heads = [(n, len(l)-len(l.lstrip('#')), re.sub(r'^#+\s*', '', l))
             for n, (l, k) in enumerate(zip(lines, kinds))
             if k == 'head' and re.match(r'^#{2,4} ' if include_level2 else r'^#{3,4} ', l)]
    result = []
    for n, (start, level, heading) in enumerate(heads):
        end = next((a for a, lev, _ in heads[n+1:] if lev <= level), len(lines))
        own_end = heads[n+1][0] if n+1 < len(heads) else len(lines)
        number = re.match(SECTION_NUMBER, heading)
        result.append(dict(number=number[0] if number else heading, heading=heading, line=start+1,
                           text='\n'.join(lines[start+1:end]), own='\n'.join(lines[start+1:own_end]),
                           container=own_end < end, level=level))
    return result


def author_text(text):
    """原题引文、程序、图源、空标签和占位句不作为已有讲解的证据。"""
    lines = text.splitlines()
    result = []
    for line, kind in zip(lines, classify(lines)):
        s = line.strip()
        if kind not in ('text', 'table') or re.match(r'</?(?:details|summary)|<!--', s):
            continue
        if re.match(r'^\*\*[^*]+\*\*\s*[:：]?\s*$', s):
            continue
        s = r_strip_md(s)
        if s and not PLACEHOLDER.fullmatch(s):
            result.append(s)
    return '\n'.join(result)


def safe_number(expression):
    """仅求有界数字四则/幂/开方；不执行名称、属性、下标或任意函数。"""
    def walk(node, depth=0):
        if depth > 16:
            raise ValueError('expression too deep')
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            value = node.value
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = walk(node.operand, depth+1) * (-1 if isinstance(node.op, ast.USub) else 1)
        elif isinstance(node, ast.BinOp) and type(node.op) in (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow):
            left, right = walk(node.left, depth+1), walk(node.right, depth+1)
            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError('exponent too large')
            value = {ast.Add: lambda: left+right, ast.Sub: lambda: left-right,
                     ast.Mult: lambda: left*right, ast.Div: lambda: left/right,
                     ast.Pow: lambda: left**right}[type(node.op)]()
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'sqrt' and len(node.args) == 1 and not node.keywords:
            value = math.sqrt(walk(node.args[0], depth+1))
        else:
            raise ValueError('not pure arithmetic')
        if not isinstance(value, (int, float)) or not math.isfinite(value) or abs(value) > 1e15:
            raise ValueError('out of range')
        return value
    if len(expression) > 160:
        raise ValueError('expression too long')
    return walk(ast.parse(expression, mode='eval').body)


def arithmetic_checks(body):
    findings = []
    # 有意错误示例、原题选项及运行输出不自动判成作者算错；代码不会被执行。
    for kind, text, line, zone, context in r_blocks(body)[0]:
        if kind not in ('para', 'li', 'formula') or zone != 'main':
            continue
        if re.search(r'错误|错法|误写|不应|不等于|不是|❌|wrong|incorrect', text, re.I) or '误解' in (context.get('label') or ''):
            continue
        fragments = re.findall(r'(?<!\$)\$(?!\$)([^$\n]+)\$(?!\$)', text)
        if kind == 'formula':
            fragments.append(text.replace('$$', ''))
        for raw in fragments:
            expr = raw.replace('−', '-').replace('×', '*').replace('÷', '/').replace(r'\times', '*').replace(r'\cdot', '*').replace(r'\approx', '=').replace('≈', '=')
            expr = re.sub(r'\\(?:left|right|,|;|!)', '', expr)
            for _ in range(4):
                expr = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', expr)
                expr = re.sub(r'\\sqrt\{([^{}]+)\}', r'sqrt(\1)', expr)
            expr = expr.replace('^', '**')
            expr = re.sub(r'(?<=\d)(?=\()', '*', expr)
            expr = re.sub(r'(?<=\))(?=\d|\()', '*', expr)
            expr = re.sub(r'(?<=\d),(?=\d{3}(?:\D|$))', '', expr)
            parts = expr.strip().rstrip('.,。').split('=')
            if len(parts) < 2 or not all(parts):
                continue
            # 等式中出现变量/百分号/单位/未支持LaTeX时整条跳过，不猜参数或单位。
            try:
                values = [safe_number(part.strip()) for part in parts]
            except (ValueError, SyntaxError, TypeError, ZeroDivisionError, OverflowError):
                continue
            for left, right, displayed in zip(values, values[1:], parts[1:]):
                digits = re.fullmatch(r'\s*[+-]?\d+(?:\.(\d+))?\s*', displayed)
                tol = (0.5 * 10**(-len(digits[1] or ''))) if digits else 1e-8
                if abs(left-right) > max(tol, abs(left)*1e-9) + 1e-10:
                    findings.append(dict(code='C_ARITHMETIC', section=context.get('sec', ''),
                                         line=line, message='纯数字等式与显示精度不符，须回算：'+raw,
                                         evidence=raw))
                    break
    return findings


def source_contract_checks(body, manifest_path):
    """清单须人工从原件建立；只认证源版本/字面完整/声明的逐问锚点，不认证语义。"""
    result = dict(status='unverified_without_manifest', checked_questions=0, hard=[], warnings=[])
    if not manifest_path:
        return result
    def fail(message, section=''):
        result['hard'].append(dict(code='C_SOURCE_CONTRACT', section=section, line=0, message=message, evidence=str(manifest_path)))
    try:
        path = Path(manifest_path)
        data = json.loads(path.read_text(encoding='utf-8'))
        if data.get('schema') != 'note-source-checks-v1' or not isinstance(data.get('questions'), list) or not data['questions']:
            raise ValueError('须有schema note-source-checks-v1与非空questions')
        sources = data['sources']
        verified = set()
        for source_id, source in sources.items():
            p = path.parent / source['path']
            if not re.fullmatch(r'[a-fA-F0-9]{64}', source['sha256']):
                raise ValueError('source sha256无效')
            if hashlib.sha256(p.read_bytes()).hexdigest().lower() != source['sha256'].lower():
                fail('原题源版本哈希不符：'+source_id)
            else:
                verified.add(source_id)
        sections = content_sections(body)
        def normalize(s):
            s = unicodedata.normalize('NFKC', s)
            s = re.sub(r'(?m)^\s*>\s?', '', s)
            return re.sub(r'\s+', ' ', s).strip()
        seen = set()
        for question in data['questions']:
            qid = question['id']
            if not isinstance(qid, str) or not qid or qid in seen:
                raise ValueError('题号为空或重复')
            seen.add(qid)
            section = question['section']
            matches = [s for s in sections if s['number'] == section or s['heading'] == section]
            if len(matches) != 1 or question['source_id'] not in verified:
                fail(qid+'：正文定位不唯一/缺失或源版本未核', section)
                continue
            question_text = strip_code(matches[0]['text'])
            content = normalize(question_text)
            original = question['original']
            units = question['answers']
            if not isinstance(original, str) or not original.strip() or not isinstance(units, list) or not units:
                raise ValueError(qid+'：须有完整original和逐问answers')
            if normalize(original) not in content:
                fail(qid+'：缺完整原题，不能以题号/中文概述替代', section)
            options = question.get('options', {})
            if not isinstance(options, dict):
                raise ValueError('options须为字母到完整选项的对象')
            for letter, option in options.items():
                if not re.fullmatch('[A-Z]', letter) or not isinstance(option, str) or not option.strip():
                    raise ValueError('选项字母/全文无效')
                if normalize(option) not in normalize(original) or not re.search(r'(?:^|\n)\s*'+letter+r'[.)、]\s', original):
                    raise ValueError(qid+'：original须包含声明的原选项字母和全文'+letter)
                if normalize(option) not in content or not re.search(r'(?:^|\n)\s*(?:>\s*)?(?:[-*]\s*)?'+letter+r'[.)、]\s', question_text):
                    fail(qid+'：缺原字母或完整选项'+letter, section)
            # 英文参考可以在引用/斜体中；排除程序后再匹配，不把原题本身当答案。
            answers_text = normalize(strip_code(matches[0]['text']))
            answer_ids = set()
            for unit in units:
                if unit['id'] in answer_ids:
                    raise ValueError('逐问答案id重复')
                answer_ids.add(unit['id'])
                chinese, english = unit['chinese'], unit['english']
                if not isinstance(chinese, str) or not CJK.search(chinese) or not isinstance(english, str) or not re.search('[A-Za-z]', english):
                    raise ValueError(qid+'：逐问中英答案锚点无效')
                if chinese.strip() in ('中文解析', '中文题意', '答案') or re.fullmatch(r'English reference answers?', english.strip(), re.I):
                    raise ValueError(qid+'：标签不是答案证据')
                if normalize(chinese) not in answers_text or normalize(chinese) in normalize(original):
                    fail(qid+'/'+unit['id']+'：缺声明的中文解析', section)
                if normalize(english) not in answers_text or normalize(english) in normalize(original):
                    fail(qid+'/'+unit['id']+'：缺独立英文参考答案', section)
            result['checked_questions'] += 1
        result['status'] = 'contract_failed' if result['hard'] else 'manifest_contract_passed'
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        fail('原题清单无效，不能跳过：'+str(exc))
        result['status'] = 'contract_failed'
    return result


def assess_current(t, fn, total=0, tut=False, source_checks=None):
    fm = frontmatter(t)
    primary_module = bool(re.fullmatch(r'[MT]\d{2}', fm.get('module', '').strip().strip("\"'")))
    standalone_assignment = bool(fm.get('assignment', '').strip()) and not primary_module
    learning_document = fm.get('type', '').strip("\"'") in {'课堂练习解析', 'practice-guide'} or standalone_assignment
    body = t if learning_document else (body_T(t) if tut else body_M(t))
    sections = content_sections(body, include_level2=learning_document)
    hard, warnings = [], []
    if not sections:
        hard.append(dict(code='C_STRUCTURE', section='§2', line=0,
                         message='未找到教学单元，空正文不能获得机器通过', evidence='### / ####'))
    shared_steps = [s['number'] for s in sections if any(NUM_STEP.search(line) for line in s['text'].splitlines() if not line.lstrip().startswith('>'))]
    offset = t[:t.index(body)].count('\n') if body else 0
    def add(code, s, message, blocking=False, evidence=''):
        (hard if blocking else warnings).append(dict(code=code, section=s['heading'], line=s['line']+offset,
                                                     message=message, evidence=evidence))
    for section in sections:
        content = section['text']
        own = author_text(section['own'])
        if not own and section['container'] and not re.search(chr(96)*3, section['own']):
            continue
        if not own:
            add('C_EXPLANATION', section, '未找到作者解释；标题、原题、标签和占位句不能代替讲解', True)
        # 一个连续教学单元统合子步骤；叶节不因共享推导或数字例而反复报缺。
        if section['level'] == 3:
            author = author_text(content)
            formulas = [text for kind, text, _, _, _ in r_blocks(content)[0] if kind == 'formula']
            computational = any(re.search(r'\\(?:frac|sum|sqrt|prod)|[+\-−*/×÷]', formula) for formula in formulas)
            steps = any(NUM_STEP.search(line) for line in content.splitlines() if not line.lstrip().startswith('>'))
            if computational and not steps:
                add('C_CALCULATION_STEPS', section,
                    '本单元有计算公式但未找到数字代入过程；给定结果或API调用不能替代可复算例'
                    + ('。本篇其他单元有代入，请核是否为同一机制及是否需就近回指：'+', '.join(shared_steps) if shared_steps else ''),
                    not shared_steps)
            if formulas and not re.search(r'符号|单位|其中|表示|代表|分别|意味着|是|为|含义', author):
                add('C_SYMBOLS', section, '公式符号/单位解释线索不足，须核具体含义与适用条件')
        # 程序解释接受普通段落、表格、编号步骤与代码注释，不要求固定加粗标题。
        code_pattern = re.compile(r'(?m)^'+chr(96)*3+r'(python|py|sql|bash|sh|r|R)\s*\n([\s\S]*?)^'+chr(96)*3+r'\s*$', re.M)
        for code in code_pattern.finditer(section['own']):
            pre = author_text(section['own'][:code.start()])
            next_code = code_pattern.search(section['own'], code.end())
            post = author_text(section['own'][code.end():next_code.start() if next_code else None])
            comments = re.search(r'(?m)^\s*(?:#|--)\s*\S', code[2])
            if not pre and not comments:
                add('C_CODE_PURPOSE', section, '代码前未找到任务/输入说明或有效行注释', True)
            if not post and not comments:
                add('C_CODE_EXPLANATION', section, '代码后未找到动作/输出/关键行解释', True)
        if own and not re.search(r'因为|因此|所以|为了|避免|否则|意味着|若|如果|不能|误解|失败|作用|对应|输入|输出|这会|使|从而|理由|先|再|更新|取|选择', own):
            add('C_REASONING_REVIEW', section, '找到正文，但理由/过程线索不足；人工核对，不能凭字数断言缺失')
    for item in arithmetic_checks(body):
        item['line'] += offset
        hard.append(item)
    contract = source_contract_checks(body, source_checks)
    hard.extend(contract['hard'])
    if total and not tut:
        declared = sorted(set(int(n) for n in re.findall(r'(\d+)\s*页', frontmatter(t).get('source', ''))))
        ambiguous = bool(declared and (len(declared) > 1 or total not in declared))
        missing = sorted(set(range(1, total+1)) - pages_in(strip_code(body), total) - noncontent_pages(t, total))
        contract['page_references'] = dict(requested_total=total, declared_totals=declared,
                                          status='ambiguous_version' if ambiguous else 'reference_check_only')
        if ambiguous:
            warnings.append(dict(code='C_PAGE_VERSION', section='source/--pages', line=0,
                                 message='页数与source声明冲突或存在多版本，须绑定源版本后逐页核；不把另一版页数套到旧页码。', evidence=str(declared)))
        elif missing:
            hard.append(dict(code='C_PAGE_REFERENCES', section='§2', line=0, message='内容页缺正文页码归属：'+str(missing), evidence=str(missing)))
    # 不持有源题清单时，不能声称排除了漏整题、漏末选项或错抄原文。
    return dict(spec=CURRENT_SPEC, hard=hard, warn=warnings, source_coverage=contract,
                limits=['机检通过不代表解释正确或读者已理解；页码引述不证明该页已实质讲解。',
                        '纯数字等式只核支持的四则/幂/开方及显示精度；不执行代码、不验证符号推导或模型结果。',
                        '无显式源题清单时，无法验证漏整题/原文保真；有清单也只核其字面契约，清单抄写与逐问语义仍需回源。'])


# ---------------------------------------------------------------- 输出
def fmt(v):
    if isinstance(v, (list, tuple)):
        s = json.dumps(v, ensure_ascii=False)
        return s if len(s) <= 160 else s[:157] + '…'
    return str(v)

def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('path', nargs='?'); ap.add_argument('--pages', type=int, default=0); ap.add_argument('--tut', action='store_true')
    ap.add_argument('--json', action='store_true'); ap.add_argument('--strict', action='store_true'); ap.add_argument('--legacy', action='store_true')
    ap.add_argument('--sections', action='store_true'); ap.add_argument('-h', '--help', action='store_true')
    ap.add_argument('--readability', action='store_true'); ap.add_argument('--readability-strict', action='store_true')
    ap.add_argument('--profile', choices=('current', 'historical'), default='current')
    ap.add_argument('--source-checks')
    a = ap.parse_args()
    if a.help: print(__doc__); return 0
    fn = a.path
    if not fn: print(__doc__); return 2
    if a.profile == 'historical' and a.source_checks: print('原题清单须在current模式核对'); return 2
    if not os.path.exists(fn): print('文件不存在:', fn); return 2
    t = io.open(fn, encoding='utf-8').read()
    fm = frontmatter(t)
    tut = a.tut or re.match(r'T\d', os.path.basename(fn)) is not None
    TOTAL = a.pages
    if not TOTAL and not tut:
        mm = re.search(r'（\s*(\d+)\s*页', fm.get('source', ''))
        TOTAL = int(mm.group(1)) if mm else 0
    strict = (a.strict or 'quality_spec' in fm) and not a.legacy
    probs, info = legacy_checks(t, TOTAL, tut)
    res = evaluate_T(t, fn, strict) if tut else evaluate_M(t, fn, TOTAL, strict)
    if res is None: print('找不到 §2 正文，无法评估'); return 2
    historical = dict(spec=SPEC_DATE, G=res['G'], E=res['E'], verdict=res['verdict'])
    C = None
    if a.profile == 'current':
        C = assess_current(t, fn, TOTAL, tut, a.source_checks)
        res['G'] = {}
        res['E'] = [(x['section'], '待核线索', [x['message']]) for x in C['warn']]
        res['verdict'] = 'FAIL（现行内容阻塞%d项）' % len(C['hard']) if C['hard'] else 'PASS（机器可验证项；仍须教学、计算运行与原题回源核对）'
        if probs: res['verdict'] = 'FAIL（L格式问题%d项）' % len(probs)
        if tut and 'code_cells' in res['summary']:
            res['summary']['code_blocks_observed'] = res['summary'].pop('code_cells')

    print('=' * 100)
    print('笔记质量量表  ', os.path.basename(fn), '  模式:', a.profile + ('/strict' if strict else '/legacy'), '  status:', fm.get('status', '?'))
    print('-' * 100)
    print('【L 合规检查】')
    for k, v in info.items(): print('  ', k, ':', fmt(v))
    for p in probs: print('   ✗', p)
    if not probs: print('   ✓ 七项无问题（L1 未讲解页见上，封面/目标页允许）')
    if a.profile == 'historical':
        print('【G 硬门槛】')
        for k, (val, ok) in res['G'].items():
            mark = '✓' if ok else ('—' if ok is None else '✗')
            print('   %s %-42s %s' % (mark, k, fmt(val)))
        print('【E 元素清单】 %s' % ('计入判定' if strict else '只报 WARN'))
        if not res['E']: print('   ✓ 全部小节元素齐全')
        for num, ty, miss in res['E']:
            print('   %s §%s [%s] %s' % ('✗' if strict else '△', num, ty, '；'.join(miss)))
    else:
        print('【现行内容检查】字数/固定标签/类比配额不计FAIL')
        for x in C['hard']: print('   ✗ %s 行%s §%s %s' % (x['code'], x['line'] or '—', x['section'], x['message']))
        for x in C['warn']: print('   △ %s 行%s §%s %s' % (x['code'], x['line'] or '—', x['section'], x['message']))
        if not C['hard']: print('   ✓ 未报确定性阻塞；不是教学完整证明')
        print('   原题清单:', C['source_coverage']['status'], '核对题数:', C['source_coverage']['checked_questions'])
        for limitation in C['limits']: print('   范围:', limitation)
        print('   历史G/E统计已保存；查看旧配额详情用 --profile historical')
    if a.sections:
        print('【逐小节明细】')
        hdr = (['num', 'type', 'cjk', 'own_cjk', 'bq_ratio', 'terms', 'pages', 'need_cjk', 'alt_angles', 'misc_n', 'misc_reason', 'formula_n', 'numex_step', 'has_so', 'first_kind'] if a.profile == 'historical' else ['num', 'cjk', 'pages', 'formula_n', 'numex_step', 'first_kind'])
        print('   ' + ' | '.join(hdr))
        for r in res['rows']:
            print('   ' + ' | '.join(str(r.get(h, '') if h != 'pages' else len(r.get('pages', []))) for h in hdr))
    # ---- R 可读性层：frontmatter 有 readability_rules 或 --readability-strict 时计入判定（readability_spec 已被 sentence-table-v1 占用）；否则只报告
    r_version = fm.get('readability_rules', '').split('#', 1)[0].strip().strip('\"\'')
    if r_version and r_version not in ('v1', 'v2'):
        print('readability_rules 版本无效:', r_version, '（允许 v1 / v2）'); return 2
    r_strict = a.readability_strict or r_version in ('v1', 'v2')
    R = readability_checks(t, tut, fn)
    print('【R 可读性】 %s（规则：_meta/可读性总规则.md）' % ('计入判定' if r_strict else '只报告，不改变判定'))
    st_ = R['stats']
    print('   语义检查仅为 △ 疑点；PASS 不表示读者已理解。')
    print('   表格: 最多 %d 列，最大单元格 %d 单元（行 %s）' % (
        st_['table_max_columns'], st_['table_max_cell_units'], st_['table_max_cell_line'] or '—'))
    if st_.get('sentences'):
        print('   句长（阅读单元）: %d 句  均值 %s  中位 %s  p90 %s  最长 %s  >80: %d（%.1f%%）  >120: %d  豁免块: %d' % (
            st_['sentences'], st_['mean'], st_['p50'], st_['p90'], st_['max'], st_['over80'], 100 * st_['long_share'], st_['over120'], st_['exempt']))
    cnt_h = collections.Counter(c for c, _, _ in R['hard']); cnt_w = collections.Counter(c for c, _, _ in R['warn'])
    print('   ✗ %d 项  △ %d 项' % (len(R['hard']), len(R['warn'])))
    for code, name in R_CODE.items():
        if cnt_h[code] or cnt_w[code]: print('     %-4s %-14s ✗ %-4d △ %d' % (code, name, cnt_h[code], cnt_w[code]))
    shown = R['hard'] if a.readability else R['hard'][:12]
    for code, ln, d in shown: print('   ✗ %s 行%s %s' % (code, ln or '—', d))
    if not a.readability and len(R['hard']) > 12: print('   …其余 ✗ %d 项与全部 △ 用 --readability 查看' % (len(R['hard']) - 12))
    if a.readability:
        for code, ln, d in R['warn']: print('   △ %s 行%s %s' % (code, ln or '—', d))
    if r_strict and R['hard'] and res['verdict'].startswith('PASS'):
        res['verdict'] = 'FAIL（R 可读性 ✗ %d 项）' % len(R['hard'])
    elif r_strict and R['hard']:
        res['verdict'] += ' + R 可读性 ✗ %d 项' % len(R['hard'])
    s = res['summary']
    print('【汇总】', {k: v for k, v in s.items() if k != 'file'})
    print('【判定】', res['verdict'], '' if not probs else ' + L 合规问题 %d 条' % len(probs))
    print('【教学边界】本脚本未评估教学可读性；须独立子代理按高中知识起点审查，零报错不能作为教学质量指标。')
    print('=' * 100)
    if a.json:
        out = dict(file=fn, profile=a.profile, teaching_assessment='not_assessed_by_script', C=C, historical=historical, verdict=res['verdict'], legacy_problems=probs, legacy_info=info, G={k: [v[0], v[1]] for k, v in res['G'].items()},
                   E=res['E'], summary=s, sections=[{k: v for k, v in r.items() if k != 'first_para'} for r in res['rows']],
                   R=dict(strict=r_strict, stats=st_, hard=R['hard'], warn=R['warn']))
        print('JSON:' + json.dumps(out, ensure_ascii=False, default=str))
    return 0 if res['verdict'].startswith('PASS') and not probs else 1

if __name__ == '__main__':
    sys.exit(main())
