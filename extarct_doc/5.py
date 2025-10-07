import os
import io
import typer
import pickle
from rich.progress import Progress
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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


def list_all_files(service, folder_id):
    """Fetch all files from Google Drive folder (handles pagination)."""
    files = []
    page_token = None
    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(id, name, mimeType)",
            pageSize=1000,  # get up to 1000 per call
            pageToken=page_token
        ).execute()

        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    return files


@app.command()
def download_files(folder_id: str, output: str = typer.Argument("downloads")):
    """
    Download .zip, .pdf, and .doc/.docx files from a Google Drive folder.
    """
    service = get_drive_service()
    os.makedirs(output, exist_ok=True)

    file_types = [
        "application/zip",
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword"
    ]

    typer.echo("📁 Fetching all files from Google Drive folder...")
    files = list_all_files(service, folder_id)

    if not files:
        typer.echo("❌ No files found in this folder.")
        raise typer.Exit()

    typer.echo(f"✅ Found {len(files)} total files. Downloading allowed types...")

    with Progress() as progress:
        task = progress.add_task("Downloading...", total=len(files))
        for file in files:
            if file["mimeType"] in file_types:
                file_id = file["id"]
                file_name = file["name"]
                file_path = os.path.join(output, file_name)

                try:
                    request = service.files().get_media(fileId=file_id)
                    fh = io.FileIO(file_path, "wb")
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                    fh.close()
                    progress.console.print(f"✅ Downloaded: {file_name}")
                except Exception as e:
                    progress.console.print(f"⚠️ Failed: {file_name} — {e}")
            progress.update(task, advance=1)

    typer.echo("🎉 All downloads complete.")


if __name__ == "__main__":
    app()
