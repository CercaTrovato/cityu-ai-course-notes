"""Validate and atomically replace one metadata file using its expected SHA-256."""
import argparse
import hashlib
import json
import sys
sys.dont_write_bytecode = True
from datetime import datetime
from pathlib import Path
from server import ROOT, TZ, validate
sys.path.insert(0, str(ROOT / '_meta/tools'))
from safe_write import atomic_write

def apply_candidate(target, candidate, expected_sha, dry_run=False):
    original = target.read_bytes()
    actual = hashlib.sha256(original).hexdigest()
    if actual != expected_sha:
        raise ValueError('元数据已被其他会话修改；重新读取并合并，禁止覆盖。')
    before = json.loads(original.decode('utf-8-sig'))
    after = json.loads(candidate.read_text(encoding='utf-8-sig'))
    if (after.get('id'), after.get('course')) != (before['id'], before['course']):
        raise ValueError('不可改变作业 ID 或课程。')
    issues = validate(after)
    if issues:
        raise ValueError('; '.join(issues))
    if dry_run:
        return {'validated': True, 'written': False, 'expected_sha': actual}
    after['updated_at'] = datetime.now(TZ).isoformat(timespec='seconds')
    history = target.parent / 'metadata-history'
    history.mkdir(exist_ok=True)
    # Full previous revision, uniquely named; never rewrite another revision.
    backup = history / f"{datetime.now(TZ).strftime('%Y%m%dT%H%M%S%f')}-{actual[:12]}.json"
    atomic_write(str(backup), original.decode('utf-8-sig'))
    if hashlib.sha256(target.read_bytes()).hexdigest() != actual:
        raise ValueError('写前检测到并发修改，已停止。')
    text = json.dumps(after, ensure_ascii=False, indent=2) + '\n'
    atomic_write(str(target), text)
    assert target.read_text(encoding='utf-8') == text
    return {'validated': True, 'written': True, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'previous_revision': str(backup)}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--id', required=True)
    p.add_argument('--candidate', required=True, type=Path)
    p.add_argument('--expected-sha', required=True)
    p.add_argument('--dry-run', action='store_true')
    a = p.parse_args()
    matches = [f for f in ROOT.glob('*/assignment/graded/*/assignment.json')
               if json.loads(f.read_text(encoding='utf-8-sig')).get('id') == a.id]
    if len(matches) != 1:
        p.error('作业 ID 不唯一或不存在')
    print(json.dumps(apply_candidate(matches[0], a.candidate, a.expected_sha, a.dry_run), ensure_ascii=False, indent=2))
