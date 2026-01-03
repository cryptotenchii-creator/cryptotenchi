import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get credentials from environment
INSTAGRAM_PAGE_POSTS_ACCESS_ID = os.getenv("INSTAGRAM_PAGE_POSTS_ACCESS_ID")
INSTAGRAM_USER_ACCESS_DATA_ID = os.getenv("INSTAGRAM_USER_ACCESS_DATA_ID")
EXTENDED_ACCESS_TOKEN = os.getenv("EXTENDED_ACCESS_TOKEN")


# Make a request to check if the Facebook page is linked to an Instagram Business Account
url = f"https://graph.facebook.com/{INSTAGRAM_PAGE_POSTS_ACCESS_ID}?&fields=id,username,name&access_token={EXTENDED_ACCESS_TOKEN}"

media_url = f'https://graph.facebook.com/{INSTAGRAM_PAGE_POSTS_ACCESS_ID}?&fields=media&access_token={EXTENDED_ACCESS_TOKEN}'

response = requests.get(url)
media_response = requests.get(media_url)

# Check if the page has an Instagram business account linked
data = response.json()

instagram_business_account_id = data.get('id')
print(f"Instagram Business Account is linked to this page. Instagram ID: {instagram_business_account_id}")

if response.status_code == 200:
    data = response.json()
    name = data.get('username')
    account_id = data.get('id')
    name =data.get('name')
    print(f'Instagram Account Info: {name}, ID: {account_id}, name: {name}')
else:
    print(f'Error fetching account info: {response.json()}')
    