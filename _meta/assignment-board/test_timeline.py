import copy
from datetime import datetime
import unittest
import timeline

def fixture():
    def item(id,status='planned'):
        return {'id':id,'title':id,'status':status,'owner':'本人','owner_role':'me','scope':'team','summary':'任务说明','deliverable':'可核交件','next_action':'核对结果','my_next_action':None,'depends_on':[],'dependency_gates':[],'acceptance':[{'id':'one','label':'一项检查','status':'pass' if status=='done' else 'unknown'}],'target':{'value':None,'precision':'unknown','basis':'unknown'},'started_on':None,'completed_on':None,'observed_on':'2026-11-11','estimated_minutes':None,'state_basis':'真实记录','evidence':[{'label':'回执','url':None}],'history':[{'observed_on':'2026-11-11','status':status,'note':'已核'}]}
    return {'schema_version':1,'assignment_id':'IS6400-A06','course':'IS6400','timezone':'Asia/Shanghai','as_of':'2026-11-11','repository_url':'https://github.com/example/course','items':[item('upstream'),item('downstream')]}

NOW=datetime.fromisoformat('2026-11-11T12:00:00+08:00')
class TimelineTests(unittest.TestCase):
    def test_blocked_execution_not_ready(self):
        t=fixture();t['items'][1]['depends_on']=['upstream'];r=timeline.enrich(t,NOW);self.assertEqual(r['items'][1]['readiness'],'waiting_dependency')
    def test_partial_acceptance_gate_allows_parallel_work(self):
        t=fixture();t['items'][0]['acceptance'][0]['status']='pass';t['items'][1]['depends_on']=['upstream'];t['items'][1]['dependency_gates']=[{'task_id':'upstream','check_ids':['one']}];self.assertEqual(timeline.enrich(t,NOW)['items'][1]['readiness'],'ready')
    def test_completed_does_not_invent_date_or_effort(self):
        t=fixture();i=t['items'][0];i['status']='done';i['acceptance'][0]['status']='pass';r=timeline.enrich(t,NOW)['items'][0];self.assertIsNone(r['completed_on']);self.assertIsNone(r['estimated_minutes']);self.assertEqual(r['lane'],'past')
    def test_done_requires_evidence_and_accepted_checks(self):
        t=fixture();t['items'][0]['status']='done'
        with self.assertRaises(ValueError):timeline.validate(t)
        t['items'][0]['acceptance'][0]['status']='pass';t['items'][0]['evidence']=[]
        with self.assertRaises(ValueError):timeline.validate(t)
    def test_proposed_date_not_made_confirmed_or_failed(self):
        t=fixture();t['items'][0]['target']={'value':'2026-11-10','precision':'date','basis':'proposed'};r=timeline.enrich(t,NOW)['items'][0];self.assertEqual(r['status'],'planned');self.assertEqual(r['target']['basis'],'proposed');self.assertEqual(r['date_state'],'past_due_unverified');self.assertEqual(r['lane'],'current');self.assertEqual(r['readiness'],'verify')
    def test_timezone_and_before_date_boundary(self):
        t=fixture();t['items'][0]['target']={'value':'2026-11-11','precision':'before_date','basis':'official'};self.assertEqual(timeline.enrich(t,NOW)['items'][0]['date_state'],'past_due_unverified')
    def test_cycle_rejected(self):
        t=fixture();t['items'][0]['depends_on']=['downstream'];t['items'][1]['depends_on']=['upstream']
        with self.assertRaises(ValueError):timeline.validate(t)
    def test_stale_and_unknown_not_ready(self):
        t=fixture();t['items'][0]['status']='unknown';self.assertEqual(timeline.enrich(t,NOW)['items'][0]['readiness'],'verify');self.assertEqual(timeline.enrich(t,NOW,stale=True)['items'][1]['readiness'],'verify')
    def test_personal_export_excludes_teammate_work(self):
        t=fixture();t['items'][1]['owner_role']='member';p=timeline.daily_plan(t,NOW);self.assertEqual(len(p['actions']),1);self.assertTrue(p['scheduling_policy']['confirm_proposed_dates']);self.assertIsNone(p['actions'][0]['estimated_minutes'])

if __name__=='__main__':unittest.main()
