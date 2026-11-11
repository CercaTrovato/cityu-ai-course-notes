"""Evidence-backed management view; never turns a receipt into acceptance."""
import json
from pathlib import Path

APP = Path(__file__).resolve().parent
PEOPLE = Path('E:/app-data/codex/outputs/cityu-assignment-board-launcher/people.local.json')
STATES = {'pass', 'gap', 'unknown'}

def validate_project(p, source_ids):
    for key in ('headline', 'situation', 'implication', 'action', 'as_of', 'basis_revision'):
        if not isinstance(p.get(key), str) or not p[key].strip():
            raise ValueError('管理字段缺失：' + key)
    nodes = p.get('deliverables')
    if not isinstance(nodes, list) or not nodes:
        raise ValueError('管理视图需要明确的交付项')
    ids = [n['id'] for n in nodes]
    if len(set(ids)) != len(ids):
        raise ValueError('交付 ID 重复')
    for n in nodes:
        if n.get('receipt') not in ('verified', 'reported', 'none', 'unknown'):
            raise ValueError('无效收件状态')
        if n.get('dispatch') not in ('confirmed', 'proposed', 'unknown'):
            raise ValueError('无效派工状态')
        for key in ('title', 'owner', 'request', 'actual', 'gap', 'next'):
            if not isinstance(n.get(key), str):
                raise ValueError('交付字段缺失：' + key)
        checks = n.get('checks', [])
        if not checks or len({c['id'] for c in checks}) != len(checks):
            raise ValueError('验收项为空或重复')
        for c in checks:
            if c.get('status') not in STATES:
                raise ValueError('无效验收状态')
            if c['status'] != 'unknown' and not c.get('evidence'):
                raise ValueError('已核验收结论必须有来源')
            if not set(c.get('evidence', [])).issubset(source_ids):
                raise ValueError('验收来源不存在')
        if n['receipt'] != 'verified' and any(c['status'] == 'pass' for c in checks):
            raise ValueError('没有可核版本时不能记为已验证通过')
    edges = p.get('edges', [])
    graph = {i: [] for i in ids}
    by_id = {n['id']: n for n in nodes}
    for e in edges:
        if e['from'] not in graph or e['to'] not in graph or e['from'] == e['to']:
            raise ValueError('依赖指向无效')
        if e['kind'] not in ('required', 'parallel'):
            raise ValueError('依赖类型无效')
        available = {c['id'] for c in by_id[e['from']]['checks']}
        if not set(e.get('requires', [])).issubset(available):
            raise ValueError('依赖验收项不存在')
        graph[e['from']].append(e['to'])
    visiting, visited = set(), set()
    def visit(n):
        if n in visiting:
            raise ValueError('依赖有环；反馈实验请拆为独立轮次')
        if n in visited:
            return
        visiting.add(n)
        for target in graph[n]: visit(target)
        visiting.remove(n); visited.add(n)
    for n in ids: visit(n)

def enrich(record, config, people=None):
    p = json.loads(json.dumps(config))
    validate_project(p, {s['id'] for s in record['sources']})
    coordination_sha = (record.get('coordination') or {}).get('coordination_sha256')
    p['fresh'] = p['basis_revision'] == record['revision'] and p.get('basis_coordination_revision') == coordination_sha and not any(w.startswith('依据') for w in record.get('warnings', []))
    p['freshness_note'] = '' if p['fresh'] else '来源或课程状态已更新，以下管理拆解为历史快照，需总监督复核。最新原始记录仍可查看。'
    people = people or {}
    for n in p['deliverables']:
        n['owner_label'] = people.get(n['owner'], n['owner'])
        n['passed'] = sum(c['status'] == 'pass' for c in n['checks'])
        n['gaps'] = sum(c['status'] == 'gap' for c in n['checks'])
        n['unknown'] = sum(c['status'] == 'unknown' for c in n['checks'])
        n['total'] = len(n['checks'])
        n['accepted'] = n['passed'] == n['total'] and n['receipt'] == 'verified'
        n['state'] = 'accepted' if n['accepted'] else 'reported' if n['receipt']=='reported' else 'rework' if n['gaps'] else 'review' if n['receipt']=='verified' else 'waiting'
    by_id = {n['id']:n for n in p['deliverables']}
    for e in p['edges']:
        n = by_id[e['from']]
        required = e.get('requires') or [c['id'] for c in n['checks']]
        e['satisfied'] = e['kind'] == 'parallel' or all(c['status']=='pass' for c in n['checks'] if c['id'] in required)
    for n in p['deliverables']:
        n['blocked_by'] = [e['from'] for e in p['edges'] if e['to']==n['id'] and e['kind']=='required' and not e['satisfied']]
    nodes = [n for n in p['deliverables'] if n.get('scope') != 'supporting']
    p['metrics'] = {'accepted':sum(n['accepted'] for n in nodes),'received':sum(n['receipt']=='verified' for n in nodes),
                    'reported':sum(n['receipt']=='reported' for n in nodes),'total':len(nodes),
                    'pass':sum(n['passed'] for n in nodes),'gap':sum(n['gaps'] for n in nodes),
                    'unknown':sum(n['unknown'] for n in nodes),'checks':sum(n['total'] for n in nodes),'supporting':sum(n.get('scope')=='supporting' for n in p['deliverables'])}
    return p

def attach(records, config_path=None):
    path = config_path or APP / 'management.json'
    if not path.exists() and path != APP / 'management.json':
        return []
    try:
        configs = json.loads(path.read_text(encoding='utf-8'))['projects']
    except (OSError, ValueError, KeyError) as exc:
        return [{'path':'management.json','message':str(exc)}]
    try:
        people = json.loads(PEOPLE.read_text(encoding='utf-8')) if PEOPLE.exists() else {}
        if not isinstance(people,dict) or not all(isinstance(v,str) for v in people.values()): people={}
    except (OSError, ValueError): people={}
    errors=[]
    for r in records:
        if r['id'] not in configs: continue
        try: r['management']=enrich(r, configs[r['id']], people)
        except (ValueError,KeyError,TypeError) as exc:
            errors.append({'path':'management.json / '+r['id'],'message':str(exc)})
    return errors
