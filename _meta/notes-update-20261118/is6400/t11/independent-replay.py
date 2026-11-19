from pathlib import Path
import sys,runpy,json,hashlib
root=Path('D:/上课资料/CityU')
scratch=Path('E:/app-data/codex/scratchpad/cityu-notes-20261118/is6400/t11/independent-replay')
scratch.mkdir(exist_ok=True)
sys.path.insert(0,str(root/'_meta/tools'))
import safe_write
original=safe_write.atomic_write
script=root/'IS6400_Business_Data_Analytics/assignment/graded/A12-week11-model-selection/work/learning-reference.py'
expected=script.parent/'learning-reference-results.json'
def redirect(path,content,*args,**kwargs):
    if Path(path).resolve()!=expected.resolve():
        raise RuntimeError('Unexpected replay write target: '+str(path))
    return original(scratch/'learning-reference-results.json',content,*args,**kwargs)
safe_write.atomic_write=redirect
print('executing_final_path',script,flush=True)
print('script_sha256',hashlib.sha256(script.read_bytes()).hexdigest(),flush=True)
runpy.run_path(str(script),run_name='__main__')
old=json.loads(expected.read_text(encoding='utf-8'))
new=json.loads((scratch/'learning-reference-results.json').read_text(encoding='utf-8'))
old.pop('elapsed_seconds',None);new.pop('elapsed_seconds',None)
print('results_equal_except_elapsed',old==new,flush=True)
