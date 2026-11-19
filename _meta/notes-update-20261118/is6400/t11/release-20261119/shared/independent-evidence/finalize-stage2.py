from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,inspect,numpy as np,sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import f_classif
from sklearn.preprocessing._data import _is_constant_feature
W=Path(__file__).parent.parent;O=Path(__file__).parent;R=Path('D:/上课资料/CityU');P=R/'_meta/notes-update-20261118/is6400/t11'
sys.path.insert(0,str(R/'_meta/tools'));from safe_write import atomic_write
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name,t):
    p=O/name;assert not p.exists();atomic_write(str(p),t);assert p.read_bytes()==t.encode('utf-8')
def js(name,v):write(name,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
s=StandardScaler().fit([[2],[4]]);changed=StandardScaler().fit([[3],[7]]);constant=StandardScaler().fit([[5],[5]])
js('stage-2-installed-api-probes.json',{'python':sys.version,'sklearn':sklearn.__version__,'numpy':np.__version__,'installed_StandardScaler_source':inspect.getfile(StandardScaler),'source_sha256':sha(inspect.getfile(StandardScaler)),'ddof0_in_installed_doc':('ddof=0' in StandardScaler.__doc__),'near_constant_rule_source':inspect.getsource(_is_constant_feature),'example':{'train':[2,4],'mean':s.mean_.tolist(),'var':s.var_.tolist(),'scale':s.scale_.tolist(),'validation_6_z':s.transform([[6]]).tolist()},'changed_example':{'train':[3,7],'mean':changed.mean_.tolist(),'scale':changed.scale_.tolist(),'validation_9_z':changed.transform([[9]]).tolist()},'constant_example':{'var':constant.var_.tolist(),'scale':constant.scale_.tolist()},'F_example':f_classif([[1],[2],[5],[6]],[0,0,1,1])[0].tolist(),'execution':'new reviewer library probes only; no source tutorial33cell rerun, no changes to any learner source/output'})
receipt=json.loads((O/'stage-2-source-receipt.json').read_text(encoding='utf-8'));replay=json.loads((O/'stage-2-new-replay-verification.json').read_text(encoding='utf-8'))
now=datetime.now(timezone.utc).isoformat()
report='''# T11 / A12 独立第二阶段：回源与局部修复关闭

## 本次实际身份、范围与结论

审查者 `/root/cityu_is5113_package`，作者 `/root/is6400_update`。未参加本包创作；独立第一阶段完整顺读已先冻结，之后root明确授予来源及旧审查材料，才开展本阶段。第一阶段披露的其他课程规则暴露、原文及算术精度补记均保留，不补造完全盲审历史。原审者不能恢复，本报告是另一位独立代理基于自己的新第一阶段及实际回源作出的关闭判断，不伪署原审者。

最终受审候选：

- T11 `5c3b876cc27a1951b7eca79d32bc13da1ef84e88173530b9320ddfbf056312be`，91554字节。
- A12学习参考 `13f1a87de7503d84135de9f4709fbe0b4e3ba3a6423f3754d7cfae2ac3ead7bd`，18855字节。
- 真实Notebook `a1b85cb3d817cf64e5fbe2ccc7fbdbf86c99f3bf76834f2e09269e10dd0c17a2`。

**独立教学结论：passed。旧B1、B2、B3均已关闭，没有发现其他实质教学阻塞。** 本结论结合本代理Stage1全篇学习动作、当前全部63cell源向对照、13张实际图像、真实代码/数据角色检查及本次新A12复跑。不是以旧passed、作者运行0error或机械分数替代实读。

**最终发布显示仍由root实际验收。** 本阶段用view_image看源资产，不冒称浏览器/Obsidian/KaTeX/Mermaid已显示通过；正式门槛、CAS写回、跨文件/Notion/Git/看板也不由本报告代办。没有改任何旧报告、候选、原件、正式文件或本人字段。

## 一、从真实源反查全部63格

直接读取原Notebook JSON：63cells＝30markdown＋33code。30个markdown逐个读其原文，不只拿候选标题倒推覆盖；33个源code与第一阶段已完整顺读的对应候选Python块逐一比较，**33/33全文一致**。每个候选都有唯一cell入口，§8的63行能对上本地正文标题。逐格源SHA、入口、代码/保存输出检查见 `stage-2-source-receipt.json` 的63行。

主要源向观察（与Stage1全部学习动作互补）：

| 源cell范围 | 当前源中实际要素及候选处理 |
|---|---|
| 1–4 | 源为Tutorial11 Model Selection；明确“一个模型调参/多个模型选家族”，列5个学习目标、4个API工具，正弦噪声与15幂。候选按T11与理论M10分工，不伪造授课日或教师AI Prompt；源实际没有Prompt格。 |
| 5–12 | 真实seed10、60–296步4、0.15噪声、MinMax训练fit/留出transform、15系数与训练/验证原图原输出。cell8原注释的L2与实际MinMax冲突原样保留并解释；原保存MAE与作者复跑末位差分开。 |
| 13–20 | 源固定Ridge0.1后再0–0.19网格，全部20条保存结果在候选；0.01最小而最后对象0.19，原which alpha问及validation问有直接中英答案。惩罚目标与训练/验证指标未混用。 |
| 21–27 | 源为内置Wisconsin Diagnostic数据和FNA核特征说明，569×30，0恶性/1良性；目标表头Cancer不被误当1恶性；ravel与随机0默认426/143切分代码完全相同，未冒称stratify。 |
| 28–38 | 源path的有效alpha和叶不纯度、13棵候选树、first/index5/last、节点数/深度和截尾。候选没有把路径生成当验证选优；原5th标法明确纠正为第6项；重跑截尾会再删的状态说明真实。cell29只有Text输出，新增曲线不冒充原保存图。 |
| 39–47 | 同乳腺训练侧SVC默认基线、25组合五折GridSearch、refit、best_params C1/gamma.0001、两份报告及原完整对照表/bullet。候选完整保留代码，准确率134/143对135/143、类0precision下降/recall上升而非全涨；继续用留出选择的历史限制合理。 |
| 48–57 | 源含官方StratifiedKFold远程图、Iris相对文件、剥离class、KNN10/DT深10五折、十模型固定配置及完整五分数/弃用警告。候选不把导入Scaler当已缩放，不把图100索引当实际150Iris，不把固定配置比较称充分调参或部署赢家。 |
| 58–60 | 单次100/50留出报告，17/19/14支持数、48/50正确；源micro/macro precision两公式已同义保留，并补充单标签全部类时micro=accuracy及90/10反例，没有改分母。 |
| 61–63 | 源四部分总结、纯分隔、完整三道评分题。两候选中的3问逐字匹配源英文行，40/40/20、default、nested、Please evaluate限制都在；中文解题及英文参考不是官方答案或本人提交。 |

33个code cell的保存文本输出中32个在对应候选完整包含；唯一例外cell44是约125次重复CV日志，候选透明节录并明确完整源位置，没有抹去独有题面/配置/结论。原Notebook内9个PNG从base64重新解码，逐字节与正式图资产匹配。不是仅查图片清单存在。

作者历史`source-run.json`记录33格/0error，本代理核每格source hash与原Notebook一致，也阅读其runner：只去Jupyter魔法、Agg显示保存钩子与尾表达式输出，原数据/模型代码未替换。**本代理没有新执行这33个课堂格**，历史运行事实按原记录引用，不把它写成当前新复跑。真正新增执行的是下述A12持久脚本。

## 二、13张图的实际查看与B3关闭

本阶段逐张用view_image打开正式路径的全部13图：9个原内嵌PNG、cell48官方缓存图、cell29已有复跑曲线、cell33/34已有较清晰复跑图。所有正式图与all-figures清单及来源载体SHA匹配；候选13个图引用存在，另外两个大图打开链接也到达同一正式资产。逐图尺寸、SHA、观察记在新source receipt中。

- cell5黑观测点X约1–5、Y约+1到−1；cell8训练蓝预测/橙真实贴近；cell12右端蓝橙明显偏离；cell14标题lambda0.1且没有图例，按原plot顺序辨认；cell17验证偏差仍可见。与就地图说明一致。
- 原cell33密树515×409确实小字，但新版保留它并在旁嵌入/链接正式`cell-33-recomputed.png`。本阶段在较大载体读到根`x[7]<=0.049`、gini0.468、samples426、value[159,267]，True后x[23]<=952.9、False后x[23]<=785.8，及深处分支/叶value[0,4]与[1,0]。不是用“有较大PNG”推定可读。
- cell34较大图可读根426、True260/[13,247]、x[13]<=42.19、247/[4,243]、False166/[146,20]、x[10]<=0.192等。源图仍题作5-th，但候选就地已说明index5为第6个。未悄悄修改教师原图。
- cell35仅根图保留426与159/267，不含特征规则；cell37节点31→3、深度8→1及平台清楚。cell29曲线从0升至约0.14，末根-only排除的范围符合代码。
- cell48官方图确有0–100示例索引、CV0–4、红Testing/蓝Training与class/group两条；按类分层并未整组隔离的解释符合实际图。

**B3关闭**：现在不是scratch专有“另存”声明；读者从拟发布T11的相对路径能到正式较清晰资产，原图仍保留、新图已明示前次按源代码复跑，不新增训练、不混淆来源。必要节点可辨，原小图限制透明。最终阅读窗口中的嵌入/缩放/点击则仍是root视觉门槛，不能由本次单图查看替代。

## 三、B1真实学习文件/目录/命令与新增独立执行

从拟发布A12学习页位置解析`../work/learning-reference.py`及结果JSON，均实际存在。代码`Path(__file__).resolve().parents[5]`从该A12/work布局确到CityU根；`safe_write`存在；候选PowerShell的Set-Location、解释器`D:/anaconda3/python.exe -X utf8`、无额外参数、同目录结果文件名与真实脚本一致。候选明确再跑会覆盖同名结果并建议先保存副本，不说这一步是上传。

持久脚本SHA：`50c88a8d963d4bb97f554cdbd1090635e2bea8e303cb6f9a7d625f60292f4064`。与历史真实执行版对比仅根/输出路径、去中间进度和结果文件名不同；数据、模型、分折、种子、指标逻辑相同，差异保存在`stage-2-script-path-diff.json`。

**本代理这次实际从持久脚本原路径执行**，不是只沿用旧独立复跑。为不覆盖作者已验证结果，wrapper仅截获唯一预期的最终JSON写入，重定向到当前独审scratch；`__file__`根定位、输入、模型、split和计算不改，其他写目标会拒绝。约15.46秒结束，结果除elapsed_seconds外，与完整已有JSON完全一致，包括各折参数、分数、警告及版本；原结果和脚本SHA执行前后不变。新结果、wrapper和验证在本目录保存。不能据此声称原输出文件被重新写入；保护性重定向事实明确记录。

**B1关闭**：新版§6既给可打开完整脚本/JSON、精确工作目录和命令、输入/输出/覆盖边界，又给真实三行GridSearchCV→fit(X[tr],y[tr])→predict(X[te])及JSON读取入口。读者不需要自行猜第一次怎么跑，且脚本可实际定位/运行。未要求把实验重抄成第二套代码。

## 四、B2标准化与三问数值/数据角色

**B2关闭**：新版§5.1直接说明原值减训练均值再除拟合scale_，给符号、默认ddof0、零/近常数因子1与读取mean_/scale_的操作；[2,4]均值3/方差1→−1,1，验证6→3，改mean5/scale2/值9→2，均可按正文重做，不靠标准差恰1遮掉除法。

本阶段还实际核当前安装sklearn1.5.1的StandardScaler文档/常数检测源码，并执行局部库探针：训练[2,4]的mean3/var1/scale1、[3,7]的mean5/scale2使9→2、常数[5,5]的scale1，以及f_classif两组[1,2]/[5,6]得F32。证据见`stage-2-installed-api-probes.json`。这是当前新增局部执行，不是重跑33格，也不引用官网stable新版本覆盖本地实现。

新独立A12完整执行核实：

| 比较 | 实际核对与结论 |
|---|---|
| Q1 | 569×30，类数212/357；相同426/143、未stratify，默认构造器及fit前外部NumPy seed20261118。错数19/4/9，RF错误4/143≈0.027972最小；恶性recall分别约0.943396/0.981132/0.849057。 |
| Q2 | 外层固定三折379/190、379/190、380/189；内层只接本外训。DT/RF/SVC外层均值0.927959/0.957839/0.940230，样本SD0.010823/0.009020/0.011102，与候选六位表一致；外层与inner_best_score没有偷换。 |
| Q3 | SelectKBest→StandardScaler→model随每个内训拟合，赢家在本外训refit；DT/RF/SVC均值0.915632/0.947257/0.975411。RF下降0.010582，不能采纳为改善原赢家；SVC三折k=all，不把其提升归因于删列。 |
| 预算与统计 | 每家族Q2为39次fit、Q3为111次；样本SD用ddof1，与Scaler列方差ddof0分开。三折准确率等权而非直接合并分母569；第三折189的差别已解释。 |
| 选择史 | Q1 testing用来选家族；Q2/Q3外层也被用作跨家族/处理方案开发比较。候选没有把最高已选均值再叫额外未见的最终效果，不以“nested”名称免除选择影响。 |

实际代码在每个外折重建Pipeline/GridSearch，内验/外测只应用当轮训练侧拟合状态；监督F不在全569标签先选。候选最难句“same dataset/nested/Please evaluate/default/minimum testing error”已被拆成具体对象/动作/选择边界，三问均有直接中文及英文有条件参考，负结果如实保留。脚本是学习参考，不等于正式Notebook/HTML成品或本人确认。

## 五、规则及机器疑点核对

本阶段核对总可读性、机制深度、逐cell/图示、完整原题中英、课堂练习、材料Notebook处理、本课可读性与作业细则；制作流程沿本会话此前已读的现行文本核职责。实际使用的规则路径/SHA存于source receipt。按当前规则，固定七格/逐行表标签/字数配额不凌驾于实际解释；本包有目的、关键语法/行、状态、数值例、输出读法、失败/改条件与来源分层，不因历史G/E缺固定标签而扩写。

现有预检日志：T11 L/C.hard/R.hard均0，C.warn4、R.warn124；A12同样硬项0，C.warn1、R.warn15。**本代理没有重新跑发布门槛**，这些是既有日志，不能替代root对最终候选的正式gate。日志没有source-checks契约，source_coverage为unverified_without_manifest；本次63格直接回源与3题原文比较才提供来源证据，不把机器该字段改成已验证。

所有警告原位置/文字保留`stage-2-existing-mechanical-warnings.json`；按机制处理而非一律豁免：

- C_REASONING：T11 cell20可从cell19完整20项直接找最小并重述循环状态，cell52是CV角色唤醒，cell61是四部分总结，cell62是纯横线；A12§8是状态/未完成说明。不存在由这些短段落漏掉核心推理的现象。
- R1a/R1c/R2a/R1e：集中在路线、配置清单、三问参考汇总、输出来源和否定易错条件。Stage1已经逐段复述同一对象/数据角色；原题必须保真的英文长句不因长度删除，A12负结果与因果限制不能删来清警告。
- R3a：T11 cell63原题及A12 Q3入口虽表/列表邻近，前后均交代实际任务、对象和处理包；不是裸公式要求初学者自猜。R4c/R4f：配置表的多参数/代码片段与参数字典同义，行/列含义和一行实际取值已解释，表不是替代算法讲解。
- R6a/R6b/R6d：MAE、SVC、CV、KNN、RBF、DT/RF、F、API与alpha等在首次操作或本节唤醒已给用途，`fit`状态/shape/分母按实际代码解释；10家族的底层完整推导不是本轮“同协议比较固定候选”的必要操作，但C/gamma/缩放/剪枝/分折这些真正决定结论的机制有就地桥梁。
- R7a：源保存、作者历史新跑、当前新增A12复跑/局部探针分别标明。被提示数字要么直接源输出保真，要么能由明确计数/公式/脚本核出，不能因为警告要求重新训练所有未变课堂模型。
- R8a/R8b：A12首次管线命名/参数双下划线与关键fit/predict三行有语法、输入和状态解释；自测答案有理由/反例而非只给数字。没有被长折叠输出吞掉正文关键操作。

Stage1关于“可给§4.2折SD更早回指”的建议保持非阻塞：完整正文已提供必要方差/平方根操作与不同分母的明确约定，当前数值也经代码和手算吻合；不把偏好性更顺的放置扩成新统计课。

## 六、三场景与发布边界

- **预习**：Stage1已经对全部学习单元顺读/复做，当前回源没有发现遗漏源独有条件；B1/B2启动和算式桥梁已关闭。
- **课中**：源1–63与正文1–63逐格唯一对应，老师指cell34能定位第6候选及原/大图，13图均有实际对照说明；B3长期图链与必要标签已核。最终浏览器中的点击/尺寸仍由root看，不以文件存在代替。
- **复习**：§3流程的三次数据切换、§4操作边界、§5英文术语、§6来源等级、§7六道/两道自测与正文和实际结果一致。没有把材料v0.9/transcript pending、学习独审、本人通读/自测/提交混成一个完成勾。

尚需root负责的实际门槛：最终两篇图文/公式/折叠/链接/两份Mermaid显示，最终note-review-v2绑定和gate、正式CAS与回读、课程及根元文件/Notion/Git/看板适用同步。当前原生Obsidian未由本代理查看。Canvas Nov27 23:59香港时区/10points/file upload仅承接2026-11-18已有root只读记录；未重新上网核四入口，具体允许扩展名、后续公告、本人答卷与提交仍未知，所以学习参考不能宣称可提交或已交。行政缺口不阻止这份有完整题干的参考学习解释完成。

本报告和source receipt只更新本独审scratch；旧stage1/2的pending-fixes历史不被追改。当前关闭实际绑定以上两个新候选SHA，任何后续实质变化须据真实diff核其受影响范围，不能只换哈希沿用本结论。
'''
write('stage-2.md',report)
index='''# T11 / A12 当前独立教学审查索引

- reviewer：`/root/cityu_is5113_package`；author：`/root/is6400_update`；未参与本包创作。
- T11 SHA：`5c3b876cc27a1951b7eca79d32bc13da1ef84e88173530b9320ddfbf056312be`。
- A12 SHA：`13f1a87de7503d84135de9f4709fbe0b4e3ba3a6423f3754d7cfae2ac3ead7bd`。
- **独立教学passed**：本代理先独立全篇Stage1，后实际63cell回源、33代码保真、9源PNG解码、13图实看及新A12保护性复跑；旧B1/B2/B3已关闭，无未决教学阻塞。
- 细节：[stage-1.md](stage-1.md)、[stage-1-arithmetic-errata.md](stage-1-arithmetic-errata.md)、[stage-2.md](stage-2.md)、[stage-2-source-receipt.json](stage-2-source-receipt.json)、[stage-2-new-replay-verification.json](stage-2-new-replay-verification.json)。
- 原审者报告仍是其原候选的pending-fixes历史，未修改、未伪署原审。此索引属于当前替补独审者自己的实际审查。
- 源图查看不等于最终browser/Obsidian/Mermaid/KaTeX显示通过；正式gate/CAS/同步及本人学习/提交均单列，不能从本索引推断已完成。
'''
write('independent-review.md',index)
files=['stage-1.md','stage-1-freeze.json','stage-1-arithmetic.json','stage-1-arithmetic-errata.md','stage-2.md','independent-review.md','stage-2-source-receipt.json','stage-2-script-path-diff.json','stage-2-existing-mechanical-warnings.json','stage-2-installed-api-probes.json','stage-2-new-replay-results.json','stage-2-new-replay-verification.json','replay-stage2.py','audit-stage2.py']
js('review-closure.json',{'schema':'cityu-independent-review-closure-v1','created_utc':now,'reviewer_id':'/root/cityu_is5113_package','author_ids':['/root/is6400_update'],'perspective':'high-school-beginner','status':'passed','scope':'T11 full sections0-9 /63cells/33code/all13figures/6selftests + A12 full3questions/2selftests/learning script-data-result trace','candidates':[{'path':str(W/n),'sha256':sha(W/n)} for n in ['candidate.md','a12-learning-candidate.md']],'blockers_closed':['B1 reader executable entry/paths/code/results','B2 actual StandardScaler arithmetic and learned scale definition','B3 persistent readable larger cell33/34 assets with provenance'],'unresolved_teaching_blockers':[],'final_visual_status':'pending-root actual display; this reviewer did not use browser/UI','new_execution':replay,'historical_classroom_run':'33cells author record verified against source hashes; NOT newly executed here','assets':[{'path':n,'sha256':sha(O/n)} for n in files],'root_remaining':['final actual two-candidate display validation','final note-review-v2 binding and release gate','CAS official write/readback and applicable synchronization'],'personal_or_submission_status_changed':False})
assert sha(W/'candidate.md')==receipt['candidate_sha256'] and sha(W/'a12-learning-candidate.md')==receipt['a12_candidate_sha256']
print(json.dumps({'independent_review':str(O/'independent-review.md'),'report_sha256':sha(O/'independent-review.md'),'stage2':str(O/'stage-2.md'),'stage2_sha256':sha(O/'stage-2.md'),'closure':str(O/'review-closure.json'),'status':'passed independent teaching; final display/root release separate','source_receipt':str(O/'stage-2-source-receipt.json')},ensure_ascii=False,indent=2))
