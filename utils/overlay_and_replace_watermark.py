# import cv2
# import os
# import numpy as np
# from moviepy.editor import VideoFileClip
# from utils.detect_watermark import detect_watermark
# from utils.remove_watermark_overlay import remove_with_background_overlay

# # Multiple watermark templates
# OG_WATERMARKS = [
#     "OG_watermark/watermark1.png",
# ]

# MY_WATERMARK_IMAGE = "zynicon_logo/Zynicon_social_watermark_logo.png"
# OUTPUT_DIR = os.path.join("assets", "WT_zynicon_video")
# os.makedirs(OUTPUT_DIR, exist_ok=True)


# def add_original_audio(original_video, processed_video):
#     try:
#         original_clip = VideoFileClip(original_video)
#         processed_clip = VideoFileClip(processed_video)

#         final = processed_clip.set_audio(original_clip.audio)
#         final_output_path = processed_video.replace(".mp4", "_with_audio.mp4")
#         final.write_videofile(final_output_path, codec="libx264", audio_codec="aac")

#         print(f"[✅] Audio reattached: {final_output_path}")
#         return final_output_path
#     except Exception as e:
#         print(f"[❌ ERROR] Failed to reattach audio: {e}")
#         return processed_video


# # def replace_watermark_with_custom_logo(video_file):
# #     if not os.path.isfile(video_file):
# #         print(f"[✘] File not found: {video_file}")
# #         return None

# #     cap = cv2.VideoCapture(video_file)
# #     if not cap.isOpened():
# #         print(f"[✘] Failed to open video: {video_file}")
# #         return None

# #     fps = cap.get(cv2.CAP_PROP_FPS)
# #     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# #     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# #     fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# #     video_filename = os.path.splitext(os.path.basename(video_file))[0]
# #     output_path = os.path.join(OUTPUT_DIR, f"{video_filename}_watermarked.mp4")
# #     out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# #     # Read first frame to detect watermark
# #     ret, first_frame = cap.read()
# #     if not ret:
# #         print("[✘] Could not read first frame.")
# #         cap.release()
# #         return None

# #     # Try detecting from multiple watermark templates
# #     best_bbox = None
# #     best_confidence = 0.0
# #     matched_template = None

# #     for wm_path in OG_WATERMARKS:
# #         bbox, confidence = detect_watermark(first_frame, wm_path)
# #         if bbox and confidence > best_confidence:
# #             best_bbox = bbox
# #             best_confidence = confidence
# #             matched_template = wm_path

# #     if not best_bbox:
# #         print("[✘] No watermark detected from given templates.")
# #         cap.release()
# #         return None

# #     print(f"[✔] Watermark found ({matched_template}) at {best_bbox} (confidence: {best_confidence:.2f})")
# #     cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # rewind

# #     # Load replacement logo
# #     logo = cv2.imread(MY_WATERMARK_IMAGE, cv2.IMREAD_UNCHANGED)
# #     if logo is None:
# #         print(f"[✘] Could not load watermark logo image: {MY_WATERMARK_IMAGE}")
# #         return None

# #     # Placement calculation
# #     top_left, bottom_right = best_bbox
# #     x1, y1 = top_left
# #     x2, y2 = bottom_right
# #     box_w = x2 - x1
# #     box_h = y2 - y1

# #     scale_factor = 0.85
# #     new_w = int(box_w * scale_factor)
# #     new_h = int(box_h * scale_factor)
# #     resized_logo = cv2.resize(logo, (new_w, new_h))

# #     new_x1 = x1 + int((box_w - new_w) * 1.5)
# #     new_y1 = y1 + int((box_h - new_h) / 2)
# #     new_x2 = new_x1 + new_w
# #     new_y2 = new_y1 + new_h

# #     # Process all frames
# #     while True:
# #         ret, frame = cap.read()
# #         if not ret:
# #             break

# #         clean_frame = remove_with_background_overlay(frame.copy(), best_bbox)

# #         overlay = resized_logo.copy()
# #         if overlay.shape[2] == 4:
# #             alpha = overlay[:, :, 3] / 255.0
# #             for c in range(3):
# #                 clean_frame[new_y1:new_y2, new_x1:new_x2, c] = (
# #                     alpha * overlay[:, :, c] +
# #                     (1 - alpha) * clean_frame[new_y1:new_y2, new_x1:new_x2, c]
# #                 )
# #         else:
# #             clean_frame[new_y1:new_y2, new_x1:new_x2] = overlay

