import numpy as np
arr=np.array([1,2,4,5,6])
x=arr.copy()
arr[0]=42

print(x)
print(arr)
