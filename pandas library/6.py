""" Pandas Anylyzing Data 
That Can Analyzy data fro  file
1 head() method its returns the header and no of rows  
"""

import pandas as pd

file='/home/yogesh/Desktop/python standard library/task1/1.csv'

view=pd.read_csv(file)
print(view.head(2))# its give header and specified no of rows by default its 5
print(view.head())# by default its 5



# now tail() methiod is oposite from head() its also return the header

print(view.tail())# by default its 5)
print(view.tail(2))# its return last 2 row from data



print(view.info())

