""" Filter Function filter the result with some condition 

# filter have two parameter 
  1.function: that complete return true or false based on condition
  2: any iterable(list,tuple,set)
its give result in filter object so convert the result into the list also before printing
"""

def res(w):
    return w.startswith('a')
lis=['apple','bannana','almond']
result=filter(res,lis)
print(list(result))


# filter the even numbers 

def even(n):
    return n%2==0
lis1=[1,2,3,45,56,65,68,70]
result=filter(even,lis1)
print(list(result))