import numpy as np

arr=np.array([1,2,3,4,55,34])
ar1=np.array([11,12,13,14,15,16])
arr2=np.hstack((arr,ar1))#its works like concate and its join horizontally 
print(arr2)