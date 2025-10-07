""" Wrong Data Cleaning using Pandas """

#Wrong Data means Not to be "Empty cell" or 'Wrong format data' 
import pandas as pd

view=pd.read_csv("/home/yogesh/Downloads/data.csv")
view.drop_duplicates(inplace=True)
print(view.to_string())