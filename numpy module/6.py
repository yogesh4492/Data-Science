import numpy as np

arr=np.array([11,1.2,3.4,5.6,7.8])
print(arr.astype('i'))
arr1=np.array(['a',1.2,34.5]) #because of a valueerror occurs
# print(arr1.astype('i4')) #doent run or use exeception handling

try:
    arr1=np.array(['a',1.2,34.5]) #because of a valueerror occurs
    print(arr1.astype('i')) #doent run or use exeception handling
except Exception as e:
    print(e)
else:
    print("Exception Handling")





ar1=np.array([1,23.5,45,54])
print(ar1.astype('M'))