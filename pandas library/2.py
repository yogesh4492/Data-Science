"""pandas Series is just like tble column"""

import pandas as pd

myvar=[1,2,3,4,5]
var=pd.Series(myvar)
print(var)

print(myvar[0])# in normal pyton its index but when you come in pndas its labels

#but in labels you have special feature to also change index with specified value
# series () function have index parameter their you can give any specific indedx to array


myvar1=[1,2,3,4]
var=pd.Series(myvar1,index=['x','y','z','a'])
print(var)


myvar2={'day1':101,'day2':102,'day3':103,'day4':104,'day5':105}
var3=pd.Series(myvar2)
print(var3)

myvar2={'day1':101,'day2':102,'day3':103,'day4':104,'day5':105}
var3=pd.Series(myvar2,index=['day1'])
print(var3)
