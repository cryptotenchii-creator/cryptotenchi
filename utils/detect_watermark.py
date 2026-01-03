import cv2

def detect_watermark(frame, watermark_path, threshold=0.35):
    watermark_orig = cv2.imread(watermark_path)
    if watermark_orig is None:
        return None, 0.0

    frame_h, frame_w = frame.shape[:2]
    top_crop = frame[:int(frame_h * 0.5), :]  # Only top 30% of video

    best_match = None
    best_conf = 0.0

    for scale in [0.95, 1.0, 1.05]:
        watermark = cv2.resize(watermark_orig, (0, 0), fx=scale, fy=scale)
        if watermark.shape[0] > top_crop.shape[0] or watermark.shape[1] > top_crop.shape[1]:
            continue

        result = cv2.matchTemplate(top_crop, watermark, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > best_conf:
            best_conf = max_val
            top_left = max_loc
            bottom_right = (
                top_left[0] + watermark.shape[1],
                top_left[1] + watermark.shape[0]
            )
            best_match = (top_left, bottom_right)

    if best_conf >= threshold:
        return best_match, best_conf
    else:
        return None, best_conf
