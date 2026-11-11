'use strict';
window.TimelineBoard = (() => {
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const statusNames = {done:'阶段已完成',in_progress:'正在推进',planned:'计划中',waiting:'等待回件',needs_review:'待核阅／修订',unknown:'状态待确认'};
  const basisNames = {official:'正式截止',agreed:'已确认',proposed:'内部建议',unknown:'日期未定'};
  const readyNames = {ready:'可以先推进',verify:'先核实状态',waiting_dependency:'等待前置完成',waiting_external:'等待回件',done:'所述交付已完成'};
  const courseNames = {AC6761:'财务分析',IS6400:'数据分析',IS5113:'AI 伦理',IS5542:'客服 Agent',EF5560:'金融科技案例'};
  const colors = {AC6761:'#527d57',IS6400:'#277a83',IS5113:'#526ca0',IS5542:'#a56742',EF5560:'#9b7941'};
  const moduleOrder = ['方向与口径','资料与分析','工程与演示','核验与修订','个人准备与协作','合稿与交付','其他事项'];
  const state = {mode:'calendar',scale:'weeks',offset:0,course:'all',grouping:'course',status:'all',mine:false,query:''};
  let records = [], lists = [], panelReturn = null, renderedSignature = '';
  const signature = input => JSON.stringify(input.map(r=>[r.id,r.timeline]));
  const todayISO = () => new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  const dayNumber = iso => Math.floor(Date.parse(iso.slice(0,10)+'T00:00:00Z')/86400000);
  const isoDay = value => new Date(value*86400000).toISOString().slice(0,10);
  const shortDay = value => {const d=typeof value==='number'?isoDay(value):value;return Number(d.slice(5,7))+'/'+Number(d.slice(8,10));};
  const monday = iso => {const d=dayNumber(iso);return d-((new Date(d*86400000).getUTCDay()+6)%7);};
  const itemKey = i => i.assignment_id+'|'+i.id;
  // Only an actual completion date can place a completed item on the calendar.
  const eventDate = i => i.status==='done'?(i.completed_on||null):(i.target?.value?.slice(0,10)||null);
  function moduleFor(i) {
    const id=i.id.replace(/^my-/,'');
    if(i.id.startsWith('my-')||['personal','handoff','team-plan'].includes(id))return '个人准备与协作';
    if(['scope','preparation','history-team-plan','date-direction','history-briefing'].includes(id))return '方向与口径';
    if(['core','web','demo-record'].includes(id))return '工程与演示';
    if(['feedback','team-april','p01','p23','acceptance','sources','remote-report-review','rules'].includes(id))return '核验与修订';
    if(['data','prediction','clusters','local-comparison','observations','part1','part2','part3'].includes(id))return '资料与分析';
    if(/^(date-|report|slides|video|record-video|rehearsal|group-rehearsal|delivery|merge|pdf-review|ppt-received|english-draft-ready)/.test(id)||id==='team')return '合稿与交付';
    if(id==='e-draft-ready')return '个人准备与协作';
    if(id==='rules-received')return '核验与修订';
    return '其他事项';
  }
  function periods(anchor, scale) {
    const width=scale==='days'?1:7,count=scale==='days'?7:4;
    return Array.from({length:count},(_,n)=>({start:anchor+n*width,end:anchor+(n+1)*width-1}));
  }
  function allItems() {
    return records.filter(r=>state.course==='all'||r.course===state.course).flatMap(r=>(r.timeline?.items||[]).map(i=>({...i,course:r.course,assignment_id:r.id,stale:!!r.timeline.stale})));
  }
  function visibleItems() {
    const q=state.query.trim().toLowerCase();
    return allItems().filter(i=>(state.status==='all'||(state.status==='done'?i.status==='done':i.status!=='done'))&&(!state.mine||i.personal_action&&i.status!=='done')&&(!q||[i.title,i.owner,i.summary,i.next_action].join(' ').toLowerCase().includes(q)));
  }
  function makeGroups(items, grouping) {
    const groups=new Map();
    for(const i of items){const key=grouping==='course'?i.course:moduleFor(i);if(!groups.has(key))groups.set(key,{key,title:key,items:[]});groups.get(key).items.push(i);}
    return [...groups.values()].sort((a,b)=>grouping==='course'?a.key.localeCompare(b.key):moduleOrder.indexOf(a.key)-moduleOrder.indexOf(b.key));
  }
  const byDate = (a,b) => (eventDate(a)||'9999').localeCompare(eventDate(b)||'9999') || ((a.target?.basis==='official'?0:1)-(b.target?.basis==='official'?0:1)) || a.title.localeCompare(b.title);
  const openSort = (a,b) => (a.status==='done')-(b.status==='done') || byDate(a,b);
  const addList = (items,title,subtitle='') => {lists.push({items:[...items].sort(openSort),title,subtitle});return lists.length-1;};
  function listButton(items,title,label,classes='tl-text-button',subtitle='') {
    return `<button class="${classes}" data-tl-list="${addList(items,title,subtitle)}">${esc(label)}</button>`;
  }
  function groupName(g) {return state.course==='all'&&state.grouping==='course'?`${g.key} <span>${esc(courseNames[g.key]||'')}</span>`:esc(g.title);}
  function eventButton(i, compact=false) {
    const date=eventDate(i),kind=i.status==='done'?'done':i.target.basis;
    const title=`${date||'日期未定'} · ${basisNames[i.target.basis]} · ${i.title} · ${i.owner}`;
    return `<button class="tl-event ${esc(kind)} ${compact?'compact':''}" data-tl-item="${esc(itemKey(i))}" title="${esc(title)}"><span class="tl-event-date">${kind==='official'?'◆ ':''}${date?shortDay(date):'待定'}</span><span class="tl-event-title">${esc(i.title)}</span><span class="tl-event-kind">${esc(kind==='done'?'已完成':basisNames[kind])}</span></button>`;
  }
  function groupSide(g) {
    const done=g.items.filter(i=>i.status==='done'),undated=g.items.filter(i=>i.status!=='done'&&!eventDate(i));
    const next=g.items.filter(i=>i.status!=='done'&&eventDate(i)).sort(byDate)[0];
    return `<div class="tl-row-head"><div class="tl-group-title"><i style="background:${colors[g.key]||'#517c83'}"></i><h3>${groupName(g)}</h3></div><p>${g.items.length} 条记录${next?' · 下一节点 '+shortDay(eventDate(next)):''}</p><div class="tl-row-links">${done.length?listButton(done,g.title+' · 完成记录','✓ '+done.length+' 已完成','tl-text-button','完成的是标题所述阶段；实际完成日未知时保留核实日期。'):''}${undated.length?listButton(undated,g.title+' · 未排期事项',undated.length+' 未排期'):''}</div></div>`;
  }
  function calendar(groups,items) {
    const anchor=monday(todayISO())+state.offset,cols=periods(anchor,state.scale),today=dayNumber(todayISO());
    const outside=items.filter(i=>eventDate(i)&&(dayNumber(eventDate(i))<cols[0].start||dayNumber(eventDate(i))>cols.at(-1).end));
    const width=state.scale==='days'?108:178,template=`196px repeat(${cols.length},minmax(${width}px,1fr))`;
    return `<div class="tl-datebar"><div class="tl-period-nav"><button data-tl-move="-1" aria-label="上一时间段">‹</button><b>${shortDay(cols[0].start)} — ${shortDay(cols.at(-1).end)} <span>${isoDay(anchor).slice(0,4)}</span></b><button data-tl-move="1" aria-label="下一时间段">›</button><button data-tl-today>今天</button></div><div class="tl-segments" aria-label="日期尺度"><button data-tl-scale="weeks" aria-pressed="${state.scale==='weeks'}">4 周</button><button data-tl-scale="days" aria-pressed="${state.scale==='days'}">7 天</button></div></div><div class="tl-calendar-scroll" tabindex="0" aria-label="横向日历，可水平滚动"><div class="tl-calendar" data-scale="${state.scale}" style="--tl-columns:${template};--tl-min-width:${196+cols.length*width}px"><div class="tl-calendar-head"><div class="tl-corner">${state.course==='all'&&state.grouping==='course'?'课程项目':'工作模块'}<span>点击事项查看详细</span></div>${cols.map(c=>`<div class="tl-period ${c.start<=today&&today<=c.end?'is-today':''}"><b>${state.scale==='days'?shortDay(c.start):shortDay(c.start)+' — '+shortDay(c.end)}</b><span>${state.scale==='days'?['周日','周一','周二','周三','周四','周五','周六'][new Date(c.start*86400000).getUTCDay()]:c.start<=today&&today<=c.end?'本周 · 今天 '+shortDay(today):'第 '+(Math.floor((c.start-anchor)/7)+1)+' 周'}</span></div>`).join('')}</div>${groups.map(g=>`<section class="tl-calendar-row" aria-label="${esc(g.title)} 时间安排">${groupSide(g)}${cols.map(c=>{const entries=g.items.filter(i=>eventDate(i)&&dayNumber(eventDate(i))>=c.start&&dayNumber(eventDate(i))<=c.end).sort(byDate);return `<div class="tl-cell ${c.start<=today&&today<=c.end?'is-today':''}">${entries.slice(0,2).map(i=>eventButton(i,state.scale==='days')).join('')}${entries.length>2?listButton(entries,`${g.title} · ${shortDay(c.start)} — ${shortDay(c.end)}`,`还有 ${entries.length-2} 项 →`,'tl-more'):''}${!entries.length?'<span class="tl-no-event">—</span>':''}</div>`;}).join('')}</section>`).join('')||'<div class="tl-empty">当前筛选下没有记录。</div>'}</div></div><div class="tl-calendar-foot"><span><i class="tl-legend-official">◆</i> 正式节点 <i class="tl-legend-proposed">○</i> 内部建议</span><span>仅显示已登记日期；未排期与完成记录在左侧入口。</span>${outside.length?listButton(outside,'当前日期范围外的事项',outside.length+' 项在当前范围外 →','tl-text-button'):''}</div>`;
  }
  function modules(groups) {
    return `<div class="tl-modules">${groups.map(g=>{const done=g.items.filter(i=>i.status==='done'),current=g.items.filter(i=>i.status!=='done'&&i.lane==='current'),future=g.items.filter(i=>i.status!=='done'&&i.lane==='future');const upcoming=g.items.filter(i=>i.status!=='done').sort(byDate).slice(0,3);return `<article class="tl-module"><div class="tl-module-head"><div class="tl-group-title"><i style="background:${colors[g.key]||'#517c83'}"></i><h3>${groupName(g)}</h3></div><span>${g.items.length} 项</span></div><div class="tl-module-counts">${listButton(done,g.title+' · 已完成',done.length+' 已完成')}${listButton(current,g.title+' · 当前',current.length+' 当前')}${listButton(future,g.title+' · 未来',future.length+' 未来')}</div><div class="tl-distribution" aria-label="记录分布：${done.length} 已完成、${current.length} 当前、${future.length} 未来"><span class="done" style="width:${done.length/g.items.length*100}%"></span><span class="current" style="width:${current.length/g.items.length*100}%"></span></div><div class="tl-module-next"><span>下一步关注</span>${upcoming.map(i=>`<button class="tl-module-task" data-tl-item="${esc(itemKey(i))}"><span>${eventDate(i)?shortDay(eventDate(i)):'待定'}</span><b>${esc(i.title)}</b><small>${esc(i.target.basis==='unknown'?statusNames[i.status]:basisNames[i.target.basis])}</small></button>`).join('')||'<p>所述阶段已有完成记录。</p>'}</div><footer>${listButton(g.items,g.title+' · 所有事项','查看全部事项 →','tl-text-button')}</footer></article>`;}).join('')||'<div class="tl-empty">没有匹配的模块。</div>'}</div>`;
  }
  function toolbar() {
    return `<div class="tl-toolbar"><div class="tl-segments tl-view-switch" aria-label="时间线展示方式"><button data-tl-mode="calendar" aria-pressed="${state.mode==='calendar'}">▦ 横向日历</button><button data-tl-mode="modules" aria-pressed="${state.mode==='modules'}">▤ 模块概览</button></div><div class="tl-toolbar-filters">${records.length>1?`<label><span>课程</span><select id="tl-course" aria-label="筛选课程"><option value="all">全部课程</option>${records.map(r=>`<option value="${esc(r.course)}" ${state.course===r.course?'selected':''}>${esc(r.course)}</option>`).join('')}</select></label>`:''}<label><span>状态</span><select id="tl-status" aria-label="筛选状态"><option value="all" ${state.status==='all'?'selected':''}>全部状态</option><option value="open" ${state.status==='open'?'selected':''}>未完成</option><option value="done" ${state.status==='done'?'selected':''}>已完成</option></select></label>${state.course==='all'?`<label><span>分组</span><select id="tl-group" aria-label="时间线分组"><option value="course" ${state.grouping==='course'?'selected':''}>按课程</option><option value="module" ${state.grouping==='module'?'selected':''}>按工作模块</option></select></label>`:''}<label class="tl-mine"><input id="tl-mine" type="checkbox" ${state.mine?'checked':''}> 总监督事项</label><input class="tl-search" id="tl-search" aria-label="查找时间线任务" placeholder="搜索任务或负责人" value="${esc(state.query)}"></div><details class="tl-export-menu"><summary>导出 · 助手</summary><div><button id="tl-export">导出时间线 JSON</button><button id="tl-daily">导出总监督事项</button>${records.filter(r=>state.course==='all'||r.course===state.course).map(r=>r.timeline?.repository_url?`<a href="${esc(r.timeline.repository_url+'/blob/main/ASSISTANT-README.md')}" target="_blank" rel="noopener">${esc(r.course)} · 助手读取说明 ↗</a>`:'').join('')}</div></details></div>`;
  }
  function render(input) {
    renderedSignature=signature(input);
    const previousCount=records.length;records=input;
    if(records.length===1)state.course=records[0].course;
    else if(previousCount===1||!records.some(r=>r.course===state.course))state.course='all';
    lists=[];const items=visibleItems(),groups=makeGroups(items,state.course==='all'?state.grouping:'module');
    const completed=items.filter(i=>i.status==='done'),undated=items.filter(i=>i.status!=='done'&&!eventDate(i));
    return `<section id="timeline-panel" class="tl-workspace">${toolbar()}${records.filter(r=>(state.course==='all'||r.course===state.course)&&(r.timeline?.stale||r.timeline?.error)).map(r=>`<div class="tl-warning">${esc(r.course)} · ${esc(r.timeline.warning||r.timeline.error)} 先核实新状态，历史记录保留。</div>`).join('')}<div class="tl-context"><span>${groups.length} 个${state.course==='all'&&state.grouping==='course'?'课程':'工作模块'} · ${items.length} 条记录</span><div>${completed.length?listButton(completed,'已完成的阶段成果','✓ '+completed.length+' 项完成记录'):''}${undated.length?listButton(undated,'尚未排期的事项',undated.length+' 项未排期'):''}<span>只读 · 香港时间</span></div></div>${state.mode==='calendar'?calendar(groups,items):modules(groups)}<dialog id="tl-detail" class="tl-detail" aria-labelledby="tl-detail-title"><div id="tl-detail-content"></div></dialog></section>`;
  }
  function refreshPanel(keepSearch=false) {
    const panel=document.getElementById('timeline-panel');if(!panel)return;
    const pos=keepSearch?panel.querySelector('#tl-search')?.selectionStart:null;
    panel.outerHTML=render(records);bind();
    if(keepSearch){const search=document.getElementById('tl-search');search.focus();search.setSelectionRange(pos,pos);}
  }
  const dialogHeader=(title,sub,back=false)=>`<header class="tl-detail-head"><div>${back?'<button class="tl-back" data-tl-back>‹ 返回列表</button>':''}<small>${esc(sub)}</small><h2 id="tl-detail-title">${esc(title)}</h2></div><button class="tl-close" aria-label="关闭时间线详情">×</button></header>`;
  function showDialog(html) {
    const dialog=document.getElementById('tl-detail');dialog.querySelector('#tl-detail-content').innerHTML=html;
    dialog.querySelector('.tl-close').onclick=()=>dialog.close();dialog.onclick=e=>{if(e.target===dialog)dialog.close();};
    dialog.querySelectorAll('[data-tl-item]').forEach(b=>b.onclick=()=>openItem(b.dataset.tlItem));
    dialog.querySelector('[data-tl-back]')?.addEventListener('click',()=>openList(panelReturn));
    if(!dialog.open)dialog.showModal();dialog.scrollTop=0;
  }
  function openList(list) {
    if(!list)return;panelReturn=list;
    showDialog(dialogHeader(list.title,list.subtitle||list.items.length+' 项 · 点击查看完整交付和依据')+`<div class="tl-detail-body tl-drill-list">${list.items.map(i=>`<button data-tl-item="${esc(itemKey(i))}"><span class="tl-status-dot ${esc(i.status)}"></span><div><b>${esc(i.title)}</b><small>${esc(i.course+' · '+i.owner)}</small><span>${esc(statusNames[i.status])} · ${eventDate(i)?esc(eventDate(i)+' · '+basisNames[i.target.basis]):i.status==='done'?'实际完成日未记录 · 核实于 '+esc(i.observed_on):'未排期'}</span></div><span>›</span></button>`).join('')||'<p class="tl-empty">没有登记记录。</p>'}</div>`);
  }
  function openItem(key) {
    const all=allItems(),i=all.find(i=>itemKey(i)===key);if(!i)return;
    const counts=i.check_progress||{passed:0,total:i.acceptance.length};
    showDialog(dialogHeader(i.title,i.course+' · '+statusNames[i.status],!!panelReturn)+`<div class="tl-detail-body"><div class="tl-detail-meta"><span><small>负责人</small>${esc(i.owner)}</span><span><small>${esc(basisNames[i.target.basis])}</small>${esc(i.target.value||'尚未安排')}</span></div><section><h3>目前进展</h3><p>${esc(i.summary)}</p></section><section class="tl-action"><h3>下一步</h3><p>${esc(state.mine&&i.personal_action?i.personal_action:i.next_action)}</p><small>${esc(readyNames[i.readiness]||'待核')}${i.estimated_minutes?' · '+esc(i.estimated_minutes)+' 分钟':' · 用时待估计'}</small></section><section><h3>要交什么</h3><p>${esc(i.deliverable)}</p></section><section><h3>验收检查 <span>${counts.passed} / ${counts.total}</span></h3><div class="tl-checkbar"><i style="width:${counts.total?counts.passed/counts.total*100:0}%"></i></div><ul class="tl-checks">${i.acceptance.map(c=>`<li><span class="${esc(c.status)}">${c.status==='pass'?'✓':c.status==='gap'?'!':'○'}</span><div>${esc(c.label)}<small>${c.status==='pass'?'已核通过':c.status==='gap'?'仍有缺项':'尚未核实'}</small></div></li>`).join('')}</ul></section><section><h3>前置与依赖</h3>${i.depends_on.map(id=>{const n=all.find(x=>x.assignment_id===i.assignment_id&&x.id===id),gate=(i.dependency_gates||[]).find(g=>g.task_id===id);return `<button class="tl-dependency" data-tl-item="${esc(i.assignment_id+'|'+id)}"><span>${esc(n?.title||id)}</span><small>${esc(gate?.note||'以前置任务记录为准')} · ${i.blocked_by.includes(id)?'尚未满足':'已满足'} →</small></button>`;}).join('')||'<p class="tl-muted">无已登记前置条件。</p>'}</section><details class="tl-detail-evidence"><summary>证据、日期与状态变化</summary><dl><dt>实际开始／完成</dt><dd>${esc(i.started_on||'未记录')} ／ ${esc(i.completed_on||'未记录')}</dd><dt>核实日期</dt><dd>${esc(i.observed_on)}</dd><dt>状态依据</dt><dd>${esc(i.state_basis)}</dd></dl><ul>${i.evidence.map(e=>`<li>${e.url&&/^https:\/\//.test(e.url)?`<a href="${esc(e.url)}" target="_blank" rel="noopener">${esc(e.label)} ↗</a>`:esc(e.label)}</li>`).join('')}</ul><h4>状态变化</h4><ul>${i.history.map(h=>`<li>${esc(h.observed_on)} · ${esc(statusNames[h.status])}<br>${esc(h.note)}</li>`).join('')}</ul></details></div>`);
  }
  function download(value,name){const u=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)],{type:'application/json;charset=utf-8'})),a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);}
  function bind() {
    const panel=document.getElementById('timeline-panel');if(!panel)return;
    panel.querySelectorAll('[data-tl-mode]').forEach(b=>b.onclick=()=>{state.mode=b.dataset.tlMode;refreshPanel();});
    panel.querySelectorAll('[data-tl-scale]').forEach(b=>b.onclick=()=>{state.scale=b.dataset.tlScale;state.offset=0;refreshPanel();});
    panel.querySelectorAll('[data-tl-move]').forEach(b=>b.onclick=()=>{state.offset+=Number(b.dataset.tlMove)*(state.scale==='days'?7:28);refreshPanel();});
    panel.querySelector('[data-tl-today]')?.addEventListener('click',()=>{state.offset=0;refreshPanel();});
    for(const [id,key] of [['tl-course','course'],['tl-group','grouping'],['tl-status','status']])panel.querySelector('#'+id)?.addEventListener('change',e=>{state[key]=e.target.value;refreshPanel();});
    panel.querySelector('#tl-mine').onchange=e=>{state.mine=e.target.checked;refreshPanel();};
    panel.querySelector('#tl-search').oninput=e=>{state.query=e.target.value;refreshPanel(true);};
    panel.querySelectorAll('[data-tl-list]').forEach(b=>b.onclick=()=>openList(lists[Number(b.dataset.tlList)]));
    panel.querySelectorAll('[data-tl-item]').forEach(b=>b.onclick=()=>{panelReturn=null;openItem(b.dataset.tlItem);});
    panel.querySelector('#tl-export').onclick=()=>download({schema_version:1,exported_at:new Date().toISOString(),timelines:records.filter(r=>state.course==='all'||r.course===state.course).map(r=>r.timeline)},'course-timelines.json');
    panel.querySelector('#tl-daily').onclick=()=>download({schema_version:1,generated_at:new Date().toISOString(),timezone:'Asia/Shanghai',advisory_only:true,confirm_proposed_dates:true,actions:allItems().filter(i=>i.personal_action&&i.status!=='done').map(i=>({assignment_id:i.assignment_id,id:i.id,title:i.title,action:i.personal_action,readiness:i.readiness,target:i.target,blocked_by:i.blocked_by,estimated_minutes:i.estimated_minutes,observed_on:i.observed_on}))},'supervisor-daily-actions.json');
  }
  return {render,bind,isCurrent:input=>renderedSignature===signature(input),model:{eventDate,dayNumber,isoDay,monday,periods,moduleFor,makeGroups}};
})();
