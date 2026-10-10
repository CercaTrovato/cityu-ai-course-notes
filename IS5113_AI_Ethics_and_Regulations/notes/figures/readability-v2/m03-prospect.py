"""Render the registered teaching function to an explicitly selected SVG.

Example from the candidate package:
  python m03-prospect.py --output E:/.../preview.svg --vault-root D:/上课资料/CityU

The source-adjacent SVG is not overwritten by default. --overwrite is explicit.
"""
from pathlib import Path
import argparse, importlib.util, io, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype']='none'
matplotlib.rcParams['svg.hashsalt']='cityu-is5113-prospect-v2'
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent

def load_atomic_write(vault_root=None,tools_dir=None):
    if vault_root and tools_dir:
        raise ValueError('Use --vault-root or --tools-dir, not both')
    candidates=[]
    if tools_dir:candidates.append(Path(tools_dir).resolve()/'safe_write.py')
    elif vault_root:candidates.append(Path(vault_root).resolve()/'_meta/tools/safe_write.py')
    else:candidates.extend(parent/'_meta/tools/safe_write.py' for parent in HERE.parents)
    found=next((p for p in candidates if p.is_file()),None)
    if found is None:
        raise FileNotFoundError('safe_write.py not found; pass --vault-root or --tools-dir')
    spec=importlib.util.spec_from_file_location('cityu_safe_write',found)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.atomic_write

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=HERE/'m03-prospect.json')
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--vault-root',type=Path)
    parser.add_argument('--tools-dir',type=Path)
    parser.add_argument('--overwrite',action='store_true')
    args=parser.parse_args()
    output=args.output.resolve()
    if output.suffix.lower()!='.svg':parser.error('--output must name an SVG file')
    if output.exists() and not args.overwrite:
        parser.error('Output exists; choose a new path or explicitly pass --overwrite')
    write=load_atomic_write(args.vault_root,args.tools_dir)
    parameters=json.loads(args.input.read_text(encoding='utf-8'))
    a,b,lam=parameters['alpha'],parameters['beta'],parameters['lambda']
    def value(x):return x**a if x>=0 else -lam*(-x)**b
    xs=np.linspace(-220,220,881)
    fig,ax=plt.subplots(figsize=(8,5))
    ax.plot(xs,[value(float(x)) for x in xs],color='#24577b',label='Teaching value function')
    ax.axhline(0,color='gray',lw=.7);ax.axvline(0,color='gray',lw=.7)
    for x in [-100,100,200]:
        y=value(x);ax.scatter([x],[y],color='#a24a2e')
        ax.annotate(f'x={x}, v={y:.1f}',(x,y),xytext=(8,8),textcoords='offset points')
    ax.set_xlabel('Gain / loss relative to reference point (teaching units)')
    ax.set_ylabel('Subjective value (teaching units)')
    ax.set_title(f'Teaching parameters: alpha=beta={a}, lambda={lam}')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout()
    buf=io.StringIO();fig.savefig(buf,format='svg',metadata={'Date':'2026-10-09'})
    output.parent.mkdir(parents=True,exist_ok=True)
    write(str(output),buf.getvalue())
    print(json.dumps({'output':str(output),'input':str(args.input.resolve()),
                      'points':len(xs),'visual_review':'pending'},ensure_ascii=False))
if __name__=='__main__':main()

