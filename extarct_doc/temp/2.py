import os
import io
import typer
from rich.progress import Progress
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

app = typer.Typer()

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

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

@app.command()
def download_files(folder_id: str, output: str = typer.Argument("downloads")):
    """
    Download .zip, .pdf, and .doc/.docx files from a Google Drive folder.
    """
    service = get_drive_service()

    os.makedirs(output, exist_ok=True)
    file_types = ["application/zip", "application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]

    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])

    if not files:
        typer.echo("No files found in this folder.")
        raise typer.Exit()

    typer.echo(f"Found {len(files)} files. Downloading allowed types...")

    with Progress() as progress:
        task = progress.add_task("Downloading...", total=len(files))
        for file in files:
            if file["mimeType"] in file_types:
                file_id = file["id"]
                file_name = file["name"]
                request = service.files().get_media(fileId=file_id)
                file_path = os.path.join(output, file_name)
                fh = io.FileIO(file_path, "wb")
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                fh.close()
                progress.console.print(f"✅ Downloaded: {file_name}")
            progress.update(task, advance=1)

    typer.echo("🎉 All downloads complete.")

if __name__ == "__main__":
    app()
