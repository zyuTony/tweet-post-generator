 
import logging
from dotenv import load_dotenv
import os 
import tweepy
import requests
import requests_oauthlib 
# Get API key
load_dotenv()
bearer_token = os.getenv('bearer_token') # to auth you as an developer and gain access to public info
client_id = os.getenv('twit_client_id')
client_secret = os.getenv('twit_client_secret')

api_key = os.getenv('twit_api_key')
api_secret = os.getenv('twit_api_secret')
access_token = os.getenv('twit_access_token') 
access_secret = os.getenv('twit_access_secret')

def create_url():
    return "https://api.twitter.com/2/tweets"    

def make_header(api_key, api_secret, access_token, access_secret):
    # Correctly use OAuth for header
    oauth = requests_oauthlib.OAuth1(api_key, api_secret, access_token, access_secret)
    return oauth

def get_param():
    return {"text":"trying only request lib for tweeting"}

def connect_to_endpoint(url, oauth, params=None):
    response = requests.post(url, auth=oauth, json=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(f"Request Error. {response.status_code} {response.text}")
    return response.json()

def save_messages(messages, file_path):
    """Save messages to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(messages, file)

def main():
    oauth = make_header(api_key, api_secret, access_token, access_secret)
    url = create_url()
    params = get_param()
    json_resp = connect_to_endpoint(url, oauth, params)
    save_messages(json_resp, "./output_request.json")


main()