import requests
import os 

token = os.getenv("EXTENDED_ACCESS_TOKEN")

url = f"https://graph.facebook.com/debug_token?input_token={token}&access_token={token}"
res = requests.get(url)
print(res.json())