import numpy as np

arr=np.array([1,2,43,46])

#op_dtypes give binary
for i in np.nditer(arr,flags=['buffered'],op_dtypes='S'):
    print(i)