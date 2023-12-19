from dotenv import load_dotenv
import os
load_dotenv()

# Auth you as an developer and gain access to public info
bearer_token = os.getenv('bearer_token') 

client_id = os.getenv('twit_client_id')
client_secret = os.getenv('twit_client_secret')


# for Oauth 1------------
# Representing your app - the developer account
api_key = os.getenv('twit_api_key')
api_secret = os.getenv('twit_api_secret')

# Representing the user - on behald of the user making the request
access_token = os.getenv('twit_access_token') 
access_secret = os.getenv('twit_access_secret')

# my twitter id 
user_id = "1138631920873484288"