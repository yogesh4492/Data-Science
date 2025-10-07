""" Pandas data Cleaning :

cleaning means remove bad data from the dataset 
bad data: 
- empty cells
- Data in wrong format
-  wrong Data
- Duplicates
"""

# this file is for the  empty  cells 
""" this code create new dataset without emptyshells its not change original """
# import pandas as pd
# # pd.options.display.max_rows=200
# view=pd.read_csv("/home/yogesh/Downloads/data.csv")
# new_view=view.dropna()
# print(new_view.info())
# print(view.info())

import pandas as pd
view=pd.read_csv("/home/yogesh/Downloads/data.csv")
view.dropna(inplace=True)
print(view.info())

 
