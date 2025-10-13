# gdrive_videos_to_wav.py

import os
import io
import time
import tempfile
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import typer
from rich.progress import Progress
from moviepy import VideoFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

app = typer.Typer()

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_drive():
    """Authenticate and return a Google Drive service instance."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def list_videos(service, folder_id):
    """List all video files in a given Google Drive folder."""
    query = f"'{folder_id}' in parents and mimeType contains 'video/'"
    results = []
    page_token = None

    while True:
        response = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token
        ).execute()
        results.extend(response.get('files', []))
        page_token = response.get('nextPageToken')
        if not page_token:
            break
    return results

def download_file(service, file_id, filename, output_dir):
    """Download a single file from Google Drive."""
    request = service.files().get_media(fileId=file_id)
    file_path = os.path.join(output_dir, filename)
    with io.FileIO(file_path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
    return file_path

def convert_to_wav(video_path, output_dir):
    """Convert video to WAV using moviepy."""
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    wav_path = os.path.join(output_dir, f"{base_name}.wav")
    try:
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(wav_path, codec='pcm_s16le')
        clip.close()
    except Exception as e:
        print(f"[ERROR] {video_path}: {e}")
    return wav_path

@app.command()
def main(folder_id: str, output: str = "output_wav", max_workers: int = 4):
    """
    Download all videos from a Google Drive folder (using folder ID)
    and convert them to WAV files.
    """
    os.makedirs(output, exist_ok=True)
    temp_dir = tempfile.mkdtemp()

    typer.echo(f"🔐 Authenticating Google Drive...")
    service = authenticate_drive()

    typer.echo(f"📂 Listing videos in folder: {folder_id}")
    videos = list_videos(service, folder_id)
    typer.echo(f"🎞️ Found {len(videos)} videos")

    if not videos:
        typer.echo("No videos found in this folder.")
        return

    with Progress() as progress:
        task = progress.add_task("[cyan]Downloading and converting videos...", total=len(videos))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for v in videos:
                futures.append(executor.submit(process_video, service, v, temp_dir, output, progress, task))

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    typer.echo(f"Error: {e}")

    typer.echo(f"✅ Conversion complete. WAV files saved in: {output}")

def process_video(service, file, temp_dir, output_dir, progress, task):
    """Download and convert a single video."""
    try:
        file_path = download_file(service, file['id'], file['name'], temp_dir)
        convert_to_wav(file_path, output_dir)
    except Exception as e:
        print(f"Error processing {file['name']}: {e}")
    finally:
        progress.update(task, advance=1)

if __name__ == "__main__":
    app()
