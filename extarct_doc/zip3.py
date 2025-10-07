import os
import io
import zipfile
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from rich.progress import Progress

# Google Drive full access scope
SCOPES = ['https://www.googleapis.com/auth/drive']

# Number of parallel downloads (tune this based on your network)
MAX_WORKERS = 10


def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def list_files(service, folder_id):
    """Recursively list all files inside a folder"""
    files = []
    page_token = None
    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces='drive',
            fields='nextPageToken, files(id, name, mimeType)',
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            pageToken=page_token
        ).execute()
        for file in response.get('files', []):
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                files.extend(list_files(service, file['id']))
            else:
                files.append(file)
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    return files


def download_file(service, file_id, mime_type, name):
    """Download or export a file depending on type"""
    export_map = {
        'application/vnd.google-apps.document': 'application/pdf',
        'application/vnd.google-apps.spreadsheet': 'text/csv',
        'application/vnd.google-apps.presentation': 'application/pdf'
    }

    try:
        if mime_type in export_map:
            request = service.files().export_media(fileId=file_id, mimeType=export_map[mime_type])
        else:
            request = service.files().get_media(fileId=file_id, supportsAllDrives=True)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.seek(0)
        return (name, fh.read())
    except Exception as e:
        print(f"[!] Skipping {name} ({file_id}) → {e}")
        return None


def download_and_zip_folder(folder_id, zip_name='drive_folder.zip'):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    print("[+] Fetching file list from Drive...")
    all_files = list_files(service, folder_id)
    total_files = len(all_files)
    print(f"[+] Total files found: {total_files}")

    if total_files == 0:
        print("[-] No files found in this folder.")
        return

    # Parallel download
    with Progress() as progress:
        task = progress.add_task("[green]Downloading files...", total=total_files)
        results = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(download_file, service, f['id'], f['mimeType'], f['name']): f for f in all_files
            }
            for future in as_completed(futures):
                data = future.result()
                if data:
                    results.append(data)
                progress.advance(task)

    # Write all files to ZIP
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for name, content in results:
            zipf.writestr(name, content)

    print(f"\n✅ Folder downloaded and zipped successfully: {zip_name}")


if __name__ == '__main__':
    folder_id = input("Enter Google Drive Folder ID: ").strip()
    zip_name = input("Enter output ZIP name (default: drive_folder.zip): ").strip() or "drive_folder.zip"
    download_and_zip_folder(folder_id, zip_name)
