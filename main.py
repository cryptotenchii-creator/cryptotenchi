import os
from dotenv import load_dotenv

from utils.connect_to_google_drive import run_download_pipeline
from utils.extract_text_from_thumbnail import run_thumbnail_ocr_pipeline
from utils.generate_content_from_LLM import (
    run_caption_generation_pipeline,
    save_caption_to_file
)
from utils.generate_youtube_metadata import (
    run_youtube_metadata_generation,
    save_youtube_metadata_to_file
)
from utils.upload_video_to_instagram import run_instagram_upload_pipeline
from utils.upload_video_to_youtube import run_youtube_upload_pipeline
from utils.google_sheets_tracker import update_links_in_sheet
from utils.extract_frame_from_video import extract_frame_from_WT_removed_video
from utils.upload_final_video_to_cloudinary import run_upload_to_cloudinary_pipeline

load_dotenv()


def get_actual_video_path(video_file):
    """
    Handles case where Google Drive download gives a folder instead of a file
    """
    base_path = os.path.join("assets", "OG_video", video_file)

    # If it's already a file → return
    if os.path.isfile(base_path):
        return base_path

    # If it's a folder → find first mp4 inside
    if os.path.isdir(base_path):
        for file in os.listdir(base_path):
            if file.lower().endswith((".mp4", ".mov", ".mkv")):
                return os.path.join(base_path, file)

    return None


def process_video(video_file, drive_file_id):
    try:
        downloaded_video = get_actual_video_path(video_file)

        if not downloaded_video:
            print("[❌] No valid video file found.")
            return False

        print(f"[✅] Using video file: {downloaded_video}")

        print("\n📺 STEP 2: Extracting first frame...")
        image_file = extract_frame_from_WT_removed_video(downloaded_video)

        if image_file is None:
            print("[⚠️] Frame extraction failed. Continuing without OCR.")
            thumbnail_text = ""
        else:
            print("\n🖼️ STEP 3: Extracting text from thumbnail...")
            try:
                thumbnail_text = run_thumbnail_ocr_pipeline(image_file)
            except Exception:
                thumbnail_text = ""

        print("\n✍️ STEP 4: Generating Instagram caption...")
        caption = run_caption_generation_pipeline(thumbnail_text)
        save_caption_to_file(caption, video_file)

        print("\n📺 STEP 5: Generating YouTube metadata...")
        try:
            title, description, tags = run_youtube_metadata_generation(thumbnail_text)
            save_youtube_metadata_to_file(title, description, tags, video_file)
        except Exception:
            title, description, tags = "", "", ""

        print("\n☁️ STEP 6: Uploading video to Cloudinary...")
        video_url = run_upload_to_cloudinary_pipeline(downloaded_video)

        if not video_url:
            print("[❌] Cloudinary upload failed.")
            return False

        print(f"[✅] Cloudinary URL: {video_url}")

        print("\n📤 STEP 7: Uploading to Instagram...")
        try:
            instagram_url = run_instagram_upload_pipeline(video_url, caption)
            if instagram_url:
                update_links_in_sheet(video_name=video_file, instagram_link=instagram_url)
        except Exception as e:
            print("Instagram upload error:", e)

        print("\n🚀 STEP 8: Uploading to YouTube Shorts...")
        try:
            youtube_url = run_youtube_upload_pipeline(
                downloaded_video, title, description, tags
            )
            if youtube_url:
                update_links_in_sheet(video_name=video_file, youtube_link=youtube_url)
        except Exception as e:
            print("YouTube upload error:", e)

        return True

    except Exception as e:
        print("[❌] Unexpected error:", e)
        return False


def main():
    while True:
        print("\n📥 STEP 1: Fetching next video from Google Drive...")

        video_file, drive_file_id = run_download_pipeline()

        if not video_file:
            print("[✅] No new videos available.")
            break

        success = process_video(video_file, drive_file_id)

        if not success:
            print("\n⏭️ Skipping this video...\n")
            continue

        print("\n✅ Video processed & uploaded successfully!")
        break


if __name__ == "__main__":
    main()
