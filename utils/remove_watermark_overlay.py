import cv2
import numpy as np

def remove_with_background_overlay(frame, bbox):
    top_left, bottom_right = bbox
    x1, y1 = top_left
    x2, y2 = bottom_right

    pad = 10
    sample_area = frame[max(0, y1 - pad):max(0, y1), x1:x2]
    if sample_area.size == 0:
        color = (0, 0, 0)
    else:
        avg_color = np.mean(sample_area, axis=(0, 1))
        color = tuple(map(int, avg_color))

    cv2.rectangle(frame, top_left, bottom_right, color, thickness=-1)
    return frame
