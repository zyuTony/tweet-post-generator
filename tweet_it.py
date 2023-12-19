import os
import json
import requests
from requests_oauthlib import OAuth1
import shared_var
from shared_var import *

# URLs for Twitter API
POST_TWEET_URL = "https://api.twitter.com/2/tweets"
UPLOAD_MEDIA_URL = "https://upload.twitter.com/1.1/media/upload.json"


# OAuth 1 
def make_oauth(api_key: str, api_secret: str, access_token: str, access_secret: str) -> OAuth1:
    """
    Constructs and returns an OAuth1 object for authentication with the Twitter API.

    Parameters:
    api_key (str): The API key obtained from your Twitter developer account.
    api_secret (str): The API secret key associated with your Twitter developer account.
    access_token (str): The access token that provides Twitter API access.
    access_secret (str): The access token secret for secure API requests.

    Returns:
    OAuth1: An OAuth1 authentication object configured with the provided credentials,
    ready for use in Twitter API requests.
    """
    return OAuth1(api_key, api_secret, access_token, access_secret)

def upload_media(oauth: OAuth1, file_path: str) -> str:
    """
    Uploads media to Twitter and returns its media ID.

    Parameters:
    oauth (OAuth1): The OAuth1 authentication object.
    file_path (str): The local path to the media file to be uploaded.

    Returns:
    str: The media ID string of the uploaded media.
    """
    files = {'media': open(file_path, 'rb')}
    response = requests.post(UPLOAD_MEDIA_URL, auth=oauth, files=files)
    if response.status_code != 200:
        raise Exception(f"Media upload failed: {response.status_code} {response.text}")
    media_id = response.json()['media_id_string']
    return media_id

def tweet_with_media(oauth: OAuth1, text: str, media_id: str, reply_to_id: str=None) -> dict:
    """
    Posts a tweet with media on Twitter.

    Parameters:
    oauth (OAuth1): The OAuth1 authentication object.
    text (str): The text of the tweet.
    media_id (str): The media ID of the media to be included in the tweet.
    reply_to_id (str, optional): The tweet ID to which this tweet is replying.

    Returns:
    dict: The response from the Twitter API as a JSON object.
    """
    if reply_to_id:
        payload = {
            "text": text,
            "media": {
                "media_ids": [media_id]
            },
            "reply": {
                "in_reply_to_tweet_id": reply_to_id
            }}
    else:
        payload = {
            "text": text,
            "media": {
                "media_ids": [media_id]
            }}
    response = requests.post(POST_TWEET_URL, auth=oauth, json=payload) 

    if response.status_code != 201:
        raise Exception(f"Tweet failed: {response.status_code} {response.text}")
    return response.json()

def save_messages(messages: str, file_path: str) -> None:
    """
    Save messages to a file.

    Parameters:
    messages: the text to save as json
    file_path: the path of the saved json file

    Return:
    None   
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(messages, file)

def tweet_it(text: str, img_path: str, reply_to_id: str=None) -> dict:
    """
    Posts a tweet with the specified text and image. Optionally, the tweet can be a reply to an existing tweet.

    Parameters:
    text (str): The text content of the tweet.
    img_path (str): The file path of the image to be uploaded and included in the tweet.
    reply_to_id (str): The ID of an existing tweet to which this tweet is replying. If not replying to a tweet, this can be None.

    Returns:
    dict: The response from the Twitter API as a JSON object, containing details of the posted tweet.
    """
    oauth = make_oauth(api_key, api_secret, access_token, access_secret)
    media_id = upload_media(oauth, img_path)  
    response = tweet_with_media(oauth, text, media_id, reply_to_id)
    
    return response


if __name__ == "__main__":
    tweet_it()