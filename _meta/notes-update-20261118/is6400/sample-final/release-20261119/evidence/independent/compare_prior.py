from pathlib import Path
import json
S=Path(__file__).resolve().parent
p=Path('D:/上课资料/CityU/_meta/notes-update-20261118/is6400/sample-final/tree-calculations.json')
old=json.loads(p.read_text(encoding='utf-8'));new=json.loads((S/'tree-independent.json').read_text(encoding='utf-8'))
a={(x['leaves'],x['training_errors'],x['validation_errors']) for x in old['models']}
b={(x['leaves'],x['train_errors'],x['validation_errors']) for x in new['models']}
assert len(a)==len(b)==9 and a==b
out={'prior_file':str(p),'prior_source_sha256':old['source_sha256'],'nine_model_results_equal_to_this_actual_independent_replay':True,'prior_original_train_errors':old['training_original']['errors'],'prior_original_validation_errors':old['validation_original']['errors']}
(S/'prior-tree-comparison.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
