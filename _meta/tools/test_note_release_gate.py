"""发布门槛回归：检查器失败、R 漏放、证据缺失/失效不得写回。"""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import note_release_gate as gate
import merge_apply as merge

SCRATCH = Path('E:/app-data/codex/scratchpad/cityu-readability-gates')


class ReleaseGate(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='test-', dir=SCRATCH)
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)
        self.source = self.work / 'before.md'
        self.candidate = self.work / 'candidate.md'
        self.text = '---\ncourse: AC6761\nreadability_rules: v2\n---\n\n## 2. 正文\n\n### 2.1 对象（讲义 p.1）\n\n一个对象。\n'
        self.source.write_text(self.text, encoding='utf-8')
        self.candidate.write_text(self.text, encoding='utf-8')
        self.note = 'AC6761_Artificial_Intelligence_Accounting/notes/M01-test.md'

    def result(self, hard=None, problems=None, verdict='FAIL', rc=1):
        payload = dict(verdict=verdict, legacy_problems=problems or [], R=dict(hard=hard or [], warn=[]))
        return SimpleNamespace(returncode=rc, stdout='JSON:' + json.dumps(payload), stderr='')

    def check(self, result, **kwargs):
        with patch.object(gate.subprocess, 'run', return_value=result):
            return gate.quality_gate(self.candidate, self.note, self.source, **kwargs)

    def test_old_ge_failure_remains_diagnostic(self):
        ok, output = self.check(self.result())
        self.assertTrue(ok)
        self.assertIn('FAIL', output)
        self.assertIn('不代表教学', output)

    def test_r_failure_blocks_even_when_l_is_zero(self):
        with patch.object(merge, 'run', return_value=(0, 'audit PASS')), patch.object(gate.subprocess, 'run', return_value=self.result(hard=[['R5e', 9, '小数缺零']])):
            audit, quality, _, _ = merge.verify(str(self.candidate), ['transcript.txt'], 1, str(self.source), self.note)
        self.assertTrue(audit)
        self.assertFalse(quality)

    def test_l_cannot_hide_behind_pass_verdict(self):
        ok, _ = self.check(self.result(problems=['L3 broken table'], verdict='PASS'))
        self.assertFalse(ok)

    def test_checker_crash_missing_or_malformed_json_blocks(self):
        for output, rc in [('Traceback', 1), ('', 0), ('JSON:broken', 1), ('JSON:{}', 0), (self.result().stdout, 2)]:
            with self.subTest(output=output, rc=rc):
                ok, _ = self.check(SimpleNamespace(returncode=rc, stdout=output, stderr=''))
                self.assertFalse(ok)

    def test_partial_audit_crash_does_not_pass(self):
        with patch.object(merge, 'run', return_value=(1, 'Traceback')), patch.object(merge, 'quality_gate', return_value=(True, 'ok')):
            self.assertFalse(merge.verify(str(self.candidate), ['t.txt'], 1, str(self.source), self.note, partial=True)[0])

    def test_tutorial_target_controls_type_not_candidate_name(self):
        with patch.object(gate.subprocess, 'run', return_value=self.result()) as call:
            gate.quality_gate(self.candidate, 'course/notes/T01-test.md', self.source)
        self.assertIn('--tut', call.call_args.args[0])

    def test_full_requires_v2_and_local_cannot_drop_or_downgrade(self):
        for replacement in ('', 'readability_rules: v1\n'):
            self.candidate.write_text(self.text.replace('readability_rules: v2\n', replacement), encoding='utf-8')
            for scope in ('full', 'changed'):
                with self.subTest(scope=scope, replacement=replacement):
                    self.assertFalse(self.check(self.result(), scope=scope)[0])

    def test_legacy_unchanged_section_can_move(self):
        before = '## 2. 正文\n\n### 2.1 标题\n\n取 .5。\n\n### 2.2 后节\n\n旧内容。\n'
        after = '新增导读。\n\n' + before.replace('旧内容。', '新增内容。')
        baseline = gate.readability_checks(before)
        issue = next(x for x in gate.readability_checks(after)['hard'] if x[0] == 'R5e')
        self.assertTrue(gate.inherited_hard(issue, before, after, baseline))

    def test_legacy_new_error_cannot_offset_old_count(self):
        before = '### 2.1 标题\n\n取 .5。\n'
        after = before.replace('.5', '.6')
        issue = next(x for x in gate.readability_checks(after)['hard'] if x[0] == 'R5e')
        self.assertFalse(gate.inherited_hard(issue, before, after, gate.readability_checks(before)))

    def receipt(self):
        evidence = self.work / 'review.md'
        evidence.write_text('测试证据：理解链、来源、疑点、图均已核对。仅测试夹具。', encoding='utf-8')
        data = dict(schema='note-review-v1', note=self.note, scope='changed', source_sha256=gate.sha256(self.source), candidate_sha256=gate.sha256(self.candidate), review_file=evidence.name, review_sha256=gate.sha256(evidence), checks={key: dict(status='passed', evidence='review.md 中对应证据') for key in ('understanding', 'sources', 'warnings', 'visuals')}, assets=[], unresolved=[])
        path = self.work / 'review.json'
        path.write_text(json.dumps(data), encoding='utf-8')
        return path, data

    def review(self, path):
        return gate.review_gate(path, self.candidate, self.note, self.source)

    def test_missing_receipt_blocks(self):
        self.assertFalse(self.review(self.work / 'missing.json')[0])

    def test_bound_receipt_accepts(self):
        path, _ = self.receipt()
        self.assertTrue(self.review(path)[0])

    def test_candidate_source_or_report_change_invalidates(self):
        for name in ('candidate.md', 'before.md', 'review.md'):
            with self.subTest(name=name):
                path, _ = self.receipt()
                target = self.work / name
                old = target.read_bytes()
                target.write_bytes(old + b'\nchanged')
                self.assertFalse(self.review(path)[0])
                target.write_bytes(old)

    def test_pending_gaps_wrong_scope_or_missing_check_blocks(self):
        for key in ('pending', 'gap', 'scope', 'missing'):
            path, data = self.receipt()
            if key == 'pending': data['checks']['visuals']['status'] = 'pending'
            if key == 'gap': data['unresolved'] = ['图尚未查看']
            if key == 'scope': data['scope'] = 'full'
            if key == 'missing': del data['checks']['understanding']
            path.write_text(json.dumps(data), encoding='utf-8')
            with self.subTest(key=key):
                self.assertFalse(self.review(path)[0])

    def test_changed_visual_asset_invalidates(self):
        path, data = self.receipt()
        asset = self.work / 'diagram.svg'
        asset.write_text('<svg/>', encoding='utf-8')
        data['assets'] = [dict(path=asset.name, sha256=gate.sha256(asset))]
        path.write_text(json.dumps(data), encoding='utf-8')
        self.assertTrue(self.review(path)[0])
        asset.write_text('<svg>changed</svg>', encoding='utf-8')
        self.assertFalse(self.review(path)[0])

    def setup_merge(self):
        target = self.work / 'course/notes/M01-test.md'
        target.parent.mkdir(parents=True)
        target.write_text(self.text, encoding='utf-8')
        work = self.work / 'merge'
        (work / 'shard_1').mkdir(parents=True)
        (work / 'shard_1/patch.json').write_text('{"cells": [], "s8": []}', encoding='utf-8')
        args = ['merge_apply.py', str(work), '--note', 'course/notes/M01-test.md', '--pages', '1', '--transcript', 'source.txt']
        return target, work, args

    def test_apply_without_receipt_never_calls_writer(self):
        target, work, args = self.setup_merge()
        initial = target.read_bytes()
        with patch.object(merge, 'ROOT', str(self.work)), patch.object(sys, 'argv', args), patch.object(merge, 'verify', return_value=(True, True, 'audit PASS', 'mechanical PASS')), patch.object(merge, 'atomic_write') as writer:
            with self.assertRaises(SystemExit) as raised:
                merge.main()
            self.assertEqual(raised.exception.code, 1)
            writer.assert_not_called()
        self.assertEqual(target.read_bytes(), initial)
        self.assertTrue((work / 'merged.md').exists())

    def test_dry_run_never_calls_writer_or_requires_receipt(self):
        _, _, args = self.setup_merge()
        with patch.object(merge, 'ROOT', str(self.work)), patch.object(sys, 'argv', args + ['--dry-run']), patch.object(merge, 'verify', return_value=(True, True, 'audit PASS', 'mechanical PASS')), patch.object(merge, 'atomic_write') as writer:
            merge.main()
            writer.assert_not_called()

    def test_concurrent_source_change_blocks_writer(self):
        target, _, args = self.setup_merge()
        def review_and_change(*args):
            target.write_text(self.text + '\n并发修改。', encoding='utf-8')
            return True, 'test: simulate change after accepted review'
        with patch.object(merge, 'ROOT', str(self.work)), patch.object(sys, 'argv', args), patch.object(merge, 'verify', return_value=(True, True, 'audit PASS', 'mechanical PASS')), patch.object(merge, 'review_gate', side_effect=review_and_change), patch.object(merge, 'atomic_write') as writer:
            with self.assertRaises(SystemExit):
                merge.main()
            writer.assert_not_called()

    def test_reviewed_candidate_writes_exact_bytes_in_scratch(self):
        target, work, args = self.setup_merge()
        with patch.object(merge, 'ROOT', str(self.work)), patch.object(merge, 'verify', return_value=(True, True, 'audit PASS', 'mechanical PASS')):
            with patch.object(sys, 'argv', args + ['--dry-run']):
                merge.main()
            self.source, self.candidate = target, work / 'merged.md'
            self.note = 'course/notes/M01-test.md'
            path, data = self.receipt()
            data['review_file'] = '../review.md'
            (work / 'review.json').write_text(json.dumps(data), encoding='utf-8')
            with patch.object(sys, 'argv', args):
                merge.main()
        self.assertEqual(target.read_bytes(), self.candidate.read_bytes())


if __name__ == '__main__':
    unittest.main()
