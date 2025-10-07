""" Dataframes in Pandas :
 Its sbehave like 2d array and their is loc attribte to access specific row and column"""

import pandas as pd
mydict={
    'name':['yogesh','ram','rohit','sai','rahul'],
    'age':[20,25,28,22,27]
}
var=pd.DataFrame(mydict)
print(var)

# their is loc attribut access value like index

print(var.loc[0])# its return value like series of pandas 
print(var.loc[1])


print(var.loc[[0,1,2]])


""" # Most Import thing is : import csv or any file in csv """

df=pd.read_csv("/home/yogesh/Desktop/python standard library/task1/1.csv")
print(df)


