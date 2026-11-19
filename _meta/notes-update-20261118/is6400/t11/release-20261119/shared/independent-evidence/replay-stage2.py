from pathlib import Path
import sys,runpy,json,hashlib,time
root=Path('D:/上课资料/CityU')
out=Path(__file__).parent
sys.path.insert(0,str(root/'_meta/tools'))
import safe_write
original=safe_write.atomic_write
script=root/'IS6400_Business_Data_Analytics/assignment/graded/A12-week11-model-selection/work/learning-reference.py'
expected=script.parent/'learning-reference-results.json'
target=out/'stage-2-new-replay-results.json'
assert not target.exists()
oldsha=hashlib.sha256(expected.read_bytes()).hexdigest()
scriptsha=hashlib.sha256(script.read_bytes()).hexdigest()
def redirect(path,content,*args,**kwargs):
    if Path(path).resolve()!=expected.resolve():raise RuntimeError('Unexpected replay write target: '+str(path))
    return original(target,content,*args,**kwargs)
safe_write.atomic_write=redirect
t=time.time()
print('Executing actual learner-linked script; only expected final result target redirected to new independent scratch.',flush=True)
print('SCRIPT_SHA256='+scriptsha,flush=True)
runpy.run_path(str(script),run_name='__main__')
old=json.loads(expected.read_text(encoding='utf-8'));new=json.loads(target.read_text(encoding='utf-8'))
old.pop('elapsed_seconds',None);new.pop('elapsed_seconds',None)
assert old==new
assert hashlib.sha256(expected.read_bytes()).hexdigest()==oldsha
assert hashlib.sha256(script.read_bytes()).hexdigest()==scriptsha
original(out/'stage-2-new-replay-verification.json',json.dumps({'script':str(script),'script_sha256':scriptsha,'original_result':str(expected),'original_result_sha256':oldsha,'new_result':str(target),'new_result_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'wall_seconds':time.time()-t,'equal_except_elapsed':True,'original_result_unchanged':True,'new_execution':True,'write_difference':'only final JSON redirected to this reviewer scratch; actual __file__, root discovery, input/model/splits/seeds/computation unchanged'},ensure_ascii=False,indent=2)+'\n')
print('RESULTS_EQUAL_EXCEPT_ELAPSED=True; ORIGINAL_RESULT_UNCHANGED=True',flush=True)
