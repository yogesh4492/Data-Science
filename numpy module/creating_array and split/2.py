""" Spliting array """
# 1. using .split() but its fail when element are less

import numpy as np

arr=np.array([1,2,3,4,5,6])
x=np.split(arr,3)
print(x)

#2. uaing .aray_split() its work also with less element

arr2=np.array([7,8,9,10,11,12,13])
y=np.array_split(arr2,4)
print(y)