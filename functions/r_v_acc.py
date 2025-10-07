""" reduce and accumulate both tkes two value from the iterable and return result 

the difference beetween them is accumulates comes in itrtools() module and reduce coimes ith the funtools module
second diff is the accumulate is return vlue like yield method and the reduce retur the final result
"""

from functools import reduce
from itertools import accumulate
from operator import add
lis=[x for x in range(1,11)]
res=reduce(lambda x,y:x+y,lis)#reduce method give the final sum
result=list(accumulate(lis,add))# accumulate  methdod  gives the result after every sum ofm two values
print(lis)
print(res)
print(result)

