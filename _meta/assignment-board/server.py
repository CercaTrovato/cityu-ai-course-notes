"""Read-only, loopback-only CityU assignment dashboard. No course files are executed."""
from __future__ import annotations
import argparse
import hashlib
import json
from datetime import datetime, date, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from jsonschema import Draft202012Validator, FormatChecker

APP = Path(__file__).resolve().parent
ROOT = APP.parent.parent
TZ = timezone(timedelta(hours=8))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate(record):
    schema = json.loads((APP / 'schema.json').read_text(encoding='utf-8'))
    issues = [f"{'/'.join(map(str, e.absolute_path))}: {e.message}" for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record)]
    if issues:
        return issues
    sources = {x['id'] for x in record['sources']}
    for key in ('sources', 'tasks', 'milestones'):
        ids = [x['id'] for x in record[key]]
        if len(ids) != len(set(ids)):
            issues.append(f'{key}: 重复 ID')
    for item in record['tasks'] + record['milestones']:
        if not set(item['evidence']).issubset(sources):
            issues.append(f"{item['id']}: 引用了不存在的证据")
        if item['status'] in ('done', 'submitted') and not item['evidence']:
            issues.append(f"{item['id']}: 完成或提交必须有证据")
    for m in record['milestones']:
        value = m['due']
        if m['precision'] == 'datetime':
            try:
                dt = datetime.fromisoformat(value)
                if dt.utcoffset() is None:
                    raise ValueError()
            except (ValueError, TypeError):
                issues.append(f"{m['id']}: 精确截止必须为带时区的 ISO 时间")
        elif m['precision'] in ('date', 'before_date'):
            try:
                date.fromisoformat(value)
            except (ValueError, TypeError):
                issues.append(f"{m['id']}: 日期格式无效")
        elif value is not None:
            issues.append(f"{m['id']}: 未知日期必须为 null")
    if not set(record['submission']['evidence']).issubset(sources):
        issues.append('submission: 引用了不存在的证据')
    if record['submission']['status'] in ('submitted', 'graded') and not record['submission']['evidence']:
        issues.append('submission: 已提交或已评分必须有证据')
    return issues

def due_state(m, now):
    if m['status'] in ('done', 'submitted'):
        return '已完成'
    if m['due'] is None:
        return '日期待确认'
    if m['precision'] == 'datetime':
        delta = (datetime.fromisoformat(m['due']) - now).total_seconds()
        return '已到期 · 待核提交' if delta < 0 else ('72 小时内' if delta <= 259200 else '计划中')
    day = date.fromisoformat(m['due'])
    today = now.astimezone(TZ).date()
    if m['precision'] == 'before_date' and today >= day:
        return '已到截止边界 · 待核提交'
    if today > day:
        return '日期已过 · 待核提交'
    if today == day:
        return '今天 · 时刻待确认'
    return '3 天内 · 时刻未定' if (day - today).days <= 3 else '计划中'

def load_supervision(root):
    folder = root / '_meta/assignment-board'
    result = {}
    errors = []
    for filename in ('supervision.json', 'supervisor-reviews.json'):
        path = folder / filename
        try:
            value = json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else {}
            if not isinstance(value, dict) or not isinstance(value.get('assignments', {}), dict):
                raise ValueError('必须包含 assignments 对象')
            result[filename] = value.get('assignments', {})
        except (ValueError, OSError) as e:
            errors.append({'path': path.relative_to(root).as_posix(), 'message': str(e)})
            result[filename] = {}
    return result['supervision.json'], result['supervisor-reviews.json'], errors

