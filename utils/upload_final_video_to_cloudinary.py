import os
import time
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_to_cloudinary(file_path, max_retries=3, delay_seconds=30):
    """Upload a video to Cloudinary with retry logic."""
    if not file_path or not isinstance(file_path, (str, os.PathLike)):
        print(f"[❌ ERROR] Invalid file path provided: {file_path}")
        return None

    if not os.path.exists(file_path):
        print(f"[❌ ERROR] File not found at: {file_path}")
        return None

    attempt = 1
    while attempt <= max_retries:
        try:
            print(f"📤 Attempt {attempt} to upload {os.path.basename(file_path)} to Cloudinary...")

            response = cloudinary.uploader.upload_large(
                file_path,
                resource_type="video",
                chunk_size=60_000_000,                      # 60MB
                folder="Zynicon_social_media_automation",
                use_filename=True,
                unique_filename=False
            )

            url = response.get("secure_url")
            if url:
                print(f"[✅] Uploaded successfully to Cloudinary: {url}")
                return url
            else:
                raise Exception("Upload returned no URL")

        except Exception as e:
            print(f"[⚠️] Cloudinary upload attempt {attempt} failed: {e}")
            if attempt < max_retries:
                print(f"⏳ Retrying in {delay_seconds} seconds...")
                time.sleep(delay_seconds)
            attempt += 1

    print("[❌ ERROR] All Cloudinary upload attempts failed.")
    return None


def run_upload_to_cloudinary_pipeline(file_name):
    """Wrapper to trigger upload pipeline with validation."""
    if not file_name or not os.path.exists(file_name):
        print(f"[❌ ERROR] Watermarked video not found or invalid path: {file_name}")
        return None

    print(f"📤 Starting Cloudinary upload for: {file_name}")
    return upload_to_cloudinary(file_name)


# Example usage
if __name__ == "__main__":
    file_path = os.path.join("assets", "OG_video", "sample.mp4")
    run_upload_to_cloudinary_pipeline(file_path)
