import numpy as np
from numpy import random

arr=np.array([1,2,3,4])
random.shuffle(arr)
print(arr)


arr2=np.array([1,2,3,4,4,5,6])
x=random.permutation(arr2)
print(x)