"""Source-backed project timelines and conservative daily-planning projections."""
from datetime import date, datetime, timezone, timedelta
from pathlib import Path
import hashlib
import json
import re

TZ = timezone(timedelta(hours=8))
STATES = {'done', 'in_progress', 'planned', 'waiting', 'needs_review', 'unknown'}
LABELS = {'done':'已完成所述交付', 'in_progress':'正在推进', 'planned':'后续计划', 'waiting':'等待回件', 'needs_review':'待核阅或修订', 'unknown':'进展待确认'}
BASIS = {'official':'正式截止', 'agreed':'已确认安排', 'proposed':'内部建议', 'unknown':'日期未定'}

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def validate(t):
    if t.get('schema_version') != 1 or not re.fullmatch(r'[A-Z]{2}\d{4}-A\d{2}', t.get('assignment_id','')):
        raise ValueError('时间线版本或作业编号无效')
    if t.get('timezone') != 'Asia/Shanghai': raise ValueError('时间线时区无效')
    date.fromisoformat(t['as_of'])
    if not re.fullmatch(r'https://github\.com/[\w.-]+/[\w.-]+',t['repository_url']): raise ValueError('仓库链接无效')
    items=t.get('items',[]); ids=[i['id'] for i in items]
    if not items or len(ids)!=len(set(ids)): raise ValueError('时间线任务缺失或编号重复')
    for i in items:
        if not re.fullmatch(r'[a-z0-9-]+',i['id']) or i['status'] not in STATES: raise ValueError('任务编号或状态无效')
        for k in ('title','summary','deliverable','next_action','owner','state_basis'):
            if not isinstance(i[k],str) or not i[k].strip(): raise ValueError('任务字段缺失：'+k)
        if i['owner_role'] not in ('me','member','team','unknown'): raise ValueError('负责人类型无效')
        if i['scope'] not in ('team','supporting'): raise ValueError('任务范围无效')
        if i['status']=='done' and not i['evidence']: raise ValueError('已完成任务必须有依据')
        if not set(i['depends_on']).issubset(ids) or i['id'] in i['depends_on']: raise ValueError('依赖任务不存在')
        target=i['target']; value=target['value']; precision=target['precision']
        if target['basis'] not in BASIS: raise ValueError('日期性质无效')
        if precision=='unknown':
            if value is not None or target['basis']!='unknown': raise ValueError('未知日期必须为 null')
        elif precision=='datetime':
            if datetime.fromisoformat(value).utcoffset() is None: raise ValueError('精确时间必须带时区')
        elif precision in ('date','before_date'):date.fromisoformat(value)
        else:raise ValueError('日期精度无效')
        for field in ('started_on','completed_on','observed_on'):
            if i.get(field) is not None: date.fromisoformat(i[field])
        if i.get('completed_on') and i['status']!='done': raise ValueError('未完成任务不可填完成日期')
        if i['estimated_minutes'] is not None and (type(i['estimated_minutes']) is not int or i['estimated_minutes']<=0): raise ValueError('工时必须为正整数或 null')
        for check in i['acceptance']:
            if check['status'] not in ('pass','gap','unknown') or not check['label']:raise ValueError('验收项无效')
        if not i['acceptance'] or i['status']=='done' and any(c['status']!='pass' for c in i['acceptance']):raise ValueError('已完成状态需要本环节验收项全部通过')
        for e in i['evidence']:
            if not e['label'] or (e.get('url') and not re.match(r'^https://',e['url'])):raise ValueError('依据链接无效')
        if not i['history'] or any(h['status'] not in STATES for h in i['history']): raise ValueError('缺少状态变化记录')
    graph={i['id']:i['depends_on'] for i in items};visited=set();visiting=set()
    def visit(k):
        if k in visiting:raise ValueError('任务依赖有环')
        if k in visited:return
        visiting.add(k)
        for x in graph[k]:visit(x)
        visiting.remove(k);visited.add(k)
    for k in graph:visit(k)

