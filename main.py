# import os
# from dotenv import load_dotenv

# from utils.connect_to_google_drive import run_download_pipeline
# from utils.extract_text_from_thumbnail import run_thumbnail_ocr_pipeline
# from utils.generate_content_from_LLM import run_caption_generation_pipeline, save_caption_to_file
# from utils.upload_video_to_instagram import run_instagram_upload_pipeline
# from utils.upload_video_to_youtube import run_youtube_upload_pipeline
# from utils.generate_youtube_metadata import run_youtube_metadata_generation, save_youtube_metadata_to_file
# from utils.google_sheets_tracker import update_links_in_sheet
# from utils.watermark_detector_n_remover import OG_watermark_remover
# from utils.extract_frame_from_video import extract_frame_from_WT_removed_video
# from utils.overlay_and_replace_watermark import replace_watermark_with_custom_logo
# from utils.upload_final_video_to_cloudinary import run_upload_to_cloudinary_pipeline



# load_dotenv()


# def process_video(video_file, drive_file_id):
#     """
#     Process a single video: remove watermark, extract text, generate caption,
#     add Zynicon logo, upload to Cloudinary + Instagram + YouTube.
#     Returns True if successful, False if skipped or failed.
#     """
#     try:
#         base_name = os.path.splitext(video_file)[0]
#         donwloaded_video = os.path.join("assets", "OG_video", video_file)
#         print(f"\n🖼️ STEP 2: Removing watermark from OG video: {donwloaded_video}")
#         WT_removed_video = OG_watermark_remover(donwloaded_video)

#         if not WT_removed_video:
#             print("[⚠️] Watermark not found — skipping this video.")
#             return False

#     except Exception as e:
#         print(f"[❌ STEP 2 FAILED] Error in removing OG watermark: {e}")
#         return False

#     try:
#         print("\n📺 STEP 2.1: Extracting first frame from WT removed video...")
#         image_file = extract_frame_from_WT_removed_video(WT_removed_video)
#     except Exception as e:
#         print(f"[❌ STEP 2.1 FAILED] Error in extracting 1st Frame: {e}")
#         return False

#     try:
#         print("\n🖼️ STEP 3: Extracting text from image...")
#         thumbnail_text = run_thumbnail_ocr_pipeline(image_file)
#     except Exception as e:
#         print(f"[❌ STEP 3 FAILED] Could not extract text from image: {e}")
#         thumbnail_text = ""

#     try:
#         print("\n✍️ STEP 4: Generating Instagram caption...")
#         caption = run_caption_generation_pipeline(thumbnail_text)
#         save_caption_to_file(caption, video_file)
#     except Exception as e:
#         print(f"[❌ STEP 4 FAILED] Caption generation failed: {e}")
#         return False

#     try:
#         print("\n📺 STEP 4.1: Generating YouTube Shorts metadata...")
#         title, description, tags = run_youtube_metadata_generation(thumbnail_text)
#         save_youtube_metadata_to_file(title, description, tags, video_file)
#     except Exception as e:
#         print(f"[❌ STEP 4.1 FAILED] YouTube metadata generation failed: {e}")
#         title, description, tags = "", "", ""

#     try:
#         print("\n🎬 STEP 5: Adding Zynicon Watermark Logo...")
#         custom_watermarked_video = replace_watermark_with_custom_logo(donwloaded_video)

#         if not custom_watermarked_video or custom_watermarked_video == donwloaded_video:
#             print("[⚠️] No watermark detected — skipping this video.")
#             return False

#         print(f"[✅] Custom watermarked video ready: {custom_watermarked_video}")
#     except Exception as e:
#         print(f"[❌ STEP 5 FAILED] Failed to Add zynicon Logo: {e}")
#         return False

#     try:
#         print("\n☁️ STEP 6: Uploading final watermarked video to Cloudinary...")
#         video_url = run_upload_to_cloudinary_pipeline(custom_watermarked_video)
#         if not video_url:
#             raise Exception("Cloudinary upload failed.")
#         print(f"[✅] Cloudinary URL: {video_url}")
#     except Exception as e:
#         print(f"[❌ STEP 6 FAILED] Cloudinary upload failed: {e}")
#         return False

#     try:
#         print("\n📤 STEP 7: Uploading to Instagram...")
#         instagram_url = run_instagram_upload_pipeline(video_url, caption)
#         if instagram_url:
#             update_links_in_sheet(video_name=video_file, instagram_link=instagram_url)
#             print(f"[✅] Instagram upload done: {instagram_url}")
#         else:
#             print("[⚠️] Instagram upload skipped (no URL).")
#     except Exception as e:
#         print(f"[❌ STEP 7 FAILED] Instagram upload failed: {e}")

