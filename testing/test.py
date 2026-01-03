from dotenv import load_dotenv
import os

# Load secrets from .env
load_dotenv()

OG_DRIVE_FOLDER_ID = "1iKgjKHerpiRiMxYxIBSxPG-XpCGGvn_k"
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
VIDEO_FOLDER = "assets/OG_video"
os.makedirs(VIDEO_FOLDER, exist_ok=True)


print(f"🔐 Using credentials file: {SERVICE_ACCOUNT_FILE}")
print("📂 File exists?", os.path.exists(SERVICE_ACCOUNT_FILE))
print("📂 Full path:", os.path.abspath(SERVICE_ACCOUNT_FILE))
