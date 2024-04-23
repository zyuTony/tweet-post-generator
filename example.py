import tweepy
import logging

from dotenv import load_dotenv
import os 

load_dotenv()
bearer_token = os.getenv('bearer_token')
client_id = os.getenv('twit_client_id')
client_secret = os.getenv('twit_client_secret')
api_key = os.getenv('twit_api_key')
api_secret = os.getenv('twit_api_secret')
access_token = os.getenv('twit_access_token')
access_secret = os.getenv('twit_access_secret')

# v1 auth and create API
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
zyu_api_v1 = tweepy.API(auth)

# V2 API
zyu_api_v2 = tweepy.Client(bearer_token=bearer_token, 
                        consumer_key=api_key, 
                        consumer_secret=api_secret, 
                        access_token=access_token, 
                        access_token_secret=access_secret)


media_paths = ["./imgs/pepe.webp", "./imgs/pepe_2.webp"]
media_ids = []
for i, path in enumerate(media_paths):
  media = zyu_api_v1.media_upload(filename=path)
  media_ids.append(media.media_id)

for i, path in enumerate(media_ids):
  media_id = media_ids[i]
  zyu_api_v2.create_tweet(
    text=f"automated tweet {i} with pictures!!",
    user_auth=True,
    media_ids=[media_id]
  )

