""" Read CSv Using Pandas Module"""

import pandas as pd

csw='/home/yogesh/Desktop/python standard library/task1/1.csv'
pd.options.display.max_rows=8# its can set only 8 rows of data are visible 
df=pd.read_csv(csw)
print(df.to_string())
print(df)

#pd.optios.display.ax_rows its return  numbr of row in csv

print(pd.options.display.max_rows)#by default its 60 use can also change it but above we cn change its to 8

