from pathlib import Path
import sys,json,re,hashlib,collections
sys.dont_write_bytecode=True
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
OUT=Path(__file__).parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):atomic_write(str(OUT/name),json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
base=json.loads((OUT/'baseline.json').read_text(encoding='utf-8'))
course=Path('D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance')
now={str(p.relative_to(course)):sha(p) for p in course.rglob('*') if p.is_file()}
before=base['course_files']
integrity={'changed':[p for p in before.keys()&now.keys() if before[p]!=now[p]],'added':sorted(now.keys()-before.keys()),'removed':sorted(before.keys()-now.keys()),'old_inputs_changed':[p for p,h in base['old_inputs'].items() if sha(Path(p))!=h],'scope':'Read-only whole-course baseline comparison; no shared manifest or formal files written.'}
put('integrity-comparison.json',integrity)
text=(OUT/'candidate.md').read_text(encoding='utf-8')
heads=set(re.findall(r'^#{1,4} (.+)$',text,re.M))
links=re.findall(r'\[\[#([^|\]]+)\\\|[^\]]+\]\]',text)
missing_anchors=[l for l in links if l not in heads]
image_links=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text)
quality=json.loads((OUT/'quality-v3.txt.parsed.json').read_text(encoding='utf-8'))
manifest=json.loads((OUT/'source-checks.json').read_text(encoding='utf-8'))
summary={'candidate_sha256':sha(OUT/'candidate.md'),'candidate_bytes':len(text.encode('utf-8')),'pages_actually_viewed':14,'questions':len(manifest['questions']),'answer_units':sum(len(q['answers']) for q in manifest['questions']),'MC_options':sum(len(q['options']) for q in manifest['questions']),'source_contract':quality['C']['source_coverage'],'C_hard':quality['C']['hard'],'C_warn_count':len(quality['C']['warn']),'R_hard':quality['R']['hard'],'R_warn_count':len(quality['R']['warn']),'R_warn_by_code':dict(collections.Counter(x[0] for x in quality['R']['warn'])),'internal_anchor_count':len(links),'missing_internal_anchors':missing_anchors,'image_links':image_links,'missing_images':[x for x in image_links if not (OUT/x).exists()],'integrity':integrity,'teaching_assessment':'pending independent review','official_answer':'not obtained; absence of publication not asserted','final_display':'UI prohibited for this task; final Markdown/Obsidian/browser display not performed','writes':'scratch-only; no course, Notion or Git changes by this author'}
put('author-summary.json',summary)
assets=[]
for name in ['b2-loss.svg','b2-loss.png','compute.py','computation-results.json','page-evidence.md','source-checks.json','questions-extracted.json','reuse-audit.json']:
    assets.append({'file':name,'sha256':sha(OUT/name),'role':'source/computation/author evidence; not acceptance'})
put('assets.json',assets)
lines=['# Practice Exam A · 作者集中自查（未独审）','',f'当前候选 SHA `{sha(OUT/"candidate.md")}`。冻结后不修改正文；问题待同一批缺陷修复。','', '## 真实修复','', '- 旧 B1(a) 等金额多空示例直接报约 −15% 缺资本分母。改为 100 元资本各 50 元，PDD −20%/JD −5% 对应 −7.5 元/−7.5%；−15 个百分点是股票收益差。', '- 旧JSON公式反斜线过度转义，按实际LaTeX恢复；正文额外明确系数×A的乘法。', '- 第一轮机械发现 C1 原题表旁中文说明打断完整原题契约、导航单元格分号被当多句等；保留原输出，调整为完整引用表与简洁分问速查，不改任何源数值。', '- 第二轮仅余原题引用表的表前说明启发式；改用原题所属的Markdown引用语义，不把原题当作者无说明表。第三轮 current/strict/source-checks exit 0。原题契约只核字面，源与答案语义仍待独审。','', '## 数学复算','', '- A4：拟合0.20%→3.20%，增3.00个百分点。', '- A5：费用0.06%，净均值0.24%，周夏普0.08；A6总100%/净20%。', '- A16：净年贡献率0.003，AUM2亿美元；四选项均回代年度利润核对。', '- B4：200万×80%−130万=30万元人民币，严格限定完整最新融资记录。', '- C1：SSE=.0004/.0018、R²=7/9；C2费用80、净拨款1920、贡献20→−5港元。', '- 补充例/变式另有计算，不冒称原数据或真实市场表现。脚本及输入输出都在本目录。','', '## C.warn（逐位置）','']
for w in quality['C']['warn']:lines.append(f'- 行{w["line"]} {w["section"]}：{w["message"]}')
lines+=['','处置依据：p1/2.0为卷面制度/指令，已在相邻中文解释行动；9.2是核验事实说明，不承担题目机制。作者判定不需为行政事项造算例，但不替代独审。','', '## R.warn（合并说明、列齐位置）','']
by=collections.defaultdict(list)
for code,line,desc in quality['R']['warn']:by[code].append((line,desc))
for code,items in by.items():
    lines += ['### '+code,'','涉及行：'+', '.join(str(i[0]) for i in items)+'。']
    lines += [f'- {line}：{desc}' for line,desc in items]
    lines += ['']
lines+=['## 不能批量当作已关闭的部分','', '- R6d有原题缩写、金融模型、资产/法庭外术语等不同类别；A1–A16/B/C正文已按当前任务解释，仍交独审逐单元判断桥梁是否足够，不能用词表替代。', '- R4f要求读者能解释表的一行、单位和分母；本稿多处已设定并走例，但最终表宽与引用内表实际显示未核。', '- R5等提示可能由同一算例中多个公式引发；符号/单位/数字已配桥梁，公式显示仍待最终载体。', '- R8a的13处多为非源页推理的答题/复习子节或分问标题；主问题已带页号，§8按源页全列。保留原位置供独审核。', '- 不宣称所有警告都是误报，更不因此标教学通过。','', '## 真实材料缺口而非算术阻塞','', '- 未取得官方答案/评分rubric，且未查当前Canvas发布状态。', '- 最终期末通知未重核；卷封面要求仅作为本练习事实。', '- 不能从题面估计真实托管回收率、个体排序统计显著、B1因果效应、B4现实债务完整性或净策略利润。', '- 无需为完成固定计算而强求未给行情、MA12历史原数或真实BNPL财报。', '', '## 最终状态', '', '原题来源14页已实看，数值已作者复算，候选未被接受。独立审查、最终阅读载体显示及正式发布门槛仍待执行；不写passed回执。']
atomic_write(str(OUT/'author-self-check.md'),'\n'.join(lines)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
