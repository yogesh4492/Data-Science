import numpy as np
arr=np.array([23,4,5,6,7,4,5,67,7,7,8,7])
# x=arr.reshape(3,2)
# print(x)
arr1=np.array([1,2,3,4,5,6,7,8,9,10,11,12])
print(arr1.shape)

y=arr1.reshape(2,3,2)# first 2 contain 2 value in one array ,3 is 3 of list and last 2 divide in two part 
# print(arr1.shape)

print(y)