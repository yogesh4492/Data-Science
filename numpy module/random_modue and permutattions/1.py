from numpy import random
import numpy as np

x=random.randint(100) #generate Int number
print(x)

y=random.rand(20) #generate float its return 0 to 1
print(y)

z=random.randint(100,size=(5))# gerate array randomly from size 1 -d
print(z)

a=random.randint(100,size=((3,5))) # generate   2 d array
print(a)
print(a.ndim)

# if you want to take input from list or array radomly use random.choice

# arr=[1,2,3,4,5,6]

b=random.choice([1,2,3,4,5,6])
print(b)




