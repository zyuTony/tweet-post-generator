import tweepy
import logging
####################API key##########################
bearer_token = "AAAAAAAAAAAAAAAAAAAAAI6zrQEAAAAA2czZFNpCmk3PkA7PxvJJmgZgw3I%3DMLHxcU57DnkRreygJIYRjjSwYx3J4lWfLKm6e5PDxyqPgVhYUL"
client_id = "UEZWOTBYUFBUMXYzTnpOS1dLWHY6MTpjaQ"
client_secret = "icK0T8UUVbqzMaomh-W-hoAr-ZVqveH9c3AzqIuvQKJ0pSSmCy"
api_key = "FE1Qi2Mh866mpyshjO0A9POAJ"
api_secret = "Fussjmc3OqNX3zjRMpwEKbyDmuWmrem6Ubv7tFxj8BJ5kk32C5"
access_token = "1138631920873484288-brALlkViJgpDrk5b4GMER3ypXkrTaz" 
access_secret = "K0MdWhU1Ca7sCBrQHOX1S5CaldyAv7oSOoQJRcByw4mrB"  
####################API key##########################
import tweepy

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

# def tweet_it(text, img_url=None):
#   # v1 auth and create API
#   auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
#   zyu_api_v1 = tweepy.API(auth)
#   zyu_api_v2 = tweepy.Client(bearer_token=bearer_token, 
#                           consumer_key=api_key, 
#                           consumer_secret=api_secret, 
#                           access_token=access_token, 
#                           access_token_secret=access_secret)

#   try:
#       print(f"Tweeting: {text}")
#       if not img_url:
#         zyu_api_v2.create_tweet(text=text, user_auth=True)
#       else:
#         media = zyu_api_v1.media_upload(filename=img_url)
#         zyu_api_v2.create_tweet(text=text, user_auth=True, media_ids=[media.media_id])
#       print("tweeted succesfully")
#   except Exception as e:
#       print(f"An error occurred while tweeting: {e}")