def read_coordination(folder, root, record, registration, review, now):
    path = folder / 'coordination.json'
    if not path.exists():
        return ({**registration, 'status': 'dispatched', 'summary': '已派出；尚未收到课程会话的阶段记录',
                 'updated_at': registration['dispatched_at'], 'decisions': [], 'review_status': '待首次回传'}
                if registration else None)
    c = json.loads(path.read_text(encoding='utf-8-sig'))
    schema = json.loads((APP / 'coordination-schema.json').read_text(encoding='utf-8'))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(c)
    if c['assignment_id'] != record['id']:
        raise ValueError('协调记录的 assignment_id 与所属作业不符')
    if registration and c['thread_id'] != registration['thread_id']:
        raise ValueError('协调记录的 thread_id 与派出登记不符')
    if len({d['id'] for d in c['decisions']}) != len(c['decisions']):
        raise ValueError('决策 ID 重复')
    for d in c['decisions']:
        if d['status'] == 'decided' and (not d['answer'] or not d['answer_source']):
            raise ValueError('已决定事项缺少本人答复或来源')
    if c['status'] == 'waiting_user' and not any(d['status'] == 'pending' for d in c['decisions']):
        raise ValueError('等待本人状态须列出具体待决定问题')
    report = (root / c['report_path']).resolve()
    if not report.is_relative_to(folder.resolve()) or report.suffix != '.md':
        raise ValueError('报告必须为本作业目录内的 Markdown 文件')
    c['report_exists'] = report.is_file()
    c['report_sha256'] = digest(report) if report.is_file() else None
    c['coordination_sha256'] = digest(path)
    if c['status'] in ('ready_for_review', 'complete') and not c['report_exists']:
        raise ValueError('已回传阶段缺少报告文件')
    c['title'] = registration.get('title', record['course'] + ' 工作会话') if registration else record['course'] + ' 工作会话'
    c['age_minutes'] = max(0, round((now - datetime.fromisoformat(c['updated_at'])).total_seconds() / 60))
    reviewed = review and all(review.get(key) == value for key, value in (
        ('metadata_sha256', record['revision']), ('coordination_sha256', c['coordination_sha256']), ('report_sha256', c['report_sha256'])))
    c['review_status'] = ('已核对本阶段 · ' + review.get('reviewed_at', '')) if reviewed else ('阶段记录已更新 · 待监督核对' if review else '尚未核对本阶段')
    c['review_note'] = review.get('note', '') if reviewed else ''
    return c

