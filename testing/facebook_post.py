import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get values from .env
EXTENDED_ACCESS_TOKEN = "EAAOlmZCARVLABPFHFw3dsQMRWUlNzZBtW7DPTUgllrnqUfLZCZAFSofCNzFjUFiDnFSZC49xzBARmwbZCWd1bi2ZCr2CBCvflYZC27sQG7rkuLTaZBcQuha0Ek8SnRoXXGK7WAbiNgKsYkMNxm8DscZBtYu31JC5ZB2eHdMyfq7SqZCGHaEWSFWT4W7tNuGzLgqjTgBsuCuCzLQb81CQipkPTW1tR333YOzdLWhFC9Sk"
INSTAGRAM_PAGE_POSTS_ACCESS_ID = os.getenv("INSTAGRAM_PAGE_POSTS_ACCESS_ID")  # Replace with your actual Facebook Page ID
GRAPH_API_VERSION = 'v22.0'

# Post content
message = "Hello, this is an automated post using the Facebook Graph API via Python! 🚀"

# Facebook Graph API endpoint to post to page feed
post_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{INSTAGRAM_PAGE_POSTS_ACCESS_ID}/feed"
# media_url = f'https://graph.facebook.com/{INSTAGRAM_PAGE_POSTS_ACCESS_ID}?&fields=media&access_token={EXTENDED_ACCESS_TOKEN}'

# Payload
payload = {
    "message": message,
    "access_token": EXTENDED_ACCESS_TOKEN
}

# Make the POST request
response = requests.post(post_url, data=payload)

# Handle response
if response.status_code == 200:
    print("✅ Post successfully published!")
    print("📌 Post ID:", response.json().get("id"))
else:
    print("❌ Failed to publish post.")
    print("🔍 Error:", response.status_code, response.text)
