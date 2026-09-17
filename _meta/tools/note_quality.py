# -*- coding: utf-8 -*-
"""
note_quality.py — CityU 课程笔记质量量表（《_meta/笔记质量规范.md》的执行脚本）

用法
    PYTHONIOENCODING=utf-8 /d/anaconda3/python.exe _meta/tools/note_quality.py <笔记路径> [--pages N] [--tut] [--json] [--strict|--legacy] [--sections]

    --pages N   讲义总页数（省略时从 frontmatter `source:` 的「（NN 页）」读）
    --tut       T 系列（notebook 逐块讲解）笔记，走 T 指标集
    --json      额外输出机器可读 JSON（stdout 末尾一行，以 `JSON:` 开头）
    --strict    元素清单 E 计入 PASS/FAIL（默认：frontmatter 有 `quality_spec:` 字段时自动 strict）
    --legacy    强制 legacy 模式（E 只报 WARN）
    --sections  打印逐小节明细表（默认只打印不达标小节）

退出码：0 = PASS，1 = FAIL，2 = 文件/参数错误。

判定分三层（详见《笔记质量规范》§3）：
  L  合规检查（原 notecheck.py 七项，逐条列出问题；有问题时退出码 1）
       L1 逐页覆盖（§2 正文里 p.N 引用覆盖到每一页；封面/目标页允许）  L2 伪公式（代码块 / 行内代码里的数学字符）
       L3 表格：管道数不一致 / 公式含裸竖线 / 双链别名未转义；未转义货币 $      L4 标题含 | [ ] ^ * ` 等特殊字符
       L5 代码围栏成对、<details> 配对    L6 同文件锚点 [[#…]] 能对上标题    （原 ⑦ 小节首元素并入 G3a）
  G  硬门槛（任一不过即 FAIL；阈值来自 2026-09-16 校准，见规范附录 A）
       G1  §2 中文字数 / 内容页 ≥ 250                    G2a §5 术语数 / leaf 小节 ≤ 1.6
       G2b 内容页 / leaf 小节 ≤ 2.5                       G2c 承载术语的 leaf 小节 ≥ 150 字
       G3a 小节首元素是段落（不是表格 / 公式 / 代码）        G3b 每个 $$ 公式的符号都有着落（符号表 / 散文点名 / 前文已解释 / 自注释 / 纯数字代入）
       G3c 有公式的小节有数字例子                          G3d 每个 python/sql/bash 代码块前有「在做什么」、后有逐行说明
       G6  每个 ### 单元（含其 #### 子节）至少一处「所以呢」，覆盖率 ≥ 0.80
       T 笔记：G1t 逐块讲解中文字数 / code cell ≥ 350；G3a；G3d 缺失率 ≤ 0.20
  E  元素清单（规范 §5 每型概念的必备元素 + §6 术语首现 + §4 先修唤醒）
       strict 模式（frontmatter 有 quality_spec: 或 --strict）计入 FAIL；legacy 模式只报 △ WARN，判定写「PASS（存量宽限）」

指标定义
  内容页            = 讲义总页数 − §8 表里小节列为「—（封面）」等、或备注含「封面 / 章节标题页 / 学习目标页 / 行政页 / 安装截图页 / 空白页 / 分隔页」的页
  leaf 小节         = §2 里的 ###/#### 标题块，去掉纯容器（正文 < 60 中文字）
  cjk              = 小节非代码、非标题行的中文字符数；own_cjk = 其中普通段落（不含引用块 / 表格 / 公式）的中文字数
  bq_ratio         = 引用块字符 / 小节非代码字符（只报告，不作门槛：校准显示它不区分好坏）
  术语数            = §5 术语卡「首现」列落在该小节的行数（首现指向容器节时平摊给子节）
  小节类型          = 标题/内容启发式（公式型 / 算法流程型 / 对比型 / 案例数据型 / 图表读法型 / 勘误型 / 代码型 / 行政型 / 定义型），可在小节标题下一行用
                     <!-- 类型: 公式型 --> 显式指定
  换个说法角度        = 「💡 换个说法」块里 ≥ 40 字的独立段落或列表项数（标签行不算）
  常见误解条数/带理由   = 「⚠️ 常见误解」块里 ❌ 条数 / 其中 ❌ 之后含 → —— 因为 其实 … 等理由标记的条数
  数字例子           = 小节普通段落或表格里出现 = ≈ × + − 接数字、小数或千分位数字；numex_step = 含算式（两数相乘/相减/连等）的行数
  术语首现解释率      = §5 每个术语在其「首现」小节里：标题含该术语，或首次出现处 40 字内有括号 / 定义词（是、指、即、就是…）/ 4 行内出现英文名
  先修概念唤醒        = PREREQ 词典（统计 101 / 线代 / 微积分）里的词在 §2 首次出现处：25 字内有括号、或同行有 [[回指]] / §x 指向、或该词在 §1.1 表 / §5 术语卡里
  需补字数（估算）     = max(0, 250 × 该小节覆盖页数 − 该小节 cjk)，只用于返工清单排序
"""
import re, io, sys, os, json, collections, argparse

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
        m = re.search(r'§\s*(\d+(?:\.\d+)*)', cells[-1])
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
SUBJ = re.compile(r'^\d+(?:\.\d+)*')

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
        if not re.match(r'^\s*```(python|py|sql|bash|sh|r|R)', lines[a]): continue
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
            mm = re.match(r'^#+\s*(\d+(?:\.\d+)*)', l); cur = mm.group(1) if mm else cur
        sec_of[i] = cur
    heads_by_sec = {}
    for i, (l, k) in enumerate(zip(lines, kinds)):
        if k == 'head':
            mm = re.match(r'^#+\s*(\d+(?:\.\d+)*)', l)
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

