"""Evidence assembly only. Writes exclusively inside this new scratch directory."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import hashlib
import json
import re
import importlib.metadata

HERE = Path(__file__).resolve().parent
VAULT = Path('D:/上课资料/CityU')
SOURCE = VAULT/'IS6400_Business_Data_Analytics/course_files_export/canvas-20261118/Sample Final.docx'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


with ZipFile(SOURCE) as z:
    doc = ET.fromstring(z.read('word/document.xml'))
    paragraphs = []
    for p in doc.findall('.//w:p', NS):
        text = ''.join(n.text or '' for n in p.iter()
                       if n.tag in (f"{{{NS['w']}}}t", f"{{{NS['m']}}}t"))
        if text.strip():
            paragraphs.append(text)
    (HERE/'source-xml-text.txt').write_text('\n'.join(paragraphs)+'\n', encoding='utf-8')
    media = []
    for name in z.namelist():
        if name.startswith('word/media/'):
            blob = z.read(name)
            local = HERE.parent/'media/media'/Path(name).name
            assert local.read_bytes() == blob, f'Extracted asset differs: {name}'
            media.append({'docx_member': name, 'extracted_file': str(local),
                          'sha256': hashlib.sha256(blob).hexdigest(),
                          'bytes': len(blob), 'actual_visual_read': True})
    embeddings = [name for name in z.namelist() if name.startswith('word/embeddings/')]

# Independent traversal through an explicit source-image tree, not prediction if/else.
# Each internal tuple is (feature index, zero branch, one branch).
original = (0, (1, (2, (3, '+', '-'), '-'), '-'), (1, '+', '-'))
train = [(0,0,0,0,4,0), (0,0,0,1,0,1), (0,0,1,0,0,1),
         (0,1,0,1,0,1), (1,0,1,0,3,0), (1,1,0,1,0,5)]
valid = [(0,0,0,1,4,0), (0,0,1,1,3,0), (0,1,0,0,0,1),
         (0,1,1,0,0,2), (1,0,0,0,2,0), (1,0,0,1,3,0)]


def all_prunings(tree, rows):
    if isinstance(tree, str):
        return [tree]
    feature, zero, one = tree
    zeros = [row for row in rows if row[feature] == 0]
    ones = [row for row in rows if row[feature] == 1]
    positive = sum(row[4] for row in rows)
    negative = sum(row[5] for row in rows)
    assert positive != negative  # no unspecified tie rule needed for this source
    majority = '+' if positive > negative else '-'
    return [(feature, left, right) for left in all_prunings(zero, zeros)
            for right in all_prunings(one, ones)] + [majority]


def predict(tree, row):
    while not isinstance(tree, str):
        tree = tree[1+row[tree[0]]]
    return tree


def counts(tree, rows):
    return sum(row[5] if predict(tree, row)=='+' else row[4] for row in rows)


def leaves(tree):
    return 1 if isinstance(tree, str) else leaves(tree[1])+leaves(tree[2])


models = all_prunings(original, train)
assert len(models) == 9
independent = sorted((leaves(m), counts(m,train), counts(m,valid)) for m in models)
calculated = json.loads((HERE/'tree-recalculated.json').read_text(encoding='utf-8'))
reported = sorted((m['leaves'], m['train_errors'], m['validation_errors'])
                  for m in calculated['models'])
assert independent == reported
(HERE/'tree-independent-enumeration.json').write_text(
    json.dumps({'tree': original, 'n_all_majority_prunings': len(models),
                'sorted_leaf_train_validation_counts': independent,
                'agrees_with_reproduce': True}, indent=2)+'\n', encoding='utf-8')

def compact(text):
    return ''.join(c.lower() for c in text if c.isalnum())

candidate = (HERE/'sample-final-learning.md').read_text(encoding='utf-8')
compact_candidate = compact(candidate)
unmatched = [p for p in paragraphs if len(compact(p)) > 6
             and compact(p) not in compact_candidate]
(HERE/'source-text-compare.json').write_text(json.dumps(
    {'comparison': 'Each DOCX paragraph alphanumeric normalized, text+OMML.',
     'unmatched_paragraphs': unmatched,
     'note': 'Manual source comparison is still required for numbering, math layout and semantics.'},
    ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

evidence = {
    'author_id': '/root/is6400_sample_author',
    'scope': '9 subquestions: Q1(1-2), Problem3(1-4), Q5(1-3). Learning walkthrough only.',
    'writes': 'New scratch dot-author only; no formal vault write, Git, board, user message or submission.',
    'source_file': str(SOURCE), 'source_sha256': sha(SOURCE),
    'source_native_tables': len(doc.findall('.//w:tbl',NS)),
    'source_media': media, 'source_embedded_data_objects': embeddings,
    'missing_data_search': {
        'filenames': ['Q1.xlsx','Q4 BTC-USD.csv'],
        'patterns': ['^Q1\\.xlsx$', '^Q4[ _-]*BTC.*\\.csv$'],
        'searched_roots': ['D:/上课资料 (including CityU)',
                           'C:/Users/BenLi/Downloads', 'C:/Users/BenLi/Desktop',
                           'C:/Users/BenLi/Documents', 'C:/Users/BenLi/OneDrive',
                           'C:/Users/BenLi/anaconda_projects',
                           'E:/app-data/codex/scratchpad/cityu-notes-20261118'],
        'result': 'No matching files found in checked roots; no claim about unchecked cloud/other locations.'},
    'calculation': 'Original tree and all 9 majority-class prunings recomputed; independent explicit-tree enumeration agrees.',
    'execution': {'tree': 'Executed against all original tabulated inputs.',
                  'Q1': 'Original data absent. Missing-file path exercised, exit 2; no numeric result.',
                  'BTC': 'Original data absent. Missing-file path exercised, exit 2; no numeric forecast or screenshot.'},
    'package_versions': {name: importlib.metadata.version(name)
                         for name in ['pandas','numpy','scikit-learn','statsmodels','openpyxl']},
    'mechanical': 'note_quality current --strict --sections --readability: PASS, R hard 0, warnings require semantic review.',
    'independent_review': 'Pending; author did not review own text as independent agent.',
    'final_rendered_candidate_visuals': 'Pending, not claimed from source-image viewing.',
    'content_blockers': ['Q1 missing-count and IQR values need Q1.xlsx.',
                         'Q5 five numeric forecasts/results screenshot need original Q4 BTC-USD.csv.',
                         'Official solutions and current Canvas status not verified by this author.'],
    'source_paragraph_comparison_unmatched': unmatched,
    'files': {p.name: sha(p) for p in HERE.iterdir()
              if p.is_file() and p.name not in ['frozen-evidence.json']}
}
(HERE/'frozen-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'candidate_sha256':sha(HERE/'sample-final-learning.md'),
                  'source_sha256':sha(SOURCE), 'tree_models':len(models),
                  'source_unmatched': unmatched}, ensure_ascii=False, indent=2))
