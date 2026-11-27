"""Cooperative, non-waiting locks for course review maintenance.

Locks live under the Git common directory, never in published course content.
The CLI PID is acquisition metadata, not proof that the owning agent is alive.
"""
from pathlib import Path
import argparse
import datetime
import json
import subprocess
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[0]))
from safe_write import atomic_write

SCOPES = ['course-AC6761', 'course-EF5560', 'course-IS5113',
          'course-IS5542', 'course-IS6400', 'shared-publish']

def state(root, scope):
    directory = root / scope
    if not directory.exists():
        return {'state': 'free', 'scope': scope}
    try:
        data = json.loads((directory / 'owner.json').read_text('utf-8'))
        return {'state': 'held', **data}
    except (OSError, ValueError):
        return {'state': 'held-owner-unreadable', 'scope': scope}

def acquire(root, scope, owner, job):
    root.mkdir(parents=True, exist_ok=True)
    directory = root / scope
    try:
        directory.mkdir()
    except FileExistsError:
        return False, state(root, scope)
    record = {'scope': scope, 'owner': owner, 'job': job,
              'token': uuid.uuid4().hex,
              'acquired_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    # If writing fails, leave the lock held for explicit recovery.
    atomic_write(str(directory / 'owner.json'), json.dumps(record, ensure_ascii=False, indent=2)+'\n')
    return True, {'state': 'acquired', **record}

def release(root, scope, token):
    current = state(root, scope)
    if current.get('state') != 'held' or current.get('token') != token:
        return False, {'state': 'release-refused', 'scope': scope}
    directory = root / scope
    if directory.is_symlink() or (directory / 'owner.json').is_symlink():
        raise RuntimeError('Refusing to release a redirected lock path')
    (directory / 'owner.json').unlink()
    directory.rmdir()
    return True, {'state': 'released', 'scope': scope}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['acquire', 'status', 'release'])
    parser.add_argument('--scope', required=True, choices=SCOPES)
    parser.add_argument('--owner')
    parser.add_argument('--job')
    parser.add_argument('--token')
    args = parser.parse_args()
    if args.action == 'acquire' and (not args.owner or not args.job):
        parser.error('acquire requires --owner and --job')
    if args.action == 'release' and not args.token:
        parser.error('release requires --token')
    common = Path(subprocess.check_output(['git','rev-parse','--git-common-dir'], text=True).strip()).resolve()
    root = common / 'cityu-review-locks'
    if args.action == 'status':
        result, code = state(root, args.scope), 0
    elif args.action == 'acquire':
        ok, result = acquire(root, args.scope, args.owner, args.job)
        code = 0 if ok else 2
    else:
        ok, result = release(root, args.scope, args.token)
        code = 0 if ok else 3
    print(json.dumps(result, ensure_ascii=False))
    return code

if __name__ == '__main__':
    sys.exit(main())
