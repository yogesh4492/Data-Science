# gdrive_folder_zip_fast_retry.py
import os
import io
import zipfile
import pickle
import tempfile
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn

# Full Drive access
SCOPES = ['https://www.googleapis.com/auth/drive']

# Tunables (adjust if you hit rate limits)
MAX_WORKERS = 8        # reduce to 4 or 2 if you keep getting 403/429
MAX_RETRIES = 5
INITIAL_BACKOFF = 1.0  # seconds

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
    files = []
    page_token = None
    while True:
        resp = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces='drive',
            fields='nextPageToken, files(id, name, mimeType, size)',
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            pageToken=page_token
        ).execute()
        for f in resp.get('files', []):
            if f.get('mimeType') == 'application/vnd.google-apps.folder':
                files.extend(list_files(service, f['id']))
            else:
                files.append(f)
        page_token = resp.get('nextPageToken')
        if not page_token:
            break
    return files

def _safe_name(name: str) -> str:
    # sanitize names used inside the ZIP archive
    return name.replace(os.path.sep, "_")

def download_worker(file_meta, creds):
    """
    Download a single file to a temporary file and return a dict with result.
    Each worker builds its own Drive service (to avoid thread-safety issues).
    """
    file_id = file_meta['id']
    name = file_meta.get('name', file_id)
    mime = file_meta.get('mimeType', '')
    export_map = {
        'application/vnd.google-apps.document': 'application/pdf',
        'application/vnd.google-apps.spreadsheet': 'text/csv',
        'application/vnd.google-apps.presentation': 'application/pdf'
    }

    attempt = 0
    backoff = INITIAL_BACKOFF

    while attempt < MAX_RETRIES:
        try:
            # build a fresh service per thread
            service = build('drive', 'v3', credentials=creds, cache_discovery=False)
            if mime in export_map:
                request = service.files().export_media(fileId=file_id, mimeType=export_map[mime])
            else:
                request = service.files().get_media(fileId=file_id, supportsAllDrives=True)

            tmpf = tempfile.NamedTemporaryFile(delete=False)
            tmp_path = tmpf.name
            tmpf.close()

            with open(tmp_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
            return {'id': file_id, 'name': name, 'tmp_path': tmp_path, 'success': True, 'error': None}
        except HttpError as he:
            code = None
            try:
                code = int(he.resp.status)
            except Exception:
                pass
            # For throttling/rate-limit/server errors we retry
            if code in (403, 429) or (code is not None and 500 <= code < 600):
                attempt += 1
                time.sleep(backoff)
                backoff *= 2
                continue
            else:
                return {'id': file_id, 'name': name, 'tmp_path': None, 'success': False, 'error': f'HttpError {he}'}
        except Exception as e:
            attempt += 1
            if attempt >= MAX_RETRIES:
                tb = traceback.format_exc()
                return {'id': file_id, 'name': name, 'tmp_path': None, 'success': False, 'error': f'{e}\\n{tb}'}
            time.sleep(backoff)
            backoff *= 2
    return {'id': file_id, 'name': name, 'tmp_path': None, 'success': False, 'error': 'max retries exceeded'}

def download_and_zip_folder(folder_id, zip_name='drive_folder.zip', max_workers=MAX_WORKERS):
    creds = authenticate()
    # single short-lived service for listing; workers will build their own
    service = build('drive', 'v3', credentials=creds, cache_discovery=False)

    print("[+] Listing files (this may take a while for large folders)...")
    all_files = list_files(service, folder_id)
    total_files = len(all_files)
    print(f"[+] Found {total_files} files to download. Using {max_workers} workers.\\n")

    if total_files == 0:
        print("[-] No files found - exiting.")
        return

    temp_results = []
    failed = []

    # Download in parallel; write to ZIP in the main thread to avoid concurrency on the zip file.
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TimeRemainingColumn()) as progress:
        task = progress.add_task("Downloading...", total=total_files)
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(download_worker, f, creds): f for f in all_files}
            for fut in as_completed(futures):
                res = fut.result()
                if res.get('success'):
                    temp_results.append(res)
                else:
                    failed.append(res)
                    print(f"[!] Failed: {res.get('name')} -> {res.get('error')}")
                progress.advance(task)

    # Write downloaded temp files to ZIP (sequentially)
    seen = {}
    with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for item in temp_results:
            tmp_path = item['tmp_path']
            orig_name = _safe_name(item['name'])
            base = orig_name
            count = seen.get(base, 0)
            if count > 0:
                name_root, ext = os.path.splitext(base)
                arcname = f"{name_root}_{count}{ext}"
            else:
                arcname = base
            seen[base] = count + 1
            try:
                zf.write(tmp_path, arcname=arcname)
            except Exception as e:
                print(f"[!] Error writing {tmp_path} to zip: {e}")
                failed.append({'id': item['id'], 'name': item['name'], 'error': str(e)})
            finally:
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    print(f"✅ Done. ZIP created: {zip_name}")
    if failed:
        print(f"[!] {len(failed)} files failed to download or write. See details above.")

if __name__ == '__main__':
    folder_id = input("Enter Google Drive Folder ID: ").strip()
    zip_name = input("Output zip filename (default drive_folder.zip): ").strip() or "drive_folder.zip"
    workers_inp = input(f"Max workers (default {MAX_WORKERS}): ").strip()
    try:
        workers = int(workers_inp) if workers_inp else MAX_WORKERS
    except:
        workers = MAX_WORKERS

    download_and_zip_folder(folder_id, zip_name, max_workers=workers)
