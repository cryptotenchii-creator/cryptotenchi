import os
import pytesseract
from PIL import Image, UnidentifiedImageError
from datetime import datetime
import re
import unicodedata
import platform


# ✅ Set correct Tesseract path based on OS
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

THUMBNAIL_DIR = os.path.join("assets", "clean_video_thumbnail")
OUTPUT_DIR = os.path.join("assets", "clean_thubnail_text")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_ocr_text(text):
    text = unicodedata.normalize("NFKC", text)
    replacements = {
        "|": "I", "‘": "'", "’": "'", "“": '"', "”": '"',
        "`": "'", "•": "-", "—": "-", "–": "-",
        "ﬁ": "fi", "ﬂ": "fl"
    }
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    text = re.sub(
        r"\b(can|don|won|doesn|didn|hasn|haven|isn|wasn|aren|ain|wouldn|shouldn|couldn|mightn|mustn|needn)[’']\b",
        r"\1't", text, flags=re.IGNORECASE
    )
    text = re.sub(r"\b(can|won|don)'tt\b", r"\1't", text, flags=re.IGNORECASE)
    text = re.sub(r"(?<!\w)[\\/|]+(?!\w)", " ", text)
    text = re.sub(r"[\n\r\t]+", " ", text)
    text = re.sub(r"\b(?!I\b|a\b)[a-zA-Z]\b", "", text)
    text = re.sub(r"\b[A-Z]{2,4}\b(?=\s*$)", "", text)
    return re.sub(r"\s{2,}", " ", text).strip()

def extract_text_from_image(image_path):
    try:
        with Image.open(image_path) as img:
            raw_text = pytesseract.image_to_string(img, lang='eng')
            return clean_ocr_text(raw_text)
    except UnidentifiedImageError:
        print(f"[❌ ERROR] Unrecognized or corrupt image file: {image_path}")
    except Exception as e:
        print(f"[❌ ERROR] Failed to OCR {image_path}: {e}")
    return None


def extract_text_from_specific_thumbnail(filename):
    text = extract_text_from_image(filename)

    if text:
        base_file = os.path.basename(filename)
        output_name = f"{base_file.split('_')[0]}_text_from_thumbnail.txt"
        output_path = os.path.join(OUTPUT_DIR, output_name)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"[✅] Saved: {output_name}")
        return text

    print(f"[❌] No text extracted from: {filename}")
    return ""


def run_thumbnail_ocr_pipeline(image_filename):
    return extract_text_from_specific_thumbnail(image_filename)
