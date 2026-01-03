import os
from dotenv import load_dotenv

from utils.connect_to_google_drive import run_download_pipeline
from utils.extract_text_from_thumbnail import run_thumbnail_ocr_pipeline
from utils.generate_content_from_LLM import run_caption_generation_pipeline, save_caption_to_file
from utils.upload_video_to_instagram import run_instagram_upload_pipeline
from utils.upload_video_to_youtube import run_youtube_upload_pipeline
from utils.generate_youtube_metadata import run_youtube_metadata_generation, save_youtube_metadata_to_file
from utils.google_sheets_tracker import update_links_in_sheet
from utils.watermark_detector_n_remover import OG_watermark_remover
from utils.extract_frame_from_video import extract_frame_from_WT_removed_video
from utils.overlay_and_replace_watermark import replace_watermark_with_custom_logo
from utils.upload_final_video_to_cloudinary import run_upload_to_cloudinary_pipeline


load_dotenv()

def main():
    
    # try:
    #     print("📥 STEP 1: Downloading video from Google Drive...")
    #     video_file, drive_file_id = run_download_pipeline()

    #     if not video_file:
    #         print("[✅] No new videos found.")
    #         return
    #     base_name = os.path.splitext(video_file)[0]
    # except Exception as e:
    #     print(f"[❌ STEP 1 FAILED] Could not download video/image: {e}")
    #     return
    

    try:
        print("\n🖼️ STEP 2: Removing watermark from OG video...")
        # donwloaded_video = os.path.join("assets", "OG_video", video_file)

        #---------------------------------------------------
        ### Manual Testing Part --> Add Video path below
        donwloaded_video = os.path.join("assets", "OG_video", "Video-701.mp4")
        #---------------------------------------------------

        print(f"donwloaded_video: {donwloaded_video}")
        WT_removed_video = OG_watermark_remover(donwloaded_video)
        print(f"WT removed video: {WT_removed_video}")
    except Exception as e:
        print(f"[❌ STEP 2 FAILED] Error in removing OG watermark: {e}")
        return
    

    try:
        print("\n📺 STEP 2.1: Extracting first frame from WT removed video...")
        image_file = extract_frame_from_WT_removed_video(WT_removed_video)
        print(f"WT removed video: {image_file}")
    except Exception as e:
        print(f"[❌ STEP 2.1 FAILED] Error in extracting 1st Frame: {e}")
        return


    try:
        print("\n🖼️ STEP 3: Extracting text from image...")
        thumbnail_text = run_thumbnail_ocr_pipeline(image_file)
    except Exception as e:
        print(f"[❌ STEP 3 FAILED] Could not extract text from image: {e}")
        return


    # try:
    #     print("\n✍️ STEP 4: Generating Instagram caption...")
    #     caption = run_caption_generation_pipeline(thumbnail_text) 
    #     save_caption_to_file(caption, video_file) 
    # except Exception as e:
    #     print(f"[❌ STEP 4 FAILED] Caption generation failed: {e}")
    #     return
    

    # try:
    #     print("\n📺 STEP 4.1: Generating YouTube Shorts metadata...")
    #     title, description, tags = run_youtube_metadata_generation(thumbnail_text)
    #     save_youtube_metadata_to_file(title, description, tags, video_file)
    # except Exception as e:
    #     print(f"[❌ STEP 4.1 FAILED] YouTube metadata generation failed: {e}")


    try:
        print("\n🎬 STEP 5: Adding Zynicon Watermark Logo...")
        custom_watermarked_video = replace_watermark_with_custom_logo(donwloaded_video)
    except Exception as e:
        print(f"[❌ STEP 5 FAILED] Failed to Add zynicon Logo: {e}")
        return

    # Uploading to Cloudinary instead of Google Drive
    try:
        print("\n☁️ STEP 6: Uploading final watermarked video to Cloudinary...")
        video_url = run_upload_to_cloudinary_pipeline(custom_watermarked_video)
        print(f"\nLocal Path: {custom_watermarked_video}\n\nVideo URL: {video_url}")
        
        if not video_url:
            raise Exception("Cloudinary URL is empty or upload failed.")
    except Exception as e:
        print(f"[❌ STEP 6 FAILED] Cloudinary upload failed: {e}")
        return


    # try:
    #     print("\n📤 STEP 7: Uploading to Instagram...")
    #     if video_url and caption:
    #         instagram_url = run_instagram_upload_pipeline(video_url, caption)
    #         if instagram_url:
    #             update_links_in_sheet(
    #                 video_name=video_file,
    #                 instagram_link=instagram_url)
    #     else:
    #         raise ValueError("Missing caption or video URL")
    # except Exception as e:
    #     print(f"[❌ STEP 7 FAILED] Instagram upload failed: {e}")
    #     return

    
    # try:
    #     print("\n🚀 STEP 9: Uploading to YouTube Shorts...")
    #     youtube_url = run_youtube_upload_pipeline(custom_watermarked_video, title, description, tags)
    #     if youtube_url:
    #         update_links_in_sheet(
    #             video_name=video_file,
    #             youtube_link=youtube_url)
    # except Exception as e:
    #     print(f"[❌ STEP 9 FAILED] YouTube upload failed: {e}")
    #     return
  

if __name__ == "__main__":
    main()
