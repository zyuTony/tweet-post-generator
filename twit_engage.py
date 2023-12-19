"""
https://www.exampleapi.com/data?userId=123&showDetails=true
1. data is the Path parameters - directly alter URL
like api.twitter.com/2/users/by/username/:username
you need to turn it to 
     api.twitter.com/2/users/by/username/DHpoon

2. after ? is the Query Parameters, connected by & - use params= to change

3. Body doesn't exist in URL - use json= to add

4. header doesn't exist in URL - use header= to add

5. authorization - use auth= to add
"""

from tweet_it import *
import shared_var
from shared_var import *
 
def id_lookup(oauth: OAuth1, user_name: str) -> str:
  """
  Look up a user's id with username
  """
  LOOKUP_API = "https://api.twitter.com/2/users/by/username/{}"
  url = LOOKUP_API.format(user_name)

  response = requests.get(url=url, auth=oauth)
  if response.status_code != 200:
        raise Exception(f"Media upload failed: {response.status_code} {response.text}")
  return response.json()['data']['id']

def get_user_tweet_timeline(oauth: OAuth1, user_id: str) -> list:
  """
  Return a user's home timeline in reverse chronological order.
  Parameters: 
  user_id:
  Returns:
  List of home timeline tweet
  """
  USER_TIMELINE_API = "https://api.twitter.com/2/users/{}/tweets"
  max_results = 5
  url = USER_TIMELINE_API.format(user_id)
  payload = {
     "max_results": max_results
  }

  response = requests.get(url=url, auth=oauth, params=payload)
  if response.status_code != 200:
        raise Exception(f"timeline retrieval failed: {response.status_code} {response.text}")
  
  return [item["id"] for item in response.json()["data"]]


def get_home_timeline(oauth: OAuth1, user_id: str) -> list:
  """
  Return a user's home timeline in reverse chronological order.
  Parameters: 
  user_id:
  Returns:
  List of home timeline tweet
  """
  HOME_TIMELINE_API = "https://api.twitter.com/2/users/{}/timelines/reverse_chronological"

  max_results = 5
  url = HOME_TIMELINE_API.format(user_id)
  payload = {
     "max_results": max_results
  }

  response = requests.get(url=url, auth=oauth, params=payload)
  if response.status_code != 200:
        raise Exception(f"timeline retrieval failed: {response.status_code} {response.text}")
  
  return [item["id"] for item in response.json()["data"]]

# update user_id
if __name__ == "__main__":
  oauth = make_oauth(api_key, api_secret, access_token, access_secret)
  shared_var.user_id = id_lookup(oauth=oauth, user_name="DHpoon")


