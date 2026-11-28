from pathlib import Path
import hashlib,json
root=Path('E:/app-data/codex/scratchpad/ef5560-final-20261128')
items=[('m11','首轮VAD批处理版946段存在漏句，不用于融合','首轮946段因VAD漏低声语句不用于融合','ddb0849fd31d45515b1c5452f415c858e0949da595096ef8e6c6a0b0639bafa8'),('m12','教授把“抽取数字”扩为“读懂条件”，说明','教授把“抽取数字”扩为“读懂条件”，问','365c481e9bdc9604d74f8d94e6ef1ca74e83ee138054d2865760ecc964bd5f7a')]
rows=[]
for name,new,old,oldhash in items:
    p=root/name/'merged.md'; raw=p.read_bytes(); enc=raw.decode('utf-8')
    assert enc.count(new)==1
    inverse=enc.replace(new,old).encode('utf-8')
    mapped=hashlib.sha256(inverse).hexdigest()
    row={'candidate':name,'final_sha256':hashlib.sha256(raw).hexdigest(),'inverse_only_this_replacement_sha256':mapped,'matches_previously_reviewed_sha':mapped==oldhash}
    print(json.dumps(row))
    assert mapped==oldhash
    rows.append(row)
(root/'independent-review/final-wording-hash-mapping.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
