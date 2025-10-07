import numpy as np

arr=np.array([1,2,3,4,5])
arr1=np.array([6,7,8,9,10])
arr3=np.dstack((arr,arr1))# its sameas stack but increase dimension
print(arr3)

