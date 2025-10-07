import numpy as np
arr1=np.array([[1,1,2,34],[12,35,6,7]])
arr2=np.array([[1,2,3,4],[5,6,7,8]])

arr=np.concatenate((arr1,arr2),axis=1)#if array is nested use axis always
print(arr)
