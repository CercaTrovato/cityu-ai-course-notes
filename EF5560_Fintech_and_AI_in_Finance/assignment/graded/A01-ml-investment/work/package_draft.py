"""Validate draft weights and package the same teaching Notebook without outputs."""
from pathlib import Path
import argparse, importlib.util, json, os, sys, zipfile
import nbformat
from safe_write import atomic_write

WORK = Path(__file__).resolve().parent
TASK = WORK.parent if WORK.name == 'work' else WORK
SUBMISSION = TASK / 'submission'
NOTEBOOK = WORK / 'EF5560-A01-逐步实操.ipynb'
if not NOTEBOOK.exists():
    NOTEBOOK = WORK / 'EF5560-A01-step-by-step.ipynb'

def package(data_dir=None):
    if data_dir is None:
        course = next((p for p in WORK.parents if (p / 'course_files_export').is_dir()), None)
        if course is None:
            raise ValueError('Use --data-dir with the official student_release folder')
        data_dir = course / 'course_files_export/EF5560_ML_Investment_Project_2026_Student/student_release'
    release = Path(data_dir).resolve()
    SUBMISSION.mkdir(exist_ok=True)
    target_weight = SUBMISSION / 'DRAFT_EF5560_LEAD_ID.csv'
    atomic_write(target_weight, (WORK / 'output/DRAFT_EF5560_LEAD_ID.csv').read_text(encoding='utf-8'))
    # Do not create __pycache__ inside the read-only official release.
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('official_checker', release / 'check_submission_2026.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    header, dates, weights = checker.load_and_validate(target_weight)
    assert len(header) == 81 and len(dates) == len(weights) == 156
    nb = nbformat.read(NOTEBOOK, as_version=4)
    assert all(c.execution_count is not None for c in nb.cells if c.cell_type == 'code'), 'Run all cells and save before packaging'
    for cell in nb.cells:
        if cell.cell_type == 'code':
            assert not any(o.output_type == 'error' for o in cell.outputs)
            cell.outputs = []
            cell.execution_count = None
    target = SUBMISSION / 'DRAFT_EF5560_LEAD_ID_code.zip'
    temp = SUBMISSION / '.DRAFT_EF5560_LEAD_ID_code.zip'
    helpers = ['build_report.py', 'package_draft.py', 'safe_write.py']
    with zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('EF5560-A01-step-by-step.ipynb', nbformat.writes(nb))
        for name in helpers:
            z.write(WORK / name, arcname=name)
    with zipfile.ZipFile(temp) as z:
        assert z.testzip() is None
        assert sorted(z.namelist()) == sorted(['EF5560-A01-step-by-step.ipynb', *helpers])
        packaged = nbformat.reads(z.read('EF5560-A01-step-by-step.ipynb').decode('utf8'), as_version=4)
        assert all(not c.outputs and c.execution_count is None for c in packaged.cells if c.cell_type == 'code')
    assert temp.stat().st_size < 10_000_000
    os.replace(temp,target)
    print(f'Official checker PASS: {len(dates)} dates, {len(header)-1} stocks')
    print(f'ZIP: {target.stat().st_size} bytes; one output-free Notebook and {len(helpers)} helpers')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path)
    package(parser.parse_args().data_dir)
