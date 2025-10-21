from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import boto3
import zipfile
import traceback
import json
import csv
import pickle
import typer
import os
import io
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress


scope=['https://www.googleapis.com/auth/drive']

# flow=InstalledAppFlow.from_client_secrets_file('credentials.json',scope)

# creds=flow.run_local_server(port=0)

# service=build('drive','v3',credentials=creds)



class Main:
    def __init__(self,folder_id):
        self.folder_id=folder_id
    # def authenticate(self):
    #     creds=None
    #     if os.path.exists('token.pickle'):
    #         with open('token.pickle','rb') as token:
    #             creds=pickle.load(token)
    #     if not creds or not creds.valid:
    #         if creds and creds.refresh_token and creds.expired:
    #             creds.refresh(Request())
    #         else:
    #             flow=InstalledAppFlow.from_client_secrets_file('credentials.json',scope)
    #             creds=flow.run_local_server(port=0)
    #             with open('token.pickle','wb') as token:
    #                 pickle.dump(creds,token)
    #     return creds
    def run(self):
        authn=self.auth()
        aut=self.authentication()
        service=build('drive','v3',credentials=aut)
        list1=self.processing(service)
        print(authn)
        print(aut)
        print(list1)
    def auth(self):
        creds=None
        if os.path.exists('token.pickle'):
            with open('token.pickle','rb') as token:
                creds=pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.refresh_token and creds.expired:
                creds.refresh(Request())
            else:
                flow=InstalledAppFlow.from_client_secrets_file('credentials.json',scope)
                creds=flow.run_local_server(port=0)
                with open('token.pickle','wb') as token:
                    pickle.dump(creds,token)
        return creds
    def authentication(self):
        creds=None
        if os.path.exists('token.pickle'):
            with open('token.pickle','rb') as token:
                creds=pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.refresh_token and creds.expired:
                creds.refresh(Request())
            else:
                flow=InstalledAppFlow.from_client_secrets_file('credentials.json',scope)
                creds=flow.run_local_server(port=0)
                with open('token.pickle','wb') as token:
                    pickle.dump(creds,token)
        return creds
    def processing(self,service):
        files=[]
        page_token=None
        while True:
            resp=service.files().list(
                q=f"'{self.folder_id}' in parents and trashed=false",
                spaces='drive',
                fields='nextPageToken,files(id,name,size)',
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                pageToken=page_token
            ).execute()

            for f in resp.get('files', []):
                if f.get('mimeType') == 'application/vnd.google-apps.folder':
                    files.extend(self.processing(service, f['id']))
                else:
                    files.append(f)
            page_token = resp.get('nextPageToken')
            if not page_token:
                break
        return files
    

app=typer.Typer()

@app.command()
def main(folder_id):
    Obj=Main(folder_id)
    Obj.run()


if __name__=="__main__":
    app()




        



