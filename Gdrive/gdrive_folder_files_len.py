# from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# scope=['https://www.googleapis.com/auth/drive']
# flow=InstalledAppFlow.from_client_secrets_file('credentials.json',scope)
# cred=flow.run_local_server(port=0)

# service = build('drive', 'v3', credentials=cred)

# folder_id="15Vv-HwqAO7ty61Scs-hgv-t4gN9ev0mo"

# # List all files inside the folder
# results = service.files().list(
#     q=f"'{folder_id}' in parents and trashed=false",
#     fields="files(id, name)"
# ).execute()

# files = results.get('files', [])
# print(f"Total files: {len(files)}")

# for f in files:
#     print(f"{f['name']} ({f['id']})")


from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import csv

# 1️⃣ Authentication
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('drive', 'v3', credentials=creds)

# 2️⃣ Your Folder ID
folder_id = "1XxMoo2sNnKlAOkJrVRndSf9-W9KBxc4i"

# 3️⃣ Pagination Loop
all_files = []
page_token = None

print("Fetching files... please wait...")

while True:
    response = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="nextPageToken, files(id, name, mimeType, size)",
        pageSize=1000,  # max per page
        pageToken=page_token
    ).execute()
    
    all_files.extend(response.get('files', []))
    page_token = response.get('nextPageToken', None)
    
    if not page_token:
        break  # no more pages

# 4️⃣ Display Summary
print(f"\n✅ Total files found: {len(all_files)}")

# Calculate total size (optional)
total_size = sum(int(f.get('size', 0)) for f in all_files if 'size' in f)
print(f"📦 Total size: {total_size / (1024 * 1024):.2f} MB")

# 5️⃣ Save results to CSV (optional)
with open("drive_folder.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "ID", "MIME Type", "Size (bytes)"])
    for f in all_files:
        writer.writerow([
            f.get("name", ""),
            f.get("id", ""),
            f.get("mimeType", ""),
            f.get("size", "")
        ])

print("\n💾 File list saved as: drive_folder_files.csv")
