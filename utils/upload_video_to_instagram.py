import requests
import time
import os
from datetime import datetime
from moviepy.editor import VideoFileClip
from PIL import Image

INSTAGRAM_PAGE_POSTS_ACCESS_ID = os.getenv("INSTAGRAM_PAGE_POSTS_ACCESS_ID")
INSTAGRAM_USER_ACCESS_DATA_ID = os.getenv("INSTAGRAM_USER_ACCESS_DATA_ID")
EXTENDED_ACCESS_TOKEN = os.getenv("EXTENDED_ACCESS_TOKEN")

GRAPH_API_VERSION = 'v22.0'

def get_account_info():
    url = f"https://graph.facebook.com/{INSTAGRAM_PAGE_POSTS_ACCESS_ID}?fields=id,username,name&access_token={EXTENDED_ACCESS_TOKEN}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('name'), data.get('id')
    else:
        print(f'[❌ ERROR] Account info fetch failed: {response.json()}')
        return None, None


def upload_reel_on_insta(video_url, caption):
    print(f"🕒 publishing immediately.")
    
    _, account_id = get_account_info()
    if not account_id:
        print("❌ Failed to get account info")
        return False

    url = f'https://graph.facebook.com/{GRAPH_API_VERSION}/{INSTAGRAM_USER_ACCESS_DATA_ID}/media'
    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": EXTENDED_ACCESS_TOKEN
    }

    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print('❌ Failed to create container:', response.json())
        return False
        
    container_id = response.json().get('id')
    print(f"✅ Container created with ID: {container_id}")
    
    container_url = f'https://graph.facebook.com/{GRAPH_API_VERSION}/{container_id}'
    params = {'fields': 'status_code', 'access_token': EXTENDED_ACCESS_TOKEN}
    
    is_ready = False
    for attempt in range(20):
        response = requests.get(container_url, params=params)
        if response.status_code == 200:
            status = response.json().get('status_code')
            print(f"🔄 Container status check {attempt+1}: {status}")
            
            if status == 'FINISHED':
                print("✅ Container processing complete")
                is_ready = True
                break
            elif status == 'ERROR':
                print("❌ Container processing failed")
                return False
        time.sleep(5)
    
    if not is_ready:
        print("❌ Container never reached FINISHED state")
        return False
    
    publish_url = f'https://graph.facebook.com/{GRAPH_API_VERSION}/{INSTAGRAM_USER_ACCESS_DATA_ID}/media_publish'
    publish_payload = {
        'creation_id': container_id,
        'access_token': EXTENDED_ACCESS_TOKEN
    }

    print("🔄 Sending publishing request immediately...")
    response = requests.post(publish_url, data=publish_payload)
    result = response.json()

    if response.status_code == 200:
        print("✅ Reel published immediately")
        try:
            media_id = result.get('id')
            media_url = f'https://graph.facebook.com/{GRAPH_API_VERSION}/{media_id}'
            media_params = {'fields': 'id,permalink', 'access_token': EXTENDED_ACCESS_TOKEN}
            media_response = requests.get(media_url, params=media_params)
            media_data = media_response.json()
            instagrm_reel_link = media_data.get("permalink")
            print(f"🔍 Published media info: {media_data}")
        except Exception as e:
            print(f"⚠️ Error getting media details: {e}")
        return instagrm_reel_link
    else:
        print(f"❌ Publication failed: {result}")
        return False


def run_instagram_upload_pipeline(video_url, caption):
    print("🚀 Starting Instagram upload pipeline...")
    try:
        success = upload_reel_on_insta(
            video_url=video_url,
            caption=caption
        )

        if success:
            print("🎉 Reel uploaded to Instagram.")
        else:
            print("❌ Instagram upload pipeline failed.")
        return success

    except Exception as e:
        print(f"[❌ EXCEPTION] Upload pipeline failed: {e}")
        return False
