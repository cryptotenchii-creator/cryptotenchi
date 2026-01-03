import cv2
import os

def extract_frame_from_WT_removed_video(video_path):

    THUMBNAIL_DIR = os.path.join("assets", "clean_video_thumbnail")
    os.makedirs(THUMBNAIL_DIR, exist_ok=True)

    # Load the video
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()

    if not ret:
        print("[✘] Could not read the first frame.")
        cap.release()
        return None

    # Build output image path
    video_filename = os.path.splitext(os.path.basename(video_path))[0]
    thumbnail_path = os.path.join(THUMBNAIL_DIR, f"{video_filename}_thumbnail.jpg")

    # Save the frame as image
    cv2.imwrite(thumbnail_path, frame)
    cap.release()

    print(f"[✅] First frame saved as thumbnail: {thumbnail_path}")
    return thumbnail_path
