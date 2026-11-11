import copy
import json
import tempfile
import unittest
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime
import server
from update import apply_candidate

SCRATCH=Path('E:/app-data/codex/scratchpad/cityu-action-board-20261107')

class BoardTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='test-',dir=SCRATCH)
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        original=next(server.ROOT.glob('AC*/assignment/graded/*/assignment.json'))
        self.folder=self.root/original.parent.relative_to(server.ROOT)
        self.folder.mkdir(parents=True)
        self.file=self.folder/'assignment.json'
        self.record=json.loads(original.read_text(encoding='utf-8'))
        self.record['sources']=[{**s,'kind':'thread','locator':'fixture-source','sha256':None} if s['kind'] in ('local','external_file') else s for s in self.record['sources']]
        self.record['submission']={'status':'unknown','note':'test fixture','evidence':[]}
        self.record['tasks'][0]['evidence']=['progress-chat']
        self.write(self.record)

    def write(self, data):
        self.file.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')

    def test_real_metadata_valid_and_complete_inventory(self):
        result=server.collect()
        self.assertFalse(result['errors'])
        self.assertFalse(result['missing'])
        self.assertEqual(5,len([r for r in result['assignments'] if r['board_scope']=='active']))

    def test_unknown_work_does_not_get_percentage(self):
        r=server.collect(self.root)['assignments'][0]
        self.assertIsNone(r['completion_percent'])
        self.assertEqual('unknown',r['submission']['status'])

    def test_completion_and_submission_need_evidence(self):
        r=copy.deepcopy(self.record)
        r['tasks'][0]['evidence']=[]
        r['submission']['status']='submitted'
        self.assertEqual(2,len(server.validate(r)))

    def test_invalid_reference_and_duplicate_ids(self):
        r=copy.deepcopy(self.record)
        r['tasks'][0]['evidence']=['invented-source']
        r['tasks'][1]['id']=r['tasks'][0]['id']
        self.assertEqual(2,len(server.validate(r)))

    def test_deadline_precision_and_timezone(self):
        m={'due':'2026-11-11','precision':'before_date','status':'unknown'}
        self.assertIn('截止边界',server.due_state(m,datetime.fromisoformat('2026-11-11T00:00:00+08:00')))
        m={'due':'2026-11-15T23:59:00+08:00','precision':'datetime','status':'unknown'}
        self.assertIn('72 小时',server.due_state(m,datetime.fromisoformat('2026-11-15T15:58:00+00:00')))
        self.assertIn('已到期',server.due_state(m,datetime.fromisoformat('2026-11-15T16:00:00+00:00')))
        r=copy.deepcopy(self.record)
        r['milestones'][0].update(due='2026-11-11T12:00:00',precision='datetime')
        self.assertTrue(server.validate(r))

    def test_live_read_detects_changes_without_restart(self):
        self.assertNotEqual('新核实的进展',server.collect(self.root)['assignments'][0]['summary'])
        self.record['summary']='新核实的进展'
        self.write(self.record)
        self.assertEqual('新核实的进展',server.collect(self.root)['assignments'][0]['summary'])

    def test_corrupt_and_missing_metadata_are_visible(self):
        self.file.write_text('{',encoding='utf-8')
        data=server.collect(self.root)
        self.assertEqual(1,len(data['errors']))
        self.assertEqual([],data['assignments'])
        self.file.unlink()
        self.assertEqual(1,len(server.collect(self.root)['missing']))

    def test_source_drift_warning(self):
        source=self.root/'proof.md'
        source.write_text('old',encoding='utf-8')
        self.record['sources'].append({'id':'local-proof','kind':'local','label':'证据','locator':'proof.md','sha256':server.digest(source),'observed_at':'2026-11-07'})
        self.write(self.record)
        source.write_text('changed',encoding='utf-8')
        self.assertTrue(any('依据已变更' in w for w in server.collect(self.root)['assignments'][0]['warnings']))

    def test_update_rejects_stale_revision_and_preserves_history(self):
        old=self.file.read_bytes()
        sha=server.digest(self.file)
        candidate=self.root/'candidate.json'
        self.record['stage']='已核新的阶段'
        candidate.write_text(json.dumps(self.record,ensure_ascii=False),encoding='utf-8')
        with self.assertRaises(ValueError):
            apply_candidate(self.file,candidate,'0'*64)
        self.assertEqual(old,self.file.read_bytes())
        result=apply_candidate(self.file,candidate,sha)
        self.assertTrue(result['written'])
        self.assertEqual(json.loads(old),json.loads(Path(result['previous_revision']).read_text(encoding='utf-8')))
        self.assertEqual('已核新的阶段',json.loads(self.file.read_text(encoding='utf-8'))['stage'])

    def coordination(self):
        return {'schema_version': 1, 'assignment_id': self.record['id'],
                'thread_id': '01a1b4b5-28d9-7ab3-8933-36583e623c7f',
                'root_thread_id': '01a1b491-403e-7651-9aba-13e5b647af93',
                'model': 'gpt-6.1-sol', 'status': 'working', 'updated_at': '2026-11-07T14:35:00+08:00',
                'summary': '正在核对', 'report_path': (self.folder.relative_to(self.root) / 'notes/supervision-report.md').as_posix(),
                'decisions': []}

    def write_coordination(self, c):
        (self.folder / 'coordination.json').write_text(json.dumps(c), encoding='utf-8')

    def test_coordination_error_preserves_assignment(self):
        (self.folder / 'coordination.json').write_text('{', encoding='utf-8')
        data = server.collect(self.root)
        self.assertEqual(1, len(data['assignments']))
        self.assertEqual(1, len(data['errors']))

    def test_decision_requires_human_evidence(self):
        c = self.coordination()
        c['decisions'] = [{'id': 'D01', 'question': '选择方向', 'recommendation': '方案 A', 'options': ['A', 'B'],
                           'status': 'decided', 'answer': 'A', 'answer_source': None}]
        self.write_coordination(c)
        self.assertIn('本人答复', server.collect(self.root)['errors'][0]['message'])

    def test_report_path_cannot_escape_assignment(self):
        c = self.coordination()
        c['report_path'] = '../private.md'
        self.write_coordination(c)
        self.assertIn('本作业目录', server.collect(self.root)['errors'][0]['message'])

    def test_ready_phase_requires_report(self):
        c = self.coordination()
        c['status'] = 'ready_for_review'
        self.write_coordination(c)
        self.assertIn('缺少报告', server.collect(self.root)['errors'][0]['message'])

    def test_supervisor_review_invalidated_by_new_metadata(self):
        c = self.coordination()
        self.write_coordination(c)
        first = server.collect(self.root)['assignments'][0]
        review = {'metadata_sha256': first['revision'],
                  'coordination_sha256': first['coordination']['coordination_sha256'],
                  'report_sha256': None, 'reviewed_at': '2026-11-07T14:36:00+08:00', 'note': '核过当前阶段'}
        config = self.root / '_meta/assignment-board'
        config.mkdir(parents=True)
        (config / 'supervisor-reviews.json').write_text(json.dumps({'assignments': {self.record['id']: review}}), encoding='utf-8')
        self.assertIn('已核对', server.collect(self.root)['assignments'][0]['coordination']['review_status'])
        self.record['summary'] = '新一轮工作'
        self.write(self.record)
        self.assertIn('待监督核对', server.collect(self.root)['assignments'][0]['coordination']['review_status'])

if __name__=='__main__':
    unittest.main(verbosity=2)
