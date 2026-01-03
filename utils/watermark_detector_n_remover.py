import cv2
import os
from utils.detect_watermark import detect_watermark
from utils.remove_watermark_overlay import remove_with_background_overlay

# List of watermark templates (add more if needed)
OG_WATERMARKS = [
    "OG_watermark/watermark1.png",
]

OUTPUT_DIR = os.path.join("assets", "WT_removed_video")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def OG_watermark_remover(video_file):
    if not os.path.isfile(video_file):
        print(f"[✘] Video file not found: {video_file}")
        return None

    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"[✘] Failed to open video: {video_file}")
        return None

    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    # Output path
    video_filename = os.path.splitext(os.path.basename(video_file))[0]
    output_video_path = os.path.join(OUTPUT_DIR, f"{video_filename}_removed_watermark.mp4")

    out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width, height))

    # Read first frame to detect watermark position
    ret, frame = cap.read()
    if not ret:
        print("[✘] Failed to read video.")
        cap.release()
        out.release()
        return None

    best_bbox = None
    best_confidence = 0
    best_watermark_file = None

    # Try all watermark templates and keep the best match
    for watermark_path in OG_WATERMARKS:
        if not os.path.isfile(watermark_path):
            print(f"[⚠] Skipping missing watermark file: {watermark_path}")
            continue

        bbox, confidence = detect_watermark(frame, watermark_path)
        if bbox and confidence > best_confidence:
            best_bbox = bbox
            best_confidence = confidence
            best_watermark_file = watermark_path

    if not best_bbox:
        print("[✘] No watermark detected from given templates.")
        cap.release()
        out.release()
        return None

    print(f"[✔] Watermark detected using {best_watermark_file} at {best_bbox} (confidence: {best_confidence:.2f})")

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Rewind video

    # Remove watermark from all frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = remove_with_background_overlay(frame, best_bbox)
        out.write(frame)

    cap.release()
    out.release()
    print(f"[✅] Output video saved to: {output_video_path}")
    return output_video_path
