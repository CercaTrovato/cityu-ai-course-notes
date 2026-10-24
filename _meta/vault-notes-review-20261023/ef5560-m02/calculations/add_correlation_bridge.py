import hashlib,json,sys
from pathlib import Path
import numpy as np
B=Path(__file__).parent;R=Path('D:/上课资料/CityU');sys.path.insert(0,str(R/'_meta/tools'))
from safe_write import atomic_write
src=B/'candidate.md';text=src.read_text(encoding='utf-8');assert hashlib.sha256(src.read_bytes()).hexdigest()=='31a6336f24cb8f0b9ec1ea36621099cae469ded1c694a24c404340aece833b9d'
changes=[]
def edit(old,new,why):
 global text
 assert text.count(old)==1,(why,text.count(old));changes.append({'old':old,'new':new,'reason':why});text=text.replace(old,new,1)
edit('2013 年 Fama 得诺奖时合过影）。','2013 年 Fama 得诺奖时合过影。','删除独审指出的孤立右括号。')
anchor='**🎙️ 课堂补充**（P1 `37:28`–`39:12`）：'
bridge='**💡 先认清新闻例的对象（笔记补充）**：消费者价格指数（Consumer Price Index，CPI）衡量一篮子居民消费品和服务价格水平的变化。这里用它说明“数据属于哪个月”与“何时公开”不同，不用这则新闻证明因果关系。\n\n'
edit(anchor,bridge+anchor,'CPI首次实际用于推理前就地给中文、英文与对象作用；不改课堂原话。')
anchor='**代入课程数据**（180 个月的训练样本，2006-07 ~ 2021-06）：'
bridge=r'''**💡 从两列原数算一次（笔记教学例）**

先用后文 §2.4.1a 的三行教学数据。$x$ 是教学信号，$y$ 是教学收益（百分点）；不是另一个真实市场的样本。

| 行 | $x$ | $y$ | $x-\bar x$ | $y-\bar y$ |
|---|---:|---:|---:|---:|
| 1 | 0 | 1 | $-1$ | $-2/3$ |
| 2 | 1 | 2 | $0$ | $1/3$ |
| 3 | 2 | 2 | $1$ | $1/3$ |

1. 先求两列均值：$\bar x=1$、$\bar y=5/3$，然后逐行减去各自均值。
2. 偏差乘积相加：$S_{xy}=(-1)(-2/3)+0(1/3)+1(1/3)=1$。两列偏差平方和分别为 $S_{xx}=2$、$S_{yy}=2/3$。
3. 本例样本协方差为 $S_{xy}/(3-1)=1/2$。两个样本标准差为 $s_x=\sqrt{2/2}=1$、$s_y=\sqrt{(2/3)/2}=\sqrt{1/3}$。
4. 代入同一组行的协方差与标准差，相关系数为 $\operatorname{corr}(x,y)=(1/2)/(1\sqrt{1/3})\approx0.8660254$。它没有收益单位；任一列标准差为零时，分母为零，不能报告这个相关系数。

本例相关系数平方为 $0.75$，与后文这三行含截距简单 OLS 的 $R^2$ 对上。这里只教计算动作；不能把教学例的强关系搬给下面的真实 SPY 数据。

'''
# Raw literals above use doubled slashes for patch transport; normalize only this newly authored bridge.
bridge=bridge.replace('\\\\','\\')
edit(anchor,bridge+anchor,'补足协方差/标准差从同一两列原数到corr的当前核心操作，沿用已有三行而非新增市场结论。')
out=B/'author/main-bridge-proposed.md';atomic_write(out,text)
x=np.array([0.,1.,2.]);y=np.array([1.,2.,2.]);xc=x-x.mean();yc=y-y.mean();sx=float(np.std(x,ddof=1));sy=float(np.std(y,ddof=1));cov=float(xc@yc/2);corr=float(np.corrcoef(x,y)[0,1]);assert np.isclose(cov,.5) and np.isclose(corr**2,.75)
rec={'schema':'exact-root-targeted-replacements-v1','author_id':'/root','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'changes':changes,'calculation':{'x':x.tolist(),'y':y.tolist(),'means':[float(x.mean()),float(y.mean())],'Sxy':float(xc@yc),'Sxx':float(xc@xc),'Syy':float(yc@yc),'sample_covariance':cov,'sample_standard_deviations':[sx,sy],'correlation':corr,'correlation_squared':corr**2},'status':'pending_independent_targeted_review'}
atomic_write(B/'author/main-bridge-changes.json',json.dumps(rec,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'sha256':rec['candidate_sha256'],'changes':len(changes),'correlation':corr,'square':corr**2}))