# #         out.write(clean_frame)

# #     cap.release()
# #     out.release()

# #     print(f"[✅] Final watermarked video saved at: {output_path}")

# #     return add_original_audio(video_file, output_path)
# def replace_watermark_with_custom_logo(video_file):
#     if not os.path.isfile(video_file):
#         print(f"[✘] File not found: {video_file}")
#         return None

#     cap = cv2.VideoCapture(video_file)
#     if not cap.isOpened():
#         print(f"[✘] Failed to open video: {video_file}")
#         return None

#     fps = cap.get(cv2.CAP_PROP_FPS)
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fourcc = cv2.VideoWriter_fourcc(*"mp4v")

#     video_filename = os.path.splitext(os.path.basename(video_file))[0]
#     output_path = os.path.join(OUTPUT_DIR, f"{video_filename}_watermarked.mp4")
#     out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

#     # Read first frame to detect watermark
#     ret, first_frame = cap.read()
#     if not ret:
#         print("[✘] Could not read first frame.")
#         cap.release()
#         return None

#     # Try detecting from multiple watermark templates
#     best_bbox = None
#     best_confidence = 0.0
#     matched_template = None

#     for wm_path in OG_WATERMARKS:
#         bbox, confidence = detect_watermark(first_frame, wm_path)
#         if bbox and confidence > best_confidence:
#             best_bbox = bbox
#             best_confidence = confidence
#             matched_template = wm_path

#     # ✅ If no watermark found → skip processing and return original
#     if not best_bbox:
#         print("[⚠️] No watermark detected — using original video as is.")
#         cap.release()
#         return video_file

#     print(f"[✔] Watermark found ({matched_template}) at {best_bbox} (confidence: {best_confidence:.2f})")
#     cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # rewind

#     # Load replacement logo
#     logo = cv2.imread(MY_WATERMARK_IMAGE, cv2.IMREAD_UNCHANGED)
#     if logo is None:
#         print(f"[✘] Could not load watermark logo image: {MY_WATERMARK_IMAGE}")
#         return video_file  # fall back to original video

#     # Placement calculation
#     top_left, bottom_right = best_bbox
#     x1, y1 = top_left
#     x2, y2 = bottom_right
#     box_w = x2 - x1
#     box_h = y2 - y1

#     scale_factor = 0.85
#     new_w = int(box_w * scale_factor)
#     new_h = int(box_h * scale_factor)
#     resized_logo = cv2.resize(logo, (new_w, new_h))

#     new_x1 = x1 + int((box_w - new_w) * 1.5)
#     new_y1 = y1 + int((box_h - new_h) / 2)
#     new_x2 = new_x1 + new_w
#     new_y2 = new_y1 + new_h

#     # Process all frames
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         clean_frame = remove_with_background_overlay(frame.copy(), best_bbox)

#         overlay = resized_logo.copy()
#         if overlay.shape[2] == 4:
#             alpha = overlay[:, :, 3] / 255.0
#             for c in range(3):
#                 clean_frame[new_y1:new_y2, new_x1:new_x2, c] = (
#                     alpha * overlay[:, :, c] +
#                     (1 - alpha) * clean_frame[new_y1:new_y2, new_x1:new_x2, c]
#                 )
#         else:
#             clean_frame[new_y1:new_y2, new_x1:new_x2] = overlay

#         out.write(clean_frame)

#     cap.release()
#     out.release()

#     print(f"[✅] Final watermarked video saved at: {output_path}")

#     return add_original_audio(video_file, output_path)


#New code------------------------------------------------------------

import cv2
import os
import numpy as np
from moviepy.editor import VideoFileClip
from utils.detect_watermark import detect_watermark
from utils.remove_watermark_overlay import remove_with_background_overlay

# === Configuration ===
OG_WATERMARKS = [
    "OG_watermark/watermark1.png",
]

