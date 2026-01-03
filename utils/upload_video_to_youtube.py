import os
import pickle
import glob
import subprocess
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Constants
CATEGORY_ID = "22"  # Entertainment
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRETS_FILE")
TOKEN_FILE = os.getenv("TOKEN_FILE")


# def fetch_authenticate_youtube():
#     """Authenticate and return the YouTube service."""
#     creds = None
#     if os.path.exists(TOKEN_FILE):
#         with open(TOKEN_FILE, 'rb') as token:
#             creds = pickle.load(token)

#     if not creds:
#         flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#             CLIENT_SECRETS_FILE, SCOPES)
#         creds = flow.run_local_server(port=0)
#         with open(TOKEN_FILE, 'wb') as token:
#             pickle.dump(creds, token)

#     youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)
#     return youtube

# Refresh token if expired
from google.auth.transport.requests import Request

def fetch_authenticate_youtube():
    """Authenticate and return the YouTube service with token refresh support."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # ✅ Automatically refresh token if expired
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    # 🟡 Only run flow if creds are invalid and cannot refresh
    if not creds or not creds.valid:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)
    return youtube


def run_youtube_upload_pipeline(video_file_path, title, description, tags_str):
    youtube = fetch_authenticate_youtube()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": [tag.strip() for tag in tags_str.split(",")],
            "categoryId": CATEGORY_ID
        },
        "status": {
            "privacyStatus": "public",  # Publish immediately
            "selfDeclaredMadeForKids": False,
            "madeForKids": False
        }
    }

    media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True, mimetype="video/*")

    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    try:
        print("📤 Uploading video to YouTube...")
        response = request.execute()
        yt_link = f"https://www.youtube.com/shorts/{response['id']}"
        print(f"[✅ Uploaded] {yt_link}")
        return yt_link
    except Exception as e:
        print(f"[❌ Upload failed] {e}")
        return None
