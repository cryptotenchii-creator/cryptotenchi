import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
OG_DRIVE_FOLDER_ID = os.getenv("OG_DRIVE_FOLDER_ID")

VIDEO_FOLDER = "assets/OG_video"
os.makedirs(VIDEO_FOLDER, exist_ok=True)

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

drive_service = build("drive", "v3", credentials=credentials)


def run_download_pipeline():
    print("✅ Google Drive auth SUCCESS")

    query = f"'{OG_DRIVE_FOLDER_ID}' in parents and trashed=false"
    results = drive_service.files().list(
        q=query,
        fields="files(id, name)",
        pageSize=1
    ).execute()

    files = results.get("files", [])
    if not files:
        print("[✅] No new videos available.")
        return None, None

    file = files[0]
    file_id = file["id"]
    file_name = file["name"]

    if not file_name.lower().endswith((".mp4", ".mov", ".mkv")):
        print("[⚠️] Skipping non-video file:", file_name)
        return None, None

    local_path = os.path.join(VIDEO_FOLDER, file_name)

    print(f"📥 Downloading: {file_name}")

    request = drive_service.files().get_media(fileId=file_id)
    with open(local_path, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

    print(f"[✅] Downloaded to: {local_path}")

    return file_name, file_id
