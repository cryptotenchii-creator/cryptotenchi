import os
import json
import time
import requests
from dotenv import load_dotenv  
load_dotenv()  

API_KEY = os.getenv("OPENROUTER_API_KEY")
FALLBACK_API_KEY = os.getenv("OPENROUTER_API_KEY2")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
CAPTION_DIR = os.path.join("assets", "LLM_caption")
CONTENT_GENERATION_MODEL = "mistralai/mistral-7b-instruct:free"


def build_instagram_prompt(thumbnail_text):
    return f"""
You are a professional content strategist for Crypto Tenchi — a Crypto and Web 3 media brand.

🎯 TASK:
Act as a professinal Crypto & Web 3 Instagram creator, Generate an Instagram caption based on the thumbnail text below. 
Include factual, publicly available information in your own words.
Keep the caption concise to fit within 300 tokens.

📌 FORMAT:
Title with a Short, clear, plain text (no bold, no markdown)
add a line break
Description of 1-2 short paragraphs summarizing the reel content. Include only professional, relevant emojis. 
add a line break
Add Hashtags #crypto #investment #cryptocurrency #web3 plus 3–5 topic-related trending hashtags.
New line
Insert the video-related keywords in square brackets: [keyword1, keyword2, keyword3, topic1, topic2, topic3]
add a line break
New line
CTA:
Stay Ahead in Finance & Investing!
Follow 👉 (@cryptotenchi) for daily investing updates 

📥 THUMBNAIL TEXT:
{thumbnail_text}

Return only the caption text with proper spacing. 
Do not include markdown, numbered lists, [B-INST], <s> or label tags.
""".strip()


def generate_instagram_caption(thumbnail_text, api_key, model=CONTENT_GENERATION_MODEL, temperature=0.5, max_tokens=300):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Title": "Instagram Caption Generator"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You write trending social media captions."},
            {"role": "user", "content": build_instagram_prompt(thumbnail_text)}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        raise Exception(f"OpenRouter API Error: {response.status_code} - {response.text}")
    
    caption = response.json()["choices"][0]["message"]["content"]

    # Clean unwanted model artifacts and extra spaces
    for unwanted in ["<s>", "</s>", "B-INST:", "[B-INST]",  "<pad>", "</pad>"]:
        caption = caption.replace(unwanted, "")

    # Trim all leading/trailing whitespace, tabs, and invisible characters
    caption = caption.strip().lstrip("\u00A0").lstrip()

    return caption


def get_fallback_caption():
    return (
        "Stay updated with the latest updates in crypto and web 3. 💻📊\n\n"
        "Daily Crypto News, Memes & Market Updates.\n\n"
        "#crypto #news #cryptocurrency #blockchain #web3 \n\n"
        "Keywords: [crypto, web3, blockchain]\n\n"
        "Stay ahead in Crypto!\n"
        "Follow 👉 (@cryptotenchi) for daily tech drops\n\n"
    )


def try_generate_with_retries(thumbnail_text, api_key, retries=3, delay=30):
    for attempt in range(1, retries + 1):
        try:
            print(f"[🔁] Attempt {attempt}/{retries} using {'Fallback API' if api_key == FALLBACK_API_KEY else 'Primary API'}...")
            caption = generate_instagram_caption(thumbnail_text, api_key)

            # ✅ If caption is empty or too short, treat it as a failure
            if not caption or len(caption.strip()) < 10:
                raise ValueError("Received empty or invalid caption.")

            print("[✅] Caption generation successful.")
            return caption

        except Exception as e:
            print(f"[⚠️] Attempt {attempt} failed: {e}")
            if attempt < retries:
                print(f"[⏳] Retrying in {delay} seconds...")
                time.sleep(delay)

    # All retries failed
    return None


def run_caption_generation_pipeline(thumbnail_text: str):
    try:
        if not thumbnail_text.strip():
            print("[ℹ️] No thumbnail text, using transcript only.")
            thumbnail_text = ""

        # Try with Primary API Key
        caption = try_generate_with_retries(thumbnail_text, API_KEY)
        if caption:
            return caption

        # Try with Fallback API Key
        print("[🔁] Switching to fallback API key...")
        caption = try_generate_with_retries(thumbnail_text, FALLBACK_API_KEY)
        if caption:
            return caption

        # Both failed → use hardcoded fallback
        print("[❌] All attempts failed. Using hardcoded fallback caption.")
        return get_fallback_caption()

    except Exception as e:
        print(f"[❌ ERROR in caption generation pipeline]: {e}")
        return get_fallback_caption()


def save_caption_to_file(caption: str, video_name: str):
    base_name = os.path.splitext(video_name)[0]
    caption_dir = os.path.join("assets", "LLM_caption")
    os.makedirs(caption_dir, exist_ok=True)

    caption_path = os.path.join(caption_dir, f"{base_name}_llm_caption.txt")

    with open(caption_path, 'w', encoding='utf-8') as f:
        f.write(caption)

    print(f"[💾] Caption saved at: {caption_path}")
    return caption_path


if __name__ == "__main__":
    sample_thumbnail = "This iPhone 17 concept thinks the selfie camera"
    caption = run_caption_generation_pipeline(sample_thumbnail)
    print("Generated Caption:\n", caption)
