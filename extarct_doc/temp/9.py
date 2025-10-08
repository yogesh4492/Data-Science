import io
import os
import zipfile
import typer
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

app = typer.Typer()
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
MAX_WORKERS = 5  # concurrency for normal file downloads


def get_drive_service():
    """Authenticate and return Google Drive API service."""
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
    return build('drive', 'v3', credentials=creds)


def list_all_files(service, folder_id):
    """Fetch all files (with pagination)."""
    files = []
    page_token = None
    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(id, name, mimeType)",
            pageSize=1000,
            pageToken=page_token
        ).execute()
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken')
        if not page_token:
            break
    return files


def download_file_to_bytes(service, f, export_map, normal_types):
    """Download a file (normal or Google Docs) and return its bytes and target name."""
    file_id = f["id"]
    name = f["name"]
    mime = f["mimeType"]

    try:
        # Normal downloadable files
        if mime in normal_types:
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            fh.seek(0)
            return name, fh.read()

        # Google Docs/Sheets/Slides
        elif mime in export_map:
            export_mime, ext = export_map[mime]
            request = service.files().export_media(fileId=file_id, mimeType=export_mime)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            fh.seek(0)
            return f"{name}{ext}", fh.read()

        else:
            return None, None
    except Exception as e:
        return f"ERROR_{name}", str(e).encode()


@app.command()
def download_to_zip(folder_id: str, output_zip: str = typer.Argument("gdrive_download.zip")):
    """
    Download all files from a Google Drive folder into a single ZIP file.
    """
    service = get_drive_service()
    typer.echo(f"📦 Creating ZIP file: {os.path.abspath(output_zip)}")

    export_map = {
        "application/vnd.google-apps.document": ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".docx"),
        "application/vnd.google-apps.spreadsheet": ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx"),
        "application/vnd.google-apps.presentation": ("application/pdf", ".pdf")
    }

    normal_types = [
        "application/pdf",
        "application/zip",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]

    files = list_all_files(service, folder_id)
    if not files:
        typer.echo("❌ No files found in folder.")
        raise typer.Exit()

    typer.echo(f"✅ Found {len(files)} files. Starting download into ZIP...")

    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zipf, Progress() as progress:
        task = progress.add_task("Downloading files...", total=len(files))

        # Split normal files and Google files
        normal_files = [f for f in files if f["mimeType"] in normal_types]
        google_files = [f for f in files if f["mimeType"] in export_map]

        # 1️⃣ Download normal files in parallel
        if normal_files:
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = [
                    executor.submit(download_file_to_bytes, service, f, export_map, normal_types)
                    for f in normal_files
                ]
                for future in as_completed(futures):
                    filename, data = future.result()
                    if filename and data:
                        zipf.writestr(filename, data)
                        progress.console.print(f"✅ Added: {filename}")
                    progress.update(task, advance=1)

        # 2️⃣ Download Google Docs/Sheets/Slides sequentially
        for f in google_files:
            filename, data = download_file_to_bytes(service, f, export_map, normal_types)
            if filename and data:
                zipf.writestr(filename, data)
                progress.console.print(f"📄 Added: {filename}")
            progress.update(task, advance=1)

    typer.echo(f"🎉 All files downloaded into {os.path.abspath(output_zip)}")
if __name__=="__main__":
    app()