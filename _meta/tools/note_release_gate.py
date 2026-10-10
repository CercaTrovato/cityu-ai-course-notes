"""笔记发布前置检查：机械门槛 + 与候选绑定的实质核对记录。

不写笔记，不认证记录中的语义判断。新稿 --scope full；局部融合 --scope changed。
--check-only 仅预检；正式发布必须带 --review，并在原子写前再次核对源哈希。
"""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from note_quality import frontmatter, readability_checks

HERE = Path(__file__).resolve().parent


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def version(text):
    return frontmatter(text).get('readability_rules', '').split('#', 1)[0].strip().strip('\"\'')


def inherited_hard(issue, before, after, baseline):
    """仅放行未启用 v1/v2 的旧稿中，完整未变教学单元内原有的 R 硬项。

    行号移动不影响判断；在同一单元换掉问题句不能借原问题数量抵消。
    全文分布项只允许原有指标不恶化，不能据此声称全篇通过。
    """
    code, line, detail = issue
    if not line:
        now = readability_checks(after)['stats']
        old = baseline['stats']
        keys = {'R1b': ('p90', 'long_share'), 'R0': ('exempt',)}.get(code, ())
        return bool(keys) and any(x[0] == code and not x[1] for x in baseline['hard']) and all(now.get(k, 0) <= old.get(k, 0) for k in keys)
    new_lines, old_lines = after.splitlines(), before.splitlines()
    start = line - 1
    while start > 0 and not re.match(r'^#{1,4} ', new_lines[start]):
        start -= 1
    end = line
    while end < len(new_lines) and not re.match(r'^#{1,4} ', new_lines[end]):
        end += 1
    for a, b, size in difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False).get_matching_blocks():
        if b <= start and end <= b + size:
            old_line = a + line - b
            return any(tuple(x) == (code, old_line, detail) for x in baseline['hard'])
    return False


def quality_gate(candidate, note, source=None, scope='changed', pages=0):
    candidate, note = Path(candidate), Path(note)
    after = candidate.read_text(encoding='utf-8')
    before = Path(source).read_text(encoding='utf-8') if source else ''
    errors = []
    if scope == 'changed' and not source:
        errors.append('局部修改缺少原始副本，无法识别本次范围')
    if scope == 'full' or not source:
        if version(after) != 'v2':
            errors.append('新写或整篇整改必须保留 readability_rules: v2')
    elif version(before) in ('v1', 'v2') and version(after) not in ('v1', 'v2'):
        errors.append('不能移除已有 readability_rules 来绕过 R 层')
    elif version(before) == 'v2' and version(after) != 'v2':
        errors.append('不能把 readability_rules: v2 降级')
    cmd = [sys.executable, str(HERE / 'note_quality.py'), str(candidate), '--json', '--strict', '--sections', '--readability', '--pages', str(pages)]
    # scratch 中常叫 merged.md / candidate.md，不能因此把 T 笔记误当 M。
    if re.match(r'T\d', note.name):
        cmd.append('--tut')
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=HERE.parent.parent)
    output = (proc.stdout or '') + (proc.stderr or '')
    payloads = [line[5:] for line in output.splitlines() if line.startswith('JSON:')]
    try:
        data = json.loads(payloads[0]) if len(payloads) == 1 else None
        if proc.returncode not in (0, 1) or not isinstance(data, dict):
            raise ValueError('检查器未正常完成或缺少唯一 JSON 结果')
        if not isinstance(data['legacy_problems'], list) or not isinstance(data['R']['hard'], list):
            raise ValueError('缺少 L/R 检查结果')
        if data['legacy_problems']:
            errors.append('L 格式/覆盖检查有 %d 项，须定位处理，不能用 G/E PASS 覆盖' % len(data['legacy_problems']))
        hard = data['R']['hard']
        if scope == 'changed' and source and not version(before) and not version(after):
            baseline = readability_checks(before, bool(re.match(r'T\d', note.name)), str(note))
            blocked = [x for x in hard if not inherited_hard(x, before, after, baseline)]
            output += '\nR 历史未变项 %d；本次阻塞项 %d（非全篇通过）\n' % (len(hard) - len(blocked), len(blocked))
        else:
            blocked = hard
        if blocked:
            errors.append('R 机械硬项未清零：%d 项' % len(blocked))
        # 旧 G/E 判定只如实保留在原始输出；不能用凑字数/标签替代教学验收。
    except (ValueError, KeyError, TypeError) as exc:
        errors.append('无法可靠读取检查结果：%s' % exc)
    output += '\n发布机械门槛：' + ('FAIL\n' + '\n'.join(errors) if errors else 'PASS（不代表教学或视觉通过）') + '\n'
    return not errors, output


def review_gate(review, candidate, note, source=None, scope='changed'):
    """核验回执完整性与版本绑定；记录内容仍由执行者据实负责。"""
    errors = []
    try:
        review = Path(review)
        data = json.loads(review.read_text(encoding='utf-8'))
        expected = {
            'schema': 'note-review-v1', 'note': Path(note).as_posix(), 'scope': scope,
            'source_sha256': sha256(source) if source else None,
            'candidate_sha256': sha256(candidate),
        }
        for key, value in expected.items():
            if data.get(key) != value:
                errors.append('回执 %s 与本次候选/基线不一致' % key)
        if data.get('unresolved') != []:
            errors.append('回执尚有缺口或未明确列出 unresolved: []')
        evidence = review.parent / data['review_file']
        if not evidence.read_text(encoding='utf-8').strip() or sha256(evidence) != data['review_sha256']:
            errors.append('实质核对报告为空或哈希已变')
        for key in ('understanding', 'sources', 'warnings', 'visuals'):
            check = data['checks'][key]
            allowed = ('passed', 'not_applicable') if key == 'visuals' else ('passed',)
            if check.get('status') not in allowed or not isinstance(check.get('evidence'), str) or not check['evidence'].strip():
                errors.append('%s 未完成或缺少证据位置' % key)
        if not isinstance(data.get('assets'), list):
            errors.append('须显式列出已核对图源/渲染资产 assets（无外部资产填 []）')
        else:
            for asset in data['assets']:
                if sha256(review.parent / asset['path']) != asset['sha256']:
                    errors.append('已核对资产内容已变：%s' % asset['path'])
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append('教学核对记录无效或缺失：%s' % exc)
    return not errors, '\n'.join(errors) or '教学核对记录完整且哈希一致（不代替实际语义/视觉判断）'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('candidate')
    ap.add_argument('--note', required=True, help='正式目标路径；建议 vault 相对路径')
    ap.add_argument('--source', help='本次修改前的原始副本；新笔记不传')
    ap.add_argument('--scope', choices=('full', 'changed'), required=True)
    ap.add_argument('--pages', type=int, default=0)
    ap.add_argument('--review', help='review.json，正式发布必需')
    ap.add_argument('--check-only', action='store_true', help='只做机械预检，不能用于宣布可发布')
    args = ap.parse_args()
    if args.scope == 'changed' and not args.source:
        ap.error('局部修改必须提供 --source')
    ok, output = quality_gate(args.candidate, args.note, args.source, args.scope, args.pages)
    print(output)
    if args.check_only:
        print('仅机械预检；尚未验教学记录，不构成发布授权。')
        return 0 if ok else 1
    reviewed, message = review_gate(args.review or '', args.candidate, args.note, args.source, args.scope)
    print(message)
    return 0 if ok and reviewed else 1


if __name__ == '__main__':
    sys.exit(main())
