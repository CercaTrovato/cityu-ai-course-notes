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
    --readability         打印 R 可读性层的全部 ✗ 与 △（默认只列前 12 条 ✗ 与分项计数）
    --readability-strict  R 层 ✗ 计入 FAIL（frontmatter 的 readability_rules 为 v1 / v2 时也启用）

退出码：0 = PASS，1 = FAIL，2 = 文件/参数错误。

R 可读性层（2026-10-08，规则与阈值见《_meta/可读性总规则.md》；存量笔记只报告，不改变 L/G/E 判定）
  阅读单元：汉字 / 可见标点各 1；连续英文单词或数字串 1；行内公式、行内代码各 2；Markdown 标记不计
  R1 句子：单句 >120 ✗、>80 △；全篇 p90 >60 或 >80 长句占比 >3% ✗；一句 ≥2 分号 △；括号插入 >30 △；一段否定澄清 ≥4 ✗ / 3 △
  R2 段落：>200 单元或 ≥7 句 ✗，>150 或 6 句 △；列表项 >150 ✗ / >80 △；段内 ①②③ ≥3 ✗；段内加粗 ≥4 △
  R3 版面：无标题/标签/表/公式隔断的连续正文 >800 ✗ / >500 △；##### 及以下标题 ✗；表格紧贴上一行文字 ✗
  R4 表格：列 ≥9 ✗ / 7–8 △；单元格 >80 ✗ / >40 △；单元格 ≥3 句 ✗ / 2 句 △；§2 表格前无引导文字 ✗；一行 >200 △（页码映射区只报 △）
  R5 公式代码：一段 ≥6 个不同行内公式 ✗ / 4–5 △；一个 $$ 块多个等式 △；行内公式 >60 字符 △；代码块 >30 行 △；“.5” 式小数 ✗
  R6 术语：一段 ≥3 处括号英文注释 △        R7 分层：主线出现 6 位以上小数 / 绝对路径 / 哈希 / ≥3 时间戳 △；段内长英文原话 △
  R8 场景：§2 的 ###/#### 标题缺 p.页码 △；小节首段 ≥4 句 △
  范围：§0–§7 与 T 笔记主体；「页码映射」区只查表格（降为 △）；「延伸与勘误」区与标题含复算/来源/核验的 <details> 只查渲染（R3c）
  豁免：块前一行写 <!-- 可读性豁免: 理由 -->，该块不检查但计入「豁免块」数；超过 5 块报 ✗
  v2（2026-10-09）：R4f/g、R6b/c/d、R8c 是启发式疑点，只报 △，须人工核对。
  识别到定义词、冒号或格式，只代表找到解释线索，不代表解释正确完整。

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
import re, io, sys, os, json, collections, argparse, glob

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
            hm = re.match(r'^#+\s*(\d+(?:\.\d+)*)', s); sec = hm.group(1) if hm else sec
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
    ap.add_argument('--readability', action='store_true'); ap.add_argument('--readability-strict', action='store_true')
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
    print('=' * 100)
    if a.json:
        out = dict(file=fn, verdict=res['verdict'], legacy_problems=probs, legacy_info=info, G={k: [v[0], v[1]] for k, v in res['G'].items()},
                   E=res['E'], summary=s, sections=[{k: v for k, v in r.items() if k != 'first_para'} for r in res['rows']],
                   R=dict(strict=r_strict, stats=st_, hard=R['hard'], warn=R['warn']))
        print('JSON:' + json.dumps(out, ensure_ascii=False, default=str))
    return 0 if res['verdict'].startswith('PASS') and not probs else 1

if __name__ == '__main__':
    sys.exit(main())
