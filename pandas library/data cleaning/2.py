
""" Pandas Cleaning Wrong Format Data 
There Is two Ways To 
remove the rows
or convert all cells in the column into the same format

"""

#converting in the same format

import pandas as pd
pd.options.display.max_rows=200
view=pd.read_csv("/home/yogesh/Downloads/data.csv")
print(view)
# view['Date']=pd.to_datetime(view['Date'],format="mixed") its not work if date column not in data.csv
#otherwise throw key error

# print(view)