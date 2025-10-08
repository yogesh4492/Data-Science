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
    """Authenticate and return Drive service object."""
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
    """Recursively list all files (including subfolders) inside a folder."""
    all_files = []
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()
    files = results.get("files", [])

    for f in files:
        # If it's a folder, recurse
        if f["mimeType"] == "application/vnd.google-apps.folder":
            all_files += list_all_files(service, f["id"])
        else:
            all_files.append(f)
    return all_files

@app.command()
def download(folder_id: str, output: str = typer.Argument("downloads")):
    """
    Download all PDF, DOC/DOCX, and ZIP files from your Google Drive folder (recursively).
    """
    service = get_drive_service()
    os.makedirs(output, exist_ok=True)

    file_types = {
        "application/pdf",
        "application/zip",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }

    typer.echo("🔍 Scanning folder, please wait...")
    files = list_all_files(service, folder_id)

    if not files:
        typer.echo("❌ No files found in this folder.")
        raise typer.Exit()

    typer.echo(f"📁 Found {len(files)} items. Filtering by allowed file types...")

    filtered = [f for f in files if f["mimeType"] in file_types]

    if not filtered:
        typer.echo("⚠️ No matching (.pdf/.zip/.doc/.docx) files found.")
        raise typer.Exit()

    with Progress() as progress:
        task = progress.add_task("⬇️ Downloading files...", total=len(filtered))
        for file in filtered:
            file_id = file["id"]
            file_name = file["name"]
            file_path = os.path.join(output, file_name)

            request = service.files().get_media(fileId=file_id)
            fh = io.FileIO(file_path, "wb")
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            fh.close()
            progress.console.print(f"✅ Downloaded: {file_name}")
            progress.update(task, advance=1)

    typer.echo("🎉 All matching files have been downloaded successfully!")

if __name__ == "__main__":
    app()
