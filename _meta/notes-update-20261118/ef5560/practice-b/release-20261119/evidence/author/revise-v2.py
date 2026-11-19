from pathlib import Path
import hashlib,re,json,difflib,shutil
d=Path(__file__).resolve().parent; old=d/'candidate.md'; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(old)=='16739080ea24d74068d2379871988cf261653154e1c5df545ef7f0471cc9ff64'
t=old.read_text('utf-8'); initial=t
t=t.replace('type: practice-exam-learning-analysis','type: practice-guide\nassignment: Practice-Exam-B-learning-analysis\nreadability_rules: v2\nteaching_standard: novice-v1')
wrong='例如报告写收入500百万元，误录为500元，会把比率和模型输入缩小一百万倍。'
right='例如报告写收入500百万元，误录为500元，绝对金额输入会缩小一百万倍。比率要另核分子、分母的单位：如果两边同样按一百万倍缩小，比率不变；如果只有分子缩小、分母保持原单位，比率才会缩小一百万倍。不能把单位错误对所有比率的影响一概而论。'
assert t.count(wrong)==1;t=t.replace(wrong,right)
t=t.replace('描述市场暴露，$\\alpha$ 是控制这项暴露后剩余的平均表现；不是保证未来额外赚钱。','描述市场暴露，$\\alpha$ 是控制这项暴露后剩余的平均表现；不是保证未来额外赚钱。')
t=t.replace('**参考答案 B。** 资本资产定价模型（Capital Asset Pricing Model，CAPM）的评估回归可写成 $r_p-r_f=\\alpha+\\beta(r_m-r_f)+\\epsilon$。$r_p$ 是组合收益，$r_f$ 是同期无风险收益，$r_m$ 是市场收益。$\\beta$ 描述市场暴露，$\\alpha$ 是控制这项暴露后剩余的平均表现；不是保证未来额外赚钱。','**参考答案 B。** 资本资产定价模型（Capital Asset Pricing Model，CAPM）的评估回归可写成 $r_p-r_f=\\alpha+\\beta(r_m-r_f)+\\epsilon$。\n\n$r_p$ 是组合收益，$r_f$ 是同期无风险收益，$r_m$ 是市场收益。\n\n$\\beta$ 描述市场暴露，$\\alpha$ 是控制这项暴露后剩余的平均表现；不是保证未来额外赚钱。')
t=t.replace('缺失值不能当零。例如报告写收入500百万元','缺失值不能当零。\n\n例如报告写收入500百万元')
t=t.replace('一概而论。错误数据会使预测关系失真','一概而论。\n\n错误数据会使预测关系失真')
t=t.replace('## 阅读入口与状态','''## 0. 三分钟速览

这是一份按原题条件推理的参考学习稿，不是官方答案或学生提交稿。

- A区16题：每题保留A–D并逐项解释。
- B区4题、C区2题：每题各两小问，分别给中文过程与英文参考作答。
- 共22大题、28作答单元；原卷14页全部保留，13–14为草稿纸。
- 预习看§1及§2当地解释；课中/复做按§8定位；复习用§3–§7，不替本人勾选已学会或已交。

## 1. 阅读入口与状态''')
t=t.replace('## 按页对照','## 2. 按原页对照 · 原题与学习解析')
lines=t.splitlines(); page=0; count=0; pageheads={}
for i,s in enumerate(lines):
 m=re.match(r'## p\.(\d+) · (.*)',s)
 if m:
  page=int(m.group(1));count=0;lines[i]=f'### 2.{page} p.{page} · {m.group(2)}';pageheads[page]=lines[i][4:]
 elif re.match(r'### [ABC]\d+',s):
  count+=1;lines[i]=f'#### 2.{page}.{count} '+s[4:]
