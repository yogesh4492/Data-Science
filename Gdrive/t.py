import os
import io
import pickle
import json
import csv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import progress

scope=['https://www.googleapis.com/auth/drive']


creds=None
if os.path.exists("token.pickle"):
    with open('token.pickle','rb') as rb:
        creds=pickle.load(rb)
if not creds or creds.valid:
    pass


flow=InstalledAppFlow.from_client_secrets_file("credentials.json",scope)

creds=flow.run_local_server(port=0)

service = build('drive','v3',credentials=creds)

