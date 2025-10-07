import numpy as np

arr=np.array([1,2,3,4])
arr1=np.array([5,6,7,8])

arr2=np.stack((arr,arr1),axis=1)#its take one by one element from both array like [1 5] [2 6]
print(arr2)