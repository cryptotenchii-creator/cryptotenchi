import os
from datetime import datetime, timedelta, timezone
import cloudinary
import cloudinary.api
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

# Setup Cloudinary config
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def delete_old_videos(folder="Zynicon_social_media_automation"):
    now = datetime.now(timezone.utc)
    cutoff_date = now - timedelta(days=14)

    print(f"🔍 Scanning Cloudinary folder '{folder}' for videos older than {cutoff_date.isoformat()}...")

    next_cursor = None
    deleted_count = 0

    while True:
        response = cloudinary.api.resources(
            type="upload",
            resource_type="video",
            prefix=folder,
            max_results=100,
            next_cursor=next_cursor
        )

        for item in response.get("resources", []):
            created_at = datetime.strptime(item["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            if created_at < cutoff_date:
                cloudinary.api.delete_resources([item["public_id"]], resource_type="video")
                print(f"[🗑️] Deleted: {item['public_id']} (Uploaded: {created_at.isoformat()})")
                deleted_count += 1

        next_cursor = response.get("next_cursor")
        if not next_cursor:
            break

    print(f"✅ Cleanup complete. Total deleted: {deleted_count}")

if __name__ == "__main__":
    delete_old_videos()
