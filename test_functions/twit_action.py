from tweet_it import *
from test_functions.twit_engage import *
import shared_var
from shared_var import *

# 50 requests per 15-minute window per each authenticated user
def like_tweets(oauth, user_id, tweet_list):
  LIKE_API = "https://api.twitter.com/2/users/{}/likes"
  url = LIKE_API.format(user_id)

  for tweet_id in tweet_list:
    payload = {
        "tweet_id": tweet_id
    }

    response = requests.post(url=url, auth=oauth, json=payload)
    if response.status_code != 200:
          raise Exception(f"Liking tweet failed: {response.status_code} {response.text}")
    else:
        print(f"Liked tweet {tweet_id}!")

if __name__ == "__main__":
  oauth = make_oauth(api_key, api_secret, access_token, access_secret)
  # tweet_list = get_home_timeline(oauth, shared_var.user_id)
  # like_tweets(oauth, shared_var.user_id, tweet_list)
  