"""Export the saved, executed notebook with Jupyter's standard HTMLExporter.

Equivalent CLI: python -m jupyter nbconvert --to html <notebook> --output-dir ../submission
There is no independent HTML layout, rearrangement, formula conversion or content rewrite.
"""
from pathlib import Path
import sys,argparse
from nbconvert import HTMLExporter
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'_meta/tools/safe_write.py').exists())
sys.path.insert(0,str(ROOT/'_meta/tools'))
from safe_write import atomic_write

def export(notebook,destination):
    exporter=HTMLExporter(template_name="lab")
    body,resources=exporter.from_filename(str(notebook))
    destination.parent.mkdir(parents=True,exist_ok=True)
    atomic_write(destination,body)
    print("Jupyter nbconvert HTML export:",destination)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--notebook",type=Path,default=HERE/"IS6400_Week4_60234350_LI_Binxiong.ipynb")
    parser.add_argument("--out",type=Path,default=HERE.parent/"submission/IS6400_Week4_60234350_LI_Binxiong.html")
    args=parser.parse_args()
    export(args.notebook,args.out)
