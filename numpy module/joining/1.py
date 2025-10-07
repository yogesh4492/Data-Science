""" Joining array means join two arrays in single one"""

#for normal use .concatenate() function 

import numpy as np

arr1=np.array([12,2,3,4,5])
arr2=np.array([13,14,15,16])
arr=np.concatenate((arr1,arr2))
print(arr)

