import numpy as np

arr=np.array([1,2,3,4],ndmin=5)#ndmin create dimension of array here 5 dimension array
print(arr)
print(arr.ndim)# 5 dimension array because ndmin is equal to 5
print(arr.shape)# shape also return tuple