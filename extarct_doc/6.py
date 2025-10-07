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


@app.command()
def download_files(folder_id: str, output: str = typer.Argument("downloads")):
    """Download files (including Google Docs/Sheets/Slides) from a Google Drive folder."""
    service = get_drive_service()
    os.makedirs(output, exist_ok=True)
    output = os.path.abspath(output)
    typer.echo(f"📂 Download path: {output}")

    files = list_all_files(service, folder_id)
    if not files:
        typer.echo("❌ No files found in folder.")
        raise typer.Exit()

    typer.echo(f"✅ Found {len(files)} files. Starting download...")

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

    with Progress() as progress:
        task = progress.add_task("Downloading...", total=len(files))
        for f in files:
            file_id = f["id"]
            name = f["name"]
            mime = f["mimeType"]

            try:
                if mime in normal_types:
                    # Normal downloadable file
                    request = service.files().get_media(fileId=file_id)
                    filepath = os.path.join(output, name)
                    with io.FileIO(filepath, "wb") as fh:
                        downloader = MediaIoBaseDownload(fh, request)
                        done = False
                        while not done:
                            status, done = downloader.next_chunk()
                    progress.console.print(f"✅ Downloaded: {name}")

                elif mime in export_map:
                    # Google Doc/Sheet/Slide
                    export_mime, ext = export_map[mime]
                    request = service.files().export_media(fileId=file_id, mimeType=export_mime)
                    filepath = os.path.join(output, f"{name}{ext}")
                    with io.FileIO(filepath, "wb") as fh:
                        downloader = MediaIoBaseDownload(fh, request)
                        done = False
                        while not done:
                            status, done = downloader.next_chunk()
                    progress.console.print(f"📄 Exported: {name}{ext}")

                else:
                    progress.console.print(f"⚠️ Skipped unsupported type: {name}")

            except Exception as e:
                progress.console.print(f"❌ Failed: {name} — {e}")

            progress.update(task, advance=1)

    typer.echo("🎉 All downloads complete!")


if __name__ == "__main__":
    app()
