# import cv2
# import os

# # === Config ===
# input_video = "test.mp4"  # Only change this file name of the video
# output_watermark = "test_case_watermark.png"

# # === Step 1: Read first frame ===
# cap = cv2.VideoCapture(input_video)
# ret, frame = cap.read()
# cap.release()

# if not ret:
#     print("[✘] Failed to read first frame.")
#     exit()

# # === Step 2: Save the full first frame (optional) ===
# cv2.imwrite("first_frame.png", frame)
# print("[📸] Saved full first frame as 'first_frame.png'.")

# # === Step 3: Crop watermark (Ai researches logo) region ===
# frame_h, frame_w = frame.shape[:2]

# # --- Manual crop coordinates (your working values) ---
# x1, y1 = 50, 330   # top-left corner
# x2, y2 = 350, 200  # bottom-right corner

# wm_width = x2 - x1
# wm_height = y2 - y1

# # Crop
# watermark_crop = frame[y1:y2, x1:x2]

# # === Step 4: Save output ===
# cv2.imwrite(output_watermark, watermark_crop)
# print(f"[✔] Cropped logo saved as '{output_watermark}' at size {wm_width}x{wm_height}")


# # import cv2

# # cap = cv2.VideoCapture("test.mp4")
# # ret, frame = cap.read()
# # cap.release()

# # if not ret:
# #     print("[✘] Failed to read video.")
# #     exit()

# # print("[ℹ] Frame shape:", frame.shape)
# # cv2.imwrite("debug_frame.png", frame)
# # print("[📸] Saved as debug_frame.png")

# # # Example crop coordinates — we’ll adjust them after seeing the result
# # x1, y1 = 50, 330
# # x2, y2 = 350, 200

# # # Draw rectangle on a copy
# # debug = frame.copy()
# # cv2.rectangle(debug, (x1, y1), (x2, y2), (0, 0, 255), 2)
# # cv2.imwrite("debug_box.png", debug)
# # print("[🟥] Saved 'debug_box.png' with red rectangle")

import cv2
import os

# === Config ===
input_video = "test.mp4"  # Change only the video file name
output_watermark = "test_case_watermark.png"

# === Step 1: Read first frame ===
cap = cv2.VideoCapture(input_video)
ret, frame = cap.read()
cap.release()

if not ret or frame is None:
    print("[✘] Failed to read first frame.")
    exit()

frame_h, frame_w = frame.shape[:2]
print(f"[ℹ] Frame size: {frame_w}x{frame_h}")

# === Step 2: Save the full first frame (optional) ===
cv2.imwrite("first_frame.png", frame)
print("[📸] Saved full first frame as 'first_frame.png'.")

# === Step 3: Define and normalize crop coordinates ===
# These are your working values (may appear reversed)
x1, y1 = 250, 880
x2, y2 = 510,970

# Ensure coordinates are always in top-left → bottom-right order
x1, x2 = sorted([x1, x2])
y1, y2 = sorted([y1, y2])

wm_width = x2 - x1
wm_height = y2 - y1

# === Step 4: Crop the region ===
watermark_crop = frame[y1:y2, x1:x2]

if watermark_crop.size == 0:
    print("[✘] Crop region is empty. Check coordinates.")
    print(f"    Frame size: {frame_w}x{frame_h}, crop: x[{x1}:{x2}], y[{y1}:{y2}]")
    exit()

# === Step 5: Save the cropped watermark ===
cv2.imwrite(output_watermark, watermark_crop)
print(f"[✔] Cropped logo saved as '{output_watermark}' ({wm_width}x{wm_height}).")

# === Step 6: Debug visualization ===
debug = frame.copy()
cv2.rectangle(debug, (x1, y1), (x2, y2), (0, 0, 255), 2)
cv2.imwrite("debug_box.png", debug)
print("[🟥] Saved 'debug_box.png' with red rectangle overlay.")
