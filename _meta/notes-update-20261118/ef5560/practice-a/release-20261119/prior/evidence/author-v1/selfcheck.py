from pathlib import Path
import sys,json,re,hashlib,collections
sys.dont_write_bytecode=True
sys.path.insert(0,'D:/上课资料/CityU/_meta/tools')
from safe_write import atomic_write
OUT=Path(__file__).parent
fn=sys.argv[1] if len(sys.argv)>1 else 'quality-v2.txt'
raw=(OUT/fn).read_text(encoding='utf-8-sig')
j=json.loads(raw[raw.index('JSON:')+5:])
atomic_write(str(OUT/(fn+'.parsed.json')),json.dumps(j,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'C_hard':j['C']['hard'],'C_warn':j['C']['warn'],'source_contract':j['C'].get('source_contract',j['C'].get('source_checks')),'R_hard':j['R']['hard'],'R_warn_by_code':dict(collections.Counter(x[0] for x in j['R']['warn'])),'L':j.get('L',{}),'summary':j.get('problems',j.get('issues',{}))},ensure_ascii=False,indent=2))
print('top-level keys',list(j.keys()))
print('C keys',list(j['C'].keys()))
