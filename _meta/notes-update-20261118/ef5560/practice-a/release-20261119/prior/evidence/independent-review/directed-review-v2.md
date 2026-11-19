# Practice Exam A · v2 定向复核与当前教学结论

审查者 /root/ef_m11_review；此为Stage1/2同一次独审的集中修复定向复核，不重开全文、不修改原报告或候选。

## 输入实核

- 已审原候选SHA b53346b0ee0ee4ebe207d02bf894b74f62b2aa24897993ef6bc28bdc100da8ee。
- 新候选 ../practice-exam-a-dot-author-v2/candidate-v2.md，实际SHA 7162919ff6e65f613e571d6e67b81923d7fcd47804f6b9b791ef990e898b409d。
- 实读targeted-v2.diff/json，另用文件实际行差异比对，六个行差异块均只改A1/A4/A5/C1已列公式损坏位置。未发现越范围修改题面、答案、金额、条件、图义或学习次序。
- 原Stage1/2完整学习/来源证据承接到未变部分，不用新SHA伪装又做一次全文盲审。

## S1-MATH-01：关闭（源码与教学语义）

当前直接读到：
- A1：\mathrm{SSE}、\beta_j、\lambda、\mathrm{SSE}+\lambda\sum_j\beta_j^2；与中文非负惩罚/平方系数和相符。
- A4：\widehat r_p^e=\alpha+\beta r_m^e；符号表alpha/beta/拟合帽号同步恢复。原0.20%→3.20%、3pp变化和拟合非保证边界未改。
- A5：S_{\mathrm{weekly}}=\mu_{\mathrm{weekly}}^e/\sigma_{\mathrm{weekly}}恢复为单个完整式；同频分子/分母和0.24/3=.08解释一致，没有把净均值重复扣费或年化。
- C1：\mathrm{SSE}=\sum_{t=1}^{4}e_t^2正确；模型误差/MA12第四月代入、下方原正确OOS分式均保留。
- 对新候选全部字符实查，除正常空白外控制字符数为0，原4个U+0008全部消失；异常三段周下标LF已消除。

这些是已经中文定义的数学符号恢复，不是改金融/统计结论。当前未发现依赖未同步。

## S2-ASSET-01：关闭（可检索文本与图义）

- 新b2-loss.svg实际SHA d402808a013840c6def08d8de3dc9a8453037c9b397c2ac0fc553e715a93e932。
- 实际XML解析得到15个text标签，内容为10/30/60、训练时长轴、五个损失刻度、Loss(as provided)、最低三候选标注/30 epochs loss.0024、完整标题、Training loss/Validation loss。不是仅注释里有文字。
- 新compute.py实际SHA 05ed45a09f4af8ec3501a2c6f664a910c116fd42b7fe72b3593385470ec0b1bc，确有matplotlib.rcParams['svg.fonttype']='none'，保源码可重做。
- 新旧b2-loss.png逐字节相同，新旧computation-results.json也逐字节相同；图数据/点位/选择理由未改。Stage2已经真实观看这张PNG，蓝训练/橙验证、三点和圈标30/.0024、轴/图例均正确。
- 当前候选相邻说明仍限制三候选连线不代表真实中间轨迹/全局最优，且引用同名SVG，未引入来源漂移。

本次尝试用现有cairosvg将新SVG独立栅格化，模块不可用，没有声称生成或看过不存在的渲染。XML文字及同源PNG/数据验证足以确认“恢复可检索文字”资产缺陷已修；新SVG在最终笔记中的实际字体/布局显示，仍须root真实UI核验，不以XML存在替代。

## 当前结论与剩余边界

**两项集中缺陷已关闭；本次全篇独立教学语义和来源核查结论可绑定7162919...，没有剩余已知实质教学返修项。**

不认领整体发布PASS或最终UI。root仍需对确切候选真实查看公式、A4符号表、C1引用内源表、B2新SVG嵌入、details和页级链接，完成机械门槛/资产绑定/安全写回。若最终显示发现具体问题，只修相应显示依赖，不重做未变全卷。

旧Stage2的needs_fixes是修前历史，本报告负责说明实际关闭依据，不追改旧记录。候选当前仍带待审/草稿行政文本可由root按实际结论作最小状态维护，不能用状态文字替代真实验收。本代理没有编辑正式笔记、用户学习状态、Notion或Git。

