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

@app.command()
def download_files(folder_id: str, output: str = typer.Argument("downloads")):
    """
    Download .zip, .pdf, .doc/.docx files (and export Google Docs) from a Google Drive folder.
    """
    service = get_drive_service()
    os.makedirs(output, exist_ok=True)

    # Allowed file MIME types
    direct_types = {
        "application/pdf",
        "application/zip",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword"
    }

    # Map Google Apps types to export formats
    export_map = {
        "application/vnd.google-apps.document": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.google-apps.spreadsheet": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.google-apps.presentation": "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    }

    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()
    files = results.get("files", [])

    if not files:
        typer.echo("❌ No files found in this folder.")
        raise typer.Exit()

    typer.echo(f"📁 Found {len(files)} files. Starting downloads...")

    with Progress() as progress:
        task = progress.add_task("⬇️ Downloading...", total=len(files))
        for file in files:
            file_id = file["id"]
            file_name = file["name"]
            mime_type = file["mimeType"]
            file_path = os.path.join(output, file_name)

            try:
                # Handle Google Docs/Sheets/Slides by exporting
                if mime_type in export_map:
                    export_mime = export_map[mime_type]
                    if not file_name.endswith(".docx") and "document" in mime_type:
                        file_name += ".docx"
                    elif not file_name.endswith(".xlsx") and "spreadsheet" in mime_type:
                        file_name += ".xlsx"
                    elif not file_name.endswith(".pptx") and "presentation" in mime_type:
                        file_name += ".pptx"
                    file_path = os.path.join(output, file_name)

                    request = service.files().export_media(fileId=file_id, mimeType=export_mime)
                    fh = io.FileIO(file_path, "wb")
                    downloader = MediaIoBaseDownload(fh, request)
                elif mime_type in direct_types:
                    request = service.files().get_media(fileId=file_id)
                    fh = io.FileIO(file_path, "wb")
                    downloader = MediaIoBaseDownload(fh, request)
                else:
                    progress.console.print(f"⚠️ Skipped unsupported file: {file_name}")
                    progress.update(task, advance=1)
                    continue

                done = False
                while not done:
                    status, done = downloader.next_chunk()
                fh.close()

                progress.console.print(f"✅ Downloaded: {file_name}")
            except Exception as e:
                progress.console.print(f"❌ Error downloading {file_name}: {e}")

            progress.update(task, advance=1)

    typer.echo("🎉 All downloads complete! Check your output folder.")

if __name__ == "__main__":
    app()
