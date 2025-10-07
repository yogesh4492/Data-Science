""" searching array """
#1. using where () method :its return tuple and index where the element is present

import numpy as np
arr=np.array([1,2,3,4,45,32,1])
x=np.where(arr==1)
print(x)


#even number using where()

arr1=np.array([1,2,3,4,5,6])
y=np.where(arr1%2!=0)
print(y)


# 2. searchsorted () check s and return ordered ouput its first srt the array an after that return the index of its

arr2=np.array([2,3,4,5,5])
z=np.searchsorted(arr2,5)
print(z)

