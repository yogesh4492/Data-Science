import numpy as np
arr=np.array([1,2,3])
x=arr.view()
arr[0]=42
print(x)
print(arr)

x[0]=25
print(x)
print(arr)