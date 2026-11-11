import unittest,json,hashlib,tempfile,sys
from pathlib import Path
sys.path.insert(0,'D:/上课资料/CityU/_meta/assignment-board')
import thinking
class Tests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix='test-',dir='E:/app-data/codex/scratchpad/thinking-board-20261110');self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  self.base=self.root/'IS6400_Test/assignment/graded/A06-group-project';self.base.mkdir(parents=True);(self.base/'assignment.json').write_text('{}',encoding='utf-8')
  self.source=self.base/'one.md';self.source.write_text('# 原文\n\n| 列 | 值 |\n|---|---|\n| A | 46 |\n\n[继续](two.md)\n<script>alert(1)</script><img src=x onerror=alert(1)>\n[恶意](javascript:alert(1))',encoding='utf-8');self.second=self.base/'two.md';self.second.write_text('# 第二份',encoding='utf-8')
  self.data={'schema_version':1,'assignment_id':'IS6400-A06','publication':'local_review','assignment_revision':thinking.digest(self.base/'assignment.json'),'sources':[{'id':'one','title':'原文','path':str(self.source),'sha256':thinking.digest(self.source)},{'id':'two','title':'第二份','path':str(self.second),'sha256':thinking.digest(self.second)}],'nodes':[dict(id='start',stage=0,status='team',evidence=['one'],**{k:'具体解释' for k in ['title','summary','question','choice','result','meaning','next','owner','date']})],'edges':[]};self.write()
 def write(self): (self.base/'thinking.json').write_text(json.dumps(self.data,ensure_ascii=False),encoding='utf-8')
 def test_source_html_has_tables_and_safe_inline_links(self):
  result=thinking.source_content(self.root,'IS6400-A06','one')['html'];self.assertIn('<table>',result);self.assertIn('data-thinking-source="two"',result)
  for bad in ['<script','<img','onerror','javascript:']:self.assertNotIn(bad,result)
 def test_source_drift_and_progress_drift_remain_visible(self):
  self.source.write_text('来源新增结果',encoding='utf-8');(self.base/'assignment.json').write_text('{"new":1}',encoding='utf-8');d=thinking.load(self.root,'IS6400-A06');self.assertEqual(2,len(d['warnings']));self.assertTrue(d['sources'][0]['changed'])
 def test_other_courses_and_arbitrary_paths_are_not_served(self):
  other=self.root/'IS5542_Test';other.mkdir();p=other/'private.md';p.write_text('不共享',encoding='utf-8');self.data['sources'][0]['path']=str(p);self.write();self.assertFalse(thinking.load(self.root,'IS6400-A06')['sources'][0]['available']);self.assertRaises(ValueError,thinking.source_content,self.root,'IS6400-A06','one');self.assertRaises(ValueError,thinking.location,self.root,'../private')
 def test_bad_graph_cannot_claim_a_valid_story(self):
  self.data['edges']=[{'from':'start','to':'missing'}];self.write();self.assertRaises(ValueError,thinking.load,self.root,'IS6400-A06')
 def test_all_five_real_courses_have_distinct_content(self):
  root=Path('D:/上课资料/CityU');ids=['AC6761-A01','IS6400-A06','IS5113-A02','IS5542-A01','EF5560-A02'];loaded=[thinking.load(root,id) for id in ids];self.assertTrue(all(len(d['nodes'])>=1 for d in loaded));self.assertEqual(5,len({d['intro'] for d in loaded}));self.assertTrue(all(d['publication']=='local_review' for d in loaded));self.assertTrue(all(s['available'] for d in loaded for s in d['sources']))
 def test_original_is_preserved_in_full_and_metrics_include_all_seeds(self):
  root=Path('D:/上课资料/CityU');d=thinking.source_content(root,'IS6400-A06','original');self.assertGreaterEqual(d['html'].count('<table>'),5);self.assertIn('原始订单',d['html']);self.assertIn('前 10%',d['html']);self.assertGreaterEqual(len(thinking.source_content(root,'IS6400-A06','metrics')['rows']),10)
if __name__=='__main__':unittest.main(verbosity=2)
