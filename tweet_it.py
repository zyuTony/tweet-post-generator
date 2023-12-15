import tweepy
import logging
from dotenv import load_dotenv
import os 
import tweepy

# Get API key
load_dotenv()
bearer_token = os.getenv('bearer_token') # to auth you as an developer and gain access to public info
client_id = os.getenv('twit_client_id')
client_secret = os.getenv('twit_client_secret')

api_key = os.getenv('twit_api_key')
api_secret = os.getenv('twit_api_secret')
access_token = os.getenv('twit_access_token') 
access_secret = os.getenv('twit_access_secret')
 


def tweet_it(text, img_url=None):
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
    zyu_api_v1 = tweepy.API(auth)
    zyu_api_v2 = tweepy.Client(bearer_token=bearer_token, 
                               consumer_key=api_key, 
                               consumer_secret=api_secret, 
                               access_token=access_token, 
                               access_token_secret=access_secret)

    try:
        # Twitter character limit per tweet
        char_limit = 280

        # Split the text into chunks of 280 characters
        tweets = [text[i:i+char_limit] for i in range(0, len(text), char_limit)]

        # Initialize variables for image and last tweet ID
        media_id = None
        last_tweet_id = None

        # If there's an image URL, upload the image first and get the media ID
        if img_url:
            media = zyu_api_v1.media_upload(filename=img_url)
            media_id = media.media_id

        # Tweet each chunk of text in a thread
        for i, tweet in enumerate(tweets):
            print(f"Tweeting: {tweet}")

            # Attach image only to the last tweet
            if i == len(tweets) - 1 and media_id:
                response = zyu_api_v2.create_tweet(text=tweet, user_auth=True, 
                                                   media_ids=[media_id],
                                                   in_reply_to_tweet_id=last_tweet_id)
            else:
                response = zyu_api_v2.create_tweet(text=tweet, user_auth=True, 
                                                   in_reply_to_tweet_id=last_tweet_id)

            # Update the last tweet ID
            last_tweet_id = response.data['id']
            print("Tweeted successfully")

    except Exception as e:
        print(f"An error occurred while tweeting: {e}")

 