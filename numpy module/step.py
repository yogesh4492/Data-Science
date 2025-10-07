import numpy as np

arr=np.array([[1,2,3,4],[5,6,7,8]])

for i in np.nditer(arr[:,::2]):
    print(i)
# for i in np.nditer(arr[:,::2]):
#     print(i)