def enrich(t, now=None, stale=False):
    validate(t);t=json.loads(json.dumps(t));now=now or datetime.now(TZ);today=now.astimezone(TZ).date();by_id={i['id']:i for i in t['items']}
    stale=stale or (today-date.fromisoformat(t['as_of'])).days>7
    t['stale']=stale;t['warning']='来源或进度已有更新，需先复核时间线后安排每日事项。' if stale else ''
    for i in t['items']:
        def satisfied(x):
            gate=next((g for g in i.get('dependency_gates',[]) if g['task_id']==x),None)
            if gate and gate.get('check_ids'):
                checks={c.get('id'):c['status'] for c in by_id[x]['acceptance']}
                return all(checks.get(k)=='pass' for k in gate['check_ids'])
            return by_id[x]['status']=='done'
        i['blocked_by']=[x for x in i['depends_on'] if not satisfied(x)]
        i['lane']='past' if i['status']=='done' else 'future' if i['status']=='planned' else 'current'
        i['readiness']='done' if i['status']=='done' else 'verify' if stale or i['status']=='unknown' else 'waiting_dependency' if i['blocked_by'] else 'waiting_external' if i['status']=='waiting' and not i.get('my_next_action') else 'ready'
        i['personal_action']=i.get('my_next_action') or (i['next_action'] if i['owner_role']=='me' else None)
        target=i['target'];v=target['value'];i['date_state']='unscheduled'
        if v:
            day=date.fromisoformat(v[:10]);expired=(datetime.fromisoformat(v)<now if target['precision']=='datetime' else today>=day if target['precision']=='before_date' else today>day)
            i['date_state']='completed' if i['status']=='done' else 'past_due_unverified' if expired else 'today' if day==today else 'next_7_days' if (day-today).days<=7 else 'later'
            if expired and i['status']=='planned':i['lane']='current';i['readiness']='verify'
        i['check_progress']={'passed':sum(c['status']=='pass' for c in i['acceptance']),'total':len(i['acceptance'])}
    t['counts']={k:sum(i['lane']==k for i in t['items']) for k in ('past','current','future')}
    return t

def daily_plan(t, now=None):
    t=enrich(t,now)
    items=[]
    for i in t['items']:
        if not i['personal_action'] or i['status']=='done':continue
        items.append({k:i[k] for k in ('id','title','owner','status','personal_action','readiness','target','blocked_by','estimated_minutes','observed_on','date_state')})
    items.sort(key=lambda i:(i['readiness']!='ready',i['target']['value'] or '9999',i['id']))
    return {'schema_version':1,'assignment_id':t['assignment_id'],'course':t['course'],'as_of':t['as_of'],'timezone':t['timezone'],'source_revision':t['revision'] if 'revision' in t else None,'repository_url':t['repository_url'],'stale':t['stale'],'scheduling_policy':{'advisory_only':True,'unknown_effort_is_null':True,'confirm_proposed_dates':True,'do_not_schedule_blocked_execution':True,'recheck_current_date_and_latest_revision':True},'actions':items,'deadlines':[{'id':i['id'],'title':i['title'],'target':i['target'],'status':i['status']} for i in t['items'] if i['target']['basis']=='official']}

def attach(records,root):
    errors=[]
    management_file=root/'_meta/assignment-board/management.json'
    management=json.loads(management_file.read_text('utf-8')).get('projects',{}) if management_file.exists() else {}
    for r in records:
        file=root/Path(r['metadata_path']).parent/'timeline.json'
        if not file.exists():continue
        try:
            t=json.loads(file.read_text('utf-8'));validate(t)
            if t['assignment_id']!=r['id'] or t['course']!=r['course']:raise ValueError('时间线与课程归属不一致')
            expected=hashlib.sha256(json.dumps(management.get(r['id'],{}),ensure_ascii=False,sort_keys=True).encode()).hexdigest()
            t['revision']=digest(file);r['timeline']=enrich(t,stale=t['basis_revision']!=r['revision'] or t.get('basis_management_revision')!=expected)
        except (ValueError,KeyError,TypeError,OSError) as e:
            r['timeline']={'error':str(e)};errors.append({'path':str(file.relative_to(root)),'message':'时间线：'+str(e)})
    return errors

