import math,json,pathlib
T=pathlib.Path('E:/app-data/codex/scratchpad/cityu-notes-20261028')
sig=lambda x:1/(1+math.exp(-x))
out={}
out['AND_OR_XNOR']=[]
for x1,x2 in [(0,0),(0,1),(1,0),(1,1)]:
    a=sig(-30+20*x1+20*x2);b=sig(10-20*x1-20*x2);p=sig(-10+20*a+20*b)
    out['AND_OR_XNOR'].append({'x':[x1,x2],'AND':a,'OR':sig(-10+20*x1+20*x2),'NOR':b,'XNOR':p,'class':int(p>=.5)})
out['training_step']={'initial_prediction':6,'initial_loss':2,'gradients':{'w':12,'b':6,'v':4,'c':2},'new_parameters':{'w':.88,'b':-.06,'v':2.96,'c':-.02},'new_hidden':1.7,'new_prediction':2.96*1.7-.02,'new_loss':(.5*(2.96*1.7-.02-4)**2)}
h=0;rn=[]
for x in [1,0,1]:h=math.tanh(.5*h+.2*x);rn.append(h)
out['RNN_scalar']=rn
h=.1;C=.2;lst=[]
for x in [.5,-.5]:
    f=sig(.5*h+.4*x);i=sig(-.3*h+.2*x);candidate=math.tanh(.2*h+.6*x);o=sig(.1*h-.2*x)
    Cnew=f*C+i*candidate;hnew=o*math.tanh(Cnew)
    lst.append({'x':x,'old_h':h,'old_C':C,'f':f,'i':i,'candidate':candidate,'o':o,'C':Cnew,'h':hnew});C,h=Cnew,hnew
out['LSTM_two_step']=lst
out['given_gate_LSTM']={'C':1.7,'h':.5*math.tanh(1.7)}
out['TFIDF']=.5*math.log(3)
(T/'bd09-calculations.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
