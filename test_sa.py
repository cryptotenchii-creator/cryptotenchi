from google.oauth2 import service_account
from google.auth.transport.requests import Request

creds = service_account.Credentials.from_service_account_file(
    r"C:\CryptoTenchi\social-media-automation-479601-c80a04db259e.json",
    scopes=["https://www.googleapis.com/auth/drive.readonly"]
)

creds.refresh(Request())
print("✅ JWT token generated successfully")