MY_WATERMARK_IMAGE = "zynicon_logo/Zynicon_social_watermark_logo.png"
OUTPUT_DIR = os.path.join("assets", "WT_zynicon_video")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# === Utility: Reattach Audio ===
def add_original_audio(original_video, processed_video):
    """Reattach original audio to the processed video."""
    try:
        original_clip = VideoFileClip(original_video)
        processed_clip = VideoFileClip(processed_video)

        final = processed_clip.set_audio(original_clip.audio)
        final_output_path = processed_video.replace(".mp4", "_with_audio.mp4")
        final.write_videofile(final_output_path, codec="libx264", audio_codec="aac")

        print(f"[✅] Audio reattached: {final_output_path}")
        return final_output_path
    except Exception as e:
        print(f"[❌ ERROR] Failed to reattach audio: {e}")
        return processed_video


# === Core Function: Replace Watermark ===
def replace_watermark_with_custom_logo(video_file):
    """Detects and replaces an existing watermark with a custom logo."""
    if not os.path.isfile(video_file):
        print(f"[✘] File not found: {video_file}")
        return None

    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"[✘] Failed to open video: {video_file}")
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    video_filename = os.path.splitext(os.path.basename(video_file))[0]
    output_path = os.path.join(OUTPUT_DIR, f"{video_filename}_watermarked.mp4")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # === Step 1: Detect watermark from first frame ===
    ret, first_frame = cap.read()
    if not ret:
        print("[✘] Could not read first frame.")
        cap.release()
        return None

    best_bbox = None
    best_confidence = 0.0
    matched_template = None

    for wm_path in OG_WATERMARKS:
        bbox, confidence = detect_watermark(first_frame, wm_path)
        if bbox and confidence > best_confidence:
            best_bbox = bbox
            best_confidence = confidence
            matched_template = wm_path

    if not best_bbox:
        print("[⚠️] No watermark detected — skipping this video.")
        cap.release()
        return None

    print(f"[✔] Watermark found ({matched_template}) at {best_bbox} (confidence: {best_confidence:.2f})")
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # rewind

    # === Step 2: Expand the detected bounding box (to ensure full cleanup) ===
    top_left, bottom_right = best_bbox
    x1, y1 = top_left
    x2, y2 = bottom_right

    expand_left = 20     # 🔧 increase if you still see residue on the left
    expand_right = 3
    expand_top = 3
    expand_bottom = 3

    x1 = max(x1 - expand_left, 0)
    y1 = max(y1 - expand_top, 0)
    x2 = min(x2 + expand_right, width)
    y2 = min(y2 + expand_bottom, height)

    expanded_bbox = ((x1, y1), (x2, y2))

    # === Step 3: Load replacement logo ===
    logo = cv2.imread(MY_WATERMARK_IMAGE, cv2.IMREAD_UNCHANGED)
    if logo is None:
        print(f"[✘] Could not load watermark logo image: {MY_WATERMARK_IMAGE}")
        cap.release()
        return None

    box_w = x2 - x1
    box_h = y2 - y1

    scale_factor = 0.85  # adjust as needed
    new_w = int(box_w * scale_factor)
    new_h = int(box_h * scale_factor)
    resized_logo = cv2.resize(logo, (new_w, new_h))

    # === Step 4: Position logo inside expanded box ===
    # Moved slightly left to align perfectly
    new_x1 = x1 + int((box_w - new_w) * 0.0) - 2  # fine-tune horizontally
    new_y1 = y1 + int((box_h - new_h) / 2)
    new_x2 = new_x1 + new_w
    new_y2 = new_y1 + new_h

    # === Step 5: Process all frames ===
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Remove old watermark (expanded area)
        clean_frame = remove_with_background_overlay(frame.copy(), expanded_bbox)

        # Overlay new logo with transparency
        overlay = resized_logo.copy()
        if overlay.shape[2] == 4:  # has alpha channel
            alpha = overlay[:, :, 3] / 255.0
            for c in range(3):
                clean_frame[new_y1:new_y2, new_x1:new_x2, c] = (
                    alpha * overlay[:, :, c] +
                    (1 - alpha) * clean_frame[new_y1:new_y2, new_x1:new_x2, c]
                )
        else:
            clean_frame[new_y1:new_y2, new_x1:new_x2] = overlay

        out.write(clean_frame)

    cap.release()
    out.release()

    print(f"[✅] Final watermarked video saved at: {output_path}")
    return add_original_audio(video_file, output_path)


# === Example run ===
# replace_watermark_with_custom_logo("test.mp4")
