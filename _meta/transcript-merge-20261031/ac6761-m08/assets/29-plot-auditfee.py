"""Classroom PredictAuditFee.xlsx: original data and intercept-inclusive OLS.
Figure provenance: 25 observations, source units unspecified. No external test set.
"""
from pathlib import Path
from fractions import Fraction as F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DATA=[(2000,1.8,206),(2001,3.3,150),(2002,2.5,162),(2003,3.6,127),(2004,1.9,188),(2005,2.8,128),(2006,4.5,105),(2007,3.2,111),(2008,5.6,100),(2009,6.1,108),(2010,3.0,156),(2011,6.6,88),(2012,2.8,129),(2013,1.9,138),(2014,5.8,112),(2015,7.6,90),(2016,2.6,190),(2017,3.2,186),(2018,2.5,176),(2019,4.7,123),(2020,3.0,136),(2021,2.5,138),(2022,5.3,102),(2023,3.9,158),(2024,5.6,116)]
x=[F(str(row[1])) for row in DATA];y=[F(row[2]) for row in DATA];n=len(x)
b=(n*sum(xx*yy for xx,yy in zip(x,y))-sum(x)*sum(y))/(n*sum(xx*xx for xx in x)-sum(x)**2)
a=(sum(y)-b*sum(x))/n
fig,ax=plt.subplots(figsize=(8.2,4.9),layout='constrained')
ax.scatter([float(xx) for xx in x],[float(yy) for yy in y],s=38,color='#235b87',alpha=.8,label='25 observed annual pairs (2000–2024)')
xx=[1.8,7.6];ax.plot(xx,[float(a+b*F(str(v))) for v in xx],color='#b54e32',linewidth=2,label='OLS fitted on all 25 observations')
p=float(a+b*5);ax.scatter([5],[p],marker='*',s=180,color='#3f7f5f',edgecolor='white',linewidth=.7,zorder=5,label='Conditional prediction at CGI = 5')
ax.annotate(f'CGI=5: predicted AuditFee={p:.4f}',(5,p),xytext=(3.2,80),arrowprops={'arrowstyle':'->','color':'#3f7f5f'},fontsize=10)
ax.set(xlabel='CGI (source index units)',ylabel='AuditFee (source units unspecified)',title='Classroom data: association and conditional prediction')
ax.grid(alpha=.2);ax.legend(fontsize=8,loc='upper right');ax.spines[['top','right']].set_visible(False)
fig.savefig(Path(__file__).with_name('auditfee-ols.svg'))
fig.savefig(Path(__file__).with_name('auditfee-ols.png'),dpi=150)
print(f'a={float(a):.12f}, b={float(b):.12f}, CGI5={p:.12f}')
