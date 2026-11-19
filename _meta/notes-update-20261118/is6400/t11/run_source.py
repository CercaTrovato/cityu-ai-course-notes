from pathlib import Path
import sys,json,hashlib,os,ast,io,contextlib,warnings,platform,shutil,time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy,pandas,scipy,sklearn
R=Path('D:/上课资料/CityU');S=Path('E:/app-data/codex/scratchpad/cityu-notes-20261118/is6400/t11');P=R/'_meta/notes-update-20261118/is6400/t11';P.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_meta/tools'));from safe_write import atomic_write
src=R/'IS6400_Business_Data_Analytics/course_files_export/canvas-20261118/Week 11 selection.ipynb';nb=json.loads(src.read_text(encoding='utf-8'));run=S/'source-run';run.mkdir(exist_ok=True);shutil.copy2(R/'IS6400_Business_Data_Analytics/course_files_export/iris.txt',run/'iris.txt');os.chdir(run)
namespace={'__name__':'__main__'};results=[];current_cell=0;saved=[]
def show(*args,**kwargs):
 for fnum in plt.get_fignums():
  p=run/f'cell-{current_cell:02}-fig-{fnum:02}.png';plt.figure(fnum).savefig(p,dpi=160,bbox_inches='tight');saved.append(str(p))
 plt.close('all')
plt.show=show
for i,c in enumerate(nb['cells'],1):
 if c['cell_type']!='code':continue
 current_cell=i;before=len(saved);source=''.join(c['source']);code='\n'.join(line for line in source.splitlines() if not line.lstrip().startswith('%'));start=time.time();stream=io.StringIO();err=None;value=None
 try:
  with contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream),warnings.catch_warnings(record=True) as caught:
   warnings.simplefilter('always');tree=ast.parse(code);last=tree.body[-1] if tree.body else None
   if isinstance(last,ast.Expr):
    prefix=ast.Module(body=tree.body[:-1],type_ignores=[]);exec(compile(prefix,f'cell-{i}','exec'),namespace);value=eval(compile(ast.Expression(last.value),f'cell-{i}','eval'),namespace)
    if value is not None:print(value)
   else:exec(compile(tree,f'cell-{i}','exec'),namespace)
   if plt.get_fignums():show()
   ws=[dict(category=w.category.__name__,message=str(w.message)) for w in caught]
 except Exception as e:err=repr(e);ws=[]
 results.append(dict(cell=i,source_sha256=hashlib.sha256(source.encode()).hexdigest(),stdout=stream.getvalue(),warnings=ws,error=err,elapsed_seconds=time.time()-start,figures=saved[before:]));atomic_write(str(run/'cell-results.json'),json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 if err:break
env=dict(python=sys.version,numpy=numpy.__version__,pandas=pandas.__version__,scipy=scipy.__version__,sklearn=sklearn.__version__,matplotlib=matplotlib.__version__,source_metadata=nb['metadata'],source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),modifications=['removed only Jupyter %matplotlib inline for Python execution','Matplotlib Agg and show-save hooks; no data/model source altered'],graded_cell63='markdown prompt only; no scored answer code generated or executed')
summary=dict(environment=env,source_code_cells=sum(c['cell_type']=='code' for c in nb['cells']),executed=len(results),errors=[r for r in results if r['error']],figures=len(saved),results=results)
atomic_write(str(P/'source-run.json'),json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
atomic_write(str(P/'run_source.py'),Path(__file__).read_text(encoding='utf-8'))
print(json.dumps({k:v for k,v in summary.items() if k!='results'},ensure_ascii=False,indent=2))
for i in [10,12,16,17,19,31,42,45,46,53,54,57,59]:
 found=next((r for r in results if r['cell']==i),None)
 if found:print(f'CELL {i}: '+found['stdout'][:1800])
