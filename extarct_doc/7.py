import os
import io
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
MAX_WORKERS = 8  # number of parallel downloads


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


def download_one(service, f, output, export_map, normal_types):
    """Download a single file (normal or Google Doc/Sheet/Slide)."""
    file_id = f["id"]
    name = f["name"]
    mime = f["mimeType"]

    try:
        if mime in normal_types:
            request = service.files().get_media(fileId=file_id)
            filepath = os.path.join(output, name)

        elif mime in export_map:
            export_mime, ext = export_map[mime]
            request = service.files().export_media(fileId=file_id, mimeType=export_mime)
            filepath = os.path.join(output, f"{name}{ext}")

        else:
            return f"⚠️ Skipped unsupported type: {name}"

        with io.FileIO(filepath, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
        return f"✅ Downloaded: {os.path.basename(filepath)}"

    except Exception as e:
        return f"❌ Failed: {name} — {e}"


@app.command()
def download_files(folder_id: str, output: str = typer.Argument("downloads")):
    """Download files (including Google Docs/Sheets/Slides) from a Google Drive folder in parallel."""
    service = get_drive_service()
    os.makedirs(output, exist_ok=True)
    output = os.path.abspath(output)
    typer.echo(f"📂 Download path: {output}")

    files = list_all_files(service, folder_id)
    if not files:
        typer.echo("❌ No files found in folder.")
        raise typer.Exit()

    typer.echo(f"✅ Found {len(files)} files. Starting parallel download...")

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

    # Use ThreadPoolExecutor to download files concurrently
    with Progress() as progress:
        task = progress.add_task("⬇️ Downloading files...", total=len(files))
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [
                executor.submit(download_one, service, f, output, export_map, normal_types)
                for f in files
            ]
            for future in as_completed(futures):
                result = future.result()
                progress.console.print(result)
                progress.update(task, advance=1)

    typer.echo("🎉 All downloads complete!")


if __name__ == "__main__":
    app()
