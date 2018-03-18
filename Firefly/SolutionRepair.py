import math
import random
import operator
import numpy as np

pop=[]
noofVM=5
random.seed(50)
x = [random.randint(0, noofVM-1) for x in range(0, noofVM)]
print(x)
# x.sort()
# print(x)

temp = random.sample(range(0, noofVM),noofVM)
temp.sort()
print(temp)

z=list(set(temp)-set(x))
z.sort()
print(z)

flag = [0]*noofVM
print(flag)

for i in range(0,len(x)):
    dre=x[i]
    if flag[dre]==0:
        flag[dre]=1
    else:
        min=10000
        for j in range(0,len(z)):
            if(int(math.fabs(z[j]-dre)<min)):
                min=math.fabs(z[j]-dre)
                index=j
        dre2=z[index]
        flag[dre2]=1
        x[i]=z[index]
        z.remove(z[index])
print(x)

a=list(map(operator.sub,x,temp))
print(a)
for i in range (0,5):
    a[i]=a[i]*a[i]
print(a)
r=sum(a)
print(r)