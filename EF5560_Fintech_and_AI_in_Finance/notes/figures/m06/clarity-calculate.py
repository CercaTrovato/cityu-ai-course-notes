from pathlib import Path
import json,argparse
parser=argparse.ArgumentParser(description='M06 clarity teaching examples; this is not SHA-256 collision generation or an Ethereum client.')
parser.add_argument('--output',required=True)
out=Path(parser.parse_args().output);out.mkdir(parents=True,exist_ok=True)
toy=[{'input':n,'remainder':n%4,'digest':format(n%4,'02b')} for n in range(5)]
assert toy[0]['digest']==toy[4]['digest'] and toy[0]['input']!=toy[4]['input']
assert format(1%4,'02b')==format(5%4,'02b')=='01'
weights={'A':40,'B':35,'C':25};total=sum(weights.values())
def support(groups):
    weight=sum(weights[g] for g in groups)
    return {'groups':groups,'weight':weight,'fraction':weight/total,'threshold_met':3*weight>=2*total}
result={'toy_hash':{'rule':'n modulo 4, represented as two binary digits; NOT SHA-256','rows':toy,'collision_inputs':[0,4],'variant_collision_inputs':[1,5]},'pos_example':{'assumptions':'Valid blocks/votes; successive checkpoints; source already justified; simplified normal path only','total_weight':total,'weights':weights,'round1_early':support(['A']),'round1_full':{'support':support(['A','B']),'link':'C0 -> C1','after':{'C0':'finalized','C1':'justified'}},'round2_normal':{'support':support(['A','B']),'link':'C1 -> C2','after':{'C1':'finalized','C2':'justified'}},'round2_variant':{'support':support(['A','C']),'link':'C1 -> C2','after':{'C1':'justified','C2':'not justified by this link'}}}}
assert not result['pos_example']['round1_early']['threshold_met']
assert result['pos_example']['round1_full']['support']['threshold_met']
assert not result['pos_example']['round2_variant']['support']['threshold_met']
(out/'clarity-results.json').write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
print(json.dumps(result,ensure_ascii=False,indent=2))
