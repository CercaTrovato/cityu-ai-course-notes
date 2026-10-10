import runpy
import sys
import unittest
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
q = runpy.run_path(str(ROOT / '_meta/tools/note_quality.py'))

def check(body, course='EF5560'):
    return q['readability_checks']('---\ncourse: '+course+'\n---\n\n## 2. 正文\n\n### 2.1 示例（讲义 p.1）\n\n'+body)

def codes(result, level='warn'):
    return [item[0] for item in result[level]]

class Regression(unittest.TestCase):
    def test_preceding_plain_explanation(self):
        r=check('有限数据估计的平均值有多不准（标准误）。')
        self.assertNotIn('R6d', codes(r))

    def test_explain_then_name(self):
        r=check('先把每周的数相加，再除以周数。这叫平均值。')
        self.assertNotIn('R6d', codes(r))

    def test_missing_term_is_review_not_hard(self):
        r=check('我们报告标准误。')
        self.assertIn('R6d', codes(r))
        self.assertNotIn('R6d', codes(r,'hard'))

    def test_title_is_not_explanation(self):
        r=check('### 2.2 标准误（讲义 p.2）\n\n我们报告标准误。')
        self.assertIn('R6d', codes(r))

    def test_missing_t_first_column(self):
        r=check('一行是一种结果。\n\n| $t$ | 模型 |\n|---|---|\n| 1.03 | OLS |')
        self.assertIn('R4f',codes(r))
        self.assertNotIn('R4f',codes(r,'hard'))

    def test_code_cannot_explain_table(self):
        r=check('一行是一种结果。\n\n| 模型 | $t$ |\n|---|---|\n| OLS | 1.03 |\n\n```text\nt：统计量。t=1/1=1。t 低于 2。\n```')
        self.assertIn('R4f',codes(r))

    def test_misconception_without_emoji(self):
        r=check('**常见误解**\n\n把借方当成一律增加是错的，因为增减取决于账户类型。','AC6761')
        self.assertNotIn('R8c',codes(r,'hard'))

    def test_soft_wrap_does_not_hide_long_sentence(self):
        r=check('甲'*61+'\n'+'乙'*61+'。')
        self.assertIn('R1a',codes(r,'hard'))

    def test_sentence_boundary(self):
        self.assertNotIn('R1a',codes(check('甲'*119+'。'),'hard'))
        self.assertIn('R1a',codes(check('甲'*120+'。'),'hard'))

    def test_table_cell_and_escaped_pipe(self):
        r=check('一行一个对象。\n\n| 对象 | 说明 |\n|---|---|\n| A | '+ '甲'*81 +' |')
        self.assertEqual(r['stats']['table_max_cell_units'],81)
        self.assertIn('R4b',codes(r,'hard'))
        self.assertEqual(len(q['r_cells']('| A | [[a\\|说明]] |')),2)

    def test_log_details_multiline(self):
        r=check('<details>\n<summary>复算与来源</summary>\n\n'+'甲'*160+'。\n\n</details>\n\n正文。')
        self.assertNotIn('R1a',codes(r,'hard'))

    def test_teaching_details_still_checked(self):
        r=check('<details><summary>答案</summary>\n\n'+'甲'*160+'。\n\n</details>')
        self.assertIn('R1a',codes(r,'hard'))

    def test_t_role_preserved(self):
        self.assertEqual(q['r_norm_head']('$t(\\alpha)$'), 't(alpha)')

    def test_exemption_cap(self):
        r=check(('<!-- 可读性豁免: 原文忠实转录 -->\n\n甲乙丙。\n\n')*6)
        self.assertIn('R0',codes(r,'hard'))

    def test_all_courses_have_term_hints(self):
        for c in q['R_COURSES']:
            self.assertGreaterEqual(len(q['r_risk_terms'](c)),5,c)

    def test_cell_sentence_terminal_punctuation_counts(self):
        cases = [('怎么算？',1), ('怎么算？怎么读？',2),
                 ('怎么算？怎么读？何时用？',3), ('算完！',1),
                 ('怎么算？！怎么读？！',2), ('甲。乙。',2),
                 ('甲；乙；丙；',3), ('$x=1$',1), ('',0)]
        for cell, expected in cases:
            with self.subTest(cell=cell):
                self.assertEqual(q['r_cell_sentence_count'](cell), expected)

    def test_two_questions_not_hard_three_still_hard(self):
        def table(cell):
            return check('一行是一个检查对象。\n\n| 对象 | 问题 |\n|---|---|\n| A | '+cell+' |')
        self.assertNotIn('R4c',codes(table('怎么算？'),'warn'))
        self.assertNotIn('R4c',codes(table('怎么算？怎么读？'),'hard'))
        self.assertIn('R4c',codes(table('怎么算？怎么读？何时用？'),'hard'))
        self.assertIn('R4c',codes(table('甲。乙。丙。'),'hard'))
        self.assertIn('R4c',codes(table('甲；乙；丙；'),'hard'))
        self.assertNotIn('R4c',codes(table('$x=1$'),'hard'))

if __name__ == '__main__':
    unittest.main()
