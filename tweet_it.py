import os
import json
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
 
# Get API key
load_dotenv()
bearer_token = os.getenv('bearer_token') # to auth you as an developer and gain access to public info
client_id = os.getenv('twit_client_id')
client_secret = os.getenv('twit_client_secret')

api_key = os.getenv('twit_api_key')
api_secret = os.getenv('twit_api_secret')
access_token = os.getenv('twit_access_token') 
access_secret = os.getenv('twit_access_secret')

# URLs for Twitter API
POST_TWEET_URL = "https://api.twitter.com/2/tweets"
UPLOAD_MEDIA_URL = "https://upload.twitter.com/1.1/media/upload.json"

def make_oauth(api_key, api_secret, access_token, access_secret):
    return OAuth1(api_key, api_secret, access_token, access_secret)

def upload_media(oauth, file_path):
    files = {'media': open(file_path, 'rb')}
    response = requests.post(UPLOAD_MEDIA_URL, auth=oauth, files=files)
    if response.status_code != 200:
        raise Exception(f"Media upload failed: {response.status_code} {response.text}")
    media_id = response.json()['media_id_string']
    return media_id

def tweet_with_media(oauth, text, media_id):
    payload = {
        "text": text,
        "media": {
            "media_ids": [media_id]
        }
    }
    response = requests.post(POST_TWEET_URL, auth=oauth, json=payload)
    if response.status_code != 201:
        raise Exception(f"Tweet failed: {response.status_code} {response.text}")
    return response.json()

def save_messages(messages, file_path):
    """Save messages to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(messages, file)

def tweet_it(text, img_path):
    oauth = make_oauth(api_key, api_secret, access_token, access_secret)
    media_id = upload_media(oauth, img_path)  
    tweet_response = tweet_with_media(oauth, text, media_id)
    print(tweet_response)


if __name__ == "__main__":
    tweet_it()