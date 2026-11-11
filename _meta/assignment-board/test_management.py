import copy,json,sys,unittest
sys.dont_write_bytecode=True
from pathlib import Path
from management import enrich,validate_project
from server import collect

class ManagementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records={r['id']:r for r in collect()['assignments']}
        cls.config=json.loads(Path(__file__).with_name('management.json').read_text(encoding='utf-8'))['projects']
    def test_all_five_current_views_and_metrics(self):
        for id,p in self.config.items():
            m=enrich(self.records[id],p)
            self.assertEqual(m['metrics']['checks'],m['metrics']['pass']+m['metrics']['gap']+m['metrics']['unknown'])
    def test_self_report_is_not_receipt_or_acceptance(self):
        fixture=copy.deepcopy(self.config['EF5560-A02'])
        unverified=next(n for n in fixture['deliverables'] if n['id']=='part2')
        unverified['receipt']='reported'
        for c in unverified['checks']: c.update(status='unknown',evidence=[])
        m=enrich(self.records['EF5560-A02'],fixture)
        part=next(n for n in m['deliverables'] if n['id']=='part2')
        self.assertEqual('reported',part['state']);self.assertFalse(part['accepted']);self.assertEqual(0,part['passed'])
    def test_partial_dependency_can_be_satisfied(self):
        fixture=copy.deepcopy(self.config['IS6400-A06'])
        stage=next(n for n in fixture['deliverables'] if n['id']=='clusters')
        next(c for c in stage['checks'] if c['id']=='code')['status']='unknown'
        m=enrich(self.records['IS6400-A06'],fixture)
        edges={(e['from'],e['to']):e for e in m['edges']}
        self.assertTrue(edges['clusters','feedback']['satisfied'])
        self.assertFalse(edges['clusters','delivery']['satisfied'])
    def test_parallel_work_is_not_blocked_by_unfinished_research(self):
        m=enrich(self.records['IS5542-A01'],self.config['IS5542-A01'])
        self.assertTrue(next(e for e in m['edges'] if e['from']=='rules' and e['to']=='core')['satisfied'])
        self.assertFalse(next(e for e in m['edges'] if e['from']=='rules' and e['to']=='acceptance')['satisfied'])
    def test_source_change_invalidates_manager_snapshot(self):
        r=copy.deepcopy(self.records['IS6400-A06']);r['revision']=self.config[r['id']]['basis_revision'];r['warnings']=[]
        r['coordination']['coordination_sha256']=self.config[r['id']].get('basis_coordination_revision')
        self.assertTrue(enrich(r,self.config[r['id']])['fresh'])
        r['revision']='changed'
        self.assertFalse(enrich(r,self.config[r['id']])['fresh'])
    def test_cycles_and_missing_evidence_rejected(self):
        p=copy.deepcopy(self.config['IS6400-A06']);sources={s['id'] for s in self.records['IS6400-A06']['sources']}
        p['edges'].append({'from':'delivery','to':'data','kind':'required','label':'错误循环','requires':[]})
        with self.assertRaises(ValueError):validate_project(p,sources)
        p=copy.deepcopy(self.config['IS6400-A06']);p['deliverables'][0]['checks'][0]['evidence']=[]
        with self.assertRaises(ValueError):validate_project(p,sources)

    def test_local_support_does_not_increase_team_progress(self):
        config=copy.deepcopy(self.config['IS6400-A06'])
        without=copy.deepcopy(config)
        without['deliverables']=[n for n in without['deliverables'] if n.get('scope')!='supporting']
        without['edges']=[e for e in without['edges'] if e['from']!='local-comparison' and e['to']!='local-comparison']
        baseline=enrich(self.records['IS6400-A06'],without)['metrics']
        actual=enrich(self.records['IS6400-A06'],config)['metrics']
        for key in ('received','total','pass','accepted','checks'):
            self.assertEqual(baseline[key],actual[key])
        self.assertEqual(1,actual['supporting'])

    def test_coordination_change_also_invalidates_snapshot(self):
        r=copy.deepcopy(self.records['IS6400-A06'])
        r['revision']=self.config[r['id']]['basis_revision'];r['warnings']=[]
        r['coordination']['coordination_sha256']=self.config[r['id']].get('basis_coordination_revision')
        self.assertTrue(enrich(r,self.config[r['id']])['fresh'])
        r['coordination']['coordination_sha256']='new-decision'
        self.assertFalse(enrich(r,self.config[r['id']])['fresh'])

if __name__=='__main__':unittest.main(verbosity=2)
