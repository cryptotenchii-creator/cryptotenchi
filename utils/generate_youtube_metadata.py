import os
import json
import requests

from utils.google_sheets_tracker import fetch_first_unprocessed_row

API_KEY = os.getenv("OPENROUTER_API_KEY2")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
CONTENT_GENERATION_MODEL = "mistralai/mistral-7b-instruct:free"

def build_youtube_prompt(thumbnail_text):
    return f"""
You are a YouTube Shorts strategist for Crypto Tenchi — a fast-paced brand posting about crypto, blockchain and web3 related.

🎯 TASK:
Write metadata for a YouTube Short based **only** on the thumbnail text.

📌 Follow this approach:
- Use the **thumbnail text** to write a short, paraphrased title in simple English
- Do not add new meaning or topics — just simplify and clarify what’s already there
- Match the tone with the video’s likely context (e.g. surprising, insightful, useful)

📐 OUTPUT FORMAT:

Title: (Max 100 characters)
- Rephrase the thumbnail using clear, simple language
- Keep the meaning the same
- Add "#Shorts" at the end

Description:
- 1–2 sentence summary of what the short is about
- Use 2–3 emojis that match tone
- Add fixed hashtags: #ai #technology #technews
- Add 3 trending hashtags based on thumbnail topic (short, lowercase, no duplicates)
- Add below lines in description compulsory starting with new line:
    ↗️ Subscribe @Cryptotenchi for more content  

Tags:
- 6 keyword-based tags (comma-separated, no hashtags)
- Should reflect the actual topic and keywords in the video

⚠️ RULES:
- No clickbait or made-up headlines
- Don’t assume it’s a tutorial or tool unless it says so
- No markdown or explanation
- Never change the original meaning — just simplify it

📥 THUMBNAIL TEXT:
{thumbnail_text}

Respond ONLY:
---
Title: ...
Description: ...
Tags: ...
---
""".strip()


def parse_llm_response(text):
    lines = text.strip().splitlines()
    title, description, tags = "", "", ""

    for line in lines:
        if line.lower().startswith("title:"):
            title = line.split(":", 1)[1].strip()
        elif line.lower().startswith("description:"):
            description = line.split(":", 1)[1].strip()
        elif line.lower().startswith("tags:"):
            tags = line.split(":", 1)[1].strip()

    return title, description, tags

def get_youtube_fallback_metadata(instagram_caption=None):
    fallback_title = (
        instagram_caption.split("\n\n")[1][:100] + " #Shorts"
        if instagram_caption else "↗️ Subscribe @Cryptotenchi for more content #Shorts"
    )
    fallback_description = (
        instagram_caption.split("\n\n")[1]
        if instagram_caption else "Follow us, for more such crypto, blockchain news & web3!"
    )
    fallback_tags = "shorts, crypto, trending, cryptocurrency, blockchain, web3"

    return fallback_title, fallback_description, fallback_tags


def generate_youtube_metadata(thumbnail_text, model=CONTENT_GENERATION_MODEL, temperature=0.6, max_tokens=300):
    if not API_KEY:
        raise ValueError("❌ OPENROUTER_API_KEY2 is not set in environment.")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "YouTube Metadata Generator"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You write high-performance metadata for YouTube Shorts videos."},
            {"role": "user", "content": build_youtube_prompt(thumbnail_text)}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise Exception(f"OpenRouter API Error: {response.status_code} - {response.text}")

    raw = response.json()["choices"][0]["message"]["content"]
    return parse_llm_response(raw)

def save_youtube_metadata_to_file(title: str, description: str, tags: str, video_name: str):
    base_name = os.path.splitext(video_name)[0]
    out_dir = os.path.join("assets", "LLM_caption")
    os.makedirs(out_dir, exist_ok=True)

    metadata_path = os.path.join(out_dir, f"{base_name}_youtube_metadata.txt")
    with open(metadata_path, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n")
        f.write(f"Description: {description}\n")
        f.write(f"Tags: {tags}\n")

    print(f"[💾] YouTube metadata saved to: {metadata_path}")
    return metadata_path

def run_youtube_metadata_generation(thumbnail_text, fallback_caption=None):
    try:

        title, desc, tags = generate_youtube_metadata(thumbnail_text)
        if not title or not desc or not tags:
            print("[⚠️] LLM response incomplete. Using fallback metadata.")
            return get_youtube_fallback_metadata(fallback_caption)

        print("[✅] YouTube metadata generated.")
        return title, desc, tags

    except Exception as e:
        print(f"[❌ ERROR] Metadata generation failed: {e}")
        return get_youtube_fallback_metadata(fallback_caption)
