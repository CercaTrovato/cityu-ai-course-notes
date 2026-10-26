"""现行规则回归：不奖励固定标签/篇幅，也不能漏掉确定性缺口。"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import note_quality as q
import note_release_gate as gate

SCRATCH = Path('E:/app-data/codex/scratchpad/note-quality-current-tests')
FENCE = chr(96)*3


def note(body, heading='2.1 预测（讲义 p.1）'):
    return '---\ncourse: IS6400\n---\n\n## 2. 正文\n\n### '+heading+'\n\n'+body+'\n\n## 3. 一图看懂\n\n本讲无新增图。\n'


def codes(result):
    return [x['code'] for x in result['hard']]


class CurrentChecks(unittest.TestCase):
    def test_empty_body_does_not_pass_after_removing_quota(self):
        text='---\ncourse: IS6400\n---\n\n## 2. 正文\n\n## 3. 一图看懂\n'
        self.assertIn('C_STRUCTURE',codes(q.assess_current(text,'M01.md')))

    def test_practice_document_does_not_require_subheadings_in_section2(self):
        text = ('---\ntype: 课堂练习解析\n---\n\n'
                '## 1. 任务\n\n先把本题每笔交易留下的资源与欠款分开。\n\n'
                '## 2. 英文条件\n\non account要先辨认谁欠谁，再选择应收或应付账户。\n\n'
                '## 3. 实际步骤\n\n从本次业务动作判断账户增减，再转为借贷并保留交易号。\n')
        self.assertNotIn('C_STRUCTURE', codes(q.assess_current(text, 'case2.md')))

    def test_practice_document_still_checks_later_naked_code_and_empty_units(self):
        text = ('---\ntype: 课堂练习解析\n---\n\n'
                '## 2. 条件\n\n先分清公司购买和公司提供服务这两个方向。\n\n'
                '## 3. 运行\n\n' + FENCE + 'python\nprint(1)\n' + FENCE + '\n')
        self.assertIn('C_CODE_EXPLANATION', codes(q.assess_current(text, 'case2.md')))
        empty = '---\ntype: 课堂练习解析\n---\n\n## 2. 条件\n\n## 3. 步骤\n'
        self.assertTrue(q.assess_current(empty, 'case2.md')['hard'])

    def test_standalone_guide_scans_real_steps_after_section2(self):
        prefix = '---\ntype: practice-guide\n---\n\n'
        explained = (prefix + '## 2. 题面条件\n\n'
                     '| 条件 | 含义 |\n|---|---|\n| 分次付款 | 一次销售可对应多次收款 |\n\n'
                     '## 3. 六步做题\n\n### Step 1：拆开两种事件\n\n'
                     '先将交付资源的销售与收到现金的收款分开。已售出并不表示已经到账。\n')
        self.assertNotIn('C_STRUCTURE', codes(q.assess_current(explained, 'case5.md')))
        later_code = explained + '\n## 8. 运行\n\n' + FENCE + 'python\nprint(1)\n' + FENCE + '\n'
        self.assertIn('C_CODE_EXPLANATION', codes(q.assess_current(later_code, 'case5.md')))
        empty = prefix + '## 2. 条件\n\n## 3. 步骤\n'
        self.assertTrue(q.assess_current(empty, 'case5.md')['hard'])

    def test_assignment_guide_scope_and_primary_module_guard(self):
        prefix = '---\ncourse: AC6761\nassignment: A01-project\n---\n\n'
        body = ('## 2. 教师原文\n\nPrepare a report.\n\n'
                '## 3. 准备动作\n\n先按同一年度收集两家公司报表，记录单位和集团范围，避免把母公司与集团混用。\n')
        self.assertNotIn('C_STRUCTURE', codes(q.assess_current(prefix+body, 'guide.md')))
        naked = prefix+body+'\n## 4. 运行\n\n'+FENCE+'python\nprint(1)\n'+FENCE+'\n'
        self.assertIn('C_CODE_EXPLANATION', codes(q.assess_current(naked, 'guide.md')))
        self.assertTrue(q.assess_current(prefix+'## 2. 条件\n\n## 3. 步骤\n', 'guide.md')['hard'])
        primary = prefix.replace('assignment:', 'module: M01\nassignment:')
        self.assertIn('C_STRUCTURE', codes(q.assess_current(primary+body, 'M01.md')))

    def test_unlabelled_short_but_explained_does_not_fail_quota(self):
        text = note('窗口均值用来平滑短期变化。\n\n先求过去三期的平均：$M=(2+4+6)/3=4$。\n\n若窗口包含未来销量，就会泄漏待预测的答案。')
        self.assertFalse(q.assess_current(text, 'M01.md')['hard'])
        old = q.evaluate_M(text, 'M01.md', 1, True)
        self.assertTrue(any(value[1] is False for value in old['G'].values()))

    def test_label_only_placeholder_is_not_explanation(self):
        r = q.assess_current(note('**是什么**\n\n待补。\n\n**为什么需要它**\n\nTODO'), 'M01.md')
        self.assertIn('C_EXPLANATION', codes(r))

    def test_quotation_alone_is_not_explanation(self):
        self.assertIn('C_EXPLANATION', codes(q.assess_current(note('> A forecast uses past observations.'), 'M01.md')))

    def test_actual_calculation_needs_substitution_not_only_result(self):
        body = '这个模型把过去几期的数求平均。\n\n$$M=\\frac{1}{n}\\sum_i y_i$$\n\n最终结果为4。'
        self.assertIn('C_CALCULATION_STEPS', codes(q.assess_current(note(body), 'M01.md')))
        repaired = body + '\n\n代入三期：$(2+4+6)/3=4$。'
        self.assertNotIn('C_CALCULATION_STEPS', codes(q.assess_current(note(repaired), 'M01.md')))

    def test_code_narrative_and_tables_need_no_bold_labels(self):
        body = '读取历史值以便求平均。\n\n'+FENCE+'python\nx = [2, 4, 6]\ny = sum(x)/len(x)\n'+FENCE+'\n\n| 行 | 动作 | 输出 |\n|---|---|---|\n| 1 | 保存三期观测 | 长度3 |\n| 2 | 总和除以数量 | 4 |\n'
        self.assertNotIn('C_CODE_EXPLANATION', codes(q.assess_current(note(body), 'T01.md', tut=True)))

    def test_naked_program_still_blocks(self):
        body = FENCE+'python\nx = model.fit(y)\n'+FENCE
        self.assertIn('C_CODE_EXPLANATION', codes(q.assess_current(note(body), 'M01.md')))

    def test_mermaid_is_not_a_program_requiring_line_by_line_output(self):
        body = '箭头表示收到观测后先更新状态，再输出预测。\n\n'+FENCE+'mermaid\nflowchart TD\n A --> B\n'+FENCE
        self.assertNotIn('C_CODE_EXPLANATION', codes(q.assess_current(note(body), 'M01.md')))

    def test_child_worked_example_is_shared_with_parent(self):
        text = note('模型先求均值。\n\n$$M=\\frac{1}{n}\\sum y_i$$\n\n#### 2.1.1 完整代入\n\n代入得 $(2+4+6)/3=4$。')
        self.assertNotIn('C_CALCULATION_STEPS', codes(q.assess_current(text, 'M01.md')))

    def test_example_elsewhere_keeps_specific_gap_as_review(self):
        text=note('均值模型先合并过去观测。\n\n$$M=\\frac{1}{n}\\sum y_i$$\n\n### 2.2 另一机制（讲义 p.2）\n\n另一个模型代入 $(2+4)/2=3$。')
        result=q.assess_current(text,'M01.md')
        self.assertNotIn('C_CALCULATION_STEPS',codes(result))
        self.assertIn('C_CALCULATION_STEPS',[x['code'] for x in result['warn']])

    def test_a_suffix_is_not_truncated_in_sections_or_term_cards(self):
        text = note('先求均值。', '2.4.1a 计算')+'\n## 5. 双语术语卡\n\n| 中文 | English | 定义 | 首现 |\n|---|---|---|---|\n| 均值 | Mean | Average | §2.4.1a |\n\n## 6. 考点\n'
        self.assertEqual(q.section_metrics(['#### 2.4.1a 计算', '解释。'])['num'], '2.4.1a')
        self.assertEqual(q.terms_sec5(text)[0][-1], '2.4.1a')

    def test_code_language_boundary_is_regex_not_backspace(self):
        lines=['### 2.1 计算',FENCE+'python','x = 1',FENCE]
        self.assertEqual(q.section_metrics(lines)['code_bad'],1)

    def test_wrong_numeric_equation_blocks(self):
        self.assertIn('C_ARITHMETIC', codes(q.assess_current(note('先相加：$2+3=6$。'), 'M01.md')))

    def test_rounding_implicit_multiply_fraction_and_root(self):
        text = note('代入计算：$10/3=3.33$，$0.5(10+2)=6$，$\\frac{2+3}{5}=1$，$\\sqrt{9}=3$。')
        self.assertNotIn('C_ARITHMETIC', codes(q.assess_current(text, 'M01.md')))

    def test_variables_percent_code_and_wrong_examples_are_not_guessed(self):
        text = note('假设 $a+2=100$；百分数为 $20\\%=0.2$。\n\n错误示范：$2+3=6$。\n\n'+FENCE+'python\nprint("2+3=6")\n'+FENCE+'\n\n输出用于说明错误示范。')
        self.assertNotIn('C_ARITHMETIC', codes(q.assess_current(text, 'M01.md')))

    def test_numeric_parser_does_not_execute_python(self):
        for expr in ['__import__("os").system("echo bad")', '2**100000000', '(1).__class__', '[1][0]']:
            with self.subTest(expr=expr), self.assertRaises((ValueError, SyntaxError)):
                q.safe_number(expr)

    def test_page_reference_gap_blocks_but_explicit_cover_is_excluded(self):
        text = note('第2页讲输入，第3页讲输出（讲义 p.2–3）。', '2.1 过程（讲义 p.2–3）')
        self.assertIn('C_PAGE_REFERENCES', codes(q.assess_current(text, 'M01.md', 3)))
        text += '\n## 8. 讲义页码映射\n\n| 笔记 | 物理页 | 内容 |\n|---|---|---|\n| —（封面） | p.1 | 封面 |\n\n## 9. 延伸\n'
        self.assertNotIn('C_PAGE_REFERENCES', codes(q.assess_current(text, 'M01.md', 3)))

    def test_no_contract_explicitly_leaves_source_coverage_unverified(self):
        r = q.assess_current(note('先按输入计算。'), 'M01.md')
        self.assertEqual(r['source_coverage']['status'], 'unverified_without_manifest')

    def test_multi_version_total_is_review_not_fabricated_missing_pages(self):
        text=note('先说明输入，再计算输出。').replace('course: IS6400','course: IS6400\nsource: 旧版50页 + 新版79页')
        result=q.assess_current(text,'M01.md',79)
        self.assertNotIn('C_PAGE_REFERENCES',codes(result))
        self.assertIn('C_PAGE_VERSION',[x['code'] for x in result['warn']])


class SourceContract(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        assert self.work.resolve().is_relative_to(SCRATCH.resolve())
        source = self.work/'source.txt';source.write_text('teacher version 1', encoding='utf-8')
        self.original = 'Which forecast is valid?\nA) Uses past data.\nB) Uses future data.\nC) Changes the test.\nD) Drops all data.'
        self.answers = '\n中文逐问：第一问只用过去数据。第二问要保持测试边界。\nEnglish answers: Use only past data. Keep the test untouched.'
        self.body = note('\n'.join('> '+l for l in self.original.splitlines())+self.answers, '2.1a 原题')
        self.contract = dict(schema='note-source-checks-v1',
            sources={'lecture':dict(path='source.txt', sha256=hashlib.sha256(source.read_bytes()).hexdigest())},
            questions=[dict(id='q1',source_id='lecture',section='2.1a',original=self.original,
               options={l[0]:l[3:] for l in self.original.splitlines()[1:]},
               answers=[dict(id='1',chinese='第一问只用过去数据。',english='Use only past data.'),
                        dict(id='2',chinese='第二问要保持测试边界。',english='Keep the test untouched.')])])
        self.manifest = self.work/'questions.json'

    def check(self, body=None):
        self.manifest.write_text(json.dumps(self.contract,ensure_ascii=False),encoding='utf-8')
        return q.assess_current(body or self.body, 'M01.md', source_checks=self.manifest)

    def test_complete_declared_contract_passes_its_limited_scope(self):
        r=self.check()
        self.assertFalse(r['hard'])
        self.assertEqual(r['source_coverage']['status'],'manifest_contract_passed')
        self.assertEqual(r['source_coverage']['checked_questions'],1)

    def test_truncated_last_option_and_whole_question_do_not_pass(self):
        for body in [self.body.replace('> D) Drops all data.',''),self.body.replace('Which forecast is valid?','题号见讲义')]:
            with self.subTest(body=body):
                self.assertIn('C_SOURCE_CONTRACT',codes(self.check(body)))

    def test_original_hidden_inside_program_does_not_pass(self):
        body=note(FENCE+'python\n'+self.original+'\n'+FENCE+self.answers,'2.1a 原题')
        self.assertIn('C_SOURCE_CONTRACT',codes(self.check(body)))

    def test_each_subquestion_needs_chinese_and_english(self):
        for text in ['第二问要保持测试边界。','Use only past data.']:
            self.assertIn('C_SOURCE_CONTRACT',codes(self.check(self.body.replace(text,''))))

    def test_changed_source_hash_wrong_section_and_duplicate_question_fail(self):
        original=json.loads(json.dumps(self.contract))
        self.contract['sources']['lecture']['sha256']='0'*64
        self.assertIn('C_SOURCE_CONTRACT',codes(self.check()))
        self.contract=json.loads(json.dumps(original))
        self.contract['questions'][0]['section']='2.1'
        self.assertIn('C_SOURCE_CONTRACT',codes(self.check()))
        self.contract=json.loads(json.dumps(original))
        self.contract['questions']*=2
        self.assertIn('C_SOURCE_CONTRACT',codes(self.check()))

    def test_short_original_cannot_claim_full_options_verified(self):
        self.contract['questions'][0]['original']='Which forecast is valid?'
        self.assertIn('C_SOURCE_CONTRACT',codes(self.check()))

    def test_significant_word_and_operator_changes_are_not_normalized_away(self):
        for body in [self.body.replace('Uses past data.','Uses NOT past data.'),self.body.replace('Keep the test untouched.','Keep the test un touched.')]:
            self.assertIn('C_SOURCE_CONTRACT',codes(self.check(body)))

    def test_labels_are_not_answer_evidence(self):
        self.contract['questions'][0]['answers'][0]['chinese']='中文解析'
        self.assertIn('C_SOURCE_CONTRACT',codes(self.check()))

    def test_bad_manifest_is_a_blocker_not_an_ignored_optional_check(self):
        self.manifest.write_text('not-json',encoding='utf-8')
        r=q.assess_current(self.body,'M01.md',source_checks=self.manifest)
        self.assertIn('C_SOURCE_CONTRACT',codes(r))


class ReleaseConsumer(unittest.TestCase):
    def test_explicit_source_contract_is_forwarded(self):
        SCRATCH.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            source=Path(temp)/'before.md';candidate=Path(temp)/'candidate.md'
            source.write_text('---\nreadability_rules: v2\n---\n',encoding='utf-8')
            candidate.write_bytes(source.read_bytes())
            manifest=Path(temp)/'questions.json'
            data=dict(profile='current',legacy_problems=[],R=dict(hard=[]),C=dict(hard=[]))
            result=SimpleNamespace(returncode=0,stdout='JSON:'+json.dumps(data),stderr='')
            with patch.object(gate.subprocess,'run',return_value=result) as run:
                self.assertTrue(gate.quality_gate(candidate,'M01.md',source,source_checks=manifest)[0])
                self.assertIn('--source-checks',run.call_args.args[0])
                self.assertIn(str(manifest.resolve()),run.call_args.args[0])

    def test_current_content_blocker_cannot_hide_behind_clean_l_and_r(self):
        SCRATCH.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            assert Path(temp).resolve().is_relative_to(SCRATCH.resolve())
            source=Path(temp)/'before.md';candidate=Path(temp)/'candidate.md'
            source.write_text('---\nreadability_rules: v2\n---\n',encoding='utf-8')
            candidate.write_bytes(source.read_bytes())
            data=dict(profile='current',legacy_problems=[],R=dict(hard=[]),C=dict(hard=[dict(code='C_ARITHMETIC')]))
            result=SimpleNamespace(returncode=1,stdout='JSON:'+json.dumps(data),stderr='')
            with patch.object(gate.subprocess,'run',return_value=result):
                self.assertFalse(gate.quality_gate(candidate,'M01.md',source)[0])
            data.pop('C')
            with patch.object(gate.subprocess,'run',return_value=SimpleNamespace(returncode=0,stdout='JSON:'+json.dumps(data),stderr='')):
                self.assertFalse(gate.quality_gate(candidate,'M01.md',source)[0])


class StandaloneCLI(unittest.TestCase):
    def run_cli(self, text, *extra):
        import contextlib, io, sys
        SCRATCH.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            path = Path(temp) / 'guide.md'
            path.write_text(text, encoding='utf-8')
            output = io.StringIO()
            with patch.object(sys, 'argv', ['note_quality.py', str(path), '--json', *extra]), contextlib.redirect_stdout(output):
                result = q.main()
            return result, output.getvalue()

    def test_question_headings_work_but_later_bare_code_still_fails(self):
        text = '---\nassignment: mock\nreadability_rules: v2\n---\n## Q1\n客户支付旧欠款，只把应收换为现金，因此不再确认收入。\n'
        code, out = self.run_cli(text)
        self.assertEqual(code, 0)
        payload = json.loads(out.split('JSON:')[1])
        self.assertEqual(payload['historical']['verdict'], 'not_applicable_without_module_section2')
        code, out = self.run_cli(text + '\n## Q9\n' + FENCE + 'python\nprint(1)\n' + FENCE)
        self.assertEqual(code, 1)
        self.assertIn('C_CODE_EXPLANATION', out)

    def test_empty_standalone_and_primary_module_cannot_get_pass(self):
        self.assertEqual(self.run_cli('---\nassignment: mock\n---\n')[0], 1)
        self.assertEqual(self.run_cli('---\nassignment: mock\nmodule: M01\n---\n## Q1\n解释\n')[0], 2)
        self.assertEqual(self.run_cli('---\nassignment: mock\n---\n## Q1\n解释\n', '--profile', 'historical')[0], 2)


if __name__=='__main__':
    unittest.main()
