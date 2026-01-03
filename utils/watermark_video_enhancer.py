import os
import cv2
import subprocess
from moviepy.editor import ImageSequenceClip


TARGET_RESOLUTION = (1080, 1920)  # Instagram Reels: Width x Height
OUTPUT_DIR = os.path.join("assets", "FINAL_upload_video")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def add_original_audio(original_video_path, video_no_audio_path):
    """
    Attaches original audio to processed video using FFmpeg (faster than moviepy).
    """
    output_with_audio = video_no_audio_path.replace(".mp4", "_with_audio.mp4")

    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", video_no_audio_path,
            "-i", original_video_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            output_with_audio
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print(f"[✅] Audio reattached using FFmpeg: {output_with_audio}")
        return output_with_audio

    except subprocess.CalledProcessError:
        print(f"[❌ ERROR] FFmpeg audio merge failed, returning video without audio.")
        return video_no_audio_path


def enhance_video_quality(video_file_path):
    """
    Upscales video (if needed) and re-encodes with better quality.
    """
    cap = cv2.VideoCapture(video_file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    resize_required = height < 1920

    print(f"[ℹ️] Loaded: {video_file_path}")
    print(f"[ℹ️] FPS: {fps}, Resolution: {width}x{height} (Resize Needed: {resize_required})")

    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if resize_required:
            frame = cv2.resize(frame, TARGET_RESOLUTION, interpolation=cv2.INTER_LINEAR)
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    cap.release()

    base_name = os.path.splitext(os.path.basename(video_file_path))[0]
    temp_video_path = os.path.join(OUTPUT_DIR, f"{base_name}_video_no_audio.mp4")

    # Write high-quality video (no audio)
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(
        temp_video_path,
        codec="libx264",
        bitrate="6000k",
        audio=False,
        threads=1,
        preset="medium",
        ffmpeg_params=["-pix_fmt", "yuv420p", "-crf", "20"],
        progress_bar=False,
        verbose=False
    )

    print(f"[✔] Processed video saved at: {temp_video_path}")
    return add_original_audio(video_file_path, temp_video_path)
