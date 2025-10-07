""" Filtering array """
#1 filtering using boolean value
import numpy as np

arr=np.array([1,2,34,4,5,8])
x=[True,False,True,False,True,False]
newarr=arr[x]

print(newarr)

#2 filtering using some condition'

filtering=[]
for i in arr:
    if i>1:
        filtering.append(True)
    else:
        filtering.append(False)

new1=arr[filtering]
print(new1)

#3 even numbers 

fil=[]
for i in arr:
    if i%2==0:
        fil.append(True)
    else:
        fil.append(False)
n=arr[fil]
print(n)

