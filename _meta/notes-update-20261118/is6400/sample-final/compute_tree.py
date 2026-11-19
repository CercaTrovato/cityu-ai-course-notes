from pathlib import Path
import json,sys,hashlib
R=Path('D:/上课资料/CityU');S=Path('E:/app-data/codex/scratchpad/cityu-notes-20261118/is6400/sample-final');P=R/'_meta/notes-update-20261118/is6400/sample-final';P.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_meta/tools'));from safe_write import atomic_write
training=[(0,0,0,0,4,0),(0,0,0,1,0,1),(0,0,1,0,0,1),(0,1,0,1,0,1),(1,0,1,0,3,0),(1,1,0,1,0,5)]
validation=[(0,0,0,1,4,0),(0,0,1,1,3,0),(0,1,0,0,0,1),(0,1,1,0,0,2),(1,0,0,0,2,0),(1,0,0,1,3,0)]
def pred(row,left,right,root=False):
 a,b,c,d,*_=row
 if root:return '-'
 if a==1:return '-' if right else ('+' if b==0 else '-')
 if left==3:return '+'
 if b==1:return '-'
 if left==2:return '+'
 if c==1:return '-'
 if left==1:return '+'
 return '+' if d==0 else '-'
def evaluate(data,left,right,root=False):
 result=[]
 for row in data:
  prediction=pred(row,left,right,root);error=row[5] if prediction=='+' else row[4]
  result.append(dict(A=row[0],B=row[1],C=row[2],D=row[3],positive=row[4],negative=row[5],prediction=prediction,errors=error))
 return dict(n=sum(r[4]+r[5] for r in data),positive=sum(r[4] for r in data),negative=sum(r[5] for r in data),errors=sum(r['errors'] for r in result),rows=result)
models=[]
for right in [False,True]:
 for left in range(4):
  tr=evaluate(training,left,right);va=evaluate(validation,left,right);leaves=(4-left)+(1 if right else 2)
  models.append(dict(model=f'L{left}-R{1 if right else 0}',left_pruning=['original','replace D by + leaf','replace C subtree by + leaf','replace left B subtree by + leaf'][left],right_pruned=right,leaves=leaves,training_errors=tr['errors'],training_error=tr['errors']/tr['n'],pessimistic=(tr['errors']+leaves)/tr['n'],validation_errors=va['errors'],validation_error=va['errors']/va['n']))
tr=evaluate(training,0,False,True);va=evaluate(validation,0,False,True);models.append(dict(model='root-only',left_pruning='entire tree replaced by majority -',right_pruned=True,leaves=1,training_errors=tr['errors'],training_error=tr['errors']/tr['n'],pessimistic=(tr['errors']+1)/tr['n'],validation_errors=va['errors'],validation_error=va['errors']/va['n']))
out=dict(source='Sample Final.docx embedded images1-3 visually read; weighted counts manually transcribed, not OCR alone',source_sha256='04ac67e3e3aa92ab2fff2895fde321d22d091e70d1b24fd1f7f202562e5fe0e7',training_original=evaluate(training,0,False),validation_original=evaluate(validation,0,False),pruned_node_training_counts=dict(D=[4,1],C=[4,2],left_B=[4,3],right_B=[3,5],A=[7,8]),models=models)
atomic_write(str(P/'tree-calculations.json'),json.dumps(out,ensure_ascii=False,indent=2)+'\n');atomic_write(str(P/'compute_tree.py'),Path(__file__).read_text(encoding='utf-8'))
print(json.dumps(dict(training_n=out['training_original']['n'],validation_n=out['validation_original']['n'],original_training_errors=out['training_original']['errors'],original_validation_errors=out['validation_original']['errors'],models=models),ensure_ascii=False,indent=2))
