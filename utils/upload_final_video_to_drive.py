import os
import mimetypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
UPLOAD_WATERMARKED_VIDEO_TO_DRIVE_ID = os.getenv("UPLOAD_WATERMARKED_VIDEO_TO_DRIVE_ID")


credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=credentials)

def upload_to_drive(file_path, folder_id):
    try:
        file_name = os.path.basename(file_path)
        mime_type = mimetypes.guess_type(file_path)[0]

        media = MediaFileUpload(file_path, mimetype=mime_type)

        file_metadata = {'name': file_name}
        if folder_id:
            file_metadata['parents'] = [folder_id]

        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        # Make the file public
        drive_service.permissions().create(
            fileId=uploaded_file['id'],
            body={'role': 'reader', 'type': 'anyone'}
        ).execute()

        file_url = f"https://drive.google.com/uc?export=download&id={uploaded_file['id']}"
        
        print(f"[✅] Uploaded and shared: {file_url}")
        return file_url

    except Exception as e:
        print("[❌ ERROR] Failed to upload:", str(e))
        return None


def run_upload_to_drive_pipeline(file_name):

    if not os.path.exists(file_name):
        print(f"[❌ ERROR] Watermarked video not found: {file_name}")
        return None

    print(f"📤 Uploading: {file_name}")
    return upload_to_drive(file_name, UPLOAD_WATERMARKED_VIDEO_TO_DRIVE_ID)

