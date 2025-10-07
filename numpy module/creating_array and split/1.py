""" Various way to create array """
#1 . is using numpy.array()
import numpy as np
arr=np.array([1,2,3,4,5])
print(arr)

# 2 . using various special function
#  i)np.zeros():- it creates an array fields with zero
arr1=np.zeros(5)
print(arr1)
#ii) np.ones():- it creates an array filled with ones
arr2=np.ones(5)
print(arr2)
#iii) np.full():sepcified value constant value
arr3=np.full((2),7)
print(arr3)

#iv) np.arange():- range function activate start,stop,step 4
arr4=np.arange(2,11,2)
print(arr4)

#v)np.linespace(): that creates array start  stop are first two parameter and last is how many part between start and stop
arr5=np.linspace(0,1,5)
print(arr5)



#3 . create using randomr randint
arr6=np.random.randint(0,10,size=(2,3))
print(arr6)

#4. 
