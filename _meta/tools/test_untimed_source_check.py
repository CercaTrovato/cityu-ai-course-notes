import hashlib,json,tempfile,unittest,os
from pathlib import Path
from untimed_source_check import audit

class AuditTests(unittest.TestCase):
    def setUp(self):
        scratch=Path(os.environ.get('CITYU_TEST_SCRATCH','E:/app-data/codex/scratchpad/untimed-source-check-tests'))
        scratch.mkdir(parents=True,exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=str(scratch)); self.root=Path(self.tmp.name)
        self.source=self.root/'source.txt'; self.source.write_text('U1 p.01 L001: We have 20 students in this example.\nU1 p.02 L001: A different example uses 30 students.\n',encoding='utf-8')
        self.manifest=self.root/'source.json'; self.manifest.write_text(json.dumps({'schema':'untimed-source-v1','source_mode':'untimed','sources':[{'id':'U1','text':'source.txt','text_sha256':hashlib.sha256(self.source.read_bytes()).hexdigest(),'pages':2,'page_line_counts':{'1':1,'2':1}}]}),encoding='utf-8')
        self.note=self.root/'candidate.md'
    def tearDown(self): self.tmp.cleanup()
    def run_note(self,text):
        self.note.write_text(text,encoding='utf-8'); return audit(self.note,self.manifest)['passed']
    def test_valid(self): self.assertTrue(self.run_note('**🎙️ 课堂补充**\n\n*"We have 20 students in this example."*（`U1 p.01 L001`）'))
    def test_blockquote(self): self.assertTrue(self.run_note('> "We have 20 students in this example."（`U1 p.01 L001`）'))
    def test_changed_number(self): self.assertFalse(self.run_note('*"We have 21 students in this example."*（`U1 p.01 L001`）'))
    def test_bracket_number(self): self.assertFalse(self.run_note('*"We have [999] students in this example."*（`U1 p.01 L001`）'))
    def test_wrong_page(self): self.assertFalse(self.run_note('*"We have 20 students in this example."*（`U1 p.02 L001`）'))
    def test_missing_locator(self): self.assertFalse(self.run_note('*"We have 20 students in this example."*\n另见 `U1 p.01 L001`'))
    def test_source_hash(self):
        self.source.write_text(self.source.read_text()+'\n',encoding='utf-8'); self.assertFalse(self.run_note('`U1 p.01 L001`'))
    def test_unknown_source(self): self.assertFalse(self.run_note('`U2 p.01 L001`'))
    def test_cell_missing(self): self.assertFalse(self.run_note('`U1 p.01 L001`\n\n**🎙️ 课堂补充**\n\n没有定位。'))
    def test_claim_missing(self): self.assertFalse(self.run_note('`U1 p.01 L001`\n教授强调这是必须的。'))
    def test_scope_title_not_quote_locator(self): self.assertFalse(self.run_note('### 2.1 主题（U1 p.1–2）\n*"We have 20 students in this example."*'))
    def test_false_positive_scopes(self): self.assertTrue(self.run_note('### 2.1 主题（U1 p.1–2）\n`U1 p.01 L001`\n本节仅讨论转录提到的历史事件。\n不等于已确认“教授说必考”。'))
    def test_missing_original_tail_after_new_hash(self):
        meta=json.loads(self.manifest.read_text()); meta['sources'][0]['page_line_counts']['1']=2
        self.manifest.write_text(json.dumps(meta),encoding='utf-8')
        self.assertFalse(self.run_note('`U1 p.01 L001`'))
if __name__=='__main__': unittest.main()
