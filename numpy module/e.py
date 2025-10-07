# import numpy as np

# lis1=np.array([[1,2,3,4,5],[6,7,8,9,10]])

# for i in np.nditer(lis1):
#     print(i)

# # import numpy as np

# # arr=np.array([[1,2,3,4],[5,6,7,8]])

# # for i in np.nditer(arr):
# #     print(i)
# # for i,j in enumerate(lis1):
# #     print(i,j)

import numpy as np
arr=np.array([[1,2,3,4],[5,6,7,8]])
print(arr.ndim)
for i in np.nditer(arr):
    print(i)

#its same as nested for loop
for i in arr:
    for j in i:
        print(j)