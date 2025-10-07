""" Read Json Files  Using Pandas Module """
import pandas as pd

file='/home/yogesh/Desktop/python standard library/task3/USA-369/Batch19_d1_en_IN_new_files_08122025_44h49m/WITHOUT_PII/TRANSCRIPTION/en_IN_14217896_20230428.json'

view=pd.read_json(file)
df=pd.DataFrame(view)#no means 
print(df.to_string())# does ent use to_string that can som extra space