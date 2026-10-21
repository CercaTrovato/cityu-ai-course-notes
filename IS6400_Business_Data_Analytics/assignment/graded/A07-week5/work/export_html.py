from pathlib import Path
import sys
import nbformat
from nbconvert import HTMLExporter
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / "_meta/tools"))
from safe_write import atomic_write
notebook = nbformat.read(HERE / "IS6400_Week5_60234350_LI_Binxiong.ipynb", as_version=4)
html, _ = HTMLExporter(template_name="lab").from_notebook_node(notebook)
target = HERE.parent / "submission/IS6400_Week5_60234350_LI_Binxiong.html"
atomic_write(str(target), html + "\n")
print(target)
