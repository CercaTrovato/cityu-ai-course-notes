from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
P=Path(__file__).parent;O=P/'new-assets';O.mkdir(exist_ok=True)
font=FontProperties(fname=r'C:\Windows\Fonts\msyh.ttc');plt.rcParams['font.family']=font.get_name();plt.rcParams['axes.unicode_minus']=False
x=[F(1),F(2),F(3)];y=[F(2),F(3),F(5)];xm=sum(x)/3;ym=sum(y)/3;V=sum((v-xm)**2 for v in x);S=sum((a-xm)*(b-ym) for a,b in zip(x,y));T=sum((v-ym)**2 for v in y);slope=S/V;intercept=ym-slope*xm;pred=[intercept+slope*v for v in x];res=[a-b for a,b in zip(y,pred)];sse=sum(v*v for v in res)
assert (slope,intercept,sse)==(F(3,2),F(1,3),F(1,6))
fig,ax=plt.subplots(figsize=(9.4,5.6));ax.axvspan(3,4.3,color='#fbefe0',alpha=.8,label='超过本例训练输入范围')
xx=[.7,4.2];ax.plot(xx,[float(intercept+slope*F(str(v))) for v in xx],color='#245b86',label='拟合直线：预测 = 1/3 + 1.5 × 批次')
ax.scatter([float(v) for v in x],[float(v) for v in y],s=65,color='#172c3d',zorder=4,label='已知实际观测：三点均为笔记自拟')
for i,(xi,yi,pi,ei) in enumerate(zip(x,y,pred,res)):
 ax.plot([float(xi)]*2,[float(pi),float(yi)],color='#c34334',lw=3,zorder=5)
 ax.scatter([float(xi)],[float(pi)],color='white',edgecolor='#245b86',s=45,zorder=4)
 ax.annotate('残差 '+str(ei),(float(xi),float((yi+pi)/2)),xytext=(12,6 if i!=1 else -22),textcoords='offset points',fontproperties=font,color='#9e3226')
future=intercept+slope*4;ax.scatter([4],[float(future)],s=100,facecolors='none',edgecolor='#a86d26',lw=2,zorder=5);ax.text(3.12,4.05,'空心点 x=4：预测 19/3\n未知实际值，不画真实残差',fontproperties=font,color='#855521')
ax.set(xlim=(.65,4.35),ylim=(1.3,7),xlabel='订单批次数 x（批）',ylabel='对账工时 y（小时）',title='同一个 x 上，实际点与拟合线之间的竖直差是残差')
ax.legend(loc='upper left',prop=font,frameon=False,fontsize=10);ax.grid(alpha=.15);fig.tight_layout();fig.savefig(O/'regression-three-points.svg');fig.savefig(O/'regression-three-points.png',dpi=140);plt.close(fig)
evidence={'source':'All three points and scenarios are note supplements, not reconstructed source slide30 data.','x':[str(v) for v in x],'y':[str(v) for v in y],'V':str(V),'S':str(S),'T':str(T),'slope':str(slope),'intercept':str(intercept),'predictions':[str(v) for v in pred],'residuals':[str(v) for v in res],'SSE':str(sse),'completed_square_min':str(T-S*S/V),'future_x4_prediction':str(future),'future_actual_y':None,'future_residual':None,'rl':{'A':-1,'B':5,'C':5,'A_then_C_return':4,'B_then_C_return':10,'C_1_5h_reward':4,'B_then_C_total_hours_after_change':2.5},'semi_supervised':{'labels_total':100,'initial_fit':80,'heldout':20,'unlabeled':900,'selected_pseudo':60,'retrained':140},'cash_forecast':{'base':100+80-150,'receipt_delayed':100-150}}
(O/'new-calculation-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(evidence,ensure_ascii=False))
