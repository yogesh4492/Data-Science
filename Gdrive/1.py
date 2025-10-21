import json 
import csv
import typer
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress
import os
import glob
import pickle


from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
creds=None

scope=['https://www.googleapis.com/auth/drive']


if os.path.exists('token.pickle'):
    
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
else:
    flow=InstalledAppFlow.from_client_secrets_file('credentials.json',scope)

    creds=flow.run_local_server(port=0)


service=build('drive','v3',credentials=creds)




print(creds)