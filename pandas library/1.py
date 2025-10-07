""" Pandas Library Is used To Anyly data """

""" 
What IS PAndas :pandas is used in data science branch deal with large data set """


import pandas as pd
mydataset={
    'car':['bmw','hitachi','thar'],
    'rating':['1.2',3.4,4.9]

}

myda=pd.DataFrame(mydataset)
print(myda)
print("version of pandas= ",pd.__version__)