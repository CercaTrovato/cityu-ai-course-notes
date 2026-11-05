"""课程隔离的完整性快照；复用现行完整性判据，不写共享 manifest。"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import integrity_check as base
from safe_write import atomic_write


def collect(root, course):
    scope = (root / course).resolve()
    if scope.parent != root or not scope.is_dir():
        raise ValueError('course 必须是 vault 下一个现有课程目录')
    base.ROOT = str(root)
    records = {}
    for path in sorted(scope.rglob('*.md')):
        if 'course_files_export' in path.relative_to(scope).parts:
            continue
        rel = path.relative_to(root).as_posix()
        item = base.info(rel)
        item['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        records[rel] = item
    return records


def compare(old, current, allow):
    errors, changed = [], []
    for rel, item in current.items():
        if not item['utf8']:
            errors.append({'file': rel, 'issue': 'utf8'})
        elif not base.tail_ok(rel, item):
            errors.append({'file': rel, 'issue': 'tail'})
        previous = old.get(rel)
        if previous is None:
            changed.append({'file': rel, 'change': 'added'})
        elif previous['sha256'] != item['sha256']:
            changed.append({'file': rel, 'change': 'modified'})
            if item['bytes'] < previous['bytes'] * 0.8 and rel not in allow:
                errors.append({'file': rel, 'issue': 'shrink_over_20_percent'})
    for rel in old.keys() - current.keys():
        changed.append({'file': rel, 'change': 'deleted'})
        errors.append({'file': rel, 'issue': 'missing'})
    return errors, changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['snapshot', 'verify'])
    parser.add_argument('--course', required=True)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--root', default=Path(__file__).resolve().parents[2])
    parser.add_argument('--allow', nargs='*', default=[])
    parser.add_argument('--report')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    manifest = Path(args.manifest).resolve()
    if manifest == (root / '_meta/tools/integrity_manifest.json').resolve():
        raise ValueError('禁止覆盖共享 integrity_manifest')
    if args.operation == 'snapshot' and manifest.exists():
        raise ValueError('已有基线不可覆盖；续接用 verify，新任务用新 manifest')
    current = collect(root, args.course)
    if args.operation == 'snapshot':
        payload = {'schema': 'cityu-course-integrity-v1', 'root': str(root), 'course': args.course,
                   'time_utc': datetime.now(timezone.utc).isoformat(), 'files': current}
        errors, _ = compare(current, current, set())
        manifest.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(str(manifest), json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
        result = {'operation': 'snapshot', 'files': len(current), 'manifest': str(manifest), 'errors': errors}
    else:
        payload = json.loads(manifest.read_text(encoding='utf-8'))
        if payload.get('schema') != 'cityu-course-integrity-v1' or Path(payload['root']).resolve() != root or payload['course'] != args.course:
            raise ValueError('基线的 root/course/schema 与本次不符')
        errors, changed = compare(payload['files'], current, set(args.allow))
        result = {'operation': 'verify', 'files': len(current), 'errors': errors, 'changed': changed}
    if args.report:
        path=Path(args.report); path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(str(path), json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
