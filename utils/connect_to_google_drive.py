import os
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from utils.google_sheets_tracker import get_logged_videos, append_row, get_reminder_date, update_reminder_date
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from datetime import datetime as dt

load_dotenv()

# OG_DRIVE_FOLDER_ID = "1iKgjKHerpiRiMxYxIBSxPG-XpCGGvn_k"
OG_DRIVE_FOLDER_ID = os.getenv("OG_DRIVE_FOLDER_ID")
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
VIDEO_FOLDER = "assets/OG_video"
os.makedirs(VIDEO_FOLDER, exist_ok=True)

# Email configuration
GMAIL_USER = os.getenv("GMAIL_USER")  # your Gmail
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
REMINDER_THRESHOLD = 20
REMINDER_COOLDOWN_DAYS = 7


def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)

# def list_drive_files():
#     service = get_drive_service()
#     query = f"'{OG_DRIVE_FOLDER_ID}' in parents and trashed = false"
#     response = service.files().list(q=query, fields="files(id, name)").execute()
#     return response.get("files", [])

# def search_drive_file(service, name):
#     query = f"name = '{name}' and '{OG_DRIVE_FOLDER_ID}' in parents and trashed = false"
#     result = service.files().list(q=query, fields="files(id, name)", pageSize=1).execute()
#     return result.get("files", [None])[0]


# This function lists all files in the specified Google Drive folder.
# It handles pagination to ensure all files are retrieved.
def list_drive_files():
    service = get_drive_service()
    query = f"'{OG_DRIVE_FOLDER_ID}' in parents and trashed = false"

    all_files = []
    page_token = None

    while True:
        response = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name)",
            pageSize=1000,
            pageToken=page_token
        ).execute()
        all_files.extend(response.get("files", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return all_files

# This function searches for a specific file by name in the Google Drive folder.
# It returns the first match found or None if no match is found.
def search_drive_file(service, name):
    query = f"name = '{name}' and '{OG_DRIVE_FOLDER_ID}' in parents and trashed = false"
    page_token = None

    while True:
        result = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name)",
            pageSize=100,
            pageToken=page_token
        ).execute()

        files = result.get("files", [])
        if files:
            return files[0]  # return first match

        page_token = result.get("nextPageToken")
        if not page_token:
            break

    return None


def send_reminder_email(remaining_count):
    try:
        subject = "Video Processing Reminder"
        body = f"You have {remaining_count} unprocessed videos remaining. Please upload new videos soon."

        msg = MIMEText(body)
        msg["From"] = GMAIL_USER
        msg["To"] = GMAIL_USER
        msg["Subject"] = subject

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, APP_PASSWORD)
            server.send_message(msg)
        
        print(f"[📧] Reminder email sent successfully for {remaining_count} remaining videos.")
    except Exception as e:
        print(f"[❌] Failed to send reminder email: {e}")

def check_and_send_reminder():
    """
    Check if remaining videos ≤ threshold and last reminder sent > cooldown,
    then send email and update Google Sheet.
    """
    logged_videos = get_logged_videos()
    all_files = list_drive_files()
    total_videos = len([f for f in all_files if f["name"].endswith(".mp4")])
    processed_count = len(logged_videos)
    remaining_count = total_videos - processed_count

    if remaining_count <= REMINDER_THRESHOLD:
        last_sent = get_reminder_date("Video Reminder")  # assume single row/key in sheet
        send_email = True
        if last_sent:
            last_sent_dt = dt.fromisoformat(last_sent)
            delta = dt.now() - last_sent_dt
            if delta.days < REMINDER_COOLDOWN_DAYS:
                send_email = False  # already sent recently
        if send_email:
            send_reminder_email(remaining_count)
            update_reminder_date("Video Reminder", dt.now().isoformat())



def download_file(service, file_name, dest_folder):
    file = search_drive_file(service, file_name)
    if not file:
        print(f"[❌ ERROR] File not found in Drive: {file_name}")
        return False

    file_id = file["id"]
    print(f"🔗 Drive URL: https://drive.google.com/file/d/{file_id}/view\n")

    path = os.path.join(dest_folder, file_name)
    request = service.files().get_media(fileId=file_id)

    with open(path, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

    print(f"[✅] Downloaded: {file_name}")
    return file_name, file_id

def run_download_pipeline():
    service = get_drive_service()
    all_files = list_drive_files()

    # Group files
    video_files = {f["name"]: f for f in all_files if f["name"].endswith(".mp4") and "_watermarked" not in f["name"]}
    already_logged = get_logged_videos()

    for video_name in video_files:
        if video_name in already_logged:
            continue

        base = os.path.splitext(video_name)[0]
        print(f"[📥] Attempting to download: {video_name}")

        res = download_file(service, video_name, VIDEO_FOLDER)
        if not res:
            append_row(video_name, "skipped")
            continue

        video_name, file_id = res
        append_row(video_name, "downloaded")
        # check_and_send_reminder()
        return video_name, file_id  # 🔁 Only process one per run

    print("[✅] All videos in Drive have already been processed.")
    return None, None
