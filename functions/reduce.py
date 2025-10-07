""" Reduce() comes from functools module of python
Syntax: 
reduce (function,iterable[ini])
reduce deals wvalue at same time from same list 

reduce give the original result in string in most cases no needs to convert the result in list
"""

from functools import reduce

lis=['Yogesh','rajendrabhai','patel']
res=reduce(lambda x,y:x+" "+y,lis)

print(res.upper())


"""Reduce with Normal Function"""

def sum(a,b):
    return a+b
lis=[x for x in range(1,6)]
res=reduce(sum,lis)
print(res)

""" Using Reduce with Lambdas"""


rs=reduce(lambda x,y:x*y,lis)
print(rs)#1*2*3*4*5

""" Using reduce with operator module value"""
import operator
rs=reduce(operator.add,lis)
res=reduce(operator.mul,lis)
result=reduce(operator.add,['yogesh','kumar ',' patel'])
print(res)
print(rs)
print(result)


""" with th initializer value"""


r_i=reduce(lambda x,y:x+y,lis,10)#start with 10
print(r_i)