def collect(root=ROOT, now=None):
    now = now or datetime.now(TZ)
    records, errors, missing = [], [], []
    registry, reviews, registry_errors = load_supervision(root)
    errors.extend(registry_errors)
    for folder in sorted(root.glob('*/assignment/graded/*')):
        if not folder.is_dir():
            continue
        path = folder / 'assignment.json'
        if not path.exists():
            missing.append(folder.relative_to(root).as_posix())
            continue
        try:
            raw = path.read_bytes()
            r = json.loads(raw.decode('utf-8-sig'))
            issues = validate(r)
            expected = folder.parents[2].name.split('_')[0] + '-' + folder.name.split('-')[0]
            if r.get('id') != expected:
                issues.append(f'ID 应为 {expected}')
            if issues:
                raise ValueError('; '.join(issues))
            r['metadata_path'] = path.relative_to(root).as_posix()
            r['revision'] = hashlib.sha256(raw).hexdigest()
            r['warnings'] = []
            for s in r['sources']:
                if s['kind'] in ('local', 'external_file'):
                    p = (root / s['locator']).resolve() if s['kind'] == 'local' else Path(s['locator']).resolve()
                    if s['kind'] == 'local' and not p.is_relative_to(root.resolve()):
                        r['warnings'].append(f"依据路径越出课程库：{s['label']}")
                    elif not p.is_file():
                        r['warnings'].append(f"依据文件缺失：{s['label']}")
                    elif s.get('sha256') and digest(p) != s['sha256']:
                        r['warnings'].append(f"依据已变更，请复核进度：{s['label']}")
            observed = date.fromisoformat(r['progress_as_of']) if r['progress_as_of'] else None
            r['age_days'] = (now.date() - observed).days if observed else None
            if observed and r['age_days'] >= 7 and r['board_scope'] == 'active':
                r['warnings'].append(f"制作状态已有 {r['age_days']} 天未更新")
            counts = {s: sum(t['status'] == s for t in r['tasks']) for s in ('done', 'in_progress', 'todo', 'blocked', 'unknown')}
            r['counts'] = counts
            r['completion_percent'] = round(100 * counts['done'] / len(r['tasks'])) if r['task_scope_complete'] and r['tasks'] else None
            for m in r['milestones']:
                m['urgency'] = due_state(m, now)
            try:
                r['coordination'] = read_coordination(folder, root, r, registry.get(r['id']), reviews.get(r['id'], {}), now)
            except Exception as e:
                # A malformed progress report must never hide the underlying assignment.
                r['coordination'] = None
                errors.append({'path': (folder / 'coordination.json').relative_to(root).as_posix(), 'message': str(e)})
            records.append(r)
        except (ValueError, TypeError, KeyError, OSError) as e:
            errors.append({'path': path.relative_to(root).as_posix(), 'message': str(e)})
    ids = [r['id'] for r in records]
    if len(ids) != len(set(ids)):
        errors.append({'path': '', 'message': '发现重复作业 ID，不能视为有效快照'})
    from management import attach
    errors.extend(attach(records, root / '_meta/assignment-board/management.json'))
    from timeline import attach as attach_timeline
    errors.extend(attach_timeline(records, root))
    return {'generated_at': now.isoformat(timespec='seconds'), 'root': str(root), 'poll_seconds': 5,
            'assignments': records, 'errors': errors, 'missing': missing}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Reject cross-site DNS rebinding; do not expose repository file serving.
        if self.headers.get('Host') not in (f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'):
            self.send_error(403)
            return
        status = 200
        route = urlparse(self.path).path
        if route == '/api/assignments':
            data, kind = json.dumps(collect(), ensure_ascii=False).encode('utf-8'), 'application/json; charset=utf-8'
        elif route.startswith('/api/thinking/'):
            import thinking
            try:
                parts = route.strip('/').split('/')
                if len(parts) == 3:
                    result = thinking.load(ROOT, parts[2])
                elif len(parts) == 5 and parts[3] == 'source':
                    result = thinking.source_content(ROOT, parts[2], parts[4])
                else:
                    raise ValueError('思路接口路径无效')
                data = json.dumps(result, ensure_ascii=False).encode('utf-8')
            except (ValueError, KeyError, TypeError, OSError) as exc:
                status = 400
                data = json.dumps({'error': str(exc)}, ensure_ascii=False).encode('utf-8')
            kind = 'application/json; charset=utf-8'
        elif route.startswith('/report/'):
            assignment = next((r for r in collect()['assignments'] if r['id'] == route.removeprefix('/report/')), None)
            c = assignment.get('coordination') if assignment else None
            if not c or not c.get('report_exists'):
                self.send_error(404)
                return
            data, kind = (ROOT / c['report_path']).read_bytes(), 'text/plain; charset=utf-8'
        elif route in ('/', '/index.html'):
            data, kind = (APP / 'index.html').read_bytes(), 'text/html; charset=utf-8'
        elif route in ('/board.css', '/board.js', '/thinking.css', '/thinking.js', '/timeline.js', '/timeline.css', '/classic.html'):
            kind = {'/board.css':'text/css; charset=utf-8','/board.js':'text/javascript; charset=utf-8','/classic.html':'text/html; charset=utf-8','/thinking.css':'text/css; charset=utf-8','/thinking.js':'text/javascript; charset=utf-8','/timeline.js':'text/javascript; charset=utf-8','/timeline.css':'text/css; charset=utf-8'}[route]
            data = (APP / route.lstrip('/')).read_bytes()
        elif route == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return
        else:
            self.send_error(404)
            return
        self.send_response(status)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        if args and str(args[1] if len(args) > 1 else '') != '200':
            super().log_message(fmt, *args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8766)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        data = collect()
        print(json.dumps({'count': len(data['assignments']), 'errors': data['errors'], 'missing': data['missing'],
                          'warnings': {r['id']: r['warnings'] for r in data['assignments'] if r['warnings']}}, ensure_ascii=False, indent=2))
        raise SystemExit(bool(data['errors'] or data['missing']))
    service = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'CityU action board: http://127.0.0.1:{args.port}', flush=True)
    service.serve_forever()
