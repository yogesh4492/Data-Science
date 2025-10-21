import io
import os
import pickle
import time
import zipfile
import tempfile
import traceback
import typer

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress

scope=['https://www.googleapis.com/auth/drive']


# EXPORT_MAP = {
#     'application/vnd.google-apps.document': ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx'),
#     'application/vnd.google-apps.spreadsheet': ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx'),
#     'application/vnd.google-apps.presentation': ('application/vnd.openxmlformats-officedocument.presentationml.presentation', '.pptx'),
# }
class Main:
    def __init__(self,folder_id):
        self.folder_id=folder_id

    def authenticate(self):
        creds=None
        if os.path.exists('token.pickle'):
            with open('token.pickle','rb') as p:
                creds=pickle.load(p)
        if  not creds or not creds.valid:
            if creds and creds.refresh_token and creds.expired:
                creds.refresh(Request())
            else:
                flow=InstalledAppFlow.from_client_secrets_file('credentials.json',scope)
                creds=flow.run_local_server(port=0)
                with open('token.pickle','wb') as toke:
                    pickle.dump(creds,toke)
        return creds 

                
    def list_files(self,service):
        file=[]
        page_toke=None
        while True:
            resp=service.files().list(
                q=f"'{self.folder_id}' in parents and trashed=false"
                spaces='drive',
                fields='nextPageToken,files(id,name,size)'
            )



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
    
    def run(self):
        res=self.authenticate()
        service=build('drive','v3',credentials=res,cache_discovery=False)
        proc=self.processing(service)
        print(proc)



app=typer.Typer()
@app.command()
def main(folder_id):
    obj=Main(folder_id)
    obj.run()

if __name__=="__main__":
    app()