#     try:
#         print("\n🚀 STEP 9: Uploading to YouTube Shorts...")
#         youtube_url = run_youtube_upload_pipeline(custom_watermarked_video, title, description, tags)
#         if youtube_url:
#             update_links_in_sheet(video_name=video_file, youtube_link=youtube_url)
#             print(f"[✅] YouTube upload done: {youtube_url}")
#     except Exception as e:
#         print(f"[❌ STEP 9 FAILED] YouTube upload failed: {e}")

#     return True


# def main():
#     """
#     Continuously fetch and process videos one by one.
#     If a video doesn't contain a watermark, skip it and continue with the next.
#     """
#     while True:
#         print("\n📥 STEP 1: Fetching next video from Google Drive...")
#         try:
#             video_file, drive_file_id = run_download_pipeline()
#             if not video_file:
#                 print("[✅] No new videos available. Waiting for the next scheduled upload...")
#                 break
#         except Exception as e:
#             print(f"[❌ STEP 1 FAILED] Could not fetch video: {e}")
#             break

#         success = process_video(video_file, drive_file_id)
#         if not success:
#             print("\n⏭️ Skipping this video — moving to the next available one.\n")
#             continue  # Loop again to fetch the next video

#         print("\n✅ Finished processing and uploading successfully!")
#         break  # Stop after successful upload (or remove this break if you want continuous uploads)


# if __name__ == "__main__":
#     main()


# # https://www.instagram.com/reel/DQo8IttjGhV/?utm_source=ig_web_copy_link&igsh=bzhzdGEyaHlwNnQ0 ---> last video
# # https://www.instagram.com/reel/C8zYfi2SHHj/ ----> First video


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


def process_video(video_file, drive_file_id):
    """
    Process a single video:
    - Extract thumbnail text
    - Generate caption & metadata
    - Upload original video to Instagram & YouTube
    """
    try:
        downloaded_video = os.path.join("assets", "OG_video", video_file)

        print("\n📺 STEP 2: Extracting first frame from video...")
        image_file = extract_frame_from_WT_removed_video(downloaded_video)
    except Exception as e:
        print(f"[❌ STEP 2 FAILED] Frame extraction error: {e}")
        return False

    try:
        print("\n🖼️ STEP 3: Extracting text from thumbnail...")
        thumbnail_text = run_thumbnail_ocr_pipeline(image_file)
    except Exception as e:
        print(f"[⚠️ STEP 3 WARNING] OCR failed: {e}")
        thumbnail_text = ""

    try:
        print("\n✍️ STEP 4: Generating Instagram caption...")
        caption = run_caption_generation_pipeline(thumbnail_text)
        save_caption_to_file(caption, video_file)
    except Exception as e:
        print(f"[❌ STEP 4 FAILED] Caption generation error: {e}")
        return False

    try:
        print("\n📺 STEP 5: Generating YouTube metadata...")
        title, description, tags = run_youtube_metadata_generation(thumbnail_text)
        save_youtube_metadata_to_file(title, description, tags, video_file)
    except Exception as e:
        print(f"[⚠️ STEP 5 WARNING] YouTube metadata failed: {e}")
        title, description, tags = "", "", ""

    try:
        print("\n☁️ STEP 6: Uploading video to Cloudinary...")
        video_url = run_upload_to_cloudinary_pipeline(downloaded_video)
        if not video_url:
            raise Exception("Cloudinary upload failed")
        print(f"[✅] Cloudinary URL: {video_url}")
    except Exception as e:
        print(f"[❌ STEP 6 FAILED] {e}")
        return False

    try:
        print("\n📤 STEP 7: Uploading to Instagram...")
        instagram_url = run_instagram_upload_pipeline(video_url, caption)
        if instagram_url:
            update_links_in_sheet(video_name=video_file, instagram_link=instagram_url)
            print(f"[✅] Instagram uploaded: {instagram_url}")
    except Exception as e:
        print(f"[❌ STEP 7 FAILED] Instagram upload error: {e}")

    try:
        print("\n🚀 STEP 8: Uploading to YouTube Shorts...")
        youtube_url = run_youtube_upload_pipeline(
            downloaded_video, title, description, tags
        )
        if youtube_url:
            update_links_in_sheet(video_name=video_file, youtube_link=youtube_url)
            print(f"[✅] YouTube uploaded: {youtube_url}")
    except Exception as e:
        print(f"[❌ STEP 8 FAILED] YouTube upload error: {e}")

    return True


def main():
    """
    Fetch and upload videos one by one without watermark modification.
    """
    while True:
        print("\n📥 STEP 1: Fetching next video from Google Drive...")
        try:
            video_file, drive_file_id = run_download_pipeline()
            if not video_file:
                print("[✅] No new videos available.")
                break
        except Exception as e:
            print(f"[❌ STEP 1 FAILED] {e}")
            break

        success = process_video(video_file, drive_file_id)
        if not success:
            print("\n⏭️ Skipping this video...\n")
            continue

        print("\n✅ Video processed & uploaded successfully!")
        break


if __name__ == "__main__":
    main()

# .