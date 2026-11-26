"""Read-only final-review projection. Never writes course learning records."""
import hashlib
import json
from pathlib import Path
from urllib.parse import quote

REPO = 'https://github.com/CercaTrovato/cityu-ai-course-notes/blob/main/'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def load(root, course):
    root = Path(root)
    status = json.loads((root / '_meta/final-review-2026/source-status.json').read_text('utf-8'))
    info = status['courses'][course]
    base = root / info['directory'] / 'review/final-2026'
    raw = (base / 'progress.json').read_bytes()
    progress = json.loads(raw.decode('utf-8-sig'))
    if progress['course'] != course:
        raise ValueError('复习记录课程不匹配')
    units = progress['units']
    ids = {u['id'] for u in units}
    if len(ids) != len(units):
        raise ValueError('复习单元编号重复')
    source_raw = (base / 'sources.json').read_bytes()
    source_data = json.loads(source_raw.decode('utf-8-sig'))
    sources = source_data.get('sources', [])
    source_ids = {s['id'] for s in sources}
    issues = []
    for u in units:
        if not set(u.get('prerequisite_ids', [])).issubset(ids):
            issues.append(u['id'] + ' 前置单元未找到')
        if not set(u.get('source_ids', [])).issubset(source_ids):
            issues.append(u['id'] + ' 来源编号待核')
    # Only these learning documents enter the projection, not audit/private files.
    documents = []
    selected = [base / 'framework.md', base / 'last-class-review.md']
    selected += sorted((base / 'sessions').glob('*.md'))
    selected += sorted((base / 'mistakes').glob('*.md'))
    for file in selected:
        if not file.is_file():
            continue
        real = file.resolve()
        if not real.is_relative_to(base.resolve()):
            raise ValueError('复习资料路径越界')
        content = real.read_bytes()
        text = content.decode('utf-8-sig')
        title = next((line[2:].strip() for line in text.splitlines() if line.startswith('# ')), file.stem)
        rel = file.relative_to(root).as_posix()
        documents.append({'id':file.relative_to(base).as_posix(), 'title':title,
                          'text':text, 'sha256':digest(content), 'url':REPO+quote(rel, safe='/')})
    return {**info, 'exam_basis':status['exam_basis'], 'progress_updated_at':progress.get('updated_at'),
            'progress_sha256':digest(raw), 'sources_sha256':digest(source_raw),
            'framework_status':progress.get('framework_status'), 'issues':issues,
            'units':units, 'sessions':progress.get('sessions', []), 'mistakes':progress.get('mistakes', []),
            'recorded_next_step':progress.get('next_step'), 'documents':documents,
            'source_count':len(sources), 'source_url':REPO+quote((base/'sources.json').relative_to(root).as_posix(),safe='/')}


def attach(records, root):
    errors = []
    if not (Path(root) / '_meta/final-review-2026/source-status.json').exists():
        return errors
    for record in records:
        if record.get('assignment_type') != 'group':
            continue
        try:
            record['review'] = load(root, record['course'])
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append({'path':record['course']+'/review/final-2026', 'message':'复习入口：'+str(exc)})
    return errors