# ---------------------------------------------------------------- 输出
def fmt(v):
    if isinstance(v, (list, tuple)):
        s = json.dumps(v, ensure_ascii=False)
        return s if len(s) <= 160 else s[:157] + '…'
    return str(v)

def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('path'); ap.add_argument('--pages', type=int, default=0); ap.add_argument('--tut', action='store_true')
    ap.add_argument('--json', action='store_true'); ap.add_argument('--strict', action='store_true'); ap.add_argument('--legacy', action='store_true')
    ap.add_argument('--sections', action='store_true'); ap.add_argument('-h', '--help', action='store_true')
    a = ap.parse_args()
    if a.help: print(__doc__); return 0
    fn = a.path
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
    print('=' * 100)
    print('笔记质量量表  ', os.path.basename(fn), '  模式:', 'strict' if strict else 'legacy', '  status:', fm.get('status', '?'))
    print('-' * 100)
    print('【L 合规检查】')
    for k, v in info.items(): print('  ', k, ':', fmt(v))
    for p in probs: print('   ✗', p)
    if not probs: print('   ✓ 七项无问题（L1 未讲解页见上，封面/目标页允许）')
    print('【G 硬门槛】')
    for k, (val, ok) in res['G'].items():
        mark = '✓' if ok else ('—' if ok is None else '✗')
        print('   %s %-42s %s' % (mark, k, fmt(val)))
    print('【E 元素清单】 %s' % ('计入判定' if strict else '只报 WARN'))
    if not res['E']: print('   ✓ 全部小节元素齐全')
    for num, ty, miss in res['E']:
        print('   %s §%s [%s] %s' % ('✗' if strict else '△', num, ty, '；'.join(miss)))
    if a.sections:
        print('【逐小节明细】')
        hdr = ['num', 'type', 'cjk', 'own_cjk', 'bq_ratio', 'terms', 'pages', 'need_cjk', 'alt_angles', 'misc_n', 'misc_reason', 'formula_n', 'numex_step', 'has_so', 'first_kind']
        print('   ' + ' | '.join(hdr))
        for r in res['rows']:
            print('   ' + ' | '.join(str(r.get(h, '') if h != 'pages' else len(r.get('pages', []))) for h in hdr))
    s = res['summary']
    print('【汇总】', {k: v for k, v in s.items() if k != 'file'})
    print('【判定】', res['verdict'], '' if not probs else ' + L 合规问题 %d 条' % len(probs))
    print('=' * 100)
    if a.json:
        out = dict(file=fn, verdict=res['verdict'], legacy_problems=probs, legacy_info=info, G={k: [v[0], v[1]] for k, v in res['G'].items()},
                   E=res['E'], summary=s, sections=[{k: v for k, v in r.items() if k != 'first_para'} for r in res['rows']])
        print('JSON:' + json.dumps(out, ensure_ascii=False, default=str))
    return 0 if res['verdict'].startswith('PASS') and not probs else 1

if __name__ == '__main__':
    sys.exit(main())
