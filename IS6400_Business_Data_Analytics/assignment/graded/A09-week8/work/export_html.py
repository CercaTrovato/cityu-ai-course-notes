from pathlib import Path
import sys
import nbformat
from nbconvert import HTMLExporter

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / '_meta/tools/safe_write.py').is_file())
sys.path.insert(0, str(ROOT / '_meta/tools'))
from safe_write import atomic_write

notebook = nbformat.read(HERE / 'IS6400_Week8_60234350_LI_Binxiong.ipynb', as_version=4)
html, _ = HTMLExporter(template_name='lab').from_notebook_node(notebook)
target = HERE.parent / 'submission/IS6400_Week8_60234350_LI_Binxiong.html'
atomic_write(str(target), html)
print(target)