t='\n'.join(lines)+'\n'
t=t.replace('## 复习索引与最容易错的桥梁','''## 3. 一图看懂 · 四层证据

| 从题面走向结论 | 先确定的对象 | 不能直接跳到什么 |
|---|---|---|
| 统计/预测 | 系数检验、样本内误差、未见测试误差 | 因果、未来必赚 |
| 金融计算 | 收益目标、分母、总量与每股量 | 数字近似就认为口径相同 |
| 账本/代币 | 记录、底层资产、权利与完成时点 | 储备必足、现金必到账 |
| 运营保障 | 可用信息、权限隔离、实际恢复验证 | 有文件/有备份即安全 |

三个当地流程图分别在B1(a)的信息时点、B2(a)的条件树和B4(b)的恢复链，不能互相代替。

## 4. 速查与答案索引''')
extra='''## 5. 双语术语速查

定义只作回忆，具体对象和分母仍以§2各题为准。

| 中文 | English | 当前意思 |
|---|---|---|
| 超额收益 | excess return | 股票/组合收益减匹配无风险收益 |
| 最大回撤 | maximum drawdown | 先前峰值到后续低点的最大比例跌幅 |
| 校准 | calibration | 报出的概率与实际发生比例是否匹配 |
| 前视偏差 | look-ahead bias | 决策使用当时还不可得的信息 |
| 留存收入 | retained revenue | 本题手续费减指定转付款，尚未扣其他成本 |
| 净资产值 | net asset value (NAV) | 资产减负债；每股值还要除股数 |
| 首损保证 | first-loss guarantee | 先承担约定额度内损失，不是包赔全部 |
| 标准化 | standardization | 以开发样本均值与标准差定义输入尺度 |

## 6. 英文作答框架与边界

选择题先给字母，再说题面哪条条件决定它；不能只有字母而不懂理由。计算题按“量与单位→公式→代入→结果→解释”写。简答题若问two checks，就明确分两项并分别解释为什么；若问guarantee，就说明条件为何不足以保证。

英文框架（笔记自拟）：The relevant quantity is … . Using the stated inputs and assumptions, … . This supports … but does not establish … . 正文28个单元各有具体英文答案，框架不替代逐题作答。任何合理参考答案都不自动等于官方评分要点。

'''
t=t.replace('## 改条件自测（笔记自拟，非原卷题）',extra+'## 7. 改条件自测（笔记自拟，非原卷题）')
mapping='## 8. 原页与正文精确映射\n\n| 物理页 | 题目/身份 | 正文入口 |\n|---|---|---|\n'
topics={1:'封面与原始卷面规则',2:'A1–A3',3:'A4–A6',4:'A7–A9',5:'A10–A12',6:'A13–A16',7:'B1(a)(b)',8:'B2(a)(b)',9:'B3(a)(b)',10:'B4(a)(b)',11:'C1(a)(b)',12:'C2(a)(b)',13:'草稿纸，无新增题',14:'草稿纸，无新增题'}
for p,h in pageheads.items():mapping+=f'| p.{p} | {topics[p]} | [[#{h}\\|p.{p} 正文]] |\n'
t=t.replace('## 核对范围与待补',mapping+'\n## 9. 核对范围与待补')
write=lambda p,v:p.write_text(v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(d/'candidate-v2.md',t)
write(d/'candidate-v1-to-v2.diff',''.join(difflib.unified_diff(initial.splitlines(True),t.splitlines(True),fromfile='candidate.md',tofile='candidate-v2.md')))
write(d/'revision-v2.json',{'old_sha256':sha(old),'new_sha256':sha(d/'candidate-v2.md'),'semantic_change':{'id':'P1','location':'B1(b), now 2.7.2','old':wrong,'new':right,'english_answer':'unchanged; general unit/source reconciliation remains accurate'},'nonsemantic_structure':'Existing page headings under §2 and question headings numbered; existing reading/index/selftest/boundaries moved to §§1/4/7/9. All source text, images and all answers otherwise unchanged. New §§0/3/5/6/8 are navigation/recap derived from existing explanations, not new official content.','status':'requires same-reviewer targeted semantic and structure check; no self-approval'})
print(sha(d/'candidate-v2.md'))
