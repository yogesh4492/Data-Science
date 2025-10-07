import numpy as np

arr=np.array([[1,2,23,43,45],[23,45,67,87,98]])
for id,i in np.ndenumerate(arr):
    print(id,i)