def markdown(t):
    t=enrich(t);out=[f"# {t['course']} · 项目时间线",'',t['summary'],'',f"进度依据截至 {t['as_of']}；时区 Asia/Shanghai。完成日期未知时只记录核实日期。",'', '[结构化时间线](progress/timeline.json) · [个人助手每日事项入口](progress/daily-plan.json) · [如何读取](ASSISTANT-README.md)','']
    for lane,title in [('current','当前推进与待核'),('future','未来安排'),('past','已完成的阶段成果')]:
        out+=['## '+title,'']
        for i in [x for x in t['items'] if x['lane']==lane]:
            target=i['target'];date_text=(target['value'] or '尚未安排')+' · '+BASIS[target['basis']]
            out += [f"### {i['title']} · `{i['id']}`",'',f"**{LABELS[i['status']]}** · 负责人：{i['owner']} · {date_text}",'',i['summary'],'',f"- 本环节交付：{i['deliverable']}",f"- 下一步：{i['next_action']}",f"- 前置依赖：{'、'.join(i['depends_on']) or '无已登记前置'}",f"- 开始／完成：{i['started_on'] or '未记录'} ／ {i['completed_on'] or '未记录'}；核实日期：{i['observed_on']}"]
            if i.get('my_next_action'):out+=['- 总监督可做：'+i['my_next_action']]
            out+=['- 验收：'+'；'.join(('✓ ' if c['status']=='pass' else '待补 ' if c['status']=='gap' else '待核 ')+c['label'] for c in i['acceptance'])]
            out+=['- 依据：'+'；'.join(f"[{e['label']}]({e['url']})" if e.get('url') else e['label'] for e in i['evidence']),'']
    out+=['## 维护约定','','每批实质推进维护 timeline.json 的当前状态和 history，并从同一份数据生成本页与 daily-plan.json。修改后同步 GitHub、本地看板与线上看板。日期建议不等于承诺；GitHub 提交时间不等于任务完成时间；未见回执不自动判迟交或提交完成。','']
    return '\n'.join(out)

ASSISTANT_GUIDE='''# 给文档个人助手：如何安排每日事项

1. 先读 `progress/daily-plan.json`，再按任务 ID 回到 `progress/timeline.json`。`TIMELINE.md` 是同源的人类阅读版。
2. 检查 `as_of`、`observed_on` 和最新 GitHub 提交。文件更新不代表所有事项重新核验；超过七天或有新回件，先向总监督核实。
3. `readiness=ready` 只表示已登记前置满足，可以提出安排；`verify` 先核状态，`waiting_dependency` 等前置成果，`waiting_external` 等回件。不要把给组员的任务排成本人执行任务。
4. `target.basis=official` 是正式节点，`agreed` 才是确认安排，`proposed` 只是建议。无时刻的日期不能补成 23:59；`before_date` 表示该日前。当天及已过日期要按 Asia/Shanghai 重新计算，不能照用旧导出的紧急程度。
5. 工时未知为 null，不当作零分钟。`my_next_action` 是总监督可以做的具体动作；提出每日候选后还需结合本人日历、空闲时间和确认，不自动创建日程、承诺交期或替本人发送消息。
6. 已完成指标题所述阶段。收到初稿、验收、团队定稿和正式提交分别记录；观察日期不冒充实际完成日期。
7. 依赖中的 `dependency_gates` 可只要求上游部分验收项通过，而非整个上游完全结束。`acceptance` 记录 pass/gap/unknown；history 记录状态变化，后续更新追加事实，不抹去旧阶段。

私有仓库需要个人助手通过其已有 GitHub 授权读取。不要将访问令牌、登录 Cookie 或私人材料复制到提示词或公开地址。

维护者每批更新：核事实 → 原子维护 timeline.json 和 history → 同源生成 Markdown 与每日事项 JSON → GitHub 推送并核远端 → 本地看板 → 线上发布回读。保留 task ID，关闭已补齐的缺口，未确认日期和成员状态如实标注。
'''

def export_bundle(file,out):
    from safe_write import atomic_write
    t=json.loads(file.read_text('utf-8'));validate(t);t['revision']=digest(file);out.mkdir(parents=True,exist_ok=True);(out/'progress').mkdir(exist_ok=True)
    for name,text in [('progress/timeline.json',file.read_text('utf-8')),('progress/daily-plan.json',json.dumps(daily_plan(t),ensure_ascii=False,indent=2)+'\n'),('TIMELINE.md',markdown(t)),('ASSISTANT-README.md',ASSISTANT_GUIDE)]:atomic_write(out/name,text)
    return {'assignment_id':t['assignment_id'],'items':len(t['items']),'revision':t['revision'],'output':str(out)}

if __name__=='__main__':
    import argparse,sys
    parser=argparse.ArgumentParser();parser.add_argument('--id',required=True);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'_meta/tools'));files=[f for f in root.glob('*/assignment/graded/*/timeline.json') if json.loads(f.read_text('utf-8')).get('assignment_id')==args.id]
    if len(files)!=1:parser.error('时间线编号不存在或不唯一')
    print(json.dumps(export_bundle(files[0],args.output),ensure_ascii=False))
