"""Check stable review frameworks and record references; never certify mastery."""
from pathlib import Path
import argparse
import hashlib
import json

STABLE_KEYS = ('id', 'title', 'prerequisite_ids', 'question_types',
               'learning_objective', 'learning_goal', 'outcomes')


def contract(unit):
    value = {key: unit[key] for key in STABLE_KEYS if key in unit}
    if 'subunits' in unit:
        value['subunits'] = [contract(child) for child in unit['subunits']]
    return value


def check(root, course=None):
    root = Path(root).resolve()
    results, errors = [], []
    for lock_path in sorted(root.glob('*/review/final-2026/framework-lock.json')):
        lock = json.loads(lock_path.read_text('utf-8-sig'))
        code = lock['course']
        if course and code != course:
            continue
        base = lock_path.parent
        progress = json.loads((base / 'progress.json').read_text('utf-8-sig'))
        local_errors = []
        if progress['course'] != code:
            local_errors.append('课程身份不一致')
        if hashlib.sha256((base / 'framework.md').read_bytes()).hexdigest() != lock['framework_sha256']:
            local_errors.append('固定框架正文变化：请核本人决定和版本，不自动重置锁')
        if [contract(unit) for unit in progress['units']] != lock['unit_contracts']:
            local_errors.append('稳定单元结构变化：请核ID、目标、依赖及题型')
        ids = {unit['id'] for unit in progress['units']}
        all_ids = set(ids)
        for unit in progress['units']:
            all_ids.update(child['id'] for child in unit.get('subunits', []))
            if not set(unit.get('prerequisite_ids', [])) <= ids:
                local_errors.append(unit['id'] + ' 前置引用不存在')
        if len(ids) != len(progress['units']):
            local_errors.append('主单元ID重复')
        for name in ('exam-guide.md', 'preparation.md', 'route.md', 'handover.md'):
            if not (base / name).is_file():
                local_errors.append('缺工作文件：' + name)
        for name in ('README.md', 'AGENTS.md', 'CLAUDE.md'):
            if not (base.parent / name).is_file():
                local_errors.append('缺工作入口：' + name)
        for kind in ('sessions', 'mistakes'):
            records = progress.get(kind, [])
            if not isinstance(records, list):
                local_errors.append(kind + '必须为数组')
                continue
            for record in records:
                if not isinstance(record, dict):
                    local_errors.append(kind + '条目必须保留结构化记录')
                    continue
                refs = record.get('unit_ids', [])
                if record.get('unit_id'):
                    refs = [*refs, record['unit_id']]
                if not set(refs) <= all_ids:
                    local_errors.append(kind + '含未知单元引用')
                link = record.get('path') or record.get('file')
                if link:
                    target = (base / link).resolve()
                    if not target.is_relative_to(base) or not target.is_file():
                        local_errors.append(kind + '文件引用缺失或越界：' + str(link))
        result = {'course': code, 'units': len(ids), 'subunits': len(all_ids)-len(ids),
                  'sessions': len(progress.get('sessions', [])),
                  'mistakes': len(progress.get('mistakes', [])), 'errors': local_errors}
        results.append(result)
        errors.extend(code + ': ' + error for error in local_errors)
    if not results:
        errors.append('未找到指定课程工作区')
    return {'courses': results, 'errors': errors,
            'scope': '只核结构/引用/固定框架；不认证教学、学习掌握或三端同步'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--course')
    parser.add_argument('--root', default=str(Path(__file__).resolve().parents[2]))
    args = parser.parse_args()
    result = check(args.root, args.course)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['errors']))
