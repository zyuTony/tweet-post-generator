import tweepy
import logging


bearer_token = "AAAAAAAAAAAAAAAAAAAAAI6zrQEAAAAA2czZFNpCmk3PkA7PxvJJmgZgw3I%3DMLHxcU57DnkRreygJIYRjjSwYx3J4lWfLKm6e5PDxyqPgVhYUL"
client_id = "UEZWOTBYUFBUMXYzTnpOS1dLWHY6MTpjaQ"
client_secret = "icK0T8UUVbqzMaomh-W-hoAr-ZVqveH9c3AzqIuvQKJ0pSSmCy"
api_key = "FE1Qi2Mh866mpyshjO0A9POAJ"
api_secret = "Fussjmc3OqNX3zjRMpwEKbyDmuWmrem6Ubv7tFxj8BJ5kk32C5"
access_token = "1138631920873484288-brALlkViJgpDrk5b4GMER3ypXkrTaz" 
access_secret = "K0MdWhU1Ca7sCBrQHOX1S5CaldyAv7oSOoQJRcByw4mrB"  

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

