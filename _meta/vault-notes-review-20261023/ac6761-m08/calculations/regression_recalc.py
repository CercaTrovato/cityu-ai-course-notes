from fractions import Fraction as F
data = [(F(1),F(2)), (F(2),F(3)), (F(3),F(5))]
n = len(data)
xbar = sum(x for x,y in data) / n
ybar = sum(y for x,y in data) / n
num = sum((x-xbar)*(y-ybar) for x,y in data)
den = sum((x-xbar)**2 for x,y in data)
b = num / den
a = ybar - b*xbar
rows = []
for x,y in data:
    pred = a+b*x
    resid = y-pred
    rows.append((x,y,pred,resid,resid**2))
sse = sum(r[4] for r in rows)
print('xbar=',xbar,'ybar=',ybar,'numerator=',num,'denominator=',den)
print('a=',a,'b=',b,'SSE=',sse)
for row in rows:
    print(row)
print('residual_sum=',sum(r[3] for r in rows))
print('prediction_at_4=',a+b*4)
