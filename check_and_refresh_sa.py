import datetime
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# ====== CONFIG ======
SERVICE_ACCOUNT_JSON = r"C:\Users\ratho\OneDrive\Documents\Projects\Crypto Tenchi\Cryptotenchi\social-media-automation-479601-c80a04db259e.json"
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
TIME_TOLERANCE_SECONDS = 300  # 5 minutes

# ====== STEP 1: Check system clock vs Google ======
try:
    response = requests.head("https://www.googleapis.com")
    google_time = response.headers.get("Date")
    if google_time:
        google_time = datetime.datetime.strptime(google_time, "%a, %d %b %Y %H:%M:%S %Z")
        local_time = datetime.datetime.utcnow()
        offset = (local_time - google_time).total_seconds()
        print(f"🕒 Local UTC:   {local_time}")
        print(f"🕒 Google UTC:  {google_time}")
        print(f"⏱️  Offset: {offset:.1f} seconds")

        if abs(offset) > TIME_TOLERANCE_SECONDS:
            raise Exception(f"⚠️ System clock off by more than 5 minutes. JWT will fail.")
    else:
        print("⚠️ Could not get time from Google.")
except Exception as e:
    print("⚠️ Error checking Google time:", e)

# ====== STEP 2: Load service account and refresh JWT ======
try:
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_JSON,
        scopes=SCOPES
    )
    creds.refresh(Request())
    print("✅ JWT token generated successfully!")
    print("Access token:", creds.token)
except Exception as e:
    print("❌ Failed to refresh JWT:", e)
